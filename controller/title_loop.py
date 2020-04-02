import threading as th
from model.model import parse

# These line grab test data from model.feedparser. This only temporary.
# Eventually I believe that model.model should have a function that returns a
# similar list
test_feed = parse("https://www.theguardian.com/us/rss")


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
    article = test_feed.pop()

    main_view.display_entry(article.title, article.link)
