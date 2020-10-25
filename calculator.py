# simple calculator with variables.
# -----------------------------------------------------------------------------

import ply.lex as lex
import ply.yacc as yacc


def finishProcessing(p, result): p[0] = result


tokens = (
    'NAME', 'INT', 'FLOAT',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
    'LPAREN', 'RPAREN', "IMAGINARY_NUMBER", "IMAGINARY_VARIABLE"
)

# Tokens

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NAME = r'[a-zA-Z][a-zA-Z0-9]*'


def t_IMAGINARY_VARIABLE(t):
    r'[A-Za-z][A-Za-z]*i'
    return t


def t_IMAGINARY_NUMBER(t):
    r'[-]?(\d*i)'
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
    ('right', 'UMINUS')
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
        elif(p[0] == '/'):
            return run(p[1]) / run(p[2])
        elif(p[0] == '='):
            enviroment[p[1]] = p[2]
            print(enviroment)
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
         | complex_expression
         | var_assign
         | empty
    '''
    result = run(p[1])
    print(result)


def processImaginary(productionRule):
    productionRuleLength = len(productionRule)
    isTuple = type(productionRule)
    productionIndex = 3 if productionRuleLength >= 4 else 1
    productionExpression = productionRule[productionIndex]
    imaginaryValue = float(productionExpression.replace('i', ''))
    real = run(productionRule) if isTuple else float(
        productionExpression if productionExpression else 0)
    return complex(real, imaginaryValue)


def p_complex_expression(p):
    '''
    complex_expression : expression PLUS IMAGINARY_NUMBER
                        | expression MINUS IMAGINARY_NUMBER
                        | expression TIMES IMAGINARY_NUMBER
                        | expression DIVIDE IMAGINARY_NUMBER
                        | IMAGINARY_NUMBER
    '''
    pLen = len(p)

    if(pLen >= 4):
        imaginary = float(p[3].replace('i', ''))
        real = run(p[1]) if type(p[1]) == tuple else float(p[1])
        p[0] = complex(real, imaginary)
    else:
        imaginary = float(p[1].replace('i', ''))
        p[0] = complex(0, imaginary)


def p_imaginary(production):
    '''
    imaginary : IMAGINARY_VARIABLE
    '''
    finishProcessing(production, production[1])


def p_complex_equation(production):
    'complex_expression : expression PLUS imaginary'
    imaginaryVariableName = production[3].replace('i', '')
    imaginaryVariableValue = enviroment[imaginaryVariableName]
    realVariableValue = run(production[1])

    result = complex(realVariableValue, imaginaryVariableValue)
    finishProcessing(production, result)


def p_var_assign(p):
    '''
    var_assign : NAME EQUALS expression
                | NAME EQUALS complex_expression
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


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]


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
# Variable bool
isRunning: bool = True

while isRunning:
    try:
        s = input('>> ')
    except EOFError:
        isRunning = False
    parser.parse(s)
