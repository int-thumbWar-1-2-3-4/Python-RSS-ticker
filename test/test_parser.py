import unittest
import sys
from unittest.mock import Mock
import model.parser as parser


# @patch('parser.bs4.BeautifulSoup')
class TestParser(unittest.TestCase):

    def test_get_multi_feed_contents(self):
        # TODO: Create a test for get_multi_feed_contents()
        pass

    def test_get_feed_contents(self):
        parser.get_feed_contents("C:/test.rss.xml")
        pass
