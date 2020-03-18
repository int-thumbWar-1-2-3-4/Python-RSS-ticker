import tkinter as tk
import feedparser

class MainWindow(tk.Frame):

    articles = {}

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.winfo_toplevel().title("Python RSS Ticker")
        self.pack()

        self.load_entries()
        self.create_widget()


    def create_widget(self):
        self.content_label = tk.Label(self)
        self.content_label["text"] = list(self.articles.keys())[0]
        self.content_label.pack(side="top")


    def load_entries(self):
        feed = feedparser.parse('https://www.theguardian.com/world/rss')
        for entry in feed.entries:
            self.articles[entry.title] = entry.link
