from __future__ import annotations

import os
from datetime import UTC, datetime
from uuid import UUID

from PySide6.QtCore import QObject, Signal

from ffmpeg_audio_encoder.domain.models import (
    EncodeJob,
    EncodingRequest,
    JobState,
    Toolchain,
)
from ffmpeg_audio_encoder.encoders.registry import EncoderRegistry
from ffmpeg_audio_encoder.infrastructure.output import temporary_output_path
from ffmpeg_audio_encoder.infrastructure.process import QtProcessRunner
from ffmpeg_audio_encoder.infrastructure.progress import ProgressUpdate


class JobQueueController(QObject):
    job_added = Signal(str)
    job_updated = Signal(str)
    log = Signal(str, str)
    active_changed = Signal(bool)

    def __init__(
        self,
        registry: EncoderRegistry,
        toolchain: Toolchain,
        runner: QtProcessRunner | None = None,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self.registry = registry
        self.toolchain = toolchain
        self.runner = runner or QtProcessRunner(self)
        self.jobs: list[EncodeJob] = []
        self._run_queue = False
        self._active_id: UUID | None = None
        self.runner.progress.connect(self._on_progress)
        self.runner.log.connect(self.log)
        self.runner.finished.connect(self._on_finished)

    @property
    def active_job(self) -> EncodeJob | None:
        return self._find(self._active_id) if self._active_id else None

    def add(self, request: EncodingRequest, overwrite: bool = False) -> EncodeJob:
        self.registry.get(request.encoder_id).validate(request)
        job = EncodeJob(request=request, overwrite=overwrite)
        self.jobs.append(job)
        self.job_added.emit(str(job.id))
        return job

    def start(self) -> None:
        self._run_queue = True
        self._start_next()

    def cancel_active(self) -> None:
        job = self.active_job
        if job is None:
            return
        job.status = "Cancelling…"
        self.job_updated.emit(str(job.id))
        self.runner.cancel()

    def stop_after_current(self) -> None:
        self._run_queue = False

    def retry(self, job_id: UUID) -> None:
        job = self._find(job_id)
        if job is None or job.state not in {
            JobState.FAILED,
            JobState.CANCELLED,
            JobState.SUCCEEDED,
        }:
            return
        job.state = JobState.QUEUED
        job.progress = 0.0
        job.status = "Waiting"
        job.error = None
        job.started_at = None
        job.finished_at = None
        self.job_updated.emit(str(job.id))

    def remove(self, job_ids: set[UUID]) -> None:
        self.jobs[:] = [
            job for job in self.jobs if job.id not in job_ids or job.state is JobState.RUNNING
        ]
        self.job_updated.emit("")

    def clear_completed(self) -> None:
        terminal = {JobState.SUCCEEDED, JobState.FAILED, JobState.CANCELLED}
        self.jobs[:] = [job for job in self.jobs if job.state not in terminal]
        self.job_updated.emit("")

    def _start_next(self) -> None:
        if not self._run_queue or self.runner.is_running:
            return
        job = next((job for job in self.jobs if job.state is JobState.QUEUED), None)
        if job is None:
            self._run_queue = False
            self.active_changed.emit(False)
            return
        output = job.request.output_path
        if output.exists() and not job.overwrite:
            self._fail(job, f"Output already exists: {output}")
            self._start_next()
            return
        try:
            output.parent.mkdir(parents=True, exist_ok=True)
            temporary = temporary_output_path(output, job.id)
            temporary.unlink(missing_ok=True)
            plan = self.registry.get(job.request.encoder_id).build_plan(
                job.request, self.toolchain, temporary
            )
            job.state = JobState.RUNNING
            job.status = "Encoding"
            job.progress = 0.0 if plan.duration_seconds else None
            job.started_at = datetime.now(UTC)
            self._active_id = job.id
            self.job_updated.emit(str(job.id))
            self.active_changed.emit(True)
            self.runner.start(job.id, plan)
        except (OSError, ValueError, RuntimeError) as exc:
            self._fail(job, str(exc))
            self._start_next()

    def _on_progress(self, job_id: str, raw_update: object) -> None:
        job = self._find(UUID(job_id))
        if job is None or not isinstance(raw_update, ProgressUpdate):
            return
        job.progress = raw_update.fraction
        if raw_update.speed:
            job.status = f"Encoding · {raw_update.speed}"
        self.job_updated.emit(job_id)

    def _on_finished(self, job_id: str, success: bool, error: str) -> None:
        job = self._find(UUID(job_id))
        if job is None:
            return
        temporary = temporary_output_path(job.request.output_path, job.id)
        if success:
            try:
                if job.request.output_path.exists() and not job.overwrite:
                    raise FileExistsError(f"Output already exists: {job.request.output_path}")
                os.replace(temporary, job.request.output_path)
                job.state = JobState.SUCCEEDED
                job.progress = 1.0
                job.status = "Complete"
                job.error = None
            except OSError as exc:
                temporary.unlink(missing_ok=True)
                self._fail(job, f"Could not publish output: {exc}")
        else:
            temporary.unlink(missing_ok=True)
            if error == "Cancelled":
                job.state = JobState.CANCELLED
                job.status = "Cancelled"
                job.error = None
            else:
                self._fail(job, error or "Encoder process failed")
        job.finished_at = datetime.now(UTC)
        self._active_id = None
        self.job_updated.emit(job_id)
        self.active_changed.emit(False)
        self._start_next()

    def _fail(self, job: EncodeJob, message: str) -> None:
        job.state = JobState.FAILED
        job.status = "Failed"
        job.error = message
        job.finished_at = datetime.now(UTC)
        self.job_updated.emit(str(job.id))

    def _find(self, job_id: UUID | None) -> EncodeJob | None:
        return next((job for job in self.jobs if job.id == job_id), None)
