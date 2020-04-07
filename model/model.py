from calendar import calendar
from datetime import time

import feedparser

from view.main_view import MainView
from typing import List


class Article:
    # A single rss item, i.e. a single news article

    def __init__(self, title: str, link: str, datetime):
        self.title = title
        self.link = link
        self.datetime = datetime    # time.struct_time object


class Feed:
    # A collection of articles from a single feed.

    __list_of_articles: List[Article] = list()

    def __init__(self, name: str):
        self.__position_of_current = None # TODO: Change __position_of_current: int to current_article: Article
        self.name = name

        if len(self.__list_of_articles) == 0:
            self.__position_of_current = -1    # -1 here means that the list is empty, so there is no position
        else:
            self.__position_of_current = 0    # Start the position at the first entry (index == 0)

    def __position_of(self, article: Article) -> int:
        # Returns the index of the article given. -1 if article not found. Compares by title

        for index in range(0, len(self.__list_of_articles)):
            list_article = self.__list_of_articles[index]
            if list_article.title == article.title:
                return index

        return -1

    def __sort(self):
        # Sorts all of the articles on this feed from newest to oldest. Uses the insertion sort process.

        #   Refactored from code at:
        #   https://runestone.academy/runestone/books/published/pythonds/SortSearch/TheInsertionSort.html

        for index in range(1, len(self.__list_of_articles)):
            current_article = self.__list_of_articles[index]
            position = index

            while position > 0 and self.__list_of_articles[position-1].datetime < current_article.datetime:
                self.__list_of_articles[position] = self.__list_of_articles[position - 1]
                position -= 1

            self.__list_of_articles[position] = current_article

    def add(self, new_article: Article):
        # Adds an article to the feed and sorts the feed after
        pass

    def is_empty(self) -> bool:
        return len(self.__list_of_articles) == 0

    def is_sorted(self):
        # Determines whether the articles are sorted by age or not. Returns false if there are no articles in this feed.

        if len(self.__list_of_articles) == 0:
            return False

        previous_article: Article = None
        for article in self.__list_of_articles:
            if previous_article is not None and previous_article.datetime < article.datetime:
                return False
            previous_article = article

        return True

    def get_current(self) -> Article:
        # Retreives the current article in this feed. May return None if the feed is empty.

        if len(self.__list_of_articles) == -1:
            return None
        else:
            if self.__position_of_current >= len(self.__list_of_articles): # Make sure the position is not too large
                self.__position_of_current = 0

            return self.__list_of_articles[self.__position_of_current]

    def get_next(self) -> Article:
        # Retreives the next article in order by age. May return None if the feed is empty.
        #           Returns the current if the feed has only one article. Loops around end to start.

        if len(self.__list_of_articles) == -1:
            return None

        else:
            if self.__position_of_current >= len(self.__list_of_articles): # Make sure the position is not too large
                self.__position_of_current = 0

        if len(self.__list_of_articles) == 1:
            return self.get_current()
        elif len(self.__list_of_articles) == self.__position_of_current:
            self.__position_of_current = 0
            return self.get_current()
        else:
            self.__position_of_current += 1
            return self.__list_of_articles[self.__position_of_current]

    def update(self, new_list_of_articles: List[Article]):
        # Updates the articles contained in this feed to the new one. Will not update if new list is empty.

        if len(new_list_of_articles) == 0:
            return

        current_article = self.get_current()

        self.__list_of_articles = new_list_of_articles
        self.__sort()

        self.__position_of_current = self.__position_of(current_article)
        if self.__position_of_current == -1: # Default to newest if the current article is no longer in the list.
            self.__position_of_current = 0



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
