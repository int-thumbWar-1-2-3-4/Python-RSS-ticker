import unittest
import os
import sys
from unittest.mock import patch

from model import feed_manager
from model.feed import Feed

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import timedelta, date, datetime
from model.feed_manager import *


class ArticleTestCase(unittest.TestCase):

    def test_article(self):
        # TODO: Test Article creation with mock of datetime
        article_title = "Test Article"
        article_link = "https://www.theguardian.com/us-news/2020/apr/08/bernie-sanders-ends-2020-presidential-race"
        # article_published_date = datetime mock



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


class FeedManagerTestCase(unittest.TestCase):

    def test_feed_manager_add(self):
        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago (most recent)
        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago
        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))    # 4 days ago

        article_list = [article_1, article_2, article_3]
        test_feed_manager = Feed_Manager()

        self.assertFalse(test_feed_manager.add(article_1, "Test Feed 1")) # Dont add if feed not created through update()

        test_feed_manager.update(article_list, "Test Feed 1")

        self.assertFalse(test_feed_manager.add(article_2, "Test Feed 2"))
        self.assertTrue(test_feed_manager.add(article_4, "Test Feed 1"))

    def test_feed_manager_get_next_article(self):
        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago (most recent)
        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago
        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))    # 4 days ago
        article_list_1 = [article_1, article_2, article_3]

        article_5 = Article("Article 5", "Link 5", (datetime.now() - timedelta(days=5)))    # 5 days ago
        article_6 = Article("Article 6", "Link 6", (datetime.now() - timedelta(days=6)))    # 6 days ago
        article_7 = Article("Article 7", "Link 7", (datetime.now() - timedelta(days=7)))    # 7 days ago
        article_list_2 = [article_5, article_6, article_7]

        test_feed_manager = Feed_Manager()
        test_feed_manager.update(article_list_1, "Test Feed 1")
        test_feed_manager.update(article_list_2, "Test Feed 2")

        self.assertEqual(test_feed_manager.get_next_article(), article_1)
        self.assertEqual(test_feed_manager.get_next_article(), article_5)  # Should rotate feeds

        test_feed_manager.get_next_article()

        self.assertEqual(test_feed_manager.get_next_article(), article_2)  # Should wrap around to next article from first feed

        article_list = [article_1, article_3, article_4]
        test_feed_manager.update(article_list, "Test Feed 1")      # If current article in feed no longer exists after update,
        self.assertEqual(test_feed_manager.get_next_article(), article_1)      # feed should restart at newest

    def test_feed_manager_is_empty(self):
        test_feed_manager = Feed_Manager()

        self.assertTrue(test_feed_manager.is_empty())

        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago (most recent)
        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago
        article_list = [article_1, article_2, article_3]
        test_feed_manager.update(article_list, "Test Feed")

        self.assertFalse(test_feed_manager.is_empty())

    def test_feed_manager_remove(self):
        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago (most recent)
        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago

        article_list = [article_1, article_2, article_3]
        test_feed_manager = Feed_Manager()
        test_feed_manager.update(article_list, "Test Feed 1")

        self.assertFalse(test_feed_manager.remove("Test Feed 2"))
        self.assertTrue(test_feed_manager.remove("Test Feed 1"))
        self.assertEqual(test_feed_manager.size(), 0)

    def test_feed_manager_size(self):
        test_feed_manager = Feed_Manager()

        self.assertEqual(test_feed_manager.size(), 0)

        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago (most recent)
        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago
        article_list = [article_1, article_2, article_3]
        test_feed_manager.update(article_list, "Test Feed")

        self.assertEqual(test_feed_manager.size(), 3)

        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))    # 4 days ago
        test_feed_manager.add(article_4, "Test Feed")

        self.assertEqual(test_feed_manager.size(), 4)

    def test_feed_manager_update(self):
        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago (most recent)
        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago
        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))    # 4 days ago

        article_list = [article_1, article_2, article_3]
        test_feed_manager = Feed_Manager()
        test_feed_manager.update(article_list, "Test Feed 1")

        self.assertEqual(test_feed_manager.size(), 1)

        article_list = [article_2, article_3, article_4]
        test_feed_manager.update(article_list, "Test Feed 1")

        self.assertEqual(test_feed_manager.size(), 1)

        article_list = [article_1, article_3, article_4]
        test_feed_manager.update(article_list, "Test Feed 2")

        self.assertEqual(test_feed_manager.size(), 2)

        article_list = [article_1, article_2, article_4]
        test_feed_manager.update(article_list, "Test Feed 2")

        self.assertEqual(test_feed_manager.size(), 2)

    def test_parse(self):
        # TODO: Create test for parse()
        pass


if __name__ == '__main__':
    unittest.main()
