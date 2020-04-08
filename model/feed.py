from typing import List

from model.article import Article


class Feed:
    # A collection of articles from a single feed.

    __list_of_articles: List[Article] = list()

    current_article = None

    def __init__(self, name: str):
        self.name = name
        self.__list_of_articles.clear()

    def __contains(self, article: Article) -> bool:
        # Determines whether the given article.py's title matches one already in the feed.

        if self.is_empty() or article is None:
            return False

        for list_article in self.__list_of_articles:
            if list_article.title == article.title:
                return True

        return False

    def __index_of(self, article: Article) -> int:
        # Determines the index of the given article.py. Returns -1 if no title match found.

        for index in range(0, len(self.__list_of_articles)):
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

            while position > 0 and self.__list_of_articles[position-1].published_date < current_article.published_date:
                self.__list_of_articles[position] = self.__list_of_articles[position - 1]
                position -= 1

            self.__list_of_articles[position] = current_article

    def add_new(self, new_article: Article) -> bool:
        # Adds a new article.py to the feed and sorts the feed after. Will not add a duplicate.
        #        Current article.py will set to the new one.
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

            if previous_article is not None and previous_article.published_date < article.published_date:
                return False
            previous_article = article

        return True

    def move_to_next(self) -> bool:
        # Changes the current article.py to the next one.
        #           Wraps from end back to start.
        #           Returns false if empty or only contains one article.py. True if current article.py is changed.

        if self.is_empty() or len(self.__list_of_articles) == 1:
            return False

        if self.__index_of(self.current_article) == (len(self.__list_of_articles) - 1): # The current article.py is at the end.
            self.current_article = self.__list_of_articles[0]
            return True

        else:
            new_index = (self.__index_of(self.current_article) + 1)
            self.current_article = self.__list_of_articles[new_index]
            return True


    def update(self, new_list_of_articles: List[Article]):
        # Updates the articles contained in this feed to the new one. Will not update if new list is empty

        if len(new_list_of_articles) == 0:
            return

        self.__list_of_articles = new_list_of_articles
        self.__sort()

        if self.current_article is None or not self.__contains(self.current_article):
            # Default to newest if the current article.py is no longer in the list.
            self.current_article = self.__list_of_articles[0]
