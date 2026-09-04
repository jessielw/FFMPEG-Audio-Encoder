from __future__ import annotations

import shlex
from pathlib import Path

from ffmpeg_audio_encoder.domain.errors import ValidationError
from ffmpeg_audio_encoder.domain.models import (
    ChannelLayoutChoice,
    Codec,
    EncoderDescriptor,
    EncodingRequest,
    JsonScalar,
    OptionChoice,
    OptionDefinition,
    OptionKind,
    OutputFormat,
    ProcessPlan,
    ProcessStage,
    Toolchain,
)


def _layouts(*values: str) -> tuple[ChannelLayoutChoice, ...]:
    labels = {
        "mono": "Mono",
        "stereo": "Stereo",
        "2.1": "2.1",
        "2.2": "2.2",
        "3.0": "3.0",
        "quad": "Quad",
        "4.0": "4.0",
        "5.0": "5.0",
        "5.0(back)": "5.0 (back)",
        "5.1": "5.1",
        "5.1(back)": "5.1 (back)",
        "6.1": "6.1",
        "6.1(back)": "6.1 (back)",
        "7.1": "7.1",
        "7.1(wide-back)": "7.1 (wide back)",
    }
    return tuple(ChannelLayoutChoice(labels[value], value) for value in values)


COMMON_LAYOUTS = _layouts("mono", "stereo", "3.0", "quad", "5.0", "5.1", "6.1", "7.1")
DOLBY_LAYOUTS = _layouts("mono", "stereo", "2.1", "3.0", "quad", "4.0", "5.0", "5.1")
DTS_LAYOUTS = _layouts("mono", "stereo", "2.2", "5.0", "5.1")
ALAC_LAYOUTS = _layouts(
    "mono",
    "stereo",
    "3.0",
    "4.0",
    "5.0(back)",
    "5.1(back)",
    "6.1(back)",
    "7.1(wide-back)",
)
MP3_LAYOUTS = _layouts("mono", "stereo")

OPUS_SAMPLE_RATES = (8000, 12000, 16000, 24000, 48000)
AAC_SAMPLE_RATES = (
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
)
MP3_SAMPLE_RATES = (8000, 11025, 12000, 16000, 22050, 24000, 32000, 44100, 48000)
DOLBY_SAMPLE_RATES = (32000, 44100, 48000)
DTS_SAMPLE_RATES = (8000, 11025, 12000, 16000, 22050, 24000, 32000, 44100, 48000)
LOSSLESS_SAMPLE_RATE_CHOICES = (
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
    176400,
    192000,
    352800,
    384000,
)

AC3_BITRATES = (
    32,
    40,
    48,
    56,
    64,
    80,
    96,
    112,
    128,
    160,
    192,
    224,
    256,
    320,
    384,
    448,
    512,
    576,
    640,
)
DTS_BITRATES = (
    32000,
    56000,
    64000,
    96000,
    112000,
    128000,
    192000,
    224000,
    256000,
    320000,
    384000,
    448000,
    512000,
    576000,
    640000,
    768000,
    896000,
    1024000,
    1152000,
    1280000,
    1344000,
    1408000,
    1411200,
    1472000,
    1536000,
    1920000,
    2048000,
    3072000,
    3840000,
)


def _custom_option() -> OptionDefinition:
    return OptionDefinition(
        "custom_args",
        "Custom FFmpeg output arguments",
        OptionKind.TEXT,
        "",
        tooltip=(
            "Advanced: appended after managed codec settings. Arguments are never run in a shell."
        ),
    )


def _choice(label: str, value: JsonScalar) -> OptionChoice:
    return OptionChoice(label, value)


def _bitrate_choices(values: tuple[int, ...], *, bps: bool = False) -> tuple[OptionChoice, ...]:
    return (
        _choice("Auto", None),
        *(_choice(f"{value / 1000:g} kb/s" if bps else f"{value} kb/s", value) for value in values),
    )


def _definition(descriptor: EncoderDescriptor, key: str) -> OptionDefinition:
    return next(option for option in descriptor.options if option.key == key)


def _value(request: EncodingRequest, descriptor: EncoderDescriptor, key: str) -> JsonScalar:
    definition = _definition(descriptor, key)
    return request.encoder_options.get(key, definition.default)


def _integer_option(request: EncodingRequest, descriptor: EncoderDescriptor, key: str) -> int:
    value = _value(request, descriptor, key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValidationError(f"{key} must be an integer")
    return value


def _number_option(request: EncodingRequest, descriptor: EncoderDescriptor, key: str) -> float:
    value = _value(request, descriptor, key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValidationError(f"{key} must be a number")
    return float(value)


def _string_option(request: EncodingRequest, descriptor: EncoderDescriptor, key: str) -> str:
    value = _value(request, descriptor, key)
    if not isinstance(value, str):
        raise ValidationError(f"{key} must be a string")
    return value


def _validate_identity(request: EncodingRequest, descriptor: EncoderDescriptor) -> None:
    if request.encoder_id != descriptor.id:
        raise ValidationError("The request targets a different encoder adapter")
    if request.codec not in descriptor.codecs:
        raise ValidationError(f"{descriptor.display_name} cannot encode {request.codec}")
    if request.output_format not in descriptor.output_formats:
        raise ValidationError(f"{descriptor.display_name} cannot write {request.output_format}")
    if request.stream.index < 0:
        raise ValidationError("Audio stream index cannot be negative")
    sample_rate = request.common.sample_rate
    if sample_rate is not None:
        if sample_rate <= 0:
            raise ValidationError("Sample rate must be positive")
        if descriptor.sample_rate_range is not None:
            minimum, maximum = descriptor.sample_rate_range
            if not minimum <= sample_rate <= maximum:
                raise ValidationError(
                    f"{descriptor.display_name} supports sample rates from "
                    f"{minimum} Hz to {maximum} Hz"
                )
        elif descriptor.sample_rate_choices and sample_rate not in descriptor.sample_rate_choices:
            supported = ", ".join(str(rate) for rate in descriptor.sample_rate_choices)
            raise ValidationError(
                f"{descriptor.display_name} does not support {sample_rate} Hz; "
                f"supported sample rates: {supported} Hz"
            )
    layout = request.common.channel_layout
    if layout is not None and layout not in {choice.value for choice in descriptor.channel_layouts}:
        raise ValidationError(f"{descriptor.display_name} does not support the {layout} layout")


def _validate_options(request: EncodingRequest, descriptor: EncoderDescriptor) -> None:
    for option in descriptor.options:
        value = _value(request, descriptor, option.key)
        if option.kind is OptionKind.INTEGER:
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValidationError(f"{option.label} must be an integer")
        elif option.kind is OptionKind.DECIMAL:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValidationError(f"{option.label} must be a number")
        elif option.kind is OptionKind.TEXT:
            if not isinstance(value, str):
                raise ValidationError(f"{option.label} must be text")
        elif value not in {choice.value for choice in option.choices}:
            raise ValidationError(f"Invalid {option.label.lower()}")
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if option.minimum is not None and value < option.minimum:
                raise ValidationError(f"{option.label} must be at least {option.minimum:g}")
            if option.maximum is not None and value > option.maximum:
                raise ValidationError(f"{option.label} must be at most {option.maximum:g}")
    _custom_arguments(request, descriptor)


def _custom_arguments(request: EncodingRequest, descriptor: EncoderDescriptor) -> list[str]:
    if not any(option.key == "custom_args" for option in descriptor.options):
        return []
    text = _string_option(request, descriptor, "custom_args").strip()
    if not text:
        return []
    if "\x00" in text:
        raise ValidationError("Custom arguments cannot contain NUL characters")
    try:
        return shlex.split(text, posix=True)
    except ValueError as exc:
        raise ValidationError(f"Invalid custom arguments: {exc}") from exc


def _base_arguments(request: EncodingRequest) -> list[str]:
    arguments = [
        "-nostdin",
        "-hide_banner",
        "-y",
        "-i",
        str(request.input_path),
        "-map",
        f"0:{request.stream.index}",
        "-vn",
        "-sn",
        "-dn",
        "-map_chapters",
        "-1",
    ]
    if request.common.sample_rate is not None:
        arguments.extend(("-ar", str(request.common.sample_rate)))
    if request.common.channel_layout is not None:
        arguments.extend(("-channel_layout:a", request.common.channel_layout))
    return arguments


# Shared adapter primitives. The underscore-prefixed implementations remain for
# compatibility with the original FFmpeg adapters.
base_arguments = _base_arguments
custom_arguments = _custom_arguments
integer_option = _integer_option
string_option = _string_option
validate_identity = _validate_identity
validate_options = _validate_options


def _finish_plan(
    request: EncodingRequest,
    descriptor: EncoderDescriptor,
    toolchain: Toolchain,
    temporary_output: Path,
    arguments: list[str],
) -> ProcessPlan:
    arguments.extend(_custom_arguments(request, descriptor))
    arguments.extend(
        (
            "-progress",
            "pipe:1",
            "-nostats",
            "-f",
            request.output_format.ffmpeg_muxer,
            str(temporary_output),
        )
    )
    return ProcessPlan(
        (ProcessStage(toolchain.ffmpeg, tuple(arguments), "stdout"),),
        temporary_output,
        request.output_path,
        request.stream.duration_seconds,
    )


class _FfmpegEncoder:
    descriptor: EncoderDescriptor

    def default_options(self) -> dict[str, JsonScalar]:
        return {option.key: option.default for option in self.descriptor.options}

    def validate(self, request: EncodingRequest) -> None:
        _validate_identity(request, self.descriptor)
        _validate_options(request, self.descriptor)


class OpusEncoder(_FfmpegEncoder):
    descriptor = EncoderDescriptor(
        id="ffmpeg.libopus",
        display_name="FFmpeg libopus",
        codecs=(Codec.OPUS,),
        output_formats=(OutputFormat.OGG_OPUS,),
        options=(
            OptionDefinition("bitrate_kbps", "Bitrate", OptionKind.INTEGER, 160, 6, 510, " kb/s"),
            OptionDefinition(
                "vbr",
                "Bitrate mode",
                OptionKind.CHOICE,
                "on",
                choices=(
                    _choice("Variable", "on"),
                    _choice("Constrained variable", "constrained"),
                    _choice("Constant", "off"),
                ),
            ),
            OptionDefinition(
                "application",
                "Application",
                OptionKind.CHOICE,
                "audio",
                choices=(
                    _choice("Audio", "audio"),
                    _choice("Voice", "voip"),
                    _choice("Low delay", "lowdelay"),
                ),
            ),
            OptionDefinition("compression_level", "Complexity", OptionKind.INTEGER, 10, 0, 10),
            OptionDefinition(
                "frame_duration",
                "Frame duration",
                OptionKind.CHOICE,
                "20",
                suffix=" ms",
                choices=tuple(
                    _choice(value, value) for value in ("2.5", "5", "10", "20", "40", "60")
                ),
            ),
            OptionDefinition(
                "packet_loss", "Expected packet loss", OptionKind.INTEGER, 0, 0, 100, "%"
            ),
            _custom_option(),
        ),
        required_ffmpeg_encoders=("libopus",),
        channel_layouts=COMMON_LAYOUTS,
        sample_rate_choices=OPUS_SAMPLE_RATES,
    )

    def build_plan(
        self, request: EncodingRequest, toolchain: Toolchain, temporary_output: Path
    ) -> ProcessPlan:
        self.validate(request)
        arguments = _base_arguments(request)
        arguments.extend(
            (
                "-c:a",
                "libopus",
                "-b:a",
                f"{_integer_option(request, self.descriptor, 'bitrate_kbps')}k",
                "-vbr",
                _string_option(request, self.descriptor, "vbr"),
                "-application",
                _string_option(request, self.descriptor, "application"),
                "-compression_level",
                str(_integer_option(request, self.descriptor, "compression_level")),
                "-frame_duration",
                _string_option(request, self.descriptor, "frame_duration"),
                "-packet_loss",
                str(_integer_option(request, self.descriptor, "packet_loss")),
            )
        )
        return _finish_plan(request, self.descriptor, toolchain, temporary_output, arguments)


class FlacEncoder(_FfmpegEncoder):
    descriptor = EncoderDescriptor(
        id="ffmpeg.flac",
        display_name="FFmpeg FLAC",
        codecs=(Codec.FLAC,),
        output_formats=(OutputFormat.FLAC,),
        options=(
            OptionDefinition(
                "compression_level", "Compression level", OptionKind.INTEGER, 5, 0, 12
            ),
            _custom_option(),
        ),
        required_ffmpeg_encoders=("flac",),
        channel_layouts=COMMON_LAYOUTS,
        sample_rate_choices=LOSSLESS_SAMPLE_RATE_CHOICES,
        sample_rate_range=(1, 1_048_575),
    )

    def build_plan(
        self, request: EncodingRequest, toolchain: Toolchain, temporary_output: Path
    ) -> ProcessPlan:
        self.validate(request)
        arguments = _base_arguments(request)
        arguments.extend(
            (
                "-c:a",
                "flac",
                "-compression_level",
                str(_integer_option(request, self.descriptor, "compression_level")),
            )
        )
        return _finish_plan(request, self.descriptor, toolchain, temporary_output, arguments)


class AacEncoder(_FfmpegEncoder):
    descriptor = EncoderDescriptor(
        id="ffmpeg.aac",
        display_name="FFmpeg AAC",
        codecs=(Codec.AAC,),
        output_formats=(OutputFormat.M4A, OutputFormat.ADTS_AAC),
        options=(
            OptionDefinition(
                "rate_control",
                "Rate control",
                OptionKind.CHOICE,
                "cbr",
                choices=(_choice("Constant bitrate", "cbr"), _choice("Variable quality", "vbr")),
            ),
            OptionDefinition(
                "bitrate_kbps",
                "Bitrate",
                OptionKind.INTEGER,
                192,
                8,
                512,
                " kb/s",
                enabled_when_key="rate_control",
                enabled_when_values=("cbr",),
            ),
            OptionDefinition(
                "quality",
                "VBR quality",
                OptionKind.DECIMAL,
                2.0,
                0.1,
                5.0,
                step=0.1,
                decimals=1,
                enabled_when_key="rate_control",
                enabled_when_values=("vbr",),
            ),
            OptionDefinition(
                "coder",
                "Coder",
                OptionKind.CHOICE,
                "twoloop",
                choices=(_choice("Two-loop", "twoloop"), _choice("Fast", "fast")),
            ),
            _custom_option(),
        ),
        required_ffmpeg_encoders=("aac",),
        channel_layouts=COMMON_LAYOUTS,
        sample_rate_choices=AAC_SAMPLE_RATES,
    )

    def build_plan(
        self, request: EncodingRequest, toolchain: Toolchain, temporary_output: Path
    ) -> ProcessPlan:
        self.validate(request)
        arguments = _base_arguments(request)
        arguments.extend(("-c:a", "aac"))
        if _string_option(request, self.descriptor, "rate_control") == "vbr":
            arguments.extend(("-q:a", f"{_number_option(request, self.descriptor, 'quality'):g}"))
        else:
            arguments.extend(
                ("-b:a", f"{_integer_option(request, self.descriptor, 'bitrate_kbps')}k")
            )
        arguments.extend(("-aac_coder", _string_option(request, self.descriptor, "coder")))
        return _finish_plan(request, self.descriptor, toolchain, temporary_output, arguments)


class Mp3Encoder(_FfmpegEncoder):
    descriptor = EncoderDescriptor(
        id="ffmpeg.libmp3lame",
        display_name="FFmpeg libmp3lame",
        codecs=(Codec.MP3,),
        output_formats=(OutputFormat.MP3,),
        options=(
            OptionDefinition(
                "rate_control",
                "Rate control",
                OptionKind.CHOICE,
                "vbr",
                choices=(
                    _choice("Variable quality", "vbr"),
                    _choice("Constant bitrate", "cbr"),
                    _choice("Average bitrate", "abr"),
                ),
            ),
            OptionDefinition(
                "vbr_quality",
                "VBR quality",
                OptionKind.INTEGER,
                0,
                0,
                9,
                enabled_when_key="rate_control",
                enabled_when_values=("vbr",),
            ),
            OptionDefinition(
                "bitrate_kbps",
                "Bitrate",
                OptionKind.CHOICE,
                192,
                choices=tuple(
                    _choice(f"{value} kb/s", value)
                    for value in (
                        8,
                        16,
                        24,
                        32,
                        40,
                        48,
                        56,
                        64,
                        80,
                        96,
                        112,
                        128,
                        160,
                        192,
                        224,
                        256,
                        320,
                    )
                ),
                enabled_when_key="rate_control",
                enabled_when_values=("cbr", "abr"),
            ),
            OptionDefinition("algorithm_quality", "Algorithm quality", OptionKind.INTEGER, 0, 0, 9),
            _custom_option(),
        ),
        required_ffmpeg_encoders=("libmp3lame",),
        channel_layouts=MP3_LAYOUTS,
        sample_rate_choices=MP3_SAMPLE_RATES,
    )

    def build_plan(
        self, request: EncodingRequest, toolchain: Toolchain, temporary_output: Path
    ) -> ProcessPlan:
        self.validate(request)
        arguments = _base_arguments(request)
        arguments.extend(("-c:a", "libmp3lame"))
        mode = _string_option(request, self.descriptor, "rate_control")
        if mode == "vbr":
            arguments.extend(
                ("-q:a", str(_integer_option(request, self.descriptor, "vbr_quality")))
            )
        else:
            arguments.extend(
                ("-b:a", f"{_integer_option(request, self.descriptor, 'bitrate_kbps')}k")
            )
            if mode == "abr":
                arguments.extend(("-abr", "1"))
        arguments.extend(
            (
                "-compression_level",
                str(_integer_option(request, self.descriptor, "algorithm_quality")),
            )
        )
        return _finish_plan(request, self.descriptor, toolchain, temporary_output, arguments)


class Ac3Encoder(_FfmpegEncoder):
    descriptor = EncoderDescriptor(
        id="ffmpeg.ac3",
        display_name="FFmpeg AC-3",
        codecs=(Codec.AC3,),
        output_formats=(OutputFormat.AC3,),
        options=(
            OptionDefinition(
                "bitrate_kbps",
                "Bitrate",
                OptionKind.CHOICE,
                224,
                choices=_bitrate_choices(AC3_BITRATES),
            ),
            _custom_option(),
        ),
        required_ffmpeg_encoders=("ac3",),
        channel_layouts=DOLBY_LAYOUTS,
        sample_rate_choices=DOLBY_SAMPLE_RATES,
    )

    def build_plan(
        self, request: EncodingRequest, toolchain: Toolchain, temporary_output: Path
    ) -> ProcessPlan:
        self.validate(request)
        arguments = _base_arguments(request)
        arguments.extend(("-c:a", "ac3"))
        bitrate = _value(request, self.descriptor, "bitrate_kbps")
        if bitrate is not None:
            arguments.extend(("-b:a", f"{bitrate}k"))
        return _finish_plan(request, self.descriptor, toolchain, temporary_output, arguments)


class Eac3Encoder(_FfmpegEncoder):
    descriptor = EncoderDescriptor(
        id="ffmpeg.eac3",
        display_name="FFmpeg E-AC-3",
        codecs=(Codec.EAC3,),
        output_formats=(OutputFormat.EAC3,),
        options=(
            OptionDefinition(
                "bitrate_kbps",
                "Bitrate",
                OptionKind.CHOICE,
                448,
                choices=_bitrate_choices(tuple(range(64, 6145, 32))),
            ),
            _custom_option(),
        ),
        required_ffmpeg_encoders=("eac3",),
        channel_layouts=DOLBY_LAYOUTS,
        sample_rate_choices=DOLBY_SAMPLE_RATES,
    )

    def build_plan(
        self, request: EncodingRequest, toolchain: Toolchain, temporary_output: Path
    ) -> ProcessPlan:
        self.validate(request)
        arguments = _base_arguments(request)
        arguments.extend(("-c:a", "eac3"))
        bitrate = _value(request, self.descriptor, "bitrate_kbps")
        if bitrate is not None:
            arguments.extend(("-b:a", f"{bitrate}k"))
        return _finish_plan(request, self.descriptor, toolchain, temporary_output, arguments)


class DtsEncoder(_FfmpegEncoder):
    descriptor = EncoderDescriptor(
        id="ffmpeg.dca",
        display_name="FFmpeg DTS (DCA)",
        codecs=(Codec.DTS,),
        output_formats=(OutputFormat.DTS,),
        options=(
            OptionDefinition(
                "bitrate_bps",
                "Bitrate",
                OptionKind.CHOICE,
                1411200,
                choices=_bitrate_choices(DTS_BITRATES, bps=True),
            ),
            _custom_option(),
        ),
        required_ffmpeg_encoders=("dca",),
        channel_layouts=DTS_LAYOUTS,
        sample_rate_choices=DTS_SAMPLE_RATES,
    )

    def build_plan(
        self, request: EncodingRequest, toolchain: Toolchain, temporary_output: Path
    ) -> ProcessPlan:
        self.validate(request)
        arguments = _base_arguments(request)
        arguments.extend(("-c:a", "dca", "-strict", "experimental"))
        bitrate = _value(request, self.descriptor, "bitrate_bps")
        if bitrate is not None:
            arguments.extend(("-b:a", str(bitrate)))
        return _finish_plan(request, self.descriptor, toolchain, temporary_output, arguments)


class AlacEncoder(_FfmpegEncoder):
    descriptor = EncoderDescriptor(
        id="ffmpeg.alac",
        display_name="FFmpeg ALAC",
        codecs=(Codec.ALAC,),
        output_formats=(OutputFormat.M4A,),
        options=(
            OptionDefinition("compression_level", "Compression level", OptionKind.INTEGER, 2, 0, 2),
            _custom_option(),
        ),
        required_ffmpeg_encoders=("alac",),
        channel_layouts=ALAC_LAYOUTS,
        sample_rate_choices=LOSSLESS_SAMPLE_RATE_CHOICES,
        sample_rate_range=(1, 2_147_483_647),
    )

    def build_plan(
        self, request: EncodingRequest, toolchain: Toolchain, temporary_output: Path
    ) -> ProcessPlan:
        self.validate(request)
        arguments = _base_arguments(request)
        arguments.extend(
            (
                "-c:a",
                "alac",
                "-compression_level",
                str(_integer_option(request, self.descriptor, "compression_level")),
            )
        )
        return _finish_plan(request, self.descriptor, toolchain, temporary_output, arguments)
