from typing import List

import feedparser

from model.article import Article
from model.feed import Feed


class Feed_Manager:
    # Holds all of the feeds this instance of Python-RSS-Ticker displays. Manages ordering of Articles so they rotate
    #       between feeds and repeat as little as possible.

    def __init__(self):
        self.__list_of_feeds: List[Feed] = list()
        self.__current_feed_index: int = -1

    def __get_feed(self, feed_name: str) -> Feed:
        # Gets the feed which matches the given name. May return None if match could not be found.

        for feed in self.__list_of_feeds:
            if feed.name == feed_name:
                return feed

        return None

    def add(self, new_article: Article, feed_name: str) -> bool:
        # Add a new article to a feed ONLY if the feed already exists and the feed does not already have the article.
        # Return true if successful

        if self.is_empty() or self.contains(new_article, feed_name):
            return False

        feed: Feed = self.__get_feed(feed_name)

        if feed is None:
            return False

        feed.add_new(new_article)
        return True

    def contains(self, article: Article, feed_name: str) -> bool:
        # Determines whether a feed with the given name and article exist

        if self.is_empty():
            return False

        for feed in self.__list_of_feeds:
            if feed.name == feed_name:
                return feed.contains(article)

        # No feed matched the name given
        return False

    def get_current_article(self) -> Article:
        # Gets the next article to be displayed. May return None if article could not be found.
        if self.is_empty():
            raise Exception("This FeedManager is empty. Current article does not exist.")

        current_feed: Feed = self.__list_of_feeds[self.__current_feed_index]
        return current_feed.get_current_article()

    def get_next_article(self) -> Article:
        # Gets the next article to be displayed. May return None if article could not be found.

        if self.is_empty():
            raise Exception("This FeedManager is empty. Could not get next article.")

        else:
            # current feed is at last entry of list, wrap to beginning
            if self.__current_feed_index == (self.size() - 1):
                    self.__current_feed_index = 0
            else:
                self.__current_feed_index += 1

            current_feed: Feed = self.__list_of_feeds[self.__current_feed_index]
            return current_feed.get_next_article()

    def is_empty(self) -> bool:
        # Determines whether the model has any feeds.

        if self.size() == 0:
            return True

        return False

    def remove(self, feedName: str) -> bool:
        # Removes the feed from the manager and updates the current feed if another exists.
        # Returns false if no feed matched the name given.

        matched_feed: Feed = self.__get_feed(feedName)

        if matched_feed is None:
            return False

        # If the feed to be removed is the current feed, advance the current feed if possible
        if self.__list_of_feeds[self.__current_feed_index] == matched_feed:

            # feed_manager will be empty after removal
            if self.size() == 1:
                self.__list_of_feeds.clear()
                self.__current_feed_index = -1

            # currently at last feed in list, loop to beginning
            elif self.__current_feed_index == (len(self.__list_of_feeds) - 1):
                self.__current_feed_index = 0

            # otherwise, move current feed to next in rotation
            else:
                self.__current_feed_index += 1

            return True

    def size(self) -> int:
        # Gets the number of feeds currently held

        return len(self.__list_of_feeds)

    def update(self, article_list: List[Article], feed_name: str):
        # Creates a new Feed object if one doesnt already exist, or updates an existing feed wit the list given
        #       Will not update if article list is empty.

        if len(article_list) == 0:
            return

        if self.is_empty():
            self.__current_feed_index = 0

        feed: Feed = self.__get_feed(feed_name)

        if feed is None:
            feed = Feed(feed_name, article_list)
            self.__list_of_feeds.append(feed)

        else:
            feed.update(article_list)


def parse(feed_link: str) -> []:
    # Get the contents of an atom or rss feed using the feedparser library. Return all the relevant
    #   information as Articles (unsorted).

    feed = feedparser.parse(feed_link)
    article_list = []

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        datetime = entry.published_parsed     # time.struct_time object parsed within feedparser from string attribute
        article = Article(title, link, datetime)

        article_list.append(article)

    return article_list
