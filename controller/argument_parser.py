import argparse
from controller.start import execute
from model.model import parse


def parse_args():
    parser = argparse.ArgumentParser(description="Select a file or feed to parse.")
    parser.add_argument('--url', dest='url', action='store', default="",
                        help="enter a url of an RSS or ATOM feed to parse", nargs='*')
    parser.add_argument('--file', dest='file', action='store', default="",
                        help="enter a file name to parse", nargs='*')
    parser.add_argument('--config', dest='config', action='store', default='',
                        help="optionally enter a .yaml config file", nargs='*')
    parser.add_argument('--timer', dest='timer', action='store', type=int, default=10)
    args = parser.parse_args()

    feed = parse(args.url[0])
    feed.reverse()
    seconds = 10

    if args.timer is not None:
        seconds = args.timer

    execute(feed, seconds)


