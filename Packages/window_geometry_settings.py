from tkinter import Toplevel, LabelFrame, N, S, E, W, Label, StringVar, Checkbutton, font
from configparser import ConfigParser


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
        window_height = 550
        window_width = 368
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

    for n in range(1, 7):
        option_frame.rowconfigure(n, weight=1)
    option_frame.grid_columnconfigure(0, weight=1)
    option_frame.grid_columnconfigure(1, weight=1)
    # ----------------------------------------------------------------------------- Track Frame

    info_label = Label(option_frame, anchor='center', bg=color3, fg=color4,
                       text="Checked: Automatically saves last window size/positions when closed")
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
                                         activeforeground=color5, selectcolor=color3,
                                         font=(set_font, set_font_size + 2))

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
                                         activeforeground=color5, selectcolor=color3,
                                         font=(set_font, set_font_size + 2))

    def ac3_location_pos_toggle():
        try:  # Write to config
            config.set('save_window_locations', 'audio window - ac3', ac3_pos_toggle.get())
            if ac3_pos_toggle.get() == 'no':
                config.set('save_window_locations', 'audio window - ac3 - position', '')
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except (Exception,):
            pass

    ac3_pos_toggle = StringVar()  # variable
    ac3_pos_toggle.set(config['save_window_locations']['audio window - ac3'])  # Set box from config.ini
    ac3_pos_toggle_checkbox = Checkbutton(option_frame, text='AC3 - Audio Settings', variable=ac3_pos_toggle,
                                          onvalue='yes', offvalue='no', command=ac3_location_pos_toggle)
    ac3_pos_toggle_checkbox.grid(row=2, column=0, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=W + N)
    ac3_pos_toggle_checkbox.configure(background=color3, foreground=color5, activebackground=color3,
                                      activeforeground=color5, selectcolor=color3, font=(set_font, set_font_size + 2))

    def aac_location_pos_toggle():
        try:  # Write to config
            config.set('save_window_locations', 'audio window - aac', aac_pos_toggle.get())
            if aac_pos_toggle.get() == 'no':
                config.set('save_window_locations', 'audio window - aac - position', '')
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except (Exception,):
            pass

    aac_pos_toggle = StringVar()  # variable
    aac_pos_toggle.set(config['save_window_locations']['audio window - aac'])  # Set box from config.ini
    aac_pos_toggle_checkbox = Checkbutton(option_frame, text='AAC - Audio Settings', variable=aac_pos_toggle,
                                          onvalue='yes', offvalue='no', command=aac_location_pos_toggle)
    aac_pos_toggle_checkbox.grid(row=2, column=1, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=E + N)
    aac_pos_toggle_checkbox.configure(background=color3, foreground=color5, activebackground=color3,
                                      activeforeground=color5, selectcolor=color3, font=(set_font, set_font_size + 2))

    def e_ac3_location_pos_toggle():
        try:  # Write to config
            config.set('save_window_locations', 'audio window - e-ac3', e_ac3_pos_toggle.get())
            if e_ac3_pos_toggle.get() == 'no':
                config.set('save_window_locations', 'audio window - e-ac3 - position', '')
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except (Exception,):
            pass

    e_ac3_pos_toggle = StringVar()  # variable
    e_ac3_pos_toggle.set(config['save_window_locations']['audio window - e-ac3'])  # Set box from config.ini
    e_ac3_pos_toggle_checkbox = Checkbutton(option_frame, text='E-AC3 - Audio Settings', variable=e_ac3_pos_toggle,
                                            onvalue='yes', offvalue='no', command=e_ac3_location_pos_toggle)
    e_ac3_pos_toggle_checkbox.grid(row=3, column=0, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=W + N)
    e_ac3_pos_toggle_checkbox.configure(background=color3, foreground=color5, activebackground=color3,
                                        activeforeground=color5, selectcolor=color3, font=(set_font, set_font_size + 2))

    def dts_location_pos_toggle():
        try:  # Write to config
            config.set('save_window_locations', 'audio window - dts', dts_pos_toggle.get())
            if dts_pos_toggle.get() == 'no':
                config.set('save_window_locations', 'audio window - dts - position', '')
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except (Exception,):
            pass

    dts_pos_toggle = StringVar()  # variable
    dts_pos_toggle.set(config['save_window_locations']['audio window - dts'])  # Set box from config.ini
    dts_pos_toggle_checkbox = Checkbutton(option_frame, text='DTS - Audio Settings', variable=dts_pos_toggle,
                                          onvalue='yes', offvalue='no', command=dts_location_pos_toggle)
    dts_pos_toggle_checkbox.grid(row=3, column=1, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=E + N)
    dts_pos_toggle_checkbox.configure(background=color3, foreground=color5, activebackground=color3,
                                      activeforeground=color5, selectcolor=color3, font=(set_font, set_font_size + 2))

    def opus_location_pos_toggle():
        try:  # Write to config
            config.set('save_window_locations', 'audio window - opus', opus_pos_toggle.get())
            if opus_pos_toggle.get() == 'no':
                config.set('save_window_locations', 'audio window - opus - position', '')
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except (Exception,):
            pass

    opus_pos_toggle = StringVar()  # variable
    opus_pos_toggle.set(config['save_window_locations']['audio window - opus'])  # Set box from config.ini
    opus_pos_toggle_checkbox = Checkbutton(option_frame, text='Opus - Audio Settings', variable=opus_pos_toggle,
                                           onvalue='yes', offvalue='no', command=opus_location_pos_toggle)
    opus_pos_toggle_checkbox.grid(row=4, column=0, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=W + N)
    opus_pos_toggle_checkbox.configure(background=color3, foreground=color5, activebackground=color3,
                                       activeforeground=color5, selectcolor=color3, font=(set_font, set_font_size + 2))

    def mp3_location_pos_toggle():
        try:  # Write to config
            config.set('save_window_locations', 'audio window - mp3', mp3_pos_toggle.get())
            if mp3_pos_toggle.get() == 'no':
                config.set('save_window_locations', 'audio window - mp3 - position', '')
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except (Exception,):
            pass

    mp3_pos_toggle = StringVar()  # variable
    mp3_pos_toggle.set(config['save_window_locations']['audio window - mp3'])  # Set box from config.ini
    mp3_pos_toggle_checkbox = Checkbutton(option_frame, text='Mp3 - Audio Settings', variable=mp3_pos_toggle,
                                          onvalue='yes', offvalue='no', command=mp3_location_pos_toggle)
    mp3_pos_toggle_checkbox.grid(row=4, column=1, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=E + N)
    mp3_pos_toggle_checkbox.configure(background=color3, foreground=color5, activebackground=color3,
                                      activeforeground=color5, selectcolor=color3, font=(set_font, set_font_size + 2))

    def fdk_aac_location_pos_toggle():
        try:  # Write to config
            config.set('save_window_locations', 'audio window - fdk-aac', fdk_aac_pos_toggle.get())
            if fdk_aac_pos_toggle.get() == 'no':
                config.set('save_window_locations', 'audio window - fdk-aac - position', '')
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except (Exception,):
            pass

    fdk_aac_pos_toggle = StringVar()  # variable
    fdk_aac_pos_toggle.set(config['save_window_locations']['audio window - fdk-aac'])  # Set box from config.ini
    fdk_aac_pos_toggle_checkbox = Checkbutton(option_frame, text='FDK-AAC - Audio Settings',
                                              variable=fdk_aac_pos_toggle, onvalue='yes', offvalue='no',
                                              command=fdk_aac_location_pos_toggle)
    fdk_aac_pos_toggle_checkbox.grid(row=5, column=0, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=W + N)
    fdk_aac_pos_toggle_checkbox.configure(background=color3, foreground=color5, activebackground=color3,
                                          activeforeground=color5, selectcolor=color3,
                                          font=(set_font, set_font_size + 2))

    def qaac_location_pos_toggle():
        try:  # Write to config
            config.set('save_window_locations', 'audio window - qaac', qaac_pos_toggle.get())
            if qaac_pos_toggle.get() == 'no':
                config.set('save_window_locations', 'audio window - qaac - position', '')
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except (Exception,):
            pass

    qaac_pos_toggle = StringVar()  # variable
    qaac_pos_toggle.set(config['save_window_locations']['audio window - qaac'])  # Set box from config.ini
    qaac_pos_toggle_checkbox = Checkbutton(option_frame, text='QAAC - Audio Settings', variable=qaac_pos_toggle,
                                           onvalue='yes', offvalue='no', command=qaac_location_pos_toggle)
    qaac_pos_toggle_checkbox.grid(row=5, column=1, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=E + N)
    qaac_pos_toggle_checkbox.configure(background=color3, foreground=color5, activebackground=color3,
                                       activeforeground=color5, selectcolor=color3, font=(set_font, set_font_size + 2))

    def flac_location_pos_toggle():
        try:  # Write to config
            config.set('save_window_locations', 'audio window - flac', flac_pos_toggle.get())
            if flac_pos_toggle.get() == 'no':
                config.set('save_window_locations', 'audio window - flac - position', '')
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except (Exception,):
            pass

    flac_pos_toggle = StringVar()  # variable
    flac_pos_toggle.set(config['save_window_locations']['audio window - flac'])  # Set box from config.ini
    flac_pos_toggle_checkbox = Checkbutton(option_frame, text='FLAC - Audio Settings', variable=flac_pos_toggle,
                                           onvalue='yes', offvalue='no', command=flac_location_pos_toggle)
    flac_pos_toggle_checkbox.grid(row=6, column=0, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=W + N)
    flac_pos_toggle_checkbox.configure(background=color3, foreground=color5, activebackground=color3,
                                       activeforeground=color5, selectcolor=color3, font=(set_font, set_font_size + 2))

    def alac_location_pos_toggle():
        try:  # Write to config
            config.set('save_window_locations', 'audio window - alac', alac_pos_toggle.get())
            if alac_pos_toggle.get() == 'no':
                config.set('save_window_locations', 'audio window - alac - position', '')
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except (Exception,):
            pass

    alac_pos_toggle = StringVar()  # variable
    alac_pos_toggle.set(config['save_window_locations']['audio window - alac'])  # Set box from config.ini
    alac_pos_toggle_checkbox = Checkbutton(option_frame, text='ALAC - Audio Settings', variable=alac_pos_toggle,
                                           onvalue='yes', offvalue='no', command=alac_location_pos_toggle)
    alac_pos_toggle_checkbox.grid(row=6, column=1, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=E + N)
    alac_pos_toggle_checkbox.configure(background=color3, foreground=color5, activebackground=color3,
                                       activeforeground=color5, selectcolor=color3, font=(set_font, set_font_size + 2))
# -------------------------------------------------------------------------------------------- Window geometry settings
