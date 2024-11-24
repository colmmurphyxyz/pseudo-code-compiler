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

    def single_input(self, args) -> str:
        return args + "\n"

    def print_stmt(self, args) -> str:
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

    # FIXME: 'else' branches are not transpiled correctly
    def if_stmt(self, args) -> str:
        print("IF STMT", "\n".join([ str(a) for a in args ]) )
        if_condition = args[0]
        if_body = args[1]
        return f"if {self.transform(if_condition)}:" + "\n" + if_body + "\n" + "\n".join(args[2:])

    def elifs(self, args):
        return "\n".join(args)

    def elif_(self, args):
        elif_condition = args[0]
        elif_body = args[1]
        return f"elif {self.transform(elif_condition)}:" + "\n" + elif_body

    def for_stmt(self, args):
        return args[0]

    def for_loop(self, args):
        name = args[0]
        start = args[1]
        range_op = args[2]
        end = args[3]
        loop_body = args[4]
        range_expr: str
        match range_op:
            case "to": range_expr = f"range({start}, {end} + 1)"
            case "until": range_expr = f"range({start}, {end})"
            case "downto": range_expr = f"range({start}, {end} - 1, -1)"
            case _: range_expr = f"range({start}, {end})"
        return f"for {name} in {range_expr}:" + "\n" + loop_body

    def for_iter(self, args):
        # for_iter: "for" "each" name name "in" name _NEWLINE block_stmt
        name = args[2]
        iterable = args[2]
        iter_body = args[3]
        return f"for {name} in {iterable}:" + "\n" + iter_body

    def repeat_stmt(self, args):
        # repeat_stmt: "repeat" _NEWLINE block_stmt "until" test _NEWLINE
        body = args[0]
        condition = args[1]
        return f"while not {condition}:" + "\n" + body

    def assign(self, args):
        lhs, rhs = args
        return f"{lhs} = {rhs}"

    def assign_expr(self, args):
        lhs, rhs = args
        return f"{lhs} = {rhs}"

    def comparison(self, args):
        # ?comparison: expr (_comp_op expr)*
        output: list[str] = []
        for idx, arg in enumerate(args):
            if idx % 2 == 0:
                output.append(arg)
            else:
                output.append(arg.value)
        return " ".join(output)


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
