"""
model.article

An object which hold the relevant data for a single feed entry.
"""

from datetime import datetime
from controller.utilities import logger

a_logger = logger('model.article')


class Article:
    """
    model.article.Article

    A single feed entry, i.e. a single news article.
    """

    def __init__(self, title: str, link: str, published_date: datetime):
        """
        Article.__init__

        Arguments:
            title -- the title of the entry. It describes what the article is about.
            link -- the url for the entry itself.
            published_date -- the date and time in which the article was published.
        """

        a_logger.debug('Article.__init__')

        self.title = title
        self.link = link
        self.published_date = published_date
