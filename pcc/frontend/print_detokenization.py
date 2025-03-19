# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from typing import Iterator, TextIO
import sys

from lark import Token
from lark.lark import PostLex


class PrintDetokenization(PostLex):
    def __init__(self, output: TextIO=sys.stderr) -> None:
        self._output: TextIO = output

    def iswhitespace(self, token: Token) -> bool:
        return token.strip() == ""

    def process(self, stream: Iterator[Token]) -> Iterator[Token]:
        for token in stream:
            print(token.value, end="", file = self._output)
            if len(token) > 0 and not self.iswhitespace(token[-1]):
                print(" ", end="", flush=True, file=self._output)
            yield token
