import email
from datetime import datetime

import requests
import validators

from bs4 import BeautifulSoup
from typing import List
from validators import ValidationFailure
from model.article import Article
from controller.utilities import logger
from model.feed import Feed
from email.utils import parsedate_tz

p_logger = logger('model.parser.py')

"""
This module imports and parses rss v2.0 and atom v1.0 files as collections of Articles called Feeds.

rss v2.0 specs can be found here: https://cyber.harvard.edu/rss/rss.html#hrelementsOfLtitemgt
atom v1.0 specs can be found here: https://support.google.com/merchants/answer/160593?hl=en
"""


class InvalidAtomException(Exception):
    """Exception raised if an Atom feed is not correctly formatted"""
    pass


class InvalidRssException(Exception):
    """Exception raised if an Rss feed is not correctly formatted"""
    pass


class InvalidUrlException(Exception):
    """Exception raised if url is not formatted correctly."""
    pass


def get_multi_feed_contents(urls: List[str]) -> List[Feed]:
    """
    Parse one or multiple feeds' contents from the files at the urls provided. Files must be .rss, .html, or .xml
    """

    p_logger.debug('get_multi_feed_contents')

    if len(urls) == 0:
        raise InvalidUrlException("urls[] is empty. Please include a URL.")

    # TODO: Make get_feed_contents(List[str]) return the contents of multiple feeds
    return List[List[Article]]


def get_feed_contents(url: str) -> List[Article]:
    """Uses BeautifulSoup to parse the contents an rss or atom feed file at the url provided."""

    p_logger.debug('get_feed_contents')

    try:
        _check_url(url)
    except InvalidUrlException:
        raise  # This passes the exception to whatever called this method. The rest of this method will not run.

    response = requests.get(url)
    bs_feed = BeautifulSoup(response.content, "lxml-xml")

    if bs_feed.rss is not None:
        # If the top element in the xml is an rss element, parse the file as an rss feed
        return _parse_rss(bs_feed)

    if bs_feed.feed is not None:
        # return _parse_atom(bs_feed)
        pass


def get_feed_name(url: str) -> str:
    """Uses BeautifulSoup to retrieve the name of an rss or atom feed file at the url provided."""

    # TODO: Find some way to combine get_feed_name with _parse_rss so BeautifulSoup doesnt have to be created twice

    p_logger.debug('get_feed_name')

    try:
        _check_url(url)
    except InvalidUrlException:
        raise  # This passes the exception to whatever called this method. The rest of this method will not run.

    response = requests.get(url)
    bs_feed = BeautifulSoup(response.content, "lxml-xml")

    if bs_feed.rss is not None:
        # If the top element in the xml is an rss element, parse the file as an rss feed
        return bs_feed.rss.title

    if bs_feed.feed is not None:
        # return feed title
        pass


def _parse_rss(bs_feed: BeautifulSoup) -> List[Article]:
    """Parses the data within BeautifulSoup into a single Feed object with 1 or more Articles"""

    p_logger.debug('_parse_rss')

    # Get the relevant meta about the feed itself (name & link)

    if bs_feed.rss.channel is None:
        raise InvalidRssException("By RSS V2.0 specifications the rss element must have a single, subordinate"
                                  + "<channel> element which contains metadata on the feed.")

    if bs_feed.rss.channel.title is None:
        raise InvalidRssException("By RSS V2.0 specifications the channel element must have a single, subordinate"
                                  + "<title> element which is the name of the feed itself.")

    feed_name = bs_feed.channel.title

    if bs_feed.rss.channel.link is None:
        raise InvalidRssException("By RSS V2.0 specifications the channel element must have a single, subordinate"
                                  + "<link> element which is the URL to the HTML website corresponding to the channel.")

    feed_link = bs_feed.channel.link

    # Get the items within the feed and parse them as Articles

    feed_contents = []
    items = bs_feed.find_all("item")

    if len(items) == 0:
        raise InvalidRssException("This rss feed either has no items (entries")

    for item in items:
        title = item.title.string
        link = item.link.string
        date = item.pubDate.string

        # Make sure the required data was parsed in order to create an Article
        if title is None or link is None or date is None:
            print("The Article contains blank information and cannot be parsed:"
                  "/n/t" + "title == %s" % title +
                  "/n/t" + "link == %s" % link +
                  "/n/t" + "date == %s" % str(date))
            p_logger.info("The Article contains blank information and cannot be parsed:"
                          "/n/t" + "title == %s" % title +
                          "/n/t" + "link == %s" % link +
                          "/n/t" + "date == %s" % str(date))
            continue

        # Convert the date from rfc822 (rss std format) to datetime
        # The one line of code comes from:
        # https://stackoverflow.com/questions/1568856/how-do-i-convert-rfc822-to-a-python-datetime-object
        date = datetime.utcfromtimestamp(email.utils.mktime_tz(email.utils.parsedate_tz(date)))

        feed_contents.append(Article(title, link, date))

    if len(feed_contents) == 0:
        raise InvalidRssException("The feed was found to be blank. Could not parse the feed.")

    return feed_contents


def _parse_atom(bs_feed: BeautifulSoup) -> List[Article]:
    p_logger.debug('_parse_atom')

#   TODO: Fill out the parser._parse_atom method


def _check_url(url: str):
    """
    Raises an exception if a url string is formatted incorrectly. It is not intended to be comprehensive.
    It filters some common issues that might prevent parsing, while explaining to the user what the issue might be.
    """

    p_logger.debug('_check_url')

    if len(url) == 0:
        raise InvalidUrlException("This url is blank. Please indicate a valid url.")

    if url.endswith("rss") or url.endswith("atom") or url.endswith("xml"):
        # The url has a valid suffix, skip to validators.url(url)
        pass
    else:
        # The url did not match any of the 3 valid suffixes. Therefore it is invalid.
        raise InvalidUrlException("The url: [%s] does not end in \"rss\", \"atom\", or \"xml"
                                  "Please indicate a valid feed url." % url)