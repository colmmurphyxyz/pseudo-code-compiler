# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import pathlib
import unittest

from pcc.backend.transpiler import Transpiler
from pcc.frontend.pcc_parser import PccParser
from test.frontend.test_unicode_fragment import TestUnicodeFragment
from test.frontend.test_unicode_formatter import TestUnicodeFormatter
from test.frontend.test_renderer import TestRenderer
from test.frontend.test_keyword_normalizer import TestKeywordNormalizer
from test.frontend.test_postlex_pipeline import TestPostLexPipeline
from test.backend.test_transpiler import TestTranspiler
from test.backend.test_parser_error import TestParserError

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
    suite.addTest(TestRenderer("test_renderer"))
    suite.addTest(TestKeywordNormalizer("test_keyword_normalizer"))
    suite.addTest(TestPostLexPipeline("test_postlex_pipeline"))
    suite.addTest(TestTranspiler("test_transpiler"))
    suite.addTest(TestParserError("test_parser_error"))
    suite.addTest(TestPcc("test_my_test"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
