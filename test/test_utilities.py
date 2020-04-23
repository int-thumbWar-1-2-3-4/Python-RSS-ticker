import unittest
import logging as lg
from controller.utilities import logger


class TestLogger(unittest.TestCase):

	def test_logger(self):
		result = logger('name')
		self.assertTrue(isinstance(result, lg.Logger))
