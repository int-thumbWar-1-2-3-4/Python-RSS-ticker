# Code copied from: 4/10/2020
# https://github.com/Jhawk1196/CS3250PythonProject/blob/dev/src/parser.py
from typing import List

from bs4 import BeautifulSoup
import requests
import re

from model.article import Article


class InvalidUrlException(Exception):
    """
    Exception raised if url is not formatted correctly.
    """
    pass


def get_multi_feed_contents(urls: List[str]) -> List[List[Article]]:
    """
    Parse one or multiple feeds' contents from the files at the urls provided. Files must be .rss, .html, or .xml
    """

    if len(urls) == 0:
        raise InvalidUrlException("urls[] is empty. Please include a URL.")

    # TODO: Make get_feed_contents(List[str]) return the contents of multiple feeds
    return List[List[Article]]


def get_feed_contents(url: str) -> List[Article]:
    """
    Uses BeautifulSoup to access a feed file at the url provided.
    """

    if not __check_url(url):
        raise InvalidUrlException("Invalid URL. Must Be a RSS Feed URL ending in .rss, .html, or .xml")

    feed_contents = []
    response = requests.get(url)
    parse_type = __parser_type(response)
    soup = BeautifulSoup(response.content, parse_type)
    # print(soup.prettify())

    if soup.rss is not None:
        tag = soup.rss
        tag = tag.channel
        for title in tag.find_all(re.compile("title")):
            for entry in title.find_all(string=True):
                feed_contents.append(entry)

    elif soup.find_all(re.compile("atom")) is not None:
        tag = soup.feed
        for entry in tag.find_all("entry"):
            for title in entry.find_all("title"):
                for string in title.find_all(string=True):
                    feed_contents.append(string)

    # TODO: Make get_feed_contents() return List[Article]
    feed_contents = __remove_duplicates(feed_contents)
    return feed_contents


def __check_url(url: str) -> bool:
    """
    Verify if a url string is formatted correctly for the parser.
    """

    url = str(url)
    if len(url) == 0:
        return False
    test_string = (url[-3] + url[-2] + url[-1])
    second_test_string = ""
    if len(url) > 11:
        second_test_string = (url[7] + url[8] + url[9] + url[10] + url[11])
    if test_string == "rss":
        return True
    elif test_string == "xml":
        return True
    elif test_string == "tml":
        return True
    elif second_test_string == "feeds":
        return True
    else:
        return False


def __parser_type(response):
    """
    Finds the type of parser language to use.
    """

    test_url = response.url
    test_string = (test_url[-3] + test_url[-2] + test_url[-1])
    if test_string == "tml":
        return "lxml"
    else:
        return "lxml-xml"


def __remove_duplicates(tags: List[str]) -> List[str]:
    """
    Deletes duplicate articles when they appear back-to-back.
    """

    # TODO: Make this so duplicate articles are removed regardless of where they appear.

    end_feed = []
    for i in range(len(tags)):
        if i == 0:
            end_feed.append(tags[i])
        elif tags[i] == tags[i - 1]:
            continue
        else:
            end_feed.append(tags[i])
    return end_feed
