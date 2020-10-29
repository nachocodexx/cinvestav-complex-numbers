#
# Created on Sun Oct 25 2020
#
# CINVESTAV (c) 2020 Ignacio Castillo
#


import sys
# Importar Yacc
from ply import yacc
# Importa el lexer
from lexer import Lexer
# Importar termcolor: libreria para cambiar el color de texto en la terminal
from termcolor import cprint, colored
from random import randint


'''
Description: Clase analizador gramatico, se encarga de encapsular toda la funcionalidad de Yacc.
'''


class Parser(object):
    # Traer los tokens del Lexer
    tokens = Lexer.tokens

    # Tupla de precedencia
    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'UMINUS')
    )

    # Regla de produccion principal
    def p_calc(self, production):
        '''calc :   complex_expression
                  | var_assign
                  | operations 
                  | printer
                  | exit_case
                 | empty
        '''
        # Contador de lineas
        self.line_counter += 1
        result = self.processProduction(production[1])
        printeVariable = self.line_counter
        if(type(result) == complex):
            self.db.updateVariable('res{}'.format(self.line_counter), result)
            printeVariable = "res{}".format(self.line_counter)

        cprint("[{1}] {0}".format(
            result, printeVariable), "white", "on_blue")
        return production

    # Production rule para las operaciones con variables.
    def p_operations(self, production):
        '''
        operations :  complex_term PLUS complex_term
                    | complex_term MINUS complex_term
                    | complex_term TIMES complex_term
                    | complex_term DIVIDE complex_term
        '''
        production[0] = (production[2], ('var', production[1]),
                         ('var', production[3]))
        return production

    def p_operations_times(self, production):
        '''
        operations : complex_term complex_term
        '''
        production[0] = ('*', ('var', production[1]), ('var', production[2]))
        return production

    def p_complex_term_id(self, production):
        '''
        complex_term : ID
        '''
        production[0] = production[1]
        return production

    def p_complex_term_group(self, production):
        '''
        complex_term : LEFT_PARENTHESIS complex_expression RIGHT_PARENTHESIS
        '''
        variableName = 'HIDDEN_VARIABLE' + str(randint(0, 10000))
        self.db.updateVariable(variableName, production[2])
        production[0] = variableName

        return production

    # Production rule para los numeros complejos,(e.g 2+1i , a+2i, 1+ai , a+bi)

    def p_complex_expression(self, production):
        '''
        complex_expression :  real_expression PLUS term IMAGINARY_ID
                           | real_expression PLUS complex_variable
        '''

        real = self.processProduction(production[1])
        imaginary = production[3]
        complexNumber = complex(real, imaginary)
        production[0] = complexNumber
        return production

    def p_complex_expression_negative(self, production):
        '''
        complex_expression : real_expression MINUS complex_variable
        '''

        real = self.processProduction(production[1])
        imaginary = production[3]
        complexNumber = complex(real, -imaginary)
        production[0] = complexNumber
        return production

    # production rule para detectar numeros complejos con variable en la parte imaginaria (e.g 1+bi)
    def p_complex_expression_variable(self, production):
        '''
        complex_variable :  IMAGINARY_VARIABLE
        '''
        production[0] = self.db.getVariable(production[1])
        return production

    #  Production rule para detectar expresiones negativas.
    def p_negative_complex_expression(self, production):
        '''
        complex_expression : real_expression MINUS term IMAGINARY_ID
        '''
        production[0] = complex(production[1], -production[3])
        return production

    # Production rule para detectar numeros complejos sin parte real y negativos.
    def p_negative_complex_number(self, production):
        '''
        complex_expression : MINUS term IMAGINARY_ID
        '''
        production[0] = complex(0, -production[2])
        return production

    # Production rule para detectar numeros complejos sin parte real y positivos
    def p_positive_complex_number(self, production):
        '''
        complex_expression :  term IMAGINARY_ID
                            | PLUS term IMAGINARY_ID
        '''
        imaginaryValue = production[2] if len(
            production) == 4 else production[1]
        production[0] = complex(0, imaginaryValue)
        return production

    # Production rule para detectar terminos enteros o flotantes.
    def p_term_int_float(self, production):
        '''
        term : INT 
            | FLOAT
        '''
        production[0] = production[1]
        return production

    # Production rule para detectar un numero en la parte real, entero o flotante.
    def p_real_expression_int_float(self, production):
        '''
        real_expression : INT 
                        | FLOAT
        '''
        production[0] = production[1]
        return production

    # Productio rule para detectar variables en la parte real.
    def p_real_expression_id(self, production):
        '''
        real_expression : ID
        '''
        production[0] = ('var', production[1])
        return production

    # Production rule para la asignacion, de numeros o de numeros complejos.
    def p_var_assign(self, production):
        '''
        var_assign : ID EQUALS real_expression
                    | ID EQUALS complex_expression
        '''
        production[0] = ('=', production[1], production[3])
        return production

    # Production rule, imprime el valor de la variable.
    def p_print_id_value(self, production):
        '''
        printer : ID 
        '''
        variable = production[1]
        if not self.db.exists(variable):
            cprint("[ERROR] Cannot find {}".format(
                variable), "white", "on_red")
            return None
        production[0] = self.db.getVariable(variable)
        return production

    def p_empty(self, production):
        '''
        empty :
        '''
        production[0] = None
        return production

    def p_term_uminus(self, production):
        'real_expression : MINUS term %prec UMINUS'
        production[0] = -production[2]
        return production

    def p_exit_case(self, production):
        '''
        exit_case : EXIT
        '''
        sys.exit()
    # ##########################################################

    '''
    # Funcion que se ejecutado cuando el analizador detecta un  error.
    # type: LexToken => Unit
    #
    '''

    def p_error(self, token):
        cprint("[SYNTAX_ERROR] found in {}".format(token), 'white', 'on_red')
        return

    '''
    Description: Constructor de la clase Parser, el cual construye el lexer, recibe por parametro una in-memory database :p.
    '''

    def __init__(self, db):
        self.lexer = Lexer()
        self.lexer.build()
        self.db = db
        self.line_counter = 0
        self.parser = yacc.yacc(module=self)

    '''
    Description: Metodo para realizar un analisis del texto que se pasa por parametro.
    type: String=>Unit
    '''

    def parse(self, input: str):
        self.parser.parse(input)

    '''
    Description: Procesa la tupla de produccion la cual se recibe por parametro en los metodos de cada production rule,
    la tupla que recibe es un arbol binario, el cual se evalua de forma recursiva en in-order. ejemplo si recibe ('+',1,2) ,
    el primer valor de la tupla sera el nodo padre, y los siguientes indices seran los nodos adyacentes.
    type: Tuple[..N] => Int|String|ComplexNumber
    '''

    def processProduction(self, production: tuple):
        if(type(production) == tuple):
            if(production[0] == "+"):
                # print("SUMA")
                return self.processProduction(production[1]) + self.processProduction(production[2])
            elif(production[0] == "-"):
                return self.processProduction(production[1]) - self.processProduction(production[2])
            elif(production[0] == "*"):
                return self.processProduction(production[1]) * self.processProduction(production[2])
            elif(production[0] == '/'):
                try:
                    return self.processProduction(production[1]) / self.processProduction(production[2])
                except ZeroDivisionError as e:
                    cprint("[ERROR] Complex division by zero",
                           "white", "on_red")
                    return None
                    # return "Complex division by zero"
            elif(production[0] == '='):
                variableName = production[1]
                value = production[2]
                upsertValue = {variableName: value}
                self.db.updateVariable(variableName, value)
                return '{}'.format(variableName)
            else:
                if self.db.exists(production[1]):
                    return self.db.getVariable(production[1])

                else:
                    cprint("[ERROR] Cannot find {}".format(
                        production[1]), "white", "on_red")
                    return 0

        else:
            return production

    # Metodo para ver el contenido de la tupla de produccion, solo util para el desarrollo.
    def printProduction(self, production):
        for i, v in enumerate(production):
            print("{0}: {1}".format(i, v))
