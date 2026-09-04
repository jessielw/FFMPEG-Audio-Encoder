from pathlib import Path
from uuid import UUID

from ffmpeg_audio_encoder.domain.models import Codec, OutputFormat
from ffmpeg_audio_encoder.infrastructure.output import (
    default_output_path,
    sanitize_filename_component,
    temporary_output_path,
)
from ffmpeg_audio_encoder.infrastructure.probe import parse_ffprobe_json
from ffmpeg_audio_encoder.infrastructure.progress import FFmpegProgressParser


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
