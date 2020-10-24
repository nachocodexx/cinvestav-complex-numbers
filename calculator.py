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

# dictionary of names (for storing variables)
names = {}


def p_calc(p):
    '''
    calc : expression 
         | empty
    '''
    print(p[1])


def p_expression(p):
    '''
    expression : expression PLUS expression
                | expression MINUS expression 
    '''
    operation = p[2]
    if(operation == "+"):
        p[0] = p[1] + p[3]
    elif(operation == "-"):
        p[0] = p[1] - p[3]


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


# Yacc
parser = yacc.yacc()
while True:
    try:
        s = input('>> ')
    except EOFError:
        break
    parser.parse(s)
