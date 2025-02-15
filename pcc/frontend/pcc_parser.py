from __future__ import annotations

from copy import copy
from pathlib import Path
from typing import Iterator

from lark import Lark, Tree, Token
from lark.indenter import PythonIndenter

from .parser import Parser
from .postlex_pipeline import PostLexPipeline
from .renderer import Renderer
from .unicode_formatter import UnicodeFormatter

class PccParser(Parser):

    _rendered_source: str = None

    def __init__(self, grammar: str | Path):
        super().__init__()
        self._grammar = grammar
        self._renderer = Renderer()
        self._lark = Lark(self._grammar, propagate_positions=True, start="file_input", postlex=PostLexPipeline([
            PythonIndenter(), self._renderer, UnicodeFormatter()
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
        if source_code[-1] != "\n":
            source_code += "\n"
        ast = self._lark.parse(source_code)
        identifiers: set[tuple[str, str]] = self._renderer.identifiers
        self._rendered_source = copy(source_code)
        for orig, rendered in identifiers:
            print(f"replace '{orig}' with {rendered}'")
            self._rendered_source = self._rendered_source.replace(orig, rendered)
        with open("out/rendered.pc", "w", encoding="utf-8") as file:
            file.write(self._rendered_source)
        return ast

    def lex(self, source_code: str, dont_ignore: bool = False) -> Iterator[Token]:
        return self._lark.lex(source_code, dont_ignore)
