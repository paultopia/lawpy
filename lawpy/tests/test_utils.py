import lawpy
import utils
import unittest

class TestUtils(unittest.TestCase):

    def test_safe_merge(self):
        d1 = {"foo": 1, "bar": 2}
        d2 = {"foo": 2, "bar": ""}
        self.assertEqual(utils.safe_merge(d1, d2), {"foo": 2, "bar": 2})
