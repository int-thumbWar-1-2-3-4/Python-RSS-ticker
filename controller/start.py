import argparse
import tkinter as tk
import threading as th
from view.main_view import MainView
from model.parser import parse_url_feed
from model.feed_manager import parse


def ticker_argument_parser():
    parser = argparse.ArgumentParser(description="Select a file or feed to parse.")
    parser.add_argument('--url', dest='url', action='store', default=["https://www.theguardian.com/us/rss"],
                        help="enter a url of an RSS or ATOM feed to parse", nargs='*')
    parser.add_argument('--file', dest='file', action='store', default="",
                        help="enter a file name to parse", nargs='*')
    parser.add_argument('--config', dest='config', action='store', default='',
                        help="optionally enter a .yaml config file", nargs='*')
    parser.add_argument('--timer', dest='timer', action='store', type=int, default=10,
                        help='enter an amount of time each headline should appear')
    return parser.parse_args()


def ten_second_loop(mv, t, f):
    """
    Python-RSS-ticker.controller.start.ten_second_loop spawns a thread every <t>
    seconds which calls call_switch_display
    """
    looping_thread = th.Timer(t, ten_second_loop, [mv, t, f])
    looping_thread.daemon = True
    looping_thread.start()
    # I may merge ten_second_loop and call_switch_display in the future
    call_switch_display(mv, f)


def call_switch_display(main_view, test_feed):
    """
    Python-RSS-ticker.controller.start.call_switch_display calls
    view.main_view.display_entry
    """
    # This is a temporary data set. It is not dynamic

    # Todo call get_next_article instead of test_feed
    article = test_feed.pop()

    main_view.display_entry(article.title, article.link)


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
