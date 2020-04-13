import threading as th

from model import feed_manager
from view.main_view import MainView

# These line grab test data from model.feedparser. This only temporary.
# Eventually I believe that model.model should have a function that returns a
# similar list
test_feed = feed_manager.parse("https://www.theguardian.com/us/rss")
test_feed.reverse()


def ten_second_loop(mv, t):
    """
    Python-RSS-ticker.controller.start.ten_second_loop spawns a thread every <t>
    seconds which calls call_switch_display
    """
    looping_thread = th.Timer(t, ten_second_loop, [mv, t])
    looping_thread.daemon = True
    looping_thread.start()
    # I may merge ten_second_loop and call_switch_display in the future
    call_switch_display(mv)


def call_switch_display(main_view):
    """ Python-RSS-ticker.controller.start.call_switch_display calls
    view.main_view.display_entry """
    # This is a temporary data set. It is not dynamic
    temp_tuple = test_feed.get_next_article()

    main_view.display_entry(temp_tuple[0], temp_tuple[1])
