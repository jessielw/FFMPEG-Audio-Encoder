import pathlib
import webbrowser
from configparser import ConfigParser
from tkinter import Toplevel, LabelFrame, N, S, E, W, font, Button, Frame, Entry, DISABLED, NORMAL, filedialog, END, \
    ttk, messagebox, Label


# noinspection PyGlobalUndefined
def open_general_settings():  # General Settings Window
    global general_settings_window

    try:  # Check if window is already open, if it's open break from function
        if general_settings_window.winfo_exists():
            return
    except NameError:
        pass

    def general_settings_exit_function():  # Exit function when hitting the 'X' button
        general_parser = ConfigParser()
        general_parser.read(config_file)
        if general_parser['save_window_locations']['general settings'] == 'yes':  # If auto save position on
            try:
                if general_parser['save_window_locations']['general settings position'] != \
                        general_settings_window.geometry():
                    general_parser.set('save_window_locations', 'general settings position',
                                       general_settings_window.geometry())
                    with open(config_file, 'w') as generalfile:
                        general_parser.write(generalfile)
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
    general_settings_window.title('General Settings')
    detect_font = font.nametofont("TkDefaultFont")  # Get default font value into Font object
    set_font = detect_font.actual().get("family")
    color1 = "#434547"
    general_settings_window.configure(background=color1)
    if config_parser['save_window_locations']['general settings position'] == '' or \
            config_parser['save_window_locations']['general settings'] == 'no':
        window_height = 670
        window_width = 640
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
    tabs.add(settings_tab, text=' Paths ')

    for n in range(4):
        settings_tab.grid_columnconfigure(n, weight=1)
    for n in range(2):
        settings_tab.grid_rowconfigure(n, weight=1)

    # ----------------------------------------------------------------------------------------  Settings Notebook Frame
    # ---------------------------------------------------------------------------------------------------------- Themes

    path_frame = LabelFrame(settings_tab, text=' Tool Paths ', labelanchor="n")
    path_frame.grid(column=0, row=0, columnspan=4, padx=5, pady=(10, 3), sticky=N + S + E + W)
    path_frame.configure(fg="#3498db", bg="#434547", bd=3, font=(set_font, 10, "bold"))
    for p_f in range(5):
        path_frame.grid_rowconfigure(p_f, weight=1)
    for p_f in range(4):
        path_frame.grid_columnconfigure(p_f, weight=1)

    # FFMPEG Path -----------------------------------------------------------------------------------------------------
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
            ffmpeg_parser = ConfigParser()
            ffmpeg_parser.read(config_file)
            ffmpeg = f'"{str(pathlib.Path(path))}"'
            ffmpeg_parser.set('ffmpeg_path', 'path', ffmpeg)
            with open(config_file, 'w') as ffmpeg_configfile:
                ffmpeg_parser.write(ffmpeg_configfile)
            ffmpeg_entry_box.config(state=NORMAL)
            ffmpeg_entry_box.delete(0, END)
            ffmpeg_entry_box.insert(0, str(pathlib.Path(str(
                ffmpeg_parser['ffmpeg_path']['path']).replace('"', '')).resolve()))
            ffmpeg_entry_box.config(state=DISABLED)

    set_ffmpeg_path = HoverButton(ffmpeg_frame, text="Set Path", command=set_ffmpeg_path, foreground="white",
                                  background="#23272A", borderwidth="3", activebackground='grey')
    set_ffmpeg_path.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)

    saved_ffmpeg_path = pathlib.Path(str(config_parser['ffmpeg_path']['path']).replace('"', '')).resolve()
    ffmpeg_entry_box = Entry(ffmpeg_frame, borderwidth=4, background="#CACACA")
    ffmpeg_entry_box.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=N + S + E + W)
    ffmpeg_entry_box.insert(0, str(saved_ffmpeg_path))
    ffmpeg_entry_box.config(state=DISABLED)

    # MPV Path --------------------------------------------------------------------------------------------------------
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
            mpv_cfg_parser = ConfigParser()
            mpv_cfg_parser.read(config_file)
            mpv = f'"{str(pathlib.Path(path))}"'
            mpv_cfg_parser.set('mpv_player_path', 'path', mpv)
            with open(config_file, 'w') as mpv_cfg:
                mpv_cfg_parser.write(mpv_cfg)
            mpv_entry_box.config(state=NORMAL)
            mpv_entry_box.delete(0, END)
            mpv_entry_box.insert(0, str(pathlib.Path(str(
                mpv_cfg_parser['mpv_player_path']['path']).replace('"', '')).resolve()))
            mpv_entry_box.config(state=DISABLED)

    set_mpv_path = HoverButton(mpv_frame, text="Set Path", command=set_mpv_path, foreground="white",
                               background="#23272A", borderwidth="3", activebackground='grey')
    set_mpv_path.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)

    saved_mpv_path = pathlib.Path(str(config_parser['mpv_player_path']['path']).replace('"', '')).resolve()
    mpv_entry_box = Entry(mpv_frame, borderwidth=4, background="#CACACA")
    mpv_entry_box.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=N + S + E + W)
    mpv_entry_box.insert(0, str(saved_mpv_path))
    mpv_entry_box.config(state=DISABLED)

    # Media Info Gui Path ---------------------------------------------------------------------------------------------
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
            mediainfo_cfg_parser = ConfigParser()
            mediainfo_cfg_parser.read(config_file)
            mediainfogui = f'"{str(pathlib.Path(path))}"'
            mediainfo_cfg_parser.set('mediainfogui_path', 'path', mediainfogui)
            with open(config_file, 'w') as mediainfo_cfg:
                mediainfo_cfg_parser.write(mediainfo_cfg)
            mediainfogui_entry_box.config(state=NORMAL)
            mediainfogui_entry_box.delete(0, END)
            mediainfogui_entry_box.insert(0, str(pathlib.Path(str(
                mediainfo_cfg_parser['mediainfogui_path']['path']).replace('"', '')).resolve()))
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

    # FDK-AAC Path ----------------------------------------------------------------------------------------------------
    fdkaac_frame = LabelFrame(path_frame, text=' FDK-AAC ', labelanchor="nw")
    fdkaac_frame.grid(column=0, row=3, columnspan=4, padx=5, pady=(5, 3), sticky=E + W)
    fdkaac_frame.configure(fg="#3498db", bg="#434547", bd=3, font=(set_font, 9, "italic"))
    fdkaac_frame.grid_rowconfigure(0, weight=1)
    fdkaac_frame.grid_columnconfigure(0, weight=1)
    fdkaac_frame.grid_columnconfigure(1, weight=20)
    saved_fdkaac_path = None

    def set_fdk_aac_path():
        path = filedialog.askopenfilename(title='Select Location to "fdkaac.exe"',
                                          initialdir=pathlib.Path(fdkaac_entry_box.get()).parent,
                                          filetypes=[('FDK-AAC', 'fdkaac.exe')], parent=general_settings_window)
        if path:
            fdk_parser = ConfigParser()
            fdk_parser.read(config_file)
            fdkaac = f'"{str(pathlib.Path(path))}"'
            fdk_parser.set('fdkaac_path', 'path', fdkaac)
            with open(config_file, 'w') as fdk_cfg:
                fdk_parser.write(fdk_cfg)
            fdkaac_entry_box.config(state=NORMAL)
            fdkaac_entry_box.delete(0, END)
            fdkaac_entry_box.insert(0, str(pathlib.Path(str(
                fdk_parser['fdkaac_path']['path']).replace('"', '')).resolve()))
            fdkaac_entry_box.config(state=DISABLED)

    set_fdkaac_path = HoverButton(fdkaac_frame, text="Set Path", command=set_fdk_aac_path,
                                  foreground="white", background="#23272A", borderwidth="3", activebackground='grey')
    set_fdkaac_path.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)

    if config_parser['fdkaac_path']['path'] == '':
        saved_fdkaac_path = 'not installed'.title()
    elif config_parser['fdkaac_path']['path'] != '':
        if pathlib.Path(str(config_parser['fdkaac_path']['path']).replace('"', '')).exists():
            saved_fdkaac_path = '"' + str(pathlib.Path(str(config_parser['fdkaac_path']['path']).replace(
                '"', '')).resolve()) + '"'
        else:
            saved_fdkaac_path = 'not installed'.title()
            func_parser = ConfigParser()
            func_parser.read(config_file)
            func_parser.set('fdkaac_path', 'path', '')
            with open(config_file, 'w') as configfile:
                func_parser.write(configfile)

    fdkaac_entry_box = Entry(fdkaac_frame, borderwidth=4, background="#CACACA")
    fdkaac_entry_box.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=N + S + E + W)
    fdkaac_entry_box.insert(0, str(saved_fdkaac_path).replace('"', ''))
    fdkaac_entry_box.config(state=DISABLED)

    # QAAC Path -------------------------------------------------------------------------------------------------------
    qaac_frame = LabelFrame(path_frame, text=' QAAC ', labelanchor="nw")
    qaac_frame.grid(column=0, row=4, columnspan=4, padx=5, pady=(5, 3), sticky=E + W)
    qaac_frame.configure(fg="#3498db", bg="#434547", bd=3, font=(set_font, 9, "italic"))
    qaac_frame.grid_rowconfigure(0, weight=1)
    qaac_frame.grid_rowconfigure(1, weight=1)
    for q_f in range(4):
        qaac_frame.grid_columnconfigure(q_f, weight=1)
    saved_qaac_path = None

    def set_qaac_path():
        path = filedialog.askopenfilename(title='Select Location to "qaac64.exe"',
                                          initialdir=pathlib.Path(qaac_entry_box.get()).parent,
                                          filetypes=[('qaac64', 'qaac64.exe')], parent=general_settings_window)
        if path:
            qaac_parser = ConfigParser()
            qaac_parser.read(config_file)
            qaac = f'"{str(pathlib.Path(path))}"'
            qaac_parser.set('qaac_path', 'path', qaac)
            with open(config_file, 'w') as qaac_cfg:
                qaac_parser.write(qaac_cfg)
            qt_folder_path = pathlib.Path(pathlib.Path(
                str(qaac_parser['qaac_path']['path']).replace('"', '')).resolve().parent / 'QTfiles64')
            qaac_parser.set('qaac_path', 'qt_path', f'"{str(qt_folder_path)}"')
            with open(config_file, 'w') as qaac_cfg:
                qaac_parser.write(qaac_cfg)
            qaac_entry_box.config(state=NORMAL)
            qaac_entry_box.delete(0, END)
            qaac_entry_box.insert(0, str(pathlib.Path(str(
                qaac_parser['qaac_path']['path']).replace('"', '')).resolve()))
            qaac_entry_box.config(state=DISABLED)

            update_qaac_file_paths()

    set_qaac_path = HoverButton(qaac_frame, text="Set Path", command=set_qaac_path,
                                foreground="white", background="#23272A", borderwidth="3", activebackground='grey')
    set_qaac_path.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)

    if config_parser['qaac_path']['path'] == '':
        saved_qaac_path = 'not installed'.title()
    elif config_parser['qaac_path']['path'] != '':
        if pathlib.Path(str(config_parser['qaac_path']['path']).replace('"', '')).exists():
            saved_qaac_path = '"' + str(pathlib.Path(str(config_parser['qaac_path']['path']).replace(
                '"', '')).resolve()) + '"'
        else:
            saved_qaac_path = 'not installed'.title()
            func_parser = ConfigParser()
            func_parser.read(config_file)
            func_parser.set('qaac_path', 'path', '')
            with open(config_file, 'w') as configfile:
                func_parser.write(configfile)

    qaac_entry_box = Entry(qaac_frame, borderwidth=4, background="#CACACA")
    qaac_entry_box.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky=N + S + E + W)
    qaac_entry_box.insert(0, str(saved_qaac_path).replace('"', ''))
    qaac_entry_box.config(state=DISABLED)

    def update_qaac_file_paths():
        global qt_folder, list_of_qaac_files
        update_parser = ConfigParser()
        update_parser.read(config_file)

        qt_folder = pathlib.Path(pathlib.Path(
            str(update_parser['qaac_path']['path']).replace('"', '')).resolve().parent / 'QTfiles64')
        pathlib.Path(qt_folder).mkdir(parents=True, exist_ok=True)

        list_of_qaac_files = [pathlib.Path(qt_folder / 'ASL.dll'),
                              pathlib.Path(qt_folder / 'CoreAudioToolbox.dll'),
                              pathlib.Path(qt_folder / 'CoreFoundation.dll'),
                              pathlib.Path(qt_folder / 'icudt62.dll'),
                              pathlib.Path(qt_folder / 'libdispatch.dll'),
                              pathlib.Path(qt_folder / 'libicuin.dll'),
                              pathlib.Path(qt_folder / 'libicuuc.dll'),
                              pathlib.Path(qt_folder / 'objc.dll')]

    update_qaac_file_paths()

    def check_for_qaac_files():
        global list_of_qaac_files
        checked_qaac_files = []
        for files in list_of_qaac_files:
            checked_qaac_files.append(pathlib.Path(files).is_file())

        if all(checked_qaac_files):
            qaac_status_label.config(text='Status: Ready')
        else:
            qaac_status_label.config(text='Status: Missing QTFiles')

        general_settings_window.after(1000, check_for_qaac_files)

    qaac_status_label = Label(qaac_frame, text="", background="#434547", foreground="white", width=10)
    qaac_status_label.grid(row=1, column=0, columnspan=2, padx=(5, 5), pady=(2, 0), sticky=W + E)
    check_for_qaac_files()

    qt_files_download = HoverButton(qaac_frame, text="Download QTfiles64",
                                    command=lambda: webbrowser.open('https://github.com/AnimMouse/QTFiles/releases'),
                                    foreground="white", background="#23272A", borderwidth="3", activebackground='grey')
    qt_files_download.grid(row=1, column=2, columnspan=1, padx=5, pady=(2, 0), sticky=N + S + E + W)

    qt_files_dir = HoverButton(qaac_frame, text="Open QTfiles64 Directory", command=lambda: webbrowser.open(qt_folder),
                               foreground="white", background="#23272A", borderwidth="3", activebackground='grey')
    qt_files_dir.grid(row=1, column=3, columnspan=1, padx=5, pady=(2, 0), sticky=N + S + E + W)

    # save path frame -------------------------------------------------------------------------------------------------
    save_path_frame = LabelFrame(settings_tab, text=' Save Paths ', labelanchor="n")
    save_path_frame.grid(column=0, row=1, columnspan=4, padx=5, pady=(10, 3), sticky=N + S + E + W)
    save_path_frame.configure(fg="#3498db", bg="#434547", bd=3, font=(set_font, 10, "bold"))
    save_path_frame.grid_rowconfigure(0, weight=1)
    save_path_frame.grid_rowconfigure(1, weight=1)
    for s_p in range(4):
        save_path_frame.grid_columnconfigure(s_p, weight=1)

    # Manual Auto Path ------------------------------------------------------------------------------------------------
    manual_auto_frame = LabelFrame(save_path_frame, text=' Manual/Auto Encode Path ', labelanchor="nw")
    manual_auto_frame.grid(column=0, row=0, columnspan=4, padx=5, pady=(5, 3), sticky=E + W)
    manual_auto_frame.configure(fg="#3498db", bg="#434547", bd=3, font=(set_font, 9, "italic"))
    manual_auto_frame.grid_rowconfigure(0, weight=1)
    manual_auto_frame.grid_columnconfigure(0, weight=2)
    manual_auto_frame.grid_columnconfigure(1, weight=20)
    manual_auto_frame.grid_columnconfigure(3, weight=1)

    def set_manual_auto_path():
        path = filedialog.askdirectory(title='Output Path Manual/Auto', parent=general_settings_window)
        if path:
            manual_path_parser = ConfigParser()
            manual_path_parser.read(config_file)
            path = str(pathlib.Path(path))
            manual_path_parser.set('output_path', 'path', path)
            with open(config_file, 'w') as manual_path_configfile:
                manual_path_parser.write(manual_path_configfile)
            manual_auto_entry_box.config(state=NORMAL)
            manual_auto_entry_box.delete(0, END)
            manual_auto_entry_box.insert(0, str(pathlib.Path(str(manual_path_parser['output_path']['path']))))
            manual_auto_entry_box.config(state=DISABLED)

    set_manual_auto_path = HoverButton(manual_auto_frame, text="Set Path", command=set_manual_auto_path,
                                       foreground="white", background="#23272A", borderwidth="3",
                                       activebackground='grey')
    set_manual_auto_path.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)

    saved_manual_auto_path = None
    if config_parser['output_path']['path'] == 'file input directory':
        saved_manual_auto_path = str(config_parser['output_path']['path']).title()
    elif config_parser['output_path']['path'] != 'file input directory':
        saved_manual_auto_path = str(pathlib.Path(config_parser['output_path']['path']).resolve())
    manual_auto_entry_box = Entry(manual_auto_frame, borderwidth=4, background="#CACACA")
    manual_auto_entry_box.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)
    manual_auto_entry_box.insert(0, saved_manual_auto_path)
    manual_auto_entry_box.config(state=DISABLED)

    def reset_manual_auto_path():
        msg = messagebox.askyesno(title='Prompt', message='Reset path to directory of input file?',
                                  parent=general_settings_window)
        if msg:
            reset_manual_path_parser = ConfigParser()
            reset_manual_path_parser.read(config_file)
            reset_manual_path_parser.set('output_path', 'path', 'file input directory')
            with open(config_file, 'w') as r_mp_cfg:
                reset_manual_path_parser.write(r_mp_cfg)
            manual_auto_entry_box.config(state=NORMAL)
            manual_auto_entry_box.delete(0, END)
            manual_auto_entry_box.insert(0, str(reset_manual_path_parser['output_path']['path']).title())
            manual_auto_entry_box.config(state=DISABLED)

    reset_manual_auto_path = HoverButton(manual_auto_frame, text="X", command=reset_manual_auto_path,
                                         foreground="white", background="#23272A", borderwidth="3",
                                         activebackground='grey')
    reset_manual_auto_path.grid(row=0, column=3, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)

    # Batch Path ------------------------------------------------------------------------------------------------------
    batch_frame = LabelFrame(save_path_frame, text=' Batch Processing Path ', labelanchor="nw")
    batch_frame.grid(column=0, row=1, columnspan=4, padx=5, pady=(5, 3), sticky=E + W)
    batch_frame.configure(fg="#3498db", bg="#434547", bd=3, font=(set_font, 9, "italic"))
    batch_frame.grid_rowconfigure(0, weight=1)
    batch_frame.grid_columnconfigure(0, weight=2)
    batch_frame.grid_columnconfigure(1, weight=20)
    batch_frame.grid_columnconfigure(3, weight=1)

    def set_batch_path():
        path = filedialog.askdirectory(title='Output Path Manual/Auto', parent=general_settings_window)
        if path:
            bath_path_parser = ConfigParser()
            bath_path_parser.read(config_file)
            path = str(pathlib.Path(path))
            bath_path_parser.set('batch_path', 'path', path)
            with open(config_file, 'w') as batch_cfg:
                bath_path_parser.write(batch_cfg)
            batch_entry_box.config(state=NORMAL)
            batch_entry_box.delete(0, END)
            batch_entry_box.insert(0, str(pathlib.Path(str(bath_path_parser['batch_path']['path']))))
            batch_entry_box.config(state=DISABLED)

    set_batch_path_button = HoverButton(batch_frame, text="Set Path", command=set_batch_path,
                                        foreground="white", background="#23272A", borderwidth="3",
                                        activebackground='grey')
    set_batch_path_button.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)

    saved_batch_path = None
    if config_parser['batch_path']['path'] == 'file input directory':
        saved_batch_path = str(config_parser['batch_path']['path']).title()
    elif config_parser['batch_path']['path'] != 'file input directory':
        saved_batch_path = str(pathlib.Path(config_parser['batch_path']['path']).resolve())
    batch_entry_box = Entry(batch_frame, borderwidth=4, background="#CACACA")
    batch_entry_box.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)
    batch_entry_box.insert(0, saved_batch_path)
    batch_entry_box.config(state=DISABLED)

    def reset_batch_path():
        msg = messagebox.askyesno(title='Prompt', message='Reset path to directory of input file?',
                                  parent=general_settings_window)
        if msg:
            reset_batch_path_parser = ConfigParser()
            reset_batch_path_parser.read(config_file)
            reset_batch_path_parser.set('batch_path', 'path', 'file input directory')
            with open(config_file, 'w') as reset_bp_cfg:
                reset_batch_path_parser.write(reset_bp_cfg)
            batch_entry_box.config(state=NORMAL)
            batch_entry_box.delete(0, END)
            batch_entry_box.insert(0, str(reset_batch_path_parser['batch_path']['path']).title())
            batch_entry_box.config(state=DISABLED)

    reset_batch_path_button = HoverButton(batch_frame, text="X", command=reset_batch_path,
                                          foreground="white", background="#23272A", borderwidth="3",
                                          activebackground='grey')
    reset_batch_path_button.grid(row=0, column=3, columnspan=1, padx=5, pady=5, sticky=N + S + E + W)
