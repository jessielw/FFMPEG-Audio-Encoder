from __future__ import annotations

import json
import math
import struct
import subprocess
import wave
from pathlib import Path

import pytest
from pymediainfo import MediaInfo

from ffmpeg_audio_encoder.application.queue import JobQueueController
from ffmpeg_audio_encoder.domain.errors import AudioEncoderError
from ffmpeg_audio_encoder.domain.models import (
    AppSettings,
    AudioStream,
    Codec,
    CommonAudioOptions,
    EncodingRequest,
    JobState,
    OutputFormat,
)
from ffmpeg_audio_encoder.encoders import default_registry
from ffmpeg_audio_encoder.infrastructure.probe import apply_mediainfo_delays, parse_ffprobe_json
from ffmpeg_audio_encoder.infrastructure.tools import inspect_toolchain, locate_toolchain


def _write_test_wave(path: Path, seconds: float = 0.25) -> None:
    sample_rate = 48000
    samples = int(sample_rate * seconds)
    with wave.open(str(path), "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(sample_rate)
        output.writeframes(
            b"".join(
                struct.pack("<h", int(12000 * math.sin(2 * math.pi * 440 * index / sample_rate)))
                for index in range(samples)
            )
        )


@pytest.fixture(scope="module")
def tool_report():
    try:
        return inspect_toolchain(locate_toolchain(AppSettings()))
    except AudioEncoderError as exc:
        pytest.skip(str(exc))


@pytest.mark.parametrize("delay_ms", [80.0, -80.0])
def test_real_matroska_track_delay_is_reported_with_the_correct_sign(
    tmp_path: Path, tool_report, delay_ms: float
) -> None:
    output = tmp_path / f"delay-{delay_ms:+g}.mkv"
    video_input = ["-f", "lavfi", "-i", "testsrc2=duration=0.25:size=16x16:rate=25"]
    audio_input = ["-f", "lavfi", "-i", "sine=frequency=1000:duration=0.25"]
    inputs = (
        [*video_input, "-itsoffset", "0.08", *audio_input]
        if delay_ms > 0
        else ["-itsoffset", "0.08", *video_input, *audio_input]
    )
    subprocess.run(
        [
            str(tool_report.toolchain.ffmpeg),
            "-v",
            "error",
            "-y",
            *inputs,
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "ffv1",
            "-c:a",
            "pcm_s16le",
            str(output),
        ],
        check=True,
    )
    ffprobe = subprocess.run(
        [
            str(tool_report.toolchain.ffprobe),
            "-v",
            "error",
            "-show_streams",
            "-show_format",
            "-of",
            "json",
            str(output),
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    asset = parse_ffprobe_json(output, json.loads(ffprobe.stdout))
    enriched = apply_mediainfo_delays(asset, MediaInfo.parse(output).to_data())

    assert enriched.detected_delays[0].milliseconds == pytest.approx(delay_ms, abs=1)


@pytest.mark.parametrize("delay_ms", [25.0, -25.0])
@pytest.mark.parametrize(
    ("encoder_id", "codec", "output_format"),
    [
        ("ffmpeg.libopus", Codec.OPUS, OutputFormat.OGG_OPUS),
        ("ffmpeg.flac", Codec.FLAC, OutputFormat.FLAC),
        ("ffmpeg.aac", Codec.AAC, OutputFormat.M4A),
        ("ffmpeg.libmp3lame", Codec.MP3, OutputFormat.MP3),
        ("ffmpeg.ac3", Codec.AC3, OutputFormat.AC3),
        ("ffmpeg.eac3", Codec.EAC3, OutputFormat.EAC3),
        ("ffmpeg.dca", Codec.DTS, OutputFormat.DTS),
        ("ffmpeg.alac", Codec.ALAC, OutputFormat.M4A),
    ],
)
def test_real_qprocess_queue_encode(
    tmp_path: Path,
    qtbot,
    tool_report,
    encoder_id: str,
    codec: Codec,
    output_format: OutputFormat,
    delay_ms: float,
) -> None:
    source = tmp_path / "tone.wav"
    output = tmp_path / f"tone{output_format.suffix}"
    _write_test_wave(source)
    registry = default_registry()
    adapter = registry.get(encoder_id)
    if not tool_report.supports_adapter(adapter.descriptor):
        pytest.skip(f"This FFmpeg build has no {adapter.descriptor.display_name} encoder")
    if not tool_report.supports_muxer(output_format):
        pytest.skip(f"This FFmpeg build has no {output_format.ffmpeg_muxer} muxer")
    request = EncodingRequest(
        source,
        AudioStream(0, 1, "pcm_s16le", 1, "mono", 48000, duration_seconds=0.25),
        encoder_id,
        codec,
        output_format,
        output,
        CommonAudioOptions(channel_layout="stereo", delay_ms=delay_ms),
        encoder_options=adapter.default_options(),
    )
    queue = JobQueueController(registry, tool_report.toolchain)
    job = queue.add(request)
    queue.start()
    qtbot.waitUntil(
        lambda: job.state in {JobState.SUCCEEDED, JobState.FAILED},
        timeout=20_000,
    )
    assert job.state is JobState.SUCCEEDED, job.error
    assert output.is_file() and output.stat().st_size > 0
    probe = subprocess.run(
        [
            str(tool_report.toolchain.ffprobe),
            "-v",
            "error",
            "-show_streams",
            "-of",
            "json",
            str(output),
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    payload = json.loads(probe.stdout)
    assert payload["streams"][0]["codec_name"] == codec.value
    assert payload["streams"][0]["channels"] == 2
