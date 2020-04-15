import tkinter as tk

from controller.title_loop import ten_second_loop
from controller.argument_parser import ticker_argument_parser
from view.main_view import MainView
from model.parser import parse_url_feed
from model.feed_manager import parse


if __name__ == "__main__":
    arguments = ticker_argument_parser()
    feed = parse(arguments.url[0])
    feed.reverse()

    root = tk.Tk()
    mainView = MainView(master=root)

    ten_second_loop(mainView, arguments.timer, feed)

    # KEEP THIS LAST
    mainView.mainloop()
