import tkinter as tk
import webbrowser
from tkinter import *


class MainView(tk.Frame):
    # Shows a single entry from a feed

    entry_title = "[BLANK Entry Title]"
    entry_link = "[BLANK Entry Link]"

    def __init__(self, master=None):
        """ Constructor for view.MainView. """

        super().__init__(master)
        self.master = master
        self.content_label = tk.Label(self, cursor="gumby")

        self.pack()
        self.build_window()
        self.menu_bar()

    def menu_bar(self):
        """ View.MainView.menu_bar adds a drop down menu for our tk window. """

        self.menubar = tk.Menu(self)

        self.dropdown_menu = tk.Menu(self.menubar, tearoff=0)
        self.dropdown_menu.add_command(label='white', command=self.bg_white)
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
        self.font_menu.add_command(label='12', command=self.font_12)
        self.font_menu.add_command(label='13', command=self.font_13)
        self.menubar.add_cascade(label='Font size', menu=self.font_menu)

        self.font_color = tk.Menu(self.menubar)
        self.font_color.add_command(label='red', command=self.font_red)
        self.font_color.add_command(label='blue', command=self.font_blue)
        self.font_color.add_command(label='yellow', command=self.font_yellow)
        self.menubar.add_cascade(label='Font color', menu=self.font_color)

    def font_red(self):
        """ View.MainView.font_red sets font color to red. """

        self.content_label['fg'] = 'red'

    def font_yellow(self):
        """ View.MainView.font_yellow sets font color to yellow. """

        self.content_label['fg'] = 'yellow'

    def font_blue(self):
        """ View.MainView.font_blue sets font color to blue. """

        self.content_label['fg'] = 'blue'

    def font_8(self):
        """ View.MainView.font_8 sets font size to 8. """

        self.content_label['font'] = 'times 8'

    def font_9(self):
        """ View.MainView.font_9 sets font size to 9. """

        self.content_label['font'] = 'times 9'

    def font_10(self):
        """ View.MainView.font_10 sets font size to 10. """

        self.content_label['font'] = 'times 10'

    def font_11(self):
        """ View.MainView.font_11 sets font size to 11. """

        self.content_label['font'] = 'times 11'

    def font_12(self):
        """ View.MainView.font_12 sets font size to 12. """

        self.content_label['font'] = 'times 12'

    def font_13(self):
        """ View.MainView.font_13 sets font size to 13. """

        self.content_label['font'] = 'times 13'

    def bg_white(self):
        """ View.MainView.bg_white sets background color to white. """

        self.content_label['bg'] = 'white'

    def red_color(self):
        """ View.MainView.bg_red sets background color to white. """

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
