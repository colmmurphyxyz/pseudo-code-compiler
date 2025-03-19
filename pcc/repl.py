# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import pathlib
from typing import Iterator

from lark import Lark, Tree, Token
from lark.indenter import PythonIndenter

from frontend.parser import Parser
from frontend.unicode_formatter import UnicodeFormatter
from frontend.postlex_pipeline import PostLexPipeline
from backend.transpiler import Transpiler

# Import stdlib to execute repl code
from backend.pc_stdlib import * # pylint: disable=wildcard-import


class ReplParser(Parser):
    def __init__(self, grammar: str):
        self._grammar = grammar
        self._lark = Lark(
            grammar,
            start="single_input",
            postlex=PostLexPipeline([
                PythonIndenter(),
                UnicodeFormatter()
            ]))

    def parse(self, source_code: str) -> Tree:
        return self._lark.parse(source_code)

    def lex(self, source_code: str, dont_ignore: bool = False) -> Iterator[Token]:
        return self._lark.lex(source_code, dont_ignore=dont_ignore)

def main():
    parser: ReplParser
    grammar_file_path = pathlib.Path(__file__).parent.absolute() / "grammar" / "pcc.lark"
    with open(grammar_file_path, "r", encoding="utf-8") as in_file:
        grammar: str = in_file.read()
    parser = ReplParser(grammar)
    transpiler = Transpiler()

    while True:
        statement = input(">> ")
        try :
            tree = parser.parse(statement + "\n")
        except Exception as e: # pylint: disable=broad-exception-caught
            print("Parse Error", e)
            continue

        print(tree.pretty())
        try:
            result: str = transpiler.transform(tree)
            print(result)
            exec(result) # pylint: disable=exec-used
        except Exception as e: # pylint: disable=broad-exception-caught
            print("Runtime Error")
            print(e.with_traceback(None))
        finally:
            continue


if __name__ == "__main__":
    main()
