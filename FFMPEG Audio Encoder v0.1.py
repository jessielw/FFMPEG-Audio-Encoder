# Imports--------------------------------------------------------------------
from tkinter import *
# from PIL import ImageTk,Image
from tkinter import filedialog
# import subprocess
import os

# Main Gui(s)
root = Tk()
root.title("jlw's FFMPEG Alpha")
root.iconbitmap(r'C:\Users\jlw_4\PycharmProjects\Draft\reaper.ico')
root.geometry("410x300")


# Code------------------------------------------------------------------------

def file_input():
    global VideoInput
    VideoInput = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                            filetypes=(("MKV, MP4", "*.mp4 *.mkv"), ("All Files", "*.*")))
    # video_input_label = Label(root, text=VideoInput).grid(row=0, column=1, columnspan=3, padx=10, pady=10)
    input_entry.delete(0, END)  # Remove current text in entry
    input_entry.insert(0, VideoInput)  # Insert the 'path'


def file_save():
    global VideoOutput
    VideoOutput = filedialog.asksaveasfilename(initialdir="/", title="Select a Save Location",
                                               filetypes=(("MP4", "*.mp4"), ("All Files", "*.*")))
    #video_output_label = Label(root, text=str(VideoOutput)).pack()
    output_entry.delete(0, END)  # Remove current text in entry
    output_entry.insert(0, VideoOutput)  # Insert the 'path'

# Variables

acodec = StringVar(root)
acodec_choices = { 'aac','ac3' }
acodec.set('aac') # set the default option

acodec_bitrate = StringVar(root)
acodec_bitrate_choices = { '160k' ,'320k' }
acodec_bitrate.set('160k') # set the default option

acodec_channel = StringVar(root)
acodec_channel_choices = { '2' ,'6' }
acodec_channel.set('2') # set the default option

# Job Start
def start(): #final command of start button
    os.system(" ffmpeg -i " + VideoInput + " -c:v copy -c:a " + acodec.get() + " -b:a " + acodec_bitrate.get() + " -ac " + acodec_channel.get() + " " + VideoOutput)

# Buttons, Option Menus ----------------------------------------------------

input_button = Button(root, text="Open File", command=file_input)
input_button.grid(row=0, column=0, columnspan=1, padx=10, pady=10)
input_entry = Entry(root, width=35, borderwidth=5)
input_entry.grid(row=0, column=1, columnspan=3, padx=10, pady=10)

output_button = Button(root, text="Save File", command=file_save)
output_button.grid(row=1, column=0, columnspan=1, padx=10, pady=10)
output_entry = Entry(root, width=35, borderwidth=5)
output_entry.grid(row=1, column=1, columnspan=3, padx=10, pady=10)

audio_menu = OptionMenu(root, acodec, *acodec_choices)
audio_menu.grid(row=2, column=0, columnspan=1, padx=10, pady=10)

abitrate_menu = OptionMenu(root, acodec_bitrate, *acodec_bitrate_choices)
abitrate_menu.grid(row=2, column=1, columnspan=1, padx=10, pady=10)

achannel_menu = OptionMenu(root, acodec_channel, *acodec_channel_choices)
achannel_menu.grid(row=2, column=2, columnspan=1, padx=10, pady=10)

start_button = Button(root, text="Start Job", command=start)
start_button.grid(row=3, column=0, columnspan=1, padx=10, pady=10)



# End Loop -----------------------------------------------------------------------
root.mainloop()
