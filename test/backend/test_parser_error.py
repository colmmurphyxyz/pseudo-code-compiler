import unittest

from pcc.backend.parser_error import ParserError

class TestParserError(unittest.TestCase):
    def test_error_message(self):
        error = ParserError("Syntax error")
        self.assertEqual(error.message, "Syntax error")

    def test_str(self):
        error = ParserError("Syntax error")
        self.assertEqual(str(error), "Syntax error")