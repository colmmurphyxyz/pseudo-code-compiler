import unittest
from pathlib import Path

from pcc.backend.transpiler import Transpiler
from pcc.frontend.pcc_parser import PccParser


class TestTranspiler(unittest.TestCase):
    def setUp(self):
        self.transpiler: Transpiler = Transpiler()
        self.transpiler.preamble = ""
        self.parser = PccParser.from_grammar_file(Path(__file__).parent.parent.parent / "pcc" / "grammar" / "pcc.lark")

    def _translate(self, input_code: str) -> str:
        ast = self.parser.parse(input_code)
        return self.transpiler.transpile(ast)

    def test_transpile(self):
        # Example input for transpilation
        input_code = "print \"Hello, World!\""
        # Expected output after transpilation
        expected_output = "print(\"Hello, World!\")"
        ast = self.parser.parse(input_code)
        # Perform transpilation
        result = self.transpiler.transpile(ast).strip()

        # Check if the transpiled code matches the expected output
        self.assertEqual(result, expected_output)

    def test_const_nil(self):
        input = "NIL"
        expected = "None"
        ast = self.parser.parse(input)
        res = self.transpiler.transpile(ast).strip()
        self.assertEqual(res, expected)

    def test_const_true(self):
        expected = "True"
        res = self._translate("TRUE").strip()
        self.assertEqual(res, expected)

    def test_const_false(self):
        expeected = "False"
        res = self._translate("FALSE").strip()
        self.assertEqual(res, expeected)

    def test_string(self):
        expected = "\"Hello, World!\""
        res = self._translate("\"Hello, World!\"").strip()
        self.assertEqual(res, expected)

    def test_number(self):
        expected = "42"
        res = self._translate("42").strip()
        self.assertEqual(res, expected)

    def test_comment(self):
        expected = "print(2)"
        res = self._translate("print 2 // comment").strip()
        self.assertEqual(res, expected)

    def test_name(self):
        res = self._translate("my-variable").strip()
        self.assertEqual(res, "my_variable")
        res = self._translate("var'").strip()
        self.assertEqual(res, "var_prime")

    def test_funccall(self):
        expected = "my_function(12, A, n)"
        res = self._translate("my-function(12, A, n)").strip()
        self.assertEqual(res, expected)

    def test_set_literal(self):
        res = self._translate("{1, 2, 3}").strip()
        self.assertEqual(res, "PcSet.of(1, 2, 3)")
        res = self._translate("{}").strip()
        self.assertEqual(res, "PcSet.of()")

    def test_array_literal(self):
        res = self._translate("x = [1, 2, 3]").strip()
        self.assertEqual(res, "x = PcArray.of(1, 2, 3)")
