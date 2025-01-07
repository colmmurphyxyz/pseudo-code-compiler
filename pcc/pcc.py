import sys
import pathlib

from lark import Lark, Tree

from frontend.pcc_parser import PccParser
from backend.transpiler import Transpiler

if __name__ == "__main__":
    parser: Lark
    tree: Tree
    grammar_file_path = pathlib.Path(__file__).parent.absolute() / "grammar/pcc.lark"
    print("opening", grammar_file_path)
    parser: PccParser = PccParser.from_grammar_file(grammar_file_path)

    with open(sys.argv[1], "r", encoding="utf-8") as in_file:
        source = in_file.read()
        # append trailing newline if not already present
        if source[-1] != "\n":
            source += "\n"
    print("SOURCE:", source)
    tree = parser.parse(source)
    print(tree.pretty())

    print("~~~ Transpiler ~~~")
    transpiler = Transpiler()
    output: str = transpiler.transform(tree)
    print(output)
    output_path: pathlib.Path = pathlib.Path(__file__).parent.parent.absolute() / "out/out.py"
    with open(output_path, "w", encoding="utf-8") as out_file:
        out_file.write(output)
