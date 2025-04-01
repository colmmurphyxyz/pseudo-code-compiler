import unittest

from lark import Token

from pcc.frontend.keyword_normalizer import KeywordNormalizer

class TestKeywordNormalizer(unittest.TestCase):
    UNDERTIE = '\u203F'
    normalizer = KeywordNormalizer()

    def setUp(self):
        self.non_name_token = Token("DEC_INTEGER", 123)
        self.name_token = Token("NAME", "my_identifier")
        self.pykw_identifier1 = Token("NAME", "await")
        self.pykw_identifier2 = Token("NAME", "yield")
        self.unicode_identifier = Token("NAME", "var$\\alpha$")

    def test_normalize_keyword(self):
        res = self.normalizer.process(iter([self.pykw_identifier1]))
        self.assertEqual(next(res).value, "await" + self.UNDERTIE)
        res = self.normalizer.process(iter([self.non_name_token]))
        self.assertEqual(next(res).value, 123)
        res = self.normalizer.process(iter([self.pykw_identifier2]))
        self.assertEqual(next(res).value, "yield" + self.UNDERTIE)
        res = self.normalizer.process(iter([self.unicode_identifier]))
        self.assertEqual(next(res).value, "var$\\alpha$")