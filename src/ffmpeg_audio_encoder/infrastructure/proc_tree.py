"""Ownership of a spawned process and every descendant it goes on to create.

Some encoders are wrappers: DeeZy launches ffmpeg, truehdd and dee itself, so the
process this application starts is only the root of a small tree. ``QProcess`` knows
nothing about the rest of it, and Windows does not cascade termination, so killing
the root leaves the real work running forever.

On Windows the tree is owned by a job object created with
``JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE``. That covers the case a plain ``taskkill /T``
cannot: when the root exits on its own while a grandchild is still running, closing
the job handle still takes the survivors with it.

On POSIX there is no equivalent primitive reachable from PySide6 (neither
``setChildProcessModifier`` nor ``setUnixProcessParameters`` is exposed), so
descendants are enumerated with ``ps`` at kill time. That is best effort: once the
root has exited, its children are reparented and can no longer be identified.
"""

from __future__ import annotations

import os
import signal
import subprocess
import sys
from contextlib import suppress

if sys.platform == "win32":
    import ctypes
    from ctypes import wintypes

    _kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    _JOB_OBJECT_EXTENDED_LIMIT_INFORMATION = 9
    _JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
    _PROCESS_TERMINATE = 0x0001
    _PROCESS_SET_QUOTA = 0x0100

    class _IoCounters(ctypes.Structure):
        _fields_ = (
            ("ReadOperationCount", ctypes.c_ulonglong),
            ("WriteOperationCount", ctypes.c_ulonglong),
            ("OtherOperationCount", ctypes.c_ulonglong),
            ("ReadTransferCount", ctypes.c_ulonglong),
            ("WriteTransferCount", ctypes.c_ulonglong),
            ("OtherTransferCount", ctypes.c_ulonglong),
        )

    class _BasicLimitInformation(ctypes.Structure):
        _fields_ = (
            ("PerProcessUserTimeLimit", ctypes.c_longlong),
            ("PerJobUserTimeLimit", ctypes.c_longlong),
            ("LimitFlags", wintypes.DWORD),
            ("MinimumWorkingSetSize", ctypes.c_size_t),
            ("MaximumWorkingSetSize", ctypes.c_size_t),
            ("ActiveProcessLimit", wintypes.DWORD),
            ("Affinity", ctypes.c_size_t),
            ("PriorityClass", wintypes.DWORD),
            ("SchedulingClass", wintypes.DWORD),
        )

    class _ExtendedLimitInformation(ctypes.Structure):
        _fields_ = (
            ("BasicLimitInformation", _BasicLimitInformation),
            ("IoInfo", _IoCounters),
            ("ProcessMemoryLimit", ctypes.c_size_t),
            ("JobMemoryLimit", ctypes.c_size_t),
            ("PeakProcessMemoryUsed", ctypes.c_size_t),
            ("PeakJobMemoryUsed", ctypes.c_size_t),
        )

    # Declared explicitly: HANDLEs are pointer sized and ctypes would otherwise
    # truncate them to a C int on 64-bit builds.
    _kernel32.CreateJobObjectW.argtypes = (wintypes.LPVOID, wintypes.LPCWSTR)
    _kernel32.CreateJobObjectW.restype = wintypes.HANDLE
    _kernel32.SetInformationJobObject.argtypes = (
        wintypes.HANDLE,
        ctypes.c_int,
        wintypes.LPVOID,
        wintypes.DWORD,
    )
    _kernel32.SetInformationJobObject.restype = wintypes.BOOL
    _kernel32.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
    _kernel32.OpenProcess.restype = wintypes.HANDLE
    _kernel32.AssignProcessToJobObject.argtypes = (wintypes.HANDLE, wintypes.HANDLE)
    _kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
    _kernel32.TerminateJobObject.argtypes = (wintypes.HANDLE, wintypes.UINT)
    _kernel32.TerminateJobObject.restype = wintypes.BOOL
    _kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    _kernel32.CloseHandle.restype = wintypes.BOOL

    def _create_job(pid: int) -> int | None:
        """Put ``pid`` in a fresh kill-on-close job. ``None`` if that is not possible."""
        handle = _kernel32.CreateJobObjectW(None, None)
        if not handle:
            return None
        limits = _ExtendedLimitInformation()
        limits.BasicLimitInformation.LimitFlags = _JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        assigned = False
        if _kernel32.SetInformationJobObject(
            handle,
            _JOB_OBJECT_EXTENDED_LIMIT_INFORMATION,
            ctypes.byref(limits),
            ctypes.sizeof(limits),
        ):
            process = _kernel32.OpenProcess(_PROCESS_TERMINATE | _PROCESS_SET_QUOTA, False, pid)
            if process:
                assigned = bool(_kernel32.AssignProcessToJobObject(handle, process))
                _kernel32.CloseHandle(process)
        if not assigned:
            _kernel32.CloseHandle(handle)
            return None
        return int(handle)

    def _terminate_job(handle: int) -> None:
        _kernel32.TerminateJobObject(handle, 1)

    def _close_job(handle: int) -> None:
        _kernel32.CloseHandle(handle)

else:

    def _create_job(pid: int) -> int | None:
        return None

    def _terminate_job(handle: int) -> None:
        raise NotImplementedError("Job objects are a Windows facility")

    def _close_job(handle: int) -> None:
        raise NotImplementedError("Job objects are a Windows facility")


class ProcessTree:
    """Owns one spawned process plus anything it spawns.

    A tree that could not be established degrades to terminating the root process
    only, which is what the application did before job objects were introduced.
    """

    __slots__ = ("_handle", "_root_pid", "_walk_descendants")

    def __init__(self, *, walk_descendants: bool = True) -> None:
        self._handle: int | None = None
        self._root_pid: int | None = None
        self._walk_descendants = walk_descendants

    @property
    def is_attached(self) -> bool:
        return self._root_pid is not None

    def attach(self, pid: int) -> bool:
        """Take ownership of ``pid``. Returns whether tree-wide control was gained."""
        if pid <= 0:
            return False
        self._root_pid = pid
        if sys.platform != "win32":
            return True
        self._handle = _create_job(pid)
        return self._handle is not None

    def terminate(self) -> None:
        """Stop the tree. Console children ignore WM_CLOSE, so this is immediate."""
        self.kill()

    def kill(self) -> None:
        if sys.platform == "win32":
            if self._handle is not None:
                _terminate_job(self._handle)
            else:
                _kill_pid(self._root_pid, signal.SIGTERM)
            return
        self._kill_posix_tree(signal.SIGKILL)

    def close(self) -> None:
        """Release the tree, killing anything that outlived the root process."""
        if sys.platform == "win32":
            if self._handle is not None:
                # KILL_ON_JOB_CLOSE means surviving grandchildren die here.
                _close_job(self._handle)
                self._handle = None
        elif self._root_pid is not None and _pid_is_alive(self._root_pid):
            self._kill_posix_tree(signal.SIGKILL)
        self._root_pid = None

    def _kill_posix_tree(self, sig: int) -> None:
        if self._root_pid is None:
            return
        pids = [self._root_pid]
        if self._walk_descendants:
            pids = [*_descendant_pids(self._root_pid), self._root_pid]
        for pid in pids:
            _kill_pid(pid, sig)


def _kill_pid(pid: int | None, sig: int) -> None:
    if pid is None or pid <= 0:
        return
    with suppress(OSError, ValueError):
        os.kill(pid, sig)


def _pid_is_alive(pid: int) -> bool:
    # POSIX only: on Windows os.kill maps to TerminateProcess, so signal 0 would
    # not be the harmless probe it is here.
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def _descendant_pids(root: int) -> list[int]:
    """Depth-first descendants of ``root``, deepest first, via a ``ps`` snapshot."""
    children: dict[int, list[int]] = {}
    try:
        result = subprocess.run(
            ["ps", "-Ao", "pid=,ppid="],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    for line in result.stdout.splitlines():
        columns = line.split()
        if len(columns) != 2:
            continue
        try:
            pid, parent = int(columns[0]), int(columns[1])
        except ValueError:
            continue
        children.setdefault(parent, []).append(pid)
    ordered: list[int] = []
    pending = list(children.get(root, ()))
    while pending:
        pid = pending.pop()
        ordered.append(pid)
        pending.extend(children.get(pid, ()))
    ordered.reverse()
    return ordered
