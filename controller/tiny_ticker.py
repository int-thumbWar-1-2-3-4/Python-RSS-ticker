"""
controller.tiny_ticker

Contains methods for mediating communication between this application's modules. It also initializes
and runs the Tiny Ticker application.
"""

import threading
from model import parser
from typing import List
from model.article import Article
from view.main_view import start_main_view, MainView
from model.feed_manager import create_feed_manager, FeedManager
from controller.utilities import logger, ticker_argument_parser


tt_logger = logger('controller.tiny_ticker')

arguments = ticker_argument_parser()


def ten_second_loop(main_view: MainView, cycle, feed_manager: FeedManager):
    """
    controller.tiny_ticker.ten_second_loop

    Switches the display every <cycle> seconds. This function spans a timed looping thread. Every 'cycle' seconds this
    function calls it's self to continue the loop. It is a daemon thread so it acts in the background and it calls
    controller.title_loop.call_switch_display.

    Arguments:
        main_view -- the MainView which displays articles.
        cycle -- the amount of time between view changes. User input from the command line.
        feed_manager -- the FeedManager which will provide the next article to display
    """

    tt_logger.debug('ten_second_loop')

    looping_thread = threading.Timer(cycle, ten_second_loop, [main_view, cycle, feed_manager])
    looping_thread.daemon = True
    looping_thread.start()

    # I may merge ten_second_loop and call_switch_display in the future
    call_switch_display(main_view, feed_manager)


def call_new_feed(feed_manager: FeedManager, new_feed_url: str):
    """
    controller.tiny_ticker.call_new_feed

    Downloads the contents of the feed at the url provided, then adds the contents to the feed_manager

    Arguments:
         feed_manager -- the FeedManager which will hold the contents of the new feed
         new_feed_url -- The url location of the new feed
    """

    tt_logger.debug('call_new_feed')

    feed_contents: List[Article] = parser.get_feed_contents(new_feed_url)
    feed_name: str = parser.get_feed_name(new_feed_url)
    feed_manager.update(feed_name, new_feed_url, feed_contents)


def call_switch_display(main_view: MainView, feed_manager: FeedManager):
    """
    controller.tiny_ticker.call_switch_display

    Requests the next article from the feed_manager and prompts the view to display it.

    Arguments:
        main_view -- the gui view which will display the next article
        feed_manager -- the feed_manager which holds the contents of all of the feeds currently downloaded.
    """

    tt_logger.debug('call_switch_display')

    article = feed_manager.get_next_article()

    main_view.display_entry(article.title, article.link)


def main(main_view: MainView):
    """
    controller.tiny_ticker.main

    Gathers command-line args, loads feeds into the model, and initiates the title loop.

    Arguments:
        mainView -- the gui view which displays feed articles
    """

    tt_logger.debug('main')

    urls = arguments.url
    feed_manager = create_feed_manager(urls.pop(0))
    main_view.attach_new_feed_menu(feed_manager, call_new_feed)
    ten_second_loop(main_view, arguments.timer, feed_manager)

    for u in urls:
        call_new_feed(feed_manager, u)


if __name__ == "__main__":
    tt_logger.debug('__main__')

    main_view = start_main_view()
    main(main_view)

    # KEEP THIS LAST
    main_view.mainloop()
