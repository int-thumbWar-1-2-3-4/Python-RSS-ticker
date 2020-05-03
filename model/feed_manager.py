"""
model.feed_manager

Holds all of the feeds this instance of Python-RSS-Ticker displays. Manages ordering of Articles so they rotate
between feeds and repeat Articles as little as possible.
"""

from typing import List
from model import parser
from model.feed import Feed
from model.article import Article
from controller.utilities import logger

fm_logger = logger('model.feed_manager')


class FeedManagerEmptyException(Exception):
    """
    model.feed_manager.FeedManagerEmptyException

    Exception when the FeedManager is empty.
    """
    pass


class FeedNotFoundException(Exception):
    """
    model.feed_manager.FeedNotFoundException

    Exception for when the feed requested does not exist.
    """
    pass


class FeedManager:
    """
    model.feed_manager.FeedManager

    Holds all the feeds which will be rendered in the GUI view. It manages feed creation and updating.
    Also it alternates articles between the feeds if there are more than 1 feed to choose from. That way articles from
    the same feed are not shown bak-to-back.
    """

    def __init__(self):
        """model.feed_manager.FeedManager.__init__"""

        fm_logger.debug('FeedManager.__init__')

        self.__list_of_feeds: List[Feed] = list()
        self.__current_feed_index: int = -1

    def add(self, new_article: Article, feed_name: str) -> bool:
        """
        model.feed_manager.FeedManager.add

        Add a new article to a feed ONLY if the feed already exists and the feed does not already have the article.
        Returns False if the no feed could be found corresponding to the article given.
        Also returns False if the article already exists.

        Arguments:
            new_article -- the new Article to add
            feed_name -- the name of the feed which corresponds to the given article
        """

        fm_logger.debug('FeedManager.add')

        if self.is_empty() or self.contains(new_article, feed_name):
            return False

        try:
            feed: Feed = self.__get_feed(feed_name)
            feed.add_new(new_article)
            return True

        except FeedNotFoundException:
            return False

    def contains(self, article: Article, feed_name: str) -> bool:
        """
        model.feed_manager.FeedManager.contains

        Determines whether an article exists in the feed indicated.

        Returns True if a match was found.

        Arguments:
            new_article -- the new Article to add
            feed_name -- the name of the feed which corresponds to the given article
        """

        fm_logger.debug('FeedManager.contains')

        if self.is_empty():
            return False

        for feed in self.__list_of_feeds:
            if feed.name == feed_name:
                return feed.contains(article)

        # No feed matched the name given
        return False

    def get_current_article(self) -> Article:
        """
        model.feed_manager.FeedManager.get_current_article

        Attempts to get the current article that is displayed.

        Raises an exception if the FeedManager is empty.

        Returns the next article which is displayed.
        """

        fm_logger.debug('FeedManager.get_current_article')

        if self.__current_feed_index == -1:
            raise FeedManagerEmptyException("This FeedManager is empty. Current article does not exist.")

        current_feed: Feed = self.__list_of_feeds[self.__current_feed_index]
        return current_feed.get_current_article()

    def get_next_article(self) -> Article:
        """
        model.feed_manager.FeedManager.get_next_article

        Attempts to get the next article that to display

        Raises an exception if the FeedManager is empty.

        Returns the next article to display. May return the currently displayed article if only one feed exists
        and that feed only contains one article.
        """

        fm_logger.debug('FeedManager.get_next_article')

        if self.is_empty():
            raise FeedManagerEmptyException("This FeedManager is empty. Could not get next article.")

        else:
            # current feed is at last entry of list, wrap to beginning
            if self.__current_feed_index == (self.size() - 1):
                self.__current_feed_index = 0
            else:
                self.__current_feed_index += 1

            current_feed: Feed = self.__list_of_feeds[self.__current_feed_index]
            return current_feed.get_next_article()

    def is_empty(self) -> bool:
        """
        model.feed_manager.FeedManager.is_empty

        Determines whether the model contains any feeds.

        Returns True if the FeedManager is empty
        """

        fm_logger.debug('FeedManager.is_empty')

        if self.size() == 0:
            return True

        return False

    def remove(self, feed_name: str) -> bool:
        """
        model.feed_manager.FeedManager.remove

        Removes the indicated feed from the manager and updates the current feed if another exists.

        Returns False if no feed matched the name given.

        Arguments:
            feed_name -- the name of the feed to remove
        """

        fm_logger.debug('FeedManager.remove')

        try:
            matched_feed: Feed = self.__get_feed(feed_name)
        except FeedNotFoundException:
            return False

        # feed_manager will be empty after removal
        if self.size() == 1:
            self.__list_of_feeds.clear()
            self.__current_feed_index = -1
            return True

        # If the feed to be removed is the current feed, advance the current feed if possible before removing
        if self.__list_of_feeds[self.__current_feed_index] == matched_feed:

            # currently at last feed in list, loop to beginning
            if self.__current_feed_index == (len(self.__list_of_feeds) - 1):
                self.__current_feed_index = 0

            # otherwise, move current feed to next in rotation
            else:
                self.__current_feed_index += 1

            self.__list_of_feeds.remove(matched_feed)
            return True

        # If the feed to be removed is NOT the current feed, decrease current_feed_index if necessary before removing.
        else:
            for index in range(0, len(self.__list_of_feeds)):
                if self.__list_of_feeds[index].name == matched_feed.name:
                    if index < self.__current_feed_index:
                        self.__current_feed_index -= 1

            self.__list_of_feeds.remove(matched_feed)
            return True

    def size(self) -> int:
        """
        model.feed_manager.FeedManager.size

        Returns the number of feeds currently held.
        """

        fm_logger.debug('FeedManager.size')

        return len(self.__list_of_feeds)

    def update(self, feed_name: str, feed_link: str, feed_contents: List[Article]):
        """
        model.feed_manager.FeedManager.update

        Creates a new Feed object if one doesnt already exist, or updates an existing feed with the contents given.
        Will not update if feed_contents list is empty.

        Arguments:
            feed_name -- the name of the feed to create or update
            feed_link -- the url location for the feed
            feed_contents -- the Articles which the feed contains.
        """

        fm_logger.debug('FeedManager.update')

        if len(feed_contents) == 0:
            # DO not add the articles if the list of articles given is empty
            return

        try:
            feed = self.__get_feed(feed_name)
            feed.update(feed_contents)

        except:
            if self.is_empty():
                self.__current_feed_index = 0
            self.__list_of_feeds.append(Feed(feed_name, feed_link, feed_contents))

    def __get_feed(self, feed_name: str) -> Feed:
        """
        model.feed_manager.FeedManager.__get_feed

        Returns the feed which matches the given name.

        Raises an exception if a match could not be found.

        Arguments:
            feed_name -- the name of the feed to create or update
        """

        fm_logger.debug('FeedManager.__get_feed')

        for feed in self.__list_of_feeds:
            if feed.name == feed_name:
                return feed

        raise FeedNotFoundException("No feed found with the name: %s" % feed_name)


def create_feed_manager(feed_url: str):
    """
        model.feed_manager.create_feed_manager

        Uses the model.parser module to download the contents of the indicated feed and load it into
        a new instance of FeedManager.

        Returns a newly created FeedManager

        Arguments:
            feed_name -- the url for the feed to load
        """

    fm_logger.debug('model.feed_manager.create_feed_manager')

    feed_name = parser.get_feed_name(feed_url)
    feed_contents = parser.get_feed_contents(feed_url)
    feed_manager = FeedManager()
    feed_manager.update(feed_name, feed_url, feed_contents)

    return feed_manager
