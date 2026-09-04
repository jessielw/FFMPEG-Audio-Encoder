from pathlib import Path

import pytest

from ffmpeg_audio_encoder.domain.errors import ValidationError
from ffmpeg_audio_encoder.domain.models import (
    AudioStream,
    Codec,
    CommonAudioOptions,
    EncodingRequest,
    OutputFormat,
    Toolchain,
)
from ffmpeg_audio_encoder.encoders import default_registry
from ffmpeg_audio_encoder.encoders.external import FdkAacEncoder, OpusencEncoder, QaacEncoder
from ffmpeg_audio_encoder.encoders.ffmpeg import (
    AacEncoder,
    Ac3Encoder,
    AlacEncoder,
    DtsEncoder,
    Eac3Encoder,
    FlacEncoder,
    Mp3Encoder,
    OpusEncoder,
)


def opus_request(**options: object) -> EncodingRequest:
    encoder = OpusEncoder()
    values = encoder.default_options()
    values.update(options)  # type: ignore[arg-type]
    return EncodingRequest(
        Path("input with spaces.mkv"),
        AudioStream(3, 2, "aac", 6, "5.1", 48000, "eng", duration_seconds=10.0),
        encoder.descriptor.id,
        Codec.OPUS,
        OutputFormat.OGG_OPUS,
        Path("output with spaces.opus"),
        CommonAudioOptions(48000, "stereo"),
        values,
    )


def test_default_registry_has_unique_first_party_adapters() -> None:
    registry = default_registry()
    assert [adapter.descriptor.id for adapter in registry] == [
        "ffmpeg.libopus",
        "opusenc.opus",
        "ffmpeg.flac",
        "ffmpeg.aac",
        "ffmpeg.libmp3lame",
        "ffmpeg.ac3",
        "ffmpeg.eac3",
        "ffmpeg.dca",
        "ffmpeg.alac",
        "qaac.aac",
        "fdkaac.aac",
    ]


def test_opus_builds_an_argument_list_with_exact_global_stream_mapping(tmp_path: Path) -> None:
    encoder = OpusEncoder()
    request = opus_request()
    temporary = tmp_path / ".output.part.opus"
    plan = encoder.build_plan(
        request,
        Toolchain(Path("ffmpeg"), Path("ffprobe")),
        temporary,
    )
    arguments = plan.stages[0].arguments
    assert arguments[arguments.index("-map") + 1] == "0:3"
    assert arguments[arguments.index("-c:a") + 1] == "libopus"
    assert arguments[arguments.index("-b:a") + 1] == "160k"
    assert arguments[-1] == str(temporary)
    assert plan.stages[0].program == Path("ffmpeg")


@pytest.mark.parametrize(
    ("tempo", "expected"),
    [
        (0.25, "atempo=0.5,atempo=0.5"),
        (4.0, "atempo=2,atempo=2"),
    ],
)
def test_common_gain_and_tempo_build_a_managed_filter_chain(
    tmp_path: Path, tempo: float, expected: str
) -> None:
    encoder = OpusEncoder()
    request = opus_request()
    request = EncodingRequest(
        request.input_path,
        request.stream,
        request.encoder_id,
        request.codec,
        request.output_format,
        request.output_path,
        CommonAudioOptions(48000, "stereo", 3.5, tempo),
        request.encoder_options,
    )
    plan = encoder.build_plan(
        request,
        Toolchain(Path("ffmpeg"), Path("ffprobe")),
        tmp_path / "temporary.opus",
    )
    arguments = plan.stages[0].arguments
    filters = arguments[arguments.index("-af") + 1]
    assert filters == f"volume=3.5dB,{expected}"


@pytest.mark.parametrize(("gain", "tempo"), [(31.0, 1.0), (0.0, 0.2)])
def test_common_filters_reject_out_of_range_values(gain: float, tempo: float) -> None:
    request = opus_request()
    invalid = EncodingRequest(
        request.input_path,
        request.stream,
        request.encoder_id,
        request.codec,
        request.output_format,
        request.output_path,
        CommonAudioOptions(gain_db=gain, tempo_ratio=tempo),
        request.encoder_options,
    )
    with pytest.raises(ValidationError):
        OpusEncoder().validate(invalid)


@pytest.mark.parametrize("bitrate", [5, 511, "160"])
def test_opus_rejects_invalid_bitrates(bitrate: object) -> None:
    with pytest.raises(ValidationError):
        OpusEncoder().validate(opus_request(bitrate_kbps=bitrate))


def test_flac_rejects_an_incompatible_codec() -> None:
    request = EncodingRequest(
        Path("input.wav"),
        AudioStream(0, 1, "pcm_s16le"),
        "ffmpeg.flac",
        Codec.OPUS,
        OutputFormat.FLAC,
        Path("output.flac"),
        encoder_options={"compression_level": 5},
    )
    with pytest.raises(ValidationError):
        FlacEncoder().validate(request)


@pytest.mark.parametrize(
    ("encoder", "tool_name"),
    [(QaacEncoder(), "qaac"), (FdkAacEncoder(), "fdkaac")],
)
def test_external_aac_adapters_pipe_wav_from_ffmpeg(
    encoder, tool_name: str, tmp_path: Path
) -> None:
    request = EncodingRequest(
        Path("input with spaces.mkv"),
        AudioStream(2, 1, "flac", 2, "stereo", 48000, duration_seconds=10.0),
        encoder.descriptor.id,
        Codec.AAC,
        OutputFormat.M4A,
        Path("output with spaces.m4a"),
        CommonAudioOptions(48000, "stereo"),
        encoder.default_options(),
    )
    toolchain = Toolchain(
        Path("ffmpeg"),
        Path("ffprobe"),
        qaac=Path("qaac64"),
        fdkaac=Path("fdkaac"),
    )
    temporary = tmp_path / "temporary.m4a"
    plan = encoder.build_plan(request, toolchain, temporary)

    assert len(plan.stages) == 2
    assert plan.stages[0].program == Path("ffmpeg")
    assert plan.stages[0].progress_stream == "stderr"
    assert plan.stages[0].arguments[-3:] == ("-f", "wav", "pipe:1")
    assert plan.stages[1].program == getattr(toolchain, tool_name)
    assert "--ignorelength" in plan.stages[1].arguments
    assert plan.stages[1].arguments[-3:] == ("-o", str(temporary), "-")


def test_opusenc_adapter_pipes_24_bit_wav_and_maps_native_options(tmp_path: Path) -> None:
    encoder = OpusencEncoder()
    options = encoder.default_options()
    options.update(
        {
            "rate_control": "cvbr",
            "signal": "speech",
            "phase_inversion": "disabled",
            "custom_args": "--comment title=Example",
        }
    )
    request = EncodingRequest(
        Path("input with spaces.mkv"),
        AudioStream(2, 1, "flac", 2, "stereo", 48000, duration_seconds=10.0),
        encoder.descriptor.id,
        Codec.OPUS,
        OutputFormat.OGG_OPUS,
        Path("output with spaces.opus"),
        CommonAudioOptions(48000, "stereo"),
        options,
    )
    toolchain = Toolchain(Path("ffmpeg"), Path("ffprobe"), opusenc=Path("opusenc"))
    temporary = tmp_path / "temporary.opus"

    plan = encoder.build_plan(request, toolchain, temporary)

    assert len(plan.stages) == 2
    assert plan.stages[0].program == Path("ffmpeg")
    assert plan.stages[0].arguments[plan.stages[0].arguments.index("-c:a") + 1] == "pcm_s24le"
    assert plan.stages[0].arguments[-3:] == ("-f", "wav", "pipe:1")
    assert plan.stages[1].program == Path("opusenc")
    assert "--ignorelength" in plan.stages[1].arguments
    assert "--no-downmix" in plan.stages[1].arguments
    assert "--cvbr" in plan.stages[1].arguments
    assert "--speech" in plan.stages[1].arguments
    assert "--no-phase-inv" in plan.stages[1].arguments
    assert plan.stages[1].arguments[-4:] == ("--comment", "title=Example", "-", str(temporary))


def test_opusenc_rejects_bitrate_above_effective_channel_limit() -> None:
    encoder = OpusencEncoder()
    options = encoder.default_options()
    options["bitrate_kbps"] = 513
    with pytest.raises(ValidationError, match="512 kb/s"):
        encoder.validate(
            EncodingRequest(
                Path("input.wav"),
                AudioStream(0, 1, "pcm_s16le", 6),
                encoder.descriptor.id,
                Codec.OPUS,
                OutputFormat.OGG_OPUS,
                Path("output.opus"),
                CommonAudioOptions(channel_layout="stereo"),
                options,
            )
        )


def test_opusenc_requires_configured_executable(tmp_path: Path) -> None:
    encoder = OpusencEncoder()
    request = EncodingRequest(
        Path("input.wav"),
        AudioStream(0, 1, "pcm_s16le", 2),
        encoder.descriptor.id,
        Codec.OPUS,
        OutputFormat.OGG_OPUS,
        Path("output.opus"),
        encoder_options=encoder.default_options(),
    )
    with pytest.raises(ValidationError, match="opusenc is not configured"):
        encoder.build_plan(
            request,
            Toolchain(Path("ffmpeg"), Path("ffprobe")),
            tmp_path / "temporary.opus",
        )


def test_qaac_rejects_tvbr_for_he_aac() -> None:
    encoder = QaacEncoder()
    options = encoder.default_options()
    options["profile"] = "he"
    with pytest.raises(ValidationError, match="True VBR"):
        encoder.validate(
            EncodingRequest(
                Path("input.wav"),
                AudioStream(0, 1, "pcm_s16le", 2),
                encoder.descriptor.id,
                Codec.AAC,
                OutputFormat.M4A,
                Path("output.m4a"),
                encoder_options=options,
            )
        )


def test_fdkaac_rejects_he_v2_for_multichannel_audio() -> None:
    encoder = FdkAacEncoder()
    options = encoder.default_options()
    options["profile"] = 29
    with pytest.raises(ValidationError, match="requires stereo"):
        encoder.validate(
            EncodingRequest(
                Path("input.wav"),
                AudioStream(0, 1, "pcm_s16le", 6),
                encoder.descriptor.id,
                Codec.AAC,
                OutputFormat.M4A,
                Path("output.m4a"),
                encoder_options=options,
            )
        )


def test_fdkaac_exposes_only_supported_channel_layouts() -> None:
    assert [layout.value for layout in FdkAacEncoder.descriptor.channel_layouts] == [
        "mono",
        "stereo",
        "3.0",
        "4.0",
        "5.0",
        "5.1",
        "7.1",
    ]


@pytest.mark.parametrize(
    ("encoder", "codec", "output_format", "ffmpeg_name"),
    [
        (AacEncoder(), Codec.AAC, OutputFormat.M4A, "aac"),
        (Mp3Encoder(), Codec.MP3, OutputFormat.MP3, "libmp3lame"),
        (Ac3Encoder(), Codec.AC3, OutputFormat.AC3, "ac3"),
        (Eac3Encoder(), Codec.EAC3, OutputFormat.EAC3, "eac3"),
        (DtsEncoder(), Codec.DTS, OutputFormat.DTS, "dca"),
        (AlacEncoder(), Codec.ALAC, OutputFormat.M4A, "alac"),
    ],
)
def test_new_adapters_build_managed_ffmpeg_plans(
    encoder,
    codec: Codec,
    output_format: OutputFormat,
    ffmpeg_name: str,
    tmp_path: Path,
) -> None:
    request = EncodingRequest(
        Path("input.wav"),
        AudioStream(0, 1, "pcm_s16le", 2, "stereo", 48000),
        encoder.descriptor.id,
        codec,
        output_format,
        Path(f"output{output_format.suffix}"),
        CommonAudioOptions(48000, "stereo"),
        encoder.default_options(),
    )
    plan = encoder.build_plan(
        request,
        Toolchain(Path("ffmpeg"), Path("ffprobe")),
        tmp_path / f"temporary{output_format.suffix}",
    )
    arguments = plan.stages[0].arguments
    assert arguments[arguments.index("-c:a") + 1] == ffmpeg_name
    assert arguments[arguments.index("-channel_layout:a") + 1] == "stereo"
    assert arguments[-4:-1] == ("-nostats", "-f", output_format.ffmpeg_muxer)


def test_custom_arguments_are_tokenized_without_a_shell_and_precede_managed_output() -> None:
    encoder = AacEncoder()
    options = encoder.default_options()
    options["custom_args"] = '-metadata title="My Song" -cutoff 18000'
    request = EncodingRequest(
        Path("input.wav"),
        AudioStream(0, 1, "pcm_s16le"),
        encoder.descriptor.id,
        Codec.AAC,
        OutputFormat.M4A,
        Path("output.m4a"),
        encoder_options=options,
    )
    plan = encoder.build_plan(
        request,
        Toolchain(Path("ffmpeg"), Path("ffprobe")),
        Path("temporary.m4a"),
    )
    arguments = plan.stages[0].arguments
    assert arguments[arguments.index("-metadata") + 1] == "title=My Song"
    assert arguments.index("-cutoff") < arguments.index("-progress")


def test_custom_arguments_reject_unbalanced_quotes() -> None:
    with pytest.raises(ValidationError, match="Invalid custom"):
        AacEncoder().validate(
            EncodingRequest(
                Path("input.wav"),
                AudioStream(0, 1, "pcm_s16le"),
                "ffmpeg.aac",
                Codec.AAC,
                OutputFormat.M4A,
                Path("output.m4a"),
                encoder_options={"custom_args": '"unterminated'},
            )
        )


def test_codec_specific_layout_is_validated() -> None:
    encoder = Mp3Encoder()
    with pytest.raises(ValidationError, match="does not support"):
        encoder.validate(
            EncodingRequest(
                Path("input.wav"),
                AudioStream(0, 1, "pcm_s16le"),
                encoder.descriptor.id,
                Codec.MP3,
                OutputFormat.MP3,
                Path("output.mp3"),
                CommonAudioOptions(channel_layout="5.1"),
                encoder.default_options(),
            )
        )


@pytest.mark.parametrize(
    ("encoder", "expected_rates"),
    [
        (OpusEncoder(), (8000, 12000, 16000, 24000, 48000)),
        (
            AacEncoder(),
            (
                7350,
                8000,
                11025,
                12000,
                16000,
                22050,
                24000,
                32000,
                44100,
                48000,
                64000,
                88200,
                96000,
            ),
        ),
        (
            Mp3Encoder(),
            (8000, 11025, 12000, 16000, 22050, 24000, 32000, 44100, 48000),
        ),
        (Ac3Encoder(), (32000, 44100, 48000)),
        (Eac3Encoder(), (32000, 44100, 48000)),
        (
            DtsEncoder(),
            (8000, 11025, 12000, 16000, 22050, 24000, 32000, 44100, 48000),
        ),
    ],
)
def test_fixed_rate_encoders_describe_ffmpeg_supported_rates(
    encoder, expected_rates: tuple[int, ...]
) -> None:
    assert encoder.descriptor.sample_rate_choices == expected_rates
    assert encoder.descriptor.sample_rate_range is None


def test_fixed_rate_encoder_rejects_an_unsupported_sample_rate() -> None:
    encoder = AacEncoder()
    with pytest.raises(ValidationError, match="does not support 50000 Hz"):
        encoder.validate(
            EncodingRequest(
                Path("input.wav"),
                AudioStream(0, 1, "pcm_s16le"),
                encoder.descriptor.id,
                Codec.AAC,
                OutputFormat.M4A,
                Path("output.m4a"),
                CommonAudioOptions(sample_rate=50000),
                encoder.default_options(),
            )
        )


@pytest.mark.parametrize("sample_rate", [12345, 384000, 1_048_575])
def test_flac_accepts_nonstandard_rates_within_ffmpeg_range(sample_rate: int) -> None:
    encoder = FlacEncoder()
    encoder.validate(
        EncodingRequest(
            Path("input.wav"),
            AudioStream(0, 1, "pcm_s16le"),
            encoder.descriptor.id,
            Codec.FLAC,
            OutputFormat.FLAC,
            Path("output.flac"),
            CommonAudioOptions(sample_rate=sample_rate),
            encoder.default_options(),
        )
    )


def test_flac_rejects_a_rate_above_ffmpeg_limit() -> None:
    encoder = FlacEncoder()
    with pytest.raises(ValidationError, match="supports sample rates from"):
        encoder.validate(
            EncodingRequest(
                Path("input.wav"),
                AudioStream(0, 1, "pcm_s16le"),
                encoder.descriptor.id,
                Codec.FLAC,
                OutputFormat.FLAC,
                Path("output.flac"),
                CommonAudioOptions(sample_rate=1_048_576),
                encoder.default_options(),
            )
        )


@pytest.mark.parametrize(
    ("delay_ms", "expected_filter", "expected_duration"),
    [
        (125.5, "atempo=2,adelay=0.1255s:all=1", 5.1255),
        (-125.5, "atempo=2,atrim=start=0.1255,asetpts=PTS-STARTPTS", 4.8745),
    ],
)
def test_signed_delay_is_applied_after_tempo_and_adjusts_duration(
    tmp_path: Path,
    delay_ms: float,
    expected_filter: str,
    expected_duration: float,
) -> None:
    encoder = OpusEncoder()
    original = opus_request()
    request = EncodingRequest(
        original.input_path,
        original.stream,
        original.encoder_id,
        original.codec,
        original.output_format,
        original.output_path,
        CommonAudioOptions(48000, "stereo", tempo_ratio=2.0, delay_ms=delay_ms),
        original.encoder_options,
    )

    plan = encoder.build_plan(
        request,
        Toolchain(Path("ffmpeg"), Path("ffprobe")),
        tmp_path / "temporary.opus",
    )
    arguments = plan.stages[0].arguments

    assert arguments[arguments.index("-af") + 1] == expected_filter
    assert plan.duration_seconds == pytest.approx(expected_duration)


@pytest.mark.parametrize("encoder", [QaacEncoder(), FdkAacEncoder()])
def test_external_encoders_receive_common_delay_filter(encoder, tmp_path: Path) -> None:
    request = EncodingRequest(
        Path("input.wav"),
        AudioStream(0, 1, "pcm_s16le", 2, "stereo", 48000, duration_seconds=10.0),
        encoder.descriptor.id,
        Codec.AAC,
        OutputFormat.M4A,
        Path("output.m4a"),
        CommonAudioOptions(delay_ms=50.0),
        encoder.default_options(),
    )
    toolchain = Toolchain(
        Path("ffmpeg"),
        Path("ffprobe"),
        qaac=Path("qaac64"),
        fdkaac=Path("fdkaac"),
    )

    plan = encoder.build_plan(request, toolchain, tmp_path / "temporary.m4a")
    arguments = plan.stages[0].arguments

    assert arguments[arguments.index("-af") + 1] == "adelay=0.05s:all=1"
    assert plan.duration_seconds == pytest.approx(10.05)


@pytest.mark.parametrize(
    ("delay_ms", "message"),
    [
        (float("inf"), "Audio delay must be between"),
        (86_400_001.0, "Audio delay must be between"),
        (-10_000.0, "must leave some audio"),
    ],
)
def test_invalid_audio_delays_are_rejected(delay_ms: float, message: str) -> None:
    original = opus_request()
    request = EncodingRequest(
        original.input_path,
        original.stream,
        original.encoder_id,
        original.codec,
        original.output_format,
        original.output_path,
        CommonAudioOptions(delay_ms=delay_ms),
        original.encoder_options,
    )

    with pytest.raises(ValidationError, match=message):
        OpusEncoder().validate(request)
