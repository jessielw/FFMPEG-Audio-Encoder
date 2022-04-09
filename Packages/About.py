from tkinter import Toplevel, INSERT, Text, NORMAL, DISABLED, messagebox, SUNKEN


# About Window --------------------------------------------------------------------------------------------------------
def openaboutwindow():
    global about_window

    try:  # If "About" window is already opened, display a message, then close the "About" window
        if about_window.winfo_exists():
            messagebox.showinfo(title=f'"{about_window.wm_title()}" Info!', parent=about_window,
                                message=f'"{about_window.wm_title()}" is already opened, closing window instead')
            about_window.destroy()
            return
    except NameError:
        pass

    about_window = Toplevel()
    about_window.title('About')
    about_window.configure(background="#434547")
    window_height = 140
    window_width = 470
    screen_width = about_window.winfo_screenwidth()
    screen_height = about_window.winfo_screenheight()
    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))
    about_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
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
