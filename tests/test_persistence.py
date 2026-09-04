from pathlib import Path

from ffmpeg_audio_encoder.domain.models import (
    AppSettings,
    Codec,
    CommonAudioOptions,
    EncoderPreset,
    OutputFormat,
    ThemePreference,
)
from ffmpeg_audio_encoder.infrastructure.persistence import PresetRepository, SettingsRepository


def test_settings_round_trip(tmp_path: Path) -> None:
    repository = SettingsRepository(tmp_path / "settings.json")
    settings = AppSettings(
        ffmpeg_path="/tools/ffmpeg",
        ffprobe_path="/tools/ffprobe",
        default_output_dir="/output",
        overwrite_default=True,
        theme=ThemePreference.DARK,
        window_x=20,
        window_y=30,
        window_width=900,
        window_height=700,
        draft_splitter_sizes=(500, 400),
        main_splitter_sizes=(440, 220),
        queue_panel_collapsed=True,
    )
    repository.save(settings)
    assert repository.load() == settings
    assert not (tmp_path / ".settings.json.tmp").exists()


def test_malformed_or_newer_settings_fall_back_safely(tmp_path: Path) -> None:
    path = tmp_path / "settings.json"
    path.write_text("not json", encoding="utf-8")
    assert SettingsRepository(path).load() == AppSettings()
    path.write_text('{"schema_version": 99}', encoding="utf-8")
    assert SettingsRepository(path).load() == AppSettings()


def test_presets_round_trip_in_a_stable_order(tmp_path: Path) -> None:
    repository = PresetRepository(tmp_path / "presets.json")
    presets = [
        EncoderPreset(
            "Voice",
            "ffmpeg.libopus",
            Codec.OPUS,
            OutputFormat.OGG_OPUS,
            CommonAudioOptions(48000, "mono"),
            {"bitrate_kbps": 64, "vbr": "on", "custom_args": "-cutoff 16000"},
        ),
        EncoderPreset(
            "Archive",
            "ffmpeg.flac",
            Codec.FLAC,
            OutputFormat.FLAC,
            CommonAudioOptions(),
            {"compression_level": 8},
        ),
    ]
    repository.save(presets)
    loaded = repository.load()
    assert [preset.name for preset in loaded] == ["Archive", "Voice"]
    assert loaded[1].encoder_options["bitrate_kbps"] == 64
    assert loaded[1].common.channel_layout == "mono"
    assert loaded[1].encoder_options["custom_args"] == "-cutoff 16000"


def test_legacy_channel_counts_are_migrated(tmp_path: Path) -> None:
    path = tmp_path / "presets.json"
    path.write_text(
        '{"schema_version":1,"presets":[{"name":"Old","encoder_id":"ffmpeg.flac",'
        '"codec":"flac","output_format":"flac","common":{"sample_rate":48000,'
        '"channels":2},"encoder_options":{"compression_level":5}}]}',
        encoding="utf-8",
    )
    presets = PresetRepository(path).load()
    assert presets[0].common == CommonAudioOptions(48000, "stereo")
