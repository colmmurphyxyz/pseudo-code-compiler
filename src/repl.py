import pathlib

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
        tree = parser.parse(statement + "\n")
        print(tree.pretty())
        # result = interpreter.visit(tree)
        result = interpreter.interpret(tree)
        print(result)


if __name__ == "__main__":
    main()
