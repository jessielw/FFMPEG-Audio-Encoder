# Imports--------------------------------------------------------------------
import webbrowser
from tkinter import *
from tkinter import filedialog, StringVar
from tkinter import ttk
import subprocess
import tkinter as tk
import pathlib
import tkinter.scrolledtext as scrolledtextwidget
from TkinterDnD2 import *
from tkinter import messagebox
from time import sleep
import threading
import shutil
from Packages.DirectoryCheck import directory_check
from Packages.SimpleYoutubeDLGui import youtube_dl_launcher_for_ffmpegaudioencoder
from Packages.FFMPEGAudioEncoderBatch import batch_processing
from Packages.About import openaboutwindow
from Packages.config_params import create_config_params
from configparser import ConfigParser
from ctypes import windll
from pymediainfo import MediaInfo
import pyperclip
from re import findall as re_findall, search as re_search
from idlelib.tooltip import Hovertip


# Main Gui & Windows --------------------------------------------------------
def root_exit_function():
    try:  # Check to see if any children window are open before displaying message
        if audio_window.winfo_exists() or cmd_line_window.winfo_exists():  # If open display message
            confirm_exit = messagebox.askyesno(title='Prompt', message="Are you sure you want to exit the program?\n\n"
                                                                       "Warning:\nThis will end all current tasks "
                                                                       "and close all windows!", parent=root)
            if confirm_exit:
                try:
                    subprocess.Popen(f"TASKKILL /F /im FFMPEGAudioEncoder.exe /T",
                                     creationflags=subprocess.CREATE_NO_WINDOW)
                    root.destroy()
                except (Exception,):
                    root.destroy()
    except NameError:  # If no children window are present close main gui without prompt
        root.destroy()


root = TkinterDnD.Tk()
root.title("FFMPEG Audio Encoder v3.38")
root.iconphoto(True, PhotoImage(file="Runtime/Images/topbar.png"))
root.configure(background="#434547")
window_height = 220
window_width = 460
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
root.protocol('WM_DELETE_WINDOW', root_exit_function)

# Block of code to fix DPI awareness issues on Windows 7 or higher
try:
    windll.shcore.SetProcessDpiAwareness(2)  # if your Windows version >= 8.1
except(Exception,):
    windll.user32.SetProcessDPIAware()  # Windows 8.0 or less
# Block of code to fix DPI awareness issues on Windows 7 or higher

for n in range(4):
    root.grid_columnconfigure(n, weight=1)
for n in range(4):
    root.grid_rowconfigure(n, weight=1)

# Themes --------------------------------------------------------------------------------------------------------------
# Custom Tkinter Theme-----------------------------------------
custom_style = ttk.Style()
custom_style.theme_create('jlw_style', parent='alt')
custom_style.theme_use('jlw_style')  # Enable the use of the custom theme
custom_style.configure("custom.Horizontal.TProgressbar", background="#3a4145")


# ------------------------------------------ Custom Tkinter Theme
# Hover over button theme ---------------------------------------
class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']
        if self.cget('text') == 'Open File':
            status_label.configure(text='Open file or drag and drop file...')
        if self.cget('text') == 'Display\nCommand':
            status_label.configure(text='Display command-line...')
        if self.cget('text') == 'Save File':
            status_label.configure(text='Specify save location...')
        if self.cget('text') == 'Auto Encode:\nLast Used Options':
            global rightclick_on_off
            status_label.configure(text='Right click for more options...')
            rightclick_on_off = 1
        if self.cget('text') == 'Audio Settings':
            status_label.configure(text='Configure selected audio codec..')
        if self.cget('text') == 'Start Audio Job':
            status_label.configure(text='Start job..')

    def on_leave(self, e):
        self['background'] = self.defaultBackground
        if self.cget('text') == 'Auto Encode:\nLast Used Options':
            global rightclick_on_off
            status_label.configure(text='Right Click For More Options...')
            rightclick_on_off = 0
            status_label.configure(text='')
        else:
            status_label.configure(text='')


# --------------------------------------- Hover over button theme
# -------------------------------------------------------------------------------------------------------------- Themes

# ------------------------------------------------------------------------------------------------------- Config Parser
create_config_params()  # Runs the funciton to define/create all the parameters in the needed .ini files
# Defines the path to config.ini and opens it for reading/writing
config_file = 'Runtime/config.ini'  # Creates (if doesn't exist) and defines location of config.ini
config = ConfigParser()
config.read(config_file)

# Defines the path to profiles.ini and opens it for reading/writing
config_profile_ini = 'Runtime/profiles.ini'  # Creates (if doesn't exist) and defines location of profile.ini
config_profile = ConfigParser()
config_profile.read(config_profile_ini)
# Config Parser -------------------------------------------------------------------------------------------------------

# Bundled Apps --------------------------------------------------------------------------------------------------------
ffmpeg = config['ffmpeg_path']['path']
mediainfocli = config['mediainfocli_path']['path']
mediainfo = config['mediainfogui_path']['path']
fdkaac = '"Apps/fdkaac/fdkaac.exe"'
qaac = '"Apps/qaac/qaac64.exe"'
mpv_player = config['mpv_player_path']['path']


# -------------------------------------------------------------------------------------------------------- Bundled Apps


# Open InputFile with portable MediaInfo ------------------------------------------------------------------------------
def mediainfogui():
    try:
        VideoInputQuoted = '"' + VideoInput + '"'
        commands = mediainfo + " " + VideoInputQuoted
        subprocess.Popen(commands)
    except (Exception,):
        commands = mediainfo
        subprocess.Popen(commands)


# ----------------------------------------------------------------------------------------------------------- MediaInfo

# Open InputFile with portable mpv ------------------------------------------------------------------------------------
def mpv_gui_main_gui():
    try:
        VideoInputQuoted = '"' + VideoInput + '"'
        commands = mpv_player + " " + VideoInputQuoted
        subprocess.Popen(commands)
    except (Exception,):
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
    except (Exception,):
        pass


update_shell_option()
options_submenu.add_radiobutton(label='Progress Bars', variable=shell_options,
                                value="Default", command=update_shell_option)
options_submenu.add_radiobutton(label='CMD Shell (Debug)', variable=shell_options,
                                value="Debug", command=update_shell_option)

auto_close_window = StringVar()
auto_close_window.set(config['auto_close_progress_window']['option'])
if auto_close_window.get() == '':
    auto_close_window.set('on')
elif auto_close_window.get() != '':
    auto_close_window.set(config['auto_close_progress_window']['option'])


def update_auto_close():
    try:
        config.set('auto_close_progress_window', 'option', auto_close_window.get())
        with open(config_file, 'w') as configfile:
            config.write(configfile)
    except (Exception,):
        pass


update_auto_close()
options_submenu2 = Menu(root, tearoff=0, activebackground='dim grey')
options_menu.add_cascade(label='Auto-Close Progress Window On Completion', menu=options_submenu2)
options_submenu2.add_radiobutton(label='On', variable=auto_close_window, value='on', command=update_auto_close)
options_submenu2.add_radiobutton(label='Off', variable=auto_close_window, value='off', command=update_auto_close)

options_menu.add_separator()


def set_ffmpeg_path():
    global ffmpeg
    path = filedialog.askopenfilename(title='Select Location to "ffmpeg.exe"', initialdir='/',
                                      filetypes=[('ffmpeg', 'ffmpeg.exe')])
    if path != '':
        ffmpeg = '"' + str(pathlib.Path(path)) + '"'
        config.set('ffmpeg_path', 'path', ffmpeg)
        with open(config_file, 'w') as configfile:
            config.write(configfile)


options_menu.add_command(label='Set path to FFMPEG', command=set_ffmpeg_path)


def set_mpv_player_path():
    global mpv_player
    path = filedialog.askopenfilename(title='Select Location to "mpv.exe"', initialdir='/',
                                      filetypes=[('mpv', 'mpv.exe')])
    if path != '':
        mpv_player = '"' + str(pathlib.Path(path)) + '"'
        config.set('mpv_player_path', 'path', mpv_player)
        with open(config_file, 'w') as configfile:
            config.write(configfile)


options_menu.add_command(label='Set path to MPV player', command=set_mpv_player_path)


def set_mediainfogui_path():
    global mediainfo
    path = filedialog.askopenfilename(title='Select Location to "MediaInfo.exe"', initialdir='/',
                                      filetypes=[('MediaInfoGUI', 'MediaInfo.exe')])
    if path != '':
        mediainfo = '"' + str(pathlib.Path(path)) + '"'
        config.set('mediainfogui_path', 'path', mediainfo)
        with open(config_file, 'w') as configfile:
            config.write(configfile)


options_menu.add_command(label='Set path to MediaInfo - GUI', command=set_mediainfogui_path)


def set_mediainfocli_path():
    global mediainfocli
    path = filedialog.askopenfilename(title='Select Location to "MediaInfo.exe"', initialdir='/',
                                      filetypes=[('MediaInfo', 'MediaInfo.exe')])
    if path != '':
        mediainfocli = '"' + str(pathlib.Path(path)) + '"'
        config.set('mediainfocli_path', 'path', mediainfocli)
        with open(config_file, 'w') as configfile:
            config.write(configfile)


options_menu.add_command(label='Set path to MediaInfo - CLI', command=set_mediainfocli_path)

options_menu.add_separator()


def reset_config():
    msg = messagebox.askyesno(title='Warning', message='Are you sure you want to reset the config.ini file settings?')
    if msg:
        try:
            config.set('ffmpeg_path', 'path', '')
            config.set('mpv_player_path', 'path', '')
            config.set('mediainfocli_path', 'path', '')
            config.set('mediainfogui_path', 'path', '')
            config.set('debug_option', 'option', 'Default')
            with open(config_file, 'w') as configfile:
                config.write(configfile)
            messagebox.showinfo(title='Prompt', message='Please restart the program')
        except (Exception,):
            pass
        root.destroy()


options_menu.add_command(label='Reset Configuration File', command=reset_config)

tools_submenu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
my_menu_bar.add_cascade(label='Tools', menu=tools_submenu)
tools_submenu.add_command(label="MediaInfo", command=mediainfogui)
tools_submenu.add_command(label="MPV (Media Player)", command=mpv_gui_main_gui)
tools_submenu.add_command(label="Simple-Youtube-DL-Gui", command=youtube_dl_launcher_for_ffmpegaudioencoder)
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
def set_auto_save_suffix():
    global VideoOut
    if encoder.get() != "Set Codec":
        filename = pathlib.Path(VideoInput)
        if encoder.get() == 'AAC':
            VideoOut = filename.with_suffix('._new_.mp4')
        elif encoder.get() == 'AC3' or encoder.get() == 'E-AC3':
            VideoOut = filename.with_suffix('._new_.ac3')
        elif encoder.get() == "DTS":
            VideoOut = filename.with_suffix('._new_.dts')
        elif encoder.get() == "Opus":
            VideoOut = filename.with_suffix('._new_.opus')
        elif encoder.get() == 'MP3':
            VideoOut = filename.with_suffix('._new_.mp3')
        elif encoder.get() == "FDK-AAC" or encoder.get() == "QAAC" or encoder.get() == "ALAC":
            VideoOut = filename.with_suffix('._new_.m4a')
        elif encoder.get() == "FLAC":
            VideoOut = filename.with_suffix('._new_.flac')


def encoder_changed(*args):
    global VideoOutput, autosavefilename, VideoOut
    if encoder.get() != "Set Codec":
        set_auto_save_suffix()
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
def track_counter(*args):  # Thanks for helping me shorten this 'gmes78'
    global acodec_stream_track_counter, t_info
    mediainfocli_cmd_info = '"' + mediainfocli + " " + '--Output="Audio;' \
                            + " |  %Format%  |  %Channel(s)% Channels  |  %BitRate/String% ," \
                            + '"' + " " + VideoInputQuoted + '"'
    mediainfo_count = subprocess.Popen('cmd /c ' + mediainfocli_cmd_info, creationflags=subprocess.CREATE_NO_WINDOW,
                                       universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       stdin=subprocess.PIPE, encoding="utf-8")
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
encoder_menu = OptionMenu(root, encoder, *encoder_dropdownmenu_choices.keys(), command=track_counter)
encoder_menu.grid(row=1, column=2, columnspan=1, padx=5, pady=5, sticky=N + S + W + E)
encoder_menu.config(state=DISABLED, background="#23272A", foreground="white", highlightthickness=1, width=10)
encoder_menu["menu"].configure(activebackground="dim grey")
codec_label = Label(root, text="Codec ->", background="#434547", foreground="White")
codec_label.grid(row=1, column=1, columnspan=1, padx=5, pady=5, sticky=N + S + W + E)


# -------------------------------------------------------------------------------------------------------- Encoder Menu

# Audio Codec Window --------------------------------------------------------------------------------------------------
def openaudiowindow():
    global acodec_bitrate, acodec_channel, acodec_channel_choices, acodec_bitrate_choices, acodec_stream, \
        acodec_stream_choices, acodec_volume, acodec_volume_choices, dts_settings, dts_settings_choices, \
        acodec_vbr_choices, acodec_vbr, acodec_samplerate, acodec_samplerate_choices, acodec_application, \
        acodec_application_choices, acodec_profile, acodec_profile_choices, acodec_atempo, acodec_atempo_choices, \
        opus_mapping_family_choices, opus_mapping_family, gotosavefile, set_encode_manual

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

    def opus_mapping_family_menu_hover(e):
        opus_mapping_family_menu["bg"] = "grey"
        opus_mapping_family_menu["activebackground"] = "grey"

    def opus_mapping_family_menu_hover_leave(e):
        opus_mapping_family_menu["bg"] = "#23272A"

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
        global mpv_track_number, acodec_stream
        if acodec_stream.get() != 'None':
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
            ffmpeg_volume_cmd = '"volume=' + ffmpeg_volume.get() + '"'
            if ffmpeg_volume.get() == '0.0' and acodec_atempo_choices[acodec_atempo.get()] == '':
                audio_filter_setting = ''
            elif ffmpeg_volume.get() != '0.0' and acodec_atempo_choices[acodec_atempo.get()] == '':
                audio_filter_setting = '-af ' + ffmpeg_volume_cmd + ' '
            elif ffmpeg_volume.get() == '0.0' and acodec_atempo_choices[acodec_atempo.get()] != '':
                audio_filter_setting = '-af ' + acodec_atempo_choices[acodec_atempo.get()] + ' '
            elif ffmpeg_volume.get() != '0.0' and acodec_atempo_choices[acodec_atempo.get()] != '':
                audio_filter_setting = '-af ' + ffmpeg_volume_cmd + ',' + acodec_atempo_choices[
                    acodec_atempo.get()] + ' '
        else:
            ffmpeg_volume_cmd = '"volume=' + ffmpeg_volume.get() + '"'
            if dolby_pro_logic_ii.get() == '' and ffmpeg_volume.get() == '0.0' and \
                    acodec_atempo_choices[acodec_atempo.get()] == '':
                audio_filter_setting = ''
            elif dolby_pro_logic_ii.get() == '"aresample=matrix_encoding=dplii"' and \
                    ffmpeg_volume.get() == '0.0' and acodec_atempo_choices[acodec_atempo.get()] == '':
                audio_filter_setting = '-af ' + dolby_pro_logic_ii.get() + ' '

            elif dolby_pro_logic_ii.get() == '"aresample=matrix_encoding=dplii"' \
                    and ffmpeg_volume.get() != '0.0' and acodec_atempo_choices[acodec_atempo.get()] == '':
                audio_filter_setting = '-af ' + dolby_pro_logic_ii.get() + ',' + \
                                       ffmpeg_volume_cmd + ' '
            elif dolby_pro_logic_ii.get() == '' and ffmpeg_volume.get() != '0.0' and \
                    acodec_atempo_choices[acodec_atempo.get()] == '':
                audio_filter_setting = '-af ' + ffmpeg_volume_cmd + ' '
            elif dolby_pro_logic_ii.get() == '"aresample=matrix_encoding=dplii"' and \
                    ffmpeg_volume.get() == '0.0' and acodec_atempo_choices[acodec_atempo.get()] != '':
                audio_filter_setting = '-af ' + dolby_pro_logic_ii.get() + ',' + \
                                       acodec_atempo_choices[acodec_atempo.get()] + ' '
            elif dolby_pro_logic_ii.get() == '"aresample=matrix_encoding=dplii"' \
                    and ffmpeg_volume.get() != '0.0' and acodec_atempo_choices[acodec_atempo.get()] != '':
                audio_filter_setting = '-af ' + dolby_pro_logic_ii.get() + ',' + \
                                       ffmpeg_volume_cmd + ',' + acodec_atempo_choices[acodec_atempo.get()] + ' '
            elif dolby_pro_logic_ii.get() == '' and ffmpeg_volume.get() != '0.0' and \
                    acodec_atempo_choices[acodec_atempo.get()] != '':
                audio_filter_setting = '-af ' + ffmpeg_volume_cmd + ',' + \
                                       acodec_atempo_choices[acodec_atempo.get()] + ' '
            elif dolby_pro_logic_ii.get() == '' and \
                    ffmpeg_volume.get() == '0.0' and acodec_atempo_choices[acodec_atempo.get()] != '':
                audio_filter_setting = '-af ' + acodec_atempo_choices[acodec_atempo.get()] + ' '

    # ---------------------------------------------------------------------------------------------------- combines -af

    # Set auto_or_manual to 'manual' when clicked by codecs in audio settings window ----------------------------------
    def set_encode_manual():
        global auto_or_manual
        auto_or_manual = 'manual'

    # ---------------------------------- Set auto_or_manual to 'manual' when clicked by codecs in audio settings window

    # 'Apply' button function -----------------------------------------------------------------------------------------
    def gotosavefile():
        global VideoInput, delay_string, language_string
        output_button.config(state=NORMAL)  # Enable buttons upon save file
        start_audio_button.config(state=NORMAL)
        command_line_button.config(state=NORMAL)

        try:  # If cmd_line_window is open, withdraw it (close it)
            cmd_line_window.withdraw()
        except (Exception,):
            pass

        language_string = ''  # Place holder variable
        delay_string = ''  # Place holder variable

        def update_video_output():  # Function to add language/delay strings to the output filename
            global VideoOutput, autosavefilename, total_streams
            set_auto_save_suffix()  # Run function to apply default VideoOutput before continuing code
            audio_track_number_string = f'[Audio#{acodec_stream.get().split()[1][-1]}]'
            if total_streams == 1:  # If total_streams equals 1
                VideoOutput = str(VideoOutput).replace('_new_', audio_track_number_string)  # Replace _new_ with Audio#
            elif total_streams >= 2:  # If total_streams is 2 or greater
                VideoOutput = str(VideoOutput).replace('_new_', audio_track_number_string + language_string
                                                       + delay_string)  # Replace '_new_'
            autosavefilename = pathlib.Path(VideoOutput).stem
            command_line_button.config(state=NORMAL)  # Enable the display command button for main gui
            output_entry.config(state=NORMAL)  # Enable output_entry box for editing
            output_entry.delete(0, END)  # Remove all text from box
            output_entry.insert(0, VideoOutput)  # Insert new VideoOutput path
            output_entry.config(state=DISABLED)  # Disable output_entry box

        def delay_and_lang_check():
            global language_string, delay_string, auto_or_manual, auto_track_input, total_streams
            # If input is only 1 track, parse input file name for language and delay string
            media_info = MediaInfo.parse(VideoInput)  # Parse VideoInput
            general_track = media_info.general_tracks[0]
            total_streams = 0  # Empty variable to add up all the tracks
            if general_track.count_of_video_streams is not None:
                total_streams += int(general_track.count_of_video_streams)  # check for video track(s)
            if general_track.count_of_audio_streams is not None:
                total_streams += int(general_track.count_of_audio_streams)  # check for audio track(s)
            if general_track.count_of_subtitle_streams is not None:
                total_streams += int(general_track.count_of_subtitle_streams)  # check for subtitle track(s)
            if general_track.count_of_menu_streams is not None:
                total_streams += int(general_track.count_of_menu_streams)  # check for menu track(s)

            if total_streams == 1:  # If total streams is equal to 1
                try:
                    if auto_or_manual == 'manual':  # If normal encoding is used with the start job button
                        audio_window.destroy()  # Close audio window
                        track_selection_mediainfo = media_info.audio_tracks[
                            int(acodec_stream_choices[acodec_stream.get()].strip()[-1])]
                except NameError:  # If auto_or_manual does not exist yet
                    pass

                try:
                    if auto_or_manual == 'auto':
                        audio_window.destroy()  # Destroy audio window, only opens to define variables inside it
                    # parse input file name for language and delay string
                    # language_code_input = re_findall(r"\[([A-Za-z]+)\]", str(VideoInput))
                    # if language_code_input:  # If re finds language codes within '[]'
                    #     lng_input_lengths = [len(i) for i in language_code_input]
                    #     if 3 in lng_input_lengths:  # If anything within the brackets is 3 digits
                    #         index = lng_input_lengths.index(3)  # Finds index of string inside brackets that's 3 digits
                    #         language_string = str(f'[{language_code_input[index]}]')  # Set's language string to index
                    # if not language_code_input:
                    #     language_string = ''
                    #
                    # # parse input filename for delay string, it searches for ms and any numbers (- if it has it)
                    # input_delay_string = re_search('-*[^a-zA-Z [_{+]*ms', VideoInput)
                    # if input_delay_string:  # If re finds a delay string in the input filename
                    #     delay_string = f'[delay {str(input_delay_string[0])}]'
                    # if not input_delay_string:
                    #     delay_string = ''

                    language_string = ''
                    delay_string = ''
                    auto_track_input = 0  # Since there is only 1 stream, set 0 as value (-map 0:a:'value')

                except NameError:
                    audio_window.destroy()

            if total_streams >= 2:  # If total streamss are greater than 1 (video input, remux, bluray, dvd, etc...)
                # Check delay and add delay string to variable --------------------------------------------------------
                try:
                    if auto_or_manual == 'manual':  # If normal encoding is used with the start job button
                        audio_window.destroy()  # Close audio window
                        track_selection_mediainfo = media_info.audio_tracks[
                            int(acodec_stream_choices[acodec_stream.get()].strip()[-1])]
                except NameError:  # If auto_or_manual does not exist yet
                    pass

                try:
                    if auto_or_manual == 'auto':
                        audio_window.destroy()  # Destroy audio window, only opens to define variables inside it

                        def track_window():  # Function to select which audio track user would like to encode with
                            global auto_track_input, acodec_stream, acodec_stream_choices
                            audio_track_win = Toplevel()  # Toplevel window
                            audio_track_win.configure(background='#191a1a')  # Set color of audio_track_win background
                            window_height = 340  # win height
                            window_width = 478  # win width
                            screen_width = audio_track_win.winfo_screenwidth()  # down
                            screen_height = audio_track_win.winfo_screenheight()  # down
                            x_coordinate = int((screen_width / 2) - (window_width / 2))  # down
                            y_coordinate = int((screen_height / 2) - (window_height / 2))  # down
                            audio_track_win.geometry(
                                f'{window_width}x{window_height}+{x_coordinate}+{y_coordinate}')  # code calculates
                            # middle position of window
                            audio_track_win.resizable(0, 0)  # makes window not resizable
                            audio_track_win.overrideredirect(1)  # will remove the top badge of window
                            audio_track_win.grab_set()  # forces audio_track_win to stay on top of root
                            root.attributes('-alpha', 0.8)  # Lowers mp4root transparency to .8

                            # Track Frame -----------------------------------------------------------------------------
                            # Define track frame
                            track_frame = LabelFrame(audio_track_win, text=' Track Selection ')
                            track_frame.grid(row=0, column=0, columnspan=5, sticky=E + W, padx=10, pady=(8, 0))
                            track_frame.configure(fg="white", bg="#636669", bd=3)

                            track_frame.rowconfigure(0, weight=1)
                            track_frame.grid_columnconfigure(0, weight=1)

                            # ----------------------------------------------------------------------------- Track Frame

                            # Menu to show track(s) information -------------------------------------------------------
                            def update_track_window_text(*args):
                                mapping_number = int(str(acodec_stream.get()).split()[1][1]) - 1
                                show_cmd_scrolled.configure(state=NORMAL, bg='black', fg='#CFD2D1', bd=8)
                                show_cmd_scrolled.delete(1.0, END)
                                show_cmd_scrolled.insert(END, f"-map 0:a:{str(mapping_number)} "
                                                              f"{str(config_profile['Auto Encode']['command'])}")
                                show_cmd_scrolled.see(END)
                                show_cmd_scrolled.configure(state=DISABLED)

                            show_cmd_scrolled = scrolledtextwidget.ScrolledText(track_frame, width=30, height=6,
                                                                                tabs=10, spacing2=3, spacing1=2,
                                                                                spacing3=3)
                            show_cmd_scrolled.grid(row=1, column=0, columnspan=3, pady=(20, 4), padx=5, sticky=E + W)
                            show_cmd_scrolled.configure(state=NORMAL, bg='black', fg='#CFD2D1', bd=8)
                            show_cmd_scrolled.insert(END, f"-map 0:a:0 {str(config_profile['Auto Encode']['command'])}")
                            show_cmd_scrolled.see(END)
                            show_cmd_scrolled.configure(state=DISABLED)

                            acodec_stream = StringVar()
                            acodec_stream_choices = acodec_stream_track_counter
                            acodec_stream.set(next(iter(acodec_stream_track_counter)))  # set the default option
                            acodec_stream_menu = OptionMenu(track_frame, acodec_stream, *acodec_stream_choices.keys())
                            acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1,
                                                      width=48, anchor='w')
                            acodec_stream_menu.grid(row=0, column=0, columnspan=3, padx=10, pady=6,
                                                    sticky=N + S + W + E)
                            acodec_stream_menu["menu"].configure(activebackground="dim grey")
                            acodec_stream.trace('w', update_track_window_text)

                            # ------------------------------------------------------- Menu to show track(s) information

                            def close_audio_start():  # Funciton is used when 'Confirm Track and Start' is clicked
                                global auto_track_input
                                root.attributes('-alpha', 1.0)  # Restores root transparency to default
                                audio_track_win.grab_release()
                                audio_track_win.destroy()  # Closes audio window
                                # Get track number  and subtract 1 for ffmpeg (Track 1 = -map 0:a:0)
                                auto_track_input = int(str(acodec_stream.get()).split()[1][1]) - 1

                            def close_audio_cancel():  # Function is used when 'Cancel' is clicked
                                global acodec_stream
                                root.attributes('-alpha', 1.0)  # Restores root transparency to default
                                audio_track_win.grab_release()
                                audio_track_win.destroy()  # Closes audio window
                                acodec_stream.set('None')  # Set acodec_stream to None, so job does not start
                                auto_encode_last_options.configure(state=NORMAL)  # Keeps auto_encode button enabled

                            # Button Code -----------------------------------------------------------------------------
                            select_track = HoverButton(track_frame, text="Confirm Track and Start",
                                                       command=close_audio_start, foreground="white",
                                                       background="#23272A",
                                                       borderwidth="3", activebackground='grey')
                            select_track.grid(row=2, column=2, columnspan=1, padx=5, pady=(40, 5), sticky=E)

                            cancel_select = HoverButton(track_frame, text="Cancel", command=close_audio_cancel,
                                                        foreground="white", background="#23272A", borderwidth="3",
                                                        activebackground='grey')
                            cancel_select.grid(row=2, column=0, columnspan=1, padx=5, pady=(40, 5), sticky=W)
                            # ----------------------------------------------------------------------------- Button Code

                            audio_track_win.wait_window()  # Halts program until audio_track_win is closed

                        track_window()  # Opens audio_track_win to select tracks
                        track_selection_mediainfo = media_info.audio_tracks[int(auto_track_input)]

                except NameError:
                    audio_window.destroy()

                try:
                    if track_selection_mediainfo.delay_relative_to_video is not None:
                        delay_string = f'[delay {str(track_selection_mediainfo.delay_relative_to_video)}ms]'
                    else:
                        delay_string = str('[delay 0ms]')
                except UnboundLocalError:
                    pass

                try:
                    # Obtain language string from VideoInput's parsed track
                    if track_selection_mediainfo.other_language is not None:  # If language is not None
                        l_lengths = [len(i) for i in track_selection_mediainfo.other_language]  # List of language codes
                        if 3 in l_lengths:  # Find strings in l_lengths that only are equal to 3 characters
                            l_index = l_lengths.index(3)  # Save the index of the 3 character string to variable
                        language_string = f'[{str(track_selection_mediainfo.other_language[l_index])}]'
                    else:
                        language_string = '[und]'
                except UnboundLocalError:
                    pass

        delay_and_lang_check()
        update_video_output()
        # ------------------------------------------------------------ Check delay and add delay string to variable

    # ----------------------------------------------------------------------------------------- 'Apply' button function

    # Modify what the 'X' does at the top right of the audio window ---------------------------------------------------
    def audio_window_exit_function():  # When the 'X' is clicked, it does the same thing as the "Apply" button
        set_encode_manual()  # Calls set_encode_manual() function
        gotosavefile()  # Calls gotosavefile() function

    # --------------------------------------------------- Modify what the 'X' does at the top right of the audio window

    # Profile Functions -----------------------------------------------------------------------------------------------
    def save_profile():  # Function to save current settings in codec window
        if encoder.get() == 'AC3':
            config_profile.set('FFMPEG AC3 - SETTINGS', 'ac3_bitrate', acodec_bitrate.get())
            config_profile.set('FFMPEG AC3 - SETTINGS', 'dolbyprologicii', dolby_pro_logic_ii.get())
            config_profile.set('FFMPEG AC3 - SETTINGS', 'ffmpeg_volume', ffmpeg_volume.get())
            config_profile.set('FFMPEG AC3 - SETTINGS', 'ac3_channel', acodec_channel.get())
            config_profile.set('FFMPEG AC3 - SETTINGS', 'samplerate', acodec_samplerate.get())
            config_profile.set('FFMPEG AC3 - SETTINGS', 'tempo', acodec_atempo.get())
        if encoder.get() == 'AAC':
            config_profile.set('FFMPEG AAC - SETTINGS', 'dolbyprologicii', dolby_pro_logic_ii.get())
            config_profile.set('FFMPEG AAC - SETTINGS', 'ffmpeg_volume', ffmpeg_volume.get())
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
            config_profile.set('FFMPEG DTS - SETTINGS', 'ffmpeg_volume', ffmpeg_volume.get())
            config_profile.set('FFMPEG DTS - SETTINGS', 'dts_channel', acodec_channel.get())
            config_profile.set('FFMPEG DTS - SETTINGS', 'samplerate', acodec_samplerate.get())
            config_profile.set('FFMPEG DTS - SETTINGS', 'tempo', acodec_atempo.get())
        if encoder.get() == 'E-AC3':
            config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_bitrate', eac3_spinbox.get())
            config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_channel', acodec_channel.get())
            config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_volume', ffmpeg_volume.get())
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
            config_profile.set('FFMPEG Opus - SETTINGS', 'ffmpeg_volume', ffmpeg_volume.get())
            config_profile.set('FFMPEG Opus - SETTINGS', 'tempo', acodec_atempo.get())
            config_profile.set('FFMPEG Opus - SETTINGS', 'mapping_family', opus_mapping_family.get())
        if encoder.get() == 'FDK-AAC':
            config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_bitrate', acodec_bitrate.get())
            config_profile.set('FDK-AAC - SETTINGS', 'acodec_channel', acodec_channel.get())
            config_profile.set('FDK-AAC - SETTINGS', 'dolbyprologicii', dolby_pro_logic_ii.get())
            config_profile.set('FDK-AAC - SETTINGS', 'ffmpeg_volume', ffmpeg_volume.get())
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
            config_profile.set('FFMPEG MP3 - SETTINGS', 'ffmpeg_volume', ffmpeg_volume.get())
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
            config_profile.set('FFMPEG FLAC - SETTINGS', 'volume', ffmpeg_volume.get())
            config_profile.set('FFMPEG FLAC - SETTINGS', 'samplerate', acodec_samplerate.get())
            config_profile.set('FFMPEG FLAC - SETTINGS', 'tempo', acodec_atempo.get())
            config_profile.set('FFMPEG FLAC - SETTINGS', 'flac_lpc_type', acodec_flac_lpc_type.get())
            config_profile.set('FFMPEG FLAC - SETTINGS', 'flac_coefficient', flac_acodec_coefficient.get())
            config_profile.set('FFMPEG FLAC - SETTINGS', 'flac_lpc_passes', acodec_flac_lpc_passes.get())
        if encoder.get() == 'ALAC':
            config_profile.set('FFMPEG ALAC - SETTINGS', 'acodec_channel', acodec_channel.get())
            config_profile.set('FFMPEG ALAC - SETTINGS', 'dolbyprologicii', dolby_pro_logic_ii.get())
            config_profile.set('FFMPEG ALAC - SETTINGS', 'volume', ffmpeg_volume.get())
            config_profile.set('FFMPEG ALAC - SETTINGS', 'samplerate', acodec_samplerate.get())
            config_profile.set('FFMPEG ALAC - SETTINGS', 'tempo', acodec_atempo.get())
            config_profile.set('FFMPEG ALAC - SETTINGS', 'alac_min_prediction_order', min_prediction_order.get())
            config_profile.set('FFMPEG ALAC - SETTINGS', 'alac_max_prediction_order', max_prediction_order.get())

        with open(config_profile_ini, 'w') as configfile_two:
            config_profile.write(configfile_two)

    def reset_profile():  # This function resets settings to 'default'
        msg = messagebox.askyesno(title='Prompt', message='Are you sure you want to reset to default settings?',
                                  parent=audio_window)
        if msg:
            if encoder.get() == 'AC3':
                config_profile.set('FFMPEG AC3 - SETTINGS', 'ac3_bitrate', '224k')
                config_profile.set('FFMPEG AC3 - SETTINGS', 'dolbyprologicii', '')
                config_profile.set('FFMPEG AC3 - SETTINGS', 'ffmpeg_volume', '0.0')
                config_profile.set('FFMPEG AC3 - SETTINGS', 'ac3_channel', 'Original')
                config_profile.set('FFMPEG AC3 - SETTINGS', 'samplerate', 'Original')
                config_profile.set('FFMPEG AC3 - SETTINGS', 'tempo', 'Original')
            if encoder.get() == 'AAC':
                config_profile.set('FFMPEG AAC - SETTINGS', 'dolbyprologicii', '')
                config_profile.set('FFMPEG AAC - SETTINGS', 'ffmpeg_volume', '0.0')
                config_profile.set('FFMPEG AAC - SETTINGS', 'aac_bitrate', '192')
                config_profile.set('FFMPEG AAC - SETTINGS', 'aac_vbr_quality', '2')
                config_profile.set('FFMPEG AAC - SETTINGS', 'aac_vbr_toggle', '-c:a')
                config_profile.set('FFMPEG AAC - SETTINGS', 'aac_channel', 'Original')
                config_profile.set('FFMPEG AAC - SETTINGS', 'samplerate', 'Original')
                config_profile.set('FFMPEG AAC - SETTINGS', 'tempo', 'Original')
            if encoder.get() == 'DTS':
                config_profile.set('FFMPEG DTS - SETTINGS', 'dts_bitrate', '448')
                config_profile.set('FFMPEG DTS - SETTINGS', 'dolbyprologicii', '')
                config_profile.set('FFMPEG DTS - SETTINGS', 'ffmpeg_volume', '0.0')
                config_profile.set('FFMPEG DTS - SETTINGS', 'dts_channel', '2 (Stereo)')
                config_profile.set('FFMPEG DTS - SETTINGS', 'samplerate', 'Original')
                config_profile.set('FFMPEG DTS - SETTINGS', 'tempo', 'Original')
            if encoder.get() == 'E-AC3':
                config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_bitrate', '448k')
                config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_channel', 'Original')
                config_profile.set('FFMPEG E-AC3 - SETTINGS', 'e-ac3_volume', '0.0')
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
                config_profile.set('FFMPEG Opus - SETTINGS', 'ffmpeg_volume', '0.0')
                config_profile.set('FFMPEG Opus - SETTINGS', 'tempo', 'Original')
                config_profile.set('FFMPEG Opus - SETTINGS', 'mapping_family', 'Mapping -1: Auto')
            if encoder.get() == 'FDK-AAC':
                config_profile.set('FDK-AAC - SETTINGS', 'fdk_aac_bitrate', 'CBR: 192k')
                config_profile.set('FDK-AAC - SETTINGS', 'acodec_channel', 'Original')
                config_profile.set('FDK-AAC - SETTINGS', 'dolbyprologicii', '')
                config_profile.set('FDK-AAC - SETTINGS', 'ffmpeg_volume', '0.0')
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
                config_profile.set('FFMPEG MP3 - SETTINGS', 'ffmpeg_volume', '0.0')
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
                config_profile.set('FFMPEG FLAC - SETTINGS', 'acodec_bitrate', 'Level 5 - Default Compression/Speed')
                config_profile.set('FFMPEG FLAC - SETTINGS', 'acodec_channel', 'Original')
                config_profile.set('FFMPEG FLAC - SETTINGS', 'dolbyprologicii', '')
                config_profile.set('FFMPEG FLAC - SETTINGS', 'volume', '0.0')
                config_profile.set('FFMPEG FLAC - SETTINGS', 'samplerate', 'Original')
                config_profile.set('FFMPEG FLAC - SETTINGS', 'tempo', 'Original')
                config_profile.set('FFMPEG FLAC - SETTINGS', 'flac_lpc_type', 'Default')
                config_profile.set('FFMPEG FLAC - SETTINGS', 'flac_coefficient', '15')
                config_profile.set('FFMPEG FLAC - SETTINGS', 'flac_lpc_passes', 'Default')
            if encoder.get() == 'ALAC':
                config_profile.set('FFMPEG ALAC - SETTINGS', 'acodec_channel', 'Original')
                config_profile.set('FFMPEG ALAC - SETTINGS', 'dolbyprologicii', '')
                config_profile.set('FFMPEG ALAC - SETTINGS', 'volume', '0.0')
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
                   '.........................%Language/String%\\n\\n" ' + \
                   str(pathlib.Path(VideoInputQuoted.replace('&', '^&'))) + '"'
        run = subprocess.Popen('cmd /c ' + commands, creationflags=subprocess.CREATE_NO_WINDOW, universal_newlines=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE, shell=True, encoding="utf-8")
        clean_communicate_string = str(run.communicate()).replace(r'\n', '\n').replace('{', '').replace('}', '') \
            .replace('(', '').replace(')', '').replace(',', '').replace("'", '')
        try:
            global text_area
            text_area.delete("1.0", END)
            text_area.insert(END, clean_communicate_string)
        except (Exception,):
            stream_window = Toplevel(audio_window)
            stream_window.title("Audio Streams")
            stream_window.configure(background="#434547")
            Label(stream_window, text="---------- Audio Streams ----------", font=("Times New Roman", 16),
                  background='#434547', foreground="white").grid(column=0, row=0)
            text_area = scrolledtextwidget.ScrolledText(stream_window, width=50, height=25, tabs=10, spacing2=3,
                                                        spacing1=2,
                                                        spacing3=3)
            text_area.grid(column=0, pady=10, padx=10)
            text_area.insert(INSERT, clean_communicate_string)
            text_area.configure(font=("Helvetica", 12))
            text_area.configure(state=DISABLED)
            stream_window.grid_columnconfigure(0, weight=1)

    # ---------------------------------------------------------------------------------------------------- Show Streams

    # FFMPEG Volume Spinbox Menu + HoverToolTip -----------------------------------------------------------------------
    def volume_right_click_options():
        def popup_auto_e_b_menu(e):  # Function for mouse button 3 (right click) to pop up menu
            reset_volume_menu.tk_popup(e.x_root, e.y_root)  # This gets the posision of 'e'

        reset_volume_menu = Menu(ffmpeg_volume_spinbox, tearoff=False)  # Right click menu
        reset_volume_menu.add_command(label='Reset to 0', command=lambda: ffmpeg_volume.set(0.0))
        reset_volume_menu.add_separator()
        reset_volume_menu.add_command(label='Set to 5', command=lambda: ffmpeg_volume.set(5.0))
        reset_volume_menu.add_command(label='Set to 10', command=lambda: ffmpeg_volume.set(10.0))
        reset_volume_menu.add_command(label='Set to 15', command=lambda: ffmpeg_volume.set(15.0))
        reset_volume_menu.add_command(label='Set to 20', command=lambda: ffmpeg_volume.set(20.0))
        reset_volume_menu.add_separator()
        reset_volume_menu.add_command(label='Set to -5', command=lambda: ffmpeg_volume.set(-5.0))
        reset_volume_menu.add_command(label='Set to -10', command=lambda: ffmpeg_volume.set(-10.0))
        reset_volume_menu.add_command(label='Set to -15', command=lambda: ffmpeg_volume.set(-15.0))
        reset_volume_menu.add_command(label='Set to -20', command=lambda: ffmpeg_volume.set(-20.0))
        ffmpeg_volume_spinbox.bind('<Button-3>', popup_auto_e_b_menu)  # Uses mouse button 3 (right click) to open
        Hovertip(ffmpeg_volume_spinbox, 'Right click for more options', hover_delay=600)  # Hover tip tool-tip

    # ----------------------------------------------------------------------- FFMPEG Volume Spinbox Menu + HoverToolTip

    # Set Config Profile Parser ---------------------------------------------------------------------------------------
    config_profile = ConfigParser()
    config_profile.read(config_profile_ini)
    # --------------------------------------------------------------------------------------- Set Config Profile Parser

    # AC3 Window ------------------------------------------------------------------------------------------------------
    global audio_window
    if encoder.get() == "AC3":
        try:
            audio_window.deiconify()
        except (Exception,):
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
            audio_window.protocol('WM_DELETE_WINDOW', audio_window_exit_function)

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
                global cmd_line_window, show_cmd_scrolled
                audio_filter_function()
                example_cmd_output = ' '.join(str(acodec_stream_choices[acodec_stream.get()] +
                                                  encoder_dropdownmenu_choices[encoder.get()] +
                                                  acodec_bitrate_choices[acodec_bitrate.get()] +
                                                  acodec_channel_choices[acodec_channel.get()] +
                                                  acodec_samplerate_choices[acodec_samplerate.get()] +
                                                  audio_filter_setting + ac3_custom_cmd_input).split())
                try:
                    show_cmd_scrolled.configure(state=NORMAL)
                    show_cmd_scrolled.delete(1.0, END)
                    show_cmd_scrolled.insert(END, example_cmd_output)
                    show_cmd_scrolled.see(END)
                    show_cmd_scrolled.configure(state=DISABLED)
                    cmd_line_window.deiconify()
                except (AttributeError, NameError):
                    cmd_line_window = Toplevel()
                    cmd_line_window.title('Command Line')
                    cmd_line_window.configure(background="#434547")

                    show_cmd_scrolled = scrolledtextwidget.ScrolledText(cmd_line_window, width=70, height=10, tabs=10,
                                                                        spacing2=3, spacing1=2, spacing3=3)
                    show_cmd_scrolled.grid(row=0, column=0, pady=(5, 4), padx=5, sticky=E + W)
                    show_cmd_scrolled.configure(state=NORMAL, bg='black', fg='#CFD2D1', bd=8)
                    show_cmd_scrolled.insert(END, example_cmd_output)
                    show_cmd_scrolled.see(END)
                    show_cmd_scrolled.configure(state=DISABLED)
                    cmd_line_window.resizable(False, False)  # Disables resizable functions of window

                    def copy_to_clipboard():  # Function to allow copying full command to clipboard via pyperclip module
                        pyperclip.copy(show_cmd_scrolled.get(1.0, END))

                    copy_text = HoverButton(cmd_line_window, text='Copy to clipboard', command=copy_to_clipboard,
                                            foreground='white', background='#23272A', borderwidth='3',
                                            activebackground='grey')
                    copy_text.grid(row=1, column=0, columnspan=1, padx=(20, 20), pady=(4, 5), sticky=E)

                    def hide_instead():
                        cmd_line_window.withdraw()

                    cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

            # ------------------------------------------------------------------------------------------- Views Command

            # Buttons -------------------------------------------------------------------------------------------------
            apply_button = HoverButton(audio_window, text="Apply", foreground="white", background="#23272A",
                                       command=lambda: [set_encode_manual(), gotosavefile()], activebackground='grey')
            apply_button.grid(row=8, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)

            show_cmd = HoverButton(audio_window, text="View Command", foreground="white", background="#23272A",
                                   command=view_command, activebackground='grey')
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
            # ------------------------------------------------------------------------------------------- Audio Channel

            # Dolby Pro Logic II --------------------------------------------------------------------------------------
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

            # Audio Volume Selection ----------------------------------------------------------------------------------
            ffmpeg_volume = StringVar()
            ffmpeg_volume_label = Label(audio_window, text="Volume :", background="#434547", foreground="white")
            ffmpeg_volume_label.grid(row=2, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            ffmpeg_volume_spinbox = Spinbox(audio_window, from_=-20, to=20, increment=0.1, justify=CENTER, wrap=True,
                                            textvariable=ffmpeg_volume, state='readonly')
            ffmpeg_volume_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                            buttonbackground="black", width=15, readonlybackground="#23272A")
            ffmpeg_volume_spinbox.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            ffmpeg_volume.set(config_profile['FFMPEG AC3 - SETTINGS']['ffmpeg_volume'])
            volume_right_click_options()  # Run function for right click options for volume spinbox
            # -------------------------------------------------------------------------------------------------- Volume

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
                if ac3_custom_cmd.get().strip() == "":
                    ac3_custom_cmd_input = ""
                else:
                    cstmcmd = ac3_custom_cmd.get().strip()
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
        audio_window.protocol('WM_DELETE_WINDOW', audio_window_exit_function)

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
            global cmd_line_window, show_cmd_scrolled
            audio_filter_function()
            if aac_vbr_toggle.get() == "-c:a ":
                example_cmd_output = ' '.join(str(acodec_stream_choices[acodec_stream.get()] +
                                                  encoder_dropdownmenu_choices[encoder.get()] + "-b:a " +
                                                  aac_bitrate_spinbox.get() + "k " +
                                                  acodec_channel_choices[acodec_channel.get()] +
                                                  acodec_samplerate_choices[acodec_samplerate.get()] +
                                                  audio_filter_setting + aac_custom_cmd_input +
                                                  aac_title_input).split())
            elif aac_vbr_toggle.get() == "-q:a ":
                example_cmd_output = ' '.join(str(acodec_stream_choices[acodec_stream.get()] +
                                                  encoder_dropdownmenu_choices[encoder.get()] + \
                                                  "-q:a " + aac_quality_spinbox.get() + " " +
                                                  acodec_channel_choices[acodec_channel.get()] +
                                                  acodec_samplerate_choices[acodec_samplerate.get()] +
                                                  audio_filter_setting + aac_custom_cmd_input +
                                                  aac_title_input).split())
            try:
                show_cmd_scrolled.configure(state=NORMAL)
                show_cmd_scrolled.delete(1.0, END)
                show_cmd_scrolled.insert(END, example_cmd_output)
                show_cmd_scrolled.see(END)
                show_cmd_scrolled.configure(state=DISABLED)
                cmd_line_window.deiconify()
            except (AttributeError, NameError):
                cmd_line_window = Toplevel()
                cmd_line_window.title('Command Line')
                cmd_line_window.configure(background="#434547")

                show_cmd_scrolled = scrolledtextwidget.ScrolledText(cmd_line_window, width=70, height=10, tabs=10,
                                                                    spacing2=3, spacing1=2, spacing3=3)
                show_cmd_scrolled.grid(row=0, column=0, pady=(5, 4), padx=5, sticky=E + W)
                show_cmd_scrolled.configure(state=NORMAL, bg='black', fg='#CFD2D1', bd=8)
                show_cmd_scrolled.insert(END, example_cmd_output)
                show_cmd_scrolled.see(END)
                show_cmd_scrolled.configure(state=DISABLED)
                cmd_line_window.resizable(False, False)  # Disables resizable functions of window

                def copy_to_clipboard():  # Function to allow copying full command to clipboard via pyperclip module
                    pyperclip.copy(show_cmd_scrolled.get(1.0, END))

                copy_text = HoverButton(cmd_line_window, text='Copy to clipboard', command=copy_to_clipboard,
                                        foreground='white', background='#23272A', borderwidth='3',
                                        activebackground='grey')
                copy_text.grid(row=1, column=0, columnspan=1, padx=(20, 20), pady=(4, 5), sticky=E)

                def hide_instead():
                    cmd_line_window.withdraw()

                cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

        # ----------------------------------------------------------------------------------------------- Views Command

        # Buttons -----------------------------------------------------------------------------------------------------
        apply_button = HoverButton(audio_window, text="Apply", foreground="white", background="#23272A",
                                   command=lambda: [set_encode_manual(), gotosavefile()], activebackground='grey')
        apply_button.grid(row=10, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)

        show_cmd = HoverButton(audio_window, text="View Command", foreground="white", background="#23272A",
                               command=view_command, activebackground='grey')
        show_cmd.grid(row=10, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        show_cmd.bind("<Enter>", show_cmd_hover)
        show_cmd.bind("<Leave>", show_cmd_hover_leave)

        # ----------------------------------------------------------------------------------------------------- Buttons

        # Entry Box for Custom Command Line ---------------------------------------------------------------------------
        def aac_cmd(*args):
            global aac_custom_cmd_input
            if aac_custom_cmd.get().strip() == '':
                aac_custom_cmd_input = ''
            else:
                cstmcmd = aac_custom_cmd.get().strip()
                aac_custom_cmd_input = cstmcmd + ' '

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
            if aac_title.get().strip() == '':
                aac_title_input = ''
            else:
                title_cmd = aac_title.get().strip()
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

        # Audio Volume Selection --------------------------------------------------------------------------------------
        ffmpeg_volume = StringVar()
        ffmpeg_volume_label = Label(audio_window, text="Volume :", background="#434547", foreground="white")
        ffmpeg_volume_label.grid(row=0, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        ffmpeg_volume_spinbox = Spinbox(audio_window, from_=-20, to=20, increment=0.1, justify=CENTER, wrap=True,
                                        textvariable=ffmpeg_volume, state='readonly')
        ffmpeg_volume_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                        buttonbackground="black", width=15, readonlybackground="#23272A")
        ffmpeg_volume_spinbox.grid(row=1, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        ffmpeg_volume.set(config_profile['FFMPEG AAC - SETTINGS']['ffmpeg_volume'])
        volume_right_click_options()
        # ------------------------------------------------------------------------------------------------------ Volume

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
        audio_window.protocol('WM_DELETE_WINDOW', audio_window_exit_function)

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
                ffmpeg_volume_spinbox.config(state=NORMAL)
                ffmpeg_volume.set(config_profile['FFMPEG DTS - SETTINGS']['ffmpeg_volume'])
                acodec_samplerate_menu.config(state=NORMAL)
                acodec_samplerate.set(config_profile['FFMPEG DTS - SETTINGS']['samplerate'])
                dts_acodec_bitrate_spinbox.config(state=NORMAL)
                dts_bitrate_spinbox.set(int(config_profile['FFMPEG DTS - SETTINGS']['dts_bitrate']))
                acodec_atempo_menu.config(state=NORMAL)
                acodec_atempo.set(config_profile['FFMPEG DTS - SETTINGS']['tempo'])
            else:
                achannel_menu.config(state=DISABLED)
                ffmpeg_volume_spinbox.config(state=DISABLED)
                acodec_samplerate_menu.config(state=DISABLED)
                dts_acodec_bitrate_spinbox.config(state=DISABLED)
                dolby_pro_logic_ii_checkbox.config(state=DISABLED)
                acodec_atempo_menu.config(state=DISABLED)

        # Views Command -----------------------------------------------------------------------------------------------
        def view_command():
            global cmd_line_window, show_cmd_scrolled
            audio_filter_function()
            if dts_settings.get() == 'DTS Encoder':
                example_cmd_output = ' '.join(str(acodec_stream_choices[acodec_stream.get()] +
                                                  dts_settings_choices[dts_settings.get()] + "-b:a " +
                                                  dts_bitrate_spinbox.get() + "k " +
                                                  acodec_channel_choices[acodec_channel.get()] +
                                                  acodec_samplerate_choices[acodec_samplerate.get()] +
                                                  audio_filter_setting + dts_custom_cmd_input).split())
            else:
                example_cmd_output = ' '.join(str(acodec_stream_choices[acodec_stream.get()] +
                                                  dts_settings_choices[dts_settings.get()] +
                                                  dts_custom_cmd_input).split())
            try:
                show_cmd_scrolled.configure(state=NORMAL)
                show_cmd_scrolled.delete(1.0, END)
                show_cmd_scrolled.insert(END, example_cmd_output)
                show_cmd_scrolled.see(END)
                show_cmd_scrolled.configure(state=DISABLED)
                cmd_line_window.deiconify()
            except (AttributeError, NameError):
                cmd_line_window = Toplevel()
                cmd_line_window.title('Command Line')
                cmd_line_window.configure(background="#434547")

                show_cmd_scrolled = scrolledtextwidget.ScrolledText(cmd_line_window, width=70, height=10, tabs=10,
                                                                    spacing2=3, spacing1=2, spacing3=3)
                show_cmd_scrolled.grid(row=0, column=0, pady=(5, 4), padx=5, sticky=E + W)
                show_cmd_scrolled.configure(state=NORMAL, bg='black', fg='#CFD2D1', bd=8)
                show_cmd_scrolled.insert(END, example_cmd_output)
                show_cmd_scrolled.see(END)
                show_cmd_scrolled.configure(state=DISABLED)
                cmd_line_window.resizable(False, False)  # Disables resizable functions of window

                def copy_to_clipboard():  # Function to allow copying full command to clipboard via pyperclip module
                    pyperclip.copy(show_cmd_scrolled.get(1.0, END))

                copy_text = HoverButton(cmd_line_window, text='Copy to clipboard', command=copy_to_clipboard,
                                        foreground='white', background='#23272A', borderwidth='3',
                                        activebackground='grey')
                copy_text.grid(row=1, column=0, columnspan=1, padx=(20, 20), pady=(4, 5), sticky=E)

                def hide_instead():
                    cmd_line_window.withdraw()

                cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

        # ----------------------------------------------------------------------------------------------- Views Command

        # Buttons -----------------------------------------------------------------------------------------------------
        apply_button = HoverButton(audio_window, text="Apply", foreground="white", background="#23272A",
                                   command=lambda: [set_encode_manual(), gotosavefile()], activebackground='grey')
        apply_button.grid(row=9, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)

        show_cmd = HoverButton(audio_window, text="View Command", foreground="white", background="#23272A",
                               command=view_command, activebackground='grey')
        show_cmd.grid(row=9, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        show_cmd.bind("<Enter>", show_cmd_hover)
        show_cmd.bind("<Leave>", show_cmd_hover_leave)

        # ----------------------------------------------------------------------------------------------------- Buttons

        # Entry Box for Custom Command Line ---------------------------------------------------------------------------
        def dts_cmd(*args):
            global dts_custom_cmd_input
            if dts_custom_cmd.get().strip() == "":
                dts_custom_cmd_input = ""
            else:
                cstmcmd = dts_custom_cmd.get().strip()
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
                                  '2 (Stereo)': "-ac 2 "}
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

        # Audio Volume Selection --------------------------------------------------------------------------------------
        ffmpeg_volume = StringVar()
        ffmpeg_volume_label = Label(audio_window, text="Volume :", background="#434547", foreground="white")
        ffmpeg_volume_label.grid(row=2, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        ffmpeg_volume_spinbox = Spinbox(audio_window, from_=-20, to=20, increment=0.1, justify=CENTER, wrap=True,
                                        textvariable=ffmpeg_volume, state='readonly')
        ffmpeg_volume_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                        buttonbackground="black", width=15, readonlybackground="#23272A")
        ffmpeg_volume_spinbox.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        ffmpeg_volume.set(config_profile['FFMPEG DTS - SETTINGS']['ffmpeg_volume'])
        volume_right_click_options()
        # ------------------------------------------------------------------------------------------------------ Volume

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
        audio_window.protocol('WM_DELETE_WINDOW', audio_window_exit_function)

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
            global show_cmd_scrolled, cmd_line_window
            audio_filter_function()
            example_cmd_output = ' '.join(str(acodec_stream_choices[acodec_stream.get()] +
                                              encoder_dropdownmenu_choices[encoder.get()] +
                                              acodec_bitrate_choices[acodec_bitrate.get()] +
                                              acodec_channel_choices[acodec_channel.get()] +
                                              acodec_vbr_choices[acodec_vbr.get()] +
                                              acodec_application_choices[acodec_application.get()] +
                                              opus_mapping_family_choices[opus_mapping_family.get()] +
                                              "-packet_loss " + packet_loss.get() + " -frame_duration " +
                                              frame_duration.get() + " " +
                                              acodec_samplerate_choices[acodec_samplerate.get()] +
                                              audio_filter_setting + opus_custom_cmd_input).split())
            try:
                show_cmd_scrolled.configure(state=NORMAL)
                show_cmd_scrolled.delete(1.0, END)
                show_cmd_scrolled.insert(END, example_cmd_output)
                show_cmd_scrolled.see(END)
                show_cmd_scrolled.configure(state=DISABLED)
                cmd_line_window.deiconify()
            except (AttributeError, NameError):
                cmd_line_window = Toplevel()
                cmd_line_window.title('Command Line')
                cmd_line_window.configure(background="#434547")

                show_cmd_scrolled = scrolledtextwidget.ScrolledText(cmd_line_window, width=70, height=10, tabs=10,
                                                                    spacing2=3, spacing1=2, spacing3=3)
                show_cmd_scrolled.grid(row=0, column=0, pady=(5, 4), padx=5, sticky=E + W)
                show_cmd_scrolled.configure(state=NORMAL, bg='black', fg='#CFD2D1', bd=8)
                show_cmd_scrolled.insert(END, example_cmd_output)
                show_cmd_scrolled.see(END)
                show_cmd_scrolled.configure(state=DISABLED)
                cmd_line_window.resizable(False, False)  # Disables resizable functions of window

                def copy_to_clipboard():  # Function to allow copying full command to clipboard via pyperclip module
                    pyperclip.copy(show_cmd_scrolled.get(1.0, END))

                copy_text = HoverButton(cmd_line_window, text='Copy to clipboard', command=copy_to_clipboard,
                                        foreground='white', background='#23272A', borderwidth='3',
                                        activebackground='grey')
                copy_text.grid(row=1, column=0, columnspan=1, padx=(20, 20), pady=(4, 5), sticky=E)

                def hide_instead():
                    cmd_line_window.withdraw()

                cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

        # ----------------------------------------------------------------------------------------------- Views Command

        # Buttons -----------------------------------------------------------------------------------------------------
        apply_button = HoverButton(audio_window, text="Apply", foreground="white", background="#23272A",
                                   command=lambda: [set_encode_manual(), gotosavefile()], activebackground='grey')
        apply_button.grid(row=13, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)

        show_cmd = HoverButton(audio_window, text="View Command", foreground="white", background="#23272A",
                               command=view_command, activebackground='grey')
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
            if opus_custom_cmd.get().strip() == "":
                opus_custom_cmd_input = ""
            else:
                cstmcmd = opus_custom_cmd.get().strip()
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
        acodec_channel_choices = {'1 (Mono)': "-ac 1 ",
                                  '2 (Stereo)': "-ac 2 ",
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

        # Opus Mapping Family -----------------------------------------------------------------------------------------
        opus_mapping_family = StringVar(audio_window)
        opus_mapping_family_choices = {'Mapping -1: Auto': "",
                                       'Mapping 0: Mono/Stereo': "-mapping_family 0 ",
                                       'Mapping 1: Multi-Channel': "-mapping_family 1 "}
        opus_mapping_family.set(config_profile['FFMPEG Opus - SETTINGS']['mapping_family'])  # set the default option
        opus_mapping_family_menu_label = Label(audio_window, text="Mapping Family :", background="#434547",
                                               foreground="white")
        opus_mapping_family_menu_label.grid(row=4, column=1, columnspan=1, padx=10, pady=3, sticky=W + E)
        opus_mapping_family_menu = OptionMenu(audio_window, opus_mapping_family, *opus_mapping_family_choices.keys())
        opus_mapping_family_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=10,
                                        anchor=W)
        opus_mapping_family_menu.grid(row=5, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        opus_mapping_family_menu["menu"].configure(activebackground="dim grey")
        opus_mapping_family_menu.bind("<Enter>", opus_mapping_family_menu_hover)
        opus_mapping_family_menu.bind("<Leave>", opus_mapping_family_menu_hover_leave)
        # ----------------------------------------------------------------------------------------- Opus Mapping Family

        # Audio Volume Selection --------------------------------------------------------------------------------------
        ffmpeg_volume = StringVar()
        ffmpeg_volume_label = Label(audio_window, text="Volume :", background="#434547", foreground="white")
        ffmpeg_volume_label.grid(row=2, column=0, columnspan=1, padx=10, pady=(3, 10), sticky=N + S + E + W)
        ffmpeg_volume_spinbox = Spinbox(audio_window, from_=-20, to=20, increment=0.1, justify=CENTER, wrap=True,
                                        textvariable=ffmpeg_volume, state='readonly')
        ffmpeg_volume_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                        buttonbackground="black", width=15, readonlybackground="#23272A")
        ffmpeg_volume_spinbox.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        ffmpeg_volume.set(config_profile['FFMPEG Opus - SETTINGS']['ffmpeg_volume'])
        volume_right_click_options()
        # ------------------------------------------------------------------------------------------------------ Volume

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
        audio_window.protocol('WM_DELETE_WINDOW', audio_window_exit_function)

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
            global show_cmd_scrolled, cmd_line_window
            audio_filter_function()
            example_cmd_output = ' '.join(str(acodec_stream_choices[acodec_stream.get()] +
                                              encoder_dropdownmenu_choices[encoder.get()] +
                                              acodec_bitrate_choices[acodec_bitrate.get()] +
                                              acodec_channel_choices[acodec_channel.get()] + mp3_abr.get() +
                                              acodec_samplerate_choices[acodec_samplerate.get()] +
                                              audio_filter_setting + mp3_custom_cmd_input).split())
            try:
                show_cmd_scrolled.configure(state=NORMAL)
                show_cmd_scrolled.delete(1.0, END)
                show_cmd_scrolled.insert(END, example_cmd_output)
                show_cmd_scrolled.see(END)
                show_cmd_scrolled.configure(state=DISABLED)
                cmd_line_window.deiconify()
            except (AttributeError, NameError):
                cmd_line_window = Toplevel()
                cmd_line_window.title('Command Line')
                cmd_line_window.configure(background="#434547")

                show_cmd_scrolled = scrolledtextwidget.ScrolledText(cmd_line_window, width=70, height=10, tabs=10,
                                                                    spacing2=3, spacing1=2, spacing3=3)
                show_cmd_scrolled.grid(row=0, column=0, pady=(5, 4), padx=5, sticky=E + W)
                show_cmd_scrolled.configure(state=NORMAL, bg='black', fg='#CFD2D1', bd=8)
                show_cmd_scrolled.insert(END, example_cmd_output)
                show_cmd_scrolled.see(END)
                show_cmd_scrolled.configure(state=DISABLED)
                cmd_line_window.resizable(False, False)  # Disables resizable functions of window

                def copy_to_clipboard():  # Function to allow copying full command to clipboard via pyperclip module
                    pyperclip.copy(show_cmd_scrolled.get(1.0, END))

                copy_text = HoverButton(cmd_line_window, text='Copy to clipboard', command=copy_to_clipboard,
                                        foreground='white', background='#23272A', borderwidth='3',
                                        activebackground='grey')
                copy_text.grid(row=1, column=0, columnspan=1, padx=(20, 20), pady=(4, 5), sticky=E)

                def hide_instead():
                    cmd_line_window.withdraw()

                cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

        # ----------------------------------------------------------------------------------------------- Views Command

        # Buttons -----------------------------------------------------------------------------------------------------
        apply_button = HoverButton(audio_window, text="Apply", foreground="white", background="#23272A",
                                   command=lambda: [set_encode_manual(), gotosavefile()], activebackground='grey')
        apply_button.grid(row=7, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)

        show_cmd = HoverButton(audio_window, text="View Command", foreground="white", background="#23272A",
                               command=view_command, activebackground='grey')
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
            if mp3_custom_cmd.get().strip() == "":
                mp3_custom_cmd_input = ""
            else:
                cstmcmd = mp3_custom_cmd.get().strip()
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

        # Audio Volume Selection --------------------------------------------------------------------------------------
        ffmpeg_volume = StringVar()
        ffmpeg_volume_label = Label(audio_window, text="Volume :", background="#434547", foreground="white")
        ffmpeg_volume_label.grid(row=2, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        ffmpeg_volume_spinbox = Spinbox(audio_window, from_=-20, to=20, increment=0.1, justify=CENTER, wrap=True,
                                        textvariable=ffmpeg_volume, state='readonly')
        ffmpeg_volume_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                        buttonbackground="black", width=15, readonlybackground="#23272A")
        ffmpeg_volume_spinbox.grid(row=3, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        ffmpeg_volume.set(config_profile['FFMPEG MP3 - SETTINGS']['ffmpeg_volume'])
        ffmpeg_volume.trace('w', audio_filter_function)
        volume_right_click_options()
        # ------------------------------------------------------------------------------------------------------ Volume

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
        audio_window.protocol('WM_DELETE_WINDOW', audio_window_exit_function)

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
            global show_cmd_scrolled, cmd_line_window
            audio_filter_function()
            example_cmd_output = ' '.join(str(acodec_stream_choices[acodec_stream.get()] +
                                              encoder_dropdownmenu_choices[encoder.get()] + "-b:a " +
                                              eac3_spinbox.get() + " " + acodec_channel_choices[acodec_channel.get()] +
                                              acodec_samplerate_choices[acodec_samplerate.get()] +
                                              audio_filter_setting + eac3_custom_cmd_input +
                                              per_frame_metadata_choices[per_frame_metadata.get()] +
                                              "-mixing_level " + eac3_mixing_level.get() + " " +
                                              room_type_choices[room_type.get()] + "-copyright " +
                                              copyright_bit.get() + " " + "-dialnorm " + dialogue_level.get() + " " +
                                              dolby_surround_mode_choices[dolby_surround_mode.get()] +
                                              "-original " + original_bit_stream.get() + " " +
                                              downmix_mode_choices[downmix_mode.get()] + "-ltrt_cmixlev " +
                                              lt_rt_center_mix.get() + " " + "-ltrt_surmixlev " +
                                              lt_rt_surround_mix.get() + " " + "-loro_cmixlev " +
                                              lo_ro_center_mix.get() + " " + "\n \n" + "-loro_surmixlev " +
                                              lo_ro_surround_mix.get() + " " +
                                              dolby_surround_ex_mode_choices[dolby_surround_ex_mode.get()] +
                                              dolby_headphone_mode_choices[dolby_headphone_mode.get()] +
                                              a_d_converter_type_choices[a_d_converter_type.get()] +
                                              stereo_rematrixing_choices[stereo_rematrixing.get()] +
                                              "-channel_coupling " + channel_coupling.get() + " " +
                                              "-cpl_start_band " + cpl_start_band.get() + " ").split())
            try:
                show_cmd_scrolled.configure(state=NORMAL)
                show_cmd_scrolled.delete(1.0, END)
                show_cmd_scrolled.insert(END, example_cmd_output)
                show_cmd_scrolled.see(END)
                show_cmd_scrolled.configure(state=DISABLED)
                cmd_line_window.deiconify()
            except (AttributeError, NameError):
                cmd_line_window = Toplevel()
                cmd_line_window.title('Command Line')
                cmd_line_window.configure(background="#434547")

                show_cmd_scrolled = scrolledtextwidget.ScrolledText(cmd_line_window, width=70, height=10, tabs=10,
                                                                    spacing2=3, spacing1=2, spacing3=3)
                show_cmd_scrolled.grid(row=0, column=0, pady=(5, 4), padx=5, sticky=E + W)
                show_cmd_scrolled.configure(state=NORMAL, bg='black', fg='#CFD2D1', bd=8)
                show_cmd_scrolled.insert(END, example_cmd_output)
                show_cmd_scrolled.see(END)
                show_cmd_scrolled.configure(state=DISABLED)
                cmd_line_window.resizable(False, False)  # Disables resizable functions of window

                def copy_to_clipboard():  # Function to allow copying full command to clipboard via pyperclip module
                    pyperclip.copy(show_cmd_scrolled.get(1.0, END))

                copy_text = HoverButton(cmd_line_window, text='Copy to clipboard', command=copy_to_clipboard,
                                        foreground='white', background='#23272A', borderwidth='3',
                                        activebackground='grey')
                copy_text.grid(row=1, column=0, columnspan=1, padx=(20, 20), pady=(4, 5), sticky=E)

                def hide_instead():
                    cmd_line_window.withdraw()

                cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

        # ----------------------------------------------------------------------------------------------- Views Command

        # Buttons -----------------------------------------------------------------------------------------------------
        apply_button = HoverButton(audio_window, text="Apply", foreground="white", background="#23272A",
                                   command=lambda: [set_encode_manual(), gotosavefile()], activebackground='grey')
        apply_button.grid(row=22, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)

        show_cmd = HoverButton(audio_window, text="View Command", foreground="white", background="#23272A",
                               command=view_command, activebackground='grey')
        show_cmd.grid(row=22, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        show_cmd.bind("<Enter>", show_cmd_hover)
        show_cmd.bind("<Leave>", show_cmd_hover_leave)

        # ----------------------------------------------------------------------------------------------------- Buttons

        # Entry Box for Custom Command Line ---------------------------------------------------------------------------
        def eac3_cmd(*args):
            global eac3_custom_cmd_input
            if eac3_custom_cmd.get().strip() == "":
                eac3_custom_cmd_input = ""
            else:
                cstmcmd = eac3_custom_cmd.get().strip()
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

        # Audio Volume Selection --------------------------------------------------------------------------------------
        ffmpeg_volume = StringVar()
        ffmpeg_volume_label = Label(audio_window, text="Volume :", background="#434547", foreground="white")
        ffmpeg_volume_label.grid(row=2, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        ffmpeg_volume_spinbox = Spinbox(audio_window, from_=-20, to=20, increment=0.1, justify=CENTER, wrap=True,
                                        textvariable=ffmpeg_volume, state='readonly')
        ffmpeg_volume_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                        buttonbackground="black", width=15, readonlybackground="#23272A")
        ffmpeg_volume_spinbox.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        ffmpeg_volume.set(config_profile['FFMPEG E-AC3 - SETTINGS']['e-ac3_volume'])
        volume_right_click_options()
        # ------------------------------------------------------------------------------------------------------ Volume

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
        audio_window.protocol('WM_DELETE_WINDOW', audio_window_exit_function)

        my_menu_bar = Menu(audio_window, tearoff=0)
        audio_window.config(menu=my_menu_bar)
        file_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
        my_menu_bar.add_cascade(label='Track Tools', menu=file_menu)
        file_menu.add_command(label='View Audio Tracks', command=show_streams_mediainfo)
        file_menu.add_command(label='Play Selected Audio Track  |  9 and 0 for Volume', command=mpv_gui_audio_window)
        options_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
        my_menu_bar.add_cascade(label='Options', menu=options_menu)
        options_menu.add_command(label='Save Current Settings', command=save_profile)
        options_menu.add_command(label='Reset Settings To Default', command=reset_profile)

        for n in range(3):
            audio_window.grid_columnconfigure(n, weight=1)
        for n in range(11):
            audio_window.grid_rowconfigure(n, weight=1)
        audio_window.grid_rowconfigure(15, weight=1)

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
            global show_cmd_scrolled, cmd_line_window
            audio_filter_function()
            example_cmd_output = ' '.join(str(acodec_stream_choices[acodec_stream.get()] +
                                              acodec_channel_choices[acodec_channel.get()] +
                                              acodec_samplerate_choices[acodec_samplerate.get()] +
                                              audio_filter_setting + "-f caf - | " + "fdkaac.exe" + " " +
                                              acodec_profile_choices[acodec_profile.get()] + afterburnervar.get() +
                                              fdkaac_title_input + fdkaac_custom_cmd_input +
                                              acodec_gapless_mode_choices[acodec_gapless_mode.get()] +
                                              crccheck.get() + moovbox.get() + sbrdelay.get() + headerperiod.get() +
                                              acodec_lowdelay_choices[acodec_lowdelay.get()] +
                                              acodec_sbr_ratio_choices[acodec_sbr_ratio.get()] +
                                              acodec_transport_format_choices[acodec_transport_format.get()] +
                                              acodec_bitrate_choices[acodec_bitrate.get()] + "- -o ").split())
            try:
                show_cmd_scrolled.configure(state=NORMAL)
                show_cmd_scrolled.delete(1.0, END)
                show_cmd_scrolled.insert(END, example_cmd_output)
                show_cmd_scrolled.see(END)
                show_cmd_scrolled.configure(state=DISABLED)
                cmd_line_window.deiconify()
            except (AttributeError, NameError):
                cmd_line_window = Toplevel()
                cmd_line_window.title('Command Line')
                cmd_line_window.configure(background="#434547")

                show_cmd_scrolled = scrolledtextwidget.ScrolledText(cmd_line_window, width=70, height=10, tabs=10,
                                                                    spacing2=3, spacing1=2, spacing3=3)
                show_cmd_scrolled.grid(row=0, column=0, pady=(5, 4), padx=5, sticky=E + W)
                show_cmd_scrolled.configure(state=NORMAL, bg='black', fg='#CFD2D1', bd=8)
                show_cmd_scrolled.insert(END, example_cmd_output)
                show_cmd_scrolled.see(END)
                show_cmd_scrolled.configure(state=DISABLED)
                cmd_line_window.resizable(False, False)  # Disables resizable functions of window

                def copy_to_clipboard():  # Function to allow copying full command to clipboard via pyperclip module
                    pyperclip.copy(show_cmd_scrolled.get(1.0, END))

                copy_text = HoverButton(cmd_line_window, text='Copy to clipboard', command=copy_to_clipboard,
                                        foreground='white', background='#23272A', borderwidth='3',
                                        activebackground='grey')
                copy_text.grid(row=1, column=0, columnspan=1, padx=(20, 20), pady=(4, 5), sticky=E)

                def hide_instead():
                    cmd_line_window.withdraw()

                cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

        # ----------------------------------------------------------------------------------------------- Views Command

        # Buttons -----------------------------------------------------------------------------------------------------
        apply_button = HoverButton(audio_window, text="Apply", foreground="white", background="#23272A",
                                   command=lambda: [set_encode_manual(), gotosavefile()], activebackground='grey')
        apply_button.grid(row=15, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)

        show_cmd = HoverButton(audio_window, text="View Command", foreground="white", background="#23272A",
                               command=view_command, activebackground='grey')
        show_cmd.grid(row=15, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        show_cmd.bind("<Enter>", show_cmd_hover)
        show_cmd.bind("<Leave>", show_cmd_hover_leave)

        help_button = HoverButton(audio_window, text="Help + Information", foreground="white", background="#23272A",
                                  command=gotofdkaachelp, activebackground='grey')
        help_button.grid(row=15, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
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

        # Audio Volume Selection --------------------------------------------------------------------------------------
        ffmpeg_volume = StringVar()
        ffmpeg_volume_label = Label(audio_window, text="Volume :", background="#434547", foreground="white")
        ffmpeg_volume_label.grid(row=2, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        ffmpeg_volume_spinbox = Spinbox(audio_window, from_=-20, to=20, increment=0.1, justify=CENTER, wrap=True,
                                        textvariable=ffmpeg_volume, state='readonly')
        ffmpeg_volume_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                        buttonbackground="black", width=15, readonlybackground="#23272A")
        ffmpeg_volume_spinbox.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        ffmpeg_volume.set(config_profile['FDK-AAC - SETTINGS']['ffmpeg_volume'])
        volume_right_click_options()
        # ------------------------------------------------------------------------------------------------------ Volume

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
            if fdkaac_custom_cmd.get().strip() == "":
                fdkaac_custom_cmd_input = ""
            else:
                cstmcmd = fdkaac_custom_cmd.get().strip()
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
            if fdkaac_title.get().strip() == "":
                fdkaac_title_input = ""
            else:
                title_cmd = fdkaac_title.get().strip()
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
        acodec_gapless_mode_label = Label(audio_window, text="Gapless Mode :", background="#434547", foreground="white")
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
        audio_window.protocol('WM_DELETE_WINDOW', audio_window_exit_function)

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
            global show_cmd_scrolled, cmd_line_window
            audio_filter_function()
            if q_acodec_profile.get() == "True VBR":
                example_cmd_output = ' '.join(str(acodec_stream_choices[acodec_stream.get()] +
                                                  acodec_channel_choices[acodec_channel.get()] +
                                                  acodec_samplerate_choices[acodec_samplerate.get()] +
                                                  audio_filter_setting + "-f wav - | " + qaac + " --ignorelength " +
                                                  q_acodec_profile_choices[q_acodec_profile.get()] +
                                                  q_acodec_quality_amnt.get() + " " + qaac_high_efficiency.get() +
                                                  qaac_nodither.get() + set_qaac_gain +
                                                  q_acodec_quality_choices[q_acodec_quality.get()] +
                                                  qaac_normalize.get() + qaac_nodelay.get() +
                                                  q_gapless_mode_choices[q_gapless_mode.get()] +
                                                  qaac_nooptimize.get() + qaac_threading.get() + qaac_limiter.get() +
                                                  qaac_title_input + qaac_custom_cmd_input).split())
            else:
                example_cmd_output = ' '.join(str(acodec_stream_choices[acodec_stream.get()] +
                                                  acodec_channel_choices[acodec_channel.get()] +
                                                  acodec_samplerate_choices[acodec_samplerate.get()] +
                                                  audio_filter_setting + "-f wav - | " + qaac + " --ignorelength " +
                                                  q_acodec_profile_choices[q_acodec_profile.get()] +
                                                  q_acodec_bitrate.get() + " " + qaac_high_efficiency.get() +
                                                  qaac_nodither.get() + set_qaac_gain +
                                                  q_acodec_quality_choices[q_acodec_quality.get()] +
                                                  qaac_normalize.get() + qaac_nodelay.get() +
                                                  q_gapless_mode_choices[q_gapless_mode.get()] +
                                                  qaac_nooptimize.get() + qaac_threading.get() + qaac_limiter.get() +
                                                  qaac_title_input + qaac_custom_cmd_input).split())
            try:
                show_cmd_scrolled.configure(state=NORMAL)
                show_cmd_scrolled.delete(1.0, END)
                show_cmd_scrolled.insert(END, example_cmd_output)
                show_cmd_scrolled.see(END)
                show_cmd_scrolled.configure(state=DISABLED)
                cmd_line_window.deiconify()
            except (AttributeError, NameError):
                cmd_line_window = Toplevel()
                cmd_line_window.title('Command Line')
                cmd_line_window.configure(background="#434547")

                show_cmd_scrolled = scrolledtextwidget.ScrolledText(cmd_line_window, width=70, height=10, tabs=10,
                                                                    spacing2=3, spacing1=2, spacing3=3)
                show_cmd_scrolled.grid(row=0, column=0, pady=(5, 4), padx=5, sticky=E + W)
                show_cmd_scrolled.configure(state=NORMAL, bg='black', fg='#CFD2D1', bd=8)
                show_cmd_scrolled.insert(END, example_cmd_output)
                show_cmd_scrolled.see(END)
                show_cmd_scrolled.configure(state=DISABLED)
                cmd_line_window.resizable(False, False)  # Disables resizable functions of window

                def copy_to_clipboard():  # Function to allow copying full command to clipboard via pyperclip module
                    pyperclip.copy(show_cmd_scrolled.get(1.0, END))

                copy_text = HoverButton(cmd_line_window, text='Copy to clipboard', command=copy_to_clipboard,
                                        foreground='white', background='#23272A', borderwidth='3',
                                        activebackground='grey')
                copy_text.grid(row=1, column=0, columnspan=1, padx=(20, 20), pady=(4, 5), sticky=E)

                def hide_instead():
                    cmd_line_window.withdraw()

                cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

        # ----------------------------------------------------------------------------------------------- Views Command
        # Buttons -----------------------------------------------------------------------------------------------------
        apply_button = HoverButton(audio_window, text="Apply", foreground="white", background="#23272A",
                                   command=lambda: [set_encode_manual(), gotosavefile()], activebackground='grey')
        apply_button.grid(row=16, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)

        show_cmd = HoverButton(audio_window, text="View Command", foreground="white", background="#23272A",
                               command=view_command, activebackground='grey')
        show_cmd.grid(row=16, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        show_cmd.bind("<Enter>", show_cmd_hover)
        show_cmd.bind("<Leave>", show_cmd_hover_leave)

        help_button = HoverButton(audio_window, text="Help + Information", foreground="white", background="#23272A",
                                  command=gotoqaachelp, activebackground='grey')
        help_button.grid(row=16, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
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
            if qaac_custom_cmd.get().strip() == "":
                qaac_custom_cmd_input = ""
            else:
                cstmcmd = qaac_custom_cmd.get().strip()
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
            if qaac_title.get().strip() == "":
                qaac_title_input = ""
            else:
                title_cmd = qaac_title.get().strip()
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
        qaac_normalize_checkbox.grid(row=10, column=1, columnspan=1, padx=10, pady=(10, 3), sticky=N + S + E + W)
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
        qaac_threading_checkbox.grid(row=10, column=0, columnspan=1, padx=10, pady=(10, 3), sticky=N + S + E + W)
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
        except (Exception,):
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
            audio_window.protocol('WM_DELETE_WINDOW', audio_window_exit_function)

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
                global show_cmd_scrolled, cmd_line_window
                audio_filter_function()
                example_cmd_output = ' '.join(str(acodec_stream_choices[acodec_stream.get()] +
                                                  encoder_dropdownmenu_choices[encoder.get()] +
                                                  acodec_bitrate_choices[acodec_bitrate.get()] +
                                                  acodec_channel_choices[acodec_channel.get()] +
                                                  acodec_samplerate_choices[acodec_samplerate.get()] +
                                                  audio_filter_setting + set_flac_acodec_coefficient +
                                                  acodec_flac_lpc_type_choices[acodec_flac_lpc_type.get()] +
                                                  acodec_flac_lpc_passes_choices[acodec_flac_lpc_passes.get()] +
                                                  flac_custom_cmd_input).split())
                try:
                    show_cmd_scrolled.configure(state=NORMAL)
                    show_cmd_scrolled.delete(1.0, END)
                    show_cmd_scrolled.insert(END, example_cmd_output)
                    show_cmd_scrolled.see(END)
                    show_cmd_scrolled.configure(state=DISABLED)
                    cmd_line_window.deiconify()
                except (AttributeError, NameError):
                    cmd_line_window = Toplevel()
                    cmd_line_window.title('Command Line')
                    cmd_line_window.configure(background="#434547")

                    show_cmd_scrolled = scrolledtextwidget.ScrolledText(cmd_line_window, width=70, height=10, tabs=10,
                                                                        spacing2=3, spacing1=2, spacing3=3)
                    show_cmd_scrolled.grid(row=0, column=0, pady=(5, 4), padx=5, sticky=E + W)
                    show_cmd_scrolled.configure(state=NORMAL, bg='black', fg='#CFD2D1', bd=8)
                    show_cmd_scrolled.insert(END, example_cmd_output)
                    show_cmd_scrolled.see(END)
                    show_cmd_scrolled.configure(state=DISABLED)
                    cmd_line_window.resizable(False, False)  # Disables resizable functions of window

                    def copy_to_clipboard():  # Function to allow copying full command to clipboard via pyperclip module
                        pyperclip.copy(show_cmd_scrolled.get(1.0, END))

                    copy_text = HoverButton(cmd_line_window, text='Copy to clipboard', command=copy_to_clipboard,
                                            foreground='white', background='#23272A', borderwidth='3',
                                            activebackground='grey')
                    copy_text.grid(row=1, column=0, columnspan=1, padx=(20, 20), pady=(4, 5), sticky=E)

                    def hide_instead():
                        cmd_line_window.withdraw()

                    cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

            # ------------------------------------------------------------------------------------------- Views Command

            # Buttons -------------------------------------------------------------------------------------------------
            apply_button = HoverButton(audio_window, text="Apply", foreground="white", background="#23272A",
                                       command=lambda: [set_encode_manual(), gotosavefile()], activebackground='grey')
            apply_button.grid(row=10, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)

            show_cmd = HoverButton(audio_window, text="View Command", foreground="white", background="#23272A",
                                   command=view_command, activebackground='grey')
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
            acodec_bitrate_choices = {'Level 0 - Lowest Compression/Fastest': "-compression_level 0 ",
                                      'Level 1 ......': "-compression_level 1 ",
                                      'Level 2 ......': "-compression_level 2 ",
                                      'Level 3 ......': "-compression_level 3 ",
                                      'Level 4 ......': "-compression_level 4 ",
                                      'Level 5 - Default Compression/Speed': "",
                                      'Level 6 ......': "-compression_level 6 ",
                                      'Level 7 ......': "-compression_level 7 ",
                                      'Level 8 ......': "-compression_level 8 ",
                                      'Level 9 ......': "-compression_level 9 ",
                                      'Level 10 ......': "-compression_level 10 ",
                                      'Level 11 ......': "-compression_level 11 ",
                                      'Level 12 - Highest Compression/Slow': "-compression_level 12 "}
            acodec_bitrate.set(config_profile['FFMPEG FLAC - SETTINGS']['acodec_bitrate'])  # set the default option
            acodec_bitrate_menu_label = Label(audio_window, text="Compression Level :", background="#434547",
                                              foreground="white")
            acodec_bitrate_menu_label.grid(row=0, column=2, columnspan=1, padx=10, pady=3, sticky=W + E)
            acodec_bitrate_menu = OptionMenu(audio_window, acodec_bitrate, *acodec_bitrate_choices.keys())
            acodec_bitrate_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=15,
                                       anchor=W)
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

            # Audio Volume Selection ----------------------------------------------------------------------------------
            ffmpeg_volume = StringVar()
            ffmpeg_volume_label = Label(audio_window, text="Volume :", background="#434547", foreground="white")
            ffmpeg_volume_label.grid(row=2, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            ffmpeg_volume_spinbox = Spinbox(audio_window, from_=-20, to=20, increment=0.1, justify=CENTER, wrap=True,
                                            textvariable=ffmpeg_volume, state='readonly')
            ffmpeg_volume_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                            buttonbackground="black", width=15, readonlybackground="#23272A")
            ffmpeg_volume_spinbox.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            ffmpeg_volume.set(config_profile['FFMPEG FLAC - SETTINGS']['volume'])
            volume_right_click_options()
            # -------------------------------------------------------------------------------------------------- Volume

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
                if flac_custom_cmd.get().strip() == "":
                    flac_custom_cmd_input = ""
                else:
                    cstmcmd = flac_custom_cmd.get().strip()
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
            flac_acodec_coefficient_label = Label(audio_window, text="LPC Coefficient Precision :",
                                                  background="#434547",
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
        except (Exception,):
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
            audio_window.protocol('WM_DELETE_WINDOW', audio_window_exit_function)

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
                global cmd_line_window, show_cmd_scrolled
                audio_filter_function()
                example_cmd_output = ' '.join(str(acodec_stream_choices[acodec_stream.get()] +
                                                  encoder_dropdownmenu_choices[encoder.get()] +
                                                  acodec_channel_choices[acodec_channel.get()] +
                                                  acodec_samplerate_choices[acodec_samplerate.get()] +
                                                  audio_filter_setting + min_pre_order + max_pre_order +
                                                  flac_custom_cmd_input).split())
                try:
                    show_cmd_scrolled.configure(state=NORMAL)
                    show_cmd_scrolled.delete(1.0, END)
                    show_cmd_scrolled.insert(END, example_cmd_output)
                    show_cmd_scrolled.see(END)
                    show_cmd_scrolled.configure(state=DISABLED)
                    cmd_line_window.deiconify()
                except (AttributeError, NameError):
                    cmd_line_window = Toplevel()
                    cmd_line_window.title('Command Line')
                    cmd_line_window.configure(background="#434547")

                    show_cmd_scrolled = scrolledtextwidget.ScrolledText(cmd_line_window, width=70, height=10, tabs=10,
                                                                        spacing2=3, spacing1=2, spacing3=3)
                    show_cmd_scrolled.grid(row=0, column=0, pady=(5, 4), padx=5, sticky=E + W)
                    show_cmd_scrolled.configure(state=NORMAL, bg='black', fg='#CFD2D1', bd=8)
                    show_cmd_scrolled.insert(END, example_cmd_output)
                    show_cmd_scrolled.see(END)
                    show_cmd_scrolled.configure(state=DISABLED)
                    cmd_line_window.resizable(False, False)  # Disables resizable functions of window

                    def copy_to_clipboard():  # Function to allow copying full command to clipboard via pyperclip module
                        pyperclip.copy(show_cmd_scrolled.get(1.0, END))

                    copy_text = HoverButton(cmd_line_window, text='Copy to clipboard', command=copy_to_clipboard,
                                            foreground='white', background='#23272A', borderwidth='3',
                                            activebackground='grey')
                    copy_text.grid(row=1, column=0, columnspan=1, padx=(20, 20), pady=(4, 5), sticky=E)

                    def hide_instead():
                        cmd_line_window.withdraw()

                    cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

            # --------------------------------------------------------------------------------------- Views Command

            # Buttons ---------------------------------------------------------------------------------------------
            apply_button = HoverButton(audio_window, text="Apply", foreground="white", background="#23272A",
                                       command=lambda: [set_encode_manual(), gotosavefile()], activebackground='grey')
            apply_button.grid(row=10, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)

            show_cmd = HoverButton(audio_window, text="View Command", foreground="white", background="#23272A",
                                   command=view_command, activebackground='grey')
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

            # Audio Volume Selection ----------------------------------------------------------------------------------
            ffmpeg_volume = StringVar()
            ffmpeg_volume_label = Label(audio_window, text="Volume :", background="#434547", foreground="white")
            ffmpeg_volume_label.grid(row=2, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            ffmpeg_volume_spinbox = Spinbox(audio_window, from_=-30, to=30, increment=0.5, justify=CENTER, wrap=True,
                                            textvariable=ffmpeg_volume, state='readonly')
            ffmpeg_volume_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                            buttonbackground="black", width=15, readonlybackground="#23272A")
            ffmpeg_volume_spinbox.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            ffmpeg_volume.set(config_profile['FFMPEG ALAC - SETTINGS']['volume'])
            volume_right_click_options()
            # -------------------------------------------------------------------------------------------------- Volume

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
                if flac_custom_cmd.get().strip() == "":
                    flac_custom_cmd_input = ""
                else:
                    cstmcmd = flac_custom_cmd.get().strip()
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

    try:  # If "View Command" window is opened, when the user selected "Apply" in the codec window it will close
        cmd_line_window
    except NameError:  # If "View Command" window does not exist, do nothing
        pass


# ---------------------------------------------------------------------------------------------- End Audio Codec Window

# File Input ----------------------------------------------------------------------------------------------------------
def file_input():
    global VideoInput, VideoInputQuoted, VideoOutput, autofilesave_dir_path, track_count
    VideoInput = filedialog.askopenfilename(initialdir="/", title="Select A File", filetypes=[("All Files", "*.*")])

    if VideoInput:  # If user selects a file to open
        VideoInputQuoted = f'"{VideoInput}"'  # Quote VideInput for use in the code
        media_info = MediaInfo.parse(pathlib.Path(VideoInput))  # Parse with media_info module
        total_audio_streams_in_input = media_info.general_tracks[0].count_of_audio_streams  # Check input for audio
        if total_audio_streams_in_input is not None:  # If audio is not None (1 or more audio tracks)
            input_entry.configure(state=NORMAL)  # Enable input entry box
            input_entry.delete(0, END)  # Remove text from input entry box if there is any
            autofilesave_file_path = pathlib.Path(VideoInput)  # Command to get file input location
            autofilesave_dir_path = autofilesave_file_path.parents[0]  # Get only the directory from input
            encoder_menu.config(state=NORMAL)  # Enable encoder_menu
            track_count = total_audio_streams_in_input  # Get track count from input
            input_entry.insert(0, str(pathlib.Path(VideoInput)))  # Insert VideoInput into the input entry
            input_entry.configure(state=DISABLED)  # Disable input entry
            output_entry.configure(state=NORMAL)  # Enable output entry
            output_entry.delete(0, END)  # Delete output entry text
            output_entry.configure(state=DISABLED)  # Disable output entry
        elif total_audio_streams_in_input is None:  # If input has 0 audio tracks
            input_entry.config(state=DISABLED)  # Disable input entry-box
            messagebox.showinfo(title="No Audio Streams", message=f"{VideoInputQuoted}:\n\nDoes not "
                                                                  f"contain any audio streams!")  # Display error msg

    if not VideoInput:  # If user presses cancel
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
    if encoder.get() == "AAC":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".mp4", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location", initialfile=autosavefilename,
                                                   filetypes=[("AAC", "*.mp4")])
    elif encoder.get() == "AC3" or encoder.get() == "E-AC3":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".ac3", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location", initialfile=autosavefilename,
                                                   filetypes=[("'AC3', 'E-AC3,'", "*.ac3")])
    elif encoder.get() == "DTS":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".dts", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location", initialfile=autosavefilename,
                                                   filetypes=[("DTS", "*.dts")])
    elif encoder.get() == "Opus":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".opus", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location", initialfile=autosavefilename,
                                                   filetypes=[("Opus", "*.opus")])
    elif encoder.get() == "MP3":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".mp3", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location", initialfile=autosavefilename,
                                                   filetypes=[("MP3", "*.mp3")])
    elif encoder.get() == "FDK-AAC" or encoder.get() == "QAAC" or encoder.get() == "ALAC":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".m4a", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location", initialfile=autosavefilename,
                                                   filetypes=[("'AAC,' 'ALAC,'", "*.m4a")])
    elif encoder.get() == "FLAC":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".flac", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location", initialfile=autosavefilename,
                                                   filetypes=[("FLAC", "*.flac")])

    if VideoOutput:
        output_entry.configure(state=NORMAL)  # Enable entry box for commands under
        output_entry.delete(0, END)  # Remove current text in entry
        output_entry.insert(0, str(pathlib.Path(VideoOutput)))  # Insert the 'path'
        output_entry.configure(state=DISABLED)  # Disables Entry Box


# --------------------------------------------------------------------------------------------------------- File Output
def encoder_menu_hover(e):
    encoder_menu["bg"] = "grey"
    encoder_menu["activebackground"] = "grey"


def encoder_menu_hover_leave(e):
    encoder_menu["bg"] = "#23272A"


# Print Command Line from ROOT ----------------------------------------------------------------------------------------
def print_command_line():
    cmd_line_window = Toplevel()
    cmd_line_window.title('Display Command')
    cmd_line_window.configure(background="#434547")
    VideoInputQuoted = '"' + VideoInput + '"'
    VideoOutputQuoted = '"' + VideoOutput + '"'
    audio_filter_function()
    # DTS Command Line Main Gui ---------------------------------------------------------------------------------------
    if encoder.get() == "DTS":
        if dts_settings.get() == 'DTS Encoder':
            example_cmd_output = ' '.join(str('"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " +
                                              VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] +
                                              dts_settings_choices[dts_settings.get()] + "-b:a " +
                                              dts_bitrate_spinbox.get() + "k " +
                                              acodec_channel_choices[acodec_channel.get()] +
                                              acodec_samplerate_choices[acodec_samplerate.get()] +
                                              audio_filter_setting + dts_custom_cmd_input +
                                              "-sn -vn -map_chapters -1 " + VideoOutputQuoted +
                                              " -v error -hide_banner -stats").split())
        else:
            example_cmd_output = ' '.join(str('"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " +
                                              VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] +
                                              dts_settings_choices[dts_settings.get()] + dts_custom_cmd_input +
                                              "-sn -vn -map_chapters -1 " + VideoOutputQuoted +
                                              " -v error -hide_banner -stats").split())
    # --------------------------------------------------------------------------------------- DTS Command Line Main Gui
    # FDK View Command Line -------------------------------------------------------------------------------------------
    elif encoder.get() == "FDK-AAC":
        if shell_options.get() == "Default":
            silent = '--silent '
        else:
            silent = ' '
        example_cmd_output = ' '.join(str('"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " +
                                          VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] +
                                          acodec_channel_choices[acodec_channel.get()] +
                                          acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting +
                                          "-sn -vn -map_chapters -1 -map_metadata -1 " +
                                          "-f caf - -v error -hide_banner -stats | " +
                                          fdkaac + " " + acodec_profile_choices[acodec_profile.get()] +
                                          fdkaac_title_input + fdkaac_custom_cmd_input +
                                          acodec_gapless_mode_choices[acodec_gapless_mode.get()] +
                                          afterburnervar.get() + crccheck.get() + moovbox.get() + sbrdelay.get() +
                                          headerperiod.get() + acodec_lowdelay_choices[acodec_lowdelay.get()] +
                                          acodec_sbr_ratio_choices[acodec_sbr_ratio.get()] +
                                          acodec_transport_format_choices[acodec_transport_format.get()] +
                                          acodec_bitrate_choices[acodec_bitrate.get()] + silent + "- -o " +
                                          VideoOutputQuoted).split())
    # ---------------------------------------------------------------------------------------------------- FDK CMD LINE
    # QAAC View Command Line ------------------------------------------------------------------------------------------
    elif encoder.get() == "QAAC":
        if shell_options.get() == "Default":
            silent = '--silent '
        else:
            silent = ' '
        if q_acodec_profile.get() == "True VBR":
            example_cmd_output = ' '.join(str('"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " +
                                              VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] +
                                              acodec_channel_choices[acodec_channel.get()] + audio_filter_setting +
                                              acodec_samplerate_choices[acodec_samplerate.get()] +
                                              "-sn -vn -map_chapters -1 -map_metadata -1 " +
                                              "-f wav - -v error -hide_banner -stats | " + qaac +
                                              " --ignorelength " + q_acodec_profile_choices[q_acodec_profile.get()] +
                                              q_acodec_quality_amnt.get() + ' ' + qaac_high_efficiency.get() +
                                              qaac_normalize.get() + qaac_nodither.get() + "--gain " +
                                              q_acodec_gain.get() + ' ' +
                                              q_acodec_quality_choices[q_acodec_quality.get()] +
                                              qaac_nodelay.get() + q_gapless_mode_choices[q_gapless_mode.get()] +
                                              qaac_nooptimize.get() + qaac_threading.get() + qaac_limiter.get() +
                                              qaac_title_input + qaac_custom_cmd_input + silent + "- -o " +
                                              VideoOutputQuoted).split())
        else:
            example_cmd_output = ' '.join(str('"' + ffmpeg + " -analyzeduration 100M -probesize 50M -i " +
                                              VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] +
                                              acodec_channel_choices[acodec_channel.get()] + audio_filter_setting +
                                              acodec_samplerate_choices[acodec_samplerate.get()] +
                                              "-sn -vn -map_chapters -1 -map_metadata -1 " +
                                              "-f wav - -v error -hide_banner -stats | " + qaac +
                                              " --ignorelength " + q_acodec_profile_choices[q_acodec_profile.get()] +
                                              q_acodec_bitrate.get() + qaac_high_efficiency.get() +
                                              qaac_normalize.get() + qaac_nodither.get() + "--gain " +
                                              q_acodec_gain.get() + ' ' +
                                              q_acodec_quality_choices[q_acodec_quality.get()] + qaac_nodelay.get() +
                                              q_gapless_mode_choices[q_gapless_mode.get()] + qaac_nooptimize.get() +
                                              qaac_threading.get() + qaac_limiter.get() + qaac_title_input +
                                              qaac_custom_cmd_input + silent + "- -o " +
                                              VideoOutputQuoted).split())
    # ------------------------------------------------------------------------------------------------------------ QAAC
    # AAC Command Line ------------------------------------------------------------------------------------------------
    elif encoder.get() == "AAC":
        if aac_vbr_toggle.get() == "-c:a ":
            bitrate_or_quality = f"-b:a {aac_bitrate_spinbox.get()}k "
        elif aac_vbr_toggle.get() == "-q:a ":
            bitrate_or_quality = f"-q:a {aac_quality_spinbox.get()} "
        example_cmd_output = ' '.join(str('"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " +
                                          VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] +
                                          encoder_dropdownmenu_choices[encoder.get()] + bitrate_or_quality +
                                          acodec_channel_choices[acodec_channel.get()] +
                                          acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting +
                                          "-sn -vn -map_chapters -1 -map_metadata -1 " + aac_custom_cmd_input +
                                          aac_title_input + VideoOutputQuoted +
                                          " -v error -hide_banner -stats").split())
    # ------------------------------------------------------------------------------------------------ AAC Command Line
    # AC3 Command Line ------------------------------------------------------------------------------------------------
    elif encoder.get() == "AC3":
        example_cmd_output = ' '.join(str('"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " +
                                          VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] +
                                          encoder_dropdownmenu_choices[encoder.get()] +
                                          acodec_bitrate_choices[acodec_bitrate.get()] +
                                          acodec_channel_choices[acodec_channel.get()] +
                                          acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting +
                                          "-sn -vn -map_chapters -1 -map_metadata -1 " + ac3_custom_cmd_input +
                                          VideoOutputQuoted + " -v error -hide_banner -stats").split())
    # ------------------------------------------------------------------------------------------------ AC3 Command Line
    # Opus Command Line -----------------------------------------------------------------------------------------------
    elif encoder.get() == "Opus":
        example_cmd_output = ' '.join(str('"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " +
                                          VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] +
                                          encoder_dropdownmenu_choices[encoder.get()] +
                                          acodec_vbr_choices[acodec_vbr.get()] +
                                          acodec_bitrate_choices[acodec_bitrate.get()] +
                                          acodec_channel_choices[acodec_channel.get()] +
                                          acodec_application_choices[acodec_application.get()] +
                                          opus_mapping_family_choices[opus_mapping_family.get()] + "-packet_loss " +
                                          packet_loss.get() + " -frame_duration " + frame_duration.get() + " " +
                                          acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting +
                                          "-sn -vn -map_chapters -1 -map_metadata -1 " + opus_custom_cmd_input +
                                          VideoOutputQuoted + " -v error -hide_banner -stats").split())
    # ----------------------------------------------------------------------------------------------- Opus Command Line
    # MP3 Command Line ------------------------------------------------------------------------------------------------
    elif encoder.get() == "MP3":
        example_cmd_output = ' '.join(str('"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " +
                                          VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] +
                                          encoder_dropdownmenu_choices[encoder.get()] +
                                          acodec_bitrate_choices[acodec_bitrate.get()] +
                                          acodec_channel_choices[acodec_channel.get()] + mp3_abr.get() +
                                          acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting +
                                          "-sn -vn -map_chapters -1 -map_metadata -1 " + mp3_custom_cmd_input +
                                          VideoOutputQuoted + " -v error -hide_banner -stats").split())
    # ------------------------------------------------------------------------------------------------ MP3 Command Line
    # E-AC3 Command Line ----------------------------------------------------------------------------------------------
    elif encoder.get() == "E-AC3":
        example_cmd_output = ' '.join(str('"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " +
                                          VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] +
                                          encoder_dropdownmenu_choices[encoder.get()] + "-b:a " + eac3_spinbox.get() +
                                          acodec_channel_choices[acodec_channel.get()] +
                                          acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting +
                                          eac3_custom_cmd_input + per_frame_metadata_choices[per_frame_metadata.get()] +
                                          "-mixing_level " + eac3_mixing_level.get() + " " +
                                          room_type_choices[room_type.get()] + "-copyright " + copyright_bit.get() +
                                          " " + "-dialnorm " + dialogue_level.get() + " " +
                                          dolby_surround_mode_choices[dolby_surround_mode.get()] + "-original " +
                                          original_bit_stream.get() + " " + downmix_mode_choices[downmix_mode.get()] +
                                          "-ltrt_cmixlev " + lt_rt_center_mix.get() + " " + "-ltrt_surmixlev " +
                                          lt_rt_surround_mix.get() + " " + "-loro_cmixlev " + lo_ro_center_mix.get() +
                                          " " + "-loro_surmixlev " + lo_ro_surround_mix.get() + " " +
                                          dolby_surround_ex_mode_choices[dolby_surround_ex_mode.get()] +
                                          dolby_headphone_mode_choices[dolby_headphone_mode.get()] +
                                          a_d_converter_type_choices[a_d_converter_type.get()] +
                                          stereo_rematrixing_choices[stereo_rematrixing.get()] + "-channel_coupling " +
                                          channel_coupling.get() + " " + "-cpl_start_band " + cpl_start_band.get() +
                                          " " + "-sn -vn -map_chapters -1 -map_metadata -1 " + VideoOutputQuoted +
                                          " -v error -hide_banner -stats").split())
    # ---------------------------------------------------------------------------------------------- E-AC3 Command Line
    # FLAC Command Line -----------------------------------------------------------------------------------------------
    elif encoder.get() == "FLAC":
        example_cmd_output = ' '.join(str('"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " +
                                          VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] +
                                          encoder_dropdownmenu_choices[encoder.get()] +
                                          acodec_bitrate_choices[acodec_bitrate.get()] +
                                          acodec_channel_choices[acodec_channel.get()] +
                                          acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting +
                                          set_flac_acodec_coefficient +
                                          acodec_flac_lpc_type_choices[acodec_flac_lpc_type.get()] +
                                          acodec_flac_lpc_passes_choices[acodec_flac_lpc_passes.get()] +
                                          flac_custom_cmd_input + "-sn -vn -map_chapters -1 -map_metadata -1 " +
                                          VideoOutputQuoted + " -v error -hide_banner -stats" + '"').split())
    # ----------------------------------------------------------------------------------------------- FLAC Command Line
    # ALAC Command Line -----------------------------------------------------------------------------------------------
    elif encoder.get() == "ALAC":
        example_cmd_output = ' '.join(str('"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " +
                                          VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] +
                                          encoder_dropdownmenu_choices[encoder.get()] +
                                          acodec_channel_choices[acodec_channel.get()] +
                                          acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting +
                                          min_pre_order + max_pre_order + flac_custom_cmd_input + " " +
                                          "-sn -vn -map_chapters -1 -map_metadata -1 " +
                                          VideoOutputQuoted + " -v error -hide_banner -stats" + '"').split())
    # ----------------------------------------------------------------------------------------------- ALAC Command Line
    show_cmd_scrolled = scrolledtextwidget.ScrolledText(cmd_line_window, width=90, height=10, tabs=10, spacing2=3,
                                                        spacing1=2, spacing3=3)
    show_cmd_scrolled.grid(row=0, column=0, pady=(5, 4), padx=5, sticky=E + W)
    show_cmd_scrolled.configure(state=NORMAL, bg='black', fg='#CFD2D1', bd=8)
    show_cmd_scrolled.insert(END, example_cmd_output)
    show_cmd_scrolled.see(END)
    show_cmd_scrolled.configure(state=DISABLED)

    def copy_to_clipboard():  # Function to allow copying full command to clipboard via pyperclip module
        pyperclip.copy(show_cmd_scrolled.get(1.0, END))

    copy_text = HoverButton(cmd_line_window, text='Copy to clipboard', command=copy_to_clipboard,
                            foreground='white', background='#23272A', borderwidth='3', activebackground='grey')
    copy_text.grid(row=1, column=0, columnspan=1, padx=(20, 20), pady=(4, 5), sticky=E)


# ---------------------------------------------------------------------------------------- Print Command Line from ROOT

# Start Audio Job -----------------------------------------------------------------------------------------------------
def startaudiojob():
    global example_cmd_output, ac3_job, aac_job, dts_job, opus_job, mp3_job, eac3_job, \
        fdkaac_job, qaac_job, flac_job, alac_job, auto_or_manual, auto_track_input, acodec_stream, \
        acodec_stream_choices
    # Quote File Input/Output Paths------------
    VideoInputQuoted = '"' + VideoInput + '"'
    VideoOutputQuoted = '"' + VideoOutput + '"'
    # -------------------------- Quote File Paths
    # Combine audio filters for FFMPEG
    audio_filter_function()
    # ------------------------- Filters

    complete_or_not = ''  # Set empty placeholder variable for complete_or_not

    if shell_options.get() == "Default":  # Default progress bars
        global total_duration
        media_info = MediaInfo.parse(pathlib.Path(VideoInput))  # Parse input file
        track_selection_mediainfo = media_info.audio_tracks[int(acodec_stream_choices[acodec_stream.get()].strip()[-1])]
        # track_selection_mediainfo uses the -map 0:a:x code to get the track input, the code grabs only the last number
        if track_selection_mediainfo.duration is not None:  # If track input HAS a duration
            total_duration = float(track_selection_mediainfo.duration)
        elif track_selection_mediainfo.duration is None:  # If track input DOES NOT have a duration
            messagebox.showinfo(title='Info', message='Input file has no duration, consider muxing elementary '
                                                      'stream into mka/mkv/etc...\n\nProgress bar is '
                                                      'temporarily disabled')
            total_duration = track_selection_mediainfo.duration

        def close_encode():
            if complete_or_not == 'complete':
                window.destroy()
            else:
                confirm_exit = messagebox.askyesno(title='Prompt',
                                                   message="Are you sure you want to stop the encode?", parent=window)
                if confirm_exit:
                    subprocess.Popen(f"TASKKILL /F /PID {job.pid} /T", creationflags=subprocess.CREATE_NO_WINDOW)
                    window.destroy()

        def close_window():
            thread = threading.Thread(target=close_encode)
            thread.start()

        window = Toplevel(root)
        window.title('Codec : ' + encoder.get() + '  |  ' + str(pathlib.Path(VideoInput).stem))
        window.configure(background="#434547")
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=1)
        window.protocol('WM_DELETE_WINDOW', close_window)
        encode_window_progress = scrolledtextwidget.ScrolledText(window, width=90, height=15, tabs=10, spacing2=3,
                                                                 spacing1=2, spacing3=3)
        encode_window_progress.grid(row=0, column=0, pady=(10, 6), padx=10, sticky=E + W)
        encode_window_progress.config(bg='black', fg='#CFD2D1', bd=8)
        encode_window_progress.insert(END, ' - - - - - - - - - - - Encode Started - - - - - - - - - - - \n\n')

        def auto_close_window_toggle():  # Function to save input from the checkbox below to config.ini
            try:
                config.set('auto_close_progress_window', 'option', auto_close_window.get())
                with open(config_file, 'w') as configfile:
                    config.write(configfile)
            except (Exception,):
                pass

        auto_close_window_checkbox = Checkbutton(window, text='Automatically Close', variable=auto_close_window,
                                                 onvalue='on', offvalue='off', command=auto_close_window_toggle,
                                                 takefocus=False)
        auto_close_window_checkbox.grid(row=1, column=0, columnspan=1, rowspan=1, padx=10, pady=(10, 5), sticky=W)
        auto_close_window_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                             activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        auto_close_window.set(config['auto_close_progress_window']['option'])

        def copy_to_clipboard():  # Function to allow copying full command to clipboard via pyperclip module
            pyperclip.copy(encode_window_progress.get(1.0, END))

        copy_text = HoverButton(window, text='Copy to clipboard', command=copy_to_clipboard, state=DISABLED,
                                foreground='white', background='#23272A', borderwidth='3', activebackground='grey')
        copy_text.grid(row=1, column=0, columnspan=1, padx=(20, 20), pady=(10, 5), sticky=E)

        if total_duration is not None:
            app_progress_bar = ttk.Progressbar(window, orient=HORIZONTAL, mode='determinate',
                                               style="custom.Horizontal.TProgressbar")
            app_progress_bar.grid(column=0, row=6, columnspan=4, sticky=W + E, pady=(0, 2), padx=3)
        if total_duration is None:
            temp_label = Label(window, text='Input has no duration - progress bar is temporarily disabled',
                               bd=4, relief=SUNKEN, anchor=E, background='#717171', foreground="white")
            temp_label.grid(column=0, row=6, columnspan=4, pady=(0, 2), padx=3, sticky=E + W)

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
        finalcommand = ' '.join(str('"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted +
                                    acodec_stream_choices[acodec_stream.get()] +
                                    encoder_dropdownmenu_choices[encoder.get()] +
                                    acodec_bitrate_choices[acodec_bitrate.get()] +
                                    acodec_channel_choices[acodec_channel.get()] +
                                    acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting +
                                    "-sn -vn -map_chapters -1 -map_metadata -1 " + ac3_custom_cmd_input +
                                    VideoOutputQuoted + " -v error -hide_banner -stats").split())
        last_used_command = ' '.join(str(encoder_dropdownmenu_choices[encoder.get()] +
                                         acodec_bitrate_choices[acodec_bitrate.get()] +
                                         acodec_channel_choices[acodec_channel.get()] +
                                         acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting +
                                         "-sn -vn -map_chapters -1 -map_metadata -1 " + ac3_custom_cmd_input).split())

    # --------------------------------------------------------------------------------------------------------- AC3 Job
    # AAC Start Job ---------------------------------------------------------------------------------------------------
    elif encoder.get() == "AAC":
        if aac_vbr_toggle.get() == "-c:a ":
            bitrate_or_quality = f"-b:a {aac_bitrate_spinbox.get()}k "
        elif aac_vbr_toggle.get() == "-q:a ":
            bitrate_or_quality = f"-q:a {aac_quality_spinbox.get()} "
        finalcommand = ' '.join(str('"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted +
                                    acodec_stream_choices[acodec_stream.get()] +
                                    encoder_dropdownmenu_choices[encoder.get()] + bitrate_or_quality +
                                    acodec_channel_choices[acodec_channel.get()] +
                                    acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting +
                                    "-sn -vn -map_chapters -1 -map_metadata -1 " + aac_custom_cmd_input +
                                    aac_title_input + VideoOutputQuoted + " -v error -hide_banner -stats").split())
        last_used_command = ' '.join(str(encoder_dropdownmenu_choices[encoder.get()] + bitrate_or_quality +
                                         acodec_channel_choices[acodec_channel.get()] +
                                         acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting +
                                         "-sn -vn -map_chapters -1 -map_metadata -1 " + aac_custom_cmd_input +
                                         aac_title_input).split())
        # ------------------------------------------------------------------------------------------------- AAC Job
    # DTS Start Job ---------------------------------------------------------------------------------------------------
    elif encoder.get() == 'DTS':
        if dts_settings.get() == 'DTS Encoder':
            finalcommand = ' '.join(str('"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " +
                                        VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] +
                                        dts_settings_choices[dts_settings.get()] + "-b:a " +
                                        dts_bitrate_spinbox.get() + "k " +
                                        acodec_channel_choices[acodec_channel.get()] +
                                        acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting +
                                        dts_custom_cmd_input + "-sn -vn -map_chapters -1 " + VideoOutputQuoted +
                                        " -v error -hide_banner -stats").split())
            last_used_command = ' '.join(str(dts_settings_choices[dts_settings.get()] + "-b:a " +
                                             dts_bitrate_spinbox.get() + "k " +
                                             acodec_channel_choices[acodec_channel.get()] +
                                             acodec_samplerate_choices[acodec_samplerate.get()] +
                                             audio_filter_setting + dts_custom_cmd_input +
                                             "-sn -vn -map_chapters -1 ").split())
        elif dts_settings.get() != 'DTS Encoder':
            finalcommand = ' '.join(str('"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " +
                                        VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] +
                                        dts_settings_choices[dts_settings.get()] + dts_custom_cmd_input +
                                        "-sn -vn -map_chapters -1 " + VideoOutputQuoted +
                                        " -v error -hide_banner -stats").split())
            last_used_command = ' '.join(str(dts_settings_choices[dts_settings.get()] + dts_custom_cmd_input +
                                             "-sn -vn -map_chapters -1 ").split())
    # ------------------------------------------------------------------------------------------------------------- DTS
    # Opus Start Job --------------------------------------------------------------------------------------------------
    elif encoder.get() == "Opus":
        finalcommand = ' '.join(str('"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted +
                                    acodec_stream_choices[acodec_stream.get()] +
                                    encoder_dropdownmenu_choices[encoder.get()] +
                                    acodec_vbr_choices[acodec_vbr.get()] +
                                    acodec_bitrate_choices[acodec_bitrate.get()] +
                                    acodec_channel_choices[acodec_channel.get()] +
                                    acodec_application_choices[acodec_application.get()] +
                                    opus_mapping_family_choices[opus_mapping_family.get()] + "-packet_loss " +
                                    packet_loss.get() + " -frame_duration " + frame_duration.get() + " " +
                                    acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting +
                                    "-sn -vn -map_chapters -1 -map_metadata -1 " + opus_custom_cmd_input +
                                    VideoOutputQuoted + " -v error -hide_banner -stats").split())
        last_used_command = ' '.join(str(encoder_dropdownmenu_choices[encoder.get()] +
                                         acodec_vbr_choices[acodec_vbr.get()] +
                                         acodec_bitrate_choices[acodec_bitrate.get()] +
                                         acodec_channel_choices[acodec_channel.get()] +
                                         acodec_application_choices[acodec_application.get()] +
                                         opus_mapping_family_choices[opus_mapping_family.get()] + "-packet_loss " +
                                         packet_loss.get() + " -frame_duration " + frame_duration.get() + " " +
                                         acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting +
                                         "-sn -vn -map_chapters -1 -map_metadata -1 ").split())
    # ------------------------------------------------------------------------------------------------------------ Opus
    # MP3 Start Job ---------------------------------------------------------------------------------------------------
    elif encoder.get() == "MP3":
        finalcommand = ' '.join(str('"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted +
                                    acodec_stream_choices[acodec_stream.get()] +
                                    encoder_dropdownmenu_choices[encoder.get()] +
                                    acodec_bitrate_choices[acodec_bitrate.get()] +
                                    acodec_channel_choices[acodec_channel.get()] + mp3_abr.get() +
                                    acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting +
                                    "-sn -vn -map_chapters -1 -map_metadata -1 " + mp3_custom_cmd_input +
                                    VideoOutputQuoted + " -v error -hide_banner -stats").split())
        last_used_command = ' '.join(str(encoder_dropdownmenu_choices[encoder.get()] +
                                         acodec_bitrate_choices[acodec_bitrate.get()] +
                                         acodec_channel_choices[acodec_channel.get()] + mp3_abr.get() +
                                         acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting +
                                         "-sn -vn -map_chapters -1 -map_metadata -1 " + mp3_custom_cmd_input).split())
    # ------------------------------------------------------------------------------------------------------------- MP3
    # E-AC3 Start Job -------------------------------------------------------------------------------------------------
    elif encoder.get() == "E-AC3":
        finalcommand = ' '.join(str('"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted +
                                    acodec_stream_choices[acodec_stream.get()] +
                                    encoder_dropdownmenu_choices[encoder.get()] + "-b:a " + eac3_spinbox.get() +
                                    acodec_channel_choices[acodec_channel.get()] +
                                    acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting +
                                    eac3_custom_cmd_input + per_frame_metadata_choices[per_frame_metadata.get()] +
                                    "-mixing_level " + eac3_mixing_level.get() + " " +
                                    room_type_choices[room_type.get()] + "-copyright " + copyright_bit.get() + " " +
                                    "-dialnorm " + dialogue_level.get() + " " +
                                    dolby_surround_mode_choices[dolby_surround_mode.get()] + "-original " +
                                    original_bit_stream.get() + " " + downmix_mode_choices[downmix_mode.get()] +
                                    "-ltrt_cmixlev " + lt_rt_center_mix.get() + " " + "-ltrt_surmixlev " +
                                    lt_rt_surround_mix.get() + " " + "-loro_cmixlev " + lo_ro_center_mix.get() + " " +
                                    "-loro_surmixlev " + lo_ro_surround_mix.get() + " " +
                                    dolby_surround_ex_mode_choices[dolby_surround_ex_mode.get()] +
                                    dolby_headphone_mode_choices[dolby_headphone_mode.get()] +
                                    a_d_converter_type_choices[a_d_converter_type.get()] +
                                    stereo_rematrixing_choices[stereo_rematrixing.get()] + "-channel_coupling " +
                                    channel_coupling.get() + " " + "-cpl_start_band " + cpl_start_band.get() + " " +
                                    "-sn -vn -map_chapters -1 -map_metadata -1 " + VideoOutputQuoted +
                                    " -v error -hide_banner -stats").split())
        last_used_command = ' '.join(str(encoder_dropdownmenu_choices[encoder.get()] + "-b:a " + eac3_spinbox.get() +
                                         acodec_channel_choices[acodec_channel.get()] +
                                         acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting +
                                         eac3_custom_cmd_input + per_frame_metadata_choices[per_frame_metadata.get()] +
                                         "-mixing_level " + eac3_mixing_level.get() + " " +
                                         room_type_choices[room_type.get()] + "-copyright " + copyright_bit.get() +
                                         " " + "-dialnorm " + dialogue_level.get() + " " +
                                         dolby_surround_mode_choices[dolby_surround_mode.get()] + "-original " +
                                         original_bit_stream.get() + " " + downmix_mode_choices[downmix_mode.get()] +
                                         "-ltrt_cmixlev " + lt_rt_center_mix.get() + " " + "-ltrt_surmixlev " +
                                         lt_rt_surround_mix.get() + " " + "-loro_cmixlev " + lo_ro_center_mix.get() +
                                         " " + "-loro_surmixlev " + lo_ro_surround_mix.get() + " " +
                                         dolby_surround_ex_mode_choices[dolby_surround_ex_mode.get()] +
                                         dolby_headphone_mode_choices[dolby_headphone_mode.get()] +
                                         a_d_converter_type_choices[a_d_converter_type.get()] +
                                         stereo_rematrixing_choices[stereo_rematrixing.get()] + "-channel_coupling " +
                                         channel_coupling.get() + " " + "-cpl_start_band " + cpl_start_band.get() +
                                         " " + "-sn -vn -map_chapters -1 ").split())
    # ----------------------------------------------------------------------------------------------------------- E-AC3
    # FDK_AAC Start Job -----------------------------------------------------------------------------------------------
    elif encoder.get() == "FDK-AAC":
        if shell_options.get() == "Default":
            silent = '--silent '
        else:
            silent = ' '
        finalcommand = ' '.join(str('"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted +
                                    acodec_stream_choices[acodec_stream.get()] +
                                    acodec_channel_choices[acodec_channel.get()] +
                                    acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting +
                                    "-sn -vn -map_chapters -1 -map_metadata -1 " +
                                    "-f caf - -v error -hide_banner -stats | " +
                                    fdkaac + " " + acodec_profile_choices[acodec_profile.get()] +
                                    fdkaac_title_input + fdkaac_custom_cmd_input +
                                    acodec_gapless_mode_choices[acodec_gapless_mode.get()] + afterburnervar.get() +
                                    crccheck.get() + moovbox.get() + sbrdelay.get() + headerperiod.get() +
                                    acodec_lowdelay_choices[acodec_lowdelay.get()] +
                                    acodec_sbr_ratio_choices[acodec_sbr_ratio.get()] +
                                    acodec_transport_format_choices[acodec_transport_format.get()] +
                                    acodec_bitrate_choices[acodec_bitrate.get()] + silent + "- -o " +
                                    VideoOutputQuoted).split())
        last_used_command = ' '.join(str(acodec_channel_choices[acodec_channel.get()] +
                                         acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting +
                                         "-sn -vn -map_chapters -1 -map_metadata -1 " +
                                         "-f caf - -v error -hide_banner -stats | " + fdkaac + " " +
                                         acodec_profile_choices[acodec_profile.get()] + fdkaac_title_input +
                                         fdkaac_custom_cmd_input +
                                         acodec_gapless_mode_choices[acodec_gapless_mode.get()] +
                                         afterburnervar.get() + crccheck.get() + moovbox.get() + sbrdelay.get() +
                                         headerperiod.get() + acodec_lowdelay_choices[acodec_lowdelay.get()] +
                                         acodec_sbr_ratio_choices[acodec_sbr_ratio.get()] +
                                         acodec_transport_format_choices[acodec_transport_format.get()] +
                                         acodec_bitrate_choices[acodec_bitrate.get()] +
                                         silent + "- -o ").split())
    # ------------------------------------------------------------------------------------------------------------- FDK
    # QAAC Start Job --------------------------------------------------------------------------------------------------
    elif encoder.get() == "QAAC":
        if shell_options.get() == "Default":
            silent = '--silent '
        else:
            silent = ' '
        if q_acodec_profile.get() == "True VBR":
            finalcommand = ' '.join(str('"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " +
                                        VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] +
                                        acodec_channel_choices[acodec_channel.get()] + audio_filter_setting +
                                        acodec_samplerate_choices[acodec_samplerate.get()] +
                                        "-sn -vn -map_chapters -1 -map_metadata -1 " +
                                        "-f wav - -v error -hide_banner -stats | " + qaac +
                                        " --ignorelength " + q_acodec_profile_choices[q_acodec_profile.get()] +
                                        q_acodec_quality_amnt.get() + ' ' + qaac_high_efficiency.get() +
                                        qaac_normalize.get() + qaac_nodither.get() + "--gain " +
                                        q_acodec_gain.get() + ' ' + q_acodec_quality_choices[q_acodec_quality.get()] +
                                        qaac_nodelay.get() + q_gapless_mode_choices[q_gapless_mode.get()] +
                                        qaac_nooptimize.get() + qaac_threading.get() + qaac_limiter.get() +
                                        qaac_title_input + qaac_custom_cmd_input + silent + "- -o " +
                                        VideoOutputQuoted).split())
            last_used_command = ' '.join(str(acodec_channel_choices[acodec_channel.get()] + audio_filter_setting +
                                             acodec_samplerate_choices[acodec_samplerate.get()] +
                                             "-sn -vn -map_chapters -1 -map_metadata -1 " +
                                             "-f wav - -v error -hide_banner -stats | " + qaac + " --ignorelength " +
                                             q_acodec_profile_choices[q_acodec_profile.get()] +
                                             q_acodec_quality_amnt.get() + ' ' + qaac_high_efficiency.get() +
                                             qaac_normalize.get() + qaac_nodither.get() + "--gain " +
                                             q_acodec_gain.get() + ' ' +
                                             q_acodec_quality_choices[q_acodec_quality.get()] + qaac_nodelay.get() +
                                             q_gapless_mode_choices[q_gapless_mode.get()] + qaac_nooptimize.get() +
                                             qaac_threading.get() + qaac_limiter.get() + qaac_title_input +
                                             qaac_custom_cmd_input + silent + "- -o ").split())
        else:
            finalcommand = ' '.join(str('"' + ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted +
                                        acodec_stream_choices[acodec_stream.get()] +
                                        acodec_channel_choices[acodec_channel.get()] + audio_filter_setting +
                                        acodec_samplerate_choices[acodec_samplerate.get()] +
                                        "-sn -vn -map_chapters -1 -map_metadata -1 " +
                                        "-f wav - -v error -hide_banner -stats | " + qaac +
                                        " --ignorelength " + q_acodec_profile_choices[q_acodec_profile.get()] +
                                        q_acodec_bitrate.get() + qaac_high_efficiency.get() + qaac_normalize.get() +
                                        qaac_nodither.get() + "--gain " + q_acodec_gain.get() + ' ' +
                                        q_acodec_quality_choices[q_acodec_quality.get()] + qaac_nodelay.get() +
                                        q_gapless_mode_choices[q_gapless_mode.get()] + qaac_nooptimize.get() +
                                        qaac_threading.get() + qaac_limiter.get() + qaac_title_input +
                                        qaac_custom_cmd_input + silent + "- -o " +
                                        VideoOutputQuoted).split())
            last_used_command = ' '.join(str(acodec_channel_choices[acodec_channel.get()] + audio_filter_setting +
                                             acodec_samplerate_choices[acodec_samplerate.get()] +
                                             "-sn -vn -map_chapters -1 -map_metadata -1 " +
                                             "-f wav - -v error -hide_banner -stats | " + qaac +
                                             " --ignorelength " + q_acodec_profile_choices[q_acodec_profile.get()] +
                                             q_acodec_bitrate.get() + qaac_high_efficiency.get() +
                                             qaac_normalize.get() + qaac_nodither.get() + "--gain " +
                                             q_acodec_gain.get() + ' ' +
                                             q_acodec_quality_choices[q_acodec_quality.get()] + qaac_nodelay.get() +
                                             q_gapless_mode_choices[q_gapless_mode.get()] + qaac_nooptimize.get() +
                                             qaac_threading.get() + qaac_limiter.get() + qaac_title_input +
                                             qaac_custom_cmd_input + silent + "- -o ").split())
    # ------------------------------------------------------------------------------------------------------------ QAAC
    # FLAC Start Job --------------------------------------------------------------------------------------------------
    elif encoder.get() == "FLAC":
        finalcommand = ' '.join(str('"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted +
                                    acodec_stream_choices[acodec_stream.get()] +
                                    encoder_dropdownmenu_choices[encoder.get()] +
                                    acodec_bitrate_choices[acodec_bitrate.get()] +
                                    acodec_channel_choices[acodec_channel.get()] +
                                    acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting +
                                    set_flac_acodec_coefficient +
                                    acodec_flac_lpc_type_choices[acodec_flac_lpc_type.get()] +
                                    acodec_flac_lpc_passes_choices[acodec_flac_lpc_passes.get()] +
                                    flac_custom_cmd_input + "-sn -vn -map_chapters -1 -map_metadata -1 " +
                                    VideoOutputQuoted + " -v error -hide_banner -stats" + '"').split())
        last_used_command = ' '.join(str(encoder_dropdownmenu_choices[encoder.get()] +
                                         acodec_bitrate_choices[acodec_bitrate.get()] +
                                         acodec_channel_choices[acodec_channel.get()] +
                                         acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting +
                                         set_flac_acodec_coefficient +
                                         acodec_flac_lpc_type_choices[acodec_flac_lpc_type.get()] +
                                         acodec_flac_lpc_passes_choices[acodec_flac_lpc_passes.get()] +
                                         flac_custom_cmd_input + "-sn -vn -map_chapters -1 -map_metadata -1 ").split())
    # ------------------------------------------------------------------------------------------------------------ FLAC
    # ALAC Start Job --------------------------------------------------------------------------------------------------
    elif encoder.get() == "ALAC":
        finalcommand = ' '.join(str('"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted +
                                    acodec_stream_choices[acodec_stream.get()] +
                                    encoder_dropdownmenu_choices[encoder.get()] +
                                    acodec_channel_choices[acodec_channel.get()] +
                                    acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting +
                                    min_pre_order + max_pre_order + flac_custom_cmd_input + " " +
                                    "-sn -vn -map_chapters -1 -map_metadata -1 " +
                                    VideoOutputQuoted + " -v error -hide_banner -stats" + '"').split())
        last_used_command = ' '.join(str(encoder_dropdownmenu_choices[encoder.get()] +
                                         acodec_channel_choices[acodec_channel.get()] +
                                         acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting +
                                         min_pre_order + max_pre_order + flac_custom_cmd_input +
                                         "-sn -vn -map_chapters -1 -map_metadata -1 ").split())
    # ------------------------------------------------------------------------------------------------------------ ALAC

    list_of_ffmpeg_encoders_for_job = ['AC3', 'AAC', 'DTS', 'Opus', 'MP3', 'E-AC3', 'FLAC', 'ALAC', 'FDK-AAC', 'QAAC']
    if encoder.get() in list_of_ffmpeg_encoders_for_job:  # If encoder.get() is in the list above continue
        if shell_options.get() == "Default":  # If program is set to progress bars
            if auto_or_manual == 'manual':  # If variable auto_or_manual is set to 'manual', the command = final command
                command = finalcommand
                update_last_codec_command()  # Calls a function that set's the auto encode information to ini file
            elif auto_or_manual == 'auto':  # If variable auto_or_manual is set to 'auto' it uses the info in the
                # ini file to encode with the command below
                if encoder.get() == 'QAAC' or encoder.get() == 'FDK-AAC':
                    hide_banner_verbose = ''
                else:
                    hide_banner_verbose = ' -v error -hide_banner -stats"'
                command = '"' + ffmpeg + " -y -analyzeduration 100M -probesize 50M -i " \
                          + VideoInputQuoted + f' -map 0:a:{str(auto_track_input)} ' + \
                          config_profile['Auto Encode']['command'].lstrip().rstrip() \
                          + ' ' + VideoOutputQuoted + hide_banner_verbose

            # Use subprocess.Popen to feed the command to the terminal and handle the stder/stdout output
            job = subprocess.Popen('cmd /c ' + command + '"', universal_newlines=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                   creationflags=subprocess.CREATE_NO_WINDOW, encoding="utf-8")

            if encoder.get() == 'QAAC' or encoder.get() == 'FDK-AAC':  # String to output for fdk/qaac encoder
                insert_info_string = f'Encoding {str(VideoInputQuoted)} via "FFMPEG" by piping to external encoder: ' \
                                     f'"{str(encoder.get())}"'
            elif encoder.get() != 'QAAC' or encoder.get() != 'FDK-AAC':  # String to output for all internal encoders
                insert_info_string = f'Encoding {str(VideoInputQuoted)} via "FFMPEG" with internal encoder: ' \
                                     f'"{str(encoder.get())}"'

            if auto_or_manual == 'auto':  # If auto_or_manual is set to 'auto', once the user encodes it resets
                # main gui back to default settings
                reset_main_gui()

            encode_window_progress.configure(state=NORMAL)
            encode_window_progress.insert(END, str('\n' + '-' * 62 + '\n'))
            encode_window_progress.insert(END, insert_info_string)  # Insert string for internal/external encoders
            encode_window_progress.insert(END, str('\n' + '-' * 62 + '\n\n\n'))
            encode_window_progress.configure(state=DISABLED)
            progress_error = ''  # Set an empty variable to be changed in the job code

            for line in job.stdout:  # Using subprocess.Popen, read stdout lines
                encode_window_progress.configure(state=NORMAL)
                # Code removes any/all double or white space from string to keep it looking nice (ffmpeg is messy)
                encode_window_progress.insert(END, str('\n'.join(' '.join(x.split()) for x in line.split('\n'))))
                encode_window_progress.see(END)  # Scrolls the textbox to bottom every single pass
                encode_window_progress.configure(state=DISABLED)

                if track_selection_mediainfo.duration is None:  # Set's the percent to 100% if input has no duration
                    percent = 100  # this way the job code can complete without error
                    if line.split()[0] == 'size=' and progress_error != 'no':  # Find string 'size=',
                        # if found program is running correctly, also only check if progress error isn't == 'no'
                        progress_error = 'no'  # Once 'size=' is found update progress_error to 'no'

                if total_duration is not None:  # If input file has duration metadata
                    if line.split()[0] == 'size=':  # Find string 'size=' to start work with progress bar
                        progress_error = 'no'  # Once 'size=' is found set progress_error to 'no'
                        try:  # Block of code to turn 00:00:00 frmt to milliseconds (same as duration) for progress bar
                            time = line.split()[2].rsplit('=', 1)[1]
                            progress = sum(x * float(t) for x, t in zip([1, 60, 3600],
                                                                        reversed(time.split(":")))) * 1000
                            percent = float(str('{:.1%}'.format(progress / total_duration)).replace('%', ''))
                            try:
                                app_progress_bar['value'] = int(percent)  # Input progress into progress bar
                            except (Exception,):
                                pass
                        except (Exception,):  # If progress window errors out for what ever reason
                            progress_error = 'yes'  # Set error to 'yes'
                            window.destroy()  # Close progress window
                            subprocess.Popen(f"TASKKILL /F /PID {job.pid} /T",  # Force close job.pid/children
                                             creationflags=subprocess.CREATE_NO_WINDOW)
                            msg_error = messagebox.askokcancel(title='Error!', message=f'There was an error:'
                                                                                       f'\n\n"{str(line).rstrip()}"\n\n'
                                                                                       f'Would you like to report the '
                                                                                       f'error on the github tracker?')
                            if msg_error:  # If user wants to post bug on the github tracker
                                webbrowser.open('https://github.com/jlw4049/FFMPEG-Audio-Encoder/issues')
            encode_window_progress.configure(state=NORMAL)  # Enable progress window editing
            encode_window_progress.insert(END, str('\n' + '-' * 62 + '\n'))
            if progress_error == 'no' and int(percent) >= 99:  # If no error and percent reached 99%, job is complete
                if pathlib.Path(str(VideoOutputQuoted).replace('"', '')).is_file():  # Check if file exists
                    encode_window_progress.insert(END, str('Job Completed!\n\n'))  # Insert into text window
                    encode_window_progress.insert(END, f'Output file is: \n{str(VideoOutputQuoted)}')
                    complete_or_not = str('complete')  # Set variable to complete, for closing window without prompt
                else:  # If job does not complete, string to show the user there was an error
                    messagebox.showerror(title='Error!', message='There was an error in job:\n\n' + '"Codec : '
                                                                 + encoder.get() + '  |  '
                                                                 + str(pathlib.Path(VideoInput).stem)
                                                                 + '"\n\n Please run job with program in debug mode')
                    window.destroy()  # Close window and kill job.pid/children
                    subprocess.Popen(f"TASKKILL /F /PID {job.pid} /T", creationflags=subprocess.CREATE_NO_WINDOW)

            elif progress_error != 'no' or int(percent) <= 98:  # If there is an error OR percent is less than 98%
                encode_window_progress.insert(END, '\nThere was an error, run the job in debug mode to troubleshoot\n')
            encode_window_progress.insert(END, str('\n' + '-' * 62 + '\n'))
            encode_window_progress.see(END)  # Scroll to bottom of text window
            encode_window_progress.configure(state=DISABLED)  # Disable progress window editing
            copy_text.config(state=NORMAL)  # Enable copy button once all the code completes
            if config['auto_close_progress_window']['option'] == 'on':
                window.destroy()  # If program is set to auto close encoding window when complete, close the window

        elif shell_options.get() == "Debug":  # Debug mode, only opens a cmd.exe terminal for raw output
            subprocess.Popen('cmd /k ' + finalcommand + '"')


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
audiosettings_button = HoverButton(root, text="Audio Settings", command=openaudiowindow, foreground="white",
                                   background="#23272A", state=DISABLED, borderwidth="3", activebackground='grey')
audiosettings_button.grid(row=1, column=3, columnspan=2, padx=5, pady=5, sticky=N + S + W + E)


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
    command_line_button.configure(state=DISABLED)
    output_button.config(state=DISABLED)
    command_line_button.config(state=DISABLED)
    file_input()
    if VideoInput:  # If user does not press cancel in file_input() filedialog box
        if config_profile['Auto Encode']['codec'] == '':
            auto_encode_last_options.configure(state=DISABLED)
        else:
            auto_encode_last_options.configure(state=NORMAL)
            if config_profile['Auto Encode']['codec'] == 'AAC':
                VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '._new_.mp4'
            elif config_profile['Auto Encode']['codec'] == 'AC3' or config_profile['Auto Encode']['codec'] == 'E-AC3':
                VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '._new_.ac3'
            elif config_profile['Auto Encode']['codec'] == "DTS":
                VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '._new_.dts'
            elif config_profile['Auto Encode']['codec'] == "Opus":
                VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '._new_.opus'
            elif config_profile['Auto Encode']['codec'] == 'MP3':
                VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '._new_.mp3'
            elif config_profile['Auto Encode']['codec'] == "FDK-AAC" or \
                    config_profile['Auto Encode']['codec'] == "QAAC" or config_profile['Auto Encode'][
                'codec'] == "ALAC":
                VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '._new_.m4a'
            elif config_profile['Auto Encode']['codec'] == "FLAC":
                VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '._new_.flac'
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

    VideoInputQuoted = f'"{VideoInput}"'  # Quote VideInput for use in the code
    media_info = MediaInfo.parse(pathlib.Path(VideoInput))  # Parse with media_info module
    total_audio_streams_in_input = media_info.general_tracks[0].count_of_audio_streams  # Check input for audio
    if total_audio_streams_in_input is not None:  # If audio is not None (1 or more audio tracks)
        autofilesave_file_path = pathlib.Path(VideoInput)  # Command to get file input location
        autofilesave_dir_path = autofilesave_file_path.parents[0]  # Final command to get only the directory
        track_count = total_audio_streams_in_input  # Get track count from input
        input_entry.insert(0, str(pathlib.Path(str(VideoInput))))  # Insert VideoInput into the input entrybox
        input_entry.configure(state=DISABLED)  # Disable input entry
        output_entry.configure(state=NORMAL)  # Enable output entry
        output_entry.delete(0, END)  # Delete anything in output entry if there is anything
        output_entry.configure(state=DISABLED)  # Disable output entry
        encoder.set("Set Codec")  # Reset encoder selection menu to default
        audiosettings_button.configure(state=DISABLED)  # Disable button
        start_audio_button.configure(state=DISABLED)  # Disable button
        encoder_menu.configure(state=NORMAL)
        output_button.config(state=DISABLED)  # Disable button
        command_line_button.config(state=DISABLED)  # Disable button
        if config_profile['Auto Encode']['codec'] == '':  # If auto-encode profile has no information keep disabled
            auto_encode_last_options.configure(state=DISABLED)
        else:  # If it has information, define VideoOut save location for what ever codec
            auto_encode_last_options.configure(state=NORMAL)
            if config_profile['Auto Encode']['codec'] == 'AAC':
                VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '._new_.mp4'
            elif config_profile['Auto Encode']['codec'] == 'AC3' or \
                    config_profile['Auto Encode']['codec'] == 'E-AC3':
                VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '._new_.ac3'
            elif config_profile['Auto Encode']['codec'] == "DTS":
                VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '._new_.dts'
            elif config_profile['Auto Encode']['codec'] == "Opus":
                VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '._new_.opus'
            elif config_profile['Auto Encode']['codec'] == 'MP3':
                VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '._new_.mp3'
            elif config_profile['Auto Encode']['codec'] == "FDK-AAC" or \
                    config_profile['Auto Encode']['codec'] == "QAAC" or \
                    config_profile['Auto Encode']['codec'] == "ALAC":
                VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '._new_.m4a'
            elif config_profile['Auto Encode']['codec'] == "FLAC":
                VideoOut = str(pathlib.Path(VideoInput).with_suffix('')) + '._new_.flac'
            output_entry.configure(state=NORMAL)  # Enable output_entry
            output_entry.delete(0, END)  # Clear contents of output entry
            output_entry.insert(0, VideoOut)  # Insert VideoOut information
            output_entry.configure(state=DISABLED)  # Disable output entry
            autosavefilename = pathlib.Path(VideoOut).name  # Set autosavefilename var
    elif total_audio_streams_in_input is None:  # If input has 0 audio tracks
        input_entry.config(state=DISABLED)  # Disable input entry-box
        messagebox.showinfo(title="No Audio Streams", message=f"{VideoInputQuoted}:\n\nDoes not "
                                                              f"contain any audio streams!")  # Display error msg


input_dnd = StringVar()
input_dnd.trace('w', update_file_input)

# Input Button/Entry Box ----------------------------------------------------------------------
input_button = HoverButton(root, text="Open File", command=input_button_commands, foreground="white",
                           background="#23272A", borderwidth="3", activebackground='grey')
input_button.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)
input_button.drop_target_register(DND_FILES)
input_button.dnd_bind('<<Drop>>', drop_input)

input_entry = Entry(root, width=35, borderwidth=4, background="#CACACA", state=DISABLED)
input_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=S + E + W)
input_entry.drop_target_register(DND_FILES)
input_entry.dnd_bind('<<Drop>>', drop_input)

# ------------------------------------------------------------------------- Input Button/Entry Box

# Output Button/Entry Box ------------------------------------------------------------------------
output_button = HoverButton(root, text="Save File", command=file_save, state=DISABLED, foreground="white",
                            background="#23272A", borderwidth="3", activebackground='grey')
output_button.grid(row=2, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)
output_entry = Entry(root, width=35, borderwidth=4, background="#CACACA", state=DISABLED)
output_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky=S + E + W)
# ---------------------------------------------------------------------- # Output Button/Entry Box

# Print Final Command Line ---------------------------------------------------------------------
command_line_button = HoverButton(root, text="Display\nCommand", command=print_command_line, state=DISABLED,
                                  foreground="white", background="#23272A", borderwidth="3", activebackground='grey')
command_line_button.grid(row=1, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)


# ----------------------------------------------------------------------- Print Final Command Line

# Start Audio Job: Manual -----------------------------------------------------------------------
def start_audio_job_manual():
    global auto_or_manual
    auto_or_manual = 'manual'
    threading.Thread(target=startaudiojob).start()


start_audio_button = HoverButton(root, text="Start Audio Job",
                                 command=start_audio_job_manual, state=DISABLED, foreground="white",
                                 background="#23272A", borderwidth="3", activebackground='grey')
start_audio_button.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky=N + S + E + W)


# --------------------------------------------------------------------------- Start Audio Job: Manual

# Start Audio Job: Auto -----------------------------------------------------------------------------
def encode_last_used_setting():
    global auto_or_manual, audio_window, acodec_stream_track_counter, gotosavefile, track_counter, acodec_stream
    auto_or_manual = 'auto'
    track_counter()
    encoder.set(config_profile['Auto Encode']['codec'])
    openaudiowindow()
    gotosavefile()
    command_line_button.config(state=DISABLED)
    output_button.config(state=DISABLED)
    if acodec_stream.get() != 'None':
        threading.Thread(target=startaudiojob).start()


auto_encode_last_options = HoverButton(root, text="Auto Encode:\nLast Used Options", command=encode_last_used_setting,
                                       foreground="white", background="#23272A", borderwidth="3", state=DISABLED,
                                       activebackground='grey')
auto_encode_last_options.grid(row=3, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)


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
    except (Exception,):
        pass

    show_auto_command_window = Toplevel(root)  # auto command window (shows auto encoding command)
    show_auto_command_window.title("Auto Encode Command")
    show_auto_command_window.configure(background="#434547")
    text_area = scrolledtextwidget.ScrolledText(show_auto_command_window, width=60, height=7, tabs=10, spacing2=3,
                                                spacing1=2, spacing3=3)
    text_area.grid(column=0, pady=10, padx=10)
    text_area.configure(state=NORMAL, bg='black', fg='#CFD2D1', bd=8)
    text_area.insert(INSERT, config_profile['Auto Encode']['command'])
    text_area.see(END)
    text_area.configure(state=DISABLED)
    show_auto_command_window.grid_columnconfigure(0, weight=1)


auto_encode_button_menu = Menu(root, tearoff=False)  # This is the right click menu for the auto_encode_button
auto_encode_button_menu.add_command(label='Show Command', command=show_auto_encode_command)
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
                except (Exception,):
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
        except (Exception,):
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
        except (Exception,):
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
        except (Exception,):
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
        except (Exception,):
            pass
    # check_mediainfogui ----------------------------------------------------------


if not pathlib.Path(config['ffmpeg_path']['path'].replace('"', '')).is_file():
    check_ffmpeg()
if not pathlib.Path(config['mediainfocli_path']['path'].replace('"', '')).is_file():
    check_mediainfocli()
if not pathlib.Path(config['mpv_player_path']['path'].replace('"', '')).is_file():
    check_mpv_player()
if not pathlib.Path(config['mediainfogui_path']['path'].replace('"', '')).is_file():
    check_mediainfogui()
if not pathlib.Path(fdkaac.replace('"', '')).is_file():
    messagebox.showerror(title='Error', message='Program is missing FDKAAC, please redownload or replace '
                                                'fdkaac.exe in the "Apps" folder')
if not pathlib.Path(qaac.replace('"', '')).is_file():
    messagebox.showerror(title='Error', message='Program is missing QAAC, please redownload or replace '
                                                'fdkaac.exe in the "Apps" folder')
# Checks for bundled app paths path -----------------------------------

# End Loop ------------------------------------------------------------------------------------------------------------
root.mainloop()
