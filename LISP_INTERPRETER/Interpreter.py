from visit import on, when
import sys
from MemoryStack import MemoryStack, Memory
import ast

sys.setrecursionlimit(9999)


# dictionary like implementation
class Interpreter(object):
    def __init__(self):
        self.stack = MemoryStack()

    def interpret(self, node):
        self.stack.push(Memory("global"))
        res = self.visit(node)
        return res

    @on('node')
    def visit(self, node):
        pass

    @when(ast.Define)
    def visit(self, node):
        variable = node.variable
        expression = node.expression
        self.stack.set(variable, expression)
        return

    @when(ast.ListOp)
    def visit(self, node):
        L = node.L
        res = []
        for i in range(len(L)):
            res.append(self.visit(L[i]))
        return res

    @when(ast.Single)
    def visit(self, node):
        op = node.op
        expression = node.expression
        if op == 'abs':
            return abs(expression)
        elif op == 'round':
            return round(expression)
        elif op == 'is_number':
            if isinstance(expression, int) or isinstance(expression, float):
                return True
            else:
                return False
        elif op == 'not':
            return not expression

    @when(ast.Variable)
    def visit(self, node):
        res = self.stack.get(node.identifier)
        if res is None:
            return node.identifier
        if isinstance(res, ast.Variable):
            return res.identifier
        if isinstance(res, ast.DefunExpression):
            return res.fun_body
        if isinstance(res, ast.Number):
            return res.value
        if isinstance(res, int) or isinstance(res, float):
            return res
        if isinstance(res, list):
            return res
        res = self.visit(res)
        return res

    @when(ast.IfElse)
    def visit(self, node):
        r = None
        condition = self.visit(node.condition)
        self.stack.push(Memory("IFELSE"))
        if condition:
            r = self.visit(node.if_true)
        elif node.if_false:
            r = self.visit(node.if_false)
        self.stack.pop()
        return r

    @when(ast.Number)
    def visit(self, node):
        res = node.value
        return res

    @when(ast.ComparisonExpression)
    def visit(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        res = None

        if node.op == '<':
            res = left_val < right_val
        elif node.op == '<=':
            res = left_val <= right_val
        elif node.op == '==':
            res = left_val == right_val
        elif node.op == '!=':
            res = left_val != right_val
        elif node.op == '>':
            res = left_val > right_val
        elif node.op == '>=':
            res = left_val >= right_val
        elif node.op == 'is_eq':
            if left_val is right_val:
                res = True
            else:
                res = False
        if res:
            return 1
        return 0

    @when(ast.AndOrExpresion)
    def visit(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        res = None
        if right_val >= 1:
            right_val = True
        else:
            right_val = False
        if left_val >= 1:
            left_val = True
        else:
            left_val = False
        if node.op == 'and':
            res = left_val and right_val
        elif node.op == 'or':
            res = left_val or right_val

        if res:
            return 1
        return 0

    @when(ast.ArithmeticExpression)
    def visit(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        if node.op == '+':
            return left_val + right_val
        elif node.op == '-':
            return left_val - right_val
        elif node.op == '*':
            return left_val * right_val
        elif node.op == '/':
            return left_val / right_val
        elif node.op == '%':
            return left_val % right_val
        return None

    @when(ast.DefunExpression)
    def visit(self, node):
        self.stack.set(node.identifier, node)
        return

    @when(ast.Funcall)
    def visit(self, node):
        res = None
        identifier = node.identifier
        variables = node.variables
        fun = self.stack.get(identifier)
        if isinstance(fun, ast.DefunExpression):
            fun_identifier = fun.identifier
            fun_variables = fun.variables
            fun_body = fun.fun_body
            if len(fun_variables) != len(variables):
                print("WRONG NUM OF ARGS")
                return None
            self.stack.push(Memory("local"))
            for i in range(len(fun_variables)):
                self.stack.set(fun_variables[i].identifier, variables[i].value)
            res = self.visit(fun_body)
            self.stack.pop()
        return res

    @when(ast.ListOperators)
    def visit(self, node):
        op = node.op
        L = node.L
        print(L)
        if isinstance(L, ast.Variable):
            L_val = self.stack.get(L.identifier)
            if isinstance(L_val, ast.ListOp):
                L = L_val.L # list
                tmp_list = []
                for elem in L:
                    tmp_list.append(elem)
                if op == 'min':
                    return min(tmp_list)
                elif op == 'max':
                    return max(tmp_list)
                elif op == 'car':
                    return tmp_list[0]
                elif op == 'cdr':
                    return tmp_list[len(tmp_list) - 1]
                elif op == 'len':
                    return len(tmp_list)
            else:
                print("ELEM IS NOT LIST")
                return None
        elif isinstance(L, ast.ListOp):
            L = L.L
            tmp_list = []
            for elem in L:
                tmp_list.append(elem.value)
            if op == 'min':
                return min(tmp_list)
            elif op == 'max':
                return max(tmp_list)
            elif op == 'car':
                return tmp_list[0]
            elif op == 'cdr':
                return tmp_list[len(tmp_list) - 1]
            elif op == 'len':
                return len(tmp_list)
        else:
            print("ELEM IS NOT LIST")
            return None
        return None

    @when(ast.ListAppend)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        res = None
        if isinstance(right, list) and isinstance(left, list):
            return left + right
        return res
