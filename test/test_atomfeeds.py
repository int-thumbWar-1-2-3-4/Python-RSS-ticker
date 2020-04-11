import unittest
import sys
import os

directory = os.path.dirname(__file__)
relativePath = directory[0: len(directory) - 5]

sys.path.append(relativePath)
from controller.atomfeeds import feed as ams


class TestAtomFeed(unittest.TestCase):

    def test_atomFeedDemo(self):
        assert ams.atomfeedDemoModule() == 'inside atom feed Demo Module'


if __name__ == '__main__':
    unittest.main()
