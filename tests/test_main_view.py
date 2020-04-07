import unittest
import tkinter as tk
from view.main_view import MainView
from unittest.mock import call, patch, PropertyMock


class TestMainView(unittest.TestCase):

    def test_build_window(self):
        """ Unit test for view.main_view.Model.build_window """
        with patch('view.main_view.tk.Label', new_callable=PropertyMock) as mock_label:
            root = tk.Tk()
            test_view = MainView(master=root)
            test_view.build_window()
            mock_label.assert_has_calls([
                call().__setitem__('text', '[BLANK Entry Title]'),
                call().pack(side="top")
            ], any_order=True)


    def test_display_entry(self):
        """ Unit test for view.main_view.Model.build_window """
        pass

    @patch('view.main_view.webbrowser.open_new')
    def test_open_article(self, mock_open_new):
        """ Unit test for view.main_view.MainView.open_article """
        test_link = 'www.goesnowhere.com'
        root = tk.Tk()
        test_view = MainView(master=root)
        test_view.open_article(test_link)
        mock_open_new.assert_called_with(test_link)

