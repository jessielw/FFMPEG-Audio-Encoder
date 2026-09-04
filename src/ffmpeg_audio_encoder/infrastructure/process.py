from __future__ import annotations

from functools import partial
from uuid import UUID

from PySide6.QtCore import QObject, QProcess, QTimer, Signal

from ffmpeg_audio_encoder.domain.models import ProcessPlan
from ffmpeg_audio_encoder.infrastructure.progress import FFmpegProgressParser


class QtProcessRunner(QObject):
    started = Signal(str)
    progress = Signal(str, object)
    log = Signal(str, str)
    finished = Signal(str, bool, str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._job_id: UUID | None = None
        self._plan: ProcessPlan | None = None
        self._processes: list[QProcess] = []
        self._parser: FFmpegProgressParser | None = None
        self._cancel_requested = False
        self._errors: list[str] = []

    @property
    def is_running(self) -> bool:
        return self._job_id is not None

    def start(self, job_id: UUID, plan: ProcessPlan) -> None:
        if self.is_running:
            raise RuntimeError("The process runner is already busy")
        if not plan.stages:
            raise ValueError("A process plan must contain at least one stage")
        self._job_id = job_id
        self._plan = plan
        self._parser = FFmpegProgressParser(plan.duration_seconds)
        self._cancel_requested = False
        self._errors = []
        self._processes = []

        for stage in plan.stages:
            process = QProcess(self)
            process.setProgram(str(stage.program))
            process.setArguments(list(stage.arguments))
            process.setProcessChannelMode(QProcess.ProcessChannelMode.SeparateChannels)
            process.readyReadStandardError.connect(partial(self._read_stderr, process))
            process.readyReadStandardOutput.connect(
                partial(self._read_stdout, process, stage.progress_stream)
            )
            process.finished.connect(partial(self._process_finished, process))
            process.errorOccurred.connect(partial(self._process_error, process))
            self._processes.append(process)

        for source, destination in zip(self._processes, self._processes[1:], strict=False):
            source.setStandardOutputProcess(destination)
        for process in reversed(self._processes):
            process.start()
        self.started.emit(str(job_id))

    def cancel(self) -> None:
        if not self.is_running:
            return
        self._cancel_requested = True
        for process in self._processes:
            if process.state() != QProcess.ProcessState.NotRunning:
                process.terminate()
        QTimer.singleShot(3000, self._force_kill)

    def _force_kill(self) -> None:
        if not self.is_running:
            return
        for process in self._processes:
            if process.state() != QProcess.ProcessState.NotRunning:
                process.kill()

    def _read_stderr(self, process: QProcess) -> None:
        if self._job_id is None:
            return
        text = bytes(process.readAllStandardError().data()).decode("utf-8", errors="replace")
        if text:
            self.log.emit(str(self._job_id), text)

    def _read_stdout(self, process: QProcess, progress_stream: str | None) -> None:
        if self._job_id is None:
            return
        text = bytes(process.readAllStandardOutput().data()).decode("utf-8", errors="replace")
        if progress_stream == "stdout" and self._parser is not None:
            for update in self._parser.feed(text):
                self.progress.emit(str(self._job_id), update)
        elif text:
            self.log.emit(str(self._job_id), text)

    def _process_error(self, process: QProcess, error: QProcess.ProcessError) -> None:
        message = process.errorString() or error.name
        if message not in self._errors:
            self._errors.append(message)
        QTimer.singleShot(0, self._check_completion)

    def _process_finished(
        self,
        process: QProcess,
        exit_code: int,
        _exit_status: QProcess.ExitStatus,
    ) -> None:
        if exit_code != 0 and not self._cancel_requested:
            self._errors.append(f"{process.program()} exited with code {exit_code}")
        self._check_completion()

    def _check_completion(self) -> None:
        if self._job_id is None or any(
            process.state() != QProcess.ProcessState.NotRunning for process in self._processes
        ):
            return
        job_id = str(self._job_id)
        cancelled = self._cancel_requested
        error = "\n".join(dict.fromkeys(self._errors))
        success = not cancelled and not error
        processes = self._processes
        self._job_id = None
        self._plan = None
        self._processes = []
        self._parser = None
        self._cancel_requested = False
        self._errors = []
        for process in processes:
            process.deleteLater()
        if cancelled:
            error = "Cancelled"
        self.finished.emit(job_id, success, error)
