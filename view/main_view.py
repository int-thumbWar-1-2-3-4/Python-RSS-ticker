import tkinter as tk
import webbrowser


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
        self.dropdown_menu.add_command(label='red', command=self.red_color)
        self.menubar.add_cascade(label='bg color', menu=self.dropdown_menu)
        self.master.config(menu=self.menubar)

    def red_color(self):
        self.content_label['bg'] = 'red'

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
