import math
import operator as op


Symbol = str
Number = (int, float)
Atom = (Symbol, Number)
List = list
Exp = (Atom, List)


class Env(dict):  # local variables + global in outer_Env
    def __init__(self, key=(), val=(), out_Env: dict = None):
        super().__init__()
        self.update(zip(key, val))
        self.out_Env = out_Env

    def find(self, x):
        if x in self:
            return self[x]
        if self.out_Env and x in self.out_Env:
            return self.out_Env[x]
        return None


class Scanner:
    @staticmethod
    def scan(A: str) -> Exp:
        scanned = _scan(_tokenize(A))
        return scanned


def _tokenize(A: str) -> list:
    return A.replace('(', ' ( ').replace(')', ' ) ').split()  # add spaces between parentisies


def _scan(tokens: list) -> Exp:
    if len(tokens) == 0:
        print("NO TOKENS GIVEN TO _scan")
        return []
    token = tokens.pop(0)
    if token == '(':
        Tree = []
        while tokens[0] != ')':
            Tree.append(_scan(tokens))
        tokens.pop(0)  # pop ')'
        return Tree
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        # for example: (+ (+ 2 3) 3), it is obvious what atom is
        return _atom(token)


def _atom(token: str) -> Atom:
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


class EnvironmentBuilder:
    @staticmethod
    def build_env() -> Env:
        Map = Env()
        Map.update({'+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv, 'abs': op.abs,
                    'expt': pow, 'sqrt': math.sqrt})  # arythmetical operations
        Map.update({'>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq})  # equality operations
        Map.update({'or': op.or_, 'and': op.and_, 'not': op.not_})  # boolean operations
        Map.update({'append': op.add, 'apply': lambda fun, array: fun(*array), 'begin': lambda *x: x[-1],
                    'car': lambda x: x[0], 'cdr': lambda x: x[1:], 'eq?': op.is_, 'equal?': op.eq,
                    'length': len, 'max': max, 'min': min, 'map': map, 'null?': lambda x: x == [],
                    'list?': lambda x: isinstance(x, List),
                    'number?': lambda x: isinstance(x, Number), 'print': print,
                    'round': round, 'list': lambda *x: List(x),
                    'procedure?': callable,
                    'symbol?': lambda x: isinstance(x, Symbol), 'cons': lambda x, y: [x] + y
                    })  # list operations & others
        return Map


class Lambda(object):
    def __init__(self, variables, function_body, env: Env):
        self.variables = variables
        self.function_body = function_body
        self.env = env

    def __call__(self, *args):  # args are arugments, it is like a function call
        return Parser.parse(self.function_body, Env(self.variables, args, self.env))


class Parser:
    @staticmethod
    def parse(expression: Exp, environment: Env):
        try:
            if isinstance(expression, Symbol):  # if is string, return string
                return environment.find(expression)
            elif isinstance(expression, Number):
                return expression
            elif expression[0] == 'if':
                (_, condition, if_true, if_false) = expression
                exp = (if_true if Parser.parse(condition,
                                               environment) else if_false)  # Parser.parse(condition, environment) will return true or false based on parse result
                return Parser.parse(exp, environment)
            elif expression[0] == 'define':  # definition
                (_, variable, exp) = expression
                environment[variable] = Parser.parse(exp, environment)  # appending new environment variable
            elif expression[0] == 'lambda':
                (_, arguments, function_body) = expression
                return Lambda(arguments, function_body, environment)
            else:  # procedure call
                proc = Parser.parse(expression[0], environment)
                args = [Parser.parse(arg, environment) for arg in expression[1:]]
                return proc(*args)
        except:
            print("Eror while proccesing -> " + str(expression))
