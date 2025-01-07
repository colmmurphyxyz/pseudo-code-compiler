import unittest

from unicodeitplus import replace

from pcc.frontend.unicode_fragment import UnicodeFragment, split_unicode_fragments

class TestUnicodeFragment(unittest.TestCase):
    def test_constructor(self):
        source: str = "abcd"
        f = UnicodeFragment(source)
        self.assertEqual(source, f.ascii)
        self.assertEqual(replace(source), f.transformed)

    def test_to_string(self):
        source: str = r"\alpha_2"
        f = UnicodeFragment(source)
        self.assertEqual("UnicodeFragment(\"\\alpha_2\")", str(f))
        f = UnicodeFragment("a\\alpha\\_2")
        self.assertEqual("UnicodeFragment(\"a\\alpha\\_2\")", str(f))

    def test_split_unicode_fragment(self):
        source: str = r"alpha-$\beta$-gamma-$\delta$"
        fragments: list[str | UnicodeFragment] = split_unicode_fragments(source)
        print(fragments)
        self.assertEqual([
            "alpha-",
            UnicodeFragment("\\beta"),
            "-gamma-",
            UnicodeFragment("\\delta"),
        ], fragments)