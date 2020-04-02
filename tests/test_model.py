import unittest

from datetime import timedelta, date, datetime
from model.model import *
from unittest.mock import Mock


class ModelTestCase(unittest.TestCase):

    def test_article(self):
        article_title = "title"
        article_link = "link"
        article_datetime = "datetime"

        article = Article(article_title, article_link, article_datetime)

        self.assertEqual(article.title, article_title)
        self.assertEqual(article.link, article_link)
        self.assertEqual(article.datetime, article_datetime)

    def test_feed(self):
        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago (most recent)
        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago

        feed_name = "Feed Name"
        feed = Feed(feed_name, [article_1, article_2, article_3])

        self.assertEqual(feed.name, feed_name)

    def test_feed_sort(self):
        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago (most recent)
        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago
        article_list = [article_3, article_2, article_1]    # Place them in reverse order to see if the sort works

        feed_name = "Feed Name"
        feed = Feed(feed_name, article_list)

        feed.sort()
        previous_article = None

        for article in feed.__list_of_articles:
            if previous_article is not None:
                self.assertGreater(previous_article.datetime, article.datetime)

            previous_article = article

    def test_feed_update(self):
        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago
        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=3)))    # 4 days ago
        article_list_1 = [article_1, article_3, article_4]    # In order from most recent to oldest

        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        article_list_2 = [article_1, article_2, article_3]    # In order from most recent to oldest

        feed_name = "Feed Name"
        feed = Feed(feed_name, article_list_1)

        feed.update(article_list_2)     # Should drop article_4 and add article_2 in the middle
        self.assertListEqual(feed.__list_of_articles, [article_1, article_2, article_3])

    def test_feed_get_next(self):
        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago
        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago
        article_list = [article_1, article_2, article_3]    # In order from most recent to oldest

        feed_name = "Feed Name"
        feed = Feed(feed_name, article_list)
        feed.__position = 0     # Initialize position at first entry in list (article_1)

        self.assertLess(feed.get_next(), article_1)

    def test_feed_add(self):
        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago
        article_4 = Article("Article 4", "Link 4", (datetime.now() - timedelta(days=3)))    # 4 days ago
        article_list = [article_1, article_3, article_4]    # In order from most recent to oldest

        feed_name = "Feed Name"
        feed = Feed(feed_name, article_list)
        feed.__position = 1     # Initialize position at second entry in list (article_3)

        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        feed.add(article_2)

        self.assertListEqual(feed.__list_of_articles, [article_1, article_2, article_3, article_4])
        self.assertEqual(feed.__position, 2)

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
