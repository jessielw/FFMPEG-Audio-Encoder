"""Files that ship inside the package rather than beside it."""

from __future__ import annotations

from pathlib import Path

_RESOURCES = Path(__file__).resolve().parent


def icon_path() -> Path:
    """Absolute path to the application icon.

    Resolved from this module rather than the working directory, so it holds both
    for a source checkout and for a PyInstaller one-folder bundle, where the package
    is laid out under ``_internal``.
    """
    return _RESOURCES / "icon.ico"
