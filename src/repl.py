import pathlib
import sys

from lark import Lark
from lark.indenter import PythonIndenter

from interpreter import PcInterpreter
from unicode_formatter import UnicodeFormatter
from postlex_pipeline import PostLexPipeline


def main():
    grammar_file_path = pathlib.Path(__file__).parent.absolute() / "grammar/pcc.lark"
    with open(grammar_file_path, "r") as in_file:
        grammar: str = in_file.read()
        parser = Lark(grammar, start="single_input", postlex=PostLexPipeline([PythonIndenter(), UnicodeFormatter()]))
    interpreter = PcInterpreter()
    while True:
        statement = input(">> ")
        try :
            tree = parser.parse(statement + "\n")
        except Exception as e:
            print("Parse Error", e)
            continue

        print(tree)
        print(tree.pretty())
        # result = interpreter.visit(tree)
        try:
            result = interpreter.interpret(tree)
        except Exception as e:
            print("Runtime Error", e)
            continue

        print(result)


if __name__ == "__main__":
    main()
