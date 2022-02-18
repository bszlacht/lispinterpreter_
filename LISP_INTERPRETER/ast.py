class Node(object):
    def __init__(self):
        pass


class Define(Node):
    def __init__(self, variable, expression):
        super().__init__()
        self.variable = variable
        self.expression = expression
        self.children = [expression]


class ListOp(Node):
    def __init__(self, L):
        super().__init__()
        self.L = L
        self.children = L


class Single(Node):
    def __init__(self, op, expression):
        super().__init__()
        self.op = op
        self.expression = expression
        self.children = [expression]


class Variable(Node):
    def __init__(self, identifier):
        super().__init__()
        self.identifier = identifier
        self.children = []


class IfElse(Node):
    def __init__(self, condition, if_true, if_false):
        super().__init__()
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false
        self.children = [condition, if_true]
        if if_false is not None:
            self.children += [if_false]


class Number(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.children = []


class BinaryExpression(Node):
    def __init__(self, op, left, right):
        super().__init__()
        self.op = op
        self.left = left
        self.right = right
        self.children = [left, right]


class ComparisonExpression(BinaryExpression):
    def __init__(self, op, left, right):
        super().__init__(op, left, right)
        self.op = op
        self.left = left
        self.right = right
        self.children = [left, right]


class AndOrExpresion(BinaryExpression):
    def __init__(self, op, left, right):
        super().__init__(op, left, right)
        self.op = op
        self.left = left
        self.right = right
        self.children = [left, right]


class ArithmeticExpression(BinaryExpression):
    def __init__(self, op, left, right):
        super().__init__(op, left, right)
        self.op = op
        self.left = left
        self.right = right
        self.children = [left, right]


class DefunExpression(Node):
    def __init__(self, name, variables, fun_body):
        super().__init__()
        self.identifier = name
        self.variables = variables
        self.fun_body = fun_body
        self.children = [variables, fun_body]


class Funcall(Node):
    def __init__(self, name, variables):
        super().__init__()
        self.identifier = name
        self.variables = variables
        self.children = variables


class ListOperators(Node):
    def __init__(self, op, L):
        super().__init__()
        self.op = op
        self.L = L
        self.children = L


class ListAppend(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.children = [left, right]
