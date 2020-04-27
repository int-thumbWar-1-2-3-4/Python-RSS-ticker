# https://github.com/drsjb80/MockingPython/blob/master/thecastleargv.py
import sys
import unittest
import logging as lg
from unittest.mock import patch
from controller.utilities import logger, ticker_argument_parser


class TestUtilities(unittest.TestCase):
    """Test class for controller.utilities."""
    def test_logger(self):
        """
        Unit test for controller.utilities.logger. Should return a Logger
        bject.
        """
        result = logger('name')
        self.assertTrue(isinstance(result, lg.Logger))


class TestArgumentParser(unittest.TestCase):
    """Test class for tests.test_argument_parser."""
    def test_has_each_argument(self):
        """
        Unit test for controller.utilities.ticker_argument_parser. Are all
        args present?
        """
        sys.argv = ['PRSST']
        args = ticker_argument_parser()
        self.assertTrue('url' in args)
        self.assertTrue('file' in args)
        self.assertTrue('logger' in args)
        self.assertTrue('timer' in args)

    def test_url(self):
        """
        Unit test for controller.utilities.ticker_argument_parser's url
        argument.
        """
        fake_url = ['www.fakeurl.com']
        sys.argv = ['test', '--url', fake_url[0]]
        args = ticker_argument_parser()

        self.assertTrue(args.url, args.timer)
        self.assertEqual(args.url, fake_url)

    def test_file(self):
        """
        Unit test for controller.utilities.ticker_argument_parser's
        file argument.
        """
        fake_file = ['fakefile.txt']
        sys.argv = ['test', '--file', fake_file[0]]
        args = ticker_argument_parser()

        self.assertTrue(args.file, args.timer)
        self.assertEqual(args.file, fake_file)

    def test_logger(self):
        """
        Unit test for controller.utilities.ticker_argument_parser's
        logger argument.
        """
        fake_logger = ['WARNING']
        sys.argv = ['test', '--logger', fake_logger[0]]
        args = ticker_argument_parser()

        self.assertTrue(args.logger, args.timer)
        self.assertFalse(args.file)
        self.assertEqual(args.logger, fake_logger)

    def test_timer(self):
        """
        Unit test for controller.utilities.ticker_argument_parser's
        timer argument.
        """
        sys.argv = ['news ticker', '--timer', '17']
        args = ticker_argument_parser()

        self.assertTrue(args.timer, args.logger)
        self.assertFalse(args.file)
        self.assertEqual(args.timer, 17)

    def test_default_timer(self):
        """
        Unit test for controller.utilities.ticker_argument_parser's
        default timer value.
        """
        sys.argv = ['this is the prog field (the name of the program']
        args = ticker_argument_parser()

        self.assertTrue(args.timer, args.logger)
        self.assertFalse(args.file)
        self.assertEqual(args.timer, 10)

    def test_all_args(self):
        """
        Unit test for controller.utilities.ticker_argument_parser testing
        the handling of all arguments at once.
        """
        # TODO, finish this test. The argument needs to be expanded

        url = "www.notasite.com"
        time = '13'
        file = 'some/file.txt'
        logger = 'ERROR'
        sys.argv = ['test', '-u', url, '-t', time, '-f', file, '-l', logger]
        args = ticker_argument_parser()
        self.assertEqual(args.url[0], url)
        # self.assertEqual(args.time, 13)


class TestTickerArgumentParser(unittest.TestCase):
    """Test class to test the creation of the argument parser."""
    @patch('controller.utilities.argparse.ArgumentParser')
    def test_calls_argparse_function_argument_parser(self, mock_parser):
        """
        Unit test for controller.utilities.ticker_argument_parser.
        Checks that our argument parser was reated correctly.
        """
        self.description = "Select a file or feed to parse."
        ticker_argument_parser()
        mock_parser.assert_called_with(description=self.description,
                                       fromfile_prefix_chars='@')
