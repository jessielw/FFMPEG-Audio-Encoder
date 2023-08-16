from pathlib import Path
from subprocess import run
import os


def build_app():
    # define and create pyinstaller output path
    pyinstaller_folder = Path(Path(__file__).parent / "pyinstaller_build")
    pyinstaller_folder.mkdir(exist_ok=True)

    # define paths before changing directory
    site_packages = Path(Path.cwd() / ".venv" / "Lib" / "site-packages")
    icon_path = Path(Path.cwd() / "Runtime" / "Images" / "icon.ico")
    ffmpeg_encoder_script = Path(Path.cwd() / "FFMPEGAudioEncoder.py")
    additional_hooks = Path(Path.cwd() / "Packages")

    # change directory so we output all of pyinstallers files in it's own folder
    os.chdir(pyinstaller_folder)

    # run pyinstaller command
    build_job = run(
        [
            "pyinstaller",
            "-F",
            "--paths",
            str(site_packages),
            "-n",
            "FFMPEGAudioEncoder",
            "-w",
            "--onefile",
            f"--icon={str(icon_path)}",
            str(ffmpeg_encoder_script),
            f"--additional-hooks-dir={additional_hooks}",
        ]
    )

    # get exe string based on os
    exe_str = ".exe"

    # ensure output of exe
    success = "Did not complete successfully"
    if (
        Path(Path("dist") / f"FFMPEGAudioEncoder{exe_str}").is_file()
        and str(build_job.returncode) == "0"
    ):
        success = f'\nSuccess!\nPath to exe: {str(Path.cwd() / (Path(Path("dist") / f"FFMPEGAudioEncoder{exe_str}")))}'

    # change directory back to original directory
    os.chdir(ffmpeg_encoder_script.parent)

    # return success message
    return success


if __name__ == "__main__":
    build = build_app()
    print(build)
