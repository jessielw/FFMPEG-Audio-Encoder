from __future__ import annotations

import sys
from pathlib import Path

from ffmpeg_audio_encoder.domain.models import OutputFormat, Toolchain
from ffmpeg_audio_encoder.encoders import default_registry
from ffmpeg_audio_encoder.infrastructure import tools
from ffmpeg_audio_encoder.infrastructure.tools import (
    ToolReport,
    inspect_toolchain,
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


def test_inspection_parses_audio_encoders_and_muxers(monkeypatch) -> None:
    def fake_run_tool(_program: Path, arguments: list[str]) -> str:
        if arguments == ["-version"]:
            return "ffmpeg version test"
        if arguments[-1] == "-encoders":
            return " A..... = Audio\n A..... aac AAC\n A....D flac FLAC\n V..... h264 video"
        if arguments[-1] == "-muxers":
            return " E = Muxing supported\n E ipod iPod\n E mp3 MP3\n D matroska Matroska"
        raise AssertionError(arguments)

    monkeypatch.setattr(tools, "_run_tool", fake_run_tool)
    report = inspect_toolchain(Toolchain(Path("ffmpeg"), Path("ffprobe")))
    assert report.encoders == frozenset({"aac", "flac"})
    assert report.muxers == frozenset({"ipod", "mp3"})
