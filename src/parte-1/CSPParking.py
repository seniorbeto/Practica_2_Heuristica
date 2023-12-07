# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Autores:
#       Alberto Penas Díaz
#       Natalia Rodríguez Navarro
#

import os
import csv
import sys
from constraint import *


class Parte1:
    def __init__(self, fichero) -> None:

        self.filas = None
        self.columnas = None
        self.csv = None

        dom_enchufables, dominio, vehiculos = self.leer_fichero_de_entrada(fichero)

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
                    problema.addConstraint(self.restriccion_2, (v1, v2))

        # cuarta restricción
        for v1 in vehiculos:
            if v1[1] == 'TSU':
                for v2 in vehiculos:
                    if v2[1] == 'TNU': 
                        problema.addConstraint(self.restriccion_4, (v1, v2))
        
        # Quinta restricción
        for v1 in vehiculos:
            for v2 in vehiculos:
                for v3 in vehiculos:
                    if (v1 != v2) and (v1 != v3) and (v2 != v3):
                        problema.addConstraint(self.restriccion_5, (v1, v2, v3))
        


        a = problema.getSolution()
        
        self.agregar_solucion_a_csv(a)

    def leer_fichero_de_entrada(self, file: str) -> tuple:
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

        # Generamos el archivo .csv
        # Para ello, necesitamos primero obtener el nombre del archivo
        partes_ruta = file.split(os.path.sep)
        nombre_archivo_con_extension = partes_ruta[-1]
        nombre_archivo_sin_extension = nombre_archivo_con_extension.split('.')[0]
        self.csv = nombre_archivo_sin_extension
        
        self.filas = int(fichero[0]) # m = número de filas
        self.columnas = int(fichero[2]) # n = número de columnas

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
        for i in range(self.filas):
            for j in range(self.columnas):
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
    
    def agregar_solucion_a_csv(self, solucion):
        # Definir las dimensiones totales del estacionamiento
        filas_totales = self.filas  # Cambiar según las filas totales de tu estacionamiento
        columnas_totales = self.columnas  # Cambiar según las columnas totales de tu estacionamiento

        # Crear una matriz para representar el estacionamiento
        estacionamiento = [['-' for _ in range(columnas_totales)] for _ in range(filas_totales)]

        # Llenar la matriz con la información de la solución
        for vehiculo, ubicacion in solucion.items():
            id_coche, tipo, congelador = vehiculo
            i, j, enchufe = ubicacion
            estacionamiento[i - 1][j - 1] = f"{id_coche}-{tipo}{'-C' if congelador else '-X'}"

        # Escribir la matriz al archivo CSV
        with open(self.csv + '.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([])  # Agregar una fila vacía para separar soluciones
            for fila in estacionamiento:
                writer.writerow(fila)

    def restriccion_1(self):
        """
        Todo vehículo tiene que tener asignada una plaza y sólo una.
        """
        pass

    def restriccion_2(self, p1, p2):
        """
        Dos vehículos distintos, como es natural, no pueden ocupar la misma plaza.
        """
        if p1 != p2:
            return True
        else:
            return False
        
    def restriccion_3(self, p1):
        """
        Los vehículos provistos de congelador sólo pueden ocupar plazas con conexión a la red eléctrica.
        """
        pass

    def restriccion_4(self, p1, p2):
        """
        Un vehículo de tipo TSU no puede tener aparcado por delante, en su misma fila, a ningún otro vehículo
        excepto si éste es también de tipo TSU. Por ejemplo, si un TSU está aparcado en la plaza 2.3 no podrá
        haber aparcado un TNU en las plazas 2.4, 2.5, 2.6...
        """
        if p1[0] == p2[0]:
            if p2[1] < p1[1]:
                return True
            else:
                return False
        else:
            return True
        
    def restriccion_5(self, p1, p2, p3):
        """
        Por cuestiones de maniobrabilidad dentro del parking todo vehículo debe tener libre una plaza a izquierda
        o derecha (mirando en dirección a la salida). Por ejemplo, si un vehículo ocupa la plaza 3.3 no podrá tener
        aparcado un vehículo en la 2.3 y otro en la 4.3, al menos una de esas dos plazas deberá quedar libre.
        """
        # Para cuando veas esto, Natalia: 
        # Siento mucho no haber comentado nada es que estoy muy cansado pero motivado al mismo tiempo 
        # porque está saliendo todo bastante bien 
        if p1[0] == 1 or p1[0] == self.filas:
            if (p2[0] - p1[0] == 1 and p2[1] == p1[1]) or (p3[0] - p1[0] == -1 and p3[1] == p1[1]):
                return False
            elif (p2[0] - p1[0] == -1 and p2[1] == p1[1]) or (p3[0] - p1[0] == 1 and p3[1] == p1[1]):
                return False
            else:
                return True
        else:
            if (p2[0] - p1[0] == 1 and p2[1] == p1[1]) and (p3[0] - p1[0] == -1 and p3[1] == p1[1]):
                return False
            elif (p2[0] - p1[0] == -1 and p2[1] == p1[1]) and (p3[0] - p1[0] == 1 and p3[1] == p1[1]):
                return False
            else:
                return True


#BORRAR ANTES DE ENTREGAR
###############################################################################################################################
    def imprimir_estacionamiento(self, solucion):
        if solucion is None:
            print("EL PROBLEMA NO TIENE SOLUCIÓN")
            return
        # Definir las dimensiones totales del estacionamiento
        filas_totales = self.filas  # Cambiar según las filas totales de tu estacionamiento
        columnas_totales = self.columnas  # Cambiar según las columnas totales de tu estacionamiento

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
    
    if len(sys.argv) < 2:
        raise ValueError("Es necesario especificar un archivo como argumento")
    
    Parte1(sys.argv[1])
