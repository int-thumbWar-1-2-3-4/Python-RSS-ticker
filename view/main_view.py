import tkinter as tk


class MainView(tk.Frame):
    # Shows a single entry from a feed

    __entry_title = "[BLANK Entry Title]"
    __entry_link = "[BLANK Entry Link]"

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.winfo_toplevel().title("Python RSS Ticker")

        self.content_label = tk.Label(self)
        self.content_label.pack(side="top")
        self.content_label["text"] = self.__entry_title

        self.pack()

    def display_entry(self, entry_title: str, entry_link: str):
        # Changes the entry displayed.

        self.__entry_title = entry_title
        self.__entry_link = entry_link

        self.content_label["text"] = self.__entry_title
        self.content_label.update()
