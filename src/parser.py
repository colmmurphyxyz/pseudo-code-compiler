import sys

from lark import Lark, Tree, Token, Transformer

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
    json_parser: Lark
    tree: Tree
    with open("src/grammar/json_grammar.lark", "r") as in_file:
        grammar: str = in_file.read()
        json_parser = Lark(grammar, start="value", parser="lalr", transformer=TreeToJson())
    with open(sys.argv[1], "r") as in_file:
        tree = json_parser.parse(in_file.read())
    print(tree)