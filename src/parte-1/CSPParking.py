# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Autores:
#       Alberto Penas Díaz
#       Natalia Rodríguez Navarro
#

from constraint import *


def leer_fichero_de_entrada(file: str) -> tuple:
    """
    Esta función sirve para descomponer el fichero de entrada del problema.
    Es absolutamente necesario que el fichero de entrada siga exactamente el formato que se especifica en el 
    enunciado de la práctica, como por ejemplo:
        5x6
        PE:(1,1)(1,2)(2,1)(4,1)(5,1)(5,2)
        1-TSU-C
        2-TNU-X
        3-TNU-X
        4-TNU-C
        5-TSU-X
        6-TNU-X
        7-TNU-C
        8-TSU-C
    
    Esta función devuelve una tupla con dos valores:
        1. Una lista con todos los posibles valores pertenecientes al dominio del problema
        2. Una lista con los vehículos (variables principales) del problema 
    """
    # Abrimos el fichero de entrada (esto abrá que hacerlo bien en el futuro
    # ya que el programa se tiene que ejecutar con el comando pythonCSPParking.py<pathparking>
    # desde la terminal)
    with open(file, mode="r") as f:
        fichero = f.read()
    
    m = fichero[0] # m = número de filas
    n = fichero[2] # n = número de columnas

    fichero = fichero[4:] # Eliminamos del fichero los 4 primeros caracteres (incluimos el \n)
    
    # Ahora, estableceremos una lista con las plazas con enchufe
    plazas_enchufables = []
    i = 0
    while fichero[i] != '\n':
        try:
            numero = int(fichero[i])
            plaza = int(fichero[i]), int(fichero[i+2])
            plazas_enchufables.append(plaza)
            i += 2
        except ValueError:
            pass

        i += 1
    
    fichero = fichero[i+1:] # Eliminamos del fichero los caracteres que especificaban las plazas enchufables

    dominio = []
    for i in range(int(m)):
        for j in range(int(n)):
            if (i + 1, j + 1) in plazas_enchufables:
                dominio.append((i + 1, j + 1, True))
            else:
                dominio.append((i + 1, j + 1, False))
    
    # Establecemos ahora los vehículos del fichero
    vehiculos = []
    lineas = fichero.split('\n') # Separamos el fichero por 'intros'

    for linea in lineas:
        if linea: 
            partes = linea.split('-')
            id_vehiculo = int(partes[0])
            tipo_vehiculo = partes[1]
            congelador = partes[2] == 'C'

            vehiculo = (id_vehiculo, tipo_vehiculo, congelador)
            vehiculos.append(vehiculo)
    
    return dominio, vehiculos

def restriccion_1(): ...
def restriccion_2(v1, v2): 
    if v1 != v2:
        return True
    else:
        return False
def restriccion_3(): ...
def restriccion_4(): ...
def restriccion_5(): ...


if __name__ == "__main__":
    dominio, vehiculos = leer_fichero_de_entrada("src/parte-1/ejemplo.txt")

    problema = Problem()

    problema.addVariables(vehiculos, dominio)

    for v1 in vehiculos:
        for v2 in vehiculos:
            if v1 != v2:
                problema.addConstraint(restriccion_2, (v1, v2))

    a = problema.getSolution()
    print(a)
