from tkinter import Toplevel, LabelFrame, N, S, E, W, Label, StringVar, Checkbutton, font, Menu, messagebox
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
        func_parser = ConfigParser()
        func_parser.read(config_file)
        if window_pos_toggle.get() == 'yes':  # If auto save position on close is checked
            try:
                if func_parser['save_window_locations']['window location settings position'] != \
                        geometry_settings_window.geometry():
                    func_parser.set('save_window_locations', 'window location settings position',
                                    geometry_settings_window.geometry())
                    with open(config_file, 'w') as configfile:
                        func_parser.write(configfile)
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
        window_height = 450
        window_width = 550
        screen_width = geometry_settings_window.winfo_screenwidth()
        screen_height = geometry_settings_window.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        geometry_settings_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
    elif config['save_window_locations']['window location settings position'] != '' and \
            config['save_window_locations']['window location settings'] == 'yes':
        geometry_settings_window.geometry(config['save_window_locations']['window location settings position'])
    geometry_settings_window.protocol('WM_DELETE_WINDOW', gsw_exit_function)

    geometry_settings_window.rowconfigure(0, weight=1)
    geometry_settings_window.rowconfigure(1, weight=4)
    geometry_settings_window.rowconfigure(2, weight=10)
    geometry_settings_window.rowconfigure(3, weight=1)
    geometry_settings_window.grid_columnconfigure(0, weight=1)

    # Track Frame -----------------------------------------------------------------------------
    info_label = Label(geometry_settings_window, anchor='center', bg=color3, fg=color4,
                       text="Checked: Automatically saves last window size/positions when closed")
    info_label.grid(row=0, column=0, columnspan=1, padx=10, pady=(10, 0), sticky=W + E + S + N)
    info_label.config(font=(set_font, set_font_size, "italic"))

    option_frame = LabelFrame(geometry_settings_window, text=' Window Options ', labelanchor=N)
    option_frame.grid(row=1, column=0, columnspan=1, sticky=E + W + S + N, padx=10, pady=(0, 3))
    option_frame.configure(fg=color2, bg=color3, bd=4, font=(set_font, 12, "bold"))

    option_frame.rowconfigure(1, weight=1)
    option_frame.rowconfigure(2, weight=1)
    option_frame.rowconfigure(3, weight=1)
    option_frame.grid_columnconfigure(0, weight=1)
    option_frame.grid_columnconfigure(1, weight=1)

    option_frame_audio = LabelFrame(geometry_settings_window, text=' Audio Codec Window Options ', labelanchor=N)
    option_frame_audio.grid(row=2, column=0, columnspan=1, sticky=E + W + S + N, padx=10, pady=(3, 0))
    option_frame_audio.configure(fg=color2, bg=color3, bd=4, font=(set_font, 12, "bold"))

    for n in range(0, 5):
        option_frame_audio.rowconfigure(n, weight=1)
    option_frame_audio.grid_columnconfigure(0, weight=1)
    option_frame_audio.grid_columnconfigure(1, weight=1)

    info_label = Label(geometry_settings_window, anchor='center', bg=color3, fg=color4,
                       text="Info: Right click inside each frame for more options")
    info_label.grid(row=3, column=0, columnspan=1, padx=10, pady=(0, 10), sticky=W + E + S + N)
    info_label.config(font=(set_font, set_font_size, "italic"))

    # ----------------------------------------------------------------------------- Track Frame

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
    ffmpeg_pos_toggle_checkbox.grid(row=0, column=0, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=W + N)
    ffmpeg_pos_toggle_checkbox.configure(background=color3, foreground=color5, activebackground=color3,
                                         activeforeground=color5, selectcolor=color3,
                                         font=(set_font, set_font_size + 2))

    def window_location_pos_toggle():
        func_parser = ConfigParser()
        func_parser.read(config_file)
        try:  # Write to config
            func_parser.set('save_window_locations', 'window location settings', window_pos_toggle.get())
            if window_pos_toggle.get() == 'no':
                func_parser.set('save_window_locations', 'window location settings position', '')
            with open(config_file, 'w') as configfile:
                func_parser.write(configfile)
        except (Exception,):
            pass

    window_pos_toggle = StringVar()  # variable
    window_pos_toggle.set(config['save_window_locations']['window location settings'])  # Set box from config.ini
    window_pos_toggle_checkbox = Checkbutton(option_frame, text='Window Location Settings', variable=window_pos_toggle,
                                             onvalue='yes', offvalue='no', command=window_location_pos_toggle)
    window_pos_toggle_checkbox.grid(row=0, column=1, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=E + N)
    window_pos_toggle_checkbox.configure(background=color3, foreground=color5, activebackground=color3,
                                         activeforeground=color5, selectcolor=color3,
                                         font=(set_font, set_font_size + 2))

    def about_win_pos_toggle():
        try:  # Write to config
            config.set('save_window_locations', 'about', about_pos_toggle.get())
            if about_pos_toggle.get() == 'no':
                config.set('save_window_locations', 'about position', '')
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except (Exception,):
            pass

    about_pos_toggle = StringVar()  # variable
    about_pos_toggle.set(config['save_window_locations']['about'])  # Set box from config.ini
    about_pos_toggle_checkbox = Checkbutton(option_frame, text='About Window', variable=about_pos_toggle,
                                            onvalue='yes', offvalue='no', command=about_win_pos_toggle)
    about_pos_toggle_checkbox.grid(row=1, column=1, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=N + E)
    about_pos_toggle_checkbox.configure(background=color3, foreground=color5, activebackground=color3,
                                        activeforeground=color5, selectcolor=color3, font=(set_font, set_font_size + 2))

    def progress_win_pos_toggle():
        try:  # Write to config
            config.set('save_window_locations', 'progress window', progress_pos_toggle.get())
            if progress_pos_toggle.get() == 'no':
                config.set('save_window_locations', 'progress window position', '')
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except (Exception,):
            pass

    progress_pos_toggle = StringVar()  # variable
    progress_pos_toggle.set(config['save_window_locations']['progress window'])  # Set box from config.ini
    progress_pos_toggle_checkbox = Checkbutton(option_frame, text='Progress Window', variable=progress_pos_toggle,
                                               onvalue='yes', offvalue='no', command=progress_win_pos_toggle)
    progress_pos_toggle_checkbox.grid(row=1, column=0, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=N + W)
    progress_pos_toggle_checkbox.configure(background=color3, foreground=color5, activebackground=color3,
                                           activeforeground=color5, selectcolor=color3,
                                           font=(set_font, set_font_size + 2))

    def job_manager_win_pos_toggle():
        try:  # Write to config
            config.set('save_window_locations', 'job window', job_manager_win_toggle.get())
            if job_manager_win_toggle.get() == 'no':
                config.set('save_window_locations', 'job window position', '')
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except (Exception,):
            pass

    job_manager_win_toggle = StringVar()  # variable
    job_manager_win_toggle.set(config['save_window_locations']['job window'])  # Set box from config.ini
    job_manager_win_toggle_checkbox = Checkbutton(option_frame, text='Job Manager', variable=job_manager_win_toggle,
                                                  onvalue='yes', offvalue='no', command=job_manager_win_pos_toggle)
    job_manager_win_toggle_checkbox.grid(row=2, column=0, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=N + W)
    job_manager_win_toggle_checkbox.configure(background=color3, foreground=color5, activebackground=color3,
                                              activeforeground=color5, selectcolor=color3,
                                              font=(set_font, set_font_size + 2))

    def display_command_pos_toggle():
        try:  # Write to config
            config.set('save_window_locations', 'display command', display_command_pos.get())
            if job_manager_win_toggle.get() == 'no':
                config.set('save_window_locations', 'display command position', '')
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except (Exception,):
            pass

    display_command_pos = StringVar()  # variable
    display_command_pos.set(config['save_window_locations']['display command'])  # Set box from config.ini
    display_command_pos_checkbox = Checkbutton(option_frame, text='Display Command', variable=display_command_pos,
                                               onvalue='yes', offvalue='no', command=display_command_pos_toggle)
    display_command_pos_checkbox.grid(row=2, column=1, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=N + E)
    display_command_pos_checkbox.configure(background=color3, foreground=color5, activebackground=color3,
                                           activeforeground=color5, selectcolor=color3,
                                           font=(set_font, set_font_size + 2))

    # Right click menu for "Window Options" frame ---------------------------------------------------------------------
    def option_popup_menu(e):  # Function for mouse button 3 (right click) to pop up menu
        def select_all():
            func_parser = ConfigParser()
            func_parser.read(config_file)

            ffmpeg_pos_toggle.set('yes')
            func_parser.set('save_window_locations', 'ffmpeg audio encoder', 'yes')

            window_pos_toggle.set('yes')
            func_parser.set('save_window_locations', 'window location settings', 'yes')

            progress_pos_toggle.set('yes')
            func_parser.set('save_window_locations', 'progress window', 'yes')

            job_manager_win_toggle.set('yes')
            func_parser.set('save_window_locations', 'job window', 'yes')

            about_pos_toggle.set('yes')
            func_parser.set('save_window_locations', 'about', 'yes')

            display_command_pos.set('yes')
            func_parser.set('save_window_locations', 'display command', 'yes')
            with open(config_file, 'w') as configfile:
                func_parser.write(configfile)

        def reset():  # Function to reset all items in frame to default
            msg = messagebox.askyesno(title='Prompt', parent=geometry_settings_window,
                                      message='Are you sure you want to reset all "Window Options" to default?')
            if msg:  # If user selects "yes" to prompt
                func_parser = ConfigParser()
                func_parser.read(config_file)

                ffmpeg_pos_toggle.set('no')
                func_parser.set('save_window_locations', 'ffmpeg audio encoder', 'no')
                func_parser.set('save_window_locations', 'ffmpeg audio encoder position', '')

                window_pos_toggle.set('no')
                func_parser.set('save_window_locations', 'window location settings', 'no')
                func_parser.set('save_window_locations', 'window location settings position', '')

                progress_pos_toggle.set('no')
                func_parser.set('save_window_locations', 'progress window', 'no')
                func_parser.set('save_window_locations', 'progress window position', '')

                job_manager_win_toggle.set('no')
                func_parser.set('save_window_locations', 'job window', 'no')
                func_parser.set('save_window_locations', 'job window position', '')

                about_pos_toggle.set('no')
                func_parser.set('save_window_locations', 'about', 'no')
                func_parser.set('save_window_locations', 'about position', '')

                display_command_pos.set('no')
                func_parser.set('save_window_locations', 'display command', 'no')
                func_parser.set('save_window_locations', 'display command position', '')
                with open(config_file, 'w') as configfile:
                    func_parser.write(configfile)

        option_menu = Menu(geometry_settings_window, tearoff=False)  # Menu
        option_menu.add_command(label='Reset: "FFMPEG Audio Encoder"', command=lambda: [
            ffmpeg_pos_toggle.set('no'), ffmpeg_gui_pos_toggle()])
        option_menu.add_command(label='Reset: "Window Location Settings"', command=lambda: [
            window_pos_toggle.set('no'), window_location_pos_toggle()])
        option_menu.add_command(label='Reset: "Progress Window"', command=lambda: [
            progress_pos_toggle.set('no'), progress_win_pos_toggle()])
        option_menu.add_command(label='Reset: "Job Manager Window"', command=lambda: [
            job_manager_win_toggle.set('no'), job_manager_win_pos_toggle()])
        option_menu.add_command(label='Reset: "About Window"', command=lambda: [
            about_pos_toggle.set('no'), about_win_pos_toggle()])
        option_menu.add_command(label='Reset: "Display Command"', command=lambda: [
            display_command_pos.set('no'), display_command_pos_toggle()])
        option_menu.add_separator()
        option_menu.add_command(label='Reset: All "Window Options"', command=reset)
        option_menu.add_separator()
        option_menu.add_command(label='Check all "Audio Codec Window Options"', command=select_all)
        option_menu.tk_popup(e.x_root, e.y_root)  # This gets the position of 'e' on the root widget

    option_frame.bind('<Button-3>', option_popup_menu)  # Right click to pop up menu in frame
    ffmpeg_pos_toggle_checkbox.bind('<Button-3>', option_popup_menu)  # Right click to pop up menu in frame
    window_pos_toggle_checkbox.bind('<Button-3>', option_popup_menu)  # Right click to pop up menu in frame
    progress_pos_toggle_checkbox.bind('<Button-3>', option_popup_menu)  # Right click to pop up menu in frame
    about_pos_toggle_checkbox.bind('<Button-3>', option_popup_menu)  # Right click to pop up menu in frame
    job_manager_win_toggle_checkbox.bind('<Button-3>', option_popup_menu)  # Right click to pop up menu in frame
    display_command_pos_checkbox.bind('<Button-3>', option_popup_menu)  # Right click to pop up menu in frame

    # --------------------------------------------------------------------- Right click menu for "Window Options" frame

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
    ac3_pos_toggle_checkbox = Checkbutton(option_frame_audio, text='AC3 - Audio Settings', variable=ac3_pos_toggle,
                                          onvalue='yes', offvalue='no', command=ac3_location_pos_toggle)
    ac3_pos_toggle_checkbox.grid(row=0, column=0, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=W + N)
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
    aac_pos_toggle_checkbox = Checkbutton(option_frame_audio, text='AAC - Audio Settings', variable=aac_pos_toggle,
                                          onvalue='yes', offvalue='no', command=aac_location_pos_toggle)
    aac_pos_toggle_checkbox.grid(row=0, column=1, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=E + N)
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
    e_ac3_pos_toggle_checkbox = Checkbutton(option_frame_audio, text='E-AC3 - Audio Settings',
                                            variable=e_ac3_pos_toggle, onvalue='yes', offvalue='no',
                                            command=e_ac3_location_pos_toggle)
    e_ac3_pos_toggle_checkbox.grid(row=1, column=0, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=W + N)
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
    dts_pos_toggle_checkbox = Checkbutton(option_frame_audio, text='DTS - Audio Settings', variable=dts_pos_toggle,
                                          onvalue='yes', offvalue='no', command=dts_location_pos_toggle)
    dts_pos_toggle_checkbox.grid(row=1, column=1, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=E + N)
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
    opus_pos_toggle_checkbox = Checkbutton(option_frame_audio, text='Opus - Audio Settings', variable=opus_pos_toggle,
                                           onvalue='yes', offvalue='no', command=opus_location_pos_toggle)
    opus_pos_toggle_checkbox.grid(row=2, column=0, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=W + N)
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
    mp3_pos_toggle_checkbox = Checkbutton(option_frame_audio, text='Mp3 - Audio Settings', variable=mp3_pos_toggle,
                                          onvalue='yes', offvalue='no', command=mp3_location_pos_toggle)
    mp3_pos_toggle_checkbox.grid(row=2, column=1, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=E + N)
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
    fdk_aac_pos_toggle_checkbox = Checkbutton(option_frame_audio, text='FDK-AAC - Audio Settings',
                                              variable=fdk_aac_pos_toggle, onvalue='yes', offvalue='no',
                                              command=fdk_aac_location_pos_toggle)
    fdk_aac_pos_toggle_checkbox.grid(row=3, column=0, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=W + N)
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
    qaac_pos_toggle_checkbox = Checkbutton(option_frame_audio, text='QAAC - Audio Settings', variable=qaac_pos_toggle,
                                           onvalue='yes', offvalue='no', command=qaac_location_pos_toggle)
    qaac_pos_toggle_checkbox.grid(row=3, column=1, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=E + N)
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
    flac_pos_toggle_checkbox = Checkbutton(option_frame_audio, text='FLAC - Audio Settings', variable=flac_pos_toggle,
                                           onvalue='yes', offvalue='no', command=flac_location_pos_toggle)
    flac_pos_toggle_checkbox.grid(row=4, column=0, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=W + N)
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
    alac_pos_toggle_checkbox = Checkbutton(option_frame_audio, text='ALAC - Audio Settings', variable=alac_pos_toggle,
                                           onvalue='yes', offvalue='no', command=alac_location_pos_toggle)
    alac_pos_toggle_checkbox.grid(row=4, column=1, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=E + N)
    alac_pos_toggle_checkbox.configure(background=color3, foreground=color5, activebackground=color3,
                                       activeforeground=color5, selectcolor=color3, font=(set_font, set_font_size + 2))

    # View Streams in Audio Settings Windows
    def view_streams_toggle_function():
        try:  # Write to config
            config.set('save_window_locations', 'audio window - view streams', view_streams_toggle.get())
            if alac_pos_toggle.get() == 'no':
                config.set('save_window_locations', 'audio window - view streams - position', '')
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        except (Exception,):
            pass

    view_streams_toggle = StringVar()  # variable
    view_streams_toggle.set(config['save_window_locations']['audio window - view streams'])  # Set box from config.ini
    view_streams_toggle_checkbox = Checkbutton(option_frame_audio, text='View Streams', variable=view_streams_toggle,
                                               onvalue='yes', offvalue='no', command=view_streams_toggle_function)
    view_streams_toggle_checkbox.grid(row=5, column=0, rowspan=1, columnspan=1, padx=10, pady=(0, 0), sticky=W + N)
    view_streams_toggle_checkbox.configure(background=color3, foreground=color5, activebackground=color3,
                                           activeforeground=color5, selectcolor=color3,
                                           font=(set_font, set_font_size + 2))

    # Right click menu for "Audio Codec Window Options" frame ---------------------------------------------------------
    def option_audio_popup_menu(e):  # Function for mouse button 3 (right click) to pop up menu
        def select_all():
            func_parser = ConfigParser()
            func_parser.read(config_file)
            ac3_pos_toggle.set('yes')
            func_parser.set('save_window_locations', 'audio window - ac3', 'yes')

            aac_pos_toggle.set('yes')
            func_parser.set('save_window_locations', 'audio window - aac', 'yes')

            e_ac3_pos_toggle.set('yes')
            func_parser.set('save_window_locations', 'audio window - e-ac3', 'yes')

            dts_pos_toggle.set('yes')
            func_parser.set('save_window_locations', 'audio window - dts', 'yes')

            opus_pos_toggle.set('yes')
            func_parser.set('save_window_locations', 'audio window - opus', 'yes')

            mp3_pos_toggle.set('yes')
            func_parser.set('save_window_locations', 'audio window - mp3', 'yes')

            fdk_aac_pos_toggle.set('yes')
            func_parser.set('save_window_locations', 'audio window - fdk-aac', 'yes')

            qaac_pos_toggle.set('yes')
            func_parser.set('save_window_locations', 'audio window - qaac', 'yes')

            flac_pos_toggle.set('yes')
            func_parser.set('save_window_locations', 'audio window - flac', 'yes')

            alac_pos_toggle.set('yes')
            func_parser.set('save_window_locations', 'audio window - alac', 'yes')

            view_streams_toggle.set('yes')
            func_parser.set('save_window_locations', 'audio window - view streams', 'yes')
            with open(config_file, 'w') as configfile:
                func_parser.write(configfile)

        def reset():  # Function to reset all items in frame to default
            msg = messagebox.askyesno(title='Prompt', parent=geometry_settings_window,
                                      message='Are you sure you want to reset all '
                                              '"Audio Codec Window Options" to default?')
            if msg:  # If user selects yes to prompt
                func_parser = ConfigParser()
                func_parser.read(config_file)
                ac3_pos_toggle.set('no')
                func_parser.set('save_window_locations', 'audio window - ac3', 'no')
                func_parser.set('save_window_locations', 'audio window - ac3 - position', '')

                aac_pos_toggle.set('no')
                func_parser.set('save_window_locations', 'audio window - aac', 'no')
                func_parser.set('save_window_locations', 'audio window - aac - position', '')

                e_ac3_pos_toggle.set('no')
                func_parser.set('save_window_locations', 'audio window - e-ac3', 'no')
                func_parser.set('save_window_locations', 'audio window - e-ac3 - position', '')

                dts_pos_toggle.set('no')
                func_parser.set('save_window_locations', 'audio window - dts', 'no')
                func_parser.set('save_window_locations', 'audio window - dts - position', '')

                opus_pos_toggle.set('no')
                func_parser.set('save_window_locations', 'audio window - opus', 'no')
                func_parser.set('save_window_locations', 'audio window - opus - position', '')

                mp3_pos_toggle.set('no')
                func_parser.set('save_window_locations', 'audio window - mp3', 'no')
                func_parser.set('save_window_locations', 'audio window - mp3 - position', '')

                fdk_aac_pos_toggle.set('no')
                func_parser.set('save_window_locations', 'audio window - fdk-aac', 'no')
                func_parser.set('save_window_locations', 'audio window - fdk-aac - position', '')

                qaac_pos_toggle.set('no')
                func_parser.set('save_window_locations', 'audio window - qaac', 'no')
                func_parser.set('save_window_locations', 'audio window - qaac - position', '')

                flac_pos_toggle.set('no')
                func_parser.set('save_window_locations', 'audio window - flac', 'no')
                func_parser.set('save_window_locations', 'audio window - flac - position', '')

                alac_pos_toggle.set('no')
                func_parser.set('save_window_locations', 'audio window - alac', 'no')
                func_parser.set('save_window_locations', 'audio window - alac - position', '')

                view_streams_toggle.set('no')
                func_parser.set('save_window_locations', 'audio window - view streams', 'no')
                func_parser.set('save_window_locations', 'audio window - view streams - position', '')
                with open(config_file, 'w') as configfile:
                    func_parser.write(configfile)

        option_menu = Menu(geometry_settings_window, tearoff=False)  # Menu
        option_menu.add_command(label='Reset: "AC3"', command=lambda: [
            ac3_pos_toggle.set('no'), ac3_location_pos_toggle()])
        option_menu.add_command(label='Reset: "AAC"', command=lambda: [
            aac_pos_toggle.set('no'), aac_location_pos_toggle()])
        option_menu.add_command(label='Reset: "E-AC3"', command=lambda: [
            e_ac3_pos_toggle.set('no'), e_ac3_location_pos_toggle()])
        option_menu.add_command(label='Reset: "DTS"', command=lambda: [
            dts_pos_toggle.set('no'), dts_location_pos_toggle()])
        option_menu.add_command(label='Reset: "Opus"', command=lambda: [
            opus_pos_toggle.set('no'), opus_location_pos_toggle()])
        option_menu.add_command(label='Reset: "Mp3"', command=lambda: [
            mp3_pos_toggle.set('no'), mp3_location_pos_toggle()])
        option_menu.add_command(label='Reset: "FDK-AAC"', command=lambda: [
            fdk_aac_pos_toggle.set('no'), fdk_aac_location_pos_toggle()])
        option_menu.add_command(label='Reset: "QAAC"', command=lambda: [
            qaac_pos_toggle.set('no'), qaac_location_pos_toggle()])
        option_menu.add_command(label='Reset: "FLAC"', command=lambda: [
            flac_pos_toggle.set('no'), flac_location_pos_toggle()])
        option_menu.add_command(label='Reset: "ALAC"', command=lambda: [
            alac_pos_toggle.set('no'), alac_location_pos_toggle()])
        option_menu.add_command(label='Reset: "View Streams"', command=lambda: [
            view_streams_toggle.set('no'), view_streams_toggle_function()])
        option_menu.add_separator()
        option_menu.add_command(label='Reset: All "Audio Codec Window Options"', command=reset)
        option_menu.add_separator()
        option_menu.add_command(label='Check all "Audio Codec Window Options"', command=select_all)
        option_menu.tk_popup(e.x_root, e.y_root)  # This gets the position of 'e' on the root widget

    option_frame_audio.bind('<Button-3>', option_audio_popup_menu)  # Right click to pop up menu in frame
    list_of_check_buttons = [ac3_pos_toggle_checkbox, aac_pos_toggle_checkbox, e_ac3_pos_toggle_checkbox,
                             dts_pos_toggle_checkbox, opus_pos_toggle_checkbox, mp3_pos_toggle_checkbox,
                             fdk_aac_pos_toggle_checkbox, qaac_pos_toggle_checkbox, flac_pos_toggle_checkbox,
                             alac_pos_toggle_checkbox, view_streams_toggle_checkbox]
    for check_buttons in list_of_check_buttons:  # Use list of check buttons to bind
        check_buttons.bind('<Button-3>', option_audio_popup_menu)  # Right click to pop up menu in frame
    # --------------------------------------------------------- Right click menu for "Audio Codec Window Options" frame
    # ---------------------------------------------------------------------------------------- Window geometry settings
