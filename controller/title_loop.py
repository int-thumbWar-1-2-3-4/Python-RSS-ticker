import threading as th

# These line grab test data from model.feedparser. This only temporary.
# Eventually I believe that model.model should have a function that returns a
# similar list


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
