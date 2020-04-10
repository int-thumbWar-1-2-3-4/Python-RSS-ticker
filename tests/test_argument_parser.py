import parser
import unittest
import sys
from mock import Mock
import argparse
import controller.argument_parser

class TestArgs(unittest.TestCase):
    def test_single_url(self):
        sys.argv= ["--url", "google.com"]
        args = argparse.argument_parser()
        parser.add_argument('--url', action='store_true')
        args = parser.parse_args()

        self.assertEqual(args.url, ['google.com'])
        self.assertEqual(args.file, "")
        self.assertEqual(args.config, "")

    def test_single_file(self):
        sys.argv = ["--file", "some_file.json"]
        args = argparse.argument_parser()
        parser.add_argument('--file', action='store_true')
        args = parser.parse_args()

        self.assertEqual(args.file, ['some_file.json'])
        self.assertEqual(args.url, "")
        self.assertEqual(args.config, "")

    def test_single_config(self):
        sys.argv = ["--config", "some_config.yaml"]
        args = argparse.argument_parser()
        parser.add_argument('--config', action='store_true')
        args = parser.parse_args()

        self.assertEqual(args.config, ['some_config.yaml'])
        self.assertEqual(args.url, "")
        self.assertEqual(args.file, "")

    def test_multiple_url(self):
        sys.argv = ["--url", "google.com"]
        args = argparse.argument_parser()
        parser.add_argument('--url', action='store_true')
        args = parser.parse_args()

        self.assertEqual(args.url, ['google.com'])
        self.assertEqual(args.file, "")
        self.assertEqual(args.config, "")

    def test_timer(self):
        sys.argv = ["--timer", ""]
        args = argparse.argument_parser()
        args = parser.parse_args()


        self.assertEqual(args.url, ['google.com'])
        self.assertEqual(args.file, ["some_file.json", "another_file.json"])
        self.assertEqual(args.config, "")
