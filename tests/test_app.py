import unittest
from tkinter import Tk
from view import app


class TestApp(unittest.TestCase):

    #    def test_root(self):
    #        self.assertInstaceOf(app.root, Tk)

    def testAppWhereAmI(self):
        assert app.whereAmI() == 'Inside app.py'


if __name__ == '__main__':
    unittest.main()
