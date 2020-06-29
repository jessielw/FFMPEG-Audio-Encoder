# Imports--------------------------------------------------------------------

from tkinter import *
from tkinter import filedialog, StringVar
import subprocess
import os

# Main Gui & Windows --------------------------------------------------------

root = Tk()
root.title("FFMPEG Audio Encoder Alpha Beta 1.0")
root.iconphoto(True, PhotoImage(file="C:/Users/jlw_4/Desktop/jlwFFMPEG.png"))
root.configure(background="#646464")
# root.resizable(False, False)  # This code helps to disable windows from resizing
window_height = 175
window_width = 380
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

file_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=root.quit)

edit_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Edit", menu=edit_menu)

help_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=openaboutwindow) # Possibly Expand This Later

# Encoder Codec Drop Down
encoder_dropdownmenu_choices = {
    "AC3" : "ac3",
    "AAC" : "aac"
}
encoder = StringVar(root)
encoder.set("Choose Codec")
encoder_menu = OptionMenu(root, encoder, *encoder_dropdownmenu_choices.keys())
encoder_menu.grid(row=1, column=1, columnspan=1, padx=5, pady=5, sticky=W+E)
encoder_menu.config(state=DISABLED)

# Audio Codec Window ---------------------------------------------------------

def openaudiowindow():
    global acodec_bitrate
    global acodec_channel
    global acodec_channel_choices
    global acodec_stream
    global acodec_stream_choices

    # AC3 Window ----------------------------
    if encoder.get() == "AC3":
        audio_window = Toplevel()
        audio_window.title('AC3 Settings')
        audio_window.configure(background="#646464")
        window_height = 140
        window_width = 350
        screen_width = audio_window.winfo_screenwidth()
        screen_height = audio_window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        def apply_button_hover(e):
            apply_button["bg"] = "white"
        def apply_button_hover_leave(e):
            apply_button["bg"] = "SystemButtonFace"

        apply_button = Button(audio_window, text="Apply", command=audio_window.destroy)
        apply_button.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky=W+E)
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
        acodec_channel.set("Original") # set the default option
        achannel_menu_label = Label(audio_window, text="Channels :")
        achannel_menu_label.grid(row=0, column=1, columnspan=1, padx=5, pady=5)
        achannel_menu = OptionMenu(audio_window, acodec_channel, *acodec_channel_choices.keys())
        achannel_menu.grid(row=1, column=1, columnspan=1, padx=5, pady=10)

    # AAC Window -----------------------
    elif encoder.get() == "AAC":
        audio_window = Toplevel()
        audio_window.title('AAC Settings')
        audio_window.configure(background="#646464")
        window_height = 135
        window_width = 305
        screen_width = audio_window.winfo_screenwidth()
        screen_height = audio_window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        def apply_button_hover(e):
            apply_button["bg"] = "white"

        def apply_button_hover_leave(e):
            apply_button["bg"] = "SystemButtonFace"

        apply_button = Button(audio_window, text="Apply", command=audio_window.destroy)
        apply_button.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky=W+E)
        apply_button.bind("<Enter>", apply_button_hover)
        apply_button.bind("<Leave>", apply_button_hover_leave)

        # Audio Bitrate Menu
        acodec_bitrate = StringVar(audio_window)
        acodec_bitrate_choices = ['16k', '32k', '64k', '128k', '192k', '256k', '320k', '448k', '640k']
        acodec_bitrate.set('192k')  # set the default option
        abitrate_menu_label = Label(audio_window, text="Bitrate :")
        abitrate_menu_label.grid(row=0, column=2, columnspan=1, padx=5, pady=5)
        abitrate_menu = OptionMenu(audio_window, acodec_bitrate, *acodec_bitrate_choices)
        abitrate_menu.grid(row=1, column=2, columnspan=1, padx=5, pady=5)

        # Audio Channel Selection
        acodec_channel = StringVar(audio_window)
        acodec_channel_choices = { '1 (Mono)': "1",
                                   '2 (Stereo)': "2",
                                   '5.1 (Surround)': "6",
                                   '6.1 (Surround)': "7",
                                   '7.1 (Surround)': "8"
                                   }
        acodec_channel.set('2 (Stereo)') # set the default option
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

# Code------------------------------------------------------------------------

def file_input():
    global VideoInput
    VideoInput = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                            filetypes=(("MKV, MP4", "*.mp4 *.mkv"), ("All Files", "*.*")))
    input_entry.delete(0, END)  # Remove current text in entry
    input_entry.insert(0, VideoInput)  # Insert the 'path'
    if not VideoInput:
        output_button.config(state=DISABLED)
        show_streams_button.config(state=DISABLED)
        encoder_menu.config(state=DISABLED)
        encoder_menu.config(encoder.set("Choose Codec"))
    else:
        output_button.config(state=NORMAL)
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
    output_entry.delete(0, END)  # Remove current text in entry
    output_entry.insert(0, VideoOutput)  # Insert the 'path'
    if not VideoOutput:
        start_audio_button.config(state=DISABLED)
    else:
        start_audio_button.config(state=NORMAL)

def input_button_hover(e):
    input_button["bg"] = "white"
def input_button_hover_leave(e):
    input_button["bg"] = "SystemButtonFace"

def output_button_hover(e):
    output_button["bg"] = "white"
def output_button_hover_leave(e):
    output_button["bg"] = "SystemButtonFace"

def audiosettings_button_hover(e):
    audiosettings_button["bg"] = "white"
def audiosettings_button_hover_leave(e):
    audiosettings_button["bg"] = "SystemButtonFace"

def show_streams_button_hover(e):
    show_streams_button["bg"] = "white"
def show_streams_button_hover_leave(e):
    show_streams_button["bg"] = "SystemButtonFace"

def start_audio_button_hover(e):
    start_audio_button["bg"] = "white"
def start_audio_button_hover_leave(e):
    start_audio_button["bg"] = "SystemButtonFace"

def encoder_menu_hover(e):
    encoder_menu["bg"] = "white"
def encoder_menu_hover_leave(e):
    encoder_menu["bg"] = "SystemButtonFace"

button_status_label = Label(root, relief=SUNKEN)

# Job Buttons ---------------------------------------------------------

def startaudiojob():
    if acodec_channel.get() == 'Original':
        commands = ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInput + " " + acodec_stream_choices[acodec_stream.get()] + " -c:a " + encoder_dropdownmenu_choices[encoder.get()] + " -b:a " + acodec_bitrate.get() + " -sn -vn " + VideoOutput + " -hide_banner -v error -stats"
        subprocess.Popen(commands)
    else:
        commands = ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInput + " " + acodec_stream_choices[acodec_stream.get()] + " -c:a " + encoder_dropdownmenu_choices[encoder.get()] + " -b:a " + acodec_bitrate.get() + " -ac " + acodec_channel_choices[acodec_channel.get()] + " -sn -vn " + VideoOutput + " -hide_banner -v error -stats"
        subprocess.Popen(commands)

def ffprobe_start():
    ffprobe_command_1 = "-v error -hide_banner -select_streams a -show_entries "
    ffprobe_command_2 = "stream=index,codec_name,bit_rate,channels,sample_rate:format=duration:format_tags:stream_tags"
    ffprobe_command_3 = " -of default=noprint_wrappers=1"
    commands = ffprobe + " " + ffprobe_command_1 + " " + ffprobe_command_2 + " " + ffprobe_command_3 + " " + VideoInput
    print(commands)
    subprocess.Popen(commands)

# Buttons Main Gui -------------------------------------------------

encoder_menu.bind("<Enter>", encoder_menu_hover)
encoder_menu.bind("<Leave>", encoder_menu_hover_leave)

show_streams_button = Button(root, text="Streams", command=ffprobe_start, state=DISABLED)
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
audiosettings_button = Button(root, text="Audio Settings", command=openaudiowindow, state=DISABLED)
audiosettings_button.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky=W+E)
audiosettings_button.bind("<Enter>", audiosettings_button_hover)
audiosettings_button.bind("<Leave>", audiosettings_button_hover_leave)
encoder.trace('w', enableordisable)

input_button = Button(root, text="Open File", command=file_input)
input_button.grid(row=0, column=0, columnspan=1, padx=5, pady=5)
input_entry = Entry(root, width=35, borderwidth=5)
input_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5)
input_button.bind("<Enter>", input_button_hover)
input_button.bind("<Leave>", input_button_hover_leave)

output_button = Button(root, text="Save File", command=file_save, state=DISABLED)
output_button.grid(row=2, column=0, columnspan=1, padx=5, pady=5)
output_entry = Entry(root, width=35, borderwidth=5)
output_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5)
output_button.bind("<Enter>", output_button_hover)
output_button.bind("<Leave>", output_button_hover_leave)

# Start Audio Job
start_audio_button = Button(root, text="Start Audio Job", command=startaudiojob, state=DISABLED)
start_audio_button.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky=W+E)
start_audio_button.bind("<Enter>", start_audio_button_hover)
start_audio_button.bind("<Leave>", start_audio_button_hover_leave)

# End Loop -----------------------------------------------------------------------
root.mainloop()
