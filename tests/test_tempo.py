import math
from pathlib import Path

import pytest

from ffmpeg_audio_encoder.domain.models import (
    AudioStream,
    Codec,
    CommonAudioOptions,
    EncodingRequest,
    OutputFormat,
    Toolchain,
)
from ffmpeg_audio_encoder.domain.tempo import (
    TEMPO_PRESETS,
    TEMPO_TOLERANCE,
    TempoPreset,
    find_tempo_preset,
    format_ratio,
)
from ffmpeg_audio_encoder.encoders.ffmpeg import OpusEncoder


def request_at(tempo: float) -> EncodingRequest:
    encoder = OpusEncoder()
    return EncodingRequest(
        Path("input.mkv"),
        AudioStream(0, 0, "aac", 6, "5.1", 48000, "eng", duration_seconds=7200.0),
        encoder.descriptor.id,
        Codec.OPUS,
        OutputFormat.OGG_OPUS,
        Path("output.opus"),
        CommonAudioOptions(tempo_ratio=tempo),
        encoder.default_options(),
    )


def atempo_stages(tempo: float, tmp_path: Path) -> list[float]:
    plan = OpusEncoder().build_plan(
        request_at(tempo),
        Toolchain(Path("ffmpeg"), Path("ffprobe")),
        tmp_path / "temporary.opus",
    )
    arguments = plan.stages[0].arguments
    if "-af" not in arguments:
        return []
    filters = arguments[arguments.index("-af") + 1].split(",")
    return [
        float(entry.removeprefix("atempo=")) for entry in filters if entry.startswith("atempo=")
    ]


def find(label_start: str) -> TempoPreset:
    return next(preset for preset in TEMPO_PRESETS if preset.label.startswith(label_start))


def test_presets_cover_every_framerate_pair_plus_speeds() -> None:
    # One "Original", 8 x 7 framerate pairs, 11 speed multipliers.
    assert len(TEMPO_PRESETS) == 1 + 56 + 11
    assert len({preset.label for preset in TEMPO_PRESETS}) == len(TEMPO_PRESETS)


def test_every_preset_ratio_is_inside_the_validated_range() -> None:
    # _validate_identity rejects anything outside 0.25-4.0, so no preset may be
    # offered that the encoder would then refuse.
    for preset in TEMPO_PRESETS:
        assert math.isfinite(preset.ratio)
        assert 0.25 <= preset.ratio <= 4.0, preset.label


@pytest.mark.parametrize(
    ("label_start", "expected"),
    [
        ("Original", 1.0),
        # 23.976 fps is exactly 24000/1001, so NTSC pulldown is exactly 1001/1000.
        ("23.976 → 24", 1.001),
        ("24 → 23.976", 0.999001),
        ("24 → 25", 1.041667),
        ("23.976 → 25", 1.042708),
        ("25 → 24", 0.96),
        ("23.976 → 60", 2.5025),
        ("59.94 → 23.976", 0.4),
    ],
)
def test_framerate_pairs_come_from_the_exact_rational(label_start: str, expected: float) -> None:
    assert find(label_start).ratio == expected


def test_labels_carry_the_ratio_without_padded_zeros() -> None:
    assert find("24 → 23.976").label == "24 → 23.976 (0.999001x)"
    assert find("23.976 → 24").label == "23.976 → 24 (1.001x)"
    assert find("2x speed").label == "2x speed"


def test_format_ratio_trims_trailing_zeros() -> None:
    assert format_ratio(1.0) == "1"
    assert format_ratio(2.5025) == "2.5025"
    assert format_ratio(0.999001) == "0.999001"


def test_find_tempo_preset_round_trips_every_preset() -> None:
    for preset in TEMPO_PRESETS:
        match = find_tempo_preset(preset.ratio)
        assert match is not None
        assert match.ratio == preset.ratio


def test_find_tempo_preset_rejects_values_outside_the_spinbox_resolution() -> None:
    # What a three-decimal build would have saved for the PAL speed-up. It is
    # reported as custom rather than silently snapped to the real preset.
    assert find_tempo_preset(1.043) is None
    assert find_tempo_preset(float("nan")) is None
    assert find_tempo_preset(1.001 + 2 * TEMPO_TOLERANCE) is None


def test_find_tempo_preset_returns_the_first_of_a_shared_ratio() -> None:
    # 25 -> 50, 30 -> 60, 29.97 -> 59.94 and "2x speed" are all exactly 2.0.
    shared = [preset.label for preset in TEMPO_PRESETS if preset.ratio == 2.0]
    assert len(shared) > 1
    match = find_tempo_preset(2.0)
    assert match is not None
    assert match.label == shared[0]


def test_every_preset_builds_an_atempo_chain_that_multiplies_back(tmp_path: Path) -> None:
    for preset in TEMPO_PRESETS:
        stages = atempo_stages(preset.ratio, tmp_path)
        product = math.prod(stages) if stages else 1.0
        assert math.isclose(product, preset.ratio, rel_tol=1e-9), preset.label
        for stage in stages:
            assert 0.5 <= stage <= 2.0, preset.label


def test_atempo_is_emitted_with_enough_precision(tmp_path: Path) -> None:
    # ":g" would truncate this to 1.04167, a 3.2e-6 error - about 23 ms of drift
    # over the two-hour source this request describes.
    assert atempo_stages(1.041667, tmp_path) == [1.041667]
    assert atempo_stages(1.042708, tmp_path) == [1.042708]


def test_unchanged_tempo_emits_no_atempo_filter(tmp_path: Path) -> None:
    assert atempo_stages(1.0, tmp_path) == []
