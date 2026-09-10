from __future__ import annotations

from pathlib import Path

import pytest

from ffmpeg_audio_encoder.domain.errors import ValidationError
from ffmpeg_audio_encoder.domain.models import (
    AudioStream,
    Codec,
    CommonAudioOptions,
    EncodingRequest,
    NoticeLevel,
    OutputFormat,
    ProcessPlan,
    Toolchain,
)
from ffmpeg_audio_encoder.encoders.external import QaacEncoder
from ffmpeg_audio_encoder.encoders.ffmpeg import AacEncoder

TOOLCHAIN = Toolchain(Path("ffmpeg"), Path("ffprobe"), qaac=Path("qaac"))


def _plan(custom: str, *, gain: float = 0.0, tempo: float = 1.0) -> ProcessPlan:
    encoder = AacEncoder()
    options = encoder.default_options()
    options["custom_args"] = custom
    request = EncodingRequest(
        Path("input.wav"),
        AudioStream(0, 1, "pcm_s16le"),
        encoder.descriptor.id,
        Codec.AAC,
        OutputFormat.M4A,
        Path("output.m4a"),
        common=CommonAudioOptions(gain_db=gain, tempo_ratio=tempo),
        encoder_options=options,
    )
    return encoder.build_plan(request, TOOLCHAIN, Path("temporary.m4a"))


def _arguments(custom: str, *, gain: float = 0.0, tempo: float = 1.0) -> tuple[str, ...]:
    return _plan(custom, gain=gain, tempo=tempo).stages[0].arguments


def _value_after(arguments: tuple[str, ...], flag: str) -> str:
    return arguments[arguments.index(flag) + 1]


def test_a_value_saved_before_slots_existed_produces_the_same_arguments() -> None:
    """The backward-compatibility contract: one unprefixed line means what it always did."""
    assert _arguments('-metadata title="My Song" -cutoff 18000') == _arguments(
        "-metadata title='My Song'\n-cutoff 18000"
    )
    arguments = _arguments('-metadata title="My Song" -cutoff 18000')
    assert _value_after(arguments, "-metadata") == "title=My Song"
    assert arguments.index("-cutoff") < arguments.index("-progress")


def test_pre_slot_lands_before_the_input_and_out_slot_after_the_codec() -> None:
    arguments = _arguments("pre: -guess_layout_max 0\nout: -cutoff 18000")
    assert arguments.index("-guess_layout_max") < arguments.index("-i")
    assert arguments.index("-cutoff") > arguments.index("-c:a")
    assert arguments.index("-cutoff") < arguments.index("-progress")


def test_an_unknown_slot_names_the_ones_the_encoder_offers() -> None:
    with pytest.raises(ValidationError, match="decode"):
        _arguments("decode: -c:a pcm_f32le")


def test_a_colliding_flag_replaces_the_managed_one_rather_than_joining_it() -> None:
    plan = _plan("-b:a 256k")
    arguments = plan.stages[0].arguments
    assert arguments.count("-b:a") == 1
    assert _value_after(arguments, "-b:a") == "256k"
    assert "192k" not in arguments
    warnings = [n for n in plan.notices if n.level is NoticeLevel.WARNING]
    assert len(warnings) == 1
    assert "overrides Bitrate (192k)" in warnings[0].message


def test_a_flag_alias_collides_with_the_managed_spelling() -> None:
    """-filter:a and -af are one option to FFmpeg; emitting both fails the encode."""
    arguments = _arguments("-filter:a volume=6dB", gain=3.0)
    assert arguments.count("-af") + arguments.count("-filter:a") == 1
    assert "volume=3dB" not in arguments


def test_repeated_custom_flags_are_all_kept() -> None:
    """Deduplication is custom-against-managed only; -metadata is repeatable."""
    arguments = _arguments("-metadata title=One\n-metadata artist=Two")
    assert arguments.count("-metadata") == 2


def test_the_filters_placeholder_extends_the_managed_chain() -> None:
    plan = _plan("-af {filters},highpass=f=20", gain=2.0)
    assert _value_after(plan.stages[0].arguments, "-af") == "volume=2dB,highpass=f=20"
    assert [n.level for n in plan.notices] == [NoticeLevel.INFO]


def test_an_empty_filters_placeholder_collapses_its_separators() -> None:
    """-af ',highpass=f=20' is not a filter chain FFmpeg accepts."""
    assert _value_after(_arguments("-af {filters},highpass=f=20"), "-af") == "highpass=f=20"


def test_replacing_the_filter_chain_warns_that_gain_and_tempo_are_lost() -> None:
    plan = _plan("-af volume=6dB", gain=3.0, tempo=1.5)
    warnings = [n for n in plan.notices if n.level is NoticeLevel.WARNING]
    assert len(warnings) == 1
    assert "gain, tempo and delay will NOT be applied" in warnings[0].message
    assert "atempo=1.5" in warnings[0].message


def test_a_variable_expands_where_it_is_used() -> None:
    assert _value_after(_arguments("var cutoff = 18000\n-cutoff {cutoff}"), "-cutoff") == "18000"


def test_a_defined_but_empty_variable_drops_only_its_own_group() -> None:
    plan = _plan("var cutoff =\n-cutoff {cutoff} -aac_coder fast")
    arguments = plan.stages[0].arguments
    assert "-cutoff" not in arguments
    assert _value_after(arguments, "-aac_coder") == "fast"
    assert [n.level for n in plan.notices] == [NoticeLevel.INFO, NoticeLevel.WARNING]


def test_an_undefined_placeholder_is_refused_rather_than_silently_dropped() -> None:
    """A typo, or a value saved before placeholders existed, must not change the command."""
    with pytest.raises(ValidationError, match=r"Unknown placeholder \{typo\}"):
        _arguments("-metadata comment={typo}")


def test_a_doubled_brace_is_a_literal_brace() -> None:
    assert _value_after(_arguments("-metadata comment={{typo}}"), "-metadata") == "comment={typo}"


def test_a_variable_holding_spaces_stays_one_argument() -> None:
    """Substitution runs after tokenising, so a variable can never inject an argument."""
    arguments = _arguments("var t = a b\n-metadata title={t}")
    assert _value_after(arguments, "-metadata") == "title=a b"


def test_an_option_key_is_a_placeholder_without_being_declared_as_one() -> None:
    assert _value_after(_arguments("-cutoff {bitrate_kbps}"), "-cutoff") == "192"


def test_a_negative_number_is_a_value_not_a_new_group() -> None:
    """Grouping decides what a drop or an override applies to, so -3 must not read as a flag."""
    arguments = _arguments("-metadata a=1 -filter_complex volume=-3")
    assert _value_after(arguments, "-filter_complex") == "volume=-3"
    assert _value_after(arguments, "-metadata") == "a=1"


@pytest.mark.parametrize(
    "custom",
    [
        "-f mp4",
        "-i other.mkv",
        "pre: -i other.mkv",
        "-map 0:1",
        "-progress pipe:9",
        "-nostats",
        "-o elsewhere.m4a",
    ],
)
def test_arguments_that_would_break_publishing_or_progress_are_refused(custom: str) -> None:
    with pytest.raises(ValidationError, match="Custom arguments cannot"):
        _arguments(custom)


def test_a_bare_value_is_refused_because_ffmpeg_would_read_it_as_an_output() -> None:
    with pytest.raises(ValidationError, match="must start with a flag"):
        _arguments("output.m4a")


def test_comments_and_blank_lines_are_ignored() -> None:
    assert _arguments("# a note\n\n-cutoff 18000") == _arguments("-cutoff 18000")


def test_validation_rejects_bad_custom_arguments_before_a_job_is_queued() -> None:
    encoder = AacEncoder()
    options = encoder.default_options()
    options["custom_args"] = '"unterminated'
    with pytest.raises(ValidationError, match="Invalid custom"):
        encoder.validate(
            EncodingRequest(
                Path("input.wav"),
                AudioStream(0, 1, "pcm_s16le"),
                encoder.descriptor.id,
                Codec.AAC,
                OutputFormat.M4A,
                Path("output.m4a"),
                encoder_options=options,
            )
        )


def _qaac_plan(custom: str) -> ProcessPlan:
    encoder = QaacEncoder()
    options = encoder.default_options()
    options["custom_args"] = custom
    request = EncodingRequest(
        Path("input.wav"),
        AudioStream(0, 1, "pcm_s16le"),
        encoder.descriptor.id,
        Codec.AAC,
        OutputFormat.M4A,
        Path("output.m4a"),
        encoder_options=options,
    )
    return encoder.build_plan(request, TOOLCHAIN, Path("temporary.m4a"))


def test_each_slot_reaches_its_own_stage_of_a_two_stage_pipeline() -> None:
    plan = _qaac_plan("pre: -analyzeduration 200M\ndecode: -c:a pcm_f32le\n--gapless-mode 2")
    decode, encode = plan.stages[0].arguments, plan.stages[1].arguments

    assert decode.index("-analyzeduration") < decode.index("-i")
    assert decode.count("-c:a") == 1
    assert _value_after(decode, "-c:a") == "pcm_f32le"
    assert decode[-4:] == ("-nostats", "-f", "wav", "pipe:1")

    assert "--gapless-mode" in encode
    assert encode.index("--gapless-mode") < encode.index("-o")
    assert encode[-3:] == ("-o", "temporary.m4a", "-")


def test_a_two_stage_encoder_cannot_be_pointed_at_another_output() -> None:
    with pytest.raises(ValidationError, match="published atomically"):
        _qaac_plan("-o elsewhere.m4a")
