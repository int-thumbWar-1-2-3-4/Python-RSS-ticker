import tkinter as tk
import webbrowser
from tkinter import *
from tkinter.font import Font





class MainView(tk.Frame):

    # Shows a single entry from a feed

    entry_title = "[BLANK Entry Title]"
    entry_link = "[BLANK Entry Link]"

    def __init__(self, master=None):
        """ Constructor """
        super().__init__(master)
        self.master = master
        self.label_text = StringVar()
        self.set_font = Font(family="Times New Roman", size=12)
        self.content_label = tk.Label(self, cursor="gumby", font=self.set_font)
        self.pack()
        self.build_window(master)



    def build_window(self, top):

        # Adding a drop down menu
        make_menu= Menu(top)
        top.config(menu=make_menu)

        # Create menu items


        # Rotation time.
        rotate_time = Menu(make_menu)
        make_menu.add_cascade(label="Time", menu=rotate_time)

        # Font Style
        font_menu = Menu(make_menu)
        make_menu.add_cascade(label="Font Style", menu=font_menu)

        # Font size
        size_menu = Menu(make_menu)
        make_menu.add_cascade(label="Font size", menu=size_menu)
        size_menu.add_command(label="8", command=MainView.change_size(self, self.set_font, 8))
        size_menu.add_command(label="9", command=MainView.change_size(self, self.set_font, 9))
        size_menu.add_command(label="10", command=MainView.change_size(self, self.set_font, 10))
        size_menu.add_command(label="11", command=MainView.change_size(self, self.set_font, 11))
        size_menu.add_command(label="12", command=MainView.change_size(self, self.set_font, 12))

        # Font color
        color_menu = Menu(make_menu)
        make_menu.add_cascade(label="Font color", menu=color_menu)

        # Background color
        bg_color_menu = Menu(make_menu)
        make_menu.add_cascade(label="BG color", menu=bg_color_menu)

        # Url lists
        url_menu = Menu(make_menu)
        make_menu.add_cascade(label="URL", menu=url_menu)


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

    @staticmethod
    def change_size(self, font_obj, obj_size):
        font_obj.config(size=obj_size)
        return font_obj

