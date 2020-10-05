# Imports--------------------------------------------------------------------

from tkinter import *
from tkinter import filedialog, StringVar
import subprocess
from tkinter import scrolledtext

# Main Gui & Windows --------------------------------------------------------

root = Tk()
root.title("Youtube-DL-Gui Beta v1.0")
root.iconphoto(True, PhotoImage(file="Runtime/Images/Youtube-DL-Gui.png"))
root.configure(background="#434547")
window_height = 380
window_width = 720
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width / 2) - (window_width / 2))
y_cordinate = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)

# Bundled Apps ---------------------------------------------------------------

youtube_dl_cli = '"' + "Apps/youtube-dl/youtube-dl.exe" + '"'
ffmpeg_location = ' --ffmpeg-location "Apps/ffmpeg/ffmpeg.exe" '

# --------------------------------------------------------------- Bundled Apps

# About Window --------------------------------------------------------------------------------------------------------
def openaboutwindow():
    about_window = Toplevel()
    about_window.title('About')
    about_window.configure(background="#434547")
    window_height = 140
    window_width = 470
    screen_width = about_window.winfo_screenwidth()
    screen_height = about_window.winfo_screenheight()
    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))
    about_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    about_window_text = Text(about_window, background="#434547", foreground="white", relief=SUNKEN)
    about_window_text.pack()
    about_window_text.configure(state=NORMAL)
    about_window_text.insert(INSERT, "Youtube-DL-Gui Beta v1.0 \n")
    about_window_text.insert(INSERT, "\n")
    about_window_text.insert(INSERT, "Development: jlw4049")
    about_window_text.insert(INSERT, "\n\n")
    about_window_text.insert(INSERT, "A early BETA Youtube audio/video downloader. \n")
    about_window_text.configure(state=DISABLED)


# -------------------------------------------------------------------------------------------------------- About Window

# Menu Items and Sub-Bars ---------------------------------------------------------------------------------------------
my_menu_bar = Menu(root, tearoff=0)
root.config(menu=my_menu_bar)

file_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
my_menu_bar.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Exit', command=root.quit)

options_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
my_menu_bar.add_cascade(label='Options', menu=options_menu)

options_submenu = Menu(root, tearoff=0, activebackground='dim grey')
options_menu.add_cascade(label='Shell Options', menu=options_submenu)
shell_options = StringVar()
shell_options.set('Default')
options_submenu.add_radiobutton(label='Shell Closes Automatically', variable=shell_options, value="Default")
options_submenu.add_radiobutton(label='Shell Stays Open (Debug)', variable=shell_options, value="Debug")
#
# tools_submenu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
# my_menu_bar.add_cascade(label='Tools', menu=tools_submenu)
# tools_submenu.add_command(label="Open MediaInfo") #command=mediainfogui)
#
help_menu = Menu(my_menu_bar, tearoff=0, activebackground="dim grey")
my_menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=openaboutwindow)

# --------------------------------------------------------------------------------------------- Menu Items and Sub-Bars

# Link Frame ----------------------------------------------------------------------------------------------------------
link_frame = LabelFrame(root, text=' Paste Link ')
link_frame.grid(row=0, columnspan=4, sticky=E + W + N + S, padx=20, pady=(10,10))
link_frame.configure(fg="white", bg="#434547", bd=3)

link_frame.rowconfigure(1, weight=1)
link_frame.columnconfigure(0, weight=1)
link_frame.columnconfigure(1, weight=1)

# ---------------------------------------------------------------------------------------------------------- Link Frame

# Audio Frame ---------------------------------------------------------------------------------------------------------
audio_frame = LabelFrame(root, text=' Audio Settings ')
audio_frame.grid(row=1, columnspan=4, sticky=E + W + N + S, padx=20, pady=(10,10))
audio_frame.configure(fg="white", bg="#434547", bd=3)

audio_frame.rowconfigure(0, weight=1)
audio_frame.columnconfigure(0, weight=1)
audio_frame.columnconfigure(1, weight=1)
audio_frame.columnconfigure(2, weight=1)
audio_frame.columnconfigure(3, weight=1)

# --------------------------------------------------------------------------------------------------------- Audio Frame

# Add Link to variable ------------------------------------------------------------------------------------------------
def apply_link():
    global download_link
    link_entry.config(state=NORMAL)     #
    link_entry.delete(0, END)           # This function clears entry box in order to add new link to entry box
    link_entry.config(state=DISABLED)   #
    download_link = text_area.get(1.0, END)  # Pasted download link
    text_area.delete(1.0, END)               # Deletes entry box where you pasted your link as it stores it into var
    link_entry.config(state=NORMAL)      #
    link_entry.insert(0, download_link)  # Adds download_link to entry box
    link_entry.config(state=DISABLED)    #

# ------------------------------------------------------------------------------------------------------------ Add Link

# File Output ---------------------------------------------------------------------------------------------------------
def file_save():
    global VideoOutput
    save_entry.config(state=NORMAL)       #
    save_entry.delete(0, END)             # This function clears entry box in order to add new link to entry box
    save_entry.config(state=DISABLED)     #
    VideoOutput = filedialog.askdirectory()  # Pop up window to choose a save directory location
    if VideoOutput:
        save_for_entry = '"' + VideoOutput + '/"'  # Completes save directory and adds quotes
        save_entry.config(state=NORMAL)       #
        save_entry.insert(0, save_for_entry)  # Adds download_link to entry box
        save_entry.config(state=DISABLED)     #

# --------------------------------------------------------------------------------------------------------- File Output

# Audio Only Function -------------------------------------------------------------------------------------------------
def audio_only_toggle():
    global audio_format, audio_quality
    if audio_only.get() == '-x ':
        audio_format_menu.config(state=NORMAL, background="#23272A")
        audio_quality_menu.config(state=NORMAL, background="#23272A")
        audio_format.set('Default (Best - WAV)')
        audio_quality.set('5 - Default')
    elif audio_only.get() != '-x ':
        audio_format.set('')
        audio_quality.set('')
        audio_format_menu.config(state=DISABLED, background='grey')
        audio_quality_menu.config(state=DISABLED, background='grey')

# ------------------------------------------------------------------------------------------------- Audio Only Function

# Audio Only Checkbutton ----------------------------------------------------------------------------------------------
audio_only = StringVar()
audio_only_checkbox = Checkbutton(audio_frame, text='Audio Only', variable=audio_only, onvalue="-x ",
                                   offvalue="", command=audio_only_toggle)
audio_only_checkbox.grid(row=0, column=0, columnspan=1, rowspan=2, padx=10, pady=3, sticky=N + S + E + W)
audio_only_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                               activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
audio_only.set("-x ")

# ---------------------------------------------------------------------------------------------- Audio Only Checkbutton

# Audio Format Selection ----------------------------------------------------------------------------------------------
def audio_format_menu_hover(e):
    audio_format_menu["bg"] = "grey"
    audio_format_menu["activebackground"] = "grey"

def audio_format_menu_hover_leave(e):
    audio_format_menu["bg"] = "#23272A"

audio_format = StringVar(root)
audio_format_choices = {'Default (Best - WAV)': '--audio-format wav ',
                         'AAC': '--audio-format aac ',
                         'FLAC': '--audio-format flac ',
                         'MP3': '--audio-format mp3 ',
                         'M4A': '--audio-format m4a ',
                         'Opus': '--audio-format opus ',
                         'Vorbis': '--audio-format vorbis '}
audio_format_menu_label = Label(audio_frame, text="Audio Format :", background="#434547",
                                 foreground="white")
audio_format_menu_label.grid(row=0, column=1, columnspan=2, padx=10, pady=(3,10), sticky=W + E)
audio_format_menu = OptionMenu(audio_frame, audio_format, *audio_format_choices.keys())
audio_format_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=23)
audio_format_menu.grid(row=1, column=1, columnspan=2, padx=10, pady=(3,10))
audio_format.set('Default (Best - WAV)')
audio_format_menu["menu"].configure(activebackground="dim grey")
audio_format_menu.bind("<Enter>", audio_format_menu_hover)
audio_format_menu.bind("<Leave>", audio_format_menu_hover_leave)
# -------------------------------------------------------------------------------------------------------- Audio Format

# Audio Quality Selection ---------------------------------------------------------------------------------------------
def audio_quality_menu_hover(e):
    audio_quality_menu["bg"] = "grey"
    audio_quality_menu["activebackground"] = "grey"

def audio_quality_menu_hover_leave(e):
    audio_quality_menu["bg"] = "#23272A"

audio_quality = StringVar(root)
audio_quality_choices = {'0 - Best': '--audio-quality 0 ',
                        '1': '--audio-quality 1 ',
                        '2': '--audio-quality 2 ',
                        '3': '--audio-quality 3 ',
                        '4': '--audio-quality 4 ',
                        '5 - Default': '--audio-quality 5 ',
                        '6': '--audio-quality 6 ',
                        '7': '--audio-quality 7 ',
                        '8': '--audio-quality 8 ',
                        '9 - Worse': '--audio-quality 9 '}
audio_quality_menu_label = Label(audio_frame, text="Audio Quality (VBR) :", background="#434547",
                                 foreground="white")
audio_quality_menu_label.grid(row=0, column=3, columnspan=2, padx=10, pady=(3,10), sticky=W + E)
audio_quality_menu = OptionMenu(audio_frame, audio_quality, *audio_quality_choices.keys())
audio_quality_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=23)
audio_quality_menu.grid(row=1, column=3, columnspan=2, padx=10, pady=(3,10))
audio_quality.set('5 - Default')
audio_quality_menu["menu"].configure(activebackground="dim grey")
audio_quality_menu.bind("<Enter>", audio_quality_menu_hover)
audio_quality_menu.bind("<Leave>", audio_quality_menu_hover_leave)
# ------------------------------------------------------------------------------------------------------- Audio Quality

# Start Job -----------------------------------------------------------------------------------------------------------
def start_job():
    command = '"' + youtube_dl_cli + ffmpeg_location + '--console-title ' + audio_only.get() \
              + audio_format_choices[audio_format.get()] + audio_quality_choices[audio_quality.get()] \
              + '-o ' + '"' + VideoOutput + '/%(title)s.%(ext)s' + '" ' + download_link + '"'
    if shell_options.get() == 'Default':
        subprocess.Popen('cmd /c' + command)
    elif shell_options.get() == 'Debug':
        subprocess.Popen('cmd /k' + command)

# ---------------------------------------------------------------------------------------------------------- Start Job

# Buttons and Entry Box's ---------------------------------------------------------------------------------------------
text_area = scrolledtext.ScrolledText(link_frame, wrap=WORD, width=69, height=1, font=("Times New Roman", 14))
text_area.grid(row=0, column=0, columnspan=3, pady=(1,5), padx=10, sticky=W + E)

link_entry = Entry(link_frame, borderwidth=4, background="#CACACA", state=DISABLED, width=70)
link_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=(0, 0), sticky=W + E)

def apply_btn_hover(e):
    apply_btn["bg"] = "grey"

def apply_btn_hover_leave(e):
    apply_btn["bg"] = "#8b0000"

apply_btn = Button(link_frame, text="Add Link", command=apply_link, foreground="white", background="#8b0000", width=30)
apply_btn.grid(row=1, column=0, columnspan=1, padx=10, pady=5, sticky=W)
apply_btn.bind("<Enter>", apply_btn_hover)
apply_btn.bind("<Leave>", apply_btn_hover_leave)

def save_btn_hover(e):
    save_btn["bg"] = "grey"

def save_btn_hover_leave(e):
    save_btn["bg"] = "#8b0000"

save_btn = Button(root, text="Save Directory", command=file_save, foreground="white", background="#8b0000")
save_btn.grid(row=2, column=0, columnspan=1, padx=10, pady=(15,0), sticky=W + E)
save_btn.bind("<Enter>", save_btn_hover)
save_btn.bind("<Leave>", save_btn_hover_leave)

save_entry = Entry(root, borderwidth=4, background="#CACACA", state=DISABLED)
save_entry.grid(row=2, column=1, columnspan=3, padx=10, pady=(15, 0), sticky=W + E)

def start_job_btn_hover(e):
    start_job_btn["bg"] = "grey"

def start_job_btn_hover_leave(e):
    start_job_btn["bg"] = "#8b0000"

start_job_btn = Button(root, text="Start Job", command=start_job, foreground="white", background="#8b0000")
start_job_btn.grid(row=3, column=3, columnspan=1, padx=10, pady=(15,15), sticky=N + S + W + E)
start_job_btn.bind("<Enter>", start_job_btn_hover)
start_job_btn.bind("<Leave>", start_job_btn_hover_leave)

# --------------------------------------------------------------------------------------------- Buttons and Entry Box's

# End Loop ------------------------------------------------------------------------------------------------------------
root.mainloop()
# ------------------------------------------------------------------------------------------------------------ End Loop
