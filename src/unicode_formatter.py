from typing import Iterator

from lark import Token
from lark.lark import PostLex

from unicode_fragment import UnicodeFragment, split_unicode_fragments


class UnicodeFormatter(PostLex):

    def __init__(self):
        super().__init__()

    def process(self, stream: Iterator[Token]) -> Iterator[Token]:
        for token in stream:
            if token.type != "NAME":
                yield token
                continue
            fragments = split_unicode_fragments(token.value)
            transformed: list[str] = list(map(lambda x: x.transformed if type(x) == UnicodeFragment else x, fragments))
            formatted = "".join(transformed)
            token.value = formatted
            yield token