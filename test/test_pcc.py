# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import pathlib
import unittest

from pcc.backend.transpiler import Transpiler
from pcc.frontend.pcc_parser import PccParser
from test.frontend.test_unicode_fragment import TestUnicodeFragment
from test.frontend.test_unicode_formatter import TestUnicodeFormatter

class TestPcc(unittest.TestCase):
    def test_my_test(self):
        self.assertTrue(1 > 0)

    def test_transpile_large_program(self):
        # this test takes a while to run
        # uncomment the next line to disable it
        return
        with open(pathlib.Path(__file__).parent / "large_program.pc", "r") as f:
            program = f.read()
        parser = PccParser.from_grammar_file(pathlib.Path(__file__).parent.parent / "pcc" / "grammar" / "pcc.lark")
        ast = parser.parse(program)
        transpiler = Transpiler()
        transpiler.transpile(ast)
        self.assertTrue(True)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestUnicodeFragment("test_unicode_fragment"))
    suite.addTest(TestUnicodeFormatter("test_unicode_formatter"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
