import tkinter as tk
import webbrowser
from tkinter import *

class MainView(tk.Frame):
    # Shows a single entry from a feed

    entry_title = "[BLANK Entry Title]"
    entry_link = "[BLANK Entry Link]"

    def __init__(self, master=None):
        """ Constructor """
        super().__init__(master)
        self.master = master
        self.content_label = tk.Label(self, cursor="gumby")

        self.pack()
        self.build_window()
        self.menubar()

    def menubar(self):
        self.menubar = tk.Menu(self)

        self.dropdown_menu = tk.Menu(self.menubar, tearoff=0)
        self.dropdown_menu.add_command(label='white', command=self.white_color)
        self.dropdown_menu.add_command(label='red', command=self.red_color)
        self.dropdown_menu.add_command(label='blue', command=self.blue_color)
        self.dropdown_menu.add_command(label='green', command=self.green_color)
        self.menubar.add_cascade(label='bg color', menu=self.dropdown_menu)
        self.master.config(menu=self.menubar)

        self.font_menu = tk.Menu(self.menubar)
        self.font_menu.add_command(label='8', command=self.font_8)
        self.font_menu.add_command(label='9', command=self.font_9)
        self.font_menu.add_command(label='10', command=self.font_10)
        self.font_menu.add_command(label='11', command=self.font_11)
        self.menubar.add_cascade(label='font size', menu=self.font_menu)

    def font_8(self):
        self.content_label['font'] = 'times 8'
    def font_9(self):
        self.content_label['font'] = 'times 9'
    def font_10(self):
        self.content_label['font'] = 'times 10'
    def font_11(self):
        self.content_label['font'] = 'times 11'


    def white_color(self):
        self.content_label['bg'] = 'white'

    def red_color(self):
        self.content_label['bg'] = 'red'

    def blue_color(self):
        self.content_label['bg'] = 'blue'

    def green_color(self):
        self.content_label['bg'] = 'green'

    def build_window(self):
        self.winfo_toplevel().title("Python RSS Ticker")

        self.content_label.pack(side="top")
        self.content_label["text"] = self.entry_title
        self.content_label.bind("<Button-1>",
                                lambda event,
                                       content_label=self.entry_link:
                                self.open_article(self.entry_link))
        self.pack()

    def display_entry(self, entry_title: str, entry_link: str):
        # Changes the entry displayed.

        self.entry_title = entry_title
        self.entry_link = entry_link

        self.content_label["text"] = self.entry_title
        self.content_label.update()

    def open_article(self, link):
        webbrowser.open_new(link)
        self.content_label.update()