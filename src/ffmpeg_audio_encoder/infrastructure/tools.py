from __future__ import annotations

import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from ffmpeg_audio_encoder.domain.errors import ToolNotFoundError
from ffmpeg_audio_encoder.domain.models import (
    AppSettings,
    EncoderDescriptor,
    OutputFormat,
    Toolchain,
)

_WINDOWS_CREATE_NO_WINDOW = 0x08000000


def subprocess_creation_flags() -> int:
    """Return flags that keep console tools invisible in a Windows GUI app."""
    return _WINDOWS_CREATE_NO_WINDOW if sys.platform == "win32" else 0


@dataclass(frozen=True, slots=True)
class ToolReport:
    toolchain: Toolchain
    ffmpeg_version: str
    ffprobe_version: str
    encoders: frozenset[str]
    muxers: frozenset[str] = frozenset()
    qaac_version: str | None = None
    fdkaac_version: str | None = None

    @property
    def supports_opus(self) -> bool:
        return "libopus" in self.encoders

    @property
    def supports_flac(self) -> bool:
        return "flac" in self.encoders

    def supports_encoder(self, name: str) -> bool:
        return name in self.encoders

    def supports_muxer(self, output_format: OutputFormat) -> bool:
        return not self.muxers or output_format.ffmpeg_muxer in self.muxers

    def supports_adapter(self, descriptor: EncoderDescriptor) -> bool:
        available_tools = {
            "ffmpeg",
            "ffprobe",
            *({"qaac"} if self.qaac_version else set()),
            *({"fdkaac"} if self.fdkaac_version else set()),
        }
        return (
            all(name in available_tools for name in descriptor.required_tools)
            and all(name in self.encoders for name in descriptor.required_ffmpeg_encoders)
            and (
                not self.muxers
                or all(name in self.muxers for name in descriptor.required_ffmpeg_muxers)
            )
        )


def _resolve_executable(configured: str | None, name: str) -> Path:
    if configured:
        configured_path = Path(configured).expanduser()
        if configured_path.is_file():
            return configured_path.resolve()
    discovered = shutil.which(name)
    if discovered:
        return Path(discovered).resolve()
    detail = f"Configured path {configured!r} is invalid and " if configured else ""
    raise ToolNotFoundError(f"{detail}{name} was not found on PATH")


def _resolve_optional_executable(configured: str | None, *names: str) -> Path | None:
    if configured:
        configured_path = Path(configured).expanduser()
        return configured_path.resolve() if configured_path.is_file() else None
    for name in names:
        discovered = shutil.which(name)
        if discovered:
            return Path(discovered).resolve()
    return None


def locate_toolchain(settings: AppSettings) -> Toolchain:
    return Toolchain(
        ffmpeg=_resolve_executable(settings.ffmpeg_path, "ffmpeg"),
        ffprobe=_resolve_executable(settings.ffprobe_path, "ffprobe"),
        qaac=_resolve_optional_executable(settings.qaac_path, "qaac64", "qaac"),
        fdkaac=_resolve_optional_executable(settings.fdkaac_path, "fdkaac"),
    )


def _run_tool(program: Path, arguments: list[str], *, check: bool = True) -> str:
    try:
        result = subprocess.run(
            [str(program), *arguments],
            check=check,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
            creationflags=subprocess_creation_flags(),
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise ToolNotFoundError(f"Could not run {program.name}: {exc}") from exc
    return (result.stdout or result.stderr).strip()


def inspect_toolchain(toolchain: Toolchain) -> ToolReport:
    ffmpeg_version = _run_tool(toolchain.ffmpeg, ["-version"]).splitlines()[0]
    ffprobe_version = _run_tool(toolchain.ffprobe, ["-version"]).splitlines()[0]
    encoder_text = _run_tool(toolchain.ffmpeg, ["-hide_banner", "-encoders"])
    muxer_text = _run_tool(toolchain.ffmpeg, ["-hide_banner", "-muxers"])
    encoders: set[str] = set()
    for line in encoder_text.splitlines():
        columns = line.split()
        if len(columns) >= 2 and columns[0].startswith("A") and columns[1] != "=":
            encoders.add(columns[1])
    muxers: set[str] = set()
    for line in muxer_text.splitlines():
        columns = line.split()
        if len(columns) >= 2 and "E" in columns[0] and columns[1] != "=":
            muxers.add(columns[1])
    qaac_version = _inspect_optional_tool(toolchain.qaac, ["--check"])
    fdkaac_version = _inspect_optional_tool(toolchain.fdkaac, ["--help"], check=False)
    return ToolReport(
        toolchain,
        ffmpeg_version,
        ffprobe_version,
        frozenset(encoders),
        frozenset(muxers),
        qaac_version,
        fdkaac_version,
    )


def _inspect_optional_tool(
    program: Path | None, arguments: list[str], *, check: bool = True
) -> str | None:
    if program is None:
        return None
    try:
        output = _run_tool(program, arguments, check=check)
    except ToolNotFoundError:
        return None
    return output.splitlines()[0] if output else program.name
