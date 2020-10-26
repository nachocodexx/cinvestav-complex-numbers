#
# Created on Sun Oct 25 2020
#
# CINVESTAV (c) 2020 Ignacio Castillo
#

# Importar lex de la libreria PLY
from ply import lex


'''
Description: Clase la cual contiene todo lo relacionado con lex
'''


class Lexer(object):

    '''
    # Lista de todos los tokens
    # [REQUIERED]
    #
    '''
    tokens = (
        'ID', 'INT', 'FLOAT',
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
        'LEFT_PARENTHESIS', 'RIGHT_PARENTHESIS', 'IMAGINARY_ID', 'IMAGINARY_VARIABLE',
        'EXIT'
    )
    t_PLUS = r'\+'
    '''
    # Expresion regular para el signo de resta:
    # token: MINUS
    '''
    t_MINUS = r'-'
    '''
    # Expresion regular para el signo de multiplicacion:
    # token: TIMES
    '''
    t_TIMES = r'\*'
    '''
    # Expresion regular para el signo de division:
    # token: DIVIDE
    '''
    t_DIVIDE = r'/'
    '''
    Description: Expresion regular para el signo de igualdad
    token: EQUALS
    '''
    t_EQUALS = r'='
    '''
    Description: Expresion regular para el parentesis izquierdo
    token: LEFT_PARENTHESIS
    '''
    t_LEFT_PARENTHESIS = r'\('
    '''
    Description: Expresion regular para el parentesis derecho
    token: RIGHT_PARENTHESIS
    '''
    t_RIGHT_PARENTHESIS = r'\)'
    '''
    Description: Expresion regular para las variables
    token: ID
    '''

    def t_ID(self, token):
        r'[a-zA-Z][a-zA-Z0-9]*'
        value = token.value
        if(value == 'i'):
            token.type = "IMAGINARY_ID"
        elif('i' in value and value[-1] == 'i'):
            token.value = value.replace('i', '')
            token.type = "IMAGINARY_VARIABLE"
        elif('exit' == value):
            token.type = "EXIT"
        return token
    '''
    Description: Expresion regular para las variables imaginarias
    token: IMAGINARY_ID
    '''
    # t_IMAGINARY_ID = r'[A-Za-z][A-Za-z]*i'
    t_IMAGINARY_ID = r'i'
    '''
    Description: Expresion regular para la parte imaginaria
    token: IMAGINARY_NUMBER
    '''
    '''
    Description: Token especial proporcionado por PLY para ignorar caracteres.
    '''
    t_ignore = " \t"

    '''
        Description: Metodo para realizar construir el lexer.
        type: (Map<String,Any>)=>Unit
    '''

    def build(self, **kwargs):
        self.lexer = lex.lex(object=self, **kwargs)

    '''
    Description: Expresion regular para detectar numeros flotantes (e.g 2.2 ,233.34234212)
    token: FLOAT
    '''

    def t_FLOAT(self, token):
        r'\d+\.\d+'
        token.value = float(token.value)
        return token

    '''
    Description: Expresion regular para detectar numeros enteros (e.g 23,5,6)
    token: INT
    '''

    def t_INT(self, token):
        r'\d+'
        # print(t)
        token.value = int(token.value)
        return token

    '''
    Description: contador de lineas
    '''

    def t_newline(self, token):
        r'\n+'
        token.lexer.lineno += token.value.count("\n")

    '''
    Description: Controlador de error, esta funcion se ejecuta cuando un caracter no es valido. 
    '''

    def t_error(self, token):
        print(f"Illegal character {token.value[0]!r}")
        # ignora el caracter
        token.lexer.skip(1)
