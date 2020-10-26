#
# Created on Sun Oct 25 2020
#
# CINVESTAV (c) 2020 Ignacio Castillo
#
'''
Description: Clase la cual proporciona una api simple para acceder para obtener las variables. 
'''


class Database(object):

    # Constructor inicializa el objeto vacio
    def __init__(self):
        self.db = {}

    # Verifica si existe una variable en el diccionario
    def exists(self, variableName):
        return variableName in self.db

    # Obtiene todas las variables.
    def getVariables(self):
        return self.db

    # Busca una variable por nombre.
    def getVariable(self, variableName: str):
        return self.db[variableName]

    # Actualiza el valor de una variable.
    def updateVariable(self, variableName: str, value):
        self.db[variableName] = value
        return
