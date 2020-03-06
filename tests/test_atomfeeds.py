import sys
import unittest

sys.path.append('/Users/jamescoleman/Programming/Python Projects/Python-RSS-ticker/Controller')


from atomfeeds import feed as ams


class TestAtomFeed(unittest.TestCase):

    def test_atomFeedDemo(self):
        assert ams.atomfeedDemoModule() == 'inside atom feed Demo Module'


if __name__ == '__main__':
    unittest.main()
