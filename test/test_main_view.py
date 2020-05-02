import unittest
import tkinter as tk
from unittest.mock import call, patch, PropertyMock, Mock
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
        self.test_view._build_window("test_title", "test_link")
        self.assertTrue(self.test_view.winfo_toplevel().title, expected_text)


    def test_build_window_content_label(self):
        """
        Unit test for view.main_view.Model.build_window.

        Tests the creation of the content_label feature
        """
        with patch('view.main_view.tk.Label', new_callable=PropertyMock) as mock_label:
            root = tk.Tk()
            self.view = MainView(master=root)
            self.view._build_window("Test Title", "https://github.com/int-thumbWar-1-2-3-4/Python-RSS-ticker")

            mock_label.assert_has_calls([
                call().__setitem__('text', 'Welcome to Tiny Ticker news feed'),
                call().pack(side="top"),
            ], any_order=True)

    def test_display_entry(self):
        """Unit test for view.main_view.Model.build_window."""
        fake_title = 'Man explodes'
        fake_link = 'www.virus.com'

        self.test_view.display_entry(fake_title, fake_link)

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

    @patch('view.main_view.simpledialog')
    @patch('model.feed_manager.FeedManager')
    @patch('controller.tiny_ticker.call_new_feed')
    def test_prompt_new_feed(self, mock_simpledialog, mock_feed_manager, mock_call_new_feed):
        """
        Unit test for view.main_view.MainView.test_prompt_new_feed.

        Test adding a new feed during runtime.
        """

        mock_simpledialog.askstring.return_value = "https://www.theguardian.com/us/rss"
        self.test_view._prompt_new_feed(mock_feed_manager, mock_call_new_feed)
        mock_call_new_feed.assert_called()


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
