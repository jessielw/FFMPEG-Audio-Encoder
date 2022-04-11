from tkinter import *
from configparser import ConfigParser
from tkinter import font


# Window geometry settings --------------------------------------------------------------------------------------------
def set_window_geometry_settings():
    global geometry_settings_window

    try:  # Check if window is already open, if it's open break from function
        if geometry_settings_window.winfo_exists():
            return
    except NameError:
        pass

    def gsw_exit_function():  # Exit function when hitting the 'X' button
        if window_pos_toggle.get() == 'yes':  # If auto save position on close is checked
            try:
                config.set('save_window_locations', 'window location settings position',
                           geometry_settings_window.geometry())
                with open(config_file, 'w') as configfile:
                    config.write(configfile)
            except (Exception,):
                pass

        geometry_settings_window.destroy()  # Close window

    # Defines the path to config.ini and opens it for reading/writing
    config_file = 'Runtime/config.ini'  # Creates (if doesn't exist) and defines location of config.ini
    config = ConfigParser()
    config.read(config_file)

    detect_font = font.nametofont("TkDefaultFont")  # Get default font value into Font object
    set_font = detect_font.actual().get("family")
    set_font_size = detect_font.actual().get("size")
    color1 = "#434547"
    color2 = "#3498db"
    color3 = "#636669"
    color4 = "light grey"
    color5 = "white"
    # print(detect_font.actual().get("family"))
    # print(detect_font.actual())

    geometry_settings_window = Toplevel()
    geometry_settings_window.title('Window Location Settings')
    geometry_settings_window.configure(background=color1)
    if config['save_window_locations']['window location settings position'] == '' or \
            config['save_window_locations']['window location settings'] == 'no':
        window_height = 640
        window_width = 514
        screen_width = geometry_settings_window.winfo_screenwidth()
        screen_height = geometry_settings_window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        geometry_settings_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    elif config['save_window_locations']['window location settings position'] != '' and \
            config['save_window_locations']['window location settings'] == 'yes':
        geometry_settings_window.geometry(config['save_window_locations']['window location settings position'])
    geometry_settings_window.protocol('WM_DELETE_WINDOW', gsw_exit_function)

    geometry_settings_window.rowconfigure(0, weight=1)
    geometry_settings_window.grid_columnconfigure(0, weight=1)

    # Track Frame -----------------------------------------------------------------------------
    option_frame = LabelFrame(geometry_settings_window, text=' Options ', labelanchor=N)
    option_frame.grid(row=0, column=0, columnspan=2, sticky=E + W + S + N, padx=10, pady=(10, 10))
    option_frame.configure(fg=color2, bg=color3, bd=4, font=(set_font, 12, "bold"))

    option_frame.rowconfigure(1, weight=1)
    option_frame.grid_columnconfigure(1, weight=1)
    # ----------------------------------------------------------------------------- Track Frame

    info_label = Label(option_frame, anchor='center', bg=color3, fg=color4,
                       text="Checked: Automatically saves last window positions when closed")
    info_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(0, 20), sticky=W + E + N)
    info_label.config(font=(set_font, set_font_size, "italic"))

    def ffmpeg_gui_pos_toggle():
        try:  # Write to config
            config.set('save_window_locations', 'ffmpeg audio encoder', ffmpeg_pos_toggle.get())
            if ffmpeg_pos_toggle.get() == 'no':
                config.set('save_window_locations', 'ffmpeg audio encoder position', '')
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except (Exception,):
            pass

    ffmpeg_pos_toggle = StringVar()  # variable
    ffmpeg_pos_toggle.set(config['save_window_locations']['ffmpeg audio encoder'])  # Set box from config.ini
    ffmpeg_pos_toggle_checkbox = Checkbutton(option_frame, text='FFMPEG Audio Encoder', variable=ffmpeg_pos_toggle,
                                             onvalue='yes', offvalue='no', command=ffmpeg_gui_pos_toggle)
    ffmpeg_pos_toggle_checkbox.grid(row=1, column=0, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=W + N)
    ffmpeg_pos_toggle_checkbox.configure(background=color3, foreground=color5, activebackground=color3,
                                         activeforeground=color5, selectcolor=color3)

    def window_location_pos_toggle():
        try:  # Write to config
            config.set('save_window_locations', 'window location settings', window_pos_toggle.get())
            if window_pos_toggle.get() == 'no':
                config.set('save_window_locations', 'window location settings position', '')
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except (Exception,):
            pass

    window_pos_toggle = StringVar()  # variable
    window_pos_toggle.set(config['save_window_locations']['window location settings'])  # Set box from config.ini
    window_pos_toggle_checkbox = Checkbutton(option_frame, text='Window Location Settings', variable=window_pos_toggle,
                                             onvalue='yes', offvalue='no', command=window_location_pos_toggle)
    window_pos_toggle_checkbox.grid(row=1, column=1, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=E + N)
    window_pos_toggle_checkbox.configure(background=color3, foreground=color5, activebackground=color3,
                                         activeforeground=color5, selectcolor=color3)

# -------------------------------------------------------------------------------------------- Window geometry settings
