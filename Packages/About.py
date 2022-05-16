from configparser import ConfigParser
from tkinter import Toplevel, INSERT, Text, DISABLED, messagebox, FLAT, N, E, W, S, font, LabelFrame


# About Window --------------------------------------------------------------------------------------------------------
def openaboutwindow(main_root_title):
    global about_window

    # Defines the path to config.ini and opens it for reading/writing
    config_file = 'Runtime/config.ini'  # Creates (if doesn't exist) and defines location of config.ini
    config = ConfigParser()
    config.read(config_file)

    try:  # If "About" window is already opened, display a message, then close the "About" window
        if about_window.winfo_exists():
            messagebox.showinfo(title=f'"{about_window.wm_title()}" Info!', parent=about_window,
                                message=f'"{about_window.wm_title()}" is already opened, closing window instead')
            about_window.destroy()
            return
    except NameError:
        pass

    def about_exit_function():  # Exit function when hitting the 'X' button
        func_parser = ConfigParser()
        func_parser.read(config_file)
        if func_parser['save_window_locations']['about'] == 'yes':  # If auto save position on close is checked
            try:
                if func_parser['save_window_locations']['about position'] != about_window.geometry():
                    func_parser.set('save_window_locations', 'about position', about_window.geometry())
                    with open(config_file, 'w') as configfile:
                        func_parser.write(configfile)
            except (Exception,):
                pass

        about_window.destroy()  # Close window

    about_window = Toplevel()
    about_window.title('About')
    about_window.configure(background="#434547")
    if config['save_window_locations']['about position'] == '' or config['save_window_locations']['about'] == 'no':
        window_height = 650
        window_width = 720
        screen_width = about_window.winfo_screenwidth()
        screen_height = about_window.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        about_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
    elif config['save_window_locations']['about position'] != '' and config['save_window_locations']['about'] == 'yes':
        about_window.geometry(config['save_window_locations']['about position'])
    about_window.resizable(False, False)
    about_window.protocol('WM_DELETE_WINDOW', about_exit_function)

    about_window.grid_columnconfigure(0, weight=1)

    detect_font = font.nametofont("TkDefaultFont")  # Get default font value into Font object
    set_font = detect_font.actual().get("family")

    about_information_frame = LabelFrame(about_window, text=' About ', labelanchor="nw")
    about_information_frame.grid(column=0, row=0, columnspan=1, padx=5, pady=(0, 3), sticky=N + S + E + W)
    about_information_frame.configure(fg="#3498db", bg="#434547", bd=3, font=(set_font, 10, "bold"))
    about_information_frame.grid_rowconfigure(0, weight=1)
    about_information_frame.grid_columnconfigure(0, weight=1)

    about_window_text = Text(about_information_frame, background="#434547", foreground="white", relief=FLAT, height=10)
    about_window_text.pack()
    about_window_text.insert(INSERT, f"{main_root_title}\n")
    about_window_text.insert(INSERT, "\n")
    about_window_text.insert(INSERT, "Development: jlw4049\n\nContributors: BassThatHertz, aaronrausch")
    about_window_text.insert(INSERT, "\n\n")
    about_window_text.insert(INSERT, "Power audio encoding GUI, that mostly uses FFMPEG at the heart. \n")
    about_window_text.configure(state=DISABLED)

    about_information_frame = LabelFrame(about_window, text=' License ', labelanchor="nw")
    about_information_frame.grid(column=0, row=1, columnspan=1, padx=5, pady=(0, 3), sticky=N + S + E + W)
    about_information_frame.configure(fg="#3498db", bg="#434547", bd=3, font=(set_font, 10, "bold"))
    about_information_frame.grid_rowconfigure(0, weight=1)
    about_information_frame.grid_columnconfigure(0, weight=1)

    license_text = """
    Copyright (c) 2012-2022 Scott Chacon and others

    Permission is hereby granted, free of charge, to any person obtaining
    a copy of this software and associated documentation files (the
    "Software"), to deal in the Software without restriction, including
    without limitation the rights to use, copy, modify, merge, publish,
    distribute, sublicense, and/or sell copies of the Software, and to
    permit persons to whom the Software is furnished to do so, subject to
    the following conditions:
    
    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
    LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
    OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
    WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    """

    about_window_license = Text(about_information_frame, background="#434547", foreground="white", relief=FLAT)
    about_window_license.pack(anchor='center')
    about_window_license.insert(INSERT, license_text)
    about_window_license.configure(state=DISABLED)

# -------------------------------------------------------------------------------------------------------- About Window
