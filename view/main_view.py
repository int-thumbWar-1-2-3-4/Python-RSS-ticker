import webbrowser
import tkinter as tk
from controller.utilities import logger


mv_logger = logger('view.main_view')


class MainView(tk.Frame):
    """ Class for view.main_view creates, displays, modifies and receives input from the user interface """

    entry_title = "Welcome to Tiny Ticker news feed"
    entry_link = "https://github.com/int-thumbWar-1-2-3-4/Python-RSS-ticker"

    def __init__(self, master=None):
        """ Constructor for view.main_view.MainView. """

        mv_logger.debug('MainView.__init__')

        super().__init__(master)
        self.master = master
        self.content_label = tk.Label(self, cursor="gumby")

        self.pack()
        self.build_window()
        self.display_entry(self.entry_title, self.entry_link)
        self.menu_bar()

    def menu_bar(self):
        """ View.main_view.MainView.menu_bar adds a drop down menu for our tk window. """

        mv_logger.debug('MainView.menubar')

        self.menubar = tk.Menu(self)

        self.dropdown_menu = tk.Menu(self.menubar, tearoff=0)
        self.dropdown_menu.add_command(label='white', command=self.bg_white)
        self.dropdown_menu.add_command(label='red', command=self.bg_red)
        self.dropdown_menu.add_command(label='blue', command=self.bg_blue)
        self.dropdown_menu.add_command(label='green', command=self.bg_green)
        self.menubar.add_cascade(label='bg color', menu=self.dropdown_menu)
        self.master.config(menu=self.menubar)

        self.font_menu = tk.Menu(self.menubar)
        self.font_menu.add_command(label='8', command=self.font_8)
        self.font_menu.add_command(label='9', command=self.font_9)
        self.font_menu.add_command(label='10', command=self.font_10)
        self.font_menu.add_command(label='11', command=self.font_11)
        self.font_menu.add_command(label='12', command=self.font_12)
        self.font_menu.add_command(label='13', command=self.font_13)
        self.menubar.add_cascade(label='Font size', menu=self.font_menu)

        self.font_color = tk.Menu(self.menubar)
        self.font_color.add_command(label='red', command=self.font_red)
        self.font_color.add_command(label='blue', command=self.font_blue)
        self.font_color.add_command(label='yellow', command=self.font_yellow)
        self.menubar.add_cascade(label='Font color', menu=self.font_color)

    def change_window(self, element, value):
        pass

    def font_red(self):
        """ View.main_view.MainView.font_red sets font color to red. """

        mv_logger.debug('MainView.font_red')
        self.content_label['fg'] = 'red'

    def font_yellow(self):
        """ View.main_view.MainView.font_yellow sets font color to yellow. """

        mv_logger.debug('MainView.font_yellow')
        self.content_label['fg'] = 'yellow'

    def font_blue(self):
        """ View.main_view.MainView.font_blue sets font color to blue. """

        mv_logger.debug('MainView.font_blue')
        self.content_label['fg'] = 'blue'

    def font_8(self):
        """ View.main_view.MainView.font_8 sets font size to 8. """

        mv_logger.debug('MainView.font_8')
        self.content_label['font'] = 'times 8'

    def font_9(self):
        """ View.main_view.MainView.font_9 sets font size to 9. """

        mv_logger.debug('MainView.font_9')
        self.content_label['font'] = 'times 9'

    def font_10(self):
        """ View.main_view.MainView.font_10 sets font size to 10. """

        mv_logger.debug('MainView.font_10')
        self.content_label['font'] = 'times 10'

    def font_11(self):
        """ View.main_view.MainView.font_11 sets font size to 11. """

        mv_logger.debug('MainView.font_11')
        self.content_label['font'] = 'times 11'

    def font_12(self):
        """ View.main_view.MainView.font_12 sets font size to 12. """

        mv_logger.debug('MainView.font_12')
        self.content_label['font'] = 'times 12'

    def font_13(self):
        """ View.main_view.MainView.font_13 sets font size to 13. """

        mv_logger.debug('MainView.font_13')
        self.content_label['font'] = 'times 13'

    def bg_white(self):
        """ View.main_view.MainView.bg_white sets background color to white. """

        mv_logger.debug('MainView.bg_white')
        self.content_label['bg'] = 'white'

    def bg_red(self):
        """ View.main_view.MainView.bg_red sets background color to red. """

        mv_logger.debug('MainView.bg_red')
        self.content_label['bg'] = 'red'

    def bg_blue(self):
        """ View.main_view.MainView.bg_blue sets background color to blue. """

        mv_logger.debug('MainView.bg_blue')
        self.content_label['bg'] = 'blue'

    def bg_green(self):
        """ View.main_view.MainView.bg_green sets background color to green. """

        mv_logger.debug('MainView.bg_green')
        self.content_label['bg'] = 'green'

    def build_window(self):
        """ View.main_view.MainView.build_window sets the title of the window and the initial label

        Here the label is bound to a button that when clicked, will call open_article with the current
        link as a parameter.
        """

        mv_logger.debug('MainView.build_window')
        self.winfo_toplevel().title("Tiny Ticker")

        self.content_label.pack(side="top")
        self.content_label["text"] = self.entry_title
        self.content_label.bind("<Button-1>",
                                lambda event,
                                content_label=self.entry_link:
                                self.open_article(self.entry_link))
        self.pack()

    def display_entry(self, entry_title: str, entry_link: str):
        """ Viw.main_view.MainView.display_entry changes the displayed title and associated link.

        This function updates both entry_title and entry_link with the appropriate parameters and changes the text of
        content_label to that of the new entry_title.

        Arguments:
            entry_title: a string showing a headline
            entry_link: a string that is the url for entry_title
        """

        mv_logger.debug('MainView.display_entry')
        self.entry_title = entry_title
        self.entry_link = entry_link

        self.content_label["text"] = self.entry_title
        self.content_label.update()

    def open_article(self, link):
        """ View.main_view.MainView.open_article opens the web page associated with the current entry_title

        Arguments:
            link: url for the current entry_title
        """

        mv_logger.debug('MainView.open_article')
        webbrowser.open_new(link)
        self.content_label.update()

def start_main_view():
    """ View.main_view.start_main_view is called from controller.start and initiates our gui."""
    
    mv_logger.debug('start_main_view')
    
    root = tk.Tk()
    return MainView(master=root)
