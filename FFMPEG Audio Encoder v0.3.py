# Imports--------------------------------------------------------------------
from tkinter import *
# from PIL import ImageTk,Image
from tkinter import filedialog
import subprocess
import os
from tkinter import dnd

# Main Gui & Windows --------------------------------------------------------
root = Tk()
root.title("jlw's FFMPEG Alpha")
root.iconbitmap(r'C:\Users\jlw_4\PycharmProjects\Draft\reaper.ico')
root.geometry("490x300")
root.configure(background="#D9F1F1")

# Audio Codec Window ---------------------------------------------------------
def openaudiowindow():
    global acodec
    global acodec_bitrate
    global acodec_channel
    audio_window = Toplevel()
    audio_window.title('Audio Settings')
    audio_window.iconbitmap(r'C:\Users\jlw_4\PycharmProjects\Draft\reaper.ico')
    audio_window.geometry("370x150")
    audio_window.configure(background="#D9F1F1")

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
    acodec_choices = ['aac', 'ac3']
    acodec.set('aac')  # set the default option
    audio_menu_label = Label(audio_window, text="Choose Codec :")
    audio_menu_label.grid(row=0, column=0, columnspan=1, padx=10, pady=5)
    audio_menu = OptionMenu(audio_window, acodec, *acodec_choices)
    audio_menu.grid(row=2, column=0, columnspan=1, padx=5, pady=1)

    # Audio Bitrate Menu
    acodec_bitrate = StringVar(audio_window)
    acodec_bitrate_choices = [ '160k' ,'320k' ]
    acodec_bitrate.set('160k') # set the default option
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

    # if acodec.get() == 'aac':
    #     print("True")
    # elif acodec.get() == 'ac3':
    #     print("False")


# Job Settings Window --------------------------------------------------------
def openjobsettingswindow():
    global jobstartsetting
    jobsettings_window = Toplevel()
    jobsettings_window.title('Job Settings')
    jobsettings_window.iconbitmap(r'C:\Users\jlw_4\PycharmProjects\Draft\reaper.ico')
    jobsettings_window.geometry("150x80")
    jobsettings_window.configure(background="#D9F1F1")

    jobstartsetting = StringVar(jobsettings_window)
    jobstartsetting_choices = ['powershell.exe', 'cmd.exe']
    jobstartsetting.set('powershell.exe')  # set the default option
    jobstartsetting_label = Label(jobsettings_window, text="Choose Shell :")
    jobstartsetting_label.grid(row=0, column=0, columnspan=1, padx=10, pady=5)
    jobstartsetting_menu = OptionMenu(jobsettings_window, jobstartsetting, *jobstartsetting_choices)
    jobstartsetting_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=5)



# Code------------------------------------------------------------------------

def file_input():
    global VideoInput
    VideoInput = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                            filetypes=(("MKV, MP4", "*.mp4 *.mkv"), ("All Files", "*.*")))
    input_entry.delete(0, END)  # Remove current text in entry
    input_entry.insert(0, VideoInput)  # Insert the 'path'


def file_save():
    global VideoOutput
    VideoOutput = filedialog.asksaveasfilename(initialdir="/", title="Select a Save Location",
                                               filetypes=(("MP4", "*.mp4"), ("All Files", "*.*")))
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

def audiosettings_button_hover(e):
    audiosettings_button["bg"] = "white"
def audiosettings_button_hover_leave(e):
    audiosettings_button["bg"] = "SystemButtonFace"

def start_button_powershell_hover(e):
    start_button_powershell["bg"] = "white"
def start_button_powershell_hover_leave(e):
    start_button_powershell["bg"] = "SystemButtonFace"

def start_button_commandprompt_hover(e):
    start_button_commandprompt["bg"] = "white"
def start_button_commandprompt_hover_leave(e):
    start_button_commandprompt["bg"] = "SystemButtonFace"

button_status_label = Label(root, relief=SUNKEN)


def start_powershell(): #final command of start button
    subprocess.Popen("powershell.exe -NoExit " + "ffmpeg -i " + VideoInput + " -c:v copy -c:a " + acodec.get() + " -b:a " + acodec_bitrate.get() + " -ac " + acodec_channel.get() + " " + VideoOutput)

def start_commandprompt(): #final command of start button
    subprocess.Popen("ffmpeg -i " + VideoInput + " -c:v copy -c:a " + acodec.get() + " -b:a " + acodec_bitrate.get() + " -ac " + acodec_channel.get() + " " + VideoOutput)

# Buttons Main Gui -------------------------------------------------

audiosettings_button = Button(root, text="Audio Settings", command=openaudiowindow)
audiosettings_button.grid(row=2, column=0, columnspan=1, padx=10, pady=10)
audiosettings_button.bind("<Enter>", audiosettings_button_hover)
audiosettings_button.bind("<Leave>", audiosettings_button_hover_leave)

jobsettings_button = Button(root, text="Job Settings", command=openjobsettingswindow)
jobsettings_button.grid(row=2, column=1, columnspan=1, padx=10, pady=10)

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

# Start Powershell
start_button_powershell = Button(root, text="Start PowerShell", command=start_powershell)
start_button_powershell.grid(row=3, column=0, columnspan=1, padx=10, pady=10)
start_button_powershell.bind("<Enter>", start_button_powershell_hover)
start_button_powershell.bind("<Leave>", start_button_powershell_hover_leave)

# Start CommandPrompt
start_button_commandprompt = Button(root, text="Start CMD", command=start_commandprompt)
start_button_commandprompt.grid(row=3, column=1, columnspan=1, padx=10, pady=10)
start_button_commandprompt.bind("<Enter>", start_button_commandprompt_hover)
start_button_commandprompt.bind("<Leave>", start_button_commandprompt_hover_leave)



# End Loop -----------------------------------------------------------------------
root.mainloop()
