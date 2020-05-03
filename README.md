# Python-RSS-ticker [![Build Status](https://travis-ci.org/int-thumbWar-1-2-3-4/Python-RSS-ticker.svg?branch=development)](https://travis-ci.org/int-thumbWar-1-2-3-4/Python-RSS-ticker) [![codecov](https://codecov.io/gh/int-thumbWar-1-2-3-4/Python-RSS-ticker/branch/development/graph/badge.svg)](https://codecov.io/gh/int-thumbWar-1-2-3-4/Python-RSS-ticker) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/cfada09b278548a082e369a17001880c)](https://app.codacy.com/gh/int-thumbWar-1-2-3-4/Python-RSS-ticker?utm_source=github.com&utm_medium=referral&utm_content=int-thumbWar-1-2-3-4/Python-RSS-ticker&utm_campaign=Badge_Grade_Dashboard)
## Design Structure

        MVC - Controller-Model-View

        Tkinter - A GUI module that is commonly used in Python

        Application Flow 
## Controller 
   - Contains methods for mediating communication between this application's modules. 
   - It also initializes and runs the Tiny Ticker application.
       - controller.tiny_ticker.ten_second_loop
            Switches the display every <cycle> seconds. This function spans a timed looping thread. Every 'cycle' seconds this
            function calls it's self to continue the loop. It is a daemon thread so it acts in the background and it calls
            controller.title_loop.call_switch_display.
       Arguments:
            - main_view -- the MainView which displays articles.
            - cycle -- the amount of time between view changes. User input from the command line.
            - feed_manager -- the FeedManager which will provide the next article to display
       - controller.tiny_ticker.call_new_feed
            Downloads the contents of the feed at the url provided, then adds the contents to the feed_manager
       Arguments:
            - feed_manager -- the FeedManager which will hold the contents of the new feed
            - new_feed_url -- The url location of the new feed
       - controller.tiny_ticker.call_switch_display
            Requests the next article from the feed_manager and prompts the view to display it.
       Arguments:
           - main_view -- the gui view which will display the next article
           - feed_manager -- the feed_manager which holds the contents of all of the feeds currently downloaded.
       - controller.tiny_ticker.main
            Gathers command-line args, loads feeds into the model, and initiates the title loop.
       Arguments:
           - mainView -- the gui view which displays feed articles
        
