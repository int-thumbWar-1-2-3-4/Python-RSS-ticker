import sys
import unittest


sys.path.append('/Users/jamescoleman/Programming/Python Projects/Python-RSS-ticker/Controller')

from rssfeeds import feed as rs


class TestRSSFeed(unittest.TestCase):

    def test_rssFeedDemo(self):
        assert rs.rssFeedDemoModule() == 'inside rss Feed Demo Module'


if __name__ == '__main__':
    unittest.main()
