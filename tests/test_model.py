import unittest
from model.model import Article, Feed, Model
from unittest.mock import Mock


class ModelTestCase(unittest.TestCase):

    def test_article(self):
        title = "title"
        link = "link"
        date = "date"

        article = Article(title, link, date)

        self.assertEqual(article.title, title)
        self.assertEqual(article.link, link)
        self.assertEqual(article.date, date)

    def test_feed(self):
        feed_name = "test feed"

        feed = Feed(feed_name)

        self.assertEqual(feed.name, feed_name)

    def test_feed_sort(self):
        # TODO: Create test for Feed.sort()
        pass

    def test_feed_update(self):
        # TODO: Create test for Feed.update()
        pass

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


if __name__ == '__main__':
    unittest.main()
