import feedparser

from view.main_view import MainView
from typing import List


class Article:

    def __init__(self, title: str, link: str, date: str):
        self.title = title
        self.link = link
        self.date = date


class Feed:

    def __init__(self, name: str):
        self.__list_of_articles = List[Article]
        self.__position = -1    # -1 here means the list of articles is empty

        self.name = name

    def sort(self):
        # TODO: Fill in Feed.sort() method
        pass

    def update(self, new_list_of_articles: List[Article]):
        # TODO: Fill in Feed.update() method
        pass

    def get_next(self) -> Article:
        # TODO: Fill in Feed.get_next() method
        pass

    def add(self, new_article: Article):
        # TODO: Fill in Feed.add() method
        pass


class Model:

    def __init__(self):
        self.__list_of_feeds = List[Feed]
        self.__current_feed: Feed = None

    def add(self, new_list_of_articles: List[Article]) -> bool:
        # TODO: Fill in Model.add(list) method
        return False

    def add(self, new_article: Article) -> bool:
        # TODO: Fill in Model.add(article) method
        return False

    def remove(self, feedName: str) -> bool:
        # TODO: Fill in Model.remove() method
        return False

    # This class stores articles from rss or atom feeds and orders them from newest to oldest. When multiple feeds are
    # #   loaded, they will alternate between each feed with each feed ordered internally from newest to oldest
    #
    # # The articles currently loaded  from the feed
    # __collection_of_articles = OrderedDict()
    # __index_of_current_article = -1     # -1 indicates that the collection is empty
    #
    # def __init__(self, main_view: MainView):
    #     self.__main_view = main_view
    #
    # def load_entries(self, feed_link: str):
    #     # Loads all of the entries from the feed at the specified location.
    #
    #     feed = feedparser.parse(feed_link)
    #     for entry in feed.entries:
    #         self.__collection_of_articles[entry.title] = entry.link
    #
    #     if not self.is_empty():
    #         first_title = self.__feed_titles[0]
    #         self.__main_view.display_entry(first_title, self.__collection_of_articles.get(first_title))
    #
    # def switch_displayed_entry(self):
    #     # Finds the next entry's title and link and prompts the view to display it.
    #     print('switched_displayed_entry')
    #     # Output an error message if the dictionary is empty and skip the rest of the method.
    #     if self.is_empty():
    #         print("ERROR The dictionary of feed entries is empty!")
    #         self.__main_view.display_entry("BLANK Title", "BLANK Link")
    #         return
    #
    #     # Search the dictionary of feed entries for the one that is currently displayed.
    #     for index, entry in enumerate(self.__collection_of_articles, start=0):
    #
    #         # If this entry is the last one in the dictionary, display the first title, link pair.
    #         if (index + 1) == len(self.__collection_of_articles):
    #             first_title = self.__feed_titles[0]
    #             self.__main_view.display_entry(first_title, self.__collection_of_articles.get(first_title))
    #
    #         # The entry is not at the end, so see if this title matches the one being displayed.
    #         #   Display the next title, link pair in the dictionary.
    #         elif entry.title == self.__displayed_article_title:
    #             next_title = self.__feed_titles[index + 1]
    #             self.__displayed_article_title = next_title
    #             self.__main_view.display_entry(next_title, self.__collection_of_articles.get(next_title))
    #
    # def is_empty(self):
    #     # Determines whether the dictionary of entries is empty
    #
    #     if len(self.__collection_of_articles) == 0:
    #         return True
    #     else:
    #         return False
