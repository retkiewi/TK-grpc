import unittest
from format.format_checker import check_for_formats


desired_formats = ['.jpg', '.jp2']
path = "somepath/somepath/somefile.jpg"

class TestFormatChecker(unittest.TestCase):
    def test_check_for_formats(self):
        actual = check_for_formats(file_path=path, desired_formats=desired_formats)
        expected = True
        self.assertEqual(actual, expected)

