from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from platformdirs import user_config_path

from ffmpeg_audio_encoder.domain.models import (
    AppSettings,
    Codec,
    CommonAudioOptions,
    EncoderPreset,
    JsonScalar,
    OutputFormat,
    ThemePreference,
)

SCHEMA_VERSION = 1
PRESET_SCHEMA_VERSION = 2


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


def _optional_string(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _optional_int(value: object) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) else None


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
