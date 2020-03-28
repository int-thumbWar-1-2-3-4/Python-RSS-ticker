from unittest.mock import Mock, patch
from model.model import Model
import unittest


class TestStart(unittest.TestCase):

    def test_ten_second_loop(self):
        self.assertTrue(Model.switch_displayed_entry().called)

    def test_headline_update_thread(self):
        pass