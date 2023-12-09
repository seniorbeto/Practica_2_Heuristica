# !/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   Autores:
#       Alberto Penas Díaz
#       Natalia Rodríguez Navarro
#


import csv
import sys

class Parte2:

    def __init__(self, mapa: csv, num_h: str):
        """
        Recibe un mapa.sv con toda la información sobre la ubicación de los apcientes,
        centros de atención, parkings, etc. Y resuelve el problema con el algorítmo A*
        y la heurística indicada (1, 2 o 3). Se creará el fichero con la solución del
        problema y el fichero de estadísticas.
        """
        # Si la heurística no es un entero, error
        try:
            num_h = int(num_h)
        except:
            raise ValueError("\n"+'\033[91m'+"El número de heurísitca a utilizar debe ser un entero" + '\033[0m')

        # Si la heurística no está entre 1 y 3, error
        if (num_h <= 0) or (num_h > 3):
            raise ValueError("\n"+'\033[91m'+"Es necesario especificar una heurísitca entre 1 y 3 (incluidos)" + '\033[0m')

        # Primero obtenemos el mapa como una matriz
        self.mapa = self.leer_fichero_de_entrada(mapa, num_h)

        # Definimos número de filas y columnas
        self.num_filas = len(self.mapa)
        self.num_columnas = len(self.mapa[0])

        # Obtenemos el número de celda del parking para establecer el estado inicial
        i = 0
        while i < self.num_filas:
            j = 0
            while j < self.num_columnas:
                if self.mapa[i][j] == "P":
                    self.pos_parking = (i+1, j+1)
                    break
                j+=1
            i+=1

        # Estado inicial ((i, j), energía, num_C, num_N)
        self.estado = (self.pos_parking, 50, 0, 0)

        # Resolvemos problema mediante A* con la heurística indicada
        if self.AStar(num_h):
            print("\n"+'\033[32m'+"EL PROBLEMA TIENE SOLUCIÓN REPRESENTADA EN " + self.ruta_output +
                  "\n\n" + "CUYAS ESTADÍSTICAS SE ENCUENTRAN EN " + self.ruta_stat + '\033[0m')
        else:
            print("\n"+'\033[93m'+"EL PROBLEMA NO TIENE SOLUCIÓN" + '\033[0m')


    def leer_fichero_de_entrada(self, mapa: str, num_h: int) -> list:
        """
        Esta función sirve para descomponer el .csv de entrada del problema. Es 
        absolutamente necesario que el fichero de entrada siga exactamente el formato 
        que se especifica en el enunciado de la práctica, como por ejemplo:
            N;1;1;1;1;1;1;1;N;1
            1;C;1;X;X;X;1;1;1;C
            1;1;X;2;2;1;N;1;2;2
            1;1;X;2;CC;1;1;1;CN;2
            1;1;X;2;2;2;2;2;2;2
            1;1;X;1;1;1;N;1;1;C
            N;X;X;X;X;X;1;N;1;1
            1;N;1;P;1;1;1;1;1;1
            1;N;1;1;1;1;N;1;N;1
            1;1;1;1;1;1;1;1;1;N
        
        Esta función devuelve una matriz (tupla de tuplas) con exactamente la misma
        información representada en el fichero.
        """

        # Obtenemos la ruta del archivo de entrada para definir el directorio
        # del archivo de salida (tiene que ser el mismo)
        ruta_salidas = mapa[:-4]
        # Nombre y ruta de los archivos de salida
        self.ruta_output = ruta_salidas + "-" + str(num_h) + ".output"
        self.ruta_stat = ruta_salidas + "-" + str(num_h) + ".stat"

        matriz = []
        
        try:
            with open(mapa, newline='') as csvfile:
                mapa_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for row in mapa_reader:
                    # TODO comprobar que en el fromato entrada hay ";"
                    celdas = row[0].split(";")
                    # TODO comprobar que entrada es int, N, C, CC, CN o P
                    matriz.append(celdas)
        except:
            raise ValueError("\n"+'\033[91m'+"Es necesario especificar una ruta válida como argumento" + '\033[0m')

        return matriz
    
    # OPERADORES:

    def MoverDcha(self) -> tuple or False:
        """
        Devuelve una tupla con el estado que se generaría al aplicar el operador o
        False si no es posible aplicarlo desde el estado actual. Este operador representa
        un movimiento en horizontal a la derecha.
        """
        # Estado actual: ((i, j), energía, num_C, num_N)
        # Extraemos la información para un código más limpio
        i_celda_actual = self.estado[0][0]
        j_celda_actual = self.estado[0][1]
        energia_actual = self.estado[1]
        num_C = self.estado[2]
        num_N = self.estado[3]
        
        # Si estamos en un borde derecho no podemos realizar dicha operación
        # j != num_columnas
        if j_celda_actual != self.num_columnas:
            # Obtenemos la celda siguiente y comprobamos si es transitable
            celda_derecha = self.mapa[i_celda_actual][j_celda_actual+1]
            # (i, j+1) != "X"
            if  celda_derecha != "X":
                # Si es transitable obtenemos su coste para comprobar si el
                # autobús tiene suficiente energía para transitar a ella
                # Además, comprobamos is podemos recoger o dejar paientes
                if (celda_derecha == "P"):
                    coste_dcha = 1
                elif (celda_derecha == "N"):
                    # Si no hay pacientes C y queda hueco se puede recoger al N
                    # (c=0) y (n<10)
                    if (num_C == 0) and (num_N < 10):
                        num_N_dcha = num_N + 1
                    coste_dcha = 1
                elif (celda_derecha == "C"):
                    # Si hay espacio y ningún paciente N sentado en un sitio de
                    # C's, se puede recoger al C
                    if (num_C < 2) and (num_N <= 8):
                        num_C_dcha = num_C + 1
                    coste_dcha = 1
                elif (celda_derecha == "CN"):
                    # Si no tenemos C's y tenemos N's, los dejamos. Si no, los 
                    # C's deben ser dejados los primeros
                    if (num_C == 0) and (num_N > 0):
                        num_N_dcha = 0
                    coste_dcha = 1
                elif (celda_derecha == "CC"):
                    # Si tenemos C's los dejamos
                    if (num_C > 0):
                        num_C_dcha = 0
                    coste_dcha = 1
                else:
                    coste_dcha = int(celda_derecha)
                # e > Coste celda derecha
                if energia_actual > coste_dcha:
                    # Actualizamos energía 
                    energia_dcha = energia_actual - coste_dcha

                    # Devolvemos el estado que se genraría al transitar a la
                    # derecha
                    return ((i_celda_actual, j_celda_actual+1), energia_dcha, num_C_dcha, num_N_dcha)
                
        return False
    
    def MoverIzq(self) -> tuple or False:
        """
        Devuelve una tupla con el estado que se generaría al aplicar el operador o
        False si no es posible aplicarlo desde el estado actual. Este operador representa
        un movimiento en horizontal a la izquierda.
        """
        # Estado actual: ((i, j), energía, num_C, num_N)
        # Extraemos la información para un código más limpio
        i_celda_actual = self.estado[0][0]
        j_celda_actual = self.estado[0][1]
        energia_actual = self.estado[1]
        num_C = self.estado[2]
        num_N = self.estado[3]
        
        # Si estamos en un borde izquierdo no podemos realizar dicha operación
        # j != 1
        if j_celda_actual != 1:
            # Obtenemos la celda siguiente y comprobamos si es transitable
            celda_izquierda = self.mapa[i_celda_actual][j_celda_actual-1]
            # (i, j-1) != "X"
            if  celda_izquierda != "X":
                # Si es transitable obtenemos su coste para comprobar si el
                # autobús tiene suficiente energía para transitar a ella
                # Además, comprobamos is podemos recoger o dejar paientes
                if (celda_izquierda == "P"):
                    coste_izq = 1
                elif (celda_izquierda == "N"):
                    # Si no hay pacientes C y queda hueco se puede recoger al N
                    # (c=0) y (n<10)
                    if (num_C == 0) and (num_N < 10):
                        num_N_izq = num_N + 1
                    coste_izq = 1
                elif (celda_izquierda == "C"):
                    # Si hay espacio y ningún paciente N sentado en un sitio de
                    # C's, se puede recoger al C
                    if (num_C < 2) and (num_N <= 8):
                        num_C_izq = num_C + 1
                    coste_izq = 1
                elif (celda_izquierda == "CN"):
                    # Si no tenemos C's y tenemos N's, los dejamos. Si no, los 
                    # C's deben ser dejados los primeros
                    if (num_C == 0) and (num_N > 0):
                        num_N_izq = 0
                    coste_izq = 1
                elif (celda_izquierda == "CC"):
                    # Si tenemos C's los dejamos
                    if (num_C > 0):
                        num_C_izq = 0
                    coste_izq = 1
                else:
                    coste_izq = int(celda_izquierda)
                # e > Coste celda izquierda
                if energia_actual > coste_izq:
                    # Actualizamos energía 
                    energia_dcha = energia_actual - coste_izq

                    # Devolvemos el estado que se genraría al transitar a la
                    # derecha
                    return ((i_celda_actual, j_celda_actual-1), energia_dcha, num_C_izq, num_N_izq)
                
        return False
        
    def MoverArriba(self) -> tuple or False:
        """
        Devuelve una tupla con el estado que se generaría al aplicar el operador o
        False si no es posible aplicarlo desde el estado actual. Este operador representa
        un movimiento en vertical hacia arriba.
        """
        # Estado actual: ((i, j), energía, num_C, num_N)
        # Extraemos la información para un código más limpio
        i_celda_actual = self.estado[0][0]
        j_celda_actual = self.estado[0][1]
        energia_actual = self.estado[1]
        num_C = self.estado[2]
        num_N = self.estado[3]
        
        # Si estamos en un borde superior no podemos realizar dicha operación
        # i != 1
        if i_celda_actual != 1:
            # Obtenemos la celda siguiente y comprobamos si es transitable
            celda_superior = self.mapa[i_celda_actual-1][j_celda_actual]
            # (i-1, j) != "X"
            if  celda_superior != "X":
                # Si es transitable obtenemos su coste para comprobar si el
                # autobús tiene suficiente energía para transitar a ella
                # Además, comprobamos is podemos recoger o dejar paientes
                if (celda_superior == "P"):
                    coste_sup = 1
                elif (celda_superior == "N"):
                    # Si no hay pacientes C y queda hueco se puede recoger al N
                    # (c=0) y (n<10)
                    if (num_C == 0) and (num_N < 10):
                        num_N_sup = num_N + 1
                    coste_sup = 1
                elif (celda_superior == "C"):
                    # Si hay espacio y ningún paciente N sentado en un sitio de
                    # C's, se puede recoger al C
                    if (num_C < 2) and (num_N <= 8):
                        num_C_sup = num_C + 1
                    coste_sup = 1
                elif (celda_superior == "CN"):
                    # Si no tenemos C's y tenemos N's, los dejamos. Si no, los 
                    # C's deben ser dejados los primeros
                    if (num_C == 0) and (num_N > 0):
                        num_N_sup = 0
                    coste_sup = 1
                elif (celda_superior == "CC"):
                    # Si tenemos C's los dejamos
                    if (num_C > 0):
                        num_C_sup = 0
                    coste_sup = 1
                else:
                    coste_sup = int(celda_superior)
                # e > Coste celda izquierda
                if energia_actual > coste_sup:
                    # Actualizamos energía 
                    energia_sup = energia_actual - coste_sup

                    # Devolvemos el estado que se genraría al transitar a la
                    # derecha
                    return ((i_celda_actual-1, j_celda_actual), energia_sup, num_C_sup, num_N_sup)
                
        return False      
    
    def MoverAbajo(self) -> tuple or False:
        """
        Devuelve una tupla con el estado que se generaría al aplicar el operador o
        False si no es posible aplicarlo desde el estado actual. Este operador representa
        un movimiento en vertical hacia abajo.
        """
        # Estado actual: ((i, j), energía, num_C, num_N)
        # Extraemos la información para un código más limpio
        i_celda_actual = self.estado[0][0]
        j_celda_actual = self.estado[0][1]
        energia_actual = self.estado[1]
        num_C = self.estado[2]
        num_N = self.estado[3]
        
        # Si estamos en un borde inferior no podemos realizar dicha operación
        # i != num_filas
        if i_celda_actual != self.num_filas:
            # Obtenemos la celda siguiente y comprobamos si es transitable
            celda_inferior = self.mapa[i_celda_actual+1][j_celda_actual]
            # (i+1, j) != "X"
            if  celda_inferior != "X":
                # Si es transitable obtenemos su coste para comprobar si el
                # autobús tiene suficiente energía para transitar a ella
                # Además, comprobamos is podemos recoger o dejar paientes
                if (celda_inferior == "P"):
                    coste_inf = 1
                elif (celda_inferior == "N"):
                    # Si no hay pacientes C y queda hueco se puede recoger al N
                    # (c=0) y (n<10)
                    if (num_C == 0) and (num_N < 10):
                        num_N_inf = num_N + 1
                    coste_inf = 1
                elif (celda_inferior == "C"):
                    # Si hay espacio y ningún paciente N sentado en un sitio de
                    # C's, se puede recoger al C
                    if (num_C < 2) and (num_N <= 8):
                        num_C_inf = num_C + 1
                    coste_inf = 1
                elif (celda_inferior == "CN"):
                    # Si no tenemos C's y tenemos N's, los dejamos. Si no, los 
                    # C's deben ser dejados los primeros
                    if (num_C == 0) and (num_N > 0):
                        num_N_inf = 0
                    coste_inf = 1
                elif (celda_inferior == "CC"):
                    # Si tenemos C's los dejamos
                    if (num_C > 0):
                        num_C_inf = 0
                    coste_inf = 1
                else:
                    coste_inf = int(celda_inferior)
                # e > Coste celda izquierda
                if energia_actual > coste_inf:
                    # Actualizamos energía 
                    energia_inf = energia_actual - coste_inf

                    # Devolvemos el estado que se genraría al transitar a la
                    # derecha
                    return ((i_celda_actual-1, j_celda_actual), energia_inf, num_C_inf, num_N_inf)
                
        return False


    # HEURÍSTICAS:
    
    def h1(self):
        pass

    def h2(self):
        pass

    def h3(self):
        """
        Heurística extra que siempre devuelve 0. Es el equivalente a hacer Dijkstra.
        """
        return 0
    
    # ALGORÍTMO A*:
    
    def AStar(self, num_h: int) -> bool:
        """
        Implementación del algorítmo A* haciendo uso de la heurística indicada
        como argumento. Devuelve True si ha encontrado solución y Flase si no.
        """
        # Lista ABIERTA: elementos ordenados por mejor función de evaluación,
        # estados pendientes de expandir
        # Elementos de ABIERTA: [(celda), coste, heuristica, puntero_padre]
        ABIERTA = []
        # Lista CERRADA: elementos ya expandidos
        # Elementos de CERRADA: [(celda), coste]
        CERRADA = []




if __name__ == "__main__":   
    
    if len(sys.argv) != 3:
        raise ValueError("\n"+'\033[91m'+"Es necesario especificar un archivo csv y un número como argumento" + '\033[0m')
    
    Parte2(sys.argv[1], sys.argv[2])
