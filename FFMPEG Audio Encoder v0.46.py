# Imports--------------------------------------------------------------------

from tkinter import *
from tkinter import filedialog
import subprocess

# Main Gui & Windows --------------------------------------------------------

root = Tk()
root.title("FFMPEG Audio Encoder Alpha v0.46")
root.iconbitmap(r'C:\Users\jlw_4\PycharmProjects\Draft\reaper.ico')
root.geometry("460x260")
root.configure(background="#DEF2F2")

# Menu Bar ------------------------------------------------------------------

my_menu = Menu(root, tearoff=0)
root.config(menu=my_menu)

# About Window ---------------------------------------------------------------

def openaboutwindow():
    about_window = Toplevel()
    about_window.title('About')
    about_window.iconbitmap(r'C:\Users\jlw_4\PycharmProjects\Draft\reaper.ico')
    about_window.geometry("370x150")
    about_window.configure(background="#DEF2F2")
    about_window_label = Label(about_window, text="About Text Will Go Here Eventually...")
    about_window_label.grid(row=3, column=1, columnspan=1, padx=10, pady=10)

# Menu Items and Sub-Bars ----------------------------------------------------

shell = StringVar()
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

# Video Codec Window ---------------------------------------------------------

vcodec = StringVar()
vcodec.set('-c:v copy')

def openvideowindow():
    global vcodec
    global vcodec_bitrate
    video_window = Toplevel()
    video_window.title('Video Settings')
    video_window.iconbitmap(r'C:\Users\jlw_4\PycharmProjects\Draft\reaper.ico')
    video_window.geometry("370x150")
    video_window.configure(background="#DEF2F2")

    def apply_button_hover(e):
        apply_button["bg"] = "white"
    def apply_button_hover_leave(e):
        apply_button["bg"] = "SystemButtonFace"

    apply_button = Button(video_window, text="Apply", command=video_window.destroy)
    apply_button.grid(row=3, column=1, columnspan=1, padx=10, pady=10)
    apply_button.bind("<Enter>", apply_button_hover)
    apply_button.bind("<Leave>", apply_button_hover_leave)

    # Video Codec Menu
    vcodec = StringVar(video_window)
    vcodec_choices = {
        "Copy": "-c:v copy",
        "x264": "-c:v libx264",
        "x265": "-c:v libx265"
    }
    vcodec.set('-c:v copy')
    video_menu_label = Label(video_window, text="Choose Codec :")
    video_menu_label.grid(row=0, column=0, columnspan=1, padx=10, pady=5)
    video_menu = OptionMenu(video_window, vcodec, *vcodec_choices.values())
    video_menu.grid(row=2, column=0, columnspan=1, padx=5, pady=1)

# Audio Codec Window ---------------------------------------------------------

acodec = StringVar()
acodec.set('aac')  # set the default option
acodec_bitrate = StringVar()
acodec_bitrate.set('160k') # set the default option
acodec_channel = StringVar()
acodec_channel.set('2')

def openaudiowindow():
    global acodec
    global acodec_bitrate
    global acodec_channel
    audio_window = Toplevel()
    audio_window.title('Audio Settings')
    audio_window.iconbitmap(r'C:\Users\jlw_4\PycharmProjects\Draft\reaper.ico')
    audio_window.geometry("370x150")
    audio_window.configure(background="#DEF2F2")

    def apply_button_hover(e):
        apply_button["bg"] = "white"
    def apply_button_hover_leave(e):
        apply_button["bg"] = "SystemButtonFace"

    apply_button = Button(audio_window, text="Apply", command=audio_window.destroy)
    apply_button.grid(row=3, column=1, columnspan=1, padx=10, pady=10)
    apply_button.bind("<Enter>", apply_button_hover)
    apply_button.bind("<Leave>", apply_button_hover_leave)

    # Audio Codec Menu
    acodec = StringVar(audio_window)
    acodec_choices = {'AAC' : 'aac', 'AC3' : 'ac3'}
    acodec.set('aac')  # set the default option
    audio_menu_label = Label(audio_window, text="Choose Codec :")
    audio_menu_label.grid(row=0, column=0, columnspan=1, padx=10, pady=5)
    audio_menu = OptionMenu(audio_window, acodec, *acodec_choices.values())
    audio_menu.grid(row=2, column=0, columnspan=1, padx=5, pady=1)

    # Audio Bitrate Menu

    acodec_bitrate = StringVar(audio_window)
    acodec_bitrate_choices = [ '192k' ,'224k', '384k' ,'448k', '640k' ]
    acodec_bitrate.set('192k') # set the default option
    abitrate_menu_label = Label(audio_window, text="Choose Bitrate :")
    abitrate_menu_label.grid(row=0, column=1, columnspan=1, padx=10, pady=5)
    abitrate_menu = OptionMenu(audio_window, acodec_bitrate, *acodec_bitrate_choices)
    abitrate_menu.grid(row=2, column=1, columnspan=1, padx=10, pady=10)

    # Audio Channel Menu
    acodec_channel = StringVar(audio_window)
    acodec_channel_choices = [ '2' ,'6' ]
    acodec_channel.set('2') # set the default option
    achannel_menu_label = Label(audio_window, text="Choose Channel :")
    achannel_menu_label.grid(row=0, column=2, columnspan=1, padx=10, pady=5)
    achannel_menu = OptionMenu(audio_window, acodec_channel, *acodec_channel_choices)
    achannel_menu.grid(row=2, column=2, columnspan=1, padx=10, pady=10)

# Code------------------------------------------------------------------------

def file_input():
    global VideoInput
    VideoInput = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                            filetypes=(("MKV, MP4", "*.mp4 *.mkv"), ("All Files", "*.*")))
    input_entry.delete(0, END)  # Remove current text in entry
    input_entry.insert(0, VideoInput)  # Insert the 'path'


def file_save():
    global VideoOutput
    VideoOutput = filedialog.asksaveasfilename(defaultextension=".mkv", initialdir="/", title="Select a Save Location",
                                               filetypes=(("MKV", "*.mkv"), ("MP4", "*.mp4"), ("All Files", "*.*")))
    output_entry.delete(0, END)  # Remove current text in entry
    output_entry.insert(0, VideoOutput)  # Insert the 'path'

def input_button_hover(e):
    input_button["bg"] = "white"
def input_button_hover_leave(e):
    input_button["bg"] = "SystemButtonFace"

def output_button_hover(e):
    output_button["bg"] = "white"
def output_button_hover_leave(e):
    output_button["bg"] = "SystemButtonFace"

def videosettings_button_hover(e):
    videosettings_button["bg"] = "white"
def videosettings_button_hover_leave(e):
    videosettings_button["bg"] = "SystemButtonFace"

def audiosettings_button_hover(e):
    audiosettings_button["bg"] = "white"
def audiosettings_button_hover_leave(e):
    audiosettings_button["bg"] = "SystemButtonFace"

button_status_label = Label(root, relief=SUNKEN)

def start(): #final command of start button
    subprocess.Popen(shell.get() + " " + "ffmpeg -i " + repr(VideoInput) + " " + vcodec.get() + " -c:a " + acodec.get() + " -b:a " + acodec_bitrate.get() + " -ac " + acodec_channel.get() + " " + repr(VideoOutput))

# Buttons Main Gui -------------------------------------------------

videosettings_button = Button(root, text="Video Settings", command=openvideowindow)
videosettings_button.grid(row=2, column=1, columnspan=1, padx=10, pady=10)
videosettings_button.bind("<Enter>", videosettings_button_hover)
videosettings_button.bind("<Leave>", videosettings_button_hover_leave)

audiosettings_button = Button(root, text="Audio Settings", command=openaudiowindow)
audiosettings_button.grid(row=2, column=0, columnspan=1, padx=10, pady=10)
audiosettings_button.bind("<Enter>", audiosettings_button_hover)
audiosettings_button.bind("<Leave>", audiosettings_button_hover_leave)

input_button = Button(root, text="Open File", command=file_input)
input_button.grid(row=0, column=0, columnspan=1, padx=10, pady=10)
input_entry = Entry(root, width=35, borderwidth=5)
input_entry.grid(row=0, column=1, columnspan=3, padx=10, pady=10)
input_button.bind("<Enter>", input_button_hover)
input_button.bind("<Leave>", input_button_hover_leave)

output_button = Button(root, text="Save File", command=file_save)
output_button.grid(row=1, column=0, columnspan=1, padx=10, pady=10)
output_entry = Entry(root, width=35, borderwidth=5)
output_entry.grid(row=1, column=1, columnspan=3, padx=10, pady=10)
output_button.bind("<Enter>", output_button_hover)
output_button.bind("<Leave>", output_button_hover_leave)

#Start Job
start_button = Button(root, text="Start Job", command=start)
start_button.grid(row=3, column=0, columnspan=1, padx=10, pady=10)

# End Loop -----------------------------------------------------------------------
root.mainloop()
