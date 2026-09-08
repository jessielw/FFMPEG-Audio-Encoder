from __future__ import annotations

from pathlib import Path

import pytest
from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
    QScrollArea,
    QTableWidgetItem,
    QToolButton,
)

from ffmpeg_audio_encoder.domain.errors import AudioEncoderError
from ffmpeg_audio_encoder.domain.models import (
    AppSettings,
    AudioStream,
    Codec,
    CommonAudioOptions,
    DelaySource,
    DetectedDelay,
    EncoderConfiguration,
    MediaAsset,
    OutputFormat,
    ThemePreference,
    Toolchain,
)
from ffmpeg_audio_encoder.infrastructure.persistence import PresetRepository, SettingsRepository
from ffmpeg_audio_encoder.infrastructure.tools import (
    ToolReport,
    inspect_toolchain,
    locate_toolchain,
)
from ffmpeg_audio_encoder.ui import main_window as main_window_module
from ffmpeg_audio_encoder.ui.custom_splitter import CustomSplitter, CustomSplitterHandle
from ffmpeg_audio_encoder.ui.main_window import InputDraft, MainWindow, ToolInspectionThread
from ffmpeg_audio_encoder.ui.theme import ThemeManager
from tests.test_integration_ffmpeg import _write_test_wave


def test_main_window_can_shrink_and_scroll(tmp_path: Path, qtbot, qapp: QApplication) -> None:
    window = MainWindow(
        SettingsRepository(tmp_path / "settings.json"),
        PresetRepository(tmp_path / "presets.json"),
        ThemeManager(qapp),
        None,
    )
    qtbot.addWidget(window)
    window.resize(480, 360)
    window.show()
    qtbot.wait(10)

    scroll_area = window.centralWidget()
    assert isinstance(scroll_area, QScrollArea)
    assert window.minimumSize().width() == 480
    assert window.minimumSize().height() == 360
    assert scroll_area.verticalScrollBar().maximum() > 0


def test_settings_button_is_reenabled_after_tool_inspection(
    tmp_path: Path, qtbot, qapp: QApplication
) -> None:
    window = MainWindow(
        SettingsRepository(tmp_path / "settings.json"),
        PresetRepository(tmp_path / "presets.json"),
        ThemeManager(qapp),
        None,
    )
    qtbot.addWidget(window)

    window.settings_button.setEnabled(False)
    window._tool_inspection_finished()

    assert window.settings_button.isEnabled()


def test_toolchain_actions_are_gated_while_tools_are_checked(
    tmp_path: Path, qtbot, qapp: QApplication
) -> None:
    """An in-flight probe is about to swap the toolchain, probe service and queue
    controller, so nothing that depends on them should be reachable meanwhile."""
    window = MainWindow(
        SettingsRepository(tmp_path / "settings.json"),
        PresetRepository(tmp_path / "presets.json"),
        ThemeManager(qapp),
        None,
    )
    qtbot.addWidget(window)

    window._tool_thread = ToolInspectionThread(window.settings, window)
    window._refresh_actions()

    assert not window.settings_button.isEnabled()
    assert not window.settings_action.isEnabled()
    assert not window.queue_selected_action.isEnabled()
    assert not window.start_action.isEnabled()
    assert not window.retry_action.isEnabled()

    window._tool_inspection_finished()

    assert window.settings_button.isEnabled()
    assert window.settings_action.isEnabled()


def test_settings_cannot_be_reopened_while_a_check_is_in_flight(
    tmp_path: Path, qtbot, qapp: QApplication, monkeypatch
) -> None:
    """Ctrl+, bypasses the disabled button, and _start_tool_inspection drops a second
    request, so a save made mid-check used to vanish without a word."""
    window = MainWindow(
        SettingsRepository(tmp_path / "settings.json"),
        PresetRepository(tmp_path / "presets.json"),
        ThemeManager(qapp),
        None,
    )
    qtbot.addWidget(window)
    window._tool_thread = ToolInspectionThread(window.settings, window)

    told: list[str] = []
    monkeypatch.setattr(
        main_window_module.QMessageBox,
        "information",
        lambda _parent, _title, text, *args, **kwargs: told.append(text),
    )
    monkeypatch.setattr(
        main_window_module,
        "SettingsDialog",
        lambda *args, **kwargs: pytest.fail("the settings dialog must not open"),
    )

    window._open_settings()

    assert told and "tool check" in told[0]


def test_inputs_are_not_accepted_while_tools_are_checked(
    tmp_path: Path, qtbot, qapp: QApplication
) -> None:
    """Files added mid-check would be handed to a probe service that is about to be
    cancelled, stranding them un-probed."""
    window = MainWindow(
        SettingsRepository(tmp_path / "settings.json"),
        PresetRepository(tmp_path / "presets.json"),
        ThemeManager(qapp),
        None,
    )
    qtbot.addWidget(window)
    source = tmp_path / "clip.wav"
    _write_test_wave(source, seconds=0.1)
    window._tool_thread = ToolInspectionThread(window.settings, window)

    window._add_paths([source])

    assert window.drafts == []
    assert "Checking encoder tools" in window.statusBar().currentMessage()


def test_main_window_uses_custom_splitters_and_can_collapse_queue(
    tmp_path: Path, qtbot, qapp: QApplication
) -> None:
    window = MainWindow(
        SettingsRepository(tmp_path / "settings.json"),
        PresetRepository(tmp_path / "presets.json"),
        ThemeManager(qapp),
        None,
    )
    qtbot.addWidget(window)
    window.show()
    qtbot.waitUntil(lambda: window.main_splitter.sizes()[1] > 0)

    assert isinstance(window.draft_splitter, CustomSplitter)
    assert isinstance(window.main_splitter, CustomSplitter)
    assert isinstance(window.main_splitter.handle(1), CustomSplitterHandle)
    assert window.draft_splitter.orientation() is Qt.Orientation.Horizontal
    assert window.main_splitter.orientation() is Qt.Orientation.Vertical

    window.toggle_queue_button.click()
    assert window.main_splitter.sizes()[1] == 0
    assert window.toggle_queue_button.text() == "Show queue"

    window.toggle_queue_button.click()
    assert window.main_splitter.sizes()[1] > 0
    assert window.toggle_queue_button.text() == "Hide queue"


def test_encoding_configuration_uses_scrollable_tabs(
    tmp_path: Path, qtbot, qapp: QApplication
) -> None:
    window = MainWindow(
        SettingsRepository(tmp_path / "settings.json"),
        PresetRepository(tmp_path / "presets.json"),
        ThemeManager(qapp),
        None,
    )
    qtbot.addWidget(window)

    assert [window.config_tabs.tabText(index) for index in range(window.config_tabs.count())] == [
        "General",
        "Options",
        "Output",
    ]
    for area in (window.general_scroll, window.options_scroll, window.output_scroll):
        assert area.widgetResizable()
        assert area.horizontalScrollBarPolicy() is Qt.ScrollBarPolicy.ScrollBarAlwaysOff
    assert window.options_form.rowWrapPolicy() is QFormLayout.RowWrapPolicy.WrapLongRows
    assert window.options_group.title() == "FFmpeg libopus options"


def test_main_window_restores_last_encoder_configuration(
    tmp_path: Path, qtbot, qapp: QApplication
) -> None:
    settings_repository = SettingsRepository(tmp_path / "settings.json")
    settings_repository.save(
        AppSettings(
            last_configuration=EncoderConfiguration(
                "ffmpeg.flac",
                Codec.FLAC,
                OutputFormat.FLAC,
                CommonAudioOptions(44_100, "stereo", 2.5, 1.25, -125.5),
                {"compression_level": 7, "custom_args": ""},
            )
        )
    )
    report = ToolReport(
        Toolchain(Path("ffmpeg"), Path("ffprobe")),
        "ffmpeg version",
        "ffprobe version",
        frozenset({"flac"}),
        frozenset({"flac"}),
    )

    window = MainWindow(
        settings_repository,
        PresetRepository(tmp_path / "presets.json"),
        ThemeManager(qapp),
        report,
    )
    qtbot.addWidget(window)

    assert window.encoder_combo.currentData() == "ffmpeg.flac"
    assert window._sample_rate_value() == 44_100
    assert window.channels.currentData() == "stereo"
    assert window.gain_db.value() == 2.5
    assert window.tempo_ratio.value() == 1.25
    assert window.delay_ms.value() == 0
    assert window.option_widgets["compression_level"].property("value") == 7


def test_main_window_probes_input_and_switches_generated_encoder_form(
    tmp_path: Path, qtbot, qapp: QApplication
) -> None:
    try:
        report = inspect_toolchain(locate_toolchain(AppSettings()))
    except AudioEncoderError as exc:
        pytest.skip(str(exc))
    window = MainWindow(
        SettingsRepository(tmp_path / "settings.json"),
        PresetRepository(tmp_path / "presets.json"),
        ThemeManager(qapp),
        report,
    )
    qtbot.addWidget(window)
    source = tmp_path / "tone.wav"
    _write_test_wave(source)
    window._add_paths([source])
    qtbot.waitUntil(lambda: bool(window.drafts and window.drafts[0].asset), timeout=10_000)
    window.input_table.selectRow(0)
    assert "-c:a libopus" in window.command_preview.toPlainText()
    flac_index = window.encoder_combo.findData("ffmpeg.flac")
    window.encoder_combo.setCurrentIndex(flac_index)
    window.delay_ms.setValue(-125.5)
    assert "atrim=start=0.1255,asetpts=PTS-STARTPTS" in window.command_preview.toPlainText()
    assert "-c:a flac" in window.command_preview.toPlainText()
    assert set(window.option_widgets) == {"compression_level", "custom_args"}


def test_requests_use_each_drafts_detected_or_overridden_delay(
    tmp_path: Path, qtbot, qapp: QApplication
) -> None:
    report = ToolReport(
        Toolchain(Path("ffmpeg"), Path("ffprobe")),
        "ffmpeg version",
        "ffprobe version",
        frozenset({"flac"}),
        frozenset({"flac"}),
    )
    window = MainWindow(
        SettingsRepository(tmp_path / "settings.json"),
        PresetRepository(tmp_path / "presets.json"),
        ThemeManager(qapp),
        report,
    )
    qtbot.addWidget(window)
    window.encoder_combo.setCurrentIndex(window.encoder_combo.findData("ffmpeg.flac"))
    first_stream = AudioStream(1, 1, "aac")
    second_stream = AudioStream(2, 1, "ac3")
    first = InputDraft(
        tmp_path / "First [DELAY 80ms].aac",
        asset=MediaAsset(
            tmp_path / "First [DELAY 80ms].aac",
            (first_stream,),
            detected_delays=(DetectedDelay(1, 80, DelaySource.FILENAME),),
        ),
    )
    second = InputDraft(
        tmp_path / "Second.mkv",
        asset=MediaAsset(
            tmp_path / "Second.mkv",
            (second_stream,),
            detected_delays=(DetectedDelay(2, -21.5, DelaySource.CONTAINER),),
            has_video_reference=True,
        ),
        delay_overrides_ms={2: -10},
    )

    first_request = window._build_request(first)
    second_request = window._build_request(second)

    assert first_request.common.delay_ms == 80
    assert second_request.common.delay_ms == -10
    assert "DELAY" not in first_request.output_path.name


def test_generated_aac_form_supports_decimal_conditional_and_text_options(
    tmp_path: Path, qtbot, qapp: QApplication
) -> None:
    report = ToolReport(
        Toolchain(Path("ffmpeg"), Path("ffprobe")),
        "ffmpeg version",
        "ffprobe version",
        frozenset({"aac"}),
        frozenset({"ipod", "adts"}),
    )
    window = MainWindow(
        SettingsRepository(tmp_path / "settings.json"),
        PresetRepository(tmp_path / "presets.json"),
        ThemeManager(qapp),
        report,
    )
    qtbot.addWidget(window)
    window.encoder_combo.setCurrentIndex(window.encoder_combo.findData("ffmpeg.aac"))

    quality = window.option_widgets["quality"]
    custom_args = window.option_widgets["custom_args"]
    assert isinstance(quality, QDoubleSpinBox)
    assert isinstance(custom_args, QLineEdit)
    assert not quality.isEnabled()
    rate_control = window.option_widgets["rate_control"]
    assert isinstance(rate_control, QComboBox)
    rate_control.setCurrentIndex(rate_control.findData("vbr"))
    assert quality.isEnabled()
    assert window.channels.findData("7.1") >= 0


def test_external_aac_formats_do_not_depend_on_ffmpeg_output_muxers(
    tmp_path: Path, qtbot, qapp: QApplication
) -> None:
    report = ToolReport(
        Toolchain(Path("ffmpeg"), Path("ffprobe"), qaac=Path("qaac64")),
        "ffmpeg version",
        "ffprobe version",
        frozenset(),
        frozenset({"wav"}),
        "qaac 2.82",
    )
    window = MainWindow(
        SettingsRepository(tmp_path / "settings.json"),
        PresetRepository(tmp_path / "presets.json"),
        ThemeManager(qapp),
        report,
    )
    qtbot.addWidget(window)
    window.encoder_combo.setCurrentIndex(window.encoder_combo.findData("qaac.aac"))

    assert [
        window.format_combo.itemData(index) for index in range(window.format_combo.count())
    ] == ["m4a", "adts-aac"]


def test_standalone_opus_does_not_require_ffmpeg_libopus(
    tmp_path: Path, qtbot, qapp: QApplication
) -> None:
    report = ToolReport(
        Toolchain(Path("ffmpeg"), Path("ffprobe"), opusenc=Path("opusenc")),
        "ffmpeg version",
        "ffprobe version",
        frozenset(),
        frozenset({"wav"}),
        opusenc_version="opusenc opus-tools 0.2",
    )
    window = MainWindow(
        SettingsRepository(tmp_path / "settings.json"),
        PresetRepository(tmp_path / "presets.json"),
        ThemeManager(qapp),
        report,
    )
    qtbot.addWidget(window)

    index = window.encoder_combo.findData("opusenc.opus")
    assert index >= 0
    assert window._adapter_available("opusenc.opus")
    window.encoder_combo.setCurrentIndex(index)
    assert set(window.option_widgets) == {
        "bitrate_kbps",
        "rate_control",
        "signal",
        "complexity",
        "frame_duration",
        "packet_loss",
        "phase_inversion",
        "max_delay_ms",
        "custom_args",
    }


def test_deezy_form_uses_boolean_widgets_and_disables_unsupported_common_controls(
    tmp_path: Path, qtbot, qapp: QApplication
) -> None:
    report = ToolReport(
        Toolchain(
            Path("ffmpeg"),
            Path("ffprobe"),
            deezy=Path("deezy"),
            dee=Path("dee"),
        ),
        "ffmpeg version",
        "ffprobe version",
        frozenset(),
        deezy_version="DeeZy 1.3.10",
        dee_version="dee.exe, Version 5.2.1",
    )
    window = MainWindow(
        SettingsRepository(tmp_path / "settings.json"),
        PresetRepository(tmp_path / "presets.json"),
        ThemeManager(qapp),
        report,
    )
    qtbot.addWidget(window)
    window.encoder_combo.setCurrentIndex(window.encoder_combo.findData("deezy.dd"))

    assert isinstance(window.option_widgets["dialogue_intelligence"], QCheckBox)
    assert window.channels.itemText(0) == "Auto"
    assert not window.sample_rate.isEnabled()
    assert window.channels.isEnabled()
    assert not window.gain_db.isEnabled()
    assert not window.tempo_ratio.isEnabled()

    metering = window.option_widgets["metering_mode"]
    dialogue = window.option_widgets["dialogue_intelligence"]
    speech = window.option_widgets["speech_threshold"]
    assert isinstance(metering, QComboBox)
    assert isinstance(dialogue, QCheckBox)
    assert speech.isEnabled()
    metering.setCurrentIndex(metering.findData("1770_1"))
    assert not speech.isEnabled()
    metering.setCurrentIndex(metering.findData("1770_3"))
    assert speech.isEnabled()
    dialogue.setChecked(False)
    assert not speech.isEnabled()


def test_deezy_bitrate_dropdown_tracks_layout_and_atmos_profile(
    tmp_path: Path, qtbot, qapp: QApplication
) -> None:
    report = ToolReport(
        Toolchain(
            Path("ffmpeg"),
            Path("ffprobe"),
            deezy=Path("deezy"),
            dee=Path("dee"),
            truehdd=Path("truehdd"),
        ),
        "ffmpeg version",
        "ffprobe version",
        frozenset(),
        deezy_version="DeeZy 1.3.13",
        dee_version="dee.exe, Version 5.2.1",
        truehdd_version="truehdd",
    )
    window = MainWindow(
        SettingsRepository(tmp_path / "settings.json"),
        PresetRepository(tmp_path / "presets.json"),
        ThemeManager(qapp),
        report,
    )
    qtbot.addWidget(window)

    window.encoder_combo.setCurrentIndex(window.encoder_combo.findData("deezy.dd"))
    window.channels.setCurrentIndex(window.channels.findData("5.1"))
    bitrate = window.option_widgets["bitrate_kbps"]
    assert isinstance(bitrate, QComboBox)
    assert [bitrate.itemData(index) for index in range(bitrate.count())] == [
        0,
        224,
        256,
        320,
        384,
        448,
        512,
        576,
        640,
    ]

    window.encoder_combo.setCurrentIndex(window.encoder_combo.findData("deezy.atmos"))
    bitrate = window.option_widgets["bitrate_kbps"]
    mode = window.option_widgets["atmos_mode"]
    assert isinstance(bitrate, QComboBox)
    assert isinstance(mode, QComboBox)
    assert [bitrate.itemData(index) for index in range(bitrate.count())] == [
        0,
        384,
        448,
        512,
        576,
        640,
        768,
        1024,
    ]
    mode.setCurrentIndex(mode.findData("bluray"))
    assert [bitrate.itemData(index) for index in range(bitrate.count())] == [
        0,
        1152,
        1280,
        1408,
        1512,
        1536,
        1664,
    ]

    window.encoder_combo.setCurrentIndex(window.encoder_combo.findData("deezy.dd"))
    configuration = EncoderConfiguration(
        "deezy.atmos",
        Codec.ATMOS,
        OutputFormat.EAC3,
        CommonAudioOptions(),
        {"bitrate_kbps": 1280, "atmos_mode": "bluray"},
    )
    assert window._apply_configuration(configuration)
    restored_mode = window.option_widgets["atmos_mode"]
    restored_bitrate = window.option_widgets["bitrate_kbps"]
    assert isinstance(restored_mode, QComboBox)
    assert isinstance(restored_bitrate, QComboBox)
    assert restored_mode.currentData() == "bluray"
    assert restored_bitrate.currentData() == 1280


def test_sample_rate_choices_follow_ffmpeg_encoder_capabilities(
    tmp_path: Path, qtbot, qapp: QApplication
) -> None:
    report = ToolReport(
        Toolchain(Path("ffmpeg"), Path("ffprobe")),
        "ffmpeg version",
        "ffprobe version",
        frozenset({"aac", "ac3", "flac"}),
        frozenset({"ipod", "adts", "ac3", "flac"}),
    )
    window = MainWindow(
        SettingsRepository(tmp_path / "settings.json"),
        PresetRepository(tmp_path / "presets.json"),
        ThemeManager(qapp),
        report,
    )
    qtbot.addWidget(window)

    window.encoder_combo.setCurrentIndex(window.encoder_combo.findData("ffmpeg.aac"))
    assert not window.sample_rate.isEditable()
    assert [window.sample_rate.itemData(index) for index in range(window.sample_rate.count())] == [
        None,
        7350,
        8000,
        11025,
        12000,
        16000,
        22050,
        24000,
        32000,
        44100,
        48000,
        64000,
        88200,
        96000,
    ]

    window.sample_rate.setCurrentIndex(window.sample_rate.findData(44100))
    window.encoder_combo.setCurrentIndex(window.encoder_combo.findData("ffmpeg.ac3"))
    assert window.sample_rate.currentData() == 44100
    assert [window.sample_rate.itemData(index) for index in range(window.sample_rate.count())] == [
        None,
        32000,
        44100,
        48000,
    ]

    window.encoder_combo.setCurrentIndex(window.encoder_combo.findData("ffmpeg.flac"))
    assert window.sample_rate.isEditable()
    assert window._set_sample_rate(12345)
    assert window._sample_rate_value() == 12345


def test_theme_manager_produces_a_real_icon(qapp: QApplication, qtbot) -> None:
    from PySide6.QtWidgets import QPushButton

    manager = ThemeManager(qapp)
    button = QPushButton()
    qtbot.addWidget(button)
    manager.register(button, "ph.play-light")
    manager.apply(ThemePreference.DARK)
    assert not button.icon().isNull()
    manager.apply(ThemePreference.AUTOMATIC)


def _window(tmp_path: Path, qtbot, qapp: QApplication, *, report=None) -> MainWindow:
    window = MainWindow(
        SettingsRepository(tmp_path / "settings.json"),
        PresetRepository(tmp_path / "presets.json"),
        ThemeManager(qapp),
        report,
    )
    qtbot.addWidget(window)
    return window


def test_window_geometry_round_trips_without_creeping(
    tmp_path: Path, qtbot, qapp: QApplication
) -> None:
    repository = SettingsRepository(tmp_path / "settings.json")
    window = MainWindow(
        repository,
        PresetRepository(tmp_path / "presets.json"),
        ThemeManager(qapp),
        None,
    )
    qtbot.addWidget(window)
    window.show()
    qtbot.waitExposed(window)
    window.setGeometry(QRect(120, 90, 1000, 720))
    qtbot.wait(20)
    saved = window.geometry()
    window.close()

    stored = repository.load()
    assert (stored.window_x, stored.window_y) == (saved.x(), saved.y())
    assert (stored.window_width, stored.window_height) == (saved.width(), saved.height())
    assert stored.window_maximized is False

    # Reopening must land on the same rect; the old move()/geometry() mismatch
    # walked the window down by one title bar per launch.
    reopened = MainWindow(
        SettingsRepository(tmp_path / "settings.json"),
        PresetRepository(tmp_path / "presets.json"),
        ThemeManager(qapp),
        None,
    )
    qtbot.addWidget(reopened)
    assert reopened.geometry() == saved


def test_saved_maximized_state_is_reapplied_on_show(
    tmp_path: Path, qtbot, qapp: QApplication
) -> None:
    repository = SettingsRepository(tmp_path / "settings.json")
    repository.save(AppSettings(window_maximized=True, window_x=50, window_y=50))
    window = MainWindow(
        repository,
        PresetRepository(tmp_path / "presets.json"),
        ThemeManager(qapp),
        None,
    )
    qtbot.addWidget(window)
    assert window._restore_maximized is True
    window.show()
    qtbot.waitExposed(window)
    assert window.windowState() & Qt.WindowState.WindowMaximized
    assert window._restore_maximized is False


def test_offscreen_geometry_falls_back_to_a_visible_rect(
    tmp_path: Path, qtbot, qapp: QApplication
) -> None:
    repository = SettingsRepository(tmp_path / "settings.json")
    repository.save(AppSettings(window_x=-40_000, window_y=-40_000))
    window = MainWindow(
        repository,
        PresetRepository(tmp_path / "presets.json"),
        ThemeManager(qapp),
        None,
    )
    qtbot.addWidget(window)
    available = QGuiApplication.primaryScreen().availableGeometry()
    assert available.intersects(window.geometry())


def test_input_table_has_a_context_menu_gated_on_selection(
    tmp_path: Path, qtbot, qapp: QApplication
) -> None:
    window = _window(tmp_path, qtbot, qapp)
    assert window.input_table.contextMenuPolicy() is Qt.ContextMenuPolicy.CustomContextMenu

    menu = window._build_input_menu()
    labels = [action.text() for action in menu.actions() if not action.isSeparator()]
    assert labels == [
        "Add files…",
        "Remove selected",
        "Inspect stream",
        "Open containing folder",
        "Copy full path",
        "Clear all inputs",
    ]
    by_label = {action.text(): action for action in menu.actions()}
    assert by_label["Add files…"].isEnabled()
    assert not by_label["Remove selected"].isEnabled()
    assert not by_label["Clear all inputs"].isEnabled()

    window.drafts.append(InputDraft(tmp_path / "clip.mkv"))
    window.input_table.insertRow(0)
    window.input_table.setItem(0, 0, QTableWidgetItem("clip.mkv"))
    window.input_table.selectRow(0)
    enabled = {action.text(): action.isEnabled() for action in window._build_input_menu().actions()}
    assert enabled["Remove selected"]
    assert enabled["Copy full path"]
    assert enabled["Clear all inputs"]
    # Not probed yet, so there is no stream to inspect.
    assert not enabled["Inspect stream"]


def test_queue_detail_panes_grow_with_the_splitter(
    tmp_path: Path, qtbot, qapp: QApplication
) -> None:
    window = _window(tmp_path, qtbot, qapp)
    window.resize(1200, 900)
    window.show()
    # Wait for the deferred _restore_splitters, which would otherwise overwrite the
    # sizes this test sets.
    qtbot.waitUntil(lambda: window.main_splitter.sizes()[1] >= 200)

    # The old 130px cap meant only the tab frame grew, never the text areas.
    assert window.job_details.maximumHeight() >= 16_777_215
    assert window.log_output.maximumHeight() >= 16_777_215

    upper, lower = window.main_splitter.sizes()
    before = window.job_details.height()
    window.main_splitter.setSizes([upper - 200, lower + 200])
    qtbot.waitUntil(lambda: window.job_details.height() > before)


def test_view_menu_toggle_stays_in_sync_with_the_queue_button(
    tmp_path: Path, qtbot, qapp: QApplication
) -> None:
    window = _window(tmp_path, qtbot, qapp)
    window.show()
    qtbot.waitUntil(lambda: window.main_splitter.sizes()[1] > 0)

    assert window.queue_panel_action.isChecked()
    window.toggle_queue_button.click()
    assert not window.queue_panel_action.isChecked()
    window.queue_panel_action.setChecked(True)
    assert window.toggle_queue_button.isChecked()
    assert window.main_splitter.sizes()[1] > 0


def test_adding_paths_expands_folders_and_reports_duplicates(
    tmp_path: Path, qtbot, qapp: QApplication
) -> None:
    try:
        report = inspect_toolchain(locate_toolchain(AppSettings()))
    except AudioEncoderError as exc:
        pytest.skip(str(exc))
    window = _window(tmp_path, qtbot, qapp, report=report)

    folder = tmp_path / "batch"
    (folder / "nested").mkdir(parents=True)
    _write_test_wave(folder / "one.wav")
    _write_test_wave(folder / "nested" / "two.wav")

    window._add_paths([folder])
    assert {draft.path.name for draft in window.drafts} == {"one.wav", "two.wav"}

    window._add_paths([folder / "one.wav"])
    assert len(window.drafts) == 2
    assert "already listed" in window.statusBar().currentMessage()


def test_selected_job_log_appends_instead_of_rebuilding(
    tmp_path: Path, qtbot, qapp: QApplication
) -> None:
    report = ToolReport(
        Toolchain(Path("ffmpeg"), Path("ffprobe")),
        "ffmpeg version",
        "ffprobe version",
        frozenset({"flac"}),
        frozenset({"flac"}),
    )
    window = _window(tmp_path, qtbot, qapp, report=report)
    window.encoder_combo.setCurrentIndex(window.encoder_combo.findData("ffmpeg.flac"))
    source = tmp_path / "tone.wav"
    _write_test_wave(source)
    draft = InputDraft(source)
    draft.asset = MediaAsset(
        source,
        (AudioStream(0, 1, "pcm_s16le", 2, "stereo", 48000, "eng", None, 1.0),),
    )
    window.drafts.append(draft)
    window.input_table.insertRow(0)
    window.input_table.setItem(0, 0, QTableWidgetItem(source.name))
    window.input_table.selectRow(0)

    queued = window._queue_selected()
    assert len(queued) == 1
    job_id = str(next(iter(queued)))
    window.queue_table.selectRow(0)
    assert window._details_job_id == job_id

    window._append_log(job_id, "first line\n")
    window._append_log(job_id, "second line\n")
    text = window.job_details.toPlainText()
    assert "first line" in text
    assert text.rstrip().endswith("second line")
    assert text.count("Command:") == 1

    # The command is memoised, so repeated renders never rebuild the plan.
    assert window._job_command_cache[job_id]
    window._job_command_cache[job_id] = "sentinel"
    window._selected_job_changed()
    assert "Command: sentinel" in window.job_details.toPlainText()


def _full_report() -> ToolReport:
    return ToolReport(
        Toolchain(Path("ffmpeg"), Path("ffprobe")),
        "ffmpeg version",
        "ffprobe version",
        frozenset({"libopus", "flac", "aac", "libmp3lame", "ac3", "eac3", "dca", "alac"}),
        frozenset(),
        qaac_version="qaac 2.8",
        fdkaac_version="fdkaac 1.0",
        opusenc_version="opusenc 0.2",
        deezy_version="deezy 1.0",
        dee_version="dee 5",
        truehdd_version="truehdd 0.3",
    )


def _combo_rows(combo: QComboBox) -> list[str]:
    rows: list[str] = []
    for index in range(combo.count()):
        separator = combo.itemData(index, Qt.ItemDataRole.AccessibleDescriptionRole) == "separator"
        rows.append("---" if separator else str(combo.itemData(index)))
    return rows


def test_encoder_picker_separates_the_encoder_families(
    tmp_path: Path, qtbot, qapp: QApplication
) -> None:
    window = _window(tmp_path, qtbot, qapp, report=_full_report())

    rows = _combo_rows(window.encoder_combo)
    assert rows.count("---") == 2
    assert rows[rows.index("---") - 1] == "ffmpeg.alac"
    assert rows[rows.index("---") + 1] == "opusenc.opus"
    assert rows[rows.index("---", rows.index("---") + 1) + 1] == "deezy.dd"
    # A separator carries no adapter id, so it must never become the selection.
    assert window.encoder_combo.currentData() == "ffmpeg.libopus"
    assert window._current_adapter() is not None


def test_encoder_picker_ignores_separators_when_no_encoder_is_available(
    tmp_path: Path, qtbot, qapp: QApplication
) -> None:
    # No tool report at all: every row is unavailable, and the fallback search walks
    # past the separators instead of asking the registry about them.
    window = _window(tmp_path, qtbot, qapp)

    assert window.encoder_combo.currentIndex() == 0
    assert window.encoder_combo.currentData() == "ffmpeg.libopus"


def test_queue_actions_share_one_grouped_toolbar(tmp_path: Path, qtbot, qapp: QApplication) -> None:
    window = _window(tmp_path, qtbot, qapp)

    layout = [
        "---" if action.isSeparator() else action.text()
        for action in window.queue_toolbar.actions()
    ]
    # The leading entry is the "Encoding queue" heading widget, which has no text.
    assert layout == [
        "",
        "Queue selected inputs",
        "Queue and start",
        "---",
        "Start queue",
        "Start selected",
        "---",
        "Stop after current",
        "Cancel active",
        "Cancel all",
        "---",
        "Retry selected",
        "Remove selected",
        "Clear finished",
    ]
    assert all(
        not action.icon().isNull()
        for action in window.queue_toolbar.actions()[1:]
        if not action.isSeparator()
    )
    assert window.queue_toolbar.toolButtonStyle() is Qt.ToolButtonStyle.ToolButtonTextBesideIcon
    # No style sheet: under Fusion a QSS on the toolbar makes its children resolve
    # colours from the style sheet defaults, which inverted enabled and disabled text.
    assert not window.queue_toolbar.styleSheet()


def test_stream_inspection_sits_beside_the_stream_combo(
    tmp_path: Path, qtbot, qapp: QApplication
) -> None:
    window = _window(tmp_path, qtbot, qapp)

    button = window.stream_details_button
    assert isinstance(button, QToolButton)
    assert not button.icon().isNull()
    assert not button.text()
    assert button.toolTip()
    assert button.parentWidget() is window.stream_combo.parentWidget()
    assert button.height() == window.stream_combo.sizeHint().height()
