# Imports--------------------------------------------------------------------
from tkinter import *
from tkinter import filedialog, StringVar
from tkinter import ttk
import subprocess
import tkinter as tk
import pathlib
import tkinter.scrolledtext as scrolledtextwidget
from TkinterDnD2 import *
from tkinter import messagebox
from urllib.error import URLError
from urllib.request import urlretrieve
from time import sleep
import threading
import shutil
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
from Packages.AppAutoDownloadLinks import *
from Packages.DirectoryCheck import directory_check
from Packages.YoutubeDLGui import youtube_dl_launcher_for_ffmpegaudioencoder
from Packages.FFMPEGAudioEncoderBatch import batch_processing
from Packages.About import openaboutwindow
from configparser import ConfigParser

# Main Gui & Windows --------------------------------------------------------
def root_exit_function():
    confirm_exit = messagebox.askyesno(title='Prompt', message="Are you sure you want to exit the program?\n\n"
                                                               "     Note: This will end all current tasks!",
                                       parent=root)
    if confirm_exit == False:
        pass
    elif confirm_exit == True:
        try:
            subprocess.Popen(f"TASKKILL /F /im FFMPEGAudioEncoder.exe /T", creationflags=subprocess.CREATE_NO_WINDOW)
            root.destroy()
        except:
            root.destroy()

root = TkinterDnD.Tk()
root.title("FFMPEG Audio Encoder v3.34")
root.iconphoto(True, PhotoImage(file="Runtime/Images/topbar.png"))
root.configure(background="#434547")
window_height = 220
window_width = 460
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
root.protocol('WM_DELETE_WINDOW', root_exit_function)

for n in range(4):
    root.grid_columnconfigure(n, weight=1)
for n in range(4):
    root.grid_rowconfigure(n, weight=1)

# Bundled Apps Quoted -------------------------------------------------------------------------------------------------
config_file = 'Runtime/config.ini'  # Creates (if doesn't exist) and defines location of config.ini
config = ConfigParser()
config.read(config_file)

try:  # Create config parameters
    config.add_section('ffmpeg_path')
    config.set('ffmpeg_path', 'path', '')
except:
    pass
try:
    config.add_section('mpv_player_path')
    config.set('mpv_player_path', 'path', '')
except:
    pass
try:
    config.add_section('mediainfogui_path')
    config.set('mediainfogui_path', 'path', '')
except:
    pass
try:
    config.add_section('mediainfocli_path')
    config.set('mediainfocli_path', 'path', '')
except:
    pass
try:
    config.add_section('debug_option')
    config.set('debug_option', 'option', '')
except:
    pass
try:
    with open(config_file, 'w') as configfile:
        config.write(configfile)
except:
    messagebox.showinfo(title='Error', message='Could Not Write to config.ini file, delete and try again')


ffmpeg = config['ffmpeg_path']['path']
mediainfocli = config['mediainfocli_path']['path']
mediainfo = config['mediainfogui_path']['path']
fdkaac = '"Apps/fdkaac/fdkaac.exe"'
qaac = '"Apps/qaac/qaac64.exe"'
mpv_player = config['mpv_player_path']['path']
# -------------------------------------------------------------------------------------------------------- Bundled Apps

# ------------------------------------------------------------------------------------------------------ Profile Config

config_profile_ini = 'Runtime/profiles.ini'  # Creates (if doesn't exist) and defines location of profile.ini
config_profile = ConfigParser()
config_profile.read(config_profile_ini)

# AAC settings --------------------------------------------------- # Create config parameters
if not config_profile.has_section('FFMPEG AAC - SETTINGS'):
    config_profile.add_section('FFMPEG AAC - SETTINGS')
if not config_profile.has_option('FFMPEG AAC - SETTINGS', 'dolbyprologicii'):
    config_profile.set('FFMPEG AAC - SETTINGS', 'dolbyprologicii', '')
if not config_profile.has_option('FFMPEG AAC - SETTINGS', 'ffmpeg_gain'):
    config_profile.set('FFMPEG AAC - SETTINGS', 'ffmpeg_gain', '0')
if not config_profile.has_option('FFMPEG AAC - SETTINGS', 'aac_bitrate'):
    config_profile.set('FFMPEG AAC - SETTINGS', 'aac_bitrate', '192')
if not config_profile.has_option('FFMPEG AAC - SETTINGS', 'aac_vbr_quality'):
    config_profile.set('FFMPEG AAC - SETTINGS', 'aac_vbr_quality', '2')
if not config_profile.has_option('FFMPEG AAC - SETTINGS', 'aac_vbr_toggle'):
    config_profile.set('FFMPEG AAC - SETTINGS', 'aac_vbr_toggle', '-c:a')
if not config_profile.has_option('FFMPEG AAC - SETTINGS', 'aac_channel'):
    config_profile.set('FFMPEG AAC - SETTINGS', 'aac_channel', 'Original')
if not config_profile.has_option('FFMPEG AAC - SETTINGS', 'samplerate'):
    config_profile.set('FFMPEG AAC - SETTINGS', 'samplerate', 'Original')
if not config_profile.has_option('FFMPEG AAC - SETTINGS', 'tempo'):
    config_profile.set('FFMPEG AAC - SETTINGS', 'tempo', 'Original')
# --------------------------------------------------- AAC Settings
# AC3 settings --------------------------------------------------- # Create config parameters
if not config_profile.has_section('FFMPEG AC3 - SETTINGS'):
    config_profile.add_section('FFMPEG AC3 - SETTINGS')
if not config_profile.has_option('FFMPEG AC3 - SETTINGS', 'ac3_bitrate'):
    config_profile.set('FFMPEG AC3 - SETTINGS', 'ac3_bitrate', '224k')
if not config_profile.has_option('FFMPEG AC3 - SETTINGS', 'dolbyprologicii'):
    config_profile.set('FFMPEG AC3 - SETTINGS', 'dolbyprologicii', '')
if not config_profile.has_option('FFMPEG AC3 - SETTINGS', 'ffmpeg_gain'):
    config_profile.set('FFMPEG AC3 - SETTINGS', 'ffmpeg_gain', '0')
if not config_profile.has_option('FFMPEG AC3 - SETTINGS', 'ac3_channel'):
    config_profile.set('FFMPEG AC3 - SETTINGS', 'ac3_channel', 'Original')
if not config_profile.has_option('FFMPEG AC3 - SETTINGS', 'samplerate'):
    config_profile.set('FFMPEG AC3 - SETTINGS', 'samplerate', 'Original')
if not config_profile.has_option('FFMPEG AC3 - SETTINGS', 'tempo'):
    config_profile.set('FFMPEG AC3 - SETTINGS', 'tempo', 'Original')
# --------------------------------------------------- AC3 Settings
# DTS settings --------------------------------------------------- # Create config parameters
if not config_profile.has_section('FFMPEG DTS - SETTINGS'):
    config_profile.add_section('FFMPEG DTS - SETTINGS')
if not config_profile.has_option('FFMPEG DTS - SETTINGS', 'dts_bitrate'):
    config_profile.set('FFMPEG DTS - SETTINGS', 'dts_bitrate', '448')
if not config_profile.has_option('FFMPEG DTS - SETTINGS', 'dolbyprologicii'):
    config_profile.set('FFMPEG DTS - SETTINGS', 'dolbyprologicii', '')
if not config_profile.has_option('FFMPEG DTS - SETTINGS', 'ffmpeg_gain'):
    config_profile.set('FFMPEG DTS - SETTINGS', 'ffmpeg_gain', '0')
if not config_profile.has_option('FFMPEG DTS - SETTINGS', 'dts_channel'):
    config_profile.set('FFMPEG DTS - SETTINGS', 'dts_channel', 'Original')
if not config_profile.has_option('FFMPEG DTS - SETTINGS', 'samplerate'):
    config_profile.set('FFMPEG DTS - SETTINGS', 'samplerate', 'Original')
if not config_profile.has_option('FFMPEG DTS - SETTINGS', 'tempo'):
    config_profile.set('FFMPEG DTS - SETTINGS', 'tempo', 'Original')
# --------------------------------------------------- DTS Settings
# E-AC3 settings --------------------------------------------------- # Create config parameters
if not config_profile.has_section('FFMPEG E-AC3 - SETTINGS'):
    config_profile.add_section('FFMPEG E-AC3 - SETTINGS')
if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_bitrate'):
    config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_bitrate', '448k')
if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_channel'):
    config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_channel', 'Original')
if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_gain'):
    config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_gain', '0')
if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'samplerate'):
    config_profile.set('FFMPEG E-AC3 - SETTINGS', 'samplerate', 'Original')
if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_per_frame_metadata'):
    config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_per_frame_metadata', 'Default')
if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_mixing_level'):
    config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_mixing_level', '-1')
if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_room_type'):
    config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_room_type', 'Default')
if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_copyright_bit'):
    config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_copyright_bit', '-1')
if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_dialogue_level'):
    config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_dialogue_level', '-31')
if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_surround_mode'):
    config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_surround_mode', 'Default')
if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_original_bitstream'):
    config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_original_bitstream', '-1')
if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_downmix_mode'):
    config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_downmix_mode', 'Default')
if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_lt_rt_center_mix'):
    config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_lt_rt_center_mix', '-1')
if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_lt_rt_surround_mix'):
    config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_lt_rt_surround_mix', '-1')
if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_lo_ro_center_mix'):
    config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_lo_ro_center_mix', '-1')
if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_lo_ro_surround_mix'):
    config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_lo_ro_surround_mix', '-1')
if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_dolby_surround_ex_mode'):
    config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_dolby_surround_ex_mode', 'Default')
if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_dolby_headphone_mode'):
    config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_dolby_headphone_mode', 'Default')
if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_a_d_converter_type'):
    config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_a_d_converter_type', 'Default')
if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_stereo_rematrixing'):
    config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_dolby_stereo_rematrixing', 'Default')
if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_channel_coupling'):
    config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_channel_coupling', '-1')
if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'e-ac3_cpl_start_band'):
    config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_cpl_start_band', '-1')
if not config_profile.has_option('FFMPEG E-AC3 - SETTINGS', 'tempo'):
    config_profile.set('FFMPEG E-AC3 - SETTINGS', 'tempo', 'Original')
# --------------------------------------------------- E-AC3 Settings
# Opus settings --------------------------------------------------- # Create config parameters
if not config_profile.has_section('FFMPEG Opus - SETTINGS'):
    config_profile.add_section('FFMPEG Opus - SETTINGS')
if not config_profile.has_option('FFMPEG Opus - SETTINGS', 'opus_bitrate'):
    config_profile.set('FFMPEG Opus - SETTINGS', 'opus_bitrate', '160k')
if not config_profile.has_option('FFMPEG Opus - SETTINGS', 'samplerate'):
    config_profile.set('FFMPEG Opus - SETTINGS', 'samplerate', 'Original')
if not config_profile.has_option('FFMPEG Opus - SETTINGS', 'acodec_vbr'):
    config_profile.set('FFMPEG Opus - SETTINGS', 'acodec_vbr', 'VBR: On')
if not config_profile.has_option('FFMPEG Opus - SETTINGS', 'acodec_application'):
    config_profile.set('FFMPEG Opus - SETTINGS', 'acodec_application', 'Audio')
if not config_profile.has_option('FFMPEG Opus - SETTINGS', 'frame_duration'):
    config_profile.set('FFMPEG Opus - SETTINGS', 'frame_duration', '20')
if not config_profile.has_option('FFMPEG Opus - SETTINGS', 'packet_loss'):
    config_profile.set('FFMPEG Opus - SETTINGS', 'packet_loss', '0')
if not config_profile.has_option('FFMPEG Opus - SETTINGS', 'acodec_channel'):
    config_profile.set('FFMPEG Opus - SETTINGS', 'acodec_channel', '2 (Stereo)')
if not config_profile.has_option('FFMPEG Opus - SETTINGS', 'dolbyprologicii'):
    config_profile.set('FFMPEG Opus - SETTINGS', 'dolbyprologicii', '')
if not config_profile.has_option('FFMPEG Opus - SETTINGS', 'ffmpeg_gain'):
    config_profile.set('FFMPEG Opus - SETTINGS', 'ffmpeg_gain', '0')
if not config_profile.has_option('FFMPEG Opus - SETTINGS', 'tempo'):
    config_profile.set('FFMPEG Opus - SETTINGS', 'tempo', 'Original')
# --------------------------------------------------- Opus Settings
# FDK-AAC settings --------------------------------------------------- # Create config parameters
if not config_profile.has_section('FDK-AAC - SETTINGS'):
    config_profile.add_section('FDK-AAC - SETTINGS')
if not config_profile.has_option('FDK-AAC - SETTINGS', 'fdk_aac_bitrate'):
    config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_bitrate', 'CBR: 192k')
if not config_profile.has_option('FDK-AAC - SETTINGS', 'acodec_channel'):
    config_profile.set('FDK-AAC - SETTINGS', 'acodec_channel', 'Original')
if not config_profile.has_option('FDK-AAC - SETTINGS', 'dolbyprologicii'):
    config_profile.set('FDK-AAC - SETTINGS', 'dolbyprologicii', '')
if not config_profile.has_option('FDK-AAC - SETTINGS', 'ffmpeg_gain'):
    config_profile.set('FDK-AAC - SETTINGS', 'ffmpeg_gain', '0')
if not config_profile.has_option('FDK-AAC - SETTINGS', 'samplerate'):
    config_profile.set('FDK-AAC - SETTINGS', 'samplerate', 'Original')
if not config_profile.has_option('FDK-AAC - SETTINGS', 'fdk_aac_profile'):
    config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_profile', 'AAC LC (Default)')
if not config_profile.has_option('FDK-AAC - SETTINGS', 'fdk_aac_lowdelay'):
    config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_lowdelay', 'Disable SBR on ELD (DEF)')
if not config_profile.has_option('FDK-AAC - SETTINGS', 'fdk_aac_sbr_ratio'):
    config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_sbr_ratio', 'Library Default')
if not config_profile.has_option('FDK-AAC - SETTINGS', 'fdk_aac_gapless'):
    config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_gapless', 'iTunSMPB (Def)')
if not config_profile.has_option('FDK-AAC - SETTINGS', 'fdk_aac_transport_format'):
    config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_transport_format', 'M4A (Def)')
if not config_profile.has_option('FDK-AAC - SETTINGS', 'fdk_aac_afterburner'):
    config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_afterburner', '-a1')
if not config_profile.has_option('FDK-AAC - SETTINGS', 'fdk_aac_crccheck'):
    config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_crccheck', '')
if not config_profile.has_option('FDK-AAC - SETTINGS', 'fdk_aac_headerperiod'):
    config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_headerperiod', '')
if not config_profile.has_option('FDK-AAC - SETTINGS', 'fdk_aac_sbrdelay'):
    config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_sbrdelay', '')
if not config_profile.has_option('FDK-AAC - SETTINGS', 'fdk_aac_moovbox'):
    config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_moovbox', '')
if not config_profile.has_option('FDK-AAC - SETTINGS', 'fdk_aac_tempo'):
    config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_tempo', 'Original')
# --------------------------------------------------- FDK-AAC Settings
# MP3 settings --------------------------------------------------- # Create config parameters
if not config_profile.has_section('FFMPEG MP3 - SETTINGS'):
    config_profile.add_section('FFMPEG MP3 - SETTINGS')
if not config_profile.has_option('FFMPEG MP3 - SETTINGS', 'acodec_bitrate'):
    config_profile.set('FFMPEG MP3 - SETTINGS', 'acodec_bitrate', 'VBR: -V 0')
if not config_profile.has_option('FFMPEG MP3 - SETTINGS', 'acodec_channel'):
    config_profile.set('FFMPEG MP3 - SETTINGS', 'acodec_channel', 'Original')
if not config_profile.has_option('FFMPEG MP3 - SETTINGS', 'mp3_vbr'):
    config_profile.set('FFMPEG MP3 - SETTINGS', 'mp3_vbr', '-q:a')
if not config_profile.has_option('FFMPEG MP3 - SETTINGS', 'mp3_abr'):
    config_profile.set('FFMPEG MP3 - SETTINGS', 'mp3_abr', '')
if not config_profile.has_option('FFMPEG MP3 - SETTINGS', 'dolbyprologicii'):
    config_profile.set('FFMPEG MP3 - SETTINGS', 'dolbyprologicii', '')
if not config_profile.has_option('FFMPEG MP3 - SETTINGS', 'ffmpeg_gain'):
    config_profile.set('FFMPEG MP3 - SETTINGS', 'ffmpeg_gain', '0')
if not config_profile.has_option('FFMPEG MP3 - SETTINGS', 'samplerate'):
    config_profile.set('FFMPEG MP3 - SETTINGS', 'samplerate', 'Original')
if not config_profile.has_option('FFMPEG MP3 - SETTINGS', 'tempo'):
    config_profile.set('FFMPEG MP3 - SETTINGS', 'tempo', 'Original')
if not config_profile.has_option('FFMPEG MP3 - SETTINGS', 'acodec_bitrate_vbr'):
    config_profile.set('FFMPEG MP3 - SETTINGS', 'acodec_bitrate_vbr', '')
if not config_profile.has_option('FFMPEG MP3 - SETTINGS', 'acodec_bitrate_cbr_abr'):
    config_profile.set('FFMPEG MP3 - SETTINGS', 'acodec_bitrate_cbr_abr', '')
# --------------------------------------------------- MP3 Settings
# QAAC settings --------------------------------------------------- # Create config parameters
if not config_profile.has_section('FFMPEG QAAC - SETTINGS'):
    config_profile.add_section('FFMPEG QAAC - SETTINGS')
if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'q_acodec_profile'):
    config_profile.set('FFMPEG QAAC - SETTINGS', 'q_acodec_profile', 'True VBR')
if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'dolbyprologicii'):
    config_profile.set('FFMPEG QAAC - SETTINGS', 'dolbyprologicii', '')
if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'acodec_channel'):
    config_profile.set('FFMPEG QAAC - SETTINGS', 'acodec_channel', 'Original')
if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'samplerate'):
    config_profile.set('FFMPEG QAAC - SETTINGS', 'samplerate', 'Original')
if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'q_acodec_quality'):
    config_profile.set('FFMPEG QAAC - SETTINGS', 'q_acodec_quality', 'High (Default)')
if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'q_acodec_quality_amnt'):
    config_profile.set('FFMPEG QAAC - SETTINGS', 'q_acodec_quality_amnt', '109')
if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'q_acodec_bitrate'):
    config_profile.set('FFMPEG QAAC - SETTINGS', 'q_acodec_bitrate', '256')
if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'q_acodec_gain'):
    config_profile.set('FFMPEG QAAC - SETTINGS', 'q_acodec_gain', '0')
if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'qaac_normalize'):
    config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_normalize', '')
if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'qaac_high_efficiency'):
    config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_high_efficiency', '')
if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'qaac_nodither'):
    config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_nodither', '')
if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'qaac_nodelay'):
    config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_nodelay', '')
if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'q_gapless_mode'):
    config_profile.set('FFMPEG QAAC - SETTINGS', 'q_gapless_mode', 'iTunSMPB (Default)')
if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'qaac_nooptimize'):
    config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_nooptimize', '')
if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'qaac_threading'):
    config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_threading', '')
if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'qaac_limiter'):
    config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_limiter', '')
if not config_profile.has_option('FFMPEG QAAC - SETTINGS', 'tempo'):
    config_profile.set('FFMPEG QAAC - SETTINGS', 'tempo', 'Original')
# --------------------------------------------------- QAAC Settings
# FLAC settings --------------------------------------------------- # Create config parameters
if not config_profile.has_section('FFMPEG FLAC - SETTINGS'):
    config_profile.add_section('FFMPEG FLAC - SETTINGS')
if not config_profile.has_option('FFMPEG FLAC - SETTINGS', 'acodec_bitrate'):
    config_profile.set('FFMPEG FLAC - SETTINGS', 'acodec_bitrate', 'Level 5 - Default Quality')
if not config_profile.has_option('FFMPEG FLAC - SETTINGS', 'acodec_channel'):
    config_profile.set('FFMPEG FLAC - SETTINGS', 'acodec_channel', 'Original')
if not config_profile.has_option('FFMPEG FLAC - SETTINGS', 'dolbyprologicii'):
    config_profile.set('FFMPEG FLAC - SETTINGS', 'dolbyprologicii', '')
if not config_profile.has_option('FFMPEG FLAC - SETTINGS', 'gain'):
    config_profile.set('FFMPEG FLAC - SETTINGS', 'gain', '0')
if not config_profile.has_option('FFMPEG FLAC - SETTINGS', 'samplerate'):
    config_profile.set('FFMPEG FLAC - SETTINGS', 'samplerate', 'Original')
if not config_profile.has_option('FFMPEG FLAC - SETTINGS', 'tempo'):
    config_profile.set('FFMPEG FLAC - SETTINGS', 'tempo', 'Original')
if not config_profile.has_option('FFMPEG FLAC - SETTINGS', 'flac_lpc_type'):
    config_profile.set('FFMPEG FLAC - SETTINGS', 'flac_lpc_type', 'Default')
if not config_profile.has_option('FFMPEG FLAC - SETTINGS', 'flac_coefficient'):
    config_profile.set('FFMPEG FLAC - SETTINGS', 'flac_coefficient', '15')
if not config_profile.has_option('FFMPEG FLAC - SETTINGS', 'flac_lpc_passes'):
    config_profile.set('FFMPEG FLAC - SETTINGS', 'flac_lpc_passes', 'Default')
# --------------------------------------------------- FLAC Settings
# ALAC settings --------------------------------------------------- # Create config parameters
if not config_profile.has_section('FFMPEG ALAC - SETTINGS'):
    config_profile.add_section('FFMPEG ALAC - SETTINGS')
if not config_profile.has_option('FFMPEG ALAC - SETTINGS', 'acodec_channel'):
    config_profile.set('FFMPEG ALAC - SETTINGS', 'acodec_channel', 'Original')
if not config_profile.has_option('FFMPEG ALAC - SETTINGS', 'dolbyprologicii'):
    config_profile.set('FFMPEG ALAC - SETTINGS', 'dolbyprologicii', '')
if not config_profile.has_option('FFMPEG ALAC - SETTINGS', 'gain'):
    config_profile.set('FFMPEG ALAC - SETTINGS', 'gain', '0')
if not config_profile.has_option('FFMPEG ALAC - SETTINGS', 'samplerate'):
    config_profile.set('FFMPEG ALAC - SETTINGS', 'samplerate', 'Original')
if not config_profile.has_option('FFMPEG ALAC - SETTINGS', 'tempo'):
    config_profile.set('FFMPEG ALAC - SETTINGS', 'tempo', 'Original')
if not config_profile.has_option('FFMPEG ALAC - SETTINGS', 'alac_min_prediction_order'):
    config_profile.set('FFMPEG ALAC - SETTINGS', 'alac_min_prediction_order', '4')
if not config_profile.has_option('FFMPEG ALAC - SETTINGS', 'alac_max_prediction_order'):
    config_profile.set('FFMPEG ALAC - SETTINGS', 'alac_max_prediction_order', '6')
# --------------------------------------------------- ALAC Settings
# Auto Encode Last Used Options ------------------------------------ # Create config parameters
if not config_profile.has_section('Auto Encode'):
    config_profile.add_section('Auto Encode')
if not config_profile.has_option('Auto Encode', 'codec'):
    config_profile.set('Auto Encode', 'codec', '')
if not config_profile.has_option('Auto Encode', 'command'):
    config_profile.set('Auto Encode', 'command', '')
# ------------------------------------- Auto Encode Last Used Options
try:
    with open(config_profile_ini, 'w') as configfile_two:
        config_profile.write(configfile_two)
except:
    messagebox.showinfo(title='Error', message='Could Not Write to profiles.ini file, delete and try again')

# Profile Config ------------------------------------------------------------------------------------------------------

# Open InputFile with portable MediaInfo ------------------------------------------------------------------------------
def mediainfogui():
    try:
        VideoInputQuoted = '"' + VideoInput + '"'
        commands = mediainfo + " " + VideoInputQuoted
        subprocess.Popen(commands)
    except:
        commands = mediainfo
        subprocess.Popen(commands)


# ----------------------------------------------------------------------------------------------------------- MediaInfo

# Open InputFile with portable mpv ------------------------------------------------------------------------------------
def mpv_gui_main_gui():
    try:
        VideoInputQuoted = '"' + VideoInput + '"'
        commands = mpv_player + " " + VideoInputQuoted
        subprocess.Popen(commands)
    except:
        commands = mpv_player
        subprocess.Popen(commands)

# ----------------------------------------------------------------------------------------------------------------- mpv

# Menu Items and Sub-Bars ---------------------------------------------------------------------------------------------
my_menu_bar = Menu(root, tearoff=0)
root.config(menu=my_menu_bar)

file_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
my_menu_bar.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Exit', command=root_exit_function)

options_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
my_menu_bar.add_cascade(label='Options', menu=options_menu)

options_submenu = Menu(root, tearoff=0, activebackground='dim grey')
options_menu.add_cascade(label='Shell Options', menu=options_submenu)
shell_options = StringVar()
shell_options.set(config['debug_option']['option'])
if shell_options.get() == '':
    shell_options.set('Default')
elif shell_options.get() != '':
    shell_options.set(config['debug_option']['option'])
def update_shell_option():
    try:
        config.set('debug_option', 'option', shell_options.get())
        with open(config_file, 'w') as configfile:
            config.write(configfile)
    except:
        pass
update_shell_option()
options_submenu.add_radiobutton(label='Shell Closes Automatically', variable=shell_options,
                                value="Default", command=update_shell_option)
options_submenu.add_radiobutton(label='Shell Stays Open (Debug)', variable=shell_options,
                                value="Debug", command=update_shell_option)

options_menu.add_separator()

def set_ffmpeg_path():
    global ffmpeg
    path = filedialog.askopenfilename(title='Select Location to "ffmpeg.exe"', initialdir='/',
                                      filetypes=[('ffmpeg', 'ffmpeg.exe')])
    if path == '':
        pass
    elif path != '':
        ffmpeg = '"' + str(pathlib.Path(path)) + '"'
        config.set('ffmpeg_path', 'path', ffmpeg)
        with open(config_file, 'w') as configfile:
            config.write(configfile)

options_menu.add_command(label='Set path to FFMPEG', command=set_ffmpeg_path)

def set_mpv_player_path():
    global mpv_player
    path = filedialog.askopenfilename(title='Select Location to "mpv.exe"', initialdir='/',
                                      filetypes=[('mpv', 'mpv.exe')])
    if path == '':
        pass
    elif path != '':
        mpv_player = '"' + str(pathlib.Path(path)) + '"'
        config.set('mpv_player_path', 'path', mpv_player)
        with open(config_file, 'w') as configfile:
            config.write(configfile)

options_menu.add_command(label='Set path to MPV player', command=set_mpv_player_path)

def set_mediainfogui_path():
    global mediainfo
    path = filedialog.askopenfilename(title='Select Location to "MediaInfo.exe"', initialdir='/',
                                      filetypes=[('MediaInfoGUI', 'MediaInfo.exe')])
    if path == '':
        pass
    elif path != '':
        mediainfo = '"' + str(pathlib.Path(path)) + '"'
        config.set('mediainfogui_path', 'path', mediainfo)
        with open(config_file, 'w') as configfile:
            config.write(configfile)

options_menu.add_command(label='Set path to MediaInfo - GUI', command=set_mediainfogui_path)

def set_mediainfocli_path():
    global mediainfocli
    path = filedialog.askopenfilename(title='Select Location to "MediaInfo.exe"', initialdir='/',
                                      filetypes=[('MediaInfo', 'MediaInfo.exe')])
    if path == '':
        pass
    elif path != '':
        mediainfocli = '"' + str(pathlib.Path(path)) + '"'
        config.set('mediainfocli_path', 'path', mediainfocli)
        with open(config_file, 'w') as configfile:
            config.write(configfile)

options_menu.add_command(label='Set path to MediaInfo - CLI', command=set_mediainfocli_path)

options_menu.add_separator()
def reset_config():
    msg = messagebox.askyesno(title='Warning', message='Are you sure you want to reset the config.ini file settings?')
    if msg == False:
       pass
    if msg == True:
        try:
            config.set('ffmpeg_path', 'path', '')
            config.set('mpv_player_path', 'path', '')
            config.set('mediainfocli_path', 'path', '')
            config.set('mediainfogui_path', 'path', '')
            with open(config_file, 'w') as configfile:
                config.write(configfile)
            messagebox.showinfo(title='Prompt', message='Please restart the program')
        except:
            pass
        root.destroy()

options_menu.add_command(label='Reset Configuration File', command=reset_config)

tools_submenu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
my_menu_bar.add_cascade(label='Tools', menu=tools_submenu)
tools_submenu.add_command(label="MediaInfo", command=mediainfogui)
tools_submenu.add_command(label="MPV (Media Player)", command=mpv_gui_main_gui)
tools_submenu.add_command(label="Youtube-DL-Gui", command=youtube_dl_launcher_for_ffmpegaudioencoder)
tools_submenu.add_separator()

def batch_processing_command():
    batch_processing()
    root.wm_state("iconic")  # Minimizes main window while it opens batch_processing window

tools_submenu.add_command(label='Batch Processing', command=batch_processing_command)

help_menu = Menu(my_menu_bar, tearoff=0, activebackground="dim grey")
my_menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=openaboutwindow)


# --------------------------------------------------------------------------------------------- Menu Items and Sub-Bars

# File Auto Save Function ---------------------------------------------------------------------------------------------
def encoder_changed(*args):
    global VideoOutput
    global autosavefilename
    if encoder.get() == "Set Codec":
        pass
    else:
        filename = pathlib.Path(VideoInput)
        if encoder.get() == 'AAC':
            VideoOut = filename.with_suffix('.NEW.mp4')
        elif encoder.get() == 'AC3' or encoder.get() == 'E-AC3':
            VideoOut = filename.with_suffix('.NEW.ac3')
        elif encoder.get() == "DTS":
            VideoOut = filename.with_suffix('.NEW.dts')
        elif encoder.get() == "Opus":
            VideoOut = filename.with_suffix('.NEW.opus')
        elif encoder.get() == 'MP3':
            VideoOut = filename.with_suffix('.NEW.mp3')
        elif encoder.get() == "FDK-AAC" or encoder.get() == "QAAC" or encoder.get() == "ALAC":
            VideoOut = filename.with_suffix('.NEW.m4a')
        elif encoder.get() == "FLAC":
            VideoOut = filename.with_suffix('.NEW.flac')
        VideoOutput = str(VideoOut)
        output_entry.configure(state=NORMAL)
        output_entry.delete(0, END)
        output_entry.insert(0, VideoOut)
        output_entry.configure(state=DISABLED)
        audiosettings_button.configure(state=NORMAL)
        command_line_button.config(state=DISABLED)
        start_audio_button.config(state=DISABLED)
        auto_encode_last_options.configure(state=DISABLED)
        autosavefilename = VideoOut.name


# --------------------------------------------------------------------------------------------- File Auto Save Function

# Uses MediaInfo CLI to get total audio track count and gives us a total track count ----------------------------------
def track_count(*args):  # Thanks for helping me shorten this 'gmes78'
    global acodec_stream_track_counter, t_info
    mediainfocli_cmd_info = '"' + mediainfocli + " " + '--Output="Audio;' \
                            + " |  %Format%  |  %Channel(s)% Channels  |  %BitRate/String% ," \
                            + '"' + " " + VideoInputQuoted + '"'
    mediainfo_count = subprocess.Popen('cmd /c ' + mediainfocli_cmd_info, creationflags=subprocess.CREATE_NO_WINDOW,
                                       universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       stdin=subprocess.PIPE)
    stdout, stderr = mediainfo_count.communicate()
    t_info = stdout.split(',')[:-1]
    acodec_stream_track_counter = {}
    for i in range(int(str.split(track_count)[-1])):
        acodec_stream_track_counter[f'Track #{i + 1} {t_info[i]}'] = f' -map 0:a:{i} '

# ---------------------------------------------------------------------------------------------------------------------

# Encoder Codec Drop Down ---------------------------------------------------------------------------------------------
encoder_dropdownmenu_choices = {
    "AAC": "-c:a aac ",
    "AC3": "-c:a ac3 ",
    "E-AC3": "-c:a eac3 ",
    "DTS": "-c:a dts ",
    "Opus": "-c:a libopus ",
    "MP3": "-c:a libmp3lame ",
    "FDK-AAC": fdkaac,
    "QAAC": qaac,
    "FLAC": '-c:a flac ',
    "ALAC": '-c:a alac '}
encoder = StringVar(root)
encoder.set("Set Codec")
encoder.trace('w', encoder_changed)
encoder_menu = OptionMenu(root, encoder, *encoder_dropdownmenu_choices.keys(), command=track_count)
encoder_menu.grid(row=1, column=2, columnspan=1, padx=5, pady=5, sticky=N + S + W + E)
encoder_menu.config(state=DISABLED, background="#23272A", foreground="white", highlightthickness=1, width=10)
encoder_menu["menu"].configure(activebackground="dim grey")
codec_label = Label(root, text="Codec ->", background="#434547", foreground="White")
codec_label.grid(row=1, column=1, columnspan=1, padx=5, pady=5, sticky=N + S + W + E)


# -------------------------------------------------------------------------------------------------------- Encoder Menu

# Audio Codec Window --------------------------------------------------------------------------------------------------
def openaudiowindow():
    global acodec_bitrate, acodec_channel, acodec_channel_choices, acodec_bitrate_choices, acodec_stream, \
    acodec_stream_choices, acodec_gain, acodec_gain_choices, dts_settings, dts_settings_choices, \
    acodec_vbr_choices, acodec_vbr, acodec_samplerate, acodec_samplerate_choices, acodec_application, \
    acodec_application_choices, acodec_profile, acodec_profile_choices, acodec_atempo, acodec_atempo_choices

    def apply_button_hover(e):
        apply_button["bg"] = "grey"

    def apply_button_hover_leave(e):
        apply_button["bg"] = "#23272a"

    def show_cmd_hover(e):
        show_cmd["bg"] = "grey"

    def show_cmd_hover_leave(e):
        show_cmd["bg"] = "#23272A"

    def acodec_bitrate_menu_hover(e):
        acodec_bitrate_menu["bg"] = "grey"
        acodec_bitrate_menu["activebackground"] = "grey"

    def acodec_bitrate_menu_hover_leave(e):
        acodec_bitrate_menu["bg"] = "#23272A"

    def acodec_stream_menu_hover(e):
        acodec_stream_menu["bg"] = "grey"
        acodec_stream_menu["activebackground"] = "grey"

    def acodec_stream_menu_hover_leave(e):
        acodec_stream_menu["bg"] = "#23272A"

    def achannel_menu_hover(e):
        achannel_menu["bg"] = "grey"
        achannel_menu["activebackground"] = "grey"

    def achannel_menu_hover_leave(e):
        achannel_menu["bg"] = "#23272A"

    def acodec_samplerate_menu_hover(e):
        acodec_samplerate_menu["bg"] = "grey"
        acodec_samplerate_menu["activebackground"] = "grey"

    def acodec_samplerate_menu_hover_leave(e):
        acodec_samplerate_menu["bg"] = "#23272A"

    def dts_settings_menu_hover(e):
        dts_settings_menu["bg"] = "grey"
        dts_settings_menu["activebackground"] = "grey"

    def dts_settings_menu_hover_leave(e):
        dts_settings_menu["bg"] = "#23272A"

    def acodec_vbr_menu_hover(e):
        acodec_vbr_menu["bg"] = "grey"
        acodec_vbr_menu["activebackground"] = "grey"

    def acodec_vbr_menu_hover_leave(e):
        acodec_vbr_menu["bg"] = "#23272A"

    def acodec_application_menu_hover(e):
        acodec_application_menu["bg"] = "grey"
        acodec_application_menu["activebackground"] = "grey"

    def acodec_application_menu_hover_leave(e):
        acodec_application_menu["bg"] = "#23272A"

    def per_frame_metadata_menu_hover(e):
        per_frame_metadata_menu["bg"] = "grey"
        per_frame_metadata_menu["activebackground"] = "grey"

    def per_frame_metadata_menu_hover_leave(e):
        per_frame_metadata_menu["bg"] = "#23272A"

    def dolby_surround_mode_menu_hover(e):
        dolby_surround_mode_menu["bg"] = "grey"
        dolby_surround_mode_menu["activebackground"] = "grey"

    def dolby_surround_mode_menu_hover_leave(e):
        dolby_surround_mode_menu["bg"] = "#23272A"

    def room_type_menu_hover(e):
        room_type_menu["bg"] = "grey"
        room_type_menu["activebackground"] = "grey"

    def room_type_menu_hover_leave(e):
        room_type_menu["bg"] = "#23272A"

    def downmix_mode_menu_hover(e):
        downmix_mode_menu["bg"] = "grey"
        downmix_mode_menu["activebackground"] = "grey"

    def downmix_mode_menu_hover_leave(e):
        downmix_mode_menu["bg"] = "#23272A"

    def dolby_surround_ex_mode_menu_hover(e):
        dolby_surround_ex_mode_menu["bg"] = "grey"
        dolby_surround_ex_mode_menu["activebackground"] = "grey"

    def dolby_surround_ex_mode_menu_hover_leave(e):
        dolby_surround_ex_mode_menu["bg"] = "#23272A"

    def dolby_headphone_mode_menu_hover(e):
        dolby_headphone_mode_menu["bg"] = "grey"
        dolby_headphone_mode_menu["activebackground"] = "grey"

    def dolby_headphone_mode_menu_hover_leave(e):
        dolby_headphone_mode_menu["bg"] = "#23272A"

    def a_d_converter_type_menu_hover(e):
        a_d_converter_type_menu["bg"] = "grey"
        a_d_converter_type_menu["activebackground"] = "grey"

    def a_d_converter_type_menu_hover_leave(e):
        a_d_converter_type_menu["bg"] = "#23272A"

    def stereo_rematrixing_menu_hover(e):
        stereo_rematrixing_menu["bg"] = "grey"
        stereo_rematrixing_menu["activebackground"] = "grey"

    def stereo_rematrixing_menu_hover_leave(e):
        stereo_rematrixing_menu["bg"] = "#23272A"

    def q_acodec_profile_hover(e):
        q_acodec_profile_menu["bg"] = "grey"
        q_acodec_profile_menu["activebackground"] = "grey"

    def q_acodec_profile_hover_leave(e):
        q_acodec_profile_menu["bg"] = "#23272A"

    def q_acodec_quality_menu_hover(e):
        q_acodec_quality_menu["bg"] = "grey"
        q_acodec_quality_menu["activebackground"] = "grey"

    def q_acodec_quality_menu_hover_leave(e):
        q_acodec_quality_menu["bg"] = "#23272A"

    def help_button_hover(e):
        help_button["bg"] = "grey"
        help_button["activebackground"] = "grey"

    def help_button_hover_leave(e):
        help_button["bg"] = "#23272A"

    def q_gapless_mode_menu_hover(e):
        q_gapless_mode_menu["bg"] = "grey"
        q_gapless_mode_menu["activebackground"] = "grey"

    def q_gapless_mode_menu_hover_leave(e):
        q_gapless_mode_menu["bg"] = "#23272A"

    def acodec_atempo_menu_hover(e):
        acodec_atempo_menu["bg"] = "grey"
        acodec_atempo_menu["activebackground"] = "grey"

    def acodec_atempo_menu_hover_leave(e):
        acodec_atempo_menu["bg"] = "#23272A"

    def acodec_flac_lpc_type_menu_hover(e):
        acodec_flac_lpc_type_menu["bg"] = "grey"
        acodec_flac_lpc_type_menu["activebackground"] = "grey"

    def acodec_flac_lpc_type_menu_hover_leave(e):
        acodec_flac_lpc_type_menu["bg"] = "#23272A"

    def acodec_flac_lpc_passes_menu_hover(e):
        acodec_flac_lpc_passes_menu["bg"] = "grey"
        acodec_flac_lpc_passes_menu["activebackground"] = "grey"

    def acodec_flac_lpc_passes_menu_hover_leave(e):
        acodec_flac_lpc_passes_menu["bg"] = "#23272A"

    # Checks channel for dolby pro logic II checkbox ------------------------------------------------------------------
    def dolby_pro_logic_ii_enable_disable(*args):
        if acodec_channel.get() == '2 (Stereo)':
            dolby_pro_logic_ii_checkbox.config(state=NORMAL)
        else:
            dolby_pro_logic_ii.set("")
            dolby_pro_logic_ii_checkbox.config(state=DISABLED)

    # --------------------------------------------------------------------------------------------- dplII channel check

    # Get Selected Track Number for MPV Player ------------------------------------------------------------------------
    def track_number_mpv(*args):
        global mpv_track_number
        mpv_track_number = str(acodec_stream.get().split()[1][-1])

    # ------------------------------------------------------------------------ Get Selected Track Number for MPV Player

    # Open InputFile Track X with portable mpv ------------------------------------------------------------------------
    def mpv_gui_audio_window():
        VideoInputQuoted = '"' + VideoInput + '"'
        commands = mpv_player + ' ' + '--volume=50 ' + '--aid=' + mpv_track_number[0] + ' ' + VideoInputQuoted
        subprocess.Popen(commands)

    # ------------------------------------------------------------------------------------------------------------- mpv

    # Combines -af filter settings ------------------------------------------------------------------------------------
    global audio_filter_function
    def audio_filter_function(*args):
        global audio_filter_setting
        audio_filter_setting = ''
        if encoder.get() == "QAAC":
            if dolby_pro_logic_ii.get() == '' and acodec_atempo_choices[acodec_atempo.get()] == '':
                audio_filter_setting = ''
            elif dolby_pro_logic_ii.get() != '' and acodec_atempo_choices[acodec_atempo.get()] == '':
                audio_filter_setting = '-af ' + dolby_pro_logic_ii.get() + ' '
            elif dolby_pro_logic_ii.get() != '' and acodec_atempo_choices[acodec_atempo.get()] != '':
                audio_filter_setting = '-af ' + dolby_pro_logic_ii.get() + ',' + \
                                       acodec_atempo_choices[acodec_atempo.get()] + ' '
            elif dolby_pro_logic_ii.get() == '' and acodec_atempo_choices[acodec_atempo.get()] != '':
                audio_filter_setting = '-af ' + acodec_atempo_choices[acodec_atempo.get()] + ' '
        elif encoder.get() == 'E-AC3':
            ffmpeg_gain_cmd = '"volume=' + ffmpeg_gain.get() + 'dB"'
            if ffmpeg_gain.get() == '0' and acodec_atempo_choices[acodec_atempo.get()] == '':
                audio_filter_setting = ''
            elif ffmpeg_gain.get() != '0' and acodec_atempo_choices[acodec_atempo.get()] == '':
                audio_filter_setting = '-af ' + ffmpeg_gain_cmd + ' '
            elif ffmpeg_gain.get() == '0' and acodec_atempo_choices[acodec_atempo.get()] != '':
                audio_filter_setting = '-af ' + acodec_atempo_choices[acodec_atempo.get()] + ' '
            elif ffmpeg_gain.get() != '0' and acodec_atempo_choices[acodec_atempo.get()] != '':
                audio_filter_setting = '-af ' + ffmpeg_gain_cmd + ',' + acodec_atempo_choices[acodec_atempo.get()] + ' '
        else:
            ffmpeg_gain_cmd = '"volume=' + ffmpeg_gain.get() + 'dB"'
            if dolby_pro_logic_ii.get() == '' and ffmpeg_gain.get() == '0' and \
                    acodec_atempo_choices[acodec_atempo.get()] == '':
                audio_filter_setting = ''
            elif dolby_pro_logic_ii.get() == '"aresample=matrix_encoding=dplii"' and \
                    ffmpeg_gain.get() == '0' and acodec_atempo_choices[acodec_atempo.get()] == '':
                audio_filter_setting = '-af ' + dolby_pro_logic_ii.get() + ' '

            elif dolby_pro_logic_ii.get() == '"aresample=matrix_encoding=dplii"' \
                    and ffmpeg_gain.get() != '0' and acodec_atempo_choices[acodec_atempo.get()] == '':
                audio_filter_setting = '-af ' + dolby_pro_logic_ii.get() + ',' + \
                                       ffmpeg_gain_cmd + ' '
            elif dolby_pro_logic_ii.get() == '' and ffmpeg_gain.get() != '0' and \
                    acodec_atempo_choices[acodec_atempo.get()] == '':
                audio_filter_setting = '-af ' + ffmpeg_gain_cmd + ' '
            elif dolby_pro_logic_ii.get() == '"aresample=matrix_encoding=dplii"' and \
                    ffmpeg_gain.get() == '0' and acodec_atempo_choices[acodec_atempo.get()] != '':
                audio_filter_setting = '-af ' + dolby_pro_logic_ii.get() + ',' + \
                                       acodec_atempo_choices[acodec_atempo.get()] + ' '
            elif dolby_pro_logic_ii.get() == '"aresample=matrix_encoding=dplii"' \
                    and ffmpeg_gain.get() != '0' and acodec_atempo_choices[acodec_atempo.get()] != '':
                audio_filter_setting = '-af ' + dolby_pro_logic_ii.get() + ',' + \
                                       ffmpeg_gain_cmd + ',' + acodec_atempo_choices[acodec_atempo.get()] + ' '
            elif dolby_pro_logic_ii.get() == '' and ffmpeg_gain.get() != '0' and \
                    acodec_atempo_choices[acodec_atempo.get()] != '':
                audio_filter_setting = '-af ' + ffmpeg_gain_cmd + ',' + acodec_atempo_choices[acodec_atempo.get()] + ' '
            elif dolby_pro_logic_ii.get() == '' and \
                    ffmpeg_gain.get() == '0' and acodec_atempo_choices[acodec_atempo.get()] != '':
                audio_filter_setting = '-af ' + acodec_atempo_choices[acodec_atempo.get()] + ' '

    # ---------------------------------------------------------------------------------------------------- combines -af

    # 'Apply' button function -----------------------------------------------------------------------------------------
    def gotosavefile():
        audio_window.destroy()
        output_button.config(state=NORMAL)
        start_audio_button.config(state=NORMAL)
        command_line_button.config(state=NORMAL)
        try:
            cmd_line_window.withdraw()
        except:
            pass

    # ----------------------------------------------------------------------------------------- 'Apply' button function

    # Profile Functions -----------------------------------------------------------------------------------------------
    def save_profile():  # Function to save current settings in codec window
        if encoder.get() == 'AC3':
            config_profile.set('FFMPEG AC3 - SETTINGS', 'ac3_bitrate', acodec_bitrate.get())
            config_profile.set('FFMPEG AC3 - SETTINGS', 'dolbyprologicii', dolby_pro_logic_ii.get())
            config_profile.set('FFMPEG AC3 - SETTINGS', 'ffmpeg_gain', ffmpeg_gain.get())
            config_profile.set('FFMPEG AC3 - SETTINGS', 'ac3_channel', acodec_channel.get())
            config_profile.set('FFMPEG AC3 - SETTINGS', 'samplerate', acodec_samplerate.get())
            config_profile.set('FFMPEG AC3 - SETTINGS', 'tempo', acodec_atempo.get())
        if encoder.get() == 'AAC':
            config_profile.set('FFMPEG AAC - SETTINGS', 'dolbyprologicii', dolby_pro_logic_ii.get())
            config_profile.set('FFMPEG AAC - SETTINGS', 'ffmpeg_gain', ffmpeg_gain.get())
            if aac_vbr_toggle.get() == "-c:a ":
                config_profile.set('FFMPEG AAC - SETTINGS', 'aac_bitrate', aac_bitrate_spinbox.get())
            if aac_vbr_toggle.get() == "-q:a ":
                config_profile.set('FFMPEG AAC - SETTINGS', 'aac_vbr_quality', aac_quality_spinbox.get())
            config_profile.set('FFMPEG AAC - SETTINGS', 'aac_vbr_toggle', aac_vbr_toggle.get())
            config_profile.set('FFMPEG AAC - SETTINGS', 'aac_channel', acodec_channel.get())
            config_profile.set('FFMPEG AAC - SETTINGS', 'samplerate', acodec_samplerate.get())
            config_profile.set('FFMPEG AAC - SETTINGS', 'tempo', acodec_atempo.get())
        if encoder.get() == 'DTS' and dts_settings.get() == 'DTS Encoder':
            config_profile.set('FFMPEG DTS - SETTINGS', 'dts_bitrate', dts_bitrate_spinbox.get())
            config_profile.set('FFMPEG DTS - SETTINGS', 'dolbyprologicii', dolby_pro_logic_ii.get())
            config_profile.set('FFMPEG DTS - SETTINGS', 'ffmpeg_gain', ffmpeg_gain.get())
            config_profile.set('FFMPEG DTS - SETTINGS', 'dts_channel', acodec_channel.get())
            config_profile.set('FFMPEG DTS - SETTINGS', 'samplerate', acodec_samplerate.get())
            config_profile.set('FFMPEG DTS - SETTINGS', 'tempo', acodec_atempo.get())
        if encoder.get() == 'E-AC3':
            config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_bitrate', eac3_spinbox.get())
            config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_channel', acodec_channel.get())
            config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_gain', ffmpeg_gain.get())
            config_profile.set('FFMPEG E-AC3 - SETTINGS', 'samplerate', acodec_samplerate.get())
            config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_per_frame_metadata', per_frame_metadata.get())
            config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_mixing_level', eac3_mixing_level.get())
            config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_room_type', room_type.get())
            config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_copyright_bit', copyright_bit.get())
            config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_dialogue_level', dialogue_level.get())
            config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_surround_mode', dolby_headphone_mode.get())
            config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_original_bitstream', original_bit_stream.get())
            config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_downmix_mode', downmix_mode.get())
            config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_lt_rt_center_mix', lt_rt_center_mix.get())
            config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_lt_rt_surround_mix', lt_rt_surround_mix.get())
            config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_lo_ro_center_mix', lo_ro_center_mix.get())
            config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_lo_ro_surround_mix', lo_ro_surround_mix.get())
            config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_dolby_surround_ex_mode', dolby_surround_ex_mode.get())
            config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_dolby_headphone_mode', dolby_headphone_mode.get())
            config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_a_d_converter_type', a_d_converter_type.get())
            config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_dolby_stereo_rematrixing', stereo_rematrixing.get())
            config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_channel_coupling', channel_coupling.get())
            config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_cpl_start_band', cpl_start_band.get())
            config_profile.set('FFMPEG E-AC3 - SETTINGS', 'tempo', acodec_atempo.get())
        if encoder.get() == 'Opus':
            config_profile.set('FFMPEG Opus - SETTINGS', 'opus_bitrate', acodec_bitrate.get())
            config_profile.set('FFMPEG Opus - SETTINGS', 'samplerate', acodec_samplerate.get())
            config_profile.set('FFMPEG Opus - SETTINGS', 'acodec_vbr', acodec_vbr.get())
            config_profile.set('FFMPEG Opus - SETTINGS', 'acodec_application', acodec_application.get())
            config_profile.set('FFMPEG Opus - SETTINGS', 'frame_duration', frame_duration.get())
            config_profile.set('FFMPEG Opus - SETTINGS', 'packet_loss', packet_loss.get())
            config_profile.set('FFMPEG Opus - SETTINGS', 'acodec_channel', acodec_channel.get())
            config_profile.set('FFMPEG Opus - SETTINGS', 'dolbyprologicii', dolby_pro_logic_ii.get())
            config_profile.set('FFMPEG Opus - SETTINGS', 'ffmpeg_gain', ffmpeg_gain.get())
            config_profile.set('FFMPEG Opus - SETTINGS', 'tempo', acodec_atempo.get())
        if encoder.get() == 'FDK-AAC':
            config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_bitrate', acodec_bitrate.get())
            config_profile.set('FDK-AAC - SETTINGS', 'acodec_channel', acodec_channel.get())
            config_profile.set('FDK-AAC - SETTINGS', 'dolbyprologicii', dolby_pro_logic_ii.get())
            config_profile.set('FDK-AAC - SETTINGS', 'ffmpeg_gain', ffmpeg_gain.get())
            config_profile.set('FDK-AAC - SETTINGS', 'samplerate', acodec_samplerate.get())
            config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_profile', acodec_profile.get())
            config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_lowdelay', acodec_lowdelay.get())
            config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_sbr_ratio', acodec_sbr_ratio.get())
            config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_gapless', acodec_gapless_mode.get())
            config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_transport_format', acodec_transport_format.get())
            config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_afterburner', afterburnervar.get())
            config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_crccheck', crccheck.get())
            config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_headerperiod', headerperiod.get())
            config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_sbrdelay', sbrdelay.get())
            config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_moovbox', moovbox.get())
            config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_tempo', acodec_atempo.get())
        if encoder.get() == 'MP3':
            config_profile.set('FFMPEG MP3 - SETTINGS', 'acodec_bitrate', acodec_bitrate.get())
            config_profile.set('FFMPEG MP3 - SETTINGS', 'acodec_channel', acodec_channel.get())
            config_profile.set('FFMPEG MP3 - SETTINGS', 'mp3_vbr', mp3_vbr.get())
            config_profile.set('FFMPEG MP3 - SETTINGS', 'mp3_abr', mp3_abr.get())
            config_profile.set('FFMPEG MP3 - SETTINGS', 'dolbyprologicii', dolby_pro_logic_ii.get())
            config_profile.set('FFMPEG MP3 - SETTINGS', 'ffmpeg_gain', ffmpeg_gain.get())
            config_profile.set('FFMPEG MP3 - SETTINGS', 'samplerate', acodec_samplerate.get())
            config_profile.set('FFMPEG MP3 - SETTINGS', 'tempo', acodec_atempo.get())
            if mp3_vbr.get() == '-q:a':
                config_profile.set('FFMPEG MP3 - SETTINGS', 'acodec_bitrate_vbr', acodec_bitrate.get())
            if mp3_vbr.get() == 'off':
                config_profile.set('FFMPEG MP3 - SETTINGS', 'acodec_bitrate_cbr_abr', acodec_bitrate.get())
        if encoder.get() == 'QAAC':
            config_profile.set('FFMPEG QAAC - SETTINGS', 'q_acodec_profile', q_acodec_profile.get())
            config_profile.set('FFMPEG QAAC - SETTINGS', 'dolbyprologicii', dolby_pro_logic_ii.get())
            config_profile.set('FFMPEG QAAC - SETTINGS', 'acodec_channel', acodec_channel.get())
            config_profile.set('FFMPEG QAAC - SETTINGS', 'samplerate', acodec_samplerate.get())
            config_profile.set('FFMPEG QAAC - SETTINGS', 'q_acodec_quality', q_acodec_quality.get())
            config_profile.set('FFMPEG QAAC - SETTINGS', 'q_acodec_quality_amnt', q_acodec_quality_amnt.get())
            config_profile.set('FFMPEG QAAC - SETTINGS', 'q_acodec_bitrate', q_acodec_bitrate.get())
            config_profile.set('FFMPEG QAAC - SETTINGS', 'q_acodec_gain', q_acodec_gain.get())
            config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_normalize', qaac_normalize.get())
            config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_high_efficiency', qaac_high_efficiency.get())
            config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_nodither', qaac_nodither.get())
            config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_nodelay', qaac_nodelay.get())
            config_profile.set('FFMPEG QAAC - SETTINGS', 'q_gapless_mode', q_gapless_mode.get())
            config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_nooptimize', qaac_nooptimize.get())
            config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_threading', qaac_threading.get())
            config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_limiter', qaac_limiter.get())
            config_profile.set('FFMPEG QAAC - SETTINGS', 'tempo', acodec_atempo.get())
        if encoder.get() == 'FLAC':
            config_profile.set('FFMPEG FLAC - SETTINGS', 'acodec_bitrate', acodec_bitrate.get())
            config_profile.set('FFMPEG FLAC - SETTINGS', 'acodec_channel', acodec_channel.get())
            config_profile.set('FFMPEG FLAC - SETTINGS', 'dolbyprologicii', dolby_pro_logic_ii.get())
            config_profile.set('FFMPEG FLAC - SETTINGS', 'gain', ffmpeg_gain.get())
            config_profile.set('FFMPEG FLAC - SETTINGS', 'samplerate', acodec_samplerate.get())
            config_profile.set('FFMPEG FLAC - SETTINGS', 'tempo', acodec_atempo.get())
            config_profile.set('FFMPEG FLAC - SETTINGS', 'flac_lpc_type', acodec_flac_lpc_type.get())
            config_profile.set('FFMPEG FLAC - SETTINGS', 'flac_coefficient', flac_acodec_coefficient.get())
            config_profile.set('FFMPEG FLAC - SETTINGS', 'flac_lpc_passes', acodec_flac_lpc_passes.get())
        if encoder.get() == 'ALAC':
            config_profile.set('FFMPEG ALAC - SETTINGS', 'acodec_channel', acodec_channel.get())
            config_profile.set('FFMPEG ALAC - SETTINGS', 'dolbyprologicii', dolby_pro_logic_ii.get())
            config_profile.set('FFMPEG ALAC - SETTINGS', 'gain', ffmpeg_gain.get())
            config_profile.set('FFMPEG ALAC - SETTINGS', 'samplerate', acodec_samplerate.get())
            config_profile.set('FFMPEG ALAC - SETTINGS', 'tempo', acodec_atempo.get())
            config_profile.set('FFMPEG ALAC - SETTINGS', 'alac_min_prediction_order', min_prediction_order.get())
            config_profile.set('FFMPEG ALAC - SETTINGS', 'alac_max_prediction_order', max_prediction_order.get())

        with open(config_profile_ini, 'w') as configfile_two:
            config_profile.write(configfile_two)

    def reset_profile():  # This function resets settings to 'default'
        msg = messagebox.askyesno(title='Prompt', message='Are you sure you want to reset to default settings?',
                                  parent=audio_window)
        if msg == True:
            if encoder.get() == 'AC3':
                config_profile.set('FFMPEG AC3 - SETTINGS', 'ac3_bitrate', '224k')
                config_profile.set('FFMPEG AC3 - SETTINGS', 'dolbyprologicii', '')
                config_profile.set('FFMPEG AC3 - SETTINGS', 'ffmpeg_gain', '0')
                config_profile.set('FFMPEG AC3 - SETTINGS', 'ac3_channel', 'Original')
                config_profile.set('FFMPEG AC3 - SETTINGS', 'samplerate', 'Original')
                config_profile.set('FFMPEG AC3 - SETTINGS', 'tempo', 'Original')
            if encoder.get() == 'AAC':
                config_profile.set('FFMPEG AAC - SETTINGS', 'dolbyprologicii', '')
                config_profile.set('FFMPEG AAC - SETTINGS', 'ffmpeg_gain', '0')
                config_profile.set('FFMPEG AAC - SETTINGS', 'aac_bitrate', '192')
                config_profile.set('FFMPEG AAC - SETTINGS', 'aac_vbr_quality', '2')
                config_profile.set('FFMPEG AAC - SETTINGS', 'aac_vbr_toggle', '-c:a')
                config_profile.set('FFMPEG AAC - SETTINGS', 'aac_channel', 'Original')
                config_profile.set('FFMPEG AAC - SETTINGS', 'samplerate', 'Original')
                config_profile.set('FFMPEG AAC - SETTINGS', 'tempo', 'Original')
            if encoder.get() == 'DTS':
                config_profile.set('FFMPEG DTS - SETTINGS', 'dts_bitrate', '448')
                config_profile.set('FFMPEG DTS - SETTINGS', 'dolbyprologicii', '')
                config_profile.set('FFMPEG DTS - SETTINGS', 'ffmpeg_gain', '0')
                config_profile.set('FFMPEG DTS - SETTINGS', 'dts_channel', 'Original')
                config_profile.set('FFMPEG DTS - SETTINGS', 'samplerate', 'Original')
                config_profile.set('FFMPEG DTS - SETTINGS', 'tempo', 'Original')
            if encoder.get() == 'E-AC3':
                config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_bitrate', '448k')
                config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_channel', 'Original')
                config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_gain', '0')
                config_profile.set('FFMPEG E-AC3 - SETTINGS', 'samplerate', 'Original')
                config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_per_frame_metadata', 'Default')
                config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_mixing_level', '-1')
                config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_room_type', 'Default')
                config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_copyright_bit', '-1')
                config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_dialogue_level', '-31')
                config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_surround_mode', 'Default')
                config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_original_bitstream', '-1')
                config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_downmix_mode', 'Default')
                config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_lt_rt_center_mix', '-1')
                config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_lt_rt_surround_mix', '-1')
                config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_lo_ro_center_mix', '-1')
                config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_lo_ro_surround_mix', '-1')
                config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_dolby_surround_ex_mode', 'Default')
                config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_dolby_headphone_mode', 'Default')
                config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_a_d_converter_type', 'Default')
                config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_dolby_stereo_rematrixing', 'Default')
                config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_channel_coupling', '-1')
                config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_cpl_start_band', '-1')
                config_profile.set('FFMPEG E-AC3 - SETTINGS', 'tempo', 'Original')
            if encoder.get() == 'Opus':
                config_profile.set('FFMPEG Opus - SETTINGS', 'opus_bitrate', '160k')
                config_profile.set('FFMPEG Opus - SETTINGS', 'samplerate', 'Original')
                config_profile.set('FFMPEG Opus - SETTINGS', 'acodec_vbr', 'VBR: On')
                config_profile.set('FFMPEG Opus - SETTINGS', 'acodec_application', 'Audio')
                config_profile.set('FFMPEG Opus - SETTINGS', 'frame_duration', '20')
                config_profile.set('FFMPEG Opus - SETTINGS', 'packet_loss', '0')
                config_profile.set('FFMPEG Opus - SETTINGS', 'acodec_channel', '2 (Stereo)')
                config_profile.set('FFMPEG Opus - SETTINGS', 'dolbyprologicii', '')
                config_profile.set('FFMPEG Opus - SETTINGS', 'ffmpeg_gain', '0')
                config_profile.set('FFMPEG Opus - SETTINGS', 'tempo', 'Original')
            if encoder.get() == 'FDK-AAC':
                config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_bitrate', 'CBR: 192k')
                config_profile.set('FDK-AAC - SETTINGS', 'acodec_channel', 'Original')
                config_profile.set('FDK-AAC - SETTINGS', 'dolbyprologicii', '')
                config_profile.set('FDK-AAC - SETTINGS', 'ffmpeg_gain', '0')
                config_profile.set('FDK-AAC - SETTINGS', 'samplerate', 'Original')
                config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_profile', 'AAC LC (Default)')
                config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_lowdelay', 'Disable SBR on ELD (DEF)')
                config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_sbr_ratio', 'Library Default')
                config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_gapless', 'iTunSMPB (Def)')
                config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_transport_format', 'M4A (Def)')
                config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_afterburner', '-a0')
                config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_crccheck', '')
                config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_headerperiod', '')
                config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_sbrdelay', '')
                config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_moovbox', '')
                config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_tempo', 'Original')
            if encoder.get() == 'MP3':
                config_profile.set('FFMPEG MP3 - SETTINGS', 'acodec_bitrate', 'VBR: -V 0')
                config_profile.set('FFMPEG MP3 - SETTINGS', 'acodec_channel', 'Original')
                config_profile.set('FFMPEG MP3 - SETTINGS', 'mp3_vbr', '-q:a')
                config_profile.set('FFMPEG MP3 - SETTINGS', 'mp3_abr', '')
                config_profile.set('FFMPEG MP3 - SETTINGS', 'dolbyprologicii', '')
                config_profile.set('FFMPEG MP3 - SETTINGS', 'ffmpeg_gain', '0')
                config_profile.set('FFMPEG MP3 - SETTINGS', 'samplerate', 'Original')
                config_profile.set('FFMPEG MP3 - SETTINGS', 'tempo', 'Original')
                config_profile.set('FFMPEG MP3 - SETTINGS', 'acodec_bitrate_vbr', '')
                config_profile.set('FFMPEG MP3 - SETTINGS', 'acodec_bitrate_cbr_abr', '')
            if encoder.get() == 'QAAC':
                config_profile.set('FFMPEG QAAC - SETTINGS', 'q_acodec_profile', 'True VBR')
                config_profile.set('FFMPEG QAAC - SETTINGS', 'dolbyprologicii', '')
                config_profile.set('FFMPEG QAAC - SETTINGS', 'acodec_channel', 'Original')
                config_profile.set('FFMPEG QAAC - SETTINGS', 'samplerate', 'Original')
                config_profile.set('FFMPEG QAAC - SETTINGS', 'q_acodec_quality', 'High (Default)')
                config_profile.set('FFMPEG QAAC - SETTINGS', 'q_acodec_quality_amnt', '109')
                config_profile.set('FFMPEG QAAC - SETTINGS', 'q_acodec_bitrate', '256')
                config_profile.set('FFMPEG QAAC - SETTINGS', 'q_acodec_gain', '0')
                config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_normalize', '')
                config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_high_efficiency', '')
                config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_nodither', '')
                config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_nodelay', '')
                config_profile.set('FFMPEG QAAC - SETTINGS', 'q_gapless_mode', 'iTunSMPB (Default)')
                config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_nooptimize', '')
                config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_threading', '')
                config_profile.set('FFMPEG QAAC - SETTINGS', 'qaac_limiter', '')
                config_profile.set('FFMPEG QAAC - SETTINGS', 'tempo', 'Original')
            if encoder.get() == 'FLAC':
                config_profile.set('FFMPEG FLAC - SETTINGS', 'acodec_bitrate', 'Level 5 - Default Quality')
                config_profile.set('FFMPEG FLAC - SETTINGS', 'acodec_channel', 'Original')
                config_profile.set('FFMPEG FLAC - SETTINGS', 'dolbyprologicii', '')
                config_profile.set('FFMPEG FLAC - SETTINGS', 'gain', '0')
                config_profile.set('FFMPEG FLAC - SETTINGS', 'samplerate', 'Original')
                config_profile.set('FFMPEG FLAC - SETTINGS', 'tempo', 'Original')
                config_profile.set('FFMPEG FLAC - SETTINGS', 'flac_lpc_type', 'Default')
                config_profile.set('FFMPEG FLAC - SETTINGS', 'flac_coefficient', '15')
                config_profile.set('FFMPEG FLAC - SETTINGS', 'flac_lpc_passes', 'Default')
            if encoder.get() == 'ALAC':
                config_profile.set('FFMPEG ALAC - SETTINGS', 'acodec_channel', 'Original')
                config_profile.set('FFMPEG ALAC - SETTINGS', 'dolbyprologicii', '')
                config_profile.set('FFMPEG ALAC - SETTINGS', 'gain', '0')
                config_profile.set('FFMPEG ALAC - SETTINGS', 'samplerate', 'Original')
                config_profile.set('FFMPEG ALAC - SETTINGS', 'tempo', 'Original')
                config_profile.set('FFMPEG ALAC - SETTINGS', 'alac_min_prediction_order', '4')
                config_profile.set('FFMPEG ALAC - SETTINGS', 'alac_max_prediction_order', '6')

            with open(config_profile_ini, 'w') as configfile_two:
                config_profile.write(configfile_two)
            audio_window.destroy()  # Closes Audio Window
            sleep(.25)  # Sleeps the program for 1/4th of a second
            openaudiowindow()  # Re-Opens the Audio Window with the 'Default' settings


    # ----------------------------------------------------------------------------------------------- Profile Functions

    # Show Streams Inside Audio Settings Window -----------------------------------------------------------------------
    def show_streams_mediainfo():  # Stream Viewer
        global track_count
        if int(track_count) == 1:
            stream_id_type = '1'
        else:
            stream_id_type = '%StreamKindPos%'
        commands = '"' + mediainfocli + ' --Output="Audio;Track #:..............................' \
                                        f'{stream_id_type}\\nFormat:..' + \
                   '..............................%Format%\\nDuration:.........................' + \
                   '.....%Duration/String2%\\nBit Rate Mode:.....................%BitRate_Mode/String%\\nBitrate:.' + \
                   '................................%BitRate/String%\\nSampling Rate:................' + \
                   '....%SamplingRate/String%\\nAudio Channels:..................%Channel(s)%\\nChannel Layout:..' + \
                   '................%ChannelLayout%\\nCompression Mode:.........' + \
                   '...%Compression_Mode/String%\\nStream Size:......................' + \
                   '..%StreamSize/String5%\\nTitle:....................................%Title%\\nLanguage:..' + \
                   '.........................%Language/String%\\n\\n" ' + VideoInputQuoted + '"'
        run = subprocess.Popen('cmd /c ' + commands, creationflags=subprocess.CREATE_NO_WINDOW, universal_newlines=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE, shell=True)
        try:
            global text_area
            text_area.delete("1.0", END)
            text_area.insert(END, run.communicate())
        except:
            stream_window = Toplevel(audio_window)
            stream_window.title("Audio Streams")
            stream_window.configure(background="#434547")
            Label(stream_window, text="---------- Audio Streams ----------", font=("Times New Roman", 16),
                  background='#434547', foreground="white").grid(column=0, row=0)
            text_area = scrolledtextwidget.ScrolledText(stream_window, width=50, height=25, tabs=10, spacing2=3,
                                                        spacing1=2,
                                                        spacing3=3)
            text_area.grid(column=0, pady=10, padx=10)
            text_area.insert(INSERT, run.communicate())
            text_area.configure(font=("Helvetica", 12))
            text_area.configure(state=DISABLED)
            stream_window.grid_columnconfigure(0, weight=1)

    # ---------------------------------------------------------------------------------------------------- Show Streams

    config_profile = ConfigParser()
    config_profile.read(config_profile_ini)

    # AC3 Window ------------------------------------------------------------------------------------------------------
    global audio_window
    if encoder.get() == "AC3":
        try:
            audio_window.deiconify()
        except:
            audio_window = Toplevel()
            audio_window.title('AC3 Settings')
            audio_window.configure(background="#434547")
            window_height = 400
            window_width = 600
            screen_width = audio_window.winfo_screenwidth()
            screen_height = audio_window.winfo_screenheight()
            x_coordinate = int((screen_width / 2) - (window_width / 2))
            y_coordinate = int((screen_height / 2) - (window_height / 2))
            audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

            my_menu_bar = Menu(audio_window, tearoff=0)
            audio_window.config(menu=my_menu_bar)
            file_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
            my_menu_bar.add_cascade(label='Track Tools', menu=file_menu)
            file_menu.add_command(label='View Audio Tracks', command=show_streams_mediainfo)
            file_menu.add_command(label='Play Selected Audio Track  |  9 and 0 for Volume',
                                  command=mpv_gui_audio_window)
            options_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
            my_menu_bar.add_cascade(label='Options', menu=options_menu)
            options_menu.add_command(label='Save Current Settings', command=save_profile)
            options_menu.add_command(label='Reset Settings To Default', command=reset_profile)

            for n in range(3):
                audio_window.grid_columnconfigure(n, weight=1)
            for n in range(4):
                audio_window.grid_rowconfigure(n, weight=1)

            # Views Command -------------------------------------------------------------------------------------------
            def view_command():
                global cmd_line_window
                global cmd_label
                audio_filter_function()
                example_cmd_output = acodec_stream_choices[acodec_stream.get()] \
                                     + encoder_dropdownmenu_choices[encoder.get()] + \
                                     acodec_bitrate_choices[acodec_bitrate.get()] + \
                                     acodec_channel_choices[acodec_channel.get()] + \
                                     acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting + \
                                     ac3_custom_cmd_input
                try:
                    cmd_label.config(text=example_cmd_output)
                    cmd_line_window.deiconify()
                except (AttributeError, NameError):
                    cmd_line_window = Toplevel()
                    cmd_line_window.title('Command Line')
                    cmd_line_window.configure(background="#434547")
                    cmd_label = Label(cmd_line_window, text=example_cmd_output, foreground="white",
                                      background="#434547")
                    cmd_label.config(font=("Helvetica", 16))
                    cmd_label.pack()

                    def hide_instead():
                        cmd_line_window.withdraw()

                    cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

            # ------------------------------------------------------------------------------------------- Views Command

            # Buttons -------------------------------------------------------------------------------------------------
            apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A",
                                  command=gotosavefile)
            apply_button.grid(row=8, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            apply_button.bind("<Enter>", apply_button_hover)
            apply_button.bind("<Leave>", apply_button_hover_leave)

            show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A",
                              command=view_command)
            show_cmd.grid(row=8, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            show_cmd.bind("<Enter>", show_cmd_hover)
            show_cmd.bind("<Leave>", show_cmd_hover_leave)
            # ------------------------------------------------------------------------------------------------- Buttons

            # Audio Bitrate Selection ---------------------------------------------------------------------------------
            acodec_bitrate = StringVar(audio_window)
            acodec_bitrate_choices = {'64k': "-b:a 64k ",
                                      '128k': "-b:a 128k ",
                                      '160k': "-b:a 160k ",
                                      '192k': "-b:a 192k ",
                                      '224k': "-b:a 224k ",
                                      '256k': "-b:a 256k ",
                                      '288k': "-b:a 288k ",
                                      '320k': "-b:a 320k ",
                                      '352k': "-b:a 352k ",
                                      '384k': "-b:a 384k ",
                                      '448k': "-b:a 448k ",
                                      '512k': "-b:a 512k ",
                                      '576k': "-b:a 576k ",
                                      '640k': "-b:a 640k "}
            acodec_bitrate.set(config_profile['FFMPEG AC3 - SETTINGS']['ac3_bitrate'])  # set the default option
            acodec_bitrate_menu_label = Label(audio_window, text="Bitrate :", background="#434547", foreground="white")
            acodec_bitrate_menu_label.grid(row=0, column=2, columnspan=1, padx=10, pady=3, sticky=W + E)
            acodec_bitrate_menu = OptionMenu(audio_window, acodec_bitrate, *acodec_bitrate_choices.keys())
            acodec_bitrate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            acodec_bitrate_menu.grid(row=1, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            acodec_bitrate_menu["menu"].configure(activebackground="dim grey")
            acodec_bitrate_menu.bind("<Enter>", acodec_bitrate_menu_hover)
            acodec_bitrate_menu.bind("<Leave>", acodec_bitrate_menu_hover_leave)
            # ------------------------------------------------------------------------------------------- Audio Bitrate

            # Audio Stream Selection ----------------------------------------------------------------------------------
            acodec_stream = StringVar(audio_window)
            acodec_stream_choices = acodec_stream_track_counter
            acodec_stream.set(next(iter(acodec_stream_track_counter)))  # set the default option
            acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
            acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
            acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
            acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1,
                                      width=12, anchor='w')
            acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            acodec_stream_menu["menu"].configure(activebackground="dim grey")
            acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
            acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)
            acodec_stream.trace('w', track_number_mpv)
            track_number_mpv()
            # ---------------------------------------------------------------------------------------------------------

            # Audio Channel Selection ---------------------------------------------------------------------------------
            acodec_channel = StringVar(audio_window)
            acodec_channel_choices = {'Original': "",
                                      '1 (Mono)': "-ac 1 ",
                                      '2 (Stereo)': "-ac 2 ",
                                      '2.1 (Stereo)': "-ac 3 ",
                                      '4.0 (Quad)': "-ac 4 ",
                                      '5.0 (Surround)': "-ac 5 ",
                                      '5.1 (Surround)': "-ac 6 "}
            acodec_channel.set(config_profile['FFMPEG AC3 - SETTINGS']['ac3_channel'])  # set the default option
            achannel_menu_label = Label(audio_window, text="Channels :", background="#434547", foreground="white")
            achannel_menu_label.grid(row=0, column=1, columnspan=1, padx=10, pady=3, sticky=W + E)
            achannel_menu = OptionMenu(audio_window, acodec_channel, *acodec_channel_choices.keys())
            achannel_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            achannel_menu.grid(row=1, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            achannel_menu["menu"].configure(activebackground="dim grey")
            achannel_menu.bind("<Enter>", achannel_menu_hover)
            achannel_menu.bind("<Leave>", achannel_menu_hover_leave)
            acodec_channel.trace('w', dolby_pro_logic_ii_enable_disable)
            # ----------------------------------------------------------------------------------------------- Audio Channel

            # Dolby Pro Logic II ------------------------------------------------------------------------------------------
            dolby_pro_logic_ii = StringVar()
            dolby_pro_logic_ii_checkbox = Checkbutton(audio_window, text=' Dolby Pro\nLogic II',
                                                      variable=dolby_pro_logic_ii, state=DISABLED,
                                                      onvalue='"aresample=matrix_encoding=dplii"', offvalue="")
            if acodec_channel.get() == '2 (Stereo)':
                dolby_pro_logic_ii_checkbox.configure(state=NORMAL)
            dolby_pro_logic_ii_checkbox.grid(row=4, column=2, columnspan=1, rowspan=1, padx=10, pady=(20, 5),
                                             sticky=N + S + E + W)
            dolby_pro_logic_ii_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                                  activeforeground="white", selectcolor="#434547",
                                                  font=("Helvetica", 11))
            dolby_pro_logic_ii.set(config_profile['FFMPEG AC3 - SETTINGS']['dolbyprologicii'])
            # -------------------------------------------------------------------------------------------------- DPL II

            # Audio Gain Selection ------------------------------------------------------------------------------------
            ffmpeg_gain = StringVar()
            ffmpeg_gain_label = Label(audio_window, text="Gain (dB) :", background="#434547",
                                      foreground="white")
            ffmpeg_gain_label.grid(row=2, column=0, columnspan=1, padx=10, pady=3,
                                   sticky=N + S + E + W)
            ffmpeg_gain_spinbox = Spinbox(audio_window, from_=-30, to=30, increment=1.0, justify=CENTER,
                                          wrap=True, textvariable=ffmpeg_gain)
            ffmpeg_gain_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                          buttonbackground="black", width=15, readonlybackground="#23272A")
            ffmpeg_gain_spinbox.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            ffmpeg_gain.set(int(config_profile['FFMPEG AC3 - SETTINGS']['ffmpeg_gain']))
            # ---------------------------------------------------------------------------------------------------- Gain

            # Audio Sample Rate Selection -----------------------------------------------------------------------------
            acodec_samplerate = StringVar(audio_window)
            acodec_samplerate_choices = {'Original': "",
                                         '32000 Hz': "-ar 32000 ",
                                         '44100 Hz': "-ar 44100 ",
                                         '48000 Hz': "-ar 48000 "}
            acodec_samplerate.set(config_profile['FFMPEG AC3 - SETTINGS']['samplerate'])  # set the default option
            acodec_samplerate_label = Label(audio_window, text="Sample Rate :", background="#434547",
                                            foreground="white")
            acodec_samplerate_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_samplerate_menu = OptionMenu(audio_window, acodec_samplerate, *acodec_samplerate_choices.keys())
            acodec_samplerate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            acodec_samplerate_menu.grid(row=3, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_samplerate_menu["menu"].configure(activebackground="dim grey")
            acodec_samplerate_menu.bind("<Enter>", acodec_samplerate_menu_hover)
            acodec_samplerate_menu.bind("<Leave>", acodec_samplerate_menu_hover_leave)

            # --------------------------------------------------------------------------------------------- Sample Rate

            # Entry Box for Custom Command Line -----------------------------------------------------------------------
            def ac3_cmd(*args):
                global ac3_custom_cmd_input
                if ac3_custom_cmd.get() == (""):
                    ac3_custom_cmd_input = ("")
                else:
                    cstmcmd = ac3_custom_cmd.get()
                    ac3_custom_cmd_input = cstmcmd + " "

            ac3_custom_cmd = StringVar()
            ac3_cmd_entrybox_label = Label(audio_window, text="Custom Command Line :", anchor=W, background="#434547",
                                           foreground="white")
            ac3_cmd_entrybox_label.grid(row=5, column=0, columnspan=2, padx=10, pady=(15, 0), sticky=N + S + W + E)
            ac3_cmd_entrybox = Entry(audio_window, textvariable=ac3_custom_cmd, borderwidth=4, background="#CACACA")
            ac3_cmd_entrybox.grid(row=6, column=0, columnspan=3, padx=10, pady=(0, 15), sticky=W + E)
            ac3_custom_cmd.trace('w', ac3_cmd)
            ac3_custom_cmd.set("")
            # ------------------------------------------------------------------------------------- Custom Command Line

            # Audio Atempo Selection ----------------------------------------------------------------------------------
            acodec_atempo = StringVar(audio_window)
            acodec_atempo_choices = {'Original': '',
                                     '23.976 to 24': '"atempo=23.976/24"',
                                     '23.976 to 25': '"atempo=23.976/25"',
                                     '24 to 23.976': '"atempo=24/23.976"',
                                     '24 to 25': '"atempo=24/25"',
                                     '25 to 23.976': '"atempo=25/23.976"',
                                     '25 to 24': '"atempo=25/24"',
                                     '1/4 Slow-down': '"atempo=0.5,atempo=0.5"',
                                     '1/2 Slow-down': '"atempo=0.5"',
                                     '3/4 Slow-down': '"atempo=0.75"',
                                     '1/4 Speed-up': '"atempo=1.25"',
                                     '1/2 Speed-up': '"atempo=1.5"',
                                     '3/4 Speed-up': '"atempo=1.75"',
                                     '2x Speed-up': '"atempo=2.0"',
                                     '2.5x Speed-up': '"atempo=2.5"',
                                     '3x Speed-up': '"atempo=3.0"',
                                     '3.5x Speed-up': '"atempo=3.5"',
                                     '4x Speed-up': '"atempo=4.0"'}
            acodec_atempo_menu_label = Label(audio_window, text="Time Modification :", background="#434547",
                                             foreground="white")
            acodec_atempo_menu_label.grid(row=2, column=2, columnspan=1, padx=10, pady=3, sticky=W + E)
            acodec_atempo_menu = OptionMenu(audio_window, acodec_atempo, *acodec_atempo_choices.keys())
            acodec_atempo_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            acodec_atempo_menu.grid(row=3, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            acodec_atempo.set(config_profile['FFMPEG AC3 - SETTINGS']['tempo'])
            acodec_atempo_menu["menu"].configure(activebackground="dim grey")
            acodec_atempo_menu.bind("<Enter>", acodec_atempo_menu_hover)
            acodec_atempo_menu.bind("<Leave>", acodec_atempo_menu_hover_leave)
        # ------------------------------------------------------------------------------------------------ Audio Atempo
    # ------------------------------------------------------------------------------------------------------------- AC3

    # AAC Window ------------------------------------------------------------------------------------------------------
    elif encoder.get() == "AAC":
        audio_window = Toplevel()
        audio_window.title('AAC Settings')
        audio_window.configure(background="#434547")
        window_height = 420
        window_width = 620
        screen_width = audio_window.winfo_screenwidth()
        screen_height = audio_window.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

        my_menu_bar = Menu(audio_window, tearoff=0)
        audio_window.config(menu=my_menu_bar)

        file_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
        my_menu_bar.add_cascade(label='Track Tools', menu=file_menu)
        file_menu.add_command(label='View Audio Tracks', command=show_streams_mediainfo)
        file_menu.add_command(label='Play Selected Audio Track  |  9 and 0 for Volume',
                              command=mpv_gui_audio_window)
        options_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
        my_menu_bar.add_cascade(label='Options', menu=options_menu)
        options_menu.add_command(label='Save Current Settings', command=save_profile)
        options_menu.add_command(label='Reset Settings To Default', command=reset_profile)

        for n in range(3):
            audio_window.grid_columnconfigure(n, weight=1)
        for n in range(6):
            audio_window.grid_rowconfigure(n, weight=1)
        audio_window.grid_rowconfigure(10, weight=1)

        def view_command():  # Views Command --------------------------------------------------------------------------
            global cmd_label, cmd_line_window, example_cmd_output
            audio_filter_function()
            if aac_vbr_toggle.get() == "-c:a ":
                example_cmd_output = acodec_stream_choices[acodec_stream.get()] + \
                                     encoder_dropdownmenu_choices[encoder.get()] + \
                                     "-b:a " + aac_bitrate_spinbox.get() + "k " + acodec_channel_choices[
                                         acodec_channel.get()] + \
                                     acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting + \
                                     aac_custom_cmd_input + aac_title_input
            elif aac_vbr_toggle.get() == "-q:a ":
                example_cmd_output = acodec_stream_choices[acodec_stream.get()] + \
                                     encoder_dropdownmenu_choices[encoder.get()] + \
                                     "-q:a " + aac_quality_spinbox.get() + " " + acodec_channel_choices[
                                         acodec_channel.get()] + \
                                     acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting + \
                                     aac_custom_cmd_input + aac_title_input
            try:
                cmd_label.config(text=example_cmd_output)
                cmd_line_window.deiconify()
            except (AttributeError, NameError):
                cmd_line_window = Toplevel()
                cmd_line_window.title('Command Line')
                cmd_line_window.configure(background="#434547")
                cmd_label = Label(cmd_line_window, text=example_cmd_output, foreground="white", background="#434547")
                cmd_label.config(font=("Helvetica", 16))
                cmd_label.winfo_exists()
                cmd_label.pack()

                def hide_instead():
                    cmd_line_window.withdraw()

                cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

        # ----------------------------------------------------------------------------------------------- Views Command

        # Buttons -----------------------------------------------------------------------------------------------------
        apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A",
                              command=gotosavefile)
        apply_button.grid(row=10, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        apply_button.bind("<Enter>", apply_button_hover)
        apply_button.bind("<Leave>", apply_button_hover_leave)

        show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A",
                          command=view_command)
        show_cmd.grid(row=10, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        show_cmd.bind("<Enter>", show_cmd_hover)
        show_cmd.bind("<Leave>", show_cmd_hover_leave)

        # ----------------------------------------------------------------------------------------------------- Buttons

        # Entry Box for Custom Command Line ---------------------------------------------------------------------------
        def aac_cmd(*args):
            global aac_custom_cmd_input
            if aac_custom_cmd.get() == (""):
                aac_custom_cmd_input = ("")
            else:
                cstmcmd = aac_custom_cmd.get()
                aac_custom_cmd_input = cstmcmd + " "

        aac_custom_cmd = StringVar()
        aac_cmd_entrybox_label = Label(audio_window, text="Custom Command Line :", anchor=W, background="#434547",
                                       foreground="white")
        aac_cmd_entrybox_label.grid(row=6, column=0, columnspan=2, padx=10, pady=(0, 0), sticky=N + S + W + E)
        aac_cmd_entrybox = Entry(audio_window, textvariable=aac_custom_cmd, borderwidth=4, background="#CACACA")
        aac_cmd_entrybox.grid(row=7, column=0, columnspan=3, padx=10, pady=(0, 0), sticky=W + E)
        aac_custom_cmd.trace('w', aac_cmd)
        aac_custom_cmd.set("")

        # ----------------------------------------------------------------------------------------- Custom Command Line

        # Entry Box for Track Title -----------------------------------------------------------------------------------
        def aac_title_check(*args):
            global aac_title_input
            if aac_title.get() == (""):
                aac_title_input = ("")
            else:
                title_cmd = aac_title.get()
                aac_title_input = "-metadata:s:a:0 title=" + '"' + title_cmd + '"' + " "

        aac_title = StringVar()
        aac_title_entrybox_label = Label(audio_window, text="Track Name :", anchor=W, background="#434547",
                                         foreground="white")
        aac_title_entrybox_label.grid(row=8, column=0, columnspan=2, padx=10, pady=(5, 0), sticky=N + S + W + E)
        aac_title_entrybox = Entry(audio_window, textvariable=aac_title, borderwidth=4, background="#CACACA")
        aac_title_entrybox.grid(row=9, column=0, columnspan=3, padx=10, pady=(0, 10), sticky=W + E)
        aac_title.trace('w', aac_title_check)
        aac_title.set("")
        # ------------------------------------------------------------------------------------------------- Track Title

        # Audio Channel Selection -------------------------------------------------------------------------------------
        acodec_channel = StringVar(audio_window)
        acodec_channel_choices = {'Original': "",
                                  '1 (Mono)': "-ac 1 ",
                                  '2 (Stereo)': "-ac 2 ",
                                  '2.1 (Stereo)': "-ac 3 ",
                                  '4.0 (Surround)': "-ac 4 ",
                                  '5.0 (Surround)': "-ac 5 ",
                                  '5.1 (Surround)': "-ac 6 ",
                                  '6.1 (Surround)': "-ac 7 ",
                                  '7.1 (Surround)': "-ac 8 "}
        acodec_channel.set(config_profile['FFMPEG AAC - SETTINGS']['aac_channel'])  # set the default option
        achannel_menu_label = Label(audio_window, text="Channels :", background="#434547", foreground="white")
        achannel_menu_label.grid(row=0, column=1, columnspan=1, padx=10, pady=3, sticky=W + E)
        achannel_menu = OptionMenu(audio_window, acodec_channel, *acodec_channel_choices.keys())
        achannel_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        achannel_menu.grid(row=1, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        achannel_menu["menu"].configure(activebackground="dim grey")
        achannel_menu.bind("<Enter>", achannel_menu_hover)
        achannel_menu.bind("<Leave>", achannel_menu_hover_leave)
        acodec_channel.trace('w', dolby_pro_logic_ii_enable_disable)
        # ------------------------------------------------------------------------------------- Audio Channel Selection

        # Dolby Pro Logic II ------------------------------------------------------------------------------------------
        dolby_pro_logic_ii = StringVar()
        dolby_pro_logic_ii_checkbox = Checkbutton(audio_window, text=' Dolby Pro\nLogic II',
                                                  variable=dolby_pro_logic_ii, state=DISABLED,
                                                  onvalue='"aresample=matrix_encoding=dplii"', offvalue="")
        if acodec_channel.get() == '2 (Stereo)':
            dolby_pro_logic_ii_checkbox.configure(state=NORMAL)
        dolby_pro_logic_ii_checkbox.grid(row=4, column=0, columnspan=1, rowspan=1, padx=10, pady=(15, 15),
                                         sticky=N + S + E + W)
        dolby_pro_logic_ii_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                              activeforeground="white", selectcolor="#434547", font=("Helvetica", 11))
        dolby_pro_logic_ii.set(config_profile['FFMPEG AAC - SETTINGS']['dolbyprologicii'])
        # ------------------------------------------------------------------------------------------------------ DPL II

        # Audio Gain Selection ----------------------------------------------------------------------------------------
        ffmpeg_gain = StringVar()
        ffmpeg_gain_label = Label(audio_window, text="Gain (dB) :", background="#434547",
                                  foreground="white")
        ffmpeg_gain_label.grid(row=0, column=2, columnspan=1, padx=10, pady=3,
                               sticky=N + S + E + W)
        ffmpeg_gain_spinbox = Spinbox(audio_window, from_=-30, to=30, increment=1.0, justify=CENTER,
                                      wrap=True, textvariable=ffmpeg_gain)
        ffmpeg_gain_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                      buttonbackground="black", width=15, readonlybackground="#23272A")
        ffmpeg_gain_spinbox.grid(row=1, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        ffmpeg_gain.set(int(config_profile['FFMPEG AAC - SETTINGS']['ffmpeg_gain']))
        # -------------------------------------------------------------------------------------------------------- Gain

        # Audio Bitrate Spinbox ---------------------------------------------------------------------------------------
        global aac_bitrate_spinbox
        aac_bitrate_spinbox = StringVar()
        aac_acodec_bitrate_spinbox_label = Label(audio_window, text="Bitrate :", background="#434547",
                                                 foreground="white")
        aac_acodec_bitrate_spinbox_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3,
                                              sticky=N + S + E + W)
        aac_acodec_bitrate_spinbox = Spinbox(audio_window, from_=1, to=800, increment=2.0, justify=CENTER,
                                             wrap=True, textvariable=aac_bitrate_spinbox)
        aac_acodec_bitrate_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                             buttonbackground="black", width=15, readonlybackground="#23272A")
        aac_acodec_bitrate_spinbox.grid(row=3, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        aac_bitrate_spinbox.set(int(config_profile['FFMPEG AAC - SETTINGS']['aac_bitrate']))
        # --------------------------------------------------------------------------------------- Audio Bitrate Spinbox

        # Vbr Toggle --------------------------------------------------------------------------------------------------
        global aac_vbr_toggle
        aac_vbr_toggle = StringVar()
        aac_vbr_toggle.set(config_profile['FFMPEG AAC - SETTINGS']['aac_vbr_toggle'] + ' ')

        def aac_vbr_trace(*args):  # Swap Spin Box Between CBR and VBR
            if aac_vbr_toggle.get() == "-c:a ":
                global aac_bitrate_spinbox
                aac_acodec_bitrate_spinbox_label = Label(audio_window, text="Bitrate :", background="#434547",
                                                         foreground="white")
                aac_acodec_bitrate_spinbox_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3,
                                                      sticky=N + S + E + W)
                aac_acodec_bitrate_spinbox = Spinbox(audio_window, from_=1, to=800, increment=2.0, justify=CENTER,
                                                     wrap=True, textvariable=aac_bitrate_spinbox)
                aac_acodec_bitrate_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                                     buttonbackground="black", width=15, readonlybackground="#23272A")
                aac_acodec_bitrate_spinbox.grid(row=3, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
                aac_bitrate_spinbox.set(int(config_profile['FFMPEG AAC - SETTINGS']['aac_bitrate']))
            elif aac_vbr_toggle.get() == "-q:a ":  # This enables VBR Spinbox -----------------------------------------
                global aac_quality_spinbox
                aac_quality_spinbox = StringVar()
                aac_acodec_quality_spinbox_label = Label(audio_window, text="VBR Quality :", background="#434547",
                                                         foreground="white")
                aac_acodec_quality_spinbox_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3,
                                                      sticky=N + S + E + W)
                aac_acodec_quality_spinbox = Spinbox(audio_window, from_=0.1, to=5, increment=0.1, justify=CENTER,
                                                     wrap=True, textvariable=aac_quality_spinbox)
                aac_acodec_quality_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                                     buttonbackground="black", width=15, readonlybackground="#23272A")
                aac_acodec_quality_spinbox.grid(row=3, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
                aac_quality_spinbox.set(float(config_profile['FFMPEG AAC - SETTINGS']['aac_vbr_quality']))
                # ----------------------------------------------------------------------------------------- VBR Spinbox

        aac_vbr_toggle_checkbox = Checkbutton(audio_window, text=' Variable\n Bit-Rate', variable=aac_vbr_toggle,
                                              onvalue="-q:a ", offvalue="-c:a ", command=aac_vbr_trace)
        aac_vbr_toggle_checkbox.grid(row=4, column=1, columnspan=1, rowspan=2, padx=10, pady=3, sticky=N + S + E + W)
        aac_vbr_toggle_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                          activeforeground="white", selectcolor="#434547", font=("Helvetica", 11))
        aac_vbr_trace()
        aac_vbr_toggle.trace('w', aac_vbr_trace)
        # -------------------------------------------------------------------------------------------------- Vbr Toggle

        # Audio Stream Selection --------------------------------------------------------------------------------------
        acodec_stream = StringVar(audio_window)
        acodec_stream_choices = acodec_stream_track_counter
        acodec_stream.set(next(iter(acodec_stream_track_counter)))
        next(iter(acodec_stream_track_counter))
        acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
        acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
        acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=12, anchor='w')
        acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_stream_menu["menu"].configure(activebackground="dim grey")
        acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
        acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)
        acodec_stream.trace('w', track_number_mpv)
        track_number_mpv()
        # -------------------------------------------------------------------------------------- Audio Stream Selection

        # Audio Sample Rate Selection ---------------------------------------------------------------------------------
        acodec_samplerate = StringVar(audio_window)
        acodec_samplerate_choices = {'Original': "",
                                     '8000 Hz': "-ar 8000 ",
                                     '11025 Hz': "-ar 11025 ",
                                     '12000 Hz': "-ar 12000 ",
                                     '16000 Hz': "-ar 16000 ",
                                     '22050 Hz': "-ar 22050 ",
                                     '24000 Hz': "-ar 24000 ",
                                     '32000 Hz': "-ar 32000 ",
                                     '44100 Hz': "-ar 44100 ",
                                     '48000 Hz': "-ar 48000 "}
        acodec_samplerate.set(config_profile['FFMPEG AAC - SETTINGS']['samplerate'])  # set the default option
        acodec_samplerate_label = Label(audio_window, text="Sample Rate :", background="#434547", foreground="white")
        acodec_samplerate_label.grid(row=2, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_samplerate_menu = OptionMenu(audio_window, acodec_samplerate, *acodec_samplerate_choices.keys())
        acodec_samplerate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_samplerate_menu.grid(row=3, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_samplerate_menu["menu"].configure(activebackground="dim grey")
        acodec_samplerate_menu.bind("<Enter>", acodec_samplerate_menu_hover)
        acodec_samplerate_menu.bind("<Leave>", acodec_samplerate_menu_hover_leave)
        # --------------------------------------------------------------------------------- Audio Sample Rate Selection

        # Audio Atempo Selection -------------------------------------------------------------------------------------
        acodec_atempo = StringVar(audio_window)
        acodec_atempo_choices = {'Original': '',
                                 '23.976 to 24': '"atempo=23.976/24"',
                                 '23.976 to 25': '"atempo=23.976/25"',
                                 '24 to 23.976': '"atempo=24/23.976"',
                                 '24 to 25': '"atempo=24/25"',
                                 '25 to 23.976': '"atempo=25/23.976"',
                                 '25 to 24': '"atempo=25/24"',
                                 '1/4 Slow-down': '"atempo=0.5,atempo=0.5"',
                                 '1/2 Slow-down': '"atempo=0.5"',
                                 '3/4 Slow-down': '"atempo=0.75"',
                                 '1/4 Speed-up': '"atempo=1.25"',
                                 '1/2 Speed-up': '"atempo=1.5"',
                                 '3/4 Speed-up': '"atempo=1.75"',
                                 '2x Speed-up': '"atempo=2.0"',
                                 '2.5x Speed-up': '"atempo=2.5"',
                                 '3x Speed-up': '"atempo=3.0"',
                                 '3.5x Speed-up': '"atempo=3.5"',
                                 '4x Speed-up': '"atempo=4.0"'}
        acodec_atempo_menu_label = Label(audio_window, text="Time Modification :", background="#434547",
                                         foreground="white")
        acodec_atempo_menu_label.grid(row=2, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_atempo_menu = OptionMenu(audio_window, acodec_atempo, *acodec_atempo_choices.keys())
        acodec_atempo_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=10)
        acodec_atempo_menu.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_atempo.set(config_profile['FFMPEG AAC - SETTINGS']['tempo'])
        acodec_atempo_menu["menu"].configure(activebackground="dim grey")
        acodec_atempo_menu.bind("<Enter>", acodec_atempo_menu_hover)
        acodec_atempo_menu.bind("<Leave>", acodec_atempo_menu_hover_leave)
        # ----------------------------------------------------------------------------------------------- Audio Atempto
    # ------------------------------------------------------------------------------------------------------ AAC Window

    # DTS Window ------------------------------------------------------------------------------------------------------
    elif encoder.get() == "DTS":
        audio_window = Toplevel()
        audio_window.title('DTS Settings')
        audio_window.configure(background="#434547")
        window_height = 420
        window_width = 550
        screen_width = audio_window.winfo_screenwidth()
        screen_height = audio_window.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

        my_menu_bar = Menu(audio_window, tearoff=0)
        audio_window.config(menu=my_menu_bar)

        file_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
        my_menu_bar.add_cascade(label='Track Tools', menu=file_menu)
        file_menu.add_command(label='View Audio Tracks', command=show_streams_mediainfo)
        file_menu.add_command(label='Play Selected Audio Track  |  9 and 0 for Volume',
                              command=mpv_gui_audio_window)
        options_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
        my_menu_bar.add_cascade(label='Options', menu=options_menu)
        options_menu.add_command(label='Save Current Settings', command=save_profile)
        options_menu.add_command(label='Reset Settings To Default', command=reset_profile)

        for n in range(3):
            audio_window.grid_columnconfigure(n, weight=1)
        for n in range(7):
            audio_window.grid_rowconfigure(n, weight=1)
        audio_window.grid_rowconfigure(9, weight=1)

        def dts_setting_choice_trace(*args):
            if dts_settings.get() == 'DTS Encoder':
                achannel_menu.config(state=NORMAL)
                acodec_channel.set(config_profile['FFMPEG DTS - SETTINGS']['dts_channel'])
                ffmpeg_gain_spinbox.config(state=NORMAL)
                ffmpeg_gain.set(int(config_profile['FFMPEG DTS - SETTINGS']['ffmpeg_gain']))
                acodec_samplerate_menu.config(state=NORMAL)
                acodec_samplerate.set(config_profile['FFMPEG DTS - SETTINGS']['samplerate'])
                dts_acodec_bitrate_spinbox.config(state=NORMAL)
                dts_bitrate_spinbox.set(int(config_profile['FFMPEG DTS - SETTINGS']['dts_bitrate']))
                acodec_atempo_menu.config(state=NORMAL)
                acodec_atempo.set(config_profile['FFMPEG DTS - SETTINGS']['tempo'])
            else:
                achannel_menu.config(state=DISABLED)
                ffmpeg_gain_spinbox.config(state=DISABLED)
                acodec_samplerate_menu.config(state=DISABLED)
                dts_acodec_bitrate_spinbox.config(state=DISABLED)
                dolby_pro_logic_ii_checkbox.config(state=DISABLED)
                acodec_atempo_menu.config(state=DISABLED)

        # Views Command -----------------------------------------------------------------------------------------------
        def view_command():
            global cmd_label
            global cmd_line_window
            audio_filter_function()
            if dts_settings.get() == 'DTS Encoder':
                example_cmd_output = acodec_stream_choices[acodec_stream.get()] \
                                     + dts_settings_choices[dts_settings.get()] + \
                                     "-b:a " + dts_bitrate_spinbox.get() + "k " + \
                                     acodec_channel_choices[acodec_channel.get()] + \
                                     acodec_samplerate_choices[acodec_samplerate.get()] + \
                                     audio_filter_setting + dts_custom_cmd_input
            else:
                example_cmd_output = acodec_stream_choices[acodec_stream.get()] \
                                     + dts_settings_choices[dts_settings.get()] + \
                                     dts_custom_cmd_input
            try:
                cmd_label.config(text=example_cmd_output)
                cmd_line_window.deiconify()
            except (AttributeError, NameError):
                cmd_line_window = Toplevel()
                cmd_line_window.title('Command Line')
                cmd_line_window.configure(background="#434547")
                cmd_label = Label(cmd_line_window, text=example_cmd_output, foreground="white", background="#434547")
                cmd_label.config(font=("Helvetica", 16))
                cmd_label.winfo_exists()
                cmd_label.pack()

                def hide_instead():
                    cmd_line_window.withdraw()

                cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

        # ----------------------------------------------------------------------------------------------- Views Command

        # Buttons -----------------------------------------------------------------------------------------------------
        apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A",
                              command=gotosavefile)
        apply_button.grid(row=9, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        apply_button.bind("<Enter>", apply_button_hover)
        apply_button.bind("<Leave>", apply_button_hover_leave)

        show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A",
                          command=view_command)
        show_cmd.grid(row=9, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        show_cmd.bind("<Enter>", show_cmd_hover)
        show_cmd.bind("<Leave>", show_cmd_hover_leave)

        # ----------------------------------------------------------------------------------------------------- Buttons

        # Entry Box for Custom Command Line ---------------------------------------------------------------------------
        def dts_cmd(*args):
            global dts_custom_cmd_input
            if dts_custom_cmd.get() == (""):
                dts_custom_cmd_input = ("")
            else:
                cstmcmd = dts_custom_cmd.get()
                dts_custom_cmd_input = cstmcmd + " "

        dts_custom_cmd = StringVar()
        dts_cmd_entrybox_label = Label(audio_window, text="Custom Command Line :", anchor=W, background="#434547",
                                       foreground="white")
        dts_cmd_entrybox_label.grid(row=7, column=0, columnspan=2, padx=10, pady=(15, 0), sticky=N + S + W + E)
        dts_cmd_entrybox = Entry(audio_window, textvariable=dts_custom_cmd, borderwidth=4, background="#CACACA")
        dts_cmd_entrybox.grid(row=8, column=0, columnspan=3, padx=10, pady=(0, 10), sticky=W + E)
        dts_custom_cmd.trace('w', dts_cmd)
        dts_custom_cmd.set("")

        # ----------------------------------------------------------------------------------------- Custom Command Line

        # Audio Bitrate Spinbox ---------------------------------------------------------------------------------------
        global dts_bitrate_spinbox
        dts_bitrate_spinbox = StringVar()
        dts_acodec_bitrate_spinbox_label = Label(audio_window, text="Bitrate :", background="#434547",
                                                 foreground="white")
        dts_acodec_bitrate_spinbox_label.grid(row=2, column=2, columnspan=1, padx=10, pady=3,
                                              sticky=N + S + E + W)
        dts_acodec_bitrate_spinbox = Spinbox(audio_window, from_=250, to=3840, increment=1.0, justify=CENTER,
                                             wrap=True, textvariable=dts_bitrate_spinbox, state=DISABLED,
                                             disabledbackground='grey')
        dts_acodec_bitrate_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                             buttonbackground="black", width=15, readonlybackground="#23272A")
        dts_acodec_bitrate_spinbox.grid(row=3, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        dts_bitrate_spinbox.set(int(config_profile['FFMPEG DTS - SETTINGS']['dts_bitrate']))
        # --------------------------------------------------------------------------------------- Audio Bitrate Spinbox

        # Audio Channel Selection -------------------------------------------------------------------------------------
        acodec_channel = StringVar(audio_window)
        acodec_channel_choices = {'(Mono)': "-ac 1 ",
                                  '2 (Stereo)': "-ac 2 ",
                                  'Original': ""}
        acodec_channel.set(config_profile['FFMPEG DTS - SETTINGS']['dts_channel'])  # set the default option
        achannel_menu_label = Label(audio_window, text="Channels :", background="#434547", foreground="white")
        achannel_menu_label.grid(row=0, column=2, columnspan=1, padx=10, pady=3, sticky=W + E + N + S)
        achannel_menu = OptionMenu(audio_window, acodec_channel, *acodec_channel_choices.keys())
        achannel_menu.config(background="#23272A", foreground="white", highlightthickness=1, state=DISABLED)
        achannel_menu.grid(row=1, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        achannel_menu["menu"].configure(activebackground="dim grey")
        achannel_menu.bind("<Enter>", achannel_menu_hover)
        achannel_menu.bind("<Leave>", achannel_menu_hover_leave)
        acodec_channel.trace('w', dolby_pro_logic_ii_enable_disable)
        # ------------------------------------------------------------------------------------- Audio Channel Selection

        # DTS Encoder(s) ----------------------------------------------------------------------------------------------
        dts_settings = StringVar(audio_window)
        dts_settings_choices = {'Reduce to Core': "-bsf:a dca_core -c:a copy ",
                                'Extract HD Track': "-c:a copy ",
                                'DTS Encoder': "-strict -2 -c:a dca "}
        dts_settings.set('Reduce to Core')  # set the default option
        dts_settings_label = Label(audio_window, text="DTS Settings :", background="#434547", foreground="white")
        dts_settings_label.grid(row=0, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        dts_settings_menu = OptionMenu(audio_window, dts_settings, *dts_settings_choices.keys())
        dts_settings_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        dts_settings_menu.grid(row=1, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        dts_settings_menu.bind("<Enter>", dts_settings_menu_hover)
        dts_settings_menu.bind("<Leave>", dts_settings_menu_hover_leave)
        dts_settings.trace('w', dts_setting_choice_trace)
        # ------------------------------------------------------------------------------------------------ DTS Encoders

        # Dolby Pro Logic II ------------------------------------------------------------------------------------------
        dolby_pro_logic_ii = StringVar()
        dolby_pro_logic_ii_checkbox = Checkbutton(audio_window, text=' Dolby Pro\nLogic II',
                                                  variable=dolby_pro_logic_ii, state=DISABLED,
                                                  onvalue='"aresample=matrix_encoding=dplii"', offvalue='')
        if acodec_channel.get() == '2 (Stereo)' and dts_settings.get() == 'DTS Encoder':
            dolby_pro_logic_ii_checkbox.configure(state=NORMAL)
        dolby_pro_logic_ii_checkbox.grid(row=4, column=0, columnspan=1, rowspan=2, padx=10, pady=(10, 3),
                                         sticky=N + S + E + W)
        dolby_pro_logic_ii_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                              activeforeground="white", selectcolor="#434547", font=("Helvetica", 11))
        dolby_pro_logic_ii.set(config_profile['FFMPEG DTS - SETTINGS']['dolbyprologicii'])
        # ------------------------------------------------------------------------------------------------------ DPL II

        # Audio Gain Selection ----------------------------------------------------------------------------------------
        ffmpeg_gain = StringVar()
        ffmpeg_gain_label = Label(audio_window, text="Gain (dB) :", background="#434547",
                                  foreground="white")
        ffmpeg_gain_label.grid(row=2, column=0, columnspan=1, padx=10, pady=3,
                               sticky=N + S + E + W)
        ffmpeg_gain_spinbox = Spinbox(audio_window, from_=-30, to=30, increment=1.0, justify=CENTER,
                                      wrap=True, textvariable=ffmpeg_gain, state=DISABLED)
        ffmpeg_gain_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                      buttonbackground="black", width=15, readonlybackground="#23272A",
                                      disabledbackground='grey')
        ffmpeg_gain_spinbox.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        ffmpeg_gain.set(int(config_profile['FFMPEG DTS - SETTINGS']['ffmpeg_gain']))
        # -------------------------------------------------------------------------------------------------------- Gain

        # Audio Sample Rate Selection ---------------------------------------------------------------------------------
        acodec_samplerate = StringVar(audio_window)
        acodec_samplerate_choices = {'Original': "",
                                     '16000 Hz': "-ar 16000 ",
                                     '22050 Hz': "-ar 22050 ",
                                     '24000 Hz': "-ar 24000 ",
                                     '32000 Hz': "-ar 32000 ",
                                     '44100 Hz': "-ar 44100 ",
                                     '48000 Hz': "-ar 48000 "}
        acodec_samplerate.set(config_profile['FFMPEG DTS - SETTINGS']['samplerate'])  # set the default option
        acodec_samplerate_label = Label(audio_window, text="Sample Rate :", background="#434547", foreground="white")
        acodec_samplerate_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_samplerate_menu = OptionMenu(audio_window, acodec_samplerate, *acodec_samplerate_choices.keys())
        acodec_samplerate_menu.config(background="#23272A", foreground="white", highlightthickness=1, state=DISABLED)
        acodec_samplerate_menu.grid(row=3, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_samplerate_menu["menu"].configure(activebackground="dim grey")
        acodec_samplerate_menu.bind("<Enter>", acodec_samplerate_menu_hover)
        acodec_samplerate_menu.bind("<Leave>", acodec_samplerate_menu_hover_leave)
        # --------------------------------------------------------------------------------- Audio Sample Rate Selection

        # Audio Stream Selection --------------------------------------------------------------------------------------
        acodec_stream = StringVar(audio_window)
        acodec_stream_choices = acodec_stream_track_counter
        acodec_stream.set(next(iter(acodec_stream_track_counter)))
        acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
        acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
        acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=12, anchor='w')
        acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_stream_menu["menu"].configure(activebackground="dim grey")
        acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
        acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)
        acodec_stream.trace('w', track_number_mpv)
        track_number_mpv()
        # ------------------------------------------------------------------------------------------------ Audio Stream

        # Audio Atempo Selection ---------------------------------------------------------------------------------------
        acodec_atempo = StringVar(audio_window)
        acodec_atempo_choices = {'Original': '',
                                 '23.976 to 24': '"atempo=23.976/24"',
                                 '23.976 to 25': '"atempo=23.976/25"',
                                 '24 to 23.976': '"atempo=24/23.976"',
                                 '24 to 25': '"atempo=24/25"',
                                 '25 to 23.976': '"atempo=25/23.976"',
                                 '25 to 24': '"atempo=25/24"',
                                 '1/4 Slow-down': '"atempo=0.5,atempo=0.5"',
                                 '1/2 Slow-down': '"atempo=0.5"',
                                 '3/4 Slow-down': '"atempo=0.75"',
                                 '1/4 Speed-up': '"atempo=1.25"',
                                 '1/2 Speed-up': '"atempo=1.5"',
                                 '3/4 Speed-up': '"atempo=1.75"',
                                 '2x Speed-up': '"atempo=2.0"',
                                 '2.5x Speed-up': '"atempo=2.5"',
                                 '3x Speed-up': '"atempo=3.0"',
                                 '3.5x Speed-up': '"atempo=3.5"',
                                 '4x Speed-up': '"atempo=4.0"'}
        acodec_atempo_menu_label = Label(audio_window, text="Time Modification :", background="#434547",
                                         foreground="white")
        acodec_atempo_menu_label.grid(row=4, column=2, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_atempo_menu = OptionMenu(audio_window, acodec_atempo, *acodec_atempo_choices.keys())
        acodec_atempo_menu.config(background="#23272A", foreground="white", highlightthickness=1, state=DISABLED)
        acodec_atempo_menu.grid(row=5, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_atempo.set(config_profile['FFMPEG DTS - SETTINGS']['tempo'])
        acodec_atempo_menu["menu"].configure(activebackground="dim grey")
        acodec_atempo_menu.bind("<Enter>", acodec_atempo_menu_hover)
        acodec_atempo_menu.bind("<Leave>", acodec_atempo_menu_hover_leave)
        # ------------------------------------------------------------------------------------------------ Audio Atempo
    # ------------------------------------------------------------------------------------------------------------- DTS

    # Opus Window -----------------------------------------------------------------------------------------------------
    elif encoder.get() == "Opus":
        audio_window = Toplevel()
        audio_window.title('Opus Settings')
        audio_window.configure(background="#434547")
        window_height = 580
        window_width = 650
        screen_width = audio_window.winfo_screenwidth()
        screen_height = audio_window.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

        my_menu_bar = Menu(audio_window, tearoff=0)
        audio_window.config(menu=my_menu_bar)

        file_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
        my_menu_bar.add_cascade(label='Track Tools', menu=file_menu)
        file_menu.add_command(label='View Audio Tracks', command=show_streams_mediainfo)
        file_menu.add_command(label='Play Selected Audio Track  |  9 and 0 for Volume',
                              command=mpv_gui_audio_window)
        options_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
        my_menu_bar.add_cascade(label='Options', menu=options_menu)
        options_menu.add_command(label='Save Current Settings', command=save_profile)
        options_menu.add_command(label='Reset Settings To Default', command=reset_profile)

        advanced_label = Label(audio_window,
                               text="- - - - - - - - - - - - - - - - - - - - Advanced Settings - - - - - - - - - - - "
                                    "- - - - - - - - -",
                               background="#434547", foreground="white", relief=GROOVE)
        advanced_label.grid(row=7, column=0, columnspan=3, padx=10, pady=(5, 0), sticky=W + E)

        advanced_label_end = Label(audio_window,
                                   text="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "
                                        "- - - - - - - - -",
                                   background="#434547", foreground="white", relief=GROOVE)
        advanced_label_end.grid(row=10, column=0, columnspan=3, padx=10, pady=(5, 0), sticky=W + E)

        for n in range(3):
            audio_window.grid_columnconfigure(n, weight=1)
        for n in range(7):
            audio_window.grid_rowconfigure(n, weight=1)
        for n in [8, 9, 13]:
            audio_window.grid_rowconfigure(n, weight=1)

        # Views Command -----------------------------------------------------------------------------------------------
        def view_command():
            global cmd_label
            global cmd_line_window
            audio_filter_function()
            example_cmd_output = acodec_stream_choices[acodec_stream.get()] \
                                 + encoder_dropdownmenu_choices[encoder.get()] \
                                 + acodec_bitrate_choices[acodec_bitrate.get()] \
                                 + acodec_channel_choices[acodec_channel.get()] \
                                 + acodec_vbr_choices[acodec_vbr.get()] \
                                 + acodec_application_choices[acodec_application.get()] \
                                 + "-packet_loss " + packet_loss.get() + " -frame_duration " \
                                 + frame_duration.get() + " " + acodec_samplerate_choices[acodec_samplerate.get()] \
                                 + audio_filter_setting + opus_custom_cmd_input
            try:
                cmd_label.config(text=example_cmd_output)
                cmd_line_window.deiconify()
            except (AttributeError, NameError):
                cmd_line_window = Toplevel()
                cmd_line_window.title('Command Line')
                cmd_line_window.configure(background="#434547")
                cmd_label = Label(cmd_line_window, text=example_cmd_output, foreground="white", background="#434547")
                cmd_label.config(font=("Helvetica", 16))
                cmd_label.winfo_exists()
                cmd_label.pack()

                def hide_instead():
                    cmd_line_window.withdraw()

                cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

        # ----------------------------------------------------------------------------------------------- Views Command

        # Buttons -----------------------------------------------------------------------------------------------------
        apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A",
                              command=gotosavefile)
        apply_button.grid(row=13, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        apply_button.bind("<Enter>", apply_button_hover)
        apply_button.bind("<Leave>", apply_button_hover_leave)

        show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A",
                          command=view_command)
        show_cmd.grid(row=13, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        show_cmd.bind("<Enter>", show_cmd_hover)
        show_cmd.bind("<Leave>", show_cmd_hover_leave)
        # ----------------------------------------------------------------------------------------------------- Buttons

        # Audio Bitrate Menu ------------------------------------------------------------------------------------------
        acodec_bitrate = StringVar(audio_window)
        acodec_bitrate_choices = {'6k': "-b:a 6k ",
                                  '8k': "-b:a 8k ",
                                  '16k': "-b:a 16k ",
                                  '24k': "-b:a 24k ",
                                  '40k': "-b:a 40k ",
                                  '48k': "-b:a 48k ",
                                  '64k': "-b:a 64k ",
                                  '96k': "-b:a 96k ",
                                  '112k': "-b:a 112k ",
                                  '128k': "-b:a 128k ",
                                  '160k': "-b:a 160k ",
                                  '192k': "-b:a 192k ",
                                  '256k': "-b:a 256k ",
                                  '320k': "-b:a 320k ",
                                  '448k': "-b:a 448k ",
                                  '510k': "-b:a 510k "}
        acodec_bitrate.set(config_profile['FFMPEG Opus - SETTINGS']['opus_bitrate'])  # set the default option
        acodec_bitrate_menu_label = Label(audio_window, text="Quality :", background="#434547", foreground="white")
        acodec_bitrate_menu_label.grid(row=0, column=2, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_bitrate_menu = OptionMenu(audio_window, acodec_bitrate, *acodec_bitrate_choices.keys())
        acodec_bitrate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_bitrate_menu.grid(row=1, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_bitrate_menu["menu"].configure(activebackground="dim grey")
        acodec_bitrate_menu.bind("<Enter>", acodec_bitrate_menu_hover)
        acodec_bitrate_menu.bind("<Leave>", acodec_bitrate_menu_hover_leave)
        # ----------------------------------------------------------------------------------------------- Audio Bitrate

        # Audio Sample Rate Selection ---------------------------------------------------------------------------------
        acodec_samplerate = StringVar(audio_window)
        acodec_samplerate_choices = {'Original': "",
                                     '8000 Hz': "-ar 8000 ",
                                     '12000 Hz': "-ar 12000 ",
                                     '16000 Hz': "-ar 16000 ",
                                     '24000 Hz': "-ar 24000 ",
                                     '48000 Hz': "-ar 48000 "}
        acodec_samplerate.set(config_profile['FFMPEG Opus - SETTINGS']['samplerate'])  # set the default option
        acodec_samplerate_label = Label(audio_window, text="Sample Rate :", background="#434547", foreground="white")
        acodec_samplerate_label.grid(row=2, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_samplerate_menu = OptionMenu(audio_window, acodec_samplerate, *acodec_samplerate_choices.keys())
        acodec_samplerate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_samplerate_menu.grid(row=3, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_samplerate_menu["menu"].configure(activebackground="dim grey")
        acodec_samplerate_menu.bind("<Enter>", acodec_samplerate_menu_hover)
        acodec_samplerate_menu.bind("<Leave>", acodec_samplerate_menu_hover_leave)

        # --------------------------------------------------------------------------------- Audio Sample Rate Selection

        # Entry Box for Custom Command Line ---------------------------------------------------------------------------
        def opus_cmd(*args):
            global opus_custom_cmd_input
            if opus_custom_cmd.get() == (""):
                opus_custom_cmd_input = ("")
            else:
                cstmcmd = opus_custom_cmd.get()
                opus_custom_cmd_input = cstmcmd + " "

        opus_custom_cmd = StringVar()
        opus_cmd_entrybox_label = Label(audio_window, text="Custom Command Line :", anchor=W, background="#434547",
                                        foreground="white")
        opus_cmd_entrybox_label.grid(row=11, column=0, columnspan=2, padx=10, pady=(10, 0), sticky=N + S + W + E)
        opus_cmd_entrybox = Entry(audio_window, textvariable=opus_custom_cmd, borderwidth=4, background="#CACACA")
        opus_cmd_entrybox.grid(row=12, column=0, columnspan=3, padx=10, pady=(0, 15), sticky=W + E)
        opus_custom_cmd.trace('w', opus_cmd)
        opus_custom_cmd.set("")

        # ----------------------------------------------------------------------------------------- Custom Command Line

        # Audio VBR Toggle --------------------------------------------------------------------------------------------
        acodec_vbr = StringVar(audio_window)
        acodec_vbr_choices = {'VBR: On': "",
                              'VBR: Off': "-vbr 0 ",
                              'VBR: Constrained': "-vbr 2 "}
        acodec_vbr.set(config_profile['FFMPEG Opus - SETTINGS']['acodec_vbr'])  # set the default option
        acodec_vbr_menu_label = Label(audio_window, text="VBR :", background="#434547", foreground="white")
        acodec_vbr_menu_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_vbr_menu = OptionMenu(audio_window, acodec_vbr, *acodec_vbr_choices.keys())
        acodec_vbr_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_vbr_menu.grid(row=3, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_vbr_menu["menu"].configure(activebackground="dim grey")
        acodec_vbr_menu.bind("<Enter>", acodec_vbr_menu_hover)
        acodec_vbr_menu.bind("<Leave>", acodec_vbr_menu_hover_leave)
        # -------------------------------------------------------------------------------------------------- VBR Toggle

        # Audio Application Selection ---------------------------------------------------------------------------------
        acodec_application = StringVar(audio_window)
        acodec_application_choices = {'Audio': "",
                                      'VoIP': "-application 2048 ",
                                      'Low Delay': "-application 2051 "}
        acodec_application.set(config_profile['FFMPEG Opus - SETTINGS']['acodec_application'])  # set the def option
        acodec_application_menu_label = Label(audio_window, text="Application:\n*Default is 'Audio'*",
                                              background="#434547", foreground="white")
        acodec_application_menu_label.grid(row=8, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_application_menu = OptionMenu(audio_window, acodec_application, *acodec_application_choices.keys())
        acodec_application_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_application_menu.grid(row=9, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_application_menu["menu"].configure(activebackground="dim grey")
        acodec_application_menu.bind("<Enter>", acodec_application_menu_hover)
        acodec_application_menu.bind("<Leave>", acodec_application_menu_hover_leave)
        # ------------------------------------------------------------------------------------------------- Application

        # Audio Frame Duration Spinbox --------------------------------------------------------------------------------
        global frame_duration
        frame_duration_values = (2.5, 5, 10, 20, 40, 60, 80, 100, 120)
        frame_duration = StringVar(audio_window)
        frame_duration_label = Label(audio_window, text="Frame Duration:\n*Default is '20'*", background="#434547",
                                     foreground="white")
        frame_duration_label.grid(row=8, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        frame_duration_spinbox = Spinbox(audio_window, values=frame_duration_values, justify=CENTER, wrap=True,
                                         textvariable=frame_duration, width=13)
        frame_duration_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                      buttonbackground="black")
        frame_duration_spinbox.grid(row=9, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        frame_duration.set(int(config_profile['FFMPEG Opus - SETTINGS']['frame_duration']))  # default option
        # ---------------------------------------------------------------------------------------------- Frame Duration

        # Audio Packet Loss Spinbox --------------------------------------------------------------------------------
        global packet_loss
        packet_loss = StringVar(audio_window)
        packet_loss_label = Label(audio_window, text="Packet Loss:\n*Default is '0'*", background="#434547",
                                  foreground="white")
        packet_loss_label.grid(row=8, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        packet_loss_spinbox = Spinbox(audio_window, from_=0, to=100, justify=CENTER, wrap=True,
                                      textvariable=packet_loss, width=13)
        packet_loss_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                   buttonbackground="black")
        packet_loss_spinbox.grid(row=9, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        packet_loss.set(int(config_profile['FFMPEG Opus - SETTINGS']['packet_loss']))  # default option
        # ------------------------------------------------------------------------------------------------- Packet Loss

        # Audio Channel Selection -------------------------------------------------------------------------------------
        acodec_channel = StringVar(audio_window)
        acodec_channel_choices = {'2 (Stereo)': "-ac 2 ",
                                  '5.0 (Surround)': "-ac 5 ",
                                  '5.1 (Surround)': "-ac 6 ",
                                  '6.1 (Surround)': "-ac 7 ",
                                  '7.1 (Surround)': "-ac 8 "}
        acodec_channel.set(config_profile['FFMPEG Opus - SETTINGS']['acodec_channel'])
        achannel_menu_label = Label(audio_window, text="Channels :", background="#434547", foreground="white")
        achannel_menu_label.grid(row=0, column=1, columnspan=1, padx=10, pady=3, sticky=W + E)
        achannel_menu = OptionMenu(audio_window, acodec_channel, *acodec_channel_choices.keys())
        achannel_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        achannel_menu.grid(row=1, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        achannel_menu["menu"].configure(activebackground="dim grey")
        achannel_menu.bind("<Enter>", achannel_menu_hover)
        achannel_menu.bind("<Leave>", achannel_menu_hover_leave)
        acodec_channel.trace('w', dolby_pro_logic_ii_enable_disable)
        # ------------------------------------------------------------------------------------------- Channel Selection

        # Audio Stream Selection --------------------------------------------------------------------------------------
        acodec_stream = StringVar(audio_window)
        acodec_stream_choices = acodec_stream_track_counter
        acodec_stream.set(next(iter(acodec_stream_track_counter)))
        acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
        acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
        acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=12, anchor='w')
        acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_stream_menu["menu"].configure(activebackground="dim grey")
        acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
        acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)
        acodec_stream.trace('w', track_number_mpv)
        track_number_mpv()
        # -------------------------------------------------------------------------------------- Audio Stream Selection

        # Dolby Pro Logic II ------------------------------------------------------------------------------------------
        dolby_pro_logic_ii = StringVar()
        dolby_pro_logic_ii_checkbox = Checkbutton(audio_window, text=' Dolby Pro\nLogic II',
                                                  variable=dolby_pro_logic_ii,
                                                  onvalue='"aresample=matrix_encoding=dplii"', offvalue="")
        if acodec_channel.get() == '2 (Stereo)':
            dolby_pro_logic_ii_checkbox.configure(state=NORMAL)
        dolby_pro_logic_ii_checkbox.grid(row=4, column=0, columnspan=1, rowspan=2, padx=10, pady=(15, 5),
                                         sticky=N + S + E + W)
        dolby_pro_logic_ii_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                              activeforeground="white", selectcolor="#434547", font=("Helvetica", 11))
        dolby_pro_logic_ii.set(config_profile['FFMPEG Opus - SETTINGS']['dolbyprologicii'])
        # ------------------------------------------------------------------------------------------------------ DPL II

        # Audio Gain Selection ----------------------------------------------------------------------------------------
        ffmpeg_gain = StringVar()
        ffmpeg_gain_label = Label(audio_window, text="Gain (dB) :", background="#434547",
                                  foreground="white")
        ffmpeg_gain_label.grid(row=2, column=0, columnspan=1, padx=10, pady=(3, 10),
                               sticky=N + S + E + W)
        ffmpeg_gain_spinbox = Spinbox(audio_window, from_=-30, to=30, increment=1.0, justify=CENTER,
                                      wrap=True, textvariable=ffmpeg_gain)
        ffmpeg_gain_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                      buttonbackground="black", width=15, readonlybackground="#23272A")
        ffmpeg_gain_spinbox.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        ffmpeg_gain.set(int(config_profile['FFMPEG Opus - SETTINGS']['ffmpeg_gain']))
        # -------------------------------------------------------------------------------------------------------- Gain

        # Audio Atempo Selection ---------------------------------------------------------------------------------------
        acodec_atempo = StringVar(audio_window)
        acodec_atempo_choices = {'Original': '',
                                 '23.976 to 24': '"atempo=23.976/24"',
                                 '23.976 to 25': '"atempo=23.976/25"',
                                 '24 to 23.976': '"atempo=24/23.976"',
                                 '24 to 25': '"atempo=24/25"',
                                 '25 to 23.976': '"atempo=25/23.976"',
                                 '25 to 24': '"atempo=25/24"',
                                 '1/4 Slow-down': '"atempo=0.5,atempo=0.5"',
                                 '1/2 Slow-down': '"atempo=0.5"',
                                 '3/4 Slow-down': '"atempo=0.75"',
                                 '1/4 Speed-up': '"atempo=1.25"',
                                 '1/2 Speed-up': '"atempo=1.5"',
                                 '3/4 Speed-up': '"atempo=1.75"',
                                 '2x Speed-up': '"atempo=2.0"',
                                 '2.5x Speed-up': '"atempo=2.5"',
                                 '3x Speed-up': '"atempo=3.0"',
                                 '3.5x Speed-up': '"atempo=3.5"',
                                 '4x Speed-up': '"atempo=4.0"'}
        acodec_atempo_menu_label = Label(audio_window, text="Time Modification :", background="#434547",
                                         foreground="white")
        acodec_atempo_menu_label.grid(row=4, column=2, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_atempo_menu = OptionMenu(audio_window, acodec_atempo, *acodec_atempo_choices.keys())
        acodec_atempo_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_atempo_menu.grid(row=5, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_atempo.set(config_profile['FFMPEG Opus - SETTINGS']['tempo'])
        acodec_atempo_menu["menu"].configure(activebackground="dim grey")
        acodec_atempo_menu.bind("<Enter>", acodec_atempo_menu_hover)
        acodec_atempo_menu.bind("<Leave>", acodec_atempo_menu_hover_leave)
        # ------------------------------------------------------------------------------------------------ Audio Atempo
    # ----------------------------------------------------------------------------------------------------- Opus Window

    # MP3 Window ------------------------------------------------------------------------------------------------------
    elif encoder.get() == "MP3":
        audio_window = Toplevel()
        audio_window.title('MP3 Settings')
        audio_window.configure(background="#434547")
        window_height = 360
        window_width = 550
        screen_width = audio_window.winfo_screenwidth()
        screen_height = audio_window.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

        my_menu_bar = Menu(audio_window, tearoff=0)
        audio_window.config(menu=my_menu_bar)

        file_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
        my_menu_bar.add_cascade(label='Track Tools', menu=file_menu)
        file_menu.add_command(label='View Audio Tracks', command=show_streams_mediainfo)
        file_menu.add_command(label='Play Selected Audio Track  |  9 and 0 for Volume',
                              command=mpv_gui_audio_window)
        options_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
        my_menu_bar.add_cascade(label='Options', menu=options_menu)
        options_menu.add_command(label='Save Current Settings', command=save_profile)
        options_menu.add_command(label='Reset Settings To Default', command=reset_profile)

        for n in range(3):
            audio_window.grid_columnconfigure(n, weight=1)
        for n in range(5):
            audio_window.grid_rowconfigure(n, weight=1)
        audio_window.grid_rowconfigure(7, weight=1)

        def update_cfg_mp3():
            config_profile.set('FFMPEG MP3 - SETTINGS', 'mp3_vbr', mp3_vbr.get())
            config_profile.set('FFMPEG MP3 - SETTINGS', 'mp3_abr', mp3_abr.get())
            with open(config_profile_ini, 'w') as configfile_two:
                config_profile.write(configfile_two)

        # Using VBR or CBR/ABR ----------------------------------------------------------------------------------------
        def mp3_bitrate_type(*args):
            global acodec_bitrate
            global acodec_bitrate_choices

            def acodec_bitrate_menu_hover(e):
                acodec_bitrate_menu["bg"] = "grey"
                acodec_bitrate_menu["activebackground"] = "grey"

            def acodec_bitrate_menu_hover_leave(e):
                acodec_bitrate_menu["bg"] = "#23272A"

            acodec_bitrate = StringVar()

            if mp3_vbr.get() == '-q:a':
                mp3_abr.set("")
                mp3_abr_checkbox.config(state=DISABLED)

                acodec_bitrate_choices = {'VBR: -V 0': '-q:a 0 ',
                                          'VBR: -V 1': '-q:a 1 ',
                                          'VBR: -V 2': '-q:a 2 ',
                                          'VBR: -V 3': '-q:a 3 ',
                                          'VBR: -V 4': '-q:a 4 ',
                                          'VBR: -V 5': '-q:a 5 ',
                                          'VBR: -V 6': '-q:a 6 ',
                                          'VBR: -V 7': '-q:a 7 '}
                if config_profile['FFMPEG MP3 - SETTINGS']['acodec_bitrate_vbr'] == '':
                    acodec_bitrate.set('VBR: -V 0')
                else:
                    acodec_bitrate.set(config_profile['FFMPEG MP3 - SETTINGS']['acodec_bitrate_vbr'])
                acodec_bitrate_menu_label = Label(audio_window, text="Quality :", background="#434547",
                                                  foreground="white")
                acodec_bitrate_menu_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3, sticky=W + E)
                acodec_bitrate_menu = OptionMenu(audio_window, acodec_bitrate, *acodec_bitrate_choices.keys())
                acodec_bitrate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
                acodec_bitrate_menu.grid(row=3, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
                acodec_bitrate_menu["menu"].configure(activebackground="dim grey")
                acodec_bitrate_menu.bind("<Enter>", acodec_bitrate_menu_hover)
                acodec_bitrate_menu.bind("<Leave>", acodec_bitrate_menu_hover_leave)

            elif mp3_vbr.get() == 'off':
                mp3_abr_checkbox.config(state=NORMAL)
                mp3_abr.set(config_profile['FFMPEG MP3 - SETTINGS']['mp3_abr'] + ' ')
                acodec_bitrate_choices = {'8k': '-b:a 8k ',
                                          '16k': '-b:a 16k ',
                                          '24k': '-b:a 24k ',
                                          '32k': '-b:a 32k ',
                                          '40k': '-b:a 40k ',
                                          '48k': '-b:a 48k ',
                                          '64k': '-b:a 64k ',
                                          '80k': '-b:a 80k ',
                                          '96k': '-b:a 96k ',
                                          '112k': '-b:a 112k ',
                                          '128k': '-b:a 128k ',
                                          '160k': '-b:a 160k ',
                                          '192k': '-b:a 192k ',
                                          '224k': '-b:a 224k ',
                                          '256k': '-b:a 256k ',
                                          '320k': '-b:a 320k '}
                if config_profile['FFMPEG MP3 - SETTINGS']['acodec_bitrate_cbr_abr'] == '':
                    acodec_bitrate.set('192k')
                else:
                    acodec_bitrate.set(config_profile['FFMPEG MP3 - SETTINGS']['acodec_bitrate_cbr_abr'])
                acodec_bitrate_menu_label = Label(audio_window, text="Bitrate :", background="#434547",
                                                  foreground="white")
                acodec_bitrate_menu_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3, sticky=W + E)
                acodec_bitrate_menu = OptionMenu(audio_window, acodec_bitrate, *acodec_bitrate_choices.keys())
                acodec_bitrate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
                acodec_bitrate_menu.grid(row=3, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
                acodec_bitrate_menu["menu"].configure(activebackground="dim grey")
                acodec_bitrate_menu.bind("<Enter>", acodec_bitrate_menu_hover)
                acodec_bitrate_menu.bind("<Leave>", acodec_bitrate_menu_hover_leave)
            # ------------------------------------------------------------------------------------------ VBR or CBR/ABR

        # Views Command -----------------------------------------------------------------------------------------------
        def view_command():
            global cmd_label
            global cmd_line_window
            audio_filter_function()
            example_cmd_output = acodec_stream_choices[acodec_stream.get()] \
                                 + encoder_dropdownmenu_choices[encoder.get()] \
                                 + acodec_bitrate_choices[acodec_bitrate.get()] \
                                 + acodec_channel_choices[acodec_channel.get()] + mp3_abr.get() \
                                 + acodec_samplerate_choices[acodec_samplerate.get()] \
                                 + audio_filter_setting + mp3_custom_cmd_input
            try:
                cmd_label.config(text=example_cmd_output)
                cmd_line_window.deiconify()
            except (AttributeError, NameError):
                cmd_line_window = Toplevel()
                cmd_line_window.title('Command Line')
                cmd_line_window.configure(background="#434547")
                cmd_label = Label(cmd_line_window, text=example_cmd_output, foreground="white", background="#434547")
                cmd_label.config(font=("Helvetica", 16))
                cmd_label.winfo_exists()
                cmd_label.pack()

                def hide_instead():
                    cmd_line_window.withdraw()

                cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

        # ----------------------------------------------------------------------------------------------- Views Command

        # Buttons -----------------------------------------------------------------------------------------------------
        apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A",
                              command=gotosavefile)
        apply_button.grid(row=7, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        apply_button.bind("<Enter>", apply_button_hover)
        apply_button.bind("<Leave>", apply_button_hover_leave)

        show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A",
                          command=view_command)
        show_cmd.grid(row=7, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        show_cmd.bind("<Enter>", show_cmd_hover)
        show_cmd.bind("<Leave>", show_cmd_hover_leave)
        # ----------------------------------------------------------------------------------------------------- Buttons

        # Audio Channel Selection -------------------------------------------------------------------------------------
        acodec_channel = StringVar(audio_window)
        acodec_channel_choices = {'Original': "",
                                  '1 (Mono)': "-ac 1 ",
                                  '2 (Stereo)': "-ac 2 "}
        acodec_channel.set(config_profile['FFMPEG MP3 - SETTINGS']['acodec_channel'])  # set the default option
        achannel_menu_label = Label(audio_window, text="Channels :", background="#434547", foreground="white")
        achannel_menu_label.grid(row=0, column=1, columnspan=1, padx=10, pady=3, sticky=W + E)
        achannel_menu = OptionMenu(audio_window, acodec_channel, *acodec_channel_choices.keys())
        achannel_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        achannel_menu.grid(row=1, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        achannel_menu["menu"].configure(activebackground="dim grey")
        achannel_menu.bind("<Enter>", achannel_menu_hover)
        achannel_menu.bind("<Leave>", achannel_menu_hover_leave)
        acodec_channel.trace('w', dolby_pro_logic_ii_enable_disable)
        # ----------------------------------------------------------------------------------------------- Audio Channel

        # VBR ---------------------------------------------------------------------------------------------------------
        global mp3_vbr
        mp3_vbr = StringVar()
        mp3_vbr.set(config_profile['FFMPEG MP3 - SETTINGS']['mp3_vbr'])
        mp3_vbr_checkbox = Checkbutton(audio_window, text='VBR', variable=mp3_vbr, onvalue='-q:a', offvalue='off')
        mp3_vbr_checkbox.grid(row=4, column=1, rowspan=1, columnspan=1, padx=10, pady=(5, 0), sticky=N + S + E + W)
        mp3_vbr_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                   activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        mp3_vbr.trace('w', mp3_bitrate_type)
        # --------------------------------------------------------------------------------------------------------- VBR

        # ABR ---------------------------------------------------------------------------------------------------------
        global mp3_abr
        def mp3_abr_toggle(*args):
            update_cfg_mp3()
        mp3_abr = StringVar()
        mp3_abr.set(config_profile['FFMPEG MP3 - SETTINGS']['mp3_abr'] + ' ')
        mp3_abr_checkbox = Checkbutton(audio_window, text='ABR', variable=mp3_abr, onvalue="-abr 1 ",
                                       offvalue="", state=DISABLED)
        if mp3_vbr.get() == 'off ':
            mp3_abr_checkbox.configure(state=NORMAL)
        mp3_abr_checkbox.grid(row=4, column=2, rowspan=1, columnspan=1, padx=10, pady=(0, 5), sticky=N + S + E + W)
        mp3_abr_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                   activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        mp3_abr.trace('w', mp3_abr_toggle)
        # --------------------------------------------------------------------------------------------------------- ABR

        # Entry Box for Custom Command Line ---------------------------------------------------------------------------
        def mp3_cmd(*args):
            global mp3_custom_cmd_input
            if mp3_custom_cmd.get() == (""):
                mp3_custom_cmd_input = ("")
            else:
                cstmcmd = mp3_custom_cmd.get()
                mp3_custom_cmd_input = cstmcmd + " "

        mp3_custom_cmd = StringVar()
        mp3_cmd_entrybox_label = Label(audio_window, text="Custom Command Line :", anchor=W, background="#434547",
                                       foreground="white")
        mp3_cmd_entrybox_label.grid(row=5, column=0, columnspan=2, padx=10, pady=(10, 0), sticky=N + S + W + E)
        mp3_cmd_entrybox = Entry(audio_window, textvariable=mp3_custom_cmd, borderwidth=4, background="#CACACA")
        mp3_cmd_entrybox.grid(row=6, column=0, columnspan=3, padx=10, pady=(0, 15), sticky=W + E)
        mp3_custom_cmd.trace('w', mp3_cmd)
        mp3_custom_cmd.set("")
        # ----------------------------------------------------------------------------------------- Custom Command Line

        # Audio Stream Selection --------------------------------------------------------------------------------------
        acodec_stream = StringVar(audio_window)
        acodec_stream_choices = acodec_stream_track_counter
        acodec_stream.set(next(iter(acodec_stream_track_counter)))
        acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
        acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
        acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=12, anchor='w')
        acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_stream_menu["menu"].configure(activebackground="dim grey")
        acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
        acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)
        acodec_stream.trace('w', track_number_mpv)
        track_number_mpv()
        # ------------------------------------------------------------------------------------------------ Audio Stream

        # Dolby Pro Logic II ------------------------------------------------------------------------------------------
        dolby_pro_logic_ii = StringVar()
        dolby_pro_logic_ii_checkbox = Checkbutton(audio_window, text=' Dolby Pro\nLogic II',
                                                  variable=dolby_pro_logic_ii, state=DISABLED,
                                                  onvalue='"aresample=matrix_encoding=dplii"', offvalue="")
        if acodec_channel.get() == '2 (Stereo)':
            dolby_pro_logic_ii_checkbox.configure(state=NORMAL)
        dolby_pro_logic_ii_checkbox.grid(row=4, column=0, columnspan=1, rowspan=1, padx=10, pady=(15, 3),
                                         sticky=N + S + E + W)
        dolby_pro_logic_ii_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                              activeforeground="white", selectcolor="#434547", font=("Helvetica", 11))
        dolby_pro_logic_ii.set(config_profile['FFMPEG MP3 - SETTINGS']['dolbyprologicii'])
        # ------------------------------------------------------------------------------------------------------ DPL II

        # Audio Gain Selection ----------------------------------------------------------------------------------------
        ffmpeg_gain = StringVar()
        ffmpeg_gain_label = Label(audio_window, text="Gain (dB) :", background="#434547",
                                  foreground="white")
        ffmpeg_gain_label.grid(row=2, column=2, columnspan=1, padx=10, pady=3,
                               sticky=N + S + E + W)
        ffmpeg_gain_spinbox = Spinbox(audio_window, from_=-30, to=30, increment=1.0, justify=CENTER,
                                      wrap=True, textvariable=ffmpeg_gain)
        ffmpeg_gain_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                      buttonbackground="black", width=15, readonlybackground="#23272A")
        ffmpeg_gain_spinbox.grid(row=3, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        ffmpeg_gain.set(int(config_profile['FFMPEG MP3 - SETTINGS']['ffmpeg_gain']))
        ffmpeg_gain.trace('w', audio_filter_function)
        # -------------------------------------------------------------------------------------------------------- Gain

        # Audio Sample Rate Selection ---------------------------------------------------------------------------------
        acodec_samplerate = StringVar(audio_window)
        acodec_samplerate_choices = {'Original': "",
                                     '8000 Hz': "-ar 8000 ",
                                     '11025 Hz': "-ar 11025 ",
                                     '12000 Hz': "-ar 12000 ",
                                     '16000 Hz': "-ar 16000 ",
                                     '22050 Hz': "-ar 22050 ",
                                     '24000 Hz': "-ar 24000 ",
                                     '32000 Hz': "-ar 32000 ",
                                     '44100 Hz': "-ar 44100 ",
                                     '48000 Hz': "-ar 48000 "}
        acodec_samplerate.set(config_profile['FFMPEG MP3 - SETTINGS']['samplerate'])  # set the default option
        acodec_samplerate_label = Label(audio_window, text="Sample Rate :", background="#434547", foreground="white")
        acodec_samplerate_label.grid(row=0, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_samplerate_menu = OptionMenu(audio_window, acodec_samplerate, *acodec_samplerate_choices.keys())
        acodec_samplerate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_samplerate_menu.grid(row=1, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_samplerate_menu["menu"].configure(activebackground="dim grey")
        acodec_samplerate_menu.bind("<Enter>", acodec_samplerate_menu_hover)
        acodec_samplerate_menu.bind("<Leave>", acodec_samplerate_menu_hover_leave)
        # ------------------------------------------------------------------------------------------------- Sample Rate

        # Audio Atempo Selection ---------------------------------------------------------------------------------------
        acodec_atempo = StringVar(audio_window)
        acodec_atempo_choices = {'Original': '',
                                 '23.976 to 24': '"atempo=23.976/24"',
                                 '23.976 to 25': '"atempo=23.976/25"',
                                 '24 to 23.976': '"atempo=24/23.976"',
                                 '24 to 25': '"atempo=24/25"',
                                 '25 to 23.976': '"atempo=25/23.976"',
                                 '25 to 24': '"atempo=25/24"',
                                 '1/4 Slow-down': '"atempo=0.5,atempo=0.5"',
                                 '1/2 Slow-down': '"atempo=0.5"',
                                 '3/4 Slow-down': '"atempo=0.75"',
                                 '1/4 Speed-up': '"atempo=1.25"',
                                 '1/2 Speed-up': '"atempo=1.5"',
                                 '3/4 Speed-up': '"atempo=1.75"',
                                 '2x Speed-up': '"atempo=2.0"',
                                 '2.5x Speed-up': '"atempo=2.5"',
                                 '3x Speed-up': '"atempo=3.0"',
                                 '3.5x Speed-up': '"atempo=3.5"',
                                 '4x Speed-up': '"atempo=4.0"'}
        acodec_atempo_menu_label = Label(audio_window, text="Time Modification :", background="#434547",
                                         foreground="white")
        acodec_atempo_menu_label.grid(row=2, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_atempo_menu = OptionMenu(audio_window, acodec_atempo, *acodec_atempo_choices.keys())
        acodec_atempo_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_atempo_menu.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_atempo.set(config_profile['FFMPEG MP3 - SETTINGS']['tempo'])
        acodec_atempo_menu["menu"].configure(activebackground="dim grey")
        acodec_atempo_menu.bind("<Enter>", acodec_atempo_menu_hover)
        acodec_atempo_menu.bind("<Leave>", acodec_atempo_menu_hover_leave)
        mp3_bitrate_type()
        # ------------------------------------------------------------------------------------------------ Audio Atempo
    # ------------------------------------------------------------------------------------------------------------- MP3

    # E-AC3 Window ----------------------------------------------------------------------------------------------------
    elif encoder.get() == "E-AC3":
        audio_window = Toplevel()
        audio_window.title('E-AC3 Settings')
        audio_window.configure(background="#434547")
        window_height = 850
        window_width = 850
        screen_width = audio_window.winfo_screenwidth()
        screen_height = audio_window.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

        my_menu_bar = Menu(audio_window, tearoff=0)
        audio_window.config(menu=my_menu_bar)
        file_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
        my_menu_bar.add_cascade(label='Track Tools', menu=file_menu)
        file_menu.add_command(label='View Audio Tracks', command=show_streams_mediainfo)
        file_menu.add_command(label='Play Selected Audio Track  |  9 and 0 for Volume',
                              command=mpv_gui_audio_window)
        options_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
        my_menu_bar.add_cascade(label='Options', menu=options_menu)
        options_menu.add_command(label='Save Current Settings', command=save_profile)
        options_menu.add_command(label='Reset Settings To Default', command=reset_profile)

        for n in range(3):
            audio_window.grid_columnconfigure(n, weight=1)
        for n in range(17):
            audio_window.grid_rowconfigure(n, weight=1)
        audio_window.grid_rowconfigure(19, weight=1)

        advanced_label = Label(audio_window,
                               text="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Advanced Settings - "
                                    "- - - - - - - - - - - - - - - - - - - - "
                                    "- - - - - - - - -\n *All settings are set to default below*",
                               background="#434547", foreground="white", relief=GROOVE)
        advanced_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky=W + E)

        # Views Command -----------------------------------------------------------------------------------------------
        def view_command():
            global cmd_label
            global cmd_line_window
            audio_filter_function()
            example_cmd_output = acodec_stream_choices[acodec_stream.get()] \
                                 + encoder_dropdownmenu_choices[encoder.get()] + "-b:a " + eac3_spinbox.get() + " " \
                                 + acodec_channel_choices[acodec_channel.get()] \
                                 + acodec_samplerate_choices[acodec_samplerate.get()] \
                                 + audio_filter_setting + eac3_custom_cmd_input \
                                 + "\n\n- - - - - - - -Advanced Settings- - - - - - - -\n\n" \
                                 + per_frame_metadata_choices[per_frame_metadata.get()] \
                                 + "-mixing_level " + eac3_mixing_level.get() + " " \
                                 + room_type_choices[room_type.get()] \
                                 + "-copyright " + copyright_bit.get() + " " \
                                 + "-dialnorm " + dialogue_level.get() + " " \
                                 + dolby_surround_mode_choices[dolby_surround_mode.get()] \
                                 + "-original  " + original_bit_stream.get() + " " \
                                 + downmix_mode_choices[downmix_mode.get()] \
                                 + "-ltrt_cmixlev " + lt_rt_center_mix.get() + " " \
                                 + "-ltrt_surmixlev " + lt_rt_surround_mix.get() + " " \
                                 + "-loro_cmixlev " + lo_ro_center_mix.get() + " " \
                                 + "\n \n" + "-loro_surmixlev " + lo_ro_surround_mix.get() + " " \
                                 + dolby_surround_ex_mode_choices[dolby_surround_ex_mode.get()] \
                                 + dolby_headphone_mode_choices[dolby_headphone_mode.get()] \
                                 + a_d_converter_type_choices[a_d_converter_type.get()] \
                                 + stereo_rematrixing_choices[stereo_rematrixing.get()] \
                                 + "-channel_coupling " + channel_coupling.get() + " " \
                                 + "-cpl_start_band " + cpl_start_band.get() + " "
            try:
                cmd_label.config(text=example_cmd_output)
                cmd_line_window.deiconify()
            except (AttributeError, NameError):
                cmd_line_window = Toplevel()
                cmd_line_window.title('Command Line')
                cmd_line_window.configure(background="#434547")
                cmd_label = Label(cmd_line_window, text=example_cmd_output, foreground="white", background="#434547")
                cmd_label.config(font=("Helvetica", 16))
                cmd_label.winfo_exists()
                cmd_label.pack()

                def hide_instead():
                    cmd_line_window.withdraw()

                cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

        # ----------------------------------------------------------------------------------------------- Views Command

        # Buttons -----------------------------------------------------------------------------------------------------
        apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A",
                              command=gotosavefile)
        apply_button.grid(row=22, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        apply_button.bind("<Enter>", apply_button_hover)
        apply_button.bind("<Leave>", apply_button_hover_leave)

        show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A",
                          command=view_command)
        show_cmd.grid(row=22, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        show_cmd.bind("<Enter>", show_cmd_hover)
        show_cmd.bind("<Leave>", show_cmd_hover_leave)

        # ----------------------------------------------------------------------------------------------------- Buttons

        # Entry Box for Custom Command Line ---------------------------------------------------------------------------
        def eac3_cmd(*args):
            global eac3_custom_cmd_input
            if eac3_custom_cmd.get() == (""):
                eac3_custom_cmd_input = ("")
            else:
                cstmcmd = eac3_custom_cmd.get()
                eac3_custom_cmd_input = cstmcmd + " "

        eac3_custom_cmd = StringVar()
        eac3_cmd_entrybox_label = Label(audio_window, text="Custom Command Line :", anchor=W, background="#434547",
                                        foreground="white")
        eac3_cmd_entrybox_label.grid(row=20, column=0, columnspan=2, padx=10, pady=(10, 0), sticky=N + S + W + E)
        eac3_cmd_entrybox = Entry(audio_window, textvariable=eac3_custom_cmd, borderwidth=4, background="#CACACA")
        eac3_cmd_entrybox.grid(row=21, column=0, columnspan=3, padx=10, pady=(0, 10), sticky=W + E)
        eac3_custom_cmd.trace('w', eac3_cmd)
        eac3_custom_cmd.set("")

        # ----------------------------------------------------------------------------------------- Custom Command Line

        # Audio Bitrate Menu ------------------------------------------------------------------------------------------
        global eac3_spinbox
        acodec_spinbox_values = ('64k ', '96k ', '160k ', '128k ', '192k ', '224k ', '256k ', '288k ', '320k ', '352k ',
                                 '384k ', '416k ', '448k ', '480k ', '512k ', '544k ', '576k ', '608k ', '640k ',
                                 '672k ', '704k ', '736k ', '768k ', '800k ', '832k ', '864k ', '896k ', '928k ',
                                 '960k ', '1056k ', '1088k ', '1120k ', '1152k ', '1184k ', '1216k ', '1248k ',
                                 '1280k ', '1312k ', '1344k ', '1376k ', '1408k ', '1440k ', '1472k ', '1504k ',
                                 '1536k ', '1568 ', '1600k ', '1632k ', '1664k ', '1696k ', '1728k ', '1760k ',
                                 '1792k ', '1824k ', '1856k ', '1888k ', '1920k ', '1952k ', '1984k ', '2016k ',
                                 '2048k ', '2080k ', '2112k ', '2144k ', '2176k ', '2208k ', '2240k ', '2272k ',
                                 '2304k ', '2336k ', '2368k ', '2400k ', '2432k ', '2464k ', '2496k ', '2528k ')
        eac3_spinbox = StringVar()
        q_acodec_quality_spinbox_label = Label(audio_window, text="Bitrate :", background="#434547", foreground="white")
        q_acodec_quality_spinbox_label.grid(row=0, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        q_acodec_quality_spinbox = Spinbox(audio_window, values=acodec_spinbox_values, justify=CENTER, wrap=True,
                                           textvariable=eac3_spinbox, state='readonly')
        q_acodec_quality_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                        buttonbackground="black", width=10, readonlybackground="#23272A")
        q_acodec_quality_spinbox.grid(row=1, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        eac3_spinbox.set(config_profile['FFMPEG E-AC3 - SETTINGS']['e-ac3_bitrate'] + ' ')
        # ----------------------------------------------------------------------------------------------------- Bitrate

        # Audio Channel Selection -------------------------------------------------------------------------------------
        acodec_channel = StringVar(audio_window)
        acodec_channel_choices = {'Original': "",
                                  '1 (Mono)': "-ac 1 ",
                                  '2 (Stereo)': "-ac 2 ",
                                  '2.1 (Stereo)': "-ac 3 ",
                                  '4.0 (Quad)': "-ac 4 ",
                                  '5.0 (Quad)': "-ac 5 ",
                                  '5.1 (Surround)': "-ac 6 "}
        acodec_channel.set(config_profile['FFMPEG E-AC3 - SETTINGS']['e-ac3_channel'])  # set the default option
        achannel_menu_label = Label(audio_window, text="Channels :", background="#434547", foreground="white")
        achannel_menu_label.grid(row=0, column=1, columnspan=1, padx=10, pady=3, sticky=W + E)
        achannel_menu = OptionMenu(audio_window, acodec_channel, *acodec_channel_choices.keys())
        achannel_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        achannel_menu.grid(row=1, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        achannel_menu["menu"].configure(activebackground="dim grey")
        achannel_menu.bind("<Enter>", achannel_menu_hover)
        achannel_menu.bind("<Leave>", achannel_menu_hover_leave)
        # ---------------------------------------------------------------------------------------------------- Channels

        # Audio Stream Selection --------------------------------------------------------------------------------------
        acodec_stream = StringVar(audio_window)
        acodec_stream_choices = acodec_stream_track_counter
        acodec_stream.set(next(iter(acodec_stream_track_counter)))
        acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
        acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
        acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=12, anchor='w')
        acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_stream_menu["menu"].configure(activebackground="dim grey")
        acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
        acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)
        acodec_stream.trace('w', track_number_mpv)
        track_number_mpv()
        # ------------------------------------------------------------------------------------------------------ Stream

        # Audio Gain Selection ----------------------------------------------------------------------------------------
        ffmpeg_gain = StringVar()
        ffmpeg_gain_label = Label(audio_window, text="Gain (dB) :", background="#434547",
                                  foreground="white")
        ffmpeg_gain_label.grid(row=2, column=0, columnspan=1, padx=10, pady=3,
                               sticky=N + S + E + W)
        ffmpeg_gain_spinbox = Spinbox(audio_window, from_=-30, to=30, increment=1.0, justify=CENTER,
                                      wrap=True, textvariable=ffmpeg_gain)
        ffmpeg_gain_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                      buttonbackground="black", width=15, readonlybackground="#23272A")
        ffmpeg_gain_spinbox.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        ffmpeg_gain.set(int(config_profile['FFMPEG E-AC3 - SETTINGS']['e-ac3_gain']))
        # -------------------------------------------------------------------------------------------------------- Gain

        # Audio Sample Rate Selection ---------------------------------------------------------------------------------
        acodec_samplerate = StringVar(audio_window)
        acodec_samplerate_choices = {'Original': "",
                                     '32000 Hz': "-ar 32000 ",
                                     '44100 Hz': "-ar 44100 ",
                                     '48000 Hz': "-ar 48000 "}
        acodec_samplerate.set(config_profile['FFMPEG E-AC3 - SETTINGS']['samplerate'])  # set the default option
        acodec_samplerate_label = Label(audio_window, text="Sample Rate :", background="#434547", foreground="white")
        acodec_samplerate_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_samplerate_menu = OptionMenu(audio_window, acodec_samplerate, *acodec_samplerate_choices.keys())
        acodec_samplerate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_samplerate_menu.grid(row=3, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_samplerate_menu["menu"].configure(activebackground="dim grey")
        acodec_samplerate_menu.bind("<Enter>", acodec_samplerate_menu_hover)
        acodec_samplerate_menu.bind("<Leave>", acodec_samplerate_menu_hover_leave)
        # ------------------------------------------------------------------------------------------------- Sample Rate

        # Audio Per Frame Metadata Selection --------------------------------------------------------------------------
        global per_frame_metadata, per_frame_metadata_choices
        per_frame_metadata = StringVar(audio_window)
        per_frame_metadata_choices = {'Default': "",
                                      'True': "-per_frame_metadata true ",
                                      'False': "-per_frame_metadata false "}
        per_frame_metadata.set(config_profile['FFMPEG E-AC3 - SETTINGS']['e-ac3_per_frame_metadata'])  # set def option
        per_frame_metadata_label = Label(audio_window, text="Per Frame Metadata :", background="#434547",
                                         foreground="white")
        per_frame_metadata_label.grid(row=5, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        per_frame_metadata_menu = OptionMenu(audio_window, per_frame_metadata, *per_frame_metadata_choices.keys())
        per_frame_metadata_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        per_frame_metadata_menu.grid(row=6, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        per_frame_metadata_menu["menu"].configure(activebackground="dim grey")
        per_frame_metadata_menu.bind("<Enter>", per_frame_metadata_menu_hover)
        per_frame_metadata_menu.bind("<Leave>", per_frame_metadata_menu_hover_leave)
        # ---------------------------------------------------------------------------------------------------- Metadata

        # Mixing Level Spinbox ----------------------------------------------------------------------------------------
        global eac3_mixing_level
        eac3_mixing_level = StringVar()
        eac3_mixing_level_label = Label(audio_window, text="Mixing Level :", background="#434547", foreground="white")
        eac3_mixing_level_label.grid(row=5, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        eac3_mixing_level_spinbox = Spinbox(audio_window, from_=-1, to=111, justify=CENTER, wrap=True,
                                            textvariable=eac3_mixing_level, state='readonly')
        eac3_mixing_level_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                         buttonbackground="black", width=10, readonlybackground="#23272A")
        eac3_mixing_level_spinbox.grid(row=6, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        eac3_mixing_level.set(int(config_profile['FFMPEG E-AC3 - SETTINGS']['e-ac3_mixing_level']))
        # ------------------------------------------------------------------------------------------------ Mixing Level

        # Room Type Selection -----------------------------------------------------------------------------------------
        global room_type, room_type_choices
        room_type = StringVar(audio_window)
        room_type_choices = {'Default': "",
                             'Not Indicated': "-room_type 0 ",
                             'Large': "-room_type 1 ",
                             'Small': "-room_type 2 "}
        room_type.set(config_profile['FFMPEG E-AC3 - SETTINGS']['e-ac3_room_type'])  # set the default option
        room_type_label = Label(audio_window, text="Room Type :", background="#434547", foreground="white")
        room_type_label.grid(row=5, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        room_type_menu = OptionMenu(audio_window, room_type, *room_type_choices.keys())
        room_type_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        room_type_menu.grid(row=6, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        room_type_menu["menu"].configure(activebackground="dim grey")
        room_type_menu.bind("<Enter>", room_type_menu_hover)
        room_type_menu.bind("<Leave>", room_type_menu_hover_leave)
        # --------------------------------------------------------------------------------------------------- Room Type

        # Copyright Bit Spinbox ---------------------------------------------------------------------------------------
        global copyright_bit
        copyright_bit = StringVar()
        copyright_bit_label = Label(audio_window, text="Copyright Bit :", background="#434547", foreground="white")
        copyright_bit_label.grid(row=7, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        copyright_bit_spinbox = Spinbox(audio_window, from_=-1, to=1, justify=CENTER, wrap=True,
                                        textvariable=copyright_bit, state='readonly')
        copyright_bit_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                     buttonbackground="black", width=10, readonlybackground="#23272A")
        copyright_bit_spinbox.grid(row=8, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        copyright_bit.set(int(config_profile['FFMPEG E-AC3 - SETTINGS']['e-ac3_copyright_bit']))
        # --------------------------------------------------------------------------------------------------- Copyright

        # Dialogue Level Spinbox --------------------------------------------------------------------------------------
        global dialogue_level
        dialogue_level = StringVar()
        dialogue_level_label = Label(audio_window, text="Dialogue Level (dB) :", background="#434547",
                                     foreground="white")
        dialogue_level_label.grid(row=7, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        dialogue_level_spinbox = Spinbox(audio_window, from_=-31, to=-1, justify=CENTER, wrap=True,
                                         textvariable=dialogue_level, state='readonly')
        dialogue_level_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                      buttonbackground="black", width=10, readonlybackground="#23272A")
        dialogue_level_spinbox.grid(row=8, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        dialogue_level.set(int(config_profile['FFMPEG E-AC3 - SETTINGS']['e-ac3_dialogue_level']))
        # ---------------------------------------------------------------------------------------------- Dialogue Level

        # Dolby Surround Mode Selection -------------------------------------------------------------------------------
        global dolby_surround_mode, dolby_surround_mode_choices
        dolby_surround_mode = StringVar(audio_window)
        dolby_surround_mode_choices = {'Default': "",
                                       'Not Indicated': "-dsur_mode 0 ",
                                       'On': "-dsur_mode 1 ",
                                       'Off': "-dsur_mode 2 "}
        dolby_surround_mode.set(config_profile['FFMPEG E-AC3 - SETTINGS']['e-ac3_surround_mode'])  # set the def option
        dolby_surround_mode_label = Label(audio_window, text="Dolby Surround Mode :", background="#434547",
                                          foreground="white")
        dolby_surround_mode_label.grid(row=7, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        dolby_surround_mode_menu = OptionMenu(audio_window, dolby_surround_mode, *dolby_surround_mode_choices.keys())
        dolby_surround_mode_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        dolby_surround_mode_menu.grid(row=8, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        dolby_surround_mode_menu["menu"].configure(activebackground="dim grey")
        dolby_surround_mode_menu.bind("<Enter>", dolby_surround_mode_menu_hover)
        dolby_surround_mode_menu.bind("<Leave>", dolby_surround_mode_menu_hover_leave)
        # ---------------------------------------------------------------------------------------------- Dolby Surround

        # Original Bit Stream Spinbox ---------------------------------------------------------------------------------
        global original_bit_stream
        original_bit_stream = StringVar()
        original_bit_stream_label = Label(audio_window, text="Original Bit Stream :", background="#434547",
                                          foreground="white")
        original_bit_stream_label.grid(row=9, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        original_bit_stream_spinbox = Spinbox(audio_window, from_=-1, to=1, justify=CENTER, wrap=True,
                                              textvariable=original_bit_stream, state='readonly')
        original_bit_stream_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                           buttonbackground="black", width=10, readonlybackground="#23272A")
        original_bit_stream_spinbox.grid(row=10, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        original_bit_stream.set(int(config_profile['FFMPEG E-AC3 - SETTINGS']['e-ac3_original_bitstream']))  # default
        # -------------------------------------------------------------------------------------------------- Bit Stream

        # Downmix Mode Selection --------------------------------------------------------------------------------------
        global downmix_mode, downmix_mode_choices
        downmix_mode = StringVar(audio_window)
        downmix_mode_choices = {'Default': "",
                                'Not Indicated': "-dmix_mode 0 ",
                                'Lt/RT Downmix': "-dmix_mode 1 ",
                                'Lo/Ro Downmix': "-dmix_mode 2 ",
                                'Dolby Pro Logic II': "-dmix_mode 3 "}
        downmix_mode.set(config_profile['FFMPEG E-AC3 - SETTINGS']['e-ac3_downmix_mode'])  # set the default option
        downmix_mode_label = Label(audio_window, text="Stereo Downmix Mode :", background="#434547",
                                   foreground="white")
        downmix_mode_label.grid(row=9, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        downmix_mode_menu = OptionMenu(audio_window, downmix_mode, *downmix_mode_choices.keys())
        downmix_mode_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        downmix_mode_menu.grid(row=10, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        downmix_mode_menu["menu"].configure(activebackground="dim grey")
        downmix_mode_menu.bind("<Enter>", downmix_mode_menu_hover)
        downmix_mode_menu.bind("<Leave>", downmix_mode_menu_hover_leave)
        # ------------------------------------------------------------------------------------------------ Downmix Mode

        # Lt/Rt Center Mix Level Spinbox ------------------------------------------------------------------------------
        global lt_rt_center_mix
        lt_rt_center_mix = StringVar()
        lt_rt_center_mix_label = Label(audio_window, text="Lt/Rt Center\nMix Level :", background="#434547",
                                       foreground="white")
        lt_rt_center_mix_label.grid(row=9, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        lt_rt_center_mix_spinbox = Spinbox(audio_window, from_=-1, to=1, justify=CENTER, wrap=True,
                                           textvariable=lt_rt_center_mix, state='readonly', increment=0.1)
        lt_rt_center_mix_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                        buttonbackground="black", width=10, readonlybackground="#23272A")
        lt_rt_center_mix_spinbox.grid(row=10, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        lt_rt_center_mix.set(float(config_profile['FFMPEG E-AC3 - SETTINGS']['e-ac3_lt_rt_center_mix']))  # default
        # -------------------------------------------------------------------------------------- Lt/Rt Center Mix Level

        # Lt/Rt Surround Mix Level Spinbox ----------------------------------------------------------------------------
        global lt_rt_surround_mix
        lt_rt_surround_mix = StringVar()
        lt_rt_surround_mix_label = Label(audio_window, text="Lt/Rt Surround\nMix Level :", background="#434547",
                                         foreground="white")
        lt_rt_surround_mix_label.grid(row=11, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        lt_rt_surround_mix_spinbox = Spinbox(audio_window, from_=-1, to=1, justify=CENTER, wrap=True,
                                             textvariable=lt_rt_surround_mix, state='readonly', increment=0.1)
        lt_rt_surround_mix_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                          buttonbackground="black", width=10, readonlybackground="#23272A")
        lt_rt_surround_mix_spinbox.grid(row=12, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        lt_rt_surround_mix.set(float(config_profile['FFMPEG E-AC3 - SETTINGS']['e-ac3_lt_rt_surround_mix']))  # default
        # ------------------------------------------------------------------------------------ Lt/Rt Surround Mix Level

        # Lo/Ro Center Mix Level Spinbox ------------------------------------------------------------------------------
        global lo_ro_center_mix
        lo_ro_center_mix = StringVar()
        lo_ro_center_mix_label = Label(audio_window, text="Lo/Ro Center\nMix Level :", background="#434547",
                                       foreground="white")
        lo_ro_center_mix_label.grid(row=11, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        lo_ro_center_mix_spinbox = Spinbox(audio_window, from_=-1, to=1, justify=CENTER, wrap=True,
                                           textvariable=lo_ro_center_mix, state='readonly', increment=0.1)
        lo_ro_center_mix_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                        buttonbackground="black", width=10, readonlybackground="#23272A")
        lo_ro_center_mix_spinbox.grid(row=12, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        lo_ro_center_mix.set(float(config_profile['FFMPEG E-AC3 - SETTINGS']['e-ac3_lo_ro_center_mix']))  # default
        # -------------------------------------------------------------------------------------- Lo/Ro Center Mix Level

        # Lo/Ro Surround Mix Level Spinbox ----------------------------------------------------------------------------
        global lo_ro_surround_mix
        lo_ro_surround_mix = StringVar()
        lo_ro_surround_mix_label = Label(audio_window, text="Lo/Ro Surround\nMix Level :", background="#434547",
                                         foreground="white")
        lo_ro_surround_mix_label.grid(row=11, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        lo_ro_surround_mix_spinbox = Spinbox(audio_window, from_=-1, to=1, justify=CENTER, wrap=True,
                                             textvariable=lo_ro_surround_mix, state='readonly', increment=0.1)
        lo_ro_surround_mix_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                          buttonbackground="black", width=10, readonlybackground="#23272A")
        lo_ro_surround_mix_spinbox.grid(row=12, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        lo_ro_surround_mix.set(float(config_profile['FFMPEG E-AC3 - SETTINGS']['e-ac3_lo_ro_surround_mix']))
        # ------------------------------------------------------------------------------------ Lo/Ro Surround Mix Level

        # Dolby Surround EX Mode Selection ----------------------------------------------------------------------------
        global dolby_surround_ex_mode, dolby_surround_ex_mode_choices
        dolby_surround_ex_mode = StringVar(audio_window)
        dolby_surround_ex_mode_choices = {'Default': "",
                                          'Not Indicated': "-dsurex_mode 0 ",
                                          'On': "-dsurex_mode 2 ",
                                          'Off': "-dsurex_mode 1 ",
                                          'Dolby Pro Login IIz': "-dsurex_mode 3 "}
        dolby_surround_ex_mode.set(config_profile['FFMPEG E-AC3 - SETTINGS']['e-ac3_dolby_surround_ex_mode'])  # def
        dolby_surround_ex_mode_label = Label(audio_window, text="Dolby Surround EX Mode :", background="#434547",
                                             foreground="white")
        dolby_surround_ex_mode_label.grid(row=13, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        dolby_surround_ex_mode_menu = OptionMenu(audio_window, dolby_surround_ex_mode,
                                                 *dolby_surround_ex_mode_choices.keys())
        dolby_surround_ex_mode_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        dolby_surround_ex_mode_menu.grid(row=14, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        dolby_surround_ex_mode_menu["menu"].configure(activebackground="dim grey")
        dolby_surround_ex_mode_menu.bind("<Enter>", dolby_surround_ex_mode_menu_hover)
        dolby_surround_ex_mode_menu.bind("<Leave>", dolby_surround_ex_mode_menu_hover_leave)
        # -------------------------------------------------------------------------------------- Dolby Surround EX Mode

        # Dolby Headphone Mode Selection ------------------------------------------------------------------------------
        global dolby_headphone_mode, dolby_headphone_mode_choices
        dolby_headphone_mode = StringVar(audio_window)
        dolby_headphone_mode_choices = {'Default': "",
                                        'Not Indicated': "-dheadphone_mode 0 ",
                                        'On': "-dheadphone_mode 2 ",
                                        'Off': "-dheadphone_mode 1 "}
        dolby_headphone_mode.set(config_profile['FFMPEG E-AC3 - SETTINGS']['e-ac3_dolby_headphone_mode'])  # default
        dolby_headphone_mode_label = Label(audio_window, text="Dolby Headphone Mode :", background="#434547",
                                           foreground="white")
        dolby_headphone_mode_label.grid(row=13, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        dolby_headphone_mode_menu = OptionMenu(audio_window, dolby_headphone_mode, *dolby_headphone_mode_choices.keys())
        dolby_headphone_mode_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        dolby_headphone_mode_menu.grid(row=14, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        dolby_headphone_mode_menu["menu"].configure(activebackground="dim grey")
        dolby_headphone_mode_menu.bind("<Enter>", dolby_headphone_mode_menu_hover)
        dolby_headphone_mode_menu.bind("<Leave>", dolby_headphone_mode_menu_hover_leave)
        # --------------------------------------------------------------------------------------------- Dolby Headphone

        # A/D Converter Type Selection --------------------------------------------------------------------------------
        global a_d_converter_type, a_d_converter_type_choices
        a_d_converter_type = StringVar(audio_window)
        a_d_converter_type_choices = {'Default': "",
                                      'Standard': "-ad_conv_type 0 ",
                                      'HDCD': "-ad_conv_type 1 "}
        a_d_converter_type.set(config_profile['FFMPEG E-AC3 - SETTINGS']['e-ac3_a_d_converter_type'])  # set default
        a_d_converter_type_label = Label(audio_window, text="A/D Converter Type :", background="#434547",
                                         foreground="white")
        a_d_converter_type_label.grid(row=13, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        a_d_converter_type_menu = OptionMenu(audio_window, a_d_converter_type, *a_d_converter_type_choices.keys())
        a_d_converter_type_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        a_d_converter_type_menu.grid(row=14, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        a_d_converter_type_menu["menu"].configure(activebackground="dim grey")
        a_d_converter_type_menu.bind("<Enter>", a_d_converter_type_menu_hover)
        a_d_converter_type_menu.bind("<Leave>", a_d_converter_type_menu_hover_leave)
        # ----------------------------------------------------------------------------------------------- A/D Converter

        # Stereo Rematrixing Selection --------------------------------------------------------------------------------
        global stereo_rematrixing, stereo_rematrixing_choices
        stereo_rematrixing = StringVar(audio_window)
        stereo_rematrixing_choices = {'Default': "",
                                      'True': "-stereo_rematrixing true ",
                                      'False': "-stereo_rematrixing false "}
        stereo_rematrixing.set(config_profile['FFMPEG E-AC3 - SETTINGS']['e-ac3_dolby_stereo_rematrixing'])  # default
        stereo_rematrixing_label = Label(audio_window, text="Stereo Rematrixing :", background="#434547",
                                         foreground="white")
        stereo_rematrixing_label.grid(row=15, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        stereo_rematrixing_menu = OptionMenu(audio_window, stereo_rematrixing, *stereo_rematrixing_choices.keys())
        stereo_rematrixing_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        stereo_rematrixing_menu.grid(row=16, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        stereo_rematrixing_menu["menu"].configure(activebackground="dim grey")
        stereo_rematrixing_menu.bind("<Enter>", stereo_rematrixing_menu_hover)
        stereo_rematrixing_menu.bind("<Leave>", stereo_rematrixing_menu_hover_leave)
        # ------------------------------------------------------------------------------------------ Stereo Rematrixing

        # Channel Coupling Spinbox ------------------------------------------------------------------------------------
        global channel_coupling
        channel_coupling = StringVar()
        channel_coupling_label = Label(audio_window, text="Channel Coupling :", background="#434547",
                                       foreground="white")
        channel_coupling_label.grid(row=15, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        channel_coupling_spinbox = Spinbox(audio_window, from_=-1, to=1, justify=CENTER, wrap=True,
                                           textvariable=channel_coupling, state='readonly')
        channel_coupling_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                        buttonbackground="black", width=10, readonlybackground="#23272A")
        channel_coupling_spinbox.grid(row=16, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        channel_coupling.set(int(config_profile['FFMPEG E-AC3 - SETTINGS']['e-ac3_channel_coupling']))  # default
        # -------------------------------------------------------------------------------------------- Channel Coupling

        # Channel CPL Band Spinbox ------------------------------------------------------------------------------------
        global cpl_start_band
        cpl_start_band = StringVar()
        cpl_start_band_label = Label(audio_window, text="Coupling Start Band :", background="#434547",
                                     foreground="white")
        cpl_start_band_label.grid(row=15, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        cpl_start_band_spinbox = Spinbox(audio_window, from_=-1, to=15, justify=CENTER, wrap=True,
                                         textvariable=cpl_start_band, state='readonly')
        cpl_start_band_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                      buttonbackground="black", width=10, readonlybackground="#23272A")
        cpl_start_band_spinbox.grid(row=16, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        cpl_start_band.set(int(config_profile['FFMPEG E-AC3 - SETTINGS']['e-ac3_cpl_start_band']))
        # -------------------------------------------------------------------------------------------- Channel CPL Band

        # Audio Atempo Selection --------------------------------------------------------------------------------------
        acodec_atempo = StringVar(audio_window)
        acodec_atempo_choices = {'Original': '',
                                 '23.976 to 24': '"atempo=23.976/24"',
                                 '23.976 to 25': '"atempo=23.976/25"',
                                 '24 to 23.976': '"atempo=24/23.976"',
                                 '24 to 25': '"atempo=24/25"',
                                 '25 to 23.976': '"atempo=25/23.976"',
                                 '25 to 24': '"atempo=25/24"',
                                 '1/4 Slow-down': '"atempo=0.5,atempo=0.5"',
                                 '1/2 Slow-down': '"atempo=0.5"',
                                 '3/4 Slow-down': '"atempo=0.75"',
                                 '1/4 Speed-up': '"atempo=1.25"',
                                 '1/2 Speed-up': '"atempo=1.5"',
                                 '3/4 Speed-up': '"atempo=1.75"',
                                 '2x Speed-up': '"atempo=2.0"',
                                 '2.5x Speed-up': '"atempo=2.5"',
                                 '3x Speed-up': '"atempo=3.0"',
                                 '3.5x Speed-up': '"atempo=3.5"',
                                 '4x Speed-up': '"atempo=4.0"'}
        acodec_atempo_menu_label = Label(audio_window, text="Time Modification :", background="#434547",
                                         foreground="white")
        acodec_atempo_menu_label.grid(row=2, column=2, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_atempo_menu = OptionMenu(audio_window, acodec_atempo, *acodec_atempo_choices.keys())
        acodec_atempo_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_atempo_menu.grid(row=3, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_atempo.set(config_profile['FFMPEG E-AC3 - SETTINGS']['tempo'])
        acodec_atempo_menu["menu"].configure(activebackground="dim grey")
        acodec_atempo_menu.bind("<Enter>", acodec_atempo_menu_hover)
        acodec_atempo_menu.bind("<Leave>", acodec_atempo_menu_hover_leave)
        # ------------------------------------------------------------------------------------------------ Audio Atempo
    # ----------------------------------------------------------------------------------------------------------- E-AC3

    # FDK-AAC Window --------------------------------------------------------------------------------------------------
    elif encoder.get() == "FDK-AAC":
        audio_window = Toplevel()
        audio_window.title('FDK-AAC Settings')
        audio_window.configure(background="#434547")
        window_height = 700
        window_width = 780
        screen_width = audio_window.winfo_screenwidth()
        screen_height = audio_window.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

        my_menu_bar = Menu(audio_window, tearoff=0)
        audio_window.config(menu=my_menu_bar)
        file_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
        my_menu_bar.add_cascade(label='Track Tools', menu=file_menu)
        file_menu.add_command(label='View Audio Tracks', command=show_streams_mediainfo)
        file_menu.add_command(label='Play Selected Audio Track  |  9 and 0 for Volume',
                              command=mpv_gui_audio_window)
        options_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
        my_menu_bar.add_cascade(label='Options', menu=options_menu)
        options_menu.add_command(label='Save Current Settings', command=save_profile)
        options_menu.add_command(label='Reset Settings To Default', command=reset_profile)

        for n in range(3):
            audio_window.grid_columnconfigure(n, weight=1)
        for n in range(11):
            audio_window.grid_rowconfigure(n, weight=1)
        audio_window.grid_rowconfigure(15, weight=1)

        def help_button_hover(e):
            help_button["bg"] = "grey"

        def help_button_hover_leave(e):
            help_button["bg"] = "#23272A"

        def acodec_lowdelay_menu_hover(e):
            acodec_lowdelay_menu["bg"] = "grey"
            acodec_lowdelay_menu["activebackground"] = "grey"

        def acodec_lowdelay_menu_hover_leave(e):
            acodec_lowdelay_menu["bg"] = "#23272A"

        def acodec_sbr_ratio_menu_hover(e):
            acodec_sbr_ratio_menu["bg"] = "grey"
            acodec_sbr_ratio_menu["activebackground"] = "grey"

        def acodec_sbr_ratio_menu_hover_leave(e):
            acodec_sbr_ratio_menu["bg"] = "#23272A"

        def acodec_gapless_mode_menu_hover(e):
            acodec_gapless_mode_menu["bg"] = "grey"
            acodec_gapless_mode_menu["activebackground"] = "grey"

        def acodec_gapless_mode_menu_hover_leave(e):
            acodec_gapless_mode_menu["bg"] = "#23272A"

        def acodec_transport_format_menu_hover(e):
            acodec_transport_format_menu["bg"] = "grey"
            acodec_transport_format_menu["activebackground"] = "grey"

        def acodec_transport_format_menu_hover_leave(e):
            acodec_transport_format_menu["bg"] = "#23272A"

        def acodec_profile_menu_hover(e):
            acodec_profile_menu["bg"] = "grey"
            acodec_profile_menu["activebackground"] = "grey"

        def acodec_profile_menu_hover_leave(e):
            acodec_profile_menu["bg"] = "#23272A"

        # Help Button for FDK -----------------------------------------------------------------------------------------
        def gotofdkaachelp():
            helpfile_window = Toplevel(audio_window)
            helpfile_window.title("FDK-AAC Advanced Settings Help")
            helpfile_window.configure(background="#434547")
            Label(helpfile_window, text="Advanced Settings Information",
                  font=("Times New Roman", 14), background='#434547', foreground="white").grid(column=0, row=0)
            helpfile_window.grid_columnconfigure(0, weight=1)
            helpfile_window.grid_rowconfigure(0, weight=1)
            text_area = scrolledtextwidget.ScrolledText(helpfile_window, width=80, height=25)
            text_area.grid(column=0, pady=10, padx=10)
            with open("Apps/fdkaac/FDK-AAC-Help.txt", "r") as helpfile:
                text_area.insert(INSERT, helpfile.read())
                text_area.configure(font=("Helvetica", 14))
                text_area.configure(state=DISABLED)

        # ---------------------------------------------------------------------------------------------------- FDK Help

        # Views Command -----------------------------------------------------------------------------------------------
        def view_command():
            global cmd_label
            global cmd_line_window
            audio_filter_function()
            example_cmd_output = acodec_stream_choices[acodec_stream.get()] + \
                                 acodec_channel_choices[acodec_channel.get()] + \
                                 acodec_samplerate_choices[acodec_samplerate.get()] + \
                                 audio_filter_setting + "-f caf - | " + \
                                 "\n \n" + "fdkaac.exe" + " " + \
                                 acodec_profile_choices[acodec_profile.get()] + afterburnervar.get() \
                                 + fdkaac_title_input + fdkaac_custom_cmd_input + \
                                 crccheck.get() + moovbox.get() + sbrdelay.get() + headerperiod.get() + \
                                 acodec_lowdelay_choices[acodec_lowdelay.get()] + \
                                 acodec_sbr_ratio_choices[acodec_sbr_ratio.get()] + \
                                 acodec_transport_format_choices[acodec_transport_format.get()] + \
                                 acodec_bitrate_choices[acodec_bitrate.get()] + "- -o "
            try:
                cmd_label.config(text=example_cmd_output)
                cmd_line_window.deiconify()
            except (AttributeError, NameError):
                cmd_line_window = Toplevel()
                cmd_line_window.title('Command Line')
                cmd_line_window.configure(background="#434547")
                cmd_label = Label(cmd_line_window, text=example_cmd_output, foreground="white", background="#434547")
                cmd_label.config(font=("Helvetica", 16))
                cmd_label.winfo_exists()
                cmd_label.pack()

                def hide_instead():
                    cmd_line_window.withdraw()

                cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

        # ----------------------------------------------------------------------------------------------- Views Command

        # Buttons -----------------------------------------------------------------------------------------------------
        apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A",
                              command=gotosavefile)
        apply_button.grid(row=15, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        apply_button.bind("<Enter>", apply_button_hover)
        apply_button.bind("<Leave>", apply_button_hover_leave)

        show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A",
                          command=view_command)
        show_cmd.grid(row=15, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        show_cmd.bind("<Enter>", show_cmd_hover)
        show_cmd.bind("<Leave>", show_cmd_hover_leave)

        help_button = Button(audio_window, text="Help + Information", foreground="white", background="#23272A",
                             command=gotofdkaachelp)
        help_button.grid(row=15, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        help_button.bind("<Enter>", help_button_hover)
        help_button.bind("<Leave>", help_button_hover_leave)
        # ----------------------------------------------------------------------------------------------------- Buttons

        advanced_label = Label(audio_window,
                               text="- - - - - - - - - - - - - - - - - - - - Advanced Settings - - - - - - - - - - - "
                                    "- - - - - - - - -",
                               background="#434547", foreground="white", relief=GROOVE)
        advanced_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky=W + E)

        # Audio Bitrate Menu ------------------------------------------------------------------------------------------
        acodec_bitrate = StringVar(audio_window)
        acodec_bitrate_choices = {'CBR: 16k': "-b16 ",
                                  'CBR: 32k': "-b32 ",
                                  'CBR: 64k': "-b64 ",
                                  'CBR: 128k': "-b128 ",
                                  'CBR: 192k': "-b192 ",
                                  'CBR: 256k': "-b256 ",
                                  'CBR: 320k': "-b320 ",
                                  'CBR: 448k': "-b448 ",
                                  'CBR: 640k': "-b640 ",
                                  'VBR: 1': "-m1 ",
                                  'VBR: 2': "-m2 ",
                                  'VBR: 3': "-m3 ",
                                  'VBR: 4': "-m4 ",
                                  'VBR: 5': "-m5 "}
        acodec_bitrate.set(config_profile['FDK-AAC - SETTINGS']['fdk_aac_bitrate'])  # set the default option
        acodec_bitrate_menu_label = Label(audio_window, text="Quality :", background="#434547", foreground="white")
        acodec_bitrate_menu_label.grid(row=0, column=2, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_bitrate_menu = OptionMenu(audio_window, acodec_bitrate, *acodec_bitrate_choices.keys())
        acodec_bitrate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_bitrate_menu.grid(row=1, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_bitrate_menu["menu"].configure(activebackground="dim grey")
        acodec_bitrate_menu.bind("<Enter>", acodec_bitrate_menu_hover)
        acodec_bitrate_menu.bind("<Leave>", acodec_bitrate_menu_hover_leave)
        # ------------------------------------------------------------------------------------------------ Bitrate Menu

        # Audio Channel Selection -------------------------------------------------------------------------------------
        acodec_channel = StringVar(audio_window)
        acodec_channel_choices = {'Original': "",
                                  '1 (Mono)': "-ac 1 ",
                                  '2 (Stereo)': "-ac 2 ",
                                  '5.1 (Surround)': "-ac 6 ",
                                  '6.1 (Surround)': "-ac 7 ",
                                  '7.1 (Surround)': "-ac 8 "}
        acodec_channel.set(config_profile['FDK-AAC - SETTINGS']['acodec_channel'])  # set the default option
        achannel_menu_label = Label(audio_window, text="Channels :", background="#434547", foreground="white")
        achannel_menu_label.grid(row=0, column=1, columnspan=1, padx=10, pady=3, sticky=W + E)
        achannel_menu = OptionMenu(audio_window, acodec_channel, *acodec_channel_choices.keys())
        achannel_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        achannel_menu.grid(row=1, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        achannel_menu["menu"].configure(activebackground="dim grey")
        achannel_menu.bind("<Enter>", achannel_menu_hover)
        achannel_menu.bind("<Leave>", achannel_menu_hover_leave)
        acodec_channel.trace('w', dolby_pro_logic_ii_enable_disable)
        # ----------------------------------------------------------------------------------------------------- Channel

        # Audio Stream Selection --------------------------------------------------------------------------------------
        acodec_stream = StringVar(audio_window)
        acodec_stream_choices = acodec_stream_track_counter
        acodec_stream.set(next(iter(acodec_stream_track_counter)))  # set the default option
        acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
        acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
        acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=12, anchor='w')
        acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_stream_menu["menu"].configure(activebackground="dim grey")
        acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
        acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)
        acodec_stream.trace('w', track_number_mpv)
        track_number_mpv()
        # ------------------------------------------------------------------------------------------------------ Stream

        # Dolby Pro Logic II ------------------------------------------------------------------------------------------
        dolby_pro_logic_ii = StringVar()
        dolby_pro_logic_ii_checkbox = Checkbutton(audio_window, text=' Dolby Pro\nLogic II',
                                                  variable=dolby_pro_logic_ii, state=DISABLED,
                                                  onvalue='"aresample=matrix_encoding=dplii"', offvalue='')
        if acodec_channel.get() == '2 (Stereo)':
            dolby_pro_logic_ii_checkbox.configure(state=NORMAL)
        dolby_pro_logic_ii_checkbox.grid(row=10, column=2, columnspan=1, rowspan=1, padx=10, pady=3,
                                         sticky=N + S + E + W)
        dolby_pro_logic_ii_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                              activeforeground="white", selectcolor="#434547", font=("Helvetica", 11))
        dolby_pro_logic_ii.set(config_profile['FDK-AAC - SETTINGS']['dolbyprologicii'])
        # ------------------------------------------------------------------------------------------------------ DPL II

        # Audio Gain Selection ----------------------------------------------------------------------------------------
        ffmpeg_gain = StringVar()
        ffmpeg_gain_label = Label(audio_window, text="Gain (dB) :", background="#434547",
                                  foreground="white")
        ffmpeg_gain_label.grid(row=2, column=0, columnspan=1, padx=10, pady=3,
                               sticky=N + S + E + W)
        ffmpeg_gain_spinbox = Spinbox(audio_window, from_=-30, to=30, increment=1.0, justify=CENTER,
                                      wrap=True, textvariable=ffmpeg_gain)
        ffmpeg_gain_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                      buttonbackground="black", width=15, readonlybackground="#23272A")
        ffmpeg_gain_spinbox.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        ffmpeg_gain.set(int(config_profile['FDK-AAC - SETTINGS']['ffmpeg_gain']))
        # -------------------------------------------------------------------------------------------------------- Gain

        # Audio Sample Rate Selection ---------------------------------------------------------------------------------
        acodec_samplerate = StringVar(audio_window)
        acodec_samplerate_choices = {'Original': "",
                                     '11025 Hz': "-ar 11025 ",
                                     '22050 Hz': "-ar 22050 ",
                                     '44100 Hz': "-ar 44100 ",
                                     '48000 Hz': "-ar 48000 ",
                                     '88200 Hz': "-ar 88200 ",
                                     '96000 Hz': "-ar 96000 "}
        acodec_samplerate.set(config_profile['FDK-AAC - SETTINGS']['samplerate'])  # set the default option
        acodec_samplerate_label = Label(audio_window, text="Sample Rate :", background="#434547", foreground="white")
        acodec_samplerate_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_samplerate_menu = OptionMenu(audio_window, acodec_samplerate, *acodec_samplerate_choices.keys())
        acodec_samplerate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_samplerate_menu.grid(row=3, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_samplerate_menu["menu"].configure(activebackground="dim grey")
        acodec_samplerate_menu.bind("<Enter>", acodec_samplerate_menu_hover)
        acodec_samplerate_menu.bind("<Leave>", acodec_samplerate_menu_hover_leave)

        # ------------------------------------------------------------------------------------------------- Sample Rate

        # Entry Box for Custom Command Line ---------------------------------------------------------------------------
        def fdkaac_cmd(*args):
            global fdkaac_custom_cmd_input
            if fdkaac_custom_cmd.get() == (""):
                fdkaac_custom_cmd_input = ("")
            else:
                cstmcmd = fdkaac_custom_cmd.get()
                fdkaac_custom_cmd_input = cstmcmd + " "

        fdkaac_custom_cmd = StringVar()
        fdkaac_cmd_entrybox_label = Label(audio_window, text="Custom Command Line :", anchor=W, background="#434547",
                                          foreground="white")
        fdkaac_cmd_entrybox_label.grid(row=11, column=0, columnspan=2, padx=10, pady=(0, 0), sticky=N + S + W + E)
        fdkaac_cmd_entrybox = Entry(audio_window, textvariable=fdkaac_custom_cmd, borderwidth=4, background="#CACACA")
        fdkaac_cmd_entrybox.grid(row=12, column=0, columnspan=3, padx=10, pady=(0, 0), sticky=W + E)
        fdkaac_custom_cmd.trace('w', fdkaac_cmd)
        fdkaac_custom_cmd.set("")

        # ----------------------------------------------------------------------------------------- Custom Command Line

        # Entry Box for Track Title -----------------------------------------------------------------------------------
        def fdkaac_title_check(*args):
            global fdkaac_title_input
            if fdkaac_title.get() == (""):
                fdkaac_title_input = ("")
            else:
                title_cmd = fdkaac_title.get()
                fdkaac_title_input = "--title " + '"' + title_cmd + '"' + " "

        fdkaac_title = StringVar()
        fdkaac_title_entrybox_label = Label(audio_window, text="Track Name :", anchor=W, background="#434547",
                                            foreground="white")
        fdkaac_title_entrybox_label.grid(row=13, column=0, columnspan=2, padx=10, pady=(5, 0), sticky=N + S + W + E)
        fdkaac_title_entrybox = Entry(audio_window, textvariable=fdkaac_title, borderwidth=4, background="#CACACA")
        fdkaac_title_entrybox.grid(row=14, column=0, columnspan=3, padx=10, pady=(0, 10), sticky=W + E)
        fdkaac_title.trace('w', fdkaac_title_check)
        fdkaac_title.set("")
        # ------------------------------------------------------------------------------------------------- Track Title

        # Audio Profile Selection -------------------------------------------------------------------------------------
        acodec_profile = StringVar(audio_window)
        acodec_profile_choices = {'AAC LC (Default)': "-p2 ",
                                  'HE-AAC SBR': "-p5 ",
                                  'HE-AAC V2 (SBR+PS)': "-p29 ",
                                  'AAC LD': "-p23 ",
                                  'AAC ELD': "-p39 "}
        acodec_profile.set(config_profile['FDK-AAC - SETTINGS']['fdk_aac_profile'])  # set the default option
        acodec_profile_label = Label(audio_window, text="Profile :", background="#434547", foreground="white")
        acodec_profile_label.grid(row=5, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_profile_menu = OptionMenu(audio_window, acodec_profile, *acodec_profile_choices.keys())
        acodec_profile_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_profile_menu.grid(row=6, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_profile_menu["menu"].configure(activebackground="dim grey")
        acodec_profile_menu.bind("<Enter>", acodec_profile_menu_hover)
        acodec_profile_menu.bind("<Leave>", acodec_profile_menu_hover_leave)
        # ------------------------------------------------------------------------------------------- Profile Selection

        # Audio Lowdelay SBR Selection --------------------------------------------------------------------------------
        global acodec_lowdelay
        global acodec_lowdelay_choices
        acodec_lowdelay = StringVar(audio_window)
        acodec_lowdelay_choices = {'Disable SBR on ELD (DEF)': "-L0 ",
                                   'ELD SBR Auto Conf': "-L-1 ",
                                   'Enable SBR on ELD': "-L1 "}
        acodec_lowdelay.set(config_profile['FDK-AAC - SETTINGS']['fdk_aac_lowdelay'])  # set the default option
        acodec_lowdelay_label = Label(audio_window, text="Lowdelay SBR :", background="#434547", foreground="white")
        acodec_lowdelay_label.grid(row=5, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_lowdelay_menu = OptionMenu(audio_window, acodec_lowdelay, *acodec_lowdelay_choices.keys())
        acodec_lowdelay_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_lowdelay_menu.grid(row=6, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_lowdelay_menu["menu"].configure(activebackground="dim grey")
        acodec_lowdelay_menu.bind("<Enter>", acodec_lowdelay_menu_hover)
        acodec_lowdelay_menu.bind("<Leave>", acodec_lowdelay_menu_hover_leave)
        # --------------------------------------------------------------------------------------------------- Low Delay

        # Audio SBR Ratio ---------------------------------------------------------------------------------------------
        global acodec_sbr_ratio
        global acodec_sbr_ratio_choices
        acodec_sbr_ratio = StringVar(audio_window)
        acodec_sbr_ratio_choices = {'Library Default': "-s0 ",
                                    'Downsampled SBR (ELD+SBR Def)': "-s1 ",
                                    'Dual-Rate SBR (HE-AAC-Def)': "-s2 "}
        acodec_sbr_ratio.set(config_profile['FDK-AAC - SETTINGS']['fdk_aac_sbr_ratio'])  # set the default option
        acodec_sbr_ratio_label = Label(audio_window, text="SBR Ratio :", background="#434547", foreground="white")
        acodec_sbr_ratio_label.grid(row=5, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_sbr_ratio_menu = OptionMenu(audio_window, acodec_sbr_ratio, *acodec_sbr_ratio_choices.keys())
        acodec_sbr_ratio_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_sbr_ratio_menu.grid(row=6, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_sbr_ratio_menu["menu"].configure(activebackground="dim grey")
        acodec_sbr_ratio_menu.bind("<Enter>", acodec_sbr_ratio_menu_hover)
        acodec_sbr_ratio_menu.bind("<Leave>", acodec_sbr_ratio_menu_hover_leave)
        # --------------------------------------------------------------------------------------------------- SBR Ratio

        # Audio Gapless Mode ------------------------------------------------------------------------------------------
        global acodec_gapless_mode
        global acodec_gapless_mode_choices
        acodec_gapless_mode = StringVar(audio_window)
        acodec_gapless_mode_choices = {'iTunSMPB (Def)': "-G0 ",
                                       'ISO Standard (EDTS+SGPD)': "-G1 ",
                                       'Both': "-G2 "}
        acodec_gapless_mode.set(config_profile['FDK-AAC - SETTINGS']['fdk_aac_gapless'])  # set the default option
        acodec_gapless_mode_label = Label(audio_window, text="SBR Ratio :", background="#434547", foreground="white")
        acodec_gapless_mode_label.grid(row=7, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_gapless_mode_menu = OptionMenu(audio_window, acodec_gapless_mode, *acodec_gapless_mode_choices.keys())
        acodec_gapless_mode_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_gapless_mode_menu.grid(row=8, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_gapless_mode_menu["menu"].configure(activebackground="dim grey")
        acodec_gapless_mode_menu.bind("<Enter>", acodec_gapless_mode_menu_hover)
        acodec_gapless_mode_menu.bind("<Leave>", acodec_gapless_mode_menu_hover_leave)
        # ------------------------------------------------------------------------------------------ Audio Gapless Mode

        # Audio Transport Format --------------------------------------------------------------------------------------
        global acodec_transport_format
        global acodec_transport_format_choices
        acodec_transport_format = StringVar(audio_window)
        acodec_transport_format_choices = {'M4A (Def)': "-f0 ",
                                           'ADIF': "-f1 ",
                                           'ADTS': "-f2 ",
                                           'LATM MCP=1': "-f6 ",
                                           'LATM MCP=0': "-f7 ",
                                           'LOAS/LATM (LATM w/in LOAS)': "-f10 "}
        acodec_transport_format.set(config_profile['FDK-AAC - SETTINGS']['fdk_aac_transport_format'])  # default option
        acodec_transport_format_label = Label(audio_window, text="Transport Format :", background="#434547",
                                              foreground="white")
        acodec_transport_format_label.grid(row=7, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_transport_format_menu = OptionMenu(audio_window, acodec_transport_format,
                                                  *acodec_transport_format_choices.keys())
        acodec_transport_format_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_transport_format_menu.grid(row=8, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_transport_format_menu["menu"].configure(activebackground="dim grey")
        acodec_transport_format_menu.bind("<Enter>", acodec_transport_format_menu_hover)
        acodec_transport_format_menu.bind("<Leave>", acodec_transport_format_menu_hover_leave)
        # --------------------------------------------------------------------------------------------------- Transport

        # Misc Checkboxes - Afterburner -------------------------------------------------------------------------------
        global afterburnervar
        afterburnervar = StringVar()
        afterburnervar.set(config_profile['FDK-AAC - SETTINGS']['fdk_aac_afterburner'] + ' ')
        afterburner_checkbox = Checkbutton(audio_window, text='Afterburner', variable=afterburnervar, onvalue="-a1 ",
                                           offvalue="-a0 ")
        afterburner_checkbox.grid(row=8, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        afterburner_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                       activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        # ------------------------------------------------------------------------------------------------- Afterburner

        # Misc Checkboxes - Add CRC Check on ADTS Header --------------------------------------------------------------
        global crccheck
        crccheck = StringVar()
        crccheck.set(config_profile['FDK-AAC - SETTINGS']['fdk_aac_crccheck'] + ' ')
        crccheck_checkbox = Checkbutton(audio_window, text='CRC Check on\n ADTS Header', variable=crccheck,
                                        onvalue="-C ", offvalue="")
        crccheck_checkbox.grid(row=9, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        crccheck_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                    activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        # --------------------------------------------------------------------------------------------------------- CRC

        # Misc Checkboxes - Header Period -----------------------------------------------------------------------------
        global headerperiod
        headerperiod = StringVar()
        headerperiod.set(config_profile['FDK-AAC - SETTINGS']['fdk_aac_headerperiod'] + ' ')
        headerperiod_checkbox = Checkbutton(audio_window, text='Header Period', variable=headerperiod,
                                            onvalue="-h ", offvalue="")
        headerperiod_checkbox.grid(row=9, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        headerperiod_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                        activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        # ------------------------------------------------------------------------------------------------------ Header

        # Misc Checkboxes - Include SBR Delay -------------------------------------------------------------------------
        global sbrdelay
        sbrdelay = StringVar()
        sbrdelay.set(config_profile['FDK-AAC - SETTINGS']['fdk_aac_sbrdelay'] + ' ')
        sbrdelay_checkbox = Checkbutton(audio_window, text='SBR Delay', variable=sbrdelay,
                                        onvalue="--include-sbr-delay ", offvalue="")
        sbrdelay_checkbox.grid(row=9, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        sbrdelay_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                    activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        # --------------------------------------------------------------------------------------------------- SBR Delay

        # Misc Checkboxes - Place Moov Box Before Mdat Box ------------------------------------------------------------
        global moovbox
        moovbox = StringVar()
        moovbox.set(config_profile['FDK-AAC - SETTINGS']['fdk_aac_moovbox'] + ' ')
        moovbox_checkbox = Checkbutton(audio_window, text='Place Moov Box Before Mdat Box', variable=moovbox,
                                       onvalue="--moov-before-mdat ", offvalue="")
        moovbox_checkbox.grid(row=10, column=0, columnspan=2, padx=10, pady=3, sticky=N + S + E + W)
        moovbox_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                   activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        # ---------------------------------------------------------------------------------------------------- Moov Box

        # Audio Atempo Selection ---------------------------------------------------------------------------------------
        acodec_atempo = StringVar(audio_window)
        acodec_atempo_choices = {'Original': '',
                                 '23.976 to 24': '"atempo=23.976/24"',
                                 '23.976 to 25': '"atempo=23.976/25"',
                                 '24 to 23.976': '"atempo=24/23.976"',
                                 '24 to 25': '"atempo=24/25"',
                                 '25 to 23.976': '"atempo=25/23.976"',
                                 '25 to 24': '"atempo=25/24"',
                                 '1/4 Slow-down': '"atempo=0.5,atempo=0.5"',
                                 '1/2 Slow-down': '"atempo=0.5"',
                                 '3/4 Slow-down': '"atempo=0.75"',
                                 '1/4 Speed-up': '"atempo=1.25"',
                                 '1/2 Speed-up': '"atempo=1.5"',
                                 '3/4 Speed-up': '"atempo=1.75"',
                                 '2x Speed-up': '"atempo=2.0"',
                                 '2.5x Speed-up': '"atempo=2.5"',
                                 '3x Speed-up': '"atempo=3.0"',
                                 '3.5x Speed-up': '"atempo=3.5"',
                                 '4x Speed-up': '"atempo=4.0"'}
        acodec_atempo_menu_label = Label(audio_window, text="Time Modification :", background="#434547",
                                         foreground="white")
        acodec_atempo_menu_label.grid(row=2, column=2, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_atempo_menu = OptionMenu(audio_window, acodec_atempo, *acodec_atempo_choices.keys())
        acodec_atempo_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_atempo_menu.grid(row=3, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_atempo.set(config_profile['FDK-AAC - SETTINGS']['fdk_aac_tempo'])
        acodec_atempo_menu["menu"].configure(activebackground="dim grey")
        acodec_atempo_menu.bind("<Enter>", acodec_atempo_menu_hover)
        acodec_atempo_menu.bind("<Leave>", acodec_atempo_menu_hover_leave)
        # ------------------------------------------------------------------------------------------------ Audio Atempo
    # --------------------------------------------------------------------------------------------------------- FDK AAC

    # QAAC Window -----------------------------------------------------------------------------------------------------
    elif encoder.get() == "QAAC":
        audio_window = Toplevel()
        audio_window.title('QAAC Settings')
        audio_window.configure(background="#434547")
        window_height = 700
        window_width = 750
        screen_width = audio_window.winfo_screenwidth()
        screen_height = audio_window.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

        my_menu_bar = Menu(audio_window, tearoff=0)
        audio_window.config(menu=my_menu_bar)
        file_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
        my_menu_bar.add_cascade(label='Track Tools', menu=file_menu)
        file_menu.add_command(label='View Audio Tracks', command=show_streams_mediainfo)
        file_menu.add_command(label='Play Selected Audio Track  |  9 and 0 for Volume',
                              command=mpv_gui_audio_window)
        options_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
        my_menu_bar.add_cascade(label='Options', menu=options_menu)
        options_menu.add_command(label='Save Current Settings', command=save_profile)
        options_menu.add_command(label='Reset Settings To Default', command=reset_profile)

        for n in range(3):
            audio_window.grid_columnconfigure(n, weight=1)
        for n in range(11):
            audio_window.grid_rowconfigure(n, weight=1)
        audio_window.grid_rowconfigure(15, weight=1)

        # Gets gain information for QAAC ------------------------------------------------------------------------------
        def qaac_gain_trace(*args):
            global set_qaac_gain
            if q_acodec_gain.get() == '0':
                set_qaac_gain = ''
            elif q_acodec_gain.get() != '0':
                set_qaac_gain = '--gain ' + q_acodec_gain.get() + ' '

        # ----------------------------------------------------------------------------------------------- QAAC Get Gain

        # Help --------------------------------------------------------------------------------------------------------
        def gotoqaachelp():
            helpfile_window = Toplevel(audio_window)
            helpfile_window.title("QAAC Advanced Settings Help")
            helpfile_window.configure(background="#434547")
            Label(helpfile_window, text="Advanced Settings Information",
                  font=("Times New Roman", 14), background='#434547', foreground="white").grid(column=0, row=0)
            helpfile_window.grid_columnconfigure(0, weight=1)
            helpfile_window.grid_rowconfigure(0, weight=1)
            text_area = scrolledtextwidget.ScrolledText(helpfile_window, width=80, height=25)
            text_area.grid(column=0, pady=10, padx=10)
            with open("Apps/qaac/qaac information.txt", "r") as helpfile:
                text_area.insert(INSERT, helpfile.read())
                text_area.configure(font=("Helvetica", 14))
                text_area.configure(state=DISABLED)

        # -------------------------------------------------------------------------------------------------------- Help

        # Views Command -----------------------------------------------------------------------------------------------
        def view_command():
            global cmd_label
            global cmd_line_window
            audio_filter_function()
            if q_acodec_profile.get() == "True VBR":
                example_cmd_output = acodec_stream_choices[acodec_stream.get()] + acodec_channel_choices[
                    acodec_channel.get()] + acodec_samplerate_choices[acodec_samplerate.get()] \
                                     + audio_filter_setting \
                                     + "\n \n" + "-f wav - | " + qaac + " " + "\n \n" \
                                     + q_acodec_profile_choices[q_acodec_profile.get()] + q_acodec_quality_amnt.get() \
                                     + " " + qaac_high_efficiency.get() + qaac_nodither.get() \
                                     + set_qaac_gain + \
                                     q_acodec_quality_choices[q_acodec_quality.get()] + qaac_normalize.get() \
                                     + qaac_nodelay.get() + q_gapless_mode_choices[q_gapless_mode.get()] \
                                     + qaac_nooptimize.get() + qaac_threading.get() + qaac_limiter.get() \
                                     + qaac_title_input + qaac_custom_cmd_input
            else:
                example_cmd_output = acodec_stream_choices[acodec_stream.get()] + \
                                     acodec_channel_choices[acodec_channel.get()] + \
                                     acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting \
                                     + "\n \n" + "-f wav - | " + qaac + " " + "\n \n" \
                                     + q_acodec_profile_choices[q_acodec_profile.get()] + \
                                     q_acodec_bitrate.get() + " " + qaac_high_efficiency.get() \
                                     + qaac_nodither.get() + set_qaac_gain + \
                                     q_acodec_quality_choices[q_acodec_quality.get()] + qaac_normalize.get() \
                                     + qaac_nodelay.get() \
                                     + q_gapless_mode_choices[q_gapless_mode.get()] + qaac_nooptimize.get() \
                                     + qaac_threading.get() + qaac_limiter.get() + qaac_title_input \
                                     + qaac_custom_cmd_input
            try:
                cmd_label.config(text=example_cmd_output)
                cmd_line_window.deiconify()
            except (AttributeError, NameError):
                cmd_line_window = Toplevel()
                cmd_line_window.title('Command Line')
                cmd_line_window.configure(background="#434547")
                cmd_label = Label(cmd_line_window, text=example_cmd_output, foreground="white", background="#434547")
                cmd_label.config(font=("Helvetica", 16))
                cmd_label.winfo_exists()
                cmd_label.pack()

                def hide_instead():
                    cmd_line_window.withdraw()

                cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

        # ----------------------------------------------------------------------------------------------- Views Command
        # Buttons -----------------------------------------------------------------------------------------------------
        apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A",
                              command=gotosavefile)
        apply_button.grid(row=16, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        apply_button.bind("<Enter>", apply_button_hover)
        apply_button.bind("<Leave>", apply_button_hover_leave)

        show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A",
                          command=view_command)
        show_cmd.grid(row=16, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        show_cmd.bind("<Enter>", show_cmd_hover)
        show_cmd.bind("<Leave>", show_cmd_hover_leave)

        help_button = Button(audio_window, text="Help + Information", foreground="white", background="#23272A",
                             command=gotoqaachelp)
        help_button.grid(row=16, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        help_button.bind("<Enter>", help_button_hover)
        help_button.bind("<Leave>", help_button_hover_leave)
        # ----------------------------------------------------------------------------------------------------- Buttons

        advanced_label = Label(audio_window,
                               text="- - - - - - - - - - - - - - - - - - - - Advanced Settings - - - - - - - - - - - "
                                    "- - - - - - - - -",
                               background="#434547", foreground="white", relief=GROOVE)
        advanced_label.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky=W + E)

        # Quality or Bitrate ------------------------------------------------------------------------------------------
        def quality_or_bitrate(*args):
            if q_acodec_profile.get() == 'True VBR':
                q_acodec_quality_spinbox.configure(state=NORMAL)
                q_acodec_bitrate_spinbox.configure(state=DISABLED)
                qaac_high_efficiency.set("")
                qaac_high_efficiency_checkbox.configure(state=DISABLED)
            elif q_acodec_profile.get() != 'True VBR':
                qaac_high_efficiency.set(config_profile['FFMPEG QAAC - SETTINGS']['qaac_high_efficiency'] + ' ')
                q_acodec_quality_spinbox.configure(state=DISABLED)
                q_acodec_bitrate_spinbox.configure(state=NORMAL)
                qaac_high_efficiency_checkbox.configure(state=NORMAL)

        # ------------------------------------------------------------------------------------------ Quality or Bitrate

        # Audio Channel Selection -------------------------------------------------------------------------------------
        acodec_channel = StringVar(audio_window)
        acodec_channel_choices = {'Original': "",
                                  '1 (Mono)': "-ac 1 ",
                                  '2 (Stereo)': "-ac 2 ",
                                  '5.1 (Surround)': "-ac 6 ",
                                  '6.1 (Surround)': "-ac 7 ",
                                  '7.1 (Surround)': "-ac 8 "}
        achannel_menu_label = Label(audio_window, text="Channels :", background="#434547", foreground="white")
        achannel_menu_label.grid(row=0, column=1, columnspan=1, padx=10, pady=3, sticky=W + E)
        achannel_menu = OptionMenu(audio_window, acodec_channel, *acodec_channel_choices.keys())
        achannel_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        achannel_menu.grid(row=1, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        achannel_menu["menu"].configure(activebackground="dim grey")
        achannel_menu.bind("<Enter>", achannel_menu_hover)
        achannel_menu.bind("<Leave>", achannel_menu_hover_leave)
        acodec_channel.set(config_profile['FFMPEG QAAC - SETTINGS']['acodec_channel'])
        acodec_channel.trace('w', dolby_pro_logic_ii_enable_disable)
        # ----------------------------------------------------------------------------------------------- Audio Channel

        # Dolby Pro Logic II ------------------------------------------------------------------------------------------
        dolby_pro_logic_ii = StringVar()
        dolby_pro_logic_ii_checkbox = Checkbutton(audio_window, text=' Dolby Pro\nLogic II',
                                                  variable=dolby_pro_logic_ii, state=DISABLED,
                                                  onvalue='"aresample=matrix_encoding=dplii"', offvalue="")
        if acodec_channel.get() == '2 (Stereo)':
            dolby_pro_logic_ii_checkbox.configure(state=NORMAL)
        dolby_pro_logic_ii_checkbox.grid(row=5, column=2, columnspan=1, rowspan=1, padx=10, pady=3,
                                         sticky=N + S + E + W)
        dolby_pro_logic_ii_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                              activeforeground="white", selectcolor="#434547", font=("Helvetica", 11))
        dolby_pro_logic_ii.set(config_profile['FFMPEG QAAC - SETTINGS']['dolbyprologicii'])
        # ------------------------------------------------------------------------------------------------------ DPL II

        # Audio Stream Selection --------------------------------------------------------------------------------------
        acodec_stream = StringVar(audio_window)
        acodec_stream_choices = acodec_stream_track_counter
        acodec_stream.set(next(iter(acodec_stream_track_counter)))  # set the default option
        acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
        acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
        acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=12, anchor='w')
        acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_stream_menu["menu"].configure(activebackground="dim grey")
        acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
        acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)
        acodec_stream.trace('w', track_number_mpv)
        track_number_mpv()
        # ------------------------------------------------------------------------------------------------ Audio Stream

        # Entry Box for Custom Command Line ---------------------------------------------------------------------------
        def qaac_cmd(*args):
            global qaac_custom_cmd_input
            if qaac_custom_cmd.get() == (""):
                qaac_custom_cmd_input = ("")
            else:
                cstmcmd = qaac_custom_cmd.get()
                qaac_custom_cmd_input = cstmcmd + " "

        qaac_custom_cmd = StringVar()
        qaac_cmd_entrybox_label = Label(audio_window, text="Custom Command Line :", anchor=W, background="#434547",
                                        foreground="white")
        qaac_cmd_entrybox_label.grid(row=12, column=0, columnspan=2, padx=10, pady=(0, 0), sticky=N + S + W + E)
        qaac_cmd_entrybox = Entry(audio_window, textvariable=qaac_custom_cmd, borderwidth=4, background="#CACACA")
        qaac_cmd_entrybox.grid(row=13, column=0, columnspan=3, padx=10, pady=(0, 0), sticky=W + E)
        qaac_custom_cmd.trace('w', qaac_cmd)
        qaac_custom_cmd.set("")

        # ----------------------------------------------------------------------------------------- Custom Command Line

        # Entry Box for Track Title -----------------------------------------------------------------------------------
        def qaac_title_check(*args):
            global qaac_title_input
            if qaac_title.get() == (""):
                qaac_title_input = ("")
            else:
                title_cmd = qaac_title.get()
                qaac_title_input = "--title " + '"' + title_cmd + '"' + " "

        qaac_title = StringVar()
        qaac_title_entrybox_label = Label(audio_window, text="Track Name :", anchor=W, background="#434547",
                                          foreground="white")
        qaac_title_entrybox_label.grid(row=14, column=0, columnspan=2, padx=10, pady=(5, 0), sticky=N + S + W + E)
        qaac_title_entrybox = Entry(audio_window, textvariable=qaac_title, borderwidth=4, background="#CACACA")
        qaac_title_entrybox.grid(row=15, column=0, columnspan=3, padx=10, pady=(0, 10), sticky=W + E)
        qaac_title.trace('w', qaac_title_check)
        qaac_title.set("")
        # ------------------------------------------------------------------------------------------------- Track Title

        # Audio Sample Rate Selection ---------------------------------------------------------------------------------
        acodec_samplerate = StringVar(audio_window)
        acodec_samplerate_choices = {'Original': "",
                                     '11025 Hz': "-ar 11025 ",
                                     '22050 Hz': "-ar 22050 ",
                                     '44100 Hz': "-ar 44100 ",
                                     '48000 Hz': "-ar 48000 ",
                                     '88200 Hz': "-ar 88200 ",
                                     '96000 Hz': "-ar 96000 "}
        acodec_samplerate.set(config_profile['FFMPEG QAAC - SETTINGS']['samplerate'])  # set the default option
        acodec_samplerate_label = Label(audio_window, text="Sample Rate :", background="#434547", foreground="white")
        acodec_samplerate_label.grid(row=4, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_samplerate_menu = OptionMenu(audio_window, acodec_samplerate, *acodec_samplerate_choices.keys())
        acodec_samplerate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_samplerate_menu.grid(row=5, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_samplerate_menu["menu"].configure(activebackground="dim grey")
        acodec_samplerate_menu.bind("<Enter>", acodec_samplerate_menu_hover)
        acodec_samplerate_menu.bind("<Leave>", acodec_samplerate_menu_hover_leave)
        # -------------------------------------------------------------------------------------------------- Samplerate

        # Audio Quality Selection -------------------------------------------------------------------------------------
        global q_acodec_quality
        global q_acodec_quality_choices
        q_acodec_quality = StringVar(audio_window)
        q_acodec_quality_choices = {'High (Default)': "",
                                    'Medium': "--quality 1 ",
                                    'Low': "--quality 0 "}
        q_acodec_quality.set(config_profile['FFMPEG QAAC - SETTINGS']['q_acodec_quality'])  # set the default option
        q_acodec_quality_label = Label(audio_window, text="Quality :", background="#434547", foreground="white")
        q_acodec_quality_label.grid(row=0, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        q_acodec_quality_menu = OptionMenu(audio_window, q_acodec_quality, *q_acodec_quality_choices.keys())
        q_acodec_quality_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        q_acodec_quality_menu.grid(row=1, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        q_acodec_quality_menu["menu"].configure(activebackground="dim grey")
        q_acodec_quality_menu.bind("<Enter>", q_acodec_quality_menu_hover)
        q_acodec_quality_menu.bind("<Leave>", q_acodec_quality_menu_hover_leave)
        # -------------------------------------------------------------------------------------------------------------

        # Audio Quality Spinbox ---------------------------------------------------------------------------------------
        global q_acodec_quality_amnt
        q_acodec_quality_amnt = StringVar(audio_window)
        q_acodec_quality_amnt_choices = ('0', '9', '18', '27', '36', '45', '54', '63', '73',
                                        '82', '91', '100', '109', '118', '127')
        q_acodec_quality_spinbox_label = Label(audio_window, text="T-VBR Quality :", background="#434547",
                                               foreground="white")
        q_acodec_quality_spinbox_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        q_acodec_quality_spinbox = Spinbox(audio_window, values=q_acodec_quality_amnt_choices, justify=CENTER,
                                           wrap=True, textvariable=q_acodec_quality_amnt, width=13, state='readonly')
        q_acodec_quality_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                        buttonbackground="black", disabledbackground='grey',
                                        readonlybackground="#23272A")
        q_acodec_quality_spinbox.grid(row=3, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        q_acodec_quality_amnt.set(config_profile['FFMPEG QAAC - SETTINGS']['q_acodec_quality_amnt'])
        # ----------------------------------------------------------------------------------------------------- Quality

        # Audio Bitrate -----------------------------------------------------------------------------------------------
        global q_acodec_bitrate
        q_acodec_bitrate = StringVar(audio_window)
        q_acodec_bitrate.set(int(config_profile['FFMPEG QAAC - SETTINGS']['q_acodec_bitrate']))  # set default
        q_acodec_bitrate_label = Label(audio_window, text="Bitrate :", background="#434547", foreground="white")
        q_acodec_bitrate_label.grid(row=2, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        q_acodec_bitrate_spinbox = Spinbox(audio_window, from_=0, to=1280, justify=CENTER, wrap=True,
                                           textvariable=q_acodec_bitrate, width=13)
        q_acodec_bitrate_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                        buttonbackground="black", disabledbackground='grey')
        q_acodec_bitrate_spinbox.grid(row=3, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        def disable_enable_bitrate():
            if q_acodec_profile.get() == 'True VBR':
                q_acodec_bitrate_spinbox.configure(state=DISABLED)
        # ----------------------------------------------------------------------------------------------------- Bitrate

        # QAAC Gain ---------------------------------------------------------------------------------------------------
        global q_acodec_gain
        q_acodec_gain = StringVar(audio_window)
        q_acodec_gain_label = Label(audio_window, text="Gain :", background="#434547", foreground="white")
        q_acodec_gain_label.grid(row=4, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        q_acodec_gain_spinbox = Spinbox(audio_window, from_=-100, to=100, justify=CENTER, wrap=True,
                                        textvariable=q_acodec_gain, width=13)
        q_acodec_gain_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                     buttonbackground="black", disabledbackground='grey')
        q_acodec_gain_spinbox.grid(row=5, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        q_acodec_gain.trace('w', qaac_gain_trace)
        q_acodec_gain.set(int(config_profile['FFMPEG QAAC - SETTINGS']['q_acodec_gain']))
        # -------------------------------------------------------------------------------------------------------- Gain

        # Misc Checkboxes - Normalize ---------------------------------------------------------------------------------
        global qaac_normalize
        qaac_normalize = StringVar()
        qaac_normalize.set(config_profile['FFMPEG QAAC - SETTINGS']['qaac_normalize'] + ' ')
        qaac_normalize_checkbox = Checkbutton(audio_window, text='Normalize', variable=qaac_normalize,
                                              onvalue="--normalize ", offvalue="")
        qaac_normalize_checkbox.grid(row=10, column=1, columnspan=1, padx=10, pady=(10,3), sticky=N + S + E + W)
        qaac_normalize_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                          activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        # --------------------------------------------------------------------------------------------------- Normalize

        # Misc Checkboxes - High Efficiency ---------------------------------------------------------------------------
        global qaac_high_efficiency
        qaac_high_efficiency = StringVar()
        qaac_high_efficiency_checkbox = Checkbutton(audio_window, text='High Efficiency', variable=qaac_high_efficiency,
                                                    onvalue="--he ", offvalue="", state=DISABLED)
        qaac_high_efficiency_checkbox.grid(row=8, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        qaac_high_efficiency_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                                activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        qaac_high_efficiency.set(config_profile['FFMPEG QAAC - SETTINGS']['qaac_high_efficiency'] + ' ')
        def enable_disable_he():
            if q_acodec_profile.get() != 'True VBR':
                qaac_high_efficiency_checkbox.configure(state=NORMAL)
        # --------------------------------------------------------------------------------------------- High Effeciency

        # Audio Profile Menu ------------------------------------------------------------------------------------------
        global q_acodec_profile
        global q_acodec_profile_choices
        q_acodec_profile = StringVar(audio_window)
        q_acodec_profile_choices = {'True VBR': "--tvbr ",
                                    'Constrained VBR': "--cvbr ",
                                    'ABR': "--abr ",
                                    'CBR': "--cbr "}
        q_acodec_profile.trace('w', quality_or_bitrate)
        q_acodec_profile.set(config_profile['FFMPEG QAAC - SETTINGS']['q_acodec_profile'])  # set the default option
        q_acodec_profile_menu_label = Label(audio_window, text="Mode :", background="#434547", foreground="white")
        q_acodec_profile_menu_label.grid(row=2, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
        q_acodec_profile_menu = OptionMenu(audio_window, q_acodec_profile, *q_acodec_profile_choices.keys())
        q_acodec_profile_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        q_acodec_profile_menu.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        q_acodec_profile_menu["menu"].configure(activebackground="dim grey")
        q_acodec_profile_menu.bind("<Enter>", q_acodec_profile_hover)
        q_acodec_profile_menu.bind("<Leave>", q_acodec_profile_hover_leave)
        enable_disable_he()
        disable_enable_bitrate()
        # ------------------------------------------------------------------------------------------ Audio Profile Menu

        # Misc Checkboxes - No Dither When Quantizing to Lower Bit Depth ----------------------------------------------
        global qaac_nodither
        qaac_nodither = StringVar()
        qaac_nodither.set(config_profile['FFMPEG QAAC - SETTINGS']['qaac_nodither'] + ' ')
        qaac_nodither_checkbox = Checkbutton(audio_window, text='No Dither',
                                             variable=qaac_nodither, onvalue="--no-dither ", offvalue="")
        qaac_nodither_checkbox.grid(row=7, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        qaac_nodither_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                         activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        # --------------------------------------------------------------------------------------------------- No Dither

        # Misc Checkboxes - No Delay ----------------------------------------------------------------------------------
        global qaac_nodelay
        qaac_nodelay = StringVar()
        qaac_nodelay.set(config_profile['FFMPEG QAAC - SETTINGS']['qaac_nodelay'] + ' ')
        qaac_nodelay_checkbox = Checkbutton(audio_window, text='No Delay',
                                            variable=qaac_nodelay, onvalue="--no-delay ", offvalue="")
        qaac_nodelay_checkbox.grid(row=7, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        qaac_nodelay_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                        activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        # ---------------------------------------------------------------------------------------------------- No Delay

        # Gapless Mode ------------------------------------------------------------------------------------------------
        global q_gapless_mode
        global q_gapless_mode_choices
        q_gapless_mode = StringVar(audio_window)
        q_gapless_mode_choices = {'iTunSMPB (Default)': "",
                                  'ISO standard': "--gapless-mode 1 ",
                                  'Both': "--gapless-mode 2 "}
        q_gapless_mode.set(config_profile['FFMPEG QAAC - SETTINGS']['q_gapless_mode'])  # set the default option
        q_gapless_mode_label = Label(audio_window, text="Gapless Mode :", background="#434547", foreground="white")
        q_gapless_mode_label.grid(row=8, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        q_gapless_mode_menu = OptionMenu(audio_window, q_gapless_mode, *q_gapless_mode_choices.keys())
        q_gapless_mode_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        q_gapless_mode_menu.grid(row=9, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        q_gapless_mode_menu["menu"].configure(activebackground="dim grey")
        q_gapless_mode_menu.bind("<Enter>", q_gapless_mode_menu_hover)
        q_gapless_mode_menu.bind("<Leave>", q_gapless_mode_menu_hover_leave)
        # ------------------------------------------------------------------------------------------------ Gapless Mode

        # Misc Checkboxes - No Optimize -------------------------------------------------------------------------------
        global qaac_nooptimize
        qaac_nooptimize = StringVar()
        qaac_nooptimize.set(config_profile['FFMPEG QAAC - SETTINGS']['qaac_nooptimize'] + ' ')
        qaac_nooptimize_checkbox = Checkbutton(audio_window, text='No Optimize',
                                               variable=qaac_nooptimize, onvalue="--no-optimize ", offvalue="")
        qaac_nooptimize_checkbox.grid(row=7, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        qaac_nooptimize_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                           activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        # ------------------------------------------------------------------------------------------------- No Optimize

        # Misc Checkboxes - Threading ---------------------------------------------------------------------------------
        global qaac_threading
        qaac_threading = StringVar()
        qaac_threading.set(config_profile['FFMPEG QAAC - SETTINGS']['qaac_threading'] + ' ')
        qaac_threading_checkbox = Checkbutton(audio_window, text='Threading',
                                              variable=qaac_threading, onvalue="--threading ", offvalue="")
        qaac_threading_checkbox.grid(row=10, column=0, columnspan=1, padx=10, pady=(10,3), sticky=N + S + E + W)
        qaac_threading_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                          activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        # --------------------------------------------------------------------------------------------------- Threading

        # Misc Checkboxes - Limiter -----------------------------------------------------------------------------------
        global qaac_limiter
        qaac_limiter = StringVar()
        qaac_limiter.set(config_profile['FFMPEG QAAC - SETTINGS']['qaac_limiter'] + ' ')
        qaac_limiter_checkbox = Checkbutton(audio_window, text='Limiter',
                                            variable=qaac_limiter, onvalue="--limiter ", offvalue="")
        qaac_limiter_checkbox.grid(row=9, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        qaac_limiter_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                        activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        # ----------------------------------------------------------------------------------------------------- Limiter

        # Audio Atempo Selection ---------------------------------------------------------------------------------------
        acodec_atempo = StringVar(audio_window)
        acodec_atempo_choices = {'Original': '',
                                 '23.976 to 24': '"atempo=23.976/24"',
                                 '23.976 to 25': '"atempo=23.976/25"',
                                 '24 to 23.976': '"atempo=24/23.976"',
                                 '24 to 25': '"atempo=24/25"',
                                 '25 to 23.976': '"atempo=25/23.976"',
                                 '25 to 24': '"atempo=25/24"',
                                 '1/4 Slow-down': '"atempo=0.5,atempo=0.5"',
                                 '1/2 Slow-down': '"atempo=0.5"',
                                 '3/4 Slow-down': '"atempo=0.75"',
                                 '1/4 Speed-up': '"atempo=1.25"',
                                 '1/2 Speed-up': '"atempo=1.5"',
                                 '3/4 Speed-up': '"atempo=1.75"',
                                 '2x Speed-up': '"atempo=2.0"',
                                 '2.5x Speed-up': '"atempo=2.5"',
                                 '3x Speed-up': '"atempo=3.0"',
                                 '3.5x Speed-up': '"atempo=3.5"',
                                 '4x Speed-up': '"atempo=4.0"'}
        acodec_atempo_menu_label = Label(audio_window, text="Time Modification :", background="#434547",
                                         foreground="white")
        acodec_atempo_menu_label.grid(row=8, column=1, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_atempo_menu = OptionMenu(audio_window, acodec_atempo, *acodec_atempo_choices.keys())
        acodec_atempo_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_atempo_menu.grid(row=9, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_atempo.set(config_profile['FFMPEG QAAC - SETTINGS']['tempo'])
        acodec_atempo_menu["menu"].configure(activebackground="dim grey")
        acodec_atempo_menu.bind("<Enter>", acodec_atempo_menu_hover)
        acodec_atempo_menu.bind("<Leave>", acodec_atempo_menu_hover_leave)
        # ------------------------------------------------------------------------------------------------ Audio Atempo
    # ----------------------------------------------------------------------------------------------------------- QAAC

    # FLAC Window -----------------------------------------------------------------------------------------------------
    if encoder.get() == "FLAC":
        try:
            audio_window.deiconify()
        except:
            audio_window = Toplevel()
            audio_window.title('FLAC Settings')
            audio_window.configure(background="#434547")
            window_height = 550
            window_width = 650
            screen_width = audio_window.winfo_screenwidth()
            screen_height = audio_window.winfo_screenheight()
            x_coordinate = int((screen_width / 2) - (window_width / 2))
            y_coordinate = int((screen_height / 2) - (window_height / 2))
            audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

            my_menu_bar = Menu(audio_window, tearoff=0)
            audio_window.config(menu=my_menu_bar)
            file_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
            my_menu_bar.add_cascade(label='Track Tools', menu=file_menu)
            file_menu.add_command(label='View Audio Tracks', command=show_streams_mediainfo)
            file_menu.add_command(label='Play Selected Audio Track  |  9 and 0 for Volume',
                                  command=mpv_gui_audio_window)
            options_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
            my_menu_bar.add_cascade(label='Options', menu=options_menu)
            options_menu.add_command(label='Save Current Settings', command=save_profile)
            options_menu.add_command(label='Reset Settings To Default', command=reset_profile)

            for n in range(3):
                audio_window.grid_columnconfigure(n, weight=1)
            for n in [0, 1, 2, 3, 4, 6, 7, 10]:
                audio_window.grid_rowconfigure(n, weight=1)

            # Views Command -------------------------------------------------------------------------------------------
            def view_command():
                global cmd_line_window
                global cmd_label
                audio_filter_function()
                example_cmd_output = acodec_stream_choices[acodec_stream.get()] \
                                     + encoder_dropdownmenu_choices[encoder.get()] + \
                                     acodec_bitrate_choices[acodec_bitrate.get()] + \
                                     acodec_channel_choices[acodec_channel.get()] + \
                                     acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting \
                                     + set_flac_acodec_coefficient \
                                     + acodec_flac_lpc_type_choices[acodec_flac_lpc_type.get()] \
                                     + acodec_flac_lpc_passes_choices[acodec_flac_lpc_passes.get()] \
                                     + flac_custom_cmd_input
                try:
                    cmd_label.config(text=example_cmd_output)
                    cmd_line_window.deiconify()
                except (AttributeError, NameError):
                    cmd_line_window = Toplevel()
                    cmd_line_window.title('Command Line')
                    cmd_line_window.configure(background="#434547")
                    cmd_label = Label(cmd_line_window, text=example_cmd_output, foreground="white",
                                      background="#434547")
                    cmd_label.config(font=("Helvetica", 16))
                    cmd_label.pack()

                    def hide_instead():
                        cmd_line_window.withdraw()

                    cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

            # ------------------------------------------------------------------------------------------- Views Command

            # Buttons -------------------------------------------------------------------------------------------------
            apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A",
                                  command=gotosavefile)
            apply_button.grid(row=10, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            apply_button.bind("<Enter>", apply_button_hover)
            apply_button.bind("<Leave>", apply_button_hover_leave)

            show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A",
                              command=view_command)
            show_cmd.grid(row=10, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            show_cmd.bind("<Enter>", show_cmd_hover)
            show_cmd.bind("<Leave>", show_cmd_hover_leave)
            # ------------------------------------------------------------------------------------------------- Buttons

            advanced_label = Label(audio_window,
                                   text="- - - - - - - - - - - - - - - - - - - - Advanced Settings - - - - - "
                                        "- - - - - - - - - - - - - - -",
                                   background="#434547", foreground="white", relief=GROOVE)
            advanced_label.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky=W + E)

            # Audio Bitrate Selection ---------------------------------------------------------------------------------
            acodec_bitrate = StringVar(audio_window)
            acodec_bitrate_choices = {'Level 0 - Best Quality': "-compression_level 0 ",
                                      'Level 1 ......': "-compression_level 1 ",
                                      'Level 2 ......': "-compression_level 2 ",
                                      'Level 3 ......': "-compression_level 3 ",
                                      'Level 4 ......': "-compression_level 4 ",
                                      'Level 5 - Default Quality': "",
                                      'Level 6 ......': "-compression_level 6 ",
                                      'Level 7 ......': "-compression_level 7 ",
                                      'Level 8 ......': "-compression_level 8 ",
                                      'Level 9 ......': "-compression_level 9 ",
                                      'Level 10 ......': "-compression_level 10 ",
                                      'Level 11 ......': "-compression_level 11 ",
                                      'Level 12 - Lowest Quality': "-compression_level 12 "}
            acodec_bitrate.set(config_profile['FFMPEG FLAC - SETTINGS']['acodec_bitrate'])  # set the default option
            acodec_bitrate_menu_label = Label(audio_window, text="Compression Level :", background="#434547",
                                              foreground="white")
            acodec_bitrate_menu_label.grid(row=0, column=2, columnspan=1, padx=10, pady=3, sticky=W + E)
            acodec_bitrate_menu = OptionMenu(audio_window, acodec_bitrate, *acodec_bitrate_choices.keys())
            acodec_bitrate_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=15)
            acodec_bitrate_menu.grid(row=1, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            acodec_bitrate_menu["menu"].configure(activebackground="dim grey")
            acodec_bitrate_menu.bind("<Enter>", acodec_bitrate_menu_hover)
            acodec_bitrate_menu.bind("<Leave>", acodec_bitrate_menu_hover_leave)
            # ------------------------------------------------------------------------------------------- Audio Bitrate

            # Audio Stream Selection ----------------------------------------------------------------------------------
            acodec_stream = StringVar(audio_window)
            acodec_stream_choices = acodec_stream_track_counter
            acodec_stream.set(next(iter(acodec_stream_track_counter)))  # set the default option
            acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
            acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
            acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
            acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1,
                                      width=15, anchor='w')
            acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            acodec_stream_menu["menu"].configure(activebackground="dim grey")
            acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
            acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)
            acodec_stream.trace('w', track_number_mpv)
            track_number_mpv()
            # ---------------------------------------------------------------------------------------------------------

            # Audio Channel Selection ---------------------------------------------------------------------------------
            acodec_channel = StringVar(audio_window)
            acodec_channel_choices = {'Original': "",
                                      '1 (Mono)': "-ac 1 ",
                                      '2 (Stereo)': "-ac 2 ",
                                      '5.0 (Surround)': "-ac 5 ",
                                      '5.1 (Surround)': "-ac 6 ",
                                      '6.1 (Surround)': "-ac 7 ",
                                      '7.1 (Surround)': "-ac 8 "}
            acodec_channel.set(config_profile['FFMPEG FLAC - SETTINGS']['acodec_channel'])  # set the default option
            achannel_menu_label = Label(audio_window, text="Channels :", background="#434547", foreground="white")
            achannel_menu_label.grid(row=0, column=1, columnspan=1, padx=10, pady=3, sticky=W + E)
            achannel_menu = OptionMenu(audio_window, acodec_channel, *acodec_channel_choices.keys())
            achannel_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=15)
            achannel_menu.grid(row=1, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            achannel_menu["menu"].configure(activebackground="dim grey")
            achannel_menu.bind("<Enter>", achannel_menu_hover)
            achannel_menu.bind("<Leave>", achannel_menu_hover_leave)
            acodec_channel.trace('w', dolby_pro_logic_ii_enable_disable)
            # ----------------------------------------------------------------------------------------------- Audio Channel

            # Dolby Pro Logic II ------------------------------------------------------------------------------------------
            dolby_pro_logic_ii = StringVar()
            dolby_pro_logic_ii_checkbox = Checkbutton(audio_window, text=' Dolby Pro\nLogic II',
                                                      variable=dolby_pro_logic_ii, state=DISABLED,
                                                      onvalue='"aresample=matrix_encoding=dplii"', offvalue="")
            if acodec_channel.get() == '2 (Stereo)':
                dolby_pro_logic_ii_checkbox.configure(state=NORMAL)
            dolby_pro_logic_ii_checkbox.grid(row=4, column=2, columnspan=1, rowspan=1, padx=10, pady=(20, 5),
                                             sticky=N + S + E + W)
            dolby_pro_logic_ii_checkbox.configure(background="#434547", foreground="white",
                                                  activebackground="#434547",
                                                  activeforeground="white", selectcolor="#434547",
                                                  font=("Helvetica", 11))
            dolby_pro_logic_ii.set(config_profile['FFMPEG FLAC - SETTINGS']['dolbyprologicii'])
            # -------------------------------------------------------------------------------------------------- DPL II

            # Audio Gain Selection ------------------------------------------------------------------------------------
            ffmpeg_gain = StringVar()
            ffmpeg_gain_label = Label(audio_window, text="Gain (dB) :", background="#434547", foreground="white")
            ffmpeg_gain_label.grid(row=2, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            ffmpeg_gain_spinbox = Spinbox(audio_window, from_=-30, to=30, increment=1.0, justify=CENTER,
                                          wrap=True, textvariable=ffmpeg_gain)
            ffmpeg_gain_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                          buttonbackground="black", width=15, readonlybackground="#23272A")
            ffmpeg_gain_spinbox.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            ffmpeg_gain.set(int(config_profile['FFMPEG FLAC - SETTINGS']['gain']))
            # ---------------------------------------------------------------------------------------------------- Gain

            # Audio Sample Rate Selection -----------------------------------------------------------------------------
            acodec_samplerate = StringVar(audio_window)
            acodec_samplerate_choices = {'Original': "",
                                         '8000 Hz': "-ar 8000 ",
                                         '11025 Hz': "-ar 11025 ",
                                         '22050 Hz': "-ar 22050 ",
                                         '32000 Hz': "-ar 32000 ",
                                         '44100 Hz': "-ar 44100 ",
                                         '48000 Hz': "-ar 48000 ",
                                         '96000 Hz': "-ar 96000 "}
            acodec_samplerate.set(config_profile['FFMPEG FLAC - SETTINGS']['samplerate'])  # set the default option
            acodec_samplerate_label = Label(audio_window, text="Sample Rate :", background="#434547",
                                            foreground="white")
            acodec_samplerate_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_samplerate_menu = OptionMenu(audio_window, acodec_samplerate, *acodec_samplerate_choices.keys())
            acodec_samplerate_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=15)
            acodec_samplerate_menu.grid(row=3, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_samplerate_menu["menu"].configure(activebackground="dim grey")
            acodec_samplerate_menu.bind("<Enter>", acodec_samplerate_menu_hover)
            acodec_samplerate_menu.bind("<Leave>", acodec_samplerate_menu_hover_leave)
            # --------------------------------------------------------------------------------------------- Sample Rate

            # Entry Box for Custom Command Line -----------------------------------------------------------------------
            def flac_cmd(*args):
                global flac_custom_cmd_input
                if flac_custom_cmd.get() == (""):
                    flac_custom_cmd_input = ("")
                else:
                    cstmcmd = flac_custom_cmd.get()
                    flac_custom_cmd_input = cstmcmd + " "

            flac_custom_cmd = StringVar()
            flac_cmd_entrybox_label = Label(audio_window, text="Custom Command Line :", anchor=W,
                                           background="#434547",
                                           foreground="white")
            flac_cmd_entrybox_label.grid(row=8, column=0, columnspan=2, padx=10, pady=(15, 0), sticky=N + S + W + E)
            flac_cmd_entrybox = Entry(audio_window, textvariable=flac_custom_cmd, borderwidth=4, background="#CACACA")
            flac_cmd_entrybox.grid(row=9, column=0, columnspan=3, padx=10, pady=(0, 15), sticky=W + E)
            flac_custom_cmd.trace('w', flac_cmd)
            flac_custom_cmd.set("")
            # ------------------------------------------------------------------------------------- Custom Command Line

            # Audio Atempo Selection ----------------------------------------------------------------------------------
            acodec_atempo = StringVar(audio_window)
            acodec_atempo_choices = {'Original': '',
                                     '23.976 to 24': '"atempo=23.976/24"',
                                     '23.976 to 25': '"atempo=23.976/25"',
                                     '24 to 23.976': '"atempo=24/23.976"',
                                     '24 to 25': '"atempo=24/25"',
                                     '25 to 23.976': '"atempo=25/23.976"',
                                     '25 to 24': '"atempo=25/24"',
                                     '1/4 Slow-down': '"atempo=0.5,atempo=0.5"',
                                     '1/2 Slow-down': '"atempo=0.5"',
                                     '3/4 Slow-down': '"atempo=0.75"',
                                     '1/4 Speed-up': '"atempo=1.25"',
                                     '1/2 Speed-up': '"atempo=1.5"',
                                     '3/4 Speed-up': '"atempo=1.75"',
                                     '2x Speed-up': '"atempo=2.0"',
                                     '2.5x Speed-up': '"atempo=2.5"',
                                     '3x Speed-up': '"atempo=3.0"',
                                     '3.5x Speed-up': '"atempo=3.5"',
                                     '4x Speed-up': '"atempo=4.0"'}
            acodec_atempo_menu_label = Label(audio_window, text="Time Modification :", background="#434547",
                                             foreground="white")
            acodec_atempo_menu_label.grid(row=2, column=2, columnspan=1, padx=10, pady=3, sticky=W + E)
            acodec_atempo_menu = OptionMenu(audio_window, acodec_atempo, *acodec_atempo_choices.keys())
            acodec_atempo_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=15)
            acodec_atempo_menu.grid(row=3, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            acodec_atempo.set(config_profile['FFMPEG FLAC - SETTINGS']['tempo'])
            acodec_atempo_menu["menu"].configure(activebackground="dim grey")
            acodec_atempo_menu.bind("<Enter>", acodec_atempo_menu_hover)
            acodec_atempo_menu.bind("<Leave>", acodec_atempo_menu_hover_leave)
        # ------------------------------------------------------------------------------------------------ Audio Atempo

            # LPC Algorithm Selection ---------------------------------------------------------------------------------
            global acodec_flac_lpc_type, acodec_flac_lpc_type_choices
            acodec_flac_lpc_type = StringVar(audio_window)
            acodec_flac_lpc_type_choices = {'Default': "",
                                         'None': "-lpc_type 0 ",
                                         'Fixed': "-lpc_type 1 ",
                                         'Levinson': "-lpc_type 2 ",
                                         'Cholesky': "-lpc_type 3 "}
            acodec_flac_lpc_type.set(config_profile['FFMPEG FLAC - SETTINGS']['flac_lpc_type'])  # set the default
            acodec_flac_lpc_type_label = Label(audio_window, text="LPC Algorithm :", background="#434547",
                                            foreground="white")
            acodec_flac_lpc_type_label.grid(row=6, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_flac_lpc_type_menu = OptionMenu(audio_window, acodec_flac_lpc_type,
                                                   *acodec_flac_lpc_type_choices.keys())
            acodec_flac_lpc_type_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=15)
            acodec_flac_lpc_type_menu.grid(row=7, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_flac_lpc_type_menu["menu"].configure(activebackground="dim grey")
            acodec_flac_lpc_type_menu.bind("<Enter>", acodec_flac_lpc_type_menu_hover)
            acodec_flac_lpc_type_menu.bind("<Leave>", acodec_flac_lpc_type_menu_hover_leave)

            # ------------------------------------------------------------------------------------------- LPC Algorithm

            # FLAC LPC Coefficient Precision --------------------------------------------------------------------------
            def flac_acodec_coefficient_trace(*args):
                global set_flac_acodec_coefficient
                if flac_acodec_coefficient.get() == '15':
                    set_flac_acodec_coefficient = ''
                elif flac_acodec_coefficient.get() != '15':
                    set_flac_acodec_coefficient = '-lpc_coeff_precision ' + flac_acodec_coefficient.get() + ' '

            global flac_acodec_coefficient
            flac_acodec_coefficient = StringVar(audio_window)
            flac_acodec_coefficient_label = Label(audio_window, text="LPC Coefficient Precision :", background="#434547",
                                                  foreground="white")
            flac_acodec_coefficient_label.grid(row=6, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            flac_acodec_coefficient_spinbox = Spinbox(audio_window, from_=0, to=15, justify=CENTER, wrap=True,
                                            textvariable=flac_acodec_coefficient, width=13)
            flac_acodec_coefficient_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                         buttonbackground="black", disabledbackground='grey')
            flac_acodec_coefficient_spinbox.grid(row=7, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            flac_acodec_coefficient.trace('w', flac_acodec_coefficient_trace)
            flac_acodec_coefficient.set(int(config_profile['FFMPEG FLAC - SETTINGS']['flac_coefficient']))
            # -------------------------------------------------------------------------- FLAC LPC Coefficient Precision

            # LPC Passes ----------------------------------------------------------------------------------------------
            global acodec_flac_lpc_passes, acodec_flac_lpc_passes_choices
            acodec_flac_lpc_passes = StringVar(audio_window)
            acodec_flac_lpc_passes_choices = {'Default': "",
                                              '2 Passes': "-lpc_passes 2 ",
                                              '3 Passes': "-lpc_passes 3 ",
                                              '4 Passes': "-lpc_passes 4 ",
                                              '5 Passes': "-lpc_passes 5 ",
                                              '6 Passes': "-lpc_passes 6 ",
                                              '7 Passes': "-lpc_passes 7 ",
                                              '8 Passes': "-lpc_passes 8 ",
                                              '9 Passes': "-lpc_passes 9 ",
                                              '10 Passes': "-lpc_passes 10 "}
            acodec_flac_lpc_passes.set(config_profile['FFMPEG FLAC - SETTINGS']['flac_lpc_passes'])
            acodec_flac_lpc_passes_label = Label(audio_window, text="LPC Passes :", background="#434547",
                                            foreground="white")
            acodec_flac_lpc_passes_label.grid(row=6, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_flac_lpc_passes_menu = OptionMenu(audio_window, acodec_flac_lpc_passes,
                                                     *acodec_flac_lpc_passes_choices.keys())
            acodec_flac_lpc_passes_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=15)
            acodec_flac_lpc_passes_menu.grid(row=7, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_flac_lpc_passes_menu["menu"].configure(activebackground="dim grey")
            acodec_flac_lpc_passes_menu.bind("<Enter>", acodec_flac_lpc_passes_menu_hover)
            acodec_flac_lpc_passes_menu.bind("<Leave>", acodec_flac_lpc_passes_menu_hover_leave)

            # ---------------------------------------------------------------------------------------------- LPC Passes
        # -------------------------------------------------------------------------------------------------------- FLAC

    # ALAC Window -------------------------------------------------------------------------------------------------
    if encoder.get() == "ALAC":
        try:
            audio_window.deiconify()
        except:
            audio_window = Toplevel()
            audio_window.title('ALAC Settings')
            audio_window.configure(background="#434547")
            window_height = 470
            window_width = 650
            screen_width = audio_window.winfo_screenwidth()
            screen_height = audio_window.winfo_screenheight()
            x_coordinate = int((screen_width / 2) - (window_width / 2))
            y_coordinate = int((screen_height / 2) - (window_height / 2))
            audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

            for n in range(3):
                audio_window.grid_columnconfigure(n, weight=1)
            for n in range(4):
                audio_window.grid_rowconfigure(n, weight=1)
            for n in [5, 6, 10]:
                audio_window.grid_rowconfigure(n, weight=1)

            my_menu_bar = Menu(audio_window, tearoff=0)
            audio_window.config(menu=my_menu_bar)
            file_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
            my_menu_bar.add_cascade(label='Track Tools', menu=file_menu)
            file_menu.add_command(label='View Audio Tracks', command=show_streams_mediainfo)
            file_menu.add_command(label='Play Selected Audio Track  |  9 and 0 for Volume',
                                  command=mpv_gui_audio_window)
            options_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
            my_menu_bar.add_cascade(label='Options', menu=options_menu)
            options_menu.add_command(label='Save Current Settings', command=save_profile)
            options_menu.add_command(label='Reset Settings To Default', command=reset_profile)

            # Views Command ---------------------------------------------------------------------------------------
            def view_command():
                global cmd_line_window
                global cmd_label
                audio_filter_function()
                example_cmd_output = acodec_stream_choices[acodec_stream.get()] \
                                     + encoder_dropdownmenu_choices[encoder.get()] + \
                                     acodec_channel_choices[acodec_channel.get()] + \
                                     acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting \
                                     + min_pre_order + max_pre_order + flac_custom_cmd_input
                try:
                    cmd_label.config(text=example_cmd_output)
                    cmd_line_window.deiconify()
                except (AttributeError, NameError):
                    cmd_line_window = Toplevel()
                    cmd_line_window.title('Command Line')
                    cmd_line_window.configure(background="#434547")
                    cmd_label = Label(cmd_line_window, text=example_cmd_output, foreground="white",
                                      background="#434547")
                    cmd_label.config(font=("Helvetica", 16))
                    cmd_label.pack()

                    def hide_instead():
                        cmd_line_window.withdraw()

                    cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

            # --------------------------------------------------------------------------------------- Views Command

            # Buttons ---------------------------------------------------------------------------------------------
            apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A",
                                  command=gotosavefile)
            apply_button.grid(row=10, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            apply_button.bind("<Enter>", apply_button_hover)
            apply_button.bind("<Leave>", apply_button_hover_leave)

            show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A",
                              command=view_command)
            show_cmd.grid(row=10, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            show_cmd.bind("<Enter>", show_cmd_hover)
            show_cmd.bind("<Leave>", show_cmd_hover_leave)
            # --------------------------------------------------------------------------------------------- Buttons

            advanced_label = Label(audio_window,
                                   text="- - - - - - - - - - - - - - - - - - - - Advanced Settings - - - - - "
                                        "- - - - - - - - - - - - - - -",
                                   background="#434547", foreground="white", relief=GROOVE)
            advanced_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky=W + E)

            # Audio Stream Selection ------------------------------------------------------------------------------
            acodec_stream = StringVar(audio_window)
            acodec_stream_choices = acodec_stream_track_counter
            acodec_stream.set(next(iter(acodec_stream_track_counter)))
            acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
            acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
            acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
            acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1,
                                      width=15, anchor='w')
            acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            acodec_stream_menu["menu"].configure(activebackground="dim grey")
            acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
            acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)
            acodec_stream.trace('w', track_number_mpv)
            track_number_mpv()
            # -----------------------------------------------------------------------------------------------------

            # Audio Channel Selection -----------------------------------------------------------------------------
            acodec_channel = StringVar(audio_window)
            acodec_channel_choices = {'Original': "",
                                      '1 (Mono)': "-ac 1 ",
                                      '2 (Stereo)': "-ac 2 ",
                                      '3': "-ac 3 ",
                                      '4': "-ac 4 ",
                                      '5.0 (Surround)': "-ac 5 ",
                                      '5.1 (Surround)': "-ac 6 ",
                                      '6.1 (Surround)': "-ac 7 ",
                                      '7.1 (Surround)': "-ac 8 "}
            acodec_channel.set(config_profile['FFMPEG ALAC - SETTINGS']['acodec_channel'])  # set the default option
            achannel_menu_label = Label(audio_window, text="Channels :", background="#434547",
                                        foreground="white")
            achannel_menu_label.grid(row=0, column=1, columnspan=1, padx=10, pady=3, sticky=W + E)
            achannel_menu = OptionMenu(audio_window, acodec_channel, *acodec_channel_choices.keys())
            achannel_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=15)
            achannel_menu.grid(row=1, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            achannel_menu["menu"].configure(activebackground="dim grey")
            achannel_menu.bind("<Enter>", achannel_menu_hover)
            achannel_menu.bind("<Leave>", achannel_menu_hover_leave)
            acodec_channel.trace('w', dolby_pro_logic_ii_enable_disable)
            # --------------------------------------------------------------------------------------- Audio Channel

            # Dolby Pro Logic II ----------------------------------------------------------------------------------
            dolby_pro_logic_ii = StringVar()
            dolby_pro_logic_ii_checkbox = Checkbutton(audio_window, text=' Dolby Pro\nLogic II',
                                                      variable=dolby_pro_logic_ii, state=DISABLED,
                                                      onvalue='"aresample=matrix_encoding=dplii"', offvalue="")
            if acodec_channel.get() == '2 (Stereo)':
                dolby_pro_logic_ii_checkbox.configure(state=NORMAL)
            dolby_pro_logic_ii_checkbox.grid(row=0, column=2, columnspan=1, rowspan=2, padx=10, pady=(20, 5),
                                             sticky=N + S + E + W)
            dolby_pro_logic_ii_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                                  activeforeground="white", selectcolor="#434547",
                                                  font=("Helvetica", 11))
            dolby_pro_logic_ii.set(config_profile['FFMPEG ALAC - SETTINGS']['dolbyprologicii'])
            # ---------------------------------------------------------------------------------------------- DPL II

            # Audio Gain Selection --------------------------------------------------------------------------------
            ffmpeg_gain = StringVar()
            ffmpeg_gain_label = Label(audio_window, text="Gain (dB) :", background="#434547",
                                      foreground="white")
            ffmpeg_gain_label.grid(row=2, column=0, columnspan=1, padx=10, pady=3,
                                   sticky=N + S + E + W)
            ffmpeg_gain_spinbox = Spinbox(audio_window, from_=-30, to=30, increment=1.0, justify=CENTER,
                                          wrap=True, textvariable=ffmpeg_gain)
            ffmpeg_gain_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                          buttonbackground="black", width=15, readonlybackground="#23272A")
            ffmpeg_gain_spinbox.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            ffmpeg_gain.set(int(config_profile['FFMPEG ALAC - SETTINGS']['gain']))
            # ------------------------------------------------------------------------------------------------ Gain

            # Audio Sample Rate Selection -------------------------------------------------------------------------
            acodec_samplerate = StringVar(audio_window)
            acodec_samplerate_choices = {'Original': "",
                                         '8000 Hz': "-ar 8000 ",
                                         '11025 Hz': "-ar 11025 ",
                                         '22050 Hz': "-ar 22050 ",
                                         '32000 Hz': "-ar 32000 ",
                                         '44100 Hz': "-ar 44100 ",
                                         '48000 Hz': "-ar 48000 ",
                                         '96000 Hz': "-ar 96000 "}
            acodec_samplerate.set(config_profile['FFMPEG ALAC - SETTINGS']['samplerate'])  # set the default
            acodec_samplerate_label = Label(audio_window, text="Sample Rate :", background="#434547",
                                            foreground="white")
            acodec_samplerate_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_samplerate_menu = OptionMenu(audio_window, acodec_samplerate,
                                                *acodec_samplerate_choices.keys())
            acodec_samplerate_menu.config(background="#23272A", foreground="white", highlightthickness=1,
                                          width=15)
            acodec_samplerate_menu.grid(row=3, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_samplerate_menu["menu"].configure(activebackground="dim grey")
            acodec_samplerate_menu.bind("<Enter>", acodec_samplerate_menu_hover)
            acodec_samplerate_menu.bind("<Leave>", acodec_samplerate_menu_hover_leave)
            # ----------------------------------------------------------------------------------------- Sample Rate

            # Entry Box for Custom Command Line -------------------------------------------------------------------
            def flac_cmd(*args):
                global flac_custom_cmd_input
                if flac_custom_cmd.get() == (""):
                    flac_custom_cmd_input = ("")
                else:
                    cstmcmd = flac_custom_cmd.get()
                    flac_custom_cmd_input = cstmcmd + " "

            flac_custom_cmd = StringVar()
            flac_cmd_entrybox_label = Label(audio_window, text="Custom Command Line :", anchor=W,
                                            background="#434547",
                                            foreground="white")
            flac_cmd_entrybox_label.grid(row=8, column=0, columnspan=2, padx=10, pady=(15, 0),
                                         sticky=N + S + W + E)
            flac_cmd_entrybox = Entry(audio_window, textvariable=flac_custom_cmd, borderwidth=4,
                                      background="#CACACA")
            flac_cmd_entrybox.grid(row=9, column=0, columnspan=3, padx=10, pady=(0, 15), sticky=W + E)
            flac_custom_cmd.trace('w', flac_cmd)
            flac_custom_cmd.set("")
            # --------------------------------------------------------------------------------- Custom Command Line

            # Audio Atempo Selection ------------------------------------------------------------------------------
            acodec_atempo = StringVar(audio_window)
            acodec_atempo_choices = {'Original': '',
                                     '23.976 to 24': '"atempo=23.976/24"',
                                     '23.976 to 25': '"atempo=23.976/25"',
                                     '24 to 23.976': '"atempo=24/23.976"',
                                     '24 to 25': '"atempo=24/25"',
                                     '25 to 23.976': '"atempo=25/23.976"',
                                     '25 to 24': '"atempo=25/24"',
                                     '1/4 Slow-down': '"atempo=0.5,atempo=0.5"',
                                     '1/2 Slow-down': '"atempo=0.5"',
                                     '3/4 Slow-down': '"atempo=0.75"',
                                     '1/4 Speed-up': '"atempo=1.25"',
                                     '1/2 Speed-up': '"atempo=1.5"',
                                     '3/4 Speed-up': '"atempo=1.75"',
                                     '2x Speed-up': '"atempo=2.0"',
                                     '2.5x Speed-up': '"atempo=2.5"',
                                     '3x Speed-up': '"atempo=3.0"',
                                     '3.5x Speed-up': '"atempo=3.5"',
                                     '4x Speed-up': '"atempo=4.0"'}
            acodec_atempo_menu_label = Label(audio_window, text="Time Modification :", background="#434547",
                                             foreground="white")
            acodec_atempo_menu_label.grid(row=2, column=2, columnspan=1, padx=10, pady=3, sticky=W + E)
            acodec_atempo_menu = OptionMenu(audio_window, acodec_atempo, *acodec_atempo_choices.keys())
            acodec_atempo_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=15)
            acodec_atempo_menu.grid(row=3, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            acodec_atempo.set(config_profile['FFMPEG ALAC - SETTINGS']['tempo'])
            acodec_atempo_menu["menu"].configure(activebackground="dim grey")
            acodec_atempo_menu.bind("<Enter>", acodec_atempo_menu_hover)
            acodec_atempo_menu.bind("<Leave>", acodec_atempo_menu_hover_leave)
        # -------------------------------------------------------------------------------------------- Audio Atempo

        # Min-Prediction-Order ------------------------------------------------------------------------------------
        def get_min_pre_order(*args):
            global min_pre_order
            if min_prediction_order.get() == '4':
                min_pre_order = ''
            elif min_prediction_order.get() != '4':
                min_pre_order = '-min_prediction_order ' + min_prediction_order.get() + ' '

        min_prediction_order = StringVar(audio_window)
        min_prediction_order_label = Label(audio_window, text="Min-Prediction-Order :",
                                           background="#434547", foreground="white")
        min_prediction_order_label.grid(row=5, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        min_prediction_order_spinbox = Spinbox(audio_window, from_=1, to=30, justify=CENTER, wrap=True,
                                               textvariable=min_prediction_order, width=13)
        min_prediction_order.trace('w', get_min_pre_order)
        min_prediction_order.set(int(config_profile['FFMPEG ALAC - SETTINGS']['alac_min_prediction_order']))
        min_prediction_order_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                            buttonbackground="black", disabledbackground='grey')
        min_prediction_order_spinbox.grid(row=6, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        # ------------------------------------------------------------------------------------ Min-Prediction-Order

        # Max-Prediction-Order ------------------------------------------------------------------------------------
        def get_max_pre_order(*args):
            global max_pre_order
            if max_prediction_order.get() == '6':
                max_pre_order = ''
            elif max_prediction_order.get() != '6':
                max_pre_order = '-max_prediction_order ' + max_prediction_order.get() + ' '

        max_prediction_order = StringVar(audio_window)
        max_prediction_order_label = Label(audio_window, text="Max-Prediction-Order :",
                                           background="#434547", foreground="white")
        max_prediction_order_label.grid(row=5, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        max_prediction_order_spinbox = Spinbox(audio_window, from_=1, to=30, justify=CENTER, wrap=True,
                                               textvariable=max_prediction_order, width=13)
        max_prediction_order.trace('w', get_max_pre_order)
        max_prediction_order.set(int(config_profile['FFMPEG ALAC - SETTINGS']['alac_max_prediction_order']))
        max_prediction_order_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                            buttonbackground="black", disabledbackground='grey')
        max_prediction_order_spinbox.grid(row=6, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        # ------------------------------------------------------------------------------------ Max-Prediction-Order
    # -------------------------------------------------------------------------------------------------------- ALAC

# ---------------------------------------------------------------------------------------------- End Audio Codec Window

# File Input ----------------------------------------------------------------------------------------------------------
def file_input():
    global VideoInput
    global VideoInputQuoted
    global VideoOutput
    global VideoOutputQuoted
    global autofilesave_dir_path
    global track_count
    VideoInput = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                            filetypes=((
                                                       "AAC, AC3, AVI, DTS, M4A, M4V, MKA, MKV, MOV, MP3, MP4, MPEG, "
                                                       "MT2S, OGG, OGV, VOB, WAV, WEBM, FLAC, ALAC, EAC3, OPUS, AAX",
                                                       "*.aac *.ac3 *.avi *.dts *.m4a *.m4v *.mka *.mkv *.mov *.mp3 "
                                                       "*.mp4 *.mpeg *.mt2s *.ogg *.ogv *.vob *.wav *.webm *.flac "
                                                       "*.alac *.eac3 *.opus *.aax"),
                                                       ("All Files", "*.*")))
    input_entry.configure(state=NORMAL)
    input_entry.delete(0, END)
    file_extension = pathlib.Path(VideoInput).suffix
    supported_extensions = ['.wav', '.mt2s', '.ac3', '.mka', '.mp3', '.aac', '.ogg', '.ogv', '.m4v', '.mpeg', '.avi',
                            '.vob', '.webm', '.mp4', '.mkv', '.dts', '.m4a', '.mov', '.flac', '.alac', '.eac3',
                            '.opus', '.aax']
    if VideoInput:
        if file_extension in supported_extensions:
            autofilesave_file_path = pathlib.PureWindowsPath(VideoInput)  # Command to get file input location
            # Final command to get only the directory of fileinput
            autofilesave_dir_path = autofilesave_file_path.parents[0]
            VideoInputQuoted = '"' + VideoInput + '"'
            encoder_menu.config(state=NORMAL)
            # This gets the total amount of audio streams
            mediainfocli_cmd = '"' + mediainfocli + " " + '--Output="General;%AudioCount%"' \
                               + " " + VideoInputQuoted + '"'
            mediainfo_count = subprocess.Popen('cmd /c ' + mediainfocli_cmd, creationflags=subprocess.CREATE_NO_WINDOW,
                                               universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                               stdin=subprocess.PIPE)
            stdout, stderr = mediainfo_count.communicate()
            track_count = stdout
            input_entry.configure(state=NORMAL)
            input_entry.insert(0, VideoInput)
            input_entry.configure(state=DISABLED)
            output_entry.configure(state=NORMAL)
            output_entry.delete(0, END)
            output_entry.configure(state=DISABLED)
        else:
            messagebox.showinfo(title="Wrong File Type",
                                message="Try Again With a Supported File Type!\n\nIf this is a "
                                        "file that should be supported, please let me know.")
    if not VideoInput:
        input_entry.configure(state=NORMAL)
        input_entry.delete(0, END)
        input_entry.configure(state=DISABLED)
        output_button.config(state=DISABLED)
        encoder_menu.config(state=DISABLED)
        audiosettings_button.configure(state=DISABLED)
        auto_encode_last_options.configure(state=DISABLED)


# ---------------------------------------------------------------------------------------------------------- File Input

# File Output ---------------------------------------------------------------------------------------------------------
def file_save():
    global VideoOutput
    if encoder.get() == "AAC" or config_profile['Auto Encode']['codec'] == 'AAC':
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".mp4", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location", initialfile=autosavefilename,
                                                   filetypes=(("AAC", "*.mp4"), ("All Files", "*.*")))
    elif encoder.get() == "AC3" or config_profile['Auto Encode']['codec'] == 'AC3':
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".ac3", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location", initialfile=autosavefilename,
                                                   filetypes=(("AC3", "*.ac3"), ("All Files", "*.*")))
    elif encoder.get() == "DTS" or config_profile['Auto Encode']['codec'] == 'DTS':
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".dts", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location", initialfile=autosavefilename,
                                                   filetypes=(("DTS", "*.dts"), ("All Files", "*.*")))
    elif encoder.get() == "Opus" or config_profile['Auto Encode']['codec'] == 'Opus':
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".opus", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location", initialfile=autosavefilename,
                                                   filetypes=(("Opus", "*.opus"), ("All Files", "*.*")))
    elif encoder.get() == "MP3" or config_profile['Auto Encode']['codec'] == 'MP3':
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".mp3", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location", initialfile=autosavefilename,
                                                   filetypes=(("MP3", "*.mp3"), ("All Files", "*.*")))
    elif encoder.get() == "E-AC3" or config_profile['Auto Encode']['codec'] == 'E-AC3':
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".ac3", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location", initialfile=autosavefilename,
                                                   filetypes=(("E-AC3", "*.ac3"), ("All Files", "*.*")))
    elif encoder.get() == "FDK-AAC" or config_profile['Auto Encode']['codec'] == 'FDK-AAC':
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".m4a", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location", initialfile=autosavefilename,
                                                   filetypes=(("AAC", "*.m4a"), ("All Files", "*.*")))
    elif encoder.get() == "QAAC" or config_profile['Auto Encode']['codec'] == 'QAAC':
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".m4a", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location", initialfile=autosavefilename,
                                                   filetypes=(("AAC", "*.m4a"), ("All Files", "*.*")))

    elif encoder.get() == "FLAC" or config_profile['Auto Encode']['codec'] == 'FLAC':
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".flac", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location", initialfile=autosavefilename,
                                                   filetypes=(("FLAC", "*.flac"), ("All Files", "*.*")))

    elif encoder.get() == "ALAC" or config_profile['Auto Encode']['codec'] == 'ALAC':
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".m4a", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location", initialfile=autosavefilename,
                                                   filetypes=(("ALAC", "*.m4a"), ("All Files", "*.*")))

    if VideoOutput:
        output_entry.configure(state=NORMAL)  # Enable entry box for commands under
        output_entry.delete(0, END)  # Remove current text in entry
        output_entry.insert(0, VideoOutput)  # Insert the 'path'
        output_entry.configure(state=DISABLED)  # Disables Entry Box


# --------------------------------------------------------------------------------------------------------- File Output
def input_button_hover(e):
    input_button["bg"] = "grey"


def input_button_hover_leave(e):
    input_button["bg"] = "#23272A"


def output_button_hover(e):
    output_button["bg"] = "grey"


def output_button_hover_leave(e):
    output_button["bg"] = "#23272A"

def audiosettings_button_hover(e):
    audiosettings_button["bg"] = "grey"


def audiosettings_button_hover_leave(e):
    audiosettings_button["bg"] = "#23272A"


def auto_encode_last_options_hover(e):
    auto_encode_last_options["bg"] = "grey"


def auto_encode_last_options_hover_leave(e):
    auto_encode_last_options["bg"] = "#23272A"

def start_audio_button_hover(e):
    start_audio_button["bg"] = "grey"


def start_audio_button_hover_leave(e):
    start_audio_button["bg"] = "#23272A"


def command_line_button_hover(e):
    command_line_button["bg"] = "grey"


def command_line_button_hover_leave(e):
    command_line_button["bg"] = "#23272A"


def encoder_menu_hover(e):
    encoder_menu["bg"] = "grey"
    encoder_menu["activebackground"] = "grey"


def encoder_menu_hover_leave(e):
    encoder_menu["bg"] = "#23272A"


# Print Command Line from ROOT ----------------------------------------------------------------------------------------
def print_command_line():
    cmd_line_window = Toplevel()
    cmd_line_window.title('Command Line')
    cmd_line_window.configure(background="#434547")
    VideoInputQuoted = '"' + VideoInput + '"'
    VideoOutputQuoted = '"' + VideoOutput + '"'
    audio_filter_function()
    # DTS Command Line Main Gui ---------------------------------------------------------------------------------------
    if encoder.get() == "DTS":
        if dts_settings.get() == 'DTS Encoder':
            example_cmd_output = "ffmpeg.exe -analyzeduration 100M -probesize 50M -i " + "\n \n" + VideoInputQuoted + \
                                 "\n \n" + acodec_stream_choices[acodec_stream.get()] \
                                 + dts_settings_choices[dts_settings.get()] + "-b:a " + dts_bitrate_spinbox.get() \
                                 + "k " + acodec_channel_choices[acodec_channel.get()] \
                                 + acodec_samplerate_choices[acodec_samplerate.get()] \
                                 + audio_filter_setting + dts_custom_cmd_input \
                                 + "\n \n" + VideoOutputQuoted
        else:
            example_cmd_output = "ffmpeg.exe -analyzeduration 100M -probesize 50M -i " + "\n \n" + VideoInputQuoted \
                                 + "\n \n" + acodec_stream_choices[acodec_stream.get()] \
                                 + dts_settings_choices[dts_settings.get()] \
                                 + dts_custom_cmd_input + "\n \n" + VideoOutputQuoted
    # --------------------------------------------------------------------------------------- DTS Command Line Main Gui
    # FDK View Command Line -------------------------------------------------------------------------------------------
    elif encoder.get() == "FDK-AAC":
        example_cmd_output = "ffmpeg.exe -analyzeduration 100M -probesize 50M -i " + "\n \n" + \
                             VideoInputQuoted + "\n \n" + \
                             acodec_stream_choices[acodec_stream.get()] + \
                             acodec_channel_choices[acodec_channel.get()] + \
                             acodec_samplerate_choices[acodec_samplerate.get()] + \
                             audio_filter_setting + \
                             "-f caf - | " + "\n \n" + "fdkaac.exe" + " " + \
                             acodec_profile_choices[acodec_profile.get()] + afterburnervar.get() + fdkaac_title_input \
                             + fdkaac_custom_cmd_input + \
                             crccheck.get() + moovbox.get() + sbrdelay.get() + headerperiod.get() + \
                             acodec_lowdelay_choices[acodec_lowdelay.get()] + \
                             acodec_sbr_ratio_choices[acodec_sbr_ratio.get()] + \
                             acodec_transport_format_choices[acodec_transport_format.get()] + \
                             acodec_bitrate_choices[acodec_bitrate.get()] + "- -o " + "\n \n" + VideoOutputQuoted
    # ---------------------------------------------------------------------------------------------------- FDK CMD LINE
    # QAAC View Command Line ------------------------------------------------------------------------------------------
    elif encoder.get() == "QAAC":
        if q_acodec_profile.get() == "True VBR":
            example_cmd_output = ffmpeg + " -analyzeduration 100M -probesize 50M -i " + "\n \n" \
                                 + VideoInputQuoted + "\n \n" + \
                                 acodec_stream_choices[acodec_stream.get()] + acodec_channel_choices[
                                     acodec_channel.get()] + audio_filter_setting + \
                                 acodec_samplerate_choices[acodec_samplerate.get()] \
                                 + "\n \n" + "-f wav - | " + qaac + " " + "\n \n" \
                                 + q_acodec_profile_choices[q_acodec_profile.get()] + q_acodec_quality_amnt.get() \
                                 + " " + qaac_high_efficiency.get() + qaac_normalize.get() + qaac_nodither.get() \
                                 + set_qaac_gain + q_acodec_quality_choices[q_acodec_quality.get()] \
                                 + qaac_nodelay.get() + q_gapless_mode_choices[q_gapless_mode.get()] \
                                 + qaac_nooptimize.get() + qaac_threading.get() + qaac_limiter.get() \
                                 + qaac_title_input + qaac_custom_cmd_input + "- -o " + "\n \n" + VideoOutputQuoted
        else:
            example_cmd_output = ffmpeg + " -analyzeduration 100M -probesize 50M -i " + "\n \n" \
                                 + VideoInputQuoted + "\n \n" + \
                                 acodec_stream_choices[acodec_stream.get()] + \
                                 acodec_channel_choices[acodec_channel.get()] + audio_filter_setting + \
                                 acodec_samplerate_choices[acodec_samplerate.get()] \
                                 + "\n \n" + "-f wav - | " + qaac + " " + "\n \n" \
                                 + q_acodec_profile_choices[q_acodec_profile.get()] + \
                                 q_acodec_bitrate.get() + " " + qaac_high_efficiency.get() + qaac_nodither.get() \
                                 + set_qaac_gain + q_acodec_quality_choices[q_acodec_quality.get()] \
                                 + qaac_normalize.get() + qaac_nodelay.get() \
                                 + q_gapless_mode_choices[q_gapless_mode.get()] + qaac_nooptimize.get() \
                                 + qaac_threading.get() + qaac_limiter.get() + qaac_title_input \
                                 + qaac_custom_cmd_input + "- -o " + "\n \n" + VideoOutputQuoted
    # ------------------------------------------------------------------------------------------------------------ QAAC
    # AAC Command Line ------------------------------------------------------------------------------------------------
    elif encoder.get() == "AAC":
        if aac_vbr_toggle.get() == "-c:a ":
            bitrate_or_quality = f"-b:a {aac_bitrate_spinbox.get()}k "
        elif aac_vbr_toggle.get() == "-q:a ":
            bitrate_or_quality = f"-q:a {aac_quality_spinbox.get()} "
        example_cmd_output = "ffmpeg.exe -analyzeduration 100M -probesize 50M -i " + "\n \n" + \
                             VideoInputQuoted + "\n \n" + acodec_stream_choices[acodec_stream.get()] \
                             + encoder_dropdownmenu_choices[encoder.get()] + bitrate_or_quality \
                             + acodec_channel_choices[acodec_channel.get()] + \
                             acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting + \
                             aac_custom_cmd_input + aac_title_input + "\n \n" + \
                             VideoOutputQuoted
    # ------------------------------------------------------------------------------------------------ AAC Command Line
    # AC3 Command Line ------------------------------------------------------------------------------------------------
    elif encoder.get() == "AC3":
        example_cmd_output = "ffmpeg.exe -analyzeduration 100M -probesize 50M -i " + "\n \n" \
                             + VideoInputQuoted + "\n \n" + acodec_stream_choices[acodec_stream.get()] \
                             + encoder_dropdownmenu_choices[encoder.get()] + \
                             acodec_bitrate_choices[acodec_bitrate.get()] + \
                             acodec_channel_choices[acodec_channel.get()] + \
                             acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting + \
                             ac3_custom_cmd_input + "\n \n" \
                             + VideoOutputQuoted
    # ------------------------------------------------------------------------------------------------ AC3 Command Line
    # Opus Command Line -----------------------------------------------------------------------------------------------
    elif encoder.get() == "Opus":
        example_cmd_output = "ffmpeg.exe -analyzeduration 100M -probesize 50M -i " + "\n \n" + VideoInputQuoted + \
                             "\n \n" + acodec_stream_choices[acodec_stream.get()] + \
                             encoder_dropdownmenu_choices[encoder.get()] + \
                             acodec_vbr_choices[acodec_vbr.get()] + acodec_bitrate_choices[acodec_bitrate.get()] + \
                             acodec_channel_choices[acodec_channel.get()] + \
                             acodec_application_choices[acodec_application.get()] + "-packet_loss " + \
                             packet_loss.get() + " -frame_duration " + frame_duration.get() + " " + \
                             acodec_samplerate_choices[acodec_samplerate.get()] + \
                             audio_filter_setting + opus_custom_cmd_input + "\n \n" + VideoOutputQuoted
    # ----------------------------------------------------------------------------------------------- Opus Command Line
    # MP3 Command Line ------------------------------------------------------------------------------------------------
    elif encoder.get() == "MP3":
        example_cmd_output = "ffmpeg.exe -analyzeduration 100M -probesize 50M -i " + "\n \n" + VideoInputQuoted + \
                             "\n \n" + acodec_stream_choices[acodec_stream.get()] + \
                             encoder_dropdownmenu_choices[encoder.get()] + \
                             acodec_bitrate_choices[acodec_bitrate.get()] + \
                             acodec_channel_choices[acodec_channel.get()] + mp3_abr.get() + \
                             acodec_samplerate_choices[acodec_samplerate.get()] + \
                             audio_filter_setting + mp3_custom_cmd_input \
                             + "\n \n" + VideoOutputQuoted
    # ------------------------------------------------------------------------------------------------ MP3 Command Line
    # E-AC3 Command Line ----------------------------------------------------------------------------------------------
    elif encoder.get() == "E-AC3":
        example_cmd_output = "ffmpeg.exe -analyzeduration 100M -probesize 50M -i " + "\n \n" + VideoInputQuoted + \
                             "\n \n" + acodec_stream_choices[acodec_stream.get()] \
                             + encoder_dropdownmenu_choices[encoder.get()] \
                             + "-b:a " + eac3_spinbox.get() + acodec_channel_choices[acodec_channel.get()] \
                             + acodec_samplerate_choices[acodec_samplerate.get()] \
                             + audio_filter_setting + eac3_custom_cmd_input + "\n \n" \
                             + per_frame_metadata_choices[per_frame_metadata.get()] \
                             + "-mixing_level " + eac3_mixing_level.get() + " " \
                             + room_type_choices[room_type.get()] \
                             + "-copyright " + copyright_bit.get() + " " \
                             + "-dialnorm " + dialogue_level.get() + " " \
                             + dolby_surround_mode_choices[dolby_surround_mode.get()] \
                             + "-original " + original_bit_stream.get() + " " \
                             + downmix_mode_choices[downmix_mode.get()] \
                             + "-ltrt_cmixlev " + lt_rt_center_mix.get() + " " \
                             + "-ltrt_surmixlev " + lt_rt_surround_mix.get() + " " \
                             + "-loro_cmixlev " + lo_ro_center_mix.get() + " " \
                             + "-loro_surmixlev " + lo_ro_surround_mix.get() + " " \
                             + "\n \n" + dolby_surround_ex_mode_choices[dolby_surround_ex_mode.get()] \
                             + dolby_headphone_mode_choices[dolby_headphone_mode.get()] \
                             + a_d_converter_type_choices[a_d_converter_type.get()] \
                             + stereo_rematrixing_choices[stereo_rematrixing.get()] \
                             + "-channel_coupling " + channel_coupling.get() + " " \
                             + "-cpl_start_band " + cpl_start_band.get() + " " \
                             + "\n \n" + VideoOutputQuoted
    # ---------------------------------------------------------------------------------------------- E-AC3 Command Line
    # FLAC Command Line -----------------------------------------------------------------------------------------------
    elif encoder.get() == "FLAC":
        example_cmd_output = "ffmpeg.exe -analyzeduration 100M -probesize 50M -i " + "\n \n" + VideoInputQuoted + \
                             "\n \n" + acodec_stream_choices[acodec_stream.get()] \
                                     + encoder_dropdownmenu_choices[encoder.get()] + \
                                     acodec_bitrate_choices[acodec_bitrate.get()] + \
                                     acodec_channel_choices[acodec_channel.get()] + \
                                     acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting \
                                     + set_flac_acodec_coefficient \
                                     + acodec_flac_lpc_type_choices[acodec_flac_lpc_type.get()] \
                                     + acodec_flac_lpc_passes_choices[acodec_flac_lpc_passes.get()] \
                                     + flac_custom_cmd_input + "\n \n" + VideoOutputQuoted
    # ----------------------------------------------------------------------------------------------- FLAC Command Line
    # ALAC Command Line -----------------------------------------------------------------------------------------------
    elif encoder.get() == "ALAC":
        example_cmd_output = "ffmpeg.exe -analyzeduration 100M -probesize 50M -i " + "\n \n" + VideoInputQuoted + \
                             "\n \n" + acodec_stream_choices[acodec_stream.get()] \
                             + encoder_dropdownmenu_choices[encoder.get()] + \
                             acodec_channel_choices[acodec_channel.get()] + \
                             acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting \
                             + min_pre_order + max_pre_order + flac_custom_cmd_input \
                             + "\n \n" + VideoOutputQuoted
    # ----------------------------------------------------------------------------------------------- ALAC Command Line
    cmd_label = Label(cmd_line_window, text=example_cmd_output, foreground="white", background="#434547")
    cmd_label.config(font=("Helvetica", 16))
    cmd_label.pack()

# ---------------------------------------------------------------------------------------- Print Command Line from ROOT

# Start Audio Job -----------------------------------------------------------------------------------------------------
def startaudiojob():
    global example_cmd_output, ac3_job, aac_job, dts_job, opus_job, mp3_job, eac3_job, \
        fdkaac_job, qaac_job, flac_job, alac_job, auto_or_manual
    # Quote File Input/Output Paths------------
    VideoInputQuoted = '"' + VideoInput + '"'
    VideoOutputQuoted = '"' + VideoOutput + '"'
    # -------------------------- Quote File Paths
    # Combine audio filters for FFMPEG
    audio_filter_function()
    # ------------------------- Filters

    if shell_options.get() == "Default":
        global total_duration
        ffmpeg_cmd = '"' + ffmpeg + " -i " + VideoInputQuoted + ' -hide_banner -stats"'
        ffmpeg_duration = subprocess.Popen('cmd /c ' + ffmpeg_cmd, creationflags=subprocess.CREATE_NO_WINDOW,
                                           universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                           stdin=subprocess.PIPE)
        stdout, stderr = ffmpeg_duration.communicate()
        times_index = int(stdout.split().index('Duration:')) + 1  # Finds the string 'Duration' and adds 1 to the index
        ffmpeg_total_time = stdout.split()[times_index].rsplit('.', 1)[0]  # Removes mili-seconds from string
        total_duration = (sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(ffmpeg_total_time.split(":")))))
        #  total_duration converts 00:00:00 to seconds for progress bars

        def close_encode():
            confirm_exit = messagebox.askyesno(title='Prompt',
                                               message="Are you sure you want to stop the encode?", parent=window)
            if confirm_exit == False:
                pass
            elif confirm_exit == True:
                subprocess.Popen(f"TASKKILL /F /PID {job.pid} /T", creationflags=subprocess.CREATE_NO_WINDOW)
                window.destroy()

        def close_window():
            thread = threading.Thread(target=close_encode)
            thread.start()

        window = tk.Toplevel(root)
        window.title('Codec : ' + encoder.get() + '  |  ' + str(pathlib.Path(VideoInput).stem))
        window.configure(background="#434547")
        encode_label = Label(window, text="- - - - - - - - - - - - - - - - - - - - - - Progress - - "
                                          "- - - - - - - - - - - - - - - - - - - -",
              font=("Times New Roman", 14), background='#434547', foreground="white")
        encode_label.grid(column=0, row=0)
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=1)
        window.protocol('WM_DELETE_WINDOW', close_window)
        window.geometry("640x140")
        encode_window_progress = Text(window, height=2, relief=SUNKEN, bd=3)
        encode_window_progress.grid(row=1, column=0, pady=(10, 6), padx=10, sticky=E + W)
        encode_window_progress.insert(END, '')
        app_progress_bar = ttk.Progressbar(window, orient=HORIZONTAL, mode='determinate')
        app_progress_bar.grid(row=2, pady=(10, 10), padx=15, sticky=E + W)

        def update_last_codec_command():  # Updates 'profiles.ini' last used codec/commands
            config_profile.set('Auto Encode', 'codec', encoder.get())
            config_profile.set('Auto Encode', 'command', str(last_used_command))
            with open(config_profile_ini, 'w') as configfile_two:
                config_profile.write(configfile_two)

        def reset_main_gui():  # This resets the Main Gui back to default settings
            encoder.set('Set Codec')
            audiosettings_button.configure(state=DISABLED)

    # AC3 Start Job ---------------------------------------------------------------------------------------------------
    if encoder.get() == "AC3":
        finalcommand = '"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + \
                       acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] + \
                       acodec_bitrate_choices[acodec_bitrate.get()] + \
                       acodec_channel_choices[acodec_channel.get()] + \
                       acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting \
                       + "-sn -vn -map_chapters -1 -map_metadata -1 " + ac3_custom_cmd_input + \
                       VideoOutputQuoted + " -hide_banner"
        last_used_command = acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] + \
                       acodec_bitrate_choices[acodec_bitrate.get()] + \
                       acodec_channel_choices[acodec_channel.get()] + \
                       acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting \
                       + "-sn -vn -map_chapters -1 -map_metadata -1 " + ac3_custom_cmd_input
        if shell_options.get() == "Default":
            if auto_or_manual == 'auto':
                command = finalcommand
                update_last_codec_command()
            elif auto_or_manual == 'manual':
                command = '"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " \
                          + VideoInputQuoted + ' ' + config_profile['Auto Encode']['command'].lstrip().rstrip() \
                          + ' ' + VideoOutputQuoted + ' -hide_banner'
            job = subprocess.Popen('cmd /c ' + command + " " + '-v error -stats"', universal_newlines=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                   creationflags=subprocess.CREATE_NO_WINDOW)
            if auto_or_manual == 'manual':
                reset_main_gui()
            for line in job.stdout:
                encode_window_progress.delete('1.0', END)
                encode_window_progress.insert(END, line)
                try:
                    time = line.split()[2].rsplit('=', 1)[1].rsplit('.', 1)[0]
                    progress = (sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(time.split(":")))))
                    percent = '{:.1%}'.format(progress / int(total_duration)).split('.', 1)[0]
                    app_progress_bar['value'] = int(percent)
                except:
                    pass
            window.destroy()
        elif shell_options.get() == "Debug":
            subprocess.Popen('cmd /k ' + finalcommand + '"')
    # --------------------------------------------------------------------------------------------------------- AC3 Job
    # AAC Start Job ---------------------------------------------------------------------------------------------------
    elif encoder.get() == "AAC":
        if aac_vbr_toggle.get() == "-c:a ":
            bitrate_or_quality = f"-b:a {aac_bitrate_spinbox.get()}k "
        elif aac_vbr_toggle.get() == "-q:a ":
            bitrate_or_quality = f"-q:a {aac_quality_spinbox.get()} "
        finalcommand = '"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + \
                       acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] + \
                       bitrate_or_quality + acodec_channel_choices[acodec_channel.get()] + \
                       acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting \
                       + "-sn -vn -map_chapters -1 -map_metadata -1 " \
                       + aac_custom_cmd_input \
                       + aac_title_input + VideoOutputQuoted + " -hide_banner"
        last_used_command = acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] + \
                       bitrate_or_quality + acodec_channel_choices[acodec_channel.get()] + \
                       acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting \
                       + "-sn -vn -map_chapters -1 -map_metadata -1 " \
                       + aac_custom_cmd_input + aac_title_input
        if shell_options.get() == "Default":
            if auto_or_manual == 'auto':
                command = finalcommand
                update_last_codec_command()
            elif auto_or_manual == 'manual':
                command = '"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " \
                          + VideoInputQuoted + ' ' + config_profile['Auto Encode']['command'].lstrip().rstrip() \
                          + ' ' + VideoOutputQuoted + ' -hide_banner'
            job = subprocess.Popen('cmd /c ' + command + " " + '-v error -stats"', universal_newlines=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                   creationflags=subprocess.CREATE_NO_WINDOW)
            if auto_or_manual == 'manual':
                reset_main_gui()
            for line in job.stdout:
                encode_window_progress.delete('1.0', END)
                encode_window_progress.insert(END, line)
                try:
                    time = line.split()[2].rsplit('=', 1)[1].rsplit('.', 1)[0]
                    progress = (sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(time.split(":")))))
                    percent = '{:.1%}'.format(progress / int(total_duration)).split('.', 1)[0]
                    app_progress_bar['value'] = int(percent)
                except:
                    pass
            window.destroy()
        elif shell_options.get() == "Debug":
            subprocess.Popen('cmd /k ' + finalcommand + '"')
            # ------------------------------------------------------------------------------------------------- AAC Job
    # DTS Start Job ---------------------------------------------------------------------------------------------------
    elif encoder.get() == 'DTS':
        if dts_settings.get() == 'DTS Encoder':
            finalcommand = '"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + \
                           acodec_stream_choices[acodec_stream.get()] + dts_settings_choices[dts_settings.get()] \
                           + "-b:a " + dts_bitrate_spinbox.get() + "k " \
                           + acodec_channel_choices[acodec_channel.get()] \
                           + acodec_samplerate_choices[acodec_samplerate.get()] \
                           + audio_filter_setting + dts_custom_cmd_input \
                           + "-sn -vn -map_chapters -1 " \
                           + VideoOutputQuoted + " -hide_banner"
            last_used_command = acodec_stream_choices[acodec_stream.get()] + dts_settings_choices[dts_settings.get()] \
                                 + "-b:a " + dts_bitrate_spinbox.get() + "k " \
                                 + acodec_channel_choices[acodec_channel.get()] \
                                 + acodec_samplerate_choices[acodec_samplerate.get()] \
                                 + audio_filter_setting + dts_custom_cmd_input \
                                 + "-sn -vn -map_chapters -1 "
        elif dts_settings.get() != 'DTS Encoder':
            finalcommand = '"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted \
                           + acodec_stream_choices[acodec_stream.get()] + dts_settings_choices[dts_settings.get()] \
                           + dts_custom_cmd_input + "-sn -vn -map_chapters -1 " \
                           + VideoOutputQuoted + " -hide_banner"
            last_used_command = acodec_stream_choices[acodec_stream.get()] + \
                                dts_settings_choices[dts_settings.get()] \
                                + dts_custom_cmd_input + "-sn -vn -map_chapters -1 "
        if shell_options.get() == "Default":
            if auto_or_manual == 'auto':
                command = finalcommand
                update_last_codec_command()
            elif auto_or_manual == 'manual':
                command = '"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " \
                          + VideoInputQuoted + ' ' + config_profile['Auto Encode']['command'].lstrip().rstrip() \
                          + ' ' + VideoOutputQuoted + ' -hide_banner'
            job = subprocess.Popen('cmd /c ' + command + " " + '-v error -stats"', universal_newlines=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                   creationflags=subprocess.CREATE_NO_WINDOW)
            if auto_or_manual == 'manual':
                reset_main_gui()
            for line in job.stdout:
                encode_window_progress.delete('1.0', END)
                encode_window_progress.insert(END, line)
                try:
                    time = line.split()[2].rsplit('=', 1)[1].rsplit('.', 1)[0]
                    progress = (sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(time.split(":")))))
                    percent = '{:.1%}'.format(progress / int(total_duration)).split('.', 1)[0]
                    app_progress_bar['value'] = int(percent)
                except:
                    pass
            window.destroy()
        elif shell_options.get() == "Debug":
            subprocess.Popen('cmd /k ' + finalcommand + '"')
    # ------------------------------------------------------------------------------------------------------------- DTS
    # Opus Start Job --------------------------------------------------------------------------------------------------
    elif encoder.get() == "Opus":
        finalcommand = '"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + \
                       acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] + \
                       acodec_vbr_choices[acodec_vbr.get()] + acodec_bitrate_choices[acodec_bitrate.get()] + \
                       acodec_channel_choices[acodec_channel.get()] + \
                       acodec_application_choices[acodec_application.get()] + "-packet_loss " + \
                       packet_loss.get() + " -frame_duration " + frame_duration.get() + " " + \
                       acodec_samplerate_choices[acodec_samplerate.get()] + \
                       audio_filter_setting + "-sn -vn -map_chapters -1 -map_metadata -1 " \
                       + opus_custom_cmd_input + VideoOutputQuoted + " -hide_banner"
        last_used_command = acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] + \
                            acodec_vbr_choices[acodec_vbr.get()] + acodec_bitrate_choices[acodec_bitrate.get()] + \
                            acodec_channel_choices[acodec_channel.get()] + \
                            acodec_application_choices[acodec_application.get()] + "-packet_loss " + \
                            packet_loss.get() + " -frame_duration " + frame_duration.get() + " " + \
                            acodec_samplerate_choices[acodec_samplerate.get()] + \
                            audio_filter_setting + "-sn -vn -map_chapters -1 -map_metadata -1 "
        if shell_options.get() == "Default":
            if auto_or_manual == 'auto':
                command = finalcommand
                update_last_codec_command()
            elif auto_or_manual == 'manual':
                command = '"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " \
                          + VideoInputQuoted + ' ' + config_profile['Auto Encode']['command'].lstrip().rstrip() \
                          + ' ' + VideoOutputQuoted + ' -hide_banner'
            job = subprocess.Popen('cmd /c ' + command + " " + '-v error -stats"', universal_newlines=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                   creationflags=subprocess.CREATE_NO_WINDOW)
            if auto_or_manual == 'manual':
                reset_main_gui()
            for line in job.stdout:
                encode_window_progress.delete('1.0', END)
                encode_window_progress.insert(END, line)
                try:
                    time = line.split()[2].rsplit('=', 1)[1].rsplit('.', 1)[0]
                    progress = (sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(time.split(":")))))
                    percent = '{:.1%}'.format(progress / int(total_duration)).split('.', 1)[0]
                    app_progress_bar['value'] = int(percent)
                except:
                    pass
            window.destroy()
        elif shell_options.get() == "Debug":
            subprocess.Popen('cmd /k ' + finalcommand + '"')
    # ------------------------------------------------------------------------------------------------------------ Opus
    # MP3 Start Job ---------------------------------------------------------------------------------------------------
    elif encoder.get() == "MP3":
        finalcommand = '"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + \
                       acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] + \
                       acodec_bitrate_choices[acodec_bitrate.get()] + acodec_channel_choices[acodec_channel.get()] \
                       + mp3_abr.get() + acodec_samplerate_choices[acodec_samplerate.get()] \
                       + audio_filter_setting + "-sn -vn -map_chapters -1 -map_metadata -1 " \
                       + mp3_custom_cmd_input + VideoOutputQuoted + " -hide_banner"
        last_used_command = acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] + \
                            acodec_bitrate_choices[acodec_bitrate.get()] + acodec_channel_choices[acodec_channel.get()] \
                            + mp3_abr.get() + acodec_samplerate_choices[acodec_samplerate.get()] \
                            + audio_filter_setting + "-sn -vn -map_chapters -1 -map_metadata -1 " \
                            + mp3_custom_cmd_input
        if shell_options.get() == "Default":
            if auto_or_manual == 'auto':
                command = finalcommand
                update_last_codec_command()
            elif auto_or_manual == 'manual':
                command = '"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " \
                          + VideoInputQuoted + ' ' + config_profile['Auto Encode']['command'].lstrip().rstrip() \
                          + ' ' + VideoOutputQuoted + ' -hide_banner'
            job = subprocess.Popen('cmd /c ' + command + " " + '-v error -stats"', universal_newlines=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                   creationflags=subprocess.CREATE_NO_WINDOW)
            if auto_or_manual == 'manual':
                reset_main_gui()
            for line in job.stdout:
                encode_window_progress.delete('1.0', END)
                encode_window_progress.insert(END, line)
                try:
                    time = line.split()[2].rsplit('=', 1)[1].rsplit('.', 1)[0]
                    progress = (sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(time.split(":")))))
                    percent = '{:.1%}'.format(progress / int(total_duration)).split('.', 1)[0]
                    app_progress_bar['value'] = int(percent)
                except:
                    pass
            window.destroy()
        elif shell_options.get() == "Debug":
            subprocess.Popen('cmd /k ' + finalcommand + '"')
    # ------------------------------------------------------------------------------------------------------------- MP3
    # E-AC3 Start Job -------------------------------------------------------------------------------------------------
    elif encoder.get() == "E-AC3":
        finalcommand = '"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + \
                       acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] \
                       + "-b:a " + eac3_spinbox.get() + acodec_channel_choices[acodec_channel.get()] \
                       + acodec_samplerate_choices[acodec_samplerate.get()] \
                       + audio_filter_setting + eac3_custom_cmd_input \
                       + per_frame_metadata_choices[per_frame_metadata.get()] \
                       + "-mixing_level " + eac3_mixing_level.get() + " " \
                       + room_type_choices[room_type.get()] \
                       + "-copyright " + copyright_bit.get() + " " \
                       + "-dialnorm " + dialogue_level.get() + " " \
                       + dolby_surround_mode_choices[dolby_surround_mode.get()] \
                       + "-original " + original_bit_stream.get() + " " \
                       + downmix_mode_choices[downmix_mode.get()] \
                       + "-ltrt_cmixlev " + lt_rt_center_mix.get() + " " \
                       + "-ltrt_surmixlev " + lt_rt_surround_mix.get() + " " \
                       + "-loro_cmixlev " + lo_ro_center_mix.get() + " " \
                       + "-loro_surmixlev " + lo_ro_surround_mix.get() + " " \
                       + dolby_surround_ex_mode_choices[dolby_surround_ex_mode.get()] \
                       + dolby_headphone_mode_choices[dolby_headphone_mode.get()] \
                       + a_d_converter_type_choices[a_d_converter_type.get()] \
                       + stereo_rematrixing_choices[stereo_rematrixing.get()] \
                       + "-channel_coupling " + channel_coupling.get() + " " \
                       + "-cpl_start_band " + cpl_start_band.get() + " " \
                       + "-sn -vn -map_chapters -1 -map_metadata -1 " + VideoOutputQuoted + " -hide_banner"
        last_used_command = acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] \
                            + "-b:a " + eac3_spinbox.get() + acodec_channel_choices[acodec_channel.get()] \
                            + acodec_samplerate_choices[acodec_samplerate.get()] \
                            + audio_filter_setting + eac3_custom_cmd_input \
                            + per_frame_metadata_choices[per_frame_metadata.get()] \
                            + "-mixing_level " + eac3_mixing_level.get() + " " \
                            + room_type_choices[room_type.get()] \
                            + "-copyright " + copyright_bit.get() + " " \
                            + "-dialnorm " + dialogue_level.get() + " " \
                            + dolby_surround_mode_choices[dolby_surround_mode.get()] \
                            + "-original " + original_bit_stream.get() + " " \
                            + downmix_mode_choices[downmix_mode.get()] \
                            + "-ltrt_cmixlev " + lt_rt_center_mix.get() + " " \
                            + "-ltrt_surmixlev " + lt_rt_surround_mix.get() + " " \
                            + "-loro_cmixlev " + lo_ro_center_mix.get() + " " \
                            + "-loro_surmixlev " + lo_ro_surround_mix.get() + " " \
                            + dolby_surround_ex_mode_choices[dolby_surround_ex_mode.get()] \
                            + dolby_headphone_mode_choices[dolby_headphone_mode.get()] \
                            + a_d_converter_type_choices[a_d_converter_type.get()] \
                            + stereo_rematrixing_choices[stereo_rematrixing.get()] \
                            + "-channel_coupling " + channel_coupling.get() + " " \
                            + "-cpl_start_band " + cpl_start_band.get() + " " \
                            + "-sn -vn -map_chapters -1 "
        if shell_options.get() == "Default":
            if auto_or_manual == 'auto':
                command = finalcommand
                update_last_codec_command()
            elif auto_or_manual == 'manual':
                command = '"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " \
                          + VideoInputQuoted + ' ' + config_profile['Auto Encode']['command'].lstrip().rstrip() \
                          + ' ' + VideoOutputQuoted + ' -hide_banner'
            job = subprocess.Popen('cmd /c ' + command + " " + '-v error -stats"', universal_newlines=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                   creationflags=subprocess.CREATE_NO_WINDOW)
            if auto_or_manual == 'manual':
                reset_main_gui()
            for line in job.stdout:
                encode_window_progress.delete('1.0', END)
                encode_window_progress.insert(END, line)
                try:
                    time = line.split()[2].rsplit('=', 1)[1].rsplit('.', 1)[0]
                    progress = (sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(time.split(":")))))
                    percent = '{:.1%}'.format(progress / int(total_duration)).split('.', 1)[0]
                    app_progress_bar['value'] = int(percent)
                except:
                    pass
            window.destroy()
        elif shell_options.get() == "Debug":
            subprocess.Popen('cmd /k ' + finalcommand + '"')
    # ----------------------------------------------------------------------------------------------------------- E-AC3
    # FDK_AAC Start Job -----------------------------------------------------------------------------------------------
    elif encoder.get() == "FDK-AAC":
        if shell_options.get() == "Default":
            silent = '--silent '
        else:
            silent = ' '
        finalcommand = '"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + \
                       acodec_stream_choices[acodec_stream.get()] + acodec_channel_choices[acodec_channel.get()] + \
                       acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting + \
                       "-f caf - -hide_banner -v error -stats |" \
                       + fdkaac + " " + acodec_profile_choices[acodec_profile.get()] + \
                       fdkaac_title_input + fdkaac_custom_cmd_input + \
                       afterburnervar.get() + crccheck.get() + moovbox.get() \
                       + sbrdelay.get() + headerperiod.get() + \
                       acodec_lowdelay_choices[acodec_lowdelay.get()] + \
                       acodec_sbr_ratio_choices[acodec_sbr_ratio.get()] + \
                       acodec_transport_format_choices[acodec_transport_format.get()] + \
                       acodec_bitrate_choices[acodec_bitrate.get()] + silent + " - -o " + VideoOutputQuoted + '"'
        last_used_command = acodec_stream_choices[acodec_stream.get()] \
                            + acodec_channel_choices[acodec_channel.get()] \
                            + acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting + \
                            "-f caf - -hide_banner -v error -stats |" \
                            + fdkaac + " " + acodec_profile_choices[acodec_profile.get()] + \
                            fdkaac_title_input + fdkaac_custom_cmd_input + \
                            afterburnervar.get() + crccheck.get() + moovbox.get() \
                            + sbrdelay.get() + headerperiod.get() + \
                            acodec_lowdelay_choices[acodec_lowdelay.get()] + \
                            acodec_sbr_ratio_choices[acodec_sbr_ratio.get()] + \
                            acodec_transport_format_choices[acodec_transport_format.get()] + \
                            acodec_bitrate_choices[acodec_bitrate.get()] + silent + " - -o "
        if shell_options.get() == "Default":
            if auto_or_manual == 'auto':
                command = finalcommand
                update_last_codec_command()
            elif auto_or_manual == 'manual':
                command = '"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " \
                          + VideoInputQuoted + ' ' + config_profile['Auto Encode']['command'].lstrip().rstrip() \
                          + ' ' + VideoOutputQuoted
            job = subprocess.Popen('cmd /c ' + command, universal_newlines=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                   creationflags=subprocess.CREATE_NO_WINDOW)
            if auto_or_manual == 'manual':
                reset_main_gui()
            for line in job.stdout:
                encode_window_progress.delete('1.0', END)
                encode_window_progress.insert(END, line)
                try:
                    time = line.split()[2].rsplit('=', 1)[1].rsplit('.', 1)[0]
                    progress = (sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(time.split(":")))))
                    percent = '{:.1%}'.format(progress / int(total_duration)).split('.', 1)[0]
                    app_progress_bar['value'] = int(percent)
                except:
                    pass
            window.destroy()
        elif shell_options.get() == "Debug":
            subprocess.Popen('cmd /k ' + finalcommand)
    # ------------------------------------------------------------------------------------------------------------- FDK
    # QAAC Start Job --------------------------------------------------------------------------------------------------
    elif encoder.get() == "QAAC":
        if shell_options.get() == "Default":
            silent = '--silent '
        else:
            silent = ' '
        if q_acodec_profile.get() == "True VBR":
            finalcommand = '"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " \
                           + VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] \
                           + acodec_channel_choices[acodec_channel.get()] + audio_filter_setting \
                           + acodec_samplerate_choices[acodec_samplerate.get()] \
                           + "-f wav - -hide_banner -v error -stats | " + qaac \
                           + " " + q_acodec_profile_choices[q_acodec_profile.get()] \
                           + q_acodec_quality_amnt.get() + " " + qaac_high_efficiency.get() \
                           + qaac_normalize.get() + qaac_nodither.get() + "--gain " \
                           + q_acodec_gain.get() + " " + q_acodec_quality_choices[q_acodec_quality.get()] \
                           + qaac_nodelay.get() \
                           + q_gapless_mode_choices[q_gapless_mode.get()] + qaac_nooptimize.get() \
                           + qaac_threading.get() + qaac_limiter.get() + qaac_title_input + qaac_custom_cmd_input \
                           + silent + " - -o " + VideoOutputQuoted + '"'
            last_used_command = acodec_stream_choices[acodec_stream.get()] \
                                + acodec_channel_choices[acodec_channel.get()] + audio_filter_setting \
                                + acodec_samplerate_choices[acodec_samplerate.get()] \
                                + "-f wav - -hide_banner -v error -stats | " + qaac \
                                + " " + q_acodec_profile_choices[q_acodec_profile.get()] \
                                + q_acodec_quality_amnt.get() + " " + qaac_high_efficiency.get() \
                                + qaac_normalize.get() + qaac_nodither.get() + "--gain " \
                                + q_acodec_gain.get() + " " + q_acodec_quality_choices[q_acodec_quality.get()] \
                                + qaac_nodelay.get() \
                                + q_gapless_mode_choices[q_gapless_mode.get()] + qaac_nooptimize.get() \
                                + qaac_threading.get() + qaac_limiter.get() + qaac_title_input + qaac_custom_cmd_input \
                                + silent + " - -o "
        else:
            finalcommand = '"' + ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted \
                           + acodec_stream_choices[acodec_stream.get()] + \
                           acodec_channel_choices[acodec_channel.get()] + audio_filter_setting + \
                           acodec_samplerate_choices[acodec_samplerate.get()] \
                           + "-f wav - -hide_banner -v error -stats | " + qaac \
                           + " " + q_acodec_profile_choices[q_acodec_profile.get()] + \
                           q_acodec_bitrate.get() + " " + qaac_high_efficiency.get() + qaac_normalize.get() \
                           + qaac_nodither.get() + "--gain " + q_acodec_gain.get() + " " \
                           + q_acodec_quality_choices[q_acodec_quality.get()] + qaac_nodelay.get() \
                           + q_gapless_mode_choices[q_gapless_mode.get()] + qaac_nooptimize.get() \
                           + qaac_threading.get() + qaac_limiter.get() + qaac_title_input \
                           + qaac_custom_cmd_input + silent + " - -o " + VideoOutputQuoted + '"'
            last_used_command = acodec_stream_choices[acodec_stream.get()] + \
                                acodec_channel_choices[acodec_channel.get()] + audio_filter_setting + \
                                acodec_samplerate_choices[acodec_samplerate.get()] \
                                + "-f wav - -hide_banner -v error -stats | " + qaac \
                                + " " + q_acodec_profile_choices[q_acodec_profile.get()] + \
                                q_acodec_bitrate.get() + " " + qaac_high_efficiency.get() + qaac_normalize.get() \
                                + qaac_nodither.get() + "--gain " + q_acodec_gain.get() + " " \
                                + q_acodec_quality_choices[q_acodec_quality.get()] + qaac_nodelay.get() \
                                + q_gapless_mode_choices[q_gapless_mode.get()] + qaac_nooptimize.get() \
                                + qaac_threading.get() + qaac_limiter.get() + qaac_title_input \
                                + qaac_custom_cmd_input + silent + " - -o "
        if shell_options.get() == "Default":
            if auto_or_manual == 'auto':
                command = finalcommand
                update_last_codec_command()
            elif auto_or_manual == 'manual':
                command = '"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " \
                          + VideoInputQuoted + ' ' + config_profile['Auto Encode']['command'].lstrip().rstrip() \
                          + ' ' + VideoOutputQuoted
            job = subprocess.Popen('cmd /c ' + command, universal_newlines=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                   creationflags=subprocess.CREATE_NO_WINDOW)
            if auto_or_manual == 'manual':
                reset_main_gui()
            for line in job.stdout:
                encode_window_progress.delete('1.0', END)
                encode_window_progress.insert(END, line)
                try:
                    time = line.split()[2].rsplit('=', 1)[1].rsplit('.', 1)[0]
                    progress = (sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(time.split(":")))))
                    percent = '{:.1%}'.format(progress / int(total_duration)).split('.', 1)[0]
                    app_progress_bar['value'] = int(percent)
                except:
                    pass
            window.destroy()
        elif shell_options.get() == "Debug":
            subprocess.Popen('cmd /k ' + finalcommand)
    # ------------------------------------------------------------------------------------------------------------ QAAC
    # FLAC Start Job --------------------------------------------------------------------------------------------------
    elif encoder.get() == "FLAC":
        finalcommand = '"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + \
                       acodec_stream_choices[acodec_stream.get()] \
                       + encoder_dropdownmenu_choices[encoder.get()] + \
                       acodec_bitrate_choices[acodec_bitrate.get()] + \
                       acodec_channel_choices[acodec_channel.get()] + \
                       acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting \
                       + set_flac_acodec_coefficient \
                       + acodec_flac_lpc_type_choices[acodec_flac_lpc_type.get()] \
                       + acodec_flac_lpc_passes_choices[acodec_flac_lpc_passes.get()] \
                       + flac_custom_cmd_input + VideoOutputQuoted + " -hide_banner" + '"'
        last_used_command = acodec_stream_choices[acodec_stream.get()] \
                            + encoder_dropdownmenu_choices[encoder.get()] + \
                            acodec_bitrate_choices[acodec_bitrate.get()] + \
                            acodec_channel_choices[acodec_channel.get()] + \
                            acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting \
                            + set_flac_acodec_coefficient + acodec_flac_lpc_type_choices[acodec_flac_lpc_type.get()] \
                            + acodec_flac_lpc_passes_choices[acodec_flac_lpc_passes.get()] + flac_custom_cmd_input
        if shell_options.get() == "Default":
            if auto_or_manual == 'auto':
                command = finalcommand
                update_last_codec_command()
            elif auto_or_manual == 'manual':
                command = '"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " \
                          + VideoInputQuoted + ' ' + config_profile['Auto Encode']['command'].lstrip().rstrip() \
                          + ' ' + VideoOutputQuoted
            job = subprocess.Popen('cmd /c ' + command, universal_newlines=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                   creationflags=subprocess.CREATE_NO_WINDOW)
            if auto_or_manual == 'manual':
                reset_main_gui()
            for line in job.stdout:
                encode_window_progress.delete('1.0', END)
                encode_window_progress.insert(END, line)
                try:
                    time = line.split()[2].rsplit('=', 1)[1].rsplit('.', 1)[0]
                    progress = (sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(time.split(":")))))
                    percent = '{:.1%}'.format(progress / int(total_duration)).split('.', 1)[0]
                    app_progress_bar['value'] = int(percent)
                except:
                    pass
            window.destroy()
        elif shell_options.get() == "Debug":
            subprocess.Popen('cmd /k ' + finalcommand + '"')
    # ------------------------------------------------------------------------------------------------------------ FLAC
    # ALAC Start Job --------------------------------------------------------------------------------------------------
    elif encoder.get() == "ALAC":
        finalcommand = '"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + \
                       acodec_stream_choices[acodec_stream.get()] \
                       + encoder_dropdownmenu_choices[encoder.get()] + \
                       acodec_channel_choices[acodec_channel.get()] + \
                       acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting \
                       + min_pre_order + max_pre_order + flac_custom_cmd_input \
                       + " " + VideoOutputQuoted + " -hide_banner" + '"'
        last_used_command = acodec_stream_choices[acodec_stream.get()] \
                            + encoder_dropdownmenu_choices[encoder.get()] + \
                            acodec_channel_choices[acodec_channel.get()] + \
                            acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting \
                            + min_pre_order + max_pre_order + flac_custom_cmd_input
        if shell_options.get() == "Default":
            if auto_or_manual == 'auto':
                command = finalcommand
                update_last_codec_command()
            elif auto_or_manual == 'manual':
                command = '"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " \
                          + VideoInputQuoted + ' ' + config_profile['Auto Encode']['command'].lstrip().rstrip() \
                          + ' ' + VideoOutputQuoted
            job = subprocess.Popen('cmd /c ' + command, universal_newlines=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                   creationflags=subprocess.CREATE_NO_WINDOW)
            if auto_or_manual == 'manual':
                reset_main_gui()
            for line in job.stdout:
                encode_window_progress.delete('1.0', END)
                encode_window_progress.insert(END, line)
                try:
                    time = line.split()[2].rsplit('=', 1)[1].rsplit('.', 1)[0]
                    progress = (sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(time.split(":")))))
                    percent = '{:.1%}'.format(progress / int(total_duration)).split('.', 1)[0]
                    app_progress_bar['value'] = int(percent)
                except:
                    pass
            window.destroy()
        elif shell_options.get() == "Debug":
            subprocess.Popen('cmd /k ' + finalcommand + '"')
    # ------------------------------------------------------------------------------------------------------------ ALAC

# Buttons Main Gui ----------------------------------------------------------------------------------------------------
# Encoder Menu Enter/Leave Binds ----------------------------------------------------------------
encoder_menu.bind("<Enter>", encoder_menu_hover)
encoder_menu.bind("<Leave>", encoder_menu_hover_leave)

def encoder_menu_on_enter(e):
    status_label.configure(text='Select Audio Codec...')

def encoder_menu_on_leave(e):
    status_label.configure(text='')

encoder_menu.bind("<Enter>", encoder_menu_on_enter)
encoder_menu.bind("<Leave>", encoder_menu_on_leave)
# ---------------------------------------------------------------- # Encoder Menu Enter/Leave Binds

# Audio Settings Button --------------------------------------------------------------------------
audiosettings_button = Button(root, text="Audio Settings", command=openaudiowindow, foreground="white",
                              background="#23272A", state=DISABLED, borderwidth="3")
audiosettings_button.grid(row=1, column=3, columnspan=2, padx=5, pady=5, sticky=N + S + W + E)
audiosettings_button.bind("<Enter>", audiosettings_button_hover)
audiosettings_button.bind("<Leave>", audiosettings_button_hover_leave)

def audiosettings_button_on_enter(e):
    status_label.configure(text='Click To Configure Selected Audio Codec...')

def audiosettings_button_on_leave(e):
    status_label.configure(text='')

audiosettings_button.bind("<Enter>", audiosettings_button_on_enter)
audiosettings_button.bind("<Leave>", audiosettings_button_on_leave)
# --------------------------------------------------------------------------- # Audio Settings Button

def input_button_commands():
    global autosavefilename, VideoInput
    encoder.set('Set Codec')
    audiosettings_button.configure(state=DISABLED)
    output_entry.configure(state=NORMAL)
    output_entry.delete(0, END)
    output_entry.configure(state=DISABLED)
    input_entry.configure(state=NORMAL)
    input_entry.delete(0, END)
    input_entry.configure(state=DISABLED)
    encoder_menu.configure(state=DISABLED)
    output_button.configure(state=NORMAL)
    command_line_button.configure(state=DISABLED)
    file_input()
    if config_profile['Auto Encode']['codec'] == '':
        auto_encode_last_options.configure(state=DISABLED)
    else:
        auto_encode_last_options.configure(state=NORMAL)
        if config_profile['Auto Encode']['codec'] == 'AAC':
            VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '.NEW.mp4'
        elif config_profile['Auto Encode']['codec'] == 'AC3' or config_profile['Auto Encode']['codec'] == 'E-AC3':
            VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '.NEW.ac3'
        elif config_profile['Auto Encode']['codec'] == "DTS":
            VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '.NEW.dts'
        elif config_profile['Auto Encode']['codec'] == "Opus":
            VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '.NEW.opus'
        elif config_profile['Auto Encode']['codec'] == 'MP3':
            VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '.NEW.mp3'
        elif config_profile['Auto Encode']['codec'] == "FDK-AAC" or \
                config_profile['Auto Encode']['codec'] == "QAAC" or config_profile['Auto Encode']['codec'] == "ALAC":
            VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '.NEW.m4a'
        elif config_profile['Auto Encode']['codec'] == "FLAC":
            VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '.NEW.flac'
        output_entry.configure(state=NORMAL)
        output_entry.delete(0, END)
        output_entry.insert(0, VideoOut)
        output_entry.configure(state=DISABLED)
        autosavefilename = pathlib.Path(VideoOut).name


def drop_input(event):
    input_dnd.set(event.data)


def update_file_input(*args):
    global VideoInput, track_count, autofilesave_dir_path, VideoInputQuoted, autosavefilename
    input_entry.configure(state=NORMAL)
    input_entry.delete(0, END)
    remove_brackets = str(input_dnd.get())
    if remove_brackets.startswith('{') and remove_brackets.endswith('}'):
        VideoInput = str(input_dnd.get())[1:-1]
    else:
        VideoInput = str(input_dnd.get())
    file_extension = pathlib.Path(VideoInput).suffix
    if file_extension == '.wav' or file_extension == '.mt2s' or file_extension == '.ac3' or \
            file_extension == '.mka' or \
            file_extension == '.wav' or file_extension == '.mp3' or file_extension == '.aac' or \
            file_extension == '.ogg' or file_extension == '.ogv' or file_extension == '.m4v' or \
            file_extension == '.mpeg' or file_extension == '.avi' or file_extension == '.vob' or \
            file_extension == '.webm' or file_extension == '.mp4' or file_extension == '.mkv' or \
            file_extension == '.dts' or file_extension == '.m4a' or file_extension == '.mov' or \
            file_extension == '.flac' or file_extension == '.eac3' or file_extension == '.opus' or \
            file_extension == '.aax':
        autofilesave_file_path = pathlib.PureWindowsPath(VideoInput)  # Command to get file input location
        autofilesave_dir_path = autofilesave_file_path.parents[0]  # Final command to get only the directory
        VideoInputQuoted = '"' + VideoInput + '"'
        # This gets the total amount of audio streams For DnD-
        mediainfocli_cmd = '"' + mediainfocli + " " + '--Output="General;%AudioCount%"' + " " + VideoInputQuoted + '"'
        mediainfo_count = subprocess.Popen('cmd /c ' + mediainfocli_cmd, creationflags=subprocess.CREATE_NO_WINDOW,
                                           universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                           stdin=subprocess.PIPE)
        stdout, stderr = mediainfo_count.communicate()
        track_count = stdout
        input_entry.insert(0, str(input_dnd.get()).replace("{", "").replace("}", ""))
        input_entry.configure(state=DISABLED)
        output_entry.configure(state=NORMAL)
        output_entry.delete(0, END)
        output_entry.configure(state=DISABLED)
        encoder.set("Set Codec")
        audiosettings_button.configure(state=DISABLED)
        output_button.configure(state=NORMAL)
        start_audio_button.configure(state=DISABLED)
        encoder_menu.configure(state=NORMAL)
        if config_profile['Auto Encode']['codec'] == '':
            auto_encode_last_options.configure(state=DISABLED)
        else:
            auto_encode_last_options.configure(state=NORMAL)
            if config_profile['Auto Encode']['codec'] == 'AAC':
                VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '.NEW.mp4'
            elif config_profile['Auto Encode']['codec'] == 'AC3' or config_profile['Auto Encode']['codec'] == 'E-AC3':
                VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '.NEW.ac3'
            elif config_profile['Auto Encode']['codec'] == "DTS":
                VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '.NEW.dts'
            elif config_profile['Auto Encode']['codec'] == "Opus":
                VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '.NEW.opus'
            elif config_profile['Auto Encode']['codec'] == 'MP3':
                VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '.NEW.mp3'
            elif config_profile['Auto Encode']['codec'] == "FDK-AAC" or \
                    config_profile['Auto Encode']['codec'] == "QAAC" or config_profile['Auto Encode']['codec'] == "ALAC":
                VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '.NEW.m4a'
            elif config_profile['Auto Encode']['codec'] == "FLAC":
                VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '.NEW.flac'
            output_entry.configure(state=NORMAL)
            output_entry.delete(0, END)
            output_entry.insert(0, VideoOut)
            output_entry.configure(state=DISABLED)
            autosavefilename = pathlib.Path(VideoOut).name
    else:
        messagebox.showinfo(title="Wrong File Type", message="Try Again With a Supported File Type!\n\nIf this is a "
                                                             "file that should be supported, please let me know.")

input_dnd = StringVar()
input_dnd.trace('w', update_file_input)

# Input Button/Entry Box ----------------------------------------------------------------------
input_button = tk.Button(root, text="Open File", command=input_button_commands, foreground="white",
                         background="#23272A", borderwidth="3")
input_button.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)
input_button.drop_target_register(DND_FILES)
input_button.dnd_bind('<<Drop>>', drop_input)
input_button.bind("<Enter>", input_button_hover)
input_button.bind("<Leave>", input_button_hover_leave)

input_entry = Entry(root, width=35, borderwidth=4, background="#CACACA", state=DISABLED)
input_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=S + E + W)
input_entry.drop_target_register(DND_FILES)
input_entry.dnd_bind('<<Drop>>', drop_input)

def input_button_on_enter(e):
    status_label.configure(text='Click To Open File or Drag and Drop...')

def input_button_on_leave(e):
    status_label.configure(text='')

input_button.bind("<Enter>", input_button_on_enter)
input_button.bind("<Leave>", input_button_on_leave)
# ------------------------------------------------------------------------- Input Button/Entry Box

# Output Button/Entry Box ------------------------------------------------------------------------
output_button = Button(root, text="Save File", command=file_save, state=DISABLED, foreground="white",
                       background="#23272A", borderwidth="3")
output_button.grid(row=2, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)
output_entry = Entry(root, width=35, borderwidth=4, background="#CACACA", state=DISABLED)
output_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky=S + E + W)
output_button.bind("<Enter>", output_button_hover)
output_button.bind("<Leave>", output_button_hover_leave)

def output_button_on_enter(e):
    status_label.configure(text='Click To Specify Save Location...')

def output_button_on_leave(e):
    status_label.configure(text='')

output_button.bind("<Enter>", output_button_on_enter)
output_button.bind("<Leave>", output_button_on_leave)
# ---------------------------------------------------------------------- # Output Button/Entry Box

# Print Final Command Line ---------------------------------------------------------------------
command_line_button = Button(root, text="Show\nCommand", command=print_command_line, state=DISABLED, foreground="white",
                             background="#23272A", borderwidth="3")
command_line_button.grid(row=1, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)
command_line_button.bind("<Enter>", command_line_button_hover)
command_line_button.bind("<Leave>", command_line_button_hover_leave)

def command_line_button_on_enter(e):
    status_label.configure(text='Click To Show Full Command...')

def command_line_button_on_leave(e):
    status_label.configure(text='')

command_line_button.bind("<Enter>", command_line_button_on_enter)
command_line_button.bind("<Leave>", command_line_button_on_leave)
# ----------------------------------------------------------------------- Print Final Command Line

# Start Audio Job: Manual -----------------------------------------------------------------------
def start_audio_job_manual():
    global auto_or_manual
    auto_or_manual = 'auto'
    threading.Thread(target=startaudiojob).start()
start_audio_button = Button(root, text="Start Audio Job",
                            command=start_audio_job_manual, state=DISABLED, foreground="white", background="#23272A",
                            borderwidth="3")
start_audio_button.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky=N + S + E + W)
start_audio_button.bind("<Enter>", start_audio_button_hover)
start_audio_button.bind("<Leave>", start_audio_button_hover_leave)

def start_audio_button_on_enter(e):
    status_label.configure(text='Click To Start Job...')

def start_audio_button_on_leave(e):
    status_label.configure(text='')

start_audio_button.bind("<Enter>", start_audio_button_on_enter)
start_audio_button.bind("<Leave>", start_audio_button_on_leave)
# --------------------------------------------------------------------------- Start Audio Job: Manual

# Start Audio Job: Auto -----------------------------------------------------------------------------
def encode_last_used_setting():
    global auto_or_manual, audio_window, acodec_stream_track_counter
    auto_or_manual = 'manual'
    acodec_stream_track_counter = {}
    for i in range(int(str.split(track_count)[-1])):
        acodec_stream_track_counter[f'Track {i + 1}'] = f' -map 0:a:{i} '
    encoder.set(config_profile['Auto Encode']['codec'])
    openaudiowindow()
    audio_window.destroy()
    threading.Thread(target=startaudiojob).start()
auto_encode_last_options = Button(root, text="Auto Encode:\nLast Used Options", command=encode_last_used_setting,
                                      foreground="white", background="#23272A", borderwidth="3", state=DISABLED)
auto_encode_last_options.grid(row=3, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)
auto_encode_last_options.bind("<Enter>", auto_encode_last_options_hover)
auto_encode_last_options.bind("<Leave>", auto_encode_last_options_hover_leave)
def popup_auto_e_b_menu(e):  # Function for mouse button 3 (right click) to pop up menu
    global rightclick_on_off
    try:
        if rightclick_on_off == 1:
            auto_encode_button_menu.tk_popup(e.x_root, e.y_root)  # This gets the posision of 'e' on the root widget
    except NameError:
        pass

def show_auto_encode_command(*args):  # Opens a new window with 'Auto Encode' command
    try:
        global show_auto_command_window
        show_auto_command_window.destroy()  # Destroys existing auto command window before continuing to make a new one
    except:
        pass

    show_auto_command_window = Toplevel(root)  # auto command window (shows auto encoding command)
    show_auto_command_window.title("Audio Streams")
    show_auto_command_window.configure(background="#434547")
    Label(show_auto_command_window, text="---------- Auto Encode Command ----------", font=("Times New Roman", 16),
          background='#434547', foreground="white").grid(column=0, row=0)
    text_area = scrolledtextwidget.ScrolledText(show_auto_command_window, width=60, height=5, tabs=10, spacing2=3,
                                                spacing1=2, spacing3=3)
    text_area.grid(column=0, pady=10, padx=10)
    text_area.insert(INSERT, config_profile['Auto Encode']['command'])
    text_area.configure(font=("Helvetica", 12))
    text_area.configure(state=DISABLED)
    show_auto_command_window.grid_columnconfigure(0, weight=1)

auto_encode_button_menu = Menu(root, tearoff=False)  # This is the right click menu for the auto_encode_button
auto_encode_button_menu.add_command(label='Show Command', command=show_auto_encode_command)
def auto_encode_last_options_on_enter(e):
    global rightclick_on_off
    status_label.configure(text='Right Click For More Options...')
    rightclick_on_off = 1

def auto_encode_last_options_on_leave(e):
    global rightclick_on_off
    status_label.configure(text='')
    rightclick_on_off = 0

auto_encode_last_options.bind("<Enter>", auto_encode_last_options_on_enter)
auto_encode_last_options.bind("<Leave>", auto_encode_last_options_on_leave)
root.bind('<Button-3>', popup_auto_e_b_menu)  # Uses mouse button 3 (right click) to pop up menu
# --------------------------------------------------------------------------- Start Audio Job: Auto

# Status Label at bottom of main GUI -----------------------------------------------------------------
status_label = Label(root, text='', bd=4, relief=SUNKEN, anchor=E, background='#717171', foreground="white")
status_label.grid(column=0, row=4, columnspan=4, sticky=W + E)
# ----------------------------------------------------------------- Status Label at bottom of main GUI

# Checks for App Folder and Sub-Directories - Creates Folders if they are missing -------------------------------------
directory_check()
# -------------------------------------------------------------------------------------------------------- Folder Check

# Checks config for bundled app paths path ---------------
def check_ffmpeg():
    global ffmpeg
    # FFMPEG --------------------------------------------------------------
    if shutil.which('ffmpeg') != None:
        ffmpeg = '"' + str(pathlib.Path(shutil.which('ffmpeg'))).lower() + '"'
        messagebox.showinfo(title='Prompt!', message='ffmpeg.exe found on system PATH, '
                                                     'automatically setting path to location.\n\n'
                                                     'Note: This can be changed in the config.ini file'
                                                     ' or in the Options menu')
        if pathlib.Path("Apps/ffmpeg/ffmpeg.exe").exists():
            rem_ffmpeg = messagebox.askyesno(title='Delete Included ffmpeg?',
                                             message='Would you like to delete the included FFMPEG?')
            if rem_ffmpeg == True:
                try:
                    shutil.rmtree(str(pathlib.Path("Apps/ffmpeg")))
                except:
                    pass
        config.set('ffmpeg_path', 'path', ffmpeg)
        with open(config_file, 'w') as configfile:
            config.write(configfile)
    elif ffmpeg == '' and shutil.which('ffmpeg') == None:
        messagebox.showinfo(title='Info', message='Program will use the included '
                                                  '"ffmpeg.exe" located in the "Apps" folder')
        ffmpeg = '"' + str(pathlib.Path("Apps/ffmpeg/ffmpeg.exe")) + '"'
        try:
            config.set('ffmpeg_path', 'path', ffmpeg)
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except:
            pass
    # FFMPEG ------------------------------------------------------------------

def check_mediainfocli():
    global mediainfocli
    # mediainfocli -------------------------------------------------------------
    if mediainfocli == '' or not pathlib.Path(mediainfocli.replace('"', '')).exists():
        mediainfocli = '"' + str(pathlib.Path('Apps/MediaInfoCLI/MediaInfo.exe')) + '"'
        try:
            config.set('mediainfocli_path', 'path', mediainfocli)
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except:
            pass
    # mediainfocli ----------------------------------------------------------

def check_mpv_player():
    global mpv_player
    # mpv_player -------------------------------------------------------------
    if mpv_player == '' or not pathlib.Path(mpv_player.replace('"', '')).exists():
        mpv_player = '"' + str(pathlib.Path('Apps/mpv/mpv.exe')) + '"'
        try:
            config.set('mpv_player_path', 'path', mpv_player)
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except:
            pass
    # mpv_player ----------------------------------------------------------

def check_mediainfogui():
    global mediainfo
    # check_mediainfogui -------------------------------------------------------------
    if mediainfo == '' or not pathlib.Path(mediainfo.replace('"', '')).exists():
        mediainfo = '"' + str(pathlib.Path('Apps/MediaInfo/MediaInfo.exe')) + '"'
        try:
            config.set('mediainfogui_path', 'path', mediainfo)
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except:
            pass
    # check_mediainfogui ----------------------------------------------------------

if config['ffmpeg_path']['path'] == '' or not pathlib.Path(ffmpeg.replace('"', '')).exists():
    check_ffmpeg()
if config['mediainfocli_path']['path'] == '' or not pathlib.Path(mediainfocli.replace('"', '')).exists():
    check_mediainfocli()
if config['mpv_player_path']['path'] == '' or not pathlib.Path(mpv_player.replace('"', '')).exists():
    check_mpv_player()
if config['mediainfogui_path']['path'] == '' or not pathlib.Path(mediainfo.replace('"', '')).exists():
    check_mediainfogui()
# Checks config for bundled app paths path ---------------

# Download and unzip required apps to the needed folders --------------------------------------------------------------
def downloadfiles():
    root.withdraw()  # Hides main window until all the apps are downloaded/unzipped
    app_progress_bar = ttk.Progressbar(download_window, orient=HORIZONTAL, length=395, mode='determinate')
    app_progress_bar.grid(row=2)
    if ffmpeg_path.exists():  # Checks for ffmpeg.exe
        app_progress_bar['value'] += 12
        pass
    else:
        download_window_text.configure(text="Downloading FFMPEG...")
        try:
            with urlopen(ffmpeg_url) as zipresp:  # Collects ffmpeg.zip from a link and unzips it to where we need it
                with ZipFile(BytesIO(zipresp.read())) as zfile:
                    zfile.extractall('Apps/FFMPEG')
                    app_progress_bar['value'] += 12
                    download_window_text2.configure(text='Done!')
                    sleep(1)
                    download_window_text2.configure(text='Checking Next App...')
                    sleep(2)
        except URLError:  # If first link is dead, this checks for the 2nd link
            download_window_text2.configure(text='Link #1 is broken')
            sleep(2)
            download_window_text2.configure(text='Retrying with backup link...')
            sleep(2)
            try:
                with urlopen(ffmpeg_url2) as zipresp: # Downloads and unzips ffmpeg from 2nd link
                    with ZipFile(BytesIO(zipresp.read())) as zfile:
                        zfile.extractall('Apps/FFMPEG')
                        app_progress_bar['value'] += 12
                        download_window_text2.configure(text='Done!')
                        sleep(1)
                        download_window_text2.configure(text='Checking Next App...')
                        sleep(2)
            except:
                pass

    if fdkaac_path.exists():
        app_progress_bar['value'] += 12
        pass
    else:
        download_window_text2.configure(text='')
        download_window_text.configure(text="Downloading FDKAAC...")
        try:
            with urlopen(fdkaac_url) as zipresp:
                with ZipFile(BytesIO(zipresp.read())) as zfile:
                    zfile.extractall('Apps/fdkaac')
                    app_progress_bar['value'] += 12
                    download_window_text2.configure(text='Done!')
                    sleep(1)
                    download_window_text2.configure(text='Checking Next App...')
                    sleep(2)
        except URLError:
            download_window_text2.configure(text='Link #1 is broken')
            sleep(2)
            download_window_text2.configure(text='Retrying with backup link...')
            sleep(2)
            try:
                with urlopen(fdkaac_url2) as zipresp:
                    with ZipFile(BytesIO(zipresp.read())) as zfile:
                        zfile.extractall('Apps/fdkaac')
                        app_progress_bar['value'] += 12
                        download_window_text2.configure(text='Done!')
                        sleep(1)
                        download_window_text2.configure(text='Checking Next App...')
                        sleep(2)
            except:
                pass


    if mediainfo_path.exists():
        app_progress_bar['value'] += 12
        pass
    else:
        download_window_text2.configure(text='')
        download_window_text.configure(text="Downloading MediaInfoGUI...")
        sleep(2)
        try:
            with urlopen(mediainfo_url) as zipresp:
                with ZipFile(BytesIO(zipresp.read())) as zfile:
                    zfile.extractall('Apps/MediaInfo')
                    app_progress_bar['value'] += 12
                    download_window_text2.configure(text='Done!')
                    sleep(1)
                    download_window_text2.configure(text='Checking Next App...')
                    sleep(2)
        except URLError:
            download_window_text2.configure(text='Link #1 is broken')
            sleep(2)
            download_window_text2.configure(text='Retrying with backup link...')
            sleep(2)
            try:
                with urlopen(mediainfo_url2) as zipresp:
                    with ZipFile(BytesIO(zipresp.read())) as zfile:
                        zfile.extractall('Apps/MediaInfo')
                        app_progress_bar['value'] += 12
                        download_window_text2.configure(text='Done!')
                        sleep(1)
                        download_window_text2.configure(text='Checking Next App...')
                        sleep(2)
            except:
                pass

    if mediainfocli_path.exists():
        app_progress_bar['value'] += 12
        pass
    else:
        download_window_text2.configure(text='')
        download_window_text.configure(text="Downloading MediaInfoCLI...")
        sleep(2)
        try:
            with urlopen(mediainfocli_url) as zipresp:
                with ZipFile(BytesIO(zipresp.read())) as zfile:
                    zfile.extractall('Apps/MediaInfoCLI')
                    app_progress_bar['value'] += 12
                    download_window_text2.configure(text='Done!')
                    sleep(1)
                    download_window_text2.configure(text='Checking Next App...')
                    sleep(2)
        except URLError:
            download_window_text2.configure(text='Link #1 is broken')
            sleep(2)
            download_window_text2.configure(text='Retrying with backup link...')
            sleep(2)
            try:
                with urlopen(mediainfocli_url2) as zipresp:
                    with ZipFile(BytesIO(zipresp.read())) as zfile:
                        zfile.extractall('Apps/MediaInfoCLI')
                        app_progress_bar['value'] += 12
                        download_window_text2.configure(text='Done!')
                        sleep(1)
                        download_window_text2.configure(text='Checking Next App...')
                        sleep(2)
            except:
                pass

    if qaac_path.exists():
        app_progress_bar['value'] += 12
        pass
    else:
        download_window_text2.configure(text='')
        download_window_text.configure(text="Downloading QAAC...")
        try:
            with urlopen(qaac_url) as zipresp:
                with ZipFile(BytesIO(zipresp.read())) as zfile:
                    zfile.extractall('Apps/qaac')
                    app_progress_bar['value'] += 12
                    download_window_text2.configure(text='Done!')
                    sleep(1)
                    download_window_text2.configure(text='Checking Next App...')
                    sleep(2)
        except URLError:
            download_window_text2.configure(text='Link #1 is broken')
            sleep(2)
            download_window_text2.configure(text='Retrying with backup link...')
            sleep(2)
            try:
                with urlopen(qaac_url2) as zipresp:
                    with ZipFile(BytesIO(zipresp.read())) as zfile:
                        zfile.extractall('Apps/qaac')
                        app_progress_bar['value'] += 12
                        download_window_text2.configure(text='Done!')
                        sleep(1)
                        download_window_text2.configure(text='Checking Next App...')
                        sleep(2)
            except:
                pass

    if mpv_player_path.exists():
        app_progress_bar['value'] += 12
        pass
    else:
        download_window_text2.configure(text='')
        download_window_text.configure(text="Downloading MPV Player...")
        try:
            with urlopen(mpv_player_url) as zipresp:
                with ZipFile(BytesIO(zipresp.read())) as zfile:
                    zfile.extractall('Apps/mpv')
                    app_progress_bar['value'] += 12
                    download_window_text2.configure(text='Done!')
                    sleep(1)
                    download_window_text2.configure(text='Checking Next App...')
                    sleep(2)
        except URLError:
            download_window_text2.configure(text='Link #1 is broken')
            sleep(2)
            download_window_text2.configure(text='Retrying with backup link...')
            sleep(2)
            try:
                with urlopen(mpv_player_url2) as zipresp:
                    with ZipFile(BytesIO(zipresp.read())) as zfile:
                        zfile.extractall('Apps/mpv')
                        app_progress_bar['value'] += 12
                        download_window_text2.configure(text='Done!')
                        sleep(1)
                        download_window_text2.configure(text='Checking Next App...')
                        sleep(2)
            except:
                pass

    if youtubedl_path.exists():
        app_progress_bar['value'] += 12
        pass
    else:
        download_window_text2.configure(text='')
        download_window_text.configure(text="Youtube-DL...")
        try:
            urlretrieve(youtubedl_url, 'Apps/youtube-dl/youtube-dl.exe')  # Direct downloads youtube-dl.exe from website
            urlretrieve(msvcr100dll_url, 'Apps/youtube-dl/msvcr100.dll')
            app_progress_bar['value'] += 12
            download_window_text2.configure(text='Done!')
            sleep(1)
            download_window_text2.configure(text='Checking Next App...')
            sleep(2)
        except URLError:  # If the link is broken it will run this block
            download_window_text2.configure(text='Link #1 is broken')
            sleep(2)
            download_window_text2.configure(text='Retrying with backup link...')
            sleep(2)
            try:
                with urlopen(youtubedl_url2) as zipresp:  # Gets youtube-dl.exe from a backup link
                    with ZipFile(BytesIO(zipresp.read())) as zfile:
                        zfile.extractall('Apps/youtube-dl')
                        app_progress_bar['value'] += 12
                        download_window_text2.configure(text='Done!')
                        sleep(1)
                        download_window_text2.configure(text='Checking Next App...')
                        sleep(2)
            except:
                pass

    download_window_text2.configure(text='')
    app_progress_bar['value'] += 27
    download_window_text.configure(text='Completed!')
    sleep(2)
    download_window.destroy()
    root.deiconify()
# -------------------------------------------------------------------------------------------------- Download and Unzip

# Checks for Required Apps --------------------------------------------------------------------------------------------

ffmpeg_path = pathlib.Path(ffmpeg.replace('"', ''))
mediainfocli_path = pathlib.Path(mediainfocli.replace('"', ''))
mediainfo_path = pathlib.Path(mediainfo.replace('"', ''))
mpv_player_path = pathlib.Path(mpv_player.replace('"', ''))
fdkaac_path = pathlib.Path("Apps/fdkaac/fdkaac.exe")
qaac_path = pathlib.Path("Apps/qaac/qaac64.exe")

if shutil.which("youtube-dl") != None:
    youtubedl_path = pathlib.Path(shutil.which("youtube-dl"))
elif shutil.which("youtube-dl") == None:
    youtubedl_path = pathlib.Path("Apps/youtube-dl/youtube-dl.exe")

if ffmpeg_path.exists() and mediainfo_path.exists() and mediainfocli_path.exists() and fdkaac_path.exists() and \
        qaac_path.exists() and mpv_player_path.exists() and youtubedl_path.exists():
    pass
else:
    missing_files = messagebox.askyesno(title='Missing Files', message='Download Required Binaries?', parent=root)
    if missing_files == False:
        msg_box = messagebox.showinfo(title='Error', message='Download required files manually for program to work '
                                                             ' correctly!!! \n\nPlace required files in the '
                                                             'Apps directory and restart the program',
                                      parent=root)
        root.destroy()
    elif missing_files == True:
        def dw_exit_function():
            confirm_exit = messagebox.askyesno(title='Prompt', message="Are you sure you want to exit the program?\n"
                                                                       "\nYou could potentially corrupt some required"
                                                                       " applications\n\nIf this happens delete the "
                                                                       "'Apps' folder and restart the program",
                                                parent=root)
            if confirm_exit == False:
                pass
            elif confirm_exit == True:
                root.destroy()

        download_window = Toplevel(master=root)
        download_window.title('Download')
        download_window.configure(background="#434547")
        window_height = 80
        window_width = 400
        screen_width = download_window.winfo_screenwidth()
        screen_height = download_window.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        download_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
        download_window.resizable(False, False)
        download_window.protocol('WM_DELETE_WINDOW', dw_exit_function)
        download_window_text = Label(download_window, background="#434547", foreground="white", width=50)
        download_window_text.grid(row=0, column=0, columnspan=2)
        download_window_text2 = Label(download_window, background="#434547", foreground="white", width=50)
        download_window_text2.grid(row=1, column=0, columnspan=2)
        threading.Thread(target=downloadfiles).start()

# -------------------------------------------------------------------------------------------- Checks for required apps



# End Loop ------------------------------------------------------------------------------------------------------------
root.mainloop()