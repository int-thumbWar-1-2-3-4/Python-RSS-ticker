import tkinter as tk


class MenuBar(tk.Menu):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.menubar = tk.Menu(self)
        self.dropdown_menu = tk.Menu(self.menubar)

    def background_color(self):
        self.dropdown_menu.add(label='red', command=red_color)
        self.content_label.config(menu=self.menubar)

    def red_color(self):
        self.content_label['bg'] = 'red'
