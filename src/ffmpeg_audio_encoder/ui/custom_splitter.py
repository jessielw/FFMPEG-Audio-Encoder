from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPaintEvent, QPen
from PySide6.QtWidgets import QSplitter, QSplitterHandle, QWidget


class CustomSplitterHandle(QSplitterHandle):
    """Theme-aware splitter handle adapted from NFOForge."""

    def __init__(self, orientation: Qt.Orientation, parent: QSplitter) -> None:
        super().__init__(orientation, parent)
        self.setMinimumSize(12, 12)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter()
        if not painter.begin(self):
            return

        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            dot_color = self.palette().color(self.palette().ColorRole.Mid)
            painter.setPen(QPen(dot_color, 1))
            painter.setBrush(dot_color)

            center_x = self.width() // 2
            center_y = self.height() // 2
            dot_size = 2
            dot_spacing = 6

            if self.width() > self.height():
                for offset in range(-2, 3):
                    x = center_x + (offset * dot_spacing)
                    painter.drawEllipse(
                        x - dot_size // 2,
                        center_y - dot_size // 2,
                        dot_size,
                        dot_size,
                    )
            else:
                for offset in range(-2, 3):
                    y = center_y + (offset * dot_spacing)
                    painter.drawEllipse(
                        center_x - dot_size // 2,
                        y - dot_size // 2,
                        dot_size,
                        dot_size,
                    )
        finally:
            painter.end()


class CustomSplitter(QSplitter):
    """NFOForge-style splitter with a larger, visible grab handle."""

    def __init__(self, orientation: Qt.Orientation, parent: QWidget | None = None) -> None:
        super().__init__(orientation=orientation, parent=parent)
        self.setHandleWidth(12)
        self.setChildrenCollapsible(False)

    def createHandle(self) -> CustomSplitterHandle:
        return CustomSplitterHandle(self.orientation(), self)
