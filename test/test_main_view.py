import unittest
import tkinter as tk
from view.main_view import MainView
from unittest.mock import call, patch, PropertyMock


class TestMainView(unittest.TestCase):

    def test_build_window_winfo_toplevel(self):
        """ Unit test for view.main_view.Model. build_window's first line of code """

        expected_text = 'Tiny Ticker'
        root = tk.Tk()
        test_view = MainView(master=root)
        test_view.build_window()
        self.assertTrue(test_view.winfo_toplevel().title, expected_text)

    def test_build_window_content_label(self):
        """ Unit test for view.main_view.Model.build_window's content_label feature """

        with patch('view.main_view.tk.Label', new_callable=PropertyMock) as mock_label:
            root = tk.Tk()
            test_view = MainView(master=root)
            test_view.build_window()
            mock_label.assert_has_calls([
                call().__setitem__('text', 'Welcome to Tiny Ticker news feed'),
                call().pack(side="top"),
            ], any_order=True)

    def test_display_entry(self):
        """ Unit test for view.main_view.Model.build_window """

        fake_title = 'Man explodes'
        fake_link = 'www.virus.com'

        root = tk.Tk()
        test_view = MainView(master=root)

        test_view.display_entry(fake_title, fake_link)
        self.assertEqual(test_view.entry_title, fake_title)
        self.assertEqual(test_view.entry_link, fake_link)

        test_view.content_label = PropertyMock()
        self.assertTrue(test_view.content_label.call().__setitem__('text', fake_title))

    @patch('view.main_view.webbrowser.open_new')
    def test_open_article(self, mock_open_new):
        """ Unit test for view.main_view.MainView.open_article """

        test_link = 'www.goesnowhere.com'
        root = tk.Tk()
        test_view = MainView(master=root)
        test_view.open_article(test_link)
        mock_open_new.assert_called_with(test_link)

class TestStartMainView(unittest.TestCase):

    def test_start_main_view(self):
        result = start_view()
        self.assertTrue(isinstance(result, MainView))
        result.destroy()
