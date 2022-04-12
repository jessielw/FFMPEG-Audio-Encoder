from tkinter import Toplevel, INSERT, Text, NORMAL, DISABLED, messagebox, SUNKEN
from configparser import ConfigParser


# About Window --------------------------------------------------------------------------------------------------------
def openaboutwindow():
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
        if config['save_window_locations']['about'] == 'yes':  # If auto save position on close is checked
            try:
                if config['save_window_locations']['about position'] != about_window.geometry():
                    config.set('save_window_locations', 'about position', about_window.geometry())
                    with open(config_file, 'w') as configfile:
                        config.write(configfile)
            except (Exception,):
                pass

        about_window.destroy()  # Close window

    about_window = Toplevel()
    about_window.title('About')
    about_window.configure(background="#434547")
    if config['save_window_locations']['about position'] == '' or config['save_window_locations']['about'] == 'no':
        window_height = 140
        window_width = 470
        screen_width = about_window.winfo_screenwidth()
        screen_height = about_window.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        about_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
    elif config['save_window_locations']['about position'] != '' and config['save_window_locations']['about'] == 'yes':
        about_window.geometry(config['save_window_locations']['about position'])
    about_window.protocol('WM_DELETE_WINDOW', about_exit_function)
    about_window_text = Text(about_window, background="#434547", foreground="white", relief=SUNKEN)
    about_window_text.pack()
    about_window_text.configure(state=NORMAL)
    about_window_text.insert(INSERT, "FFMPEG Audio Encoder\n")
    about_window_text.insert(INSERT, "\n")
    about_window_text.insert(INSERT, "Development: jlw4049\n\nContributors: BassThatHertz, aaronrausch")
    about_window_text.insert(INSERT, "\n\n")
    about_window_text.insert(INSERT, "A lightweight audio encoder based off of FFMPEG. \n")
    about_window_text.configure(state=DISABLED)

# -------------------------------------------------------------------------------------------------------- About Window
