import feedparser
from typing import List


class Article:
    # A single rss item, i.e. a single news article

    def __init__(self, title: str, link: str, datetime: str):
        self.title = title
        self.link = link
        self.datetime = datetime


class Feed:
    # A collection of articles from a single feed.

    def __init__(self, name: str):
        self.__list_of_articles = List[Article]
        self.__position = -1    # -1 here means the list of articles is empty

        self.name = name

    def sort(self):
        # Sort the list of articles by datetime from newest to oldest.
        # TODO: Fill in Feed.sort() method
        pass

    def update(self, new_list_of_articles: List[Article]):
        # Compare the new version of the rss feed, adding in new articles and removing old ones.
        #   Order from newest to oldest by datetime.
        # TODO: Fill in Feed.update() method
        pass

    def get_next(self) -> Article:
        # Return the article at the next position.
        # TODO: Fill in Feed.get_next() method
        pass

    def add(self, new_article: Article):
        # Add the new article at the proper position in the list. Increment position if necessary.
        # TODO: Fill in Feed.add() method
        pass


class Model:
    # Holds all of the feeds this instance of Python-RSS-Ticker displays.

    def __init__(self):
        self.__list_of_feeds = List[Feed]
        self.__current_feed: Feed = None

    def add(self, new_list_of_articles: List[Article], feed_name: str) -> bool:
        # Create a new Feed object if one doesnt already exist. Update the list with the new list of articles.
        # Return true if successful
        # TODO: Fill in Model.add(list) method
        return False

    def add(self, new_article: Article, feed_name: str) -> bool:
        # Create a new Feed object if one doesnt already exist. Add the article to it.
        # Return true if successful
        # TODO: Fill in Model.add(article) method
        return False

    def remove(self, feedName: str) -> bool:
        # Remove the feed and make sure its contents are no longer displayed.
        # Return true if successful
        # TODO: Fill in Model.remove() method
        return False


def parse(feed_link: str) -> List[Article]:
    # Get the contents of an atom or rss feed using the feedparser library. Return all the relevant
    #   information as Articles (unsorted).

    feed = feedparser.parse(feed_link)
    article_list = []

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        datetime = entry.date

        temp_article = Article(title, link, datetime)

        article_list.append(temp_article)

    return article_list
