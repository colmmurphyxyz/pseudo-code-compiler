from lark import Tree, Token
from lark.visitors import Interpreter

# pylint: disable=too-many-public-methods
class LineCountTranspiler(Interpreter):

    __indent_weight: int = 4

    __preamble: str = """
from backend.pc_stdlib import *
from debugger.web_db import set_trace
set_trace(\"input.pc\")
            """.strip()

    def __init__(self, source_code: str = None):
        super().__init__()
        preamble_lines = self.__preamble.splitlines()
        preamble_lines[-1] = f"set_trace(path=__file__, pc_source_code=\'\'\'{source_code}\'\'\')"
        self.__preamble = "\n".join(preamble_lines) + "\n"

    def transpile(self, tree: Tree) -> str:
        return self.__preamble + "\n" + self.visit(tree)

    def __line_marker(self, tree: Tree) -> str:
        return f" # l:{tree.meta.line} "

    def __default__(self, tree: Tree):
        print(f"Using default callback for {tree}")
        return tree

    def _indent_all_lines(self, lines: str) -> str:
        return "\n".join(map(lambda l: " " * self.__indent_weight + l, lines.split("\n")))

    def file_input(self, tree: Tree) -> str:
        return "\n".join(self.visit_children(tree)) + "\n"

    def funcdef(self, tree: Tree) -> str:
        func_name, parameters, body = self.visit_children(tree)
        # func_name: str = tree.children[0]
        # parameters = tree.children[1]
        # body: str = tree.children[2]
        return f"def {func_name}({parameters}):" + f"{self.__line_marker(tree)}\n" + body + "\n"

    def parameters(self, tree: Tree) -> str:
        return ", ".join(self.visit_children(tree))

    def simple_stmt(self, tree: Tree) -> str:
        stmt = []
        for child in tree.children:
            stmt.append(self.visit(child) + self.__line_marker(child))
        return "\n".join(stmt)

    def expr_stmt(self, tree: Tree) -> str:
        return str(self.visit(tree.children[0]))

    def assign_stmt(self, tree: Tree) -> str:
        return str(self.visit(tree.children[0]))

    def array_decl_stmt(self, tree: Tree) -> str:
        return self.visit(tree.children[0])

    def array_init(self, tree: Tree) -> str:
        name, start, end = self.visit_children(tree)
        return f"{name} = PcArray({start}, {end})"

    def single_array_decl(self, tree: Tree) -> str:
        return self.visit(tree.children[0]) + ";"

    def multiple_array_decl(self, tree: Tree) -> str:
        return "; ".join(self.visit_children(tree)) + ";"

    def return_stmt(self, tree: Tree) -> str:
        return f"return {self.visit(tree.children[0])}"

    def print_stmt(self, tree: Tree) -> str:
        return f"print({self.visit(tree.children[0])})"

    def error_stmt(self, tree: Tree) -> str:
        return f"error({self.visit(tree.children[0])})"

    def exchange_stmt(self, tree: Tree) -> str:
        lhs, rhs = self.visit_children(tree)
        return f"{lhs}, {rhs} = {rhs}, {lhs}"

    # FIXME: Finish implementation of if/else
    def if_stmt(self, tree: Tree) -> str:
        subtrees: list[str] = self.visit_children(tree)
        condition, body = subtrees[0], subtrees[1]
        return f"if {condition}:" + f"{self.__line_marker(tree)}\n" + body + "\n" + "\n".join(subtrees[2:])

    def elifs(self, tree: Tree) -> str:
        return "\n".join(self.visit_children(tree))

    def elif_(self, tree: Tree) -> str:
        condition, body = self.visit_children(tree)
        return f"elif {condition}:" + f"{self.__line_marker(tree)}\n" + body

    def else_(self, tree: Tree) -> str:
        return self.visit(tree.children[0])

    def else_block(self, tree: Tree) -> str:
        output = f"else: {self.__line_marker(tree)}\n" + self.visit(tree.children[0])
        if len(tree.children) > 1:
            block = self.visit(tree.children[1])
            output += f"{self.__line_marker(tree)}\n" + block

    def else_inline(self, tree: Tree) -> str:
        output = "else:\n"
        output += self._indent_all_lines(self.visit(tree.children[0])) + "\n"
        if len(tree.children) > 1:
            output += f"{self.visit(tree.children[1])}"
        return output

    def while_stmt(self, tree: Tree) -> str:
        condition, body = self.visit_children(tree)
        return f"while {condition}:" + f"{self.__line_marker(tree)}\n" + body

    def for_stmt(self, tree: Tree) -> str:
        return self.visit(tree.children[0])

    # FIXME: Finish for loop impl
    def for_loop(self, tree: Tree) -> str:
        name, start, range_op, end, body = self.visit_children(tree)
        range_expr: str
        match range_op:
            case "to":
                range_expr = f"range({start}, {end} + 1)"
            case "until":
                range_expr = f"range({start}, {end})"
            case "downto":
                range_expr = f"range({start}, {end} - 1, -1)"
            case _:
                range_expr = f"range({start}, {end})"
        return f"for {name} in {range_expr}:" + f"{self.__line_marker(tree)}\n" + body

    def for_iter(self, tree: Tree) -> str:
        name, iterable, body = self.visit_children(tree)[-3:]
        return f"for {name} in {iterable}:" + f"{self.__line_marker(tree)}\n" + body

    def range_op(self, tree: Tree) -> str:
        token: Token = tree.children[0]
        return str(token.value)

    def repeat_stmt(self, tree: Tree) -> str:
        body, condition = self.visit_children(tree)
        return f"while not {condition}:" + f"{self.__line_marker(tree)}\n" + body

    def block_stmt(self, tree: Tree) -> str:
        return self._indent_all_lines("\n".join(self.visit_children(tree)))

    def assign(self, tree: Tree) -> str:
        lhs, rhs = self.visit_children(tree)
        return f"{lhs} = {rhs}"

    def assign_expr(self, tree: Tree) -> str:
        return self.assign(tree)

    def comparison(self, tree: Tree) -> str:
        output: str = ""
        for i, child in enumerate(tree.children):
            if i % 2 == 0: # operand
                output += self.visit(child)
            else: # operator (Token)
                output += f" {child.value} "
        return output

    def expr(self, tree: Tree) -> str:
        return self.visit(tree.children[0])

    def or_expr(self, tree: Tree) -> str:
        return " or ".join(self.visit_children(tree))

    def xor_expr(self, tree: Tree) -> str:
        return " xor ".join(self.visit_children(tree))

    def and_expr(self, tree: Tree) -> str:
        return " and ".join(self.visit_children(tree))

    def shift_expr(self, tree: Tree) -> str:
        return " ".join(self.visit_children(tree))

    def arith_expr(self, tree: Tree) -> str:
        return " ".join(self.visit_children(tree))

    def term(self, tree: Tree) -> str:
        output = tree.children.copy()
        for i, child in enumerate(tree.children):
            if isinstance(child, Tree):
                output[i] = self.visit(child)
            else:
                match child.value:
                    case "mod": output[i] = "%"
                    case r"\\": output[i] = "//"
        return " ".join(output)

    def factor(self, tree: Tree) -> str:
        return " ".join(self.visit_children(tree))

    def power(self, tree: Tree) -> str:
        return " ".join(self.visit_children(tree))

    def funccall(self, tree: Tree) -> str:
        func_name, arguments = self.visit_children(tree)
        # arguments = list(map(lambda c: self.visit(c), tree.children[0].children[1:]))
        print("ARGUING", arguments)
        return f"{func_name}({arguments})"

    def getitem(self, tree: Tree) -> str:
        subject: str = self.visit(tree.children[0])
        value: str = self.visit(tree.children[1])
        return f"{subject}[{value}]"

    def getattr(self, tree: Tree) -> str:
        subject, value = self.children(tree)
        return f"{subject}.{value}"

    def arguments(self, tree: Tree) -> str:
        return ", ".join(self.visit_children(tree))

    def unary_op(self, tree: Tree) -> str:
        match str(tree.children[0]):
            case "+": return "+"
            case "-": return "-"
            case "!": return "not"

    def _add_op(self, tree: Tree) -> str:
        return str(tree.children[0])

    def _shift_op(self, tree: Tree) -> str:
        return str(tree.children[0])

    def _mul_op(self, tree: Tree) -> str:
        return str(tree.children[0])

    def _comp_op(self, tree: Tree) -> str:
        return str(tree.children[0])

    def _power_op(self, tree: Tree) -> str:
        return str(tree.children[0])

    def var(self, tree: Tree) -> str:
        return self.visit(tree.children[0])

    def number(self, tree: Tree) -> str:
        token: Token = tree.children[0]
        return token.value

    def string(self, tree: Tree) -> str:
        token: Token = tree.children[0]
        return token.value

    def __normalize_identifier(self, name: str) -> str:
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

    def name(self, tree: Tree) -> str:
        token: Token = tree.children[0]
        return self.__normalize_identifier(token.value)
