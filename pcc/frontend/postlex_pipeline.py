# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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
