import threading as th
from view.main_view import MainView
from model.feedparser import get_titles_links

# These line grab test data from model.feedparser. This only temporary.
# Eventually I believe that model.model should have a function that returns a
# similar list
test_feed = get_titles_links()
test_feed.reverse()


def ten_second_loop(mv):
    """
    Python-RSS-ticker.controller.start.ten_second_loop spawns a thread every 10
    seconds which calls call_switch_display
    """
    looping_thread = th.Timer(10, ten_second_loop, [mv])
    looping_thread.daemon = True
    looping_thread.start()
    call_switch_display(mv)


def call_switch_display(main_view):
    """ Python-RSS-ticker.controller.start.call_switch_display calls
    model.model.switch_displayed_entry """
    temp_tuple = test_feed.pop()
    main_view.display_entry(temp_tuple[0], temp_tuple[1])
