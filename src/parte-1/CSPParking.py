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
    dominio_para_enchufables = []
    for i in range(int(m)):
        for j in range(int(n)):
            if (i + 1, j + 1) in plazas_enchufables:
                dominio.append((i + 1, j + 1, True))
                dominio_para_enchufables.append((i + 1, j + 1, True))
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
    
    return dominio_para_enchufables, dominio, vehiculos

def restriccion_1(): ... # Es trivial

def restriccion_2(p1, p2): 
    if p1 != p2:
        return True
    else:
        return False
    
def restriccion_3(p1): ...

def restriccion_4(p1, p2): 
    if p2[1] < p1[1]:
        return True
    else:
        return False
    
def restriccion_5(p1, p2, p3):
    # Para cuando veas esto, Natalia: 
    # Siento mucho no haber comentado nada es que estoy muy cansado pero motivado al mismo tiempo 
    # porque está saliendo todo bastante bien 
    if p1[0] == 1 or p1[0] == 5: # Si está en una de las filas de los extremos...
        if (p2[0] - p1[0] == 1) or (p3[0] - p1[0] == -1):
            return False
        elif (p2[0] - p1[0] == -1) or (p3[0] - p1[0] == 1):
            return False
        else:
            return True
    else: 
        if (p2[0] - p1[0] == 1) and (p3[0] - p1[0] == -1):
            return False
        elif (p2[0] - p1[0] == -1) and (p3[0] - p1[0] == 1):
            return False
        else:
            return True


#BORRAR ANTES DE ENTREGAR
###############################################################################################################################
def imprimir_estacionamiento(solucion):
    # Definir las dimensiones totales del estacionamiento
    filas_totales = 5  # Cambiar según las filas totales de tu estacionamiento
    columnas_totales = 6  # Cambiar según las columnas totales de tu estacionamiento

    # Crear una matriz para representar el estacionamiento
    estacionamiento = [['    -   ' for _ in range(columnas_totales)] for _ in range(filas_totales)]

    # Llenar la matriz con la información de la solución
    for vehiculo, ubicacion in solucion.items():
        id_coche, tipo, congelador = vehiculo
        i, j, e = ubicacion
        estacionamiento[i - 1][j - 1] = f"{id_coche}({tipo}{'-C' if congelador else '-X'})"

    # Imprimir los índices de las columnas
    print("  ", end="")
    for idx in range(1, columnas_totales + 1):
        print(f"{idx: ^5}", end="")
    print("\n")

    # Imprimir el estacionamiento con los índices de las filas
    for i, fila in enumerate(estacionamiento, start=1):
        print(f"{i: <2}", end="")
        for celda in fila:
            print(f"| {celda: ^4}", end="")
        print("|")
###############################################################################################################################

if __name__ == "__main__":
    dom_enchufables, dominio, vehiculos = leer_fichero_de_entrada("src/parte-1/ejemplo.txt")
    print(dom_enchufables)
    print()
    print(dominio)

    problema = Problem()

    for v in vehiculos:
        if v[2] == True:
            problema.addVariable(v, dom_enchufables)
        else:
            problema.addVariable(v, dominio)

    # Segunda restricción
    for v1 in vehiculos:
        for v2 in vehiculos:
            if v1 != v2:
                problema.addConstraint(restriccion_2, (v1, v2))

    # cuarta restricción
    for v1 in vehiculos:
        if v1[1] == 'TSU':
            for v2 in vehiculos:
                if v2[1] == 'TNU': 
                    problema.addConstraint(restriccion_4, (v1, v2))
    
    # Quinta restricción
    """for v1 in vehiculos:
        for v2 in vehiculos:
            for v3 in vehiculos:
                if (v1 != v2) and (v1 != v3) and (v2 != v3):
                    problema.addConstraint(restriccion_5, (v1, v2, v3))"""
    


    a = problema.getSolution()
    imprimir_estacionamiento(a)
