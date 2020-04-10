#https://github.com/drsjb80/MockingPython/blob/master/thecastleargv.py
import argparse
import unittest
from mock import Mock
import controller.parser as parser
import sys
import controller.argument_parser as argument_parser

class test_URL(unittest.TestCase):
    def test_single_url(self):
        sys.argv[1:] = ["--url", "google.com"]
        args = argument_parser.parse_args()
        self.assertEqual(args.url, ['google.com'])
        self.assertEqual(args.file, "")
        self.assertEqual(args.config, "")

    def test_single_file(self):
        sys.argv[1:] = ["--file", "some_file.json"]
        args = argument_parser.parse_args()
        self.assertEqual(args.file, ['some_file.json'])
        self.assertEqual(args.url, "")
        self.assertEqual(args.config, "")

    def test_single_config(self):
        sys.argv[1:] = ["--config", "some_config.yaml"]
        args = argument_parser.parse_args()
        self.assertEqual(args.config, ['some_config.yaml'])
        self.assertEqual(args.url, "")
        self.assertEqual(args.file, "")

    def test_multiple_url(self):
        sys.argv[1:] = ["--url", "google.com"]
        args = argument_parser.parse_args()
        self.assertEqual(args.url, ['google.com'])
        self.assertEqual(args.file, "")
        self.assertEqual(args.config, "")

    def test_urls_and_files(self):
        sys.argv[1:] = ["--url", "google.com", "--file", "some_file.json", "another_file.json"]
        args = argument_parser.parse_args()
        self.assertEqual(args.url, ['google.com'])
        self.assertEqual(args.file, ["some_file.json", "another_file.json"])
        self.assertEqual(args.config, "")

    def test_timer(self):
        sys.argv = ['news ticker', '--timer', '17']
        args = argument_parser.parse_args()

        self.assertTrue(args.timer)
        self.assertFalse(args.url, args.file)
        self.assertEqual(args.timer, 17)

    def test_default_timer(self):
        sys.argv = ['this is the prog field (the name of the program']
        args = argument_parser.parse_args()

        self.assertTrue(args.timer)
        self.assertFalse(args.file, args.config)
        self.assertEqual(args.timer, 10)

    def test_all_args(self):
        pass