import pathlib

from lark import Lark
from lark.indenter import PythonIndenter

from frontend.unicode_formatter import UnicodeFormatter
from frontend.postlex_pipeline import PostLexPipeline
from backend.transpiler import Transpiler

from backend.pc_stdlib import *

def main():
    grammar_file_path = pathlib.Path(__file__).parent.absolute() / "grammar/pcc.lark"
    with open(grammar_file_path, "r", encoding="utf-8") as in_file:
        grammar: str = in_file.read()
        parser = Lark(
            grammar,
            start="single_input",
            postlex=PostLexPipeline([PythonIndenter(), UnicodeFormatter()])
        )
    transpiler = Transpiler()

    while True:
        statement = input(">> ")
        try :
            tree = parser.parse(statement + "\n")
        except Exception as e:
            print("Parse Error", e)
            continue

        print(tree.pretty())
        try:
            result: str = transpiler.transform(tree)
            print(result)
            exec(result)
        except Exception as e:
            print("Runtime Error")
            print(e.with_traceback(None))
        finally:
            continue


if __name__ == "__main__":
    main()
