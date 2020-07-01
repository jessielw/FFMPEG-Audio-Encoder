# Imports--------------------------------------------------------------------

from tkinter import *
from tkinter import filedialog, StringVar
import subprocess
import os
import shlex

# Main Gui & Windows --------------------------------------------------------

root = Tk()
root.title("FFMPEG Audio Encoder Beta 1.24")
root.iconphoto(True, PhotoImage(file="C:/Users/jlw_4/Desktop/jlwFFMPEG.png"))
root.configure(background="#434547")
# root.resizable(False, False)  # This code helps to disable windows from resizing
window_height = 180
window_width = 386
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

# Menu Bar Settings ---------------------------------------------------------

my_menu = Menu(root, tearoff=0)
root.config(menu=my_menu)

# Bundled Apps ---------------------------------------------------------------

PROGRAM_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
# ffmpeg = os.path.join(PROGRAM_DIR, "Apps/FFMPEG/ffmpeg.exe")
# ffprobe = os.path.join(PROGRAM_DIR, "Apps/FFMPEG/ffprobe.exe")
ffprobe = "Apps/FFMPEG/ffprobe.exe"
ffmpeg = "Apps/FFMPEG/ffmpeg.exe"
mediainfo = "Apps/MediaInfo/MediaInfo.exe"

# About Window ---------------------------------------------------------------

def openaboutwindow():
    about_window = Toplevel()
    about_window.title('About')
    about_window.configure(background="#646464")
    window_height = 150
    window_width = 370
    screen_width = about_window.winfo_screenwidth()
    screen_height = about_window.winfo_screenheight()
    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))
    about_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    about_window_label = Label(about_window, text="About Text Will Go Here Eventually...")
    about_window_label.grid(row=3, column=1, columnspan=1, padx=10, pady=10)


# Menu Items and Sub-Bars ----------------------------------------------------

file_menu = Menu(my_menu, tearoff=0, activebackground="dim grey")
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=root.quit)

edit_menu = Menu(my_menu, tearoff=0, activebackground="dim grey")
my_menu.add_cascade(label="Edit", menu=edit_menu)

help_menu = Menu(my_menu, tearoff=0, activebackground="dim grey")
my_menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=openaboutwindow) # Possibly Expand This Later

# Encoder Codec Drop Down
encoder_dropdownmenu_choices = {
    "AC3": "ac3",
    "AAC": "aac",
    "DTS": "dts"
}
encoder = StringVar(root)
encoder.set("Choose Codec")
encoder_menu = OptionMenu(root, encoder, *encoder_dropdownmenu_choices.keys())
encoder_menu.grid(row=1, column=1, columnspan=1, padx=5, pady=5, sticky=W+E)
encoder_menu.config(state=DISABLED, background="#23272A", foreground="white", highlightthickness=1)
encoder_menu["menu"].configure(activebackground="dim grey")

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

    # AC3 Window ----------------------------
    if encoder.get() == "AC3":
        audio_window = Toplevel()
        audio_window.title('AC3 Settings')
        audio_window.configure(background="#646464")
        window_height = 140
        window_width = 362
        screen_width = audio_window.winfo_screenwidth()
        screen_height = audio_window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        def apply_button_hover(e):
            apply_button["bg"] = "white"
        def apply_button_hover_leave(e):
            apply_button["bg"] = "SystemButtonFace"

        def gotosavefile():
            audio_window.destroy()
            output_button.config(state=NORMAL)

        apply_button = Button(audio_window, text="Apply", command=gotosavefile)
        apply_button.grid(row=3, column=2, columnspan=1, padx=5, pady=5, sticky=W+E)
        apply_button.bind("<Enter>", apply_button_hover)
        apply_button.bind("<Leave>", apply_button_hover_leave)

        # Audio Bitrate Selection
        acodec_bitrate = StringVar(audio_window)
        acodec_bitrate_choices = [ '192k' ,'224k', '384k' ,'448k', '640k' ]
        acodec_bitrate.set('224k') # set the default option
        abitrate_menu_label = Label(audio_window, text="Bitrate :")
        abitrate_menu_label.grid(row=0, column=2, columnspan=1, padx=10, pady=5)
        abitrate_menu = OptionMenu(audio_window, acodec_bitrate, *acodec_bitrate_choices)
        abitrate_menu.grid(row=1, column=2, columnspan=1, padx=10, pady=10)

        # Audio Stream Selection
        acodec_stream = StringVar(audio_window)
        acodec_stream_choices = {'Track 1': "-map 0:a:0",
                                 'Track 2': "-map 0:a:1",
                                 'Track 3': "-map 0:a:2",
                                 'Track 4': "-map 0:a:3",
                                 'Track 5': "-map 0:a:4",
                                 'Track 6': "-map 0:a:5",
                                 'Track 7': "-map 0:a:6",
                                 'Track 8': "-map 0:a:7",
                                 'Track 9': "-map 0:a:8",
                                 'Track 10': "-map 0:a:9",
                                   }
        acodec_stream.set('Track 1') # set the default option
        acodec_stream_label = Label(audio_window, text="Track :")
        acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=5, pady=5)
        acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
        acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=5, pady=5)

        # Audio Channel Selection
        acodec_channel = StringVar(audio_window)
        acodec_channel_choices = { 'Original': "Original",
                                   '1 (Mono)': "1",
                                   '2 (Stereo)': "2",
                                   '5.1 (Surround)': "6",
                                   '6.1 (Surround)': "7",
                                   '7.1 (Surround)': "8"
                                   }
        acodec_channel.set('Original') # set the default option
        achannel_menu_label = Label(audio_window, text="Channels :")
        achannel_menu_label.grid(row=0, column=1, columnspan=1, padx=5, pady=5)
        achannel_menu = OptionMenu(audio_window, acodec_channel, *acodec_channel_choices.keys())
        achannel_menu.grid(row=1, column=1, columnspan=1, padx=5, pady=10)

    # AAC Window -----------------------
    elif encoder.get() == "AAC":
        audio_window = Toplevel()
        audio_window.title('AAC Settings')
        audio_window.configure(background="#434547")
        window_height = 175
        window_width = 358
        screen_width = audio_window.winfo_screenwidth()
        screen_height = audio_window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        def apply_button_hover(e):
            apply_button["bg"] = "white"
        def apply_button_hover_leave(e):
            apply_button["bg"] = "SystemButtonFace"

        def gotosavefile():
            audio_window.destroy()
            output_button.config(state=NORMAL)

        apply_button = Button(audio_window, text="Apply", command=gotosavefile)
        apply_button.grid(row=3, column=2, columnspan=1, padx=5, pady=5, sticky=W+E)
        apply_button.bind("<Enter>", apply_button_hover)
        apply_button.bind("<Leave>", apply_button_hover_leave)

        # Audio Bitrate Menu
        acodec_bitrate = StringVar(audio_window)
        acodec_bitrate_choices = {'CBR: 16k': '-b:a 16k',
                                  'CBR: 32k': '-b:a 32k',
                                  'CBR: 64k': '-b:a 64k',
                                  'CBR: 128k': '-b:a 128k',
                                  'CBR: 192k': '-b:a 192k',
                                  'CBR: 256k': '-b:a 256k',
                                  'CBR: 320k': '-b:a 320k',
                                  'CBR: 448k': '-b:a 44kk',
                                  'VBR: 1': '-q:a 1',
                                  'VBR: 2': '-q:a 2',
                                  'VBR: 3': '-q:a 3',
                                  'VBR: 4': '-q:a 4',
                                  'VBR: 5': '-q:a 5',
                                  'VBR: 6': '-q:a 6',
                                  'VBR: 7': '-q:a 7',
                                  }
        acodec_bitrate.set('CBR: 192k')  # set the default option
        abitrate_menu_label = Label(audio_window, text="Quality :")
        abitrate_menu_label.grid(row=0, column=2, columnspan=1, padx=5, pady=5)
        abitrate_menu = OptionMenu(audio_window, acodec_bitrate, *acodec_bitrate_choices)
        abitrate_menu.grid(row=1, column=2, columnspan=1, padx=5, pady=5)

        # Audio Channel Selection
        acodec_channel = StringVar(audio_window)
        acodec_channel_choices = { 'Original': "Original",
                                   '1 (Mono)': "1",
                                   '2 (Stereo)': "2",
                                   '5.1 (Surround)': "6",
                                   '6.1 (Surround)': "7",
                                   '7.1 (Surround)': "8"
                                   }
        acodec_channel.set('Original') # set the default option
        achannel_menu_label = Label(audio_window, text="Channels :")
        achannel_menu_label.grid(row=0, column=1, columnspan=1, padx=5, pady=5)
        achannel_menu = OptionMenu(audio_window, acodec_channel, *acodec_channel_choices.keys())
        achannel_menu.grid(row=1, column=1, columnspan=1, padx=5, pady=10)

        # Audio Stream Selection
        acodec_stream = StringVar(audio_window)
        acodec_stream_choices = {'Track 1': "-map 0:a:0",
                                 'Track 2': "-map 0:a:1",
                                 'Track 3': "-map 0:a:2",
                                 'Track 4': "-map 0:a:3",
                                 'Track 5': "-map 0:a:4",
                                 'Track 6': "-map 0:a:5",
                                 'Track 7': "-map 0:a:6",
                                 'Track 8': "-map 0:a:7",
                                 'Track 9': "-map 0:a:8",
                                 'Track 10': "-map 0:a:9",
                                   }
        acodec_stream.set('Track 1') # set the default option
        acodec_stream_label = Label(audio_window, text="Track :")
        acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=5, pady=5)
        acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
        acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=5, pady=5)

        # Audio Stream Selection
        acodec_gain = StringVar(audio_window)
        acodec_gain_choices = {'Default (0)': "-sn -vn -map_chapters -1",
                               '+10 dB': "-af volume=10dB -sn -vn -map_chapters -1",
                               '+9 dB': "-af volume=9dB -sn -vn -map_chapters -1",
                               '+8 dB': "-af volume=8dB -sn -vn -map_chapters -1",
                               '+7 dB': "-af volume=7dB -sn -vn -map_chapters -1",
                               '+6 dB': "-af volume=6dB -sn -vn -map_chapters -1",
                               '+5 dB': "-af volume=5dB -sn -vn -map_chapters -1",
                               '+4 dB': "-af volume=4dB -sn -vn -map_chapters -1",
                               '+3 dB': "-af volume=3dB -sn -vn -map_chapters -1",
                               '+2 dB': "-af volume=2dB -sn -vn -map_chapters -1",
                               '+1 dB': "-af volume=1dB -sn -vn -map_chapters -1",
                               '-1 dB': "-af volume=-1dB -sn -vn -map_chapters -1",
                               '-2 dB': "-af volume=-2dB -sn -vn -map_chapters -1",
                               '-3 dB': "-af volume=-3dB -sn -vn -map_chapters -1",
                               '-4 dB': "-af volume=-4dB -sn -vn -map_chapters -1",
                               '-5 dB': "-af volume=-5dB -sn -vn -map_chapters -1",
                               '-6 dB': "-af volume=-6dB -sn -vn -map_chapters -1",
                               '-7 dB': "-af volume=-7dB -sn -vn -map_chapters -1",
                               '-8 dB': "-af volume=-8dB -sn -vn -map_chapters -1",
                               '-9 dB': "-af volume=-9dB -sn -vn -map_chapters -1",
                               '-10 dB': "-af volume=-10dB -sn -vn -map_chapters -1",
                               }
        acodec_gain.set('Default (0)') # set the default option
        acodec_gain_label = Label(audio_window, text="Gain :")
        acodec_gain_label.grid(row=2, column=0, columnspan=1, padx=5, pady=5)
        acodec_gain_menu = OptionMenu(audio_window, acodec_gain, *acodec_gain_choices.keys())
        acodec_gain_menu.grid(row=3, column=0, columnspan=1, padx=5, pady=5)

        # DTS Window ---------------------------------------------------------

    elif encoder.get() == "DTS":
        audio_window = Toplevel()
        audio_window.title('DTS Settings')
        audio_window.configure(background="#646464")
        window_height = 136
        window_width = 276
        screen_width = audio_window.winfo_screenwidth()
        screen_height = audio_window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        def apply_button_hover(e):
            apply_button["bg"] = "white"

        def apply_button_hover_leave(e):
            apply_button["bg"] = "SystemButtonFace"

        def gotosavefile():
            audio_window.destroy()
            output_button.config(state=NORMAL)

        apply_button = Button(audio_window, text="Apply", command=gotosavefile)
        apply_button.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky=W + E)
        apply_button.bind("<Enter>", apply_button_hover)
        apply_button.bind("<Leave>", apply_button_hover_leave)

        # Audio Stream Selection
        acodec_stream = StringVar(audio_window)
        acodec_stream_choices = {'Track 1': "-map 0:a:0",
                                 'Track 2': "-map 0:a:1",
                                 'Track 3': "-map 0:a:2",
                                 'Track 4': "-map 0:a:3",
                                 'Track 5': "-map 0:a:4",
                                 'Track 6': "-map 0:a:5",
                                 'Track 7': "-map 0:a:6",
                                 'Track 8': "-map 0:a:7",
                                 'Track 9': "-map 0:a:8",
                                 'Track 10': "-map 0:a:9",
                                 }
        acodec_stream.set('Track 1')  # set the default option
        acodec_stream_label = Label(audio_window, text="Track :")
        acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=5, pady=5)
        acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
        acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=5, pady=5)

        # DTS Setting(s)
        dts_settings = StringVar(audio_window)
        dts_settings_choices = {'Reduce to Core': "-bsf:a dca_core -c:a copy",
                                  'Extract HD Track': "-c:a copy",
                                  }
        dts_settings.set('Reduce to Core')  # set the default option
        dts_settings_label = Label(audio_window, text="DTS Settings :")
        dts_settings_label.grid(row=0, column=1, columnspan=1, padx=5, pady=5)
        dts_settings_menu = OptionMenu(audio_window, dts_settings, *dts_settings_choices.keys())
        dts_settings_menu.grid(row=1, column=1, columnspan=1, padx=5, pady=10)

# Code------------------------------------------------------------------------

def file_input():
    global VideoInput
    VideoInput = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                            filetypes=(("MKV, MP4, DTS", "*.mp4 *.mkv *.dts"), ("All Files", "*.*")))
    input_entry.delete(0, END)  # Remove current text in entry
    input_entry.insert(0, VideoInput)  # Insert the 'path'
    if not VideoInput:
        output_button.config(state=DISABLED)
        show_streams_button.config(state=DISABLED)
        encoder_menu.config(state=DISABLED)
        encoder_menu.config(encoder.set("Choose Codec"))
    else:
        # output_button.config(state=NORMAL)
        show_streams_button.config(state=NORMAL)
        encoder_menu.config(state=NORMAL)

def file_save():
    global VideoOutput
    if encoder.get() == "AAC":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".mp4", initialdir="/",
                                                   title="Select a Save Location",
                                                   filetypes=(("AAC", "*.mp4"), ("All Files", "*.*")))
    elif encoder.get() == "AC3":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".ac3", initialdir="/",
                                                   title="Select a Save Location",
                                                   filetypes=(("AC3", "*.ac3"), ("All Files", "*.*")))
    elif encoder.get() == "DTS":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".dts", initialdir="/",
                                                   title="Select a Save Location",
                                                   filetypes=(("DTS", "*.dts"), ("All Files", "*.*")))
    output_entry.delete(0, END)  # Remove current text in entry
    output_entry.insert(0, VideoOutput)  # Insert the 'path'
    if not VideoOutput:
        start_audio_button.config(state=DISABLED)
    else:
        start_audio_button.config(state=NORMAL)

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

def encoder_menu_hover(e):
    encoder_menu["bg"] = "grey"
    encoder_menu["activebackground"] = "grey"
def encoder_menu_hover_leave(e):
    encoder_menu["bg"] = "#23272A"

button_status_label = Label(root, relief=SUNKEN)

# Job Buttons ---------------------------------------------------------

def startaudiojob():
    # Quote File Input/Output Paths--------------
    VideoInputQuoted = '"' + VideoInput + '"'
    VideoOutputQuoted = '"' + VideoOutput + '"'
    # Commands------------------------------------
    if encoder.get() == "AC3":
        if acodec_channel.get() == 'Original':
            commands = ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + " " + acodec_stream_choices[acodec_stream.get()] + " -c:a " + encoder_dropdownmenu_choices[encoder.get()] + " -b:a " + acodec_bitrate.get() + " -sn -vn -map_chapters -1 " + VideoOutputQuoted + " -hide_banner -v error -stats"
            subprocess.Popen(commands)
        else:
            commands = ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + " " + acodec_stream_choices[acodec_stream.get()] + " -c:a " + encoder_dropdownmenu_choices[encoder.get()] + " -b:a " + acodec_bitrate.get() + " -ac " + acodec_channel_choices[acodec_channel.get()] + " -sn -vn -map_chapters -1 " + VideoOutputQuoted + " -hide_banner -v error -stats"
            subprocess.Popen(commands)

    if encoder.get() == "AAC":
        if acodec_channel.get() == 'Original':
            commands = ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + " " + acodec_stream_choices[acodec_stream.get()] + " -c:a " + encoder_dropdownmenu_choices[encoder.get()] + " " + acodec_bitrate_choices[acodec_bitrate.get()] + " " + acodec_gain_choices[acodec_gain.get()] + " " + VideoOutputQuoted + " -hide_banner -v error -stats"
            subprocess.Popen(commands)
        else:
            commands = ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + " " + acodec_stream_choices[acodec_stream.get()] + " -c:a " + encoder_dropdownmenu_choices[encoder.get()] + " " + acodec_bitrate_choices[acodec_bitrate.get()] + " -ac " + acodec_channel_choices[acodec_channel.get()] + " " + acodec_gain_choices[acodec_gain.get()] + " " + VideoOutputQuoted + " -hide_banner -v error -stats"
            subprocess.Popen(commands)

    elif encoder.get() == 'DTS':
        commands = ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + " " + acodec_stream_choices[acodec_stream.get()] + " " + dts_settings_choices[dts_settings.get()] + " -sn -vn -map_chapters -1 " + VideoOutputQuoted + " -hide_banner -v error -stats"
        subprocess.Popen(commands)

def ffprobe_start():
    VideoInputQuoted = '"' + VideoInput + '"'
    MediaInfoQuoted = '"' + mediainfo + '"'
    commands = MediaInfoQuoted + " " + VideoInputQuoted
    subprocess.Popen(commands)

# Buttons Main Gui -------------------------------------------------

encoder_menu.bind("<Enter>", encoder_menu_hover)
encoder_menu.bind("<Leave>", encoder_menu_hover_leave)

show_streams_button = Button(root, text="MediaInfo", command=ffprobe_start, state=DISABLED, foreground="white", background="#23272A", borderwidth="3")
show_streams_button.grid(row=1, column=0, columnspan=1, padx=5, pady=5)
show_streams_button.bind("<Enter>", show_streams_button_hover)
show_streams_button.bind("<Leave>", show_streams_button_hover_leave)

# Audio Encoding Button
def enableordisable(*args):
    update_button = encoder.get()
    if update_button == "Choose Codec":
        audiosettings_button.config(state=DISABLED)
    else:
        audiosettings_button.config(state=NORMAL)
audiosettings_button = Button(root, text="Audio Settings", command=openaudiowindow, foreground="white", background="#23272A", state=DISABLED, borderwidth="3")
audiosettings_button.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky=W+E)
audiosettings_button.bind("<Enter>", audiosettings_button_hover)
audiosettings_button.bind("<Leave>", audiosettings_button_hover_leave)
encoder.trace('w', enableordisable)

input_button = Button(root, text="Open File", command=file_input, foreground="white", background="#23272A", borderwidth="3")
input_button.grid(row=0, column=0, columnspan=1, padx=5, pady=5)
input_entry = Entry(root, width=35, borderwidth=4, background="#CACACA")
input_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5)
input_button.bind("<Enter>", input_button_hover)
input_button.bind("<Leave>", input_button_hover_leave)

output_button = Button(root, text="Save File", command=file_save, state=DISABLED, foreground="white", background="#23272A", borderwidth="3")
output_button.grid(row=2, column=0, columnspan=1, padx=5, pady=5)
output_entry = Entry(root, width=35, borderwidth=4, background="#CACACA")
output_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5)
output_button.bind("<Enter>", output_button_hover)
output_button.bind("<Leave>", output_button_hover_leave)

# Start Audio Job
start_audio_button = Button(root, text="Start Audio Job", command=startaudiojob, state=DISABLED, foreground="white", background="#23272A", borderwidth="3")
start_audio_button.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky=W+E)
start_audio_button.bind("<Enter>", start_audio_button_hover)
start_audio_button.bind("<Leave>", start_audio_button_hover_leave)

# End Loop -----------------------------------------------------------------------
root.mainloop()
