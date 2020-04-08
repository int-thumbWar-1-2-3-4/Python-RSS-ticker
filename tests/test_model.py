import unittest
import os
import sys

from model.feed import Feed

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import timedelta, date, datetime
from model.model import *


class ArticleTestCase(unittest.TestCase):

    def test_article(self):
        # TODO: Create test for Article
        pass


class FeedTestCase(unittest.TestCase):

    def test_feed_add_new(self):
        feed_name = "Feed Name"
        feed = Feed(feed_name)

        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago

        self.assertTrue(feed.add_new(article_1))
        self.assertFalse(feed.add_new(article_1))   # Should not add duplicate
        self.assertEqual(feed.current_article, article_1)

        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago
        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))    # 4 days ago
        feed.update([article_2, article_3, article_4])
        feed.add_new(article_1)
        self.assertEqual(feed.current_article, article_1) # Should default to the new article.py


    def test_feed_is_empty(self):
        feed_name = "Feed Name"
        feed = Feed(feed_name)

        self.assertTrue(feed.is_empty())

        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago
        feed.add_new(article_1)

        self.assertFalse(feed.is_empty())

    def test_feed_is_sorted(self):
        feed_name = "Feed Name"
        feed = Feed(feed_name)

        self.assertFalse(feed.is_sorted())

        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        feed.add_new(article_2)

        self.assertTrue(feed.is_sorted())

        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago (most recent)
        feed.add_new(article_1)

        self.assertTrue(feed.is_sorted())

        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago
        feed.add_new(article_3)

        self.assertTrue(feed.is_sorted())

        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))    # 4 days ago
        feed.update([article_1, article_4, article_2, article_3])

        self.assertTrue(feed.is_sorted())

    def test_feed_move_to_next(self):
        feed_name = "Feed Name"
        feed = Feed(feed_name)

        self.assertFalse(feed.move_to_next())

        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago
        feed.add_new(article_1)

        self.assertFalse(feed.move_to_next())

        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago
        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))    # 4 days ago
        feed.update([article_2, article_3, article_4])

        self.assertEqual(feed.current_article, article_2)

        self.assertTrue(feed.move_to_next())
        self.assertEqual(feed.current_article, article_3)

        feed.move_to_next()

        self.assertEqual(feed.current_article, article_4)

        feed.move_to_next()

        self.assertEqual(feed.current_article, article_2) # Should loop around end to start

    def test_feed_update(self):
        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago (most recent)
        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago

        feed_name = "Feed Name"
        feed = Feed(feed_name)
        feed.update([article_1, article_2, article_3])

        self.assertEqual(feed.current_article, article_1)

        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))    # 3 days ago
        feed.update([article_2, article_3, article_4])

        self.assertEqual(feed.current_article, article_2) # Should default to newest

        feed.move_to_next()
        feed.move_to_next()
        # article_4 is now current

        feed.update([article_1, article_4, article_2])
        self.assertEqual(feed.current_article, article_4) # Current should stay the same between updates if possible.


class ModelTestCase(unittest.TestCase):

    def test_model(self):
        # TODO: Create test for Model
        pass

    def test_model_add_list(self):
        # TODO: Create test for Model.add(list_of_articles)
        pass

    def test_model_add_article(self):
        # TODO: Create test for Model.add(article.py)
        pass

    def test_model_remove(self):
        # TODO: Create test for Model.remove()
        pass

    def test_parse(self):
        # TODO: Create test for parse()
        pass


if __name__ == '__main__':
    unittest.main()
