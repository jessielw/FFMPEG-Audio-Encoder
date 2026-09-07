from pathlib import Path
from typing import Any, cast

import pytest

from ffmpeg_audio_encoder.domain.errors import ValidationError
from ffmpeg_audio_encoder.domain.models import (
    AudioStream,
    Codec,
    CommonAudioOptions,
    EncodingRequest,
    OutputFormat,
    ProgressProtocol,
    Toolchain,
)
from ffmpeg_audio_encoder.encoders.deezy import (
    DeezyAc4Encoder,
    DeezyAtmosEncoder,
    DeezyDdEncoder,
    DeezyDdpBlurayEncoder,
    DeezyDdpEncoder,
)


def _toolchain(tmp_path: Path) -> Toolchain:
    return Toolchain(
        Path("ffmpeg"),
        Path("ffprobe"),
        deezy=Path("deezy"),
        dee=Path("dee"),
        truehdd=Path("truehdd"),
        deezy_work_dir=tmp_path / "work",
        deezy_temp_dir=tmp_path / "scratch",
    )


def _request(
    encoder,
    codec: Codec,
    output_format: OutputFormat,
    *,
    common: CommonAudioOptions | None = None,
    stream_channels: int = 8,
    stream_codec: str = "truehd",
    **options: object,
) -> EncodingRequest:
    values = encoder.default_options()
    values.update(options)
    return EncodingRequest(
        Path("input with spaces.mkv"),
        AudioStream(
            3,
            2,
            stream_codec,
            stream_channels,
            "7.1",
            48000,
            duration_seconds=10,
        ),
        encoder.descriptor.id,
        codec,
        output_format,
        Path(f"output{output_format.suffix}"),
        common or CommonAudioOptions(delay_ms=-21.5),
        values,
    )


@pytest.mark.parametrize(
    ("encoder", "codec", "output_format", "command", "needs_truehdd"),
    [
        (DeezyDdEncoder(), Codec.AC3, OutputFormat.AC3, "dd", False),
        (DeezyDdpEncoder(), Codec.EAC3, OutputFormat.EAC3, "ddp", False),
        (
            DeezyDdpBlurayEncoder(),
            Codec.EAC3,
            OutputFormat.EAC3,
            "ddp-bluray",
            False,
        ),
        (DeezyAtmosEncoder(), Codec.ATMOS, OutputFormat.EAC3, "atmos", True),
        (DeezyAc4Encoder(), Codec.AC4, OutputFormat.AC4, "ac4", True),
    ],
)
def test_deezy_adapters_build_managed_single_process_plans(
    encoder,
    codec: Codec,
    output_format: OutputFormat,
    command: str,
    needs_truehdd: bool,
    tmp_path: Path,
) -> None:
    request = _request(encoder, codec, output_format)
    temporary = tmp_path / f".output.part{output_format.suffix}"

    plan = encoder.build_plan(request, _toolchain(tmp_path), temporary)

    assert plan.has_determinate_progress
    assert len(plan.stages) == 1
    stage = plan.stages[0]
    assert stage.program == Path("deezy")
    assert stage.arguments[:3] == ("--no-progress-bars", "encode", command)
    # DeeZy logs through a bare logging.StreamHandler, so progress arrives on stderr.
    assert stage.progress_stream == "stderr"
    assert stage.progress_protocol is ProgressProtocol.DEEZY
    assert stage.terminate_tree
    assert "--ffmpeg" in stage.arguments
    assert "--dee" in stage.arguments
    assert ("--truehdd" in stage.arguments) is needs_truehdd
    assert "--track-index=s:3" in stage.arguments
    assert "--delay=-21.5ms" in stage.arguments
    assert stage.arguments[stage.arguments.index("--output") + 1] == str(temporary)
    # Without --temp-dir, DeeZy writes an Atmos decode the size of the source track
    # into a "<stem>_deezy" folder beside the user's media, and leaves it behind when
    # the job is cancelled.
    assert stage.arguments[stage.arguments.index("--temp-dir") + 1] == str(tmp_path / "scratch")
    assert stage.arguments[-1] == str(request.input_path)


def test_deezy_maps_channels_booleans_and_custom_downmix_metadata(tmp_path: Path) -> None:
    encoder = DeezyDdEncoder()
    request = _request(
        encoder,
        Codec.AC3,
        OutputFormat.AC3,
        common=CommonAudioOptions(channel_layout="stereo"),
        bitrate_kbps=448,
        dialogue_intelligence=False,
        low_pass_filter=False,
        upmix_50_to_51=True,
        custom_args="--lt-rt-center -4.5 --lo-ro-surround -6",
    )

    arguments = (
        encoder.build_plan(request, _toolchain(tmp_path), tmp_path / "out.ac3").stages[0].arguments
    )

    assert arguments[arguments.index("--channels") + 1] == "2"
    assert arguments[arguments.index("--bitrate") + 1] == "448"
    assert "--no-dialogue-intelligence" in arguments
    assert "--no-low-pass-filter" in arguments
    assert "--upmix-50-to-51" in arguments
    assert "--lt-rt-center" in arguments


def test_deezy_bluray_forces_71_channels(tmp_path: Path) -> None:
    encoder = DeezyDdpBlurayEncoder()
    request = _request(encoder, Codec.EAC3, OutputFormat.EAC3)
    arguments = (
        encoder.build_plan(request, _toolchain(tmp_path), tmp_path / "out.eac3").stages[0].arguments
    )
    assert arguments[arguments.index("--channels") + 1] == "8"


@pytest.mark.parametrize(
    "common",
    [
        CommonAudioOptions(sample_rate=48000),
        CommonAudioOptions(gain_db=1),
        CommonAudioOptions(tempo_ratio=1.01),
    ],
)
def test_deezy_rejects_unsupported_common_audio_edits(common: CommonAudioOptions) -> None:
    encoder = DeezyDdEncoder()
    with pytest.raises(ValidationError, match="DeeZy"):
        encoder.validate(_request(encoder, Codec.AC3, OutputFormat.AC3, common=common))


def test_deezy_rejects_operational_custom_arguments() -> None:
    encoder = DeezyDdEncoder()
    with pytest.raises(ValidationError, match="Advanced DeeZy"):
        encoder.validate(
            _request(
                encoder,
                Codec.AC3,
                OutputFormat.AC3,
                custom_args="--output stolen.ac3",
            )
        )


def test_deezy_atmos_and_ac4_require_truehdd(tmp_path: Path) -> None:
    toolchain = _toolchain(tmp_path)
    toolchain = Toolchain(
        toolchain.ffmpeg,
        toolchain.ffprobe,
        deezy=toolchain.deezy,
        dee=toolchain.dee,
        deezy_work_dir=toolchain.deezy_work_dir,
    )
    for encoder, codec, output_format in (
        (DeezyAtmosEncoder(), Codec.ATMOS, OutputFormat.EAC3),
        (DeezyAc4Encoder(), Codec.AC4, OutputFormat.AC4),
    ):
        with pytest.raises(ValidationError, match="TrueHDD"):
            encoder.build_plan(
                _request(encoder, codec, output_format),
                toolchain,
                tmp_path / f"out{output_format.suffix}",
            )


@pytest.mark.parametrize(
    ("encoder", "codec", "output_format", "metering_mode", "cli_token"),
    [
        (DeezyDdEncoder(), Codec.AC3, OutputFormat.AC3, "1770_1", "MODE_1770_1"),
        (DeezyDdpEncoder(), Codec.EAC3, OutputFormat.EAC3, "1770_2", "MODE_1770_2"),
        (
            DeezyDdpBlurayEncoder(),
            Codec.EAC3,
            OutputFormat.EAC3,
            "1770_3",
            "MODE_1770_3",
        ),
        (DeezyAtmosEncoder(), Codec.ATMOS, OutputFormat.EAC3, "1770_4", "MODE_1770_4"),
        (DeezyAc4Encoder(), Codec.AC4, OutputFormat.AC4, "leqa", "MODE_LEQA"),
    ],
)
def test_deezy_emits_metering_enum_names_accepted_by_packaged_cli(
    encoder,
    codec: Codec,
    output_format: OutputFormat,
    metering_mode: str,
    cli_token: str,
    tmp_path: Path,
) -> None:
    arguments = (
        encoder.build_plan(
            _request(encoder, codec, output_format, metering_mode=metering_mode),
            _toolchain(tmp_path),
            tmp_path / f"out{output_format.suffix}",
        )
        .stages[0]
        .arguments
    )

    assert arguments[arguments.index("--metering-mode") + 1] == cli_token


@pytest.mark.parametrize(
    ("encoder", "expected_default", "expected_values"),
    [
        (DeezyDdEncoder(), "1770_3", ("1770_1", "1770_2", "1770_3", "leqa")),
        (DeezyDdpEncoder(), "1770_3", ("1770_1", "1770_2", "1770_3", "leqa")),
        (
            DeezyDdpBlurayEncoder(),
            "1770_3",
            ("1770_1", "1770_2", "1770_3", "leqa"),
        ),
        (
            DeezyAtmosEncoder(),
            "1770_4",
            ("1770_1", "1770_2", "1770_3", "1770_4", "leqa"),
        ),
        (
            DeezyAc4Encoder(),
            "1770_4",
            ("1770_1", "1770_2", "1770_3", "1770_4", "leqa"),
        ),
    ],
)
def test_deezy_metering_choices_are_mode_specific(
    encoder,
    expected_default: str,
    expected_values: tuple[str, ...],
) -> None:
    definition = next(
        option for option in encoder.descriptor.options if option.key == "metering_mode"
    )

    assert definition.default == expected_default
    assert tuple(choice.value for choice in definition.choices) == expected_values


def test_deezy_omits_dialogue_controls_when_metering_mode_ignores_them(
    tmp_path: Path,
) -> None:
    encoder = DeezyDdEncoder()
    arguments = (
        encoder.build_plan(
            _request(
                encoder,
                Codec.AC3,
                OutputFormat.AC3,
                metering_mode="leqa",
                dialogue_intelligence=False,
                speech_threshold=99,
            ),
            _toolchain(tmp_path),
            tmp_path / "out.ac3",
        )
        .stages[0]
        .arguments
    )

    assert "--no-dialogue-intelligence" not in arguments
    assert "--speech-threshold" not in arguments


def test_deezy_mode_schemas_do_not_emit_foreign_options(tmp_path: Path) -> None:
    atmos = DeezyAtmosEncoder()
    atmos_arguments = (
        atmos.build_plan(
            _request(atmos, Codec.ATMOS, OutputFormat.EAC3),
            _toolchain(tmp_path),
            tmp_path / "atmos.eac3",
        )
        .stages[0]
        .arguments
    )
    assert "--channels" not in atmos_arguments
    assert "--no-low-pass-filter" not in atmos_arguments
    assert "--upmix-50-to-51" not in atmos_arguments

    ac4 = DeezyAc4Encoder()
    ac4_arguments = (
        ac4.build_plan(
            _request(ac4, Codec.AC4, OutputFormat.AC4),
            _toolchain(tmp_path),
            tmp_path / "audio.ac4",
        )
        .stages[0]
        .arguments
    )
    assert "--drc-line-mode" not in ac4_arguments
    assert "--custom-dialnorm" not in ac4_arguments
    assert "--stereo-down-mix" not in ac4_arguments
    assert "--channels" not in ac4_arguments


@pytest.mark.parametrize(
    (
        "encoder",
        "codec",
        "output_format",
        "common",
        "stream_channels",
        "stream_codec",
        "encoder_options",
        "message",
    ),
    [
        (
            DeezyDdpEncoder(),
            Codec.EAC3,
            OutputFormat.EAC3,
            CommonAudioOptions(channel_layout="7.1"),
            6,
            "aac",
            {},
            "cannot up-mix",
        ),
        (
            DeezyDdpBlurayEncoder(),
            Codec.EAC3,
            OutputFormat.EAC3,
            None,
            6,
            "aac",
            {},
            "at least 8 source channels",
        ),
        (
            DeezyAtmosEncoder(),
            Codec.ATMOS,
            OutputFormat.EAC3,
            None,
            6,
            "truehd",
            {"atmos_mode": "bluray"},
            "at least 8",
        ),
        (
            DeezyAc4Encoder(),
            Codec.AC4,
            OutputFormat.AC4,
            None,
            2,
            "aac",
            {},
            "at least 6 channels",
        ),
    ],
)
def test_deezy_rejects_mode_specific_invalid_source_layouts(
    encoder,
    codec: Codec,
    output_format: OutputFormat,
    common: CommonAudioOptions | None,
    stream_channels: int,
    stream_codec: str,
    encoder_options: dict[str, object],
    message: str,
) -> None:
    with pytest.raises(ValidationError, match=message):
        encoder.validate(
            _request(
                encoder,
                codec,
                output_format,
                common=common,
                stream_channels=stream_channels,
                stream_codec=stream_codec,
                **encoder_options,
            )
        )


def test_deezy_allows_explicit_50_to_51_upmix() -> None:
    encoder = DeezyDdEncoder()
    encoder.validate(
        _request(
            encoder,
            Codec.AC3,
            OutputFormat.AC3,
            common=CommonAudioOptions(channel_layout="5.1"),
            stream_channels=5,
            upmix_50_to_51=True,
        )
    )


@pytest.mark.parametrize(
    ("encoder", "codec", "output_format", "common", "stream_channels", "options", "expected"),
    [
        (
            DeezyDdEncoder(),
            Codec.AC3,
            OutputFormat.AC3,
            None,
            8,
            {},
            (0, 224, 256, 320, 384, 448, 512, 576, 640),
        ),
        (
            DeezyDdEncoder(),
            Codec.AC3,
            OutputFormat.AC3,
            CommonAudioOptions(channel_layout="stereo"),
            8,
            {},
            (0, 96, 112, 128, 160, 192, 224, 256, 320, 384, 448, 512, 576, 640),
        ),
        (
            DeezyDdpEncoder(),
            Codec.EAC3,
            OutputFormat.EAC3,
            CommonAudioOptions(channel_layout="7.1"),
            8,
            {},
            (0, 384, 448, 504, 576, 640, 704, 768, 832, 896, 960, 1008, 1024),
        ),
        (
            DeezyDdpBlurayEncoder(),
            Codec.EAC3,
            OutputFormat.EAC3,
            None,
            8,
            {},
            (0, 768, 1024, 1280, 1536, 1664),
        ),
        (
            DeezyAtmosEncoder(),
            Codec.ATMOS,
            OutputFormat.EAC3,
            None,
            8,
            {"atmos_mode": "streaming"},
            (0, 384, 448, 512, 576, 640, 768, 1024),
        ),
        (
            DeezyAtmosEncoder(),
            Codec.ATMOS,
            OutputFormat.EAC3,
            None,
            8,
            {"atmos_mode": "bluray"},
            (0, 1152, 1280, 1408, 1512, 1536, 1664),
        ),
        (
            DeezyAc4Encoder(),
            Codec.AC4,
            OutputFormat.AC4,
            None,
            8,
            {},
            (0, 64, 72, 112, 144, 256, 320),
        ),
    ],
)
def test_deezy_exposes_only_configuration_specific_bitrates(
    encoder,
    codec: Codec,
    output_format: OutputFormat,
    common: CommonAudioOptions | None,
    stream_channels: int,
    options: dict[str, object],
    expected: tuple[int, ...],
) -> None:
    request = _request(
        encoder,
        codec,
        output_format,
        common=common,
        stream_channels=stream_channels,
        **cast(Any, options),
    )

    choices = encoder.option_choices(
        "bitrate_kbps",
        request.stream,
        request.common.channel_layout,
        request.encoder_options,
    )

    assert tuple(choice.value for choice in choices) == expected


def test_deezy_rejects_stale_or_profile_incompatible_bitrate() -> None:
    encoder = DeezyAtmosEncoder()
    with pytest.raises(ValidationError, match="invalid for this DeeZy configuration"):
        encoder.validate(
            _request(
                encoder,
                Codec.ATMOS,
                OutputFormat.EAC3,
                atmos_mode="streaming",
                bitrate_kbps=1280,
            )
        )
    with pytest.raises(ValidationError, match="Invalid bitrate"):
        encoder.validate(
            _request(
                encoder,
                Codec.ATMOS,
                OutputFormat.EAC3,
                bitrate_kbps=18,
            )
        )


# DeeZy coerces every enum-typed flag with cli.utils.case_insensitive_enum, which
# accepts a bare digit or an uppercased *member name* and nothing else - notably not
# the member's own string value, which is what its --help advertises. Mirrored from
# DeeZy 1.3.2 so a token that DeeZy would reject fails here instead of at encode time.
DEEZY_ENUM_MEMBERS = {
    "--drc-line-mode": {"FILM_STANDARD", "FILM_LIGHT", "MUSIC_STANDARD", "MUSIC_LIGHT", "SPEECH"},
    "--drc-rf-mode": {"FILM_STANDARD", "FILM_LIGHT", "MUSIC_STANDARD", "MUSIC_LIGHT", "SPEECH"},
    "--metering-mode": {"MODE_1770_1", "MODE_1770_2", "MODE_1770_3", "MODE_1770_4", "MODE_LEQA"},
    "--stereo-down-mix": {"NOT_INDICATED", "LORO", "LTRT", "DPLII"},
    "--thd-warp-mode": {"NORMAL", "WARPING", "DPLII", "LORO"},
    "--atmos-mode": {"STREAMING", "BLURAY"},
    "--encoding-profile": {"IMS", "IMS_MUSIC"},
    "--channels": {"0", "1", "2", "6", "8"},
}
_AC4_DRC_MEMBERS = {
    "FILM_STANDARD",
    "FILM_LIGHT",
    "MUSIC_STANDARD",
    "MUSIC_LIGHT",
    "SPEECH",
    "NONE",
}
DEEZY_ENUM_MEMBERS.update(
    dict.fromkeys(
        (
            "--ddp-drc",
            "--flat-panel-drc",
            "--home-theatre-drc",
            "--portable-headphones-drc",
            "--portable-speakers-drc",
        ),
        _AC4_DRC_MEMBERS,
    )
)


@pytest.mark.parametrize(
    ("encoder", "codec", "output_format"),
    [
        (DeezyDdEncoder(), Codec.AC3, OutputFormat.AC3),
        (DeezyDdpEncoder(), Codec.EAC3, OutputFormat.EAC3),
        (DeezyDdpBlurayEncoder(), Codec.EAC3, OutputFormat.EAC3),
        (DeezyAtmosEncoder(), Codec.ATMOS, OutputFormat.EAC3),
        (DeezyAc4Encoder(), Codec.AC4, OutputFormat.AC4),
    ],
)
def test_every_offered_choice_is_a_token_deezy_accepts(
    encoder, codec: Codec, output_format: OutputFormat, tmp_path: Path
) -> None:
    toolchain = _toolchain(tmp_path)
    choice_options = [
        option
        for option in encoder.descriptor.options
        if option.choices and option.key != "bitrate_kbps"
    ]
    assert choice_options, "expected the adapter to offer choice-based options"
    for option in choice_options:
        for choice in option.choices:
            request = _request(encoder, codec, output_format, **{option.key: choice.value})
            arguments = (
                encoder.build_plan(
                    request, toolchain, tmp_path / f"temporary{output_format.suffix}"
                )
                .stages[0]
                .arguments
            )
            for flag, members in DEEZY_ENUM_MEMBERS.items():
                if flag not in arguments:
                    continue
                token = arguments[arguments.index(flag) + 1]
                assert token.isdigit() or token.upper() in members, (
                    f"{encoder.descriptor.id} emits {flag} {token!r}, which DeeZy would reject"
                )
