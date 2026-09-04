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
        "ffmpeg.flac",
        "ffmpeg.aac",
        "ffmpeg.libmp3lame",
        "ffmpeg.ac3",
        "ffmpeg.eac3",
        "ffmpeg.dca",
        "ffmpeg.alac",
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
