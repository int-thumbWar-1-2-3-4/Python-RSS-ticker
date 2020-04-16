# https://github.com/drsjb80/MockingPython/blob/master/thecastleargv.py
from controller.start import ticker_argument_parser
import unittest
from unittest.mock import patch
import sys


class TestArgumentParser(unittest.TestCase):

    def test_has_each_argument(self):
        sys.argv = ['PRSST']
        args = ticker_argument_parser()
        self.assertTrue('url' in args)
        self.assertTrue('file' in args)
        self.assertTrue('config' in args)
        self.assertTrue('timer' in args)

    def test_url(self):
        fake_url = ['www.fakeurl.com']
        sys.argv = ['test', '--url', fake_url[0]]
        args = ticker_argument_parser()

        self.assertTrue(args.url, args.timer)
        self.assertFalse(args.config)
        self.assertEqual(args.url, fake_url)

    def test_file(self):
        fake_file = ['www.fakefile.com']
        sys.argv = ['test', '--file', fake_file[0]]
        args = ticker_argument_parser()

        self.assertTrue(args.file, args.timer)
        self.assertFalse(args.config)
        self.assertEqual(args.file, fake_file)

    def test_config(self):
        fake_config = ['www.fakeconfig.com']
        sys.argv = ['test', '--config', fake_config[0]]
        args = ticker_argument_parser()

        self.assertTrue(args.config, args.timer)
        self.assertFalse(args.file)
        self.assertEqual(args.config, fake_config)

    def test_timer(self):
        sys.argv = ['news ticker', '--timer', '17']
        args = ticker_argument_parser()

        self.assertTrue(args.timer, args.url)
        self.assertFalse(args.config, args.file)
        self.assertEqual(args.timer, 17)

    def test_default_timer(self):
        sys.argv = ['this is the prog field (the name of the program']
        args = ticker_argument_parser()

        self.assertTrue(args.timer)
        self.assertFalse(args.file, args.config)
        self.assertEqual(args.timer, 10)

    def test_all_args(self):
        url = "www.notasite.com"
        time = 13
        file = 'some/file.txt'
        config = 'some/other/file.yml'
        sys.argv = ['test', '--url', url]
        args = ticker_argument_parser()
        self.assertEqual(args.url[0], url)


class TestTickerArgumentParser(unittest.TestCase):

    @patch('controller.start.argparse.ArgumentParser')
    def test_calls_argparse_function_argument_parser(self, mock_argument_parser):
        args = ticker_argument_parser()
        mock_argument_parser.assert_called_with(description="Select a file or feed to parse.")
