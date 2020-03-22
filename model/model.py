import feedparser

from view.main_view import MainView


class Model():
    # This class loads the feed entries and stores them in a dictionary of title, link pairs.

    # The entries currently loaded  from the feed
    __feed_titles = []
    __feed_entries = {}
    __displayed_entry_title = "[BLANK Entry Title]"

    def __init__(self, main_view: MainView):
        self.__main_view = main_view

    def load_entries(self, feed_link: str):
        # Loads all of the entries from the feed at the specified location.

        feed = feedparser.parse(feed_link)
        for entry in feed.entries:
            self.__feed_titles.append(entry.title)
            self.__feed_entries[entry.title] = entry.link

        if not self.is_empty():
            first_title = self.__feed_titles[0]
            self.__main_view.display_entry(first_title, self.__feed_entries.get(first_title))

    def switch_displayed_entry(self):
        # Finds the next entry's title and link and prompts the view to display it.

        # Output an error message if the dictionary is empty and skip the rest of the method.
        if self.is_empty():
            print("ERROR The dictionary of feed entries is empty!")
            self.__main_view.display_entry("BLANK Title", "BLANK Link")
            return

        # Search the dictionary of feed entries for the one that is currently displayed.
        for index, entry in enumerate(self.__feed_entries, start=0):

            # If this entry is the last one in the dictionary, display the first title, link pair.
            if (index + 1) == len(self.__feed_entries):
                first_title = self.__feed_titles[0]
                self.__main_view.display_entry(first_title, self.__feed_entries.get(first_title))

            # The entry is not at the end, so see if this title matches the one being displayed.
            #   Display the next title, link pair in the dictionary.
            elif entry.title == self.__displayed_entry_title:
                next_title = self.__feed_titles[index + 1]
                self.__displayed_entry_title = next_title
                self.__main_view.display_entry(next_title, self.__feed_entries.get(next_title))

    def is_empty(self):
        # Determines whether the dictionary of entries is empty

        if len(self.__feed_titles) == 0:
            return True
        else:
            return False
