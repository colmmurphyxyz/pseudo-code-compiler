from typing import Iterator, TextIO
import sys

from lark import Token
from lark.lark import PostLex


class PrintDetokenization(PostLex):
    def __init__(self, output: TextIO=sys.stderr) -> None:
        self._output: TextIO = output

    def process(self, stream: Iterator[Token]) -> Iterator[Token]:
        for token in stream:
            print(token.value, end="", flush=True, file = self._output)
            yield token
