# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from typing import Iterator
import unicodedata

from lark import Token
from lark.lark import PostLex

from .unicode_fragment import UnicodeFragment, split_unicode_fragments


def _get_symbol_name(symbol: str) -> str:
    name = unicodedata.name(symbol)
    return name.split(" ")[-1].lower()


class UnicodeFormatter(PostLex):
    def process(self, stream: Iterator[Token]) -> Iterator[Token]:
        for token in stream:
            if token.type != "NAME":
                yield token
                continue
            fragments = split_unicode_fragments(token.value)
            transformed: list[str] = list(map(
                lambda x: _get_symbol_name(x.transformed) if isinstance(x, UnicodeFragment) else x, fragments
            ))
            formatted = "".join(transformed)
            token.value = formatted
            yield token
