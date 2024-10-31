import sys

from lark import Lark, Tree, Token, Transformer, logger
from lark.indenter import PythonIndenter
import pathlib
import logging

from transpiler import Transpiler

logger.setLevel(logging.DEBUG)

class TreeToJson(Transformer):
    def string(self, s) -> str:
        (s,) = s
        return s[1:-1]

    def number(self, n) -> float:
        (n,) = n
        return float(n)

    list = list
    pair = tuple
    dict = dict

    null = lambda self, _: None
    true = lambda self, _: True
    false = lambda self, _: False

if __name__ == "__main__":
    parser: Lark
    tree: Tree
    grammar_file_path = pathlib.Path(__file__).parent.absolute() / "grammar/pcc.lark"
    print("opening", grammar_file_path)
    with open(grammar_file_path, "r") as in_file:
        grammar: str = in_file.read()
        parser = Lark(grammar, start="file_input", postlex=PythonIndenter())
    with open(sys.argv[1], "r") as in_file:
        source = in_file.read()
    # source: str = " ".join(sys.argv[1:])
    print("SOURCE:", source)
    tree = parser.parse(source)
    print(tree.pretty())
    print(tree)
    print("Done")
    transpiler = Transpiler()
    transpiled = transpiler.transform(tree)
    print("---TRANSPILED---")
    print(transpiled)