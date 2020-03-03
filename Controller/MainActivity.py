import tkinter as tk
import feedparser
import time

class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.winfo_toplevel().title("Python RSS Ticker")
        self.pack()

        self.load_articles()
        self.create_widgets()

    articles = {}

    def create_widgets(self):
        self.content_label = tk.Label(self)
        self.content_label["text"] = list(self.articles.keys())[0]
        self.content_label.pack(side="top")


    def load_articles(self):
        d = feedparser.parse('https://www.theguardian.com/world/rss')
        for entry in d.entries:
            self.articles[entry.title] = entry.link



root = tk.Tk()
app = Application(master=root)
app.mainloop()