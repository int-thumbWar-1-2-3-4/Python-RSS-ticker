import tkinter as tk
from controller.title_loop import ten_second_loop
from model.model import Model
from view.main_view import MainView

root = tk.Tk()
mainView = MainView(master=root)

model = Model(mainView)
model.load_entries("https://www.theguardian.com/us/rss")

# Thread setup, execution and termination
ten_second_loop(mainView)

# KEEP THIS LAST
mainView.mainloop()
