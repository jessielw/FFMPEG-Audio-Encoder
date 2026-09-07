import sys
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from ffmpeg_audio_encoder.domain.models import (
    Codec,
    DelaySource,
    OutputFormat,
    ProcessPlan,
    ProcessStage,
    ProgressProtocol,
)
from ffmpeg_audio_encoder.infrastructure.delay import (
    parse_filename_delay,
    strip_filename_delay_marker,
)
from ffmpeg_audio_encoder.infrastructure.output import (
    default_output_path,
    sanitize_filename_component,
    temporary_output_path,
)
from ffmpeg_audio_encoder.infrastructure.probe import (
    QtMediaProbe,
    apply_mediainfo_delays,
    parse_ffprobe_json,
)
from ffmpeg_audio_encoder.infrastructure.process import QtProcessRunner
from ffmpeg_audio_encoder.infrastructure.progress import DeezyProgressParser, FFmpegProgressParser


def test_ffprobe_parser_uses_global_duration_and_real_stream_indexes(tmp_path: Path) -> None:
    payload = {
        "format": {"duration": "12.5"},
        "streams": [
            {"index": 0, "codec_type": "video", "codec_name": "h264"},
            {
                "index": 2,
                "codec_type": "audio",
                "codec_name": "opus",
                "channels": 6,
                "channel_layout": "5.1",
                "sample_rate": "48000",
                "tags": {"language": "eng", "title": "Main"},
            },
        ],
    }
    asset = parse_ffprobe_json(tmp_path / "movie.mkv", payload)
    stream = asset.audio_streams[0]
    assert stream.index == 2
    assert stream.ordinal == 1
    assert stream.duration_seconds == 12.5
    assert stream.language == "eng"


def test_container_delays_are_correlated_to_each_audio_track(tmp_path: Path) -> None:
    asset = parse_ffprobe_json(
        tmp_path / "movie.mkv",
        {
            "streams": [
                {
                    "index": 0,
                    "codec_type": "video",
                    "codec_name": "h264",
                    "disposition": {"default": 1, "attached_pic": 0},
                },
                {"index": 2, "codec_type": "audio", "codec_name": "aac"},
                {"index": 4, "codec_type": "audio", "codec_name": "ac3"},
            ]
        },
    )
    enriched = apply_mediainfo_delays(
        asset,
        {
            "tracks": [
                {"track_type": "General"},
                {"track_type": "Video", "streamorder": "0", "delay": 0},
                {
                    "track_type": "Audio",
                    "streamorder": "4",
                    "delay_relative_to_video": -21.5,
                },
                {
                    "track_type": "Audio",
                    "streamorder": "2",
                    "delay_relative_to_video": 80,
                },
            ]
        },
    )

    assert [
        (delay.stream_index, delay.milliseconds, delay.source) for delay in enriched.detected_delays
    ] == [
        (2, 80.0, DelaySource.CONTAINER),
        (4, -21.5, DelaySource.CONTAINER),
    ]
    assert enriched.delay_detection_note is None


def test_default_non_first_video_is_used_as_delay_reference(tmp_path: Path) -> None:
    asset = parse_ffprobe_json(
        tmp_path / "alternate-angle.mkv",
        {
            "streams": [
                {
                    "index": 0,
                    "codec_type": "video",
                    "disposition": {"default": 0, "attached_pic": 0},
                },
                {
                    "index": 1,
                    "codec_type": "video",
                    "disposition": {"default": 1, "attached_pic": 0},
                },
                {"index": 2, "codec_type": "audio", "codec_name": "flac"},
            ]
        },
    )
    enriched = apply_mediainfo_delays(
        asset,
        {
            "tracks": [
                {"track_type": "Video", "delay": 0},
                {"track_type": "Video", "delay": 20},
                {"track_type": "Audio", "delay": 100, "delay_relative_to_video": 100},
            ]
        },
    )

    assert enriched.detected_delays[0].milliseconds == 80


def test_video_container_with_missing_mediainfo_delay_does_not_guess(tmp_path: Path) -> None:
    asset = parse_ffprobe_json(
        tmp_path / "movie [DELAY 90ms].mkv",
        {
            "streams": [
                {"index": 0, "codec_type": "video", "disposition": {"attached_pic": 0}},
                {"index": 1, "codec_type": "audio", "codec_name": "aac"},
            ]
        },
    )
    enriched = apply_mediainfo_delays(
        asset,
        {"tracks": [{"track_type": "Video"}, {"track_type": "Audio"}]},
    )

    assert not enriched.detected_delays
    assert enriched.delay_detection_note


@pytest.mark.parametrize(
    ("stem", "expected"),
    [
        ("Movie [DELAY -21ms]", -21.0),
        ("Movie.delay_80ms", 80.0),
        ("Movie (Delay +12.5 ms)", 12.5),
    ],
)
def test_filename_delay_parser_accepts_explicit_markers(stem: str, expected: float) -> None:
    detected = parse_filename_delay(stem)
    assert detected is not None
    assert detected.milliseconds == expected


@pytest.mark.parametrize(
    "stem",
    [
        "Movie -21ms",
        "Movie delay 1s",
        "Movie delayish -21ms",
        "Movie [DELAY 1ms] [DELAY 2ms]",
        "Movie [DELAY 86400001ms]",
    ],
)
def test_filename_delay_parser_rejects_unsafe_or_ambiguous_values(stem: str) -> None:
    assert parse_filename_delay(stem) is None


def test_audio_only_filename_delay_is_detected_and_removed_from_output_name(
    tmp_path: Path,
) -> None:
    asset = parse_ffprobe_json(
        tmp_path / "Movie [DELAY -21ms].ac3",
        {"streams": [{"index": 0, "codec_type": "audio", "codec_name": "ac3"}]},
    )

    assert asset.detected_delays[0].milliseconds == -21
    assert asset.detected_delays[0].source is DelaySource.FILENAME
    assert strip_filename_delay_marker(asset.path.stem) == "Movie"
    output = default_output_path(
        asset.path,
        asset.audio_streams[0],
        Codec.OPUS,
        OutputFormat.OGG_OPUS,
        strip_delay_marker=True,
    )
    assert output.name == "Movie [Audio 1] [Opus].opus"


def test_readable_output_and_unique_temporary_name(tmp_path: Path) -> None:
    asset = parse_ffprobe_json(
        tmp_path / "movie.mkv",
        {
            "streams": [
                {
                    "index": 1,
                    "codec_type": "audio",
                    "codec_name": "aac",
                    "channels": 6,
                    "tags": {"language": "eng"},
                }
            ]
        },
    )
    output = default_output_path(
        asset.path,
        asset.audio_streams[0],
        Codec.OPUS,
        OutputFormat.OGG_OPUS,
    )
    assert output.name == "movie [Audio 1] [eng] [6ch] [Opus].opus"
    temporary = temporary_output_path(output, UUID(int=1))
    assert temporary.name.startswith(".movie")
    assert temporary.name.endswith(".part.opus")


def test_filename_sanitization_is_portable() -> None:
    assert sanitize_filename_component("bad:<name>?*") == "bad__name___"
    assert sanitize_filename_component("CON") == "_CON"


def test_progress_parser_handles_chunks_and_known_duration() -> None:
    parser = FFmpegProgressParser(10.0)
    assert parser.feed("out_time_us=500") == []
    updates = parser.feed("0000\nspeed=2.0x\nprogress=continue\n")
    assert len(updates) == 1
    assert updates[0].fraction == 0.5
    assert updates[0].speed == "2.0x"
    assert parser.feed("progress=end\n")[0].fraction == 1.0


def test_progress_without_duration_is_indeterminate() -> None:
    update = FFmpegProgressParser(None).feed("out_time=00:00:01.0\nprogress=continue\n")[0]
    assert update.fraction is None


def test_deezy_progress_parser_aggregates_chunked_stage_lines() -> None:
    parser = DeezyProgressParser()
    assert parser.feed("FFMPEG (1 of 3) 5") == []
    first = parser.feed("0.0%\n")[0]
    second = parser.feed("DEE measure (2 of 3) 25.0%\n")[0]
    final = parser.feed("DEE encode (3 of 3) 100.0%\n")[0]
    assert first.fraction == pytest.approx(1 / 6)
    assert first.phase == "FFMPEG"
    assert second.fraction == pytest.approx(5 / 12)
    assert final.fraction == 1.0
    assert final.ended


def test_qt_runner_parses_and_logs_deezy_progress_from_stderr(tmp_path: Path, qtbot) -> None:
    plan = ProcessPlan(
        (
            ProcessStage(
                Path(sys.executable),
                (
                    "-c",
                    (
                        "import sys; "
                        "print('FFMPEG (1 of 3) 50.0%', file=sys.stderr); "
                        "print('DEE measure (2 of 3) 25.0%', file=sys.stderr)"
                    ),
                ),
                "stderr",
                ProgressProtocol.DEEZY,
            ),
        ),
        tmp_path / "temporary.eac3",
        tmp_path / "final.eac3",
        10,
    )
    runner = QtProcessRunner()
    updates = []
    logs: list[str] = []
    finished: list[bool] = []
    runner.progress.connect(lambda _job_id, update: updates.append(update))
    runner.log.connect(lambda _job_id, message: logs.append(message))
    runner.finished.connect(lambda _job_id, success, _error: finished.append(success))

    runner.start(uuid4(), plan)
    qtbot.waitUntil(lambda: bool(finished))

    assert finished == [True]
    assert [update.phase for update in updates] == ["FFMPEG", "DEE measure"]
    assert updates[-1].fraction == pytest.approx(5 / 12)
    assert "DEE measure (2 of 3) 25.0%" in "".join(logs)


def test_media_probe_reports_failed_start(tmp_path: Path, qtbot) -> None:
    probe = QtMediaProbe(tmp_path / "missing-ffprobe", timeout_ms=1_000)
    failures: list[str] = []
    probe.failed.connect(lambda _path, message: failures.append(message))

    probe.probe(tmp_path / "input.wav")

    qtbot.waitUntil(lambda: bool(failures), timeout=3_000)
    assert "start" in failures[0].lower() or "find" in failures[0].lower()


def test_media_probe_bounds_concurrent_processes(tmp_path: Path, qtbot) -> None:
    probe = QtMediaProbe(Path(sys.executable), max_concurrent=2, timeout_ms=10_000)

    for index in range(5):
        probe.probe(tmp_path / f"input-{index}.wav")

    assert len(probe._processes) == 2
    assert len(probe._pending) == 3

    probe.cancel_all()
    assert not probe._processes
    assert not probe._pending
