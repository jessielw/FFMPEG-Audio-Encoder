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
    ]
    legacy_icon = project_root / "legacy_v4" / "Runtime" / "Images" / "icon.ico"
    if sys.platform == "win32" and legacy_icon.is_file():
        arguments.extend(("--icon", str(legacy_icon)))
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
