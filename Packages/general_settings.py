import pathlib
from configparser import ConfigParser
from tkinter import Toplevel, LabelFrame, N, S, E, W, font, Button, Frame, Entry, DISABLED, NORMAL, filedialog, END, ttk


# noinspection PyGlobalUndefined
def open_general_settings():  # General Settings Window
    global general_settings_window

    try:  # Check if window is already open, if it's open break from function
        if general_settings_window.winfo_exists():
            return
    except NameError:
        pass

    def general_settings_exit_function():  # Exit function when hitting the 'X' button
        func_parser = ConfigParser()
        func_parser.read(config_file)
        if func_parser['save_window_locations']['general settings'] == 'yes':  # If auto save position on
            print('yes')
            try:
                if func_parser['save_window_locations']['general settings position'] != \
                        general_settings_window.geometry():
                    func_parser.set('save_window_locations', 'general settings position',
                                    general_settings_window.geometry())
                    with open(config_file, 'w') as configfile:
                        func_parser.write(configfile)
            except (Exception,):
                pass
        general_settings_window.grab_release()  # Release grab on window
        general_settings_window.destroy()  # Close window

    # Config Parser
    config_file = 'Runtime/config.ini'
    config_parser = ConfigParser()
    config_parser.read(config_file)
    # Config Parser

    general_settings_window = Toplevel()  # Define toplevel()
    general_settings_window.title('Window Location Settings')
    detect_font = font.nametofont("TkDefaultFont")  # Get default font value into Font object
    set_font = detect_font.actual().get("family")
    color1 = "#434547"
    general_settings_window.configure(background=color1)
    if config_parser['save_window_locations']['general settings position'] == '' or \
            config_parser['save_window_locations']['general settings'] == 'no':
        window_height = 420
        window_width = 600
        screen_width = general_settings_window.winfo_screenwidth()
        screen_height = general_settings_window.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        general_settings_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
    elif config_parser['save_window_locations']['general settings position'] != '' and \
            config_parser['save_window_locations']['general settings'] == 'yes':
        general_settings_window.geometry(config_parser['save_window_locations']['general settings position'])
    general_settings_window.protocol('WM_DELETE_WINDOW', general_settings_exit_function)
    general_settings_window.grab_set()  # Focus all of tkinters attention on this window only

    general_settings_window.rowconfigure(0, weight=1)
    general_settings_window.grid_columnconfigure(0, weight=1)

    # Themes ----------------------------------------------------------------------------------------------------------
    # Hover over button theme ---------------------------------------
    class HoverButton(Button):
        def __init__(self, master, **kw):
            Button.__init__(self, master=master, **kw)
            self.defaultBackground = self["background"]
            self.bind("<Enter>", self.on_enter)
            self.bind("<Leave>", self.on_leave)

        def on_enter(self, _):
            self['background'] = self['activebackground']

        def on_leave(self, _):
            self['background'] = self.defaultBackground

    # --------------------------------------- Hover over button theme
    # Settings Notebook Frame -----------------------------------------------------------------------------------------
    tabs = ttk.Notebook(general_settings_window)
    tabs.grid(row=0, column=0, columnspan=4, sticky=E + W + N + S, padx=0, pady=0)
    settings_tab = Frame(tabs, background="#434547")
    tabs.add(settings_tab, text=' Settings ')

    for n in range(4):
        settings_tab.grid_columnconfigure(n, weight=1)
    for n in range(2):
        settings_tab.grid_rowconfigure(n, weight=1)

    # ----------------------------------------------------------------------------------------  Settings Notebook Frame
    # ---------------------------------------------------------------------------------------------------------- Themes

    path_frame = LabelFrame(settings_tab, text=' Tool Paths ', labelanchor="n")
    path_frame.grid(column=0, row=0, columnspan=4, padx=5, pady=(10, 3), sticky=N + S + E + W)
    path_frame.configure(fg="#3498db", bg="#434547", bd=3, font=(set_font, 10, "bold"))
    for p_f in range(3):
        path_frame.grid_rowconfigure(p_f, weight=1)
    for p_f in range(4):
        path_frame.grid_columnconfigure(p_f, weight=1)

    ffmpeg_frame = LabelFrame(path_frame, text=' FFMPEG ', labelanchor="nw")
    ffmpeg_frame.grid(column=0, row=0, columnspan=4, padx=5, pady=(5, 3), sticky=E + W)
    ffmpeg_frame.configure(fg="#3498db", bg="#434547", bd=3, font=(set_font, 9, "italic"))
    ffmpeg_frame.grid_rowconfigure(0, weight=1)
    ffmpeg_frame.grid_columnconfigure(0, weight=1)
    ffmpeg_frame.grid_columnconfigure(1, weight=20)

    def set_ffmpeg_path():
        path = filedialog.askopenfilename(title='Select Location to "ffmpeg.exe"',
                                          initialdir=pathlib.Path(ffmpeg_entry_box.get()).parent,
                                          filetypes=[('ffmpeg', 'ffmpeg.exe')], parent=general_settings_window)
        if path:
            func_parser = ConfigParser()
            func_parser.read(config_file)
            ffmpeg = f'"{str(pathlib.Path(path))}"'
            func_parser.set('ffmpeg_path', 'path', ffmpeg)
            with open(config_file, 'w') as configfile:
                func_parser.write(configfile)
            ffmpeg_entry_box.config(state=NORMAL)
            ffmpeg_entry_box.delete(0, END)
            ffmpeg_entry_box.insert(0, str(pathlib.Path(str(
                func_parser['ffmpeg_path']['path']).replace('"', '')).resolve()))
            ffmpeg_entry_box.config(state=DISABLED)

    set_ffmpeg_path = HoverButton(ffmpeg_frame, text="Set Path", command=set_ffmpeg_path, foreground="white",
                                  background="#23272A", borderwidth="3", activebackground='grey')
    set_ffmpeg_path.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)

    saved_ffmpeg_path = pathlib.Path(str(config_parser['ffmpeg_path']['path']).replace('"', '')).resolve()
    ffmpeg_entry_box = Entry(ffmpeg_frame, borderwidth=4, background="#CACACA")
    ffmpeg_entry_box.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=N + S + E + W)
    ffmpeg_entry_box.insert(0, str(saved_ffmpeg_path))
    ffmpeg_entry_box.config(state=DISABLED)

    mpv_frame = LabelFrame(path_frame, text=' MPV ', labelanchor="nw")
    mpv_frame.grid(column=0, row=1, columnspan=4, padx=5, pady=(5, 3), sticky=E + W)
    mpv_frame.configure(fg="#3498db", bg="#434547", bd=3, font=(set_font, 9, "italic"))
    mpv_frame.grid_rowconfigure(0, weight=1)
    mpv_frame.grid_columnconfigure(0, weight=1)
    mpv_frame.grid_columnconfigure(1, weight=20)

    def set_mpv_path():
        path = filedialog.askopenfilename(title='Select Location to "mpv.exe"',
                                          initialdir=pathlib.Path(mpv_entry_box.get()).parent,
                                          filetypes=[('mpv', 'mpv.exe')], parent=general_settings_window)
        if path:
            func_parser = ConfigParser()
            func_parser.read(config_file)
            mpv = f'"{str(pathlib.Path(path))}"'
            func_parser.set('mpv_player_path', 'path', mpv)
            with open(config_file, 'w') as configfile:
                func_parser.write(configfile)
            mpv_entry_box.config(state=NORMAL)
            mpv_entry_box.delete(0, END)
            mpv_entry_box.insert(0, str(pathlib.Path(str(
                func_parser['mpv_player_path']['path']).replace('"', '')).resolve()))
            mpv_entry_box.config(state=DISABLED)

    set_mpv_path = HoverButton(mpv_frame, text="Set Path", command=set_mpv_path, foreground="white",
                               background="#23272A", borderwidth="3", activebackground='grey')
    set_mpv_path.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)

    saved_mpv_path = pathlib.Path(str(config_parser['mpv_player_path']['path']).replace('"', '')).resolve()
    mpv_entry_box = Entry(mpv_frame, borderwidth=4, background="#CACACA")
    mpv_entry_box.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=N + S + E + W)
    mpv_entry_box.insert(0, str(saved_mpv_path))
    mpv_entry_box.config(state=DISABLED)

    mediainfogui_frame = LabelFrame(path_frame, text=' MediaInfo GUI ', labelanchor="nw")
    mediainfogui_frame.grid(column=0, row=2, columnspan=4, padx=5, pady=(5, 3), sticky=E + W)
    mediainfogui_frame.configure(fg="#3498db", bg="#434547", bd=3, font=(set_font, 9, "italic"))
    mediainfogui_frame.grid_rowconfigure(0, weight=1)
    mediainfogui_frame.grid_columnconfigure(0, weight=1)
    mediainfogui_frame.grid_columnconfigure(1, weight=20)

    def set_mediainfogui_path():
        path = filedialog.askopenfilename(title='Select Location to "mediainfo.exe"',
                                          initialdir=pathlib.Path(mediainfogui_entry_box.get()).parent,
                                          filetypes=[('mediainfo', 'mediainfo.exe')], parent=general_settings_window)
        if path:
            func_parser = ConfigParser()
            func_parser.read(config_file)
            mediainfogui = f'"{str(pathlib.Path(path))}"'
            func_parser.set('mediainfogui_path', 'path', mediainfogui)
            with open(config_file, 'w') as configfile:
                func_parser.write(configfile)
            mediainfogui_entry_box.config(state=NORMAL)
            mediainfogui_entry_box.delete(0, END)
            mediainfogui_entry_box.insert(0, str(pathlib.Path(str(
                func_parser['mediainfogui_path']['path']).replace('"', '')).resolve()))
            mediainfogui_entry_box.config(state=DISABLED)

    set_mediainfogui_path = HoverButton(mediainfogui_frame, text="Set Path", command=set_mediainfogui_path,
                                        foreground="white", background="#23272A", borderwidth="3",
                                        activebackground='grey')
    set_mediainfogui_path.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)

    saved_mediainfogui_path = pathlib.Path(str(config_parser['mediainfogui_path']['path']).replace('"', '')).resolve()
    mediainfogui_entry_box = Entry(mediainfogui_frame, borderwidth=4, background="#CACACA")
    mediainfogui_entry_box.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=N + S + E + W)
    mediainfogui_entry_box.insert(0, str(saved_mediainfogui_path))
    mediainfogui_entry_box.config(state=DISABLED)

    save_path_frame = LabelFrame(settings_tab, text=' Save Paths ', labelanchor="n")
    save_path_frame.grid(column=0, row=1, columnspan=4, padx=5, pady=(10, 3), sticky=N + S + E + W)
    save_path_frame.configure(fg="#3498db", bg="#434547", bd=3, font=(set_font, 10, "bold"))
    save_path_frame.grid_rowconfigure(0, weight=1)
    for s_p in range(4):
        save_path_frame.grid_columnconfigure(s_p, weight=1)

    manual_auto_frame = LabelFrame(save_path_frame, text=' Manual/Auto Encode Path ', labelanchor="nw")
    manual_auto_frame.grid(column=0, row=0, columnspan=4, padx=5, pady=(5, 3), sticky=E + W)
    manual_auto_frame.configure(fg="#3498db", bg="#434547", bd=3, font=(set_font, 9, "italic"))
    manual_auto_frame.grid_rowconfigure(0, weight=1)
    manual_auto_frame.grid_columnconfigure(0, weight=1)
    manual_auto_frame.grid_columnconfigure(1, weight=20)

    def set_manual_auto_path():
        path = filedialog.askdirectory(title='Output Path Manual/Auto', parent=general_settings_window)
        if path:
            func_parser = ConfigParser()
            func_parser.read(config_file)
            path = str(pathlib.Path(path))
            func_parser.set('output_path', 'path', path)
            with open(config_file, 'w') as configfile:
                func_parser.write(configfile)
            manual_auto_entry_box.config(state=NORMAL)
            manual_auto_entry_box.delete(0, END)
            manual_auto_entry_box.insert(0, str(pathlib.Path(str(func_parser['output_path']['path']))))
            manual_auto_entry_box.config(state=DISABLED)

    set_manual_auto_path = HoverButton(manual_auto_frame, text="Set Path", command=set_manual_auto_path,
                                       foreground="white", background="#23272A", borderwidth="3",
                                       activebackground='grey')
    set_manual_auto_path.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)

    saved_manual_auto_path = pathlib.Path(str(config_parser['output_path']['path']).replace('"', '')).resolve()
    manual_auto_entry_box = Entry(manual_auto_frame, borderwidth=4, background="#CACACA")
    manual_auto_entry_box.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=N + S + E + W)
    manual_auto_entry_box.insert(0, str(saved_manual_auto_path))
    manual_auto_entry_box.config(state=DISABLED)
