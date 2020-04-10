from typing import List

import feedparser

from model.article import Article
from model.feed import Feed


class Feed_Manager:
    # Holds all of the feeds this instance of Python-RSS-Ticker displays.
    __list_of_feeds = List[Feed]
    __current_feed = None

    def __change_feed(self) -> Feed:
        # TODO: Fill in Model.__change_feed()
        # Advances the feed to the next in rotation
        pass

    def add(self, new_article: Article, feed_name: str) -> bool:
        # Create a new Feed object if one doesnt already exist. Add the article.py to it.
        # Return true if successful
        # TODO: Fill in Model.add(article)
        return False

    def get_next_article(self) -> Article:
        # TODO: Fill in Model.get_next_article()
        # Gets the next article to be displayed
        pass

    def is_empty(self) -> bool:
        # Determines whether the model has any feeds.
        return len(self.__list_of_feeds) == 0

    def remove(self, feedName: str) -> bool:
        # Remove the feed and make sure its contents are no longer displayed.
        # Return true if successful
        # TODO: Fill in Model.remove()
        return False

    def size(self) -> int:
        # Gets the number of feeds currently held
        # TODO: Fill in Model.size()
        return -1

    def update(self, article_list: List[Article], feed_name: str) -> bool:
        # Create a new Feed object if one doesnt already exist. Add the article.py to it.
        # Return true if successful
        # TODO: Fill in Model.update(article_list, feed_name)
        return False


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
