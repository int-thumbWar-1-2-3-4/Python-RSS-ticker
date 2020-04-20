import unittest
import sys
from unittest.mock import Mock
import model.parser as parser


sys.modules['atoma'] = Mock()
sys.modules['requests'] = Mock()
sys.modules['lxml'] = Mock()
sys.modules['bs4'] = Mock()


# @patch('parser.bs4.BeautifulSoup')
class test_parser(unittest.TestCase):

    def test_get_multi_feed_contents(self):
        # TODO: Create a test for get_multi_feed_contents()
        pass

    def test_get_feed_contents(self):
        # TODO: Create a test for get_feed_contents()
        pass

