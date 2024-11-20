# pylint: disable=unused-argument
from lark import Transformer, Tree, Token


class Transpiler(Transformer):

    indent_weight: int = 4

    def __default__(self, data, children, meta):
        print(f"Using default callback for {data}")
        return data

    def indent_all_lines(self, lines: str) -> str:
        return "\n".join(map(lambda l: " " * self.indent_weight + l, lines.split("\n")))

    def file_input(self, args) -> str:
        return "\n".join(args) + "\n"

    def print_stmt(self, args) -> str:
        print(f"Printing {args}")
        return f"print({"".join(args)})"

    def while_stmt(self, args) -> str:
        while_condition: Tree = args[0]
        while_body: str = args[1]
        return f"while {self.transform(while_condition)}:" + "\n" + while_body

    def block_stmt(self, args) -> str:
        return self.indent_all_lines("\n".join(args))

    def exchange_stmt(self, args) -> str:
        lhs, rhs = args[0], args[1]
        return f"{lhs}, {rhs} = {rhs}, {lhs}"

    def expr_stmt(self, args) -> str:
        return str(args[0])

    def error_stmt(self, args) -> str:
        """
        Stub Implementation
        :return: sys.exit(1)
        """
        return "sys.exit(1)"

    def arith_expr(self, args) -> str:
        return " ".join(args)

    def var(self, args) -> str:
        return str(args[0])

    def name(self, args: list[Token]) -> str:
        return str(args[0].value)
    def _NEWLINE(self, args) -> str:
        return "\n"

    def COMMENT(self, args) -> str:
        """
        We want to ignore comments in the transpiled output. Keeping the newline
        :return: newline character
        """
        return "\n"

    def number(self, args) -> str:
        return str(args[0])

    def string(self, args) -> str:
        return f"\"{args[0]}\""

    def const_true(self, args) -> str:
        return "True"

    def const_false(self, args) -> str:
        return "False"

    def const_nil(self, args) -> str:
        return "None"
