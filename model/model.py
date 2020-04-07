import feedparser

from typing import List


class Article:
    # TODO: Split Article class into its own file
    # A single rss item, i.e. a single news article

    def __init__(self, title: str, link: str, datetime):
        self.title = title
        self.link = link
        self.datetime = datetime    # time.struct_time object


class Feed:
    # TODO: Split Feed class into its own file
    # A collection of articles from a single feed.

    __list_of_articles: List[Article] = list()

    current_article = None

    def __init__(self, name: str):
        self.name = name

    def __contains(self, article: Article) -> bool:
        # Determines whether the given article's title matches one already in the feed.

        if self.is_empty():
            return False

        for list_article in self.__list_of_articles:
            if list_article.title == article.title:
                return True

        return False

    def __index_of(self, article: Article) -> int:
        # Determines the index of the given article. Returns -1 if no title match found.

        for index in range(1, len(self.__list_of_articles)):
            if self.__list_of_articles[index].title == article.title:
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

    def add_new(self, new_article: Article) -> bool:
        # Adds a new article to the feed and sorts the feed after. Will not add a duplicate.
        #        Current article will set to the new one.
        #        Returns True is added, False otherwise.

        if self.__contains(new_article):
            return False

        self.__list_of_articles.append(new_article)
        self.__sort()
        self.current_article = new_article
        return True

    def is_empty(self) -> bool:
        return len(self.__list_of_articles) == 0

    def is_sorted(self):
        # Determines whether the articles are sorted by age or not. Returns false if there are no articles in this feed.

        if self.is_empty():
            return False

        previous_article = None
        for article in self.__list_of_articles:

            if previous_article is not None and previous_article.datetime < article.datetime:
                return False
            previous_article = article

        return True

    def move_to_next(self) -> bool:
        # Changes the current article to the next one.
        #           Wraps from end back to start.
        #           Returns false if empty or only contains one article. True if current article is changed.

        if self.is_empty() or len(self.__list_of_articles) == 1:
            return False

        if len(self.__list_of_articles) == self.__index_of(self.current_article): # The current article is at the end.
            self.current_article = self.__list_of_articles[0]
        else:
            self.current_article = self.__list_of_articles[self.__index_of(self.current_article) + 1]

        return True

    def update(self, new_list_of_articles: List[Article]):
        # Updates the articles contained in this feed to the new one. Will not update if new list is empty

        if len(new_list_of_articles) == 0:
            return

        current_article = self.current_article

        self.__list_of_articles = new_list_of_articles
        self.__sort()

        if current_article is not None and self.__contains(current_article):
            self.current_article = current_article
        else:
            self.current_article = self.__list_of_articles[0] # Default to newest if the current article is no longer in the list.


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
