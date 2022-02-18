from Parser import Parser
import ply.yacc as yacc
from Interpreter import Interpreter

if __name__ == '__main__':
    # todo kolumn error
    parser = Parser()
    pars = yacc.yacc(module=parser)
    interpret = Interpreter()
    while 1:
        data = input("LISP: ")
        ast = pars.parse(data, lexer=parser.scanner)
        res = interpret.interpret(ast)
        if res is not None:
            print(str(res))