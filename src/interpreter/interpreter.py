from functools import reduce

from lark import Tree, Token
from lark.visitors import Interpreter

from .stack import Stack


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
        child: Token = tree.children[0]
        if child.type == "DEC_INTEGER":
            return int(child)
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

    def _divide(self, lhs, rhs):
        if isinstance(lhs, int) and isinstance(rhs, int) == int:
            return lhs // rhs
        return lhs

    def _evaluate_arithmetic_expression(self, tree: Tree):
        def evaluate_shift_expression(c: Tree | Token) -> int | float | str:
            if isinstance(c, Tree):
                return self.visit(c)
            if isinstance(c, Token):
                return c.value
            raise ValueError(f"Incompatible type {c.type} of expression {c}")
        children = list(map(
            lambda c: evaluate_shift_expression(c),
            tree.children)
        )

        stack = Stack()
        for child in reversed(children):
            if isinstance(child, float):
                child = int(child)
            if not (isinstance(child, (int, str))):
                raise TypeError(f"Incompatible type {type(child)} of value {child}") # pylint: disable=unidiomatic-typecheck
            stack.push(child)

        # evaluate
        while stack.size() > 1:
            lhs, op, rhs = stack.pop_next(3)
            result: int
            match op:
                case "+": result = lhs + rhs
                case "-": result = lhs - rhs
                case "<<": result = lhs << rhs
                case ">>": result = lhs >> rhs
                case "*": result = lhs * rhs
                case "/": result = lhs / rhs
                case "mod": result = lhs % rhs
                case "\\\\": result = lhs // rhs
                case "**": result = lhs ** rhs
                case _: result = lhs << rhs
            stack.push(result)
        return stack.pop()

    def shift_expr(self, tree: Tree):
        return self._evaluate_arithmetic_expression(tree)

    def arith_expr(self, tree: Tree):
        return self._evaluate_arithmetic_expression(tree)

    def term(self, tree: Tree):
        return self._evaluate_arithmetic_expression(tree)

    def factor(self, tree: Tree):
        unary_op: str = tree.children[0].value
        operand = tree.children[1]
        match unary_op:
            case "+": return self.visit(operand)
            case "-": return -1 * self.visit(operand)
            case _: raise NotImplementedError()



    def power(self, tree: Tree):
        return self._evaluate_arithmetic_expression(tree)

    def grouping(self, tree: Tree):
        return self.visit(tree.children[0])


    const_true = lambda self, _: True
    const_false = lambda self, _: False
    const_nil = lambda self, _: None
