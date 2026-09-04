from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from PySide6.QtCore import QObject, QProcess, Signal

from ffmpeg_audio_encoder.domain.errors import ProbeError
from ffmpeg_audio_encoder.domain.models import AudioStream, MediaAsset


def _optional_float(value: object) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        return None
    try:
        parsed = float(value)
        return parsed if parsed >= 0 else None
    except (TypeError, ValueError):
        return None


def _optional_int(value: object) -> int | None:
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def parse_ffprobe_json(path: Path, payload: Mapping[str, Any]) -> MediaAsset:
    raw_format = payload.get("format")
    format_duration = (
        _optional_float(raw_format.get("duration")) if isinstance(raw_format, Mapping) else None
    )
    raw_streams = payload.get("streams")
    if not isinstance(raw_streams, list):
        raise ProbeError("ffprobe response does not contain a stream list")

    audio_streams: list[AudioStream] = []
    for raw_stream in raw_streams:
        if not isinstance(raw_stream, Mapping) or raw_stream.get("codec_type") != "audio":
            continue
        index = _optional_int(raw_stream.get("index"))
        if index is None:
            continue
        raw_tags = raw_stream.get("tags")
        tags = raw_tags if isinstance(raw_tags, Mapping) else {}
        duration = _optional_float(raw_stream.get("duration")) or format_duration
        audio_streams.append(
            AudioStream(
                index=index,
                ordinal=len(audio_streams) + 1,
                codec_name=str(raw_stream.get("codec_name") or "unknown"),
                channels=_optional_int(raw_stream.get("channels")),
                channel_layout=(
                    str(raw_stream["channel_layout"]) if raw_stream.get("channel_layout") else None
                ),
                sample_rate=_optional_int(raw_stream.get("sample_rate")),
                language=str(tags["language"]) if tags.get("language") else None,
                title=str(tags["title"]) if tags.get("title") else None,
                duration_seconds=duration,
            )
        )
    if not audio_streams:
        raise ProbeError("The selected input does not contain an audio stream")
    return MediaAsset(path, tuple(audio_streams), format_duration)


class QtMediaProbe(QObject):
    completed = Signal(str, object)
    failed = Signal(str, str)

    def __init__(self, ffprobe_path: Path, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.ffprobe_path = ffprobe_path
        self._processes: dict[str, QProcess] = {}
        self._stdout: dict[str, bytearray] = {}
        self._stderr: dict[str, bytearray] = {}

    def probe(self, path: Path) -> None:
        key = str(path)
        if key in self._processes:
            return
        process = QProcess(self)
        self._processes[key] = process
        self._stdout[key] = bytearray()
        self._stderr[key] = bytearray()
        process.readyReadStandardOutput.connect(
            lambda key=key, process=process: self._stdout[key].extend(
                process.readAllStandardOutput().data()
            )
        )
        process.readyReadStandardError.connect(
            lambda key=key, process=process: self._stderr[key].extend(
                process.readAllStandardError().data()
            )
        )
        process.finished.connect(lambda exit_code, _status, key=key: self._finish(key, exit_code))
        process.setProgram(str(self.ffprobe_path))
        process.setArguments(
            [
                "-v",
                "error",
                "-show_streams",
                "-show_format",
                "-of",
                "json",
                key,
            ]
        )
        process.start()

    def _finish(self, key: str, exit_code: int) -> None:
        process = self._processes.pop(key)
        stdout = bytes(self._stdout.pop(key)).decode("utf-8", errors="replace")
        stderr = bytes(self._stderr.pop(key)).decode("utf-8", errors="replace").strip()
        process.deleteLater()
        if exit_code != 0:
            self.failed.emit(key, stderr or f"ffprobe exited with code {exit_code}")
            return
        try:
            payload = json.loads(stdout)
            if not isinstance(payload, dict):
                raise ProbeError("ffprobe returned an unexpected JSON value")
            self.completed.emit(key, parse_ffprobe_json(Path(key), payload))
        except (json.JSONDecodeError, ProbeError) as exc:
            self.failed.emit(key, str(exc))
