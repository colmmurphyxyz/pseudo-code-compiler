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
    # temp_input_file = pathlib.Path(str(__file__)).parent.absolute() / "input.pc"
    input_file = argv[1]

    with open(input_file, "r", encoding="utf-8") as file:
        source_code = file.read()
    parser = PccParser.from_grammar_file(pathlib.Path(__file__).parent.absolute() / "grammar/pcc.lark")
    # tokens: list[Token] = list(parser.lex(source_code))
    ast: Tree = parser.parse(source_code)
    transpiler: LineCountTranspiler = LineCountTranspiler(source_code=source_code)
    output: str = transpiler.transpile(ast)
    output_file: pathlib.Path = pathlib.Path(str(__file__)).parent.absolute() / "output.py"
    with open(output_file, "w") as file:
        file.write(output)

    print("### OUTPUT ###")
    print(output)

if __name__ == '__main__':
    main(sys.argv)
