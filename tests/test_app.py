import unittest
from tkinter import Tk
from View import app


class TestApp(unittest.TestCase):

    def test_root(self):
        self.assertInstaceOf(app.root, Tk)

if __name__ == '__main__':
    unittest.main()

