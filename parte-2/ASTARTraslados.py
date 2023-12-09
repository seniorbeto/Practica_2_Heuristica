# !/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   Autores:
#       Alberto Penas Díaz
#       Natalia Rodríguez Navarro
#


import csv
import sys
from operator import itemgetter

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

        # Obtenemos el número de celda del parking y la cantidad de pacientes que
        # requieren asistencia para establecer el estado inicial
        restantes = 0
        i = 0
        while i < self.num_filas:
            j = 0
            while j < self.num_columnas:
                if self.mapa[i][j] == "P":
                    self.pos_parking = (i+1, j+1)
                elif (self.mapa[i][j] == "N") or (self.mapa[i][j] == "C"):
                    restantes += 1
                j+=1
            i+=1

        # Estado inicial ((i, j), energía, num_C, num_N, pacientes_restantes_por_asistir)
        self.estado_inicial = (self.pos_parking, 50, 0, 0, restantes)

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

    def MoverDcha(self, estado_actual: tuple) -> tuple or False:
        """
        Devuelve una tupla con el estado que se generaría al aplicar el operador o
        False si no es posible aplicarlo desde el estado actual. Este operador representa
        un movimiento en horizontal a la derecha.
        """
        # Estado actual: ((i, j), energía, num_C, num_N)
        # Extraemos la información para un código más limpio
        i_celda = estado_actual[0][0]
        j_celda = estado_actual[0][1]
        energia = estado_actual[1]
        num_C = estado_actual[2]
        num_N = estado_actual[3]
        restantes = estado_actual[4]
        
        # Si estamos en un borde derecho no podemos realizar dicha operación
        # j != num_columnas
        if j_celda != self.num_columnas:
            # Obtenemos la celda siguiente y comprobamos si es transitable
            celda_derecha = self.mapa[i_celda][j_celda+1]
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
                        num_N += 1
                    coste_dcha = 1
                elif (celda_derecha == "C"):
                    # Si hay espacio y ningún paciente N sentado en un sitio de
                    # C's, se puede recoger al C
                    if (num_C < 2) and (num_N <= 8):
                        num_C += 1
                    coste_dcha = 1
                elif (celda_derecha == "CN"):
                    # Si no tenemos C's y tenemos N's, los dejamos. Si no, los 
                    # C's deben ser dejados los primeros
                    if (num_C == 0) and (num_N > 0):
                        num_N = 0
                        restantes -= 1
                    coste_dcha = 1
                elif (celda_derecha == "CC"):
                    # Si tenemos C's los dejamos
                    if (num_C > 0):
                        num_C = 0
                        restantes -= 1
                    coste_dcha = 1
                else:
                    coste_dcha = int(celda_derecha)
                # e > Coste celda derecha
                if energia > coste_dcha:
                    # Actualizamos energía 
                    energia_dcha = energia - coste_dcha

                    # Devolvemos el estado que se genraría al transitar a la
                    # derecha
                    return ((i_celda, j_celda+1), energia_dcha, num_C, num_N, restantes)
                
        return False
    
    def MoverIzq(self, estado_actual: tuple) -> tuple or False:
        """
        Devuelve una tupla con el estado que se generaría al aplicar el operador o
        False si no es posible aplicarlo desde el estado actual. Este operador representa
        un movimiento en horizontal a la izquierda.
        """
        # Estado actual: ((i, j), energía, num_C, num_N)
        # Extraemos la información para un código más limpio
        i_celda = estado_actual[0][0]
        j_celda = estado_actual[0][1]
        energia = estado_actual[1]
        num_C = estado_actual[2]
        num_N = estado_actual[3]
        restantes = estado_actual[4]
        
        # Si estamos en un borde izquierdo no podemos realizar dicha operación
        # j != 1
        if j_celda != 1:
            # Obtenemos la celda siguiente y comprobamos si es transitable
            celda_izquierda = self.mapa[i_celda][j_celda-1]
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
                        num_N += 1
                    coste_izq = 1
                elif (celda_izquierda == "C"):
                    # Si hay espacio y ningún paciente N sentado en un sitio de
                    # C's, se puede recoger al C
                    if (num_C < 2) and (num_N <= 8):
                        num_C += 1
                    coste_izq = 1
                elif (celda_izquierda == "CN"):
                    # Si no tenemos C's y tenemos N's, los dejamos. Si no, los 
                    # C's deben ser dejados los primeros
                    if (num_C == 0) and (num_N > 0):
                        num_N = 0
                        restantes -= 1
                    coste_izq = 1
                elif (celda_izquierda == "CC"):
                    # Si tenemos C's los dejamos
                    if (num_C > 0):
                        num_C = 0
                        restantes -= 1
                    coste_izq = 1
                else:
                    coste_izq = int(celda_izquierda)
                # e > Coste celda izquierda
                if energia > coste_izq:
                    # Actualizamos energía 
                    energia_izq = energia - coste_izq

                    # Devolvemos el estado que se genraría al transitar a la
                    # derecha
                    return ((i_celda, j_celda-1), energia_izq, num_C, num_N, restantes)
                
        return False
        
    def MoverArriba(self, estado_actual: tuple) -> tuple or False:
        """
        Devuelve una tupla con el estado que se generaría al aplicar el operador o
        False si no es posible aplicarlo desde el estado actual. Este operador representa
        un movimiento en vertical hacia arriba.
        """
        # Estado actual: ((i, j), energía, num_C, num_N)
        # Extraemos la información para un código más limpio
        i_celda = estado_actual[0][0]
        j_celda = estado_actual[0][1]
        energia = estado_actual[1]
        num_C = estado_actual[2]
        num_N = estado_actual[3]
        restantes = estado_actual[4]
        
        # Si estamos en un borde superior no podemos realizar dicha operación
        # i != 1
        if i_celda != 1:
            # Obtenemos la celda siguiente y comprobamos si es transitable
            celda_superior = self.mapa[i_celda-1][j_celda]
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
                        num_N += 1
                    coste_sup = 1
                elif (celda_superior == "C"):
                    # Si hay espacio y ningún paciente N sentado en un sitio de
                    # C's, se puede recoger al C
                    if (num_C < 2) and (num_N <= 8):
                        num_C += 1
                    coste_sup = 1
                elif (celda_superior == "CN"):
                    # Si no tenemos C's y tenemos N's, los dejamos. Si no, los 
                    # C's deben ser dejados los primeros
                    if (num_C == 0) and (num_N > 0):
                        num_N = 0
                        restantes -= 1
                    coste_sup = 1
                elif (celda_superior == "CC"):
                    # Si tenemos C's los dejamos
                    if (num_C > 0):
                        num_C = 0
                        restantes -= 1
                    coste_sup = 1
                else:
                    coste_sup = int(celda_superior)
                # e > Coste celda izquierda
                if energia > coste_sup:
                    # Actualizamos energía 
                    energia_sup = energia - coste_sup

                    # Devolvemos el estado que se genraría al transitar a la
                    # derecha
                    return ((i_celda-1, j_celda), energia_sup, num_C, num_N, restantes)
                
        return False      
    
    def MoverAbajo(self, estado_actual: tuple) -> tuple or False:
        """
        Devuelve una tupla con el estado que se generaría al aplicar el operador o
        False si no es posible aplicarlo desde el estado actual. Este operador representa
        un movimiento en vertical hacia abajo.
        """
        # Estado actual: ((i, j), energía, num_C, num_N)
        # Extraemos la información para un código más limpio
        i_celda = estado_actual[0][0]
        j_celda = estado_actual[0][1]
        energia = estado_actual[1]
        num_C = estado_actual[2]
        num_N = estado_actual[3]
        restantes = estado_actual[4]
        
        # Si estamos en un borde inferior no podemos realizar dicha operación
        # i != num_filas
        if i_celda != self.num_filas:
            # Obtenemos la celda siguiente y comprobamos si es transitable
            celda_inferior = self.mapa[i_celda+1][j_celda]
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
                        num_N += 1
                    coste_inf = 1
                elif (celda_inferior == "C"):
                    # Si hay espacio y ningún paciente N sentado en un sitio de
                    # C's, se puede recoger al C
                    if (num_C < 2) and (num_N <= 8):
                        num_C += 1
                    coste_inf = 1
                elif (celda_inferior == "CN"):
                    # Si no tenemos C's y tenemos N's, los dejamos. Si no, los 
                    # C's deben ser dejados los primeros
                    if (num_C == 0) and (num_N > 0):
                        num_N = 0
                        restantes -= 1
                    coste_inf = 1
                elif (celda_inferior == "CC"):
                    # Si tenemos C's los dejamos
                    if (num_C > 0):
                        num_C = 0
                        restantes -= 1
                    coste_inf = 1
                else:
                    coste_inf = int(celda_inferior)
                # e > Coste celda izquierda
                if energia > coste_inf:
                    # Actualizamos energía 
                    energia_inf = energia - coste_inf

                    # Devolvemos el estado que se genraría al transitar a la
                    # derecha
                    return ((i_celda-1, j_celda), energia_inf, num_C, num_N, restantes)
                
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

    # FUNCIÓN DE EVALUACIÓN:

    def f(self, elem_de_ABIERTA: tuple):
        g = elem_de_ABIERTA[1]
        h = elem_de_ABIERTA[2]
        return g + h

    # ALGORÍTMO A*:
    
    def AStar(self, num_h: int) -> bool:
        """
        Implementación del algorítmo A* haciendo uso de la heurística indicada
        como argumento. Devuelve True si ha encontrado solución y Flase si no.
        """
        # Lista ABIERTA: elementos ordenados por mejor función de evaluación,
        # estados pendientes de expandir
        # Elementos de ABIERTA: 
        # [estado: ((i, j), energía, num_C, num_N, restantes), coste, heuristica, puntero_padre]
        ABIERTA = []
        # Lista CERRADA: elementos ya expandidos
        # Elementos de CERRADA: 
        # [estado: ((i, j), energía, num_C, num_N, restantes), coste, heuristica, puntero_padre]
        CERRADA = []

        # Iniciamos algorítmo con el estado inicial
        if num_h == 1:
            pass
        elif num_h == 2:
            pass
        else:
            ABIERTA.append((self.estado_inicial, 0, self.h3(), None))

        # Hasta que ABIERTA esté vacía o ÉXITO
        EXITO = False
        while (len(ABIERTA) > 0) and (not EXITO):
            # Quitamos primer elemento de ABIERTA y lo metemos en CERRADA
            estado_a_expandir = ABIERTA.pop(0)
            CERRADA.append(estado_a_expandir)
            # Si el estado a expandir es final, entonces ÉXITO
            # (celda) = (celda_parking) y energía > 1 y num_C = 0 y num_N = 0 y restantes = 0
            if (estado_a_expandir[0][0] == self.pos_parking) and (estado_a_expandir[0][1] > 1) \
                and (estado_a_expandir[0][2] == 0) and (estado_a_expandir[0][3] == 0) and \
                (estado_a_expandir[0][4] == 0):

                EXITO = True
            # Si no, expandimos el estado y añademos sus sucesores a ABIERTA
            # ordenados por su función de evaluación f
            else:
                sucesor_1 = self.MoverDcha(estado_a_expandir[0])
                sucesor_2 = self.MoverIzq(estado_a_expandir[0])
                sucesor_3 = self.MoverArriba(estado_a_expandir[0])
                sucesor_4 = self.MoverAbajo(estado_a_expandir[0])
                if sucesor_1:
                    # Coste para llegar al sucesor: coste_padre + coste_hijo
                    # coste_hijo = energia_restante_padre - energia_restante_hijo 
                    coste_padre = estado_a_expandir[1]
                    coste_hijo = estado_a_expandir[0][1] - sucesor_1[1]
                    if num_h == 1:
                        pass
                    elif num_h == 2:
                        pass
                    else:
                        ABIERTA.append((sucesor_1, coste_padre+coste_hijo, self.h3(), estado_a_expandir[0]))                       
                if sucesor_2:
                    # Coste para llegar al sucesor: coste_padre + coste_hijo
                    # coste_hijo = energia_restante_padre - energia_restante_hijo 
                    coste_padre = estado_a_expandir[1]
                    coste_hijo = estado_a_expandir[0][1] - sucesor_2[1]
                    if num_h == 1:
                        pass
                    elif num_h == 2:
                        pass
                    else:
                        ABIERTA.append((sucesor_2, coste_padre+coste_hijo, self.h3(), estado_a_expandir[0])) 
                if sucesor_3:
                    # Coste para llegar al sucesor: coste_padre + coste_hijo
                    # coste_hijo = energia_restante_padre - energia_restante_hijo 
                    coste_padre = estado_a_expandir[1]
                    coste_hijo = estado_a_expandir[0][1] - sucesor_3[1]
                    if num_h == 1:
                        pass
                    elif num_h == 2:
                        pass
                    else:
                        ABIERTA.append((sucesor_3, coste_padre+coste_hijo, self.h3(), estado_a_expandir[0])) 
                if sucesor_4:
                    # Coste para llegar al sucesor: coste_padre + coste_hijo
                    # coste_hijo = energia_restante_padre - energia_restante_hijo 
                    coste_padre = estado_a_expandir[1]
                    coste_hijo = estado_a_expandir[0][1] - sucesor_4[1]
                    if num_h == 1:
                        pass
                    elif num_h == 2:
                        pass
                    else:
                        ABIERTA.append((sucesor_4, coste_padre+coste_hijo, self.h3(), estado_a_expandir[0])) 
                
                # Ordenamos la lista por función de evaluación
                ABIERTA.sort(key=self.f)
                print(ABIERTA)

        return EXITO


if __name__ == "__main__":   
    
    if len(sys.argv) != 3:
        raise ValueError("\n"+'\033[91m'+"Es necesario especificar un archivo csv y un número como argumento" + '\033[0m')
    
    Parte2(sys.argv[1], sys.argv[2])
