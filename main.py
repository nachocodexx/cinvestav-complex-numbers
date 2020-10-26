#
# Created on Sun Oct 25 2020
#
# CINVESTAV (c) 2020 Ignacio Castillo
#

# from production_rules import *
import sys
import os
# Importar yacc de la libreria PLY
import ply.yacc as yacc
# TermColor
from termcolor import colored, cprint
# Importar todos los tokens
from lexer import Lexer
#
# Importar base de datos en memoria: tinydb
from database import Database
#
# from process_production import buildProductionProcess
#
from parser import Parser
#
#
# processProduction = buildProductionProcess(db, cprint)

'''
#  Funcion para terminar un shift/reduce
# (Production, Any)=> Unit
#
'''
def finishProcessing(p, result): p[0] = result


# Build the lexer
# lexer = Lexer()
# lexer.build()

#

# Precedence rules for the arithmetic operators


#
# Funcion principal del programa
# type: ()=>Unit
#
def program():
    # LR Parser : Analizador de izquierda a derecha
    # parser: LRParser = yacc.yacc()
    db = Database()
    parser = Parser(db)
    # variable de control del main loop(ciclo principal)
    isRunning: bool = True

    # Main loop
    while isRunning:
        try:
            # Operacion I/O : Para recibir valores del teclado..
            inputValue: str = input('>> ')

        except EOFError:
            isRunning = False
        #  Analizar los datos que se reciben del teclado.
        # parser.parser.parse(s)
        parser.parse(inputValue)


# Condicional para ejecutar la funcion program(), si main.py es ejecutado.
if __name__ == '__main__':
    # Ejecutar programa
    program()
