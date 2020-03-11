# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 17:00:38 2020

@author: chen liang
"""
from tkinter import *
import webbrowser
import feedparser
import time
import tkinter as tk

root = tk.Tk()

feed = feedparser.parse("http://rss.cnn.com/rss/cnn_us.rss")

def callback(event,link):
    webbrowser.open_new(link)

for entry in feed.entries:
    article_title = entry.title
    article_link = entry.link
    link = tk.Label(root, text=article_title, fg="blue", cursor="hand2")
    link.pack()
    link.bind("<Button-1>", lambda event, link=article_link: callback(event, link))
    root.update()
    time.sleep(3)
root.mainloop()



