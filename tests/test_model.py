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
        feed_name = "Feed Name"

        feed = Feed(feed_name)

        self.assertEqual(feed.name, feed_name)

    def test_feed_sort(self):
        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago
        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago
        article_list = [article_1, article_2, article_3]

        feed_name = "Feed Name"
        feed = Feed(feed_name)
        feed.__list_of_articles = article_list  # Manually set the value of __list_of_articles to avoid calling update()
        feed.sort()

        previous_article = None

        for article in feed.__list_of_articles:
            if previous_article is not None:
                self.assertGreater(previous_article.datetime, article.datetime)

            previous_article = article

    def test_feed_update(self):
        article_1 = Article("Article 1", "Link 1", (datetime.now() - timedelta(days=1)))    # 1 day ago
        article_2 = Article("Article 2", "Link 2", (datetime.now() - timedelta(days=2)))    # 2 days ago
        article_3 = Article("Article 3", "Link 3", (datetime.now() - timedelta(days=3)))    # 3 days ago
        article_list = [article_1, article_2, article_3]

        feed_name = "Feed Name"
        feed = Feed(feed_name)
        feed.__list_of_articles = []
        feed.update(article_list)

        self.assertListEqual(article_list, feed.__list_of_articles)


    def test_feed_get_next(self):
        # TODO: Create test for Feed.get_next()
        pass

    def test_feed_add(self):
        # TODO: Create test for Feed.add()
        pass

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
