from datetime import UTC, datetime
from pathlib import Path

from ffmpeg_audio_encoder.domain.models import (
    AppSettings,
    AudioStream,
    Codec,
    CommonAudioOptions,
    EncodeJob,
    EncoderPreset,
    EncodingRequest,
    JobState,
    OutputFormat,
    ThemePreference,
)
from ffmpeg_audio_encoder.infrastructure.persistence import (
    JobRepository,
    PresetRepository,
    SettingsRepository,
)


def test_settings_round_trip(tmp_path: Path) -> None:
    repository = SettingsRepository(tmp_path / "settings.json")
    settings = AppSettings(
        ffmpeg_path="/tools/ffmpeg",
        ffprobe_path="/tools/ffprobe",
        qaac_path="/tools/qaac64",
        fdkaac_path="/tools/fdkaac",
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


def test_jobs_round_trip_all_durable_fields(tmp_path: Path) -> None:
    repository = JobRepository(tmp_path / "jobs.json")
    created_at = datetime(2026, 9, 3, 12, 30, tzinfo=UTC)
    started_at = datetime(2026, 9, 3, 12, 31, tzinfo=UTC)
    finished_at = datetime(2026, 9, 3, 12, 32, tzinfo=UTC)
    job = EncodeJob(
        request=EncodingRequest(
            input_path=tmp_path / "input.mkv",
            stream=AudioStream(
                2,
                1,
                "aac",
                channels=6,
                channel_layout="5.1",
                sample_rate=48000,
                language="eng",
                title="Main",
                duration_seconds=65.5,
            ),
            encoder_id="ffmpeg.libopus",
            codec=Codec.OPUS,
            output_format=OutputFormat.OGG_OPUS,
            output_path=tmp_path / "output.opus",
            common=CommonAudioOptions(48000, "stereo"),
            encoder_options={
                "bitrate_kbps": 128,
                "vbr": "on",
                "custom_args": "-cutoff 20000",
            },
        ),
        overwrite=True,
        state=JobState.FAILED,
        error="test failure",
        created_at=created_at,
        started_at=started_at,
        finished_at=finished_at,
    )

    repository.save([job])

    assert repository.load() == [job]
    assert not (tmp_path / ".jobs.json.tmp").exists()


def test_malformed_jobs_are_quarantined(tmp_path: Path) -> None:
    path = tmp_path / "jobs.json"
    path.write_text("not json", encoding="utf-8")

    assert JobRepository(path).load() == []
    assert not path.exists()
    quarantined = list(tmp_path.glob("jobs.corrupt-*.json"))
    assert len(quarantined) == 1
    assert quarantined[0].read_text(encoding="utf-8") == "not json"
