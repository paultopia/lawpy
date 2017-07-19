import lawpy
import unittest

class TestCourtlistener(unittest.TestCase):

    def setUp(self):
        self.session = lawpy.courtlistener()

    def test_can_fetch_case_by_cite(self):
        brown = self.session.fetch_cases_by_cite("347 U.S. 483")
        self.assertEqual(brown[0].name, 'Brown v. Board of Education')
