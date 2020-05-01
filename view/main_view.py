"""View.main_view."""
import webbrowser
import tkinter as tk
from controller.utilities import logger

mv_logger = logger('view.main_view')


def start_main_view():
    """
    View.main_view.start_main_view.

    This function is called from controller.start and it Initiates our gui.
    """
    mv_logger.debug('start_main_view')

    root = tk.Tk()
    return MainView(master=root)


class MainView(tk.Frame):
    """
    Class view.main_view.MainView.

    This class fills out a tikinter root. It creates, displays, modifies
    and receives input from the controller and the user interface.
    """

    def __init__(self, master=None,
                 entry_title="Welcome to Tiny Ticker news feed",
                 entry_link="https://github.com/int-thumbWar-1-2-3-4/Python-RSS-ticker"):
        """Constructor for view.main_view.MainView."""
        super().__init__(master)

        mv_logger.debug('MainView.__init__')

        self.master = master
        self.content_label = tk.Label(self)
        self.display_entry(entry_title, entry_link)

        self._build_window()
        self._build_menu_bar()
        self.pack()

    def display_entry(self, entry_title: str, entry_link: str):
        """
        View.main_view.MainView.display_entry.

        This function updates both entry_title and entry_link with the
        appropriate parameters and changes the text ofcontent_label to
        that of the new entry_title.

        Arguments:
            entry_title -- a string showing a headline
            entry_link -- a string that is the url for entry_title
        """
        mv_logger.debug('MainView.display_entry')

        self.content_label["text"] = entry_title
        self.content_label.update()

    def _build_menu_bar(self):
        """
        View.main_view.MainView.menu_bar.

        This function adds a drop down menu for our tk window. It also assigns
        a lambda function to each of the dropdown menu's options.
        """
        mv_logger.debug('MainView.menubar')

        colors = ["red", "green", "blue", "yellow", "cyan", "magenta", "white", "black"]
        fonts = ['8', '10', '12', '14', '16',
                 '18', '20', '24', '26', '28',
                 '36', '48']

        menubar = tk.Menu(self)
        dropdown_menu = tk.Menu(menubar, tearoff=0)
        font_color = tk.Menu(menubar)
        font_menu = tk.Menu(menubar)

        for color in colors:
            dropdown_menu.add_command(label=color, command=lambda c=color: self._change_window('bg', c))
            font_color.add_command(label=color, command=lambda c=color: self._change_window('fg', c))

        for font in fonts:
            font_menu.add_command(label=font, command=lambda f=font: self._change_window('font', f))

        menubar.add_cascade(label='Background color', menu=dropdown_menu)
        menubar.add_cascade(label='Font size', menu=font_menu)
        menubar.add_cascade(label='Font color', menu=font_color)

        self.master.config(menu=menubar)

    def _build_window(self, entry_title: str, entry_link: str):
        """
        View.main_view.MainView.build_window.

        Sets the title of the window and the initial label. Here the label
        is also bound to a button that when clicked, willcall open_article
        with the current link as a parameter.
        """
        mv_logger.debug('MainView.build_window')
        self.winfo_toplevel().title("Tiny Ticker")

        self.content_label.pack(side="top")
        self.content_label["text"] = entry_title
        self.content_label.bind("<Button-1>",
                                lambda event,
                                content_label=entry_title: self._open_article(entry_title))

    def _change_window(self, element, value):
        """View.main_view.MainView.change_window.

        Modifies the tkinter window's background color, font color or font size.

        Arguments:
            element -- Dictates which display feature is changed
            value -- Is what the feature is changed to
        """
        mv_logger.debug('MainView.change_window')

        self.content_label[element] = value

    def _open_article(self, link):
        """
        View.main_view.MainView.open_article.

        Opens entry_link's web page associated in the default browser.
        Entry link is associated with the current entry_title

        Arguments:
            link -- url for the current entry_title
        """
        mv_logger.debug('MainView.open_article')
        webbrowser.open_new(link)
        self.content_label.update()
