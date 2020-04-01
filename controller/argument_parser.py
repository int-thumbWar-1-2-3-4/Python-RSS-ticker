import argparse
from sys import argv


def parse_args():
    parser = argparse.ArgumentParser(description="Select a file or feed to parse.")
    parser.add_argument('--url', dest='url', action='store', default="",
                        help="enter a url of an RSS or ATOM feed to parse", nargs='*')
    parser.add_argument('--file', dest='file', action='store', default="",
                        help="enter a file name to parse", nargs='*')
    parser.add_argument('--config', dest='config', action='store', default='',
                        help ="optionally enter a .yaml config file", nargs='*')
    args = parser.parse_args()
    return
#return an object with attribut .file and .url