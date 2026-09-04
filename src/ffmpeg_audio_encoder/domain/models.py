from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import TypeAlias
from uuid import UUID, uuid4

JsonScalar: TypeAlias = str | int | float | bool | None


def _empty_options() -> dict[str, JsonScalar]:
    return {}


class Codec(StrEnum):
    OPUS = "opus"
    FLAC = "flac"
    AAC = "aac"
    MP3 = "mp3"
    AC3 = "ac3"
    EAC3 = "eac3"
    DTS = "dts"
    ALAC = "alac"

    def __str__(self) -> str:
        return {
            self.OPUS: "Opus",
            self.FLAC: "FLAC",
            self.AAC: "AAC",
            self.MP3: "MP3",
            self.AC3: "AC-3",
            self.EAC3: "E-AC-3",
            self.DTS: "DTS",
            self.ALAC: "ALAC",
        }[self]


class OutputFormat(StrEnum):
    OGG_OPUS = "ogg-opus"
    FLAC = "flac"
    M4A = "m4a"
    ADTS_AAC = "adts-aac"
    MP3 = "mp3"
    AC3 = "ac3"
    EAC3 = "eac3"
    DTS = "dts"

    @property
    def suffix(self) -> str:
        return {
            self.OGG_OPUS: ".opus",
            self.FLAC: ".flac",
            self.M4A: ".m4a",
            self.ADTS_AAC: ".aac",
            self.MP3: ".mp3",
            self.AC3: ".ac3",
            self.EAC3: ".eac3",
            self.DTS: ".dts",
        }[self]

    @property
    def ffmpeg_muxer(self) -> str:
        return {
            self.OGG_OPUS: "opus",
            self.FLAC: "flac",
            self.M4A: "ipod",
            self.ADTS_AAC: "adts",
            self.MP3: "mp3",
            self.AC3: "ac3",
            self.EAC3: "eac3",
            self.DTS: "dts",
        }[self]

    def __str__(self) -> str:
        return {
            self.OGG_OPUS: "Ogg Opus",
            self.FLAC: "FLAC",
            self.M4A: "M4A",
            self.ADTS_AAC: "Raw AAC (ADTS)",
            self.MP3: "MP3",
            self.AC3: "Raw AC-3",
            self.EAC3: "Raw E-AC-3",
            self.DTS: "Raw DTS",
        }[self]


class JobState(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ThemePreference(StrEnum):
    AUTOMATIC = "automatic"
    LIGHT = "light"
    DARK = "dark"

    def __str__(self) -> str:
        return self.value.title()


class OptionKind(StrEnum):
    INTEGER = "integer"
    DECIMAL = "decimal"
    CHOICE = "choice"
    TEXT = "text"


@dataclass(frozen=True, slots=True)
class OptionChoice:
    label: str
    value: JsonScalar


@dataclass(frozen=True, slots=True)
class OptionDefinition:
    key: str
    label: str
    kind: OptionKind
    default: JsonScalar
    minimum: float | None = None
    maximum: float | None = None
    suffix: str = ""
    choices: tuple[OptionChoice, ...] = ()
    tooltip: str = ""
    step: float = 1
    decimals: int = 0
    enabled_when_key: str | None = None
    enabled_when_values: tuple[JsonScalar, ...] = ()


@dataclass(frozen=True, slots=True)
class ChannelLayoutChoice:
    label: str
    value: str


@dataclass(frozen=True, slots=True)
class AudioStream:
    index: int
    ordinal: int
    codec_name: str
    channels: int | None = None
    channel_layout: str | None = None
    sample_rate: int | None = None
    language: str | None = None
    title: str | None = None
    duration_seconds: float | None = None

    @property
    def display_name(self) -> str:
        details = [self.codec_name.upper() or "Unknown codec"]
        if self.language:
            details.append(self.language)
        if self.channels:
            details.append(f"{self.channels}ch")
        if self.sample_rate:
            details.append(f"{self.sample_rate} Hz")
        return f"Audio {self.ordinal}: " + " · ".join(details)


@dataclass(frozen=True, slots=True)
class MediaAsset:
    path: Path
    audio_streams: tuple[AudioStream, ...]
    duration_seconds: float | None = None


@dataclass(frozen=True, slots=True)
class CommonAudioOptions:
    sample_rate: int | None = None
    channel_layout: str | None = None
    gain_db: float = 0.0
    tempo_ratio: float = 1.0
    delay_ms: float = 0.0


@dataclass(frozen=True, slots=True)
class EncodingRequest:
    input_path: Path
    stream: AudioStream
    encoder_id: str
    codec: Codec
    output_format: OutputFormat
    output_path: Path
    common: CommonAudioOptions = CommonAudioOptions()
    encoder_options: Mapping[str, JsonScalar] = field(default_factory=_empty_options)


@dataclass(frozen=True, slots=True)
class EncoderDescriptor:
    id: str
    display_name: str
    codecs: tuple[Codec, ...]
    output_formats: tuple[OutputFormat, ...]
    options: tuple[OptionDefinition, ...]
    required_tools: tuple[str, ...] = ("ffmpeg",)
    required_ffmpeg_encoders: tuple[str, ...] = ()
    required_ffmpeg_muxers: tuple[str, ...] = ()
    output_muxed_by_ffmpeg: bool = True
    channel_layouts: tuple[ChannelLayoutChoice, ...] = ()
    sample_rate_choices: tuple[int, ...] = ()
    sample_rate_range: tuple[int, int] | None = None


@dataclass(frozen=True, slots=True)
class ProcessStage:
    program: Path
    arguments: tuple[str, ...]
    progress_stream: str | None = None


@dataclass(frozen=True, slots=True)
class ProcessPlan:
    stages: tuple[ProcessStage, ...]
    temporary_output: Path
    final_output: Path
    duration_seconds: float | None

    def display_command(self) -> str:
        import subprocess

        return " | ".join(
            subprocess.list2cmdline([str(stage.program), *stage.arguments]) for stage in self.stages
        )


@dataclass(frozen=True, slots=True)
class Toolchain:
    ffmpeg: Path
    ffprobe: Path
    qaac: Path | None = None
    fdkaac: Path | None = None


@dataclass(slots=True)
class EncodeJob:
    request: EncodingRequest
    overwrite: bool = False
    id: UUID = field(default_factory=uuid4)
    state: JobState = JobState.QUEUED
    progress: float | None = 0.0
    status: str = "Waiting"
    error: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    started_at: datetime | None = None
    finished_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class EncoderPreset:
    name: str
    encoder_id: str
    codec: Codec
    output_format: OutputFormat
    common: CommonAudioOptions
    encoder_options: Mapping[str, JsonScalar]


@dataclass(frozen=True, slots=True)
class EncoderConfiguration:
    encoder_id: str
    codec: Codec
    output_format: OutputFormat
    common: CommonAudioOptions
    encoder_options: Mapping[str, JsonScalar]


@dataclass(frozen=True, slots=True)
class AppSettings:
    schema_version: int = 2
    ffmpeg_path: str | None = None
    ffprobe_path: str | None = None
    qaac_path: str | None = None
    fdkaac_path: str | None = None
    default_output_dir: str | None = None
    overwrite_default: bool = False
    theme: ThemePreference = ThemePreference.AUTOMATIC
    window_x: int | None = None
    window_y: int | None = None
    window_width: int = 1120
    window_height: int = 760
    draft_splitter_sizes: tuple[int, int] = (620, 460)
    main_splitter_sizes: tuple[int, int] = (460, 240)
    queue_panel_collapsed: bool = False
    last_configuration: EncoderConfiguration | None = None
