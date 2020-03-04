import sys

sys.path.append('/Users/jamescoleman/PycharmProjects/Python-RSS-ticker/Controller')

import unittest
from atomfeeds import feed as ams

class TestAtomFeed(unittest.TestCase):

    def test_atomFeedDemo(self):
        assert  ams.atomfeedDemoModule() == 'inside atom feed Demo Module'


if __name__ == '__main__':
    unittest.main()
