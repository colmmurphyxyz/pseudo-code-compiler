# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import unittest
from collections.abc import Iterator

from lark import Token

from pcc.frontend.unicode_formatter import UnicodeFormatter


def make_token(type: str, value: str) -> Token:
    return Token(type, value)

class TestUnicodeFormatter(unittest.TestCase):

    def test_format_ascii_identifier(self):
        token = make_token("NAME", "foobar")
        token_stream: Iterator[Token] = iter([token])
        formatter = UnicodeFormatter()
        output = formatter.process(token_stream)
        formatted_token = next(output)
        self.assertEqual(formatted_token, token)

    def test_format_unicode_identifier(self):
        token = make_token("NAME", "$\\beta$")
        token_stream: Iterator[Token] = iter([token])
        formatter = UnicodeFormatter()
        output = formatter.process(token_stream)
        formatted_token = next(output)
        self.assertEqual(formatted_token.value, "beta")

    def test_mixed_format_identifier(self):
        token = make_token("NAME", r"one-$\alpha$-two")
        token_stream: Iterator[Token] = iter([token])
        formatter = UnicodeFormatter()
        output = formatter.process(token_stream)
        formatted_token = next(output)
        self.assertEqual(formatted_token.value, "one-alpha-two")