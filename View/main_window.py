import tkinter as tk
import feedparser
import time

class Application(tk.Frame):

    articles = {}

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.winfo_toplevel().title("Python RSS Ticker")
        self.pack()

        self.load_articles()
        self.create_widget()


    def create_widget(self):
        self.content_label = tk.Label(self)
        self.content_label["text"] = list(self.articles.keys())[0]
        self.content_label.pack(side="top")


    def load_articles(self):
        feed = feedparser.parse('https://www.theguardian.com/world/rss')
        for entry in feed.entries:
            self.articles[entry.title] = entry.link

root = tk.Tk()
app = Application(master=root)
app.mainloop()