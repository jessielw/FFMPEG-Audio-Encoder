from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from uuid import uuid4

import pytest

from ffmpeg_audio_encoder.domain.errors import AudioEncoderError
from ffmpeg_audio_encoder.domain.models import (
    AppSettings,
    AudioStream,
    Codec,
    EncodingRequest,
    OutputFormat,
    Toolchain,
)
from ffmpeg_audio_encoder.encoders.external import FdkAacEncoder, QaacEncoder
from ffmpeg_audio_encoder.infrastructure.process import QtProcessRunner
from ffmpeg_audio_encoder.infrastructure.tools import locate_toolchain
from tests.test_integration_ffmpeg import _write_test_wave


def _local_tool(name: str) -> Path | None:
    discovered = shutil.which(name)
    if discovered:
        return Path(discovered)
    root = Path(__file__).resolve().parents[1]
    candidates = {
        "qaac": (root / "Apps" / "qaac" / "qaac64.exe"),
        "fdkaac": (root / "Apps" / "fdkaac" / "fdkaac.exe"),
    }
    candidate = candidates[name]
    return candidate if candidate.is_file() else None


def _toolchain() -> Toolchain:
    qaac = _local_tool("qaac")
    fdkaac = _local_tool("fdkaac")
    try:
        base = locate_toolchain(AppSettings())
    except AudioEncoderError as exc:
        pytest.skip(str(exc))
    return Toolchain(base.ffmpeg, base.ffprobe, qaac, fdkaac)


@pytest.mark.parametrize(
    ("adapter", "tool_attribute"),
    [(QaacEncoder(), "qaac"), (FdkAacEncoder(), "fdkaac")],
)
@pytest.mark.parametrize("output_format", [OutputFormat.M4A, OutputFormat.ADTS_AAC])
def test_external_aac_encoder_produces_probeable_m4a(
    adapter, tool_attribute: str, output_format: OutputFormat, tmp_path: Path
) -> None:
    toolchain = _toolchain()
    if getattr(toolchain, tool_attribute) is None:
        pytest.skip(f"{tool_attribute} is not installed")
    source = tmp_path / "tone.wav"
    output = tmp_path / f"{tool_attribute}{output_format.suffix}"
    _write_test_wave(source)
    request = EncodingRequest(
        source,
        AudioStream(0, 1, "pcm_s16le", 1, "mono", 48000, duration_seconds=0.25),
        adapter.descriptor.id,
        Codec.AAC,
        output_format,
        output,
        encoder_options=adapter.default_options(),
    )
    plan = adapter.build_plan(request, toolchain, output)
    decoder = subprocess.Popen(
        [str(plan.stages[0].program), *plan.stages[0].arguments],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert decoder.stdout is not None
    encoder = subprocess.Popen(
        [str(plan.stages[1].program), *plan.stages[1].arguments],
        stdin=decoder.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    decoder.stdout.close()
    _, encoder_error = encoder.communicate(timeout=20)
    decoder.wait(timeout=20)
    assert decoder.stderr is not None
    decoder_error = decoder.stderr.read()
    assert decoder.returncode == 0, decoder_error.decode(errors="replace")
    assert encoder.returncode == 0, encoder_error.decode(errors="replace")

    codec = subprocess.check_output(
        [
            str(toolchain.ffprobe),
            "-v",
            "error",
            "-select_streams",
            "a:0",
            "-show_entries",
            "stream=codec_name",
            "-of",
            "default=nw=1:nk=1",
            str(output),
        ],
        text=True,
    ).strip()
    assert codec == "aac"


@pytest.mark.parametrize(
    ("adapter", "tool_attribute"),
    [(QaacEncoder(), "qaac"), (FdkAacEncoder(), "fdkaac")],
)
def test_qt_runner_finishes_external_encoder_pipeline(
    adapter, tool_attribute: str, tmp_path: Path, qtbot
) -> None:
    toolchain = _toolchain()
    if getattr(toolchain, tool_attribute) is None:
        pytest.skip(f"{tool_attribute} is not installed")
    source = tmp_path / "long-tone.wav"
    output = tmp_path / f"{tool_attribute}.m4a"
    _write_test_wave(source, seconds=30)
    request = EncodingRequest(
        source,
        AudioStream(0, 1, "pcm_s16le", 1, "mono", 48000, duration_seconds=30),
        adapter.descriptor.id,
        Codec.AAC,
        OutputFormat.M4A,
        output,
        encoder_options=adapter.default_options(),
    )
    plan = adapter.build_plan(request, toolchain, output)
    runner = QtProcessRunner()
    result: list[tuple[str, bool, str]] = []
    runner.finished.connect(lambda job_id, success, error: result.append((job_id, success, error)))
    runner.start(uuid4(), plan)
    try:
        qtbot.waitUntil(lambda: not runner.is_running, timeout=20_000)
    finally:
        if runner.is_running:
            runner.cancel()
            qtbot.waitUntil(lambda: not runner.is_running, timeout=5_000)

    assert result and result[0][1], result
    assert output.stat().st_size > 0
