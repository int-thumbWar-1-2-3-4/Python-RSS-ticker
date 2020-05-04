"""
model.parser

This module imports and parses rss v2.0 and atom v1.0 files as collections of Articles called Feeds.

!!! At this moment the parser only has a dummy method for .atom feed parsing and cannot actually parse them !!!

rss v2.0 specs can be found here: https://cyber.harvard.edu/rss/rss.html#hrelementsOfLtitemgt
atom v1.0 specs can be found here: https://support.google.com/merchants/answer/160593?hl=en
"""

from email import utils
import requests
from re import search
from bs4 import BeautifulSoup
from typing import List
from datetime import datetime
from model.article import Article
from controller.utilities import logger

p_logger = logger('model.parser.py')


class InvalidRssException(Exception):
    """
    model.parser.InvalidRssException

    Exception raised if an Rss feed is not correctly formatted.
    """
    pass


class InvalidUrlException(Exception):
    """
    model.parser.InvalidUrlException

    Exception raised if an improperly formatted url is given
    """
    pass


def get_feed_contents(url: str) -> List[Article]:
    """
    model.parser.get_feed_contents

    Uses BeautifulSoup to parse the contents an rss or atom feed file at the url provided.

    Raises an exception if the url is not properly formatted.
    Also raises an exception if an atom feed is indicated, as that file format is not currently supported.

    Returns a new list of articles.

    Arguments:
        url -- the url location of the feed to parse
    """

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


def get_feed_name(url: str) -> str:
    """
    model.parser.get_feed_name

    Uses BeautifulSoup to retrieve the name of an rss or atom feed file at the url provided.

    Raises an exception if the url is not properly formatted.
    Also raises an exception if an atom feed is indicated, as that file format is not currently supported.

    Returns the name of the feed.

    Arguments:
        url -- the url location of the feed to parse
    """
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


def _parse_rss(bs_feed: BeautifulSoup) -> List[Article]:
    """
    model.parser._parse_rss

    Parses the data within BeautifulSoup into a list of Articles.

    Raises exceptions if the rss file is not properly formatted to be parsed. Could also raise an exception if the rss
    feed has no entries.

    Returns the contents of the feed.

    Arguments:
        bs_feed -- the BeautifulSoup object which contains data on this feed.
    """

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
        raise InvalidRssException("This rss feed has no entries.")

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
        date = datetime.utcfromtimestamp(utils.mktime_tz(utils.parsedate_tz(date)))

        feed_contents.append(Article(title, link, date))

    if len(feed_contents) == 0:
        raise InvalidRssException("The feed was found to be blank. Could not parse the feed.")

    return feed_contents


def _check_url(url: str):
    """
    model.parser._check_url

    Raises an exception if a given url is not formatted correctly.
    It is not intended to be comprehensive. Rather, it filters some common issues that might prevent parsing, while
    explaining to the user what the issue might be.

    Arguments:
        url -- the url to validate
    """

    p_logger.debug('_check_url')

    if len(url) == 0:
        raise InvalidUrlException("This url is blank. Please indicate a valid url.")

    if search('^.*a?[rtx][som][sml]/?$', url):
        # The url has a valid suffix, skip to validators.url(url)
        pass
    else:
        # The url did not match any of the 3 valid suffixes. Therefore it is invalid.
        raise InvalidUrlException("The url: [%s] does not end in \"rss\" or \"xml"
                                  "Please indicate a valid feed url." % url)

