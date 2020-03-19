import tkinter as tk

from model.model import Model
from view.main_view import MainView

root = tk.Tk()
mainView = MainView(master=root)

model = Model(mainView)
model.load_entries("https://www.theguardian.com/us/rss")
model.switch_displayed_entry()

# KEEP THIS LAST
mainView.mainloop()