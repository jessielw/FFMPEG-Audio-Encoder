from __future__ import annotations

import json
from contextlib import suppress
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from platformdirs import user_config_path

from ffmpeg_audio_encoder.domain.models import (
    AppSettings,
    AudioStream,
    Codec,
    CommonAudioOptions,
    EncodeJob,
    EncoderPreset,
    EncodingRequest,
    JobState,
    JsonScalar,
    OutputFormat,
    ThemePreference,
)

SCHEMA_VERSION = 1
PRESET_SCHEMA_VERSION = 2
JOB_SCHEMA_VERSION = 1


def default_config_directory() -> Path:
    return user_config_path("FFmpegAudioEncoder", appauthor=False)


def _atomic_json_write(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


class SettingsRepository:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or default_config_directory() / "settings.json"

    def load(self) -> AppSettings:
        if not self.path.is_file():
            return AppSettings()
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(raw, dict) or raw.get("schema_version") != SCHEMA_VERSION:
                return AppSettings()
            return AppSettings(
                ffmpeg_path=_optional_string(raw.get("ffmpeg_path")),
                ffprobe_path=_optional_string(raw.get("ffprobe_path")),
                default_output_dir=_optional_string(raw.get("default_output_dir")),
                overwrite_default=bool(raw.get("overwrite_default", False)),
                theme=ThemePreference(str(raw.get("theme", ThemePreference.AUTOMATIC))),
                window_x=_optional_int(raw.get("window_x")),
                window_y=_optional_int(raw.get("window_y")),
                window_width=_positive_int(raw.get("window_width"), 1120),
                window_height=_positive_int(raw.get("window_height"), 760),
                draft_splitter_sizes=_splitter_sizes(raw.get("draft_splitter_sizes"), (620, 460)),
                main_splitter_sizes=_splitter_sizes(raw.get("main_splitter_sizes"), (460, 240)),
                queue_panel_collapsed=bool(raw.get("queue_panel_collapsed", False)),
            )
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            return AppSettings()

    def save(self, settings: AppSettings) -> None:
        payload = asdict(settings)
        payload["theme"] = settings.theme.value
        _atomic_json_write(self.path, payload)


class PresetRepository:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or default_config_directory() / "presets.json"

    def load(self) -> list[EncoderPreset]:
        if not self.path.is_file():
            return []
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(raw, dict) or raw.get("schema_version") not in {
                SCHEMA_VERSION,
                PRESET_SCHEMA_VERSION,
            }:
                return []
            items = raw.get("presets")
            if not isinstance(items, list):
                return []
            presets = [self._decode(item) for item in items if isinstance(item, dict)]
            return sorted(presets, key=lambda preset: preset.name.casefold())
        except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError):
            return []

    def save(self, presets: list[EncoderPreset]) -> None:
        _atomic_json_write(
            self.path,
            {
                "schema_version": PRESET_SCHEMA_VERSION,
                "presets": [self._encode(preset) for preset in presets],
            },
        )

    @staticmethod
    def _encode(preset: EncoderPreset) -> dict[str, object]:
        return {
            "name": preset.name,
            "encoder_id": preset.encoder_id,
            "codec": preset.codec.value,
            "output_format": preset.output_format.value,
            "common": asdict(preset.common),
            "encoder_options": dict(preset.encoder_options),
        }

    @staticmethod
    def _decode(raw: dict[str, Any]) -> EncoderPreset:
        raw_common = raw.get("common")
        common = raw_common if isinstance(raw_common, dict) else {}
        raw_options = raw.get("encoder_options")
        options: dict[str, JsonScalar] = {}
        if isinstance(raw_options, dict):
            for key, value in raw_options.items():
                if isinstance(key, str) and (
                    value is None or isinstance(value, (str, int, float, bool))
                ):
                    options[key] = value
        return EncoderPreset(
            name=str(raw["name"]),
            encoder_id=str(raw["encoder_id"]),
            codec=Codec(str(raw["codec"])),
            output_format=OutputFormat(str(raw["output_format"])),
            common=CommonAudioOptions(
                sample_rate=_optional_int(common.get("sample_rate")),
                channel_layout=_decode_channel_layout(common),
            ),
            encoder_options=options,
        )


class JobRepository:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or default_config_directory() / "jobs.json"

    def load(self) -> list[EncodeJob]:
        if not self.path.is_file():
            return []
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(raw, dict) or raw.get("schema_version") != JOB_SCHEMA_VERSION:
                self._quarantine()
                return []
            items = raw.get("jobs")
            if not isinstance(items, list) or any(not isinstance(item, dict) for item in items):
                self._quarantine()
                return []
            return [self._decode(item) for item in items]
        except (ValueError, TypeError, KeyError, json.JSONDecodeError):
            self._quarantine()
            return []
        except OSError:
            return []

    def save(self, jobs: list[EncodeJob]) -> None:
        _atomic_json_write(
            self.path,
            {
                "schema_version": JOB_SCHEMA_VERSION,
                "jobs": [self._encode(job) for job in jobs],
            },
        )

    def _quarantine(self) -> None:
        timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
        quarantine = self.path.with_name(f"{self.path.stem}.corrupt-{timestamp}{self.path.suffix}")
        with suppress(OSError):
            self.path.replace(quarantine)

    @staticmethod
    def _encode(job: EncodeJob) -> dict[str, object]:
        request = job.request
        stream = request.stream
        return {
            "id": str(job.id),
            "state": job.state.value,
            "overwrite": job.overwrite,
            "error": job.error,
            "created_at": job.created_at.isoformat(),
            "started_at": _encode_datetime(job.started_at),
            "finished_at": _encode_datetime(job.finished_at),
            "request": {
                "input_path": str(request.input_path),
                "output_path": str(request.output_path),
                "encoder_id": request.encoder_id,
                "codec": request.codec.value,
                "output_format": request.output_format.value,
                "common": asdict(request.common),
                "encoder_options": dict(request.encoder_options),
                "stream": {
                    "index": stream.index,
                    "ordinal": stream.ordinal,
                    "codec_name": stream.codec_name,
                    "channels": stream.channels,
                    "channel_layout": stream.channel_layout,
                    "sample_rate": stream.sample_rate,
                    "language": stream.language,
                    "title": stream.title,
                    "duration_seconds": stream.duration_seconds,
                },
            },
        }

    @staticmethod
    def _decode(raw: dict[str, Any]) -> EncodeJob:
        request_raw = _required_dict(raw.get("request"))
        stream_raw = _required_dict(request_raw.get("stream"))
        common_raw = _required_dict(request_raw.get("common"))
        return EncodeJob(
            id=UUID(_required_string(raw.get("id"))),
            state=JobState(_required_string(raw.get("state"))),
            overwrite=_optional_bool(raw.get("overwrite"), False),
            error=_nullable_string(raw.get("error")),
            created_at=_required_datetime(raw.get("created_at")),
            started_at=_optional_datetime(raw.get("started_at")),
            finished_at=_optional_datetime(raw.get("finished_at")),
            request=EncodingRequest(
                input_path=Path(_required_string(request_raw.get("input_path"))),
                output_path=Path(_required_string(request_raw.get("output_path"))),
                encoder_id=_required_string(request_raw.get("encoder_id")),
                codec=Codec(_required_string(request_raw.get("codec"))),
                output_format=OutputFormat(_required_string(request_raw.get("output_format"))),
                common=CommonAudioOptions(
                    sample_rate=_optional_int(common_raw.get("sample_rate")),
                    channel_layout=_optional_string(common_raw.get("channel_layout")),
                ),
                encoder_options=_decode_options(request_raw.get("encoder_options")),
                stream=AudioStream(
                    index=_required_int(stream_raw.get("index")),
                    ordinal=_required_int(stream_raw.get("ordinal")),
                    codec_name=_required_string(stream_raw.get("codec_name")),
                    channels=_optional_int(stream_raw.get("channels")),
                    channel_layout=_optional_string(stream_raw.get("channel_layout")),
                    sample_rate=_optional_int(stream_raw.get("sample_rate")),
                    language=_optional_string(stream_raw.get("language")),
                    title=_optional_string(stream_raw.get("title")),
                    duration_seconds=_optional_float(stream_raw.get("duration_seconds")),
                ),
            ),
        )


def _optional_string(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _nullable_string(value: object) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError("expected a string or null")
    return value


def _required_string(value: object) -> str:
    parsed = _optional_string(value)
    if parsed is None:
        raise TypeError("expected a non-empty string")
    return parsed


def _optional_int(value: object) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def _required_int(value: object) -> int:
    parsed = _optional_int(value)
    if parsed is None:
        raise TypeError("expected an integer")
    return parsed


def _optional_float(value: object) -> float | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    if value is None:
        return None
    raise TypeError("expected a number or null")


def _optional_bool(value: object, default: bool) -> bool:
    if value is None:
        return default
    if not isinstance(value, bool):
        raise TypeError("expected a boolean")
    return value


def _required_dict(value: object) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TypeError("expected an object")
    return value


def _decode_options(value: object) -> dict[str, JsonScalar]:
    raw = _required_dict(value)
    options: dict[str, JsonScalar] = {}
    for key, option in raw.items():
        if not isinstance(key, str) or not (
            option is None or isinstance(option, (str, int, float, bool))
        ):
            raise TypeError("invalid encoder option")
        options[key] = option
    return options


def _encode_datetime(value: datetime | None) -> str | None:
    return value.isoformat() if value is not None else None


def _required_datetime(value: object) -> datetime:
    parsed = _optional_datetime(value)
    if parsed is None:
        raise TypeError("expected a timestamp")
    return parsed


def _optional_datetime(value: object) -> datetime | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError("expected a timestamp or null")
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def _decode_channel_layout(common: dict[str, Any]) -> str | None:
    layout = _optional_string(common.get("channel_layout"))
    if layout is not None:
        return layout
    legacy_channels = _optional_int(common.get("channels"))
    if legacy_channels == 1:
        return "mono"
    if legacy_channels == 2:
        return "stereo"
    return None


def _positive_int(value: object, default: int) -> int:
    parsed = _optional_int(value)
    return parsed if parsed is not None and parsed > 0 else default


def _splitter_sizes(value: object, default: tuple[int, int]) -> tuple[int, int]:
    if not isinstance(value, list) or len(value) != 2:
        return default
    first, second = value
    if any(not isinstance(size, int) or isinstance(size, bool) or size < 0 for size in value):
        return default
    if first + second <= 0:
        return default
    return first, second
