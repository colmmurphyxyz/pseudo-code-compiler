from __future__ import annotations
from pathlib import Path

from lark import Lark, Tree
from lark.indenter import PythonIndenter

from .parser import Parser
from .postlex_pipeline import PostLexPipeline
from .unicode_formatter import UnicodeFormatter
from .print_detokenization import PrintDetokenization

class PccParser(Parser):
    def __init__(self, grammar: str):
        super().__init__()
        self._grammar = grammar

    @staticmethod
    def from_grammar_file(grammar_file_path: str | Path) -> PccParser:
        with open(grammar_file_path) as grammar_file:
            return PccParser(grammar_file.read())

    @property
    def grammar(self) -> str:
        return self._grammar

    def parse(self, source_code: str) -> Tree:
        lark = Lark(self._grammar, start="file_input", postlex=PostLexPipeline([
            PythonIndenter(), UnicodeFormatter(), PrintDetokenization()
        ]))
        if source_code[-1] != "\n":
            source_code += "\n"
        return lark.parse(source_code)

