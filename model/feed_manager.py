from typing import List

import feedparser

from model.article import Article
from model.feed import Feed


class Feed_Manager:
    # Holds all of the feeds this instance of Python-RSS-Ticker displays. Manages ordering of Articles so they rotate
    #       between feeds and repeat as little as possible.
    __list_of_feeds = List[Feed]
    __current_feed_index = -1

    def __change_feed(self) -> bool:
        # Advances the feed to the next in rotation
        if self.size() == 0:
            self.__current_feed_index = -1
            return False

        if self.size() == 1:
            self.__current_feed_index = 0
            return False

        if self.__current_feed_index == (self.size() - 1):
            self.__current_feed_index = 0
            return True

        self.__current_feed_index += 1
        return True

    def __get_feed(self, feed_name: str) -> Feed:
        # Gets the feed which matches the given name. May return None if match could not be found.

        for feed in self.__list_of_feeds:
            if feed.name == feed_name:
                return feed

        return None

    def add(self, new_article: Article, feed_name: str) -> bool:
        # Create a new Feed object if one doesnt already exist. Add the article.py to it.
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

        matched_feed: Feed = None

        for list_feed in self.__list_of_feeds:
            if list_feed.name == feed_name:
                return matched_feed.contains(article)

        # No feed matched the name given
        return False

    def get_next_article(self) -> Article:
        # Gets the next article to be displayed. May return None if article could not be found.
        if self.size() == 0:
            return None

        if self.size() == 1:
            current_feed: Feed = self.__list_of_feeds[0]
            return current_feed.get_next()

        pass

    def is_empty(self) -> bool:
        # Determines whether the model has any feeds.
        return self.__list_of_feeds is None or len(self.__list_of_feeds) == 0

    def remove(self, feedName: str) -> bool:
        # Removes the feed from the manager and updates the current feed if another exists.
        # Return false if no feed matched the name given.

        matched_feed: Feed = self.__get_feed(feedName)

        if matched_feed is None:
            return False

        # If the feed to be removed is the current feed, advance the current feed if possible
        if self.__list_of_feeds[self.__current_feed_index] == matched_feed:

            # feed_manager is now empty
            if self.size() == 1:
                self.__list_of_feeds = List[Feed]
                self.__current_feed_index = -1

    def size(self) -> int:
        # Gets the number of feeds currently held
        return len(self.__list_of_feeds)

    def update(self, article_list: List[Article], feed_name: str):
        # Create a new Feed object if one doesnt already exist. Update its contents with the article list given.

        matched_feed: Feed = self.__get_feed(feed_name)

        if matched_feed is None:
            matched_feed = Feed(feed_name)

        matched_feed.update(article_list)


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
