"""Framerate-conversion and speed presets for the common tempo control.

The encoders only ever see a ratio - `CommonAudioOptions.tempo_ratio`. This module
turns the framerate pairs people actually work with ("24 to 23.976") into that
ratio, so nobody has to work out that NTSC pulldown is 1000/1001.

Ratios are computed from `Fraction`s rather than from the rounded decimal labels,
because 23.976 fps is exactly 24000/1001. Going through the rational makes
23.976 -> 24 come out as exactly 1.001 instead of a float artefact, then rounds
once to `TEMPO_DECIMALS` so the table matches what the spinbox can hold.

Ratios are not unique: 25 -> 50, 30 -> 60, 29.97 -> 59.94 and the 2x speed preset
are all exactly 2.0. `find_tempo_preset` therefore returns the *first* match, and
is only ever used to re-label a restored value - never to drive a selection the
user has already made.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction

# Decimal places the tempo ratio is carried to, in the preset table and in the
# spinbox alike. Six is enough that the worst preset (24 -> 25, 1.0416666...)
# drifts by well under a millisecond over a feature-length file.
TEMPO_DECIMALS = 6

# Half a unit in the last place the ratio can represent, which is the widest two
# values may differ and still be "the same preset".
TEMPO_TOLERANCE = 5 * 10 ** -(TEMPO_DECIMALS + 1)

ORIGINAL_GROUP = ""
SPEED_GROUP = "Speed"


@dataclass(frozen=True, slots=True)
class Framerate:
    label: str
    rate: Fraction


@dataclass(frozen=True, slots=True)
class TempoPreset:
    label: str
    ratio: float
    group: str


FRAMERATES = (
    Framerate("23.976", Fraction(24000, 1001)),
    Framerate("24", Fraction(24)),
    Framerate("25", Fraction(25)),
    Framerate("29.97", Fraction(30000, 1001)),
    Framerate("30", Fraction(30)),
    Framerate("50", Fraction(50)),
    Framerate("59.94", Fraction(60000, 1001)),
    Framerate("60", Fraction(60)),
)

# Kept from v4, minus its confusing labelling. v4 called 0.25x "1/4 Slow-down"
# and 1.25x "1/4 Speed-up", using "1/4" to mean two different things. v4 also
# emitted 2.5x through 4x as a single atempo=, which FFmpeg rejects outright;
# they work here because the filter chain is built by halving and doubling.
SPEED_MULTIPLIERS = (0.25, 0.5, 0.75, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 3.5, 4.0)


def format_ratio(value: float) -> str:
    """Render a ratio without padded trailing zeros: 1.001, 0.999001, 2.5025."""
    return f"{value:.{TEMPO_DECIMALS}f}".rstrip("0").rstrip(".")


def _framerate_presets() -> list[TempoPreset]:
    presets: list[TempoPreset] = []
    for source in FRAMERATES:
        for target in FRAMERATES:
            if target is source:
                continue
            ratio = round(float(target.rate / source.rate), TEMPO_DECIMALS)
            presets.append(
                TempoPreset(
                    f"{source.label} → {target.label} ({format_ratio(ratio)}x)",
                    ratio,
                    f"{source.label} fps source",
                )
            )
    return presets


def _speed_presets() -> list[TempoPreset]:
    return [
        TempoPreset(f"{format_ratio(multiplier)}x speed", multiplier, SPEED_GROUP)
        for multiplier in SPEED_MULTIPLIERS
    ]


TEMPO_PRESETS: tuple[TempoPreset, ...] = (
    TempoPreset("Original (no change)", 1.0, ORIGINAL_GROUP),
    *_framerate_presets(),
    *_speed_presets(),
)


def find_tempo_preset(ratio: float) -> TempoPreset | None:
    """Return the first preset matching `ratio`, or None for a custom value."""
    if not math.isfinite(ratio):
        return None
    for preset in TEMPO_PRESETS:
        if math.isclose(preset.ratio, ratio, rel_tol=0.0, abs_tol=TEMPO_TOLERANCE):
            return preset
    return None
