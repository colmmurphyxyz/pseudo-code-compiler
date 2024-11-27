# pylint: disable=unused-argument
from lark import Transformer, Tree, Token


class Transpiler(Transformer):  # pylint: disable=too-many-public-methods

    __indent_weight: int = 4

    __preamble: str = """
import pathlib
import sys
# add the source directory to sys.path. This is not a permanent solution
sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))
from src.backend.pc_stdlib import *
        """ + "\n"

    def __default__(self, data, children, meta):
        print(f"Using default callback for {data}")
        return data

    def _indent_all_lines(self, lines: str) -> str:
        return "\n".join(map(lambda l: " " * self.__indent_weight + l, lines.split("\n")))

    def file_input(self, args) -> str:
        return self.__preamble + "\n".join(args) + "\n"

    def single_input(self, args) -> str:
        return "\n".join(args) + "\n"

    def funcdef(self, args) -> str:
        func_name: str = args[0]
        parameters = args[1]
        body: str = args[2]
        return f"def {func_name}({parameters}):" + "\n" + body + "\n"

    def parameters(self, args) -> str:
        return ", ".join(args)

    def expr_stmt(self, args) -> str:
        return str(args[0])

    def error_stmt(self, args) -> str:
        """
        Stub Implementation
        :return: sys.exit(1)
        """
        return "import sys; sys.exit(1)"

    def assign_stmt(self, args) -> str:
        return str(args[0])

    def print_stmt(self, args) -> str:
        return f"print({"".join(args)})"

    def while_stmt(self, args) -> str:
        while_condition: Tree = args[0]
        while_body: str = args[1]
        return f"while {self.transform(while_condition)}:" + "\n" + while_body

    def block_stmt(self, args) -> str:
        return self._indent_all_lines("\n".join(args))

    def exchange_stmt(self, args) -> str:
        lhs, rhs = args[0], args[1]
        return f"{lhs}, {rhs} = {rhs}, {lhs}"

    # FIXME: 'else' branches are not transpiled correctly
    def if_stmt(self, args) -> str:
        print("IF STMT", "\n".join([ str(a) for a in args ]) )
        if_condition = args[0]
        if_body = args[1]
        # return f"if {self.transform(if_condition)}:" + "\n" + if_body + "\n" + "\n".join(args[2:])
        return f"if {if_condition}:" + "\n" + if_body + "\n".join(args[2:])


    def elifs(self, args):
        return "\n".join(args)

    def elif_(self, args):
        elif_condition = args[0]
        elif_body = args[1]
        return f"elif {self.transform(elif_condition)}:" + "\n" + elif_body

    def else_(self, args) -> str:
        return str(args[0])

    def else_block(self, args) -> str:
        return "else:\n" + str(args[0])

    def else_inline(self, args) -> str:
        result: str = "else:\n" + self._indent_all_lines(str(args[0]))
        if len(args) > 1:
            block = str(args[1])
            result += "\n" + block
        return result

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

    def range_op(self, args) -> str:
        return str(args[0])

    def assign(self, args):
        lhs, rhs = args
        return f"{lhs} = {rhs}"

    def assign_expr(self, args):
        lhs, rhs = args
        return f"{lhs} = {rhs}"

    def array_decl_stmt(self, args) -> str:
        return str(args[0])

    def array_init(self, args) -> str:
        name, start, end = args
        print(f"{type(name)=} {type(start)=} {type(end)=}")
        print("Array init")
        print(" # ".join(args))
        return f"{name} = PcArray({start}, {end})"

    def single_array_decl(self, args) -> str:
        array_init: str = args[0]
        return array_init + ";"

    def multiple_array_decl(self, args) -> str:
        return "; ".join(args) + ";"

    def test(self, args) -> str:
        return str(args[0])

    def comparison(self, args):
        # ?comparison: expr (_comp_op expr)*
        output: list[str] = []
        for idx, arg in enumerate(args):
            if idx % 2 == 0:
                output.append(arg)
            else:
                output.append(arg.value)
        return " ".join(output)

    def expr(self, args) -> str:
        return args[0]

    def or_expr(self, args) -> str:
        return " or ".join(args)

    def xor_expr(self, args) -> str:
        return " xor ".join(args)

    def and_expr(self, args) -> str:
        return " and ".join(args)

    def shift_expr(self, args) -> str:
        return " ".join(args)

    def arith_expr(self, args) -> str:
        return " ".join(args)

    def term(self, args) -> str:
        for idx, arg in enumerate(args):
            if isinstance(arg, str):
                match arg:
                    case "mod": args[idx] = "%"
                    case r"\\": args[idx] = "//"
        return " ".join(args)

    def factor(self, args) -> str:
        return " ".join(args)

    def power(self, args) -> str:
        return " ".join(args)

    def _unary_op(self, args) -> str:
        return str(args[0])

    def _add_op(self, args) -> str:
        return str(args[0])

    def _shift_op(self, args) -> str:
        return str(args[0])

    def _mul_op(self, args) -> str:
        return str(args[0])

    def _comp_op(self, args) -> str:
        return str(args[0])

    def _power_op(self, args) -> str:
        return str(args[0])

    def atom_expr(self, args) -> str:
        return str(args[0])

    def funccall(self, args) -> str:
        func_name = args[0]
        func_arguments = args[1]
        return f"{func_name}({func_arguments})"

    def getitem(self, args) -> str:
        return f"{args[0]}[{args[1]}]"

    def getattr(self, args) -> str:
        return f"{args[0]}.{args[1]}"

    def grouping(self, args) -> str:
        return f"({"".join(args)})"

    def arguments(self, args) -> str:
        return ", ".join(args)

    def var(self, args) -> str:
        return str(args[0])

    def _normalize_identifier(self, name: str) -> str:
        normalized: str = (
            name
            .replace("-", "_")
            .replace("$", "")
            .replace("{", "")
            .replace("}", "")
            .replace("^", "")
            .replace("\\", "")
        )
        if normalized[0].isdigit():
            return "_" + normalized
        return normalized

    def name(self, args: list[Token]) -> str:
        return self._normalize_identifier(str(args[0].value))

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
