from tkinter import *
import UI.userinterface
# root window created. Here, that would be the only window, but
# you can later have windows within windows.
from UI import userinterface

root = Tk()

root.geometry("400x300")

# creation of an instance
app = userinterface.Window(root)

# mainloop
root.mainloop()