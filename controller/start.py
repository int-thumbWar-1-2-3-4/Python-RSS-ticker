import tkinter as tk
import threading as th
from queue import Queue
from model.model import Model
from model.feedparser import get_titles_links
from view.main_view import MainView

root = tk.Tk()
mainView = MainView(master=root)

model = Model(mainView)
model.load_entries("https://www.theguardian.com/us/rss")

# These line grab test data from model.feedparser. This only temporary.
# Eventually I believe that model.model should have a function that returns a
# similar list
test_feed = get_titles_links()
test_feed.reverse()

def ten_second_loop():
    """
    Python-RSS-ticker.controller.start.ten_second_loop spawns a thread every 10
    seconds which calls call_switch_display
    """
    looping_thread = th.Timer(10, ten_second_loop)
    looping_thread.daemon = True
    looping_thread.start()
    call_switch_display()



def call_switch_display():
    """ Python-RSS-ticker.controller.start.call_switch_display calls
    model.model.switch_displayed_entry """
    temp_tuple = test_feed.pop()
    mainView.display_entry(temp_tuple[0], temp_tuple[1])


# Thread setup, execution and termination
ten_second_loop()

# KEEP THIS LAST
mainView.mainloop()
