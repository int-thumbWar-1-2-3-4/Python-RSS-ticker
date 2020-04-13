import unittest
import os
import sys

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
        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago
        feed = Feed("Feed Name", [article_1])

        self.assertFalse(feed.add_new(article_1))   # Should not add duplicate
        self.assertEqual(feed.get_current_article(), article_1)

        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))    # 4 days ago

        self.assertTrue(feed.add_new(article_4))

    def test_feed_contains(self):

        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago (most recent)

        test_feed = Feed("Test Feed", [article_1])

        self.assertTrue(test_feed.contains(article_1))

        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago
        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))    # 4 days ago
        test_feed.update([article_2, article_3, article_4])

        self.assertFalse(test_feed.contains(article_1))

        self.assertTrue(test_feed.contains(article_2))
        self.assertTrue(test_feed.contains(article_3))
        self.assertTrue(test_feed.contains(article_4))


    def test_feed_is_sorted(self):
        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago
        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        feed = Feed("Feed Name", [article_1, article_2])

        self.assertTrue(feed.is_sorted())

        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago
        feed.add_new(article_3)

        self.assertTrue(feed.is_sorted())

        article_4 = Article("Article 4_1", "Link 4_1", (datetime.now() - timedelta(days=4)))    # 4 days ago
        feed.update([article_1, article_4, article_2, article_3])

        self.assertTrue(feed.is_sorted())

        article_4 = Article("Article 4_2", "Link 4_2", (datetime.now() - timedelta(days=4)))    # 4 days ago

    def test_feed_get_current_article(self):
        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago
        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        test_feed = Feed("Test Feed", [article_1, article_2])

        self.assertEqual(test_feed.get_current_article(), article_1) # Should start to first entry

        test_feed.get_next_article() # Advance current article to article_2

        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago
        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))    # 4 days ago
        test_feed.update([article_1, article_3, article_4])

        # Should default to first entry if current article does not exist after update.
        self.assertEqual(test_feed.get_current_article(), article_1)

        test_feed.get_next_article() # Advance current article to article_3
        test_feed.update([article_1, article_3, article_2])

        self.assertEqual(test_feed.get_current_article(), article_3) # Should stay the same between updates if possible

    def test_feed_get_next_article(self):
        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago (most recent)
        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        test_feed = Feed("Test Feed", [article_1, article_2])

        self.assertEqual(test_feed.get_current_article(), article_1)
        self.assertEqual(test_feed.get_next_article(), article_2)

        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago
        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))    # 4 days ago
        test_feed.update([article_1, article_3, article_4])

        # Should default to the newest if the same current article no longer exists after the update
        self.assertEqual(test_feed.get_next_article(), article_3)

        test_feed.update([article_1, article_3, article_4])

        # Current article should stay same between updates if possible
        self.assertEqual(test_feed.get_next_article(), article_4)
        self.assertEqual(test_feed.get_next_article(), article_1) # Should loop around end to start

    def test_feed_update(self):
        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago (most recent)
        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago

        feed_name = "Feed Name"
        feed = Feed(feed_name, [article_1, article_2, article_3])

        self.assertEqual(feed.get_current_article(), article_1)

        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))    # 3 days ago
        feed.update([article_2, article_3, article_4])

        self.assertEqual(feed.get_current_article(), article_2) # Should default to newest

        feed.get_next_article()

        self.assertEqual(feed.get_current_article(), article_3)

        feed.get_next_article()
        self.assertEqual(feed.get_current_article(), article_4) # article_4 is now current

        feed.update([article_1, article_4, article_2])
        self.assertEqual(feed.get_current_article(), article_4) # Current should be the same between updates if possible

        feed.update([])
        self.assertEqual(feed.get_current_article(), article_4) # Should not update if given list is empty


class FeedManagerTestCase(unittest.TestCase):

    def test_feed_manager_add(self):
        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago (most recent)
        test_feed_name = "Test Feed 1"
        test_feed_manager = Feed_Manager()

        boolean = test_feed_manager.add(article_1, test_feed_name)
        self.assertFalse(boolean) # Dont add if feed not created through update()

        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago
        test_feed_manager.update([article_1, article_2, article_3], test_feed_name)

        self.assertFalse(test_feed_manager.add(article_2, "Test Feed 2"))

        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))    # 4 days ago

        self.assertTrue(test_feed_manager.add(article_4, test_feed_name))

    def test_feed_manager_get_next_article(self):
        test_feed_manager = Feed_Manager()
        test_feed_1_name = "Test Feed 1"

        article_1_1 = Article("Article 1_1", "Link 1_1", (datetime.now() - timedelta(days=1)))    # 1 day ago (most recent)
        article_1_2 = Article("Article 1_2", "Link 1_2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        article_1_3 = Article("Article 1_3", "Link 1_3", (datetime.now() - timedelta(days=3)))    # 3 days ago
        test_feed_manager.update([article_1_1, article_1_2, article_1_3], test_feed_1_name)

        self.assertEqual(test_feed_manager.get_current_article(), article_1_1)
        self.assertEqual(test_feed_manager.get_next_article(), article_1_2) # If only 1 feed, move to next within feed

        test_feed_2_name = "Test Feed 2"
        article_2_1 = Article("Article 2_1", "Link 2_1", (datetime.now() - timedelta(days=5)))    # 5 days ago
        article_2_2 = Article("Article 2_2", "Link 2_2", (datetime.now() - timedelta(days=6)))    # 6 days ago
        article_2_3 = Article("Article 2_3", "Link 2_3", (datetime.now() - timedelta(days=7)))    # 7 days ago
        test_feed_manager.update([article_2_1, article_2_2, article_2_3], test_feed_2_name)

        self.assertEqual(test_feed_manager.get_current_article(), article_1_2)
        self.assertEqual(test_feed_manager.get_next_article(), article_2_2)  # Should rotate between feeds,
                                                    # even though article_2_1 is older than all of the articles in test feed 1

        self.assertEqual(test_feed_manager.get_next_article(), article_1_3)  # Should wrap around to next article from first feed

        # article_1_3 is now the current

        article_1_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))    # 4 days ago
        article_list = [article_1_1, article_1_2, article_1_4]
        test_feed_manager.update(article_list, "Test Feed 1")
                                                                # If current article in feed no longer exists after update,
        self.assertEqual(test_feed_manager.get_current_article(), article_1_1)      # feed should restart at newest

    def test_feed_manager_contains(self):
        test_feed_manager = Feed_Manager()
        test_feed_name = "Test Feed"

        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago (most recent)
        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago

        self.assertFalse(test_feed_manager.contains(article_1, test_feed_name)) # Feed named "Test Feed" not created yet.

        test_feed_manager.update([article_1, article_2, article_3], test_feed_name)

        self.assertTrue(test_feed_manager.contains(article_1, test_feed_name))

        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))    # 4 days ago

        self.assertFalse(test_feed_manager.contains(article_4, test_feed_name))

    def test_feed_manager_is_empty(self):
        test_feed_manager = Feed_Manager()
        test_feed_name = "Test Feed"

        self.assertTrue(test_feed_manager.is_empty())

        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago (most recent)
        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago
        article_list = [article_1, article_2, article_3]
        test_feed_manager.update(article_list, test_feed_name)

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

        self.assertEqual(test_feed_manager.size(), 1)

        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=4)))    # 4 days ago
        test_feed_manager.add(article_4, "Test Feed")

        self.assertEqual(test_feed_manager.size(), 1)

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
