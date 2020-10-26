#
# Created on Sun Oct 25 2020
#
# CINVESTAV (c) 2020 Ignacio Castillo
#

import sys
import os
# Importar yacc de la libreria PLY
import ply.yacc as yacc
# TermColor
from termcolor import colored, cprint
# Importar todos los tokens
from lexer import Lexer
#
# Importar base de datos en memoria
from database import Database
# Importar el Parser.
from parser import Parser


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
        parser.parse(inputValue)


# Condicional para ejecutar la funcion program(), si main.py es ejecutado.
if __name__ == '__main__':
    # Ejecutar programa
    program()
