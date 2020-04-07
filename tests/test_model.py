import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import timedelta, date, datetime
from model.model import *
from unittest.mock import Mock, patch


class ModelTestCase(unittest.TestCase):

    def test_article(self):
        article_title = "title"
        article_link = "link"
        article_datetime = "datetime"

        article = Article(article_title, article_link, article_datetime)

        self.assertEqual(article.title, article_title)
        self.assertEqual(article.link, article_link)
        self.assertEqual(article.datetime, article_datetime)

    def test_feed_add(self):
        feed_name = "Feed Name"
        feed = Feed(feed_name)

        self.assertFalse(feed.add(None))

        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago
        feed.add(article_1)

        self.assertFalse(feed.is_empty())
        self.assertEqual(feed.get_current(), article_1)

    def test_feed_is_empty(self):
        feed_name = "Feed Name"
        feed = Feed(feed_name)

        self.assertTrue(feed.is_empty())

        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago
        feed.add(article_1)

        self.assertFalse(feed.is_empty())

    def test_feed_is_sorted(self):
        feed_name = "Feed Name"
        feed = Feed(feed_name)

        self.assertFalse(feed.is_sorted())

        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        feed.add(article_2)

        self.assertTrue(feed.is_sorted())

        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago (most recent)
        feed.add(article_1)

        self.assertTrue(feed.is_sorted())

        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago
        feed.add(article_3)

        self.assertTrue(feed.is_sorted())

        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))    # 4 days ago
        feed.update([article_1, article_4, article_2, article_3])

        self.assertTrue(feed.is_sorted())

    def test_feed_get_current(self):
        feed_name = "Feed Name"
        feed = Feed(feed_name)

        self.assertIsNone(feed.get_current())

        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago
        feed.add(article_1)

        self.assertEqual(feed.get_current(), article_1)

        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago
        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))    # 4 days ago
        feed.update([article_1, article_2, article_3, article_4])

        self.assertEqual(feed.get_current(), article_1)
        self.assertEqual(feed.get_current(), article_1) # Should be the same when it's called multiple times

        feed.get_next()
        self.assertEqual(feed.get_current(), article_2) # Should be next entry
        self.assertEqual(feed.get_current(), article_2) # Should be the same when it's called multiple times

        feed.update([article_2, article_4])
        self.assertEqual(feed.get_current(), article_2) # Should stay the same as long as it exists after updating.

    def test_feed_get_next(self):
        feed_name = "Feed Name"
        feed = Feed(feed_name)

        self.assertIsNone(feed.get_next())

        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago
        feed.add(article_1)

        self.assertEqual(feed.get_next(), feed.get_current()) # These are the same when there is only one article.

        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago
        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))    # 4 days ago
        feed.update([article_1, article_2, article_3, article_4])

        self.assertEqual(feed.get_next(), article_1)
        self.assertEqual(feed.get_next(), article_2)
        self.assertEqual(feed.get_next(), article_3)
        self.assertEqual(feed.get_next(), article_4)
        self.assertEqual(feed.get_next(), article_1) # Should loop around end to start

    #       article_2 is now current

        feed.update([article_2, article_4])
        self.assertEqual(feed.get_next(), article_4)

        feed.update([article_1, article_3])
        self.assertEqual(feed.get_next(), article_1) # Should default to newest article

    def test_feed_update(self):
        # TODO: Get test_feed_sort() to work
        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago (most recent)
        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago

        feed_name = "Feed Name"
        feed = Feed(feed_name)
        feed.update([article_1, article_2, article_3])

        self.assertEqual(feed.get_current(), article_1)

        feed.update(None) # Should not replace with None
        self.assertEqual(feed.get_current(), article_1)

        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))    # 3 days ago
        feed.update([article_2, article_3, article_4])

        self.assertEqual(feed.get_current(), article_2) # Should default to newest

        feed.get_next()
        feed.get_next()
        # article_4 is now current

        feed.update([article_1, article_4, article_2])
        self.assertEqual(feed.get_current(), article_4) # Current should stay the same between updates if possible.

    def test_model(self):
        # TODO: Create test for Model
        pass

    def test_model_add_list(self):
        # TODO: Create test for Model.add(list_of_articles)
        pass

    def test_model_add_article(self):
        # TODO: Create test for Model.add(article)
        pass

    def test_model_remove(self):
        # TODO: Create test for Model.remove()
        pass

    def test_parse(self):
        # TODO: Create test for parse()
        pass



if __name__ == '__main__':
    unittest.main()
