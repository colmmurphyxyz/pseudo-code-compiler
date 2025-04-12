# Copyright: (c) 2025, Colm Murphy <colmmurphy016@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# pylint: disable=redefined-builtin
import sys
import pathlib
from time import perf_counter_ns

import click
from lark import Lark, Tree

from frontend.pcc_parser import PccParser

def usage() -> str:
    return """
    Usage: pcc [options] file
    Options:
      -v, --version: Print version information
      -h, --help: Print this help message
      -d --debug: compile file in debug mode
      -o --output: specify output directory, defaults to ./out/output.py. This should not be changed unless you know what you are doing
      -r --output-rendered-source: Output Pseudocode source with non-ascii characters rendered as unicode. True by default
      """.strip()

@click.command(help=usage())
@click.option("-v", "--version", type=click.BOOL, default=False, is_flag=True)
@click.option("-h", "--help", type=click.BOOL, default=False, is_flag=True)
@click.option("-d", "--debug", type=click.BOOL, default=False, is_flag=True)
@click.option("-o", "--output", type=click.STRING, default="./out/output.py")
@click.option("-r", "--output-rendered-source", type=click.BOOL, default=True)
@click.argument("source_file_path", type=click.STRING, default="")
def main(version: bool, help: bool, debug: bool, output: str, source_file_path: str, output_rendered_source: bool):
    if help:
        print(usage())
        sys.exit(0)
    if version:
        print("Pseudo-Code Compiler, version 1.0.0")
        sys.exit(0)
    # if source file not given, print usage
    if not source_file_path:
        print("Error: No source file provided")
        print(usage())
        sys.exit(1)
    # if output directory does not exist, create it
    output_path: pathlib.Path = pathlib.Path(output)
    output_dir: pathlib.Path = output_path.parent
    if not output_path.parent.exists():
        output_path.parent.mkdir()

    parser: Lark
    ast: Tree
    grammar_file_path = pathlib.Path(__file__).parent.absolute() / "grammar" / "pcc.lark"
    parser: PccParser = PccParser.from_grammar_file(grammar_file_path)
    print("Performing benchmark with algorithm")
    start = perf_counter_ns()

    with open(source_file_path, "r", encoding="utf-8") as in_file:
        source = in_file.read()
        # append trailing newline if not already present
        if source[-1] != "\n":
            source += "\n"
    ast = parser.parse(source)

    end = perf_counter_ns()
    print(f"Transpiling with {parser}:\t\t{end - start} ns")

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
