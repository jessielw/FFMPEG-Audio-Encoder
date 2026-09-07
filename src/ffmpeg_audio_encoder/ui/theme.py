from __future__ import annotations

import weakref
from dataclasses import dataclass

import qtawesome as qta
from PySide6.QtCore import QObject, QSize, Qt, Slot
from PySide6.QtGui import QAction, QPalette
from PySide6.QtWidgets import QApplication, QPushButton, QToolButton
from shiboken6 import isValid

from ffmpeg_audio_encoder.domain.models import ThemePreference

IconTarget = QPushButton | QToolButton | QAction


@dataclass(slots=True)
class _IconRegistration:
    widget: weakref.ReferenceType[IconTarget]
    name: str
    size: QSize


class ThemeManager(QObject):
    """Applies Qt color schemes and keeps qtawesome icons palette-aware."""

    def __init__(self, app: QApplication) -> None:
        super().__init__(app)
        self.app = app
        self._icons: list[_IconRegistration] = []
        app.styleHints().colorSchemeChanged.connect(self._refresh_icons)

    def apply(self, preference: ThemePreference) -> None:
        hints = self.app.styleHints()
        if preference is ThemePreference.AUTOMATIC:
            hints.unsetColorScheme()
        elif preference is ThemePreference.DARK:
            hints.setColorScheme(Qt.ColorScheme.Dark)
        else:
            hints.setColorScheme(Qt.ColorScheme.Light)
        self._refresh_icons()

    def register(self, widget: IconTarget, icon_name: str, size: int = 20) -> None:
        self._icons.append(_IconRegistration(weakref.ref(widget), icon_name, QSize(size, size)))
        widget.destroyed.connect(self._discard_dead_icons)
        self._set_icon(widget, icon_name, QSize(size, size))

    @Slot()
    def _discard_dead_icons(self) -> None:
        self._icons = [registration for registration in self._icons if registration.widget()]

    @Slot()
    def _refresh_icons(self, *_args: object) -> None:
        live: list[_IconRegistration] = []
        for registration in self._icons:
            widget = registration.widget()
            # A wrapper can outlive its C++ object, so ``destroyed`` alone is not
            # enough to know the target is still there.
            if widget is None or not isValid(widget):
                continue
            self._set_icon(widget, registration.name, registration.size)
            live.append(registration)
        self._icons = live

    def _set_icon(self, widget: IconTarget, name: str, size: QSize) -> None:
        color = self.app.palette().color(QPalette.ColorRole.WindowText).name()
        widget.setIcon(qta.icon(name, color=color))
        # QAction has no icon size of its own; the toolbar or menu holding it decides.
        if not isinstance(widget, QAction):
            widget.setIconSize(size)
