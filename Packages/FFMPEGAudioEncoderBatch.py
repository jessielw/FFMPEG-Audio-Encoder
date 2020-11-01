from tkinter import *
from tkinter import filedialog, StringVar, messagebox
import subprocess
import pathlib
import tkinter.scrolledtext as scrolledtextwidget
from TkinterDnD2 import *
import shutil
import threading

# Bundled Apps Quoted -------------------------------
if shutil.which('ffmpeg') != None:
    ffmpeg = str(pathlib.Path(shutil.which('ffmpeg')))
elif shutil.which('ffmpeg') == None:
    ffmpeg = str(pathlib.Path("Apps/FFMPEG/ffmpeg.exe"))
mediainfo = '"Apps/MediaInfo/MediaInfo.exe"'
mediainfocli = '"Apps/MediaInfoCLI/MediaInfo.exe"'
fdkaac = '"Apps/fdkaac/fdkaac.exe"'
qaac = '"Apps/qaac/qaac64.exe"'
mpv_player = '"Apps/mpv/mpv.exe"'
# -------------------------------------- Bundled Apps

# Batch Processing Window ---------------------------------------------------------------------------------------------
def batch_exit_function():
    global example_cmd_output, ac3_batch_job, aac_batch_job, dts_batch_job, opus_batch_job, \
        mp3_batch_job, eac3_batch_job, fdkaac_batch_job, qaac_batch_job, \
        flac_batch_job, alac_batch_job, batch_processing_window
    confirm_exit = messagebox.askyesno(title='Prompt', message="Are you sure you want to exit the program?",
                                       parent=batch_processing_window)
    if confirm_exit == False:
        pass
    elif confirm_exit == True:
        if ac3_batch_job.get() == '' and aac_batch_job.get() == '' and dts_batch_job.get() \
                == '' and opus_batch_job.get() == '' and mp3_batch_job.get() == '' and eac3_batch_job.get() \
                == '' and fdkaac_batch_job.get() == '' and qaac_batch_job.get() == '' and flac_batch_job.get() \
                == '' and alac_batch_job.get() == '':
            batch_processing_window.destroy()

            ac3_batch_job.set('')
            aac_batch_job.set('')
            dts_batch_job.set('')
            opus_batch_job.set('')
            mp3_batch_job.set('')
            eac3_batch_job.set('')
            fdkaac_batch_job.set('')
            qaac_batch_job.set('')
            flac_batch_job.set('')
            alac_batch_job.set('')

        elif ac3_batch_job.get() != '' or aac_batch_job.get() != '' or dts_batch_job.get() != '' \
                or opus_batch_job.get() != '' or mp3_batch_job.get() != '' or eac3_batch_job.get() != '' \
                or fdkaac_batch_job.get() != '' or qaac_batch_job.get() != '' or flac_batch_job.get() != '' \
                or alac_batch_job.get() != '':
            messagebox.showinfo(title='Error', message='Wait for all jobs to finish',
                                          parent=batch_processing_window)

def batch_processing():
    global batch_processing_window, batch_widow
    batch_processing_window = Toplevel()
    batch_processing_window.title('Batch Processing Window')
    batch_processing_window.configure(background="#434547")
    window_height = 260
    window_width = 600
    screen_width = batch_processing_window.winfo_screenwidth()
    screen_height = batch_processing_window.winfo_screenheight()
    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))
    batch_processing_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    batch_processing_window.protocol('WM_DELETE_WINDOW', batch_exit_function)

    batch_processing_window.grid_columnconfigure(0, weight=1)
    batch_processing_window.grid_columnconfigure(1, weight=1)
    batch_processing_window.grid_columnconfigure(2, weight=1)
    batch_processing_window.grid_columnconfigure(3, weight=1)
    batch_processing_window.grid_rowconfigure(0, weight=1)
    batch_processing_window.grid_rowconfigure(1, weight=1)
    batch_processing_window.grid_rowconfigure(2, weight=1)
    batch_processing_window.grid_rowconfigure(3, weight=1)

    # Menu Items and Sub-Bars -----------------------------------------------------------------------------------------
    my_menu_bar = Menu(batch_processing_window, tearoff=0)
    batch_processing_window.config(menu=my_menu_bar)

    file_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
    my_menu_bar.add_cascade(label='File', menu=file_menu)
    file_menu.add_command(label='Exit', command=batch_processing_window.destroy)

    options_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
    my_menu_bar.add_cascade(label='Options', menu=options_menu)

    options_submenu = Menu(batch_processing_window, tearoff=0, activebackground='dim grey')
    options_menu.add_cascade(label='Shell Options', menu=options_submenu)
    shell_options = StringVar()
    shell_options.set('Default')
    options_submenu.add_radiobutton(label='Shell Closes Automatically', variable=shell_options, value="Default")
    options_submenu.add_radiobutton(label='Shell Stays Open (Debug)', variable=shell_options, value="Debug")

    # ----------------------------------------------------------------------------------------- Menu Items and Sub-Bars

    def open_batch_dir_hover(e):
        open_batch_dir["bg"] = "grey"

    def open_batch_dir_hover_leave(e):
        open_batch_dir["bg"] = "#23272A"

    def save_batch_dir_hover(e):
        save_batch_dir["bg"] = "grey"

    def save_batch_dir_hover_leave(e):
        save_batch_dir["bg"] = "#23272A"

    def encoder_menu_hover(e):
        encoder_menu["bg"] = "grey"
        encoder_menu["activebackground"] = "grey"

    def encoder_menu_hover_leave(e):
        encoder_menu["bg"] = "#23272A"

    def extension_menu_hover(e):
        extension_menu["bg"] = "grey"
        extension_menu["activebackground"] = "grey"

    def extension_menu_hover_leave(e):
        extension_menu["bg"] = "#23272A"

    # Encoder Codec Drop Down -----------------------------------------------------------------------------------------
    def encoder_changed_batch(*args):
        if encoder.get() == "Set Codec":
            audiosettings_button_batch.configure(state=DISABLED)
            save_batch_dir.config(state=DISABLED)
            batch_input_entry.configure(state=NORMAL)
            batch_input_entry.delete(0, END)
            batch_input_entry.configure(state=DISABLED)
            batch_output_entry.configure(state=NORMAL)
            batch_output_entry.delete(0, END)
            batch_output_entry.configure(state=DISABLED)
            command_line_button_batch.config(state=DISABLED)
            start_audio_button_batch.config(state=DISABLED)
        else:
            audiosettings_button_batch.configure(state=NORMAL)
            command_line_button_batch.config(state=DISABLED)
            start_audio_button_batch.config(state=DISABLED)

    global ac3_batch_job, aac_batch_job, dts_batch_job, opus_batch_job, mp3_batch_job, \
        eac3_batch_job, fdkaac_batch_job, qaac_batch_job, flac_batch_job, alac_batch_job
    ac3_batch_job = StringVar()
    aac_batch_job = StringVar()
    dts_batch_job = StringVar()
    opus_batch_job = StringVar()
    mp3_batch_job = StringVar()
    eac3_batch_job = StringVar()
    fdkaac_batch_job = StringVar()
    qaac_batch_job = StringVar()
    flac_batch_job = StringVar()
    alac_batch_job = StringVar()

    ac3_batch_job.set('')
    aac_batch_job.set('')
    dts_batch_job.set('')
    opus_batch_job.set('')
    mp3_batch_job.set('')
    eac3_batch_job.set('')
    fdkaac_batch_job.set('')
    qaac_batch_job.set('')
    flac_batch_job.set('')
    alac_batch_job.set('')

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
        "ALAC": '-c:a alac ',}
    encoder = StringVar()
    encoder.set("Set Codec")
    encoder.trace('w', encoder_changed_batch)
    encoder_menu = OptionMenu(batch_processing_window, encoder, *encoder_dropdownmenu_choices.keys())
    encoder_menu.grid(row=1, column=2, columnspan=1, padx=(0,0), pady=5, sticky=N + S + E)
    encoder_menu.grid(row=1, column=2, columnspan=1, padx=(0,0), pady=5, sticky=N + S + E)
    encoder_menu.config( background="#23272A", foreground="white", highlightthickness=1, width=15, state=DISABLED)
    encoder_menu["menu"].configure(activebackground="dim grey")
    codec_batch_label = Label(batch_processing_window, text="<- Batch Extension\n    Set Codec ->",
                              background="#434547", foreground="White")
    codec_batch_label.grid(row=1, column=1, columnspan=1, padx=5, pady=5, sticky=N + S + W + E)
    encoder_menu.bind("<Enter>", encoder_menu_hover)
    encoder_menu.bind("<Leave>", encoder_menu_hover_leave)

    # ---------------------------------------------------------------------------------------------------- Encoder Menu

    # Encoder Codec Drop Down -----------------------------------------------------------------------------------------
    extension_dropdownmenu_choices = {
        "Common Extensions": '("*.mov", "*.wav", "*.mt2s", "*.ac3", "*.mka", "*.wav", "*.mp3", "*.aac", "*.ogg", '
                             '"*.ogv", "*.m4v", "*.mpeg", "*.avi", "*.vob", "*.webm", "*.mp4", "*.mkv", "*.dts", '
                             '"*.flac", "*.alac", "*.mpg", "*.m4a", "*.eac3", "*.opus", "*.aax")',
        "MKV": '("*.mkv")',
        "MP4": '("*.mp4")',
        "M4V": '("*.m4v")',
        "AVI": '("*.avi")',
        "FLAC/ALAC": '("*.flac", "*.alac")',
        "WAV": '("*.wav")',
        "AC3/EAC3": '("*.ac3", "*.eac3")',
        "OPUS/OGG": '("*.opus", "*.ogg")',
        "AAX": '("*.aax")',
        "All Files": '("*.*")'}
    extension = StringVar()
    extension.set("Common Extensions")
    extension_menu = OptionMenu(batch_processing_window, extension, *extension_dropdownmenu_choices.keys())
    extension_menu.grid(row=1, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + W + E)
    extension_menu.config( background="#23272A", foreground="white", highlightthickness=1, width=15)
    extension_menu["menu"].configure(activebackground="dim grey")
    extension_menu.bind("<Enter>", extension_menu_hover)
    extension_menu.bind("<Leave>", extension_menu_hover_leave)


    # ---------------------------------------------------------------------------------------------------- Encoder Menu

    # Audio Codec Window ----------------------------------------------------------------------------------------------
    def openaudiowindow2():
        global acodec_bitrate, acodec_channel, acodec_channel_choices, acodec_bitrate_choices, acodec_stream, \
            acodec_stream_choices, acodec_gain, acodec_gain_choices, dts_settings, dts_settings_choices, \
            acodec_vbr_choices, acodec_vbr, acodec_samplerate, acodec_samplerate_choices, acodec_application, \
            acodec_application_choices, acodec_profile, acodec_profile_choices

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

        acodec_stream_batch_choices = {'Track 1': '-map 0:a:0 ',
                                       'Track 2': '-map 0:a:1 ',
                                       'Track 3': '-map 0:a:2 ',
                                       'Track 4': '-map 0:a:3 ',
                                       'Track 5': '-map 0:a:4 ',
                                       'Track 6': '-map 0:a:5 ',
                                       'Track 7': '-map 0:a:6 ',
                                       'Track 8': '-map 0:a:7 ',
                                       'Track 9': '-map 0:a:8 ',
                                       'Track 10': '-map 0:a:9 ',
                                       'Track 11': '-map 0:a:10 ',
                                       'Track 12': '-map 0:a:11 ',
                                       'Track 13': '-map 0:a:12 ',
                                       'Track 14': '-map 0:a:13 ',
                                       'Track 15': '-map 0:a:14 '}

        # Checks channel for dolby pro logic II checkbox --------------------------------------------------------------
        def dolby_pro_logic_ii_enable_disable(*args):
            if acodec_channel.get() == '2 (Stereo)':
                dolby_pro_logic_ii_checkbox.config(state=NORMAL)
            else:
                dolby_pro_logic_ii.set("")
                dolby_pro_logic_ii_checkbox.config(state=DISABLED)

        # ----------------------------------------------------------------------------------------- dplII channel check

        # Combines -af filter settings --------------------------------------------------------------------------------
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
                ffmpeg_gain_cmd = '"volume=' + ffmpeg_gain.get() + 'dB"'
                if ffmpeg_gain.get() == '0' and acodec_atempo_choices[acodec_atempo.get()] == '':
                    audio_filter_setting = ''
                elif ffmpeg_gain.get() != '0' and acodec_atempo_choices[acodec_atempo.get()] == '':
                    audio_filter_setting = '-af ' + ffmpeg_gain_cmd + ' '
                elif ffmpeg_gain.get() == '0' and acodec_atempo_choices[acodec_atempo.get()] != '':
                    audio_filter_setting = '-af ' + acodec_atempo_choices[acodec_atempo.get()] + ' '
                elif ffmpeg_gain.get() != '0' and acodec_atempo_choices[acodec_atempo.get()] != '':
                    audio_filter_setting = '-af ' + ffmpeg_gain_cmd + ',' + acodec_atempo_choices[
                        acodec_atempo.get()] + ' '
            else:
                ffmpeg_gain_cmd = '"volume=' + ffmpeg_gain.get() + 'dB"'
                if dolby_pro_logic_ii.get() == '' and ffmpeg_gain.get() == '0' and \
                        acodec_atempo_choices[acodec_atempo.get()] == '':
                    audio_filter_setting = ''
                elif dolby_pro_logic_ii.get() == '"aresample=matrix_encoding=dplii"' and \
                        ffmpeg_gain.get() == '0' and acodec_atempo_choices[acodec_atempo.get()] == '':
                    audio_filter_setting = '-af ' + dolby_pro_logic_ii.get() + ' '

                elif dolby_pro_logic_ii.get() == '"aresample=matrix_encoding=dplii"' \
                        and ffmpeg_gain.get() != '0' and acodec_atempo_choices[acodec_atempo.get()] == '':
                    audio_filter_setting = '-af ' + dolby_pro_logic_ii.get() + ',' + \
                                           ffmpeg_gain_cmd + ' '
                elif dolby_pro_logic_ii.get() == '' and ffmpeg_gain.get() != '0' and \
                        acodec_atempo_choices[acodec_atempo.get()] == '':
                    audio_filter_setting = '-af ' + ffmpeg_gain_cmd + ' '
                elif dolby_pro_logic_ii.get() == '"aresample=matrix_encoding=dplii"' and \
                        ffmpeg_gain.get() == '0' and acodec_atempo_choices[acodec_atempo.get()] != '':
                    audio_filter_setting = '-af ' + dolby_pro_logic_ii.get() + ',' + \
                                           acodec_atempo_choices[acodec_atempo.get()] + ' '
                elif dolby_pro_logic_ii.get() == '"aresample=matrix_encoding=dplii"' \
                        and ffmpeg_gain.get() != '0' and acodec_atempo_choices[acodec_atempo.get()] != '':
                    audio_filter_setting = '-af ' + dolby_pro_logic_ii.get() + ',' + \
                                           ffmpeg_gain_cmd + ',' + acodec_atempo_choices[acodec_atempo.get()] + ' '
                elif dolby_pro_logic_ii.get() == '' and ffmpeg_gain.get() != '0' and \
                        acodec_atempo_choices[acodec_atempo.get()] != '':
                    audio_filter_setting = '-af ' + ffmpeg_gain_cmd + ',' + acodec_atempo_choices[
                        acodec_atempo.get()] + ' '
                elif dolby_pro_logic_ii.get() == '' and \
                        ffmpeg_gain.get() == '0' and acodec_atempo_choices[acodec_atempo.get()] != '':
                    audio_filter_setting = '-af ' + acodec_atempo_choices[acodec_atempo.get()] + ' '

        # ------------------------------------------------------------------------------------------------ combines -af

        def gotosavefile():
            audio_window.destroy()
            save_batch_dir.config(state=NORMAL)
            command_line_button_batch.config(state=NORMAL)
            start_audio_button_batch.config(state=NORMAL)
            try:
                cmd_line_window.withdraw()
            except:
                pass

        # AC3 Window --------------------------------------------------------------------------------------------
        global audio_window
        if encoder.get() == "AC3":
            audio_window = Toplevel()
            audio_window.title('AC3 Settings')
            audio_window.configure(background="#434547")
            window_height = 400
            window_width = 600
            screen_width = audio_window.winfo_screenwidth()
            screen_height = audio_window.winfo_screenheight()
            x_cordinate = int((screen_width / 2) - (window_width / 2))
            y_cordinate = int((screen_height / 2) - (window_height / 2))
            audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

            audio_window.grid_columnconfigure(0, weight=1)
            audio_window.grid_columnconfigure(1, weight=1)
            audio_window.grid_columnconfigure(2, weight=1)
            audio_window.grid_rowconfigure(0, weight=1)
            audio_window.grid_rowconfigure(1, weight=1)
            audio_window.grid_rowconfigure(2, weight=1)
            audio_window.grid_rowconfigure(3, weight=1)
            audio_window.grid_rowconfigure(8, weight=1)

            # Views Command -----------------------------------------------------------------------------------
            def view_command():
                global cmd_line_window
                global cmd_label
                audio_filter_function()
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
                    cmd_label = Label(cmd_line_window, text=example_cmd_output, foreground="white",
                                      background="#434547")
                    cmd_label.config(font=("Helvetica", 16))
                    cmd_label.pack()

                    def hide_instead():
                        cmd_line_window.withdraw()

                    cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

            # ----------------------------------------------------------------------------- Views Command

            # Buttons ---------------------------------------------------------------------------------------
            apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A",
                                  command=gotosavefile)
            apply_button.grid(row=8, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            apply_button.bind("<Enter>", apply_button_hover)
            apply_button.bind("<Leave>", apply_button_hover_leave)

            show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A",
                              command=view_command)
            show_cmd.grid(row=8, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            show_cmd.bind("<Enter>", show_cmd_hover)
            show_cmd.bind("<Leave>", show_cmd_hover_leave)
            # ----------------------------------------------------------------------------------- Buttons

            # Audio Bitrate Selection ---------------------------------------------------------------
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
            acodec_bitrate_menu_label = Label(audio_window, text="Bitrate :", background="#434547",
                                              foreground="white")
            acodec_bitrate_menu_label.grid(row=0, column=2, columnspan=1, padx=10, pady=3, sticky=W + E)
            acodec_bitrate_menu = OptionMenu(audio_window, acodec_bitrate, *acodec_bitrate_choices.keys())
            acodec_bitrate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            acodec_bitrate_menu.grid(row=1, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            acodec_bitrate_menu["menu"].configure(activebackground="dim grey")
            acodec_bitrate_menu.bind("<Enter>", acodec_bitrate_menu_hover)
            acodec_bitrate_menu.bind("<Leave>", acodec_bitrate_menu_hover_leave)
            # ------------------------------------------------------------------------------------- Audio Bitrate

            # Audio Stream Selection ----------------------------------------------------------------
            acodec_stream = StringVar(audio_window)
            acodec_stream_choices = acodec_stream_batch_choices
            acodec_stream.set('Track 1')
            acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
            acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
            acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
            acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            acodec_stream_menu["menu"].configure(activebackground="dim grey")
            acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
            acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)
            # ---------------------------------------------------------------------------------------------------

            # Audio Channel Selection ------------------------------------------------------------------------
            acodec_channel = StringVar(audio_window)
            acodec_channel_choices = {'Original': "",
                                      '1 (Mono)': "-ac 1 ",
                                      '2 (Stereo)': "-ac 2 ",
                                      '2.1 (Stereo)': "-ac 3 ",
                                      '4.0 (Quad)': "-ac 4 ",
                                      '5.0 (Surround)': "-ac 5 ",
                                      '5.1 (Surround)': "-ac 6 "}
            acodec_channel.set('Original')  # set the default option
            achannel_menu_label = Label(audio_window, text="Channels :", background="#434547",
                                        foreground="white")
            achannel_menu_label.grid(row=0, column=1, columnspan=1, padx=10, pady=3, sticky=W + E)
            achannel_menu = OptionMenu(audio_window, acodec_channel, *acodec_channel_choices.keys())
            achannel_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            achannel_menu.grid(row=1, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            achannel_menu["menu"].configure(activebackground="dim grey")
            achannel_menu.bind("<Enter>", achannel_menu_hover)
            achannel_menu.bind("<Leave>", achannel_menu_hover_leave)
            acodec_channel.trace('w', dolby_pro_logic_ii_enable_disable)
            # -------------------------------------------------------------------------------------- Audio Channel

            # Dolby Pro Logic II ----------------------------------------------------------------------------------
            dolby_pro_logic_ii = StringVar()
            dolby_pro_logic_ii_checkbox = Checkbutton(audio_window, text=' Dolby Pro\nLogic II',
                                                      variable=dolby_pro_logic_ii, state=DISABLED,
                                                      onvalue='"aresample=matrix_encoding=dplii"', offvalue="")
            dolby_pro_logic_ii_checkbox.grid(row=4, column=2, columnspan=1, rowspan=1, padx=10, pady=(20, 5),
                                             sticky=N + S + E + W)
            dolby_pro_logic_ii_checkbox.configure(background="#434547", foreground="white",
                                                  activebackground="#434547",
                                                  activeforeground="white", selectcolor="#434547",
                                                  font=("Helvetica", 11))
            dolby_pro_logic_ii.set("")
            # ---------------------------------------------------------------------------------------- DPL II

            # Audio Gain Selection --------------------------------------------------------------------------
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
            ffmpeg_gain.set(0)
            # ---------------------------------------------------------------------------------------------- Gain

            # Audio Sample Rate Selection ----------------------------------------------------------------------
            acodec_samplerate = StringVar(audio_window)
            acodec_samplerate_choices = {'Original': "",
                                         '32000 Hz': "-ar 32000 ",
                                         '44100 Hz': "-ar 44100 ",
                                         '48000 Hz': "-ar 48000 "}
            acodec_samplerate.set('Original')  # set the default option
            acodec_samplerate_label = Label(audio_window, text="Sample Rate :", background="#434547",
                                            foreground="white")
            acodec_samplerate_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_samplerate_menu = OptionMenu(audio_window, acodec_samplerate,
                                                *acodec_samplerate_choices.keys())
            acodec_samplerate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            acodec_samplerate_menu.grid(row=3, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_samplerate_menu["menu"].configure(activebackground="dim grey")
            acodec_samplerate_menu.bind("<Enter>", acodec_samplerate_menu_hover)
            acodec_samplerate_menu.bind("<Leave>", acodec_samplerate_menu_hover_leave)

            # --------------------------------------------------------------------------------------- Sample Rate

            # Entry Box for Custom Command Line --------------------------------------------------------------
            def ac3_cmd(*args):
                global ac3_custom_cmd_input
                if ac3_custom_cmd.get() == (""):
                    ac3_custom_cmd_input = ("")
                else:
                    cstmcmd = ac3_custom_cmd.get()
                    ac3_custom_cmd_input = cstmcmd + " "

            ac3_custom_cmd = StringVar()
            ac3_cmd_entrybox_label = Label(audio_window, text="Custom Command Line :", anchor=W,
                                           background="#434547",
                                           foreground="white")
            ac3_cmd_entrybox_label.grid(row=5, column=0, columnspan=2, padx=10, pady=(15, 0),
                                        sticky=N + S + W + E)
            ac3_cmd_entrybox = Entry(audio_window, textvariable=ac3_custom_cmd, borderwidth=4,
                                     background="#CACACA")
            ac3_cmd_entrybox.grid(row=6, column=0, columnspan=3, padx=10, pady=(0, 15), sticky=W + E)
            ac3_custom_cmd.trace('w', ac3_cmd)
            ac3_custom_cmd.set("")
            # ---------------------------------------------------------------------------- Custom Command Line

            # Audio Atempo Selection --------------------------------------------------------------------------
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
            acodec_atempo.set('Original')
            acodec_atempo_menu["menu"].configure(activebackground="dim grey")
            acodec_atempo_menu.bind("<Enter>", acodec_atempo_menu_hover)
            acodec_atempo_menu.bind("<Leave>", acodec_atempo_menu_hover_leave)
            # ---------------------------------------------------------------------------------------- Audio Atempo
        # ---------------------------------------------------------------------------------------------------- AC3

            # AAC Window ------------------------------------------------------------------------------------------
        elif encoder.get() == "AAC":
            audio_window = Toplevel()
            audio_window.title('AAC Settings')
            audio_window.configure(background="#434547")
            window_height = 420
            window_width = 620
            screen_width = audio_window.winfo_screenwidth()
            screen_height = audio_window.winfo_screenheight()
            x_cordinate = int((screen_width / 2) - (window_width / 2))
            y_cordinate = int((screen_height / 2) - (window_height / 2))
            audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

            audio_window.grid_columnconfigure(0, weight=1)
            audio_window.grid_columnconfigure(1, weight=1)
            audio_window.grid_columnconfigure(2, weight=1)
            audio_window.grid_rowconfigure(0, weight=1)
            audio_window.grid_rowconfigure(1, weight=1)
            audio_window.grid_rowconfigure(2, weight=1)
            audio_window.grid_rowconfigure(3, weight=1)
            audio_window.grid_rowconfigure(4, weight=1)
            audio_window.grid_rowconfigure(5, weight=1)
            audio_window.grid_rowconfigure(10, weight=1)

            def view_command():  # Views Command --------------------------------------------------------------------
                global cmd_label
                global cmd_line_window
                audio_filter_function()
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
                    cmd_label = Label(cmd_line_window, text=example_cmd_output, foreground="white",
                                      background="#434547")
                    cmd_label.config(font=("Helvetica", 16))
                    cmd_label.winfo_exists()
                    cmd_label.pack()

                    def hide_instead():
                        cmd_line_window.withdraw()

                    cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

            # ------------------------------------------------------------------------------------------ Views Command

            # Buttons -------------------------------------------------------------------------------------------------
            apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A",
                                  command=gotosavefile)
            apply_button.grid(row=10, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            apply_button.bind("<Enter>", apply_button_hover)
            apply_button.bind("<Leave>", apply_button_hover_leave)

            show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A",
                              command=view_command)
            show_cmd.grid(row=10, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            show_cmd.bind("<Enter>", show_cmd_hover)
            show_cmd.bind("<Leave>", show_cmd_hover_leave)

            # ----------------------------------------------------------------------------------------------- Buttons

            # Entry Box for Custom Command Line -----------------------------------------------------------------------
            def aac_cmd(*args):
                global aac_custom_cmd_input
                if aac_custom_cmd.get() == (""):
                    aac_custom_cmd_input = ("")
                else:
                    cstmcmd = aac_custom_cmd.get()
                    aac_custom_cmd_input = cstmcmd + " "

            aac_custom_cmd = StringVar()
            aac_cmd_entrybox_label = Label(audio_window, text="Custom Command Line :", anchor=W, background="#434547",
                                           foreground="white")
            aac_cmd_entrybox_label.grid(row=6, column=0, columnspan=2, padx=10, pady=(0, 0), sticky=N + S + W + E)
            aac_cmd_entrybox = Entry(audio_window, textvariable=aac_custom_cmd, borderwidth=4, background="#CACACA")
            aac_cmd_entrybox.grid(row=7, column=0, columnspan=3, padx=10, pady=(0, 0), sticky=W + E)
            aac_custom_cmd.trace('w', aac_cmd)
            aac_custom_cmd.set("")

            # ------------------------------------------------------------------------------------ Custom Command Line

            # Entry Box for Track Title ------------------------------------------------------------------------------
            def aac_title_check(*args):
                global aac_title_input
                if aac_title.get() == (""):
                    aac_title_input = ("")
                else:
                    title_cmd = aac_title.get()
                    aac_title_input = "-metadata:s:a:0 title=" + '"' + title_cmd + '"' + " "

            aac_title = StringVar()
            aac_title_entrybox_label = Label(audio_window, text="Track Name :", anchor=W, background="#434547",
                                             foreground="white")
            aac_title_entrybox_label.grid(row=8, column=0, columnspan=2, padx=10, pady=(5, 0), sticky=N + S + W + E)
            aac_title_entrybox = Entry(audio_window, textvariable=aac_title, borderwidth=4, background="#CACACA")
            aac_title_entrybox.grid(row=9, column=0, columnspan=3, padx=10, pady=(0, 10), sticky=W + E)
            aac_title.trace('w', aac_title_check)
            aac_title.set("")
            # ----------------------------------------------------------------------------------------- Track Title

            # Dolby Pro Logic II --------------------------------------------------------------------------------------
            dolby_pro_logic_ii = StringVar()
            dolby_pro_logic_ii_checkbox = Checkbutton(audio_window, text=' Dolby Pro\nLogic II',
                                                      variable=dolby_pro_logic_ii, state=DISABLED,
                                                      onvalue='"aresample=matrix_encoding=dplii"', offvalue="")
            dolby_pro_logic_ii_checkbox.grid(row=4, column=0, columnspan=1, rowspan=1, padx=10, pady=(15, 15),
                                             sticky=N + S + E + W)
            dolby_pro_logic_ii_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                                  activeforeground="white", selectcolor="#434547",
                                                  font=("Helvetica", 11))
            dolby_pro_logic_ii.set("")
            # ----------------------------------------------------------------------------------------------- DPL II

            # Audio Gain Selection -----------------------------------------------------------------------------------
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
            ffmpeg_gain.set(0)
            # -------------------------------------------------------------------------------------------------- Gain

            # Audio Bitrate Spinbox -----------------------------------------------------------------------------
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
            # ------------------------------------------------------------------------------ Audio Bitrate Spinbox

            # Vbr Toggle ---------------------------------------------------------------------------------------------
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
                                                         buttonbackground="black", width=15,
                                                         readonlybackground="#23272A")
                    aac_acodec_bitrate_spinbox.grid(row=3, column=1, columnspan=1, padx=10, pady=3,
                                                    sticky=N + S + E + W)
                    aac_bitrate_spinbox.set(192)
                elif aac_vbr_toggle.get() == "-q:a ":  # This enables VBR Spinbox -------------------------------------
                    global aac_quality_spinbox
                    aac_quality_spinbox = StringVar()
                    aac_acodec_quality_spinbox_label = Label(audio_window, text="VBR Quality :", background="#434547",
                                                             foreground="white")
                    aac_acodec_quality_spinbox_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3,
                                                          sticky=N + S + E + W)
                    aac_acodec_quality_spinbox = Spinbox(audio_window, from_=0.1, to=5, increment=0.1, justify=CENTER,
                                                         wrap=True, textvariable=aac_quality_spinbox)
                    aac_acodec_quality_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                                         buttonbackground="black", width=15,
                                                         readonlybackground="#23272A")
                    aac_acodec_quality_spinbox.grid(row=3, column=1, columnspan=1, padx=10, pady=3,
                                                    sticky=N + S + E + W)
                    aac_quality_spinbox.set(2)
                    # ------------------------------------------------------------------------------------- VBR Spinbox

            aac_vbr_toggle_checkbox = Checkbutton(audio_window, text=' Variable\n Bit-Rate', variable=aac_vbr_toggle,
                                                  onvalue="-q:a ", offvalue="-c:a ", command=aac_vbr_trace)
            aac_vbr_toggle_checkbox.grid(row=4, column=1, columnspan=1, rowspan=2, padx=10, pady=3,
                                         sticky=N + S + E + W)
            aac_vbr_toggle_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                              activeforeground="white", selectcolor="#434547", font=("Helvetica", 11))
            aac_vbr_toggle.trace('w', aac_vbr_trace)
            # --------------------------------------------------------------------------------------------- Vbr Toggle

            # Audio Channel Selection ---------------------------------------------------------------------------------
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
            # --------------------------------------------------------------------------------- Audio Channel Selection

            # Audio Stream Selection --------------------------------------------------------------------------------
            acodec_stream = StringVar(audio_window)
            acodec_stream_choices = acodec_stream_batch_choices
            acodec_stream.set('Track 1')
            acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
            acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
            acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
            acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            acodec_stream_menu["menu"].configure(activebackground="dim grey")
            acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
            acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)
            # --------------------------------------------------------------------------------- Audio Stream Selection

            # Audio Sample Rate Selection ------------------------------------------------------------------------
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
            acodec_samplerate_label = Label(audio_window, text="Sample Rate :", background="#434547",
                                            foreground="white")
            acodec_samplerate_label.grid(row=2, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_samplerate_menu = OptionMenu(audio_window, acodec_samplerate, *acodec_samplerate_choices.keys())
            acodec_samplerate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            acodec_samplerate_menu.grid(row=3, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_samplerate_menu["menu"].configure(activebackground="dim grey")
            acodec_samplerate_menu.bind("<Enter>", acodec_samplerate_menu_hover)
            acodec_samplerate_menu.bind("<Leave>", acodec_samplerate_menu_hover_leave)
            # ---------------------------------------------------------------------------- Audio Sample Rate Selection

            # Audio Atempo Selection --------------------------------------------------------------------------------
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
            acodec_atempo.set('Original')
            acodec_atempo_menu["menu"].configure(activebackground="dim grey")
            acodec_atempo_menu.bind("<Enter>", acodec_atempo_menu_hover)
            acodec_atempo_menu.bind("<Leave>", acodec_atempo_menu_hover_leave)
            # ---------------------------------------------------------------------------------------- Audio Atempto
        # ------------------------------------------------------------------------------------------------- AAC Window

        # DTS Window ----------------------------------------------------------------------------------------------
        elif encoder.get() == "DTS":
            audio_window = Toplevel()
            audio_window.title('DTS Settings')
            audio_window.configure(background="#434547")
            window_height = 400
            window_width = 500
            screen_width = audio_window.winfo_screenwidth()
            screen_height = audio_window.winfo_screenheight()
            x_cordinate = int((screen_width / 2) - (window_width / 2))
            y_cordinate = int((screen_height / 2) - (window_height / 2))
            audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

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
            audio_window.grid_rowconfigure(9, weight=1)

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
                    acodec_atempo_menu.config(state=NORMAL)
                    acodec_atempo.set('Original')
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
                    acodec_atempo.set('Original')
                    acodec_atempo_menu.config(state=DISABLED)

            # Views Command -------------------------------------------------------------------------------------------
            def view_command():
                global cmd_label
                global cmd_line_window
                audio_filter_function()
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
                    cmd_label = Label(cmd_line_window, text=example_cmd_output, foreground="white",
                                      background="#434547")
                    cmd_label.config(font=("Helvetica", 16))
                    cmd_label.winfo_exists()
                    cmd_label.pack()

                    def hide_instead():
                        cmd_line_window.withdraw()

                    cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

            # --------------------------------------------------------------------------------------- Views Command

            # Buttons ----------------------------------------------------------------------------------------------
            apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A",
                                  command=gotosavefile)
            apply_button.grid(row=9, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            apply_button.bind("<Enter>", apply_button_hover)
            apply_button.bind("<Leave>", apply_button_hover_leave)

            show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A",
                              command=view_command)
            show_cmd.grid(row=9, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            show_cmd.bind("<Enter>", show_cmd_hover)
            show_cmd.bind("<Leave>", show_cmd_hover_leave)

            # --------------------------------------------------------------------------------------- Buttons

            # Entry Box for Custom Command Line --------------------------------------------------------------------
            def dts_cmd(*args):
                global dts_custom_cmd_input
                if dts_custom_cmd.get() == (""):
                    dts_custom_cmd_input = ("")
                else:
                    cstmcmd = dts_custom_cmd.get()
                    dts_custom_cmd_input = cstmcmd + " "

            dts_custom_cmd = StringVar()
            dts_cmd_entrybox_label = Label(audio_window, text="Custom Command Line :", anchor=W, background="#434547",
                                           foreground="white")
            dts_cmd_entrybox_label.grid(row=7, column=0, columnspan=2, padx=10, pady=(15, 0), sticky=N + S + W + E)
            dts_cmd_entrybox = Entry(audio_window, textvariable=dts_custom_cmd, borderwidth=4, background="#CACACA")
            dts_cmd_entrybox.grid(row=8, column=0, columnspan=3, padx=10, pady=(0, 10), sticky=W + E)
            dts_custom_cmd.trace('w', dts_cmd)
            dts_custom_cmd.set("")

            # --------------------------------------------------------------------------------- Custom Command Line

            # Audio Bitrate Spinbox ---------------------------------------------------------------------------------
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
            dts_bitrate_spinbox.set("")
            # -------------------------------------------------------------------------------- Audio Bitrate Spinbox

            # Dolby Pro Logic II --------------------------------------------------------------------------------
            dolby_pro_logic_ii = StringVar()
            dolby_pro_logic_ii_checkbox = Checkbutton(audio_window, text=' Dolby Pro\nLogic II',
                                                      variable=dolby_pro_logic_ii, state=DISABLED,
                                                      onvalue='"aresample=matrix_encoding=dplii"', offvalue='')
            dolby_pro_logic_ii_checkbox.grid(row=6, column=0, columnspan=1, rowspan=1, padx=10, pady=(10, 3),
                                             sticky=N + S + E + W)
            dolby_pro_logic_ii_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                                  activeforeground="white", selectcolor="#434547",
                                                  font=("Helvetica", 11))
            dolby_pro_logic_ii.set("")
            # ----------------------------------------------------------------------------------------------- DPL II

            # Audio Gain Selection -------------------------------------------------------------------------------
            ffmpeg_gain = StringVar()
            ffmpeg_gain_label = Label(audio_window, text="Gain (dB) :", background="#434547",
                                      foreground="white")
            ffmpeg_gain_label.grid(row=2, column=0, columnspan=1, padx=10, pady=3,
                                   sticky=N + S + E + W)
            ffmpeg_gain_spinbox = Spinbox(audio_window, from_=-30, to=30, increment=1.0, justify=CENTER,
                                          wrap=True, textvariable=ffmpeg_gain, state=DISABLED)
            ffmpeg_gain_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                          buttonbackground="black", width=15, readonlybackground="#23272A",
                                          disabledbackground='grey')
            ffmpeg_gain_spinbox.grid(row=3, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            ffmpeg_gain.set(0)
            # ---------------------------------------------------------------------------------------------------- Gain

            # Audio Sample Rate Selection --------------------------------------------------------------------------
            acodec_samplerate = StringVar(audio_window)
            acodec_samplerate_choices = {'Original': "",
                                         '16000 Hz': "-ar 16000 ",
                                         '22050 Hz': "-ar 22050 ",
                                         '24000 Hz': "-ar 24000 ",
                                         '32000 Hz': "-ar 32000 ",
                                         '44100 Hz': "-ar 44100 ",
                                         '48000 Hz': "-ar 48000 "}
            acodec_samplerate.set('Original')  # set the default option
            acodec_samplerate_label = Label(audio_window, text="Sample Rate :", background="#434547",
                                            foreground="white")
            acodec_samplerate_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_samplerate_menu = OptionMenu(audio_window, acodec_samplerate, *acodec_samplerate_choices.keys())
            acodec_samplerate_menu.config(background="#23272A", foreground="white", highlightthickness=1,
                                          state=DISABLED)
            acodec_samplerate_menu.grid(row=3, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_samplerate_menu["menu"].configure(activebackground="dim grey")
            acodec_samplerate_menu.bind("<Enter>", acodec_samplerate_menu_hover)
            acodec_samplerate_menu.bind("<Leave>", acodec_samplerate_menu_hover_leave)
            # ---------------------------------------------------------------------------- Audio Sample Rate Selection

            # Audio Stream Selection -----------------------------------------------------------------------------
            acodec_stream = StringVar(audio_window)
            acodec_stream_choices = acodec_stream_batch_choices
            acodec_stream.set('Track 1')
            acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
            acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
            acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
            acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            acodec_stream_menu["menu"].configure(activebackground="dim grey")
            acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
            acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)
            # ---------------------------------------------------------------------------------------- Audio Stream

            # Audio Channel Selection ------------------------------------------------------------------------------
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
            # --------------------------------------------------------------------------- Audio Channel Selection

            # DTS Encoder(s) ---------------------------------------------------------------------------------
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
            # ----------------------------------------------------------------------------------------- DTS Encoders

            # Audio Atempo Selection --------------------------------------------------------------------------------
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
            acodec_atempo.set('Original')
            acodec_atempo_menu["menu"].configure(activebackground="dim grey")
            acodec_atempo_menu.bind("<Enter>", acodec_atempo_menu_hover)
            acodec_atempo_menu.bind("<Leave>", acodec_atempo_menu_hover_leave)
            # ------------------------------------------------------------------------------------------- Audio Atempo
        # --------------------------------------------------------------------------------------------------------- DTS

            # Opus Window -----------------------------------------------------------------------------------------------------
        elif encoder.get() == "Opus":
            audio_window = Toplevel()
            audio_window.title('Opus Settings')
            audio_window.configure(background="#434547")
            window_height = 580
            window_width = 650
            screen_width = audio_window.winfo_screenwidth()
            screen_height = audio_window.winfo_screenheight()
            x_cordinate = int((screen_width / 2) - (window_width / 2))
            y_cordinate = int((screen_height / 2) - (window_height / 2))
            audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

            advanced_label = Label(audio_window,
                                   text="- - - - - - - - - - - - - - - - - - - - Advanced Settings - - - - - "
                                        "- - - - - - - - - - - - - - -",
                                   background="#434547", foreground="white", relief=GROOVE)
            advanced_label.grid(row=7, column=0, columnspan=3, padx=10, pady=(5, 0), sticky=W + E)

            advanced_label_end = Label(audio_window,
                                       text="- - - - - - - - - - - - - - - - - - - - - - - - "
                                            "- - - - - - - - - - - - - - - - - - - - - - -",
                                       background="#434547", foreground="white", relief=GROOVE)
            advanced_label_end.grid(row=10, column=0, columnspan=3, padx=10, pady=(5, 0), sticky=W + E)

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
            audio_window.grid_rowconfigure(8, weight=1)
            audio_window.grid_rowconfigure(9, weight=1)
            audio_window.grid_rowconfigure(13, weight=1)

            # Views Command --------------------------------------------------------------------------------------
            def view_command():
                global cmd_label
                global cmd_line_window
                audio_filter_function()
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
                    cmd_label = Label(cmd_line_window, text=example_cmd_output, foreground="white",
                                      background="#434547")
                    cmd_label.config(font=("Helvetica", 16))
                    cmd_label.winfo_exists()
                    cmd_label.pack()

                    def hide_instead():
                        cmd_line_window.withdraw()

                    cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

            # ------------------------------------------------------------------------------------------ Views Command

            # Buttons ---------------------------------------------------------------------------------------------
            apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A",
                                  command=gotosavefile)
            apply_button.grid(row=13, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            apply_button.bind("<Enter>", apply_button_hover)
            apply_button.bind("<Leave>", apply_button_hover_leave)

            show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A",
                              command=view_command)
            show_cmd.grid(row=13, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            show_cmd.bind("<Enter>", show_cmd_hover)
            show_cmd.bind("<Leave>", show_cmd_hover_leave)
            # ----------------------------------------------------------------------------------------------- Buttons

            # Audio Bitrate Menu ---------------------------------------------------------------------------------
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
            # --------------------------------------------------------------------------------------- Audio Bitrate

            # Audio Sample Rate Selection -------------------------------------------------------------------------
            acodec_samplerate = StringVar(audio_window)
            acodec_samplerate_choices = {'Original': "",
                                         '8000 Hz': "-ar 8000 ",
                                         '12000 Hz': "-ar 12000 ",
                                         '16000 Hz': "-ar 16000 ",
                                         '24000 Hz': "-ar 24000 ",
                                         '48000 Hz': "-ar 48000 "}
            acodec_samplerate.set('Original')  # set the default option
            acodec_samplerate_label = Label(audio_window, text="Sample Rate :", background="#434547",
                                            foreground="white")
            acodec_samplerate_label.grid(row=2, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_samplerate_menu = OptionMenu(audio_window, acodec_samplerate, *acodec_samplerate_choices.keys())
            acodec_samplerate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            acodec_samplerate_menu.grid(row=3, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_samplerate_menu["menu"].configure(activebackground="dim grey")
            acodec_samplerate_menu.bind("<Enter>", acodec_samplerate_menu_hover)
            acodec_samplerate_menu.bind("<Leave>", acodec_samplerate_menu_hover_leave)

            # ------------------------------------------------------------------------ Audio Sample Rate Selection

            # Entry Box for Custom Command Line -------------------------------------------------------------------
            def opus_cmd(*args):
                global opus_custom_cmd_input
                if opus_custom_cmd.get() == (""):
                    opus_custom_cmd_input = ("")
                else:
                    cstmcmd = opus_custom_cmd.get()
                    opus_custom_cmd_input = cstmcmd + " "

            opus_custom_cmd = StringVar()
            opus_cmd_entrybox_label = Label(audio_window, text="Custom Command Line :", anchor=W, background="#434547",
                                            foreground="white")
            opus_cmd_entrybox_label.grid(row=11, column=0, columnspan=2, padx=10, pady=(10, 0), sticky=N + S + W + E)
            opus_cmd_entrybox = Entry(audio_window, textvariable=opus_custom_cmd, borderwidth=4, background="#CACACA")
            opus_cmd_entrybox.grid(row=12, column=0, columnspan=3, padx=10, pady=(0, 15), sticky=W + E)
            opus_custom_cmd.trace('w', opus_cmd)
            opus_custom_cmd.set("")

            # ---------------------------------------------------------------------------------- Custom Command Line

            # Audio VBR Toggle -------------------------------------------------------------------------------
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
            # ---------------------------------------------------------------------------------------- VBR Toggle

            # Audio Application Selection -------------------------------------------------------------------------
            acodec_application = StringVar(audio_window)
            acodec_application_choices = {'Audio': "",
                                          'VoIP': "-application 2048 ",
                                          'Low Delay': "-application 2051 "}
            acodec_application.set('Audio')  # set the default option
            acodec_application_menu_label = Label(audio_window, text="Application:\n*Default is 'Audio'*",
                                                  background="#434547", foreground="white")
            acodec_application_menu_label.grid(row=8, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
            acodec_application_menu = OptionMenu(audio_window, acodec_application, *acodec_application_choices.keys())
            acodec_application_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            acodec_application_menu.grid(row=9, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            acodec_application_menu["menu"].configure(activebackground="dim grey")
            acodec_application_menu.bind("<Enter>", acodec_application_menu_hover)
            acodec_application_menu.bind("<Leave>", acodec_application_menu_hover_leave)
            # -------------------------------------------------------------------------------------- Application

            # Audio Frame Duration Spinbox -----------------------------------------------------------------------
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
            frame_duration.set(20)
            # ------------------------------------------------------------------------------------ Frame Duration

            # Audio Packet Loss Spinbox ----------------------------------------------------------------------
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
            packet_loss.set(0)
            # ------------------------------------------------------------------------------------ Packet Loss

            # Audio Channel Selection -----------------------------------------------------------------------------
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
            # ---------------------------------------------------------------------------------- Channel Selection

            # Audio Stream Selection ----------------------------------------------------------------------------
            acodec_stream = StringVar(audio_window)
            acodec_stream_choices = acodec_stream_batch_choices
            acodec_stream.set('Track 1')
            acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
            acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
            acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
            acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            acodec_stream_menu["menu"].configure(activebackground="dim grey")
            acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
            acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)
            # ------------------------------------------------------------------------------ Audio Stream Selection

            # Dolby Pro Logic II ----------------------------------------------------------------------------------
            dolby_pro_logic_ii = StringVar()
            dolby_pro_logic_ii_checkbox = Checkbutton(audio_window, text=' Dolby Pro\nLogic II',
                                                      variable=dolby_pro_logic_ii,
                                                      onvalue='"aresample=matrix_encoding=dplii"', offvalue="")
            dolby_pro_logic_ii_checkbox.grid(row=4, column=0, columnspan=1, rowspan=2, padx=10, pady=(15, 5),
                                             sticky=N + S + E + W)
            dolby_pro_logic_ii_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                                  activeforeground="white", selectcolor="#434547",
                                                  font=("Helvetica", 11))
            dolby_pro_logic_ii.set("")
            # --------------------------------------------------------------------------------------------- DPL II

            # Audio Gain Selection ---------------------------------------------------------------------------------
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
            ffmpeg_gain.set(0)
            # --------------------------------------------------------------------------------------------------- Gain

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
            acodec_atempo_menu_label.grid(row=4, column=2, columnspan=1, padx=10, pady=3, sticky=W + E)
            acodec_atempo_menu = OptionMenu(audio_window, acodec_atempo, *acodec_atempo_choices.keys())
            acodec_atempo_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            acodec_atempo_menu.grid(row=5, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            acodec_atempo.set('Original')
            acodec_atempo_menu["menu"].configure(activebackground="dim grey")
            acodec_atempo_menu.bind("<Enter>", acodec_atempo_menu_hover)
            acodec_atempo_menu.bind("<Leave>", acodec_atempo_menu_hover_leave)
            # ----------------------------------------------------------------------------------------- Audio Atempo
        # --------------------------------------------------------------------------------------------- Opus Window

        # MP3 Window -------------------------------------------------------------------------------------------------
        elif encoder.get() == "MP3":
            audio_window = Toplevel()
            audio_window.title('MP3 Settings')
            audio_window.configure(background="#434547")
            window_height = 360
            window_width = 550
            screen_width = audio_window.winfo_screenwidth()
            screen_height = audio_window.winfo_screenheight()
            x_cordinate = int((screen_width / 2) - (window_width / 2))
            y_cordinate = int((screen_height / 2) - (window_height / 2))
            audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

            audio_window.grid_columnconfigure(0, weight=1)
            audio_window.grid_columnconfigure(1, weight=1)
            audio_window.grid_columnconfigure(2, weight=1)
            audio_window.grid_rowconfigure(0, weight=1)
            audio_window.grid_rowconfigure(1, weight=1)
            audio_window.grid_rowconfigure(2, weight=1)
            audio_window.grid_rowconfigure(3, weight=1)
            audio_window.grid_rowconfigure(4, weight=1)
            audio_window.grid_rowconfigure(7, weight=1)

            # Using VBR or CBR/ABR ---------------------------------------------------------------------------------
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
                # --------------------------------------------------------------------------------- VBR or CBR/ABR

            # Views Command ---------------------------------------------------------------------------------------
            def view_command():
                global cmd_label
                global cmd_line_window
                audio_filter_function()
                example_cmd_output = acodec_stream_choices[acodec_stream.get()] \
                                     + encoder_dropdownmenu_choices[encoder.get()] \
                                     + acodec_bitrate_choices[acodec_bitrate.get()] \
                                     + acodec_channel_choices[acodec_channel.get()] + mp3_abr.get() \
                                     + acodec_samplerate_choices[acodec_samplerate.get()] \
                                     + audio_filter_setting + mp3_custom_cmd_input
                try:
                    cmd_label.config(text=example_cmd_output)
                    cmd_line_window.deiconify()
                except (AttributeError, NameError):
                    cmd_line_window = Toplevel()
                    cmd_line_window.title('Command Line')
                    cmd_line_window.configure(background="#434547")
                    cmd_label = Label(cmd_line_window, text=example_cmd_output, foreground="white",
                                      background="#434547")
                    cmd_label.config(font=("Helvetica", 16))
                    cmd_label.winfo_exists()
                    cmd_label.pack()

                    def hide_instead():
                        cmd_line_window.withdraw()

                    cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

            # ----------------------------------------------------------------------------------------- Views Command

            # Buttons ---------------------------------------------------------------------------------------------
            apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A",
                                  command=gotosavefile)
            apply_button.grid(row=7, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            apply_button.bind("<Enter>", apply_button_hover)
            apply_button.bind("<Leave>", apply_button_hover_leave)

            show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A",
                              command=view_command)
            show_cmd.grid(row=7, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            show_cmd.bind("<Enter>", show_cmd_hover)
            show_cmd.bind("<Leave>", show_cmd_hover_leave)
            # -------------------------------------------------------------------------------------------- Buttons

            # Audio VBR Menu ------------------------------------------------------------------------------------------
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
            # ------------------------------------------------------------------------------------------------- VBR

            # Audio Channel Selection ---------------------------------------------------------------------------
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
            acodec_channel.trace('w', dolby_pro_logic_ii_enable_disable)
            # ------------------------------------------------------------------------------------- Audio Channel

            # VBR ---------------------------------------------------------------------------------------------------
            global mp3_vbr
            mp3_vbr = StringVar()
            mp3_vbr.set("-q:a ")
            mp3_vbr_checkbox = Checkbutton(audio_window, text='VBR', variable=mp3_vbr, onvalue='-q:a ',
                                           offvalue='off')
            mp3_vbr_checkbox.grid(row=4, column=1, rowspan=1, columnspan=1, padx=10, pady=(5, 0), sticky=N + S + E + W)
            mp3_vbr_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                       activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
            mp3_vbr.trace('w', mp3_bitrate_type)
            # ---------------------------------------------------------------------------------------------- VBR

            # ABR --------------------------------------------------------------------------------------------------
            global mp3_abr
            mp3_abr = StringVar()
            mp3_abr.set("")
            mp3_abr_checkbox = Checkbutton(audio_window, text='ABR', variable=mp3_abr, onvalue="-abr 1 ",
                                           offvalue="", state=DISABLED)
            mp3_abr_checkbox.grid(row=4, column=2, rowspan=1, columnspan=1, padx=10, pady=(0, 5), sticky=N + S + E + W)
            mp3_abr_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                       activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))

            # ------------------------------------------------------------------------------------------- ABR

            # Entry Box for Custom Command Line ----------------------------------------------------------------
            def mp3_cmd(*args):
                global mp3_custom_cmd_input
                if mp3_custom_cmd.get() == (""):
                    mp3_custom_cmd_input = ("")
                else:
                    cstmcmd = mp3_custom_cmd.get()
                    mp3_custom_cmd_input = cstmcmd + " "

            mp3_custom_cmd = StringVar()
            mp3_cmd_entrybox_label = Label(audio_window, text="Custom Command Line :", anchor=W, background="#434547",
                                           foreground="white")
            mp3_cmd_entrybox_label.grid(row=5, column=0, columnspan=2, padx=10, pady=(10, 0), sticky=N + S + W + E)
            mp3_cmd_entrybox = Entry(audio_window, textvariable=mp3_custom_cmd, borderwidth=4, background="#CACACA")
            mp3_cmd_entrybox.grid(row=6, column=0, columnspan=3, padx=10, pady=(0, 15), sticky=W + E)
            mp3_custom_cmd.trace('w', mp3_cmd)
            mp3_custom_cmd.set("")
            # -------------------------------------------------------------------------------- Custom Command Line

            # Audio Stream Selection ----------------------------------------------------------------------------
            acodec_stream = StringVar(audio_window)
            acodec_stream_choices = acodec_stream_batch_choices
            acodec_stream.set('Track 1')
            acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
            acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
            acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
            acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            acodec_stream_menu["menu"].configure(activebackground="dim grey")
            acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
            acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)
            # --------------------------------------------------------------------------------------- Audio Stream

            # Dolby Pro Logic II -------------------------------------------------------------------------------
            dolby_pro_logic_ii = StringVar()
            dolby_pro_logic_ii_checkbox = Checkbutton(audio_window, text=' Dolby Pro\nLogic II',
                                                      variable=dolby_pro_logic_ii, state=DISABLED,
                                                      onvalue='"aresample=matrix_encoding=dplii"', offvalue="")
            dolby_pro_logic_ii_checkbox.grid(row=4, column=0, columnspan=1, rowspan=1, padx=10, pady=(15, 3),
                                             sticky=N + S + E + W)
            dolby_pro_logic_ii_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                                  activeforeground="white", selectcolor="#434547",
                                                  font=("Helvetica", 11))
            dolby_pro_logic_ii.set("")
            # -------------------------------------------------------------------------------------------- DPL II

            # Audio Gain Selection ------------------------------------------------------------------------------
            ffmpeg_gain = StringVar()
            ffmpeg_gain_label = Label(audio_window, text="Gain (dB) :", background="#434547",
                                      foreground="white")
            ffmpeg_gain_label.grid(row=2, column=2, columnspan=1, padx=10, pady=3,
                                   sticky=N + S + E + W)
            ffmpeg_gain_spinbox = Spinbox(audio_window, from_=-30, to=30, increment=1.0, justify=CENTER,
                                          wrap=True, textvariable=ffmpeg_gain)
            ffmpeg_gain_spinbox.configure(background="#23272A", foreground="white", highlightthickness=1,
                                          buttonbackground="black", width=15, readonlybackground="#23272A")
            ffmpeg_gain_spinbox.grid(row=3, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            ffmpeg_gain.set(0)
            # ------------------------------------------------------------------------------------------------ Gain

            # Audio Sample Rate Selection ----------------------------------------------------------------------
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
            acodec_samplerate_label = Label(audio_window, text="Sample Rate :", background="#434547",
                                            foreground="white")
            acodec_samplerate_label.grid(row=0, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_samplerate_menu = OptionMenu(audio_window, acodec_samplerate, *acodec_samplerate_choices.keys())
            acodec_samplerate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            acodec_samplerate_menu.grid(row=1, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_samplerate_menu["menu"].configure(activebackground="dim grey")
            acodec_samplerate_menu.bind("<Enter>", acodec_samplerate_menu_hover)
            acodec_samplerate_menu.bind("<Leave>", acodec_samplerate_menu_hover_leave)
            # ---------------------------------------------------------------------------------------- Sample Rate

            # Audio Atempo Selection -------------------------------------------------------------------------------
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
            acodec_atempo.set('Original')
            acodec_atempo_menu["menu"].configure(activebackground="dim grey")
            acodec_atempo_menu.bind("<Enter>", acodec_atempo_menu_hover)
            acodec_atempo_menu.bind("<Leave>", acodec_atempo_menu_hover_leave)
            # ---------------------------------------------------------------------------------------- Audio Atempo
        # ----------------------------------------------------------------------------------------------------- MP3

            # E-AC3 Window ------------------------------------------------------------------------------------------
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
                                   text="- - - - - - - - - - - - - - - - - - - - - - - - - - "
                                        "- - - - Advanced Settings - - - - - - - - - - - - - - - - - - - - - "
                                        "- - - - - - - - -\n *All settings are set to default below*",
                                   background="#434547", foreground="white", relief=GROOVE)
            advanced_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky=W + E)

            # Views Command ----------------------------------------------------------------------------------------
            def view_command():
                global cmd_label
                global cmd_line_window
                audio_filter_function()
                example_cmd_output = acodec_stream_choices[acodec_stream.get()] \
                                     + encoder_dropdownmenu_choices[encoder.get()] + "-b:a " + eac3_spinbox.get() \
                                     + " " + acodec_channel_choices[acodec_channel.get()] \
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
                    cmd_label = Label(cmd_line_window, text=example_cmd_output, foreground="white",
                                      background="#434547")
                    cmd_label.config(font=("Helvetica", 16))
                    cmd_label.winfo_exists()
                    cmd_label.pack()

                    def hide_instead():
                        cmd_line_window.withdraw()

                    cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

            # ---------------------------------------------------------------------------------------- Views Command

            # Buttons ------------------------------------------------------------------------------------------------
            apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A",
                                  command=gotosavefile)
            apply_button.grid(row=22, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            apply_button.bind("<Enter>", apply_button_hover)
            apply_button.bind("<Leave>", apply_button_hover_leave)

            show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A",
                              command=view_command)
            show_cmd.grid(row=22, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            show_cmd.bind("<Enter>", show_cmd_hover)
            show_cmd.bind("<Leave>", show_cmd_hover_leave)

            # ----------------------------------------------------------------------------------------------- Buttons

            # Entry Box for Custom Command Line --------------------------------------------------------------------
            def eac3_cmd(*args):
                global eac3_custom_cmd_input
                if eac3_custom_cmd.get() == (""):
                    eac3_custom_cmd_input = ("")
                else:
                    cstmcmd = eac3_custom_cmd.get()
                    eac3_custom_cmd_input = cstmcmd + " "

            eac3_custom_cmd = StringVar()
            eac3_cmd_entrybox_label = Label(audio_window, text="Custom Command Line :", anchor=W, background="#434547",
                                            foreground="white")
            eac3_cmd_entrybox_label.grid(row=20, column=0, columnspan=2, padx=10, pady=(10, 0), sticky=N + S + W + E)
            eac3_cmd_entrybox = Entry(audio_window, textvariable=eac3_custom_cmd, borderwidth=4, background="#CACACA")
            eac3_cmd_entrybox.grid(row=21, column=0, columnspan=3, padx=10, pady=(0, 10), sticky=W + E)
            eac3_custom_cmd.trace('w', eac3_cmd)
            eac3_custom_cmd.set("")

            # ------------------------------------------------------------------------------------ Custom Command Line

            # Audio Bitrate Menu ----------------------------------------------------------------------------------
            global eac3_spinbox
            acodec_spinbox_values = (
            '64k ', '96k ', '160k ', '128k ', '192k ', '224k ', '256k ', '288k ', '320k ', '352k ',
            '384k ', '416k ', '448k ', '480k ', '512k ', '544k ', '576k ', '608k ', '640k ',
            '672k ', '704k ', '736k ', '768k ', '800k ', '832k ', '864k ', '896k ', '928k ',
            '960k ', '1056k ', '1088k ', '1120k ', '1152k ', '1184k ', '1216k ', '1248k ',
            '1280k ', '1312k ', '1344k ', '1376k ', '1408k ', '1440k ', '1472k ', '1504k ',
            '1536k ', '1568 ', '1600k ', '1632k ', '1664k ', '1696k ', '1728k ', '1760k ',
            '1792k ', '1824k ', '1856k ', '1888k ', '1920k ', '1952k ', '1984k ', '2016k ',
            '2048k ', '2080k ', '2112k ', '2144k ', '2176k ', '2208k ', '2240k ', '2272k ',
            '2304k ', '2336k ', '2368k ', '2400k ', '2432k ', '2464k ', '2496k ', '2528k ')
            eac3_spinbox = StringVar()
            q_acodec_quality_spinbox_label = Label(audio_window, text="Bitrate :", background="#434547",
                                                   foreground="white")
            q_acodec_quality_spinbox_label.grid(row=0, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            q_acodec_quality_spinbox = Spinbox(audio_window, values=acodec_spinbox_values, justify=CENTER, wrap=True,
                                               textvariable=eac3_spinbox, state='readonly')
            q_acodec_quality_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                            buttonbackground="black", width=10, readonlybackground="#23272A")
            q_acodec_quality_spinbox.grid(row=1, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            eac3_spinbox.set("448k ")
            # ----------------------------------------------------------------------------------------------- Bitrate

            # Audio Channel Selection -----------------------------------------------------------------------------
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
            # ----------------------------------------------------------------------------------------------- Channels

            # Audio Stream Selection ---------------------------------------------------------------------------------
            acodec_stream = StringVar(audio_window)
            acodec_stream_choices = acodec_stream_batch_choices
            acodec_stream.set('Track 1')
            acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
            acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
            acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
            acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            acodec_stream_menu["menu"].configure(activebackground="dim grey")
            acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
            acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)
            # ------------------------------------------------------------------------------------------------ Stream

            # Audio Gain Selection ----------------------------------------------------------------------------------
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
            ffmpeg_gain.set(0)
            # --------------------------------------------------------------------------------------------------- Gain

            # Audio Sample Rate Selection -----------------------------------------------------------------------------
            acodec_samplerate = StringVar(audio_window)
            acodec_samplerate_choices = {'Original': "",
                                         '32000 Hz': "-ar 32000 ",
                                         '44100 Hz': "-ar 44100 ",
                                         '48000 Hz': "-ar 48000 "}
            acodec_samplerate.set('Original')  # set the default option
            acodec_samplerate_label = Label(audio_window, text="Sample Rate :", background="#434547",
                                            foreground="white")
            acodec_samplerate_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_samplerate_menu = OptionMenu(audio_window, acodec_samplerate, *acodec_samplerate_choices.keys())
            acodec_samplerate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            acodec_samplerate_menu.grid(row=3, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_samplerate_menu["menu"].configure(activebackground="dim grey")
            acodec_samplerate_menu.bind("<Enter>", acodec_samplerate_menu_hover)
            acodec_samplerate_menu.bind("<Leave>", acodec_samplerate_menu_hover_leave)
            # ------------------------------------------------------------------------------------------ Sample Rate

            # Audio Per Frame Metadata Selection ---------------------------------------------------------------------
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
            # ----------------------------------------------------------------------------------------------- Metadata

            # Mixing Level Spinbox ----------------------------------------------------------------------------------
            global eac3_mixing_level
            eac3_mixing_level = StringVar()
            eac3_mixing_level_label = Label(audio_window, text="Mixing Level :", background="#434547",
                                            foreground="white")
            eac3_mixing_level_label.grid(row=5, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            eac3_mixing_level_spinbox = Spinbox(audio_window, from_=-1, to=111, justify=CENTER, wrap=True,
                                                textvariable=eac3_mixing_level, state='readonly')
            eac3_mixing_level_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                             buttonbackground="black", width=10, readonlybackground="#23272A")
            eac3_mixing_level_spinbox.grid(row=6, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            eac3_mixing_level.set(-1)
            # ----------------------------------------------------------------------------------------- Mixing Level

            # Room Type Selection -----------------------------------------------------------------------------------
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
            # ------------------------------------------------------------------------------------------ Room Type

            # Copyright Bit Spinbox -------------------------------------------------------------------------------
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
            # ------------------------------------------------------------------------------------------- Copyright

            # Dialogue Level Spinbox -----------------------------------------------------------------------------
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
            dialogue_level.set(-31)
            # ----------------------------------------------------------------------------------------- Dialogue Level

            # Dolby Surround Mode Selection --------------------------------------------------------------------------
            global dolby_surround_mode, dolby_surround_mode_choices
            dolby_surround_mode = StringVar(audio_window)
            dolby_surround_mode_choices = {'Default': "",
                                           'Not Indicated': "-dsur_mode 0 ",
                                           'On': "-dsur_mode 1 ",
                                           'Off': "-dsur_mode 2 "}
            dolby_surround_mode.set('Default')  # set the default option
            dolby_surround_mode_label = Label(audio_window, text="Dolby Surround Mode :", background="#434547",
                                              foreground="white")
            dolby_surround_mode_label.grid(row=7, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            dolby_surround_mode_menu = OptionMenu(audio_window, dolby_surround_mode,
                                                  *dolby_surround_mode_choices.keys())
            dolby_surround_mode_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            dolby_surround_mode_menu.grid(row=8, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            dolby_surround_mode_menu["menu"].configure(activebackground="dim grey")
            dolby_surround_mode_menu.bind("<Enter>", dolby_surround_mode_menu_hover)
            dolby_surround_mode_menu.bind("<Leave>", dolby_surround_mode_menu_hover_leave)
            # -------------------------------------------------------------------------------------- Dolby Surround

            # Original Bit Stream Spinbox --------------------------------------------------------------------------
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
            original_bit_stream.set(-1)
            # ------------------------------------------------------------------------------------------- Bit Stream

            # Downmix Mode Selection --------------------------------------------------------------------------------
            global downmix_mode, downmix_mode_choices
            downmix_mode = StringVar(audio_window)
            downmix_mode_choices = {'Default': "",
                                    'Not Indicated': "-dmix_mode 0 ",
                                    'Lt/RT Downmix': "-dmix_mode 1 ",
                                    'Lo/Ro Downmix': "-dmix_mode 2 ",
                                    'Dolby Pro Logic II': "-dmix_mode 3 "}
            downmix_mode.set('Default')  # set the default option
            downmix_mode_label = Label(audio_window, text="Stereo Downmix Mode :", background="#434547",
                                       foreground="white")
            downmix_mode_label.grid(row=9, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            downmix_mode_menu = OptionMenu(audio_window, downmix_mode, *downmix_mode_choices.keys())
            downmix_mode_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            downmix_mode_menu.grid(row=10, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            downmix_mode_menu["menu"].configure(activebackground="dim grey")
            downmix_mode_menu.bind("<Enter>", downmix_mode_menu_hover)
            downmix_mode_menu.bind("<Leave>", downmix_mode_menu_hover_leave)
            # ------------------------------------------------------------------------------------------- Downmix Mode

            # Lt/Rt Center Mix Level Spinbox --------------------------------------------------------------------
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
            lt_rt_center_mix.set(-1)
            # -------------------------------------------------------------------------------- Lt/Rt Center Mix Level

            # Lt/Rt Surround Mix Level Spinbox ---------------------------------------------------------------------
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
            lt_rt_surround_mix.set(-1)
            # ---------------------------------------------------------------------------- Lt/Rt Surround Mix Level

            # Lo/Ro Center Mix Level Spinbox ------------------------------------------------------------------------
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
            lo_ro_center_mix.set(-1)
            # -------------------------------------------------------------------------------- Lo/Ro Center Mix Level

            # Lo/Ro Surround Mix Level Spinbox ---------------------------------------------------------------------
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
            lo_ro_surround_mix.set(-1)
            # ------------------------------------------------------------------------------ Lo/Ro Surround Mix Level

            # Dolby Surround EX Mode Selection ---------------------------------------------------------------------
            global dolby_surround_ex_mode, dolby_surround_ex_mode_choices
            dolby_surround_ex_mode = StringVar(audio_window)
            dolby_surround_ex_mode_choices = {'Default': "",
                                              'Not Indicated': "-dsurex_mode 0 ",
                                              'On': "-dsurex_mode 2 ",
                                              'Off': "-dsurex_mode 1 ",
                                              'Dolby Pro Login IIz': "-dsurex_mode 3 "}
            dolby_surround_ex_mode.set('Default')  # set the default option
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
            # -------------------------------------------------------------------------------- Dolby Surround EX Mode

            # Dolby Headphone Mode Selection ------------------------------------------------------------------------
            global dolby_headphone_mode, dolby_headphone_mode_choices
            dolby_headphone_mode = StringVar(audio_window)
            dolby_headphone_mode_choices = {'Default': "",
                                            'Not Indicated': "-dheadphone_mode 0 ",
                                            'On': "-dheadphone_mode 2 ",
                                            'Off': "-dheadphone_mode 1 "}
            dolby_headphone_mode.set('Default')  # set the default option
            dolby_headphone_mode_label = Label(audio_window, text="Dolby Headphone Mode :", background="#434547",
                                               foreground="white")
            dolby_headphone_mode_label.grid(row=13, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            dolby_headphone_mode_menu = OptionMenu(audio_window, dolby_headphone_mode,
                                                   *dolby_headphone_mode_choices.keys())
            dolby_headphone_mode_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            dolby_headphone_mode_menu.grid(row=14, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            dolby_headphone_mode_menu["menu"].configure(activebackground="dim grey")
            dolby_headphone_mode_menu.bind("<Enter>", dolby_headphone_mode_menu_hover)
            dolby_headphone_mode_menu.bind("<Leave>", dolby_headphone_mode_menu_hover_leave)
            # ------------------------------------------------------------------------------------ Dolby Headphone

            # A/D Converter Type Selection ------------------------------------------------------------------------
            global a_d_converter_type, a_d_converter_type_choices
            a_d_converter_type = StringVar(audio_window)
            a_d_converter_type_choices = {'Default': "",
                                          'Standard': "-ad_conv_type 0 ",
                                          'HDCD': "-ad_conv_type 1 "}
            a_d_converter_type.set('Default')  # set the default option
            a_d_converter_type_label = Label(audio_window, text="A/D Converter Type :", background="#434547",
                                             foreground="white")
            a_d_converter_type_label.grid(row=13, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            a_d_converter_type_menu = OptionMenu(audio_window, a_d_converter_type, *a_d_converter_type_choices.keys())
            a_d_converter_type_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            a_d_converter_type_menu.grid(row=14, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            a_d_converter_type_menu["menu"].configure(activebackground="dim grey")
            a_d_converter_type_menu.bind("<Enter>", a_d_converter_type_menu_hover)
            a_d_converter_type_menu.bind("<Leave>", a_d_converter_type_menu_hover_leave)
            # ------------------------------------------------------------------------------------------ A/D Converter

            # Stereo Rematrixing Selection ---------------------------------------------------------------------
            global stereo_rematrixing, stereo_rematrixing_choices
            stereo_rematrixing = StringVar(audio_window)
            stereo_rematrixing_choices = {'Default': "",
                                          'True': "-stereo_rematrixing true ",
                                          'False': "-stereo_rematrixing false "}
            stereo_rematrixing.set('Default')  # set the default option
            stereo_rematrixing_label = Label(audio_window, text="Stereo Rematrixing :", background="#434547",
                                             foreground="white")
            stereo_rematrixing_label.grid(row=15, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            stereo_rematrixing_menu = OptionMenu(audio_window, stereo_rematrixing, *stereo_rematrixing_choices.keys())
            stereo_rematrixing_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            stereo_rematrixing_menu.grid(row=16, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            stereo_rematrixing_menu["menu"].configure(activebackground="dim grey")
            stereo_rematrixing_menu.bind("<Enter>", stereo_rematrixing_menu_hover)
            stereo_rematrixing_menu.bind("<Leave>", stereo_rematrixing_menu_hover_leave)
            # ----------------------------------------------------------------------------------- Stereo Rematrixing

            # Channel Coupling Spinbox -----------------------------------------------------------------------------
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
            channel_coupling.set(-1)
            # -------------------------------------------------------------------------------------- Channel Coupling

            # Channel CPL Band Spinbox ------------------------------------------------------------------------------
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
            cpl_start_band.set(-1)
            # ------------------------------------------------------------------------------------- Channel CPL Band

            # Audio Atempo Selection ----------------------------------------------------------------------------
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
            acodec_atempo.set('Original')
            acodec_atempo_menu["menu"].configure(activebackground="dim grey")
            acodec_atempo_menu.bind("<Enter>", acodec_atempo_menu_hover)
            acodec_atempo_menu.bind("<Leave>", acodec_atempo_menu_hover_leave)
            # ----------------------------------------------------------------------------------------- Audio Atempo
        # ----------------------------------------------------------------------------------------------- E-AC3

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

            # -------------------------------------------------------------------------------------------- FDK Help

            # Views Command ----------------------------------------------------------------------------------------
            def view_command():
                global cmd_label
                global cmd_line_window
                audio_filter_function()
                example_cmd_output = acodec_stream_choices[acodec_stream.get()] + \
                                     acodec_channel_choices[acodec_channel.get()] + \
                                     acodec_samplerate_choices[acodec_samplerate.get()] + \
                                     audio_filter_setting + "-f caf - | " + \
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
                    cmd_label = Label(cmd_line_window, text=example_cmd_output, foreground="white",
                                      background="#434547")
                    cmd_label.config(font=("Helvetica", 16))
                    cmd_label.winfo_exists()
                    cmd_label.pack()

                    def hide_instead():
                        cmd_line_window.withdraw()

                    cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

            # --------------------------------------------------------------------------------------- Views Command

            # Buttons ---------------------------------------------------------------------------------------------
            apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A",
                                  command=gotosavefile)
            apply_button.grid(row=15, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            apply_button.bind("<Enter>", apply_button_hover)
            apply_button.bind("<Leave>", apply_button_hover_leave)

            show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A",
                              command=view_command)
            show_cmd.grid(row=15, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            show_cmd.bind("<Enter>", show_cmd_hover)
            show_cmd.bind("<Leave>", show_cmd_hover_leave)

            help_button = Button(audio_window, text="Help + Information", foreground="white", background="#23272A",
                                 command=gotofdkaachelp)
            help_button.grid(row=15, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            help_button.bind("<Enter>", help_button_hover)
            help_button.bind("<Leave>", help_button_hover_leave)
            # --------------------------------------------------------------------------------------- Buttons

            advanced_label = Label(audio_window,
                                   text="- - - - - - - - - - - - - - - - - - - - Advanced Settings - - - - "
                                        "- - - - - - - - - - - - - - - -",
                                   background="#434547", foreground="white", relief=GROOVE)
            advanced_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky=W + E)

            # Audio Bitrate Menu ----------------------------------------------------------------------------------
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
            # --------------------------------------------------------------------------------------- Bitrate Menu

            # Audio Channel Selection -------------------------------------------------------------------------
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
            acodec_channel.trace('w', dolby_pro_logic_ii_enable_disable)
            # -------------------------------------------------------------------------------------------- Channel

            # Audio Stream Selection -----------------------------------------------------------------------------
            acodec_stream = StringVar(audio_window)
            acodec_stream_choices = acodec_stream_batch_choices
            acodec_stream.set('Track 1')
            acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
            acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
            acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
            acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            acodec_stream_menu["menu"].configure(activebackground="dim grey")
            acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
            acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)
            # -------------------------------------------------------------------------------------------- Stream

            # Dolby Pro Logic II ---------------------------------------------------------------------------
            dolby_pro_logic_ii = StringVar()
            dolby_pro_logic_ii_checkbox = Checkbutton(audio_window, text=' Dolby Pro\nLogic II',
                                                      variable=dolby_pro_logic_ii, state=DISABLED,
                                                      onvalue='"aresample=matrix_encoding=dplii"', offvalue="")
            dolby_pro_logic_ii_checkbox.grid(row=10, column=2, columnspan=1, rowspan=1, padx=10, pady=3,
                                             sticky=N + S + E + W)
            dolby_pro_logic_ii_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                                  activeforeground="white", selectcolor="#434547",
                                                  font=("Helvetica", 11))
            dolby_pro_logic_ii.set("")
            # ------------------------------------------------------------------------------------------- DPL II

            # Audio Gain Selection -------------------------------------------------------------------------------
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
            ffmpeg_gain.set(0)
            # -------------------------------------------------------------------------------------------- Gain

            # Audio Sample Rate Selection -----------------------------------------------------------------------
            acodec_samplerate = StringVar(audio_window)
            acodec_samplerate_choices = {'Original': "",
                                         '11025 Hz': "-ar 11025 ",
                                         '22050 Hz': "-ar 22050 ",
                                         '44100 Hz': "-ar 44100 ",
                                         '48000 Hz': "-ar 48000 ",
                                         '88200 Hz': "-ar 88200 ",
                                         '96000 Hz': "-ar 96000 "}
            acodec_samplerate.set('Original')  # set the default option
            acodec_samplerate_label = Label(audio_window, text="Sample Rate :", background="#434547",
                                            foreground="white")
            acodec_samplerate_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_samplerate_menu = OptionMenu(audio_window, acodec_samplerate, *acodec_samplerate_choices.keys())
            acodec_samplerate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            acodec_samplerate_menu.grid(row=3, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_samplerate_menu["menu"].configure(activebackground="dim grey")
            acodec_samplerate_menu.bind("<Enter>", acodec_samplerate_menu_hover)
            acodec_samplerate_menu.bind("<Leave>", acodec_samplerate_menu_hover_leave)

            # --------------------------------------------------------------------------------------- Sample Rate

            # Entry Box for Custom Command Line ---------------------------------------------------------------------
            def fdkaac_cmd(*args):
                global fdkaac_custom_cmd_input
                if fdkaac_custom_cmd.get() == (""):
                    fdkaac_custom_cmd_input = ("")
                else:
                    cstmcmd = fdkaac_custom_cmd.get()
                    fdkaac_custom_cmd_input = cstmcmd + " "

            fdkaac_custom_cmd = StringVar()
            fdkaac_cmd_entrybox_label = Label(audio_window, text="Custom Command Line :", anchor=W,
                                              background="#434547",
                                              foreground="white")
            fdkaac_cmd_entrybox_label.grid(row=11, column=0, columnspan=2, padx=10, pady=(0, 0), sticky=N + S + W + E)
            fdkaac_cmd_entrybox = Entry(audio_window, textvariable=fdkaac_custom_cmd, borderwidth=4,
                                        background="#CACACA")
            fdkaac_cmd_entrybox.grid(row=12, column=0, columnspan=3, padx=10, pady=(0, 0), sticky=W + E)
            fdkaac_custom_cmd.trace('w', fdkaac_cmd)
            fdkaac_custom_cmd.set("")

            # ----------------------------------------------------------------------------------- Custom Command Line

            # Entry Box for Track Title ------------------------------------------------------------------------
            def fdkaac_title_check(*args):
                global fdkaac_title_input
                if fdkaac_title.get() == (""):
                    fdkaac_title_input = ("")
                else:
                    title_cmd = fdkaac_title.get()
                    fdkaac_title_input = "--title " + '"' + title_cmd + '"' + " "

            fdkaac_title = StringVar()
            fdkaac_title_entrybox_label = Label(audio_window, text="Track Name :", anchor=W, background="#434547",
                                                foreground="white")
            fdkaac_title_entrybox_label.grid(row=13, column=0, columnspan=2, padx=10, pady=(5, 0), sticky=N + S + W + E)
            fdkaac_title_entrybox = Entry(audio_window, textvariable=fdkaac_title, borderwidth=4, background="#CACACA")
            fdkaac_title_entrybox.grid(row=14, column=0, columnspan=3, padx=10, pady=(0, 10), sticky=W + E)
            fdkaac_title.trace('w', fdkaac_title_check)
            fdkaac_title.set("")
            # ---------------------------------------------------------------------------------------- Track Title

            # Audio Profile Selection ------------------------------------------------------------------------------
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
            # ------------------------------------------------------------------------------- Profile Selection

            # Audio Lowdelay SBR Selection -------------------------------------------------------------------------
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
            # ---------------------------------------------------------------------------------------- Low Delay

            # Audio SBR Ratio ----------------------------------------------------------------------------------
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
            # ----------------------------------------------------------------------------------------------- SBR Ratio

            # Audio Gapless Mode --------------------------------------------------------------------------------
            global acodec_gapless_mode
            global acodec_gapless_mode_choices
            acodec_gapless_mode = StringVar(audio_window)
            acodec_gapless_mode_choices = {'iTunSMPB (Def)': "-G0 ",
                                           'ISO Standard (EDTS+SGPD)': "-G1 ",
                                           'Both': "-G2 "}
            acodec_gapless_mode.set('iTunSMPB (Def)')  # set the default option
            acodec_gapless_mode_label = Label(audio_window, text="SBR Ratio :", background="#434547",
                                              foreground="white")
            acodec_gapless_mode_label.grid(row=7, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_gapless_mode_menu = OptionMenu(audio_window, acodec_gapless_mode,
                                                  *acodec_gapless_mode_choices.keys())
            acodec_gapless_mode_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            acodec_gapless_mode_menu.grid(row=8, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_gapless_mode_menu["menu"].configure(activebackground="dim grey")
            acodec_gapless_mode_menu.bind("<Enter>", acodec_gapless_mode_menu_hover)
            acodec_gapless_mode_menu.bind("<Leave>", acodec_gapless_mode_menu_hover_leave)
            # ----------------------------------------------------------------------------------- Audio Gapless Mode

            # Audio Transport Format -------------------------------------------------------------------------------
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
            # ---------------------------------------------------------------------------------------------- Transport

            # Misc Checkboxes - Afterburner --------------------------------------------------------------------------
            global afterburnervar
            afterburnervar = StringVar()
            afterburnervar.set("-a1 ")
            afterburner_checkbox = Checkbutton(audio_window, text='Afterburner', variable=afterburnervar,
                                               onvalue="-a1 ",
                                               offvalue="-a0 ")
            afterburner_checkbox.grid(row=8, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            afterburner_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                           activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
            # -------------------------------------------------------------------------------------------- Afterburner

            # Misc Checkboxes - Add CRC Check on ADTS Header --------------------------------------------------------
            global crccheck
            crccheck = StringVar()
            crccheck.set("")
            crccheck_checkbox = Checkbutton(audio_window, text='CRC Check on\n ADTS Header', variable=crccheck,
                                            onvalue="-C ", offvalue="")
            crccheck_checkbox.grid(row=9, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            crccheck_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                        activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
            # -------------------------------------------------------------------------------------------------- CRC

            # Misc Checkboxes - Header Period -----------------------------------------------------------------------
            global headerperiod
            headerperiod = StringVar()
            headerperiod.set("")
            headerperiod_checkbox = Checkbutton(audio_window, text='Header Period', variable=headerperiod,
                                                onvalue="-h ", offvalue="")
            headerperiod_checkbox.grid(row=9, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            headerperiod_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                            activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
            # ------------------------------------------------------------------------------------------------- Header

            # Misc Checkboxes - Include SBR Delay ---------------------------------------------------------------------
            global sbrdelay
            sbrdelay = StringVar()
            sbrdelay.set("")
            sbrdelay_checkbox = Checkbutton(audio_window, text='SBR Delay', variable=sbrdelay,
                                            onvalue="--include-sbr-delay ", offvalue="")
            sbrdelay_checkbox.grid(row=9, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            sbrdelay_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                        activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
            # ---------------------------------------------------------------------------------------------- SBR Delay

            # Misc Checkboxes - Place Moov Box Before Mdat Box ------------------------------------------------------
            global moovbox
            moovbox = StringVar()
            moovbox.set("")
            moovbox_checkbox = Checkbutton(audio_window, text='Place Moov Box Before Mdat Box', variable=moovbox,
                                           onvalue="--moov-before-mdat ", offvalue="")
            moovbox_checkbox.grid(row=10, column=0, columnspan=2, padx=10, pady=3, sticky=N + S + E + W)
            moovbox_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                       activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
            # ---------------------------------------------------------------------------------------------- Moov Box

            # Audio Atempo Selection -------------------------------------------------------------------------------
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
            acodec_atempo.set('Original')
            acodec_atempo_menu["menu"].configure(activebackground="dim grey")
            acodec_atempo_menu.bind("<Enter>", acodec_atempo_menu_hover)
            acodec_atempo_menu.bind("<Leave>", acodec_atempo_menu_hover_leave)
            # -------------------------------------------------------------------------------------------- Audio Atempo
        # -------------------------------------------------------------------------------------------------- FDK AAC

        # Qaac Window -------------------------------------------------------------------------------------------------
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

            # Gets gain information for QAAC -----------------------------------------------------------------------
            def qaac_gain_trace(*args):
                global set_qaac_gain
                if q_acodec_gain.get() == '0':
                    set_qaac_gain = ''
                elif q_acodec_gain.get() != '0':
                    set_qaac_gain = '--gain ' + q_acodec_gain.get() + ' '

            # ------------------------------------------------------------------------------------------ QAAC Get Gain

            # Help ---------------------------------------------------------------------------------------------------
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

            # ------------------------------------------------------------------------------------------- Help

            # Views Command ---------------------------------------------------------------------------------------
            def view_command():
                global cmd_label
                global cmd_line_window
                audio_filter_function()
                if q_acodec_profile.get() == "True VBR":
                    example_cmd_output = acodec_stream_choices[acodec_stream.get()] + acodec_channel_choices[
                        acodec_channel.get()] + acodec_samplerate_choices[acodec_samplerate.get()] \
                                         + audio_filter_setting \
                                         + "\n \n" + "-f wav - | " + qaac + " " + "\n \n" \
                                         + q_acodec_profile_choices[
                                             q_acodec_profile.get()] + q_acodec_quality_amnt.get() \
                                         + " " + qaac_high_efficiency.get() + qaac_nodither.get() \
                                         + set_qaac_gain + \
                                         q_acodec_quality_choices[q_acodec_quality.get()] + qaac_normalize.get() \
                                         + qaac_nodelay.get() + q_gapless_mode_choices[q_gapless_mode.get()] \
                                         + qaac_nooptimize.get() + qaac_threading.get() + qaac_limiter.get() \
                                         + qaac_title_input + qaac_custom_cmd_input
                else:
                    example_cmd_output = acodec_stream_choices[acodec_stream.get()] + \
                                         acodec_channel_choices[acodec_channel.get()] + \
                                         acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting \
                                         + "\n \n" + "-f wav - | " + qaac + " " + "\n \n" \
                                         + q_acodec_profile_choices[q_acodec_profile.get()] + \
                                         q_acodec_bitrate.get() + " " + qaac_high_efficiency.get() \
                                         + qaac_nodither.get() + set_qaac_gain + \
                                         q_acodec_quality_choices[q_acodec_quality.get()] + qaac_normalize.get() \
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
                    cmd_label = Label(cmd_line_window, text=example_cmd_output, foreground="white",
                                      background="#434547")
                    cmd_label.config(font=("Helvetica", 16))
                    cmd_label.winfo_exists()
                    cmd_label.pack()

                    def hide_instead():
                        cmd_line_window.withdraw()

                    cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

            # ------------------------------------------------------------------------------------------ Views Command

            # Buttons ---------------------------------------------------------------------------------------------
            apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A",
                                  command=gotosavefile)
            apply_button.grid(row=16, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            apply_button.bind("<Enter>", apply_button_hover)
            apply_button.bind("<Leave>", apply_button_hover_leave)

            show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A",
                              command=view_command)
            show_cmd.grid(row=16, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            show_cmd.bind("<Enter>", show_cmd_hover)
            show_cmd.bind("<Leave>", show_cmd_hover_leave)

            help_button = Button(audio_window, text="Help + Information", foreground="white", background="#23272A",
                                 command=gotoqaachelp)
            help_button.grid(row=16, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            help_button.bind("<Enter>", help_button_hover)
            help_button.bind("<Leave>", help_button_hover_leave)
            # --------------------------------------------------------------------------------------------- Buttons

            advanced_label = Label(audio_window,
                                   text="- - - - - - - - - - - - - - - - - - - - Advanced Settings - - "
                                        "- - - - - - - - - - - - - - - - - -",
                                   background="#434547", foreground="white", relief=GROOVE)
            advanced_label.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky=W + E)

            # Quality or Bitrate -----------------------------------------------------------------------------------
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

            # ----------------------------------------------------------------------------------- Quality or Bitrate

            # Audio Profile Menu -------------------------------------------------------------------------------
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
            # ------------------------------------------------------------------------------------- Audio Profile Menu

            # Dolby Pro Logic II --------------------------------------------------------------------------------------
            dolby_pro_logic_ii = StringVar()
            dolby_pro_logic_ii_checkbox = Checkbutton(audio_window, text=' Dolby Pro\nLogic II',
                                                      variable=dolby_pro_logic_ii, state=DISABLED,
                                                      onvalue='"aresample=matrix_encoding=dplii"', offvalue="",
                                                      command=audio_filter_function)
            dolby_pro_logic_ii_checkbox.grid(row=5, column=2, columnspan=1, rowspan=1, padx=10, pady=3,
                                             sticky=N + S + E + W)
            dolby_pro_logic_ii_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                                  activeforeground="white", selectcolor="#434547",
                                                  font=("Helvetica", 11))
            dolby_pro_logic_ii.set("")
            # -------------------------------------------------------------------------------------------------- DPL II

            # Audio Channel Selection --------------------------------------------------------------------------------
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
            acodec_channel.trace('w', dolby_pro_logic_ii_enable_disable)
            acodec_channel.set('Original')
            # ------------------------------------------------------------------------------------- Audio Channel

            # Audio Stream Selection -----------------------------------------------------------------------------
            acodec_stream = StringVar(audio_window)
            acodec_stream_choices = acodec_stream_batch_choices
            acodec_stream.set('Track 1')
            acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
            acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
            acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
            acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
            acodec_stream_menu["menu"].configure(activebackground="dim grey")
            acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
            acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)

            # ------------------------------------------------------------------------------------------ Audio Stream

            # Entry Box for Custom Command Line --------------------------------------------------------------------
            def qaac_cmd(*args):
                global qaac_custom_cmd_input
                if qaac_custom_cmd.get() == (""):
                    qaac_custom_cmd_input = ("")
                else:
                    cstmcmd = qaac_custom_cmd.get()
                    qaac_custom_cmd_input = cstmcmd + " "

            qaac_custom_cmd = StringVar()
            qaac_cmd_entrybox_label = Label(audio_window, text="Custom Command Line :", anchor=W, background="#434547",
                                            foreground="white")
            qaac_cmd_entrybox_label.grid(row=12, column=0, columnspan=2, padx=10, pady=(0, 0), sticky=N + S + W + E)
            qaac_cmd_entrybox = Entry(audio_window, textvariable=qaac_custom_cmd, borderwidth=4, background="#CACACA")
            qaac_cmd_entrybox.grid(row=13, column=0, columnspan=3, padx=10, pady=(0, 0), sticky=W + E)
            qaac_custom_cmd.trace('w', qaac_cmd)
            qaac_custom_cmd.set("")

            # ------------------------------------------------------------------------------- Custom Command Line

            # Entry Box for Track Title ----------------------------------------------------------------------------
            def qaac_title_check(*args):
                global qaac_title_input
                if qaac_title.get() == (""):
                    qaac_title_input = ("")
                else:
                    title_cmd = qaac_title.get()
                    qaac_title_input = "--title " + '"' + title_cmd + '"' + " "

            qaac_title = StringVar()
            qaac_title_entrybox_label = Label(audio_window, text="Track Name :", anchor=W, background="#434547",
                                              foreground="white")
            qaac_title_entrybox_label.grid(row=14, column=0, columnspan=2, padx=10, pady=(5, 0), sticky=N + S + W + E)
            qaac_title_entrybox = Entry(audio_window, textvariable=qaac_title, borderwidth=4, background="#CACACA")
            qaac_title_entrybox.grid(row=15, column=0, columnspan=3, padx=10, pady=(0, 10), sticky=W + E)
            qaac_title.trace('w', qaac_title_check)
            qaac_title.set("")
            # ------------------------------------------------------------------------------------------ Track Title

            # Audio Sample Rate Selection ----------------------------------------------------------------------
            acodec_samplerate = StringVar(audio_window)
            acodec_samplerate_choices = {'Original': "",
                                         '11025 Hz': "-ar 11025 ",
                                         '22050 Hz': "-ar 22050 ",
                                         '44100 Hz': "-ar 44100 ",
                                         '48000 Hz': "-ar 48000 ",
                                         '88200 Hz': "-ar 88200 ",
                                         '96000 Hz': "-ar 96000 "}
            acodec_samplerate.set('Original')  # set the default option
            acodec_samplerate_label = Label(audio_window, text="Sample Rate :", background="#434547",
                                            foreground="white")
            acodec_samplerate_label.grid(row=4, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_samplerate_menu = OptionMenu(audio_window, acodec_samplerate, *acodec_samplerate_choices.keys())
            acodec_samplerate_menu.config(background="#23272A", foreground="white", highlightthickness=1)
            acodec_samplerate_menu.grid(row=5, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_samplerate_menu["menu"].configure(activebackground="dim grey")
            acodec_samplerate_menu.bind("<Enter>", acodec_samplerate_menu_hover)
            acodec_samplerate_menu.bind("<Leave>", acodec_samplerate_menu_hover_leave)
            # ------------------------------------------------------------------------------------------ Samplerate

            # Audio Quality Selection --------------------------------------------------------------------------------
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
            # -----------------------------------------------------------------------------------------------------

            # Audio Quality Spinbox --------------------------------------------------------------------------------
            global q_acodec_quality_amnt
            q_acodec_quality_amnt = StringVar(audio_window)
            q_acodec_quality_amnt_choices = ('0', '9', '18', '27', '36', '45', '54', '63', '73',
                                             '82', '91', '100', '109', '118', '127')
            q_acodec_quality_spinbox_label = Label(audio_window, text="T-VBR Quality :", background="#434547",
                                                   foreground="white")
            q_acodec_quality_spinbox_label.grid(row=2, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            q_acodec_quality_spinbox = Spinbox(audio_window, values=q_acodec_quality_amnt_choices, justify=CENTER,
                                               wrap=True, textvariable=q_acodec_quality_amnt, width=13,
                                               state='readonly')
            q_acodec_quality_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                            buttonbackground="black", disabledbackground='grey',
                                            readonlybackground="#23272A")
            q_acodec_quality_spinbox.grid(row=3, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            q_acodec_quality_amnt.set('109')
            # ---------------------------------------------------------------------------------------------- Quality

            # Audio Bitrate -----------------------------------------------------------------------------------------
            global q_acodec_bitrate
            q_acodec_bitrate = StringVar(audio_window)
            q_acodec_bitrate.set(256)
            q_acodec_bitrate_label = Label(audio_window, text="Bitrate :", background="#434547", foreground="white")
            q_acodec_bitrate_label.grid(row=2, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            q_acodec_bitrate_spinbox = Spinbox(audio_window, from_=0, to=1280, justify=CENTER, wrap=True,
                                               textvariable=q_acodec_bitrate, width=13, state=DISABLED)
            q_acodec_bitrate_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                            buttonbackground="black", disabledbackground='grey')
            q_acodec_bitrate_spinbox.grid(row=3, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            # -------------------------------------------------------------------------------------------- Bitrate

            # QAAC Gain --------------------------------------------------------------------------------------------
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
            q_acodec_gain.set(0)
            # ------------------------------------------------------------------------------------------------- Gain

            # Misc Checkboxes - Normalize ---------------------------------------------------------------------------
            global qaac_normalize
            qaac_normalize = StringVar()
            qaac_normalize.set("")
            qaac_normalize_checkbox = Checkbutton(audio_window, text='Normalize', variable=qaac_normalize,
                                                  onvalue="--normalize ",
                                                  offvalue="")
            qaac_normalize_checkbox.grid(row=10, column=1, columnspan=1, padx=10, pady=(10, 3), sticky=N + S + E + W)
            qaac_normalize_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                              activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
            # --------------------------------------------------------------------------------------------- Normalize

            # Misc Checkboxes - High Efficiency --------------------------------------------------------------
            global qaac_high_efficiency
            qaac_high_efficiency = StringVar()
            qaac_high_efficiency.set("")
            qaac_high_efficiency_checkbox = Checkbutton(audio_window, text='High Efficiency',
                                                        variable=qaac_high_efficiency,
                                                        onvalue="--he ",
                                                        offvalue="", state=DISABLED)
            qaac_high_efficiency_checkbox.grid(row=8, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            qaac_high_efficiency_checkbox.configure(background="#434547", foreground="white",
                                                    activebackground="#434547",
                                                    activeforeground="white", selectcolor="#434547",
                                                    font=("Helvetica", 12))
            # ------------------------------------------------------------------------------------- High Effeciency

            # Misc Checkboxes - No Dither When Quantizing to Lower Bit Depth ---------------------------------------
            global qaac_nodither
            qaac_nodither = StringVar()
            qaac_nodither.set("")
            qaac_nodither_checkbox = Checkbutton(audio_window, text='No Dither',
                                                 variable=qaac_nodither, onvalue="--no-dither ",
                                                 offvalue="")
            qaac_nodither_checkbox.grid(row=7, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            qaac_nodither_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                             activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
            # ---------------------------------------------------------------------------------------------- No Dither

            # Misc Checkboxes - No Delay ------------------------------------------------------------------------
            global qaac_nodelay
            qaac_nodelay = StringVar()
            qaac_nodelay.set("")
            qaac_nodelay_checkbox = Checkbutton(audio_window, text='No Delay',
                                                variable=qaac_nodelay, onvalue="--no-delay ",
                                                offvalue="")
            qaac_nodelay_checkbox.grid(row=7, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            qaac_nodelay_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                            activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
            # ----------------------------------------------------------------------------------------------- No Delay

            # Gapless Mode ----------------------------------------------------------------------------------------
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
            # ------------------------------------------------------------------------------------------ Gapless Mode

            # Misc Checkboxes - No Optimize ---------------------------------------------------------------------
            global qaac_nooptimize
            qaac_nooptimize = StringVar()
            qaac_nooptimize.set("")
            qaac_nooptimize_checkbox = Checkbutton(audio_window, text='No Optimize',
                                                   variable=qaac_nooptimize, onvalue="--no-optimize ",
                                                   offvalue="")
            qaac_nooptimize_checkbox.grid(row=7, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            qaac_nooptimize_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                               activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
            # --------------------------------------------------------------------------------------------- No Optimize

            # Misc Checkboxes - Threading ---------------------------------------------------------------------
            global qaac_threading
            qaac_threading = StringVar()
            qaac_threading.set("")
            qaac_threading_checkbox = Checkbutton(audio_window, text='Threading',
                                                  variable=qaac_threading, onvalue="--threading ",
                                                  offvalue="")
            qaac_threading_checkbox.grid(row=10, column=0, columnspan=1, padx=10, pady=(10, 3), sticky=N + S + E + W)
            qaac_threading_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                              activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
            # --------------------------------------------------------------------------------------------- Threading

            # Misc Checkboxes - Limiter -----------------------------------------------------------------------------
            global qaac_limiter
            qaac_limiter = StringVar()
            qaac_limiter.set("")
            qaac_limiter_checkbox = Checkbutton(audio_window, text='Limiter',
                                                variable=qaac_limiter, onvalue="--limiter ",
                                                offvalue="")
            qaac_limiter_checkbox.grid(row=9, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            qaac_limiter_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                            activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
            # --------------------------------------------------------------------------------------------- Limiter

            # Audio Atempo Selection ---------------------------------------------------------------------------------
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
            acodec_atempo.set('Original')
            acodec_atempo_menu["menu"].configure(activebackground="dim grey")
            acodec_atempo_menu.bind("<Enter>", acodec_atempo_menu_hover)
            acodec_atempo_menu.bind("<Leave>", acodec_atempo_menu_hover_leave)
            # ------------------------------------------------------------------------------------------ Audio Atempo
        # ---------------------------------------------------------------------------------------------------- QAAC

        # FLAC Window -------------------------------------------------------------------------------------------------
        if encoder.get() == "FLAC":
            try:
                audio_window.deiconify()
            except:
                audio_window = Toplevel()
                audio_window.title('FLAC Settings')
                audio_window.configure(background="#434547")
                window_height = 550
                window_width = 650
                screen_width = audio_window.winfo_screenwidth()
                screen_height = audio_window.winfo_screenheight()
                x_cordinate = int((screen_width / 2) - (window_width / 2))
                y_cordinate = int((screen_height / 2) - (window_height / 2))
                audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

                audio_window.grid_columnconfigure(0, weight=1)
                audio_window.grid_columnconfigure(1, weight=1)
                audio_window.grid_columnconfigure(2, weight=1)
                audio_window.grid_rowconfigure(0, weight=1)
                audio_window.grid_rowconfigure(1, weight=1)
                audio_window.grid_rowconfigure(2, weight=1)
                audio_window.grid_rowconfigure(3, weight=1)
                audio_window.grid_rowconfigure(4, weight=1)
                audio_window.grid_rowconfigure(6, weight=1)
                audio_window.grid_rowconfigure(7, weight=1)
                audio_window.grid_rowconfigure(10, weight=1)

                # Views Command ---------------------------------------------------------------------------------------
                def view_command():
                    global cmd_line_window
                    global cmd_label
                    audio_filter_function()
                    example_cmd_output = acodec_stream_choices[acodec_stream.get()] \
                                         + encoder_dropdownmenu_choices[encoder.get()] + \
                                         acodec_bitrate_choices[acodec_bitrate.get()] + \
                                         acodec_channel_choices[acodec_channel.get()] + \
                                         acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting \
                                         + set_flac_acodec_coefficient \
                                         + acodec_flac_lpc_type_choices[acodec_flac_lpc_type.get()] \
                                         + acodec_flac_lpc_passes_choices[acodec_flac_lpc_passes.get()] \
                                         + flac_custom_cmd_input
                    try:
                        cmd_label.config(text=example_cmd_output)
                        cmd_line_window.deiconify()
                    except (AttributeError, NameError):
                        cmd_line_window = Toplevel()
                        cmd_line_window.title('Command Line')
                        cmd_line_window.configure(background="#434547")
                        cmd_label = Label(cmd_line_window, text=example_cmd_output, foreground="white",
                                          background="#434547")
                        cmd_label.config(font=("Helvetica", 16))
                        cmd_label.pack()

                        def hide_instead():
                            cmd_line_window.withdraw()

                        cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

                # --------------------------------------------------------------------------------------- Views Command

                # Buttons ---------------------------------------------------------------------------------------------
                apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A",
                                      command=gotosavefile)
                apply_button.grid(row=10, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
                apply_button.bind("<Enter>", apply_button_hover)
                apply_button.bind("<Leave>", apply_button_hover_leave)

                show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A",
                                  command=view_command)
                show_cmd.grid(row=10, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
                show_cmd.bind("<Enter>", show_cmd_hover)
                show_cmd.bind("<Leave>", show_cmd_hover_leave)
                # --------------------------------------------------------------------------------------------- Buttons

                advanced_label = Label(audio_window,
                                       text="- - - - - - - - - - - - - - - - - - - - Advanced Settings - - - - - "
                                            "- - - - - - - - - - - - - - -",
                                       background="#434547", foreground="white", relief=GROOVE)
                advanced_label.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky=W + E)

                # Audio Bitrate Selection -----------------------------------------------------------------------------
                acodec_bitrate = StringVar(audio_window)
                acodec_bitrate_choices = {'Level 0 - Best Quality': "-compression_level 0 ",
                                          'Level 1 ......': "-compression_level 1 ",
                                          'Level 2 ......': "-compression_level 2 ",
                                          'Level 3 ......': "-compression_level 3 ",
                                          'Level 4 ......': "-compression_level 4 ",
                                          'Level 5 - Default Quality': "",
                                          'Level 6 ......': "-compression_level 6 ",
                                          'Level 7 ......': "-compression_level 7 ",
                                          'Level 8 ......': "-compression_level 8 ",
                                          'Level 9 ......': "-compression_level 9 ",
                                          'Level 10 ......': "-compression_level 10 ",
                                          'Level 11 ......': "-compression_level 11 ",
                                          'Level 12 - Lowest Quality': "-compression_level 12 "}
                acodec_bitrate.set('Level 5 - Default Quality')  # set the default option
                acodec_bitrate_menu_label = Label(audio_window, text="Compression Level :", background="#434547",
                                                  foreground="white")
                acodec_bitrate_menu_label.grid(row=0, column=2, columnspan=1, padx=10, pady=3, sticky=W + E)
                acodec_bitrate_menu = OptionMenu(audio_window, acodec_bitrate, *acodec_bitrate_choices.keys())
                acodec_bitrate_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=15)
                acodec_bitrate_menu.grid(row=1, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
                acodec_bitrate_menu["menu"].configure(activebackground="dim grey")
                acodec_bitrate_menu.bind("<Enter>", acodec_bitrate_menu_hover)
                acodec_bitrate_menu.bind("<Leave>", acodec_bitrate_menu_hover_leave)
                # --------------------------------------------------------------------------------------- Audio Bitrate

                # Audio Stream Selection ------------------------------------------------------------------------------
                acodec_stream = StringVar(audio_window)
                acodec_stream_choices = acodec_stream_batch_choices
                acodec_stream.set('Track 1')
                acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
                acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
                acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
                acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=15)
                acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
                acodec_stream_menu["menu"].configure(activebackground="dim grey")
                acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
                acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)
                # -----------------------------------------------------------------------------------------------------

                # Audio Channel Selection -----------------------------------------------------------------------------
                acodec_channel = StringVar(audio_window)
                acodec_channel_choices = {'Original': "",
                                          '1 (Mono)': "-ac 1 ",
                                          '2 (Stereo)': "-ac 2 ",
                                          '5.0 (Surround)': "-ac 5 ",
                                          '5.1 (Surround)': "-ac 6 ",
                                          '6.1 (Surround)': "-ac 7 ",
                                          '7.1 (Surround)': "-ac 8 "}
                acodec_channel.set('Original')  # set the default option
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
                dolby_pro_logic_ii_checkbox.grid(row=4, column=2, columnspan=1, rowspan=1, padx=10, pady=(20, 5),
                                                 sticky=N + S + E + W)
                dolby_pro_logic_ii_checkbox.configure(background="#434547", foreground="white",
                                                      activebackground="#434547",
                                                      activeforeground="white", selectcolor="#434547",
                                                      font=("Helvetica", 11))
                dolby_pro_logic_ii.set("")
                # ---------------------------------------------------------------------------------------------- DPL II

                # Audio Gain Selection --------------------------------------------------------------------------------
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
                ffmpeg_gain.set(0)
                # ------------------------------------------------------------------------------------------------ Gain

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
                acodec_samplerate.set('Original')  # set the default option
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
                    if flac_custom_cmd.get() == (""):
                        flac_custom_cmd_input = ("")
                    else:
                        cstmcmd = flac_custom_cmd.get()
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
                acodec_atempo.set('Original')
                acodec_atempo_menu["menu"].configure(activebackground="dim grey")
                acodec_atempo_menu.bind("<Enter>", acodec_atempo_menu_hover)
                acodec_atempo_menu.bind("<Leave>", acodec_atempo_menu_hover_leave)
            # -------------------------------------------------------------------------------------------- Audio Atempo

            # LPC Algorithm Selection ---------------------------------------------------------------------------------
            global acodec_flac_lpc_type, acodec_flac_lpc_type_choices
            acodec_flac_lpc_type = StringVar(audio_window)
            acodec_flac_lpc_type_choices = {'Default': "",
                                            'None': "-lpc_type 0 ",
                                            'Fixed': "-lpc_type 1 ",
                                            'Levinson': "-lpc_type 2 ",
                                            'Cholesky': "-lpc_type 3 "}
            acodec_flac_lpc_type.set('Default')  # set the default option
            acodec_flac_lpc_type_label = Label(audio_window, text="LPC Algorithm :", background="#434547",
                                               foreground="white")
            acodec_flac_lpc_type_label.grid(row=6, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_flac_lpc_type_menu = OptionMenu(audio_window, acodec_flac_lpc_type,
                                                   *acodec_flac_lpc_type_choices.keys())
            acodec_flac_lpc_type_menu.config(background="#23272A", foreground="white", highlightthickness=1,
                                             width=15)
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
            flac_acodec_coefficient_spinbox.grid(row=7, column=1, columnspan=1, padx=10, pady=3,
                                                 sticky=N + S + E + W)
            flac_acodec_coefficient.trace('w', flac_acodec_coefficient_trace)
            flac_acodec_coefficient.set(15)
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
            acodec_flac_lpc_passes.set('Default')
            acodec_flac_lpc_passes_label = Label(audio_window, text="LPC Passes :", background="#434547",
                                                 foreground="white")
            acodec_flac_lpc_passes_label.grid(row=6, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            acodec_flac_lpc_passes_menu = OptionMenu(audio_window, acodec_flac_lpc_passes,
                                                     *acodec_flac_lpc_passes_choices.keys())
            acodec_flac_lpc_passes_menu.config(background="#23272A", foreground="white", highlightthickness=1,
                                               width=15)
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
            except:
                audio_window = Toplevel()
                audio_window.title('ALAC Settings')
                audio_window.configure(background="#434547")
                window_height = 470
                window_width = 650
                screen_width = audio_window.winfo_screenwidth()
                screen_height = audio_window.winfo_screenheight()
                x_cordinate = int((screen_width / 2) - (window_width / 2))
                y_cordinate = int((screen_height / 2) - (window_height / 2))
                audio_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

                audio_window.grid_columnconfigure(0, weight=1)
                audio_window.grid_columnconfigure(1, weight=1)
                audio_window.grid_columnconfigure(2, weight=1)
                audio_window.grid_rowconfigure(0, weight=1)
                audio_window.grid_rowconfigure(1, weight=1)
                audio_window.grid_rowconfigure(2, weight=1)
                audio_window.grid_rowconfigure(3, weight=1)
                audio_window.grid_rowconfigure(5, weight=1)
                audio_window.grid_rowconfigure(6, weight=1)
                audio_window.grid_rowconfigure(10, weight=1)

                # Views Command ---------------------------------------------------------------------------------------
                def view_command():
                    global cmd_line_window
                    global cmd_label
                    audio_filter_function()
                    example_cmd_output = acodec_stream_choices[acodec_stream.get()] \
                                         + encoder_dropdownmenu_choices[encoder.get()] + \
                                         acodec_channel_choices[acodec_channel.get()] + \
                                         acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting \
                                         + min_pre_order + max_pre_order + flac_custom_cmd_input
                    try:
                        cmd_label.config(text=example_cmd_output)
                        cmd_line_window.deiconify()
                    except (AttributeError, NameError):
                        cmd_line_window = Toplevel()
                        cmd_line_window.title('Command Line')
                        cmd_line_window.configure(background="#434547")
                        cmd_label = Label(cmd_line_window, text=example_cmd_output, foreground="white",
                                          background="#434547")
                        cmd_label.config(font=("Helvetica", 16))
                        cmd_label.pack()

                        def hide_instead():
                            cmd_line_window.withdraw()

                        cmd_line_window.protocol('WM_DELETE_WINDOW', hide_instead)

                # --------------------------------------------------------------------------------------- Views Command

                # Buttons ---------------------------------------------------------------------------------------------
                apply_button = Button(audio_window, text="Apply", foreground="white", background="#23272A",
                                      command=gotosavefile)
                apply_button.grid(row=10, column=2, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
                apply_button.bind("<Enter>", apply_button_hover)
                apply_button.bind("<Leave>", apply_button_hover_leave)

                show_cmd = Button(audio_window, text="View Command", foreground="white", background="#23272A",
                                  command=view_command)
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
                acodec_stream_choices = acodec_stream_batch_choices
                acodec_stream.set('Track 1')
                acodec_stream_label = Label(audio_window, text="Track :", background="#434547", foreground="white")
                acodec_stream_label.grid(row=0, column=0, columnspan=1, padx=10, pady=3, sticky=W + E)
                acodec_stream_menu = OptionMenu(audio_window, acodec_stream, *acodec_stream_choices.keys())
                acodec_stream_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=15)
                acodec_stream_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=3, sticky=N + S + W + E)
                acodec_stream_menu["menu"].configure(activebackground="dim grey")
                acodec_stream_menu.bind("<Enter>", acodec_stream_menu_hover)
                acodec_stream_menu.bind("<Leave>", acodec_stream_menu_hover_leave)
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
                acodec_channel.set('Original')  # set the default option
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
                dolby_pro_logic_ii_checkbox.grid(row=0, column=2, columnspan=1, rowspan=2, padx=10, pady=(20, 5),
                                                 sticky=N + S + E + W)
                dolby_pro_logic_ii_checkbox.configure(background="#434547", foreground="white",
                                                      activebackground="#434547",
                                                      activeforeground="white", selectcolor="#434547",
                                                      font=("Helvetica", 11))
                dolby_pro_logic_ii.set("")
                # ---------------------------------------------------------------------------------------------- DPL II

                # Audio Gain Selection --------------------------------------------------------------------------------
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
                ffmpeg_gain.set(0)
                # ------------------------------------------------------------------------------------------------ Gain

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
                acodec_samplerate.set('Original')  # set the default option
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
                    if flac_custom_cmd.get() == (""):
                        flac_custom_cmd_input = ("")
                    else:
                        cstmcmd = flac_custom_cmd.get()
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
                acodec_atempo.set('Original')
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
            min_prediction_order.set(4)
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
            max_prediction_order.set(6)
            max_prediction_order_spinbox.config(background="#23272A", foreground="white", highlightthickness=1,
                                                buttonbackground="black", disabledbackground='grey')
            max_prediction_order_spinbox.grid(row=6, column=1, columnspan=1, padx=10, pady=3, sticky=N + S + E + W)
            # ------------------------------------------------------------------------------------ Max-Prediction-Order

        # -------------------------------------------------------------------------------------------------------- ALAC

    # ------------------------------------------------------------------------------------------ End Audio Codec Window

    def audiosettings_button_batch_hover(e):
        audiosettings_button_batch["bg"] = "grey"

    def audiosettings_button_batch_hover_leave(e):
        audiosettings_button_batch["bg"] = "#23272A"

    audiosettings_button_batch = Button(batch_processing_window, text="Audio Settings", command=openaudiowindow2,
                                  foreground="white", background="#23272A", borderwidth="3", state=DISABLED)
    audiosettings_button_batch.grid(row=1, column=3, columnspan=1, padx=5, pady=5, sticky=N + S + W + E)
    audiosettings_button_batch.bind("<Enter>", audiosettings_button_batch_hover)
    audiosettings_button_batch.bind("<Leave>", audiosettings_button_batch_hover_leave)


    def open_directory():
        global batch_input_directory, batch_input_directory_quoted, batch_save_directory
        batch_input_directory = filedialog.askdirectory(parent=batch_processing_window,
                                                        title='Select Directory To Batch Encode', initialdir='/')
        batch_input_directory_quoted = '"' + batch_input_directory + '"'
        batch_input_entry.configure(state=NORMAL)
        batch_input_entry.delete(0, END)
        try:
            del batch_save_directory
        except:
            pass
        if batch_input_directory:
            autofilesave_batch_path_output_entry_box = pathlib.Path('"' + batch_input_directory + '/Encoded"')
            encoder_menu.config(state=NORMAL)
            batch_input_entry.configure(state=NORMAL)
            batch_input_entry.insert(0, '"' + batch_input_directory + '"')
            batch_input_entry.configure(state=DISABLED)
            batch_output_entry.configure(state=NORMAL)
            batch_output_entry.delete(0, END)
            batch_output_entry.insert(0, autofilesave_batch_path_output_entry_box)
            batch_output_entry.configure(state=DISABLED)
            encoder_menu.config(state=NORMAL)
        if not batch_input_directory:
            batch_input_entry.configure(state=NORMAL)
            batch_input_entry.delete(0, END)
            batch_input_entry.configure(state=DISABLED)
            batch_output_entry.configure(state=NORMAL)
            batch_output_entry.delete(0, END)
            batch_output_entry.configure(state=DISABLED)
            encoder_menu.config(state=NORMAL)
            encoder.set('Set Codec')
            encoder_menu.config(state=DISABLED)
            audiosettings_button_batch.configure(state=DISABLED)
            start_audio_button_batch.config(state=DISABLED)
            command_line_button_batch.config(state=DISABLED)
            save_batch_dir.config(state=DISABLED)

    def save_directory():
        global batch_save_directory
        batch_save_directory = filedialog.askdirectory(parent=batch_processing_window,
                                                       title='Select Directory To Save Batch Encodes',
                                                       initialdir="/")
        if save_directory:
            batch_output_entry.configure(state=NORMAL)
            batch_output_entry.delete(0, END)
            batch_output_entry.insert(0, '"' + batch_save_directory + '"')
            batch_output_entry.configure(state=DISABLED)
        if not batch_save_directory:
            batch_save_directory = str(input_dnd_batch.get() + '/Encoded').replace("{", "").replace("}", "")
            batch_output_entry.configure(state=NORMAL)
            batch_output_entry.delete(0, END)
            batch_output_entry.insert(0, '"' + batch_save_directory + '"')
            batch_output_entry.configure(state=DISABLED)

    def drop_input_batch(event):
        global batch_input_directory_quoted, batch_save_directory, batch_input_directory
        input_dnd_batch.set(event.data)
        batch_input_directory = str(input_dnd_batch.get()).replace("{", "").replace("}", "")
        batch_input_directory_quoted = '"' + batch_input_directory + '"'
        batch_input_entry.configure(state=NORMAL)
        batch_input_entry.delete(0, END)
        encoder.set("Set Codec")
        try:
            del batch_save_directory
        except:
            pass
        batch_save_directory = str(input_dnd_batch.get() + '/Encoded').replace("{", "").replace("}", "")
        if batch_input_directory:
            autofilesave_batch_path_output_entry_box = pathlib.Path('"' + batch_input_directory + '/Encoded"')
            encoder_menu.config(state=NORMAL)
            batch_input_entry.configure(state=NORMAL)
            batch_input_entry.insert(0, '"' + batch_input_directory + '"')
            batch_input_entry.configure(state=DISABLED)
            batch_output_entry.configure(state=NORMAL)
            batch_output_entry.delete(0, END)
            batch_output_entry.insert(0, autofilesave_batch_path_output_entry_box)
            batch_output_entry.configure(state=DISABLED)
            encoder_menu.config(state=NORMAL)
        if not batch_input_directory:
            batch_input_entry.configure(state=NORMAL)
            batch_input_entry.delete(0, END)
            batch_input_entry.configure(state=DISABLED)
            batch_output_entry.configure(state=NORMAL)
            batch_output_entry.delete(0, END)
            batch_output_entry.configure(state=DISABLED)
            encoder_menu.config(state=NORMAL)
            encoder.set('Set Codec')
            encoder_menu.config(state=DISABLED)
            audiosettings_button_batch.configure(state=DISABLED)
            start_audio_button_batch.config(state=DISABLED)
            command_line_button_batch.config(state=DISABLED)
            save_batch_dir.config(state=DISABLED)


    input_dnd_batch = StringVar()
    open_batch_dir = Button(batch_processing_window, text="Open\nDirectory", command=open_directory,
                                          foreground="white", background="#23272A", borderwidth="3")
    open_batch_dir.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)
    open_batch_dir.bind("<Enter>", open_batch_dir_hover)
    open_batch_dir.bind("<Leave>", open_batch_dir_hover_leave)
    open_batch_dir.drop_target_register(DND_FILES)
    open_batch_dir.dnd_bind('<<Drop>>', drop_input_batch)

    batch_input_entry = Entry(batch_processing_window, width=50, borderwidth=4, background="#CACACA")
    batch_input_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=(5,15), sticky=S + E + W)
    batch_input_entry.drop_target_register(DND_FILES)
    batch_input_entry.dnd_bind('<<Drop>>', drop_input_batch)

    batch_output_entry = Entry(batch_processing_window, width=50, borderwidth=4, background="#CACACA")
    batch_output_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=(5,15), sticky=S + E + W)

    save_batch_dir = Button(batch_processing_window, text="Save\nDirectory", command=save_directory,
                                          foreground="white", background="#23272A", borderwidth="3", state=DISABLED)
    save_batch_dir.grid(row=2, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)
    save_batch_dir.bind("<Enter>", save_batch_dir_hover)
    save_batch_dir.bind("<Leave>", save_batch_dir_hover_leave)

    # Start Batch Job -------------------------------------------------------------------------------------------------
    def startbatchaudiojob():
        global automatic_batch_save_dir, automatic_batch_save_dir_quoted, ac3_batch_job, aac_batch_job, \
            dts_batch_job, opus_batch_job, mp3_batch_job, eac3_batch_job, fdkaac_batch_job, qaac_batch_job, \
            flac_batch_job, alac_batch_job
        try:
            automatic_batch_save_dir = batch_save_directory
        except:
            automatic_batch_save_dir = batch_input_directory + '/Encoded'
        audio_filter_function()

        ac3_batch_job = StringVar()
        aac_batch_job = StringVar()
        dts_batch_job = StringVar()
        opus_batch_job = StringVar()
        mp3_batch_job = StringVar()
        eac3_batch_job = StringVar()
        fdkaac_batch_job = StringVar()
        qaac_batch_job = StringVar()
        flac_batch_job = StringVar()
        alac_batch_job = StringVar()

        def close_encode():
            confirm_exit = messagebox.askyesno(title='Prompt',
                                               message="Are you sure you want to stop the encode?", parent=window)
            if confirm_exit == False:
                pass
            elif confirm_exit == True:
                global example_cmd_output
                ac3_batch_job.set('')
                aac_batch_job.set('')
                dts_batch_job.set('')
                opus_batch_job.set('')
                mp3_batch_job.set('')
                eac3_batch_job.set('')
                fdkaac_batch_job.set('')
                qaac_batch_job.set('')
                flac_batch_job.set('')
                alac_batch_job.set('')
                try:
                    subprocess.Popen(f"TASKKILL /F /PID {job.pid} /T", creationflags=subprocess.CREATE_NO_WINDOW)
                    if ac3_batch_job.get() == '' and aac_batch_job.get() == '' and dts_batch_job.get() == '' and opus_batch_job.get() \
                            == '' and mp3_batch_job.get() == '' and eac3_batch_job.get() == '' and fdkaac_batch_job.get() == '' \
                            and qaac_batch_job.get() == '' and flac_batch_job.get() == '' and alac_batch_job.get() == '':
                        batch_processing_window.deiconify()
                    elif ac3_batch_job.get() != '' or aac_batch_job.get() != '' or dts_batch_job.get() != '' or opus_batch_job.get() \
                            != '' or mp3_batch_job.get() != '' or eac3_batch_job.get() != '' or fdkaac_batch_job.get() != '' \
                            or qaac_batch_job.get() != '' or flac_batch_job.get() != '' or alac_batch_job.get() != '':
                        window.destroy()
                except NameError:
                    window.destroy()


        def close_window():
            thread = threading.Thread(target=close_encode)
            thread.start()

        window = Toplevel(batch_processing_window)
        window.title('Codec : ' + encoder.get() + '  |  ' + str(pathlib.Path(batch_save_directory)))
        window.configure(background="#434547")
        encode_label = Label(window, text="- - - - - - - - - - - - - - - - - - - - - - Progress - - "
                                          "- - - - - - - - - - - - - - - - - - - -",
                             font=("Times New Roman", 14), background='#434547', foreground="white")
        encode_label.grid(column=0, row=0)
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=1)
        window.protocol('WM_DELETE_WINDOW', close_window)
        encode_window_progress = Text(window, width=70, height=2, relief=SUNKEN, bd=3)
        encode_window_progress.grid(row=1, column=0, pady=(10, 10), padx=10)
        encode_window_progress.insert(END, '')


        # AC3 Start Job -----------------------------------------------------------------------------------------------
        if encoder.get() == "AC3":
            ac3_batch_job.set('Working')
            finalcommand = '"' + 'cd /d ' + batch_input_directory_quoted + ' & md ' + '"' \
                           + automatic_batch_save_dir + '"' \
                           +' & for %a in ' + extension_dropdownmenu_choices[extension.get()] + ' do ' + \
                           '"' + ffmpeg + '"' \
                           + ' -y -analyzeduration 100M -probesize 50M -i "%a" ' \
                           + acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] \
                           + acodec_bitrate_choices[acodec_bitrate.get()] + \
                           acodec_channel_choices[acodec_channel.get()] + \
                           acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting \
                           + ac3_custom_cmd_input + "-sn -vn -map_chapters -1 -map_metadata -1 " + \
                           '"' + automatic_batch_save_dir + '/%~na.ac3"' + " -hide_banner"
            if shell_options.get() == "Default":
                job = subprocess.Popen('cmd /c ' + finalcommand + " " + '-v error -stats"', universal_newlines=True,
                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                       creationflags=subprocess.CREATE_NO_WINDOW)
                for line in job.stdout:
                    encode_window_progress.delete('1.0', END)
                    encode_window_progress.insert(END, line)
                    ac3_batch_job.set('Working')
                window.destroy()
            elif shell_options.get() == "Debug":
                subprocess.Popen('cmd /k ' + finalcommand + '"')
            ac3_batch_job.set('')
        # ----------------------------------------------------------------------------------------------------- AC3 Job
        # AAC Start Job -----------------------------------------------------------------------------------------------
        elif encoder.get() == "AAC":
            aac_batch_job.set('Working')
            if aac_vbr_toggle.get() == "-c:a ":
                bitrate_or_quality = f"-b:a {aac_bitrate_spinbox.get()}k "
            elif aac_vbr_toggle.get() == "-q:a ":
                bitrate_or_quality = f"-q:a {aac_quality_spinbox.get()} "
            finalcommand = '"' + 'cd /d ' + batch_input_directory_quoted + ' & md ' + '"' \
                           + automatic_batch_save_dir + '"' \
                           +' & for %a in ' + extension_dropdownmenu_choices[extension.get()] + ' do ' + \
                           '"' + ffmpeg + '"' \
                           + ' -y -analyzeduration 100M -probesize 50M -i "%a" ' \
                           + acodec_stream_choices[acodec_stream.get()] + \
                           encoder_dropdownmenu_choices[encoder.get()] + bitrate_or_quality + \
                           acodec_channel_choices[acodec_channel.get()] + \
                           acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting \
                           + aac_custom_cmd_input + "-sn -vn -map_chapters -1 -map_metadata -1 " \
                           + '"' + automatic_batch_save_dir + '/%~na.mp4"' + " -hide_banner"
            if shell_options.get() == "Default":
                job = subprocess.Popen('cmd /c ' + finalcommand + " " + '-v error -stats"', stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, universal_newlines=True,
                                       creationflags=subprocess.CREATE_NO_WINDOW)
                for line in job.stdout:
                    encode_window_progress.delete('1.0', END)
                    encode_window_progress.insert(END, line)
                    aac_batch_job.set('Working')
                window.destroy()
            elif shell_options.get() == "Debug":
                subprocess.Popen('cmd /k ' + finalcommand + '"')
            aac_batch_job.set('')
                # --------------------------------------------------------------------------------------------- AAC Job
        # DTS Start Job -----------------------------------------------------------------------------------------------
        elif encoder.get() == 'DTS':
            dts_batch_job.set('Working')
            if dts_settings.get() == 'DTS Encoder':
                finalcommand = '"' + 'cd /d ' + batch_input_directory_quoted + ' & md ' + '"' \
                               + automatic_batch_save_dir + '"' \
                               +' & for %a in ' + extension_dropdownmenu_choices[extension.get()] + ' do ' + \
                               '"' + ffmpeg + '"' \
                               + ' -y -analyzeduration 100M -probesize 50M -i "%a" ' \
                               + acodec_stream_choices[acodec_stream.get()] + dts_settings_choices[dts_settings.get()] \
                               + "-b:a " + dts_bitrate_spinbox.get() + "k " \
                               + acodec_channel_choices[acodec_channel.get()] \
                               + acodec_samplerate_choices[acodec_samplerate.get()] \
                               + audio_filter_setting + dts_custom_cmd_input \
                               + "-sn -vn -map_chapters -1 " \
                               + '"' + automatic_batch_save_dir + '/%~na.dts"' + " -hide_banner"
            else:
                finalcommand = '"' + 'cd /d ' + batch_input_directory_quoted + ' & md ' + '"' \
                               + automatic_batch_save_dir + '"' \
                               +' & for %a in ' + extension_dropdownmenu_choices[extension.get()] + ' do ' + \
                               '"' + ffmpeg + '"' \
                               + ' -y -analyzeduration 100M -probesize 50M -i "%a" ' \
                               + acodec_stream_choices[acodec_stream.get()] + dts_settings_choices[dts_settings.get()] \
                               + dts_custom_cmd_input + "-sn -vn -map_chapters -1 " \
                               + '"' + automatic_batch_save_dir + '/%~na.dts"' + " -hide_banner"
            if shell_options.get() == "Default":
                job = subprocess.Popen('cmd /c ' + finalcommand + " " + '-v error -stats"', stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, universal_newlines=True,
                                       creationflags=subprocess.CREATE_NO_WINDOW)
                for line in job.stdout:
                    encode_window_progress.delete('1.0', END)
                    encode_window_progress.insert(END, line)
                    dts_batch_job.set('Working')
                window.destroy()
            elif shell_options.get() == "Debug":
                subprocess.Popen('cmd /k ' + finalcommand + '"')
            dts_batch_job.set('')
        # --------------------------------------------------------------------------------------------------------- DTS
        # Opus Start Job ----------------------------------------------------------------------------------------------
        elif encoder.get() == "Opus":
            opus_batch_job.set('Working')
            finalcommand = '"' + 'cd /d ' + batch_input_directory_quoted + ' & md ' + '"' \
                           + automatic_batch_save_dir + '"' \
                           +' & for %a in ' + extension_dropdownmenu_choices[extension.get()] + ' do ' + \
                           '"' + ffmpeg + '"' \
                           + ' -y -analyzeduration 100M -probesize 50M -i "%a" ' \
                           + acodec_stream_choices[acodec_stream.get()] + \
                           encoder_dropdownmenu_choices[encoder.get()] + \
                           acodec_vbr_choices[acodec_vbr.get()] + acodec_bitrate_choices[acodec_bitrate.get()] + \
                           acodec_channel_choices[acodec_channel.get()] + \
                           acodec_application_choices[acodec_application.get()] + "-packet_loss " + \
                           packet_loss.get() + " -frame_duration " + frame_duration.get() + " " + \
                           acodec_samplerate_choices[acodec_samplerate.get()] + \
                           audio_filter_setting + opus_custom_cmd_input + "-sn -vn -map_chapters -1 -map_metadata -1 " \
                           + '"' + automatic_batch_save_dir + '/%~na.opus"' \
                           + " -hide_banner"
            if shell_options.get() == "Default":
                job = subprocess.Popen('cmd /c ' + finalcommand + " " + '-v error -stats"', stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, universal_newlines=True,
                                       creationflags=subprocess.CREATE_NO_WINDOW)
                for line in job.stdout:
                    encode_window_progress.delete('1.0', END)
                    encode_window_progress.insert(END, line)
                    opus_batch_job.set('Working')
                window.destroy()
            elif shell_options.get() == "Debug":
                subprocess.Popen('cmd /k ' + finalcommand + '"')
            opus_batch_job.set('')
        # -------------------------------------------------------------------------------------------------------- Opus
        # MP3 Start Job -----------------------------------------------------------------------------------------------
        elif encoder.get() == "MP3":
            mp3_batch_job.set('Working')
            finalcommand = '"' + 'cd /d ' + batch_input_directory_quoted + ' & md ' + '"' \
                           + automatic_batch_save_dir + '"' \
                           +' & for %a in ' + extension_dropdownmenu_choices[extension.get()] + ' do ' + \
                           '"' + ffmpeg + '"' \
                           + ' -y -analyzeduration 100M -probesize 50M -i "%a" ' \
                           + acodec_stream_choices[acodec_stream.get()] \
                           + encoder_dropdownmenu_choices[encoder.get()] + \
                           acodec_bitrate_choices[acodec_bitrate.get()] \
                           + acodec_channel_choices[acodec_channel.get()] \
                           + mp3_abr.get() + acodec_samplerate_choices[acodec_samplerate.get()] \
                           + audio_filter_setting + mp3_custom_cmd_input \
                           + "-sn -vn -map_chapters -1 -map_metadata -1 " + '"' \
                           + automatic_batch_save_dir + '/%~na.mp3"' \
                           + " -hide_banner"
            if shell_options.get() == "Default":
                job = subprocess.Popen('cmd /c ' + finalcommand + " " + '-v error -stats"', stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, universal_newlines=True,
                                       creationflags=subprocess.CREATE_NO_WINDOW)
                for line in job.stdout:
                    encode_window_progress.delete('1.0', END)
                    encode_window_progress.insert(END, line)
                    mp3_batch_job.set('Working')
                window.destroy()
            elif shell_options.get() == "Debug":
                subprocess.Popen('cmd /k ' + finalcommand + '"')
            mp3_batch_job.set('')
        # --------------------------------------------------------------------------------------------------------- MP3
        # E-AC3 Start Job ---------------------------------------------------------------------------------------------
        elif encoder.get() == "E-AC3":
            eac3_batch_job.set('Working')
            finalcommand = '"' + 'cd /d ' + batch_input_directory_quoted + ' & md ' + '"' \
                           + automatic_batch_save_dir + '"' \
                           +' & for %a in ' + extension_dropdownmenu_choices[extension.get()] + ' do ' + \
                           '"' + ffmpeg + '"' \
                           + ' -y -analyzeduration 100M -probesize 50M -i "%a" ' \
                           + acodec_stream_choices[acodec_stream.get()] + encoder_dropdownmenu_choices[encoder.get()] \
                           + "-b:a " + eac3_spinbox.get() + acodec_channel_choices[acodec_channel.get()] \
                           + acodec_samplerate_choices[acodec_samplerate.get()] \
                           + audio_filter_setting + eac3_custom_cmd_input \
                           + "-sn -vn -map_chapters -1 -map_metadata -1 " \
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
                           + "-cpl_start_band " + cpl_start_band.get() + " " + '"' + automatic_batch_save_dir \
                           + '/%~na.ac3"' + " -hide_banner"
            if shell_options.get() == "Default":
                job = subprocess.Popen('cmd /c ' + finalcommand + " " + '-v error -stats"', stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, universal_newlines=True,
                                       creationflags=subprocess.CREATE_NO_WINDOW)
                for line in job.stdout:
                    encode_window_progress.delete('1.0', END)
                    encode_window_progress.insert(END, line)
                    eac3_batch_job.set('Working')
                window.destroy()
            elif shell_options.get() == "Debug":
                subprocess.Popen('cmd /k ' + finalcommand + '"')
            eac3_batch_job.set('')
        # ------------------------------------------------------------------------------------------------------- E-AC3
        # FDK_AAC Start Job -------------------------------------------------------------------------------------------
        elif encoder.get() == "FDK-AAC":
            fdkaac_batch_job.set('Working')
            finalcommand = '"' + 'cd /d ' + batch_input_directory_quoted + ' & md ' + '"' \
                           + automatic_batch_save_dir + '"' \
                           +' & for %a in ' + extension_dropdownmenu_choices[extension.get()] + ' do ' + \
                           '"' + ffmpeg + '"' \
                           + ' -y -analyzeduration 100M -probesize 50M -i "%a" ' \
                           + acodec_stream_choices[acodec_stream.get()] \
                           + acodec_channel_choices[acodec_channel.get()] + \
                           acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting + \
                           "-f caf - | " + '"' + f"{pathlib.Path.cwd()}{'/Apps/fdkaac/fdkaac.exe'}" + '"' + " " + \
                           acodec_profile_choices[acodec_profile.get()] + \
                           fdkaac_title_input + fdkaac_custom_cmd_input + \
                           afterburnervar.get() + crccheck.get() + moovbox.get() \
                           + sbrdelay.get() + headerperiod.get() + \
                           acodec_lowdelay_choices[acodec_lowdelay.get()] + \
                           acodec_sbr_ratio_choices[acodec_sbr_ratio.get()] + \
                           acodec_transport_format_choices[acodec_transport_format.get()] + \
                           acodec_bitrate_choices[acodec_bitrate.get()] + "- -o " + '"' + automatic_batch_save_dir \
                           + '/%~na.m4a"' + '"'
            if shell_options.get() == "Default":
                job = subprocess.Popen('cmd /c ' + finalcommand, stdout=subprocess.PIPE, stdin=subprocess.DEVNULL,
                                       stderr=subprocess.STDOUT, universal_newlines=True,
                                       creationflags=subprocess.CREATE_NO_WINDOW)
                for line in job.stdout:
                    encode_window_progress.delete('1.0', END)
                    encode_window_progress.insert(END, line)
                    fdkaac_batch_job.set('Working')
                window.destroy()
            elif shell_options.get() == "Debug":
                subprocess.Popen('cmd /k ' + finalcommand)
            fdkaac_batch_job.set('')
        # --------------------------------------------------------------------------------------------------------- FDK
        # QAAC Start Job ----------------------------------------------------------------------------------------------
        elif encoder.get() == "QAAC":
            qaac_batch_job.set('Working')
            if q_acodec_profile.get() == "True VBR":
                finalcommand = '"' + 'cd /d ' + batch_input_directory_quoted + ' & md ' + '"' \
                               + automatic_batch_save_dir + '"' \
                               +' & for %a in ' + extension_dropdownmenu_choices[extension.get()] + ' do ' + \
                               '"' + ffmpeg + '"' \
                               + ' -y -analyzeduration 100M -probesize 50M -i "%a" ' \
                               + acodec_stream_choices[acodec_stream.get()] \
                               + acodec_channel_choices[acodec_channel.get()] + audio_filter_setting \
                               + acodec_samplerate_choices[acodec_samplerate.get()] \
                               + "-f wav - | " + '"' + f"{pathlib.Path.cwd()}{'/Apps/qaac/qaac64.exe'}" + '"' + " " \
                               + q_acodec_profile_choices[q_acodec_profile.get()] \
                               + q_acodec_quality_amnt.get() + " " + qaac_high_efficiency.get() \
                               + qaac_normalize.get() + qaac_nodither.get() + "--gain " \
                               + q_acodec_gain.get() + " " + q_acodec_quality_choices[q_acodec_quality.get()] \
                               + qaac_nodelay.get() \
                               + q_gapless_mode_choices[q_gapless_mode.get()] + qaac_nooptimize.get() \
                               + qaac_threading.get() + qaac_limiter.get() + qaac_title_input + qaac_custom_cmd_input \
                               + "- -o " + '"' + automatic_batch_save_dir + '/%~na.m4a"' + '"'
            else:
                finalcommand = '"' + 'cd /d ' + batch_input_directory_quoted + ' & md ' + '"' \
                               + automatic_batch_save_dir + '"' \
                               +' & for %a in ' + extension_dropdownmenu_choices[extension.get()] + ' do ' + \
                               '"' + ffmpeg + '"' \
                               + ' -y -analyzeduration 100M -probesize 50M -i "%a" ' \
                               + acodec_stream_choices[acodec_stream.get()] + \
                               acodec_channel_choices[acodec_channel.get()] + audio_filter_setting + \
                               acodec_samplerate_choices[acodec_samplerate.get()] \
                               + "-f wav - | " + '"' + f"{pathlib.Path.cwd()}{'/Apps/qaac/qaac64.exe'}" + '"' + " " \
                               + q_acodec_profile_choices[q_acodec_profile.get()] + \
                               q_acodec_bitrate.get() + " " + qaac_high_efficiency.get() + qaac_normalize.get() \
                               + qaac_nodither.get() + "--gain " + q_acodec_gain.get() + " " \
                               + q_acodec_quality_choices[q_acodec_quality.get()] + qaac_nodelay.get() \
                               + q_gapless_mode_choices[q_gapless_mode.get()] + qaac_nooptimize.get() \
                               + qaac_threading.get() + qaac_limiter.get() + qaac_title_input \
                               + qaac_custom_cmd_input + "- -o " + '"' + automatic_batch_save_dir + '/%~na.m4a"' + '"'
            if shell_options.get() == "Default":
                job = subprocess.Popen('cmd /c ' + finalcommand, stdout=subprocess.PIPE, stdin=subprocess.DEVNULL,
                                       stderr=subprocess.STDOUT, universal_newlines=True,
                                       creationflags=subprocess.CREATE_NO_WINDOW)
                for line in job.stdout:
                    encode_window_progress.delete('1.0', END)
                    encode_window_progress.insert(END, line)
                    qaac_batch_job.set('Working')
                window.destroy()
            elif shell_options.get() == "Debug":
                subprocess.Popen('cmd /k ' + finalcommand)
            qaac_batch_job.set('')
        # -------------------------------------------------------------------------------------------------------- QAAC
        # FLAC Start Job ----------------------------------------------------------------------------------------------
        if encoder.get() == "FLAC":
            flac_batch_job.set('Working')
            finalcommand = '"' + 'cd /d ' + batch_input_directory_quoted + ' & md ' + '"' \
                           + automatic_batch_save_dir + '"' \
                           +' & for %a in ' + extension_dropdownmenu_choices[extension.get()] + ' do ' + \
                           '"' + ffmpeg + '"' \
                           + ' -y -analyzeduration 100M -probesize 50M -i "%a" ' \
                           + acodec_stream_choices[acodec_stream.get()] \
                           + encoder_dropdownmenu_choices[encoder.get()] + \
                           acodec_bitrate_choices[acodec_bitrate.get()] + \
                           acodec_channel_choices[acodec_channel.get()] + \
                           acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting \
                           + set_flac_acodec_coefficient + acodec_flac_lpc_type_choices[acodec_flac_lpc_type.get()] \
                           + acodec_flac_lpc_passes_choices[acodec_flac_lpc_passes.get()] \
                           + flac_custom_cmd_input + "-sn -vn -map_chapters -1 -map_metadata -1 " + \
                           '"' + automatic_batch_save_dir + '/%~na.flac"' + " -hide_banner"
            if shell_options.get() == "Default":
                job = subprocess.Popen('cmd /c ' + finalcommand + " " + '-v error -stats"', stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, universal_newlines=True,
                                       creationflags=subprocess.CREATE_NO_WINDOW)
                for line in job.stdout:
                    encode_window_progress.delete('1.0', END)
                    encode_window_progress.insert(END, line)
                    flac_batch_job.set('Working')
                window.destroy()
            elif shell_options.get() == "Debug":
                subprocess.Popen('cmd /k ' + finalcommand + '"')
            flac_batch_job.set('')
        # ---------------------------------------------------------------------------------------------------- FLAC Job
        # FLAC Start Job ----------------------------------------------------------------------------------------------
        if encoder.get() == "ALAC":
            alac_batch_job.set('Working')
            finalcommand = '"' + 'cd /d ' + batch_input_directory_quoted + ' & md ' + '"' \
                           + automatic_batch_save_dir + '"' \
                           +' & for %a in ' + extension_dropdownmenu_choices[extension.get()] + ' do ' + \
                           '"' + ffmpeg + '"' \
                           + ' -y -analyzeduration 100M -probesize 50M -i "%a" ' \
                           + acodec_stream_choices[acodec_stream.get()] \
                           + encoder_dropdownmenu_choices[encoder.get()] + \
                           acodec_channel_choices[acodec_channel.get()] + \
                           acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting \
                           + min_pre_order + max_pre_order + flac_custom_cmd_input \
                           + "-sn -vn -map_chapters -1 -map_metadata -1 " + \
                           '"' + automatic_batch_save_dir + '/%~na.m4a"' + " -hide_banner"
            if shell_options.get() == "Default":
                job = subprocess.Popen('cmd /c ' + finalcommand + " " + '-v error -stats"', stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, universal_newlines=True,
                                       creationflags=subprocess.CREATE_NO_WINDOW)
                for line in job.stdout:
                    encode_window_progress.delete('1.0', END)
                    encode_window_progress.insert(END, line)
                    alac_batch_job.set('Working')
                window.destroy()
            elif shell_options.get() == "Debug":
                subprocess.Popen('cmd /k ' + finalcommand + '"')
            alac_batch_job.set('')
        # ---------------------------------------------------------------------------------------------------- FLAC Job

    # Print Command Line from Batch -----------------------------------------------------------------------------------
    def print_batch_command_line():
        global automatic_batch_save_dir, automatic_batch_save_dir_quoted
        try:
            automatic_batch_save_dir = batch_save_directory
        except:
            automatic_batch_save_dir = batch_input_directory + '/Encoded'
        cmd_line_window = Toplevel()
        cmd_line_window.title('Command Line')
        cmd_line_window.configure(background="#434547")
        audio_filter_function()
        # AC3 View Command --------------------------------------------------------------------------------------------
        if encoder.get() == "AC3":
            example_cmd_output = '"' + 'cd /d ' + batch_input_directory_quoted + ' & md ' + '\n \n' + '"' \
                                 + automatic_batch_save_dir + '"' \
                                 + ' & for %a in ' + extension.get() + '\n \n' + ' do ' + \
                                 '"' + '/Apps/FFMPEG/ffmpeg.exe' + '"' \
                                 + ' -analyzeduration 100M -probesize 50M -i "%a" ' + '\n \n' \
                                 + acodec_stream_choices[acodec_stream.get()] \
                                 + encoder_dropdownmenu_choices[encoder.get()] \
                                 + acodec_bitrate_choices[acodec_bitrate.get()] + \
                                 acodec_channel_choices[acodec_channel.get()] + \
                                 acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting \
                                 + ac3_custom_cmd_input + '\n \n' \
                                 + "-sn -vn -map_chapters -1 -map_metadata -1 " + '\n \n' + \
                                 '"' + automatic_batch_save_dir + '/%~na.ac3"' + " -hide_banner"
        # ----------------------------------------------------------------------------------------------------- AC3 Job
        # AAC View Command --------------------------------------------------------------------------------------------
        elif encoder.get() == "AAC":
            if aac_vbr_toggle.get() == "-c:a ":
                bitrate_or_quality = f"-b:a {aac_bitrate_spinbox.get()}k "
            elif aac_vbr_toggle.get() == "-q:a ":
                bitrate_or_quality = f"-q:a {aac_quality_spinbox.get()} "
            example_cmd_output = '"' + 'cd /d ' + batch_input_directory_quoted + ' & md ' + '\n \n' + '"' \
                                 + automatic_batch_save_dir + '"' \
                                 + ' & for %a in ' + extension.get() + '\n \n' + ' do ' + \
                                 '"' + '/Apps/FFMPEG/ffmpeg.exe' + '"' \
                                 + ' -analyzeduration 100M -probesize 50M -i "%a" ' + '\n \n' \
                                 + acodec_stream_choices[acodec_stream.get()] + \
                                 encoder_dropdownmenu_choices[encoder.get()] + bitrate_or_quality + \
                                 acodec_channel_choices[acodec_channel.get()] + \
                                 acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting \
                                 + aac_custom_cmd_input + '\n \n' + "-sn -vn -map_chapters -1 -map_metadata -1 " \
                                 + '\n \n' + '"' + automatic_batch_save_dir + '/%~na.mp4"' \
                                 + " -hide_banner"
                # --------------------------------------------------------------------------------------------- AAC Job
        # DTS View Command --------------------------------------------------------------------------------------------
        elif encoder.get() == 'DTS':
            if dts_settings.get() == 'DTS Encoder':
                example_cmd_output = '"' + 'cd /d ' + batch_input_directory_quoted + ' & md ' + '\n \n' + '"' \
                                     + automatic_batch_save_dir + '"' \
                                     + ' & for %a in ' + extension.get() + '\n \n' + ' do ' + \
                                     '"' + '/Apps/FFMPEG/ffmpeg.exe' + '"' \
                                     + ' -analyzeduration 100M -probesize 50M -i "%a" ' + '\n \n' \
                                     + acodec_stream_choices[acodec_stream.get()] \
                                     + dts_settings_choices[dts_settings.get()] \
                                     + "-b:a " + dts_bitrate_spinbox.get() + "k " \
                                     + acodec_channel_choices[acodec_channel.get()] \
                                     + acodec_samplerate_choices[acodec_samplerate.get()] \
                                     + audio_filter_setting + dts_custom_cmd_input + '\n \n' \
                                     + "-sn -vn -map_chapters -1 -map_metadata -1 " + '\n \n' \
                                     + '"' + automatic_batch_save_dir + '/%~na.dts"' + " -hide_banner"
            else:
                example_cmd_output = '"' + 'cd /d ' + batch_input_directory_quoted + ' & md ' + '\n \n' + '"' \
                                     + automatic_batch_save_dir + '"' \
                                     + ' & for %a in ' + extension.get() + '\n \n' + ' do ' + \
                                     '"' + f"{pathlib.Path.cwd()}{'/Apps/FFMPEG/ffmpeg.exe'}" + '"' \
                                     + ' -analyzeduration 100M -probesize 50M -i "%a" ' + '\n \n' \
                                     + acodec_stream_choices[acodec_stream.get()] \
                                     + dts_settings_choices[dts_settings.get()] \
                                     + dts_custom_cmd_input + '\n \n' + "-sn -vn -map_chapters -1 -map_metadata -1 " \
                                     + '\n \n' + '"' + automatic_batch_save_dir + '/%~na.dts"' + " -hide_banner"
        # --------------------------------------------------------------------------------------------------------- DTS
        # Opus View Command -------------------------------------------------------------------------------------------
        elif encoder.get() == "Opus":
            example_cmd_output = '"' + 'cd /d ' + batch_input_directory_quoted + ' & md ' + '\n \n' + '"' \
                                 + automatic_batch_save_dir + '"' \
                                 + ' & for %a in ' + extension.get() + '\n \n' + ' do ' + \
                                 '"' + '/Apps/FFMPEG/ffmpeg.exe' + '"' \
                                 + ' -analyzeduration 100M -probesize 50M -i "%a" ' + '\n \n' \
                                 + acodec_stream_choices[acodec_stream.get()] + \
                                 encoder_dropdownmenu_choices[encoder.get()] + \
                                 acodec_vbr_choices[acodec_vbr.get()] + acodec_bitrate_choices[acodec_bitrate.get()] + \
                                 acodec_channel_choices[acodec_channel.get()] + \
                                 acodec_application_choices[acodec_application.get()] + "-packet_loss " + \
                                 packet_loss.get() + " -frame_duration " + frame_duration.get() + " " + \
                                 acodec_samplerate_choices[acodec_samplerate.get()] + \
                                 audio_filter_setting + opus_custom_cmd_input + '\n \n' \
                                 + "-sn -vn -map_chapters -1 -map_metadata -1 " + '\n \n' \
                                 + '"' + automatic_batch_save_dir + '/%~na.opus"' \
                                 + " -hide_banner"
        # -------------------------------------------------------------------------------------------------------- Opus
        # MP3 View Command --------------------------------------------------------------------------------------------
        elif encoder.get() == "MP3":
            example_cmd_output = '"' + 'cd /d ' + batch_input_directory_quoted + ' & md ' + '\n \n' + '"' \
                                 + automatic_batch_save_dir + '"' \
                                 + ' & for %a in ' + extension.get() + '\n \n' + ' do ' + \
                                 '"' + f"{pathlib.Path.cwd()}{'/Apps/FFMPEG/ffmpeg.exe'}" + '"' \
                                 + ' -analyzeduration 100M -probesize 50M -i "%a" ' + '\n \n' \
                                 + acodec_stream_choices[acodec_stream.get()] \
                                 + encoder_dropdownmenu_choices[encoder.get()] + \
                                 acodec_bitrate_choices[acodec_bitrate.get()] \
                                 + acodec_channel_choices[acodec_channel.get()] \
                                 + mp3_abr.get() + acodec_samplerate_choices[acodec_samplerate.get()] \
                                 + audio_filter_setting + mp3_custom_cmd_input + '\n \n' \
                                 + "-sn -vn -map_chapters -1 -map_metadata -1 " + '\n \n' \
                                 + '"' + automatic_batch_save_dir + '/%~na.mp3"' \
                                 + " -hide_banner"
        # --------------------------------------------------------------------------------------------------------- MP3
        # E-AC3 View Command ------------------------------------------------------------------------------------------
        elif encoder.get() == "E-AC3":
            example_cmd_output = '"' + 'cd /d ' + batch_input_directory_quoted + ' & md ' + '\n \n' + '"' \
                                 + automatic_batch_save_dir + '"' \
                                 + ' & for %a in ' + extension.get() + '\n \n' + ' do ' + \
                                 '"' + '/Apps/FFMPEG/ffmpeg.exe' + '"' \
                                 + ' -analyzeduration 100M -probesize 50M -i "%a" ' + '\n \n' \
                                 + acodec_stream_choices[acodec_stream.get()] \
                                 + encoder_dropdownmenu_choices[encoder.get()] \
                                 + "-b:a " + eac3_spinbox.get() + acodec_channel_choices[acodec_channel.get()] \
                                 + acodec_samplerate_choices[acodec_samplerate.get()] \
                                 + audio_filter_setting + '\n \n' \
                                 + "-sn -vn -map_chapters -1 -map_metadata -1 " + '\n \n' \
                                 + eac3_custom_cmd_input + per_frame_metadata_choices[per_frame_metadata.get()] \
                                 + "-mixing_level " + eac3_mixing_level.get() + " " \
                                 + room_type_choices[room_type.get()] \
                                 + "-copyright " + copyright_bit.get() + " " \
                                 + "-dialnorm " + dialogue_level.get() + " " \
                                 + '\n \n' + dolby_surround_mode_choices[dolby_surround_mode.get()] \
                                 + "-original " + original_bit_stream.get() + " " \
                                 + downmix_mode_choices[downmix_mode.get()] \
                                 + "-ltrt_cmixlev " + lt_rt_center_mix.get() + " " \
                                 + "-ltrt_surmixlev " + lt_rt_surround_mix.get() + " " \
                                 + "-loro_cmixlev " + lo_ro_center_mix.get() + " " \
                                 + "-loro_surmixlev " + lo_ro_surround_mix.get() + " " \
                                 + dolby_surround_ex_mode_choices[dolby_surround_ex_mode.get()] + '\n \n' \
                                 + dolby_headphone_mode_choices[dolby_headphone_mode.get()] \
                                 + a_d_converter_type_choices[a_d_converter_type.get()] \
                                 + stereo_rematrixing_choices[stereo_rematrixing.get()] \
                                 + "-channel_coupling " + channel_coupling.get() + " " \
                                 + "-cpl_start_band " + cpl_start_band.get() + " " + '\n \n' \
                                 + '"' + automatic_batch_save_dir + '/%~na.ac3"' + " -hide_banner"
        # ------------------------------------------------------------------------------------------------------- E-AC3
        # FDK_AAC View Command ----------------------------------------------------------------------------------------
        elif encoder.get() == "FDK-AAC":
            example_cmd_output = '"' + 'cd /d ' + batch_input_directory_quoted + ' & md ' + '\n \n' + '"' \
                                 + automatic_batch_save_dir + '"' \
                                 + ' & for %a in ' + extension.get() + '\n \n' + ' do ' + \
                                 '"' + '/Apps/FFMPEG/ffmpeg.exe' + '"' \
                                 + ' -analyzeduration 100M -probesize 50M -i "%a" ' + '\n \n' \
                                 + acodec_stream_choices[acodec_stream.get()] \
                                 + acodec_channel_choices[acodec_channel.get()] + \
                                 acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting + \
                                 "-f caf - | " + '\n \n' + '"' + '/Apps/fdkaac/fdkaac.exe' + '"' + " " + '\n \n' + \
                                 acodec_profile_choices[acodec_profile.get()] + \
                                 fdkaac_title_input + fdkaac_custom_cmd_input + \
                                 afterburnervar.get() + crccheck.get() + moovbox.get() \
                                 + sbrdelay.get() + headerperiod.get() + \
                                 acodec_lowdelay_choices[acodec_lowdelay.get()] + \
                                 acodec_sbr_ratio_choices[acodec_sbr_ratio.get()] + \
                                 acodec_transport_format_choices[acodec_transport_format.get()] + \
                                 acodec_bitrate_choices[acodec_bitrate.get()] + "- -o " +  '\n \n' + '"' \
                                 + automatic_batch_save_dir + '/%~na.m4a"' + '"'
        # --------------------------------------------------------------------------------------------------------- FDK
        # QAAC View Command -------------------------------------------------------------------------------------------
        elif encoder.get() == "QAAC":
            if q_acodec_profile.get() == "True VBR":
                example_cmd_output = '"' + 'cd /d ' + batch_input_directory_quoted + ' & md ' + '\n \n' + '"' \
                                     + automatic_batch_save_dir + '"' \
                                     + ' & for %a in ' + extension.get() + '\n \n' + ' do ' + \
                                     '"' + '/Apps/FFMPEG/ffmpeg.exe' + '"' \
                                     + ' -analyzeduration 100M -probesize 50M -i "%a" ' + '\n \n' \
                                     + acodec_stream_choices[acodec_stream.get()] \
                                     + acodec_channel_choices[acodec_channel.get()] + audio_filter_setting \
                                     + acodec_samplerate_choices[acodec_samplerate.get()] \
                                     + "-f wav - | " + '\n \n' + '"' + '/Apps/qaac/qaac64.exe' + '"' + " " + '\n \n' \
                                     + q_acodec_profile_choices[q_acodec_profile.get()] \
                                     + q_acodec_quality_amnt.get() + " " + qaac_high_efficiency.get() \
                                     + qaac_normalize.get() + qaac_nodither.get() + "--gain " \
                                     + q_acodec_gain.get() + " " + q_acodec_quality_choices[q_acodec_quality.get()] \
                                     + qaac_nodelay.get() \
                                     + q_gapless_mode_choices[q_gapless_mode.get()] + qaac_nooptimize.get() \
                                     + qaac_threading.get() + qaac_limiter.get() + qaac_title_input \
                                     + qaac_custom_cmd_input \
                                     + "- -o " + '\n \n' + '"' + automatic_batch_save_dir + '/%~na.m4a"' + '"'
            else:
                example_cmd_output = '"' + 'cd /d ' + batch_input_directory_quoted + ' & md ' + '\n \n' + '"' \
                                     + automatic_batch_save_dir + '"' \
                                     + ' & for %a in ' + extension.get() + '\n \n' + ' do ' + \
                                     '"' + '/Apps/FFMPEG/ffmpeg.exe' + '"' \
                                     + ' -analyzeduration 100M -probesize 50M -i "%a" ' + '\n \n' \
                                     + acodec_stream_choices[acodec_stream.get()] + \
                                     acodec_channel_choices[acodec_channel.get()] + audio_filter_setting + \
                                     acodec_samplerate_choices[acodec_samplerate.get()] \
                                     + "-f wav - | " + '\n \n' + '/Apps/qaac/qaac64.exe' + " " + '\n \n' \
                                     + q_acodec_profile_choices[q_acodec_profile.get()] + \
                                     q_acodec_bitrate.get() + " " + qaac_high_efficiency.get() + qaac_normalize.get() \
                                     + qaac_nodither.get() + "--gain " + q_acodec_gain.get() + " " \
                                     + q_acodec_quality_choices[q_acodec_quality.get()] + qaac_nodelay.get() \
                                     + q_gapless_mode_choices[q_gapless_mode.get()] + qaac_nooptimize.get() \
                                     + qaac_threading.get() + qaac_limiter.get() + qaac_title_input \
                                     + qaac_custom_cmd_input + "- -o " + '\n \n' + '"' \
                                     + automatic_batch_save_dir + '/%~na.m4a"' + '"'
        # -------------------------------------------------------------------------------------------------------- QAAC
        # FLAC View Command --------------------------------------------------------------------------------------------
        if encoder.get() == "FLAC":
            example_cmd_output = '"' + 'cd /d ' + batch_input_directory_quoted + ' & md ' + '\n \n' + '"' \
                                 + automatic_batch_save_dir + '"' \
                                 + ' & for %a in ' + extension.get() + '\n \n' + ' do ' + \
                                 '"' + '/Apps/FFMPEG/ffmpeg.exe' + '"' \
                                 + ' -analyzeduration 100M -probesize 50M -i "%a" ' + '\n \n' \
                                 + acodec_stream_choices[acodec_stream.get()] \
                                 + encoder_dropdownmenu_choices[encoder.get()] + \
                                 acodec_bitrate_choices[acodec_bitrate.get()] + \
                                 acodec_channel_choices[acodec_channel.get()] + \
                                 acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting \
                                 + set_flac_acodec_coefficient \
                                 + acodec_flac_lpc_type_choices[acodec_flac_lpc_type.get()] \
                                 + acodec_flac_lpc_passes_choices[acodec_flac_lpc_passes.get()] \
                                 + flac_custom_cmd_input + '\n \n' \
                                 + "-sn -vn -map_chapters -1 -map_metadata -1 " + '\n \n' + \
                                 '"' + automatic_batch_save_dir + '/%~na.flac"' + " -hide_banner"
        # ---------------------------------------------------------------------------------------------------- FLAC Job
        # ALAC View Command --------------------------------------------------------------------------------------------
        if encoder.get() == "ALAC":
            example_cmd_output = '"' + 'cd /d ' + batch_input_directory_quoted + ' & md ' + '\n \n' + '"' \
                                 + automatic_batch_save_dir + '"' \
                                 + ' & for %a in ' + extension.get() + '\n \n' + ' do ' + \
                                 '"' + '/Apps/FFMPEG/ffmpeg.exe' + '"' \
                                 + ' -analyzeduration 100M -probesize 50M -i "%a" ' + '\n \n' \
                                 + acodec_stream_choices[acodec_stream.get()] \
                                 + encoder_dropdownmenu_choices[encoder.get()] + \
                                 acodec_channel_choices[acodec_channel.get()] + \
                                 acodec_samplerate_choices[acodec_samplerate.get()] + audio_filter_setting \
                                 + min_pre_order + max_pre_order + flac_custom_cmd_input + '\n \n' \
                                 + "-sn -vn -map_chapters -1 -map_metadata -1 " + '\n \n' + \
                                 '"' + automatic_batch_save_dir + '/%~na.m4a"' + " -hide_banner"
        # ---------------------------------------------------------------------------------------------------- ALAC Job
        cmd_label = Label(cmd_line_window, text=example_cmd_output, foreground="white", background="#434547")
        cmd_label.config(font=("Helvetica", 16))
        cmd_label.pack()

    def command_line_button_batch_hover(e):
        command_line_button_batch["bg"] = "grey"

    def command_line_button_batch_hover_leave(e):
        command_line_button_batch["bg"] = "#23272A"

    # Print Final Command Line
    command_line_button_batch = Button(batch_processing_window, text="Show\nCommand", command=print_batch_command_line,
                                 state=DISABLED, foreground="white", background="#23272A", borderwidth="3")
    command_line_button_batch.grid(row=3, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)
    command_line_button_batch.bind("<Enter>", command_line_button_batch_hover)
    command_line_button_batch.bind("<Leave>", command_line_button_batch_hover_leave)


    def start_audio_button_batch_hover(e):
        start_audio_button_batch["bg"] = "grey"

    def start_audio_button_batch_hover_leave(e):
        start_audio_button_batch["bg"] = "#23272A"

    # Start Batch Jobs
    start_audio_button_batch = Button(batch_processing_window, text="Start Batch Jobs",
                                      command = lambda: threading.Thread(target=startbatchaudiojob).start(),
                                state=DISABLED, foreground="white", background="#23272A", borderwidth="3")
    start_audio_button_batch.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky=N + S + E + W)
    start_audio_button_batch.bind("<Enter>", start_audio_button_batch_hover)
    start_audio_button_batch.bind("<Leave>", start_audio_button_batch_hover_leave)


