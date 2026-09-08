from __future__ import annotations

import json
import math
from collections import deque
from collections.abc import Mapping
from dataclasses import replace
from pathlib import Path
from typing import Any

from pymediainfo import MediaInfo
from PySide6.QtCore import QObject, QProcess, QRunnable, QThreadPool, QTimer, Signal, Slot

from ffmpeg_audio_encoder.domain.errors import ProbeError
from ffmpeg_audio_encoder.domain.models import (
    AudioStream,
    DelaySource,
    DetectedDelay,
    MediaAsset,
)
from ffmpeg_audio_encoder.infrastructure.delay import MAX_DELAY_MS, parse_filename_delay


def _optional_float(value: object) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        return None
    try:
        parsed = float(value)
        return parsed if parsed >= 0 else None
    except (TypeError, ValueError):
        return None


def _optional_signed_float(value: object) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        return None
    try:
        parsed = float(value)
        return parsed if math.isfinite(parsed) else None
    except (TypeError, ValueError):
        return None


def _optional_int(value: object) -> int | None:
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def parse_ffprobe_json(path: Path, payload: Mapping[str, Any]) -> MediaAsset:
    raw_format = payload.get("format")
    format_duration = (
        _optional_float(raw_format.get("duration")) if isinstance(raw_format, Mapping) else None
    )
    raw_streams = payload.get("streams")
    if not isinstance(raw_streams, list):
        raise ProbeError("ffprobe response does not contain a stream list")

    video_streams = [
        stream
        for stream in raw_streams
        if isinstance(stream, Mapping)
        and stream.get("codec_type") == "video"
        and _optional_int(stream.get("index")) is not None
        and not (
            isinstance(stream.get("disposition"), Mapping)
            and stream["disposition"].get("attached_pic") == 1
        )
    ]
    reference_video_position = next(
        (
            position
            for position, stream in enumerate(video_streams)
            if isinstance(stream.get("disposition"), Mapping)
            and stream["disposition"].get("default") == 1
        ),
        0 if video_streams else None,
    )
    audio_streams: list[AudioStream] = []
    for raw_stream in raw_streams:
        if not isinstance(raw_stream, Mapping) or raw_stream.get("codec_type") != "audio":
            continue
        index = _optional_int(raw_stream.get("index"))
        if index is None:
            continue
        raw_tags = raw_stream.get("tags")
        tags = raw_tags if isinstance(raw_tags, Mapping) else {}
        duration = _optional_float(raw_stream.get("duration")) or format_duration
        audio_streams.append(
            AudioStream(
                index=index,
                ordinal=len(audio_streams) + 1,
                codec_name=str(raw_stream.get("codec_name") or "unknown"),
                channels=_optional_int(raw_stream.get("channels")),
                channel_layout=(
                    str(raw_stream["channel_layout"]) if raw_stream.get("channel_layout") else None
                ),
                sample_rate=_optional_int(raw_stream.get("sample_rate")),
                language=str(tags["language"]) if tags.get("language") else None,
                title=str(tags["title"]) if tags.get("title") else None,
                duration_seconds=duration,
            )
        )
    if not audio_streams:
        raise ProbeError("The selected input does not contain an audio stream")
    asset = MediaAsset(
        path,
        tuple(audio_streams),
        format_duration,
        has_video_reference=bool(video_streams),
        video_stream_indexes=tuple(
            index
            for stream in video_streams
            if (index := _optional_int(stream.get("index"))) is not None
        ),
        reference_video_position=reference_video_position,
    )
    if video_streams or len(audio_streams) != 1:
        return asset
    filename_delay = parse_filename_delay(path.stem)
    if filename_delay is None:
        return asset
    return replace(
        asset,
        detected_delays=(
            DetectedDelay(
                audio_streams[0].index,
                filename_delay.milliseconds,
                DelaySource.FILENAME,
            ),
        ),
    )


def apply_mediainfo_delays(
    asset: MediaAsset, payload: Mapping[str, Any], error: str | None = None
) -> MediaAsset:
    if not asset.has_video_reference:
        return asset
    if error:
        return replace(
            asset, delay_detection_note=f"MediaInfo delay detection unavailable: {error}"
        )
    raw_tracks = payload.get("tracks")
    if not isinstance(raw_tracks, list):
        return replace(asset, delay_detection_note="MediaInfo did not return a track list")
    audio_tracks = [
        track
        for track in raw_tracks
        if isinstance(track, Mapping) and str(track.get("track_type")).casefold() == "audio"
    ]
    video_tracks = [
        track
        for track in raw_tracks
        if isinstance(track, Mapping) and str(track.get("track_type")).casefold() == "video"
    ]
    matched_audio_tracks = _match_mediainfo_tracks(
        tuple(stream.index for stream in asset.audio_streams), audio_tracks
    )
    matched_video_tracks = _match_mediainfo_tracks(asset.video_stream_indexes, video_tracks)
    reference_position = asset.reference_video_position
    if (
        matched_audio_tracks is None
        or matched_video_tracks is None
        or reference_position is None
        or reference_position >= len(matched_video_tracks)
    ):
        return replace(asset, delay_detection_note="MediaInfo track matching was ambiguous")

    detected: list[DetectedDelay] = []
    for stream, track in zip(asset.audio_streams, matched_audio_tracks, strict=True):
        if reference_position == 0:
            milliseconds = _optional_signed_float(track.get("delay_relative_to_video"))
        else:
            audio_delay = _optional_signed_float(track.get("delay"))
            video_delay = _optional_signed_float(
                matched_video_tracks[reference_position].get("delay")
            )
            milliseconds = (
                audio_delay - video_delay
                if audio_delay is not None and video_delay is not None
                else None
            )
        if milliseconds is None or abs(milliseconds) > MAX_DELAY_MS:
            continue
        detected.append(DetectedDelay(stream.index, round(milliseconds, 3), DelaySource.CONTAINER))
    note = (
        None
        if len(detected) == len(asset.audio_streams)
        else "MediaInfo did not report a usable delay for every audio track"
    )
    return replace(asset, detected_delays=tuple(detected), delay_detection_note=note)


def _match_mediainfo_tracks(
    stream_indexes: tuple[int, ...], tracks: list[Mapping[str, Any]]
) -> tuple[Mapping[str, Any], ...] | None:
    tracks_by_order: dict[int, Mapping[str, Any]] = {}
    ambiguous_orders: set[int] = set()
    for track in tracks:
        order = _optional_int(track.get("streamorder", track.get("stream_order")))
        if order is None:
            continue
        if order in tracks_by_order:
            ambiguous_orders.add(order)
        else:
            tracks_by_order[order] = track
    if all(index in tracks_by_order and index not in ambiguous_orders for index in stream_indexes):
        return tuple(tracks_by_order[index] for index in stream_indexes)
    if len(stream_indexes) == len(tracks):
        return tuple(tracks)
    return None


class _MediaInfoTaskSignals(QObject):
    finished = Signal(str, object, str)


class _MediaInfoTask(QRunnable):
    def __init__(self, key: str) -> None:
        super().__init__()
        self.key = key
        self.signals = _MediaInfoTaskSignals()

    @Slot()
    def run(self) -> None:
        try:
            result = MediaInfo.parse(self.key).to_data()
            self.signals.finished.emit(self.key, result, "")
        except Exception as exc:
            self.signals.finished.emit(self.key, {}, str(exc))


class QtMediaProbe(QObject):
    completed = Signal(str, object)
    failed = Signal(str, str)

    def __init__(
        self,
        ffprobe_path: Path,
        parent: QObject | None = None,
        *,
        max_concurrent: int = 4,
        timeout_ms: int = 30_000,
    ) -> None:
        super().__init__(parent)
        self.ffprobe_path = ffprobe_path
        self.max_concurrent = max(1, max_concurrent)
        self.timeout_ms = max(1, timeout_ms)
        self._pending: deque[Path] = deque()
        self._known: set[str] = set()
        self._processes: dict[str, QProcess] = {}
        self._stdout: dict[str, bytearray] = {}
        self._stderr: dict[str, bytearray] = {}
        self._media_info_pool = QThreadPool(self)
        self._media_info_pool.setMaxThreadCount(1)
        self._media_info_tasks: dict[str, _MediaInfoTask] = {}
        self._awaiting_media_info: dict[str, MediaAsset] = {}

    def probe(self, path: Path) -> None:
        key = str(path)
        if key in self._known:
            return
        self._known.add(key)
        self._pending.append(path)
        self._start_pending()

    def cancel_all(self) -> None:
        self._pending.clear()
        self._known.clear()
        processes = list(self._processes.values())
        self._processes.clear()
        self._stdout.clear()
        self._stderr.clear()
        self._media_info_pool.clear()
        self._media_info_tasks.clear()
        self._awaiting_media_info.clear()
        for process in processes:
            process.disconnect(self)
            if process.state() is not QProcess.ProcessState.NotRunning:
                process.kill()
            process.deleteLater()

    def _start_pending(self) -> None:
        while self._pending and len(self._processes) < self.max_concurrent:
            self._start_process(self._pending.popleft())

    def _start_process(self, path: Path) -> None:
        key = str(path)
        process = QProcess(self)
        self._processes[key] = process
        self._stdout[key] = bytearray()
        self._stderr[key] = bytearray()
        process.readyReadStandardOutput.connect(
            lambda key=key, process=process: self._stdout[key].extend(
                process.readAllStandardOutput().data()
            )
        )
        process.readyReadStandardError.connect(
            lambda key=key, process=process: self._stderr[key].extend(
                process.readAllStandardError().data()
            )
        )
        process.finished.connect(lambda exit_code, _status, key=key: self._finish(key, exit_code))
        process.errorOccurred.connect(
            lambda error, key=key, process=process: self._process_error(key, process, error)
        )
        process.setProgram(str(self.ffprobe_path))
        process.setArguments(
            [
                "-v",
                "error",
                "-show_streams",
                "-show_format",
                "-of",
                "json",
                key,
            ]
        )
        process.start()
        QTimer.singleShot(
            self.timeout_ms,
            lambda key=key, process=process: self._timeout(key, process),
        )

    def _process_error(self, key: str, process: QProcess, error: QProcess.ProcessError) -> None:
        if error is QProcess.ProcessError.FailedToStart:
            # Qt words this per platform, and Linux reports the bare execve failure
            # without naming the program, so lead with our own sentence and keep Qt's
            # wording as the detail after it.
            detail = process.errorString()
            self._fail(
                key,
                f"ffprobe failed to start: {detail}" if detail else "ffprobe failed to start",
            )

    def _timeout(self, key: str, process: QProcess) -> None:
        if self._processes.get(key) is process:
            self._fail(key, f"ffprobe timed out after {self.timeout_ms / 1000:g} seconds")

    def _fail(self, key: str, message: str) -> None:
        process = self._processes.pop(key, None)
        if process is None:
            return
        self._stdout.pop(key, None)
        self._stderr.pop(key, None)
        self._known.discard(key)
        process.disconnect(self)
        if process.state() is not QProcess.ProcessState.NotRunning:
            process.kill()
        process.deleteLater()
        self.failed.emit(key, message)
        self._start_pending()

    def _finish(self, key: str, exit_code: int) -> None:
        process = self._processes.pop(key, None)
        if process is None:
            return
        stdout = bytes(self._stdout.pop(key)).decode("utf-8", errors="replace")
        stderr = bytes(self._stderr.pop(key)).decode("utf-8", errors="replace").strip()
        process.deleteLater()
        if exit_code != 0:
            self._known.discard(key)
            self.failed.emit(key, stderr or f"ffprobe exited with code {exit_code}")
            self._start_pending()
            return
        try:
            payload = json.loads(stdout)
            if not isinstance(payload, dict):
                raise ProbeError("ffprobe returned an unexpected JSON value")
            asset = parse_ffprobe_json(Path(key), payload)
            if asset.has_video_reference:
                self._start_media_info(key, asset)
            else:
                self._known.discard(key)
                self.completed.emit(key, asset)
        except (json.JSONDecodeError, ProbeError) as exc:
            self._known.discard(key)
            self.failed.emit(key, str(exc))
        self._start_pending()

    def _start_media_info(self, key: str, asset: MediaAsset) -> None:
        task = _MediaInfoTask(key)
        self._awaiting_media_info[key] = asset
        self._media_info_tasks[key] = task
        task.signals.finished.connect(self._finish_media_info)
        self._media_info_pool.start(task)

    def _finish_media_info(self, key: str, raw_payload: object, error: str) -> None:
        asset = self._awaiting_media_info.pop(key, None)
        self._media_info_tasks.pop(key, None)
        if asset is None:
            return
        self._known.discard(key)
        payload = raw_payload if isinstance(raw_payload, Mapping) else {}
        self.completed.emit(key, apply_mediainfo_delays(asset, payload, error or None))
