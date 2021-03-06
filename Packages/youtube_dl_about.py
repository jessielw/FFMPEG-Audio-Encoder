from tkinter import *

# About Window --------------------------------------------------------------------------------------------------------
def openaboutwindow():
    about_window = Toplevel()
    about_window.title('About')
    about_window.configure(background="#434547")
    window_height = 140
    window_width = 470
    screen_width = about_window.winfo_screenwidth()
    screen_height = about_window.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (window_width / 2))
    y_coordinate = int((screen_height / 2) - (window_height / 2))
    about_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
    about_window_text = Text(about_window, background="#434547", foreground="white", relief=SUNKEN)
    about_window_text.pack()
    about_window_text.configure(state=NORMAL)
    about_window_text.insert(INSERT, "Youtube-DL-Gui v1.1 \n")
    about_window_text.insert(INSERT, "\n")
    about_window_text.insert(INSERT, "Development: jlw4049")
    about_window_text.insert(INSERT, "\n\n")
    about_window_text.insert(INSERT, "Youtube audio/video downloader. \n")
    about_window_text.configure(state=DISABLED)


# -------------------------------------------------------------------------------------------------------- About Window