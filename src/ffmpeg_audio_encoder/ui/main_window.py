from __future__ import annotations

import math
import os
from dataclasses import dataclass, field, replace
from pathlib import Path
from uuid import UUID

from PySide6.QtCore import QPoint, Qt, QThread, QTimer, QUrl, Signal
from PySide6.QtGui import (
    QAction,
    QCloseEvent,
    QDesktopServices,
    QDragEnterEvent,
    QDropEvent,
    QIntValidator,
    QKeySequence,
    QStandardItemModel,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QLayout,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QTableView,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ffmpeg_audio_encoder.application.queue import JobQueueController
from ffmpeg_audio_encoder.domain.errors import AudioEncoderError
from ffmpeg_audio_encoder.domain.models import (
    Codec,
    CommonAudioOptions,
    DelaySource,
    DetectedDelay,
    EncoderConfiguration,
    EncoderPreset,
    EncodingRequest,
    JobState,
    JsonScalar,
    MediaAsset,
    OptionKind,
    OutputFormat,
    Toolchain,
)
from ffmpeg_audio_encoder.encoders import default_registry
from ffmpeg_audio_encoder.encoders.base import EncoderAdapter
from ffmpeg_audio_encoder.infrastructure.output import default_output_path, temporary_output_path
from ffmpeg_audio_encoder.infrastructure.persistence import (
    JobRepository,
    PresetRepository,
    SettingsRepository,
)
from ffmpeg_audio_encoder.infrastructure.probe import QtMediaProbe
from ffmpeg_audio_encoder.infrastructure.tools import (
    ToolReport,
    inspect_toolchain,
    locate_toolchain,
)
from ffmpeg_audio_encoder.ui.custom_splitter import CustomSplitter
from ffmpeg_audio_encoder.ui.dialogs import SettingsDialog
from ffmpeg_audio_encoder.ui.models import ProgressDelegate, QueueTableModel
from ffmpeg_audio_encoder.ui.theme import ThemeManager


@dataclass(slots=True)
class InputDraft:
    path: Path
    status: str = "Probing…"
    asset: MediaAsset | None = None
    stream_position: int = 0
    output_override: Path | None = None
    error: str | None = None
    delay_overrides_ms: dict[int, float] = field(default_factory=dict)


OptionWidget = QSpinBox | QDoubleSpinBox | QComboBox | QLineEdit


class ToolInspectionThread(QThread):
    succeeded = Signal(object)
    failed = Signal(str)

    def __init__(self, settings, parent=None) -> None:
        super().__init__(parent)
        self.settings = settings

    def run(self) -> None:
        try:
            self.succeeded.emit(inspect_toolchain(locate_toolchain(self.settings)))
        except AudioEncoderError as exc:
            self.failed.emit(str(exc))


class MainWindow(QMainWindow):
    def __init__(
        self,
        settings_repository: SettingsRepository,
        preset_repository: PresetRepository,
        theme_manager: ThemeManager,
        tool_report: ToolReport | None,
        job_repository: JobRepository | None = None,
    ) -> None:
        super().__init__()
        self.settings_repository = settings_repository
        self.preset_repository = preset_repository
        self.job_repository = job_repository
        self.theme_manager = theme_manager
        self.settings = settings_repository.load()
        self.registry = default_registry()
        self.tool_report = tool_report
        self.probe_service: QtMediaProbe | None = None
        self.queue: JobQueueController | None = None
        self.drafts: list[InputDraft] = []
        self.presets = preset_repository.load()
        self.option_widgets: dict[str, OptionWidget] = {}
        self.job_logs: dict[str, str] = {}
        self._syncing_output = False
        self._restoring_configuration = False
        self._closing = False
        self._expanded_queue_height = 250
        self._tool_thread: ToolInspectionThread | None = None
        self._pending_settings = None
        self._configuration_save_timer = QTimer(self)
        self._configuration_save_timer.setSingleShot(True)
        self._configuration_save_timer.setInterval(350)
        self._configuration_save_timer.timeout.connect(self._persist_last_configuration)

        self.setWindowTitle("FFmpeg Audio Encoder v5")
        self.setAcceptDrops(True)
        self.setMinimumSize(480, 360)
        self.resize(self.settings.window_width, self.settings.window_height)
        if self.settings.window_x is not None and self.settings.window_y is not None:
            self.move(self.settings.window_x, self.settings.window_y)
        self._build_ui()
        self._configure_services(tool_report)
        self._populate_encoders()
        self._populate_presets()
        self._restore_last_configuration()
        self.theme_manager.apply(self.settings.theme)
        self._refresh_actions()
        if tool_report is None:
            self.statusBar().showMessage(
                "FFmpeg/ffprobe are not configured. Open Settings before adding files."
            )

    def _build_ui(self) -> None:
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

        input_actions = QHBoxLayout()
        self.add_files_button = QPushButton("Add files")
        self.remove_inputs_button = QPushButton("Remove selected")
        input_actions.addWidget(self.add_files_button)
        input_actions.addWidget(self.remove_inputs_button)
        input_actions.addStretch(1)
        self.toggle_queue_button = QPushButton("Hide queue")
        self.toggle_queue_button.setCheckable(True)
        self.toggle_queue_button.setChecked(True)
        input_actions.addWidget(self.toggle_queue_button)
        self.settings_button = QPushButton("Settings")
        input_actions.addWidget(self.settings_button)
        outer.addLayout(input_actions)

        self.input_table = QTableWidget(0, 3)
        self.input_table.setHorizontalHeaderLabels(("Input", "Status", "Audio streams"))
        self.input_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.input_table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.input_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.input_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.input_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )
        self.input_table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.ResizeToContents
        )

        config_panel = QGroupBox("Encoding configuration")
        config_panel.setMinimumWidth(340)
        config_layout = QVBoxLayout(config_panel)

        self.config_tabs = QTabWidget()
        self.config_tabs.setDocumentMode(True)
        config_layout.addWidget(self.config_tabs)

        general_page = QWidget()
        general_layout = QVBoxLayout(general_page)
        general_layout.setContentsMargins(9, 9, 9, 9)
        config_form = QFormLayout()
        config_form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        config_form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)
        self.stream_combo = QComboBox()
        self.encoder_combo = QComboBox()
        self.codec_combo = QComboBox()
        self.format_combo = QComboBox()
        self.codec_combo.setEnabled(False)
        self.format_combo.setEnabled(False)
        self.sample_rate = QComboBox()
        self.sample_rate.addItem("Preserve", None)
        self.channels = QComboBox()
        self.channels.addItem("Preserve", None)
        self.gain_db = QDoubleSpinBox()
        self.gain_db.setRange(-30.0, 30.0)
        self.gain_db.setDecimals(1)
        self.gain_db.setSingleStep(0.5)
        self.gain_db.setSuffix(" dB")
        self.tempo_ratio = QDoubleSpinBox()
        self.tempo_ratio.setRange(0.25, 4.0)
        self.tempo_ratio.setDecimals(3)
        self.tempo_ratio.setSingleStep(0.001)
        self.tempo_ratio.setValue(1.0)
        self.delay_ms = QDoubleSpinBox()
        self.delay_ms.setRange(-86_400_000.0, 86_400_000.0)
        self.delay_ms.setDecimals(3)
        self.delay_ms.setSingleStep(1.0)
        self.delay_ms.setSuffix(" ms")
        self.delay_ms.setToolTip(
            "Positive values prepend silence; negative values trim the beginning."
        )
        self.delay_ms.setEnabled(False)
        self.delay_status = QLabel("Select a probed audio track to detect its delay.")
        self.delay_status.setWordWrap(True)
        self.tempo_ratio.setSuffix("x")
        self.stream_details_button = QPushButton("Inspect selected stream")
        config_form.addRow("Audio stream", self.stream_combo)
        config_form.addRow("", self.stream_details_button)
        config_form.addRow("Encoder", self.encoder_combo)
        config_form.addRow("Codec", self.codec_combo)
        config_form.addRow("Container", self.format_combo)
        config_form.addRow("Sample rate", self.sample_rate)
        config_form.addRow("Channel layout", self.channels)
        config_form.addRow("Gain", self.gain_db)
        config_form.addRow("Tempo", self.tempo_ratio)
        config_form.addRow("Audio delay", self.delay_ms)
        config_form.addRow("", self.delay_status)
        general_layout.addLayout(config_form)
        general_layout.addStretch(1)

        self.general_scroll = QScrollArea()
        self.general_scroll.setWidgetResizable(True)
        self.general_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.general_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.general_scroll.setWidget(general_page)
        self.config_tabs.addTab(self.general_scroll, "General")

        options_page = QWidget()
        options_layout = QVBoxLayout(options_page)
        options_layout.setContentsMargins(9, 9, 9, 9)
        self.options_group = QGroupBox()
        self.options_form = QFormLayout(self.options_group)
        self.options_form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.options_form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)
        options_layout.addWidget(self.options_group)
        options_layout.addStretch(1)

        self.options_scroll = QScrollArea()
        self.options_scroll.setWidgetResizable(True)
        self.options_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.options_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.options_scroll.setWidget(options_page)
        self.config_tabs.addTab(self.options_scroll, "Options")

        output_page = QWidget()
        output_layout = QVBoxLayout(output_page)
        output_layout.setContentsMargins(9, 9, 9, 9)
        preset_form = QFormLayout()
        preset_form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        preset_form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)
        self.preset_combo = QComboBox()
        preset_form.addRow("Preset", self.preset_combo)
        output_layout.addLayout(preset_form)

        preset_actions = QHBoxLayout()
        self.save_preset_button = QPushButton("Save preset")
        self.delete_preset_button = QPushButton("Delete preset")
        preset_actions.addStretch(1)
        preset_actions.addWidget(self.save_preset_button)
        preset_actions.addWidget(self.delete_preset_button)
        output_layout.addLayout(preset_actions)

        output_form = QFormLayout()
        output_form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        output_form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)
        self.output_edit = QLineEdit()
        output_path_widget = QWidget()
        output_path_layout = QHBoxLayout(output_path_widget)
        output_path_layout.setContentsMargins(0, 0, 0, 0)
        output_path_layout.addWidget(self.output_edit, 1)
        self.browse_output_button = QPushButton("Browse...")
        output_path_layout.addWidget(self.browse_output_button)
        self.overwrite = QCheckBox("Replace an existing file")
        self.overwrite.setChecked(self.settings.overwrite_default)
        output_form.addRow("Output", output_path_widget)
        output_form.addRow("Collision policy", self.overwrite)
        output_layout.addLayout(output_form)

        self.command_preview = QPlainTextEdit()
        self.command_preview.setReadOnly(True)
        self.command_preview.setMaximumHeight(92)
        self.command_preview.setPlaceholderText(
            "Select a successfully probed input to preview the command"
        )
        output_layout.addWidget(QLabel("Command preview"))
        output_layout.addWidget(self.command_preview)
        output_layout.addStretch(1)

        self.output_scroll = QScrollArea()
        self.output_scroll.setWidgetResizable(True)
        self.output_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.output_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.output_scroll.setWidget(output_page)
        self.config_tabs.addTab(self.output_scroll, "Output")

        self.draft_splitter = CustomSplitter(Qt.Orientation.Horizontal)
        self.draft_splitter.addWidget(self.input_table)
        self.draft_splitter.addWidget(config_panel)
        self.draft_splitter.setMinimumHeight(240)
        self.draft_splitter.setStretchFactor(0, 3)
        self.draft_splitter.setStretchFactor(1, 2)

        queue_panel = QWidget()
        queue_layout = QVBoxLayout(queue_panel)
        queue_layout.setContentsMargins(0, 0, 0, 0)
        queue_primary_actions = QHBoxLayout()
        queue_primary_actions.addWidget(QLabel("Encoding queue"))
        self.queue_selected_button = QPushButton("Queue selected inputs")
        self.queue_start_button = QPushButton("Queue and start")
        self.start_button = QPushButton("Start queue")
        self.start_selected_button = QPushButton("Start selected")
        self.stop_button = QPushButton("Stop after current")
        self.cancel_button = QPushButton("Cancel active")
        self.cancel_all_button = QPushButton("Cancel all")
        self.retry_button = QPushButton("Retry selected")
        self.remove_jobs_button = QPushButton("Remove selected")
        self.clear_button = QPushButton("Clear finished")
        for button in (
            self.queue_selected_button,
            self.queue_start_button,
            self.start_button,
            self.start_selected_button,
        ):
            queue_primary_actions.addWidget(button)
        queue_primary_actions.addStretch(1)
        queue_layout.addLayout(queue_primary_actions)

        queue_secondary_actions = QHBoxLayout()
        for button in (
            self.stop_button,
            self.cancel_button,
            self.cancel_all_button,
            self.retry_button,
            self.remove_jobs_button,
            self.clear_button,
        ):
            queue_secondary_actions.addWidget(button)
        queue_secondary_actions.addStretch(1)
        queue_layout.addLayout(queue_secondary_actions)
        self.queue_model = QueueTableModel()
        self.queue_table = QTableView()
        self.queue_table.setModel(self.queue_model)
        self.queue_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.queue_table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.queue_table.setItemDelegateForColumn(4, ProgressDelegate(self.queue_table))
        self.queue_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.queue_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.queue_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.queue_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        queue_layout.addWidget(self.queue_table)
        self.queue_summary = QLabel("No jobs")
        queue_layout.addWidget(self.queue_summary)
        self.job_details = QPlainTextEdit()
        self.job_details.setReadOnly(True)
        self.job_details.setMaximumHeight(130)
        self.job_details.setPlaceholderText("Select a job to see its details")
        self.log_output = QPlainTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMaximumBlockCount(3000)
        self.log_output.setMaximumHeight(130)
        self.queue_details_tabs = QTabWidget()
        self.queue_details_tabs.addTab(self.job_details, "Selected job")
        self.queue_details_tabs.addTab(self.log_output, "Session log")
        queue_layout.addWidget(self.queue_details_tabs)
        queue_panel.setMinimumHeight(0)

        self.main_splitter = CustomSplitter(Qt.Orientation.Vertical)
        self.main_splitter.addWidget(self.draft_splitter)
        self.main_splitter.addWidget(queue_panel)
        self.main_splitter.setChildrenCollapsible(True)
        self.main_splitter.setCollapsible(0, False)
        self.main_splitter.setCollapsible(1, True)
        self.main_splitter.setStretchFactor(0, 3)
        self.main_splitter.setStretchFactor(1, 2)
        outer.addWidget(self.main_splitter)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setWidget(page)
        self.setCentralWidget(scroll_area)

        self.theme_manager.register(self.add_files_button, "ph.files-light")
        self.theme_manager.register(self.settings_button, "ph.gear-light")
        self.theme_manager.register(self.toggle_queue_button, "ph.queue-light")
        self.theme_manager.register(self.queue_selected_button, "ph.queue-light")
        self.theme_manager.register(self.queue_start_button, "ph.play-circle-light")
        self.theme_manager.register(self.start_button, "ph.play-light")
        self.theme_manager.register(self.cancel_button, "ph.stop-light")

        self.add_files_button.clicked.connect(self._choose_files)
        self.remove_inputs_button.clicked.connect(self._remove_inputs)
        self.settings_button.clicked.connect(self._open_settings)
        self.toggle_queue_button.toggled.connect(self._set_queue_visible)
        self.main_splitter.splitterMoved.connect(self._splitter_moved)
        self.input_table.itemSelectionChanged.connect(self._sync_selected_draft)
        self.stream_combo.currentIndexChanged.connect(self._stream_changed)
        self.stream_details_button.clicked.connect(self._show_stream_details)
        self.encoder_combo.currentIndexChanged.connect(self._encoder_changed)
        self.codec_combo.currentIndexChanged.connect(self._common_options_changed)
        self.format_combo.currentIndexChanged.connect(self._common_options_changed)
        self.sample_rate.currentTextChanged.connect(self._common_options_changed)
        self.channels.currentIndexChanged.connect(self._common_options_changed)
        self.gain_db.valueChanged.connect(self._common_options_changed)
        self.tempo_ratio.valueChanged.connect(self._common_options_changed)
        self.delay_ms.valueChanged.connect(self._delay_changed)
        self.output_edit.textEdited.connect(self._output_edited)
        self.browse_output_button.clicked.connect(self._browse_output)
        self.queue_selected_button.clicked.connect(self._queue_selected)
        self.queue_start_button.clicked.connect(self._queue_and_start_selected)
        self.start_button.clicked.connect(self._start_queue)
        self.start_selected_button.clicked.connect(self._start_selected_jobs)
        self.stop_button.clicked.connect(self._stop_queue)
        self.cancel_button.clicked.connect(self._cancel_active)
        self.cancel_all_button.clicked.connect(self._cancel_all)
        self.retry_button.clicked.connect(self._retry_selected)
        self.remove_jobs_button.clicked.connect(self._remove_selected_jobs)
        self.clear_button.clicked.connect(self._clear_finished)
        self.save_preset_button.clicked.connect(self._save_preset)
        self.delete_preset_button.clicked.connect(self._delete_preset)
        self.preset_combo.currentIndexChanged.connect(self._apply_preset)
        self.queue_table.selectionModel().selectionChanged.connect(self._selected_job_changed)
        self.queue_table.customContextMenuRequested.connect(self._queue_context_menu)
        self.input_table.itemSelectionChanged.connect(self._refresh_actions)

        self._build_menus()

        QTimer.singleShot(0, self._restore_splitters)

    def _build_menus(self) -> None:
        file_menu = self.menuBar().addMenu("&File")
        open_action = QAction("&Open files...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self._choose_files)
        file_menu.addAction(open_action)
        queue_start_action = QAction("Queue and &start selected", self)
        queue_start_action.setShortcut(QKeySequence("Ctrl+Return"))
        queue_start_action.triggered.connect(self._queue_and_start_selected)
        file_menu.addAction(queue_start_action)
        file_menu.addSeparator()
        quit_action = QAction("&Quit", self)
        quit_action.setShortcut(QKeySequence.StandardKey.Quit)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        edit_menu = self.menuBar().addMenu("&Edit")
        settings_action = QAction("&Settings...", self)
        settings_action.setShortcut(QKeySequence("Ctrl+,"))
        settings_action.triggered.connect(self._open_settings)
        edit_menu.addAction(settings_action)

        help_menu = self.menuBar().addMenu("&Help")
        documentation_action = QAction("&Documentation", self)
        documentation_action.setShortcut(QKeySequence.StandardKey.HelpContents)
        documentation_action.triggered.connect(
            lambda: QDesktopServices.openUrl(
                QUrl("https://github.com/jessielw/FFMPEG-Audio-Encoder/wiki")
            )
        )
        help_menu.addAction(documentation_action)
        project_action = QAction("Project page", self)
        project_action.triggered.connect(
            lambda: QDesktopServices.openUrl(
                QUrl("https://github.com/jessielw/FFMPEG-Audio-Encoder")
            )
        )
        help_menu.addAction(project_action)
        issue_action = QAction("Report an issue", self)
        issue_action.triggered.connect(
            lambda: QDesktopServices.openUrl(
                QUrl("https://github.com/jessielw/FFMPEG-Audio-Encoder/issues/new/choose")
            )
        )
        help_menu.addAction(issue_action)
        help_menu.addAction("Copy diagnostics", self._copy_diagnostics)
        help_menu.addSeparator()
        help_menu.addAction("&About", self._show_about)

    def _copy_diagnostics(self) -> None:
        report = self.tool_report
        lines = ["FFmpeg Audio Encoder v5"]
        if report is None:
            lines.append("Toolchain: unavailable")
        else:
            lines.extend(
                (
                    f"FFmpeg: {report.ffmpeg_version}",
                    f"ffprobe: {report.ffprobe_version}",
                    f"qaac: {report.qaac_version or 'unavailable'}",
                    f"fdkaac: {report.fdkaac_version or 'unavailable'}",
                )
            )
        QApplication.clipboard().setText("\n".join(lines))
        self.statusBar().showMessage("Diagnostics copied to the clipboard", 5000)

    def _show_about(self) -> None:
        QMessageBox.about(
            self,
            "About FFmpeg Audio Encoder",
            "FFmpeg Audio Encoder v5\n\nA cross-platform PySide6 front end for "
            "FFmpeg, qaac, and fdkaac.\n\nLicensed under the MIT License.",
        )

    def _restore_splitters(self) -> None:
        self.draft_splitter.setSizes(list(self.settings.draft_splitter_sizes))
        self.main_splitter.setSizes(list(self.settings.main_splitter_sizes))
        lower_size = self.main_splitter.sizes()[1]
        if lower_size > 0:
            self._expanded_queue_height = lower_size
        if self.settings.queue_panel_collapsed:
            self._set_queue_visible(False)

    def _set_queue_visible(self, visible: bool) -> None:
        sizes = self.main_splitter.sizes()
        if visible:
            total = max(sum(sizes), self.main_splitter.height())
            lower = min(self._expanded_queue_height, max(total - 1, 1))
            self.main_splitter.setSizes([max(total - lower, 1), lower])
        else:
            if sizes[1] > 0:
                self._expanded_queue_height = sizes[1]
            self.main_splitter.setSizes([max(sum(sizes), 1), 0])
        self._sync_queue_toggle(visible)

    def _splitter_moved(self, *_args: object) -> None:
        lower_size = self.main_splitter.sizes()[1]
        if lower_size > 0:
            self._expanded_queue_height = lower_size
        self._sync_queue_toggle(lower_size > 0)

    def _sync_queue_toggle(self, visible: bool) -> None:
        self.toggle_queue_button.blockSignals(True)
        self.toggle_queue_button.setChecked(visible)
        self.toggle_queue_button.setText("Hide queue" if visible else "Show queue")
        self.toggle_queue_button.blockSignals(False)

    def _configure_services(self, report: ToolReport | None) -> None:
        if self.probe_service is not None:
            self.probe_service.cancel_all()
            self.probe_service.deleteLater()
        if self.queue is not None:
            self.queue.shutdown()
            self.queue.deleteLater()
        self.tool_report = report
        if report is None:
            self.probe_service = None
            self.queue = None
            self.queue_model.set_controller(None)
            self._refresh_queue_summary()
            self._refresh_actions()
            return

        self.probe_service = QtMediaProbe(report.toolchain.ffprobe, self)
        self.probe_service.completed.connect(self._probe_completed)
        self.probe_service.failed.connect(self._probe_failed)
        self.queue = JobQueueController(
            self.registry,
            report.toolchain,
            job_repository=self.job_repository,
            parent=self,
        )
        self.queue.log.connect(self._append_log)
        self.queue.active_changed.connect(self._active_changed)
        self.queue.job_added.connect(self._queue_changed)
        self.queue.job_updated.connect(self._queue_changed)
        self.queue.persistence_error.connect(
            lambda message: self.statusBar().showMessage(message, 12000)
        )
        self.queue_model.set_controller(self.queue)
        self._refresh_queue_summary()
        self._refresh_actions()
        self.statusBar().showMessage(
            f"Ready · {report.ffmpeg_version} · {report.ffprobe_version}", 12000
        )

    def _queue_changed(self, *_args: object) -> None:
        self._refresh_queue_summary()
        self._selected_job_changed()
        self._refresh_actions()

    def _populate_encoders(self) -> None:
        current_id = self.encoder_combo.currentData()
        self.encoder_combo.blockSignals(True)
        self.encoder_combo.clear()
        for adapter in self.registry:
            available = self._adapter_available(adapter.descriptor.id)
            label = (
                adapter.descriptor.display_name
                if available
                else f"{adapter.descriptor.display_name} (unavailable)"
            )
            self.encoder_combo.addItem(label, adapter.descriptor.id)
            model = self.encoder_combo.model()
            if isinstance(model, QStandardItemModel):
                model.item(self.encoder_combo.count() - 1).setEnabled(available)
        index = self.encoder_combo.findData(current_id)
        if index < 0:
            index = next(
                (
                    i
                    for i in range(self.encoder_combo.count())
                    if self._adapter_available(str(self.encoder_combo.itemData(i)))
                ),
                0,
            )
        self.encoder_combo.setCurrentIndex(index)
        self.encoder_combo.blockSignals(False)
        self._encoder_changed()

    def _adapter_available(self, adapter_id: str) -> bool:
        if self.tool_report is None:
            return False
        try:
            adapter = self.registry.get(adapter_id)
        except KeyError:
            return False
        return self.tool_report.supports_adapter(adapter.descriptor)

    def _current_adapter(self) -> EncoderAdapter | None:
        adapter_id = self.encoder_combo.currentData()
        return self.registry.get(adapter_id) if isinstance(adapter_id, str) else None

    def _encoder_changed(self, *_args: object) -> None:
        adapter = self._current_adapter()
        current_layout = self.channels.currentData()
        current_sample_rate = self._sample_rate_value()
        self.codec_combo.clear()
        self.format_combo.clear()
        self.channels.clear()
        self.channels.addItem("Preserve", None)
        if adapter is None:
            return
        for codec in adapter.descriptor.codecs:
            self.codec_combo.addItem(str(codec), codec.value)
        for output_format in adapter.descriptor.output_formats:
            if (
                self.tool_report is None
                or not adapter.descriptor.output_muxed_by_ffmpeg
                or self.tool_report.supports_muxer(output_format)
            ):
                self.format_combo.addItem(str(output_format), output_format.value)
        for layout in adapter.descriptor.channel_layouts:
            self.channels.addItem(layout.label, layout.value)
        layout_index = self.channels.findData(current_layout)
        self.channels.setCurrentIndex(max(layout_index, 0))
        self._populate_sample_rates(adapter, current_sample_rate)
        self._rebuild_option_widgets(adapter)
        self._refresh_preview()
        self._schedule_configuration_save()

    def _populate_sample_rates(
        self, adapter: EncoderAdapter, current_sample_rate: int | None
    ) -> None:
        descriptor = adapter.descriptor
        self.sample_rate.blockSignals(True)
        self.sample_rate.clear()
        self.sample_rate.setEditable(descriptor.sample_rate_range is not None)
        self.sample_rate.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.sample_rate.addItem("Preserve", None)
        for rate in descriptor.sample_rate_choices:
            self.sample_rate.addItem(f"{rate:,} Hz", rate)
        if descriptor.sample_rate_range is not None:
            minimum, maximum = descriptor.sample_rate_range
            line_edit = self.sample_rate.lineEdit()
            if line_edit is not None:
                line_edit.setValidator(QIntValidator(minimum, maximum, line_edit))
            self.sample_rate.setToolTip(
                "Choose a common rate or type any rate supported by this encoder "
                f"from {minimum:,} to {maximum:,} Hz."
            )
        else:
            self.sample_rate.setToolTip("Sample rates supported by this FFmpeg encoder.")
        self._set_sample_rate(current_sample_rate)
        self.sample_rate.blockSignals(False)

    def _sample_rate_value(self) -> int | None:
        data = self.sample_rate.currentData()
        if isinstance(data, int) and not isinstance(data, bool):
            return data
        text = self.sample_rate.currentText().strip()
        if not text or self.sample_rate.currentIndex() == 0:
            return None
        try:
            return int(text)
        except ValueError as exc:
            raise ValueError("Enter a valid sample rate in Hz") from exc

    def _set_sample_rate(self, sample_rate: int | None) -> bool:
        if sample_rate is None:
            self.sample_rate.setCurrentIndex(0)
            return True
        index = self.sample_rate.findData(sample_rate)
        if index >= 0:
            self.sample_rate.setCurrentIndex(index)
            return True
        adapter = self._current_adapter()
        limits = adapter.descriptor.sample_rate_range if adapter is not None else None
        if self.sample_rate.isEditable() and limits is not None:
            minimum, maximum = limits
            if minimum <= sample_rate <= maximum:
                self.sample_rate.setCurrentIndex(-1)
                self.sample_rate.setEditText(str(sample_rate))
                return True
        self.sample_rate.setCurrentIndex(0)
        return False

    def _rebuild_option_widgets(self, adapter: EncoderAdapter) -> None:
        while self.options_form.rowCount():
            self.options_form.removeRow(0)
        self.options_group.setTitle(f"{adapter.descriptor.display_name} options")
        self.option_widgets = {}
        for definition in adapter.descriptor.options:
            if definition.kind is OptionKind.INTEGER:
                widget = QSpinBox()
                widget.setRange(
                    int(definition.minimum) if definition.minimum is not None else 0,
                    int(definition.maximum) if definition.maximum is not None else 2_147_483_647,
                )
                if not isinstance(definition.default, int) or isinstance(definition.default, bool):
                    raise TypeError(f"Integer option {definition.key} has a non-integer default")
                widget.setValue(definition.default)
                widget.setSingleStep(int(definition.step))
                widget.setSuffix(definition.suffix)
                widget.valueChanged.connect(self._option_values_changed)
            elif definition.kind is OptionKind.DECIMAL:
                widget = QDoubleSpinBox()
                widget.setRange(
                    definition.minimum if definition.minimum is not None else 0,
                    definition.maximum if definition.maximum is not None else 1_000_000,
                )
                if isinstance(definition.default, bool) or not isinstance(
                    definition.default, (int, float)
                ):
                    raise TypeError(f"Decimal option {definition.key} has a non-number default")
                widget.setDecimals(definition.decimals)
                widget.setSingleStep(definition.step)
                widget.setValue(float(definition.default))
                widget.setSuffix(definition.suffix)
                widget.valueChanged.connect(self._option_values_changed)
            elif definition.kind is OptionKind.CHOICE:
                widget = QComboBox()
                for choice in definition.choices:
                    widget.addItem(choice.label, choice.value)
                widget.setCurrentIndex(widget.findData(definition.default))
                widget.currentIndexChanged.connect(self._option_values_changed)
            else:
                widget = QLineEdit()
                if not isinstance(definition.default, str):
                    raise TypeError(f"Text option {definition.key} has a non-string default")
                widget.setText(definition.default)
                widget.setPlaceholderText("Example: -cutoff 18000")
                widget.textChanged.connect(self._option_values_changed)
            widget.setToolTip(definition.tooltip)
            self.option_widgets[definition.key] = widget
            self.options_form.addRow(definition.label, widget)
        self._refresh_option_states()

    def _widget_value(self, widget: OptionWidget) -> JsonScalar:
        if isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            return widget.value()
        if isinstance(widget, QComboBox):
            return widget.currentData()
        return widget.text()

    def _option_values_changed(self, *_args: object) -> None:
        self._refresh_option_states()
        self._refresh_preview()
        self._schedule_configuration_save()

    def _common_options_changed(self, *_args: object) -> None:
        self._refresh_preview()
        self._schedule_configuration_save()

    def _delay_changed(self, value: float) -> None:
        draft = self._current_draft()
        if draft is None or draft.asset is None:
            return
        stream = draft.asset.audio_streams[draft.stream_position]
        detected = self._detected_delay(draft, stream.index)
        automatic = detected.milliseconds if detected is not None else 0.0
        if math.isclose(value, automatic, abs_tol=0.0005):
            draft.delay_overrides_ms.pop(stream.index, None)
        else:
            draft.delay_overrides_ms[stream.index] = value
        self._update_delay_status(draft, stream.index)
        self._refresh_preview()

    def _refresh_option_states(self) -> None:
        adapter = self._current_adapter()
        if adapter is None:
            return
        for definition in adapter.descriptor.options:
            widget = self.option_widgets.get(definition.key)
            if widget is None:
                continue
            enabled = True
            if definition.enabled_when_key is not None:
                controlling = self.option_widgets.get(definition.enabled_when_key)
                enabled = (
                    controlling is not None
                    and self._widget_value(controlling) in definition.enabled_when_values
                )
            widget.setEnabled(enabled)

    def _choose_files(self) -> None:
        paths, _ = QFileDialog.getOpenFileNames(self, "Choose media files", "", "All files (*)")
        self._add_paths(Path(path) for path in paths)

    def _add_paths(self, paths) -> None:
        if self.probe_service is None:
            QMessageBox.warning(self, "Tools not configured", "Configure FFmpeg and ffprobe first.")
            return
        existing = {draft.path for draft in self.drafts}
        for raw_path in paths:
            path = raw_path.expanduser().resolve()
            if not path.is_file() or path in existing:
                continue
            existing.add(path)
            draft = InputDraft(path)
            self.drafts.append(draft)
            row = self.input_table.rowCount()
            self.input_table.insertRow(row)
            path_item = QTableWidgetItem(path.name)
            path_item.setToolTip(str(path))
            self.input_table.setItem(row, 0, path_item)
            self.input_table.setItem(row, 1, QTableWidgetItem(draft.status))
            self.input_table.setItem(row, 2, QTableWidgetItem("…"))
            self.probe_service.probe(path)
        if self.input_table.rowCount() and self.input_table.currentRow() < 0:
            self.input_table.selectRow(0)

    def _probe_completed(self, path_string: str, raw_asset: object) -> None:
        if not isinstance(raw_asset, MediaAsset):
            return
        row = self._draft_row(Path(path_string))
        if row < 0:
            return
        draft = self.drafts[row]
        draft.asset = raw_asset
        draft.status = "Ready"
        status_item = self.input_table.item(row, 1)
        streams_item = self.input_table.item(row, 2)
        if status_item is not None:
            status_item.setText("Ready")
        if streams_item is not None:
            streams_item.setText(str(len(raw_asset.audio_streams)))
        if row == self.input_table.currentRow():
            self._sync_selected_draft()
        self._refresh_actions()

    def _probe_failed(self, path_string: str, error: str) -> None:
        row = self._draft_row(Path(path_string))
        if row < 0:
            return
        draft = self.drafts[row]
        draft.status = "Failed"
        draft.error = error
        item = self.input_table.item(row, 1)
        if item is not None:
            item.setText("Failed")
            item.setToolTip(error)
        self._refresh_actions()

    def _draft_row(self, path: Path) -> int:
        return next((index for index, draft in enumerate(self.drafts) if draft.path == path), -1)

    def _sync_selected_draft(self) -> None:
        draft = self._current_draft()
        self.stream_combo.blockSignals(True)
        self.stream_combo.clear()
        if draft and draft.asset:
            for stream in draft.asset.audio_streams:
                self.stream_combo.addItem(stream.display_name)
            self.stream_combo.setCurrentIndex(draft.stream_position)
        self.stream_combo.blockSignals(False)
        self._sync_delay_control()
        self._refresh_preview()
        self._refresh_actions()

    def _stream_changed(self, position: int) -> None:
        draft = self._current_draft()
        if draft and draft.asset and 0 <= position < len(draft.asset.audio_streams):
            draft.stream_position = position
            draft.output_override = None
        self._sync_delay_control()
        self._refresh_preview()

    @staticmethod
    def _detected_delay(draft: InputDraft, stream_index: int) -> DetectedDelay | None:
        if draft.asset is None:
            return None
        return next(
            (
                detected
                for detected in draft.asset.detected_delays
                if detected.stream_index == stream_index
            ),
            None,
        )

    def _effective_delay_ms(self, draft: InputDraft, stream_index: int) -> float:
        override = draft.delay_overrides_ms.get(stream_index)
        if override is not None:
            return override
        detected = self._detected_delay(draft, stream_index)
        return detected.milliseconds if detected is not None else 0.0

    def _sync_delay_control(self) -> None:
        draft = self._current_draft()
        self.delay_ms.blockSignals(True)
        if draft is None or draft.asset is None:
            self.delay_ms.setValue(0.0)
            self.delay_ms.setEnabled(False)
            self.delay_status.setText("Select a probed audio track to detect its delay.")
        else:
            stream = draft.asset.audio_streams[draft.stream_position]
            self.delay_ms.setEnabled(True)
            self.delay_ms.setValue(self._effective_delay_ms(draft, stream.index))
            self._update_delay_status(draft, stream.index)
        self.delay_ms.blockSignals(False)

    def _update_delay_status(self, draft: InputDraft, stream_index: int) -> None:
        detected = self._detected_delay(draft, stream_index)
        override = draft.delay_overrides_ms.get(stream_index)
        if override is not None:
            detected_text = (
                f"; detected {detected.milliseconds:+.3f} ms from {detected.source.value}"
                if detected is not None
                else ""
            )
            self.delay_status.setText(f"Manual override{detected_text}.")
        elif detected is not None:
            self.delay_status.setText(
                f"Automatically detected {detected.milliseconds:+.3f} ms "
                f"from {detected.source.value}."
            )
        elif draft.asset is not None and draft.asset.delay_detection_note:
            self.delay_status.setText(draft.asset.delay_detection_note)
        elif draft.asset is not None and draft.asset.has_video_reference:
            self.delay_status.setText("Container delay was unavailable; using 0 ms.")
        else:
            self.delay_status.setText("No filename DELAY marker detected; using 0 ms.")

    def _show_stream_details(self) -> None:
        draft = self._current_draft()
        if draft is None or draft.asset is None:
            return
        stream = draft.asset.audio_streams[draft.stream_position]
        detected = self._detected_delay(draft, stream.index)
        effective_delay = self._effective_delay_ms(draft, stream.index)
        duration = (
            f"{stream.duration_seconds:.3f} seconds"
            if stream.duration_seconds is not None
            else "Unknown"
        )
        QMessageBox.information(
            self,
            f"Audio stream {stream.ordinal}",
            "\n".join(
                (
                    f"File: {draft.path}",
                    f"FFmpeg stream index: {stream.index}",
                    f"Codec: {stream.codec_name}",
                    f"Channels: {stream.channels or 'Unknown'}",
                    f"Layout: {stream.channel_layout or 'Unknown'}",
                    f"Sample rate: {stream.sample_rate or 'Unknown'}",
                    f"Language: {stream.language or 'Unknown'}",
                    f"Title: {stream.title or 'Untitled'}",
                    f"Duration: {duration}",
                    (
                        f"Detected delay: {detected.milliseconds:+.3f} ms ({detected.source.value})"
                        if detected is not None
                        else "Detected delay: Unavailable"
                    ),
                    f"Effective delay: {effective_delay:+.3f} ms",
                )
            ),
        )

    def _current_draft(self) -> InputDraft | None:
        row = self.input_table.currentRow()
        return self.drafts[row] if 0 <= row < len(self.drafts) else None

    def _selected_drafts(self) -> list[InputDraft]:
        rows = sorted({index.row() for index in self.input_table.selectedIndexes()})
        return [self.drafts[row] for row in rows]

    def _current_options(self) -> dict[str, JsonScalar]:
        return {key: self._widget_value(widget) for key, widget in self.option_widgets.items()}

    def _build_request(self, draft: InputDraft) -> EncodingRequest:
        if draft.asset is None:
            raise ValueError(f"{draft.path.name} has not been probed successfully")
        adapter = self._current_adapter()
        try:
            codec = Codec(str(self.codec_combo.currentData()))
            output_format = OutputFormat(str(self.format_combo.currentData()))
        except ValueError as exc:
            raise ValueError("Select an available encoder") from exc
        if adapter is None:
            raise ValueError("Select an available encoder")
        stream = draft.asset.audio_streams[draft.stream_position]
        output_directory = (
            Path(self.settings.default_output_dir) if self.settings.default_output_dir else None
        )
        detected_delay = self._detected_delay(draft, stream.index)
        output = draft.output_override or default_output_path(
            draft.path,
            stream,
            codec,
            output_format,
            output_directory,
            strip_delay_marker=(
                detected_delay is not None and detected_delay.source is DelaySource.FILENAME
            ),
        )
        if draft.output_override is not None and output.suffix.lower() != output_format.suffix:
            raise ValueError(f"Output extension must be {output_format.suffix} for {output_format}")
        return EncodingRequest(
            input_path=draft.path,
            stream=stream,
            encoder_id=adapter.descriptor.id,
            codec=codec,
            output_format=output_format,
            output_path=output,
            common=CommonAudioOptions(
                sample_rate=self._sample_rate_value(),
                channel_layout=self.channels.currentData(),
                gain_db=self.gain_db.value(),
                tempo_ratio=self.tempo_ratio.value(),
                delay_ms=self._effective_delay_ms(draft, stream.index),
            ),
            encoder_options=self._current_options(),
        )

    def _refresh_preview(self, *_args: object) -> None:
        draft = self._current_draft()
        if draft is None or draft.asset is None:
            self.command_preview.clear()
            return
        try:
            request = self._build_request(draft)
            self._syncing_output = True
            self.output_edit.setText(str(request.output_path))
            self._syncing_output = False
            toolchain = (
                self.tool_report.toolchain
                if self.tool_report
                else Toolchain(Path("ffmpeg"), Path("ffprobe"))
            )
            adapter = self.registry.get(request.encoder_id)
            plan = adapter.build_plan(
                request, toolchain, temporary_output_path(request.output_path, UUID(int=0))
            )
            self.command_preview.setPlainText(plan.display_command())
        except (ValueError, AudioEncoderError) as exc:
            self.command_preview.setPlainText(str(exc))

    def _output_edited(self, text: str) -> None:
        if self._syncing_output:
            return
        draft = self._current_draft()
        if draft is not None:
            draft.output_override = Path(text).expanduser() if text.strip() else None
        self._refresh_preview()

    def _browse_output(self) -> None:
        draft = self._current_draft()
        if draft is None or draft.asset is None:
            return
        try:
            output_format = OutputFormat(str(self.format_combo.currentData()))
            suggested = self._build_request(draft).output_path
        except (ValueError, AudioEncoderError):
            return
        selected, _ = QFileDialog.getSaveFileName(
            self,
            "Choose output file",
            str(suggested),
            f"{output_format} (*{output_format.suffix})",
        )
        if not selected:
            return
        path = Path(selected)
        if path.suffix.lower() != output_format.suffix:
            path = path.with_suffix(output_format.suffix)
        draft.output_override = path
        self.output_edit.setText(str(path))
        self._refresh_preview()

    def _queue_selected(self) -> set[UUID]:
        if self.queue is None:
            QMessageBox.warning(self, "Tools not configured", "Configure FFmpeg and ffprobe first.")
            return set()
        drafts = self._selected_drafts()
        if not drafts:
            QMessageBox.information(self, "No inputs selected", "Select one or more input rows.")
            return set()
        errors: list[str] = []
        queued: set[UUID] = set()
        reserved = {
            _path_key(job.request.output_path)
            for job in self.queue.jobs
            if job.state in {JobState.QUEUED, JobState.RUNNING}
        }
        for draft in drafts:
            try:
                request = self._build_request(draft)
                if draft.output_override is None:
                    request = replace(
                        request,
                        output_path=self._unique_output_path(
                            request.output_path,
                            reserved,
                            avoid_existing=not self.overwrite.isChecked(),
                        ),
                    )
                job = self.queue.add(request, self.overwrite.isChecked())
                queued.add(job.id)
                reserved.add(_path_key(request.output_path))
            except (ValueError, AudioEncoderError) as exc:
                errors.append(f"{draft.path.name}: {exc}")
        if errors:
            QMessageBox.warning(self, "Some inputs were not queued", "\n".join(errors))
        self._refresh_queue_summary()
        self._refresh_actions()
        return queued

    @staticmethod
    def _unique_output_path(path: Path, reserved: set[str], *, avoid_existing: bool) -> Path:
        candidate = path
        counter = 2
        while _path_key(candidate) in reserved or (avoid_existing and candidate.exists()):
            candidate = path.with_name(f"{path.stem} ({counter}){path.suffix}")
            counter += 1
        return candidate

    def _queue_and_start_selected(self) -> None:
        queued = self._queue_selected()
        if self.queue is not None and queued:
            self.queue.start(queued)

    def _start_queue(self) -> None:
        if self.queue:
            self.queue.start()

    def _start_selected_jobs(self) -> None:
        if self.queue:
            selected = {
                job_id
                for job_id in self._selected_job_ids()
                if (job := self.queue.job(job_id)) is not None and job.state is JobState.QUEUED
            }
            if selected:
                self.queue.start(selected)

    def _stop_queue(self) -> None:
        if self.queue:
            self.queue.stop_after_current()
            self.statusBar().showMessage("The queue will stop after the active job.", 5000)
            self._refresh_actions()

    def _cancel_active(self) -> None:
        if self.queue:
            self.queue.cancel_active()

    def _cancel_all(self) -> None:
        if self.queue:
            self.queue.cancel_all()
            self._refresh_actions()

    def _selected_job_ids(self) -> set[UUID]:
        ids: set[UUID] = set()
        for index in self.queue_table.selectionModel().selectedRows():
            job = self.queue_model.job_at(index.row())
            if job:
                ids.add(job.id)
        return ids

    def _retry_selected(self) -> None:
        if self.queue:
            for job_id in self._selected_job_ids():
                self.queue.retry(job_id)
        self._refresh_actions()

    def _remove_selected_jobs(self) -> None:
        if not self.queue:
            return
        selected = self._selected_job_ids()
        if not selected:
            return
        if len(selected) > 1:
            answer = QMessageBox.question(
                self,
                "Remove jobs",
                f"Remove {len(selected)} selected jobs from the queue?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if answer is not QMessageBox.StandardButton.Yes:
                return
        self.queue.remove(selected)
        self._selected_job_changed()
        self._refresh_queue_summary()
        self._refresh_actions()

    def _clear_finished(self) -> None:
        if not self.queue:
            return
        count = sum(
            job.state in {JobState.SUCCEEDED, JobState.FAILED, JobState.CANCELLED}
            for job in self.queue.jobs
        )
        if not count:
            return
        answer = QMessageBox.question(
            self,
            "Clear finished jobs",
            f"Remove {count} finished jobs and their history?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if answer is QMessageBox.StandardButton.Yes:
            self.queue.clear_completed()
            self._selected_job_changed()
            self._refresh_queue_summary()
            self._refresh_actions()

    def _remove_inputs(self) -> None:
        rows = sorted({index.row() for index in self.input_table.selectedIndexes()}, reverse=True)
        for row in rows:
            self.input_table.removeRow(row)
            self.drafts.pop(row)
        self._sync_selected_draft()
        self._refresh_actions()

    def _append_log(self, job_id: str, text: str) -> None:
        self.log_output.appendPlainText(f"[{job_id[:8]}] {text.rstrip()}")
        self.job_logs[job_id] = (self.job_logs.get(job_id, "") + text)[-200_000:]
        selected = self._selected_job_ids()
        if any(str(job_id_value) == job_id for job_id_value in selected):
            self._selected_job_changed()

    def _selected_job_changed(self, *_args: object) -> None:
        if self.queue is None:
            self.job_details.clear()
            return
        selected = self._selected_job_ids()
        job = self.queue.job(next(iter(selected))) if len(selected) == 1 else None
        if job is None:
            self.job_details.clear()
            self._refresh_actions()
            return
        try:
            adapter = self.registry.get(job.request.encoder_id)
            plan = adapter.build_plan(
                job.request,
                self.queue.toolchain,
                temporary_output_path(job.request.output_path, job.id),
            )
            command = plan.display_command()
        except AudioEncoderError as exc:
            command = str(exc)
        log_text = self.job_logs.get(str(job.id), "")
        self.job_details.setPlainText(
            "\n".join(
                (
                    f"State: {job.state.value}",
                    f"Status: {job.status}",
                    f"Input: {job.request.input_path}",
                    f"Output: {job.request.output_path}",
                    f"Encoder: {job.request.encoder_id}",
                    f"Created: {job.created_at.isoformat()}",
                    f"Started: {job.started_at.isoformat() if job.started_at else '-'}",
                    f"Finished: {job.finished_at.isoformat() if job.finished_at else '-'}",
                    f"Error: {job.error or '-'}",
                    f"Command: {command}",
                    "",
                    "Log:",
                    log_text.rstrip() or "(No session log for this job)",
                )
            )
        )
        self._refresh_actions()

    def _queue_context_menu(self, position: QPoint) -> None:
        index = self.queue_table.indexAt(position)
        if index.isValid() and not self.queue_table.selectionModel().isRowSelected(
            index.row(), index.parent()
        ):
            self.queue_table.selectRow(index.row())
        menu = QMenu(self)
        menu.addAction("Start selected", self._start_selected_jobs)
        menu.addAction("Retry selected", self._retry_selected)
        menu.addSeparator()
        menu.addAction("Open output folder", self._open_selected_output_folder)
        menu.addAction("Copy command", self._copy_selected_command)
        menu.addAction("Copy error", self._copy_selected_error)
        menu.addSeparator()
        menu.addAction("Remove selected", self._remove_selected_jobs)
        menu.exec(self.queue_table.viewport().mapToGlobal(position))

    def _selected_job(self):
        if self.queue is None:
            return None
        selected = self._selected_job_ids()
        return self.queue.job(next(iter(selected))) if len(selected) == 1 else None

    def _open_selected_output_folder(self) -> None:
        job = self._selected_job()
        if job is not None:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(job.request.output_path.parent)))

    def _copy_selected_command(self) -> None:
        job = self._selected_job()
        if job is None or self.queue is None:
            return
        try:
            command = (
                self.registry.get(job.request.encoder_id)
                .build_plan(
                    job.request,
                    self.queue.toolchain,
                    temporary_output_path(job.request.output_path, job.id),
                )
                .display_command()
            )
        except AudioEncoderError as exc:
            command = str(exc)
        QApplication.clipboard().setText(command)

    def _copy_selected_error(self) -> None:
        job = self._selected_job()
        if job is not None:
            QApplication.clipboard().setText(job.error or job.status)

    def _refresh_queue_summary(self, *_args: object) -> None:
        jobs = self.queue.jobs if self.queue else []
        if not jobs:
            self.queue_summary.setText("No jobs")
            return
        counts = {state: sum(job.state is state for job in jobs) for state in JobState}
        terminal = {JobState.SUCCEEDED, JobState.FAILED, JobState.CANCELLED}
        completed = sum(1.0 if job.state in terminal else (job.progress or 0.0) for job in jobs)
        self.queue_summary.setText(
            f"{len(jobs)} jobs - {counts[JobState.QUEUED]} queued, "
            f"{counts[JobState.RUNNING]} running, {counts[JobState.SUCCEEDED]} complete, "
            f"{counts[JobState.FAILED]} failed - overall {completed / len(jobs):.0%}"
        )

    def _refresh_actions(self, *_args: object) -> None:
        queue = self.queue
        selected_jobs = [queue.job(job_id) for job_id in self._selected_job_ids()] if queue else []
        selected_jobs = [job for job in selected_jobs if job is not None]
        has_queued = bool(queue and any(job.state is JobState.QUEUED for job in queue.jobs))
        has_active = bool(queue and queue.active_job)
        selected_queued = any(job.state is JobState.QUEUED for job in selected_jobs)
        selected_terminal = any(
            job.state in {JobState.SUCCEEDED, JobState.FAILED, JobState.CANCELLED}
            for job in selected_jobs
        )
        removable = any(job.state is not JobState.RUNNING for job in selected_jobs)
        terminal_jobs = bool(
            queue
            and any(
                job.state in {JobState.SUCCEEDED, JobState.FAILED, JobState.CANCELLED}
                for job in queue.jobs
            )
        )
        ready_inputs = any(draft.asset is not None for draft in self._selected_drafts())
        self.queue_selected_button.setEnabled(bool(queue) and ready_inputs)
        self.queue_start_button.setEnabled(bool(queue) and ready_inputs and not has_active)
        self.start_button.setEnabled(has_queued and not has_active)
        self.start_selected_button.setEnabled(selected_queued and not has_active)
        self.stop_button.setEnabled(bool(queue and queue.is_dispatching and has_active))
        self.cancel_button.setEnabled(has_active)
        self.cancel_all_button.setEnabled(has_active or has_queued)
        self.retry_button.setEnabled(selected_terminal and not has_active)
        self.remove_jobs_button.setEnabled(removable)
        self.clear_button.setEnabled(terminal_jobs)
        self.remove_inputs_button.setEnabled(bool(self._selected_drafts()))
        self.stream_details_button.setEnabled(
            (draft := self._current_draft()) is not None and draft.asset is not None
        )
        self.browse_output_button.setEnabled(draft is not None and draft.asset is not None)

    def _populate_presets(self) -> None:
        self.preset_combo.blockSignals(True)
        self.preset_combo.clear()
        self.preset_combo.addItem("Custom", None)
        for preset in self.presets:
            self.preset_combo.addItem(preset.name, preset.name)
        self.preset_combo.blockSignals(False)

    def _save_preset(self) -> None:
        adapter = self._current_adapter()
        try:
            codec = Codec(str(self.codec_combo.currentData()))
            output_format = OutputFormat(str(self.format_combo.currentData()))
        except ValueError:
            return
        if adapter is None:
            return
        name, accepted = QInputDialog.getText(self, "Save preset", "Preset name")
        name = name.strip()
        if not accepted or not name:
            return
        preset = EncoderPreset(
            name,
            adapter.descriptor.id,
            codec,
            output_format,
            CommonAudioOptions(
                self._sample_rate_value(),
                self.channels.currentData(),
                self.gain_db.value(),
                self.tempo_ratio.value(),
            ),
            self._current_options(),
        )
        self.presets = [
            existing for existing in self.presets if existing.name.casefold() != name.casefold()
        ]
        self.presets.append(preset)
        try:
            self.preset_repository.save(self.presets)
        except OSError as exc:
            QMessageBox.critical(self, "Could not save preset", str(exc))
            return
        self.presets = self.preset_repository.load()
        self._populate_presets()
        self.preset_combo.setCurrentIndex(self.preset_combo.findData(name))

    def _apply_preset(self, *_args: object) -> None:
        name = self.preset_combo.currentData()
        preset = next((item for item in self.presets if item.name == name), None)
        if preset is None:
            return
        if not self._apply_configuration(preset):
            QMessageBox.warning(self, "Preset unavailable", "The preset's encoder is unavailable.")

    def _restore_last_configuration(self) -> None:
        configuration = self.settings.last_configuration
        if configuration is not None and not self._apply_configuration(configuration):
            self.statusBar().showMessage(
                "The last-used encoder is unavailable; using safe defaults.",
                12000,
            )

    def _apply_configuration(self, configuration: EncoderPreset | EncoderConfiguration) -> bool:
        adapter_index = self.encoder_combo.findData(configuration.encoder_id)
        if adapter_index < 0 or not self._adapter_available(configuration.encoder_id):
            return False
        self._restoring_configuration = True
        self.encoder_combo.setCurrentIndex(adapter_index)
        codec_index = self.codec_combo.findData(configuration.codec.value)
        if codec_index >= 0:
            self.codec_combo.setCurrentIndex(codec_index)
        format_index = self.format_combo.findData(configuration.output_format.value)
        if format_index >= 0:
            self.format_combo.setCurrentIndex(format_index)
        restored_all = self._set_sample_rate(configuration.common.sample_rate)
        layout_index = self.channels.findData(configuration.common.channel_layout)
        self.channels.setCurrentIndex(max(layout_index, 0))
        self.gain_db.setValue(configuration.common.gain_db)
        self.tempo_ratio.setValue(configuration.common.tempo_ratio)
        for key, value in configuration.encoder_options.items():
            widget = self.option_widgets.get(key)
            if (
                isinstance(widget, QSpinBox)
                and isinstance(value, int)
                and not isinstance(value, bool)
            ):
                widget.setValue(value)
            elif (
                isinstance(widget, QDoubleSpinBox)
                and isinstance(value, (int, float))
                and not isinstance(value, bool)
            ):
                widget.setValue(float(value))
            elif isinstance(widget, QComboBox):
                option_index = widget.findData(value)
                if option_index >= 0:
                    widget.setCurrentIndex(option_index)
            elif isinstance(widget, QLineEdit) and isinstance(value, str):
                widget.setText(value)
        self._restoring_configuration = False
        self._refresh_option_states()
        self._refresh_preview()
        self._schedule_configuration_save()
        if not restored_all:
            self.statusBar().showMessage(
                "A saved sample rate is unsupported; preserving the input rate.",
                12000,
            )
        return True

    def _current_configuration(self) -> EncoderConfiguration | None:
        adapter = self._current_adapter()
        if adapter is None:
            return None
        try:
            codec = Codec(str(self.codec_combo.currentData()))
            output_format = OutputFormat(str(self.format_combo.currentData()))
            sample_rate = self._sample_rate_value()
        except ValueError:
            return None
        return EncoderConfiguration(
            adapter.descriptor.id,
            codec,
            output_format,
            CommonAudioOptions(
                sample_rate,
                self.channels.currentData(),
                self.gain_db.value(),
                self.tempo_ratio.value(),
            ),
            self._current_options(),
        )

    def _schedule_configuration_save(self) -> None:
        if not self._restoring_configuration:
            self._configuration_save_timer.start()

    def _persist_last_configuration(self) -> None:
        configuration = self._current_configuration()
        if configuration is None:
            return
        self.settings = replace(self.settings, last_configuration=configuration)
        try:
            self.settings_repository.save(self.settings)
        except OSError as exc:
            self.statusBar().showMessage(f"Could not save settings: {exc}", 12000)

    def _delete_preset(self) -> None:
        name = self.preset_combo.currentData()
        if not isinstance(name, str):
            return
        self.presets = [preset for preset in self.presets if preset.name != name]
        try:
            self.preset_repository.save(self.presets)
        except OSError as exc:
            QMessageBox.critical(self, "Could not delete preset", str(exc))
            return
        self._populate_presets()

    def _open_settings(self) -> None:
        if self.queue and self.queue.active_job:
            QMessageBox.information(
                self, "Encoding in progress", "Wait for or cancel the active job first."
            )
            return
        dialog = SettingsDialog(self.settings, self)
        if not dialog.exec():
            return
        candidate = dialog.settings()
        self._start_tool_inspection(candidate, save_on_success=True, show_errors=True)

    def discover_tools(self) -> None:
        if self.tool_report is None:
            self._start_tool_inspection(
                self.settings,
                save_on_success=False,
                show_errors=False,
            )

    def _start_tool_inspection(
        self,
        candidate,
        *,
        save_on_success: bool,
        show_errors: bool,
    ) -> None:
        if self._tool_thread is not None:
            return
        self._pending_settings = (candidate, save_on_success, show_errors)
        thread = ToolInspectionThread(candidate, self)
        self._tool_thread = thread
        thread.succeeded.connect(self._tool_inspection_succeeded)
        thread.failed.connect(self._tool_inspection_failed)
        thread.finished.connect(self._tool_inspection_finished)
        self.settings_button.setEnabled(False)
        self.statusBar().showMessage("Checking encoder tools...")
        thread.start()

    def _tool_inspection_succeeded(self, raw_report: object) -> None:
        if self._closing or not isinstance(raw_report, ToolReport):
            return
        pending = self._pending_settings
        if pending is None:
            return
        candidate, save_on_success, _show_errors = pending
        if save_on_success:
            self.settings = candidate
            try:
                self.settings_repository.save(candidate)
            except OSError as exc:
                QMessageBox.critical(self, "Could not save settings", str(exc))
                return
            self.theme_manager.apply(candidate.theme)
        self._configure_services(raw_report)
        self._populate_encoders()
        self._restore_last_configuration()

    def _tool_inspection_failed(self, message: str) -> None:
        pending = self._pending_settings
        show_errors = bool(pending and pending[2])
        if show_errors and not self._closing:
            QMessageBox.critical(self, "Invalid tool configuration", message)
        else:
            self.statusBar().showMessage(f"Tools unavailable: {message}")

    def _tool_inspection_finished(self) -> None:
        thread = self._tool_thread
        self._tool_thread = None
        self._pending_settings = None
        if thread is not None:
            thread.deleteLater()
        self.settings_button.setEnabled(not bool(self.queue and self.queue.active_job))
        self._refresh_actions()
        if self._closing and not (self.queue and self.queue.active_job):
            QTimer.singleShot(0, self.close)

    def _active_changed(self, active: bool) -> None:
        self.settings_button.setEnabled(not active)
        self._refresh_actions()
        if self._closing and not active:
            QTimer.singleShot(0, self.close)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        self._add_paths(
            Path(url.toLocalFile()) for url in event.mimeData().urls() if url.isLocalFile()
        )
        event.acceptProposedAction()

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.queue and self.queue.active_job and not self._closing:
            answer = QMessageBox.question(
                self,
                "Encoding in progress",
                "Cancel the active encode and exit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if answer is QMessageBox.StandardButton.No:
                event.ignore()
                return
            self._closing = True
            self.queue.shutdown()
            if self.probe_service is not None:
                self.probe_service.cancel_all()
            event.ignore()
            return
        if self.queue and self.queue.active_job:
            event.ignore()
            return
        if self._tool_thread is not None and self._tool_thread.isRunning():
            self._closing = True
            event.ignore()
            return
        if self.probe_service is not None:
            self.probe_service.cancel_all()
        configuration = self._current_configuration()
        if configuration is not None:
            self.settings = replace(self.settings, last_configuration=configuration)
        geometry = self.geometry()
        draft_sizes = self.draft_splitter.sizes()
        main_sizes = self.main_splitter.sizes()
        if main_sizes[1] == 0:
            main_sizes[1] = self._expanded_queue_height
        self.settings = replace(
            self.settings,
            window_x=geometry.x(),
            window_y=geometry.y(),
            window_width=geometry.width(),
            window_height=geometry.height(),
            draft_splitter_sizes=(draft_sizes[0], draft_sizes[1]),
            main_splitter_sizes=(main_sizes[0], main_sizes[1]),
            queue_panel_collapsed=not self.toggle_queue_button.isChecked(),
        )
        try:
            self.settings_repository.save(self.settings)
        except OSError as exc:
            QMessageBox.warning(self, "Could not save settings", str(exc))
        event.accept()


def _path_key(path: Path) -> str:
    return os.path.normcase(os.path.abspath(os.fspath(path)))
