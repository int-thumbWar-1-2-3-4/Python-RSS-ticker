from unittest.mock import Mock, patch
from controller.start import ten_second_loop
import unittest

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestStart(unittest.TestCase):

    def test_ten_second_loop(self):
        pass

    def test_call_switch_display(self):
        pass
