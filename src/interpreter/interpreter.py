from functools import reduce

from lark import Tree, Token
from lark.visitors import Interpreter

from .stack import Stack
from .environment import Environment


class PcInterpreter(Interpreter):
    _environment: Environment

    def __init__(self):
        super().__init__()
        self._environment = Environment()

    def single_input(self, tree: Tree):
        return self.visit(tree.children[0])

    def file_input(self, tree: Tree):
        for child in tree.children:
            self.visit(child)

    def print_stmt(self, tree: Tree):
        body = self.visit(tree.children[0])
        print(body)

    def simple_stmt(self, tree: Tree):
        # simple_stmt may have multiple child statements, separated by a semicolon
        self.visit_children(tree)

    def block_stmt(self, tree: Tree):
        previous = self._environment
        try:
            self._environment = Environment(enclosing_environment=previous)
            self.visit_children(tree)
        finally:
            self._environment = previous

    # MARK: Flow Statements

    def if_stmt(self, tree):
        print(f"If has {len(tree.children)} kiddies")
        [ print(c) for c in tree.children ]
        condition = self.visit(tree.children[0])
        if condition:
            return self.visit(tree.children[1])
        for child in tree.children[1:]:
            if child.data == "elif_":
                condition = self.visit(child.children[0])
                if condition:
                    return self.visit(child.children[1])
        if len(tree.children) > 2:
            return self.visit(tree.children[2])



    # def elifs(self, tree: Tree) -> bool:
    #     for child in tree.children:
    #         condition = self.visit(child.children[0])
    #         if condition:
    #             self.visit(child.children[1])
    #             return True
    #     return False

    def number(self, tree: Tree):
        child: Token = tree.children[0]
        if child.type == "DEC_INTEGER":
            return int(child)
        return float(tree.children[0])

    # MARK: Comparisons
    def comparison(self, tree: Tree):
        return self._evaluate_arithmetic_expression(tree)

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
        def parse_binary_expression(c: Tree | Token) -> int | float | str | bool:
            if isinstance(c, Tree):
                return self.visit(c)
            if isinstance(c, Token):
                return c.value
            raise ValueError(f"Incompatible type {c.type} of expression {c}")
        children = list(map(
            lambda c: parse_binary_expression(c),
            tree.children)
        )

        stack = Stack()
        for child in reversed(children):
            if isinstance(child, float):
                child = int(child)
            if not (isinstance(child, (int, str, bool))):
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
                case "<": result = lhs < rhs
                case "<=": result = lhs <= rhs
                case "==": result = lhs == rhs
                case "!=": result = lhs != rhs
                case ">=": result = lhs >= rhs
                case ">": result = lhs > rhs
                case "in": result = lhs in rhs
                case "not in": result = lhs not in rhs
                case "is": result = lhs == rhs
                case "is not": result = lhs != rhs
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

    def assign_stmt(self, tree: Tree):
        print("assign_stmt")
        self.visit_children(tree)
        return

    def assign(self, tree: Tree):
        print("assign")

    def assign_expr(self, tree: Tree):
        lhs: Tree = tree.children[0]
        rhs: Tree = tree.children[-1]
        var_name = lhs.children[0].value
        var_value = self.visit(rhs)
        self._environment.define(var_name, var_value)

    def var(self, tree: Tree):
        var_name: str = tree.children[0].children[0].value
        return self._environment.get(var_name)


    const_true = lambda self, _: True
    const_false = lambda self, _: False
    const_nil = lambda self, _: None
