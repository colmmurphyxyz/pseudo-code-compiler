import pathlib
import sys

from lark import Token, Tree

from frontend.pcc_parser import PccParser
from backend.line_count_transpiler import LineCountTranspiler

usage: str = """
usage: python ipcc [options] file
""".strip()

def main(argv: list[str]):
    if len(argv) != 2:
        print(usage)
        sys.exit(1)
    source_code: str
    with open(argv[1]) as file:
        source_code = file.read()
    parser = PccParser.from_grammar_file(pathlib.Path(__file__).parent.absolute() / "grammar/pcc.lark")
    tokens: list[Token] = list(parser.lex(source_code))
    ast: Tree = parser.parse(source_code)
    transpiler: LineCountTranspiler = LineCountTranspiler()
    output: str = transpiler.transpile(ast)

    print("### OUTPUT ###")
    print(output)

if __name__ == '__main__':
    main(sys.argv)
