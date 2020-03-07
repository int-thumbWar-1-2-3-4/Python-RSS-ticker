import unittest
from  import feed as rs


class TestRSSFeed(unittest.TestCase):

    def test_rssFeedDemo(self):
        assert rs.rssFeedDemoModule() == 'inside rss Feed Demo Module'


if __name__ == '__main__':
    unittest.main()
