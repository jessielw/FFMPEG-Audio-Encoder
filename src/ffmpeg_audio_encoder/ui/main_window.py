from __future__ import annotations

import math
import os
from dataclasses import dataclass, field, replace
from pathlib import Path
from uuid import UUID

from PySide6.QtCore import QPoint, QRect, QSize, Qt, QThread, QTimer, QUrl, Signal
from PySide6.QtGui import (
    QAction,
    QCloseEvent,
    QDesktopServices,
    QDragEnterEvent,
    QDropEvent,
    QGuiApplication,
    QIntValidator,
    QKeySequence,
    QShowEvent,
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
    QToolBar,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from ffmpeg_audio_encoder import __version__
from ffmpeg_audio_encoder.application.queue import JobQueueController
from ffmpeg_audio_encoder.domain.errors import AudioEncoderError, ValidationError
from ffmpeg_audio_encoder.domain.models import (
    Codec,
    CommonAudioOptions,
    DelaySource,
    DetectedDelay,
    EncoderConfiguration,
    EncoderGroup,
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
from ffmpeg_audio_encoder.encoders.base import DynamicOptionChoiceProvider, EncoderAdapter
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

_FOLDER_PROMPT_THRESHOLD = 100


@dataclass(slots=True)
class InputDraft:
    path: Path
    status: str = "Probing…"
    asset: MediaAsset | None = None
    stream_position: int = 0
    output_override: Path | None = None
    error: str | None = None
    delay_overrides_ms: dict[int, float] = field(default_factory=dict)


OptionWidget = QSpinBox | QDoubleSpinBox | QComboBox | QLineEdit | QCheckBox


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
        self._refreshing_dynamic_choices = False
        self._closing = False
        self._expanded_queue_height = 250
        self._restore_maximized = self.settings.window_maximized
        self._job_command_cache: dict[str, str] = {}
        self._details_job_id: str | None = None
        self._tool_thread: ToolInspectionThread | None = None
        self._pending_settings = None
        self._configuration_save_timer = QTimer(self)
        self._configuration_save_timer.setSingleShot(True)
        self._configuration_save_timer.setInterval(350)
        self._configuration_save_timer.timeout.connect(self._persist_last_configuration)

        self.setWindowTitle(f"FFmpeg Audio Encoder v{__version__}")
        self.setAcceptDrops(True)
        self.setMinimumSize(480, 360)
        self._restore_window_geometry()
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

    def _restore_window_geometry(self) -> None:
        """Reapply the saved client-area rect.

        ``setGeometry`` is deliberate: it consumes the same client rect that
        ``geometry``/``normalGeometry`` report at save time, so the window lands exactly
        where it was left. ``move`` would position the frame instead and walk the window
        down the screen by one title bar per launch.
        """
        width = max(self.settings.window_width, self.minimumWidth())
        height = max(self.settings.window_height, self.minimumHeight())
        if self.settings.window_x is None or self.settings.window_y is None:
            self.resize(width, height)
            return
        rect = QRect(self.settings.window_x, self.settings.window_y, width, height)
        self.setGeometry(_visible_rect(rect))

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
        self.input_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
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
        self.stream_details_button = QToolButton()
        self.stream_details_button.setAutoRaise(True)
        self.stream_details_button.setToolTip("Inspect the selected audio stream")
        self.stream_details_button.setAccessibleName("Inspect selected stream")
        # Square, combo-height: the eye reads as part of the stream row, not a field.
        stream_button_extent = self.stream_combo.sizeHint().height()
        self.stream_details_button.setFixedSize(stream_button_extent, stream_button_extent)
        stream_row = QWidget()
        stream_row_layout = QHBoxLayout(stream_row)
        stream_row_layout.setContentsMargins(0, 0, 0, 0)
        stream_row_layout.setSpacing(4)
        stream_row_layout.addWidget(self.stream_combo, 1)
        stream_row_layout.addWidget(self.stream_details_button)
        config_form.addRow("Audio stream", stream_row)
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
        queue_heading = QLabel("Encoding queue")
        heading_font = queue_heading.font()
        heading_font.setBold(True)
        queue_heading.setFont(heading_font)
        queue_heading.setContentsMargins(2, 0, 10, 0)

        # A toolbar rather than two ragged rows of push buttons: one flat strip that
        # separates queueing from running, halting and housekeeping, and that folds
        # into an overflow menu instead of wrapping when the window narrows.
        self.queue_toolbar = QToolBar()
        self.queue_toolbar.setMovable(False)
        self.queue_toolbar.setFloatable(False)
        self.queue_toolbar.setIconSize(QSize(16, 16))
        self.queue_toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.queue_toolbar.addWidget(queue_heading)
        self.queue_selected_action = self._add_queue_action(
            "Queue selected inputs",
            "ph.list-plus-light",
            "Add the selected inputs to the queue without starting them",
        )
        self.queue_start_action = self._add_queue_action(
            "Queue and start",
            "ph.rocket-launch-light",
            "Queue the selected inputs and begin encoding immediately",
        )
        self.queue_toolbar.addSeparator()
        self.start_action = self._add_queue_action(
            "Start queue", "ph.play-light", "Run every queued job in order"
        )
        self.start_selected_action = self._add_queue_action(
            "Start selected", "ph.play-circle-light", "Run only the selected queued jobs"
        )
        self.queue_toolbar.addSeparator()
        self.stop_action = self._add_queue_action(
            "Stop after current",
            "ph.pause-light",
            "Finish the running job, then hold the rest of the queue",
        )
        self.cancel_action = self._add_queue_action(
            "Cancel active", "ph.stop-circle-light", "Abort the job that is running now"
        )
        self.cancel_all_action = self._add_queue_action(
            "Cancel all", "ph.x-circle-light", "Abort the running job and drop everything queued"
        )
        self.queue_toolbar.addSeparator()
        self.retry_action = self._add_queue_action(
            "Retry selected",
            "ph.arrow-counter-clockwise-light",
            "Requeue the selected finished, failed or cancelled jobs",
        )
        self.remove_jobs_action = self._add_queue_action(
            "Remove selected", "ph.minus-circle-light", "Drop the selected jobs from the queue"
        )
        self.clear_action = self._add_queue_action(
            "Clear finished",
            "ph.eraser-light",
            "Remove every succeeded, failed and cancelled job",
        )
        queue_layout.addWidget(self.queue_toolbar)
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
        self.queue_table.setMinimumHeight(120)
        queue_layout.addWidget(self.queue_table, 3)
        self.queue_summary = QLabel("No jobs")
        queue_layout.addWidget(self.queue_summary)
        self.job_details = QPlainTextEdit()
        self.job_details.setReadOnly(True)
        self.job_details.setMinimumHeight(90)
        self.job_details.setPlaceholderText("Select a job to see its details")
        self.log_output = QPlainTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMaximumBlockCount(3000)
        self.log_output.setMinimumHeight(90)
        self.queue_details_tabs = QTabWidget()
        self.queue_details_tabs.addTab(self.job_details, "Selected job")
        self.queue_details_tabs.addTab(self.log_output, "Session log")
        # Stretch rather than a fixed cap, so dragging the splitter grows the text
        # areas instead of only the tab frame around them.
        queue_layout.addWidget(self.queue_details_tabs, 2)
        queue_panel.setMinimumHeight(0)

        self.main_splitter = CustomSplitter(Qt.Orientation.Vertical)
        self.main_splitter.addWidget(self.draft_splitter)
        self.main_splitter.addWidget(queue_panel)
        self.main_splitter.setChildrenCollapsible(True)
        self.main_splitter.setCollapsible(0, True)
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
        self.theme_manager.register(self.stream_details_button, "ph.eye-light", 16)

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
        self.queue_selected_action.triggered.connect(self._queue_selected)
        self.queue_start_action.triggered.connect(self._queue_and_start_selected)
        self.start_action.triggered.connect(self._start_queue)
        self.start_selected_action.triggered.connect(self._start_selected_jobs)
        self.stop_action.triggered.connect(self._stop_queue)
        self.cancel_action.triggered.connect(self._cancel_active)
        self.cancel_all_action.triggered.connect(self._cancel_all)
        self.retry_action.triggered.connect(self._retry_selected)
        self.remove_jobs_action.triggered.connect(self._remove_selected_jobs)
        self.clear_action.triggered.connect(self._clear_finished)
        self.save_preset_button.clicked.connect(self._save_preset)
        self.delete_preset_button.clicked.connect(self._delete_preset)
        self.preset_combo.currentIndexChanged.connect(self._apply_preset)
        self.queue_table.selectionModel().selectionChanged.connect(self._selected_job_changed)
        self.queue_table.customContextMenuRequested.connect(self._queue_context_menu)
        self.input_table.customContextMenuRequested.connect(self._input_context_menu)
        self.input_table.itemSelectionChanged.connect(self._refresh_actions)
        self.input_table.itemDoubleClicked.connect(self._show_stream_details)
        self.queue_table.doubleClicked.connect(self._open_selected_output_folder)
        self._install_delete_shortcut(self.input_table, self._remove_inputs)
        self._install_delete_shortcut(self.queue_table, self._remove_selected_jobs)

        self._build_menus()

        QTimer.singleShot(0, self._restore_splitters)

    def _add_queue_action(self, text: str, icon_name: str, tooltip: str) -> QAction:
        action = QAction(text, self)
        action.setToolTip(tooltip)
        self.queue_toolbar.addAction(action)
        self.theme_manager.register(action, icon_name)
        return action

    @staticmethod
    def _install_delete_shortcut(widget: QWidget, slot) -> None:
        action = QAction("Remove selected", widget)
        action.setShortcut(QKeySequence.StandardKey.Delete)
        action.setShortcutContext(Qt.ShortcutContext.WidgetShortcut)
        action.triggered.connect(slot)
        widget.addAction(action)

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

        view_menu = self.menuBar().addMenu("&View")
        self.queue_panel_action = QAction("&Queue panel", self)
        self.queue_panel_action.setCheckable(True)
        self.queue_panel_action.setChecked(self.toggle_queue_button.isChecked())
        # Not Ctrl+Q: that is StandardKey.Quit on Linux.
        self.queue_panel_action.setShortcut(QKeySequence("F9"))
        self.queue_panel_action.toggled.connect(self._set_queue_visible)
        view_menu.addAction(self.queue_panel_action)

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
        lines = [f"FFmpeg Audio Encoder v{__version__}"]
        if report is None:
            lines.append("Toolchain: unavailable")
        else:
            lines.extend(
                (
                    f"FFmpeg: {report.ffmpeg_version}",
                    f"ffprobe: {report.ffprobe_version}",
                    f"qaac: {report.qaac_version or 'unavailable'}",
                    f"fdkaac: {report.fdkaac_version or 'unavailable'}",
                    f"opusenc: {report.opusenc_version or 'unavailable'}",
                    f"DeeZy: {report.deezy_version or 'unavailable'}",
                    f"DEE: {report.dee_version or 'unavailable'}",
                    f"TrueHDD: {report.truehdd_version or 'unavailable'}",
                )
            )
        QApplication.clipboard().setText("\n".join(lines))
        self.statusBar().showMessage("Diagnostics copied to the clipboard", 5000)

    def _show_about(self) -> None:
        QMessageBox.about(
            self,
            "About FFmpeg Audio Encoder",
            f"FFmpeg Audio Encoder v{__version__}\n\nA cross-platform PySide6 front end for "
            "FFmpeg, DeeZy, opusenc, qaac, and fdkaac.\n\nLicensed under the MIT License.",
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
        action = getattr(self, "queue_panel_action", None)
        if action is not None:
            action.blockSignals(True)
            action.setChecked(visible)
            action.blockSignals(False)

    def _configure_services(self, report: ToolReport | None) -> None:
        if self.probe_service is not None:
            self.probe_service.cancel_all()
            self.probe_service.deleteLater()
        if self.queue is not None:
            self.queue.shutdown()
            # deleteLater destroys the runner's QProcess objects on the next event
            # loop turn, which is far sooner than an async cancel can finish. Take
            # the process trees down synchronously first so nothing is orphaned.
            self.queue.terminate_processes()
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
        if self.queue is not None and self._job_command_cache:
            live = {str(job.id) for job in self.queue.jobs}
            self._job_command_cache = {
                key: value for key, value in self._job_command_cache.items() if key in live
            }
        self._refresh_queue_summary()
        self._selected_job_changed()
        self._refresh_actions()

    def _populate_encoders(self) -> None:
        current_id = self.encoder_combo.currentData()
        self.encoder_combo.blockSignals(True)
        self.encoder_combo.clear()
        previous_group: EncoderGroup | None = None
        for adapter in self.registry:
            descriptor = adapter.descriptor
            if previous_group is not None and descriptor.group is not previous_group:
                self.encoder_combo.insertSeparator(self.encoder_combo.count())
            previous_group = descriptor.group
            available = self._adapter_available(descriptor.id)
            label = (
                descriptor.display_name if available else f"{descriptor.display_name} (unavailable)"
            )
            self.encoder_combo.addItem(label, descriptor.id)
            model = self.encoder_combo.model()
            if isinstance(model, QStandardItemModel):
                model.item(self.encoder_combo.count() - 1).setEnabled(available)
        # ``findData(None)`` would land on a separator row, so only search for real ids.
        index = self.encoder_combo.findData(current_id) if isinstance(current_id, str) else -1
        if index < 0:
            index = next(
                (
                    i
                    for i in range(self.encoder_combo.count())
                    if self._adapter_available(self.encoder_combo.itemData(i))
                ),
                0,
            )
        self.encoder_combo.setCurrentIndex(index)
        self.encoder_combo.blockSignals(False)
        self._encoder_changed()

    def _adapter_available(self, adapter_id: object) -> bool:
        """Separator rows carry no adapter id, so anything unknown counts as unavailable."""
        if self.tool_report is None or not isinstance(adapter_id, str):
            return False
        try:
            adapter = self.registry.get(adapter_id)
        except ValidationError:
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
        if adapter is None:
            self.channels.addItem("Preserve", None)
            return
        self.channels.addItem(adapter.descriptor.default_channel_layout_label, None)
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
        self._apply_common_control_capabilities(adapter)
        self._refresh_preview()
        self._schedule_configuration_save()

    def _apply_common_control_capabilities(self, adapter: EncoderAdapter) -> None:
        descriptor = adapter.descriptor
        if not descriptor.supports_sample_rate:
            self.sample_rate.setCurrentIndex(0)
        if not descriptor.supports_channel_layout:
            self.channels.setCurrentIndex(0)
        if not descriptor.supports_gain:
            self.gain_db.setValue(0.0)
        if not descriptor.supports_tempo:
            self.tempo_ratio.setValue(1.0)
        self.sample_rate.setEnabled(descriptor.supports_sample_rate)
        self.channels.setEnabled(descriptor.supports_channel_layout)
        self.gain_db.setEnabled(descriptor.supports_gain)
        self.tempo_ratio.setEnabled(descriptor.supports_tempo)
        self._sync_delay_control()

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
            elif definition.kind is OptionKind.BOOLEAN:
                if not isinstance(definition.default, bool):
                    raise TypeError(f"Boolean option {definition.key} has a non-boolean default")
                widget = QCheckBox()
                widget.setChecked(definition.default)
                widget.toggled.connect(self._option_values_changed)
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
        self._refresh_dynamic_option_choices()
        self._refresh_option_states()

    def _widget_value(self, widget: OptionWidget) -> JsonScalar:
        if isinstance(widget, QCheckBox):
            return widget.isChecked()
        if isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            return widget.value()
        if isinstance(widget, QComboBox):
            return widget.currentData()
        return widget.text()

    def _option_values_changed(self, *_args: object) -> None:
        self._refresh_dynamic_option_choices()
        self._refresh_option_states()
        self._refresh_preview()
        self._schedule_configuration_save()

    def _common_options_changed(self, *_args: object) -> None:
        self._refresh_dynamic_option_choices()
        self._refresh_preview()
        self._schedule_configuration_save()

    def _refresh_dynamic_option_choices(self) -> None:
        if self._refreshing_dynamic_choices:
            return
        adapter = self._current_adapter()
        if adapter is None or not isinstance(adapter, DynamicOptionChoiceProvider):
            return
        draft = self._current_draft()
        stream = (
            draft.asset.audio_streams[draft.stream_position]
            if draft is not None and draft.asset is not None
            else None
        )
        encoder_options = adapter.default_options()
        encoder_options.update(self._current_options())
        self._refreshing_dynamic_choices = True
        try:
            for definition in adapter.descriptor.options:
                widget = self.option_widgets.get(definition.key)
                if definition.kind is not OptionKind.CHOICE or not isinstance(widget, QComboBox):
                    continue
                choices = adapter.option_choices(
                    definition.key,
                    stream,
                    self.channels.currentData(),
                    encoder_options,
                )
                existing = tuple(
                    (widget.itemText(index), widget.itemData(index))
                    for index in range(widget.count())
                )
                desired = tuple((choice.label, choice.value) for choice in choices)
                if existing == desired:
                    continue
                current = widget.currentData()
                widget.blockSignals(True)
                widget.clear()
                for choice in choices:
                    widget.addItem(choice.label, choice.value)
                selected = widget.findData(current)
                if selected < 0:
                    selected = widget.findData(definition.default)
                widget.setCurrentIndex(max(selected, 0))
                widget.blockSignals(False)
        finally:
            self._refreshing_dynamic_choices = False

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
            for controlling_key, allowed_values in definition.enabled_when_all:
                controlling = self.option_widgets.get(controlling_key)
                enabled = (
                    enabled
                    and controlling is not None
                    and self._widget_value(controlling) in allowed_values
                )
            widget.setEnabled(enabled)

    def _choose_files(self) -> None:
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Choose media files", self.settings.last_input_dir or "", "All files (*)"
        )
        if not paths:
            return
        self.settings = replace(self.settings, last_input_dir=str(Path(paths[0]).parent))
        self._add_paths(Path(path) for path in paths)

    def _expand_inputs(self, paths) -> list[Path] | None:
        """Flatten directories into their files. Returns None if the user backs out."""
        expanded: list[Path] = []
        for raw_path in paths:
            path = raw_path.expanduser()
            if path.is_dir():
                found = sorted(child for child in path.rglob("*") if child.is_file())
                if len(found) > _FOLDER_PROMPT_THRESHOLD:
                    answer = QMessageBox.question(
                        self,
                        "Add folder",
                        f"{path.name} contains {len(found)} files. Add all of them?",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    )
                    if answer is not QMessageBox.StandardButton.Yes:
                        return None
                expanded.extend(found)
            else:
                expanded.append(path)
        return expanded

    def _add_paths(self, paths) -> None:
        if self.probe_service is None:
            QMessageBox.warning(self, "Tools not configured", "Configure FFmpeg and ffprobe first.")
            return
        candidates = self._expand_inputs(paths)
        if candidates is None:
            return
        existing = {draft.path for draft in self.drafts}
        added = 0
        duplicates = 0
        skipped = 0
        for candidate in candidates:
            path = candidate.resolve()
            if not path.is_file():
                skipped += 1
                continue
            if path in existing:
                duplicates += 1
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
            added += 1
        if self.input_table.rowCount() and self.input_table.currentRow() < 0:
            self.input_table.selectRow(0)
        self._report_added_inputs(added, duplicates, skipped)

    def _report_added_inputs(self, added: int, duplicates: int, skipped: int) -> None:
        if not (added or duplicates or skipped):
            return
        parts = [f"Added {added} input{'' if added == 1 else 's'}"]
        if duplicates:
            parts.append(f"{duplicates} already listed")
        if skipped:
            parts.append(f"{skipped} not readable")
        self.statusBar().showMessage(" - ".join(parts), 8000)

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
        self._refresh_dynamic_option_choices()
        self._refresh_preview()
        self._refresh_actions()

    def _stream_changed(self, position: int) -> None:
        draft = self._current_draft()
        if draft and draft.asset and 0 <= position < len(draft.asset.audio_streams):
            draft.stream_position = position
            draft.output_override = None
        self._sync_delay_control()
        self._refresh_dynamic_option_choices()
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
            adapter = self._current_adapter()
            supports_delay = adapter is not None and adapter.descriptor.supports_delay
            self.delay_ms.setEnabled(supports_delay)
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

    def _show_stream_details(self, *_args: object) -> None:
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
        had_log = bool(self.job_logs.get(job_id))
        self.job_logs[job_id] = (self.job_logs.get(job_id, "") + text)[-200_000:]
        if job_id != self._details_job_id:
            return
        if had_log:
            # Append rather than re-render: rebuilding per line would re-run build_plan
            # and snap the scrollbar back on every line of a long encode.
            self._append_details_line(text.rstrip())
        else:
            self._selected_job_changed()

    def _append_details_line(self, line: str) -> None:
        scrollbar = self.job_details.verticalScrollBar()
        previous = scrollbar.value()
        following = previous >= scrollbar.maximum()
        self.job_details.appendPlainText(line)
        scrollbar.setValue(scrollbar.maximum() if following else previous)

    def _job_command(self, job) -> str:
        """Render, and memoise, a job's display command.

        EncodingRequest is frozen and retry reuses the same request, so a job's command
        never changes once it has been queued.
        """
        key = str(job.id)
        cached = self._job_command_cache.get(key)
        if cached is not None:
            return cached
        if self.queue is None:
            return ""
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
        self._job_command_cache[key] = command
        return command

    def _selected_job_changed(self, *_args: object) -> None:
        if self.queue is None:
            self.job_details.clear()
            self._details_job_id = None
            return
        selected = self._selected_job_ids()
        job = self.queue.job(next(iter(selected))) if len(selected) == 1 else None
        if job is None:
            self.job_details.clear()
            self._details_job_id = None
            self._refresh_actions()
            return
        job_id = str(job.id)
        log_text = self.job_logs.get(job_id, "")
        details = "\n".join(
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
                f"Command: {self._job_command(job)}",
                "",
                "Log:",
                log_text.rstrip() or "(No session log for this job)",
            )
        )
        if details != self.job_details.toPlainText():
            scrollbar = self.job_details.verticalScrollBar()
            same_job = job_id == self._details_job_id
            previous = scrollbar.value()
            following = previous >= scrollbar.maximum()
            self.job_details.setPlainText(details)
            if same_job:
                scrollbar.setValue(scrollbar.maximum() if following else previous)
        self._details_job_id = job_id
        self._refresh_actions()

    def _build_input_menu(self) -> QMenu:
        menu = QMenu(self)
        draft = self._current_draft()
        selected = self._selected_drafts()
        menu.addAction("Add files…", self._choose_files)
        remove_action = menu.addAction("Remove selected", self._remove_inputs)
        remove_action.setEnabled(bool(selected))
        menu.addSeparator()
        inspect_action = menu.addAction("Inspect stream", self._show_stream_details)
        inspect_action.setEnabled(draft is not None and draft.asset is not None)
        folder_action = menu.addAction("Open containing folder", self._open_selected_input_folder)
        folder_action.setEnabled(draft is not None)
        copy_action = menu.addAction("Copy full path", self._copy_selected_input_paths)
        copy_action.setEnabled(bool(selected))
        menu.addSeparator()
        clear_action = menu.addAction("Clear all inputs", self._clear_inputs)
        clear_action.setEnabled(bool(self.drafts))
        return menu

    def _input_context_menu(self, position: QPoint) -> None:
        index = self.input_table.indexAt(position)
        if index.isValid() and not self.input_table.selectionModel().isRowSelected(
            index.row(), index.parent()
        ):
            self.input_table.selectRow(index.row())
        self._build_input_menu().exec(self.input_table.viewport().mapToGlobal(position))

    def _open_selected_input_folder(self) -> None:
        draft = self._current_draft()
        if draft is not None:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(draft.path.parent)))

    def _copy_selected_input_paths(self) -> None:
        drafts = self._selected_drafts()
        if drafts:
            QApplication.clipboard().setText("\n".join(str(draft.path) for draft in drafts))

    def _clear_inputs(self) -> None:
        if not self.drafts:
            return
        if len(self.drafts) > 1:
            answer = QMessageBox.question(
                self,
                "Clear inputs",
                f"Remove all {len(self.drafts)} inputs?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if answer is not QMessageBox.StandardButton.Yes:
                return
        self.drafts.clear()
        self.input_table.setRowCount(0)
        self._sync_selected_draft()
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

    def _open_selected_output_folder(self, *_args: object) -> None:
        job = self._selected_job()
        if job is not None:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(job.request.output_path.parent)))

    def _copy_selected_command(self) -> None:
        job = self._selected_job()
        if job is None or self.queue is None:
            return
        QApplication.clipboard().setText(self._job_command(job))

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
        draft = self._current_draft()
        probed_draft = draft is not None and draft.asset is not None
        ready_inputs = any(item.asset is not None for item in self._selected_drafts())
        self.queue_selected_action.setEnabled(bool(queue) and ready_inputs)
        self.queue_start_action.setEnabled(bool(queue) and ready_inputs and not has_active)
        self.start_action.setEnabled(has_queued and not has_active)
        self.start_selected_action.setEnabled(selected_queued and not has_active)
        self.stop_action.setEnabled(bool(queue and queue.is_dispatching and has_active))
        self.cancel_action.setEnabled(has_active)
        self.cancel_all_action.setEnabled(has_active or has_queued)
        self.retry_action.setEnabled(selected_terminal and not has_active)
        self.remove_jobs_action.setEnabled(removable)
        self.clear_action.setEnabled(terminal_jobs)
        self.remove_inputs_button.setEnabled(bool(self._selected_drafts()))
        self.stream_details_button.setEnabled(probed_draft)
        self.browse_output_button.setEnabled(probed_draft)

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
        adapter = self._current_adapter()
        if adapter is None:
            self._restoring_configuration = False
            return False
        descriptor = adapter.descriptor
        codec_index = self.codec_combo.findData(configuration.codec.value)
        if codec_index >= 0:
            self.codec_combo.setCurrentIndex(codec_index)
        format_index = self.format_combo.findData(configuration.output_format.value)
        if format_index >= 0:
            self.format_combo.setCurrentIndex(format_index)
        restored_all = self._set_sample_rate(
            configuration.common.sample_rate if descriptor.supports_sample_rate else None
        )
        layout = configuration.common.channel_layout if descriptor.supports_channel_layout else None
        layout_index = self.channels.findData(layout)
        self.channels.setCurrentIndex(max(layout_index, 0))
        self.gain_db.setValue(configuration.common.gain_db if descriptor.supports_gain else 0.0)
        self.tempo_ratio.setValue(
            configuration.common.tempo_ratio if descriptor.supports_tempo else 1.0
        )
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
            elif isinstance(widget, QCheckBox) and isinstance(value, bool):
                widget.setChecked(value)
            elif isinstance(widget, QLineEdit) and isinstance(value, str):
                widget.setText(value)
        self._refresh_dynamic_option_choices()
        for key, value in configuration.encoder_options.items():
            widget = self.option_widgets.get(key)
            if isinstance(widget, QComboBox):
                option_index = widget.findData(value)
                if option_index >= 0:
                    widget.setCurrentIndex(option_index)
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

    def terminate_encoders(self) -> None:
        """Kill any surviving encoder process tree. Wired to QApplication.aboutToQuit
        so that quitting by a route other than closeEvent cannot leak a child."""
        if self.queue is not None:
            self.queue.terminate_processes()

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        if self._restore_maximized:
            # Deferred to the first show so callers keep control of when the window
            # appears; maximizing in __init__ would force it visible early.
            self._restore_maximized = False
            self.setWindowState(self.windowState() | Qt.WindowState.WindowMaximized)

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
        # normalGeometry is the un-maximized client rect, so a window closed while
        # maximized still remembers a sane size to restore down to.
        geometry = self.normalGeometry()
        if geometry.isEmpty():
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
            window_maximized=self.isMaximized(),
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


def _visible_rect(rect: QRect) -> QRect:
    """Return ``rect`` if any screen still shows it, otherwise a centred fallback.

    Guards against a rect saved on a monitor that has since been unplugged or resized,
    which would otherwise reopen the window somewhere the user cannot reach it.
    """
    if any(screen.availableGeometry().intersects(rect) for screen in QGuiApplication.screens()):
        return rect
    screen = QGuiApplication.primaryScreen()
    if screen is None:
        return rect
    available = screen.availableGeometry()
    size = rect.size().boundedTo(available.size())
    centred = QRect(available.topLeft(), size)
    centred.moveCenter(available.center())
    return centred
