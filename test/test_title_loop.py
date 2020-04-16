import unittest
from unittest.mock import patch
from controller.start import ten_second_loop, call_switch_display
from model.article import Article

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestTitleLoop(unittest.TestCase):

    @patch('controller.start.th.Timer')
    @patch('view.main_view')
    @patch('controller.start.call_switch_display')
    def test_ten_second_loop_calls_its_self(self, mock_timer, mock_main_view, mock_switch_display):
        """ Unit test of controller.title_loop.ten_second_loop """
        test_feed = [Article('test title', "test url", "date")]
        ten_second_loop(mock_main_view, 7, test_feed)
        self.assertTrue(mock_timer.called)
        self.assertTrue(mock_switch_display.called)

    @patch('view.main_view.MainView')
    def test_call_switch_display(self, mock_main_view):
        """ Unit test of controller.title_loop.call_switch_display """
        test_feed = [Article('test title', "test url", "date")]
        call_switch_display(mock_main_view, test_feed)
        mock_main_view.display_entry.assert_called_with('test title', "test url")


