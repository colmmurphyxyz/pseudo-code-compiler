import sys
import pathlib

from lark import Lark, Tree
from lark.indenter import PythonIndenter

from frontend.unicode_formatter import UnicodeFormatter
from frontend.print_detokenization import PrintDetokenization
from frontend.postlex_pipeline import PostLexPipeline
from src.backend.transpiler import Transpiler

if __name__ == "__main__":
    parser: Lark
    tree: Tree
    grammar_file_path = pathlib.Path(__file__).parent.absolute() / "grammar/pcc.lark"
    print("opening", grammar_file_path)
    with open(grammar_file_path, "r", encoding="utf-8") as in_file:
        grammar: str = in_file.read()
        parser = Lark(grammar, start="file_input", postlex=PostLexPipeline([
            PythonIndenter(), UnicodeFormatter(), PrintDetokenization()
        ]))
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
