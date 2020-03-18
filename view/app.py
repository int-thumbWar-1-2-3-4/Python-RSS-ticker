from tkinter import *

# root window created. Here, that would be the only window, but
# you can later have windows within windows.


def whereAmI():
    return 'Inside app.py'


root = Tk()

root.geometry("400x300")

# creation of an instance
app = ui.Window(root)

# mainloop
root.mainloop()
