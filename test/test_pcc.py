# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import unittest

from test.frontend.test_unicode_fragment import TestUnicodeFragment
from test.frontend.test_unicode_formatter import TestUnicodeFormatter

class TestPcc(unittest.TestCase):
    def test_my_test(self):
        self.assertTrue(1 > 0)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestUnicodeFragment("test_unicode_fragment"))
    suite.addTest(TestUnicodeFormatter("test_unicode_formatter"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
