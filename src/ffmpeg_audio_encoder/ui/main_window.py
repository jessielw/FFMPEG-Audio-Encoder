from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from uuid import UUID

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import (
    QCloseEvent,
    QDragEnterEvent,
    QDropEvent,
    QIntValidator,
    QStandardItemModel,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
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
from ffmpeg_audio_encoder.domain.errors import AudioEncoderError, ToolNotFoundError
from ffmpeg_audio_encoder.domain.models import (
    Codec,
    CommonAudioOptions,
    EncoderPreset,
    EncodingRequest,
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
from ffmpeg_audio_encoder.ui.models import QueueTableModel
from ffmpeg_audio_encoder.ui.theme import ThemeManager


@dataclass(slots=True)
class InputDraft:
    path: Path
    status: str = "Probing…"
    asset: MediaAsset | None = None
    stream_position: int = 0
    output_override: Path | None = None
    error: str | None = None


OptionWidget = QSpinBox | QDoubleSpinBox | QComboBox | QLineEdit


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
        self._syncing_output = False
        self._closing = False
        self._expanded_queue_height = 250

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
        self.theme_manager.apply(self.settings.theme)
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
        config_form.addRow("Audio stream", self.stream_combo)
        config_form.addRow("Encoder", self.encoder_combo)
        config_form.addRow("Codec", self.codec_combo)
        config_form.addRow("Container", self.format_combo)
        config_form.addRow("Sample rate", self.sample_rate)
        config_form.addRow("Channel layout", self.channels)
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
        self.overwrite = QCheckBox("Replace an existing file")
        self.overwrite.setChecked(self.settings.overwrite_default)
        output_form.addRow("Output preview", self.output_edit)
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
        self.start_button = QPushButton("Start queue")
        self.cancel_button = QPushButton("Cancel active")
        self.retry_button = QPushButton("Retry selected")
        self.remove_jobs_button = QPushButton("Remove selected")
        self.clear_button = QPushButton("Clear finished")
        for button in (
            self.queue_selected_button,
            self.start_button,
            self.cancel_button,
        ):
            queue_primary_actions.addWidget(button)
        queue_primary_actions.addStretch(1)
        queue_layout.addLayout(queue_primary_actions)

        queue_secondary_actions = QHBoxLayout()
        for button in (
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
        self.queue_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.queue_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.queue_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        queue_layout.addWidget(self.queue_table)
        self.log_output = QPlainTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMaximumBlockCount(3000)
        self.log_output.setMaximumHeight(130)
        queue_layout.addWidget(self.log_output)
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
        self.theme_manager.register(self.start_button, "ph.play-light")
        self.theme_manager.register(self.cancel_button, "ph.stop-light")

        self.add_files_button.clicked.connect(self._choose_files)
        self.remove_inputs_button.clicked.connect(self._remove_inputs)
        self.settings_button.clicked.connect(self._open_settings)
        self.toggle_queue_button.toggled.connect(self._set_queue_visible)
        self.main_splitter.splitterMoved.connect(self._splitter_moved)
        self.input_table.itemSelectionChanged.connect(self._sync_selected_draft)
        self.stream_combo.currentIndexChanged.connect(self._stream_changed)
        self.encoder_combo.currentIndexChanged.connect(self._encoder_changed)
        self.sample_rate.currentTextChanged.connect(self._refresh_preview)
        self.channels.currentIndexChanged.connect(self._refresh_preview)
        self.output_edit.textEdited.connect(self._output_edited)
        self.queue_selected_button.clicked.connect(self._queue_selected)
        self.start_button.clicked.connect(self._start_queue)
        self.cancel_button.clicked.connect(self._cancel_active)
        self.retry_button.clicked.connect(self._retry_selected)
        self.remove_jobs_button.clicked.connect(self._remove_selected_jobs)
        self.clear_button.clicked.connect(self._clear_finished)
        self.save_preset_button.clicked.connect(self._save_preset)
        self.delete_preset_button.clicked.connect(self._delete_preset)
        self.preset_combo.currentIndexChanged.connect(self._apply_preset)

        QTimer.singleShot(0, self._restore_splitters)

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
        self.tool_report = report
        if report is None:
            self.probe_service = None
            self.queue = None
            self.queue_model.set_controller(None)
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
        self.queue.persistence_error.connect(
            lambda message: self.statusBar().showMessage(message, 12000)
        )
        self.queue_model.set_controller(self.queue)
        self.statusBar().showMessage(
            f"Ready · {report.ffmpeg_version} · {report.ffprobe_version}", 12000
        )

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
        self._refresh_preview()

    def _stream_changed(self, position: int) -> None:
        draft = self._current_draft()
        if draft and draft.asset and 0 <= position < len(draft.asset.audio_streams):
            draft.stream_position = position
            draft.output_override = None
        self._refresh_preview()

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
        output = draft.output_override or default_output_path(
            draft.path, stream, codec, output_format, output_directory
        )
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

    def _queue_selected(self) -> None:
        if self.queue is None:
            QMessageBox.warning(self, "Tools not configured", "Configure FFmpeg and ffprobe first.")
            return
        drafts = self._selected_drafts()
        if not drafts:
            QMessageBox.information(self, "No inputs selected", "Select one or more input rows.")
            return
        errors: list[str] = []
        for draft in drafts:
            try:
                self.queue.add(self._build_request(draft), self.overwrite.isChecked())
            except (ValueError, AudioEncoderError) as exc:
                errors.append(f"{draft.path.name}: {exc}")
        if errors:
            QMessageBox.warning(self, "Some inputs were not queued", "\n".join(errors))

    def _start_queue(self) -> None:
        if self.queue:
            self.queue.start()

    def _cancel_active(self) -> None:
        if self.queue:
            self.queue.cancel_active()

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

    def _remove_selected_jobs(self) -> None:
        if self.queue:
            self.queue.remove(self._selected_job_ids())

    def _clear_finished(self) -> None:
        if self.queue:
            self.queue.clear_completed()

    def _remove_inputs(self) -> None:
        rows = sorted({index.row() for index in self.input_table.selectedIndexes()}, reverse=True)
        for row in rows:
            self.input_table.removeRow(row)
            self.drafts.pop(row)
        self._sync_selected_draft()

    def _append_log(self, job_id: str, text: str) -> None:
        self.log_output.appendPlainText(f"[{job_id[:8]}] {text.rstrip()}")

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
            CommonAudioOptions(self._sample_rate_value(), self.channels.currentData()),
            self._current_options(),
        )
        self.presets = [
            existing for existing in self.presets if existing.name.casefold() != name.casefold()
        ]
        self.presets.append(preset)
        self.preset_repository.save(self.presets)
        self.presets = self.preset_repository.load()
        self._populate_presets()
        self.preset_combo.setCurrentIndex(self.preset_combo.findData(name))

    def _apply_preset(self, *_args: object) -> None:
        name = self.preset_combo.currentData()
        preset = next((item for item in self.presets if item.name == name), None)
        if preset is None:
            return
        adapter_index = self.encoder_combo.findData(preset.encoder_id)
        if adapter_index < 0 or not self._adapter_available(preset.encoder_id):
            QMessageBox.warning(self, "Preset unavailable", "The preset's encoder is unavailable.")
            return
        self.encoder_combo.setCurrentIndex(adapter_index)
        self.codec_combo.setCurrentIndex(self.codec_combo.findData(preset.codec.value))
        self.format_combo.setCurrentIndex(self.format_combo.findData(preset.output_format.value))
        if not self._set_sample_rate(preset.common.sample_rate):
            self.statusBar().showMessage(
                "The preset's sample rate is not supported by this encoder; preserving input rate.",
                12000,
            )
        self.channels.setCurrentIndex(self.channels.findData(preset.common.channel_layout))
        for key, value in preset.encoder_options.items():
            widget = self.option_widgets.get(key)
            if isinstance(widget, QSpinBox) and isinstance(value, int):
                widget.setValue(value)
            elif isinstance(widget, QDoubleSpinBox) and isinstance(value, (int, float)):
                widget.setValue(float(value))
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(widget.findData(value))
            elif isinstance(widget, QLineEdit) and isinstance(value, str):
                widget.setText(value)
        self._refresh_option_states()
        self._refresh_preview()

    def _delete_preset(self) -> None:
        name = self.preset_combo.currentData()
        if not isinstance(name, str):
            return
        self.presets = [preset for preset in self.presets if preset.name != name]
        self.preset_repository.save(self.presets)
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
        try:
            report = inspect_toolchain(locate_toolchain(candidate))
        except ToolNotFoundError as exc:
            QMessageBox.critical(self, "Invalid tool configuration", str(exc))
            return
        self.settings = candidate
        self.settings_repository.save(candidate)
        self.theme_manager.apply(candidate.theme)
        self._configure_services(report)
        self._populate_encoders()

    def _active_changed(self, active: bool) -> None:
        self.settings_button.setEnabled(not active)
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
            self.queue.cancel_active()
            event.ignore()
            return
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
        self.settings_repository.save(self.settings)
        event.accept()
