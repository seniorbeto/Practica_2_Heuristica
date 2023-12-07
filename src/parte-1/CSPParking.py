# !/usr/bin/env python3
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

        # Del fichero de entrada establecemos las variables vehículo (id, tipo, congelador),
        # su dominio, que son las plazas de parking (i, j, e) y el dominio que tendrá un 
        # vehículo con congelador (solo plazas enchufables, (i, j, e=True))
        # Primera restricción: Dos vehículos tiene que tener asignada una plaza y solo una
        dom_enchufables, dominio, vehiculos = self.leer_fichero_de_entrada(fichero)

        self.problema = Problem()
        
        # DOMINIOS:

        # Tercera restricción: Los vehículos con congelador solo pueden ocupar plazas eléctricas
        self.restriccion_3(vehiculos, dom_enchufables, dominio)

        # RESTRICCIONES:

        # Segunda restricción: Dos vehículos distintos no pueden ocupar la misma plaza
        self.problema.addConstraint(AllDifferentConstraint(), vehiculos)

        # Cuarta restricción: Un TSU no puede tener por delante un TNU
        for v1 in vehiculos:
            if v1[1] == 'TSU':
                for v2 in vehiculos:
                    if v2[1] == 'TNU': 
                        self.problema.addConstraint(self.restriccion_4, (v1, v2))

        
        # Quinta restricción: Todo vehículo debe tener una plaza libre a dcha o izq
        for v1 in vehiculos:
            for v2 in vehiculos:
                for v3 in vehiculos:
                    if (v1 != v2) and (v1 != v3) and (v2 != v3):
                        self.problema.addConstraint(self.restriccion_5, (v1, v2, v3))
        


        primera_sol = self.problema.getSolution()
        
        #self.agregar_solucion_a_csv(a)
        self.imprimir_estacionamiento(primera_sol)



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

        with open(file, mode="r") as f:
            fichero = f.read()

        # Obtenemos nombre del archivo de entrada para definir el nombre
        # del archivo de salida (tiene que ser el mismo)
        partes_ruta = file.split(os.path.sep)
        nombre_archivo_con_extension = partes_ruta[-1]
        nombre_archivo_sin_extension = nombre_archivo_con_extension.split('.')[0]
        self.csv = nombre_archivo_sin_extension
        
        i = 0
        m = ''
        # Leemos filas (hasta encontrar una "x")
        while fichero[i] != 'x':
            # Si el número de filas no es un entero, error
            try:
                int(fichero[i])  
            except TypeError:
                raise ValueError("El número de filas del parking debe ser un entero.")
            
            m += fichero[i]
            i += 1
        i+=1

        self.filas = int(m) # m = número de filas

        n = ''
        # Leemos columnas (hasta encontrar un "/n")
        while fichero[i] != '\n': 
            # Si el número de columnas no es un entero, error
            try:
                int(fichero[i])  
            except ValueError:
                raise ValueError("El número de columnas del parking debe ser un entero.")
            n += fichero[i]
            i += 1
        i += 1

        self.columnas = int(n) # n = número de columnas

        fichero = fichero[i:] # Movemos el puntero del fichero a la siguiente línea

        # Comprobamos el formato de declaración de plazas eléctricas
        comprobacion_def_pe = fichero[:3]
        if comprobacion_def_pe != 'PE:':
            raise ValueError("Las plazas eléctricas han de estar especificadas con el siguiente\n \
                              formato: 'PE:(i,j)(i',j') ...'")
        
        i = 3 # Movemos el puntero a la primera plaza enchufable

        # Ahora, estableceremos una lista con las plazas con enchufe
        plazas_enchufables = []
        while fichero[i] != '\n':
            # Si no se sigue el formato (i,j)(i',j')..., error
            # Comprobación '('
            if fichero[i] != '(': 
                raise ValueError("Para la declaración de las plazas, se ha de seguir el siguiente\n \
                                 formato: (i,j)(i',j')(i'',j'')...")
            i += 1
            
            # Comprobación 'i' = fila de la plaza y de ','
            i_pe = ''
            while fichero[i] != ',':
                try:
                    int(fichero[i])  
                except ValueError:
                    raise ValueError("Las filas de las plazas enchufables del parking deben de ser enteros\n \
                                     seguidos de una coma ','.")
                i_pe += fichero[i]
                i += 1
            i += 1

            i_pe = int(i_pe)

            # Comprobación 'j' = columna de la plaza y de ')'
            j_pe = ''
            while fichero[i] != ')':
                try:
                    int(fichero[i])  
                except ValueError:
                    raise ValueError("Las columnas de las plazas enchufables del parking deben de ser enteros\n \
                                     seguidos de un final de paréntesis ')'.")
                j_pe += fichero[i]
                i += 1
            i += 1
            
            j_pe = int(j_pe)

            # Si las plazas enchufables no están dentro del dominio (filas), error
            if (i_pe > self.filas) or (i_pe < 1) or (j_pe > self.columnas) or (j_pe < 1):
                raise ValueError(f"Las plazas enchufables deben estar dentro de la matriz de \
                                 dimensiones {self.filas}x{self.columnas}.")
            else:
                plaza = (i_pe, j_pe)

            plazas_enchufables.append(plaza)


        i += 1
        fichero = fichero[i:] # Movemos el puntero a la siguiente línea (def. vehículos)

        # Establecemos los dominios
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
 
                if len(partes) != 3:
                    raise ValueError("El formato de definición de los vehículos debe ser \n \
                                     ID(int)-TIPO(TSU o TNU)-CONGELADOR(C o X).")   

                try:
                    id_vehiculo = int(partes[0])
                except ValueError:
                    raise ValueError("El ID del vehículo debe de ser un entero.")

                if partes[1] != 'TSU' and partes[1] != 'TNU':
                    raise ValueError("El tipo de vehículo debe ser 'TSU' o 'TNU'.")
                else:
                    tipo_vehiculo = partes[1]
                
                if partes[2] != 'C' and partes[2] != 'X':
                    raise ValueError("Para especificar si un vehículo tiene congelador o no, es necesario \n \
                                     especificarlo con una 'C' (si tiene) o con una 'X' (si no).")
                else:
                    congelador = partes[2] == 'C'


                vehiculo = (id_vehiculo, tipo_vehiculo, congelador)
                vehiculos.append(vehiculo)

        # Primera restricción: La id debe ser única (dos vehículos únicamente
        # ocupan una plaza)
        self.restriccion_1(vehiculos)
        
        return dominio_para_enchufables, dominio, vehiculos
    

    def restriccion_1(self, vehiculos):
        """
        Todo vehículo tiene que tener asignada una plaza y sólo una. Es decir, como
        el dominio de una variable solo asigna una plaza, es necesario que dos vehículos
        NO TENGAN la misma ID.
        """
        ids = []
        for v in vehiculos: 
            if v[0] not in ids:
                ids.append(v[0])
            else:
                raise ValueError("Los vehículos han de tener ID's únicas.")

    def restriccion_3(self, vehiculos, dom_enchufables, dominio):
        """
        Los vehículos provistos de congelador sólo pueden ocupar plazas con conexión a la red eléctrica.
        """

        # Por arco-consistencia, reduciremos el dominino de todas aquellas variables
        # que tengan congelador (id, tipo, c=True), ya que solamente podrán posicionarse 
        # en aquellas plazas con enchufe disponible. El resto de vehículos podrán estar 
        # en cualquier plaza (tenga enchufe o no).
        for v in vehiculos:
            if v[2] == True:
                self.problema.addVariable(v, dom_enchufables)
            else:
                self.problema.addVariable(v, dominio)

    def restriccion_4(self, p1, p2):
        """
        Un vehículo de tipo TSU no puede tener aparcado por delante, en su misma fila, a ningún otro vehículo
        excepto si éste es también de tipo TSU. Por ejemplo, si un TSU está aparcado en la plaza 2.3 no podrá
        haber aparcado un TNU en las plazas 2.4, 2.5, 2.6...
        """

        # Si están están en la misma fila
        if p1[0] == p2[0]:
            # Si v2 (TNU) está por detrás de v1 (TSU)
            if p2[1] < p1[1]:
                return True
            # Si v2 (TNU) está por delante de v1 (TSU)
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
        
        # Para cuando el vehículo está en un borde, es decir, pegado a la pared dcha o izq
        # (i=p[0]=1, j=p[1], e) o (i=p[0]=m=filas, j, e)
        if p1[0] == 1 or p1[0] == self.filas:
            # Si v2 está a la dcha de v1 (j2 = j1, misma columna) OR v3 está a la izq de v1 (j3 = j1, misma columna)
            if (p2[0] - p1[0] == 1 and p2[1] == p1[1]) or (p3[0] - p1[0] == -1 and p3[1] == p1[1]):
                return False
            else:
                return True
        # Para cuando el vehículo NO está en un borde, es decir, no está pegado a la pared dcha o izq
        # (i=p[0], j=p[1])
        else:
            # Si v2 está a la dcha de v1 (j2 = j1, misma columna) AND v3 está a la izq de v1 (j3 = j1, misma columna)
            if (p2[0] - p1[0] == 1 and p2[1] == p1[1]) and (p3[0] - p1[0] == -1 and p3[1] == p1[1]):
                return False
            else:
                return True




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
