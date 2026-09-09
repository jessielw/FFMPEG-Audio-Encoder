"""Disposal of Qt objects whose owner may not outlive them.

``deleteLater`` hands the C++ object to Qt but leaves it parented, so until the event
loop delivers the deferred delete the object has two things able to destroy it: the
posted event and its parent. PySide6 does not survive both happening. A parent torn
down in the same turn -- a service replaced while a job is finishing, or a test letting
an unparented owner fall out of scope -- aborts the process on Windows with no Qt
message and no Python traceback, which is what it looked like in CI.

Detaching first leaves the posted event as the only owner, so the object is deleted
once, on the next turn, whatever happens to the parent in between.
"""

from __future__ import annotations

from PySide6.QtCore import QObject


def detach_and_delete(obj: QObject) -> None:
    """Schedule ``obj`` for deletion, first removing it from its parent."""
    obj.setParent(None)
    obj.deleteLater()
