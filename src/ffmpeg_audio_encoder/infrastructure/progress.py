from __future__ import annotations

import re
from contextlib import suppress
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProgressUpdate:
    fraction: float | None
    speed: str | None = None
    total_size: int | None = None
    ended: bool = False
    phase: str | None = None


class FFmpegProgressParser:
    def __init__(self, duration_seconds: float | None) -> None:
        self.duration_seconds = duration_seconds
        self._buffer = ""
        self._values: dict[str, str] = {}

    def feed(self, text: str) -> list[ProgressUpdate]:
        self._buffer += text.replace("\r\n", "\n")
        lines = self._buffer.split("\n")
        self._buffer = lines.pop()
        updates: list[ProgressUpdate] = []
        for line in lines:
            key, separator, value = line.partition("=")
            if not separator:
                continue
            self._values[key.strip()] = value.strip()
            if key == "progress":
                updates.append(self._snapshot(value.strip() == "end"))
                self._values = {}
        return updates

    def _snapshot(self, ended: bool) -> ProgressUpdate:
        fraction: float | None = None
        if ended:
            fraction = 1.0
        elif self.duration_seconds and self.duration_seconds > 0:
            elapsed = self._elapsed_seconds()
            if elapsed is not None:
                fraction = min(max(elapsed / self.duration_seconds, 0.0), 1.0)
        total_size: int | None = None
        raw_size = self._values.get("total_size")
        if raw_size:
            with suppress(ValueError):
                total_size = int(raw_size)
        return ProgressUpdate(fraction, self._values.get("speed"), total_size, ended)

    def _elapsed_seconds(self) -> float | None:
        for key in ("out_time_us", "out_time_ms"):
            raw_value = self._values.get(key)
            if raw_value:
                try:
                    return int(raw_value) / 1_000_000
                except ValueError:
                    pass
        raw_time = self._values.get("out_time")
        if not raw_time:
            return None
        try:
            hours, minutes, seconds = raw_time.split(":")
            return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
        except (ValueError, TypeError):
            return None


class DeezyProgressParser:
    _PROGRESS_LINE = re.compile(
        r"(?P<phase>.+?)\s+\((?P<current>\d+) of (?P<total>\d+)\)\s+"
        r"(?P<percent>\d+(?:\.\d+)?)%"
    )

    def __init__(self) -> None:
        self._buffer = ""

    def feed(self, text: str) -> list[ProgressUpdate]:
        self._buffer += text.replace("\r\n", "\n").replace("\r", "\n")
        lines = self._buffer.split("\n")
        self._buffer = lines.pop()
        updates: list[ProgressUpdate] = []
        for line in lines:
            match = self._PROGRESS_LINE.search(line.strip())
            if match is None:
                continue
            current = int(match.group("current"))
            total = int(match.group("total"))
            percent = float(match.group("percent"))
            if total <= 0 or not 1 <= current <= total:
                continue
            stage_fraction = min(max(percent / 100.0, 0.0), 1.0)
            fraction = min(max(((current - 1) + stage_fraction) / total, 0.0), 1.0)
            updates.append(
                ProgressUpdate(
                    fraction,
                    ended=current == total and stage_fraction >= 1.0,
                    phase=match.group("phase").strip(),
                )
            )
        return updates
