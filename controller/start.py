import tkinter as tk

from controller.title_loop import ten_second_loop
from controller.argument_parser import ticker_argument_parser
from view.main_view import MainView
from model.parser import parse_url_feed
from model.feed_manager import parse

def main():
    arguments = ticker_argument_parser()
    feed = parse(arguments.url[0])
    feed.reverse()
    ten_second_loop(mainView, arguments.timer, feed)



if __name__ == "__main__":
    root = tk.Tk()
    mainView = MainView(master=root)

    main()

    # KEEP THIS LAST
    mainView.mainloop()
