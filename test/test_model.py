"""Test.test_model"""

import os
import sys
import unittest
from bs4 import BeautifulSoup
from model import parser
from datetime import timedelta, datetime
from model.parser import InvalidUrlException, InvalidRssException, get_feed_contents, get_feed_name
from unittest.mock import patch
from model.feed_manager import *

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class ArticleTestCase(unittest.TestCase):
    """Test class for model.article"""

    def test_article(self):
        """Unit test for model.article.Article"""

        article_title = "Test Article"
        article_link = "https://www.theguardian.com/us-news/2020/apr/08/bernie-sanders-ends-2020-presidential-race"
        article_published_date = datetime.now()
        test_article = Article(article_title, article_link, article_published_date)

        self.assertEqual(test_article.title, article_title)
        self.assertEqual(test_article.link, article_link)
        self.assertEqual(test_article.published_date, article_published_date)


class FeedTestCase(unittest.TestCase):
    """Test class for model.feed"""

    def test_feed_add_new(self):
        """Unit test for model.feed.Feed.add_new"""

        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))  # 1 day ago
        feed = Feed("Feed Name", "https://cyber.harvard.edu/rss/examples/rss2sample.xml", [article_1])

        self.assertFalse(feed.add_new(article_1))  # Should not add duplicate
        self.assertEqual(feed.get_current_article(), article_1)

        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))  # 4 days ago

        self.assertTrue(feed.add_new(article_4))

    def test_feed_contains(self):
        """Unit test for model.feed.Feed.contains"""

        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))  # 1 day ago (most recent)

        test_feed = Feed("Test Feed", "https://cyber.harvard.edu/rss/examples/rss2sample.xml", [article_1])

        self.assertTrue(test_feed.contains(article_1))

        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))  # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))  # 3 days ago
        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))  # 4 days ago
        test_feed.update([article_2, article_3, article_4])

        self.assertFalse(test_feed.contains(article_1))

        self.assertTrue(test_feed.contains(article_2))
        self.assertTrue(test_feed.contains(article_3))
        self.assertTrue(test_feed.contains(article_4))

    def test_feed_get_current_article(self):
        """Unit test for model.feed.Feed.get_current_article"""

        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))  # 1 day ago
        test_feed = Feed("Test Feed", "https://cyber.harvard.edu/rss/examples/rss2sample.xml", [article_1])
        self.assertEqual(test_feed.get_next_article(), article_1)  # Should stay at first entry since it only contains 1

        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))  # 2 days ago
        test_feed = Feed("Test Feed", "https://cyber.harvard.edu/rss/examples/rss2sample.xml", [article_1, article_2])

        self.assertEqual(test_feed.get_current_article(), article_1)  # Should start to first entry

        test_feed.get_next_article()  # Advance current article to article_2

        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))  # 3 days ago
        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))  # 4 days ago
        test_feed.update([article_1, article_3, article_4])

        # Should default to first entry if current article does not exist after update.
        self.assertEqual(test_feed.get_current_article(), article_1)

        test_feed.get_next_article()  # Advance current article to article_3
        test_feed.update([article_1, article_3, article_2])

        self.assertEqual(test_feed.get_current_article(), article_3)  # Should stay the same between updates if possible

    def test_feed_get_next_article(self):
        """Unit test for model.feed.Feed.get_next_article"""

        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))  # 1 day ago (most recent)
        test_feed = Feed("Test Feed", "https://cyber.harvard.edu/rss/examples/rss2sample.xml", [article_1])
        self.assertEqual(test_feed.get_next_article(), article_1)  # Should stay at first entry since it only contains 1

        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))  # 2 days ago
        test_feed = Feed("Test Feed", "https://cyber.harvard.edu/rss/examples/rss2sample.xml", [article_1, article_2])

        self.assertEqual(test_feed.get_next_article(), article_2)

        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))  # 3 days ago
        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))  # 4 days ago
        test_feed.update([article_1, article_3, article_4])

        # Should default to the newest if the same current article no longer exists after the update
        self.assertEqual(test_feed.get_next_article(), article_3)

        test_feed.update([article_1, article_3, article_4])

        # Current article should stay same between updates if possible
        self.assertEqual(test_feed.get_next_article(), article_4)
        self.assertEqual(test_feed.get_next_article(), article_1)  # Should loop around end to start

    def test_feed_update(self):
        """Unit test for model.feed.Feed.update"""

        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))  # 1 day ago (most recent)
        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))  # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))  # 3 days ago

        feed_name = "Feed Name"
        feed_link = "https://cyber.harvard.edu/rss/examples/rss2sample.xml"
        feed = Feed(feed_name, feed_link, [article_1, article_2, article_3])

        self.assertEqual(feed.get_current_article(), article_1)

        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))  # 3 days ago
        feed.update([article_2, article_3, article_4])

        self.assertEqual(feed.get_current_article(), article_2)  # Should default to newest

        feed.get_next_article()

        self.assertEqual(feed.get_current_article(), article_3)

        feed.get_next_article()
        self.assertEqual(feed.get_current_article(), article_4)  # article_4 is now current

        feed.update([article_1, article_4, article_2])
        self.assertEqual(feed.get_current_article(),
                         article_4)  # Current should be the same between updates if possible

        feed.update([])
        self.assertEqual(feed.get_current_article(), article_4)  # Should not update if given list is empty


class FeedManagerTestCase(unittest.TestCase):
    """Test class for model.feed_manager"""

    def test_feed_manager_add(self):
        """Unit test for model.feed_manager.FeedManager.add"""

        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))  # 1 day ago (most recent)
        test_feed_name = "Test Feed 1"
        test_feed_link = "https://cyber.harvard.edu/rss/examples/rss2sample.xml"
        test_feed_manager = FeedManager()

        boolean = test_feed_manager.add(article_1, test_feed_name)
        self.assertFalse(boolean)  # Dont add if feed not created through update()

        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))  # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))  # 3 days ago
        test_feed_manager.update(test_feed_name, test_feed_link, [article_1, article_2, article_3])

        self.assertFalse(test_feed_manager.add(article_2, "Test Feed 2"))

        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))  # 4 days ago

        self.assertTrue(test_feed_manager.add(article_4, test_feed_name))

    def test_feed_manager_contains(self):
        """Unit test for model.feed_manager.FeedManager.contains"""

        test_feed_manager = FeedManager()
        test_feed_name = "Test Feed"
        test_feed_link = "https://cyber.harvard.edu/rss/examples/rss2sample.xml"

        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))  # 1 day ago (most recent)
        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))  # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))  # 3 days ago

        self.assertFalse(
            test_feed_manager.contains(article_1, test_feed_name))  # Feed named "Test Feed" not created yet.

        test_feed_manager.update(test_feed_name, test_feed_link, [article_1, article_2, article_3])

        self.assertTrue(test_feed_manager.contains(article_1, test_feed_name))

        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))  # 4 days ago

        self.assertFalse(test_feed_manager.contains(article_4, test_feed_name))

    def test_feed_manager_get_current_article(self):
        """Unit test for model.feed_manager.FeedManager.get_current_article"""

        test_feed_manager = FeedManager()
        test_feed_name = "Test Feed 1"
        test_feed_link = "https://cyber.harvard.edu/rss/examples/rss2sample.xml"

        article_1_1 = Article("Article 1_1", "Link 1_1",
                              (datetime.now() - timedelta(days=1)))  # 1 day ago (most recent)
        article_1_2 = Article("Article 1_2", "Link 1_2", (datetime.now() - timedelta(days=2)))  # 2 days ago
        article_1_3 = Article("Article 1_3", "Link 1_3", (datetime.now() - timedelta(days=3)))  # 3 days ago
        test_feed_manager.update(test_feed_name, test_feed_link, [article_1_1, article_1_2, article_1_3])

        #                                                   If current article in feed no longer exists after update,
        self.assertEqual(test_feed_manager.get_current_article(), article_1_1)  # feed should restart at newest

        test_feed_manager.remove(test_feed_name)
        # tes_feed_manager should be empty now

        self.assertTrue(test_feed_manager.is_empty())
        self.assertRaises(FeedManagerEmptyException, test_feed_manager.get_current_article)

    def test_feed_manager_get_next_article(self):
        """Unit test for model.feed_manager.FeedManager.get_next_article"""

        test_feed_manager = FeedManager()
        test_feed_1_name = "Test Feed 1"
        test_feed_1_link = "https://cyber.harvard.edu/rss/examples/rss2sample.xml"

        article_1_1 = Article("Article 1_1", "Link 1_1",
                              (datetime.now() - timedelta(days=1)))  # 1 day ago (most recent)
        article_1_2 = Article("Article 1_2", "Link 1_2", (datetime.now() - timedelta(days=2)))  # 2 days ago
        article_1_3 = Article("Article 1_3", "Link 1_3", (datetime.now() - timedelta(days=3)))  # 3 days ago
        test_feed_manager.update(test_feed_1_name, test_feed_1_link, [article_1_1, article_1_2, article_1_3])

        self.assertEqual(test_feed_manager.get_next_article(), article_1_2)  # If only 1 feed, move to next within feed

        test_feed_2_name = "Test Feed 2"
        test_feed_2_link = "https://www.theguardian.com/world/rss"
        article_2_1 = Article("Article 2_1", "Link 2_1", (datetime.now() - timedelta(days=5)))  # 5 days ago
        article_2_2 = Article("Article 2_2", "Link 2_2", (datetime.now() - timedelta(days=6)))  # 6 days ago
        article_2_3 = Article("Article 2_3", "Link 2_3", (datetime.now() - timedelta(days=7)))  # 7 days ago
        test_feed_manager.update(test_feed_2_name, test_feed_2_link, [article_2_1, article_2_2, article_2_3])

        self.assertEqual(test_feed_manager.get_next_article(), article_2_2)  # Should rotate between feeds,
        # even though article_2_1 is older than all of the articles in test feed 1

        self.assertEqual(test_feed_manager.get_next_article(),
                         article_1_3)  # Should wrap around to next article from first feed

        # article_1_3 is now the current

        article_1_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))  # 4 days ago
        article_list = [article_1_1, article_1_2, article_1_4]
        test_feed_manager.update(test_feed_1_name, test_feed_1_link, article_list)

        #                                                   If current article in feed no longer exists after update,
        self.assertEqual(test_feed_manager.get_current_article(), article_1_1)  # feed should restart at newest

        test_feed_manager.remove(test_feed_1_name)
        test_feed_manager.remove(test_feed_2_name)
        # tes_feed_manager should be empty now

        self.assertRaises(FeedManagerEmptyException, test_feed_manager.get_next_article)

    def test_feed_manager_is_empty(self):
        """Unit test for model.feed_manager.FeedManager.is_empty"""

        test_feed_manager = FeedManager()
        test_feed_name = "Test Feed"
        test_feed_link = "https://cyber.harvard.edu/rss/examples/rss2sample.xml"

        self.assertTrue(test_feed_manager.is_empty())

        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))  # 1 day ago (most recent)
        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))  # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))  # 3 days ago
        article_list = [article_1, article_2, article_3]
        test_feed_manager.update(test_feed_name, test_feed_link, article_list)

        self.assertFalse(test_feed_manager.is_empty())

    def test_feed_manager_remove(self):
        """Unit test for model.feed_manager.FeedManager.remove"""

        test_feed_1_name = "Test Feed 1"
        test_feed_1_link = "https://cyber.harvard.edu/rss/examples/rss2sample.xml"

        article_1_1 = Article("Article 1_1", "Link 1_1",
                              (datetime.now() - timedelta(days=1)))  # 1 day ago (most recent)
        article_1_2 = Article("Article 1_2", "Link 1_2", (datetime.now() - timedelta(days=2)))  # 2 days ago
        article_1_3 = Article("Article 1_3", "Link 1_3", (datetime.now() - timedelta(days=3)))  # 3 days ago

        test_feed_manager = FeedManager()
        test_feed_manager.update(test_feed_1_name, test_feed_1_link, [article_1_1, article_1_2, article_1_3])

        test_feed_2_name = "Test Feed 2"
        test_feed_2_link = "https://www.theguardian.com/world/rss"
        self.assertFalse(test_feed_manager.remove(test_feed_2_name))

        article_2_1 = Article("Article 2_1", "Link 2_1", (datetime.now() - timedelta(days=5)))  # 5 days ago
        article_2_2 = Article("Article 2_2", "Link 2_2", (datetime.now() - timedelta(days=6)))  # 6 days ago
        article_2_3 = Article("Article 2_3", "Link 2_3", (datetime.now() - timedelta(days=7)))  # 7 days ago
        test_feed_manager.update(test_feed_2_name, test_feed_2_link, [article_2_1, article_2_2, article_2_3])

        test_feed_3_name = "Test Feed 3"
        test_feed_3_link = "https://www.theguardian.com/us/rss"
        article_3_1 = Article("Article 3_1", "Link 3_1", (datetime.now() - timedelta(days=5)))  # 5 days ago
        article_3_2 = Article("Article 3_2", "Link 3_2", (datetime.now() - timedelta(days=6)))  # 6 days ago
        article_3_3 = Article("Article 3_3", "Link 3_3", (datetime.now() - timedelta(days=7)))  # 7 days ago
        test_feed_manager.update(test_feed_3_name, test_feed_3_link, [article_3_1, article_3_2, article_3_3])

        self.assertEqual(test_feed_manager.get_next_article(), article_2_2)
        self.assertEqual(test_feed_manager.get_next_article(), article_3_2)

        self.assertTrue(test_feed_manager.remove(test_feed_3_name))
        # Current feed is now feed 1

        # Advance current feed to feed 2
        self.assertEqual(test_feed_manager.get_next_article(), article_2_3)

        self.assertTrue(test_feed_manager.remove(test_feed_1_name)) # Current_feed_index should decrement with this

    def test_feed_manager_size(self):
        """Unit test for model.feed_manager.FeedManager.size"""

        test_feed_manager = FeedManager()

        self.assertEqual(test_feed_manager.size(), 0)

        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))  # 1 day ago (most recent)
        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))  # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))  # 3 days ago
        article_list = [article_1, article_2, article_3]

        test_feed_1_name = "Test Feed 1"
        test_feed_1_link = "https://cyber.harvard.edu/rss/examples/rss2sample.xml"
        test_feed_manager.update(test_feed_1_name, test_feed_1_link, article_list)

        self.assertEqual(test_feed_manager.size(), 1)

        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))  # 4 days ago
        test_feed_manager.add(article_4, "Test Feed")

        self.assertEqual(test_feed_manager.size(), 1)

    def test_feed_manager_update(self):
        """Unit test for model.feed_manager.FeedManager.update"""

        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))  # 1 day ago (most recent)
        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))  # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))  # 3 days ago
        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))  # 4 days ago

        test_feed_1_name = "Test Feed 1"
        test_feed_1_link = "https://cyber.harvard.edu/rss/examples/rss2sample.xml"
        article_list = [article_2, article_3, article_4]

        test_feed_manager = FeedManager()
        test_feed_manager.update(test_feed_1_name, test_feed_1_link, article_list)

        self.assertEqual(test_feed_manager.size(), 1)

        article_list = [article_2, article_3, article_4]
        test_feed_manager.update(test_feed_1_name, test_feed_1_link, article_list)

        self.assertEqual(test_feed_manager.size(), 1)

        test_feed_2_name = "Test Feed 2"
        test_feed_2_link = "https://www.theguardian.com/world/rss"
        article_list = [article_1, article_3, article_4]
        test_feed_manager.update(test_feed_2_name, test_feed_2_link, article_list)

        self.assertEqual(test_feed_manager.size(), 2)

        article_list = [article_1, article_2, article_4]
        test_feed_manager.update(test_feed_2_name, test_feed_2_link, article_list)

        self.assertEqual(test_feed_manager.size(), 2)


class TestParser(unittest.TestCase):
    """Test class for model.parser"""

    def test_get_multi_feed_contents_with_bad_url(self):
        """Unit test for model.parser.get_multi_feed_contents"""
        # TODO: DELETE test_get_multi_feed_contents_with_bad_url as get_multi_feed_contents is not functional

        with self.assertRaises(InvalidUrlException):
            parser.get_multi_feed_contents([])

    def test_check_url(self):
        """Unit test for model.parser._check_url"""

        parser._check_url('www.test_url.net/feeds/xml/')
        parser._check_url('www.test_url.net/feeds/rss')
        parser._check_url('www.test_url.net/feeds/atom')

        with self.assertRaises(InvalidUrlException):
            parser._check_url('www.thistestshallnotpass.com')

        with self.assertRaises(InvalidUrlException):
            parser._check_url('')

    def test_parse_rss_without_channel(self):
        """Unit test for model.parser._parse_rss"""

        feed_with_no_channel = BeautifulSoup('''<?xml version="1.0" encoding="utf-8"?>
            <?xml-stylesheet title="XSL_formatting" type="text/xsl" href="/shared/bsp/xsl/rss/nolsol.xsl"?><rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:media="http://search.yahoo.com/mrss/">
            </rss>''', 'lxml-xml')

        with self.assertRaises(InvalidRssException):
            parser._parse_rss(feed_with_no_channel)

    def test_parse_rss_without_title(self):
        """Unit test for model.parser._parse_rss"""

        feed_with_no_title = BeautifulSoup('''<?xml version="1.0" encoding="utf-8"?>
            <?xml-stylesheet title="XSL_formatting" type="text/xsl" href="/shared/bsp/xsl/rss/nolsol.xsl"?><rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:media="http://search.yahoo.com/mrss/">
            <channel>
                <description>BBC News - Home</description>
            </channel>
            </rss>''', 'lxml-xml')

        with self.assertRaises(InvalidRssException):
            parser._parse_rss(feed_with_no_title)

    def test_parse_rss_without_link(self):
        """Unit test for model.parser._parse_rss"""

        feed_with_no_link = BeautifulSoup('''<?xml version="1.0" encoding="utf-8"?>
            <?xml-stylesheet title="XSL_formatting" type="text/xsl" href="/shared/bsp/xsl/rss/nolsol.xsl"?><rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:media="http://search.yahoo.com/mrss/">
            <channel>
                <title>BBC News</title>
                <description>BBC News - Home</description>
            </channel>
            </rss>''', 'lxml-xml')

        with self.assertRaises(InvalidRssException):
            parser._parse_rss(feed_with_no_link)

    @patch('model.parser.requests.get')
    @patch('model.parser.BeautifulSoup')
    def test_get_feed_contents_without_item(self, mock_get, mock_bs):
        """Unit test for model.parser._get_feed_contents"""

        feed_with_no_item = ''' <?xml version="1.0" encoding="utf-8"?>
            <?xml-stylesheet title="XSL_formatting" type="text/xsl" href="/shared/bsp/xsl/rss/nolsol.xsl"?><rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:media="http://search.yahoo.com/mrss/">
            </rss>'''

        get_feed_contents.bs_feed = feed_with_no_item

        with self.assertRaises(InvalidRssException):
            get_feed_contents('http://feeds.bbci.co.uk/news/rss.xml')

    def test_get_feed_contents_with_bad_input(self):
        """Unit test for model.parser._get_feed_contents"""

        with self.assertRaises(InvalidUrlException):
            get_feed_contents('')

    def test_get_feed_name_with_bad_input(self):
        """Unit test for model.parser._get_feed_name"""

        with self.assertRaises(InvalidUrlException):
            get_feed_name('')


if __name__ == '__main__':
    unittest.main()
