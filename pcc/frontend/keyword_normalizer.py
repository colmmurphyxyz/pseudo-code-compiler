from typing import Iterator

from lark import Token
from lark.lark import PostLex


class KeywordNormalizer(PostLex):
    UNDERTIE = '\u203F'
    PY_KEYWORDS = {"as", "assert", "async", "await", "class", "def", "del", "elif", "except", "finally", "from", "global",
                   "import", "is", "lambda", "nonlocal", "pass", "raise", "try", "with", "yield"}

    def _normalize(self, token: Token) -> None:
        if token.value not in self.PY_KEYWORDS:
            return
        orig = token.value
        token.value = orig + self.UNDERTIE

    def process(self, stream: Iterator[Token]) -> Iterator[Token]:
        for token in stream:
            if token.type == "NAME":
                self._normalize(token)
            yield token
