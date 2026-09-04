from pathlib import Path

from PySide6.QtCore import QObject, Signal

from ffmpeg_audio_encoder.application.queue import JobQueueController
from ffmpeg_audio_encoder.domain.models import (
    AudioStream,
    Codec,
    EncodingRequest,
    JobState,
    OutputFormat,
    ProcessPlan,
    Toolchain,
)
from ffmpeg_audio_encoder.encoders import default_registry
from ffmpeg_audio_encoder.encoders.ffmpeg import FlacEncoder


class FakeRunner(QObject):
    progress = Signal(str, object)
    log = Signal(str, str)
    finished = Signal(str, bool, str)

    def __init__(self) -> None:
        super().__init__()
        self.is_running = False
        self.job_id = None
        self.plan: ProcessPlan | None = None

    def start(self, job_id, plan: ProcessPlan) -> None:
        self.is_running = True
        self.job_id = job_id
        self.plan = plan

    def cancel(self) -> None:
        assert self.job_id is not None
        self.is_running = False
        self.finished.emit(str(self.job_id), False, "Cancelled")

    def complete(self, success: bool = True, error: str = "") -> None:
        assert self.job_id is not None
        self.is_running = False
        self.finished.emit(str(self.job_id), success, error)


def request(input_path: Path, output_path: Path) -> EncodingRequest:
    encoder = FlacEncoder()
    return EncodingRequest(
        input_path,
        AudioStream(0, 1, "pcm_s16le", duration_seconds=1.0),
        encoder.descriptor.id,
        Codec.FLAC,
        OutputFormat.FLAC,
        output_path,
        encoder_options=encoder.default_options(),
    )


def test_queue_runs_sequentially_and_publishes_atomically(tmp_path: Path, qtbot) -> None:
    runner = FakeRunner()
    controller = JobQueueController(
        default_registry(),
        Toolchain(Path("ffmpeg"), Path("ffprobe")),
        runner=runner,  # type: ignore[arg-type]
    )
    first = controller.add(request(tmp_path / "one.wav", tmp_path / "one.flac"))
    second = controller.add(request(tmp_path / "two.wav", tmp_path / "two.flac"))
    controller.start()
    assert first.state is JobState.RUNNING
    assert second.state is JobState.QUEUED
    assert runner.plan is not None
    runner.plan.temporary_output.write_bytes(b"flac")
    runner.complete()
    assert first.state is JobState.SUCCEEDED
    assert first.request.output_path.read_bytes() == b"flac"
    assert second.state is JobState.RUNNING


def test_cancellation_cleans_partial_output(tmp_path: Path, qtbot) -> None:
    runner = FakeRunner()
    controller = JobQueueController(
        default_registry(),
        Toolchain(Path("ffmpeg"), Path("ffprobe")),
        runner=runner,  # type: ignore[arg-type]
    )
    job = controller.add(request(tmp_path / "one.wav", tmp_path / "one.flac"))
    controller.start()
    assert runner.plan is not None
    runner.plan.temporary_output.write_bytes(b"partial")
    controller.cancel_active()
    assert job.state is JobState.CANCELLED
    assert not runner.plan.temporary_output.exists()


def test_existing_output_requires_explicit_overwrite(tmp_path: Path, qtbot) -> None:
    output = tmp_path / "one.flac"
    output.write_bytes(b"existing")
    runner = FakeRunner()
    controller = JobQueueController(
        default_registry(),
        Toolchain(Path("ffmpeg"), Path("ffprobe")),
        runner=runner,  # type: ignore[arg-type]
    )
    job = controller.add(request(tmp_path / "one.wav", output))
    controller.start()
    assert job.state is JobState.FAILED
    assert output.read_bytes() == b"existing"
    assert not runner.is_running
