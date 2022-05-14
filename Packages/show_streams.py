# Show Streams Inside Audio Settings Window -----------------------------------------------------------------------
import pathlib
from configparser import ConfigParser
from idlelib.tooltip import Hovertip
from time import sleep as time_sleep
from tkinter import NORMAL, END, TclError, Toplevel, scrolledtext, INSERT, DISABLED, Menu, LabelFrame, font, N, E, W, S

from pyautogui import hotkey as pya_hotkey
from pymediainfo import MediaInfo
from pyperclip import copy as pyperclip_copy


def exit_stream_window():  # Global function to exit stream window (so it can be accessed via main script)
    config_file = 'Runtime/config.ini'  # Creates (if it doesn't exist) and defines location of config.ini
    func_parser = ConfigParser()
    func_parser.read(config_file)
    if func_parser['save_window_locations']['audio window - view streams'] == 'yes':  # If auto save position on
        try:
            if func_parser['save_window_locations']['audio window - view streams - position'] != \
                    stream_window.geometry():
                func_parser.set('save_window_locations', 'audio window - '
                                                         'view streams - position', stream_window.geometry())
                with open(config_file, 'w') as configfile:
                    func_parser.write(configfile)
        except (Exception,):
            pass
    stream_window.destroy()  # Destroy global stream_window


def show_streams_mediainfo_function(x):  # Stream Viewer
    global stream_win_text_area, exit_stream_window, stream_window
    video_input = pathlib.Path(x)  # "x" is passed through from main GUI

    # Defines the path to config.ini and opens it for reading/writing
    config_file = 'Runtime/config.ini'  # Creates (if it doesn't exist) and defines location of config.ini
    config = ConfigParser()
    config.read(config_file)

    detect_font = font.nametofont("TkDefaultFont")  # Get default font value into Font object
    set_font = detect_font.actual().get("family")
    # set_font_size = detect_font.actual().get("size")

    try:
        stream_win_text_area.config(state=NORMAL)
        stream_win_text_area.delete(1.0, END)
    except (NameError, TclError):
        stream_window = Toplevel()
        stream_window.title("Audio Streams")
        stream_window.configure(background="#434547")
        stream_window.resizable(False, False)  # Disable resize of this window
        if config['save_window_locations']['audio window - view streams - position'] != '' and \
                config['save_window_locations']['audio window - view streams'] == 'yes':
            stream_window.geometry(config['save_window_locations']['audio window - view streams - position'])
        stream_window.protocol('WM_DELETE_WINDOW', exit_stream_window)
        stream_window.grid_columnconfigure(0, weight=1)
        stream_window.grid_rowconfigure(0, weight=1)

        stream_window_frame = LabelFrame(stream_window, text=' Audio Streams ', labelanchor="n")
        stream_window_frame.grid(column=0, row=0, columnspan=1, padx=5, pady=(0, 3), sticky=N + S + E + W)
        stream_window_frame.configure(fg="#3498db", bg="#434547", bd=3, font=(set_font, 10, "bold"))
        stream_window_frame.grid_rowconfigure(0, weight=1)
        stream_window_frame.grid_columnconfigure(0, weight=1)

        stream_win_text_area = scrolledtext.ScrolledText(stream_window_frame, width=80, height=25, tabs=10, spacing2=3,
                                                         spacing1=2, spacing3=3)
        stream_win_text_area.config(bg='black', fg='#CFD2D1', bd=8)
        stream_win_text_area.grid(column=0, pady=5, padx=5, sticky=N + E + S + W)

    character_space = 30  # Can be changed to adjust space of all items in the list automatically
    media_info = MediaInfo.parse(video_input)  # Uses pymediainfo to get information for track selection
    for track in media_info.tracks:  # For loop to loop through mediainfo tracks
        # Formatting --------------------------------------------------------------------------------------------------
        if track.track_type == 'Audio':  # Only grab audio track information
            if str(track.stream_identifier) != 'None':  # Gets stream #
                audio_track_id_space = 'Track#' + ' ' * int(f'{character_space - len("Track#")}')
                audio_track_id = audio_track_id_space + f': {str(int(track.stream_identifier) + 1)}\n'
            else:
                audio_track_id = ''
            if str(track.format) != 'None':  # Gets format string of tracks (aac, ac3 etc...)
                audio_format_space = 'Codec' + ' ' * int(f'{character_space - len("Codec")}')
                audio_format = audio_format_space + f": {str(track.commercial_name)} - ({str(track.format).lower()})\n"
            else:
                audio_format = ''
            if str(track.channel_s) != 'None':  # Gets audio channels of input tracks
                audio_channel_space = 'Channels' + ' ' * int(f'{character_space - len("Channels")}')
                if str(track.channel_s) == '8':
                    show_channels = '7.1'
                elif str(track.channel_s) == '6':
                    show_channels = '5.1'
                elif str(track.channel_s) == '3':
                    show_channels = '2.1'
                else:
                    show_channels = str(track.channel_s)
                audio_channels = audio_channel_space + f": {show_channels} - {str(track.channel_layout)}\n"
            else:
                audio_channels = ''
            if str(track.bit_rate_mode) != 'None':  # Gets audio bit rate mode
                audio_bitrate_mode_space = 'Bit rate mode' + ' ' * int(f'{character_space - len("Bit rate mode")}')
                if str(track.other_bit_rate_mode) != 'None':  # Get secondary string of audio bit rate mode
                    audio_bitrate_mode = audio_bitrate_mode_space + f": {str(track.bit_rate_mode)} / " \
                                                                    f"{str(track.other_bit_rate_mode[0])}\n"
                else:
                    audio_bitrate_mode = audio_bitrate_mode_space + f": {str(track.bit_rate_mode)}\n"
            else:
                audio_bitrate_mode = ''
            if str(track.other_bit_rate) != 'None':  # Gets audio bit rate of input tracks
                audio_bitrate_space = 'Bit rate' + ' ' * int(f'{character_space - len("Bit rate")}')
                audio_bitrate = audio_bitrate_space + f": {str(track.other_bit_rate[0])}\n"
            else:
                audio_bitrate = ''
            if str(track.other_language) != 'None':  # Gets audio language of input tracks
                audio_language_space = 'Language' + ' ' * int(f'{character_space - len("Language")}')
                audio_language = audio_language_space + f": {str(track.other_language[0])}\n"
            else:
                audio_language = ''
            if str(track.title) != 'None':  # Gets audio title of input tracks
                audio_title_space = 'Title' + ' ' * int(f'{character_space - len("Title")}')
                if len(str(track.title)) > 40:  # Counts title character length
                    audio_title = audio_title_space + f": {str(track.title)[:40]}...\n"  # If title > 40 characters
                else:
                    audio_title = audio_title_space + f": {str(track.title)}\n"  # If title is < 40 characters
            else:
                audio_title = ''
            if str(track.other_sampling_rate) != 'None':  # Gets audio sampling rate of input tracks
                audio_sampling_rate_space = 'Sampling Rate' + ' ' * int(f'{character_space - len("Sampling Rate")}')
                audio_sampling_rate = audio_sampling_rate_space + f": {str(track.other_sampling_rate[0])}\n"
            else:
                audio_sampling_rate = ''
            if str(track.other_duration) != 'None':  # Gets audio duration of input tracks
                audio_duration_space = 'Duration' + ' ' * int(f'{character_space - len("Duration")}')
                audio_duration = audio_duration_space + f": {str(track.other_duration[0])}\n"
            else:
                audio_duration = ''
            if str(track.delay) != 'None':  # Gets audio delay of input tracks
                if str(track.delay) == '0':
                    audio_delay = ''
                else:
                    audio_delay_space = 'Delay' + ' ' * int(f'{character_space - len("Delay")}')
                    audio_del_to_vid_space = 'Delay to Video' + ' ' * int(f'{character_space - len("Delay to Video")}')
                    audio_delay = audio_delay_space + f': {str(track.delay)}ms\n' \
                                  + audio_del_to_vid_space + f': {str(track.delay_relative_to_video)}ms\n '
            else:
                audio_delay = ''
            if str(track.other_stream_size) != 'None':  # Get tracks stream size
                audio_track_size_space = 'Stream size' + ' ' * int(f'{character_space - len("Stream size")}')
                audio_track_stream_size = audio_track_size_space + f": {str(track.other_stream_size[4])}\n"
            else:
                audio_track_stream_size = ''
            if str(track.other_bit_depth) != 'None':  # Get tracks bit-depth
                audio_track_b_depth_space = 'Bit Depth' + ' ' * int(f'{character_space - len("Bit Depth")}')
                audio_track_bit_depth = audio_track_b_depth_space + f": {(track.other_bit_depth[0])}\n"
            else:
                audio_track_bit_depth = ''
            if str(track.compression_mode) != 'None':
                audio_track_compression_space = 'Compression' + ' ' * int(f'{character_space - len("Compression")}')
                audio_track_compression = audio_track_compression_space + f": {str(track.compression_mode)}\n"
            else:
                audio_track_compression = ''
            if str(track.default) != 'None':  # Get tracks default boolean
                audio_track_default_space = 'Default' + ' ' * int(f'{character_space - len("Default")}')
                audio_track_default = audio_track_default_space + f": {str(track.default)}\n"
            else:
                audio_track_default = ''
            if str(track.forced) != 'None':  # Get tracks forced boolean
                audio_track_forced_space = 'Forced' + ' ' * int(f'{character_space - len("Forced")}')
                audio_track_forced = audio_track_forced_space + f": {str(track.forced)}"
            else:
                audio_track_forced = ''

            # ---------------------------------------------------------------------------------------------- Formatting
            audio_track_info = str(audio_track_id + audio_format + audio_channels + audio_bitrate_mode +
                                   audio_bitrate + audio_sampling_rate + audio_delay + audio_duration +
                                   audio_language + audio_title + audio_track_stream_size + audio_track_bit_depth +
                                   audio_track_compression + audio_track_default + audio_track_forced)  # Formatting
            media_info_track_string = 80 * '#' + '\n' + audio_track_info + '\n' + 80 * '#' + '\n'  # String to insert
            stream_win_text_area.configure(state=NORMAL)  # Enable textbox
            stream_win_text_area.insert(INSERT, media_info_track_string)  # Insert string
            stream_win_text_area.insert(INSERT, '\n')  # Insert a newline
            stream_win_text_area.configure(state=DISABLED)  # Disable textbox

    def right_click_menu_func(x_y_pos):  # Function for mouse button 3 (right click) to pop up menu
        right_click_menu.tk_popup(x_y_pos.x_root, x_y_pos.y_root)  # This gets the position of cursor

    def copy_selected_text():  # Function to copy only selected text
        pya_hotkey('ctrl', 'c')
        time_sleep(.01)  # Slow program incase ctrl+c is slower

    right_click_menu = Menu(stream_window, tearoff=False)  # This is the right click menu
    right_click_menu.add_command(label='Copy Selected Text', command=copy_selected_text)
    right_click_menu.add_command(label='Copy All Text', command=pyperclip_copy(stream_win_text_area.get(1.0, END)))
    stream_window.bind('<Button-3>', right_click_menu_func)  # Uses mouse button 3 (right click) to pop up menu
    Hovertip(stream_win_text_area, 'Right click to copy', hover_delay=1200)  # Hover tip tool-tip


def stream_menu(x):
    build_list = []
    media_info = MediaInfo.parse(pathlib.Path(x))  # Uses pymediainfo to get information for track selection
    for track in media_info.tracks:  # For loop to loop through mediainfo tracks
        # Formatting --------------------------------------------------------------------------------------------------
        if track.track_type == 'Audio':  # Only grab audio track information
            if str(track.format) != 'None':  # Gets format string of tracks (aac, ac3 etc...)
                audio_format = f"{str(track.commercial_name)} - ({str(track.format).lower()})  |  "
            else:
                audio_format = ''
            if str(track.channel_s) != 'None':  # Gets audio channels of input tracks
                if str(track.channel_s) == '8':
                    show_channels = '7.1'
                elif str(track.channel_s) == '6':
                    show_channels = '5.1'
                elif str(track.channel_s) == '3':
                    show_channels = '2.1'
                else:
                    show_channels = str(track.channel_s)
                audio_channels = f"Chnl: {show_channels}  |  "
            else:
                audio_channels = ''
            if str(track.bit_rate_mode) != 'None':  # Gets audio bit rate mode
                if str(track.other_bit_rate_mode) != 'None':  # Get secondary string of audio bit rate mode
                    audio_bitrate_mode = f"{str(track.bit_rate_mode)}  |  "
            else:
                audio_bitrate_mode = ''
            if str(track.other_bit_rate) != 'None':  # Gets audio bit rate of input tracks
                audio_bitrate = f"{str(track.other_bit_rate[0])}  |  "
            else:
                audio_bitrate = ''
            if str(track.other_language) != 'None':  # Gets audio language of input tracks
                audio_language = f"{str(track.other_language[0])}  |  "
            else:
                audio_language = ''
            if str(track.title) != 'None':  # Gets audio title of input tracks
                if len(str(track.title)) > 40:  # Counts title character length
                    audio_title = f"{str(track.title)[:20]}...  |  "  # If title > 40 characters
                else:
                    audio_title = f"{str(track.title)}  |  "  # If title is < 40 characters
            else:
                audio_title = ''
            if str(track.other_sampling_rate) != 'None':  # Gets audio sampling rate of input tracks
                audio_sampling_rate = f"{str(track.other_sampling_rate[0])}  |  "
            else:
                audio_sampling_rate = ''
            if str(track.other_duration) != 'None':  # Gets audio duration of input tracks
                audio_duration = f"{str(track.other_duration[0])}  |  "
            else:
                audio_duration = ''
            if str(track.delay) != 'None':  # Gets audio delay of input tracks
                if str(track.delay) == '0':
                    audio_delay = ''
                else:
                    audio_delay = f'{str(track.delay)}ms  |  '
            else:
                audio_delay = ''
            if str(track.other_stream_size) != 'None':  # Get tracks stream size
                audio_track_stream_size = f"{str(track.other_stream_size[4])}  |  "
            else:
                audio_track_stream_size = ''
            if str(track.other_bit_depth) != 'None':  # Get tracks bit-depth
                audio_track_bit_depth = f"{(track.other_bit_depth[0])}-bit  |  "
            else:
                audio_track_bit_depth = ''
            # ---------------------------------------------------------------------------------------------- Formatting
            audio_track_info = str(audio_format + audio_channels + audio_bitrate_mode +
                                   audio_bitrate + audio_sampling_rate + audio_delay + audio_duration +
                                   audio_language + audio_title + audio_track_stream_size +
                                   audio_track_bit_depth).strip()
            # Formatting
            build_list.append(audio_track_info)
    return build_list
# ---------------------------------------------------------------------------------------------------- Show Streams
