#https://github.com/Jhawk1196/CS3250PythonProject/blob/dev/src/parser.py
import re
import requests
from bs4 import BeautifulSoup
from controller.utilities import logger


p_logger = logger('model.parser')


def parse_url_feed(url):

    p_logger.debug('parser_url_feed')

    feed = []
    if not check_url(url):
        return "Invalid URL. Must Be a RSS Feed URL ending in .rss, .html, or .xml"
    response = requests.get(url)
    parse_value = find_parser(response)
    soup = BeautifulSoup(response.content, parse_value)
    # print(soup.prettify())
    if soup.rss is not None:
        tag = soup.rss
        tag = tag.channel
        for title in tag.find_all(re.compile("title")):
            for entry in title.find_all(string=True):
                feed.append(entry)
    elif soup.find_all(re.compile("atom")) is not None:
        tag = soup.feed
        for entry in tag.find_all("entry"):
            for title in entry.find_all("title"):
                for string in title.find_all(string=True):
                    feed.append(string)
    feed = fix_feed(feed)
    return feed


def check_url(url):

    p_logger.debug('check_url')

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


def find_parser(response):

    p_logger.debug('find_parser')

    test_url = response.url
    test_string = (test_url[-3] + test_url[-2] + test_url[-1])
    if test_string == "tml":
        return "lxml"
    else:
        return "lxml-xml"


def fix_feed(feed):

    p_logger.debug('fix_feed')

    end_feed = []
    for i in range(len(feed)):
        if i == 0:
            end_feed.append(feed[i])
        elif feed[i] == feed[i - 1]:
            continue
        else:
            end_feed.append(feed[i])
    return end_feed
