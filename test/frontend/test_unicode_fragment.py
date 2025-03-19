# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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
        self.assertEqual([
            "alpha-",
            UnicodeFragment("\\beta"),
            "-gamma-",
            UnicodeFragment("\\delta"),
        ], fragments)