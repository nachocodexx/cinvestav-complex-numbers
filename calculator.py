# simple calculator with variables.
# -----------------------------------------------------------------------------

import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'NAME', 'INT', 'FLOAT',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
    'LPAREN', 'RPAREN', "IMAGINARY_NUMBER"
)

# Tokens

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'


def t_IMAGINARY_NUMBER(t):
    r'(\d+i)'
    print(t.value)
    t.value = float(t.value.replace('i', ''))
    return t


def t_FLOAT(t):
    r'(\d+\.\d+)'
    t.value = float(t.value)
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)


# Build the lexer
lex.lex()
# Precedence rules for the arithmetic operators
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# dictionary of enviroment variable (for storing variables)
enviroment = {}


def run(p):
    if(type(p) == tuple):
        if(p[0] == "+"):
            return run(p[1]) + run(p[2])
        elif(p[0] == "-"):
            return run(p[1]) - run(p[2])
        elif(p[0] == "*"):
            return run(p[1]) * run(p[2])
        elif(p[0] == '='):
            enviroment[p[1]] = p[2]
            return ''
        else:
            if p[1] in enviroment:
                return enviroment[p[1]]
            else:
                print("{} not found".format(p[1]))
                return 0

    else:
        return p


def p_calc(p):
    '''
    calc : expression 
         | var_assign
         | empty
    '''
    result = run(p[1])
    print(result)


def p_var_assign(p):
    '''
    var_assign : NAME EQUALS expression
                | NAME EQUALS NAME
    '''
    p[0] = ('=', p[1], p[3])


def p_expression(p):
    '''
    expression : expression DIVIDE expression
                | expression TIMES expression
                | expression PLUS expression
                | expression MINUS expression 
    '''

    p[0] = (p[2], p[1], p[3])


def p_expression_var(p):
    '''
    expression : NAME
    '''
    p[0] = ("var", p[1])


def p_expression_int_float(p):
    '''
    expression : INT 
              | FLOAT 
    '''
    p[0] = p[1]


def p_empty(p):
    '''
    empty :
    '''
    p[0] = None


def p_error(p):
    print("Syntax error found :c...")
    return


# Yacc
parser = yacc.yacc()
while True:
    try:
        s = input('>> ')
    except EOFError:
        break
    parser.parse(s)
