from lark import Tree, Token
from lark.visitors import Interpreter


class LineCountTranspiler(Interpreter):

    __indent_weight: int = 4

    __preamble: str = """
import pathlib
import sys
# add the source directory to sys.path. This is not a permanent solution
sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))
from pcc.backend.pc_stdlib import *
            """.strip() + "\n"

    def __init__(self):
        super().__init__()

    def transpile(self, tree: Tree) -> str:
        return self.visit(tree)

    def __line_marker(self, tree: Tree) -> str:
        return f" # l:{tree.meta.line} "

    def __default__(self, tree: Tree):
        print(f"Using default callback for {tree}")
        return tree

    def _indent_all_lines(self, lines: str) -> str:
        return "\n".join(map(lambda l: " " * self.__indent_weight + l, lines.split("\n")))

    def file_input(self, tree: Tree) -> str:
        print("FILE INPUT, line", tree.meta)
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
        return "\n".join(stmt) + "\n"

    def expr_stmt(self, tree: Tree) -> str:
        return str(self.visit(tree.children[0]))

    def assign_stmt(self, tree: Tree) -> str:
        return str(self.visit(tree.children[0]))

    def array_decl_stmt(self, tree: Tree) -> str:
        return str(self.visit(tree.children[0]))

    def array_init(self, tree: Tree) -> str:
        name, start, end = self.visit_children(tree)
        return f"{name} = PcArray({start}, {end})"

    def single_array_decl(self, tree: Tree) -> str:
        return str(tree.children[0]) + ";"

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
        condition, body = self.visit_children(tree)[:2]
        return f"if {condition}:" + f"{self.__line_marker(tree)}\n" + body

    def elifs(self, tree: Tree) -> str:
        return "\n".join(self.visit_children(tree))

    def elif_(self, tree: Tree) -> str:
        condition, body = self.visit_children(tree)
        return f"elif {condition}:" + f"{self.__line_marker(tree)}\n" + body

    def else_(self, tree: Tree) -> str:
        return self.visit(tree.children[0])

    def else_block(self, tree: Tree) -> str:
        return f"else:" + f"{self.__line_marker(tree)}\n" + self.visit(tree.children[0])

    def else_inline(self, tree: Tree) -> str:
        return f"else: {self.visit(tree.children[0])}"

    def while_stmt(self, tree: Tree) -> str:
        condition, body = self.visit_children(tree)
        return f"while {condition}:" + f"{self.__line_marker(tree)}\n" + body

    def for_stmt(self, tree: Tree) -> str:
        return self.visit(tree.children[0])

    # FIXME: Finish for loop impl
    def for_loop(self, tree: Tree) -> str:
        name, start, end, body = self.visit_children(tree)
        return f"for {name} in range({start}, {end}):" + f"{self.__line_marker(tree)}\n" + body

    def for_iter(self, tree: Tree) -> str:
        name, iterable, body = self.visit_children(tree)[-3:]
        return f"for {name} in {iterable}:" + f"{self.__line_marker(tree)}\n" + body

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
        for i in range(len(tree.children)):
            if i % 2 == 0: # operand
                output += self.visit(tree.children[i])
            else: # operator (Token)
                output += f" {tree.children[i].value} "
        return output

    def expr(self, tree: Tree) -> str:
        return self.visit(tree.children[0])

    """
    ?or_expr: xor_expr ("or" xor_expr)*
    ?xor_expr: and_expr ("xor" and_expr)*
    ?and_expr: shift_expr ("and" shift_expr)*
    ?shift_expr: arith_expr (_shift_op arith_expr)*
    ?arith_expr: term (_add_op term)*
    ?term: factor (_mul_op factor)*
    ?factor: _unary_op factor | power
    """

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

    def _unary_op(self, tree: Tree) -> str:
        return str(tree.children[0])

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

