from view.main_view import MainView
from unittest.mock import Mock, patch
import tkinter as tk
import unittest


class TestMainView(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        root = tk.Tk()
        cls.window = MainView(master=root)
        cls.window.mainloop()

    @classmethod
    def tearDown(cls) -> None:
        del(cls.window)


    def test_master(self):
        # self.assertEqual(self.mock_main_view.master, self.mock_root)
        pass

    def test_winfo_toplevel(self):
        # title = "Python RSS Ticker"
        # self.assertEqual(self.mock_main_view.title, title)
        pass

    def test_display_entry(self):
        test_title = "test title"
        test_link = "test_link"
        self.window.display_entry(test_title, test_link)

        # self.assertEqual(self.window.content_label["test"], test_title)
        self.assertEqual(self.window.__entry_link, test_link)
