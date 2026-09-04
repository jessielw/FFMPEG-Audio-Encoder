from __future__ import annotations

import argparse
import json
import sys

from PySide6.QtWidgets import QApplication

from ffmpeg_audio_encoder import __version__
from ffmpeg_audio_encoder.domain.errors import AudioEncoderError
from ffmpeg_audio_encoder.encoders import default_registry
from ffmpeg_audio_encoder.infrastructure.persistence import PresetRepository, SettingsRepository
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


def main() -> int:
    arguments, qt_arguments = _parser().parse_known_args()
    settings_repository = SettingsRepository()
    if arguments.diagnostics:
        return _diagnostics(settings_repository)

    app = QApplication([sys.argv[0], *qt_arguments])
    app.setStyle("Fusion")
    app.setApplicationName("FFmpeg Audio Encoder")
    app.setApplicationVersion(__version__)
    app.setOrganizationName("FFmpegAudioEncoder")
    theme_manager = ThemeManager(app)

    try:
        tool_report = inspect_toolchain(locate_toolchain(settings_repository.load()))
    except AudioEncoderError:
        tool_report = None
    window = MainWindow(
        settings_repository,
        PresetRepository(),
        theme_manager,
        tool_report,
    )
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
