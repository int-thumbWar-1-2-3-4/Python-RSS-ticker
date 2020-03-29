from unittest.mock import Mock, patch
from model.model import Model
from controller import start
import unittest


class TestStart(unittest.TestCase):

    @patch('model.model.Model.switch_displayed_entry')
    def test_ten_second_loop(self, mock_switch):
        start.ten_second_loop()
        self.assertTrue(mock_switch().called)

    def test_headline_update_thread(self):
        pass