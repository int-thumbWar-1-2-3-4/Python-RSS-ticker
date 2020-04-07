import tkinter as tk
from controller.title_loop import ten_second_loop
from view.main_view import MainView


def execute(feed, seconds):
    root = tk.Tk()
    mainView = MainView(master=root)

    ten_second_loop(mainView, seconds, feed)

    # KEEP THIS LAST
    mainView.mainloop()
