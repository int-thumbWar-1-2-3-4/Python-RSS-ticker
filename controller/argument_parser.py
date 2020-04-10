import argparse


def ticker_argument_parser():
    parser = argparse.ArgumentParser(description="Select a file or feed to parse.")
    parser.add_argument('--url', dest='url', action='store', default=["https://www.theguardian.com/us/rss"],
                        help="enter a url of an RSS or ATOM feed to parse", nargs='*')
    parser.add_argument('--file', dest='file', action='store', default="",
                        help="enter a file name to parse", nargs='*')
    parser.add_argument('--config', dest='config', action='store', default='',
                        help="optionally enter a .yaml config file", nargs='*')
    parser.add_argument('--timer', dest='timer', action='store', type=int, default=10,
                        help='enter an amount of time each headline should appear')
    return parser.parse_args()






