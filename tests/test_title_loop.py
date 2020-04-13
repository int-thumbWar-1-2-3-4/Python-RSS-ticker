import unittest
from unittest.mock import patch
from controller import title_loop
from model.model import Article

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestTitleLoop(unittest.TestCase):

    @patch('controller.title_loop.th.Timer')
    @patch('view.main_view')
    @patch('controller.title_loop.call_switch_display')
    def test_ten_second_loop(self, mock_timer, mock_main_view, mock_switch_display):
        """ Unit test of controller.title_loop.ten_second_loop """
        title_loop.mv = mock_main_view
        title_loop.t = 7
        title_loop.ten_second_loop(title_loop.mv, title_loop.t)
        self.assertTrue(mock_timer.called)
        # title_loop.ten_second_loop.assert_called_with(mock_main_view, 7)
        self.assertTrue(mock_switch_display.called)

    @patch('view.main_view.MainView')
    def test_call_switch_display(self, mock_main_view):
        """ Unit test of controller.title_loop.call_switch_display """
        title_loop.test_feed = [Article('test title', "test url", "date")]
        title_loop.call_switch_display(mock_main_view)
        mock_main_view.display_entry.assert_called_with('test title', "test url")
