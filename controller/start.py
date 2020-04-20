import argparse
import tkinter as tk
import threading as th
from view.main_view import MainView
from model.parser import parse_url_feed
from model.feed_manager import parse


def ticker_argument_parser():
    """ Argument Parser for Headline Ticker """

    parser = argparse.ArgumentParser(description="Select a file or feed to parse.", fromfile_prefix_chars='@')
    parser.add_argument('--url', '-u', dest='url', action='store', default=["https://www.theguardian.com/us/rss"],
                        help="enter a url of an RSS or ATOM feed to parse", nargs='*')
    parser.add_argument('--file', '-f', dest='file', action='store', default="",
                        help="enter a file name to parse", nargs='*')
    parser.add_argument('--config', '-c', dest='config', action='store', default='',
                        help="optionally enter a .yaml config file", nargs='*')
    parser.add_argument('--timer', '-t', dest='timer', action='store', type=int, choices=range(1, 601), default=10,
                        help='enter an amount of time each headline should appear')
    return parser.parse_args()


def ten_second_loop(main_view, cycle, feed):
    """ Controller.title_loop.ten_second_loop switches the display every <cycle> seconds.

    This function spans a timed looping thread. Every 'cycle' seconds this function calls it's self to continue the
    loop. It is a daemon thread so it acts in the background and it calls controller.title_loop.call_switch_display
    with the parameters gui and feed.

    Arguments:
        gui: an instance of model.MainView
        cycle: the amount of time between view changes
        feed: a list of article objects
    """
    looping_thread = th.Timer(cycle, ten_second_loop, [main_view, cycle, feed])
    looping_thread.daemon = True
    looping_thread.start()
    # I may merge ten_second_loop and call_switch_display in the future
    call_switch_display(main_view, feed)


def call_switch_display(main_view, feed):
    """ Controller.title_loop.call_switch_display calls view.main_view.display_entry

    This function pops an article object off of the feed loop. It then calls the function from
    view.MainView.display_entry() with parameters title and link from the article object.

    Arguments:
        main_view: an instance of model.MainView
        feed: a list of article objects
    """
    # This is a temporary data set. It is not dynamic
    article = feed.pop()

    main_view.display_entry(article.title, article.link)


def main(mainView):
    arguments = ticker_argument_parser()
    feed = parse(arguments.url[0])
    feed.reverse()
    ten_second_loop(mainView, arguments.timer, feed)


if __name__ == "__main__":
    root = tk.Tk()
    mainView = MainView(master=root)

    main(mainView)

    # KEEP THIS LAST
    mainView.mainloop()
