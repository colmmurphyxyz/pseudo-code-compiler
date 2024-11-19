from typing import Iterator

from lark import Token
from lark.lark import PostLex


class PostLexPipeline(PostLex):
    def __init__(self, postlexers: list[PostLex]):
        super().__init__()
        self.postlexers: list[PostLex] = postlexers

    def process(self, stream: Iterator[Token]) -> Iterator[Token]:
        output: Iterator[Token] = stream
        for postlexer in self.postlexers:
            output = postlexer.process(output)
        return output