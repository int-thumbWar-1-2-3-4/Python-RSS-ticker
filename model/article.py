from datetime import datetime
from controller.utilities import logger

a_logger = logger('model.article')


class Article:
    """
    A single feed entry
    """

    def __init__(self, title: str, link: str, published_date: datetime):
        a_logger.debug('Article.__init__')

        self.title: str = title
        self.link: str = link
        self.published_date: datetime = published_date
