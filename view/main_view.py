"""
View.main_view

This module manages the gui for this application.
"""

import webbrowser
import tkinter as tk
from tkinter import simpledialog
from controller.utilities import logger
from model.feed_manager import FeedManager

mv_logger = logger('view.main_view')


class MainView(tk.Frame):
    """
    view.main_view.MainView

    This class fills out a tikinter frame. It creates, displays, modifies
    and receives input from the controller and the user interface.
    """

    def __init__(self, master=None,
                 entry_title="Welcome to Tiny Ticker news feed",
                 entry_link="https://github.com/int-thumbWar-1-2-3-4/Python-RSS-ticker"):
        """
        view.main_view.MainView.__init__

        Populates this frame with content and a menu. Prepares the frame for display but does not prompt
        it to be made visible.

        Arguments:
            master -- the Tkinter object which manages the gui for this application. Defaults to None
            entry_title -- the title for the entry to display. Defaults to a dummy string.
            entry_link -- the link for the entry to display. Defaults to a dummy string.
        """

        super().__init__(master)
        mv_logger.debug('MainView.__init__')

        self.master = master
        self.content_label = tk.Label(self)

        self._build_window(entry_title, entry_link)
        self._build_menu_bar()
        self.pack()

    def attach_new_feed_menu(self, feed_manager: FeedManager, call_new_feed_method):
        """
        View.main_view.attach_new_feed_menu.

        An access method for tiny_ticker which provides the menus a method within tiny_ticker.py to be called
        when the user inputs a new feed url.

        Arguments:
            feed_manager -- the feed_manager which the controller will add the new feed to
            call_new_feed_method -- the method to be called when the user chooses to add a new feed
        """

        mv_logger.debug('MainView.attach_new_feed_menu')

        self.new_feed_menu.add_command(label="Add New Feed...",
                                       command=lambda: self._prompt_new_feed(feed_manager, call_new_feed_method))

    def display_entry(self, entry_title: str, entry_link: str):
        """
        View.main_view.MainView.display_entry.

        This function updates both entry_title and entry_link with the
        appropriate parameters and changes the text of content_label to
        that of the new entry_title.

        Arguments:
            entry_title -- a string showing a headline
            entry_link -- a string that is the url for the article
        """

        mv_logger.debug('MainView.display_entry')

        self.content_label["text"] = entry_title
        self.content_label.unbind_all(self)
        self.content_label.bind("<Button-1>",
                                lambda event,
                                content_label=entry_title: self._open_article(entry_link))
        self.content_label.update()

    def _prompt_new_feed(self, feed_manager: FeedManager, call_new_feed_method):
        """
        View.main_view.MainView._prompt_new_feed

        Creates a popup window which prompts the user to input a link for a new feed.

        Arguments:
            feed_manager -- the FeedManager to add the new feed to
            call_new_feed_method -- the method to be called when the user chooses to add a new feed
        """

        mv_logger.debug('MainView._prompt_new_feed')

        user_input_url = simpledialog.askstring(title="", prompt="New Feed URL:")

        if user_input_url is not None and user_input_url != "":
            # Only call call_new_feed_method if the input url is not blank.
            call_new_feed_method(feed_manager, user_input_url)

    def _build_menu_bar(self):
        """
        View.main_view.MainView._build_menu_bar

        This function adds a drop down menu for our tk window. It also assigns
        a lambda function to each of the dropdown menu's options.
        """

        mv_logger.debug('MainView._build_menu_bar')

        colors = ["red", "green", "blue", "yellow", "cyan", "magenta", "white", "black"]
        fonts = ['8', '10', '12', '14', '16',
                 '18', '20', '24', '26', '28',
                 '36', '48']

        menubar = tk.Menu(self)
        dropdown_menu = tk.Menu(menubar, tearoff=0)
        font_color_menu = tk.Menu(menubar)
        font_menu = tk.Menu(menubar)
        self.new_feed_menu = tk.Menu(menubar)

        for color in colors:
            dropdown_menu.add_command(label=color, command=lambda c=color: self._change_window('bg', c))
            font_color_menu.add_command(label=color, command=lambda c=color: self._change_window('fg', c))


        for font in fonts:
            font_size = 'times ' + font
            font_menu.add_command(label=font, command=lambda size=font_size: self._change_window('font', size))


        menubar.add_cascade(label='Background color', menu=dropdown_menu)
        menubar.add_cascade(label='Font size', menu=font_menu)
        menubar.add_cascade(label='Font color', menu=font_color_menu)
        menubar.add_cascade(label='Add Feed', menu=self.new_feed_menu)

        self.master.config(menu=menubar)

    def _build_window(self, entry_title: str, entry_link: str):
        """
        View.main_view.MainView._build_window.

        Sets the title of the window and the initial label. Here the label
        is also bound to a button that when clicked, will call open_article
        with the current link as a parameter.

        Arguments:
            entry_title -- a string showing a headline
            entry_link -- a string that is the url for the article
        """
        mv_logger.debug('MainView._build_window')
        self.winfo_toplevel().title("Tiny Ticker")

        self.content_label.pack(side="top")
        self.content_label["text"] = entry_title
        self.content_label.bind("<Button-1>",
                                lambda event,
                                content_label=entry_title: self._open_article(entry_link))

    def _change_window(self, element: str, value: str):
        """
        View.main_view.MainView._change_window.

        Modifies the tkinter window's background color, font color or font size.

        Arguments:
            element -- Dictates which display feature is changed
            value -- Is what the feature is changed to
        """

        mv_logger.debug('MainView._change_window')

        self.content_label[element] = value

    def _open_article(self, link: str):
        """
        View.main_view.MainView._open_article.

        Opens entry_link's web page associated in the default browser.
        Entry link is associated with the current entry_title

        Arguments:
            link -- url for the currently displayed Article
        """

        mv_logger.debug('MainView._open_article')

        webbrowser.open_new(link)
        self.content_label.update()


def start_main_view() -> MainView:
    """
    View.main_view.start_main_view.

    This function is called from controller.start and it Initiates our gui.

    Returns a new instance of MainView
    """

    mv_logger.debug('start_main_view')

    root = tk.Tk()
    return MainView(master=root)
