from functools import reduce

from lark import Tree, Token
from lark.visitors import Interpreter

from stack import Stack


class PcInterpreter(Interpreter):
    def single_input(self, tree: Tree):
        return self.visit(tree.children[0])

    def file_input(self, tree: Tree):
        for child in tree.children:
            self.visit(child)

    def print_stmt(self, tree: Tree):
        body = self.visit(tree.children[0])
        print(body)

    def number(self, tree: Tree):
        print("Number", tree.children[0])
        return float(tree.children[0])

    # MARK: Arithmetic Expressions
    def or_expr(self, tree: Tree):
        operands = list(map(lambda c: self.visit(c), tree.children))
        return reduce(lambda x, y: x or y, operands)

    def xor_expr(self, tree: Tree):
        operands = list(map(lambda c: self.visit(c), tree.children))
        return reduce(lambda x, y: x ^ y, operands)

    def and_expr(self, tree: Tree):
        operands = list(map(lambda c: self.visit(c), tree.children))
        return reduce(lambda x, y: x and y, operands)

    def shift_expr(self, tree: Tree):
        def evaluate_shift_expression(c: Tree | Token) -> int | str:
            if isinstance(c, Tree):
                return int(self.visit(c))
            elif isinstance(c, Token):
                return c.value
            else:
                raise ValueError(f"Incompatible type {c.type} of expression {c}")
        children = list(map(
            lambda c: evaluate_shift_expression(c),
            tree.children)
        )
        stack = Stack()
        for child in reversed(children):
            if type(child) == float: child = int(child)
            if type(child) != int and type(child) != str:
                raise TypeError(f"Incompatible type {type(child)} of value {child}")
            stack.push(child)
        # evaluate
        while stack.size() > 1:
            lhs, op, rhs = stack.pop_next(3)
            result: int
            match op:
                case "<<": result = lhs << rhs
                case ">>": result = lhs >> rhs
                case _: result = lhs << rhs
            stack.push(result)

        return stack.pop()


    const_true = lambda self, _: True
    const_false = lambda self, _: False
    const_nil = lambda self, _: None

