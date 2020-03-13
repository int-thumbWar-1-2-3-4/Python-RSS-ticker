import unittest
import sys
import os

directory = os.path.dirname(__file__)
relativePath = directory[0: len(directory) - 5]

sys.path.append(relativePath)
from Controller.rssfeeds import feed as rs


class TestRSSFeed(unittest.TestCase):

    def test_rssFeedDemo(self):
        assert rs.rssFeedDemoModule() == 'inside rss Feed Demo Module'


if __name__ == '__main__':
    unittest.main()
