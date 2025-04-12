# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import annotations

from copy import copy
from pathlib import Path
from typing import Iterator

from lark import Lark, Tree, Token
from lark.indenter import PythonIndenter

from .keyword_normalizer import KeywordNormalizer
from .parser import Parser
from .postlex_pipeline import PostLexPipeline
from .renderer import Renderer
from .unicode_formatter import UnicodeFormatter

class PccParser(Parser):

    _rendered_source: str = None

    def __init__(self, grammar: str):
        super().__init__()
        self._grammar = grammar
        self._renderer = Renderer()
        self._lark = Lark(self._grammar, propagate_positions=True, start="file_input", postlex=PostLexPipeline([
            PythonIndenter(), self._renderer, UnicodeFormatter(), KeywordNormalizer()
        ]))

    @property
    def rendered_source(self) -> str | None:
        return self._rendered_source

    @staticmethod
    def from_grammar_file(grammar_file_path: str | Path) -> PccParser:
        with open(grammar_file_path, encoding="utf-8") as grammar_file:
            return PccParser(grammar_file.read())

    @property
    def grammar(self) -> str:
        return self._grammar

    def parse(self, source_code: str) -> Tree:
        # append trailing newline if not present
        if source_code[-1] != "\n":
            source_code += "\n"
        ast = self._lark.parse(source_code)

        # replace latex expressions with unicode to use in debugger GUI and other presentations
        # `ast` has already transformed latex expressions to ascii
        identifiers: set[tuple[str, str]] = self._renderer.identifiers
        self._rendered_source = copy(source_code)
        for orig, rendered in identifiers:
            self._rendered_source = self._rendered_source.replace(orig, rendered)

        return ast

    def lex(self, source_code: str, dont_ignore: bool = False) -> Iterator[Token]:
        return self._lark.lex(source_code, dont_ignore)
