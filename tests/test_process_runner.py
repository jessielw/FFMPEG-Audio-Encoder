"""Lifetime tests for the real QtProcessRunner.

The queue tests drive a FakeRunner whose cancel is synchronous, so none of the
termination behaviour is exercised there. These tests spawn real processes.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from uuid import uuid4

import pytest
from PySide6.QtCore import QObject

from ffmpeg_audio_encoder.domain.models import ProcessPlan, ProcessStage
from ffmpeg_audio_encoder.infrastructure import process as process_module
from ffmpeg_audio_encoder.infrastructure.process import QtProcessRunner

# Spawns a grandchild, announces its pid, then idles. The grandchild is what the
# application cannot see: DeeZy launches truehdd/dee/ffmpeg exactly this way.
SPAWNS_GRANDCHILD = (
    "import subprocess, sys, time; "
    "child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(120)']); "
    "print('grandchild', child.pid, file=sys.stderr, flush=True); "
    "time.sleep(120)"
)
SLEEP_FOREVER = "import time; time.sleep(120)"


@pytest.fixture
def runner(qtbot):
    """A runner that outlives its QProcess children.

    Without a parent the Python object can be collected before Qt delivers the
    deferred deletes posted by _check_completion, which aborts the interpreter.
    """
    holder = QObject()
    instance = QtProcessRunner(holder)
    yield instance
    instance.shutdown()
    qtbot.wait(100)


def _pid_is_alive(pid: int) -> bool:
    if sys.platform == "win32":
        # os.kill(pid, 0) terminates the process on Windows, so it cannot be used
        # as a liveness probe here.
        result = subprocess.run(
            ["tasklist.exe", "/FI", f"PID eq {pid}", "/NH"],
            check=False,
            capture_output=True,
            text=True,
        )
        return str(pid) in result.stdout
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def _python_plan(source: str, tmp_path: Path, *, terminate_tree: bool = True) -> ProcessPlan:
    return ProcessPlan(
        (
            ProcessStage(
                Path(sys.executable),
                ("-c", source),
                None,
                terminate_tree=terminate_tree,
            ),
        ),
        tmp_path / "temporary.eac3",
        tmp_path / "final.eac3",
        None,
    )


def test_cancel_kills_the_whole_process_tree(tmp_path: Path, qtbot, runner) -> None:
    logs: list[str] = []
    finished: list[bool] = []
    runner.log.connect(lambda _job_id, message: logs.append(message))
    runner.finished.connect(lambda _job_id, success, _error: finished.append(success))

    runner.start(uuid4(), _python_plan(SPAWNS_GRANDCHILD, tmp_path))
    qtbot.waitUntil(lambda: any("grandchild" in message for message in logs), timeout=20_000)
    grandchild_pid = int(next(message for message in logs if "grandchild" in message).split()[1])
    assert _pid_is_alive(grandchild_pid)

    runner.cancel()
    qtbot.waitUntil(lambda: bool(finished), timeout=20_000)

    assert finished == [False]
    assert not runner.is_running
    qtbot.waitUntil(lambda: not _pid_is_alive(grandchild_pid), timeout=10_000)


def test_force_kill_timer_cannot_reach_a_later_job(
    tmp_path: Path, qtbot, monkeypatch, runner
) -> None:
    """Cancelling one job must not kill the job the queue starts straight after."""
    monkeypatch.setattr(process_module, "FORCE_KILL_DELAY_MS", 250)
    finished: list[tuple[bool, str]] = []
    runner.finished.connect(lambda _job_id, success, error: finished.append((success, error)))

    runner.start(uuid4(), _python_plan(SLEEP_FOREVER, tmp_path))
    runner.cancel()
    qtbot.waitUntil(lambda: bool(finished), timeout=20_000)
    assert finished == [(False, "Cancelled")]

    # The stale timer from the cancel above fires while this job is running.
    runner.start(uuid4(), _python_plan("import time; time.sleep(1.5)", tmp_path))
    qtbot.waitUntil(lambda: len(finished) == 2, timeout=20_000)

    assert finished[1] == (True, "")


def test_stage_that_fails_to_start_tears_down_its_pipeline(tmp_path: Path, qtbot, runner) -> None:
    """Otherwise the surviving stage keeps the runner busy and the window unclosable."""
    plan = ProcessPlan(
        (
            ProcessStage(Path(sys.executable), ("-c", SLEEP_FOREVER), None),
            ProcessStage(tmp_path / "definitely-not-an-encoder", (), None),
        ),
        tmp_path / "temporary.eac3",
        tmp_path / "final.eac3",
        None,
    )
    finished: list[tuple[bool, str]] = []
    runner.finished.connect(lambda _job_id, success, error: finished.append((success, error)))

    runner.start(uuid4(), plan)
    qtbot.waitUntil(lambda: bool(finished), timeout=20_000)

    success, error = finished[0]
    assert not success
    assert error
    assert not runner.is_running


def test_shutdown_terminates_a_running_tree(tmp_path: Path, qtbot, runner) -> None:
    logs: list[str] = []
    runner.log.connect(lambda _job_id, message: logs.append(message))

    runner.start(uuid4(), _python_plan(SPAWNS_GRANDCHILD, tmp_path))
    qtbot.waitUntil(lambda: any("grandchild" in message for message in logs), timeout=20_000)
    grandchild_pid = int(next(message for message in logs if "grandchild" in message).split()[1])

    runner.shutdown()

    qtbot.waitUntil(lambda: not _pid_is_alive(grandchild_pid), timeout=10_000)
