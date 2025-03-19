# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from typing import Iterator

from lark import Token
from lark.lark import PostLex

from .unicode_fragment import UnicodeFragment, split_unicode_fragments


class Renderer(PostLex):
    _identifiers: set[tuple[str, str]]

    @property
    def identifiers(self) -> set[tuple[str, str]]:
        return self._identifiers

    def __init__(self):
        self._identifiers = set()

    def process(self, stream: Iterator[Token]) -> Iterator[Token]:
        for token in stream:
            if token.type != "NAME":
                yield token
                continue
            orig_value: str = token.value
            fragments = split_unicode_fragments(token.value)
            transformed: list[str] = list(map(
                lambda x: x.transformed if isinstance(x, UnicodeFragment) else x, fragments
            ))
            formatted = "".join(transformed)
            self._identifiers.add((orig_value, formatted))
            yield token
