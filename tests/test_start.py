from unittest.mock import Mock, patch
from controller import start
import unittest


class TestStart(unittest.TestCase):

    @patch('controller.start.call_switch_display')
    @patch('controller.start.th.Timer')
    def test_ten_second_loop(self, mock_timer, mock_call_switch):
        start.ten_second_loop()
        mock_timer.assert_called_with(10, start.ten_second_loop())
        assert mock_timer.called
        assert mock_call_switch.called
