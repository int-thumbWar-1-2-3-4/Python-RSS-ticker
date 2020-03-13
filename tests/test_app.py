import unittest
import sys
import os

directory = os.path.dirname(__file__)
relativePath = directory[0: len(directory) - 5]

sys.path.append(relativePath)


from tkinter import Tk
from View import app 


class TestApp(unittest.TestCase):

    def test_root(self):
        self.assertInstaceOf(app.root, Tk)


if __name__ == '__main__':
    unittest.main()
