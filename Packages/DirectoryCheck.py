import pathlib
import shutil

# Checks for App Folder and Sub-Directories - Creates Folders if they are missing -------------------------------------

def directory_check():
    if shutil.which('ffmpeg') != None:
        pass
    elif shutil.which('ffmpeg') == None:
        ffmpeg_folder = pathlib.Path.cwd() / 'Apps' / 'FFMPEG'
    mediainfo_folder = pathlib.Path.cwd() / 'Apps' / 'MediaInfo'
    mediainfocli_folder = pathlib.Path.cwd() / 'Apps' / 'MediaInfoCLI'
    fdkaac_folder = pathlib.Path.cwd() / 'Apps' / 'fdkaac'
    qaac_folder = pathlib.Path.cwd() / 'Apps' / 'qaac'
    mpv_player_folder = pathlib.Path.cwd() / 'Apps' / 'mpv'
    if shutil.which('youtube-dl') != None:
        pass
    elif shutil.which('youtube-dl') == None:
        youtube_dl_folder = pathlib.Path.cwd() / 'Apps' / 'youtube-dl'

    try:
        if shutil.which('ffmpeg') != None:
            pass
        elif shutil.which('ffmpeg') == None:
            ffmpeg_folder.mkdir(parents=True, exist_ok=False)
        if shutil.which('youtube-dl') != None:
            pass
        elif shutil.which('youtube-dl') == None:
            youtube_dl_folder.mkdir(parents=True, exist_ok=False)
        mediainfo_folder.mkdir(parents=True, exist_ok=False)
        mediainfocli_folder.mkdir(parents=True, exist_ok=False)
        fdkaac_folder.mkdir(parents=True, exist_ok=False)
        qaac_folder.mkdir(parents=True, exist_ok=False)
        mpv_player_folder.mkdir(parents=True, exist_ok=False)
        fdkaac_folder.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        pass

# -------------------------------------------------------------------------------------------------------- Folder Check