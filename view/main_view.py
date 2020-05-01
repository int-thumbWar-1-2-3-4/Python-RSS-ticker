"""View.main_view."""
import webbrowser
import tkinter as tk
from tkinter import *
from controller.utilities import logger
from view.gui_config import yaml_loader, yaml_dump

mv_logger = logger('view.main_view')

class MainView(tk.Frame):
    """
    Class view.main_view.MainView.

    This class fills out a tikinter root. It creates, displays, modifies
    and receives input from the controller and the user interface.
    """

    entry_title = "Welcome to Tiny Ticker news feed"
    entry_link = "https://github.com/int-thumbWar-1-2-3-4/Python-RSS-ticker"


    def __init__(self, master=None):
        """Constructor for view.main_view.MainView."""
        mv_logger.debug('MainView.__init__')

        super().__init__(master)
        self.master = master
        self.fcolor = StringVar()
        self.bcolor = StringVar()
        self.font_var = StringVar()
        list_set = yaml_loader("gui_settings.yaml")
        if 'bg' in list_set:
            self.bcolor = list_set['bg']
        if 'fg' in list_set:
            self.fcolor = list_set['fg']
        if 'font' in list_set:
            self.font_var = list_set['font']

        self.content_label = tk.Label(self, cursor="gumby", fg= self.fcolor, bg= self.bcolor, font= self.font_var)
        self.pack()
        self.build_window()
        self.display_entry(self.entry_title, self.entry_link)
        self.menu_bar()

    def save_values(self):
        """
        View.main_view.MainView.save_values.

        Records the gui values and saves them to a dictionary. The dictionary
        is then written to a yaml file.
        """
        save_list = {'bg': self.bcolor, 'fg': self.fcolor, 'font': self.font_var }
        yaml_dump("gui_settings.yaml", save_list)

    def menu_bar(self):
        """
        View.main_view.MainView.menu_bar.

        This function adds a drop down menu for our tk window. It also assigns
        a lambda function to each of the dropdown menu's options.
        """
        mv_logger.debug('MainView.menubar')

        color = ["red", "green", "blue", "yellow", "cyan", "magenta", "white",
                 "black"]
        fonts = ['8', '10', '12', '14', '16',
                 '18', '20', '24', '26', '28',
                 '36', '48']

        self.menubar = tk.Menu(self)
        self.dropdown_menu = tk.Menu(self.menubar, tearoff=0)
        self.font_color = tk.Menu(self.menubar)
        self.font_menu = tk.Menu(self.menubar)
        self.exit_menu = tk.Menu(self.menubar)

        for c in color:
            self.dropdown_menu.add_command(label=c, command=lambda c=c:
                                           self.change_window('bg', c))
            self.font_color.add_command(label=c, command=lambda c=c:
                                        self.change_window('fg', c))


        for f in fonts:
            self.font_menu.add_command(label=f, command=lambda f=f:
                                       self.change_window('font', f))

        self.exit_menu.add_command(label="Save and exit", command=lambda: [
             self.save_values(),  tk.Tk.quit(self)])

        self.menubar.add_cascade(label='Background color', menu=self.dropdown_menu)
        self.menubar.add_cascade(label='Font size', menu=self.font_menu)
        self.menubar.add_cascade(label='Font color', menu=self.font_color)
        self.menubar.add_cascade(label='Exit', menu=self.exit_menu)
        self.master.config(menu=self.menubar)

    def change_window(self, element, value):
        """View.main_view.MainView.change_window.

        Modifys the tkinter window's background color, font color or font size.

        Arguments:
            element -- Dictates which display feature is changed
            value -- Is what the feature is changed to
        """
        mv_logger.debug('MainView.change_window')

        self.content_label[element] = value
        if element == 'bg':
            self.bcolor = value
        if element == 'fg':
            self.fcolor = value
        if element == 'font':
            self.font_var = value

    def build_window(self):
        """
        View.main_view.MainView.build_window.

        Sets the title of the window and the initial label. Here the label
        is also bound to a button that when clicked, willcall open_article
        with the current link as a parameter.
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
        """
        Viw.main_view.MainView.display_entry.

        This function updates both entry_title and entry_link with the
        appropriate parameters and changes the text ofcontent_label to
        that of the new entry_title.

        Arguments:
            entry_title -- a string showing a headline
            entry_link -- a string that is the url for entry_title
        """
        mv_logger.debug('MainView.display_entry')
        self.entry_title = entry_title
        self.entry_link = entry_link

        self.content_label["text"] = self.entry_title
        self.content_label.update()

    def open_article(self, link):
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


def start_main_view():
    """
    View.main_view.start_main_view.

    This function is called from controller.start and it Initiates our gui.
    """
    mv_logger.debug('start_main_view')

    root = tk.Tk()
    return MainView(master=root)




