from __future__ import annotations

import shutil
import subprocess
import sys
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path

from platformdirs import user_cache_path

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
    opusenc_version: str | None = None
    deezy_version: str | None = None
    dee_version: str | None = None
    truehdd_version: str | None = None

    @property
    def supports_opus(self) -> bool:
        return "libopus" in self.encoders or self.opusenc_version is not None

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
            *({"opusenc"} if self.opusenc_version else set()),
            *({"deezy"} if self.deezy_version else set()),
            *({"dee"} if self.dee_version else set()),
            *({"truehdd"} if self.truehdd_version else set()),
        }
        return (
            all(name in available_tools for name in descriptor.required_tools)
            and all(name in self.encoders for name in descriptor.required_ffmpeg_encoders)
            and (
                not self.muxers
                or all(name in self.muxers for name in descriptor.required_ffmpeg_muxers)
            )
        )


def _configured_file(configured: str | None) -> Path | None:
    if not configured:
        return None
    configured_path = Path(configured).expanduser()
    return configured_path.resolve() if configured_path.is_file() else None


def _on_path(*names: str) -> Path | None:
    for name in names:
        discovered = shutil.which(name)
        if discovered:
            return Path(discovered).resolve()
    return None


def _resolve_executable(configured: str | None, name: str) -> Path:
    resolved = _configured_file(configured) or _on_path(name)
    if resolved is not None:
        return resolved
    detail = f"Configured path {configured!r} is invalid and " if configured else ""
    raise ToolNotFoundError(f"{detail}{name} was not found on PATH")


def _resolve_optional_executable(configured: str | None, *names: str) -> Path | None:
    if configured:
        return _configured_file(configured)
    return _on_path(*names)


def _resolve_deezy_tool(configured: str | None, *names: str) -> Path | None:
    """Locate a DeeZy toolchain member: PATH first, then the configured override."""
    return _on_path(*names) or _configured_file(configured)


def _resolve_deezy_dependency(
    configured: str | None,
    deezy: Path | None,
    directory_name: str,
    *names: str,
) -> Path | None:
    """Locate a tool DeeZy drives: PATH, then DeeZy's bundled ``apps`` layout, then
    the configured override. ``truehdd`` and ``dee`` normally ship beside DeeZy
    rather than on PATH."""
    discovered = _on_path(*names)
    if discovered is not None:
        return discovered
    if deezy is not None:
        for name in names:
            adjacent = deezy.parent / "apps" / directory_name / name
            if adjacent.is_file():
                return adjacent.resolve()
    return _configured_file(configured)


def locate_toolchain(settings: AppSettings) -> Toolchain:
    deezy = _resolve_deezy_tool(settings.deezy_path, "deezy")
    executable_suffix = ".exe" if sys.platform == "win32" else ""
    return Toolchain(
        ffmpeg=_resolve_executable(settings.ffmpeg_path, "ffmpeg"),
        ffprobe=_resolve_executable(settings.ffprobe_path, "ffprobe"),
        qaac=_resolve_optional_executable(settings.qaac_path, "qaac64", "qaac"),
        fdkaac=_resolve_optional_executable(settings.fdkaac_path, "fdkaac"),
        opusenc=_resolve_optional_executable(settings.opusenc_path, "opusenc"),
        deezy=deezy,
        dee=_resolve_deezy_dependency(
            settings.dee_path,
            deezy,
            "dee",
            f"dee{executable_suffix}",
        ),
        truehdd=_resolve_deezy_dependency(
            settings.truehdd_path,
            deezy,
            "truehdd",
            f"truehdd{executable_suffix}",
        ),
        deezy_work_dir=user_cache_path("FFmpegAudioEncoder", appauthor=False) / "deezy-work",
        deezy_temp_dir=user_cache_path("FFmpegAudioEncoder", appauthor=False) / "deezy-temp",
    )


def prune_deezy_scratch(toolchain: Toolchain) -> None:
    """Drop DeeZy intermediates left behind by a killed or cancelled job.

    DeeZy only cleans up after a run it completes, and the Atmos and AC-4 decodes it
    leaves behind are the size of the source track. Safe to call at startup, when no
    job of ours can be running.
    """
    scratch = toolchain.deezy_temp_dir
    if scratch is None or not scratch.is_dir():
        return
    for entry in scratch.iterdir():
        with suppress(OSError):
            if entry.is_dir():
                shutil.rmtree(entry, ignore_errors=True)
            else:
                entry.unlink()


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
    opusenc_version = _inspect_optional_tool(toolchain.opusenc, ["--version"])
    # These probes stay tolerant of a non-zero exit: a tool that prints its version
    # and then complains about something unrelated is still a usable tool, and a
    # failure here silently hides every adapter that depends on it.
    deezy_version = _inspect_optional_tool(toolchain.deezy, ["--version"], check=False)
    dee_version = _inspect_optional_tool(toolchain.dee, ["--help"], check=False)
    truehdd_version = _inspect_optional_tool(toolchain.truehdd, ["--version"], check=False)
    return ToolReport(
        toolchain,
        ffmpeg_version,
        ffprobe_version,
        frozenset(encoders),
        frozenset(muxers),
        qaac_version,
        fdkaac_version,
        opusenc_version,
        deezy_version,
        dee_version,
        truehdd_version,
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
