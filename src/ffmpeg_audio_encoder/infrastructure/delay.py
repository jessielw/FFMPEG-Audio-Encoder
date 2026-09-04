from __future__ import annotations

import math
import re
from dataclasses import dataclass

MAX_DELAY_MS = 86_400_000.0
_NUMBER = r"[+-]?(?:\d+(?:\.\d+)?|\.\d+)"
_DELAY_MARKER = re.compile(
    rf"""
    (?:
        \[\s*delay[\s_.:=]*(?P<bracket>{_NUMBER})\s*ms\s*\]
        |
        \(\s*delay[\s_.:=]*(?P<parenthesized>{_NUMBER})\s*ms\s*\)
        |
        (?<![A-Za-z0-9])delay[\s_.:=]*(?P<plain>{_NUMBER})\s*ms(?![A-Za-z0-9])
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)


@dataclass(frozen=True, slots=True)
class FilenameDelay:
    milliseconds: float
    start: int
    end: int


def parse_filename_delay(value: str) -> FilenameDelay | None:
    matches = list(_DELAY_MARKER.finditer(value))
    if len(matches) != 1:
        return None
    match = matches[0]
    raw_value = next(group for group in match.groups() if group is not None)
    milliseconds = float(raw_value)
    if not math.isfinite(milliseconds) or abs(milliseconds) > MAX_DELAY_MS:
        return None
    return FilenameDelay(milliseconds, match.start(), match.end())


def strip_filename_delay_marker(value: str) -> str:
    detected = parse_filename_delay(value)
    if detected is None:
        return value
    cleaned = f"{value[: detected.start]} {value[detected.end :]}"
    cleaned = re.sub(r"(?:\s*[-_.]\s*){2,}", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip(" ._-")
