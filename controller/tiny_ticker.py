"""Controller.tiny_ticker."""
import threading as th
from typing import List
from view.main_view import start_main_view
from model.feed_manager import create_feed_manager
from controller.utilities import logger, ticker_argument_parser


tt_logger = logger('controller.tiny_ticker')
arguments = ticker_argument_parser()

def ten_second_loop(main_view, cycle, feed_manager):
    """
    Controller.tiny_ticker.ten_second_loop switches the display every <cycle> seconds.

    This function spans a timed looping thread. Every 'cycle' seconds this function calls it's self to continue the
    loop. It is a daemon thread so it acts in the background and it calls controller.title_loop.call_switch_display
    with the parameters gui and feed.

    Arguments:
        main_view -- an instance of model.MainView
        cycle -- the amount of time between view changes
        feed -- a list of article objects
    """
    tt_logger.debug('ten_second_loop')
    looping_thread = th.Timer(cycle, ten_second_loop, [main_view, cycle, feed_manager])
    looping_thread.daemon = True
    looping_thread.start()
    # I may merge ten_second_loop and call_switch_display in the future
    call_switch_display(main_view, feed_manager)


def call_switch_display(main_view, feed_manager):
    """
    Controller.tiny_ticker.call_switch_display calls view.main_view.display_entry.

    This function pops an article object off of the feed loop. It then calls the function from
    view.MainView.display_entry() with parameters title and link from the article object.

    Arguments:
        main_view -- an instance of model.MainView
        feed -- a list of article objects
    """
    tt_logger.debug('call_switch_display')
    article = feed_manager.get_next_article()

    main_view.display_entry(article.title, article.link)


def main(main_view):
    """Controller.tiny_ticker.main gathers command-line args, calls the model, initiates the title loop.
    Arguments:
        mainView -- an instance of model.MainView
    """
    tt_logger.debug('main')

    ten_second_loop(main_view, arguments.timer, create_feed_manager(arguments.url[0]))


if __name__ == "__main__":
    tt_logger.debug('__main__')
    main_view = start_main_view()
    main(main_view)

    # KEEP THIS LAST
    main_view.mainloop()
