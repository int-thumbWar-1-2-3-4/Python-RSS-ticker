import tkinter as tk
from controller.title_loop import ten_second_loop
from view.main_view import MainView
from tkinter import *

root = tk.Tk()
mainView = MainView(master=root)


ten_second_loop(mainView, 5)

# KEEP THIS LAST
mainView.mainloop()
