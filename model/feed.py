import feedparser
from typing import List
from model.article import Article
from controller.utilities import logger


f_logger = logger('model.feed')


class Feed:
    # A collection of articles from a single feed.

    def __init__(self, name: str, list_of_articles: List[Article]):
        # Will not create with empty list

        f_logger.debug('Feed.__init__')

        if len(list_of_articles) == 0:
            # TODO: Make this create an exception if the list is empty
            pass

        self.name: str = name

        self.__list_of_articles: List[Article] = list_of_articles

        self.__sort()
        self.__current_article_index: int = 0

    def __sort(self):
        # Sorts all of the articles on this feed from newest to oldest. Uses the insertion sort process.

        #   Refactored from code at:
        #   https://runestone.academy/runestone/books/published/pythonds/SortSearch/TheInsertionSort.html

        f_logger.debug('Feed.__sort')

        for index in range(1, len(self.__list_of_articles)):
            current_article = self.__list_of_articles[index]
            position = index

            while position > 0 \
                    and self.__list_of_articles[position - 1].published_date < current_article.published_date:
                self.__list_of_articles[position] = self.__list_of_articles[position - 1]
                position -= 1

            self.__list_of_articles[position] = current_article

    def add_new(self, new_article: Article) -> bool:
        # Adds a new article.py to the feed and sorts the feed after. Will not add a duplicate.
        #        Current article.py will set to the new one.
        #        Returns True is added, False otherwise.

        f_logger.debug('Feed.add_new')

        if self.contains(new_article):
            return False

        self.__list_of_articles.append(new_article)
        self.__sort()
        return True

    def contains(self, article: Article) -> bool:
        # Determines whether the given article's title matches one already in the feed.

        f_logger.debug('Feed.contains')

        for list_article in self.__list_of_articles:
            if list_article.title == article.title:
                return True

        return False

    def get_current_article(self) -> Article:
        # Gets the current article for this feed.

        f_logger.debug('Feed.get_current_article')

        return self.__list_of_articles[self.__current_article_index]

    def get_next_article(self) -> Article:
        # Gets the next article in this feed's order after the current one.
        #           Wraps from end back to start.
        #           Returns None if empty. Returns the current article if there is only 1 article.

        f_logger.debug('Feed.get_next_article')

        if len(self.__list_of_articles) == 1:
            return self.get_current_article()

        # The current article is at the end.
        if self.__current_article_index == (len(self.__list_of_articles) - 1):
            self.__current_article_index = 0
            return self.get_current_article()

        self.__current_article_index += 1
        return self.get_current_article()

    def update(self, new_list_of_articles: List[Article]):
        # Updates the articles contained in this feed to the new one. Will not update if new list is empty

        f_logger.debug('Feed.update')

        if len(new_list_of_articles) == 0:
            return

        saved_current_article = self.get_current_article()

        self.__list_of_articles = new_list_of_articles
        self.__sort()

        if self.contains(saved_current_article):
            for index in range(0, len(self.__list_of_articles)):
                if self.__list_of_articles[index].title == saved_current_article.title:
                    self.__current_article_index = index
                    break

        else:
            # Default to newest if the current article is no longer in the list.
            self.__current_article_index = 0


def parse(feed_link: str) -> []:
    # Get the contents of an atom or rss feed using the feedparser library. Return all the relevant
    #   information as Articles (unsorted).

    f_logger.debug('Feed.parse')

    feed = feedparser.parse(feed_link)
    article_list = []

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        datetime = entry.published_parsed  # time.struct_time object parsed within feedparser from string attribute
        article = Article(title, link, datetime)

        article_list.append(article)

    return article_list