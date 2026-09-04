from __future__ import annotations

import re
from pathlib import Path
from uuid import UUID

from ffmpeg_audio_encoder.domain.models import AudioStream, Codec, OutputFormat

_INVALID_FILENAME = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
_WINDOWS_RESERVED = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}


def sanitize_filename_component(value: str) -> str:
    cleaned = _INVALID_FILENAME.sub("_", value).strip().rstrip(".")
    cleaned = re.sub(r"\s+", " ", cleaned)
    if not cleaned:
        cleaned = "audio"
    if cleaned.upper() in _WINDOWS_RESERVED:
        cleaned = f"_{cleaned}"
    return cleaned[:180].rstrip(" .")


def default_output_path(
    input_path: Path,
    stream: AudioStream,
    codec: Codec,
    output_format: OutputFormat,
    output_directory: Path | None = None,
) -> Path:
    parts = [sanitize_filename_component(input_path.stem), f"[Audio {stream.ordinal}]"]
    if stream.language:
        parts.append(f"[{sanitize_filename_component(stream.language)}]")
    if stream.channels:
        parts.append(f"[{stream.channels}ch]")
    parts.append(f"[{codec.value.title()}]")
    return (output_directory or input_path.parent) / (" ".join(parts) + output_format.suffix)


def temporary_output_path(final_output: Path, job_id: UUID) -> Path:
    return final_output.with_name(f".{final_output.stem}.{job_id.hex}.part{final_output.suffix}")
