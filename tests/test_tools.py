from __future__ import annotations

import sys
from pathlib import Path

from ffmpeg_audio_encoder.domain.models import AppSettings, OutputFormat, Toolchain
from ffmpeg_audio_encoder.encoders import default_registry
from ffmpeg_audio_encoder.infrastructure import tools
from ffmpeg_audio_encoder.infrastructure.tools import (
    ToolReport,
    inspect_toolchain,
    locate_toolchain,
    prune_deezy_scratch,
    subprocess_creation_flags,
)


def test_tool_processes_are_hidden_on_windows() -> None:
    expected = 0x08000000 if sys.platform == "win32" else 0
    assert subprocess_creation_flags() == expected


def test_capability_report_is_descriptor_driven() -> None:
    report = ToolReport(
        Toolchain(Path("ffmpeg"), Path("ffprobe")),
        "ffmpeg version",
        "ffprobe version",
        frozenset({"aac", "flac"}),
        frozenset({"ipod", "flac"}),
    )
    registry = default_registry()
    assert report.supports_adapter(registry.get("ffmpeg.aac").descriptor)
    assert not report.supports_adapter(registry.get("ffmpeg.libmp3lame").descriptor)
    assert report.supports_muxer(OutputFormat.M4A)
    assert not report.supports_muxer(OutputFormat.MP3)


def test_external_encoder_capability_requires_tool_and_wav_muxer() -> None:
    registry = default_registry()
    toolchain = Toolchain(
        Path("ffmpeg"),
        Path("ffprobe"),
        qaac=Path("qaac64"),
        fdkaac=Path("fdkaac"),
        opusenc=Path("opusenc"),
    )
    report = ToolReport(
        toolchain,
        "ffmpeg version",
        "ffprobe version",
        frozenset({"aac"}),
        frozenset({"wav"}),
        "qaac 2.82",
        None,
        "opusenc opus-tools 0.2",
    )
    assert report.supports_adapter(registry.get("qaac.aac").descriptor)
    assert not report.supports_adapter(registry.get("fdkaac.aac").descriptor)
    assert report.supports_adapter(registry.get("opusenc.opus").descriptor)
    assert report.supports_opus


def test_inspection_parses_audio_encoders_and_muxers(monkeypatch) -> None:
    def fake_run_tool(program: Path, arguments: list[str], *, check: bool = True) -> str:
        if program == Path("fdkaac"):
            assert not check
            return "fdkaac 1.0.0\nUsage: fdkaac [options] input_file"
        if program == Path("opusenc"):
            assert arguments == ["--version"]
            return "opusenc opus-tools 0.2"
        if arguments == ["-version"]:
            return "ffmpeg version test"
        if arguments[-1] == "-encoders":
            return " A..... = Audio\n A..... aac AAC\n A....D flac FLAC\n V..... h264 video"
        if arguments[-1] == "-muxers":
            return " E = Muxing supported\n E ipod iPod\n E mp3 MP3\n D matroska Matroska"
        raise AssertionError(arguments)

    monkeypatch.setattr(tools, "_run_tool", fake_run_tool)
    report = inspect_toolchain(
        Toolchain(
            Path("ffmpeg"),
            Path("ffprobe"),
            fdkaac=Path("fdkaac"),
            opusenc=Path("opusenc"),
        )
    )
    assert report.encoders == frozenset({"aac", "flac"})
    assert report.muxers == frozenset({"ipod", "mp3"})
    assert report.fdkaac_version == "fdkaac 1.0.0"
    assert report.opusenc_version == "opusenc opus-tools 0.2"


def test_deezy_dependencies_are_discovered_beside_configured_executable(
    tmp_path: Path,
    monkeypatch,
) -> None:
    suffix = ".exe" if sys.platform == "win32" else ""
    ffmpeg = tmp_path / f"ffmpeg{suffix}"
    ffprobe = tmp_path / f"ffprobe{suffix}"
    deezy = tmp_path / f"deezy{suffix}"
    dee = tmp_path / "apps" / "dee" / f"dee{suffix}"
    truehdd = tmp_path / "apps" / "truehdd" / f"truehdd{suffix}"
    for executable in (ffmpeg, ffprobe, deezy, dee, truehdd):
        executable.parent.mkdir(parents=True, exist_ok=True)
        executable.touch()

    # DeeZy tools resolve from PATH first, so this has to run with an empty PATH to
    # prove the configured executable and its adjacent apps folder are the fallback.
    monkeypatch.setattr(tools.shutil, "which", lambda _name: None)

    toolchain = locate_toolchain(
        AppSettings(
            ffmpeg_path=str(ffmpeg),
            ffprobe_path=str(ffprobe),
            deezy_path=str(deezy),
        )
    )

    assert toolchain.deezy == deezy.resolve()
    assert toolchain.dee == dee.resolve()
    assert toolchain.truehdd == truehdd.resolve()


def test_deezy_capabilities_require_truehdd_only_for_immersive_modes() -> None:
    registry = default_registry()
    report = ToolReport(
        Toolchain(Path("ffmpeg"), Path("ffprobe"), deezy=Path("deezy"), dee=Path("dee")),
        "ffmpeg version",
        "ffprobe version",
        frozenset(),
        deezy_version="DeeZy 1.3.10",
        dee_version="dee.exe, Version 5.2.1",
    )
    assert report.supports_adapter(registry.get("deezy.dd").descriptor)
    assert report.supports_adapter(registry.get("deezy.ddp_bluray").descriptor)
    assert not report.supports_adapter(registry.get("deezy.atmos").descriptor)
    assert not report.supports_adapter(registry.get("deezy.ac4").descriptor)


def test_prune_deezy_scratch_clears_intermediates_from_a_killed_run(tmp_path: Path) -> None:
    scratch = tmp_path / "deezy-temp"
    leftover = scratch / "movie_deezy"
    leftover.mkdir(parents=True)
    (leftover / "atmos_meta.atmos.audio").write_bytes(b"partial decode")
    (scratch / "stray.caf").write_bytes(b"stray")
    toolchain = Toolchain(Path("ffmpeg"), Path("ffprobe"), deezy_temp_dir=scratch)

    prune_deezy_scratch(toolchain)

    assert scratch.is_dir()
    assert list(scratch.iterdir()) == []


def test_prune_deezy_scratch_tolerates_a_missing_directory(tmp_path: Path) -> None:
    prune_deezy_scratch(Toolchain(Path("ffmpeg"), Path("ffprobe")))
    prune_deezy_scratch(
        Toolchain(Path("ffmpeg"), Path("ffprobe"), deezy_temp_dir=tmp_path / "absent")
    )
