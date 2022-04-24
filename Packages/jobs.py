from tkinter import *
from tkinter import messagebox

root = Tk()
root.configure(background="#434547")
# root.geometry("400x300")


my_frame = Frame(root)
my_frame.grid(column=0, row=0, padx=5, pady=5)

right_scrollbar = Scrollbar(my_frame, orient=VERTICAL)

bottom_scrollbar = Scrollbar(my_frame, orient=HORIZONTAL)

my_listbox = Listbox(my_frame, width=50, xscrollcommand=bottom_scrollbar, yscrollcommand=right_scrollbar.set, bd=2,
                     bg="#636669", fg='white', selectbackground='light grey')
my_listbox.grid(row=0, column=0)

right_scrollbar.config(command=my_listbox.yview)
right_scrollbar.grid(row=0, column=1, sticky=N + E + S)

bottom_scrollbar.config(command=my_listbox.xview)
bottom_scrollbar.grid(row=1, column=0, sticky=W + E + S)

button_frame = Frame()
button_frame.grid(column=1, row=0)
button_frame.config(bg="#434547")
for x_button in range(3):
    button_frame.grid_rowconfigure(x_button, weight=1)


def delete():
    msg = messagebox.askyesno(title='Prompt!', message='Delete selected item?')
    if msg:
        for selected_items in reversed(my_listbox.curselection()):
            my_listbox.delete(selected_items)


delete_job_button = Button(button_frame, text="Delete Selected",
                           command=delete, state=DISABLED, foreground="white",
                           background="#23272A", borderwidth="3", activebackground='grey')
delete_job_button.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=N + E + W)


def delete_all():
    msg = messagebox.askyesno(title='Prompt!', message='Delete all items?')
    if msg:
        my_listbox.delete(0, END)


delete_all_button = Button(button_frame, text="Delete All",
                           command=delete_all, foreground="white",
                           background="#23272A", borderwidth="3", activebackground='grey')
delete_all_button.grid(row=1, column=0, columnspan=1, padx=5, pady=(5, 60), sticky=N + E + W)

start_selected_button = Button(button_frame, text="Start Selected Job",
                               command=None, state=DISABLED, foreground="white",
                               background="#23272A", borderwidth="3", activebackground='grey')
start_selected_button.grid(row=2, column=0, columnspan=1, padx=5, pady=5, sticky=S + E + W)

start_audio_button = Button(button_frame, text="Start All Jobs",
                            command=None, state=DISABLED, foreground="white",
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

for item in range(30):
    my_listbox.insert(END, item)

my_listbox.insert(END, ' - ' * 100)

root.mainloop()
