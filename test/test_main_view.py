import unittest
import tkinter as tk
from unittest.mock import call, patch, PropertyMock
from view.main_view import MainView, start_main_view


class TestMainView(unittest.TestCase):

    """Testing Class for view.main_view."""

    @classmethod
    def setUp(cls):
        root = tk.Tk()
        cls.test_view = MainView(master=root)

    @classmethod
    def tearDown(cls):
        cls.test_view.destroy()

    def test_build_window_winfo_toplevel(self):
        """
        Unit test for view.main_view.Model.build_window.

        Tests the first line of code in this function.
        """
        expected_text = 'Tiny Ticker'
        self.test_view._build_window()
        self.assertTrue(self.test_view.winfo_toplevel().title, expected_text)

    def test_build_window_content_label(self):
        """
        Unit test for view.main_view.Model.build_window.

        Tests the creation of the content_label feature
        """
        with patch('view.main_view.tk.Label', new_callable=PropertyMock) as mock_label:
            root = tk.Tk()
            self.view = MainView(master=root)
            self.view._build_window()
            mock_label.assert_has_calls([
                call().__setitem__('text', 'Welcome to Tiny Ticker news feed'),
                call().pack(side="top"),
            ], any_order=True)

    def test_font_red(self):
        root = tk.Tk()
        test_view = MainView(master=root)
        test_view.font_red()
        self.assertEqual(test_view.content_label['fg'], 'red')

    def test_font_yellow(self):
        root = tk.Tk()
        test_view = MainView(master=root)
        test_view.font_yellow()
        self.assertEqual(test_view.content_label['fg'], 'yellow')

    def test_font_blue(self):
        root = tk.Tk()
        test_view = MainView(master=root)
        test_view.font_blue()
        self.assertEqual(test_view.content_label['fg'], 'blue')

    def test_font_8(self):
        root = tk.Tk()
        test_view = MainView(master=root)
        test_view.font_8()
        self.assertEqual(test_view.content_label['font'], 'times 8')

    def test_font_9(self):
        root = tk.Tk()
        test_view = MainView(master=root)
        test_view.font_9()
        self.assertEqual(test_view.content_label['font'], 'times 9')

    def test_font_10(self):
        root = tk.Tk()
        test_view = MainView(master=root)
        test_view.font_10()
        self.assertEqual(test_view.content_label['font'], 'times 10')

    def test_font_11(self):
        root = tk.Tk()
        test_view = MainView(master=root)
        test_view.font_11()
        self.assertEqual(test_view.content_label['font'], 'times 11')

    def test_font_12(self):
        root = tk.Tk()
        test_view = MainView(master=root)
        test_view.font_12()
        self.assertEqual(test_view.content_label['font'], 'times 12')

    def test_font_13(self):
        root = tk.Tk()
        test_view = MainView(master=root)
        test_view.font_13()
        self.assertEqual(test_view.content_label['font'], 'times 13')

    def test_bg_white(self):
        root = tk.Tk()
        test_view = MainView(master=root)
        test_view.bg_white()
        self.assertEqual(test_view.content_label['bg'], 'white')

    def test_bg_red(self):
        root = tk.Tk()
        test_view = MainView(master=root)
        test_view.bg_red()
        self.assertEqual(test_view.content_label['bg'], 'red')

    def test_bg_blue(self):
        root = tk.Tk()
        test_view = MainView(master=root)
        test_view.bg_blue()
        self.assertEqual(test_view.content_label['bg'], 'blue')

    def test_bg_green(self):
        root = tk.Tk()
        test_view = MainView(master=root)
        test_view.bg_green()
        self.assertEqual(test_view.content_label['bg'], 'green')

    def test_display_entry(self):
        """Unit test for view.main_view.Model.build_window."""
        fake_title = 'Man explodes'
        fake_link = 'www.virus.com'

        self.test_view.display_entry(fake_title, fake_link)
        self.assertEqual(self.test_view.default_entry_title, fake_title)
        self.assertEqual(self.test_view.default_entry_link, fake_link)

        self.test_view.content_label = PropertyMock()
        self.assertTrue(self.test_view.content_label.call().__setitem__('text', fake_title))

    @patch('view.main_view.webbrowser.open_new')
    def test_open_article(self, mock_open_new):
        """Unit test for view.main_view.MainView.open_article."""
        test_link = 'www.goesnowhere.com'

        self.test_view._open_article(test_link)
        mock_open_new.assert_called_with(test_link)

    def test_change_windows_background(self):
        """
        Unit test for view.main_view.MainView.change_window.

        Test background color change.
        """
        self.test_view._change_window('bg', 'blue')
        self.assertEqual(self.test_view.content_label['bg'], 'blue')

    def test_change_font_size(self):
        """
        Unit test for view.main_view.MainView.change_window.

        Test font size change.
        """
        self.test_view._change_window('font', '9')
        self.assertEqual(self.test_view.content_label['font'], '9')

    def test_change_font_color(self):
        """
        Unit test for view.main_view.MainView.change_window.

        Test font color change.
        """
        self.test_view._change_window('fg', 'red')
        self.assertEqual(self.test_view.content_label['fg'], 'red')


class TestStartMainView(unittest.TestCase):
    
    """Test class for view.main_view.start_main_view."""

    def test_start_main_view(self):
        """
        Unit test for view.main_view.start_main_view.

        Function should return an object of type MainView.
        """
        result = start_main_view()
        self.assertTrue(isinstance(result, MainView))
        result.destroy()
