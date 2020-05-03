"""
model.feed

Holds the contents of a single feed in order from newest to oldest.
"""

from typing import List
from model.article import Article
from controller.utilities import logger

f_logger = logger('model.feed')


class EmptyFeedException(Exception):
    """
    model.feed.EmptyFeedException

    Exception if the feed is empty and cannot be created.
    """
    pass


class Feed:
    """
    model.feed.Feed

    A collection of entries (Articles) from a single feed. It automatically sorts its articles by date published.
    It also keeps track of which article to display next.

    This class should ONLY be automatically created by the feed_manager. This prevents unnecessary creation
    of duplicate objects which hold large amounts of data.
    """

    def __init__(self, name: str, url: str, feed_contents: List[Article]):
        """
        model.feed.Feed.__init__

        Raises an exception if the feed_contents are empty.

        Arguments:
            name -- the title for the feed
            url -- the url where the feed is located.
            feed_contents -- the date and time in which the article was published.
        """

        f_logger.debug('Feed.__init__')

        if len(feed_contents) == 0:
            raise EmptyFeedException("The list_of_articles given is empty. " +
                                     "The feed: \"%s\" could not be created." % name)

        self.url: str = url
        self.name: str = name
        self.__list_of_articles: List[Article] = feed_contents
        self.__current_article_index: int = 0

        self.__sort()

    def add_new(self, new_article: Article) -> bool:
        """
        model.feed.Feed.add_new

        Adds a new Article to the feed and sorts the feed after. Will not add a duplicate.
        Returns False if the article already exists.

        Arguments:
            new_article -- the new article to be added
        """

        f_logger.debug('Feed.add_new')

        if self.contains(new_article):
            return False

        self.__list_of_articles.append(new_article)
        self.__sort()
        return True

    def contains(self, article: Article) -> bool:
        """
        model.feed.Feed.contains

        Determines whether the given article matches one already in the feed.

        Returns True if a matching article was found.

        Arguments:
            article -- the new article to search for within this feed.
        """

        f_logger.debug('Feed.contains')

        for list_article in self.__list_of_articles:
            if list_article.title == article.title:
                return True

        return False

    def get_current_article(self) -> Article:
        """
        model.feed.Feed.get_current_article

        Gets the current article for this feed.

        Returns the current article
        """

        f_logger.debug('Feed.get_current_article')

        return self.__list_of_articles[self.__current_article_index]

    def get_next_article(self) -> Article:
        """
        model.feed.Feed.get_next_article

        Gets the next article in this feed's order after the current one. Wraps from the end back to start.

        Returns None if empty. Returns the current article if there is only 1 article.
        """

        f_logger.debug('Feed.get_next_article')

        if len(self.__list_of_articles) == 1:
            return self.get_current_article()

        # The current article is at the end.
        if self.__current_article_index == (len(self.__list_of_articles) - 1):
            self.__current_article_index = 0
            return self.get_current_article()

        self.__current_article_index += 1
        return self.get_current_article()

    def update(self, new_feed_contents: List[Article]):
        """"
        model.feed.Feed.update

        Updates the articles contained in this feed to the new one. Will not update if new contents is empty.

        Arguments:
            new_feed_contents -- the newly downloaded contents for this feed
        """

        f_logger.debug('Feed.update')

        if len(new_feed_contents) == 0:
            return

        saved_current_article = self.get_current_article()

        self.__list_of_articles = new_feed_contents
        self.__sort()

        if self.contains(saved_current_article):
            for index in range(0, len(self.__list_of_articles)):
                if self.__list_of_articles[index].title == saved_current_article.title:
                    self.__current_article_index = index
                    break

        else:
            # Default to newest if the current article is no longer in the list.
            self.__current_article_index = 0

    def __sort(self):
        """
        model.feed.Feed.__sort

        Sorts all of the articles on this feed from newest to oldest. Uses the insertion sort process.

        Sorting code refactored from examples at:
        https://runestone.academy/runestone/books/published/pythonds/SortSearch/TheInsertionSort.html
        """

        f_logger.debug('Feed.__sort')

        for index in range(1, len(self.__list_of_articles)):
            current_article = self.__list_of_articles[index]
            position = index

            while position > 0 \
                    and self.__list_of_articles[position - 1].published_date < current_article.published_date:
                self.__list_of_articles[position] = self.__list_of_articles[position - 1]
                position -= 1

            self.__list_of_articles[position] = current_article
