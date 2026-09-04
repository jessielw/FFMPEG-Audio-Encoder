from __future__ import annotations

from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
    Qt,
    Slot,
)
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QApplication, QStyle, QStyledItemDelegate, QStyleOptionProgressBar

from ffmpeg_audio_encoder.application.queue import JobQueueController
from ffmpeg_audio_encoder.domain.models import EncodeJob

_ROOT_INDEX = QModelIndex()


class QueueTableModel(QAbstractTableModel):
    HEADERS = ("State", "Input", "Encoder", "Output", "Progress", "Status")

    def __init__(self, controller: JobQueueController | None = None) -> None:
        super().__init__()
        self.controller: JobQueueController | None = None
        self.set_controller(controller)

    def set_controller(self, controller: JobQueueController | None) -> None:
        if self.controller is not None:
            self.controller.job_added.disconnect(self.refresh)
            self.controller.job_updated.disconnect(self.refresh)
        self.beginResetModel()
        self.controller = controller
        self.endResetModel()
        if controller is not None:
            controller.job_added.connect(self.refresh)
            controller.job_updated.connect(self.refresh)

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = _ROOT_INDEX) -> int:
        del parent
        return len(self.controller.jobs) if self.controller else 0

    def columnCount(self, parent: QModelIndex | QPersistentModelIndex = _ROOT_INDEX) -> int:
        del parent
        return len(self.HEADERS)

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> object:
        if orientation is Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.HEADERS[section]
        return None

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> object:
        if not index.isValid() or self.controller is None:
            return None
        job = self.controller.jobs[index.row()]
        if role == Qt.ItemDataRole.ToolTipRole and job.error:
            return job.error
        if role == Qt.ItemDataRole.UserRole and index.column() == 4:
            return job.progress
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        values = (
            job.state.value.title(),
            job.request.input_path.name,
            job.request.encoder_id,
            job.request.output_path.name,
            "Working…" if job.progress is None else f"{job.progress:.0%}",
            job.status,
        )
        return values[index.column()]

    def job_at(self, row: int) -> EncodeJob | None:
        if self.controller is None or not 0 <= row < len(self.controller.jobs):
            return None
        return self.controller.jobs[row]

    @Slot(str)
    def refresh(self, job_id: str = "") -> None:
        if job_id and self.controller is not None:
            row = next(
                (index for index, job in enumerate(self.controller.jobs) if str(job.id) == job_id),
                -1,
            )
            if row >= 0:
                self.dataChanged.emit(
                    self.index(row, 0),
                    self.index(row, len(self.HEADERS) - 1),
                )
                return
        self.beginResetModel()
        self.endResetModel()


class ProgressDelegate(QStyledItemDelegate):
    def paint(self, painter: QPainter, option, index) -> None:
        if index.column() != 4:
            super().paint(painter, option, index)
            return
        progress = index.data(Qt.ItemDataRole.UserRole)
        progress_option = QStyleOptionProgressBar()
        progress_option.rect = option.rect.adjusted(2, 2, -2, -2)
        progress_option.state = option.state
        progress_option.textVisible = True
        if isinstance(progress, float):
            progress_option.minimum = 0
            progress_option.maximum = 1000
            progress_option.progress = round(progress * 1000)
            progress_option.text = f"{progress:.0%}"
        else:
            progress_option.minimum = 0
            progress_option.maximum = 0
            progress_option.text = "Working..."
        style = option.widget.style() if option.widget is not None else QApplication.style()
        style.drawControl(QStyle.ControlElement.CE_ProgressBar, progress_option, painter)
