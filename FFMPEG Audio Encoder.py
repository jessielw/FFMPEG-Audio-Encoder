# Imports--------------------------------------------------------------------
from tkinter import *
from tkinter import filedialog, StringVar
import subprocess
import ctypes
import tkinter as tk
import pathlib
import tkinter.scrolledtext as scrolledtextwidget
from TkinterDnD2 import *
from tkinter import messagebox

# Main Gui & Windows --------------------------------------------------------

if __name__ == "__main__":
    if 'win' in sys.platform:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

root = TkinterDnD.Tk()
root.title("FFMPEG Audio Encoder v2.0")
root.iconphoto(True, PhotoImage(file="Runtime/topbar.png"))
root.configure(background="#434547")
window_height = 210
window_width = 450
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width / 2) - (window_width / 2))
y_cordinate = int((screen_height / 2) - (window_height / 2))
root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)

# Menu Bar Settings ---------------------------------------------------------

my_menu_bar = Menu(root, tearoff=0)
root.config(menu=my_menu_bar)

# Bundled Apps ---------------------------------------------------------------

ffmpeg = '"Apps/FFMPEG/ffmpeg.exe"'
mediainfo = "Apps/MediaInfo/MediaInfo.exe"
mediainfocli = '"Apps/MediaInfoCLI/MediaInfo.exe"'
fdkaac = '"Apps/fdkaac/fdkaac.exe"'
qaac = '"Apps/qaac/qaac64.exe"'

# About Window --------------------------------------------------------------------------------------------------------
def openaboutwindow():
    about_window = Toplevel()
    about_window.title('About')
    about_window.configure(background="#434547")
    window_height = 140
    window_width = 450
    screen_width = about_window.winfo_screenwidth()
    screen_height = about_window.winfo_screenheight()
    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))
    about_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    about_window_text = Text(about_window, background="#434547", foreground="white", relief=SUNKEN)
    about_window_text.pack()
    about_window_text.configure(state=NORMAL)
    about_window_text.insert(INSERT, "FFMPEG Audio Encoder v1.98 \n")
    about_window_text.insert(INSERT, "\n")
    about_window_text.insert(INSERT, "Development: jlw4049\n\nContributors: BassThatHertz")
    about_window_text.insert(INSERT, "\n\n")
    about_window_text.insert(INSERT, "A lightweight audio encoder based off of FFMPEG. \n")
    about_window_text.configure(state=DISABLED)
# -------------------------------------------------------------------------------------------------------- About Window

# Menu Items and Sub-Bars ---------------------------------------------------------------------------------------------
file_menu = Menu(my_menu_bar, tearoff=0, activebackground="dim grey")
my_menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=root.quit)

shell_options = StringVar()
shell_options.set("Default")
options_menu = Menu(my_menu_bar, tearoff=0, activebackground="dim grey")
my_menu_bar.add_cascade(label="Options", menu=options_menu)
options_submenu = Menu(root, tearoff=0, activebackground="dim grey")
options_menu.add_cascade(label="Shell Options", menu=options_submenu)
options_submenu.add_radiobutton(label="Shell Closes Automatically", variable=shell_options, value="Default")
options_submenu.add_radiobutton(label="Shell Stays Open (Debug)", variable=shell_options, value="Debug")

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
        elif encoder.get() == "FDK-AAC" or encoder.get() == "QAAC":
            VideoOut = filename.with_suffix('.NEW.m4a')
        VideoOutput = str(VideoOut)
        output_entry.configure(state=NORMAL)
        output_entry.delete(0, END)
        output_entry.insert(0, VideoOut)
        output_entry.configure(state=DISABLED)
        audiosettings_button.configure(state=NORMAL)
        command_line_button.config(state=DISABLED)
        autosavefilename = VideoOut.name
# --------------------------------------------------------------------------------------------- File Auto Save Function

# Uses MediaInfo CLI to get total audio track count and gives us a total track count ----------------------------------
def track_count(*args):  # Thanks for helping me shorten this 'gmes78'
    global acodec_stream_track_counter
    acodec_stream_track_counter = {}
    for i in range(int(str.split(track_count)[-1])):
        acodec_stream_track_counter[f'Track {i + 1}'] = f' -map 0:a:{i} '
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
    "QAAC": qaac}
encoder = StringVar(root)
encoder.set("Set Codec")
encoder.trace('w', encoder_changed)
encoder_menu = OptionMenu(root, encoder, *encoder_dropdownmenu_choices.keys(), command=track_count)
encoder_menu.grid(row=1, column=2, columnspan=1, padx=5, pady=5, sticky=N + S + W + E)
encoder_menu.config(state=DISABLED, background="#23272A", foreground="white", highlightthickness=1)
encoder_menu["menu"].configure(activebackground="dim grey")
codec_label = Label(root, text="Codec ->", background="#434547", foreground="White")
codec_label.grid(row=1, column=1, columnspan=1, padx=5, pady=5, sticky=N + S + W + E)
# -------------------------------------------------------------------------------------------------------- Encoder Menu

# Audio Codec Window --------------------------------------------------------------------------------------------------
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
    global acodec_application
    global acodec_application_choices
    global acodec_profile
    global acodec_profile_choices

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

    # Checks channel for dolby pro logic II checkbox ------------------------------------------------------------------
    def dolby_pro_logic_ii_enable_disable(*args):
        if acodec_channel.get() == '2 (Stereo)':
            dolby_pro_logic_ii_checkbox.config(state=NORMAL)
        else:
            dolby_pro_logic_ii.set("")
            dolby_pro_logic_ii_checkbox.config(state=DISABLED)
    # --------------------------------------------------------------------------------------------- dplII channel check

    # Combines -af filter settings ------------------------------------------------------------------------------------
    def audio_filter_function(*args):
        global audio_filter_setting
        audio_filter_setting = ''
        ffmpeg_gain_cmd = '"volume=' + ffmpeg_gain.get() + 'dB"'
        if encoder.get() == 'E-AC3':
            if ffmpeg_gain.get() == '0':
                audio_filter_setting = ''
            else:
                audio_filter_setting = '-af ' + ffmpeg_gain_cmd + ' '
        else:
            if dolby_pro_logic_ii.get() == '' and ffmpeg_gain.get() == '0':
                audio_filter_setting = ''
            elif dolby_pro_logic_ii.get() == '"aresample=matrix_encoding=dplii"' and \
                    ffmpeg_gain.get() == '0':
                audio_filter_setting = '-af ' + dolby_pro_logic_ii.get()
            elif dolby_pro_logic_ii.get() == '"aresample=matrix_encoding=dplii"' \
                    and ffmpeg_gain.get() != '0':
                audio_filter_setting = '-af ' + dolby_pro_logic_ii.get() + ',' + \
                                       ffmpeg_gain_cmd + ' '
            elif dolby_pro_logic_ii.get() == '' and ffmpeg_gain.get() != '0':
                audio_filter_setting = '-af ' + ffmpeg_gain_cmd + ' '
    # ---------------------------------------------------------------------------------------------------- combines -af

    def gotosavefile():
        audio_window.destroy()
        output_button.config(state=NORMAL)
        start_audio_button.config(state=NORMAL)
        command_line_button.config(state=NORMAL)
        try:
            cmd_line_window.withdraw()
        except:
            pass

    # Show Streams Inside Audio Settings Window -----------------------------------------------------------------------
    def show_streams_mediainfo():  # Stream Viewer
        commands = '"' + mediainfocli + ' --Output="Audio;Track #:..............................%ID%\\nFormat:..' + \
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

    # AC3 Window ------------------------------------------------------------------------------------------------------
    if encoder.get() == "AC3":
        audio_window = Toplevel()
        audio_window.title('AC3 Settings')
        audio_window.configure(background="#434547")
        window_height = 310
        window_width = 600
        screen_width = audio_window.winfo_screenwidth()
        screen_height = audio_window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        my_menu = Menu(audio_window, tearoff=0)
        audio_window.config(menu=my_menu)
        Menu(my_menu, tearoff=0, activebackground="dim grey")
        my_menu.add_command(label="View Streams", command=show_streams_mediainfo)

        audio_window.grid_columnconfigure(0, weight=1)
        audio_window.grid_columnconfigure(1, weight=1)
        audio_window.grid_columnconfigure(2, weight=1)
        audio_window.grid_rowconfigure(0, weight=1)
        audio_window.grid_rowconfigure(1, weight=1)
        audio_window.grid_rowconfigure(2, weight=1)
        audio_window.grid_rowconfigure(3, weight=1)
        audio_window.grid_rowconfigure(8, weight=1)

        # Views Command -----------------------------------------------------------------------------------------------
        def view_command():
            global cmd_line_window
            global cmd_label
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
                cmd_label = Label(cmd_line_window, text=example_cmd_output, foreground="white", background="#434547")
                cmd_label.config(font=("Helvetica", 16))
                cmd_label.pack()

                def hide_instead():
                    cmd_line_window.withdraw()

                cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)
        # ----------------------------------------------------------------------------------------------- Views Command

        # Buttons -----------------------------------------------------------------------------------------------------
        apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A",
                              command=gotosavefile)
        apply_button.grid(row=8, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        apply_button.bind("<Enter>", apply_button_hover)
        apply_button.bind("<Leave>", apply_button_hover_leave)

        show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A", \
                          command=view_command)
        show_cmd.grid(row=8, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        show_cmd.bind("<Enter>", show_cmd_hover)
        show_cmd.bind("<Leave>", show_cmd_hover_leave)
        # ----------------------------------------------------------------------------------------------------- Buttons

        # Audio Bitrate Selection -------------------------------------------------------------------------------------
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
        acodec_bitrate.set('224k')  # set the default option
        acodec_bitrate_menu_label = Label(audio_window, text="Bitrate :", background="#434547", foreground="white")
        acodec_bitrate_menu_label.grid(row=0, column=2, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_bitrate_menu = OptionMenu(audio_window, acodec_bitrate, *acodec_bitrate_choices.keys())
        acodec_bitrate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_bitrate_menu.grid(row=1, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_bitrate_menu["menu"].configure(activebackground="dim grey")
        acodec_bitrate_menu.bind("<Enter>", acodec_bitrate_menu_hover)
        acodec_bitrate_menu.bind("<Leave>", acodec_bitrate_menu_hover_leave)
        # ----------------------------------------------------------------------------------------------- Audio Bitrate

        # Audio Stream Selection --------------------------------------------------------------------------------------
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
        # -------------------------------------------------------------------------------------------------------------

        # Audio Channel Selection -------------------------------------------------------------------------------------
        acodec_channel = StringVar(audio_window)
        acodec_channel_choices = {'Original': "",
                                  '1 (Mono)': "-ac 1 ",
                                  '2 (Stereo)': "-ac 2 ",
                                  '2.1 (Stereo)': "-ac 3 ",
                                  '4.0 (Quad)': "-ac 4 ",
                                  '5.0 (Surround)': "-ac 5 ",
                                  '5.1 (Surround)': "-ac 6 "}
        acodec_channel.set('Original')  # set the default option
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
        dolby_pro_logic_ii_checkbox = Checkbutton(audio_window, text=' Dolby Pro\nLogic II', \
                                                  variable=dolby_pro_logic_ii, state=DISABLED, \
                                                  onvalue='"aresample=matrix_encoding=dplii"', offvalue="", \
                                                  command=audio_filter_function)
        dolby_pro_logic_ii_checkbox.grid(row=3, column=2, columnspan=1, rowspan=1, padx=10, pady=3, \
                                         sticky=N + S + E + W)
        dolby_pro_logic_ii_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                          activeforeground="white", selectcolor="#434547", font=("Helvetica", 11))
        dolby_pro_logic_ii.set("")
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
        ffmpeg_gain.trace('w', audio_filter_function)
        ffmpeg_gain.set(0)
        # -------------------------------------------------------------------------------------------------------- Gain

        # Audio Sample Rate Selection ---------------------------------------------------------------------------------
        acodec_samplerate = StringVar(audio_window)
        acodec_samplerate_choices = {'Original': "",
                                     '32000 Hz': "-ar 32000 ",
                                     '44100 Hz': "-ar 44100 ",
                                     '48000 Hz': "-ar 48000 "}
        acodec_samplerate.set('Original')  # set the default option
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
        def ac3_cmd(*args):
            global ac3_custom_cmd_input
            if ac3_custom_cmd.get() == (""):
                ac3_custom_cmd_input = ("")
            else:
                cstmcmd = ac3_custom_cmd.get()
                ac3_custom_cmd_input = cstmcmd + " "

        ac3_custom_cmd = StringVar()
        ac3_cmd_entrybox_label = Label(audio_window, text="Custom Command Line :", anchor=W, background="#434547", \
                                       foreground="white")
        ac3_cmd_entrybox_label.grid(row=4, column=0, columnspan=2, padx=10, pady=(15, 0), sticky=N + S + W + E)
        ac3_cmd_entrybox = Entry(audio_window, textvariable=ac3_custom_cmd, borderwidth=4, background="#CACACA")
        ac3_cmd_entrybox.grid(row=5, column=0, columnspan=3, padx=10, pady=(0, 15), sticky=W + E)
        ac3_custom_cmd.trace('w', ac3_cmd)
        ac3_custom_cmd.set("")
        # ----------------------------------------------------------------------------------------- Custom Command Line
    # ------------------------------------------------------------------------------------------------------------- AC3

    # AAC Window ------------------------------------------------------------------------------------------------------
    elif encoder.get() == "AAC":
        audio_window = Toplevel()
        audio_window.title('AAC Settings')
        audio_window.configure(background="#434547")
        window_height = 420
        window_width = 600
        screen_width = audio_window.winfo_screenwidth()
        screen_height = audio_window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        my_menu = Menu(audio_window, tearoff=0)
        audio_window.config(menu=my_menu)
        Menu(my_menu, tearoff=0, activebackground="dim grey")
        my_menu.add_command(label="View Streams", command=show_streams_mediainfo)

        audio_window.grid_columnconfigure(0, weight=1)
        audio_window.grid_columnconfigure(1, weight=1)
        audio_window.grid_columnconfigure(2, weight=1)
        audio_window.grid_rowconfigure(0, weight=1)
        audio_window.grid_rowconfigure(1, weight=1)
        audio_window.grid_rowconfigure(2, weight=1)
        audio_window.grid_rowconfigure(3, weight=1)
        audio_window.grid_rowconfigure(9, weight=1)

        def view_command():  # Views Command ---------------------------------------------------------------------------
            global cmd_label
            global cmd_line_window
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
        apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A", \
                              command=gotosavefile)
        apply_button.grid(row=9, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        apply_button.bind("<Enter>", apply_button_hover)
        apply_button.bind("<Leave>", apply_button_hover_leave)

        show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A", \
                          command=view_command)
        show_cmd.grid(row=9, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
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
        aac_cmd_entrybox_label = Label(audio_window, text="Custom Command Line :", anchor=W, background="#434547", \
                                       foreground="white")
        aac_cmd_entrybox_label.grid(row=5, column=0, columnspan=2, padx=10, pady=(0, 0), sticky=N + S + W + E)
        aac_cmd_entrybox = Entry(audio_window, textvariable=aac_custom_cmd, borderwidth=4, background="#CACACA")
        aac_cmd_entrybox.grid(row=6, column=0, columnspan=3, padx=10, pady=(0, 0), sticky=W + E)
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
        aac_title_entrybox_label = Label(audio_window, text="Track Name :", anchor=W, background="#434547", \
                                         foreground="white")
        aac_title_entrybox_label.grid(row=7, column=0, columnspan=2, padx=10, pady=(5, 0), sticky=N + S + W + E)
        aac_title_entrybox = Entry(audio_window, textvariable=aac_title, borderwidth=4, background="#CACACA")
        aac_title_entrybox.grid(row=8, column=0, columnspan=3, padx=10, pady=(0, 10), sticky=W + E)
        aac_title.trace('w', aac_title_check)
        aac_title.set("")
        # ------------------------------------------------------------------------------------------------- Track Title

        # Dolby Pro Logic II ------------------------------------------------------------------------------------------
        dolby_pro_logic_ii = StringVar()
        dolby_pro_logic_ii_checkbox = Checkbutton(audio_window, text=' Dolby Pro\nLogic II', \
                                                  variable=dolby_pro_logic_ii, state=DISABLED, \
                                                  onvalue='"aresample=matrix_encoding=dplii"', offvalue="", \
                                                  command=audio_filter_function)
        dolby_pro_logic_ii_checkbox.grid(row=4, column=0, columnspan=1, rowspan=1, padx=10, pady=(15,15), \
                                         sticky=N + S + E + W)
        dolby_pro_logic_ii_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                          activeforeground="white", selectcolor="#434547", font=("Helvetica", 11))
        dolby_pro_logic_ii.set("")
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
        ffmpeg_gain.trace('w', audio_filter_function)
        ffmpeg_gain.set(0)
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
        aac_bitrate_spinbox.set(192)
        # --------------------------------------------------------------------------------------- Audio Bitrate Spinbox

        # Vbr Toggle --------------------------------------------------------------------------------------------------
        global aac_vbr_toggle
        aac_vbr_toggle = StringVar()
        aac_vbr_toggle.set("-c:a ")

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
                aac_bitrate_spinbox.set(192)
            elif aac_vbr_toggle.get() == "-q:a ":  # This enables VBR Spinbox ------------------------------------------
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
                aac_quality_spinbox.set(2)
                # ----------------------------------------------------------------------------------------- VBR Spinbox

        aac_vbr_toggle_checkbox = Checkbutton(audio_window, text=' Variable\n Bit-Rate', variable=aac_vbr_toggle,
                                              onvalue="-q:a ", offvalue="-c:a ", command=aac_vbr_trace)
        aac_vbr_toggle_checkbox.grid(row=2, column=0, columnspan=1, rowspan=2, padx=10, pady=3, sticky=N + S + E + W)
        aac_vbr_toggle_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                          activeforeground="white", selectcolor="#434547", font=("Helvetica", 11))
        aac_vbr_toggle.trace('w', aac_vbr_trace)
        # -------------------------------------------------------------------------------------------------- Vbr Toggle

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
        acodec_channel.set('Original')  # set the default option
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

        # Audio Stream Selection --------------------------------------------------------------------------------------
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
        acodec_samplerate.set('Original')  # set the default option
        acodec_samplerate_label = Label(audio_window, text="Sample Rate :", background="#434547", foreground="white")
        acodec_samplerate_label.grid(row=2, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_samplerate_menu = OptionMenu(audio_window, acodec_samplerate, *acodec_samplerate_choices.keys())
        acodec_samplerate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_samplerate_menu.grid(row=3, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_samplerate_menu["menu"].configure(activebackground="dim grey")
        acodec_samplerate_menu.bind("<Enter>", acodec_samplerate_menu_hover)
        acodec_samplerate_menu.bind("<Leave>", acodec_samplerate_menu_hover_leave)
        # --------------------------------------------------------------------------------- Audio Sample Rate Selection
        # -------------------------------------------------------------------------------------------------- AAC Window

    # DTS Window ------------------------------------------------------------------------------------------------------
    elif encoder.get() == "DTS":
        audio_window = Toplevel()
        audio_window.title('DTS Settings')
        audio_window.configure(background="#434547")
        window_height = 350
        window_width = 470
        screen_width = audio_window.winfo_screenwidth()
        screen_height = audio_window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        my_menu = Menu(audio_window, tearoff=0)
        audio_window.config(menu=my_menu)
        Menu(my_menu, tearoff=0, activebackground="dim grey")
        my_menu.add_command(label="View Streams", command=show_streams_mediainfo)

        audio_window.grid_columnconfigure(0, weight=1)
        audio_window.grid_columnconfigure(1, weight=1)
        audio_window.grid_columnconfigure(2, weight=1)
        audio_window.grid_rowconfigure(0, weight=1)
        audio_window.grid_rowconfigure(1, weight=1)
        audio_window.grid_rowconfigure(2, weight=1)
        audio_window.grid_rowconfigure(3, weight=1)
        audio_window.grid_rowconfigure(4, weight=1)
        audio_window.grid_rowconfigure(7, weight=1)

        def dts_setting_choice_trace(*args):
            if dts_settings.get() == 'DTS Encoder':
                achannel_menu.config(state=NORMAL)
                acodec_channel.set('2 (Stereo)')
                ffmpeg_gain_spinbox.config(state=NORMAL)
                ffmpeg_gain.set(0)
                acodec_samplerate_menu.config(state=NORMAL)
                acodec_samplerate.set('Original')
                dts_acodec_bitrate_spinbox.config(state=NORMAL)
                dts_bitrate_spinbox.set(448)
            else:
                acodec_channel.set('2 (Stereo)')
                achannel_menu.config(state=DISABLED)
                ffmpeg_gain.set(0)
                ffmpeg_gain_spinbox.config(state=DISABLED)
                acodec_samplerate.set('Original')
                acodec_samplerate_menu.config(state=DISABLED)
                dts_bitrate_spinbox.set('')
                dts_acodec_bitrate_spinbox.config(state=DISABLED)
                dolby_pro_logic_ii.set('')
                dolby_pro_logic_ii_checkbox.config(state=DISABLED)

        # Views Command -----------------------------------------------------------------------------------------------
        def view_command():
            global cmd_label
            global cmd_line_window
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
        apply_button.grid(row=7, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        apply_button.bind("<Enter>", apply_button_hover)
        apply_button.bind("<Leave>", apply_button_hover_leave)

        show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A", \
                          command=view_command)
        show_cmd.grid(row=7, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
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
        dts_cmd_entrybox_label = Label(audio_window, text="Custom Command Line :", anchor=W, background="#434547", \
                                       foreground="white")
        dts_cmd_entrybox_label.grid(row=5, column=0, columnspan=2, padx=10, pady=(15, 0), sticky=N + S + W + E)
        dts_cmd_entrybox = Entry(audio_window, textvariable=dts_custom_cmd, borderwidth=4, background="#CACACA")
        dts_cmd_entrybox.grid(row=6, column=0, columnspan=3, padx=10, pady=(0, 10), sticky=W + E)
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
                                             wrap=True, textvariable=dts_bitrate_spinbox, state=DISABLED, \
                                             disabledbackground='grey')
        dts_acodec_bitrate_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                             buttonbackground="black", width=15, readonlybackground="#23272A")
        dts_acodec_bitrate_spinbox.grid(row=3, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        dts_bitrate_spinbox.set("")
        # --------------------------------------------------------------------------------------- Audio Bitrate Spinbox

        # Dolby Pro Logic II ------------------------------------------------------------------------------------------
        dolby_pro_logic_ii = StringVar()
        dolby_pro_logic_ii_checkbox = Checkbutton(audio_window, text=' Dolby Pro\nLogic II', \
                                                  variable=dolby_pro_logic_ii, state=DISABLED, \
                                                  onvalue='"aresample=matrix_encoding=dplii"', offvalue='', \
                                                  command=audio_filter_function)
        dolby_pro_logic_ii_checkbox.grid(row=4, column=0, columnspan=1, rowspan=1, padx=10, pady=(10, 3), \
                                         sticky=N + S + E + W)
        dolby_pro_logic_ii_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                              activeforeground="white", selectcolor="#434547", font=("Helvetica", 11))
        dolby_pro_logic_ii.set("")
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
                                      buttonbackground="black", width=15, readonlybackground="#23272A", \
                                      disabledbackground='grey')
        ffmpeg_gain_spinbox.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        ffmpeg_gain.trace('w', audio_filter_function)
        ffmpeg_gain.set(0)
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
        acodec_samplerate.set('Original')  # set the default option
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
        acodec_stream.set('Track 1')
        acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
        acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
        acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_stream_menu["menu"].configure(activebackground="dim grey")
        acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
        acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)
        # ------------------------------------------------------------------------------------------------ Audio Stream

        # Audio Channel Selection -------------------------------------------------------------------------------------
        acodec_channel = StringVar(audio_window)
        acodec_channel_choices = {'(Mono)': "-ac 1 ",
                                  '2 (Stereo)': "-ac 2 ",
                                  'Original': ""}
        acodec_channel.set('2 (Stereo)')  # set the default option
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
    # ------------------------------------------------------------------------------------------------------------- DTS

    # Opus Window -----------------------------------------------------------------------------------------------------
    elif encoder.get() == "Opus":
        audio_window = Toplevel()
        audio_window.title('Opus Settings')
        audio_window.configure(background="#434547")
        window_height = 530
        window_width = 640
        screen_width = audio_window.winfo_screenwidth()
        screen_height = audio_window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        my_menu = Menu(audio_window, tearoff=0)
        audio_window.config(menu=my_menu)
        Menu(my_menu, tearoff=0, activebackground="dim grey")
        my_menu.add_command(label="View Streams", command=show_streams_mediainfo)

        advanced_label = Label(audio_window,
                               text="- - - - - - - - - - - - - - - - - - - - Advanced Settings - - - - - - - - - - - "
                                    "- - - - - - - - -",
                               background="#434547", foreground="white", relief=GROOVE)
        advanced_label.grid(row=5, column=0, columnspan=3, padx=10, pady=(5, 0), sticky=W + E)

        advanced_label_end = Label(audio_window,
                                   text="- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - "
                                        "- - - - - - - - -",
                                   background="#434547", foreground="white", relief=GROOVE)
        advanced_label_end.grid(row=8, column=0, columnspan=3, padx=10, pady=(5, 0), sticky=W + E)

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
        audio_window.grid_rowconfigure(11, weight=1)

        # Views Command -----------------------------------------------------------------------------------------------
        def view_command():
            global cmd_label
            global cmd_line_window
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
        apply_button.grid(row=11, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        apply_button.bind("<Enter>", apply_button_hover)
        apply_button.bind("<Leave>", apply_button_hover_leave)

        show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A", \
                          command=view_command)
        show_cmd.grid(row=11, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
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
        acodec_bitrate.set('160k')  # set the default option
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
        acodec_samplerate.set('Original')  # set the default option
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
        opus_cmd_entrybox_label = Label(audio_window, text="Custom Command Line :", anchor=W, background="#434547", \
                                        foreground="white")
        opus_cmd_entrybox_label.grid(row=9, column=0, columnspan=2, padx=10, pady=(10, 0), sticky=N + S + W + E)
        opus_cmd_entrybox = Entry(audio_window, textvariable=opus_custom_cmd, borderwidth=4, background="#CACACA")
        opus_cmd_entrybox.grid(row=10, column=0, columnspan=3, padx=10, pady=(0, 15), sticky=W + E)
        opus_custom_cmd.trace('w', opus_cmd)
        opus_custom_cmd.set("")

        # ----------------------------------------------------------------------------------------- Custom Command Line

        # Audio VBR Toggle --------------------------------------------------------------------------------------------
        acodec_vbr = StringVar(audio_window)
        acodec_vbr_choices = {'VBR: On': "",
                              'VBR: Off': "-vbr 0 ",
                              'VBR: Constrained': "-vbr 2 "}
        acodec_vbr.set('VBR: On')  # set the default option
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
        acodec_application.set('Audio')  # set the default option
        acodec_application_menu_label = Label(audio_window, text="Application:\n*Default is 'Audio'*",
                                              background="#434547", foreground="white")
        acodec_application_menu_label.grid(row=6, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_application_menu = OptionMenu(audio_window, acodec_application, *acodec_application_choices.keys())
        acodec_application_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_application_menu.grid(row=7, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_application_menu["menu"].configure(activebackground="dim grey")
        acodec_application_menu.bind("<Enter>", acodec_application_menu_hover)
        acodec_application_menu.bind("<Leave>", acodec_application_menu_hover_leave)
        # ------------------------------------------------------------------------------------------------- Application

        # Audio Frame Duration Spinbox --------------------------------------------------------------------------------
        global frame_duration
        frame_duration_values = (2.5, 5, 10, 20, 40, 60, 80, 100, 120)
        frame_duration = StringVar(audio_window)
        frame_duration_label = Label(audio_window, text="Frame Duration:\n*Default is '20'*", background="#434547", \
                                     foreground="white")
        frame_duration_label.grid(row=6, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        frame_duration_spinbox = Spinbox(audio_window, values=frame_duration_values, justify=CENTER, wrap=True,
                                         textvariable=frame_duration, width=13)
        frame_duration_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                      buttonbackground="black")
        frame_duration_spinbox.grid(row=7, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        frame_duration.set(20)
        # ---------------------------------------------------------------------------------------------- Frame Duration

        # Audio Packet Loss Spinbox --------------------------------------------------------------------------------
        global packet_loss
        packet_loss = StringVar(audio_window)
        packet_loss_label = Label(audio_window, text="Packet Loss:\n*Default is '0'*", background="#434547", \
                                  foreground="white")
        packet_loss_label.grid(row=6, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        packet_loss_spinbox = Spinbox(audio_window, from_=0, to=100, justify=CENTER, wrap=True,
                                      textvariable=packet_loss, width=13)
        packet_loss_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                   buttonbackground="black")
        packet_loss_spinbox.grid(row=7, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        packet_loss.set(0)
        # ------------------------------------------------------------------------------------------------- Packet Loss

        # Audio Channel Selection -------------------------------------------------------------------------------------
        acodec_channel = StringVar(audio_window)
        acodec_channel_choices = {'2 (Stereo)': "-ac 2 ",
                                  '5.0 (Surround)': "-ac 5 ",
                                  '5.1 (Surround)': "-ac 6 ",
                                  '6.1 (Surround)': "-ac 7 ",
                                  '7.1 (Surround)': "-ac 8 "}
        acodec_channel.set('2 (Stereo)')
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
        acodec_stream.set('Track 1')
        acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
        acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
        acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_stream_menu["menu"].configure(activebackground="dim grey")
        acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
        acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)
        # -------------------------------------------------------------------------------------- Audio Stream Selection

        # Dolby Pro Logic II ------------------------------------------------------------------------------------------
        dolby_pro_logic_ii = StringVar()
        dolby_pro_logic_ii_checkbox = Checkbutton(audio_window, text=' Dolby Pro\nLogic II', \
                                                  variable=dolby_pro_logic_ii, \
                                                  onvalue='"aresample=matrix_encoding=dplii"', offvalue="", \
                                                  command=audio_filter_function)
        dolby_pro_logic_ii_checkbox.grid(row=4, column=0, columnspan=1, rowspan=1, padx=10, pady=(15,5), \
                                         sticky=N + S + E + W)
        dolby_pro_logic_ii_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                              activeforeground="white", selectcolor="#434547", font=("Helvetica", 11))
        dolby_pro_logic_ii.set("")
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
        ffmpeg_gain.trace('w', audio_filter_function)
        ffmpeg_gain.set(0)
        # -------------------------------------------------------------------------------------------------------- Gain
    # ----------------------------------------------------------------------------------------------------- Opus Window

    # MP3 Window ------------------------------------------------------------------------------------------------------
    elif encoder.get() == "MP3":
        audio_window = Toplevel()
        audio_window.title('MP3 Settings')
        audio_window.configure(background="#434547")
        window_height = 310
        window_width = 550
        screen_width = audio_window.winfo_screenwidth()
        screen_height = audio_window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        my_menu = Menu(audio_window, tearoff=0)
        audio_window.config(menu=my_menu)
        Menu(my_menu, tearoff=0, activebackground="dim grey")
        my_menu.add_command(label="View Streams", command=show_streams_mediainfo)

        audio_window.grid_columnconfigure(0, weight=1)
        audio_window.grid_columnconfigure(1, weight=1)
        audio_window.grid_columnconfigure(2, weight=1)
        audio_window.grid_rowconfigure(0, weight=1)
        audio_window.grid_rowconfigure(1, weight=1)
        audio_window.grid_rowconfigure(2, weight=1)
        audio_window.grid_rowconfigure(3, weight=1)
        audio_window.grid_rowconfigure(6, weight=1)

        # Using VBR or CBR/ABR ----------------------------------------------------------------------------------------
        def mp3_bitrate_type(*args):
            global acodec_bitrate
            global acodec_bitrate_choices

            def acodec_bitrate_menu_hover(e):
                acodec_bitrate_menu["bg"] = "grey"
                acodec_bitrate_menu["activebackground"] = "grey"

            def acodec_bitrate_menu_hover_leave(e):
                acodec_bitrate_menu["bg"] = "#23272A"

            if mp3_vbr.get() == '-q:a ':
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
                acodec_bitrate.set('VBR: -V 0')
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
                mp3_abr.set("")
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
                acodec_bitrate.set('192k')
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
            example_cmd_output = acodec_stream_choices[acodec_stream.get()] \
                                 + encoder_dropdownmenu_choices[encoder.get()] \
                                 + acodec_bitrate_choices[acodec_bitrate.get()] \
                                 + acodec_channel_choices[acodec_channel.get()] + mp3_abr.get() \
                                 + acodec_samplerate_choices[acodec_samplerate.get()] \
                                 + acodec_gain_choices[acodec_gain.get()] + mp3_custom_cmd_input
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
        apply_button.grid(row=6, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        apply_button.bind("<Enter>", apply_button_hover)
        apply_button.bind("<Leave>", apply_button_hover_leave)

        show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A", \
                          command=view_command)
        show_cmd.grid(row=6, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        show_cmd.bind("<Enter>", show_cmd_hover)
        show_cmd.bind("<Leave>", show_cmd_hover_leave)
        # ----------------------------------------------------------------------------------------------------- Buttons

        # Audio VBR Menu ----------------------------------------------------------------------------------------------
        acodec_bitrate = StringVar(audio_window)
        acodec_bitrate_choices = {'VBR: -V 0': '-q:a 0 ',
                                  'VBR: -V 1': '-q:a 1 ',
                                  'VBR: -V 2': '-q:a 2 ',
                                  'VBR: -V 3': '-q:a 3 ',
                                  'VBR: -V 4': '-q:a 4 ',
                                  'VBR: -V 5': '-q:a 5 ',
                                  'VBR: -V 6': '-q:a 6 ',
                                  'VBR: -V 7': '-q:a 7 '}
        acodec_bitrate.set('VBR: -V 0')
        acodec_bitrate_menu_label = Label(audio_window, text="Quality :", background="#434547", foreground="white")
        acodec_bitrate_menu_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_bitrate_menu = OptionMenu(audio_window, acodec_bitrate, *acodec_bitrate_choices.keys())
        acodec_bitrate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_bitrate_menu.grid(row=3, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_bitrate_menu["menu"].configure(activebackground="dim grey")
        acodec_bitrate_menu.bind("<Enter>", acodec_bitrate_menu_hover)
        acodec_bitrate_menu.bind("<Leave>", acodec_bitrate_menu_hover_leave)
        # --------------------------------------------------------------------------------------------------------- VBR

        # Audio Channel Selection -------------------------------------------------------------------------------------
        acodec_channel = StringVar(audio_window)
        acodec_channel_choices = {'Original': "",
                                  '1 (Mono)': "-ac 1 ",
                                  '2 (Stereo)': "-ac 2 "}
        acodec_channel.set('Original')  # set the default option
        achannel_menu_label = Label(audio_window, text="Channels :", background="#434547", foreground="white")
        achannel_menu_label.grid(row=0, column=1, columnspan=1, padx=10, pady=3, sticky=W + E)
        achannel_menu = OptionMenu(audio_window, acodec_channel, *acodec_channel_choices.keys())
        achannel_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        achannel_menu.grid(row=1, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        achannel_menu["menu"].configure(activebackground="dim grey")
        achannel_menu.bind("<Enter>", achannel_menu_hover)
        achannel_menu.bind("<Leave>", achannel_menu_hover_leave)
        # ----------------------------------------------------------------------------------------------- Audio Channel

        # VBR ---------------------------------------------------------------------------------------------------------
        global mp3_vbr
        mp3_vbr = StringVar()
        mp3_vbr.set("-q:a ")
        mp3_vbr_checkbox = Checkbutton(audio_window, text='VBR', variable=mp3_vbr, onvalue='-q:a ',
                                       offvalue='off')
        mp3_vbr_checkbox.grid(row=2, column=0, rowspan=1, columnspan=1, padx=10, pady=(5, 0), sticky=N + S + E + W)
        mp3_vbr_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                   activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        mp3_vbr.trace('w', mp3_bitrate_type)
        # --------------------------------------------------------------------------------------------------------- VBR

        # ABR ---------------------------------------------------------------------------------------------------------
        global mp3_abr
        mp3_abr = StringVar()
        mp3_abr.set("")
        mp3_abr_checkbox = Checkbutton(audio_window, text='ABR', variable=mp3_abr, onvalue="-abr 1 ",
                                       offvalue="", state=DISABLED)
        mp3_abr_checkbox.grid(row=3, column=0, rowspan=1, columnspan=1, padx=10, pady=(0, 5), sticky=N + S + E + W)
        mp3_abr_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                   activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))

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
        mp3_cmd_entrybox_label = Label(audio_window, text="Custom Command Line :", anchor=W, background="#434547", \
                                       foreground="white")
        mp3_cmd_entrybox_label.grid(row=4, column=0, columnspan=2, padx=10, pady=(10, 0), sticky=N + S + W + E)
        mp3_cmd_entrybox = Entry(audio_window, textvariable=mp3_custom_cmd, borderwidth=4, background="#CACACA")
        mp3_cmd_entrybox.grid(row=5, column=0, columnspan=3, padx=10, pady=(0, 15), sticky=W + E)
        mp3_custom_cmd.trace('w', mp3_cmd)
        mp3_custom_cmd.set("")
        # ----------------------------------------------------------------------------------------- Custom Command Line

        # Audio Stream Selection --------------------------------------------------------------------------------------
        acodec_stream = StringVar(audio_window)
        acodec_stream_choices = acodec_stream_track_counter
        acodec_stream.set('Track 1')
        acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
        acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
        acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_stream_menu["menu"].configure(activebackground="dim grey")
        acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
        acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)
        # ------------------------------------------------------------------------------------------------ Audio Stream

        # Audio Gain Selection ----------------------------------------------------------------------------------------
        acodec_gain = StringVar(audio_window)
        acodec_gain_choices = {'Default (0)': "",
                               '+10 dB': "-af volume=10dB ",
                               '+9 dB': "-af volume=9dB ",
                               '+8 dB': "-af volume=8dB ",
                               '+7 dB': "-af volume=7dB ",
                               '+6 dB': "-af volume=6dB ",
                               '+5 dB': "-af volume=5dB ",
                               '+4 dB': "-af volume=4dB ",
                               '+3 dB': "-af volume=3dB ",
                               '+2 dB': "-af volume=2dB ",
                               '+1 dB': "-af volume=1dB ",
                               '-1 dB': "-af volume=-1dB ",
                               '-2 dB': "-af volume=-2dB ",
                               '-3 dB': "-af volume=-3dB ",
                               '-4 dB': "-af volume=-4dB ",
                               '-5 dB': "-af volume=-5dB ",
                               '-6 dB': "-af volume=-6dB ",
                               '-7 dB': "-af volume=-7dB ",
                               '-8 dB': "-af volume=-8dB ",
                               '-9 dB': "-af volume=-9dB ",
                               '-10 dB': "-af volume=-10dB "}
        acodec_gain.set('Default (0)')  # set the default option
        acodec_gain_label = Label(audio_window, text="Gain :", background="#434547", foreground="white")
        acodec_gain_label.grid(row=2, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_gain_menu = OptionMenu(audio_window, acodec_gain, *acodec_gain_choices.keys())
        acodec_gain_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_gain_menu.grid(row=3, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_gain_menu["menu"].configure(activebackground="dim grey")
        acodec_gain_menu.bind("<Enter>", acodec_gain_menu_hover)
        acodec_gain_menu.bind("<Leave>", acodec_gain_menu_hover_leave)
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
        acodec_samplerate.set('Original')  # set the default option
        acodec_samplerate_label = Label(audio_window, text="Sample Rate :", background="#434547", foreground="white")
        acodec_samplerate_label.grid(row=0, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_samplerate_menu = OptionMenu(audio_window, acodec_samplerate, *acodec_samplerate_choices.keys())
        acodec_samplerate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_samplerate_menu.grid(row=1, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_samplerate_menu["menu"].configure(activebackground="dim grey")
        acodec_samplerate_menu.bind("<Enter>", acodec_samplerate_menu_hover)
        acodec_samplerate_menu.bind("<Leave>", acodec_samplerate_menu_hover_leave)
        # ------------------------------------------------------------------------------------------------- Sample Rate
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
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        my_menu = Menu(audio_window, tearoff=0)
        audio_window.config(menu=my_menu)
        Menu(my_menu, tearoff=0, activebackground="dim grey")
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
        audio_window.grid_rowconfigure(11, weight=1)
        audio_window.grid_rowconfigure(12, weight=1)
        audio_window.grid_rowconfigure(13, weight=1)
        audio_window.grid_rowconfigure(14, weight=1)
        audio_window.grid_rowconfigure(15, weight=1)
        audio_window.grid_rowconfigure(16, weight=1)
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

        show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A", \
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
        eac3_cmd_entrybox_label = Label(audio_window, text="Custom Command Line :", anchor=W, background="#434547", \
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
        eac3_spinbox.set("448k ")
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
        acodec_channel.set('Original')  # set the default option
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
        acodec_stream.set('Track 1')
        acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
        acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
        acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
        acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        acodec_stream_menu["menu"].configure(activebackground="dim grey")
        acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
        acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)
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
        ffmpeg_gain.trace('w', audio_filter_function)
        ffmpeg_gain.set(0)
        # -------------------------------------------------------------------------------------------------------- Gain

        # Audio Sample Rate Selection ---------------------------------------------------------------------------------
        acodec_samplerate = StringVar(audio_window)
        acodec_samplerate_choices = {'Original': "",
                                     '32000 Hz': "-ar 32000 ",
                                     '44100 Hz': "-ar 44100 ",
                                     '48000 Hz': "-ar 48000 "}
        acodec_samplerate.set('Original')  # set the default option
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
        per_frame_metadata.set('Default')  # set the default option
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
        eac3_mixing_level.set(-1)
        # ------------------------------------------------------------------------------------------------ Mixing Level

        # Room Type Selection -----------------------------------------------------------------------------------------
        global room_type, room_type_choices
        room_type = StringVar(audio_window)
        room_type_choices = {'Default': "",
                             'Not Indicated': "-room_type 0 ",
                             'Large': "-room_type 1 ",
                             'Small': "-room_type 2 "}
        room_type.set('Default')  # set the default option
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
        copyright_bit.set(-1)
        # --------------------------------------------------------------------------------------------------- Copyright

        # Dialogue Level Spinbox --------------------------------------------------------------------------------------
        global dialogue_level
        dialogue_level = StringVar()
        dialogue_level_label = Label(audio_window, text="Dialogue Level (dB) :", background="#434547", \
                                     foreground="white")
        dialogue_level_label.grid(row=7, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        dialogue_level_spinbox = Spinbox(audio_window, from_=-31, to=-1, justify=CENTER, wrap=True,
                                         textvariable=dialogue_level, state='readonly')
        dialogue_level_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                      buttonbackground="black", width=10, readonlybackground="#23272A")
        dialogue_level_spinbox.grid(row=8, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        dialogue_level.set(-31)
        # ---------------------------------------------------------------------------------------------- Dialogue Level

        # Dolby Surround Mode Selection -------------------------------------------------------------------------------
        global dolby_surround_mode, dolby_surround_mode_choices
        dolby_surround_mode = StringVar(audio_window)
        dolby_surround_mode_choices = {'Default': "",
                                       'Not Indicated': "-dsur_mode 0 ",
                                       'On': "-dsur_mode 1 ",
                                       'Off': "-dsur_mode 2 "}
        dolby_surround_mode.set('Default')  # set the default option
        dolby_surround_mode_label = Label(audio_window, text="Dolby Surround Mode :", background="#434547", \
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
        original_bit_stream_label = Label(audio_window, text="Original Bit Stream :", background="#434547", \
                                          foreground="white")
        original_bit_stream_label.grid(row=9, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        original_bit_stream_spinbox = Spinbox(audio_window, from_=-1, to=1, justify=CENTER, wrap=True,
                                              textvariable=original_bit_stream, state='readonly')
        original_bit_stream_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                           buttonbackground="black", width=10, readonlybackground="#23272A")
        original_bit_stream_spinbox.grid(row=10, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        original_bit_stream.set(-1)
        # -------------------------------------------------------------------------------------------------- Bit Stream

        # Downmix Mode Selection --------------------------------------------------------------------------------------
        global downmix_mode, downmix_mode_choices
        downmix_mode = StringVar(audio_window)
        downmix_mode_choices = {'Default': "",
                                'Not Indicated': "-dmix_mode 0 ",
                                'Lt/RT Downmix': "-dmix_mode 1 ",
                                'Lo/Ro Downmix': "-dmix_mode 2 ",
                                'Dolby Pro Logic II': "-dmix_mode 3 "}
        downmix_mode.set('Default')  # set the default option
        downmix_mode_label = Label(audio_window, text="Stereo Downmix Mode :", background="#434547", \
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
        lt_rt_center_mix_label = Label(audio_window, text="Lt/Rt Center\nMix Level :", background="#434547", \
                                       foreground="white")
        lt_rt_center_mix_label.grid(row=9, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        lt_rt_center_mix_spinbox = Spinbox(audio_window, from_=-1, to=1, justify=CENTER, wrap=True,
                                           textvariable=lt_rt_center_mix, state='readonly', increment=0.1)
        lt_rt_center_mix_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                        buttonbackground="black", width=10, readonlybackground="#23272A")
        lt_rt_center_mix_spinbox.grid(row=10, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        lt_rt_center_mix.set(-1)
        # -------------------------------------------------------------------------------------- Lt/Rt Center Mix Level

        # Lt/Rt Surround Mix Level Spinbox ----------------------------------------------------------------------------
        global lt_rt_surround_mix
        lt_rt_surround_mix = StringVar()
        lt_rt_surround_mix_label = Label(audio_window, text="Lt/Rt Surround\nMix Level :", background="#434547", \
                                         foreground="white")
        lt_rt_surround_mix_label.grid(row=11, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        lt_rt_surround_mix_spinbox = Spinbox(audio_window, from_=-1, to=1, justify=CENTER, wrap=True,
                                             textvariable=lt_rt_surround_mix, state='readonly', increment=0.1)
        lt_rt_surround_mix_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                          buttonbackground="black", width=10, readonlybackground="#23272A")
        lt_rt_surround_mix_spinbox.grid(row=12, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        lt_rt_surround_mix.set(-1)
        # ------------------------------------------------------------------------------------ Lt/Rt Surround Mix Level

        # Lo/Ro Center Mix Level Spinbox ------------------------------------------------------------------------------
        global lo_ro_center_mix
        lo_ro_center_mix = StringVar()
        lo_ro_center_mix_label = Label(audio_window, text="Lo/Ro Center\nMix Level :", background="#434547", \
                                       foreground="white")
        lo_ro_center_mix_label.grid(row=11, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        lo_ro_center_mix_spinbox = Spinbox(audio_window, from_=-1, to=1, justify=CENTER, wrap=True,
                                           textvariable=lo_ro_center_mix, state='readonly', increment=0.1)
        lo_ro_center_mix_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                        buttonbackground="black", width=10, readonlybackground="#23272A")
        lo_ro_center_mix_spinbox.grid(row=12, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        lo_ro_center_mix.set(-1)
        # -------------------------------------------------------------------------------------- Lo/Ro Center Mix Level

        # Lo/Ro Surround Mix Level Spinbox ----------------------------------------------------------------------------
        global lo_ro_surround_mix
        lo_ro_surround_mix = StringVar()
        lo_ro_surround_mix_label = Label(audio_window, text="Lo/Ro Surround\nMix Level :", background="#434547", \
                                         foreground="white")
        lo_ro_surround_mix_label.grid(row=11, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        lo_ro_surround_mix_spinbox = Spinbox(audio_window, from_=-1, to=1, justify=CENTER, wrap=True,
                                             textvariable=lo_ro_surround_mix, state='readonly', increment=0.1)
        lo_ro_surround_mix_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                          buttonbackground="black", width=10, readonlybackground="#23272A")
        lo_ro_surround_mix_spinbox.grid(row=12, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        lo_ro_surround_mix.set(-1)
        # ------------------------------------------------------------------------------------ Lo/Ro Surround Mix Level

        # Dolby Surround EX Mode Selection ----------------------------------------------------------------------------
        global dolby_surround_ex_mode, dolby_surround_ex_mode_choices
        dolby_surround_ex_mode = StringVar(audio_window)
        dolby_surround_ex_mode_choices = {'Default': "",
                                          'Not Indicated': "-dsurex_mode 0 ",
                                          'On': "-dsurex_mode 2 ",
                                          'Off': "-dsurex_mode 1 ",
                                          'Dolby Pro Login IIz': "-dsurex_mode 3 "}
        dolby_surround_ex_mode.set('Default')  # set the default option
        dolby_surround_ex_mode_label = Label(audio_window, text="Dolby Surround EX Mode :", background="#434547", \
                                             foreground="white")
        dolby_surround_ex_mode_label.grid(row=13, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        dolby_surround_ex_mode_menu = OptionMenu(audio_window, dolby_surround_ex_mode, \
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
        dolby_headphone_mode.set('Default')  # set the default option
        dolby_headphone_mode_label = Label(audio_window, text="Dolby Headphone Mode :", background="#434547", \
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
        a_d_converter_type.set('Default')  # set the default option
        a_d_converter_type_label = Label(audio_window, text="A/D Converter Type :", background="#434547", \
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
        stereo_rematrixing.set('Default')  # set the default option
        stereo_rematrixing_label = Label(audio_window, text="Stereo Rematrixing :", background="#434547", \
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
        channel_coupling_label = Label(audio_window, text="Channel Coupling :", background="#434547", \
                                       foreground="white")
        channel_coupling_label.grid(row=15, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        channel_coupling_spinbox = Spinbox(audio_window, from_=-1, to=1, justify=CENTER, wrap=True,
                                           textvariable=channel_coupling, state='readonly')
        channel_coupling_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                        buttonbackground="black", width=10, readonlybackground="#23272A")
        channel_coupling_spinbox.grid(row=16, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        channel_coupling.set(-1)
        # -------------------------------------------------------------------------------------------- Channel Coupling

        # Channel CPL Band Spinbox ------------------------------------------------------------------------------------
        global cpl_start_band
        cpl_start_band = StringVar()
        cpl_start_band_label = Label(audio_window, text="Coupling Start Band :", background="#434547", \
                                     foreground="white")
        cpl_start_band_label.grid(row=15, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        cpl_start_band_spinbox = Spinbox(audio_window, from_=-1, to=15, justify=CENTER, wrap=True,
                                         textvariable=cpl_start_band, state='readonly')
        cpl_start_band_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                      buttonbackground="black", width=10, readonlybackground="#23272A")
        cpl_start_band_spinbox.grid(row=16, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        cpl_start_band.set(-1)
        # -------------------------------------------------------------------------------------------- Channel CPL Band
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
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        my_menu = Menu(audio_window, tearoff=0)
        audio_window.config(menu=my_menu)
        Menu(my_menu, tearoff=0, activebackground="dim grey")
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
            example_cmd_output = acodec_stream_choices[acodec_stream.get()] + \
                                 acodec_channel_choices[acodec_channel.get()] + \
                                 acodec_samplerate_choices[acodec_samplerate.get()] + \
                                 acodec_gain_choices[acodec_gain.get()] + "-f caf - | " + \
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

        show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A", \
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
        acodec_bitrate.set('CBR: 192k')  # set the default option
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
        acodec_channel.set('Original')  # set the default option
        achannel_menu_label = Label(audio_window, text="Channels :", background="#434547", foreground="white")
        achannel_menu_label.grid(row=0, column=1, columnspan=1, padx=10, pady=3, sticky=W + E)
        achannel_menu = OptionMenu(audio_window, acodec_channel, *acodec_channel_choices.keys())
        achannel_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        achannel_menu.grid(row=1, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        achannel_menu["menu"].configure(activebackground="dim grey")
        achannel_menu.bind("<Enter>", achannel_menu_hover)
        achannel_menu.bind("<Leave>", achannel_menu_hover_leave)
        # ----------------------------------------------------------------------------------------------------- Channel

        # Audio Stream Selection --------------------------------------------------------------------------------------
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
        # ------------------------------------------------------------------------------------------------------ Stream

        # Audio Gain Selection ----------------------------------------------------------------------------------------
        acodec_gain = StringVar(audio_window)
        acodec_gain_choices = {'Default (0)': "",
                               '+10 dB': "-af volume=10dB ",
                               '+9 dB': "-af volume=9dB ",
                               '+8 dB': "-af volume=8dB ",
                               '+7 dB': "-af volume=7dB ",
                               '+6 dB': "-af volume=6dB ",
                               '+5 dB': "-af volume=5dB ",
                               '+4 dB': "-af volume=4dB ",
                               '+3 dB': "-af volume=3dB ",
                               '+2 dB': "-af volume=2dB ",
                               '+1 dB': "-af volume=1dB ",
                               '-1 dB': "-af volume=-1dB ",
                               '-2 dB': "-af volume=-2dB ",
                               '-3 dB': "-af volume=-3dB ",
                               '-4 dB': "-af volume=-4dB ",
                               '-5 dB': "-af volume=-5dB ",
                               '-6 dB': "-af volume=-6dB ",
                               '-7 dB': "-af volume=-7dB ",
                               '-8 dB': "-af volume=-8dB ",
                               '-9 dB': "-af volume=-9dB ",
                               '-10 dB': "-af volume=-10dB "}
        acodec_gain.set('Default (0)')  # set the default option
        acodec_gain_label = Label(audio_window, text="Gain :", background="#434547", foreground="white")
        acodec_gain_label.grid(row=2, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_gain_menu = OptionMenu(audio_window, acodec_gain, *acodec_gain_choices.keys())
        acodec_gain_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        acodec_gain_menu.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        acodec_gain_menu["menu"].configure(activebackground="dim grey")
        acodec_gain_menu.bind("<Enter>", acodec_gain_menu_hover)
        acodec_gain_menu.bind("<Leave>", acodec_gain_menu_hover_leave)
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
        acodec_samplerate.set('Original')  # set the default option
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
        fdkaac_cmd_entrybox_label = Label(audio_window, text="Custom Command Line :", anchor=W, background="#434547", \
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
        fdkaac_title_entrybox_label = Label(audio_window, text="Track Name :", anchor=W, background="#434547", \
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
        acodec_profile.set('AAC LC (Default)')  # set the default option
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
        acodec_lowdelay.set('Disable SBR on ELD (DEF)')  # set the default option
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
        # --------------------------------------------------------------------------------------------------- SBR Ratio

        # Audio Gapless Mode ------------------------------------------------------------------------------------------
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
        acodec_transport_format.set('M4A (Def)')  # set the default option
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
        afterburnervar.set("-a1 ")
        afterburner_checkbox = Checkbutton(audio_window, text='Afterburner', variable=afterburnervar, onvalue="-a1 ",
                                           offvalue="-a0 ")
        afterburner_checkbox.grid(row=8, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        afterburner_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                       activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        # ------------------------------------------------------------------------------------------------- Afterburner

        # Misc Checkboxes - Add CRC Check on ADTS Header --------------------------------------------------------------
        global crccheck
        crccheck = StringVar()
        crccheck.set("")
        crccheck_checkbox = Checkbutton(audio_window, text='CRC Check on\n ADTS Header', variable=crccheck,
                                        onvalue="-C ", offvalue="")
        crccheck_checkbox.grid(row=9, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        crccheck_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                    activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        # --------------------------------------------------------------------------------------------------------- CRC

        # Misc Checkboxes - Header Period -----------------------------------------------------------------------------
        global headerperiod
        headerperiod = StringVar()
        headerperiod.set("")
        headerperiod_checkbox = Checkbutton(audio_window, text='Header Period', variable=headerperiod,
                                            onvalue="-h ", offvalue="")
        headerperiod_checkbox.grid(row=9, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        headerperiod_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                        activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        # ------------------------------------------------------------------------------------------------------ Header

        # Misc Checkboxes - Include SBR Delay -------------------------------------------------------------------------
        global sbrdelay
        sbrdelay = StringVar()
        sbrdelay.set("")
        sbrdelay_checkbox = Checkbutton(audio_window, text='SBR Delay', variable=sbrdelay,
                                        onvalue="--include-sbr-delay ", offvalue="")
        sbrdelay_checkbox.grid(row=9, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        sbrdelay_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                    activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        # --------------------------------------------------------------------------------------------------- SBR Delay

        # Misc Checkboxes - Place Moov Box Before Mdat Box ------------------------------------------------------------
        global moovbox
        moovbox = StringVar()
        moovbox.set("")
        moovbox_checkbox = Checkbutton(audio_window, text='Place Moov Box Before Mdat Box', variable=moovbox,
                                       onvalue="--moov-before-mdat ", offvalue="", anchor='w')
        moovbox_checkbox.grid(row=10, column=1, columnspan=3, padx=10, pady=3, sticky=N + S + E + W)
        moovbox_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                   activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        # ---------------------------------------------------------------------------------------------------- Moov Box
    # --------------------------------------------------------------------------------------------------------- FDK AAC

    # 1 Window -----------------------------------------------------------------------------------------------------
    elif encoder.get() == "QAAC":
        audio_window = Toplevel()
        audio_window.title('QAAC Settings')
        audio_window.configure(background="#434547")
        window_height = 700
        window_width = 750
        screen_width = audio_window.winfo_screenwidth()
        screen_height = audio_window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        my_menu = Menu(audio_window, tearoff=0)
        audio_window.config(menu=my_menu)
        Menu(my_menu, tearoff=0, activebackground="dim grey")
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
        audio_window.grid_rowconfigure(14, weight=1)


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
            if q_acodec_profile.get() == "True VBR":
                example_cmd_output = acodec_stream_choices[acodec_stream.get()] + acodec_channel_choices[
                                     acodec_channel.get()] + acodec_samplerate_choices[acodec_samplerate.get()] \
                                     + "\n \n" + "-f wav - | " + qaac + " " + "\n \n" \
                                     + q_acodec_profile_choices[q_acodec_profile.get()] + q_acodec_quality_amnt.get() \
                                     + " " + qaac_high_efficiency.get() + qaac_normalize.get() + qaac_nodither.get() \
                                     + "--gain " + q_acodec_gain.get() + " " + \
                                     q_acodec_quality_choices[q_acodec_quality.get()] + qaac_normalize.get() \
                                     + qaac_nodelay.get() + q_gapless_mode_choices[q_gapless_mode.get()] \
                                     + qaac_nooptimize.get() + qaac_threading.get() + qaac_limiter.get() \
                                     + qaac_title_input + qaac_custom_cmd_input
            else:
                example_cmd_output = acodec_stream_choices[acodec_stream.get()] + \
                                     acodec_channel_choices[acodec_channel.get()] + \
                                     acodec_samplerate_choices[acodec_samplerate.get()] \
                                     + "\n \n" + "-f wav - | " + qaac + " " + "\n \n" \
                                     + q_acodec_profile_choices[q_acodec_profile.get()] + \
                                     q_acodec_bitrate.get() + " " + qaac_high_efficiency.get() + qaac_normalize.get() \
                                     + qaac_nodither.get() + "--gain " + q_acodec_gain.get() + " " \
                                     + q_acodec_quality_choices[q_acodec_quality.get()] + qaac_normalize.get() \
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
        apply_button.grid(row=14, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        apply_button.bind("<Enter>", apply_button_hover)
        apply_button.bind("<Leave>", apply_button_hover_leave)

        show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A", \
                          command=view_command)
        show_cmd.grid(row=14, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        show_cmd.bind("<Enter>", show_cmd_hover)
        show_cmd.bind("<Leave>", show_cmd_hover_leave)

        help_button = Button(audio_window, text="Help + Information", foreground="white", background="#23272A",
                             command=gotoqaachelp)
        help_button.grid(row=14, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
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
            elif q_acodec_profile.get() == 'Constrained VBR' or q_acodec_profile.get() == 'ABR' or \
                    q_acodec_profile.get() == 'CBR':
                q_acodec_quality_spinbox.configure(state=DISABLED)
                q_acodec_bitrate_spinbox.configure(state=NORMAL)
                qaac_high_efficiency_checkbox.configure(state=NORMAL)
        # ------------------------------------------------------------------------------------------ Quality or Bitrate

        # Audio Profile Menu ------------------------------------------------------------------------------------------
        global q_acodec_profile
        global q_acodec_profile_choices
        q_acodec_profile = StringVar(audio_window)
        q_acodec_profile_choices = {'True VBR': "--tvbr ",
                                    'Constrained VBR': "--cvbr ",
                                    'ABR': "--abr ",
                                    'CBR': "--cbr "}
        q_acodec_profile.set('True VBR')  # set the default option
        q_acodec_profile.trace('w', quality_or_bitrate)
        q_acodec_profile_menu_label = Label(audio_window, text="Mode :", background="#434547", foreground="white")
        q_acodec_profile_menu_label.grid(row=2, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
        q_acodec_profile_menu = OptionMenu(audio_window, q_acodec_profile, *q_acodec_profile_choices.keys())
        q_acodec_profile_menu.config(background="#23272A", foreground="white", highlightthickness=1)
        q_acodec_profile_menu.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
        q_acodec_profile_menu["menu"].configure(activebackground="dim grey")
        q_acodec_profile_menu.bind("<Enter>", q_acodec_profile_hover)
        q_acodec_profile_menu.bind("<Leave>", q_acodec_profile_hover_leave)
        # ------------------------------------------------------------------------------------------ Audio Profile Menu

        # Audio Channel Selection -------------------------------------------------------------------------------------
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
        # ----------------------------------------------------------------------------------------------- Audio Channel

        # Audio Stream Selection --------------------------------------------------------------------------------------
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
        qaac_cmd_entrybox_label = Label(audio_window, text="Custom Command Line :", anchor=W, background="#434547", \
                                          foreground="white")
        qaac_cmd_entrybox_label.grid(row=10, column=0, columnspan=2, padx=10, pady=(0, 0), sticky=N + S + W + E)
        qaac_cmd_entrybox = Entry(audio_window, textvariable=qaac_custom_cmd, borderwidth=4, background="#CACACA")
        qaac_cmd_entrybox.grid(row=11, column=0, columnspan=3, padx=10, pady=(0, 0), sticky=W + E)
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
        qaac_title_entrybox_label = Label(audio_window, text="Track Name :", anchor=W, background="#434547", \
                                            foreground="white")
        qaac_title_entrybox_label.grid(row=12, column=0, columnspan=2, padx=10, pady=(5, 0), sticky=N + S + W + E)
        qaac_title_entrybox = Entry(audio_window, textvariable=qaac_title, borderwidth=4, background="#CACACA")
        qaac_title_entrybox.grid(row=13, column=0, columnspan=3, padx=10, pady=(0, 10), sticky=W + E)
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
        acodec_samplerate.set('Original')  # set the default option
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
        q_acodec_quality.set('High (Default)')  # set the default option
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
        q_acodec_quality_amnt.set(50)  # set the default option
        q_acodec_quality_spinbox_label = Label(audio_window, text="T-VBR Quality :", background="#434547",
                                               foreground="white")
        q_acodec_quality_spinbox_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        q_acodec_quality_spinbox = Spinbox(audio_window, from_=0, to=127, justify=CENTER, wrap=True,
                                           textvariable=q_acodec_quality_amnt, width=13)
        q_acodec_quality_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                        buttonbackground="black", disabledbackground='grey')
        q_acodec_quality_spinbox.grid(row=3, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        # ----------------------------------------------------------------------------------------------------- Quality

        # Audio Bitrate -----------------------------------------------------------------------------------------------
        global q_acodec_bitrate
        q_acodec_bitrate = StringVar(audio_window)
        q_acodec_bitrate.set(256)  # set the default option
        q_acodec_bitrate_label = Label(audio_window, text="Bitrate :", background="#434547", foreground="white")
        q_acodec_bitrate_label.grid(row=2, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        q_acodec_bitrate_spinbox = Spinbox(audio_window, from_=0, to=1280, justify=CENTER, wrap=True,
                                           textvariable=q_acodec_bitrate, width=13, state=DISABLED)
        q_acodec_bitrate_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                        buttonbackground="black", disabledbackground='grey')
        q_acodec_bitrate_spinbox.grid(row=3, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
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
        q_acodec_gain.set(0)
        # -------------------------------------------------------------------------------------------------------- Gain

        # Misc Checkboxes - Normalize ---------------------------------------------------------------------------------
        global qaac_normalize
        qaac_normalize = StringVar()
        qaac_normalize.set("")
        qaac_normalize_checkbox = Checkbutton(audio_window, text='Normalize', variable=qaac_normalize,
                                              onvalue="--normalize ",
                                              offvalue="")
        qaac_normalize_checkbox.grid(row=5, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        qaac_normalize_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                          activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        # --------------------------------------------------------------------------------------------------- Normalize

        # Misc Checkboxes - High Efficiency ---------------------------------------------------------------------------
        global qaac_high_efficiency
        qaac_high_efficiency = StringVar()
        qaac_high_efficiency.set("")
        qaac_high_efficiency_checkbox = Checkbutton(audio_window, text='High Efficiency', variable=qaac_high_efficiency,
                                                    onvalue="--he ",
                                                    offvalue="", state=DISABLED)
        qaac_high_efficiency_checkbox.grid(row=8, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        qaac_high_efficiency_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                                activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        # --------------------------------------------------------------------------------------------- High Effeciency

        # Misc Checkboxes - No Dither When Quantizing to Lower Bit Depth ----------------------------------------------
        global qaac_nodither
        qaac_nodither = StringVar()
        qaac_nodither.set("")
        qaac_nodither_checkbox = Checkbutton(audio_window, text='No Dither',
                                             variable=qaac_nodither, onvalue="--no-dither ",
                                             offvalue="")
        qaac_nodither_checkbox.grid(row=7, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        qaac_nodither_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                         activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        # --------------------------------------------------------------------------------------------------- No Dither

        # Misc Checkboxes - No Delay ----------------------------------------------------------------------------------
        global qaac_nodelay
        qaac_nodelay = StringVar()
        qaac_nodelay.set("")
        qaac_nodelay_checkbox = Checkbutton(audio_window, text='No Delay',
                                             variable=qaac_nodelay, onvalue="--no-delay ",
                                             offvalue="")
        qaac_nodelay_checkbox.grid(row=7, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        qaac_nodelay_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                         activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        # ---------------------------------------------------------------------------------------------------- No Delay

        # Gapless Mode ------------------------------------------------------------------------------------------------
        global q_gapless_mode
        global q_gapless_mode_choices
        q_gapless_mode = StringVar(audio_window)
        q_gapless_mode_choices = {'iTunSMPB (default)': "",
                                    'ISO standard': "--gapless-mode 1 ",
                                    'Both': "--gapless-mode 2 "}
        q_gapless_mode.set('iTunSMPB (default)')  # set the default option
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
        qaac_nooptimize.set("")
        qaac_nooptimize_checkbox = Checkbutton(audio_window, text='No Optimize',
                                             variable=qaac_nooptimize, onvalue="--no-optimize ",
                                             offvalue="")
        qaac_nooptimize_checkbox.grid(row=7, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        qaac_nooptimize_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                         activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        # ------------------------------------------------------------------------------------------------- No Optimize

        # Misc Checkboxes - Threading ---------------------------------------------------------------------------------
        global qaac_threading
        qaac_threading = StringVar()
        qaac_threading.set("")
        qaac_threading_checkbox = Checkbutton(audio_window, text='Threading',
                                             variable=qaac_threading, onvalue="--no-optimize ",
                                             offvalue="")
        qaac_threading_checkbox.grid(row=8, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        qaac_threading_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                         activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        # --------------------------------------------------------------------------------------------------- Threading

        # Misc Checkboxes - Limiter -----------------------------------------------------------------------------------
        global qaac_limiter
        qaac_limiter = StringVar()
        qaac_limiter.set("")
        qaac_limiter_checkbox = Checkbutton(audio_window, text='Limiter',
                                             variable=qaac_limiter, onvalue="--limiter ",
                                             offvalue="")
        qaac_limiter_checkbox.grid(row=9, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
        qaac_limiter_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                         activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        # ----------------------------------------------------------------------------------------------------- Limiter
    # ----------------------------------------------------------------------------------------------------------- QAAC
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
                                                           "MOV, MKA, WAV, MP3, AAC, OGG, OGV, M4V, MPEG, AVI, VOB, "
                                                           "WEBM, MKV, MP4, DTS, AC3, MT2S, WAV",
                                                           "*.mov *.wav *.mt2s *.ac3 *.mka *.wav *.mp3 *.aac *.ogg "
                                                           "*.ogv *.m4v *.mpeg *.avi *.vob *.webm *.mp4 *.mkv *.dts"),
                                                       ("All Files", "*.*")))
    input_entry.configure(state=NORMAL)
    input_entry.delete(0, END)
    file_extension = pathlib.Path(VideoInput).suffix
    if VideoInput:
        if file_extension == '.wav' or file_extension == '.mt2s' or file_extension == '.ac3' or \
                file_extension == '.mka' or \
                file_extension == '.wav' or file_extension == '.mp3' or file_extension == '.aac' or \
                file_extension == '.ogg' or file_extension == '.ogv' or file_extension == '.m4v' or \
                file_extension == '.mpeg' or file_extension == '.avi' or file_extension == '.vob' or \
                file_extension == '.webm' or file_extension == '.mp4' or file_extension == '.mkv' or \
                file_extension == '.dts' or file_extension == '.m4a' or file_extension == '.mov':
            autofilesave_file_path = pathlib.PureWindowsPath(VideoInput)  # Command to get file input location
            # Final command to get only the directory of fileinput
            autofilesave_dir_path = autofilesave_file_path.parents[0]
            VideoInputQuoted = '"' + VideoInput + '"'
            show_streams_button.config(state=NORMAL)
            encoder_menu.config(state=NORMAL)
            # This gets the total amount of audio streams
            mediainfocli_cmd = '"' + mediainfocli + " " + '--Output="General;%AudioCount%"' \
                               + " " + VideoInputQuoted + '"'
            mediainfo_count = subprocess.Popen('cmd /c ' + mediainfocli_cmd, creationflags=subprocess.CREATE_NO_WINDOW,
                                               universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                               stdin=subprocess.PIPE)
            stdout, stderr = mediainfo_count.communicate()
            track_count = stdout
            show_streams_button.configure(state=NORMAL)
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
        show_streams_button.config(state=DISABLED)
        encoder_menu.config(state=DISABLED)
        audiosettings_button.configure(state=DISABLED)
# ---------------------------------------------------------------------------------------------------------- File Input

# File Output ---------------------------------------------------------------------------------------------------------
def file_save():
    global VideoOutput
    if encoder.get() == "AAC":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".mp4", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location", initialfile=autosavefilename,
                                                   filetypes=(("AAC", "*.mp4"), ("All Files", "*.*")))
    elif encoder.get() == "AC3":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".ac3", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location", initialfile=autosavefilename,
                                                   filetypes=(("AC3", "*.ac3"), ("All Files", "*.*")))
    elif encoder.get() == "DTS":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".dts", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location", initialfile=autosavefilename,
                                                   filetypes=(("DTS", "*.dts"), ("All Files", "*.*")))
    elif encoder.get() == "Opus":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".opus", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location", initialfile=autosavefilename,
                                                   filetypes=(("Opus", "*.opus"), ("All Files", "*.*")))
    elif encoder.get() == "MP3":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".mp3", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location", initialfile=autosavefilename,
                                                   filetypes=(("MP3", "*.mp3"), ("All Files", "*.*")))
    elif encoder.get() == "E-AC3":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".ac3", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location", initialfile=autosavefilename,
                                                   filetypes=(("E-AC3", "*.ac3"), ("All Files", "*.*")))
    elif encoder.get() == "FDK-AAC":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".m4a", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location", initialfile=autosavefilename,
                                                   filetypes=(("AAC", "*.m4a"), ("All Files", "*.*")))
    elif encoder.get() == "QAAC":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".m4a", initialdir=autofilesave_dir_path,
                                                   title="Select a Save Location", initialfile=autosavefilename,
                                                   filetypes=(("AAC", "*.m4a"), ("All Files", "*.*")))

    if VideoOutput:
        output_entry.configure(state=NORMAL)  # Enable entry box for commands under
        output_entry.delete(0, END)  # Remove current text in entry
        output_entry.insert(0, VideoOutput)  # Insert the 'path'
        output_entry.configure(state=DISABLED)  # Disables Entry Box
    if not VideoOutput:
        pass
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

# Print Command Line from ROOT ----------------------------------------------------------------------------------------
def print_command_line():
    cmd_line_window = Toplevel()
    cmd_line_window.title('Command Line')
    cmd_line_window.configure(background="#434547")
    VideoInputQuoted = '"' + VideoInput + '"'
    VideoOutputQuoted = '"' + VideoOutput + '"'
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
                             acodec_gain_choices[acodec_gain.get()] + \
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
                                     acodec_channel.get()] + acodec_samplerate_choices[acodec_samplerate.get()] \
                                 + "\n \n" + "-f wav - | " + qaac + " " + "\n \n" \
                                 + q_acodec_profile_choices[q_acodec_profile.get()] + q_acodec_quality_amnt.get() \
                                 + " " + qaac_high_efficiency.get() + qaac_normalize.get() + qaac_nodither.get() \
                                 + "--gain " + q_acodec_gain.get() + " " + \
                                 q_acodec_quality_choices[q_acodec_quality.get()] + qaac_normalize.get() \
                                 + qaac_nodelay.get() + q_gapless_mode_choices[q_gapless_mode.get()] \
                                 + qaac_nooptimize.get() + qaac_threading.get() + qaac_limiter.get() \
                                 + qaac_title_input + qaac_custom_cmd_input + "- -o " + "\n \n" + VideoOutputQuoted
        else:
            example_cmd_output = ffmpeg + " -analyzeduration 100M -probesize 50M -i " + "\n \n" \
                                 + VideoInputQuoted + "\n \n" + \
                                 acodec_stream_choices[acodec_stream.get()] + \
                                 acodec_channel_choices[acodec_channel.get()] + \
                                 acodec_samplerate_choices[acodec_samplerate.get()] \
                                 + "\n \n" + "-f wav - | " + qaac + " " + "\n \n" \
                                 + q_acodec_profile_choices[q_acodec_profile.get()] + \
                                 q_acodec_bitrate.get() + " " + qaac_high_efficiency.get() + qaac_normalize.get() \
                                 + qaac_nodither.get() + "--gain " + q_acodec_gain.get() + " " \
                                 + q_acodec_quality_choices[q_acodec_quality.get()] + qaac_normalize.get() \
                                 + qaac_nodelay.get() \
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
                             acodec_gain_choices[acodec_gain.get()] + \
                             acodec_samplerate_choices[acodec_samplerate.get()] + \
                             acodec_gain_choices[acodec_gain.get()] + mp3_custom_cmd_input \
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
    cmd_label = Label(cmd_line_window, text=example_cmd_output, foreground="white", background="#434547")
    cmd_label.config(font=("Helvetica", 16))
    cmd_label.pack()
# ---------------------------------------------------------------------------------------- Print Command Line from ROOT

# Start Audio Job -----------------------------------------------------------------------------------------------------
def startaudiojob():
    global example_cmd_output
    # Quote File Input/Output Paths------------
    VideoInputQuoted = '"' + VideoInput + '"'
    VideoOutputQuoted = '"' + VideoOutput + '"'
    # -------------------------- Quote File Paths
    # AC3 Start Job ---------------------------------------------------------------------------------------------------
    if encoder.get() == "AC3":
        finalcommand = '"' + ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + \
                       acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] + \
                       acodec_bitrate_choices[acodec_bitrate.get()] + \
                       acodec_channel_choices[acodec_channel.get()] + \
                       acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting \
                       + "-sn -vn -map_chapters -1 -map_metadata -1 " + ac3_custom_cmd_input + \
                       VideoOutputQuoted + " -hide_banner"
        if shell_options.get() == "Default":
            subprocess.Popen('cmd /c ' + finalcommand + " " + '-v error -stats"')
        elif shell_options.get() == "Debug":
            subprocess.Popen('cmd /k ' + finalcommand + '"')
    # --------------------------------------------------------------------------------------------------------- AC3 Job
    # AAC Start Job ---------------------------------------------------------------------------------------------------
    elif encoder.get() == "AAC":
        if aac_vbr_toggle.get() == "-c:a ":
            bitrate_or_quality = f"-b:a {aac_bitrate_spinbox.get()}k "
        elif aac_vbr_toggle.get() == "-q:a ":
            bitrate_or_quality = f"-q:a {aac_quality_spinbox.get()} "
        finalcommand = '"' + ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + \
                       acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] + \
                       bitrate_or_quality + acodec_channel_choices[acodec_channel.get()] + \
                       acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting \
                       + "-sn -vn -map_chapters -1 -map_metadata -1 " \
                       + aac_custom_cmd_input \
                       + aac_title_input + VideoOutputQuoted + " -hide_banner"
        if shell_options.get() == "Default":
            subprocess.Popen('cmd /c ' + finalcommand + " " + '-v error -stats"')
        elif shell_options.get() == "Debug":
            subprocess.Popen('cmd /k ' + finalcommand + '"')
            # ------------------------------------------------------------------------------------------------- AAC Job
    # DTS Start Job ---------------------------------------------------------------------------------------------------
    elif encoder.get() == 'DTS':
        if dts_settings.get() == 'DTS Encoder':
            finalcommand = '"' + ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + \
                           acodec_stream_choices[acodec_stream.get()] + dts_settings_choices[dts_settings.get()] \
                           + "-b:a " + dts_bitrate_spinbox.get() + "k " \
                           + acodec_channel_choices[acodec_channel.get()] \
                           + acodec_samplerate_choices[acodec_samplerate.get()] \
                           + audio_filter_setting + dts_custom_cmd_input \
                           + "-sn -vn -map_chapters -1 " \
                           + VideoOutputQuoted + " -hide_banner"
        else:
            finalcommand = '"' + ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted \
                           + acodec_stream_choices[acodec_stream.get()] + dts_settings_choices[dts_settings.get()] \
                           + dts_custom_cmd_input + "-sn -vn -map_chapters -1 " \
                           + VideoOutputQuoted + " -hide_banner"
        if shell_options.get() == "Default":
            subprocess.Popen('cmd /c ' + finalcommand + " " + '-v error -stats"')
        elif shell_options.get() == "Debug":
            subprocess.Popen('cmd /k ' + finalcommand + '"')
    # ------------------------------------------------------------------------------------------------------------- DTS
    # Opus Start Job --------------------------------------------------------------------------------------------------
    elif encoder.get() == "Opus":
        finalcommand = '"' + ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + \
                       acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] + \
                       acodec_vbr_choices[acodec_vbr.get()] + acodec_bitrate_choices[acodec_bitrate.get()] + \
                       acodec_channel_choices[acodec_channel.get()] + \
                       acodec_application_choices[acodec_application.get()] + "-packet_loss " + \
                       packet_loss.get() + " -frame_duration " + frame_duration.get() + " " + \
                       acodec_samplerate_choices[acodec_samplerate.get()] + \
                       audio_filter_setting + "-sn -vn -map_chapters -1 -map_metadata -1 " \
                       + opus_custom_cmd_input + VideoOutputQuoted + " -hide_banner"
        if shell_options.get() == "Default":
            subprocess.Popen('cmd /c ' + finalcommand + " " + '-v error -stats"')
        elif shell_options.get() == "Debug":
            subprocess.Popen('cmd /k ' + finalcommand + '"')
    # ------------------------------------------------------------------------------------------------------------ Opus
    # MP3 Start Job ---------------------------------------------------------------------------------------------------
    elif encoder.get() == "MP3":
        finalcommand = '"' + ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + \
                       acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] + \
                       acodec_bitrate_choices[acodec_bitrate.get()] + acodec_channel_choices[acodec_channel.get()] \
                       + mp3_abr.get() + acodec_samplerate_choices[acodec_samplerate.get()] \
                       + acodec_gain_choices[acodec_gain.get()] + "-sn -vn -map_chapters -1 -map_metadata -1 " \
                       + mp3_custom_cmd_input + VideoOutputQuoted + " -hide_banner"
        if shell_options.get() == "Default":
            subprocess.Popen('cmd /c ' + finalcommand + " " + '-v error -stats"')
        elif shell_options.get() == "Debug":
            subprocess.Popen('cmd /k ' + finalcommand + '"')
    # ------------------------------------------------------------------------------------------------------------- MP3
    # E-AC3 Start Job -------------------------------------------------------------------------------------------------
    elif encoder.get() == "E-AC3":
        finalcommand = '"' + ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + \
                       acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] \
                       + "-b:a " + eac3_spinbox.get() + acodec_channel_choices[acodec_channel.get()] \
                       + acodec_samplerate_choices[acodec_samplerate.get()] \
                       + audio_filter_setting + "-sn -vn -map_chapters -1 -map_metadata -1 " \
                       + eac3_custom_cmd_input \
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
                       + "-cpl_start_band " + cpl_start_band.get() + " " + \
                       VideoOutputQuoted + " -hide_banner"
        if shell_options.get() == "Default":
            subprocess.Popen('cmd /c ' + finalcommand + " " + '-v error -stats"')
        elif shell_options.get() == "Debug":
            subprocess.Popen('cmd /k ' + finalcommand + '"')
    # ----------------------------------------------------------------------------------------------------------- E-AC3
    # FDK_AAC Start Job -----------------------------------------------------------------------------------------------
    elif encoder.get() == "FDK-AAC":
        finalcommand = '"' + ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted + \
                       acodec_stream_choices[acodec_stream.get()] + acodec_channel_choices[acodec_channel.get()] + \
                       acodec_samplerate_choices[acodec_samplerate.get()] + \
                       acodec_gain_choices[acodec_gain.get()] + \
                       "-f caf - | " + fdkaac + " " + acodec_profile_choices[acodec_profile.get()] + \
                       fdkaac_title_input + fdkaac_custom_cmd_input + \
                       afterburnervar.get() + crccheck.get() + moovbox.get() \
                       + sbrdelay.get() + headerperiod.get() + \
                       acodec_lowdelay_choices[acodec_lowdelay.get()] + \
                       acodec_sbr_ratio_choices[acodec_sbr_ratio.get()] + \
                       acodec_transport_format_choices[acodec_transport_format.get()] + \
                       acodec_bitrate_choices[acodec_bitrate.get()] + "- -o " + VideoOutputQuoted + '"'
        if shell_options.get() == "Default":
            subprocess.Popen('cmd /c ' + finalcommand)
        elif shell_options.get() == "Debug":
            subprocess.Popen('cmd /k ' + finalcommand)
    # ------------------------------------------------------------------------------------------------------------- FDK
    # QAAC Start Job --------------------------------------------------------------------------------------------------
    elif encoder.get() == "QAAC":
        if q_acodec_profile.get() == "True VBR":
            finalcommand = '"' + ffmpeg + " -analyzeduration 100M -probesize 50M -i " \
                           + VideoInputQuoted + acodec_stream_choices[acodec_stream.get()] \
                           + acodec_channel_choices[acodec_channel.get()] \
                           + acodec_samplerate_choices[acodec_samplerate.get()] \
                           + "-f wav - | " + qaac + " " + q_acodec_profile_choices[q_acodec_profile.get()] \
                           + q_acodec_quality_amnt.get() + " " + qaac_high_efficiency.get() \
                           + qaac_normalize.get() + qaac_nodither.get() + "--gain " \
                           + q_acodec_gain.get() + " " + q_acodec_quality_choices[q_acodec_quality.get()] \
                           + qaac_normalize.get() + qaac_nodelay.get() \
                           + q_gapless_mode_choices[q_gapless_mode.get()] + qaac_nooptimize.get() \
                           + qaac_threading.get() + qaac_limiter.get() + qaac_title_input + qaac_custom_cmd_input \
                           + "- -o " + VideoOutputQuoted + '"'
        else:
            finalcommand = '"' + ffmpeg + " -analyzeduration 100M -probesize 50M -i " + VideoInputQuoted \
                           + acodec_stream_choices[acodec_stream.get()] + \
                           acodec_channel_choices[acodec_channel.get()] + \
                           acodec_samplerate_choices[acodec_samplerate.get()] \
                           + "-f wav - | " + qaac + " " + q_acodec_profile_choices[q_acodec_profile.get()] + \
                           q_acodec_bitrate.get() + " " + qaac_high_efficiency.get() + qaac_normalize.get() \
                           + qaac_nodither.get() + "--gain " + q_acodec_gain.get() + " " \
                           + q_acodec_quality_choices[q_acodec_quality.get()] + qaac_normalize.get() \
                           + qaac_nodelay.get() \
                           + q_gapless_mode_choices[q_gapless_mode.get()] + qaac_nooptimize.get() \
                           + qaac_threading.get() + qaac_limiter.get() + qaac_title_input \
                           + qaac_custom_cmd_input + "- -o " + VideoOutputQuoted + '"'
        if shell_options.get() == "Default":
            subprocess.Popen('cmd /c ' + finalcommand)
        elif shell_options.get() == "Debug":
            subprocess.Popen('cmd /k ' + finalcommand)
    # ------------------------------------------------------------------------------------------------------------ QAAC

# Open InputFile with portable MediaInfo ------------------------------
def mediainfogui():
    VideoInputQuoted = '"' + VideoInput + '"'
    MediaInfoQuoted = '"' + mediainfo + '"'
    commands = MediaInfoQuoted + " " + VideoInputQuoted
    subprocess.Popen(commands)
# ------------------------------------------------------------ MediaInfo


# Buttons Main Gui ----------------------------------------------------------------------------------------------------
encoder_menu.bind("<Enter>", encoder_menu_hover)
encoder_menu.bind("<Leave>", encoder_menu_hover_leave)

show_streams_button = Button(root, text="MediaInfo", command=mediainfogui, state=DISABLED, foreground="white",
                             background="#23272A", borderwidth="3")
show_streams_button.grid(row=1, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)
show_streams_button.bind("<Enter>", show_streams_button_hover)
show_streams_button.bind("<Leave>", show_streams_button_hover_leave)

audiosettings_button = Button(root, text="Audio Settings", command=openaudiowindow, foreground="white",
                              background="#23272A", state=DISABLED, borderwidth="3")
audiosettings_button.grid(row=1, column=3, columnspan=2, padx=5, pady=5, sticky=N + S + W + E)
audiosettings_button.bind("<Enter>", audiosettings_button_hover)
audiosettings_button.bind("<Leave>", audiosettings_button_hover_leave)

def input_button_commands():
    encoder.set('Set Codec')
    audiosettings_button.configure(state=DISABLED)
    output_entry.configure(state=NORMAL)
    output_entry.delete(0, END)
    output_entry.configure(state=DISABLED)
    input_entry.configure(state=NORMAL)
    input_entry.delete(0, END)
    input_entry.configure(state=DISABLED)
    show_streams_button.configure(state=DISABLED)
    encoder_menu.configure(state=DISABLED)
    output_button.configure(state=DISABLED)
    command_line_button.configure(state=DISABLED)
    file_input()

def drop_input(event):
    input_dnd.set(event.data)

def update_file_input(*args):
    global VideoInput
    global track_count
    global autofilesave_dir_path
    global VideoInputQuoted
    input_entry.configure(state=NORMAL)
    input_entry.delete(0, END)
    VideoInput = str(input_dnd.get()).replace("{", "").replace("}", "")
    file_extension = pathlib.Path(VideoInput).suffix
    if file_extension == '.wav' or file_extension == '.mt2s' or file_extension == '.ac3' or \
            file_extension == '.mka' or \
            file_extension == '.wav' or file_extension == '.mp3' or file_extension == '.aac' or \
            file_extension == '.ogg' or file_extension == '.ogv' or file_extension == '.m4v' or \
            file_extension == '.mpeg' or file_extension == '.avi' or file_extension == '.vob' or \
            file_extension == '.webm' or file_extension == '.mp4' or file_extension == '.mkv' or \
            file_extension == '.dts' or file_extension == '.m4a' or file_extension == '.mov':
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
        output_button.configure(state=DISABLED)
        start_audio_button.configure(state=DISABLED)
        encoder_menu.configure(state=NORMAL)
        show_streams_button.configure(state=NORMAL)
    else:
        messagebox.showinfo(title="Wrong File Type", message="Try Again With a Supported File Type!\n\nIf this is a "
                                                             "file that should be supported, please let me know.")

input_dnd = StringVar()
input_dnd.trace('w', update_file_input)
input_button = tk.Button(root, text="Open File", command=input_button_commands, foreground="white",
                         background="#23272A", borderwidth="3")
input_button.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)
input_button.drop_target_register(DND_FILES)
input_button.dnd_bind('<<Drop>>', drop_input)
input_button.bind("<Enter>", input_button_hover)
input_button.bind("<Leave>", input_button_hover_leave)

input_entry = Entry(root, width=35, borderwidth=4, background="#CACACA")
input_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=S + E + W)
input_entry.drop_target_register(DND_FILES)
input_entry.dnd_bind('<<Drop>>', drop_input)

output_button = Button(root, text="Save File", command=file_save, state=DISABLED, foreground="white",
                       background="#23272A", borderwidth="3")
output_button.grid(row=2, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)
output_entry = Entry(root, width=35, borderwidth=4, background="#CACACA")
output_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky=S + E + W)
output_button.bind("<Enter>", output_button_hover)
output_button.bind("<Leave>", output_button_hover_leave)

# Print Final Command Line
command_line_button = Button(root, text="Show\nCommand", command=print_command_line, state=DISABLED, foreground="white",
                             background="#23272A", borderwidth="3")
command_line_button.grid(row=3, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)
command_line_button.bind("<Enter>", command_line_button_hover)
command_line_button.bind("<Leave>", command_line_button_hover_leave)

# Start Audio Job
start_audio_button = Button(root, text="Start Audio Job", command=startaudiojob, state=DISABLED, foreground="white",
                            background="#23272A", borderwidth="3")
start_audio_button.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky=N + S + E + W)
start_audio_button.bind("<Enter>", start_audio_button_hover)
start_audio_button.bind("<Leave>", start_audio_button_hover_leave)

# End Loop -----------------------------------------------------------------------
root.mainloop()
