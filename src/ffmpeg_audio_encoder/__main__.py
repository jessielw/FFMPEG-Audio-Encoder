from __future__ import annotations

import argparse
import json
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# import qtawesome as qta
from pymediainfo import MediaInfo
from PySide6.QtCore import QLockFile, QTimer
from PySide6.QtWidgets import QApplication, QMessageBox

from ffmpeg_audio_encoder import __version__
from ffmpeg_audio_encoder.domain.errors import AudioEncoderError
from ffmpeg_audio_encoder.encoders import default_registry
from ffmpeg_audio_encoder.infrastructure.persistence import (
    JobRepository,
    PresetRepository,
    SettingsRepository,
    default_config_directory,
)
from ffmpeg_audio_encoder.infrastructure.tools import inspect_toolchain, locate_toolchain
from ffmpeg_audio_encoder.ui.main_window import MainWindow
from ffmpeg_audio_encoder.ui.theme import ThemeManager


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ffmpeg-audio-encoder")
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "--diagnostics",
        action="store_true",
        help="print tool discovery and encoder capability information without opening the GUI",
    )
    return parser


def _diagnostics(settings_repository: SettingsRepository) -> int:
    try:
        report = inspect_toolchain(locate_toolchain(settings_repository.load()))
    except AudioEncoderError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2))
        return 1
    print(
        json.dumps(
            {
                "ok": True,
                "ffmpeg": str(report.toolchain.ffmpeg),
                "ffprobe": str(report.toolchain.ffprobe),
                "ffmpeg_version": report.ffmpeg_version,
                "ffprobe_version": report.ffprobe_version,
                "mediainfo_available": MediaInfo.can_parse(),
                "qaac": str(report.toolchain.qaac) if report.toolchain.qaac else None,
                "qaac_version": report.qaac_version,
                "fdkaac": str(report.toolchain.fdkaac) if report.toolchain.fdkaac else None,
                "fdkaac_version": report.fdkaac_version,
                "encoders": {
                    adapter.descriptor.id: report.supports_adapter(adapter.descriptor)
                    for adapter in default_registry()
                },
                "muxers": sorted(report.muxers),
            },
            indent=2,
        )
    )
    return 0


def _configure_logging(config_directory: Path) -> Path:
    config_directory.mkdir(parents=True, exist_ok=True)
    log_path = config_directory / "application.log"
    handler = RotatingFileHandler(
        log_path,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    logging.basicConfig(level=logging.INFO, handlers=[handler])
    return log_path


def _install_exception_handler(log_path: Path) -> None:
    previous_hook = sys.excepthook

    def handle_exception(exception_type, exception, traceback) -> None:
        logging.getLogger(__name__).critical(
            "Unhandled exception",
            exc_info=(exception_type, exception, traceback),
        )
        if QApplication.instance() is not None:
            QMessageBox.critical(
                None,
                "Unexpected error",
                f"An unexpected error was recorded in:\n{log_path}\n\n{exception}",
            )
        else:
            previous_hook(exception_type, exception, traceback)

    sys.excepthook = handle_exception


def main() -> int:
    arguments, qt_arguments = _parser().parse_known_args()
    settings_repository = SettingsRepository()
    if arguments.diagnostics:
        return _diagnostics(settings_repository)

    config_directory = default_config_directory()
    log_path = _configure_logging(config_directory)
    _install_exception_handler(log_path)
    app = QApplication([sys.argv[0], *qt_arguments])
    app.setStyle("Fusion")
    app.setApplicationName("FFmpeg Audio Encoder")
    app.setApplicationVersion(__version__)
    app.setOrganizationName("FFmpegAudioEncoder")
    # app.setWindowIcon(qta.icon("ph.waveform-light", color="#3498db"))
    theme_manager = ThemeManager(app)
    instance_lock = QLockFile(str(config_directory / "application.lock"))
    if not instance_lock.tryLock(0):
        QMessageBox.critical(
            None,
            "FFmpeg Audio Encoder is already running",
            "Close the other application window before starting another instance.",
        )
        return 2
    window = MainWindow(
        settings_repository,
        PresetRepository(),
        theme_manager,
        None,
        JobRepository(),
    )
    window.show()
    QTimer.singleShot(0, window.discover_tools)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
