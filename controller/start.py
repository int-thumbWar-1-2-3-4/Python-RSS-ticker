import tkinter as tk
from controller.title_loop import ten_second_loop
from model.feed_manager import Feed_Manager
from view.main_view import MainView

root = tk.Tk()
mainView = MainView(master=root)

model = Feed_Manager(mainView)
model.load_entries("https://www.theguardian.com/us/rss")

# This is a call to controller.title_loop with the view and the amount of
# time between ticker changes
ten_second_loop(mainView, 5)

# KEEP THIS LAST
mainView.mainloop()
