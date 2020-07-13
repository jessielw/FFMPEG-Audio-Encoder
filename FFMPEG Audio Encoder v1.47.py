# Imports--------------------------------------------------------------------
from tkinter import *
from tkinter import filedialog, StringVar
import subprocess
import ctypes
import tkinter as tk
import pathlib
import tkinter.scrolledtext as scrolledtextwidget

# Main Gui & Windows --------------------------------------------------------

if __name__ == "__main__":
    if 'win' in sys.platform:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

root = Tk()
root.title("FFMPEG Audio Encoder v1.47")
root.iconphoto(True, PhotoImage(file="Runtime/topbar.png"))
root.configure(background="#434547")
window_height = 190
window_width = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

root.grid_columnconfigure(0,weight=1)
root.grid_columnconfigure(1,weight=1)
root.grid_columnconfigure(2,weight=1)
root.grid_columnconfigure(3,weight=1)
root.grid_rowconfigure(0,weight=1)
root.grid_rowconfigure(1,weight=1)
root.grid_rowconfigure(2,weight=1)
root.grid_rowconfigure(3,weight=1)

# Menu Bar Settings ---------------------------------------------------------

my_menu_bar = Menu(root, tearoff=0)
root.config(menu=my_menu_bar)

# Bundled Apps ---------------------------------------------------------------

ffmpeg = '"' + 'Apps/FFMPEG/ffmpeg.exe' + '"'
mediainfo = "Apps/MediaInfo/MediaInfo.exe"
mediainfocli = '"' + "Apps/MediaInfoCLI/MediaInfo.exe" + '"'
fdkaac = '"' + 'Apps/fdkaac/fdkaac.exe' + '"'

# About Window ---------------------------------------------------------------

def openaboutwindow():
    about_window = Toplevel()
    about_window.title('About')
    about_window.configure(background="#434547")
    window_height = 110
    window_width = 370
    screen_width = about_window.winfo_screenwidth()
    screen_height = about_window.winfo_screenheight()
    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))
    about_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    about_window_text = Text(about_window, background="#434547", foreground="white", relief=SUNKEN)
    about_window_text.pack()
    about_window_text.configure(state=NORMAL)
    about_window_text.insert(INSERT, "FFMPEG Audio Encoder v1.47 \n")
    about_window_text.insert(INSERT, "\n")
    about_window_text.insert(INSERT, "Development: jlw4049 \n")
    about_window_text.insert(INSERT, "\n")
    about_window_text.insert(INSERT, "A lightweight audio encoder based off of FFMPEG. \n")
    about_window_text.configure(state=DISABLED)


# Menu Items and Sub-Bars ----------------------------------------------------

file_menu = Menu(my_menu_bar, tearoff=0, activebackground="dim grey")
my_menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=root.quit)

# def shell_selection(*args):
#     print(shell_options.get())
shell_options = StringVar()
shell_options.set("Default")
options_menu = Menu(my_menu_bar, tearoff=0, activebackground="dim grey")
my_menu_bar.add_cascade(label="Options", menu=options_menu)
options_submenu = Menu(root, tearoff=0, activebackground="dim grey")
options_menu.add_cascade(label="Shell Options", menu=options_submenu)
options_submenu.add_radiobutton(label="Shell Closes Automatically", variable=shell_options, value="Default")
options_submenu.add_radiobutton(label="Shell Stays Open (Debug)", variable=shell_options, value="Debug")
# shell_options.trace('w', shell_selection)

help_menu = Menu(my_menu_bar, tearoff=0, activebackground="dim grey")
my_menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=openaboutwindow) # Possibly Expand This Later

def encoder_changed(*args): #File Auto Save Feature
    global VideoOutput
    start_audio_button.config(state=DISABLED)
    if encoder.get() == 'AAC':
        filename = pathlib.PureWindowsPath(VideoInput)
        VideoOut = filename.with_suffix('.NEW.mp4')
        VideoOutput = str(VideoOut)
        output_entry.configure(state=NORMAL)
        output_entry.delete(0, END)
        output_entry.insert(0, VideoOut)
        output_entry.configure(state=DISABLED)
        audiosettings_button.configure(state=NORMAL)
        command_line_button.config(state=DISABLED)

    elif encoder.get() == 'AC3':
        filename = pathlib.PureWindowsPath(VideoInput)
        VideoOut = filename.with_suffix('.NEW.ac3')
        VideoOutput = str(VideoOut)
        output_entry.configure(state=NORMAL)
        output_entry.delete(0, END)
        output_entry.insert(0, VideoOut)
        output_entry.configure(state=DISABLED)
        audiosettings_button.configure(state=NORMAL)
        command_line_button.config(state=DISABLED)

    elif encoder.get() == "DTS":
        filename = pathlib.PureWindowsPath(VideoInput)
        VideoOut = filename.with_suffix('.NEW.dts')
        VideoOutput = str(VideoOut)
        output_entry.configure(state=NORMAL)
        output_entry.delete(0, END)
        output_entry.insert(0, VideoOut)
        output_entry.configure(state=DISABLED)
        audiosettings_button.configure(state=NORMAL)
        command_line_button.config(state=DISABLED)

    elif encoder.get() == "Opus":
        filename = pathlib.PureWindowsPath(VideoInput)
        VideoOut = filename.with_suffix('.NEW.opus')
        VideoOutput = str(VideoOut)
        output_entry.configure(state=NORMAL)
        output_entry.delete(0, END)
        output_entry.insert(0, VideoOut)
        output_entry.configure(state=DISABLED)
        audiosettings_button.configure(state=NORMAL)
        command_line_button.config(state=DISABLED)

    elif encoder.get() == 'MP3':
        filename = pathlib.PureWindowsPath(VideoInput)
        VideoOut = filename.with_suffix('.NEW.mp3')
        VideoOutput = str(VideoOut)
        output_entry.configure(state=NORMAL)
        output_entry.delete(0, END)
        output_entry.insert(0, VideoOut)
        output_entry.configure(state=DISABLED)
        audiosettings_button.configure(state=NORMAL)
        command_line_button.config(state=DISABLED)

    elif encoder.get() == 'E-AC3':
        filename = pathlib.PureWindowsPath(VideoInput)
        VideoOut = filename.with_suffix('.NEW.ac3')
        VideoOutput = str(VideoOut)
        output_entry.configure(state=NORMAL)
        output_entry.delete(0, END)
        output_entry.insert(0, VideoOut)
        output_entry.configure(state=DISABLED)
        audiosettings_button.configure(state=NORMAL)
        command_line_button.config(state=DISABLED)

    elif encoder.get() == "FDK-AAC":
        filename = pathlib.PureWindowsPath(VideoInput)
        VideoOut = filename.with_suffix('.NEW.m4a')
        VideoOutput = str(VideoOut)
        output_entry.configure(state=NORMAL)
        output_entry.delete(0, END)
        output_entry.insert(0, VideoOut)
        output_entry.configure(state=DISABLED)
        audiosettings_button.configure(state=NORMAL)
        command_line_button.config(state=DISABLED)


def track_count(*args):
    global acodec_stream_track_counter
    if str.split(track_count)[-1] == '1': # 1 Track
        acodec_stream_track_counter = {'Track 1': " -map 0:a:0 "}
    if str.split(track_count)[-1] == '2': # 2 Tracks
        acodec_stream_track_counter = {'Track 1': " -map 0:a:0 ",
                                       'Track 2': " -map 0:a:1 "}
    if str.split(track_count)[-1] == '3': # 3 Tracks
        acodec_stream_track_counter = {'Track 1': " -map 0:a:0 ",
                                     'Track 2': " -map 0:a:1 ",
                                     'Track 3': " -map 0:a:2 "}
    if str.split(track_count)[-1] == '4': # 4 Tracks
        acodec_stream_track_counter = {'Track 1': " -map 0:a:0 ",
                                     'Track 2': " -map 0:a:1 ",
                                     'Track 3': " -map 0:a:2 ",
                                     'Track 4': " -map 0:a:3 "}
    if str.split(track_count)[-1] == '5': # 5 Tracks
        acodec_stream_track_counter = {'Track 1': " -map 0:a:0 ",
                                     'Track 2': " -map 0:a:1 ",
                                     'Track 3': " -map 0:a:2 ",
                                     'Track 4': " -map 0:a:3 ",
                                     'Track 5': " -map 0:a:4 "}
    if str.split(track_count)[-1] == '6': # 6 Tracks
        acodec_stream_track_counter = {'Track 1': " -map 0:a:0 ",
                                     'Track 2': " -map 0:a:1 ",
                                     'Track 3': " -map 0:a:2 ",
                                     'Track 4': " -map 0:a:3 ",
                                     'Track 5': " -map 0:a:4 ",
                                     'Track 6': " -map 0:a:5 "}
    if str.split(track_count)[-1] == '7': # 7 Tracks
        acodec_stream_track_counter = {'Track 1': " -map 0:a:0 ",
                                     'Track 2': " -map 0:a:1 ",
                                     'Track 3': " -map 0:a:2 ",
                                     'Track 4': " -map 0:a:3 ",
                                     'Track 5': " -map 0:a:4 ",
                                     'Track 6': " -map 0:a:5 ",
                                     'Track 7': " -map 0:a:6 "}
    if str.split(track_count)[-1] == '8': # 8 Tracks
        acodec_stream_track_counter = {'Track 1': " -map 0:a:0 ",
                                     'Track 2': " -map 0:a:1 ",
                                     'Track 3': " -map 0:a:2 ",
                                     'Track 4': " -map 0:a:3 ",
                                     'Track 5': " -map 0:a:4 ",
                                     'Track 6': " -map 0:a:5 ",
                                     'Track 7': " -map 0:a:6 ",
                                     'Track 8': " -map 0:a:7 "}
    if str.split(track_count)[-1] == '9': # 9 Tracks
        acodec_stream_track_counter = {'Track 1': " -map 0:a:0",
                                     'Track 2': " -map 0:a:1 ",
                                     'Track 3': " -map 0:a:2 ",
                                     'Track 4': " -map 0:a:3 ",
                                     'Track 5': " -map 0:a:4 ",
                                     'Track 6': " -map 0:a:5 ",
                                     'Track 7': " -map 0:a:6 ",
                                     'Track 8': " -map 0:a:7 ",
                                     'Track 9': " -map 0:a:8 "}
    if str.split(track_count)[-1] == '10': # 10 Tracks
        acodec_stream_track_counter = {'Track 1': " -map 0:a:0 ",
                                     'Track 2': " -map 0:a:1 ",
                                     'Track 3': " -map 0:a:2 ",
                                     'Track 4': " -map 0:a:3 ",
                                     'Track 5': " -map 0:a:4 ",
                                     'Track 6': " -map 0:a:5 ",
                                     'Track 7': " -map 0:a:6 ",
                                     'Track 8': " -map 0:a:7 ",
                                     'Track 9': " -map 0:a:8 ",
                                     'Track 10': " -map 0:a:9 "}
    if str.split(track_count)[-1] == '11': # 11 Tracks
        acodec_stream_track_counter = {'Track 1': " -map 0:a:0 ",
                                     'Track 2': " -map 0:a:1 ",
                                     'Track 3': " -map 0:a:2 ",
                                     'Track 4': " -map 0:a:3 ",
                                     'Track 5': " -map 0:a:4 ",
                                     'Track 6': " -map 0:a:5 ",
                                     'Track 7': " -map 0:a:6 ",
                                     'Track 8': " -map 0:a:7 ",
                                     'Track 9': " -map 0:a:8 ",
                                     'Track 10': " -map 0:a:9 ",
                                     'Track 11': " -map 0:a:10 "}
    if str.split(track_count)[-1] == '12': # 12 Tracks
        acodec_stream_track_counter = {'Track 1': " -map 0:a:0 ",
                                     'Track 2': " -map 0:a:1 ",
                                     'Track 3': " -map 0:a:2 ",
                                     'Track 4': " -map 0:a:3 ",
                                     'Track 5': " -map 0:a:4 ",
                                     'Track 6': " -map 0:a:5 ",
                                     'Track 7': " -map 0:a:6 ",
                                     'Track 8': " -map 0:a:7 ",
                                     'Track 9': " -map 0:a:8 ",
                                     'Track 10': " -map 0:a:9 ",
                                     'Track 11': " -map 0:a:10 ",
                                     'Track 12': " -map 0:a:11 "}
    if str.split(track_count)[-1] == '13': # 13 Tracks
        acodec_stream_track_counter = {'Track 1': " -map 0:a:0 ",
                                     'Track 2': " -map 0:a:1 ",
                                     'Track 3': " -map 0:a:2 ",
                                     'Track 4': " -map 0:a:3 ",
                                     'Track 5': " -map 0:a:4 ",
                                     'Track 6': " -map 0:a:5 ",
                                     'Track 7': " -map 0:a:6 ",
                                     'Track 8': " -map 0:a:7 ",
                                     'Track 9': " -map 0:a:8 ",
                                     'Track 10': " -map 0:a:9 ",
                                     'Track 11': " -map 0:a:10 ",
                                     'Track 12': " -map 0:a:11 ",
                                     'Track 13': " -map 0:a:12 "}
    if str.split(track_count)[-1] == '14': # 14 Tracks
        acodec_stream_track_counter = {'Track 1': " -map 0:a:0 ",
                                     'Track 2': " -map 0:a:1 ",
                                     'Track 3': " -map 0:a:2 ",
                                     'Track 4': " -map 0:a:3 ",
                                     'Track 5': " -map 0:a:4 ",
                                     'Track 6': " -map 0:a:5 ",
                                     'Track 7': " -map 0:a:6 ",
                                     'Track 8': " -map 0:a:7 ",
                                     'Track 9': " -map 0:a:8 ",
                                     'Track 10': " -map 0:a:9 ",
                                     'Track 11': " -map 0:a:10 ",
                                     'Track 12': " -map 0:a:11 ",
                                     'Track 13': " -map 0:a:12 ",
                                     'Track 14': " -map 0:a:13 "}
    if str.split(track_count)[-1] == '15': # 15 Tracks
        acodec_stream_track_counter = {'Track 1': " -map 0:a:0 ",
                                     'Track 2': " -map 0:a:1 ",
                                     'Track 3': " -map 0:a:2 ",
                                     'Track 4': " -map 0:a:3 ",
                                     'Track 5': " -map 0:a:4 ",
                                     'Track 6': " -map 0:a:5 ",
                                     'Track 7': " -map 0:a:6 ",
                                     'Track 8': " -map 0:a:7 ",
                                     'Track 9': " -map 0:a:8 ",
                                     'Track 10': " -map 0:a:9 ",
                                     'Track 11': " -map 0:a:10 ",
                                     'Track 12': " -map 0:a:11 ",
                                     'Track 13': " -map 0:a:12 ",
                                     'Track 14': " -map 0:a:13 ",
                                     'Track 15': " -map 0:a:14 "}
    if str.split(track_count)[-1] == '16':  # 16 Tracks
        acodec_stream_track_counter = {'Track 1': " -map 0:a:0 ",
                                     'Track 2': " -map 0:a:1 ",
                                     'Track 3': " -map 0:a:2 ",
                                     'Track 4': " -map 0:a:3 ",
                                     'Track 5': " -map 0:a:4 ",
                                     'Track 6': " -map 0:a:5 ",
                                     'Track 7': " -map 0:a:6 ",
                                     'Track 8': " -map 0:a:7 ",
                                     'Track 9': " -map 0:a:8 ",
                                     'Track 10': " -map 0:a:9 ",
                                     'Track 11': " -map 0:a:10 ",
                                     'Track 12': " -map 0:a:11 ",
                                     'Track 13': " -map 0:a:12 ",
                                     'Track 14': " -map 0:a:13 ",
                                     'Track 15': " -map 0:a:14 ",
                                     'Track 16': " -map 0:a:15 "}
    if str.split(track_count)[-1] == '17':  # 17 Tracks
        acodec_stream_track_counter = {'Track 1': " -map 0:a:0 ",
                                     'Track 2': " -map 0:a:1 ",
                                     'Track 3': " -map 0:a:2 ",
                                     'Track 4': " -map 0:a:3 ",
                                     'Track 5': " -map 0:a:4 ",
                                     'Track 6': " -map 0:a:5 ",
                                     'Track 7': " -map 0:a:6 ",
                                     'Track 8': " -map 0:a:7 ",
                                     'Track 9': " -map 0:a:8 ",
                                     'Track 10': " -map 0:a:9 ",
                                     'Track 11': " -map 0:a:10 ",
                                     'Track 12': " -map 0:a:11 ",
                                     'Track 13': " -map 0:a:12 ",
                                     'Track 14': " -map 0:a:13 ",
                                     'Track 15': " -map 0:a:14 ",
                                     'Track 16': " -map 0:a:15 ",
                                     'Track 17': " -map 0:a:16 "}
    if str.split(track_count)[-1] == '18':  # 18 Tracks
        acodec_stream_track_counter = {'Track 1': " -map 0:a:0 ",
                                     'Track 2': " -map 0:a:1 ",
                                     'Track 3': " -map 0:a:2 ",
                                     'Track 4': " -map 0:a:3 ",
                                     'Track 5': " -map 0:a:4 ",
                                     'Track 6': " -map 0:a:5 ",
                                     'Track 7': " -map 0:a:6 ",
                                     'Track 8': " -map 0:a:7 ",
                                     'Track 9': " -map 0:a:8 ",
                                     'Track 10': " -map 0:a:9 ",
                                     'Track 11': " -map 0:a:10 ",
                                     'Track 12': " -map 0:a:11 ",
                                     'Track 13': " -map 0:a:12 ",
                                     'Track 14': " -map 0:a:13 ",
                                     'Track 15': " -map 0:a:14 ",
                                     'Track 16': " -map 0:a:15 ",
                                     'Track 17': " -map 0:a:16 ",
                                     'Track 18': " -map 0:a:17 "}
    if str.split(track_count)[-1] == '19':  # 19 Tracks
        acodec_stream_track_counter = {'Track 1': " -map 0:a:0 ",
                                     'Track 2': " -map 0:a:1 ",
                                     'Track 3': " -map 0:a:2 ",
                                     'Track 4': " -map 0:a:3 ",
                                     'Track 5': " -map 0:a:4 ",
                                     'Track 6': " -map 0:a:5 ",
                                     'Track 7': " -map 0:a:6 ",
                                     'Track 8': " -map 0:a:7 ",
                                     'Track 9': " -map 0:a:8 ",
                                     'Track 10': " -map 0:a:9 ",
                                     'Track 11': " -map 0:a:10 ",
                                     'Track 12': " -map 0:a:11 ",
                                     'Track 13': " -map 0:a:12 ",
                                     'Track 14': " -map 0:a:13 ",
                                     'Track 15': " -map 0:a:14 ",
                                     'Track 16': " -map 0:a:15 ",
                                     'Track 17': " -map 0:a:16 ",
                                     'Track 18': " -map 0:a:17 ",
                                     'Track 19': " -map 0:a:18 "}
    if str.split(track_count)[-1] == '20':  # 20 Tracks
        acodec_stream_track_counter = {'Track 1': " -map 0:a:0 ",
                                     'Track 2': " -map 0:a:1 ",
                                     'Track 3': " -map 0:a:2 ",
                                     'Track 4': " -map 0:a:3 ",
                                     'Track 5': " -map 0:a:4 ",
                                     'Track 6': " -map 0:a:5 ",
                                     'Track 7': " -map 0:a:6 ",
                                     'Track 8': " -map 0:a:7 ",
                                     'Track 9': " -map 0:a:8 ",
                                     'Track 10': " -map 0:a:9 ",
                                     'Track 11': " -map 0:a:10 ",
                                     'Track 12': " -map 0:a:11 ",
                                     'Track 13': " -map 0:a:12 ",
                                     'Track 14': " -map 0:a:13 ",
                                     'Track 15': " -map 0:a:14 ",
                                     'Track 16': " -map 0:a:15 ",
                                     'Track 17': " -map 0:a:16 ",
                                     'Track 18': " -map 0:a:17 ",
                                     'Track 19': " -map 0:a:18 ",
                                     'Track 20': " -map 0:a:19 "}
    if str.split(track_count)[-1] == '21':  # 21 Tracks
        acodec_stream_track_counter = {'Track 1': " -map 0:a:0 ",
                                       'Track 2': " -map 0:a:1 ",
                                       'Track 3': " -map 0:a:2 ",
                                       'Track 4': " -map 0:a:3 ",
                                       'Track 5': " -map 0:a:4 ",
                                       'Track 6': " -map 0:a:5 ",
                                       'Track 7': " -map 0:a:6 ",
                                       'Track 8': " -map 0:a:7 ",
                                       'Track 9': " -map 0:a:8 ",
                                       'Track 10': " -map 0:a:9 ",
                                       'Track 11': " -map 0:a:10 ",
                                       'Track 12': " -map 0:a:11 ",
                                       'Track 13': " -map 0:a:12 ",
                                       'Track 14': " -map 0:a:13 ",
                                       'Track 15': " -map 0:a:14 ",
                                       'Track 16': " -map 0:a:15 ",
                                       'Track 17': " -map 0:a:16 ",
                                       'Track 18': " -map 0:a:17 ",
                                       'Track 19': " -map 0:a:18 ",
                                       'Track 20': " -map 0:a:19 ",
                                       'Track 21': " -map 0:a:20 "}
    if str.split(track_count)[-1] == '22':  # 22 Tracks
        acodec_stream_track_counter = {'Track 1': " -map 0:a:0 ",
                                       'Track 2': " -map 0:a:1 ",
                                       'Track 3': " -map 0:a:2 ",
                                       'Track 4': " -map 0:a:3 ",
                                       'Track 5': " -map 0:a:4 ",
                                       'Track 6': " -map 0:a:5 ",
                                       'Track 7': " -map 0:a:6 ",
                                       'Track 8': " -map 0:a:7 ",
                                       'Track 9': " -map 0:a:8 ",
                                       'Track 10': " -map 0:a:9 ",
                                       'Track 11': " -map 0:a:10 ",
                                       'Track 12': " -map 0:a:11 ",
                                       'Track 13': " -map 0:a:12 ",
                                       'Track 14': " -map 0:a:13 ",
                                       'Track 15': " -map 0:a:14 ",
                                       'Track 16': " -map 0:a:15 ",
                                       'Track 17': " -map 0:a:16 ",
                                       'Track 18': " -map 0:a:17 ",
                                       'Track 19': " -map 0:a:18 ",
                                       'Track 20': " -map 0:a:19 ",
                                       'Track 21': " -map 0:a:20 ",
                                       'Track 22': " -map 0:a:21 "}
    if str.split(track_count)[-1] == '23':  # 23 Tracks
        acodec_stream_track_counter = {'Track 1': " -map 0:a:0 ",
                                       'Track 2': " -map 0:a:1 ",
                                       'Track 3': " -map 0:a:2 ",
                                       'Track 4': " -map 0:a:3 ",
                                       'Track 5': " -map 0:a:4 ",
                                       'Track 6': " -map 0:a:5 ",
                                       'Track 7': " -map 0:a:6 ",
                                       'Track 8': " -map 0:a:7 ",
                                       'Track 9': " -map 0:a:8 ",
                                       'Track 10': " -map 0:a:9 ",
                                       'Track 11': " -map 0:a:10 ",
                                       'Track 12': " -map 0:a:11 ",
                                       'Track 13': " -map 0:a:12 ",
                                       'Track 14': " -map 0:a:13 ",
                                       'Track 15': " -map 0:a:14 ",
                                       'Track 16': " -map 0:a:15 ",
                                       'Track 17': " -map 0:a:16 ",
                                       'Track 18': " -map 0:a:17 ",
                                       'Track 19': " -map 0:a:18 ",
                                       'Track 20': " -map 0:a:19 ",
                                       'Track 21': " -map 0:a:20 ",
                                       'Track 22': " -map 0:a:21 ",
                                       'Track 23': " -map 0:a:22 "}
    if str.split(track_count)[-1] == '24':  # 24 Tracks
        acodec_stream_track_counter = {'Track 1': " -map 0:a:0 ",
                                       'Track 2': " -map 0:a:1 ",
                                       'Track 3': " -map 0:a:2 ",
                                       'Track 4': " -map 0:a:3 ",
                                       'Track 5': " -map 0:a:4 ",
                                       'Track 6': " -map 0:a:5 ",
                                       'Track 7': " -map 0:a:6 ",
                                       'Track 8': " -map 0:a:7 ",
                                       'Track 9': " -map 0:a:8 ",
                                       'Track 10': " -map 0:a:9 ",
                                       'Track 11': " -map 0:a:10 ",
                                       'Track 12': " -map 0:a:11 ",
                                       'Track 13': " -map 0:a:12 ",
                                       'Track 14': " -map 0:a:13 ",
                                       'Track 15': " -map 0:a:14 ",
                                       'Track 16': " -map 0:a:15 ",
                                       'Track 17': " -map 0:a:16 ",
                                       'Track 18': " -map 0:a:17 ",
                                       'Track 19': " -map 0:a:18 ",
                                       'Track 20': " -map 0:a:19 ",
                                       'Track 21': " -map 0:a:20 ",
                                       'Track 22': " -map 0:a:21 ",
                                       'Track 23': " -map 0:a:22 ",
                                       'Track 24': " -map 0:a:23 "}
    if str.split(track_count)[-1] == '25':  # 25 Tracks
        acodec_stream_track_counter = {'Track 1': " -map 0:a:0 ",
                                       'Track 2': " -map 0:a:1 ",
                                       'Track 3': " -map 0:a:2 ",
                                       'Track 4': " -map 0:a:3 ",
                                       'Track 5': " -map 0:a:4 ",
                                       'Track 6': " -map 0:a:5 ",
                                       'Track 7': " -map 0:a:6 ",
                                       'Track 8': " -map 0:a:7 ",
                                       'Track 9': " -map 0:a:8 ",
                                       'Track 10': " -map 0:a:9 ",
                                       'Track 11': " -map 0:a:10 ",
                                       'Track 12': " -map 0:a:11 ",
                                       'Track 13': " -map 0:a:12 ",
                                       'Track 14': " -map 0:a:13 ",
                                       'Track 15': " -map 0:a:14 ",
                                       'Track 16': " -map 0:a:15 ",
                                       'Track 17': " -map 0:a:16 ",
                                       'Track 18': " -map 0:a:17 ",
                                       'Track 19': " -map 0:a:18 ",
                                       'Track 20': " -map 0:a:19 ",
                                       'Track 21': " -map 0:a:20 ",
                                       'Track 22': " -map 0:a:21 ",
                                       'Track 23': " -map 0:a:22 ",
                                       'Track 24': " -map 0:a:23 ",
                                       'Track 25': " -map 0:a:24 "}

# Encoder Codec Drop Down
encoder_dropdownmenu_choices = {
    "AAC": "-c:a aac ",
    "AC3": "-c:a ac3 ",
    "E-AC3": "-c:a eac3 ",
    "DTS": "-c:a dts ",
    "Opus": "-c:a libopus ",
    "MP3": "-c:a libmp3lame ",
    "FDK-AAC": fdkaac}
encoder = StringVar(root)
encoder.set("Set Codec")
encoder.trace('w', encoder_changed)
encoder_menu = OptionMenu(root, encoder, *encoder_dropdownmenu_choices.keys(), command=track_count)
encoder_menu.grid(row=1, column=2, columnspan=1, padx=5, pady=5, sticky=N+S+W+E)
encoder_menu.config(state=DISABLED, background="#23272A", foreground="white", highlightthickness=1)
encoder_menu["menu"].configure(activebackground="dim grey")
codec_label = Label(root, text="Codec ->", background="#434547", foreground="White")
codec_label.grid(row=1, column=1, columnspan=1, padx=5, pady=5, sticky=N+S+W+E)

# Audio Codec Window ---------------------------------------------------------

def openaudiowindow():
    global acodec_bitrate
    global acodec_channel
    global acodec_channel_choices
    global acodec_bitrate_choices
    global acodec_stream
    global acodec_stream_choices
    global acodec_gain
    global acodec_gain_choices
    global dts_settings
    global dts_settings_choices
    global acodec_vbr_choices
    global acodec_vbr
    global acodec_samplerate
    global acodec_samplerate_choices

    def show_streams_mediainfo(): # Stream Viewer
        commands = '"' + mediainfocli + ' --Output="Audio;Track #:..............................%ID%\\nFormat:................................%Format%\\nDuration:..............................%Duration/String2%\\nBit Rate Mode:.....................%BitRate_Mode/String%\\nBitrate:.................................%BitRate/String%\\nSampling Rate:....................%SamplingRate/String%\\nAudio Channels:..................%Channel(s)%\\nChannel Layout:..................%ChannelLayout%\\nCompression Mode:............%Compression_Mode/String%\\nStream Size:........................%StreamSize/String5%\\nTitle:....................................%Title%\\nLanguage:...........................%Language/String%\\n\\n" ' + VideoInputQuoted + '"'
        run = subprocess.Popen('cmd /c ' + commands, creationflags=subprocess.CREATE_NO_WINDOW, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE, shell=True)
        stream_window = Toplevel(audio_window)
        stream_window.title("Audio Streams")
        stream_window.configure(background="#434547")
        Label(stream_window, text="---------- Audio Streams ----------", font = ("Times New Roman", 16), background='#434547', foreground="white").grid(column=0, row=0)
        text_area = scrolledtextwidget.ScrolledText(stream_window, width=50, height=25, tabs=10, spacing2=3, spacing1=2, spacing3=3)
        text_area.grid(column=0, pady=10, padx=10)
        text_area.insert(INSERT, run.communicate())
        text_area.configure(font=("Helvetica" ,12))
        text_area.configure(state=DISABLED)
        stream_window.grid_columnconfigure(0, weight=1)

    # AC3 Window ----------------------------
    if encoder.get() == "AC3":
        audio_window = Toplevel()
        audio_window.title('AC3 Settings')
        audio_window.configure(background="#434547")
        window_height = 150
        window_width = 370
        screen_width = audio_window.winfo_screenwidth()
        screen_height = audio_window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        my_menu = Menu(audio_window, tearoff=0)
        audio_window.config(menu=my_menu)
        check_streams = Menu(my_menu, tearoff=0, activebackground="dim grey")
        my_menu.add_command(label="View Streams", command=show_streams_mediainfo)

        audio_window.grid_columnconfigure(0, weight=1)
        audio_window.grid_columnconfigure(1, weight=1)
        audio_window.grid_columnconfigure(2, weight=1)
        audio_window.grid_rowconfigure(0, weight=1)
        audio_window.grid_rowconfigure(1, weight=1)
        audio_window.grid_rowconfigure(2, weight=1)
        audio_window.grid_rowconfigure(3, weight=1)

        def apply_button_hover(e):
            apply_button["bg"] = "grey"
        def apply_button_hover_leave(e):
            apply_button["bg"] = "#23272a"

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

        def acodec_gain_menu_hover(e):
            acodec_gain_menu["bg"] = "grey"
            acodec_gain_menu["activebackground"] = "grey"
        def acodec_gain_menu_hover_leave(e):
            acodec_gain_menu["bg"] = "#23272A"

        def acodec_samplerate_menu_hover(e):
            acodec_samplerate_menu["bg"] = "grey"
            acodec_samplerate_menu["activebackground"] = "grey"
        def acodec_samplerate_menu_hover_leave(e):
            acodec_samplerate_menu["bg"] = "#23272A"

        def gotosavefile():
            audio_window.destroy()
            output_button.config(state=NORMAL)
            start_audio_button.config(state=NORMAL)
            command_line_button.config(state=NORMAL)

        apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A", command=gotosavefile)
        apply_button.grid(row=3, column=2, columnspan=1, padx=10, pady=3, sticky=N+S+W+E)
        apply_button.bind("<Enter>", apply_button_hover)
        apply_button.bind("<Leave>", apply_button_hover_leave)

        # Audio Bitrate Selection
        acodec_bitrate = StringVar(audio_window)
        acodec_bitrate_choices = { '192k': "-b:a 192k ",
                                   '224k': "-b:a 224k ",
                                   '384k': "-b:a 384k ",
                                   '448k': "-b:a 448k ",
                                   '640k': "-b:a 640k "}
        acodec_bitrate.set('224k') # set the default option
        acodec_bitrate_menu_label = Label(audio_window, text="Bitrate :", background="#434547", foreground="white")
        acodec_bitrate_menu_label.grid(row=0, column=2, columnspan=1, padx=10, pady=3, sticky=W+E)
        acodec_bitrate_menu = OptionMenu(audio_window, acodec_bitrate, *acodec_bitrate_choices.keys())
        acodec_bitrate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_bitrate_menu.grid(row=1, column=2, columnspan=1, padx=10, pady=3, sticky=N+S+W+E)
        acodec_bitrate_menu["menu"].configure(activebackground="dim grey")
        acodec_bitrate_menu.bind("<Enter>", acodec_bitrate_menu_hover)
        acodec_bitrate_menu.bind("<Leave>", acodec_bitrate_menu_hover_leave)

        # Audio Stream Selection
        acodec_stream = StringVar(audio_window)
        acodec_stream_choices = acodec_stream_track_counter
        acodec_stream.set('Track 1') # set the default option
        acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
        acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W+E)
        acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
        acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N+S+W+E)
        acodec_stream_menu["menu"].configure(activebackground="dim grey")
        acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
        acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)

        # Audio Channel Selection
        acodec_channel = StringVar(audio_window)
        acodec_channel_choices = { 'Original': "",
                                   '1 (Mono)': "-ac 1 ",
                                   '2 (Stereo)': "-ac 2 ",
                                   '5.1 (Surround)': "-ac 6 ",
                                   '6.1 (Surround)': "-ac 7 ",
                                   '7.1 (Surround)': "-ac 8 "}
        acodec_channel.set('Original') # set the default option
        achannel_menu_label = Label(audio_window, text="Channels :", background="#434547", foreground="white")
        achannel_menu_label.grid(row=0, column=1, columnspan=1, padx=10, pady=3, sticky=W+E)
        achannel_menu = OptionMenu(audio_window, acodec_channel, *acodec_channel_choices.keys())
        achannel_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        achannel_menu.grid(row=1, column=1, columnspan=1, padx=10, pady=3, sticky=N+S+W+E)
        achannel_menu["menu"].configure(activebackground="dim grey")
        achannel_menu.bind("<Enter>", achannel_menu_hover)
        achannel_menu.bind("<Leave>", achannel_menu_hover_leave)

        # Audio Gain Selection
        acodec_gain = StringVar(audio_window)
        acodec_gain_choices = {'Default (0)': "-sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+10 dB': "-af volume=10dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+9 dB': "-af volume=9dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+8 dB': "-af volume=8dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+7 dB': "-af volume=7dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+6 dB': "-af volume=6dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+5 dB': "-af volume=5dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+4 dB': "-af volume=4dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+3 dB': "-af volume=3dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+2 dB': "-af volume=2dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+1 dB': "-af volume=1dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-1 dB': "-af volume=-1dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-2 dB': "-af volume=-2dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-3 dB': "-af volume=-3dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-4 dB': "-af volume=-4dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-5 dB': "-af volume=-5dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-6 dB': "-af volume=-6dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-7 dB': "-af volume=-7dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-8 dB': "-af volume=-8dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-9 dB': "-af volume=-9dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-10 dB': "-af volume=-10dB -sn -vn -map_chapters -1 -map_metadata -1 "}
        acodec_gain.set('Default (0)')  # set the default option
        acodec_gain_label = Label(audio_window, text="Gain :", background="#434547", foreground="white")
        acodec_gain_label.grid(row=2, column=0, columnspan=1, padx=10, pady=3, sticky=N+S+E+W)
        acodec_gain_menu = OptionMenu(audio_window, acodec_gain, *acodec_gain_choices.keys())
        acodec_gain_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_gain_menu.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N+S+E+W)
        acodec_gain_menu["menu"].configure(activebackground="dim grey")
        acodec_gain_menu.bind("<Enter>", acodec_gain_menu_hover)
        acodec_gain_menu.bind("<Leave>", acodec_gain_menu_hover_leave)

        # Audio Sample Rate Selection
        acodec_samplerate = StringVar(audio_window)
        acodec_samplerate_choices = {'Original': "",
                                     '44100 Hz': "-ar 44100 ",
                                     '48000 Hz': "-ar 48000 "}
        acodec_samplerate.set('Original')  # set the default option
        acodec_samplerate_label = Label(audio_window, text="Sample Rate :", background="#434547", foreground="white")
        acodec_samplerate_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3, sticky=N+S+E+W)
        acodec_samplerate_menu = OptionMenu(audio_window, acodec_samplerate, *acodec_samplerate_choices.keys())
        acodec_samplerate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_samplerate_menu.grid(row=3, column=1, columnspan=1, padx=10, pady=3, sticky=N+S+E+W)
        acodec_samplerate_menu["menu"].configure(activebackground="dim grey")
        acodec_samplerate_menu.bind("<Enter>", acodec_samplerate_menu_hover)
        acodec_samplerate_menu.bind("<Leave>", acodec_samplerate_menu_hover_leave)

    # AAC Window -----------------------
    elif encoder.get() == "AAC":
        audio_window = Toplevel()
        audio_window.title('AAC Settings')
        audio_window.configure(background="#434547")
        window_height = 150
        window_width = 385
        screen_width = audio_window.winfo_screenwidth()
        screen_height = audio_window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        my_menu = Menu(audio_window, tearoff=0)
        audio_window.config(menu=my_menu)
        check_streams = Menu(my_menu, tearoff=0, activebackground="dim grey")
        my_menu.add_command(label="View Streams", command=show_streams_mediainfo)

        audio_window.grid_columnconfigure(0, weight=1)
        audio_window.grid_columnconfigure(1, weight=1)
        audio_window.grid_columnconfigure(2, weight=1)
        audio_window.grid_rowconfigure(0, weight=1)
        audio_window.grid_rowconfigure(1, weight=1)
        audio_window.grid_rowconfigure(2, weight=1)
        audio_window.grid_rowconfigure(3, weight=1)

        def apply_button_hover(e):
            apply_button["bg"] = "grey"
        def apply_button_hover_leave(e):
            apply_button["bg"] = "#23272A"

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

        def acodec_gain_menu_hover(e):
            acodec_gain_menu["bg"] = "grey"
            acodec_gain_menu["activebackground"] = "grey"
        def acodec_gain_menu_hover_leave(e):
            acodec_gain_menu["bg"] = "#23272A"

        def acodec_samplerate_menu_hover(e):
            acodec_samplerate_menu["bg"] = "grey"
            acodec_samplerate_menu["activebackground"] = "grey"
        def acodec_samplerate_menu_hover_leave(e):
            acodec_samplerate_menu["bg"] = "#23272A"

        def gotosavefile():
            audio_window.destroy()
            output_button.config(state=NORMAL)
            start_audio_button.config(state=NORMAL)
            command_line_button.config(state=NORMAL)

        apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A", command=gotosavefile)
        apply_button.grid(row=3, column=2, columnspan=1, padx=10, pady=3, sticky=N+S+W+E)
        apply_button.bind("<Enter>", apply_button_hover)
        apply_button.bind("<Leave>", apply_button_hover_leave)

        # Audio Bitrate Menu
        acodec_bitrate = StringVar(audio_window)
        acodec_bitrate_choices = {'CBR: 16k': "-b:a 16k ",
                                  'CBR: 32k': "-b:a 32k ",
                                  'CBR: 64k': "-b:a 64k ",
                                  'CBR: 128k': "-b:a 128k ",
                                  'CBR: 192k': "-b:a 192k ",
                                  'CBR: 256k': "-b:a 256k ",
                                  'CBR: 320k': "-b:a 320k ",
                                  'CBR: 448k': "-b:a 448k ",
                                  'CBR: 640k': "-b:a 640k ",
                                  'VBR: 1': "-q:a 1 ",
                                  'VBR: 2': "-q:a 2 ",
                                  'VBR: 3': "-q:a 3 ",
                                  'VBR: 4': "-q:a 4 ",
                                  'VBR: 5': "-q:a 5 ",
                                  'VBR: 6': "-q:a 6 ",
                                  'VBR: 7': "-q:a 7 "}
        acodec_bitrate.set('CBR: 192k')  # set the default option
        acodec_bitrate_menu_label = Label(audio_window, text="Quality :", background="#434547", foreground="white")
        acodec_bitrate_menu_label.grid(row=0, column=2, columnspan=1, padx=10, pady=3, sticky=W+E)
        acodec_bitrate_menu = OptionMenu(audio_window, acodec_bitrate, *acodec_bitrate_choices.keys())
        acodec_bitrate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_bitrate_menu.grid(row=1, column=2, columnspan=1, padx=10, pady=3, sticky=N+S+W+E)
        acodec_bitrate_menu["menu"].configure(activebackground="dim grey")
        acodec_bitrate_menu.bind("<Enter>", acodec_bitrate_menu_hover)
        acodec_bitrate_menu.bind("<Leave>", acodec_bitrate_menu_hover_leave)

        # Audio Channel Selection
        acodec_channel = StringVar(audio_window)
        acodec_channel_choices = { 'Original': "",
                                   '1 (Mono)': "-ac 1 ",
                                   '2 (Stereo)': "-ac 2 ",
                                   '5.1 (Surround)': "-ac 6 ",
                                   '6.1 (Surround)': "-ac 7 ",
                                   '7.1 (Surround)': "-ac 8 "}
        acodec_channel.set('Original') # set the default option
        achannel_menu_label = Label(audio_window, text="Channels :", background="#434547", foreground="white")
        achannel_menu_label.grid(row=0, column=1, columnspan=1, padx=10, pady=3, sticky=W+E)
        achannel_menu = OptionMenu(audio_window, acodec_channel, *acodec_channel_choices.keys())
        achannel_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        achannel_menu.grid(row=1, column=1, columnspan=1, padx=10, pady=3, sticky=N+S+W+E)
        achannel_menu["menu"].configure(activebackground="dim grey")
        achannel_menu.bind("<Enter>", achannel_menu_hover)
        achannel_menu.bind("<Leave>", achannel_menu_hover_leave)

        # Audio Stream Selection
        acodec_stream = StringVar(audio_window)
        acodec_stream_choices = acodec_stream_track_counter
        acodec_stream.set('Track 1') # set the default option
        acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
        acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W+E)
        acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
        acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N+S+W+E)
        acodec_stream_menu["menu"].configure(activebackground="dim grey")
        acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
        acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)

        # Audio Gain Selection
        acodec_gain = StringVar(audio_window)
        acodec_gain_choices = {'Default (0)': "-sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+10 dB': "-af volume=10dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+9 dB': "-af volume=9dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+8 dB': "-af volume=8dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+7 dB': "-af volume=7dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+6 dB': "-af volume=6dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+5 dB': "-af volume=5dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+4 dB': "-af volume=4dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+3 dB': "-af volume=3dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+2 dB': "-af volume=2dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+1 dB': "-af volume=1dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-1 dB': "-af volume=-1dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-2 dB': "-af volume=-2dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-3 dB': "-af volume=-3dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-4 dB': "-af volume=-4dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-5 dB': "-af volume=-5dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-6 dB': "-af volume=-6dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-7 dB': "-af volume=-7dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-8 dB': "-af volume=-8dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-9 dB': "-af volume=-9dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-10 dB': "-af volume=-10dB -sn -vn -map_chapters -1 -map_metadata -1 "}
        acodec_gain.set('Default (0)')  # set the default option
        acodec_gain_label = Label(audio_window, text="Gain :", background="#434547", foreground="white")
        acodec_gain_label.grid(row=2, column=0, columnspan=1, padx=10, pady=3, sticky=N+S+E+W)
        acodec_gain_menu = OptionMenu(audio_window, acodec_gain, *acodec_gain_choices.keys())
        acodec_gain_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_gain_menu.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N+S+E+W)
        acodec_gain_menu["menu"].configure(activebackground="dim grey")
        acodec_gain_menu.bind("<Enter>", acodec_gain_menu_hover)
        acodec_gain_menu.bind("<Leave>", acodec_gain_menu_hover_leave)

        # Audio Sample Rate Selection
        acodec_samplerate = StringVar(audio_window)
        acodec_samplerate_choices = {'Original': "",
                                     '11025 Hz': "-ar 11025 ",
                                     '22050 Hz': "-ar 22050 ",
                                     '44100 Hz': "-ar 44100 ",
                                     '48000 Hz': "-ar 48000 ",
                                     '88200 Hz': "-ar 88200 ",
                                     '96000 Hz': "-ar 96000 "}
        acodec_samplerate.set('Original')  # set the default option
        acodec_samplerate_label = Label(audio_window, text="Sample Rate :", background="#434547", foreground="white")
        acodec_samplerate_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3, sticky=N+S+E+W)
        acodec_samplerate_menu = OptionMenu(audio_window, acodec_samplerate, *acodec_samplerate_choices.keys())
        acodec_samplerate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_samplerate_menu.grid(row=3, column=1, columnspan=1, padx=10, pady=3, sticky=N+S+E+W)
        acodec_samplerate_menu["menu"].configure(activebackground="dim grey")
        acodec_samplerate_menu.bind("<Enter>", acodec_samplerate_menu_hover)
        acodec_samplerate_menu.bind("<Leave>", acodec_samplerate_menu_hover_leave)

        # DTS Window ---------------------------------------------------------

    elif encoder.get() == "DTS":
        audio_window = Toplevel()
        audio_window.title('DTS Settings')
        audio_window.configure(background="#434547")
        window_height = 110
        window_width = 276
        screen_width = audio_window.winfo_screenwidth()
        screen_height = audio_window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        my_menu = Menu(audio_window, tearoff=0)
        audio_window.config(menu=my_menu)
        check_streams = Menu(my_menu, tearoff=0, activebackground="dim grey")
        my_menu.add_command(label="View Streams", command=show_streams_mediainfo)

        audio_window.grid_columnconfigure(0, weight=1)
        audio_window.grid_columnconfigure(1, weight=1)
        audio_window.grid_columnconfigure(2, weight=1)
        audio_window.grid_rowconfigure(0, weight=1)
        audio_window.grid_rowconfigure(1, weight=1)
        audio_window.grid_rowconfigure(2, weight=1)

        def apply_button_hover(e):
            apply_button["bg"] = "grey"
        def apply_button_hover_leave(e):
            apply_button["bg"] = "#23272A"

        def acodec_stream_menu_hover(e):
            acodec_stream_menu["bg"] = "grey"
            acodec_stream_menu["activebackground"] = "grey"
        def acodec_stream_menu_hover_leave(e):
            acodec_stream_menu["bg"] = "#23272A"


        def dts_settings_menu_hover(e):
            dts_settings_menu["bg"] = "grey"
            dts_settings_menu["activebackground"] = "grey"
        def dts_settings_menu_hover_leave(e):
            dts_settings_menu["bg"] = "#23272A"

        def gotosavefile():
            audio_window.destroy()
            output_button.config(state=NORMAL)
            start_audio_button.config(state=NORMAL)
            command_line_button.config(state=NORMAL)

        apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A", command=gotosavefile)
        apply_button.grid(row=2, column=2, columnspan=1, padx=10, pady=3, sticky=N+S+E)
        apply_button.bind("<Enter>", apply_button_hover)
        apply_button.bind("<Leave>", apply_button_hover_leave)

        # Audio Stream Selection
        acodec_stream = StringVar(audio_window)
        acodec_stream_choices = acodec_stream_track_counter
        acodec_stream.set('Track 1') # set the default option
        acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
        acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W+E)
        acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
        acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N+S+W+E)
        acodec_stream_menu["menu"].configure(activebackground="dim grey")
        acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
        acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)

        # DTS Setting(s)
        dts_settings = StringVar(audio_window)
        dts_settings_choices = {'Reduce to Core': "-bsf:a dca_core -c:a copy ",
                                  'Extract HD Track': "-c:a copy "}
        dts_settings.set('Reduce to Core')  # set the default option
        dts_settings_label = Label(audio_window, text="DTS Settings :", background="#434547", foreground="white")
        dts_settings_label.grid(row=0, column=2, columnspan=1, padx=10, pady=3)
        dts_settings_menu = OptionMenu(audio_window, dts_settings, *dts_settings_choices.keys())
        dts_settings_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        dts_settings_menu.grid(row=1, column=2, columnspan=1, padx=10, pady=3)
        dts_settings_menu.bind("<Enter>",  dts_settings_menu_hover)
        dts_settings_menu.bind("<Leave>",  dts_settings_menu_hover_leave)

    # Opus Window --------------------------------------------
    elif encoder.get() == "Opus":
        audio_window = Toplevel()
        audio_window.title('Opus Settings')
        audio_window.configure(background="#434547")
        window_height = 150
        window_width = 360
        screen_width = audio_window.winfo_screenwidth()
        screen_height = audio_window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        my_menu = Menu(audio_window, tearoff=0)
        audio_window.config(menu=my_menu)
        check_streams = Menu(my_menu, tearoff=0, activebackground="dim grey")
        my_menu.add_command(label="View Streams", command=show_streams_mediainfo)

        audio_window.grid_columnconfigure(0, weight=1)
        audio_window.grid_columnconfigure(1, weight=1)
        audio_window.grid_columnconfigure(2, weight=1)
        audio_window.grid_rowconfigure(0, weight=1)
        audio_window.grid_rowconfigure(1, weight=1)
        audio_window.grid_rowconfigure(2, weight=1)
        audio_window.grid_rowconfigure(3, weight=1)

        def apply_button_hover(e):
            apply_button["bg"] = "grey"
        def apply_button_hover_leave(e):
            apply_button["bg"] = "#23272A"

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

        def acodec_gain_menu_hover(e):
            acodec_gain_menu["bg"] = "grey"
            acodec_gain_menu["activebackground"] = "grey"
        def acodec_gain_menu_hover_leave(e):
            acodec_gain_menu["bg"] = "#23272A"

        def acodec_vbr_menu_hover(e):
            acodec_vbr_menu["bg"] = "grey"
            acodec_vbr_menu["activebackground"] = "grey"
        def acodec_vbr_menu_hover_leave(e):
            acodec_vbr_menu["bg"] = "#23272A"

        def gotosavefile():
            audio_window.destroy()
            output_button.config(state=NORMAL)
            start_audio_button.config(state=NORMAL)
            command_line_button.config(state=NORMAL)

        apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A", command=gotosavefile)
        apply_button.grid(row=3, column=2, columnspan=1, padx=10, pady=3, sticky=N+S+E+W)
        apply_button.bind("<Enter>", apply_button_hover)
        apply_button.bind("<Leave>", apply_button_hover_leave)

        # Audio Bitrate Menu
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
        acodec_bitrate.set('160k')  # set the default option
        acodec_bitrate_menu_label = Label(audio_window, text="Quality :", background="#434547", foreground="white")
        acodec_bitrate_menu_label.grid(row=0, column=2, columnspan=1, padx=10, pady=3, sticky=W+E)
        acodec_bitrate_menu = OptionMenu(audio_window, acodec_bitrate, *acodec_bitrate_choices.keys())
        acodec_bitrate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_bitrate_menu.grid(row=1, column=2, columnspan=1, padx=10, pady=3, sticky=N+S+W+E)
        acodec_bitrate_menu["menu"].configure(activebackground="dim grey")
        acodec_bitrate_menu.bind("<Enter>", acodec_bitrate_menu_hover)
        acodec_bitrate_menu.bind("<Leave>", acodec_bitrate_menu_hover_leave)

        # Audio VBR Toggle
        acodec_vbr = StringVar(audio_window)
        acodec_vbr_choices = {'VBR: On': "-vbr on ",
                              'VBR: Off': "-vbr off "}
        acodec_vbr.set('VBR: On')  # set the default option
        acodec_vbr_menu_label = Label(audio_window, text="VBR :", background="#434547", foreground="white")
        acodec_vbr_menu_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3)
        acodec_vbr_menu = OptionMenu(audio_window, acodec_vbr, *acodec_vbr_choices.keys())
        acodec_vbr_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_vbr_menu.grid(row=3, column=1, columnspan=1, padx=10, pady=3)
        acodec_vbr_menu["menu"].configure(activebackground="dim grey")
        acodec_vbr_menu.bind("<Enter>", acodec_vbr_menu_hover)
        acodec_vbr_menu.bind("<Leave>", acodec_vbr_menu_hover_leave)

        # Audio Channel Selection
        acodec_channel = StringVar(audio_window)
        acodec_channel_choices = { 'Original': "-ac 2 ",
                                   '1 (Mono)': "-ac 1 ",
                                   '2 (Stereo)': "-ac 2 ",
                                   '5.1 (Surround)': "-ac 6 ",
                                   '6.1 (Surround)': "-ac 7 ",
                                   '7.1 (Surround)': "-ac 8 "}
        acodec_channel.set('Original') # set the default option
        achannel_menu_label = Label(audio_window, text="Channels :", background="#434547", foreground="white")
        achannel_menu_label.grid(row=0, column=1, columnspan=1, padx=10, pady=3, sticky=W+E)
        achannel_menu = OptionMenu(audio_window, acodec_channel, *acodec_channel_choices.keys())
        achannel_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        achannel_menu.grid(row=1, column=1, columnspan=1, padx=10, pady=3, sticky=N+S+W+E)
        achannel_menu["menu"].configure(activebackground="dim grey")
        achannel_menu.bind("<Enter>", achannel_menu_hover)
        achannel_menu.bind("<Leave>", achannel_menu_hover_leave)

        # Audio Stream Selection
        acodec_stream = StringVar(audio_window)
        acodec_stream_choices = acodec_stream_track_counter
        acodec_stream.set('Track 1') # set the default option
        acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
        acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W+E)
        acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
        acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N+S+W+E)
        acodec_stream_menu["menu"].configure(activebackground="dim grey")
        acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
        acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)

        # Audio Gain Selection
        acodec_gain = StringVar(audio_window)
        acodec_gain_choices = {'Default (0)': "-sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+10 dB': "-af volume=10dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+9 dB': "-af volume=9dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+8 dB': "-af volume=8dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+7 dB': "-af volume=7dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+6 dB': "-af volume=6dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+5 dB': "-af volume=5dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+4 dB': "-af volume=4dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+3 dB': "-af volume=3dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+2 dB': "-af volume=2dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+1 dB': "-af volume=1dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-1 dB': "-af volume=-1dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-2 dB': "-af volume=-2dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-3 dB': "-af volume=-3dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-4 dB': "-af volume=-4dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-5 dB': "-af volume=-5dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-6 dB': "-af volume=-6dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-7 dB': "-af volume=-7dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-8 dB': "-af volume=-8dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-9 dB': "-af volume=-9dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-10 dB': "-af volume=-10dB -sn -vn -map_chapters -1 -map_metadata -1 "}
        acodec_gain.set('Default (0)')  # set the default option
        acodec_gain_label = Label(audio_window, text="Gain :", background="#434547", foreground="white")
        acodec_gain_label.grid(row=2, column=0, columnspan=1, padx=10, pady=3, sticky=N+S+E+W)
        acodec_gain_menu = OptionMenu(audio_window, acodec_gain, *acodec_gain_choices.keys())
        acodec_gain_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_gain_menu.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N+S+E+W)
        acodec_gain_menu["menu"].configure(activebackground="dim grey")
        acodec_gain_menu.bind("<Enter>", acodec_gain_menu_hover)
        acodec_gain_menu.bind("<Leave>", acodec_gain_menu_hover_leave)

        # MP3 Window -----------------------
    elif encoder.get() == "MP3":
        audio_window = Toplevel()
        audio_window.title('AAC Settings')
        audio_window.configure(background="#434547")
        window_height = 150
        window_width = 385
        screen_width = audio_window.winfo_screenwidth()
        screen_height = audio_window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        my_menu = Menu(audio_window, tearoff=0)
        audio_window.config(menu=my_menu)
        check_streams = Menu(my_menu, tearoff=0, activebackground="dim grey")
        my_menu.add_command(label="View Streams", command=show_streams_mediainfo)

        audio_window.grid_columnconfigure(0, weight=1)
        audio_window.grid_columnconfigure(1, weight=1)
        audio_window.grid_columnconfigure(2, weight=1)
        audio_window.grid_rowconfigure(0, weight=1)
        audio_window.grid_rowconfigure(1, weight=1)
        audio_window.grid_rowconfigure(2, weight=1)
        audio_window.grid_rowconfigure(3, weight=1)

        def apply_button_hover(e):
            apply_button["bg"] = "grey"
        def apply_button_hover_leave(e):
            apply_button["bg"] = "#23272A"

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

        def acodec_gain_menu_hover(e):
            acodec_gain_menu["bg"] = "grey"
            acodec_gain_menu["activebackground"] = "grey"
        def acodec_gain_menu_hover_leave(e):
            acodec_gain_menu["bg"] = "#23272A"

        def acodec_samplerate_menu_hover(e):
            acodec_samplerate_menu["bg"] = "grey"
            acodec_samplerate_menu["activebackground"] = "grey"
        def acodec_samplerate_menu_hover_leave(e):
            acodec_samplerate_menu["bg"] = "#23272A"

        def gotosavefile():
            audio_window.destroy()
            output_button.config(state=NORMAL)
            start_audio_button.config(state=NORMAL)
            command_line_button.config(state=NORMAL)

        apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A", command=gotosavefile)
        apply_button.grid(row=3, column=2, columnspan=1, padx=10, pady=3, sticky=N+S+E+W)
        apply_button.bind("<Enter>", apply_button_hover)
        apply_button.bind("<Leave>", apply_button_hover_leave)

        # Audio Bitrate Menu
        acodec_bitrate = StringVar(audio_window)
        acodec_bitrate_choices = {'CBR: 16k': '-b:a 16k ',
                                  'CBR: 32k': '-b:a 32k ',
                                  'CBR: 64k': '-b:a 64k ',
                                  'CBR: 128k': '-b:a 128k ',
                                  'CBR: 192k': '-b:a 192k ',
                                  'CBR: 256k': '-b:a 256k ',
                                  'CBR: 320k': '-b:a 320k ',
                                  'CBR: 448k': '-b:a 448k ',
                                  'VBR: 1': '-q:a 1 ',
                                  'VBR: 2': '-q:a 2 ',
                                  'VBR: 3': '-q:a 3 ',
                                  'VBR: 4': '-q:a 4 ',
                                  'VBR: 5': '-q:a 5 ',
                                  'VBR: 6': '-q:a 6 ',
                                  'VBR: 7': '-q:a 7 '}
        acodec_bitrate.set('CBR: 192k')  # set the default option
        acodec_bitrate_menu_label = Label(audio_window, text="Quality :", background="#434547", foreground="white")
        acodec_bitrate_menu_label.grid(row=0, column=2, columnspan=1, padx=10, pady=3, sticky=W+E)
        acodec_bitrate_menu = OptionMenu(audio_window, acodec_bitrate, *acodec_bitrate_choices.keys())
        acodec_bitrate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_bitrate_menu.grid(row=1, column=2, columnspan=1, padx=10, pady=3, sticky=N+S+W+E)
        acodec_bitrate_menu["menu"].configure(activebackground="dim grey")
        acodec_bitrate_menu.bind("<Enter>", acodec_bitrate_menu_hover)
        acodec_bitrate_menu.bind("<Leave>", acodec_bitrate_menu_hover_leave)

        # Audio Channel Selection
        acodec_channel = StringVar(audio_window)
        acodec_channel_choices = { 'Original': "",
                                   '1 (Mono)': "-ac 1 ",
                                   '2 (Stereo)': "-ac 2 ",
                                   '5.1 (Surround)': "-ac 6 ",
                                   '6.1 (Surround)': "-ac 7 ",
                                   '7.1 (Surround)': "-ac 8 "}
        acodec_channel.set('Original') # set the default option
        achannel_menu_label = Label(audio_window, text="Channels :", background="#434547", foreground="white")
        achannel_menu_label.grid(row=0, column=1, columnspan=1, padx=10, pady=3, sticky=W+E)
        achannel_menu = OptionMenu(audio_window, acodec_channel, *acodec_channel_choices.keys())
        achannel_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        achannel_menu.grid(row=1, column=1, columnspan=1, padx=10, pady=3, sticky=N+S+W+E)
        achannel_menu["menu"].configure(activebackground="dim grey")
        achannel_menu.bind("<Enter>", achannel_menu_hover)
        achannel_menu.bind("<Leave>", achannel_menu_hover_leave)

        # Audio Stream Selection
        acodec_stream = StringVar(audio_window)
        acodec_stream_choices = acodec_stream_track_counter
        acodec_stream.set('Track 1') # set the default option
        acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
        acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W+E)
        acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
        acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N+S+W+E)
        acodec_stream_menu["menu"].configure(activebackground="dim grey")
        acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
        acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)

        # Audio Gain Selection
        acodec_gain = StringVar(audio_window)
        acodec_gain_choices = {'Default (0)': "-sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+10 dB': "-af volume=10dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+9 dB': "-af volume=9dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+8 dB': "-af volume=8dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+7 dB': "-af volume=7dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+6 dB': "-af volume=6dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+5 dB': "-af volume=5dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+4 dB': "-af volume=4dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+3 dB': "-af volume=3dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+2 dB': "-af volume=2dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+1 dB': "-af volume=1dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-1 dB': "-af volume=-1dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-2 dB': "-af volume=-2dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-3 dB': "-af volume=-3dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-4 dB': "-af volume=-4dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-5 dB': "-af volume=-5dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-6 dB': "-af volume=-6dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-7 dB': "-af volume=-7dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-8 dB': "-af volume=-8dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-9 dB': "-af volume=-9dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-10 dB': "-af volume=-10dB -sn -vn -map_chapters -1 -map_metadata -1 "}
        acodec_gain.set('Default (0)')  # set the default option
        acodec_gain_label = Label(audio_window, text="Gain :", background="#434547", foreground="white")
        acodec_gain_label.grid(row=2, column=0, columnspan=1, padx=10, pady=3, sticky=N+S+E+W)
        acodec_gain_menu = OptionMenu(audio_window, acodec_gain, *acodec_gain_choices.keys())
        acodec_gain_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_gain_menu.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N+S+E+W)
        acodec_gain_menu["menu"].configure(activebackground="dim grey")
        acodec_gain_menu.bind("<Enter>", acodec_gain_menu_hover)
        acodec_gain_menu.bind("<Leave>", acodec_gain_menu_hover_leave)

        # Audio Sample Rate Selection
        acodec_samplerate = StringVar(audio_window)
        acodec_samplerate_choices = {'Original': "",
                                     '11025 Hz': "-ar 11025 ",
                                     '22050 Hz': "-ar 22050 ",
                                     '44100 Hz': "-ar 44100 ",
                                     '48000 Hz': "-ar 48000 "}
        acodec_samplerate.set('Original')  # set the default option
        acodec_samplerate_label = Label(audio_window, text="Sample Rate :", background="#434547", foreground="white")
        acodec_samplerate_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3, sticky=N+S+E+W)
        acodec_samplerate_menu = OptionMenu(audio_window, acodec_samplerate, *acodec_samplerate_choices.keys())
        acodec_samplerate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_samplerate_menu.grid(row=3, column=1, columnspan=1, padx=10, pady=3, sticky=N+S+E+W)
        acodec_samplerate_menu["menu"].configure(activebackground="dim grey")
        acodec_samplerate_menu.bind("<Enter>", acodec_samplerate_menu_hover)
        acodec_samplerate_menu.bind("<Leave>", acodec_samplerate_menu_hover_leave)

        # E-AC3 Window -----------------------
    elif encoder.get() == "E-AC3":
        audio_window = Toplevel()
        audio_window.title('E-AC3 Settings')
        audio_window.configure(background="#434547")
        window_height = 150
        window_width = 385
        screen_width = audio_window.winfo_screenwidth()
        screen_height = audio_window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        my_menu = Menu(audio_window, tearoff=0)
        audio_window.config(menu=my_menu)
        check_streams = Menu(my_menu, tearoff=0, activebackground="dim grey")
        my_menu.add_command(label="View Streams", command=show_streams_mediainfo)

        audio_window.grid_columnconfigure(0, weight=1)
        audio_window.grid_columnconfigure(1, weight=1)
        audio_window.grid_columnconfigure(2, weight=1)
        audio_window.grid_rowconfigure(0, weight=1)
        audio_window.grid_rowconfigure(1, weight=1)
        audio_window.grid_rowconfigure(2, weight=1)
        audio_window.grid_rowconfigure(3, weight=1)

        def apply_button_hover(e):
            apply_button["bg"] = "grey"
        def apply_button_hover_leave(e):
            apply_button["bg"] = "#23272A"

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

        def acodec_gain_menu_hover(e):
            acodec_gain_menu["bg"] = "grey"
            acodec_gain_menu["activebackground"] = "grey"
        def acodec_gain_menu_hover_leave(e):
            acodec_gain_menu["bg"] = "#23272A"

        def acodec_samplerate_menu_hover(e):
            acodec_samplerate_menu["bg"] = "grey"
            acodec_samplerate_menu["activebackground"] = "grey"
        def acodec_samplerate_menu_hover_leave(e):
            acodec_samplerate_menu["bg"] = "#23272A"

        def gotosavefile():
            audio_window.destroy()
            output_button.config(state=NORMAL)
            start_audio_button.config(state=NORMAL)
            command_line_button.config(state=NORMAL)

        apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A", command=gotosavefile)
        apply_button.grid(row=3, column=2, columnspan=1, padx=10, pady=3, sticky=N+S+E+W)
        apply_button.bind("<Enter>", apply_button_hover)
        apply_button.bind("<Leave>", apply_button_hover_leave)

        # Audio Bitrate Menu
        acodec_bitrate = StringVar(audio_window)
        acodec_bitrate_choices = {'CBR: 64k': '-b:a 64k ',
                                  'CBR: 96k': '-b:a 96k ',
                                  'CBR: 160k': '-b:a 160k ',
                                  'CBR: 128k': '-b:a 128k ',
                                  'CBR: 192k': '-b:a 192k ',
                                  'CBR: 224k': '-b:a 224k ',
                                  'CBR: 256k': '-b:a 256k ',
                                  'CBR: 288k': '-b:a 288k ',
                                  'CBR: 320k': '-b:a 320k ',
                                  'CBR: 352k': '-b:a 352k ',
                                  'CBR: 384k': '-b:a 384k ',
                                  'CBR: 416k': '-b:a 416k ',
                                  'CBR: 448k': '-b:a 448k ',
                                  'CBR: 480k': '-b:a 480k ',
                                  'CBR: 512k': '-b:a 512k ',
                                  'CBR: 544k': '-b:a 544k ',
                                  'CBR: 576k': '-b:a 576k ',
                                  'CBR: 608k': '-b:a 608k ',
                                  'CBR: 640k': '-b:a 640k ',
                                  'CBR: 672k': '-b:a 672k ',
                                  'CBR: 704k': '-b:a 704k ',
                                  'CBR: 736k': '-b:a 736k ',
                                  'CBR: 768k': '-b:a 768k ',
                                  'CBR: 800k': '-b:a 800k ',
                                  'CBR: 832k': '-b:a 832k ',
                                  'CBR: 864k': '-b:a 864k ',
                                  'CBR: 896k': '-b:a 896k ',
                                  'CBR: 928k': '-b:a 928k ',
                                  'CBR: 960k': '-b:a 960k ',
                                  'CBR: 1056k': '-b:a 1056k ',
                                  'CBR: 1088k': '-b:a 1088k ',
                                  'CBR: 1120k': '-b:a 1120k ',
                                  'CBR: 1152k': '-b:a 1152k ',
                                  'CBR: 1184k': '-b:a 1184k ',
                                  'CBR: 1216k': '-b:a 1216k ',
                                  'CBR: 1248k': '-b:a 1248k ',
                                  'CBR: 1280k': '-b:a 1280k ',
                                  'CBR: 1312k': '-b:a 1312k ',
                                  'CBR: 1344k': '-b:a 1344k ',
                                  'CBR: 1367k': '-b:a 1376k ',
                                  'CBR: 1408k': '-b:a 1408k '}
        acodec_bitrate.set('CBR: 192k')  # set the default option
        acodec_bitrate_menu_label = Label(audio_window, text="Quality :", background="#434547", foreground="white")
        acodec_bitrate_menu_label.grid(row=0, column=2, columnspan=1, padx=10, pady=3, sticky=W+E)
        acodec_bitrate_menu = OptionMenu(audio_window, acodec_bitrate, *acodec_bitrate_choices.keys())
        acodec_bitrate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_bitrate_menu.grid(row=1, column=2, columnspan=1, padx=10, pady=3, sticky=N+S+W+E)
        acodec_bitrate_menu["menu"].configure(activebackground="dim grey")
        acodec_bitrate_menu.bind("<Enter>", acodec_bitrate_menu_hover)
        acodec_bitrate_menu.bind("<Leave>", acodec_bitrate_menu_hover_leave)

        # Audio Channel Selection
        acodec_channel = StringVar(audio_window)
        acodec_channel_choices = { 'Original': "",
                                   '1 (Mono)': "-ac 1 ",
                                   '2 (Stereo)': "-ac 2 ",
                                   '5.1 (Surround)': "-ac 6 "}
        acodec_channel.set('Original') # set the default option
        achannel_menu_label = Label(audio_window, text="Channels :", background="#434547", foreground="white")
        achannel_menu_label.grid(row=0, column=1, columnspan=1, padx=10, pady=3, sticky=W+E)
        achannel_menu = OptionMenu(audio_window, acodec_channel, *acodec_channel_choices.keys())
        achannel_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        achannel_menu.grid(row=1, column=1, columnspan=1, padx=10, pady=3, sticky=N+S+W+E)
        achannel_menu["menu"].configure(activebackground="dim grey")
        achannel_menu.bind("<Enter>", achannel_menu_hover)
        achannel_menu.bind("<Leave>", achannel_menu_hover_leave)

        # Audio Stream Selection
        acodec_stream = StringVar(audio_window)
        acodec_stream_choices = acodec_stream_track_counter
        acodec_stream.set('Track 1') # set the default option
        acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
        acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W+E)
        acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
        acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N+S+W+E)
        acodec_stream_menu["menu"].configure(activebackground="dim grey")
        acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
        acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)

        # Audio Gain Selection
        acodec_gain = StringVar(audio_window)
        acodec_gain_choices = {'Default (0)': "-sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+10 dB': "-af volume=10dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+9 dB': "-af volume=9dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+8 dB': "-af volume=8dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+7 dB': "-af volume=7dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+6 dB': "-af volume=6dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+5 dB': "-af volume=5dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+4 dB': "-af volume=4dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+3 dB': "-af volume=3dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+2 dB': "-af volume=2dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+1 dB': "-af volume=1dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-1 dB': "-af volume=-1dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-2 dB': "-af volume=-2dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-3 dB': "-af volume=-3dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-4 dB': "-af volume=-4dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-5 dB': "-af volume=-5dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-6 dB': "-af volume=-6dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-7 dB': "-af volume=-7dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-8 dB': "-af volume=-8dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-9 dB': "-af volume=-9dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-10 dB': "-af volume=-10dB -sn -vn -map_chapters -1 -map_metadata -1 "}
        acodec_gain.set('Default (0)')  # set the default option
        acodec_gain_label = Label(audio_window, text="Gain :", background="#434547", foreground="white")
        acodec_gain_label.grid(row=2, column=0, columnspan=1, padx=10, pady=3, sticky=N+S+E+W)
        acodec_gain_menu = OptionMenu(audio_window, acodec_gain, *acodec_gain_choices.keys())
        acodec_gain_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_gain_menu.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N+S+E+W)
        acodec_gain_menu["menu"].configure(activebackground="dim grey")
        acodec_gain_menu.bind("<Enter>", acodec_gain_menu_hover)
        acodec_gain_menu.bind("<Leave>", acodec_gain_menu_hover_leave)

        # Audio Sample Rate Selection
        acodec_samplerate = StringVar(audio_window)
        acodec_samplerate_choices = {'Original': "",
                                     '44100 Hz': "-ar 44100 ",
                                     '48000 Hz': "-ar 48000 "}
        acodec_samplerate.set('Original')  # set the default option
        acodec_samplerate_label = Label(audio_window, text="Sample Rate :", background="#434547", foreground="white")
        acodec_samplerate_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3, sticky=N+S+E+W)
        acodec_samplerate_menu = OptionMenu(audio_window, acodec_samplerate, *acodec_samplerate_choices.keys())
        acodec_samplerate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_samplerate_menu.grid(row=3, column=1, columnspan=1, padx=10, pady=3, sticky=N+S+E+W)
        acodec_samplerate_menu["menu"].configure(activebackground="dim grey")
        acodec_samplerate_menu.bind("<Enter>", acodec_samplerate_menu_hover)
        acodec_samplerate_menu.bind("<Leave>", acodec_samplerate_menu_hover_leave)

        # FDK-AAC Window -----------------------
    elif encoder.get() == "FDK-AAC":
        audio_window = Toplevel()
        audio_window.title('FDK-AAC Settings')
        audio_window.configure(background="#434547")
        window_height = 500
        window_width = 700
        screen_width = audio_window.winfo_screenwidth()
        screen_height = audio_window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        my_menu = Menu(audio_window, tearoff=0)
        audio_window.config(menu=my_menu)
        check_streams = Menu(my_menu, tearoff=0, activebackground="dim grey")
        my_menu.add_command(label="View Streams", command=show_streams_mediainfo)

        audio_window.grid_columnconfigure(0, weight=1)
        audio_window.grid_columnconfigure(1, weight=1)
        audio_window.grid_columnconfigure(2, weight=1)
        audio_window.grid_rowconfigure(0, weight=1)
        audio_window.grid_rowconfigure(1, weight=1)
        audio_window.grid_rowconfigure(2, weight=1)
        audio_window.grid_rowconfigure(3, weight=1)
        audio_window.grid_rowconfigure(4, weight=1)
        audio_window.grid_rowconfigure(5, weight=1)
        audio_window.grid_rowconfigure(6, weight=1)
        audio_window.grid_rowconfigure(7, weight=1)
        audio_window.grid_rowconfigure(8, weight=1)
        audio_window.grid_rowconfigure(9, weight=1)
        audio_window.grid_rowconfigure(10, weight=1)

        def apply_button_hover(e):
            apply_button["bg"] = "grey"
        def apply_button_hover_leave(e):
            apply_button["bg"] = "#23272A"

        def help_button_hover(e):
            help_button["bg"] = "grey"
        def help_button_hover_leave(e):
            help_button["bg"] = "#23272A"


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

        def acodec_gain_menu_hover(e):
            acodec_gain_menu["bg"] = "grey"
            acodec_gain_menu["activebackground"] = "grey"
        def acodec_gain_menu_hover_leave(e):
            acodec_gain_menu["bg"] = "#23272A"

        def acodec_samplerate_menu_hover(e):
            acodec_samplerate_menu["bg"] = "grey"
            acodec_samplerate_menu["activebackground"] = "grey"
        def acodec_samplerate_menu_hover_leave(e):
            acodec_samplerate_menu["bg"] = "#23272A"

        def acodec_profile_menu_hover(e):
            acodec_profile_menu["bg"] = "grey"
            acodec_profile_menu["activebackground"] = "grey"
        def acodec_profile_menu_hover_leave(e):
            acodec_profile_menu["bg"] = "#23272A"

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

        def gotosavefile():
            audio_window.destroy()
            output_button.config(state=NORMAL)
            start_audio_button.config(state=NORMAL)
            command_line_button.config(state=NORMAL)

        apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A",
                              command=gotosavefile)
        apply_button.grid(row=10, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        apply_button.bind("<Enter>", apply_button_hover)
        apply_button.bind("<Leave>", apply_button_hover_leave)

        help_button = Button(audio_window, text="Help + Information", foreground="white", background="#23272A", command=gotofdkaachelp)
        help_button.grid(row=3, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        help_button.bind("<Enter>", help_button_hover)
        help_button.bind("<Leave>", help_button_hover_leave)

        advanced_label = Label(audio_window, text="- - - - - - - - - - - - - - - - - - - - Advanced Settings - - - - - - - - - - - - - - - - - - - -", background="#434547", foreground="white", relief=GROOVE)
        advanced_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky=W+E)

        # Audio Bitrate Menu
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
        acodec_bitrate.set('CBR: 192k')  # set the default option
        acodec_bitrate_menu_label = Label(audio_window, text="Quality :", background="#434547", foreground="white")
        acodec_bitrate_menu_label.grid(row=0, column=2, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_bitrate_menu = OptionMenu(audio_window, acodec_bitrate, *acodec_bitrate_choices.keys())
        acodec_bitrate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_bitrate_menu.grid(row=1, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_bitrate_menu["menu"].configure(activebackground="dim grey")
        acodec_bitrate_menu.bind("<Enter>", acodec_bitrate_menu_hover)
        acodec_bitrate_menu.bind("<Leave>", acodec_bitrate_menu_hover_leave)

        # Audio Channel Selection
        acodec_channel = StringVar(audio_window)
        acodec_channel_choices = {'Original': "",
                                  '1 (Mono)': "-ac 1 ",
                                  '2 (Stereo)': "-ac 2 ",
                                  '5.1 (Surround)': "-ac 6 ",
                                  '6.1 (Surround)': "-ac 7 ",
                                  '7.1 (Surround)': "-ac 8 "}
        acodec_channel.set('Original')  # set the default option
        achannel_menu_label = Label(audio_window, text="Channels :", background="#434547", foreground="white")
        achannel_menu_label.grid(row=0, column=1, columnspan=1, padx=10, pady=3, sticky=W + E)
        achannel_menu = OptionMenu(audio_window, acodec_channel, *acodec_channel_choices.keys())
        achannel_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        achannel_menu.grid(row=1, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        achannel_menu["menu"].configure(activebackground="dim grey")
        achannel_menu.bind("<Enter>", achannel_menu_hover)
        achannel_menu.bind("<Leave>", achannel_menu_hover_leave)

        # Audio Stream Selection
        acodec_stream = StringVar(audio_window)
        acodec_stream_choices = acodec_stream_track_counter
        acodec_stream.set('Track 1')  # set the default option
        acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
        acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
        acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_stream_menu["menu"].configure(activebackground="dim grey")
        acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
        acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)

        # Audio Gain Selection
        acodec_gain = StringVar(audio_window)
        acodec_gain_choices = {'Default (0)': "-sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+10 dB': "-af volume=10dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+9 dB': "-af volume=9dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+8 dB': "-af volume=8dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+7 dB': "-af volume=7dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+6 dB': "-af volume=6dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+5 dB': "-af volume=5dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+4 dB': "-af volume=4dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+3 dB': "-af volume=3dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+2 dB': "-af volume=2dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '+1 dB': "-af volume=1dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-1 dB': "-af volume=-1dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-2 dB': "-af volume=-2dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-3 dB': "-af volume=-3dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-4 dB': "-af volume=-4dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-5 dB': "-af volume=-5dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-6 dB': "-af volume=-6dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-7 dB': "-af volume=-7dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-8 dB': "-af volume=-8dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-9 dB': "-af volume=-9dB -sn -vn -map_chapters -1 -map_metadata -1 ",
                               '-10 dB': "-af volume=-10dB -sn -vn -map_chapters -1 -map_metadata -1 "}
        acodec_gain.set('Default (0)')  # set the default option
        acodec_gain_label = Label(audio_window, text="Gain :", background="#434547", foreground="white")
        acodec_gain_label.grid(row=2, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_gain_menu = OptionMenu(audio_window, acodec_gain, *acodec_gain_choices.keys())
        acodec_gain_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_gain_menu.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_gain_menu["menu"].configure(activebackground="dim grey")
        acodec_gain_menu.bind("<Enter>", acodec_gain_menu_hover)
        acodec_gain_menu.bind("<Leave>", acodec_gain_menu_hover_leave)

        # Audio Sample Rate Selection
        acodec_samplerate = StringVar(audio_window)
        acodec_samplerate_choices = {'Original': "",
                                     '11025 Hz': "-ar 11025 ",
                                     '22050 Hz': "-ar 22050 ",
                                     '44100 Hz': "-ar 44100 ",
                                     '48000 Hz': "-ar 48000 ",
                                     '88200 Hz': "-ar 88200 ",
                                     '96000 Hz': "-ar 96000 "}
        acodec_samplerate.set('Original')  # set the default option
        acodec_samplerate_label = Label(audio_window, text="Sample Rate :", background="#434547", foreground="white")
        acodec_samplerate_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_samplerate_menu = OptionMenu(audio_window, acodec_samplerate, *acodec_samplerate_choices.keys())
        acodec_samplerate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_samplerate_menu.grid(row=3, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_samplerate_menu["menu"].configure(activebackground="dim grey")
        acodec_samplerate_menu.bind("<Enter>", acodec_samplerate_menu_hover)
        acodec_samplerate_menu.bind("<Leave>", acodec_samplerate_menu_hover_leave)

        # Advanced Section ---------

        # Audio Profile Selection
        global acodec_profile
        global acodec_profile_choices
        acodec_profile = StringVar(audio_window)
        acodec_profile_choices = {'AAC LC (Default)': "-p2 ",
                                     'HE-AAC SBR': "-p5 ",
                                     'HE-AAC V2 (SBR+PS)': "-p29 ",
                                     'AAC LD': "-p23 ",
                                     'AAC ELD': "-p39 "}
        acodec_profile.set('AAC LC (Default)')  # set the default option
        acodec_profile_label = Label(audio_window, text="Profile :", background="#434547", foreground="white")
        acodec_profile_label.grid(row=5, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_profile_menu = OptionMenu(audio_window, acodec_profile, *acodec_profile_choices.keys())
        acodec_profile_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_profile_menu.grid(row=6, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_profile_menu["menu"].configure(activebackground="dim grey")
        acodec_profile_menu.bind("<Enter>", acodec_profile_menu_hover)
        acodec_profile_menu.bind("<Leave>", acodec_profile_menu_hover_leave)

        # Audio Lowdelay SBR Selection
        global acodec_lowdelay
        global acodec_lowdelay_choices
        acodec_lowdelay = StringVar(audio_window)
        acodec_lowdelay_choices = {'Disable SBR on ELD (DEF)': "-L0 ",
                                     'ELD SBR Auto Conf': "-L-1 ",
                                     'Enable SBR on ELD': "-L1 "}
        acodec_lowdelay.set('Disable SBR on ELD (DEF)')  # set the default option
        acodec_lowdelay_label = Label(audio_window, text="Lowdelay SBR :", background="#434547", foreground="white")
        acodec_lowdelay_label.grid(row=5, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_lowdelay_menu = OptionMenu(audio_window, acodec_lowdelay, *acodec_lowdelay_choices.keys())
        acodec_lowdelay_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_lowdelay_menu.grid(row=6, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_lowdelay_menu["menu"].configure(activebackground="dim grey")
        acodec_lowdelay_menu.bind("<Enter>", acodec_lowdelay_menu_hover)
        acodec_lowdelay_menu.bind("<Leave>", acodec_lowdelay_menu_hover_leave)

        # Audio SBR Ratio
        global acodec_sbr_ratio
        global acodec_sbr_ratio_choices
        acodec_sbr_ratio = StringVar(audio_window)
        acodec_sbr_ratio_choices = {'Libary Default': "-s0 ",
                                     'Downsampled SBR (ELD+SBR Def)': "-s1 ",
                                     'Dual-Rate SBR (HE-AAC-Def)': "-s2 "}
        acodec_sbr_ratio.set('Libary Default')  # set the default option
        acodec_sbr_ratio_label = Label(audio_window, text="SBR Ratio :", background="#434547", foreground="white")
        acodec_sbr_ratio_label.grid(row=5, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_sbr_ratio_menu = OptionMenu(audio_window, acodec_sbr_ratio, *acodec_sbr_ratio_choices.keys())
        acodec_sbr_ratio_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_sbr_ratio_menu.grid(row=6, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_sbr_ratio_menu["menu"].configure(activebackground="dim grey")
        acodec_sbr_ratio_menu.bind("<Enter>", acodec_sbr_ratio_menu_hover)
        acodec_sbr_ratio_menu.bind("<Leave>", acodec_sbr_ratio_menu_hover_leave)

        # Audio Gapless Mode
        global acodec_gapless_mode
        global acodec_gapless_mode_choices
        acodec_gapless_mode = StringVar(audio_window)
        acodec_gapless_mode_choices = {'iTunSMPB (Def)': "-G0 ",
                                     'ISO Standard (EDTS+SGPD)': "-G1 ",
                                     'Both': "-G2 "}
        acodec_gapless_mode.set('iTunSMPB (Def)')  # set the default option
        acodec_gapless_mode_label = Label(audio_window, text="SBR Ratio :", background="#434547", foreground="white")
        acodec_gapless_mode_label.grid(row=7, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_gapless_mode_menu = OptionMenu(audio_window, acodec_gapless_mode, *acodec_gapless_mode_choices.keys())
        acodec_gapless_mode_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_gapless_mode_menu.grid(row=8, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_gapless_mode_menu["menu"].configure(activebackground="dim grey")
        acodec_gapless_mode_menu.bind("<Enter>", acodec_gapless_mode_menu_hover)
        acodec_gapless_mode_menu.bind("<Leave>", acodec_gapless_mode_menu_hover_leave)

        # Audio Transport Format
        global acodec_transport_format
        global acodec_transport_format_choices
        acodec_transport_format = StringVar(audio_window)
        acodec_transport_format_choices = {'M4A (Def)': "-f0 ",
                                           'ADIF': "-f1 ",
                                           'ADTS': "-f2 ",
                                           'LATM MCP=1': "-f6 ",
                                           'LATM MCP=0': "-f7 ",
                                           'LOAS/LATM (LATM w/in LOAS)': "-f10 "}
        acodec_transport_format.set('M4A (Def)')  # set the default option
        acodec_transport_format_label = Label(audio_window, text="Transport Format :", background="#434547", foreground="white")
        acodec_transport_format_label.grid(row=7, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_transport_format_menu = OptionMenu(audio_window, acodec_transport_format, *acodec_transport_format_choices.keys())
        acodec_transport_format_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_transport_format_menu.grid(row=8, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_transport_format_menu["menu"].configure(activebackground="dim grey")
        acodec_transport_format_menu.bind("<Enter>", acodec_transport_format_menu_hover)
        acodec_transport_format_menu.bind("<Leave>", acodec_transport_format_menu_hover_leave)

        #Misc Checkboxes - Afterburner
        global afterburnervar
        afterburnervar = StringVar()
        afterburnervar.set("-a1 ")
        afterburner_checkbox = Checkbutton(audio_window, text='Afterburner', variable=afterburnervar, onvalue="-a1 ", offvalue="-a0 ")
        afterburner_checkbox.grid(row=8, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        afterburner_checkbox.configure(background="#434547", foreground="white", activebackground="#434547", activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))

        #Misc Checkboxes - Add CRC Check on ADTS Header
        global crccheck
        crccheck = StringVar()
        crccheck.set("")
        crccheck_checkbox = Checkbutton(audio_window, text='CRC Check on\n ADTS Header', variable=crccheck, onvalue="-C ", offvalue="")
        crccheck_checkbox.grid(row=9, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        crccheck_checkbox.configure(background="#434547", foreground="white", activebackground="#434547", activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))

        # Misc Checkboxes - Header Period
        global headerperiod
        headerperiod = StringVar()
        headerperiod.set("")
        headerperiod_checkbox = Checkbutton(audio_window, text='Header Period', variable=headerperiod,
                                        onvalue="-h ", offvalue="")
        headerperiod_checkbox.grid(row=9, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        headerperiod_checkbox.configure(background="#434547", foreground="white", activebackground="#434547", activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))

        # Misc Checkboxes - Include SBR Delay
        global sbrdelay
        sbrdelay = StringVar()
        sbrdelay.set("")
        sbrdelay_checkbox = Checkbutton(audio_window, text='SBR Delay', variable=sbrdelay,
                                            onvalue="--include-sbr-delay ", offvalue="")
        sbrdelay_checkbox.grid(row=9, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        sbrdelay_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                        activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))

        # Misc Checkboxes - Place Moov Box Before Mdat Box
        global moovbox
        moovbox = StringVar()
        moovbox.set("")
        moovbox_checkbox = Checkbutton(audio_window, text='Place Moov Box Before Mdat Box', variable=moovbox,
                                            onvalue="--moov-before-mdat ", offvalue="", anchor='w')
        moovbox_checkbox.grid(row=10, column=0, columnspan=2, padx=10, pady=3, sticky=N + S + E + W)
        moovbox_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                        activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
# Code------------------------------------------------------------------------

def file_input():
    global VideoInput
    global VideoInputQuoted
    global VideoOutput
    global VideoOutputQuoted
    global autofilesave_dir_path
    global track_count
    VideoInput = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                            filetypes=(("MKA, WAV, MP3, AAC, OGG, OGV, M4V, MPEG, AVI, VOB, WEBM, MKV, MP4, DTS, AC3, MT2S, WAV", "*.wav *.mt2s *.ac3 *.mka *.wav *.mp3 *.aac *.ogg *.ogv *.m4v *.mpeg *.avi *.vob *.webm *.mp4 *.mkv *.dts"), ("All Files", "*.*")))
    input_entry.delete(0, END)  # Remove current text in entry
    input_entry.insert(0, VideoInput)  # Insert the 'path'
    autofilesave_file_path = pathlib.PureWindowsPath(VideoInput) # Command to get file input location
    autofilesave_dir_path = autofilesave_file_path.parents[0] # Final command to get only the directory of fileinput

    if not VideoInput:
        output_button.config(state=DISABLED)
        show_streams_button.config(state=DISABLED)
        encoder_menu.config(state=DISABLED)
        audiosettings_button.configure(state=DISABLED)
    else:
        show_streams_button.config(state=NORMAL)
        encoder_menu.config(state=NORMAL)
        VideoInputQuoted = '"' + VideoInput + '"'
        # This gets the total amount of audio streams -----------------------------------------------------------------
        mediainfocli_cmd = '"' + mediainfocli + " " + '--Output="General;%AudioCount%"' + " " + VideoInputQuoted + '"'
        mediainfo_count = subprocess.Popen('cmd /c ' + mediainfocli_cmd, creationflags=subprocess.CREATE_NO_WINDOW, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout, stderr = mediainfo_count.communicate()
        track_count = stdout

        output_entry.configure(state=NORMAL)
        output_entry.delete(0, END)
        output_entry.configure(state=DISABLED)

def file_save():
    global VideoOutput
    if encoder.get() == "AAC":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".mp4", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location",
                                                   filetypes=(("AAC", "*.mp4"), ("All Files", "*.*")))
    elif encoder.get() == "AC3":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".ac3", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location",
                                                   filetypes=(("AC3", "*.ac3"), ("All Files", "*.*")))
    elif encoder.get() == "DTS":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".dts", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location",
                                                   filetypes=(("DTS", "*.dts"), ("All Files", "*.*")))
    elif encoder.get() == "Opus":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".opus", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location",
                                                   filetypes=(("Opus", "*.opus"), ("All Files", "*.*")))
    elif encoder.get() == "MP3":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".mp3", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location",
                                                   filetypes=(("MP3", "*.mp3"), ("All Files", "*.*")))
    elif encoder.get() == "E-AC3":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".ac3", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location",
                                                   filetypes=(("E-AC3", "*.ac3"), ("All Files", "*.*")))
    elif encoder.get() == "FDK-AAC":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".m4a", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location",
                                                   filetypes=(("AAC", "*.m4a"), ("All Files", "*.*")))

    output_entry.configure(state=NORMAL) # Enable entry box for commands under
    output_entry.delete(0, END)  # Remove current text in entry
    output_entry.insert(0, VideoOutput)  # Insert the 'path'
    output_entry.configure(state=DISABLED) # Disables Entry Box

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

def show_streams_button_hover(e):
    show_streams_button["bg"] = "grey"
def show_streams_button_hover_leave(e):
    show_streams_button["bg"] = "#23272A"

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

button_status_label = Label(root, relief=SUNKEN)

def print_command_line():
    cmd_line_window = Toplevel()
    cmd_line_window.title('Command Line')
    cmd_line_window.configure(background="#434547")
    VideoInputQuoted = '"' + VideoInput + '"'
    VideoOutputQuoted = '"' + VideoOutput + '"'
    if encoder.get() == "DTS":
        example_cmd_output = "ffmpeg.exe -analyzeduration 100M -probesize 50M -i " +"\n \n"+ VideoInputQuoted +"\n \n"+ acodec_stream_choices[
            acodec_stream.get()] + dts_settings_choices[
                           dts_settings.get()] + " -sn -vn -map_chapters -1 " +"\n \n"+ VideoOutputQuoted
    elif encoder.get() == "FDK-AAC":
        example_cmd_output = "ffmpeg.exe -analyzeduration 100M -probesize 50M -i " +"\n \n"+ VideoInputQuoted +"\n \n"+ acodec_stream_choices[acodec_stream.get()] + acodec_channel_choices[acodec_channel.get()] + acodec_samplerate_choices[acodec_samplerate.get()] + acodec_gain_choices[acodec_gain.get()] + "-f caf - | " +"\n \n"+ "fdkaac.exe" + " " + acodec_profile_choices[acodec_profile.get()] + afterburnervar.get() + crccheck.get() + moovbox.get() + sbrdelay.get() + headerperiod.get() + acodec_lowdelay_choices[acodec_lowdelay.get()] + acodec_sbr_ratio_choices[acodec_sbr_ratio.get()] + acodec_transport_format_choices[acodec_transport_format.get()] + acodec_bitrate_choices[acodec_bitrate.get()] + "- -o " +"\n \n"+ VideoOutputQuoted

    else:
        example_cmd_output = "ffmpeg.exe -analyzeduration 100M -probesize 50M -i " +"\n \n"+ VideoInputQuoted +"\n \n"+ \
                             acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] + \
                             acodec_bitrate_choices[acodec_bitrate.get()] + acodec_channel_choices[acodec_channel.get()] + \
                             acodec_samplerate_choices[acodec_samplerate.get()] + acodec_gain_choices[
                                 acodec_gain.get()] +"\n \n"+ VideoOutputQuoted
    cmd_label = Label(cmd_line_window, text=example_cmd_output, foreground="white", background="#434547")
    cmd_label.config(font=("Helvetica", 16))
    cmd_label.pack()


# Job Buttons ---------------------------------------------------------

def startaudiojob():
    global example_cmd_output
    # Quote File Input/Output Paths--------------
    VideoInputQuoted = '"' + VideoInput + '"'
    VideoOutputQuoted = '"' + VideoOutput + '"'
    # Commands------------------------------------
    if encoder.get() == "AC3":
        if shell_options.get() == "Default":
            finalcommand = ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] + acodec_bitrate_choices[acodec_bitrate.get()] + acodec_channel_choices[acodec_channel.get()] + acodec_samplerate_choices[acodec_samplerate.get()] + acodec_gain_choices[acodec_gain.get()] + VideoOutputQuoted + " -hide_banner -v error -stats"
            subprocess.Popen(finalcommand)
        elif shell_options.get() == "Debug":
            finalcommand = '"' + ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] + acodec_bitrate_choices[acodec_bitrate.get()] + acodec_channel_choices[acodec_channel.get()] + acodec_samplerate_choices[acodec_samplerate.get()] + acodec_gain_choices[acodec_gain.get()] + VideoOutputQuoted + " -hide_banner" + '"'
            subprocess.Popen('cmd /k ' + finalcommand)

    elif encoder.get() == "AAC":
        if shell_options.get() == "Default":
            finalcommand = ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] + acodec_bitrate_choices[acodec_bitrate.get()] + acodec_channel_choices[acodec_channel.get()] + acodec_samplerate_choices[acodec_samplerate.get()] + acodec_gain_choices[acodec_gain.get()] + VideoOutputQuoted + " -hide_banner -v error -stats"
            subprocess.Popen(finalcommand)
        elif shell_options.get() == "Debug":
            finalcommand = '"' + ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] + acodec_bitrate_choices[acodec_bitrate.get()] + acodec_channel_choices[acodec_channel.get()] + acodec_samplerate_choices[acodec_samplerate.get()] + acodec_gain_choices[acodec_gain.get()] + VideoOutputQuoted + " -hide_banner" + '"'
            subprocess.Popen('cmd /k ' + finalcommand)

    elif encoder.get() == 'DTS':
        if shell_options.get() == "Default":
            finalcommand = ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] + dts_settings_choices[dts_settings.get()] + " -sn -vn -map_chapters -1 " + VideoOutputQuoted + " -hide_banner -v error -stats"
            subprocess.Popen(finalcommand)
        elif shell_options.get() == "Debug":
            finalcommand = '"' + ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] + dts_settings_choices[dts_settings.get()] + " -sn -vn -map_chapters -1 " + VideoOutputQuoted + " -hide_banner" + '"'
            subprocess.Popen('cmd /k ' + finalcommand)

    elif encoder.get() == "Opus":
        if shell_options.get() == "Default":
            finalcommand = ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] + acodec_vbr_choices[acodec_vbr.get()] + acodec_bitrate_choices[acodec_bitrate.get()] + acodec_channel_choices[acodec_channel.get()] + acodec_gain_choices[acodec_gain.get()] + VideoOutputQuoted + " -hide_banner -v error -stats"
            subprocess.Popen(finalcommand)
        elif shell_options.get() == "Debug":
            finalcommand = '"' + ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] + acodec_vbr_choices[acodec_vbr.get()] + acodec_bitrate_choices[acodec_bitrate.get()] + acodec_channel_choices[acodec_channel.get()] + acodec_gain_choices[acodec_gain.get()] + VideoOutputQuoted + " -hide_banner" + '"'
            subprocess.Popen('cmd /k ' + finalcommand)

    elif encoder.get() == "MP3":
        if shell_options.get() == "Default":
            finalcommand = ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] + acodec_bitrate_choices[acodec_bitrate.get()] + acodec_channel_choices[acodec_channel.get()] + acodec_samplerate_choices[acodec_samplerate.get()] + acodec_gain_choices[acodec_gain.get()] + VideoOutputQuoted + " -hide_banner -v error -stats"
            subprocess.Popen(finalcommand)
        elif shell_options.get() == "Debug":
            finalcommand = '"' + ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] + acodec_bitrate_choices[acodec_bitrate.get()] + acodec_channel_choices[acodec_channel.get()] + acodec_samplerate_choices[acodec_samplerate.get()] + acodec_gain_choices[acodec_gain.get()] + VideoOutputQuoted + " -hide_banner" + '"'
            subprocess.Popen('cmd /k ' + finalcommand)

    elif encoder.get() == "E-AC3":
        if shell_options.get() == "Default":
            finalcommand = ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] + acodec_bitrate_choices[acodec_bitrate.get()] + acodec_channel_choices[acodec_channel.get()] + acodec_samplerate_choices[acodec_samplerate.get()] + acodec_gain_choices[acodec_gain.get()] + VideoOutputQuoted + " -hide_banner -v error -stats"
            subprocess.Popen(finalcommand)
        elif shell_options.get() == "Debug":
            finalcommand = '"' + ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] + acodec_bitrate_choices[acodec_bitrate.get()] + acodec_channel_choices[acodec_channel.get()] + acodec_samplerate_choices[acodec_samplerate.get()] + acodec_gain_choices[acodec_gain.get()] + VideoOutputQuoted + " -hide_banner" + '"'
            subprocess.Popen('cmd /k ' + finalcommand)

    elif encoder.get() == "FDK-AAC":
        if shell_options.get() == "Default":
            finalcommand = '"' + ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] + acodec_channel_choices[acodec_channel.get()] + acodec_samplerate_choices[acodec_samplerate.get()] + acodec_gain_choices[acodec_gain.get()] + "-f caf - | " + fdkaac + " " + acodec_profile_choices[acodec_profile.get()] + afterburnervar.get() + crccheck.get() + moovbox.get() + sbrdelay.get() + headerperiod.get() + acodec_lowdelay_choices[acodec_lowdelay.get()] + acodec_sbr_ratio_choices[acodec_sbr_ratio.get()] + acodec_transport_format_choices[acodec_transport_format.get()] + acodec_bitrate_choices[acodec_bitrate.get()] + "- -o " + VideoOutputQuoted + '"'
            subprocess.Popen('cmd /c ' + finalcommand) #DELETE THIS AND FINISH THIS LATER, THIS IS PROPER COMMAND WITH ABOVE COMMAND
        elif shell_options.get() == "Debug":
            finalcommand = '"' + ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] + acodec_channel_choices[acodec_channel.get()] + acodec_samplerate_choices[acodec_samplerate.get()] + acodec_gain_choices[acodec_gain.get()] + "-f caf - | " + fdkaac + " " + acodec_profile_choices[acodec_profile.get()] + afterburnervar.get() + crccheck.get() + moovbox.get() + sbrdelay.get() + headerperiod.get() + acodec_lowdelay_choices[acodec_lowdelay.get()] + acodec_sbr_ratio_choices[acodec_sbr_ratio.get()] + acodec_transport_format_choices[acodec_transport_format.get()] + acodec_bitrate_choices[acodec_bitrate.get()] + "- -o " + VideoOutputQuoted + '"'
            subprocess.Popen('cmd /k ' + finalcommand)

def mediainfogui(): # Opens file via included portable MediaInfo
    VideoInputQuoted = '"' + VideoInput + '"'
    MediaInfoQuoted = '"' + mediainfo + '"'
    commands = MediaInfoQuoted + " " + VideoInputQuoted
    subprocess.Popen(commands)

# Buttons Main Gui -------------------------------------------------

encoder_menu.bind("<Enter>", encoder_menu_hover)
encoder_menu.bind("<Leave>", encoder_menu_hover_leave)

show_streams_button = Button(root, text="MediaInfo", command=mediainfogui, state=DISABLED, foreground="white", background="#23272A", borderwidth="3")
show_streams_button.grid(row=1, column=0, columnspan=1, padx=5, pady=5, sticky=N+S+E+W)
show_streams_button.bind("<Enter>", show_streams_button_hover)
show_streams_button.bind("<Leave>", show_streams_button_hover_leave)

audiosettings_button = Button(root, text="Audio Settings", command=openaudiowindow, foreground="white", background="#23272A", state=DISABLED, borderwidth="3")
audiosettings_button.grid(row=1, column=3, columnspan=2, padx=5, pady=5, sticky=N+S+W+E)
audiosettings_button.bind("<Enter>", audiosettings_button_hover)
audiosettings_button.bind("<Leave>", audiosettings_button_hover_leave)

def input_button_commands():
    encoder.set('Set Codec')
    audiosettings_button.configure(state=DISABLED)
    file_input()


input_button = tk.Button(root, text="Open File", command=input_button_commands, foreground="white", background="#23272A", borderwidth="3")
input_button.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=N+S+E+W)
input_entry = Entry(root, width=35, borderwidth=4, background="#CACACA")
input_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=S+E+W)
input_button.bind("<Enter>", input_button_hover)
input_button.bind("<Leave>", input_button_hover_leave)

output_button = Button(root, text="Save File", command=file_save, state=DISABLED, foreground="white", background="#23272A", borderwidth="3")
output_button.grid(row=2, column=0, columnspan=1, padx=5, pady=5, sticky=N+S+E+W)
output_entry = Entry(root, width=35, borderwidth=4, background="#CACACA")
output_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky=S+E+W)
output_button.bind("<Enter>", output_button_hover)
output_button.bind("<Leave>", output_button_hover_leave)

# Print Final Command Line
command_line_button = Button(root, text="Show\nCommand", command=print_command_line, state=DISABLED, foreground="white", background="#23272A", borderwidth="3")
command_line_button.grid(row=3, column=0, columnspan=1, padx=5, pady=5, sticky=N+S+E+W)
command_line_button.bind("<Enter>", command_line_button_hover)
command_line_button.bind("<Leave>", command_line_button_hover_leave)

# Start Audio Job
start_audio_button = Button(root, text="Start Audio Job", command=startaudiojob, state=DISABLED, foreground="white", background="#23272A", borderwidth="3")
start_audio_button.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky=N+S+E+W)
start_audio_button.bind("<Enter>", start_audio_button_hover)
start_audio_button.bind("<Leave>", start_audio_button_hover_leave)

# End Loop -----------------------------------------------------------------------
root.mainloop()