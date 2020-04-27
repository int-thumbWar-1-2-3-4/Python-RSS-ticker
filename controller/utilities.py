"""Controller.utilities."""
import argparse
import logging as lg


def logger(name):
	"""Controller.utilities.logger builds and returns a logger."""
	logger = lg.getLogger(name)
	sys_handler = lg.StreamHandler()
	sys_format = lg.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	sys_handler.setFormatter(sys_format)
	logger.addHandler(sys_handler)
	logger.setLevel(ticker_argument_parser().logger[0])

	return logger


def ticker_argument_parser():
    """Argument Parser for Tiny Ticker. Controller.utilities."""
    parser = argparse.ArgumentParser(description="Select a file or feed to parse.", fromfile_prefix_chars='@')
    parser.add_argument('--url', '-u', dest='url', action='store', default=["https://www.theguardian.com/us/rss"],
                        help="enter a url of an RSS or ATOM feed to parse", nargs='*')
    parser.add_argument('--file', '-f', dest='file', action='store', default="",
                        help="enter a file name to parse", nargs='*')
    parser.add_argument('--logger', '-l', dest='logger', action='store', type=str, choices={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'},
    					default=['CRITICAL'], help="optionally enter a .yaml config file", nargs='*')
    parser.add_argument('--timer', '-t', dest='timer', action='store', type=int, choices=range(1, 601), default=10,
                        help='enter an amount of time each headline should appear')
    return parser.parse_args()