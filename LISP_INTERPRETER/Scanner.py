import ply.lex as lex


class Scanner(object):
    def build(self):
        self.lexer = lex.lex(object=self)

    def input(self, text):
        self.lexer.input(text)

    def token(self):
        return self.lexer.token()


    literals = "()=+-*/<>"
    reserved = {
        'if': 'IF',
        'define': 'DEF',
        'defun': 'DEFUN',
        'and': 'AND',
        'or': 'OR',
        'abs': 'ABS',
        'append': 'APPEND',
        'car': 'CAR',
        'cdr': 'CDR',
        'is_eq': 'ISEQ',
        'pow': 'POW',
        'len': 'LEN',
        'list': 'LIST',
        'max': 'MAX',
        'min': 'MIN',
        'not': 'NOT',
        'is_number': 'ISNUMBER',
        'round': 'ROUND'
    }
    t_EQ = r"=="
    t_NEQ = r"!="
    t_LE = r"<="
    t_GE = r">="

    tokens = ["EQ", "FLOAT", "GE", "ID", "INTEGER", "LE", "NEQ"] + list(reserved.values())

    def t_ID(self, t):
        r"[a-zA-Z_]\w*"
        t.type = Scanner.reserved.get(t.value, 'ID')
        return t

    def t_FLOAT(self, t):
        r"\d+(\.\d*)|\.\d+"
        t.value = float(t.value)
        return t

    def t_INTEGER(self, t):
        r"\d+"
        t.value = int(t.value)
        return t

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def error_handler(self, token):
        last_cr = self.lexer.lexdata.rfind('\n', 0, token.lexpos)
        if last_cr < 0:
            last_cr = 0
        return token.lexpos - last_cr

    t_ignore = ' \t\f'
