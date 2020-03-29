import time
import tkinter as tk
import threading as th
from model.model import Model
from view.main_view import MainView
from concurrent.futures import ThreadPoolExecutor

root = tk.Tk()
mainView = MainView(master=root)

model = Model(mainView)
model.load_entries("https://www.theguardian.com/us/rss")


def ten_second_loop():
    """
    Python-RSS-ticker.controller.start.ten_second_loop spawns a thread every 10
    seconds which calls call_switch_display
    """
    red_thread = th.Timer(10, ten_second_loop)
    red_thread.daemon = True
    red_thread.start()
    call_switch_display()

def call_switch_display():
    """ Python-RSS-ticker.controller.start.call_switch_display calls
    model.model.switch_displayed_entry """
    model.switch_displayed_entry()


# Thread setup, execution and termination
ten_second_loop()

# KEEP THIS LAST
mainView.mainloop()
