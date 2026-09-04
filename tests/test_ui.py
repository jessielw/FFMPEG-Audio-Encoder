from __future__ import annotations

from pathlib import Path

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
    QScrollArea,
)

from ffmpeg_audio_encoder.domain.errors import AudioEncoderError
from ffmpeg_audio_encoder.domain.models import (
    AppSettings,
    Codec,
    CommonAudioOptions,
    EncoderConfiguration,
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
from ffmpeg_audio_encoder.ui.custom_splitter import CustomSplitter, CustomSplitterHandle
from ffmpeg_audio_encoder.ui.main_window import MainWindow
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
    assert window.delay_ms.value() == -125.5
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
