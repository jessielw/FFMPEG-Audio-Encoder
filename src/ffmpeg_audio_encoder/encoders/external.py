from __future__ import annotations

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
from ffmpeg_audio_encoder.encoders.ffmpeg import (
    AAC_SAMPLE_RATES,
    COMMON_LAYOUTS,
    adjusted_duration,
    base_arguments,
    custom_arguments,
    integer_option,
    string_option,
    validate_identity,
    validate_options,
)


def _choice(label: str, value: JsonScalar) -> OptionChoice:
    return OptionChoice(label, value)


FDK_LAYOUTS = (
    ChannelLayoutChoice("Mono", "mono"),
    ChannelLayoutChoice("Stereo", "stereo"),
    ChannelLayoutChoice("3.0", "3.0"),
    ChannelLayoutChoice("4.0", "4.0"),
    ChannelLayoutChoice("5.0", "5.0"),
    ChannelLayoutChoice("5.1", "5.1"),
    ChannelLayoutChoice("7.1", "7.1"),
)


def _custom_option(tool_name: str) -> OptionDefinition:
    return OptionDefinition(
        "custom_args",
        f"Custom {tool_name} arguments",
        OptionKind.TEXT,
        "",
        tooltip=(
            f"Advanced: appended after managed {tool_name} settings. "
            "Arguments are never run in a shell."
        ),
    )


def _pcm_stage(request: EncodingRequest, toolchain: Toolchain) -> ProcessStage:
    arguments = base_arguments(request)
    arguments.extend(
        (
            "-c:a",
            "pcm_s16le",
            "-progress",
            "pipe:2",
            "-nostats",
            "-f",
            "wav",
            "pipe:1",
        )
    )
    return ProcessStage(toolchain.ffmpeg, tuple(arguments), "stderr")


def _external_plan(
    request: EncodingRequest,
    toolchain: Toolchain,
    temporary_output: Path,
    encoder: Path,
    arguments: list[str],
) -> ProcessPlan:
    return ProcessPlan(
        (
            _pcm_stage(request, toolchain),
            ProcessStage(encoder, tuple(arguments)),
        ),
        temporary_output,
        request.output_path,
        adjusted_duration(request),
    )


class _ExternalAacEncoder:
    descriptor: EncoderDescriptor

    def default_options(self) -> dict[str, JsonScalar]:
        return {option.key: option.default for option in self.descriptor.options}

    def validate(self, request: EncodingRequest) -> None:
        validate_identity(request, self.descriptor)
        validate_options(request, self.descriptor)


class QaacEncoder(_ExternalAacEncoder):
    descriptor = EncoderDescriptor(
        id="qaac.aac",
        display_name="qaac (Apple AAC)",
        codecs=(Codec.AAC,),
        output_formats=(OutputFormat.M4A, OutputFormat.ADTS_AAC),
        options=(
            OptionDefinition(
                "profile",
                "Profile",
                OptionKind.CHOICE,
                "lc",
                choices=(
                    _choice("AAC-LC", "lc"),
                    _choice("HE-AAC", "he"),
                ),
            ),
            OptionDefinition(
                "rate_control",
                "Rate control",
                OptionKind.CHOICE,
                "tvbr",
                choices=(
                    _choice("True VBR", "tvbr"),
                    _choice("Constrained VBR", "cvbr"),
                    _choice("Average bitrate", "abr"),
                    _choice("Constant bitrate", "cbr"),
                ),
            ),
            OptionDefinition(
                "tvbr_quality",
                "TVBR quality",
                OptionKind.INTEGER,
                90,
                0,
                127,
                enabled_when_key="rate_control",
                enabled_when_values=("tvbr",),
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
                enabled_when_values=("cvbr", "abr", "cbr"),
            ),
            OptionDefinition(
                "encoder_quality",
                "Encoder quality",
                OptionKind.CHOICE,
                2,
                choices=(
                    _choice("Best", 2),
                    _choice("High", 1),
                    _choice("Fast", 0),
                ),
            ),
            _custom_option("qaac"),
        ),
        required_tools=("ffmpeg", "qaac"),
        required_ffmpeg_muxers=("wav",),
        output_muxed_by_ffmpeg=False,
        channel_layouts=COMMON_LAYOUTS,
        sample_rate_choices=AAC_SAMPLE_RATES,
    )

    def validate(self, request: EncodingRequest) -> None:
        super().validate(request)
        if (
            string_option(request, self.descriptor, "profile") == "he"
            and string_option(request, self.descriptor, "rate_control") == "tvbr"
        ):
            raise ValidationError("qaac True VBR is not available for HE-AAC")

    def build_plan(
        self, request: EncodingRequest, toolchain: Toolchain, temporary_output: Path
    ) -> ProcessPlan:
        self.validate(request)
        if toolchain.qaac is None:
            raise ValidationError("qaac is not configured or available on PATH")
        arguments = ["--ignorelength"]
        if string_option(request, self.descriptor, "profile") == "he":
            arguments.append("--he")
        mode = string_option(request, self.descriptor, "rate_control")
        mode_flag = {
            "tvbr": "--tvbr",
            "cvbr": "--cvbr",
            "abr": "--abr",
            "cbr": "--cbr",
        }[mode]
        value = (
            integer_option(request, self.descriptor, "tvbr_quality")
            if mode == "tvbr"
            else integer_option(request, self.descriptor, "bitrate_kbps")
        )
        arguments.extend(
            (
                mode_flag,
                str(value),
                "--quality",
                str(integer_option(request, self.descriptor, "encoder_quality")),
            )
        )
        if request.output_format is OutputFormat.ADTS_AAC:
            arguments.append("--adts")
        arguments.extend(custom_arguments(request, self.descriptor))
        arguments.extend(("-o", str(temporary_output), "-"))
        return _external_plan(request, toolchain, temporary_output, toolchain.qaac, arguments)


class FdkAacEncoder(_ExternalAacEncoder):
    descriptor = EncoderDescriptor(
        id="fdkaac.aac",
        display_name="fdkaac (Fraunhofer FDK AAC)",
        codecs=(Codec.AAC,),
        output_formats=(OutputFormat.M4A, OutputFormat.ADTS_AAC),
        options=(
            OptionDefinition(
                "profile",
                "Profile",
                OptionKind.CHOICE,
                2,
                choices=(
                    _choice("AAC-LC", 2),
                    _choice("HE-AAC", 5),
                    _choice("HE-AAC v2", 29),
                ),
            ),
            OptionDefinition(
                "rate_control",
                "Rate control",
                OptionKind.CHOICE,
                "cbr",
                choices=(
                    _choice("Constant bitrate", "cbr"),
                    _choice("Variable quality", "vbr"),
                ),
            ),
            OptionDefinition(
                "bitrate_kbps",
                "Bitrate",
                OptionKind.INTEGER,
                192,
                8,
                1024,
                " kb/s",
                enabled_when_key="rate_control",
                enabled_when_values=("cbr",),
            ),
            OptionDefinition(
                "vbr_quality",
                "VBR quality",
                OptionKind.INTEGER,
                3,
                1,
                5,
                enabled_when_key="rate_control",
                enabled_when_values=("vbr",),
            ),
            OptionDefinition(
                "afterburner",
                "Afterburner",
                OptionKind.CHOICE,
                1,
                choices=(
                    _choice("On", 1),
                    _choice("Off", 0),
                ),
            ),
            _custom_option("fdkaac"),
        ),
        required_tools=("ffmpeg", "fdkaac"),
        required_ffmpeg_muxers=("wav",),
        output_muxed_by_ffmpeg=False,
        channel_layouts=FDK_LAYOUTS,
        sample_rate_choices=AAC_SAMPLE_RATES,
    )

    def validate(self, request: EncodingRequest) -> None:
        super().validate(request)
        profile = integer_option(request, self.descriptor, "profile")
        mode = string_option(request, self.descriptor, "rate_control")
        if mode == "vbr" and profile != 2:
            raise ValidationError("fdkaac VBR is only supported with the AAC-LC profile")
        channels = request.stream.channels
        if request.common.channel_layout is not None:
            channels = {
                "mono": 1,
                "stereo": 2,
                "3.0": 3,
                "4.0": 4,
                "5.0": 5,
                "5.1": 6,
                "7.1": 8,
            }.get(request.common.channel_layout)
        if profile == 29 and channels not in {None, 2}:
            raise ValidationError("fdkaac HE-AAC v2 requires stereo audio")

    def build_plan(
        self, request: EncodingRequest, toolchain: Toolchain, temporary_output: Path
    ) -> ProcessPlan:
        self.validate(request)
        if toolchain.fdkaac is None:
            raise ValidationError("fdkaac is not configured or available on PATH")
        mode = string_option(request, self.descriptor, "rate_control")
        arguments = [
            "--ignorelength",
            "--profile",
            str(integer_option(request, self.descriptor, "profile")),
            "--bitrate-mode",
            (
                "0"
                if mode == "cbr"
                else str(integer_option(request, self.descriptor, "vbr_quality"))
            ),
            "--afterburner",
            str(integer_option(request, self.descriptor, "afterburner")),
            "--transport-format",
            "2" if request.output_format is OutputFormat.ADTS_AAC else "0",
        ]
        if mode == "cbr":
            arguments.extend(
                (
                    "--bitrate",
                    str(integer_option(request, self.descriptor, "bitrate_kbps")),
                )
            )
        arguments.extend(custom_arguments(request, self.descriptor))
        arguments.extend(("-o", str(temporary_output), "-"))
        return _external_plan(request, toolchain, temporary_output, toolchain.fdkaac, arguments)
