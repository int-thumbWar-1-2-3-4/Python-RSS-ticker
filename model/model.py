from typing import List

import feedparser

from model.article import Article
from model.feed import Feed


class Model:
    # Holds all of the feeds this instance of Python-RSS-Ticker displays.

    def __init__(self):
        self.__list_of_feeds = List[Feed]

    def add(self, new_list_of_articles: List[Article], feed_name: str) -> bool:
        # Create a new Feed object if one doesnt already exist. Update the list with the new list of articles.
        # Return true if successful
        # TODO: Fill in Model.add(list) method
        return False

    def add(self, new_article: Article, feed_name: str) -> bool:
        # Create a new Feed object if one doesnt already exist. Add the article.py to it.
        # Return true if successful
        # TODO: Fill in Model.add(article.py) method
        return False

    def remove(self, feedName: str) -> bool:
        # Remove the feed and make sure its contents are no longer displayed.
        # Return true if successful
        # TODO: Fill in Model.remove() method
        return False


def parse(feed_link: str) -> []:
    # Get the contents of an atom or rss feed using the feedparser library. Return all the relevant
    #   information as Articles (unsorted).

    feed = feedparser.parse(feed_link)
    article_list = []

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        datetime = entry.updated_parsed     # time.struct_time object parsed within feedparser from string attribute
        article = Article(title, link, datetime)

        article_list.append(article)

    return article_list
