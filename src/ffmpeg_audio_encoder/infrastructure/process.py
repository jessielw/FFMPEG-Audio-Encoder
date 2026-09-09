from __future__ import annotations

from functools import partial
from uuid import UUID

from PySide6.QtCore import QObject, QProcess, QTimer, Signal

from ffmpeg_audio_encoder.domain.models import ProcessPlan, ProgressProtocol
from ffmpeg_audio_encoder.infrastructure.proc_tree import ProcessTree
from ffmpeg_audio_encoder.infrastructure.progress import DeezyProgressParser, FFmpegProgressParser
from ffmpeg_audio_encoder.infrastructure.qt_lifetime import detach_and_delete

ProgressParser = FFmpegProgressParser | DeezyProgressParser

FORCE_KILL_DELAY_MS = 3000

# A failing tool explains itself on its last few stderr lines. Without them a job
# reports only "exited with code -22", which says nothing about which argument the
# tool rejected, in the log file and in any bug report built from it.
STDERR_TAIL_LINES = 8
STDERR_TAIL_CHARS = 4000


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
        self._parsers: dict[QProcess, ProgressParser] = {}
        self._trees: dict[QProcess, ProcessTree] = {}
        self._stderr_tails: dict[QProcess, str] = {}
        self._killed: set[QProcess] = set()
        self._cancel_requested = False
        self._errors: list[str] = []
        # Bumped on every start so a force-kill timer armed for one run can never
        # reach into the next one.
        self._generation = 0
        self._force_kill_generation = 0
        # Parented to self and reused, so it dies with the runner instead of firing
        # into a torn-down object.
        self._force_kill_timer = QTimer(self)
        self._force_kill_timer.setSingleShot(True)
        self._force_kill_timer.timeout.connect(self._on_force_kill_timeout)

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
        self._parsers = {}
        self._trees = {}
        self._stderr_tails = {}
        self._killed = set()
        self._cancel_requested = False
        self._errors = []
        self._processes = []
        self._generation += 1
        self._force_kill_timer.stop()

        for stage in plan.stages:
            process = QProcess(self)
            process.setProgram(str(stage.program))
            process.setArguments(list(stage.arguments))
            process.setProcessChannelMode(QProcess.ProcessChannelMode.SeparateChannels)
            process.readyReadStandardError.connect(
                partial(self._read_stderr, process, stage.progress_stream)
            )
            process.readyReadStandardOutput.connect(
                partial(self._read_stdout, process, stage.progress_stream)
            )
            process.finished.connect(partial(self._process_finished, process))
            process.errorOccurred.connect(partial(self._process_error, process))
            self._processes.append(process)
            if stage.progress_stream is not None:
                self._parsers[process] = (
                    DeezyProgressParser()
                    if stage.progress_protocol is ProgressProtocol.DEEZY
                    else FFmpegProgressParser(plan.duration_seconds)
                )
            self._trees[process] = ProcessTree(walk_descendants=stage.terminate_tree)
            self._stderr_tails[process] = ""

        for source, destination in zip(self._processes, self._processes[1:], strict=False):
            source.setStandardOutputProcess(destination)
        for index, process in enumerate(self._processes):
            process.start()
            self._trees[process].attach(process.processId())
            if index == 0:
                # Qt opens the child ReadWrite and holds the stdin write end open for
                # the life of the process. Wrapper tools such as DeeZy hand that
                # inherited handle to their own children, which then wait on a pipe
                # that never reaches EOF. Downstream stages of a pipeline must keep
                # their write channel: it is where the previous stage writes.
                process.closeWriteChannel()
        self.started.emit(str(job_id))

    def cancel(self) -> None:
        if not self.is_running:
            return
        self._cancel_requested = True
        self._stop_processes(self._processes)
        self._force_kill_generation = self._generation
        self._force_kill_timer.start(FORCE_KILL_DELAY_MS)

    def shutdown(self) -> None:
        """Last-resort teardown for application exit."""
        self._force_kill_timer.stop()
        for process in self._processes:
            tree = self._trees.get(process)
            if tree is not None:
                tree.kill()
        self._release_trees()

    def _stop_processes(self, processes: list[QProcess]) -> None:
        for process in processes:
            if process.state() == QProcess.ProcessState.NotRunning:
                continue
            self._killed.add(process)
            tree = self._trees.get(process)
            if tree is not None and tree.is_attached:
                tree.terminate()
            else:
                process.terminate()

    def _on_force_kill_timeout(self) -> None:
        self._force_kill(self._force_kill_generation)

    def _force_kill(self, generation: int) -> None:
        if not self.is_running or generation != self._generation:
            return
        for process in self._processes:
            if process.state() != QProcess.ProcessState.NotRunning:
                self._killed.add(process)
                tree = self._trees.get(process)
                if tree is not None and tree.is_attached:
                    tree.kill()
                process.kill()

    def _release_trees(self) -> None:
        for tree in self._trees.values():
            # On Windows this is what reaps a grandchild that outlived its parent.
            tree.close()

    def _read_stderr(self, process: QProcess, progress_stream: str | None) -> None:
        if self._job_id is None:
            return
        text = bytes(process.readAllStandardError().data()).decode("utf-8", errors="replace")
        if text and process in self._stderr_tails:
            # Kept as a rolling window rather than the whole stream: a long encode can
            # write megabytes of stderr, and only the end of it explains a failure.
            self._stderr_tails[process] = (self._stderr_tails[process] + text)[-STDERR_TAIL_CHARS:]
        parser = self._parsers.get(process)
        if progress_stream == "stderr" and parser is not None:
            for update in parser.feed(text):
                self.progress.emit(str(self._job_id), update)
        if text:
            self.log.emit(str(self._job_id), text)

    def _read_stdout(self, process: QProcess, progress_stream: str | None) -> None:
        if self._job_id is None:
            return
        text = bytes(process.readAllStandardOutput().data()).decode("utf-8", errors="replace")
        parser = self._parsers.get(process)
        if progress_stream == "stdout" and parser is not None:
            for update in parser.feed(text):
                self.progress.emit(str(self._job_id), update)
        if text and progress_stream != "stdout":
            self.log.emit(str(self._job_id), text)

    def _process_error(self, process: QProcess, error: QProcess.ProcessError) -> None:
        if self._job_id is None or process in self._killed:
            return
        message = process.errorString() or error.name
        if message not in self._errors:
            self._errors.append(message)
        # A stage that never starts leaves its pipeline siblings holding a pipe that
        # will not close; without this the runner would stay busy forever.
        self._stop_processes([other for other in self._processes if other is not process])
        QTimer.singleShot(0, self._check_completion)

    def _process_finished(
        self,
        process: QProcess,
        exit_code: int,
        _exit_status: QProcess.ExitStatus,
    ) -> None:
        if exit_code != 0 and not self._cancel_requested and process not in self._killed:
            self._errors.append(f"{process.program()} exited with code {exit_code}")
            self._errors.extend(self._stderr_tail(process))
        self._check_completion()

    def _stderr_tail(self, process: QProcess) -> list[str]:
        """The last few meaningful stderr lines the process wrote before it failed."""
        buffered = self._stderr_tails.get(process, "")
        if not buffered:
            return []
        # ffmpeg redraws its stats line with carriage returns, so those are line breaks
        # here too; without that the whole run collapses into one unreadable line.
        lines = [line.strip() for line in buffered.replace("\r", "\n").split("\n")]
        lines = [line for line in lines if line]
        # A buffer that filled up almost certainly starts mid-line.
        if len(buffered) >= STDERR_TAIL_CHARS and lines:
            lines = lines[1:]
        return lines[-STDERR_TAIL_LINES:]

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
        self._force_kill_timer.stop()
        self._release_trees()
        self._job_id = None
        self._plan = None
        self._processes = []
        self._parsers = {}
        self._trees = {}
        self._stderr_tails = {}
        self._killed = set()
        self._cancel_requested = False
        self._errors = []
        for process in processes:
            detach_and_delete(process)
        if cancelled:
            error = "Cancelled"
        self.finished.emit(job_id, success, error)
