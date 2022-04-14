# Show Streams Inside Audio Settings Window -----------------------------------------------------------------------
from tkinter import NORMAL, END, TclError, Toplevel, scrolledtext, INSERT, DISABLED, Menu
from pathlib import Path
from pymediainfo import MediaInfo
from pyperclip import copy as pyperclip_copy
from idlelib.tooltip import Hovertip


def exit_stream_window():  # Global function to exit stream window (so it can be accessed via main script)
    stream_window.destroy()  # Destroy global stream_window


def show_streams_mediainfo_function(x):  # Stream Viewer
    global stream_win_text_area, exit_stream_window, stream_window
    video_input = Path(x)  # "x" is passed through from main GUI

    try:
        stream_win_text_area.config(state=NORMAL)
        stream_win_text_area.delete(1.0, END)
    except (NameError, TclError):
        stream_window = Toplevel()
        stream_window.title("Audio Streams")
        stream_window.configure(background="#434547")
        stream_window.resizable(False, False)  # Disable resize of this window
        stream_window.protocol('WM_DELETE_WINDOW', exit_stream_window)
        stream_win_text_area = scrolledtext.ScrolledText(stream_window, width=80, height=25, tabs=10, spacing2=3,
                                                         spacing1=2, spacing3=3)
        stream_win_text_area.config(bg='black', fg='#CFD2D1', bd=8)
        stream_win_text_area.grid(column=0, pady=5, padx=5)
        stream_window.grid_columnconfigure(0, weight=1)
    media_info = MediaInfo.parse(video_input)  # Uses pymediainfo to get information for track selection
    for track in media_info.tracks:  # For loop to loop through mediainfo tracks
        # Formatting --------------------------------------------------------------------------------------------------
        if track.track_type == 'Audio':  # Only grab audio track information
            if str(track.stream_identifier) != 'None':  # Gets stream #
                audio_track_id = 'Track#:          ' + str(int(track.stream_identifier) + 1) + '\n'
            else:
                pass
            if str(track.format) != 'None':  # Gets format string of tracks (aac, ac3 etc...)
                audio_format = 'Codec:           ' + str(track.commercial_name) + ' - ' + str(track.format) + '\n'
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
                audio_channels = 'Channels:        ' + show_channels + '  -  ' + str(f'({track.channel_layout})') + '\n'
            else:
                audio_channels = ''
            if str(track.other_bit_rate) != 'None':  # Gets audio bit rate of input tracks
                audio_bitrate = 'Bitrate:         ' + str(track.other_bit_rate).replace('[', '') \
                    .replace(']', '').replace("'", '') + '\n'
            else:
                audio_bitrate = ''
            if str(track.other_language) != 'None':  # Gets audio language of input tracks
                audio_language = 'Language:        ' + str(track.other_language[0]) + '\n'
            else:
                audio_language = ''
            if str(track.title) != 'None':  # Gets audio title of input tracks
                if len(str(track.title)) > 50:  # Counts title character length
                    audio_title = 'Title:           ' + str(track.title)[:50] + '...\n'  # If title > 50 characters
                else:
                    audio_title = 'Title:           ' + str(track.title) + '\n'  # If title is < 50 characters
            else:
                audio_title = ''
            if str(track.other_sampling_rate) != 'None':  # Gets audio sampling rate of input tracks
                audio_sampling_rate = 'Sampling Rate:   ' + str(track.other_sampling_rate) \
                    .replace('[', '').replace(']', '').replace("'", '') + '\n'
            else:
                audio_sampling_rate = ''
            if str(track.other_duration) != 'None':  # Gets audio duration of input tracks
                audio_duration = 'Duration:        ' + str(track.other_duration[0]) + '\n'
            else:
                audio_duration = ''
            if str(track.delay) != 'None':  # Gets audio delay of input tracks
                if str(track.delay) == '0':
                    audio_delay = ''
                else:
                    audio_delay = 'Delay:   ' + f'        "{str(track.delay)}ms"' \
                                  + f'\nDelay to Video:  "{str(track.delay_relative_to_video)}ms"' + '\n'
            else:
                audio_delay = ''
            if str(track.compression_mode) != 'None':
                audio_track_compression = 'Compression:     ' + str(track.compression_mode)
            else:
                audio_track_compression = ''

            # -------------------------------------------------------------------------------------------------- Formatting
            audio_track_info = str(audio_track_id + audio_format + audio_channels + audio_bitrate +
                                   audio_sampling_rate + audio_delay + audio_duration + audio_language +
                                   audio_title + audio_track_compression)  # Formatting variable
            media_info_track_string = 80 * '#' + '\n' + audio_track_info + '\n' + 80 * '#' + '\n'  # String to insert
            stream_win_text_area.configure(state=NORMAL)  # Enable textbox
            stream_win_text_area.insert(INSERT, media_info_track_string)  # Insert string
            stream_win_text_area.insert(INSERT, '\n')  # Insert a newline
            stream_win_text_area.configure(state=DISABLED)  # Disable textbox

    def right_click_menu_func(x_y_pos):  # Function for mouse button 3 (right click) to pop up menu
        right_click_menu.tk_popup(x_y_pos.x_root, x_y_pos.y_root)  # This gets the position of cursor

    right_click_menu = Menu(stream_window, tearoff=False)  # This is the right click menu
    right_click_menu.add_command(label='Copy', command=pyperclip_copy(stream_win_text_area.get(1.0, END)))
    stream_window.bind('<Button-3>', right_click_menu_func)  # Uses mouse button 3 (right click) to pop up menu
    Hovertip(stream_win_text_area, 'Right click to copy', hover_delay=1000)  # Hover tip tool-tip
# ---------------------------------------------------------------------------------------------------- Show Streams
