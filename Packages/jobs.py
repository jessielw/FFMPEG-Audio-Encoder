import pathlib
from tkinter import *
from tkinter import messagebox, font

root = Tk()
root.configure(background="#434547")
root.resizable(False, False)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

detect_font = font.nametofont("TkDefaultFont")  # Get default font value into Font object
set_font = detect_font.actual().get("family")
set_font_size = detect_font.actual().get("size")


my_frame = Frame(root)
my_frame.grid(column=0, row=0, padx=5, pady=5, sticky=N+S+E+W)

right_scrollbar = Scrollbar(my_frame, orient=VERTICAL)

bottom_scrollbar = Scrollbar(my_frame, orient=HORIZONTAL)

my_listbox = Listbox(my_frame, width=100, height=20, xscrollcommand=bottom_scrollbar, activestyle="none",
                     yscrollcommand=right_scrollbar.set, bd=2, bg="#636669", fg='white', selectbackground='light grey',
                     font=(set_font, set_font_size + 2))
my_listbox.grid(row=0, column=0)

right_scrollbar.config(command=my_listbox.yview)
right_scrollbar.grid(row=0, column=1, sticky=N+E+S)

bottom_scrollbar.config(command=my_listbox.xview)
bottom_scrollbar.grid(row=1, column=0, sticky=W+E+S)

button_frame = Frame()
button_frame.grid(column=1, row=0, sticky=N + S + E + W)
button_frame.config(bg="#434547")
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_rowconfigure(0, weight=1)
button_frame.grid_rowconfigure(1, weight=300)
button_frame.grid_rowconfigure(2, weight=300)
button_frame.grid_rowconfigure(3, weight=1)


def delete():
    msg = messagebox.askyesno(title='Prompt!', message='Delete selected item?')
    if msg:
        for selected_items in reversed(my_listbox.curselection()):
            my_listbox.delete(selected_items)


delete_job_button = Button(button_frame, text="Delete Selected", command=delete, state=DISABLED, foreground="white",
                           background="#23272A", borderwidth="3", activebackground='grey')
delete_job_button.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=N + E + W)


def delete_all():
    msg = messagebox.askyesno(title='Prompt!', message='Delete all items?')
    if msg:
        my_listbox.delete(0, END)


delete_all_button = Button(button_frame, text="Delete All", command=delete_all, foreground="white",
                           background="#23272A", borderwidth="3", activebackground='grey')
delete_all_button.grid(row=1, column=0, columnspan=1, padx=5, pady=(5, 5), sticky=N + E + W)

start_selected_button = Button(button_frame, text="Start Selected Job", command=None, state=DISABLED,
                               foreground="white", background="#23272A", borderwidth="3", activebackground='grey')
start_selected_button.grid(row=2, column=0, columnspan=1, padx=5, pady=5, sticky=S + E + W)

start_audio_button = Button(button_frame, text="Start All Jobs", command=None, state=DISABLED, foreground="white",
                            background="#23272A", borderwidth="3", activebackground='grey')
start_audio_button.grid(row=6, column=0, columnspan=1, padx=5, pady=5, sticky=S + E + W)


def popup_menu(e):
    option_menu = Menu(my_frame, tearoff=False)  # Menu
    option_menu.add_command(label='Delete Selection', command=delete)
    option_menu.add_command(label='Delete All', command=delete_all)
    option_menu.add_separator()
    option_menu.add_command(label='Start Selected Job', command=None)
    option_menu.add_command(label='Start All Jobs', command=None)
    option_menu.tk_popup(e.x_root, e.y_root)  # This gets the position of 'e' on the root widget


my_listbox.bind('<Button-3>', popup_menu)  # Right click to pop up menu in frame

file1 = r"C:\Users\jlw_4\Desktop\Avatar The Last Airbender - 1x01 - The Boy in the Iceberg.mkv"
codec = 'ac3'
my_listbox.insert(END, f'Codec: {codec.upper()}  >>>>  "{pathlib.Path(file1).name}"')
# for item in range(30):
#     my_listbox.insert(END, item)
#
# my_listbox.insert(END, ' - ' * 100)

root.mainloop()
