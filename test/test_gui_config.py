import yaml
import unittest
from unittest.mock import patch, mock_open
# source:https://stackoverflow.com/questions/1289894/how-do-i-mock-an-open-used-in-a-with-statement-using-the-mock-framework-in-pyth

class TestGuiConfig(unittest.TestCase):
    def test_loader(self):
        with patch("builtins.open", mock_open(read_data="data")) as mock_file:
            assert open("path/to/open").safe_load() == "data"
            mock_file.assert_called_with("path/to/open")


if __name__ == '__main__':
    unittest.main()
