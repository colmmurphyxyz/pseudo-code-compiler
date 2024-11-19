import sys
import pathlib
import logging

from lark import Lark, Tree, logger
from lark.indenter import PythonIndenter

from print_detokenization import PrintDetokenization
from unicode_formatter import UnicodeFormatter
from postlex_pipeline import PostLexPipeline

logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    parser: Lark
    tree: Tree
    grammar_file_path = pathlib.Path(__file__).parent.absolute() / "grammar/pcc.lark"
    print("opening", grammar_file_path)
    with open(grammar_file_path, "r") as in_file:
        grammar: str = in_file.read()
        parser = Lark(grammar, start="file_input", postlex=PostLexPipeline([PythonIndenter(), UnicodeFormatter(), PrintDetokenization()]))
    with open(sys.argv[1], "r") as in_file:
        source = in_file.read()
        # append trailing newline if not already present
        if source[-1] != "\n": source += "\n"
    print("SOURCE:", source)
    tree = parser.parse(source)
    # print(tree.pretty())

    print("~~~ Interpreter ~~~")
    # interpreter = PcInterpreter()
    # interpreter.visit(tree)
