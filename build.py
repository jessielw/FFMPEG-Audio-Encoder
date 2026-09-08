from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def build_app() -> Path:
    project_root = Path(__file__).resolve().parent
    name = "FFMPEGAudioEncoder"
    arguments = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--windowed",
        "--onedir",
        "--name",
        name,
        "--paths",
        str(project_root / "src"),
        "--collect-all",
        "qtawesome",
        "--collect-all",
        "pymediainfo",
        # Carries the packaged icon into the bundle, where the runtime reads it back
        # out of ``ffmpeg_audio_encoder/resources``.
        "--collect-data",
        "ffmpeg_audio_encoder",
    ]
    icon = project_root / "src" / "ffmpeg_audio_encoder" / "resources" / "icon.ico"
    # Linux executables carry no embedded icon, so PyInstaller ignores --icon there.
    # On macOS it converts the .ico to an .icns, which needs Pillow from the build group.
    if sys.platform in {"win32", "darwin"} and icon.is_file():
        arguments.extend(("--icon", str(icon)))
    arguments.append(str(project_root / "src" / "ffmpeg_audio_encoder" / "__main__.py"))
    subprocess.run(arguments, cwd=project_root, check=True)
    app_bundle = project_root / "dist" / f"{name}.app"
    folder_bundle = project_root / "dist" / name
    output = app_bundle if app_bundle.exists() else folder_bundle
    if not output.exists():
        raise RuntimeError("PyInstaller completed without creating the expected application")
    return output


if __name__ == "__main__":
    artifact = build_app()
    print(artifact)
