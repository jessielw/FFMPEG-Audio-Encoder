# Imports--------------------------------------------------------------------

from tkinter import *
from tkinter import filedialog, StringVar
import subprocess
import os

# Main Gui & Windows --------------------------------------------------------

root = Tk()
root.title("FFMPEG Audio Encoder Alpha v0.51")
root.iconbitmap(r'C:\Users\jlw_4\PycharmProjects\Draft\reaper.ico')
root.geometry("380x195")
root.configure(background="#646464")

# Menu Bar ------------------------------------------------------------------

my_menu = Menu(root, tearoff=0)
root.config(menu=my_menu)

# About Window ---------------------------------------------------------------

def openaboutwindow():
    about_window = Toplevel()
    about_window.title('About')
    about_window.iconbitmap(r'C:\Users\jlw_4\PycharmProjects\Draft\reaper.ico')
    about_window.geometry("370x150")
    about_window.configure(background="#646464")
    about_window_label = Label(about_window, text="About Text Will Go Here Eventually...")
    about_window_label.grid(row=3, column=1, columnspan=1, padx=10, pady=10)

# Menu Items and Sub-Bars ----------------------------------------------------

shell: StringVar = StringVar()
shell.set("powershell.exe") #Default

file_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=root.quit)

edit_menu = Menu(my_menu, tearoff=0)
shellmenu = Menu(my_menu, tearoff=0)
shellmenu.add_radiobutton(label="PowerShell", value="powershell.exe", variable=shell)
shellmenu.add_radiobutton(label="Command Prompt", value="cmd", variable=shell)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_cascade(label="Shell", menu=shellmenu)

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
encoder_menu = OptionMenu(root, encoder, *encoder_dropdownmenu_choices.values())
encoder_menu.grid(row=1, column=1, columnspan=1, padx=5, pady=5, sticky=W+E)
encoder_menu.config(state=DISABLED)

# Audio Codec Window ---------------------------------------------------------

# acodec = StringVar()
# acodec_bitrate = StringVar()
# acodec_bitrate.set('160k') # set the default option
# acodec_channel = StringVar()
# acodec_channel.set('2')

def openaudiowindow():
    global acodec
    global acodec_bitrate
    global acodec_channel
    if encoder.get() == "ac3":
        audio_window = Toplevel()
        audio_window.title('AC3 Settings')
        audio_window.iconbitmap(r'C:\Users\jlw_4\PycharmProjects\Draft\reaper.ico')
        audio_window.geometry("335x90")
        audio_window.configure(background="#646464")

        def apply_button_hover(e):
            apply_button["bg"] = "white"
        def apply_button_hover_leave(e):
            apply_button["bg"] = "SystemButtonFace"

        apply_button = Button(audio_window, text="Apply", command=audio_window.destroy)
        apply_button.grid(row=3, column=1, columnspan=1, padx=10, pady=10)
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
        acodec_stream_choices = {'Track 1' : '-map 0:a:0',
                                 'Track 2' : '-map 0:a:1',
                                 'Track 3' : '-map 0:a:2',
                                 'Track 4' : '-map 0:a:3',
                                 'Track 5' : '-map 0:a:4',
                                 'Track 6' : '-map 0:a:5',
                                 'Track 7' : '-map 0:a:6',
                                 'Track 8' : '-map 0:a:7',
                                 'Track 9' : '-map 0:a:8',
                                 'Track 10' : '-map 0:a:9',
                                   }
        acodec_stream.set('-map 0:a:0') # set the default option
        acodec_stream_label = Label(audio_window, text="Track :")
        acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=5, pady=5)
        acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices)
        acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=5, pady=5)

        # Audio Channel Selection
        acodec_channel = StringVar(audio_window)
        acodec_channel_choices = { '1 (Mono)' : '1',
                                   '2 (Stereo)' : '2',
                                   '5.1' : '6',
                                   '6.1' : '7',
                                   '7.1' : '8'
                                   }
        acodec_channel.set('2') # set the default option
        achannel_menu_label = Label(audio_window, text="Channels :")
        achannel_menu_label.grid(row=0, column=1, columnspan=1, padx=5, pady=5)
        achannel_menu = OptionMenu(audio_window, acodec_channel, *acodec_channel_choices)
        achannel_menu.grid(row=1, column=1, columnspan=1, padx=5, pady=10)

    elif encoder.get() == "aac":
        audio_window = Toplevel()
        audio_window.title('AAC Settings')
        audio_window.iconbitmap(r'C:\Users\jlw_4\PycharmProjects\Draft\reaper.ico')
        audio_window.geometry("340x100")
        audio_window.configure(background="#646464")

        def apply_button_hover(e):
            apply_button["bg"] = "white"

        def apply_button_hover_leave(e):
            apply_button["bg"] = "SystemButtonFace"

        apply_button = Button(audio_window, text="Apply", command=audio_window.destroy)
        apply_button.grid(row=3, column=1, columnspan=1, padx=10, pady=10)
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
        acodec_channel_choices = { '1 (Mono)' : '1',
                                   '2 (Stereo)' : '2',
                                   '5.1' : '6',
                                   '6.1' : '7',
                                   '7.1' : '8'
                                   }
        acodec_channel.set('2') # set the default option
        achannel_menu_label = Label(audio_window, text="Channels :")
        achannel_menu_label.grid(row=0, column=1, columnspan=1, padx=5, pady=5)
        achannel_menu = OptionMenu(audio_window, acodec_channel, *acodec_channel_choices)
        achannel_menu.grid(row=1, column=1, columnspan=1, padx=5, pady=10)

        # Audio Stream Selection
        acodec_stream = StringVar(audio_window)
        acodec_stream_choices = {'Track 1' : '-map 0:a:0',
                                 'Track 2' : '-map 0:a:1',
                                 'Track 3' : '-map 0:a:2',
                                 'Track 4' : '-map 0:a:3',
                                 'Track 5' : '-map 0:a:4',
                                 'Track 6' : '-map 0:a:5',
                                 'Track 7' : '-map 0:a:6',
                                 'Track 8' : '-map 0:a:7',
                                 'Track 9' : '-map 0:a:8',
                                 'Track 10' : '-map 0:a:9',
                                   }
        acodec_stream.set('-map 0:a:0') # set the default option
        acodec_stream_label = Label(audio_window, text="Track :")
        acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=5, pady=5)
        acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices)
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
    if encoder.get() == "aac":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".mp4", initialdir="/",
                                                   title="Select a Save Location",
                                                   filetypes=(("AAC", "*.mp4"), ("All Files", "*.*")))
    elif encoder.get() == "ac3":
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
    VideoInputQuoted = '"' + VideoInput + '"'
    VideoOutputQuoted = '"' + VideoOutput + '"'
    subprocess.Popen(shell.get() + " ffmpeg -i " + VideoInputQuoted + " -c:a " + acodec.get() + " -b:a " + acodec_bitrate.get() + " -ac " + acodec_channel.get() + " -sn -vn " + VideoOutputQuoted)

# def start(): # Button to Encode
#     VideoInputQuoted = '"' + VideoInput + '"'
#     VideoOutputQuoted = '"' + VideoOutput + '"'
#     # Determine if user wants CMD or PowerShell
#     if shell.get() == "cmd":
#         subprocess.Popen(shell.get() + " /c " + "ffmpeg -i " + VideoInputQuoted + " " + vcodec.get() + " -c:a " + acodec.get() + " -b:a " + acodec_bitrate.get() + " -ac " + acodec_channel.get() + " " + VideoOutputQuoted)
#     elif shell.get() == "powershell.exe":
#         subprocess.Popen(shell.get() + " ffmpeg -i " + VideoInputQuoted + " " + vcodec.get() + " -c:a " + acodec.get() + " -b:a " + acodec_bitrate.get() + " -ac " + acodec_channel.get() + " " + VideoOutputQuoted)

def ffprobe_start():  # Start FFProbe based on cmd or powershell selection (Defualt is powershell)
    ffprobe_command_1 = "ffprobe.exe -v error -hide_banner -select_streams a -show_entries "
    ffprobe_command_2 = "stream=index,codec_name,bit_rate,channels,sample_rate:format=duration:format_tags:stream_tags"
    ffprobe_command_2_quoted = '"' + ffprobe_command_2 + '"'
    ffprobe_command_3 = " -of default=noprint_wrappers=1"
    if shell.get() == "powershell.exe":
        VideoInputQuoted = '"' + VideoInput + '"' # Convert Variable with propper quotes
        subprocess.Popen(shell.get() + " -noexit" + " " + ffprobe_command_1 + " " + ffprobe_command_2_quoted + " " + ffprobe_command_3 + " " + VideoInputQuoted)
    elif shell.get() == "cmd":
        VideoInputQuoted = '"' + VideoInput + '"' # Convert Variable with propper quotes
        subprocess.Popen(shell.get() + " /k " + ffprobe_command_1 + " " + ffprobe_command_2_quoted + " " + ffprobe_command_3 + " " + VideoInputQuoted)

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
