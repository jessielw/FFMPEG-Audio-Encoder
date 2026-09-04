from __future__ import annotations

from dataclasses import replace

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ffmpeg_audio_encoder.domain.models import AppSettings, ThemePreference


class _PathRow(QWidget):
    def __init__(self, value: str | None, directory: bool, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.directory = directory
        self.edit = QLineEdit(value or "")
        browse = QPushButton("Browse…")
        browse.clicked.connect(self._browse)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.edit, 1)
        layout.addWidget(browse)

    def _browse(self) -> None:
        if self.directory:
            selected = QFileDialog.getExistingDirectory(self, "Choose directory", self.edit.text())
        else:
            selected, _ = QFileDialog.getOpenFileName(
                self, "Choose executable", self.edit.text(), "All files (*)"
            )
        if selected:
            self.edit.setText(selected)

    def value(self) -> str | None:
        return self.edit.text().strip() or None


class SettingsDialog(QDialog):
    def __init__(self, settings: AppSettings, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._settings = settings
        self.setWindowTitle("Settings")
        self.setMinimumWidth(620)

        self.ffmpeg = _PathRow(settings.ffmpeg_path, directory=False)
        self.ffprobe = _PathRow(settings.ffprobe_path, directory=False)
        self.output = _PathRow(settings.default_output_dir, directory=True)
        self.overwrite = QCheckBox("Allow queued jobs to replace existing outputs")
        self.overwrite.setChecked(settings.overwrite_default)
        self.theme = QComboBox()
        for preference in ThemePreference:
            self.theme.addItem(str(preference), preference.value)
        self.theme.setCurrentIndex(self.theme.findData(settings.theme.value))

        form = QFormLayout()
        form.addRow("FFmpeg", self.ffmpeg)
        form.addRow("ffprobe", self.ffprobe)
        form.addRow("Default output folder", self.output)
        form.addRow("Appearance", self.theme)
        form.addRow("Overwrite", self.overwrite)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)

    def settings(self) -> AppSettings:
        try:
            theme = ThemePreference(str(self.theme.currentData()))
        except ValueError:
            theme = ThemePreference.AUTOMATIC
        return replace(
            self._settings,
            ffmpeg_path=self.ffmpeg.value(),
            ffprobe_path=self.ffprobe.value(),
            default_output_dir=self.output.value(),
            overwrite_default=self.overwrite.isChecked(),
            theme=theme,
        )
