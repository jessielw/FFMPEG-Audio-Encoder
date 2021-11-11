# Code needed for Standalone Release-----------------------------------------------------------------------------------
combined_with_ffmpeg_audio_encoder = True  # If combined with FFMPEG...Gui set this to 'True'


# ------------------------------------------------------------------------------------------ Code needed for Standalone

def youtube_dl_launcher_for_ffmpegaudioencoder():
    # Imports----------------------------------------------------------------------------------------------------------
    from tkinter import (filedialog, StringVar, Menu, E, W, N, S, LabelFrame, NORMAL, END,
                         DISABLED, Checkbutton, Label, ttk, scrolledtext, messagebox, OptionMenu,
                         Toplevel, WORD, Entry, Button, HORIZONTAL, SUNKEN, Text)
    import pyperclip, pathlib, threading, yt_dlp
    from re import sub
    from configparser import ConfigParser

    global main

    # --------------------------------------------------------------------------------------------------------- Imports

    # Main Gui & Windows ----------------------------------------------------------------------------------------------
    def main_exit_function():  # Asks if the user is ready to exit
        confirm_exit = messagebox.askyesno(title='Prompt', message="Are you sure you want to exit the program?\n\n"
                                                                   "     Note: This will end all current tasks!",
                                           parent=main)
        if confirm_exit:  # If user selects Yes - destroy window
            main.destroy()

    # Main UI window --------------------------------------------------------------------------------------------------
    try:  # Checks rather or not the youtube-dl-gui window is already open
        if main is not None or Toplevel.winfo_exists(main):
            main.lift()  # If youtube-dl-gui window exists then bring to top of all other windows

    except:  # If youtube-dl-gui does not exist, create it...
        if not combined_with_ffmpeg_audio_encoder:
            from tkinter import Tk, PhotoImage
            main = Tk()  # Make full tkinter loop if standalone
            main.iconphoto(True, PhotoImage(file="Runtime/Images/Youtube-DL-Gui.png"))
        if combined_with_ffmpeg_audio_encoder:
            main = Toplevel()  # Make toplevel loop if NOT standalone
        main.title("Simple-Youtube-DL-Gui v1.1")
        main.configure(background="#434547")
        window_height = 500
        window_width = 600
        screen_width = main.winfo_screenwidth()
        screen_height = main.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        main.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        main.protocol('WM_DELETE_WINDOW', main_exit_function)

        for n in range(4):  # Loop to specify the needed column/row configures
            main.grid_columnconfigure(n, weight=1)
        for n in range(5):
            main.grid_rowconfigure(n, weight=1)

        # The entire top bar/menu is only present during standalone version -------------------------------------------
        if not combined_with_ffmpeg_audio_encoder:
            my_menu_bar = Menu(main, tearoff=0)
            main.config(menu=my_menu_bar)
            file_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
            my_menu_bar.add_cascade(label='File', menu=file_menu)
            file_menu.add_command(label='Exit', command=main_exit_function)  # Exits the program
            options_menu = Menu(my_menu_bar, tearoff=0, activebackground='dim grey')
            my_menu_bar.add_cascade(label='Options', menu=options_menu)

            def set_ffmpeg_path():
                global ffmpeg
                path = filedialog.askopenfilename(title='Select Location to "ffmpeg.exe"', initialdir='/',
                                                  filetypes=[('ffmpeg', 'ffmpeg.exe')])
                if path == '':
                    pass
                elif path != '':
                    ffmpeg = str(pathlib.Path(path))
                    config.set('ffmpeg_path', 'path', ffmpeg)
                    with open(config_file, 'w') as configfile:
                        config.write(configfile)

            options_menu.add_command(label='Set path to FFMPEG', command=set_ffmpeg_path)

            options_menu.add_separator()

            def reset_config():
                msg = messagebox.askyesno(title='Warning',
                                          message='Are you sure you want to reset the config.ini file settings?')
                if not msg:
                    pass
                if msg:
                    try:
                        config.set('ffmpeg_path', 'path', '')
                        with open(config_file, 'w') as configfile:
                            config.write(configfile)
                        messagebox.showinfo(title='Prompt', message='Please restart the program')
                    except:
                        pass
                    main.destroy()

            options_menu.add_command(label='Reset Configuration File', command=reset_config)

            from Packages.about import openaboutwindow

            def open_browser_for_ffmpeg():
                import webbrowser
                webbrowser.open_new_tab('https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z')

            help_menu = Menu(my_menu_bar, tearoff=0, activebackground="dim grey")
            my_menu_bar.add_cascade(label="Help", menu=help_menu)
            help_menu.add_command(label="Download FFMPEG", command=open_browser_for_ffmpeg)
            help_menu.add_separator()
            help_menu.add_command(label="About", command=openaboutwindow)
        # ------------------------------------------- The entire top bar/menu is only present during standalone version

        # Bundled Apps ------------------------------------------------------------------------------------------------
        config_file = 'Runtime/config.ini'  # Defines location of config.ini
        config = ConfigParser()
        config.read(config_file)

        # This creates the config file if on the standalone version ---------------------------------------------------
        if not combined_with_ffmpeg_audio_encoder:
            if not config.has_section('ffmpeg_path'):  # Create config parameters
                config.add_section('ffmpeg_path')
            if not config.has_option('ffmpeg_path', 'path'):
                config.set('ffmpeg_path', 'path', '')
            try:
                with open(config_file, 'w') as configfile:
                    config.write(configfile)
            except:
                messagebox.showinfo(title='Error', message='Could Not Write to config.ini file, delete and try again')
        # --------------------------------------------------- This creates the config file if on the standalone version

        ffmpeg = config['ffmpeg_path']['path']  # Sets path to ffmpeg from config.ini

        # Code needed to add location of ffmpeg.exe in the event it's missing for standalone version -----------------
        if not combined_with_ffmpeg_audio_encoder:
            if not pathlib.Path(ffmpeg).is_file():  # Checks config for bundled app paths path ------------------------
                def check_ffmpeg():  # FFMPEG -------------------------------------------------------------------------
                    global ffmpeg
                    import shutil

                    def write_path_to_ffmpeg():  # Writes path to ffmpeg to the config.ini file
                        try:
                            config.set('ffmpeg_path', 'path', ffmpeg)
                            with open(config_file, 'w') as configfile:
                                config.write(configfile)
                        except:
                            pass

                    if shutil.which('ffmpeg') is not None:
                        ffmpeg = str(pathlib.Path(shutil.which('ffmpeg'))).lower()
                        messagebox.showinfo(title='Prompt!', message='ffmpeg.exe found on system PATH, '
                                                                     'automatically setting path to location.\n\n'
                                                                     'Note: This can be changed in the config.ini file'
                                                                     ' or in the Options menu')
                        if pathlib.Path("Apps/ffmpeg/ffmpeg.exe").is_file():
                            rem_ffmpeg = messagebox.askyesno(title='Delete Included ffmpeg?',
                                                             message='Would you like to delete the included FFMPEG?')
                            if rem_ffmpeg:
                                try:
                                    shutil.rmtree(str(pathlib.Path("Apps/ffmpeg")))
                                except:
                                    pass
                        write_path_to_ffmpeg()
                    elif pathlib.Path("Apps/ffmpeg/ffmpeg.exe").is_file():
                        messagebox.showinfo(title='Info', message='Program will use the included '
                                                                  '"ffmpeg.exe" located in the "Apps" folder')
                        ffmpeg = str(pathlib.Path("Apps/ffmpeg/ffmpeg.exe"))
                        write_path_to_ffmpeg()
                    else:
                        error_prompt = messagebox.askyesno(title='Error!',
                                                           message='Cannot find ffmpeg, '
                                                                   'please navigate to "ffmpeg.exe"')
                        if not error_prompt:
                            messagebox.showerror(title='Error!',
                                                 message='Program requires ffmpeg.exe to work correctly')
                            main.destroy()
                        if error_prompt:
                            set_ffmpeg_path()
                            if not pathlib.Path(ffmpeg).is_file():
                                messagebox.showerror(title='Error!',
                                                     message='Program requires ffmpeg.exe to work correctly')
                                main.destroy()

                check_ffmpeg()  # FFMPEG ------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------------------ Bundled Apps
        # ------------------ Code needed to add location of ffmpeg.exe in the event it's missing for standalone version

        # Link Frame --------------------------------------------------------------------------------------------------
        link_frame = LabelFrame(main, text=' Paste Link ')
        link_frame.grid(row=0, columnspan=4, sticky=E + W, padx=20, pady=(10, 10))
        link_frame.configure(fg="white", bg="#434547", bd=3)

        link_frame.rowconfigure(1, weight=1)
        link_frame.columnconfigure(0, weight=1)
        link_frame.columnconfigure(1, weight=1)

        # -------------------------------------------------------------------------------------------------- Link Frame

        # Options Frame -----------------------------------------------------------------------------------------------
        options_frame = LabelFrame(main, text=' Options ')
        options_frame.grid(row=2, columnspan=4, sticky=E + W, padx=20, pady=(10, 10))
        options_frame.configure(fg="white", bg="#434547", bd=3)

        options_frame.rowconfigure(1, weight=1)
        options_frame.columnconfigure(0, weight=1)
        options_frame.columnconfigure(1, weight=1)

        # ----------------------------------------------------------------------------------------------- Options Frame

        # Input Frame -------------------------------------------------------------------------------------------------
        global link_input_label
        input_frame = LabelFrame(main, text=' Input ')
        input_frame.grid(row=1, columnspan=4, sticky=E + W, padx=20, pady=(4, 10))
        input_frame.configure(fg="white", bg="#434547", bd=3)
        input_frame.rowconfigure(1, weight=1)
        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=1)
        link_input_label = Label(input_frame, text='Please Paste Link Above and Select "Add Link"',
                                 background="#434547", foreground="white", height=1, font=("Helvetica", 10))
        link_input_label.grid(row=0, column=0, columnspan=4, padx=8, pady=(4, 7), sticky=W + E)

        # ------------------------------------------------------------------------------------------------- Input Frame

        # File Output -------------------------------------------------------------------------------------------------
        def file_save():
            global VideoOutput
            save_entry.config(state=NORMAL)  #
            save_entry.delete(0, END)  # This function clears entry box in order to add new link to entry box
            save_entry.config(state=DISABLED)  #
            VideoOutput = filedialog.askdirectory(parent=main)  # Pop up window to choose a save directory location
            if VideoOutput:
                save_for_entry = '"' + VideoOutput + '/"'  # Completes save directory and adds quotes
                save_entry.config(state=NORMAL)  #
                save_entry.insert(0, save_for_entry)  # Adds download_link to entry box
                save_entry.config(state=DISABLED)  #
                start_job_btn.config(state=NORMAL)  # Enables Button

        # ------------------------------------------------------------------------------------------------- File Output

        # Best Video Function -----------------------------------------------------------------------------------------
        def set_video_only():
            if video_only.get() == 'on':  # If video checkbutton is checked enable video options menu and set audio off
                highest_quality_audio_only.set('')
                video_menu_options_menu.config(state=NORMAL)
            if video_only.get() != 'on':  # If not checked, set video_only to on
                video_only.set('on')  # This prevents you from being able to de-select the check button

        # ----------------------------------------------------------------------------------------- Audio Only Function
        def highest_quality_audio_only_toggle():
            if highest_quality_audio_only.get() == 'on':  # If audio checkbutton is checked
                video_only.set('')  # enables video options menu and set audio to off
                video_menu_options_menu.config(state=DISABLED)
            if highest_quality_audio_only.get() != 'on':  # If not checked, set audio_only to on
                highest_quality_audio_only.set('on')  # This prevents you from being able to de-select the check button

        # Video Only Checkbutton --------------------------------------------------------------------------------------
        video_only = StringVar()
        video_only_checkbox = Checkbutton(options_frame, text='Best Video + Audio\nSingle File', variable=video_only,
                                          onvalue='on', offvalue='', command=set_video_only, takefocus=False)
        video_only_checkbox.grid(row=0, column=1, columnspan=1, rowspan=1, padx=10, pady=6, sticky=N + S + E + W)
        video_only_checkbox.configure(background="#434547", foreground="white", activebackground="#434547",
                                      activeforeground="white", selectcolor="#434547", font=("Helvetica", 12))
        video_only.set('on')  # Enables Best Video by default

        # -------------------------------------------------------------------------------------- Video Only Checkbutton

        # Highest Quality Audio Only ----------------------------------------------------------------------------------
        highest_quality_audio_only = StringVar()
        highest_quality_audio_only_checkbox = Checkbutton(options_frame, text='Best Audio Only',
                                                          variable=highest_quality_audio_only, onvalue='on',
                                                          offvalue='', command=highest_quality_audio_only_toggle,
                                                          takefocus=False)
        highest_quality_audio_only_checkbox.grid(row=0, column=2, columnspan=1, rowspan=1, padx=10, pady=3,
                                                 sticky=N + S + E + W)
        highest_quality_audio_only_checkbox.configure(background="#434547", foreground="white",
                                                      activebackground="#434547", activeforeground="white",
                                                      selectcolor="#434547", font=("Helvetica", 12))
        highest_quality_audio_only.set('')  # Disables audio only by default

        # ---------------------------------------------------------------------------------- Highest Quality Audio Only

        # Download Rate -----------------------------------------------------------------------------------------------
        def download_rate_menu_hover(e):
            download_rate_menu["bg"] = "grey"
            download_rate_menu["activebackground"] = "grey"

        def download_rate_menu_hover_leave(e):
            download_rate_menu["bg"] = "#23272A"

        download_rate = StringVar(main)
        download_rate_choices = {'Unlimited': 131072000000000,
                                 '10 - KiB      (Slowest)': 1280,
                                 '50 - KiB': 6400,
                                 '100 - KiB': 12800,
                                 '250 - KiB': 32000,
                                 '500 - KiB': 64000,
                                 '750 - KiB': 96000,
                                 '1 - MiB': 131072,
                                 '5 - MiB': 655360,
                                 '10 - MiB': 1310720,
                                 '30 - MiB': 3932160,
                                 '50 - MiB': 6553600,
                                 '100 - MiB': 13107200,
                                 '250 - MiB': 32768000,
                                 '500 - MiB': 65536000,
                                 '750 - MiB': 98304000,
                                 '1000 - MiB  (Fastest)': 13107200000}
        download_rate_menu_label = Label(options_frame, text="Download Rate :", background="#434547",
                                         foreground="white")
        download_rate_menu_label.grid(row=0, column=0, columnspan=1, padx=10, pady=(3, 10), sticky=W + E)
        download_rate_menu = OptionMenu(options_frame, download_rate, *download_rate_choices.keys())
        download_rate_menu.config(background="#23272A", foreground="white", highlightthickness=1, width=15)
        download_rate_menu.grid(row=1, column=0, columnspan=1, padx=10, pady=(3, 20))
        download_rate.set('Unlimited')
        download_rate_menu["menu"].configure(activebackground="dim grey")
        download_rate_menu.bind("<Enter>", download_rate_menu_hover)
        download_rate_menu.bind("<Leave>", download_rate_menu_hover_leave)

        # ----------------------------------------------------------------------------------------------- Download Rate

        # Video Options -----------------------------------------------------------------------------------------------
        def video_menu_options_menu_hover(e):
            video_menu_options_menu["bg"] = "grey"
            video_menu_options_menu["activebackground"] = "grey"

        def video_menu_options_menu_hover_leave(e):
            video_menu_options_menu["bg"] = "#23272A"

        video_menu_options = StringVar(main)
        video_menu_options_choices = {'(bv+ba/b) Best video + audio format '
                                      'and combine both, or download best combined format': 'bv+ba/b',
                                      '(Same as above with video up to 480p)':
                                          'bv*[height<=480]+ba/b[height<=480] / wv*+ba/w',
                                      '(Same as above with video up to 720p)':
                                          'bv*[height<=720]+ba/b[height<=720] / wv*+ba/w',
                                      '(Same as above with video up to 1080p)':
                                          'bv*[height<=1080]+ba/b[height<=1080] / wv*+ba/w',
                                      '(Same as above with video up to 1440p)':
                                          'bv*[height<=1440]+ba/b[height<=1440] / wv*+ba/w',
                                      '(Same as above with video up to 2160p)':
                                          'bv*[height<=2160]+ba/b[height<=2160] / wv*+ba/w',
                                      '(Default) (bv*+ba/b) Best video and if missing audio, '
                                      'merge it with best available audio': 'bv*+ba/b',
                                      '(bv) Best video only': 'bv',
                                      'Download the best h264 video, '
                                      'or best video if no such codec':
                                          '(bv * +ba / b)[vcodec ^= avc1] / (bv * +ba / b)'}
        video_menu_options_menu = OptionMenu(options_frame, video_menu_options, *video_menu_options_choices.keys())
        video_menu_options_menu.config(background="#23272A", foreground="white", highlightthickness=1,
                                       width=15, anchor=W)
        video_menu_options_menu.grid(row=1, column=1, columnspan=1, padx=10, pady=(3, 20))
        video_menu_options.set('(Default) (bv*+ba/b) Best video and if missing audio, '
                               'merge it with best available audio')
        video_menu_options_menu["menu"].configure(activebackground="dim grey")
        video_menu_options_menu.bind("<Enter>", video_menu_options_menu_hover)
        video_menu_options_menu.bind("<Leave>", video_menu_options_menu_hover_leave)

        # ----------------------------------------------------------------------------------------------- Video Options

        # Add Link to variable ----------------------------------------------------------------------------------------
        def apply_link():
            global download_link, link_input_label, extracted_title_name
            link_entry.config(state=NORMAL)  #
            link_entry.delete(0, END)  # This function clears entry box in order to add new link to entry box
            link_entry.config(state=DISABLED)  #
            download_link = text_area.get(1.0, END).rstrip("\n")  # Pasted download link and strips the unneeded newline
            text_area.delete(1.0, END)  # Deletes entry box where you pasted your link as it stores it into var
            link_entry.config(state=NORMAL)  #
            link_entry.insert(0, download_link)  # Adds download_link to entry box
            link_entry.config(state=DISABLED)  #
            save_btn.config(state=NORMAL)  #
            try:  # The code below checks link input for the title and adds it to a variable for use with the gui
                with yt_dlp.YoutubeDL() as ydl:
                    dl_link_input = ydl.extract_info(download_link, download=False)
                    string_one = sub('[^a-zA-Z0-9 \n]', '', dl_link_input['title'])
                    string_two = " ".join(string_one.split())
                    extracted_title_name = pathlib.Path(string_two[:128]).with_suffix('')
            except:
                extracted_title_name = download_link
            link_input_label.configure(text=extracted_title_name)

        # ---------------------------------------------------------------------------------------------------- Add Link

        # Start Job ---------------------------------------------------------------------------------------------------
        def start_job():  # This is the progress window and everything that has to do with actually processing the file
            global download_link

            def close_encode():
                confirm_exit = messagebox.askyesno(title='Prompt',
                                                   message="Are you sure you want to stop progress?", parent=window)
                if confirm_exit:  # If user selects 'Yes' to the above message prompt, destroy the window in question
                    window.destroy()

            def close_window():  # This thread is needed in order to close the window while the GUI is processing a file
                thread = threading.Thread(target=close_encode)
                thread.start()

            window = Toplevel(main)  # Programs download window
            window.title(extracted_title_name)  # Takes extracted_title_name and adds it as the windows title
            window.configure(background='#434547')
            encode_label = Label(window, text='- ' * 22 + 'Progress ' + '- ' * 22,
                                 font=('Times New Roman', 14), background='#434547', foreground='white')
            encode_label.grid(column=0, columnspan=2, row=0)
            window.grid_columnconfigure(0, weight=1)
            window.grid_rowconfigure(0, weight=1)
            window.grid_rowconfigure(1, weight=1)
            window.protocol('WM_DELETE_WINDOW', close_window)
            window.geometry('600x140')
            encode_window_progress = Text(window, height=2, relief=SUNKEN, bd=3)
            encode_window_progress.grid(row=1, column=0, columnspan=2, pady=(10, 6), padx=10, sticky=E + W)
            encode_window_progress.insert(END, '')
            app_progress_bar = ttk.Progressbar(window, orient=HORIZONTAL, mode='determinate')
            app_progress_bar.grid(row=2, columnspan=2, pady=(10, 10), padx=15, sticky=E + W)

            def my_hook(d):  # This updates the progress bar with the correct percentage
                if d['status'] == 'downloading':
                    p = d['_percent_str']
                    p = p.replace('%', '')
                    app_progress_bar['value'] = float(p)

            class MyLogger:  # ytb-dl logger, allows the program to get all the needed info from the program
                global download_info_string

                def debug(self, msg):
                    # For compatability with youtube-dl, both debug and info are passed into debug
                    # You can distinguish them by the prefix '[debug] '
                    if msg.startswith('[debug] '):
                        pass
                    else:
                        self.info(msg)

                def info(self, msg):
                    encode_window_progress.delete('1.0', END)
                    encode_window_progress.insert(END, msg)

                def warning(self, msg):
                    pass

                def error(self, msg):
                    pass

            if video_only.get() == 'on':  # If "Best Video..." is selected then use these options for ytb-dl
                ydl_opts = {'ratelimit': download_rate_choices[download_rate.get()],
                            'progress_hooks': [my_hook],
                            'noplaylist': True,
                            'overwrites': True,
                            'merge_output_format': 'mkv',
                            'final_ext': 'mkv',
                            'outtmpl': str(pathlib.Path(VideoOutput)) + '/%(title)s.%(ext)s',
                            'ffmpeg_location': str(pathlib.Path(config['ffmpeg_path']['path'])),
                            'logger': MyLogger(),
                            "progress_with_newline": True,
                            'format': video_menu_options_choices[video_menu_options.get()]}
            else:  # If "Best Video..." is NOT selected then use these options for ytb-dl
                ydl_opts = {'ratelimit': download_rate_choices[download_rate.get()],
                            'progress_hooks': [my_hook],
                            'noplaylist': True,
                            'overwrites': True,
                            'outtmpl': str(pathlib.Path(VideoOutput)) + '/%(title)s.%(ext)s',
                            'ffmpeg_location': str(pathlib.Path(config['ffmpeg_path']['path'])),
                            'logger': MyLogger(),
                            "progress_with_newline": True,
                            'format': 'bestaudio/best',
                            'extractaudio': True,
                            'audioformat': 'opus'}

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # Block of code needed to process the link/file
                ydl.download([download_link])

            window.destroy()  # Once the job is complete this destroys the download/processing window

        # --------------------------------------------------------------------------------------------------- Start Job

        # Buttons and Entry Box's -------------------------------------------------------------------------------------
        text_area = scrolledtext.ScrolledText(link_frame, wrap=WORD, width=69, height=1, font=("Times New Roman", 14),
                                              foreground="grey")
        text_area.insert(END, "Right Click or 'Ctrl + V'")
        text_area.grid(row=0, column=0, columnspan=3, pady=(1, 5), padx=10, sticky=W + E)

        # ------------------------------------------------------------------ Right click menu to paste in text_area box
        def paste_clipboard():  # Allows user to paste what ever is in their clipboard with right click and paste
            text_area.delete(1.0, END)
            text_area.config(foreground="black")
            text_area.insert(END, pyperclip.paste())

        def remove_text(e):  # Deletes current text in text box upon 'Left Clicking'
            text_area.config(foreground="black")
            text_area.delete(1.0, END)
            link_input_label.configure(text='Please Paste Link Above and Select "Add Link"')
            link_entry.config(state=NORMAL)  #
            link_entry.delete(0, END)  # This function clears entry box in order to add new link to entry box
            link_entry.config(state=DISABLED)  #

        m = Menu(main, tearoff=0)  # Pop up menu for 'Paste'
        m.add_command(label="Paste", command=paste_clipboard)

        def do_popup(event):  # This code allows the program to know where the cursor is upon right clicking
            try:
                m.tk_popup(event.x_root, event.y_root)
            finally:
                m.grab_release()

        text_area.bind("<Button-3>", do_popup)  # Uses right click to make a function
        text_area.bind("<Button-1>", remove_text)  # Uses left click to make a function
        # Right click menu to paste in text_area box ------------------------------------------------------------------

        link_entry = Entry(link_frame, borderwidth=4, background="#CACACA", state=DISABLED, width=70)
        link_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=(0, 0), sticky=W + E)

        def apply_btn_hover(e):
            apply_btn["bg"] = "grey"

        def apply_btn_hover_leave(e):
            apply_btn["bg"] = "#8b0000"

        apply_btn = Button(link_frame, text="Add Link", command=apply_link, foreground="white", background="#8b0000",
                           width=30)
        apply_btn.grid(row=1, column=0, columnspan=1, padx=10, pady=5, sticky=W)
        apply_btn.bind("<Enter>", apply_btn_hover)
        apply_btn.bind("<Leave>", apply_btn_hover_leave)

        def save_btn_hover(e):
            save_btn["bg"] = "grey"

        def save_btn_hover_leave(e):
            save_btn["bg"] = "#8b0000"

        save_btn = Button(main, text="Save Directory", command=file_save, foreground="white", background="#8b0000",
                          state=DISABLED)
        save_btn.grid(row=4, column=0, columnspan=1, padx=10, pady=(15, 0), sticky=W + E)
        save_btn.bind("<Enter>", save_btn_hover)
        save_btn.bind("<Leave>", save_btn_hover_leave)

        save_entry = Entry(main, borderwidth=4, background="#CACACA", state=DISABLED)
        save_entry.grid(row=4, column=1, columnspan=3, padx=10, pady=(15, 0), sticky=W + E)

        def start_job_btn_hover(e):
            start_job_btn["bg"] = "grey"

        def start_job_btn_hover_leave(e):
            start_job_btn["bg"] = "#8b0000"

        start_job_btn = Button(main, text="Start Job", command=lambda: threading.Thread(target=start_job).start(),
                               foreground="white", background="#8b0000", state=DISABLED)
        start_job_btn.grid(row=5, column=3, columnspan=1, padx=10, pady=(15, 15), sticky=N + S + W + E)
        start_job_btn.bind("<Enter>", start_job_btn_hover)
        start_job_btn.bind("<Leave>", start_job_btn_hover_leave)

        # ------------------------------------------------------------------------------------- Buttons and Entry Box's

        # End Loop ----------------------------------------------------------------------------------------------------
        main.mainloop()
        # ---------------------------------------------------------------------------------------------------- End Loop


# Code needed for Standalone Release----------------------------------------------------------------------------------
if not combined_with_ffmpeg_audio_encoder:
    youtube_dl_launcher_for_ffmpeguaudioencoder()
# ------------------------------------------------------------------------------------------ Code needed for Standalone
