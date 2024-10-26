from lark import Transformer

class Interpreter(Transformer):
    from operator import \
        add as addition, \
        sub as subtraction, \
        mul as multiplication, \
        truediv as division

    true = lambda _: True
    false = lambda _: False
    nil = lambda _: None

