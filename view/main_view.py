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

        color = ["red", "green", "blue", "yellow", "cyan", "magenta", "white", "black"]
        fonts = ['times 8', 'times 10', 'times 12', 'times 14', 'times 16', 'times 18', 
                 'times 20', 'times 24', 'times 26', 'times 28', 'times 36', 'times 48']

        self.menubar = tk.Menu(self)
        self.dropdown_menu = tk.Menu(self.menubar, tearoff=0)
        self.font_color = tk.Menu(self.menubar)
        self.font_menu = tk.Menu(self.menubar)

        for c in color:
            self.dropdown_menu.add_command(label=c, command=lambda c=c: self.change_window('bg', c))
            self.font_color.add_command(label=c, command=lambda c=c: self.change_window('fg', c))


        for f in fonts:
            self.font_menu.add_command(label=f, command=lambda f=f: self.change_window('font', f))

        self.menubar.add_cascade(label='bg color', menu=self.dropdown_menu)
        self.menubar.add_cascade(label='Font size', menu=self.font_menu)
        self.menubar.add_cascade(label='Font color', menu=self.font_color)

        self.master.config(menu=self.menubar)


    def change_window(self, element, value):
        """ View.main_view.MainView.change_window. 

        Modifys the tkinter window's background color, font color or font size.

        Arguments:
            element: Dictates which display feature is changed
            value: Is what the feature is changed to 
        """
        mv_logger.debug('MainView.change_window')

        self.content_label[element] = value

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
