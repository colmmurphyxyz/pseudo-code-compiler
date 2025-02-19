# pylint: disable=redefined-builtin
import sys
import pathlib

import click
from lark import Lark, Tree

from frontend.pcc_parser import PccParser
from backend.transpiler import Transpiler
from backend.line_count_transpiler import LineCountTranspiler


def usage() -> str:
    return """
    Usage: pcc [options] file
    Options:
      -v, --version: Print version information
      -h, --help: Print this help message
      -d --debug: compile file in debug mode
      -o --output: specify output directory, defaults to ./out/output.py
      """

@click.command(help=usage())
@click.option("-v", "--version", type=click.BOOL, default=False, is_flag=True)
@click.option("-h", "--help", type=click.BOOL, default=False, is_flag=True)
@click.option("-d", "--debug", type=click.BOOL, default=False, is_flag=True)
@click.option("-o", "--output", type=click.STRING, default="./out/output.py")
@click.argument("source_file_path", type=click.STRING, default="")
def main(version: bool, help: bool, debug: bool, output: str, source_file_path: str):
    if help:
        print("Usage: pcc [options] file")
        print("Options:")
        print("  -v, --version: Print version information")
        print("  -h, --help: Print this help message")
        print("  -d --debug: compile file in debug mode")
        print("  -o --output: specify output directory, defaults to ./out")
        sys.exit(0)
    if version:
        print("Pseudo-Code Compiler, version x.y.z")
        sys.exit(0)
    # if output directory does not exist, create it
    output_path: pathlib.Path = pathlib.Path(output)
    output_dir: pathlib.Path = output_path.parent
    if not output_path.parent.exists():
        output_path.parent.mkdir()

    parser: Lark
    tree: Tree
    grammar_file_path = pathlib.Path(__file__).parent.absolute() / "grammar/pcc.lark"
    print("opening", grammar_file_path)
    parser: PccParser = PccParser.from_grammar_file(grammar_file_path)

    with open(source_file_path, "r", encoding="utf-8") as in_file:
        source = in_file.read()
        # append trailing newline if not already present
        if source[-1] != "\n":
            source += "\n"
    tree = parser.parse(source)
    rendered_source: str = parser.rendered_source
    with open(output_dir / "rendered_source.pc", "w", encoding="utf-8") as out_file:
        out_file.write(rendered_source)

    print("~~~ Transpiler ~~~")
    transpiler: Transpiler = LineCountTranspiler() if debug else Transpiler()
    output_code: str = transpiler.transpile(tree)
    with open(output_path, "w", encoding="utf-8") as out_file:
        out_file.write(output_code)

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
