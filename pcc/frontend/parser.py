# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from typing import Iterator, Protocol

from lark import Tree, Token

class Parser(Protocol):
    def parse(self, source_code: str) -> Tree:
        ...

    def lex(self, source_code: str, dont_ignore: bool = False) -> Iterator[Token]:
        ...

# if __name__ == "__main__":
#     parser: Lark
#     tree: Tree
#     grammar_file_path = pathlib.Path(__file__).parent.absolute() / "grammar/pcc.lark"
#     print("opening", grammar_file_path)
#     with open(grammar_file_path, "r", encoding="utf-8") as in_file:
#         grammar: str = in_file.read()
#         parser = Lark(grammar, start="file_input", postlex=PostLexPipeline([
#             PythonIndenter(), UnicodeFormatter(), PrintDetokenization()
#         ]))
#     with open(sys.argv[1], "r", encoding="utf-8") as in_file:
#         source = in_file.read()
#         # append trailing newline if not already present
#         if source[-1] != "\n":
#             source += "\n"
#     print("SOURCE:", source)
#     tree = parser.parse(source)
#     # print(tree.pretty())
#
#     print("~~~ Interpreter ~~~")
#     interpreter = PcInterpreter()
#     interpreter.visit(tree)
