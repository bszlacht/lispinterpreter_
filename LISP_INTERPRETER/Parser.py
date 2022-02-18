from Scanner import Scanner
import ast


class Parser(object):

    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens

    def p_start(self, p):
        '''
        S : '(' expression ')'
        '''
        p[0] = p[2]

    def p_arithmetical_operators(self, p):
        '''
        expression  : '+' factor expression
                    | '-' factor expression
                    | '*' factor expression
                    | '/' factor expression
                    | POW factor expression
        '''
        p[0] = ast.ArithmeticExpression(p[1], p[2], p[3])

    def p_comparison_operators(self, p):
        '''
        expression  : '<' factor factor
                    | '>' factor factor
                    | EQ factor factor
                    | NEQ factor factor
                    | LE factor factor
                    | GE factor factor
                    | ISEQ factor factor
        '''
        p[0] = ast.ComparisonExpression(p[1], p[2], p[3])

    def p_boolean_operators(self, p):
        '''
        expression  : AND factor factor
                    | OR factor factor
        '''
        p[0] = ast.AndOrExpresion(p[1], p[2], p[3])

    def p_single_operators(self, p):
        '''
        expression  : ABS factor
                    | ROUND factor
                    | ISNUMBER factor
                    | NOT factor
        '''
        p[0] = ast.Single(p[1], p[2])

    def p_define_operators(self, p):
        '''
        expression  : DEF ID expression
        '''
        p[0] = ast.Define(p[2], p[3])

    def p_if_operators(self, p):
        '''
        expression  : IF '(' expression ')' '(' expression ')' '(' expression ')'
        '''
        p[0] = ast.IfElse(p[3], p[6], p[9])

    def p_list_operators(self, p):
        '''
        expression  : LIST '(' list_prod ')'
        '''
        p[0] = ast.ListOp(p[3])

    def p_defun_operators(self, p):
        '''
        expression  : DEFUN '(' name ')' '(' variables ')' '(' fun_body ')'
        '''
        p[0] = ast.DefunExpression(p[3], p[6], p[9])

    def p_funcall_operators(self, p):
        '''
        expression : ID '(' list_prod ')'
        '''
        p[0] = ast.Funcall(p[1], p[3])

    def p_name_expression(self, p):
        '''
        name    : ID
        '''
        p[0] = p[1]

    def p_variables_expression(self, p):
        '''
        variables   : list_prod
        '''
        p[0] = p[1]

    def p_fun_body_expression(self, p):
        '''
        fun_body    : expression
        '''
        p[0] = p[1]

    def p_expression_factor_operators(self, p):
        '''
        expression  : factor
        '''
        p[0] = p[1]

    def p_listop_operators(self, p):
        '''
        expression  : MIN listy
                    | MAX listy
                    | CAR listy
                    | CDR listy
                    | LEN listy
                    | APPEND listy listy
        '''
        if len(p) == 4:
            p[0] = ast.ListAppend(p[2], p[3])
        else:
            p[0] = ast.ListOperators(p[1], p[2])

    def p_lister_operators(self, p):
        '''
        listy   : ID
                | LIST '(' list_prod ')'
        '''
        if len(p) == 5:
            p[0] = ast.ListOp(p[3])
        else:
            p[0] = ast.Variable(p[1])

    def p_list_prod_operators(self, p):
        '''
        list_prod   : factor
                    | list_prod factor
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 3:
            p[0] = p[1] + [p[2]]

    def p_factor_ID(self, p):
        '''
        factor  : ID
        '''
        p[0] = ast.Variable(p[1])

    def p_factor_num(self, p):
        '''
        factor      : INTEGER
                    | FLOAT
                    | '-' INTEGER
                    | '-' FLOAT
                    | '(' expression ')'
        '''
        if len(p) == 2:
            p[0] = ast.Number(p[1])
        elif len(p) == 3:
            p[0] = ast.Number(-p[2])
        elif len(p) == 4:
            p[0] = p[2]

    def p_error(self, p):
        if p:
            print(
                "Syntax error at column {0}: LexToken({1}, '{2}')".format(self.scanner.error_handler(p), p.type, p.value))
        else:
            print('ERROR p_error')
