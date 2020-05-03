"""Test.test_tiny_ticker."""

import os
import sys
import unittest
import tkinter as tk
from datetime import datetime, timedelta
from model.article import Article
from unittest.mock import patch, PropertyMock
from view.main_view import MainView
from model.feed_manager import FeedManager
from controller.tiny_ticker import main, ten_second_loop, call_switch_display, call_new_feed

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestMain(unittest.TestCase):
    """Test class for controller.tiny_ticker."""

    @classmethod
    def setUp(cls):
        """Test.test_tiny_ticker.TestTinyTicker.setUp."""
        root = tk.Tk()
        cls.test_view = MainView(master=root)

    @classmethod
    def tearDown(cls):
        """Test.test_tiny_ticker.TestTinyTicker.tearDown."""
        cls.test_view.destroy()

    @patch('controller.tiny_ticker.ten_second_loop')
    def test_call_ten_second_loop(self, mock_loop):
        """
        Unit test for controller.tiny_ticker.main.

        Tests the call to the ten second loop.
        """

        with patch('model.feed_manager.create_feed_manager', new_callable=PropertyMock) as mock_create:
            main(self.test_view)
            mock_loop.assert_called()


class TestLoop(unittest.TestCase):
    """Test class for controller.tiny_ticker."""

    test_title = 'test title'
    test_url = 'www.nowhere.com'
    test_date = '5/11/2020'

    @patch('controller.tiny_ticker.threading.Timer')
    @patch('view.main_view')
    @patch('controller.tiny_ticker.call_switch_display')
    def test_ten_second_loop_calls_its_self(self, mock_timer, mock_main_view, mock_switch_display):
        """Unit test of controller.title_loop.ten_second_loop"""

        test_feed_manager = FeedManager()
        test_article = Article(self.test_title, self.test_url, datetime.now())
        test_feed_manager.update("Test Feed Title", "Test Feed Url", [test_article])

        ten_second_loop(mock_main_view, 7, test_feed_manager)
        self.assertTrue(mock_timer.called)
        self.assertTrue(mock_switch_display.called)

    @patch('view.main_view.MainView')
    def test_call_switch_display(self, mock_main_view):
        """Unit test of controller.title_loop.call_switch_display"""

        test_feed_manager = FeedManager()
        test_article = Article(self.test_title, self.test_url, datetime.now())
        test_feed_manager.update("Test Feed Title", "Test Feed Url", [test_article])

        call_switch_display(mock_main_view, test_feed_manager)
        mock_main_view.display_entry.assert_called_with(self.test_title, self.test_url)

    @patch('model.feed_manager.FeedManager')
    @patch('model.parser.get_feed_contents')
    @patch('model.parser.get_feed_name')
    def test_call_new_feed(self, mock_feedmanager, mock_getfeedcontents, mock_getfeedname):
        """Unit test of controller.title_loop.test_call_new_feed"""

        test_url = "https://www.theguardian.com/us/rss"
        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))  # 1 day ago (most recent)
        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))  # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))  # 3 days ago

        mock_getfeedcontents.return_value = [article_1, article_2, article_3]
        mock_getfeedname.return_value = "Test Feed Name"

        call_new_feed(mock_feedmanager, test_url)
        mock_feedmanager.update.assert_called_once()