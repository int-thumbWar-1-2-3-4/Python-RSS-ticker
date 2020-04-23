import unittest
import logging as lg
from controller.utilities import logger


class TestUtilities(unittest.TestCase):
""" Test class for controller.utilities """

	def test_logger(self):
		""" Unit test for controller.utilities.logger. Should return a Logger object """
		
		result = logger('name')
		self.assertTrue(isinstance(result, lg.Logger))
