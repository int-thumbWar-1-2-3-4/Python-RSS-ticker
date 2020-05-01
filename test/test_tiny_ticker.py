"""Test.test_tiny_ticker."""
import os
import sys
import unittest
import tkinter as tk
from unittest.mock import patch
from view.main_view import MainView
from controller.tiny_ticker import main


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestTinyTicker(unittest.TestCase):

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

    @patch('controller.tiny_ticker.ticker_argument_parser')
    def test_call_ticker_argument_parser(self, mock_arg_parser):
        """Unit test for controller.tiny_ticker.main. Tests the call to the argument parser."""
        test_url = 'http://www.fakeurl.com/rss'
        main(self.test_view, [test_url])
        mock_arg_parser.assert_called()

    @patch('model.parser')
    def test_call_parse(self, mock_parser):
        """Unit test for controller.tiny_ticker.main. Tests the call to the model's feedmanager.parse."""
        test_url = ['http://www.fakeurl.com/rss']
        sys.argv = ['test', '--url', test_url[0]]

        main(self.test_view, test_url[0])
        mock_parser.assert_called_with(test_url[0])

    @patch('controller.tiny_ticker.ten_second_loop')
    def test_call_ten_second_loop(self, mock_loop):
        """Unit test for controller.tiny_ticker.main. Tests the call to the ten second loop."""
        test_url = ['http://www.fakeurl.com/rss']
        main(self.test_view, test_url)
        mock_loop.assert_called_with('www.fakeurl.com/rss')


