from __future__ import annotations

import math
import tempfile
from collections.abc import Mapping
from pathlib import Path

from ffmpeg_audio_encoder.domain.errors import ValidationError
from ffmpeg_audio_encoder.domain.models import (
    AudioStream,
    ChannelLayoutChoice,
    Codec,
    EncoderDescriptor,
    EncoderGroup,
    EncodingRequest,
    JsonScalar,
    OptionChoice,
    OptionDefinition,
    OptionKind,
    OutputFormat,
    ProcessPlan,
    ProcessStage,
    ProgressProtocol,
    Toolchain,
)
from ffmpeg_audio_encoder.encoders.ffmpeg import (
    custom_arguments,
    integer_option,
    string_option,
    validate_identity,
    validate_options,
)


def _choice(label: str, value: JsonScalar) -> OptionChoice:
    return OptionChoice(label, value)


DRC_CHOICES = tuple(
    _choice(label, value)
    for label, value in (
        ("Film standard", "film_standard"),
        ("Film light", "film_light"),
        ("Music standard", "music_standard"),
        ("Music light", "music_light"),
        ("Speech", "speech"),
    )
)
AC4_DRC_CHOICES = (*DRC_CHOICES, _choice("None", "none"))
DD_METERING_CHOICES = tuple(
    _choice(label, value)
    for label, value in (
        ("ITU-R BS.1770-1", "1770_1"),
        ("ITU-R BS.1770-2", "1770_2"),
        ("ITU-R BS.1770-3", "1770_3"),
        ("Leq(A)", "leqa"),
    )
)
FULL_METERING_CHOICES = (
    *DD_METERING_CHOICES[:-1],
    _choice("ITU-R BS.1770-4", "1770_4"),
    DD_METERING_CHOICES[-1],
)
_METERING_CLI_TOKENS = {
    "1770_1": "MODE_1770_1",
    "1770_2": "MODE_1770_2",
    "1770_3": "MODE_1770_3",
    "1770_4": "MODE_1770_4",
    "leqa": "MODE_LEQA",
}
STEREO_DOWNMIX_CHOICES = (
    _choice("Automatic", "not_indicated"),
    _choice("Lo/Ro", "loro"),
    _choice("Lt/Rt", "ltrt"),
    _choice("Dolby Pro Logic II", "dplii"),
)
DD_LAYOUTS = (
    ChannelLayoutChoice("Mono", "mono"),
    ChannelLayoutChoice("Stereo", "stereo"),
    ChannelLayoutChoice("5.1", "5.1"),
)
DDP_LAYOUTS = (*DD_LAYOUTS, ChannelLayoutChoice("7.1", "7.1"))
_CHANNEL_VALUES = {"mono": "1", "stereo": "2", "5.1": "6", "7.1": "8"}
DD_MONO_STEREO_BITRATES = (96, 112, 128, 160, 192, 224, 256, 320, 384, 448, 512, 576, 640)
DD_SURROUND_BITRATES = (224, 256, 320, 384, 448, 512, 576, 640)
DDP_STEREO_BITRATES = (
    96,
    104,
    112,
    120,
    128,
    144,
    160,
    176,
    192,
    200,
    208,
    216,
    224,
    232,
    240,
    248,
    256,
    272,
    288,
    304,
    320,
    336,
    352,
    368,
    384,
    400,
    448,
    512,
    576,
    640,
    704,
    768,
    832,
    896,
    960,
    1008,
    1024,
)
DDP_MONO_BITRATES = (32, 40, 48, 56, 64, 72, 80, 88, *DDP_STEREO_BITRATES)
DDP_SURROUND_BITRATES = tuple(value for value in DDP_STEREO_BITRATES if value >= 192)
DDP_SURROUNDEX_BITRATES = (384, 448, 504, 576, 640, 704, 768, 832, 896, 960, 1008, 1024)
DDP_BLURAY_BITRATES = (768, 1024, 1280, 1536, 1664)
ATMOS_STREAMING_BITRATES = (384, 448, 512, 576, 640, 768, 1024)
ATMOS_BLURAY_BITRATES = (1152, 1280, 1408, 1512, 1536, 1664)
AC4_BITRATES = (64, 72, 112, 144, 256, 320)
# The Dolby Encoding Engine rejects paths beyond the classic Windows MAX_PATH. The
# temporary ".part" name this application encodes into is longer than the final one,
# so it is the value worth checking.
DEE_MAX_PATH_LENGTH = 259

# How many DeeZy run logs to keep in the working directory.
DEEZY_LOG_RETENTION = 10

_CUSTOM_LEVELS = {
    "--lt-rt-center": {"+3", "+1.5", "0", "-1.5", "-3", "-4.5", "-6", "-inf"},
    "--lt-rt-surround": {"-1.5", "-3", "-4.5", "-6", "-inf"},
    "--lo-ro-center": {"+3", "+1.5", "0", "-1.5", "-3", "-4.5", "-6", "-inf"},
    "--lo-ro-surround": {"-1.5", "-3", "-4.5", "-6", "-inf"},
}


def _boolean(key: str, label: str, default: bool, tooltip: str = "") -> OptionDefinition:
    return OptionDefinition(key, label, OptionKind.BOOLEAN, default, tooltip=tooltip)


def _bitrate_choices(values: tuple[int, ...]) -> tuple[OptionChoice, ...]:
    return (
        _choice("Automatic (DeeZy default)", 0),
        *(_choice(f"{value} kb/s", value) for value in values),
    )


def _bitrate(*groups: tuple[int, ...]) -> OptionDefinition:
    values = tuple(sorted({value for group in groups for value in group}))
    return OptionDefinition(
        "bitrate_kbps",
        "Bitrate",
        OptionKind.CHOICE,
        0,
        choices=_bitrate_choices(values),
        tooltip="Only bitrates accepted by the selected DeeZy layout or profile are shown.",
    )


def _loudness_options(
    *, metering_default: str, full_metering: bool
) -> tuple[OptionDefinition, ...]:
    dialogue_metering_modes = (
        ("1770_2", "1770_3", "1770_4")
        if full_metering
        else (
            "1770_2",
            "1770_3",
        )
    )
    return (
        _boolean("dialogue_intelligence", "Dialogue Intelligence", True),
        OptionDefinition(
            "speech_threshold",
            "Speech threshold",
            OptionKind.INTEGER,
            15,
            0,
            100,
            "%",
            enabled_when_all=(
                ("dialogue_intelligence", (True,)),
                ("metering_mode", dialogue_metering_modes),
            ),
        ),
        OptionDefinition(
            "metering_mode",
            "Metering mode",
            OptionKind.CHOICE,
            metering_default,
            choices=FULL_METERING_CHOICES if full_metering else DD_METERING_CHOICES,
        ),
    )


def _dolby_options(
    *bitrate_groups: tuple[int, ...],
    metering_default: str = "1770_3",
    full_metering: bool = False,
) -> tuple[OptionDefinition, ...]:
    return (
        _bitrate(*bitrate_groups),
        OptionDefinition(
            "drc_line_mode",
            "Line-mode DRC",
            OptionKind.CHOICE,
            "film_light",
            choices=DRC_CHOICES,
        ),
        OptionDefinition(
            "drc_rf_mode",
            "RF-mode DRC",
            OptionKind.CHOICE,
            "film_light",
            choices=DRC_CHOICES,
        ),
        OptionDefinition(
            "custom_dialnorm",
            "Custom dialnorm",
            OptionKind.INTEGER,
            0,
            -31,
            0,
            " dB",
            tooltip="Use 0 to let DeeZy measure dialnorm.",
        ),
        *_loudness_options(
            metering_default=metering_default,
            full_metering=full_metering,
        ),
        OptionDefinition(
            "stereo_down_mix",
            "Stereo downmix",
            OptionKind.CHOICE,
            "loro",
            choices=STEREO_DOWNMIX_CHOICES,
        ),
    )


def _processing_options(*, upmix: bool) -> tuple[OptionDefinition, ...]:
    options = (
        _boolean("low_pass_filter", "Low-pass filter", True),
        _boolean("surround_3db", "Surround 3 dB attenuation", True),
        _boolean("surround_phase_shift", "Surround 90-degree phase shift", True),
    )
    if upmix:
        return (*options, _boolean("upmix_50_to_51", "Upmix 5.0 to 5.1", False))
    return options


def _custom_option() -> OptionDefinition:
    return OptionDefinition(
        "custom_args",
        "Advanced downmix metadata",
        OptionKind.TEXT,
        "",
        tooltip=(
            "Optional Lt/Rt or Lo/Ro level arguments. Inputs, outputs, dependencies, "
            "and managed encoder settings cannot be overridden."
        ),
    )


class _DeezyEncoder:
    descriptor: EncoderDescriptor
    format_command: str
    requires_truehdd = False
    fixed_channels: str | None = None
    allow_custom_downmix = True

    def default_options(self) -> dict[str, JsonScalar]:
        return {option.key: option.default for option in self.descriptor.options}

    def validate(self, request: EncodingRequest) -> None:
        validate_identity(request, self.descriptor)
        validate_options(request, self.descriptor)
        if request.common.sample_rate is not None:
            raise ValidationError("DeeZy manages sample rate internally")
        if not math.isclose(request.common.gain_db, 0.0):
            raise ValidationError("DeeZy does not support the common gain control")
        if not math.isclose(request.common.tempo_ratio, 1.0):
            raise ValidationError("DeeZy does not support the common tempo control")
        self._validate_mode(request)
        self._validate_bitrate(request)
        self._safe_custom_arguments(request)

    def option_choices(
        self,
        key: str,
        stream: AudioStream | None,
        channel_layout: str | None,
        encoder_options: Mapping[str, JsonScalar],
    ) -> tuple[OptionChoice, ...]:
        definition = next(option for option in self.descriptor.options if option.key == key)
        if key != "bitrate_kbps":
            return definition.choices
        return _bitrate_choices(
            self._allowed_bitrates(
                stream.channels if stream is not None else None,
                channel_layout,
                encoder_options,
            )
        )

    def _allowed_bitrates(
        self,
        source_channels: int | None,
        channel_layout: str | None,
        encoder_options: Mapping[str, JsonScalar],
    ) -> tuple[int, ...]:
        del source_channels, channel_layout, encoder_options
        definition = next(
            option for option in self.descriptor.options if option.key == "bitrate_kbps"
        )
        return tuple(
            choice.value
            for choice in definition.choices
            if isinstance(choice.value, int)
            and not isinstance(choice.value, bool)
            and choice.value != 0
        )

    def _validate_bitrate(self, request: EncodingRequest) -> None:
        bitrate = integer_option(request, self.descriptor, "bitrate_kbps")
        if not bitrate:
            return
        allowed = self._allowed_bitrates(
            request.stream.channels,
            request.common.channel_layout,
            request.encoder_options,
        )
        if bitrate not in allowed:
            allowed_text = ", ".join(str(value) for value in allowed)
            raise ValidationError(
                f"Bitrate {bitrate} kb/s is invalid for this DeeZy configuration; "
                f"choose Automatic or one of: {allowed_text} kb/s"
            )

    def _validate_mode(self, request: EncodingRequest) -> None:
        desired_layout = request.common.channel_layout
        if desired_layout is None or request.stream.channels is None:
            return
        desired_channels = int(_CHANNEL_VALUES[desired_layout])
        if desired_channels <= request.stream.channels:
            return
        allow_50_to_51 = (
            desired_channels == 6
            and request.stream.channels == 5
            and any(option.key == "upmix_50_to_51" for option in self.descriptor.options)
            and self._bool_option(request, "upmix_50_to_51")
        )
        if not allow_50_to_51:
            raise ValidationError(
                f"DeeZy cannot up-mix {request.stream.channels} channels to "
                f"{desired_channels} channels"
            )

    def build_plan(
        self, request: EncodingRequest, toolchain: Toolchain, temporary_output: Path
    ) -> ProcessPlan:
        self.validate(request)
        if toolchain.deezy is None:
            raise ValidationError("DeeZy is not configured or available on PATH")
        if toolchain.dee is None:
            raise ValidationError("Dolby Encoding Engine is not configured or available")
        if self.requires_truehdd and toolchain.truehdd is None:
            raise ValidationError("TrueHDD is required for DeeZy Atmos and AC-4 encoding")
        if len(str(temporary_output)) > DEE_MAX_PATH_LENGTH:
            raise ValidationError(
                "The Dolby Encoding Engine cannot write paths longer than "
                f"{DEE_MAX_PATH_LENGTH} characters; choose a shorter output "
                "name or a shallower destination folder"
            )

        default_scratch = Path(tempfile.gettempdir()) / "FFmpegAudioEncoder"
        work_dir = toolchain.deezy_work_dir or default_scratch / "deezy-work"
        # Without --temp-dir DeeZy writes its intermediates into a "<stem>_deezy"
        # folder beside the source file. For Atmos and AC-4 that is a decode the size
        # of the source track, on whichever drive the user's media happens to live,
        # and it survives a cancelled run.
        temp_dir = toolchain.deezy_temp_dir or default_scratch / "deezy-temp"
        arguments = [
            "--no-progress-bars",
            "encode",
            self.format_command,
            "--ffmpeg",
            str(toolchain.ffmpeg),
            "--dee",
            str(toolchain.dee),
        ]
        if self.requires_truehdd and toolchain.truehdd is not None:
            arguments.extend(("--truehdd", str(toolchain.truehdd)))
        arguments.extend(
            (
                f"--track-index=s:{request.stream.index}",
                f"--delay={request.common.delay_ms:g}ms",
                "--working-dir",
                str(work_dir),
                "--temp-dir",
                str(temp_dir),
                # DeeZy never prunes its own log folder; bound it rather than let a
                # directory we chose for it grow without limit.
                "--max-logs",
                str(DEEZY_LOG_RETENTION),
                "--overwrite",
                "--output",
                str(temporary_output),
            )
        )
        arguments.extend(self._managed_arguments(request))
        arguments.extend(self._safe_custom_arguments(request))
        arguments.append(str(request.input_path))
        return ProcessPlan(
            (
                ProcessStage(
                    toolchain.deezy,
                    tuple(arguments),
                    "stderr",
                    ProgressProtocol.DEEZY,
                    terminate_tree=True,
                ),
            ),
            temporary_output,
            request.output_path,
            request.stream.duration_seconds,
        )

    def _managed_arguments(self, request: EncodingRequest) -> list[str]:
        arguments: list[str] = []
        bitrate = integer_option(request, self.descriptor, "bitrate_kbps")
        if bitrate:
            arguments.extend(("--bitrate", str(bitrate)))
        if request.common.channel_layout is not None:
            arguments.extend(("--channels", _CHANNEL_VALUES[request.common.channel_layout]))
        elif self.fixed_channels is not None:
            arguments.extend(("--channels", self.fixed_channels))
        self._append_common_dolby(arguments, request)
        return arguments

    def _append_common_dolby(
        self, arguments: list[str], request: EncodingRequest, *, include_drc: bool = True
    ) -> None:
        if include_drc:
            arguments.extend(
                (
                    "--drc-line-mode",
                    string_option(request, self.descriptor, "drc_line_mode"),
                    "--drc-rf-mode",
                    string_option(request, self.descriptor, "drc_rf_mode"),
                    "--custom-dialnorm",
                    str(integer_option(request, self.descriptor, "custom_dialnorm")),
                )
            )
        metering_mode = string_option(request, self.descriptor, "metering_mode")
        arguments.extend(("--metering-mode", self._metering_cli_token(metering_mode)))
        if metering_mode not in {"1770_1", "leqa"}:
            if self._bool_option(request, "dialogue_intelligence"):
                arguments.extend(
                    (
                        "--speech-threshold",
                        str(integer_option(request, self.descriptor, "speech_threshold")),
                    )
                )
            else:
                arguments.append("--no-dialogue-intelligence")
        if include_drc:
            arguments.extend(
                ("--stereo-down-mix", string_option(request, self.descriptor, "stereo_down_mix"))
            )

    @staticmethod
    def _metering_cli_token(value: str) -> str:
        try:
            return _METERING_CLI_TOKENS[value]
        except KeyError as exc:
            raise ValidationError(f"Unsupported DeeZy metering mode: {value}") from exc

    def _append_processing(self, arguments: list[str], request: EncodingRequest) -> None:
        for key, flag in (
            ("low_pass_filter", "--no-low-pass-filter"),
            ("surround_3db", "--no-surround-3db"),
            ("surround_phase_shift", "--no-surround-90-deg-phase-shift"),
        ):
            if not self._bool_option(request, key):
                arguments.append(flag)
        supports_upmix = any(option.key == "upmix_50_to_51" for option in self.descriptor.options)
        if supports_upmix and self._bool_option(request, "upmix_50_to_51"):
            arguments.append("--upmix-50-to-51")

    def _bool_option(self, request: EncodingRequest, key: str) -> bool:
        definition = next(option for option in self.descriptor.options if option.key == key)
        value = request.encoder_options.get(key, definition.default)
        if not isinstance(value, bool):
            raise ValidationError(f"{definition.label} must be enabled or disabled")
        return value

    def _safe_custom_arguments(self, request: EncodingRequest) -> list[str]:
        values = custom_arguments(request, self.descriptor)
        if not values:
            return []
        if not self.allow_custom_downmix:
            raise ValidationError("This DeeZy mode does not support custom downmix metadata")
        validated: list[str] = []
        index = 0
        while index < len(values):
            flag = values[index]
            allowed = _CUSTOM_LEVELS.get(flag)
            if allowed is None or index + 1 >= len(values):
                raise ValidationError(
                    "Advanced DeeZy arguments may only set Lt/Rt and Lo/Ro metadata levels"
                )
            value = values[index + 1]
            if value not in allowed:
                raise ValidationError(f"Invalid value {value!r} for {flag}")
            validated.extend((flag, value))
            index += 2
        return validated


class DeezyDdEncoder(_DeezyEncoder):
    format_command = "dd"
    descriptor = EncoderDescriptor(
        id="deezy.dd",
        display_name="DeeZy DD (Dolby Digital)",
        codecs=(Codec.AC3,),
        output_formats=(OutputFormat.AC3,),
        options=(
            *_dolby_options(DD_MONO_STEREO_BITRATES, DD_SURROUND_BITRATES),
            *_processing_options(upmix=True),
            _custom_option(),
        ),
        group=EncoderGroup.DEEZY,
        required_tools=("ffmpeg", "deezy", "dee"),
        output_muxed_by_ffmpeg=False,
        channel_layouts=DD_LAYOUTS,
        default_channel_layout_label="Auto",
        supports_sample_rate=False,
        supports_gain=False,
        supports_tempo=False,
    )

    def _managed_arguments(self, request: EncodingRequest) -> list[str]:
        arguments = super()._managed_arguments(request)
        self._append_processing(arguments, request)
        return arguments

    def _allowed_bitrates(
        self,
        source_channels: int | None,
        channel_layout: str | None,
        encoder_options: Mapping[str, JsonScalar],
    ) -> tuple[int, ...]:
        del encoder_options
        if channel_layout in {"mono", "stereo"}:
            return DD_MONO_STEREO_BITRATES
        if channel_layout == "5.1":
            return DD_SURROUND_BITRATES
        if source_channels is None:
            return tuple(sorted({*DD_MONO_STEREO_BITRATES, *DD_SURROUND_BITRATES}))
        return DD_MONO_STEREO_BITRATES if source_channels < 6 else DD_SURROUND_BITRATES


class DeezyDdpEncoder(_DeezyEncoder):
    format_command = "ddp"
    descriptor = EncoderDescriptor(
        id="deezy.ddp",
        display_name="DeeZy DDP (Dolby Digital Plus)",
        codecs=(Codec.EAC3,),
        output_formats=(OutputFormat.EAC3,),
        options=(
            *_dolby_options(
                DDP_MONO_BITRATES,
                DDP_STEREO_BITRATES,
                DDP_SURROUND_BITRATES,
                DDP_SURROUNDEX_BITRATES,
            ),
            *_processing_options(upmix=True),
            _custom_option(),
        ),
        group=EncoderGroup.DEEZY,
        required_tools=("ffmpeg", "deezy", "dee"),
        output_muxed_by_ffmpeg=False,
        channel_layouts=DDP_LAYOUTS,
        default_channel_layout_label="Auto",
        supports_sample_rate=False,
        supports_gain=False,
        supports_tempo=False,
    )

    def _managed_arguments(self, request: EncodingRequest) -> list[str]:
        arguments = super()._managed_arguments(request)
        self._append_processing(arguments, request)
        return arguments

    def _allowed_bitrates(
        self,
        source_channels: int | None,
        channel_layout: str | None,
        encoder_options: Mapping[str, JsonScalar],
    ) -> tuple[int, ...]:
        del encoder_options
        by_layout = {
            "mono": DDP_MONO_BITRATES,
            "stereo": DDP_STEREO_BITRATES,
            "5.1": DDP_SURROUND_BITRATES,
            "7.1": DDP_SURROUNDEX_BITRATES,
        }
        if channel_layout in by_layout:
            return by_layout[channel_layout]
        if source_channels is None:
            return tuple(sorted({value for group in by_layout.values() for value in group}))
        if source_channels == 1:
            return DDP_MONO_BITRATES
        if source_channels < 6:
            return DDP_STEREO_BITRATES
        if source_channels == 6:
            return DDP_SURROUND_BITRATES
        return DDP_SURROUNDEX_BITRATES


class DeezyDdpBlurayEncoder(_DeezyEncoder):
    format_command = "ddp-bluray"
    fixed_channels = "8"
    descriptor = EncoderDescriptor(
        id="deezy.ddp_bluray",
        display_name="DeeZy DDP-BluRay 7.1",
        codecs=(Codec.EAC3,),
        output_formats=(OutputFormat.EAC3,),
        options=(
            *_dolby_options(DDP_BLURAY_BITRATES),
            *_processing_options(upmix=False),
            _custom_option(),
        ),
        group=EncoderGroup.DEEZY,
        required_tools=("ffmpeg", "deezy", "dee"),
        output_muxed_by_ffmpeg=False,
        supports_sample_rate=False,
        supports_channel_layout=False,
        supports_gain=False,
        supports_tempo=False,
    )

    def _managed_arguments(self, request: EncodingRequest) -> list[str]:
        arguments = super()._managed_arguments(request)
        self._append_processing(arguments, request)
        return arguments

    def _validate_mode(self, request: EncodingRequest) -> None:
        if request.stream.channels is not None and request.stream.channels < 8:
            raise ValidationError("DeeZy DDP-BluRay requires at least 8 source channels")

    def _allowed_bitrates(
        self,
        source_channels: int | None,
        channel_layout: str | None,
        encoder_options: Mapping[str, JsonScalar],
    ) -> tuple[int, ...]:
        del source_channels, channel_layout, encoder_options
        return DDP_BLURAY_BITRATES


class DeezyAtmosEncoder(_DeezyEncoder):
    format_command = "atmos"
    requires_truehdd = True
    descriptor = EncoderDescriptor(
        id="deezy.atmos",
        display_name="DeeZy Dolby Digital Plus Atmos",
        codecs=(Codec.ATMOS,),
        output_formats=(OutputFormat.EAC3,),
        options=(
            *_dolby_options(
                ATMOS_STREAMING_BITRATES,
                ATMOS_BLURAY_BITRATES,
                metering_default="1770_4",
                full_metering=True,
            ),
            OptionDefinition(
                "atmos_mode",
                "Atmos mode",
                OptionKind.CHOICE,
                "streaming",
                choices=(
                    _choice("Streaming (5.1)", "streaming"),
                    _choice("BluRay (7.1)", "bluray"),
                ),
            ),
            OptionDefinition(
                "thd_warp_mode",
                "TrueHD warp mode",
                OptionKind.CHOICE,
                "normal",
                choices=(
                    _choice("Normal", "normal"),
                    _choice("Warping", "warping"),
                    _choice("Pro Logic IIx", "dplii"),
                    _choice("Lo/Ro", "loro"),
                ),
            ),
            _boolean("bed_conform", "Bed conformance", False),
            _custom_option(),
        ),
        group=EncoderGroup.DEEZY,
        required_tools=("ffmpeg", "deezy", "dee", "truehdd"),
        output_muxed_by_ffmpeg=False,
        supports_sample_rate=False,
        supports_channel_layout=False,
        supports_gain=False,
        supports_tempo=False,
    )

    def _managed_arguments(self, request: EncodingRequest) -> list[str]:
        arguments = super()._managed_arguments(request)
        arguments.extend(
            (
                "--atmos-mode",
                string_option(request, self.descriptor, "atmos_mode"),
                "--thd-warp-mode",
                string_option(request, self.descriptor, "thd_warp_mode"),
            )
        )
        if self._bool_option(request, "bed_conform"):
            arguments.append("--bed-conform")
        return arguments

    def _validate_mode(self, request: EncodingRequest) -> None:
        if request.stream.channels is None:
            return
        mode = string_option(request, self.descriptor, "atmos_mode")
        desired_channels = 6 if mode == "streaming" else 8
        if request.stream.channels < desired_channels:
            raise ValidationError(
                f"DeeZy Atmos {mode} mode requires at least {desired_channels} source channels"
            )

    def _allowed_bitrates(
        self,
        source_channels: int | None,
        channel_layout: str | None,
        encoder_options: Mapping[str, JsonScalar],
    ) -> tuple[int, ...]:
        del source_channels, channel_layout
        mode = encoder_options.get("atmos_mode", "streaming")
        return ATMOS_BLURAY_BITRATES if mode == "bluray" else ATMOS_STREAMING_BITRATES


class DeezyAc4Encoder(_DeezyEncoder):
    format_command = "ac4"
    requires_truehdd = True
    allow_custom_downmix = False
    descriptor = EncoderDescriptor(
        id="deezy.ac4",
        display_name="DeeZy Dolby AC-4",
        codecs=(Codec.AC4,),
        output_formats=(OutputFormat.AC4,),
        options=(
            _bitrate(AC4_BITRATES),
            *_loudness_options(metering_default="1770_4", full_metering=True),
            OptionDefinition(
                "encoding_profile",
                "Encoding profile",
                OptionKind.CHOICE,
                "ims",
                choices=(_choice("IMS", "ims"), _choice("IMS Music", "ims_music")),
            ),
            _boolean("ims_legacy_presentation", "IMS legacy presentation", False),
            *(
                OptionDefinition(
                    key,
                    label,
                    OptionKind.CHOICE,
                    "film_light",
                    choices=AC4_DRC_CHOICES,
                )
                for key, label in (
                    ("ddp_drc", "DDP DRC"),
                    ("flat_panel_drc", "Flat-panel DRC"),
                    ("home_theatre_drc", "Home-theatre DRC"),
                    ("portable_headphones_drc", "Portable-headphones DRC"),
                    ("portable_speakers_drc", "Portable-speakers DRC"),
                )
            ),
            OptionDefinition(
                "thd_warp_mode",
                "TrueHD warp mode",
                OptionKind.CHOICE,
                "normal",
                choices=(
                    _choice("Normal", "normal"),
                    _choice("Warping", "warping"),
                    _choice("Pro Logic IIx", "dplii"),
                    _choice("Lo/Ro", "loro"),
                ),
            ),
            _boolean("bed_conform", "Bed conformance", False),
        ),
        group=EncoderGroup.DEEZY,
        required_tools=("ffmpeg", "deezy", "dee", "truehdd"),
        output_muxed_by_ffmpeg=False,
        supports_sample_rate=False,
        supports_channel_layout=False,
        supports_gain=False,
        supports_tempo=False,
    )

    def _managed_arguments(self, request: EncodingRequest) -> list[str]:
        arguments: list[str] = []
        bitrate = integer_option(request, self.descriptor, "bitrate_kbps")
        if bitrate:
            arguments.extend(("--bitrate", str(bitrate)))
        self._append_common_dolby(arguments, request, include_drc=False)
        arguments.extend(
            ("--encoding-profile", string_option(request, self.descriptor, "encoding_profile"))
        )
        if self._bool_option(request, "ims_legacy_presentation"):
            arguments.append("--ims-legacy-presentation")
        for key, flag in (
            ("ddp_drc", "--ddp-drc"),
            ("flat_panel_drc", "--flat-panel-drc"),
            ("home_theatre_drc", "--home-theatre-drc"),
            ("portable_headphones_drc", "--portable-headphones-drc"),
            ("portable_speakers_drc", "--portable-speakers-drc"),
        ):
            arguments.extend((flag, string_option(request, self.descriptor, key)))
        arguments.extend(
            ("--thd-warp-mode", string_option(request, self.descriptor, "thd_warp_mode"))
        )
        if self._bool_option(request, "bed_conform"):
            arguments.append("--bed-conform")
        return arguments

    def _validate_mode(self, request: EncodingRequest) -> None:
        if (
            request.stream.channels is not None
            and request.stream.channels < 6
            and request.stream.codec_name.casefold() != "truehd"
        ):
            raise ValidationError(
                "DeeZy AC-4 requires a source with at least 6 channels or TrueHD Atmos"
            )

    def _allowed_bitrates(
        self,
        source_channels: int | None,
        channel_layout: str | None,
        encoder_options: Mapping[str, JsonScalar],
    ) -> tuple[int, ...]:
        del source_channels, channel_layout, encoder_options
        return AC4_BITRATES
