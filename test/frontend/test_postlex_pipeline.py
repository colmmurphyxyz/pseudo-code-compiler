import unittest
from typing import Iterator

from lark import Token
from lark.lark import PostLex

from pcc.frontend.postlex_pipeline import PostLexPipeline


class DummyPostLex(PostLex):
    """
    Dummy post-lexing class that does nothing.
    """
    def process(self, stream: Iterator[Token]) -> Iterator[Token]:
        for token in stream:
            token.value += "X"
            yield token

class TestPostLexPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = PostLexPipeline([DummyPostLex(), DummyPostLex()])

    def test_process(self):
        tokens = [Token("NAME", "test"), Token("NUMBER", "42")]
        result = list(self.pipeline.process(iter(tokens)))
        for tok in result:
            self.assertEqual(tok.value[-2:], "XX")