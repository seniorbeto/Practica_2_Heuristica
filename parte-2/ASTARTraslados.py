# !/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   Autores:
#       Alberto Penas Díaz
#       Natalia Rodríguez Navarro
#


import csv
import sys
import time
from copy import deepcopy


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
            raise ValueError("\n"+'\033[91m'+"El número de heurísitca a utilizar debe ser un entero." + '\033[0m')

        # Si la heurística no está entre 1 y 3, error
        if (num_h <= 0) or (num_h > 3):
            raise ValueError("\n"+'\033[91m'+"Es necesario especificar una heurísitca entre 1 y 3 (incluidos)." + '\033[0m')

        # Primero obtenemos el mapa como una matriz
        self.mapa = self.leer_fichero_de_entrada(mapa, num_h)

        # Definimos número de filas y columnas
        self.num_filas = len(self.mapa)
        self.num_columnas = len(self.mapa[0])

        # Obtenemos el número de celda del parking y la cantidad de pacientes que
        # requieren asistencia para establecer el estado inicial
        hay_parking = False
        hay_CC = False
        hay_CN = False
        restantes = 0
        i = 0
        while i < self.num_filas:
            j = 0
            while j < self.num_columnas:
                # Comprobar que hay un único P 
                if self.mapa[i][j] == "P":
                    if hay_parking:
                        raise ValueError("\n"+'\033[91m'+"El mapa debe tener únicamente un parking." + '\033[0m')
                    self.pos_parking = (i+1, j+1)
                    hay_parking = True
                elif (self.mapa[i][j] == "N") or (self.mapa[i][j] == "C"):
                    restantes += 1
                # Comrpobamos que hay como mínimo un CC
                elif (self.mapa[i][j] == "CC"):
                    hay_CC = True
                # Comprobamos que hay como mínimo un CN
                elif (self.mapa[i][j] == "CN"):
                    hay_CN = True
                j+=1
            i+=1

        # Si no hay un CC ni un CN, error
        if (not hay_CC) or (not hay_CN):
            raise ValueError("\n"+'\033[91m'+"El mapa debe tener como minímo un CC y un CN." + '\033[0m')

        # Todos los pacientes que hay inicialmente
        self.todos_los_pacientes = restantes

        # Estado inicial ((i, j), energía, num_C, num_N, pacientes_restantes_por_dejar, mapa)
        self.estado_inicial = (self.pos_parking, 50, 0, 0, restantes, self.mapa)

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
                mapa_reader = list(csv.reader(csvfile, delimiter="\n", quotechar='|'))
        except:
            raise ValueError("\n"+'\033[91m'+"Es necesario especificar una ruta válida como argumento." + '\033[0m')
                
        validos = ['C', 'CC', 'CN', 'N', 'P', 'X']
        check_num_filas = None
        for row in mapa_reader:
            row[0] = row[0].replace(' ', 'no_valido')
            celdas = row[0].split(";")

            # Comprobamos que en las celdas solamente hay valores válidos y están
            # separados por ';'
            for c in celdas:
                if c not in validos:
                    # Comprobar que es un entero
                    try:
                        int(c) 
                    except:
                        raise ValueError("\n"+'\033[91m'+"El valor de una celda en el mapa debe ser N, C," + 
                                        "CC, CN, P o un entero, separados por ';' sin espacios."+ '\033[0m')

            # Comprobamos que el mapa es rectangular (mismo número de columnas en 
            # cada fila)
            if check_num_filas is not None:
                if len(celdas) != check_num_filas:
                    print(len(celdas))
                    raise ValueError("\n"+'\033[91m'+"El mapa debe ser rectangular." + '\033[0m')
            else:
                check_num_filas = len(celdas)

            matriz.append(celdas)
        
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
        mapa = deepcopy(estado_actual[5])
        
        # Si estamos en un borde derecho no podemos realizar dicha operación
        # j != num_columnas
        if j_celda != self.num_columnas:
            # Obtenemos la celda siguiente y comprobamos si es transitable
            celda_derecha = mapa[i_celda-1][j_celda]
            # (i, j+1) != "X"
            if celda_derecha != "X":
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
                        # Modificamos el mapa indicando que ya hemos recogido al paciente
                        mapa[i_celda-1][j_celda] = "1"
                    coste_dcha = 1
                elif (celda_derecha == "C"):
                    # Si hay espacio y ningún paciente N sentado en un sitio de
                    # C's, se puede recoger al C
                    if (num_C < 2) and (num_N <= 8):
                        num_C += 1
                        # Modificamos el mapa indicando que ya hemos recogido al paciente
                        mapa[i_celda-1][j_celda] = "1"
                    coste_dcha = 1
                elif (celda_derecha == "CN"):
                    # Si no tenemos C's y tenemos N's, los dejamos. Si no, los 
                    # C's deben ser dejados los primeros
                    if (num_C == 0) and (num_N > 0):
                        restantes -= num_N
                        num_N = 0
                    coste_dcha = 1
                elif (celda_derecha == "CC"):
                    # Si tenemos C's los dejamos
                    if (num_C > 0):
                        restantes -= num_C
                        num_C = 0          
                    coste_dcha = 1
                else:
                    coste_dcha = int(celda_derecha)
                # e > Coste celda derecha
                if (energia > coste_dcha):
                    # Actualizamos energía 
                    energia_dcha = energia - coste_dcha

                    # Si estamos en el parking recargamos energía
                    if (celda_derecha == "P"):
                        energia_dcha = 50

                    # Devolvemos el estado que se genraría al transitar a la
                    # derecha
                    return ((i_celda, j_celda+1), energia_dcha, num_C, num_N, restantes, mapa)
                
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
        mapa = deepcopy(estado_actual[5])
        
        # Si estamos en un borde izquierdo no podemos realizar dicha operación
        # j != 1
        if j_celda != 1:
            # Obtenemos la celda siguiente y comprobamos si es transitable
            celda_izquierda = mapa[i_celda-1][j_celda-2]
            # (i, j-1) != "X"
            if celda_izquierda != "X":
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
                        # Modificamos el mapa indicando que ya hemos recogido al paciente
                        mapa[i_celda-1][j_celda-2] = "1"
                    coste_izq = 1
                elif (celda_izquierda == "C"):
                    # Si hay espacio y ningún paciente N sentado en un sitio de
                    # C's, se puede recoger al C
                    if (num_C < 2) and (num_N <= 8):
                        num_C += 1
                        # Modificamos el mapa indicando que ya hemos recogido al paciente
                        mapa[i_celda-1][j_celda-2] = "1"
                    coste_izq = 1
                elif (celda_izquierda == "CN"):
                    # Si no tenemos C's y tenemos N's, los dejamos. Si no, los 
                    # C's deben ser dejados los primeros
                    if (num_C == 0) and (num_N > 0):
                        restantes -= num_N
                        num_N = 0
                    coste_izq = 1
                elif (celda_izquierda == "CC"):
                    # Si tenemos C's los dejamos
                    if (num_C > 0):
                        restantes -= num_C
                        num_C = 0
                    coste_izq = 1
                else:
                    coste_izq = int(celda_izquierda)
                # e > Coste celda izquierda
                if energia > coste_izq:
                    # Actualizamos energía 
                    energia_izq = energia - coste_izq

                    # Si estamos en el parking recargamos energía
                    if (celda_izquierda == "P"):
                        energia_izq = 50

                    # Devolvemos el estado que se genraría al transitar a la
                    # derecha
                    return ((i_celda, j_celda-1), energia_izq, num_C, num_N, restantes, mapa)
                
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
        mapa = deepcopy(estado_actual[5])
        
        # Si estamos en un borde superior no podemos realizar dicha operación
        # i != 1
        if i_celda != 1:
            # Obtenemos la celda siguiente y comprobamos si es transitable
            celda_superior = mapa[i_celda-2][j_celda-1]
            # (i-1, j) != "X"
            if celda_superior != "X":
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
                        # Modificamos el mapa indicando que ya hemos recogido al paciente
                        mapa[i_celda-2][j_celda-1] = "1"
                    coste_sup = 1
                elif (celda_superior == "C"):
                    # Si hay espacio y ningún paciente N sentado en un sitio de
                    # C's, se puede recoger al C
                    if (num_C < 2) and (num_N <= 8):
                        num_C += 1
                        # Modificamos el mapa indicando que ya hemos recogido al paciente
                        mapa[i_celda-2][j_celda-1] = "1"
                    coste_sup = 1
                elif (celda_superior == "CN"):
                    # Si no tenemos C's y tenemos N's, los dejamos. Si no, los 
                    # C's deben ser dejados los primeros
                    if (num_C == 0) and (num_N > 0):
                        restantes -= num_N
                        num_N = 0
                    coste_sup = 1
                elif (celda_superior == "CC"):
                    # Si tenemos C's los dejamos
                    if (num_C > 0):
                        restantes -= num_C
                        num_C = 0
                    coste_sup = 1
                else:
                    coste_sup = int(celda_superior)
                # e > Coste celda izquierda
                if energia > coste_sup:
                    # Actualizamos energía 
                    energia_sup = energia - coste_sup

                    # Si estamos en el parking recargamos energía
                    if (celda_superior == "P"):
                        energia_sup = 50

                    # Devolvemos el estado que se genraría al transitar a la
                    # derecha
                    return ((i_celda-1, j_celda), energia_sup, num_C, num_N, restantes, mapa)
                
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
        mapa = deepcopy(estado_actual[5])
        
        # Si estamos en un borde inferior no podemos realizar dicha operación
        # i != num_filas
        if i_celda != self.num_filas:
            # Obtenemos la celda siguiente y comprobamos si es transitable
            celda_inferior = mapa[i_celda][j_celda-1]
            # (i+1, j) != "X"
            if celda_inferior != "X":
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
                        # Modificamos el mapa indicando que ya hemos recogido al paciente
                        mapa[i_celda][j_celda-1] = "1"
                    coste_inf = 1
                elif (celda_inferior == "C"):
                    # Si hay espacio y ningún paciente N sentado en un sitio de
                    # C's, se puede recoger al C
                    if (num_C < 2) and (num_N <= 8):
                        num_C += 1
                        # Modificamos el mapa indicando que ya hemos recogido al paciente
                        mapa[i_celda][j_celda-1] = "1"
                    coste_inf = 1
                elif (celda_inferior == "CN"):
                    # Si no tenemos C's y tenemos N's, los dejamos. Si no, los 
                    # C's deben ser dejados los primeros
                    if (num_C == 0) and (num_N > 0):
                        restantes -= num_N
                        num_N = 0
                    coste_inf = 1
                elif (celda_inferior == "CC"):
                    # Si tenemos C's los dejamos
                    if (num_C > 0):
                        restantes -= num_C
                        num_C = 0
                    coste_inf = 1
                else:
                    coste_inf = int(celda_inferior)
                # e > Coste celda izquierda
                if energia > coste_inf:
                    # Actualizamos energía 
                    energia_inf = energia - coste_inf

                    # Si estamos en el parking recargamos energía
                    if (celda_inferior == "P"):
                        energia_inf = 50

                    # Devolvemos el estado que se genraría al transitar a la
                    # derecha
                    return ((i_celda+1, j_celda), energia_inf, num_C, num_N, restantes, mapa)
                
        return False


    # HEURÍSTICAS:
    
    def h1(self, estado: tuple) -> int:
        """
        Heurística que dado un estado, devuelve el camino mínimo usando la distancia Manhatan
        (sin tener en cuenta los costes y las paredes, coste unitario siempre) que debería hacer 
        el bus para dejar y recoger pacientes en el centro más cercano. O volver al parking en 
        caso de que no queden pacientes por dejar.

        Si restantes = 0 -> h1(estado) = distanciaMan(a P)
        Si restantes > 0 -> h1(estado) = pacientes_que_quedan_por_recoger + 
                                         distanciaMan(a cualquier CENTRO <el más cercano>) + 
                                         distanciaMan(a P desde ese CENTRO)
        """    

        indice_actual = estado[0]
        num_C_recogidos = estado[2]
        num_N_recogidos = estado[3]
        pacientes_restantes_por_dejar = estado[4]
        # Estado ((i, j), energía, num_C, num_N, pacientes_restantes_por_dejar, mapa)

        if pacientes_restantes_por_dejar == 0:
            return self.distanciaMan(indice_actual, self.pos_parking)
        else:
            # Calculamos pacientes que quedan por dejar en sus centros
            quedan_por_recoger = self.todos_los_pacientes - (num_C_recogidos + num_N_recogidos)
            
            # Calculamos la distancia Manhattan desde donde estamos 
            # hasta el centro más cercano
            distancia_centros = {}
            i = 0
            while i < self.num_filas:
                j = 0
                while j < self.num_columnas:
                    if self.mapa[i][j] == 'CC' or self.mapa[i][j] == 'CN':
                        distancia_centros[(i, j)] = self.distanciaMan(indice_actual, (i, j))
                    j += 1
                i+=1

            min = None
            for elem in distancia_centros.keys():
                if min is None:
                    min = elem
                else:
                    if distancia_centros[elem] < distancia_centros[min]:
                        min = elem
            
            distancia_centro_mas_cercano = distancia_centros[min]

            ditancia_centro_mas_cercano_a_parking = self.distanciaMan(min, self.pos_parking)

            return distancia_centro_mas_cercano + ditancia_centro_mas_cercano_a_parking + quedan_por_recoger
            

    def distanciaMan(self, indice1: tuple, indice2: tuple) -> int:
        """
        Distancia Manhattan entre dos elementos del mapa dados sus índices
        (suponiendo costes unitarios).
        """
        diferencia_filas = abs(indice1[0] - indice2[0])
        diferencia_columnas = abs(indice1[1] - indice2[1])
        return abs(diferencia_filas - diferencia_columnas)
        
    def h2(self, estado: tuple) -> int:
        """
        N/10 -> 10(num_N)+disM(a CN)
        Si N/10 ahora es <0 (quedan menos o igual que 8 num_N's) -> num_N+(num_C/2 los que quepan)+dis(CN a CC)+dis(de CC a CN)
        ...
        ultima dis(desde donde te quedas a P)
        """
        indice_actual = estado[0]
        num_C_recogidos = estado[2]
        num_N_recogidos = estado[3]
        pacientes_restantes_por_dejar = estado[4]
        mapa_estado = estado[5]
        # Estado ((i, j), energía, num_C, num_N, pacientes_restantes_por_dejar, mapa)

        # Dado el mapa del estado, obtenemos cuántos pacientes de cada tipo quedan por recoger,
        # así como la localización de cada centro junto con su distancia manhattan al indice actual.
        centros_cc = {}
        cc_mas_cercano = None
        centros_nc = {}
        nc_mas_cercano = None
        pacientes_c_por_recoger = 0
        pacientes_n_por_recoger = 0
        i = 0
        while i < self.num_filas:
            j = 0
            while j < self.num_columnas:
                if mapa_estado[i][j] == 'CC':
                    distancia = self.distanciaMan((i,j), indice_actual)
                    centros_cc[(i, j)] = distancia
                    if cc_mas_cercano is None:
                        cc_mas_cercano = (i, j)
                    elif distancia < centros_cc[cc_mas_cercano]:
                        cc_mas_cercano = (i, j)
                elif mapa_estado[i][j] == 'NC':
                    distancia = self.distanciaMan((i, j), indice_actual)
                    centros_nc[(i, j)] = distancia
                    if nc_mas_cercano is None:
                        nc_mas_cercano = (i, j)
                    elif distancia < centros_nc[nc_mas_cercano]:
                        nc_mas_cercano = (i, j)
                elif mapa_estado[i][j] == 'C':
                    pacientes_c_por_recoger += 1
                elif mapa_estado[i][j] == 'N':
                    pacientes_n_por_recoger += 1
                j += 1
            i += 1

        # Si no queda ningún tipo de paciente por recoger
        if pacientes_c_por_recoger == 0 and pacientes_n_por_recoger == 0:
            # Comprobamos si aún nos quedan pacientes por dejar (ya que puede ser que los tengamos
            # en el bus)
            if num_C_recogidos == 0 and num_N_recogidos == 0:
                # Si no queda nadie en el bus, la heurística devuelve la distancia Manhattan
                # desde el índice actual hasta el parking
                return self.distanciaMan(indice_actual, self.pos_parking)

            elif num_C_recogidos == 0 and num_N_recogidos != 0:
                # Si únicamente nos queda por dejar a pacientes de tipo N, la heurística será
                # la suma de la distancia Manhattan desde índice actual hasta el NC que más rente
                # más la distancia desde ese NC hasta el parking
                distancia_mas_rentable = -1
                for nc in centros_nc.keys():
                    posibilidad = self.distanciaMan(indice_actual, nc) + self.distanciaMan(nc, self.pos_parking)
                    if distancia_mas_rentable == -1:
                        distancia_mas_rentable = posibilidad
                    elif posibilidad < distancia_mas_rentable:
                        distancia_mas_rentable = posibilidad
                return distancia_mas_rentable

            elif num_C_recogidos != 0 and num_N_recogidos == 0:
                # Si únicamente nos queda por dejar a pacientes de tipo C, la heurística será
                # la suma de la distancia Manhattan desde índice actual hasta el CC que más rente
                # más la distancia desde ese CC hasta el parking
                distancia_mas_rentable = -1
                for cc in centros_cc.keys():
                    posibilidad = self.distanciaMan(indice_actual, cc) + self.distanciaMan(cc, self.pos_parking)
                    if distancia_mas_rentable == -1:
                        distancia_mas_rentable = posibilidad
                    elif posibilidad < distancia_mas_rentable:
                        distancia_mas_rentable = posibilidad
                return distancia_mas_rentable

            elif num_C_recogidos != 0 and num_N_recogidos != 0:
                # Si nos quedan por dejar a pacientes de tipo C y a pacientes de tipo N,
                # la heurística será la distancia Manhattan desde el índice actual hasta el
                # centro CC más cercano, más la distancia desde ese CC hasta el NC QUE MÁS RENTE
                # más la distancia desde ese NC que más rente hasta el parking
                # (En el video que le pasé a natalia el 11.12.2023 a las 13:39 está explicado)

                distancia_mas_rentable = -1
                for cc in centros_cc.keys():
                    for nc in centros_nc.keys():
                        posibilidad = self.distanciaMan(indice_actual, cc) + self.distanciaMan(cc, nc) + self.distanciaMan(nc, self.pos_parking)
                        if distancia_mas_rentable == -1:
                            distancia_mas_rentable = posibilidad
                        elif posibilidad < distancia_mas_rentable:
                            distancia_mas_rentable = posibilidad

                return distancia_mas_rentable

        # Si solamente quedan pacientes N por recoger
        elif pacientes_c_por_recoger == 0 and pacientes_n_por_recoger != 0:
            # Comprobamos qué pacientes nos quedan por dejar (ya que puede ser que
            # tengamos alguno en el bus)
            if num_C_recogidos == 0 and num_N_recogidos == 0:
                # Si no hay nadie en el bus, la heurística será la distancia más rentable
                # desde nuestro índice actual hasta el NC más rentable más el número de usuarios
                # N que quedan en el mapa
                distancia_mas_rentable = -1
                for nc in centros_nc.keys():
                    posibilidad = self.distanciaMan(indice_actual, nc) + self.distanciaMan(nc, self.pos_parking)
                    if distancia_mas_rentable == -1:
                        distancia_mas_rentable = posibilidad
                    elif posibilidad < distancia_mas_rentable:
                        distancia_mas_rentable = posibilidad
                return distancia_mas_rentable + pacientes_n_por_recoger

            elif num_C_recogidos == 0 and num_N_recogidos != 0:
                # Si en el autobus solo nos quedan pacientes de tipo N, devolveremos
                # exactamente lo mismo que en el caso anterior

                # FIXME revisar este caso porque creo que está mal.

                distancia_mas_rentable = -1
                for nc in centros_nc.keys():
                    posibilidad = self.distanciaMan(indice_actual, nc) + self.distanciaMan(nc, self.pos_parking)
                    if distancia_mas_rentable == -1:
                        distancia_mas_rentable = posibilidad
                    elif posibilidad < distancia_mas_rentable:
                        distancia_mas_rentable = posibilidad
                return distancia_mas_rentable + pacientes_n_por_recoger

            elif num_C_recogidos != 0 and num_N_recogidos == 0:
                # Si solo tenemos pacientes C en el bus y solo quedan por recoger
                # Pacientes de tipo N en el mapa, primero tenemos que dejar a los C y luego ir a por los N
                # La heurística será la ruta indice_actual -> CC -> NC -> P más rentable más
                # la cantidad de pacientes N que queden por recoger.
                # Al resultado final le restamos 8 (como máximo) porque en el mejor de los casos,
                # puede haber cogido 8 pacientes N de los que quedaban restantes por el mapa en el trayecto
                # que hace desde la posicion actual hasta NC (pasando por CC, claro)

                distancia_mas_rentable = -1
                distancia_pos_actual_cn_mas_rentable = None
                for cc in centros_cc.keys():
                    for nc in centros_nc.keys():
                        distancia_pos_actual_cn = self.distanciaMan(indice_actual, cc) + self.distanciaMan(cc, nc)
                        posibilidad = distancia_pos_actual + self.distanciaMan(nc, self.pos_parking)
                        if distancia_mas_rentable == -1:
                            distancia_mas_rentable = posibilidad
                            distancia_pos_actual_cn_mas_rentable = distancia_pos_actual
                        elif posibilidad < distancia_mas_rentable:
                            distancia_mas_rentable = posibilidad
                            distancia_pos_actual_cn_mas_rentable = distancia_pos_actual
                return distancia_mas_rentable + max(pacientes_n_por_recoger - max(distancia_pos_actual_cn_mas_rentable, 8), 0)

            elif num_C_recogidos != 0 and num_N_recogidos != 0: ...

        # Si solamente quedan pacientes C por recoger
        elif pacientes_c_por_recoger != 0 and pacientes_n_por_recoger == 0: ...

        # Si quedan tanto C como N por recoger en el mapa
        elif pacientes_c_por_recoger != 0 and pacientes_n_por_recoger != 0: ...


    def entidadMasCercana(self, indice: tuple, tipo: str) -> tuple:
        """
        Devuelve el índice de la entidad más cercana desde "indice" hasta "tipo".
        Por ejemplo, si indice = (1,1) y tipo = 'CC', devuelve el indice (i, j) del
        CC más cercano a (1,1).
        """
        entidades = {}
        mas_cercano = None
        i = 0
        while i < self.num_filas:
            j = 0
            while j < self.num_columnas:
                if self.mapa[i][j] == tipo:
                    distancia = self.distanciaMan((i, j), indice)
                    entidades[(i, j)] = distancia
                    if mas_cercano is None:
                        mas_cercano = (i, j)
                    elif distancia < entidades[mas_cercano]:
                        mas_cercano = (i, j)
                j += 1
            i += 1

        return mas_cercano

    def h3(self) -> int:
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
        # Inicializamos el cronómetro
        inicio_contador = time.time()
        
        # Lista ABIERTA: elementos ordenados por mejor función de evaluación,
        # estados pendientes de expandir
        # Elementos de ABIERTA: 
        # [((i, j), energía, num_C, num_N, restantes, mapa_actual), coste, heuristica, puntero_padre]
        ABIERTA = []
        # Lista CERRADA: elementos ya expandidos
        # Elementos de CERRADA: 
        # [((i, j), energía, num_C, num_N, restantes, mapa_actual), coste, heuristica, puntero_padre]
        CERRADA = []

        # Iniciamos algorítmo con el estado inicial
        if num_h == 1:
            ABIERTA.append((self.estado_inicial, 0, self.h1(self.estado_inicial), None))
        elif num_h == 2:
            pass
        else:
            ABIERTA.append((self.estado_inicial, 0, self.h3(), None))

        # Hasta que ABIERTA esté vacía o ÉXITO
        EXITO = False
        caca = 0
        while (len(ABIERTA) > 0) and (not EXITO):
            # Quitamos primer elemento de ABIERTA y lo metemos en CERRADA
            estado_a_expandir = ABIERTA.pop(0)
  
            # Por limpieza de código, extraemos la información
            tupla_estado = estado_a_expandir[0]
            celda = estado_a_expandir[0][0]
            energia_padre = estado_a_expandir[0][1]
            num_C = estado_a_expandir[0][2]
            num_N = estado_a_expandir[0][3]
            restantes = estado_a_expandir[0][4]
            coste_padre = estado_a_expandir[1]

            # Si el estado a expandir es final, entonces ÉXITO
            # (celda) = (celda_parking) y energía > 1 y num_C = 0 y num_N = 0 y restantes = 0
            if (celda == self.pos_parking) and (energia_padre > 1) and (num_C == 0) and (num_N == 0) and \
                (restantes == 0):
                    CERRADA.append(estado_a_expandir)
                    EXITO = True
                    final_contador = time.time()

            # Si no, antes de meter el estado en CERRADA y expandirlo, comprobamos si ya
            # se encuentra en CERRADA para evitar reexpansiones
            expandir = True
            for estado_en_cerrada in CERRADA:
                if tupla_estado in estado_en_cerrada:
                    # Si está comprobamos cuál es mejor de los dos
                    if self.f(estado_a_expandir) < self.f(estado_en_cerrada):
                        # Metemos nuevo estado y eliminamos el anterior
                        CERRADA.remove(estado_en_cerrada)
                        CERRADA.append(estado_a_expandir)
                        # Reecalculamos los costes, ya que ahora tenemos un camino
                        # mejor para llegar al estado en cuestión
                        for estado_en_abierta in ABIERTA:
                            # Modificamos los estados cuyo padre sea el estado añadido
                            if tupla_estado == estado_en_abierta[3][0]:
                                # Coste hijo = coste llegar nuevo padre + el suyo (el de antes - 
                                # el del padre anterior)
                                estado_en_abierta[1] = coste_padre + (estado_en_abierta[1] - estado_en_cerrada[1])
                                # Puntero al padre = puntero al nuevo padre
                                estado_en_abierta[3] = tupla_estado
                                # Modificamos la energía, el num_C, el num_N, los restantes y el mapa
                                # haciendo uso del operador correspondiente
                                celda_hijo = estado_en_abierta[0][0]
                                celda_padre = celda
                                # El hijo está a la derecha del padre: j_h > j_p
                                if (celda_hijo[1] > celda_padre[1]):
                                    estado_en_abierta[0] = self.MoverDcha(tupla_estado)
                                # El hijo está a la izquierda del padre: j_h < j_p
                                elif (celda_hijo[1] < celda_padre[1]):
                                    estado_en_abierta[0] = self.MoverIzq(tupla_estado)
                                # El hijo está a la arriba del padre: i_h < i_p
                                elif (celda_hijo[0] < celda_padre[0]):
                                    estado_en_abierta[0] = self.MoverArriba(tupla_estado)
                                # El hijo está a debajo del padre: i_h > i_p
                                elif (celda_hijo[0] > celda_padre[0]):
                                    estado_en_abierta[0] = self.MoverAbajo(tupla_estado)
                                
                    # Marcamos que no hay que reexpandir
                    expandir = False
                    break

            if expandir:
                CERRADA.append(estado_a_expandir)
                # Si no, expandimos el estado y añademos sus sucesores a ABIERTA
                # ordenados por su función de evaluación f
                sucesor_1 = self.MoverDcha(tupla_estado)
                sucesor_2 = self.MoverIzq(tupla_estado)
                sucesor_3 = self.MoverArriba(tupla_estado)
                sucesor_4 = self.MoverAbajo(tupla_estado)
                if (sucesor_1):
                    # Coste para llegar al sucesor: coste_padre + coste_hijo
                    # coste_hijo = energia_restante_padre - energia_restante_hijo 
                    energia_hijo = sucesor_1[1]
                    # Para evitar ciclos negativos al volver al parking y recargar la energía:
                    coste_hijo = max(energia_padre - energia_hijo, 1)
                    if num_h == 1:
                        ABIERTA.append((sucesor_1, coste_padre+coste_hijo, self.h1(sucesor_1), tupla_estado)) 
                    elif num_h == 2:
                        pass
                    else:
                        ABIERTA.append((sucesor_1, coste_padre+coste_hijo, self.h3(), tupla_estado))                       
                if (sucesor_2):
                    # Coste para llegar al sucesor: coste_padre + coste_hijo
                    # coste_hijo = energia_restante_padre - energia_restante_hijo 
                    energia_hijo = sucesor_2[1]
                    # Para evitar ciclos negativos al volver al parking y recargar la energía:
                    coste_hijo = max(energia_padre - energia_hijo, 1)
                    if num_h == 1:
                        ABIERTA.append((sucesor_2, coste_padre+coste_hijo, self.h1(sucesor_2), tupla_estado)) 
                    elif num_h == 2:
                        pass
                    else:
                        ABIERTA.append((sucesor_2, coste_padre+coste_hijo, self.h3(), tupla_estado)) 
                if (sucesor_3):
                    # Coste para llegar al sucesor: coste_padre + coste_hijo
                    # coste_hijo = energia_restante_padre - energia_restante_hijo 
                    energia_hijo = sucesor_3[1]
                    # Para evitar ciclos negativos al volver al parking y recargar la energía:
                    coste_hijo = max(energia_padre - energia_hijo, 1)
                    if num_h == 1:
                        ABIERTA.append((sucesor_3, coste_padre+coste_hijo, self.h1(sucesor_3), tupla_estado)) 
                    elif num_h == 2:
                        pass
                    else:
                        ABIERTA.append((sucesor_3, coste_padre+coste_hijo, self.h3(), tupla_estado)) 
                if (sucesor_4):
                    # Coste para llegar al sucesor: coste_padre + coste_hijo
                    # coste_hijo = energia_restante_padre - energia_restante_hijo 
                    energia_hijo = sucesor_4[1]
                    # Para evitar ciclos negativos al volver al parking y recargar la energía:
                    coste_hijo = max(energia_padre - energia_hijo, 1)
                    if num_h == 1:
                        ABIERTA.append((sucesor_4, coste_padre+coste_hijo, self.h1(sucesor_4), tupla_estado)) 
                    elif num_h == 2:
                        pass
                    else:
                        ABIERTA.append((sucesor_4, coste_padre+coste_hijo, self.h3(), tupla_estado)) 
                
                # Ordenamos la lista por función de evaluación
                ABIERTA.sort(key=self.f)
                if (caca == 4):
                    print(ABIERTA)
                caca+=1
        
        if EXITO:
            # El último estado de la lista CERRADA será siempre el estado final 
            # de la solución.
            estado_final = CERRADA[-1]
            solucion = [estado_final]
            # Recuperamos la solución yendo a la inversa, siguiendo los 
            # punteros padre
            # Hasta encontrar estado inicial = ((pos_parking, 50, 0, 0, todos_restantes))
            while (solucion[0][0][0] != self.pos_parking) or (solucion[0][0][1] != 50) or \
                  (solucion[0][0][2] != 0) or (solucion[0][0][3] != 0) or \
                  (solucion[0][0][4] != self.todos_los_pacientes): 
                # Obtenemos el puntero del padre del primer elemento, que es siguiente
                # a encontrar su padre
                current_puntero_padre = solucion[0][3]
                # Buscamos el elemento correspondiente en la lista CERRADA
                for elem in CERRADA:
                    if elem[0] == current_puntero_padre:
                        solucion.insert(0, elem)
                        break
            
            tiempo_total = round(final_contador - inicio_contador, 4)
            self.generar_solucion_output(solucion)
            # Le pasamos la solución para obtener el coste total, le pasamos el tiempo total
            # ya calculado, la longitud del plan que es la longitud de la lista que contiene la
            # solución y el número de nodos expandidos que es la longitud de la lista CERRADA
            self.generar_estadisticas_stat(solucion, tiempo_total, len(solucion), len(CERRADA))

        return EXITO
    
    def generar_solucion_output(self, solucion: list):
        """
        Generamos un fichero .output en el que definimos el orden que ha seguido el 
        algoritmo para encontrar la solución. Contiene una línea por casilla transitada con el siguiente
        formato: (x,y):valor:carga, donde x es el numero de fila en el mapa, y el de columna, valor
        el coste o tipo de celda (N, C, CC, CN o P) según el caso y carga el valor de carga que le queda al
        vehículo en ese momento. 
        """
        cadena = ''
        for elem in solucion: 
            posicion = elem[0][0]
            tipo_celda = self.mapa[posicion[0]-1][posicion[1]-1]
            carga_restante = elem[0][1]
            cadena += str(posicion) + ':' + tipo_celda + ':' + str(carga_restante) + '\n'

        with open(self.ruta_output, mode='w') as file: 
            file.write(cadena)
            
    
    def generar_estadisticas_stat(self, solucion: list, tiempo_total, longitud_del_plan, nodos_expandidos):
        """
        Generamos un fichero .stat que contiene informacion relativa al proceso de búsqueda, como el
        tiempo total, coste total, longitud de la solución y los nodos expandidos. 
        """
        tiempo = 'Tiempo total: ' + str(tiempo_total) + '\n'
        coste = 'Coste total: ' + str(solucion[-1][1]) + '\n'
        longitud = 'Longitud del plan: ' + str(longitud_del_plan) + '\n'
        expandidos = 'Nodos expandidos: ' + str(nodos_expandidos)

        with open(self.ruta_stat, mode='w') as file: 
            file.write(tiempo)
            file.write(coste)
            file.write(longitud)
            file.write(expandidos)



if __name__ == "__main__":   
    
    if len(sys.argv) != 3:
        raise ValueError("\n"+'\033[91m'+"Es necesario especificar un archivo csv y un número como argumento" + '\033[0m')
    
    Parte2(sys.argv[1], sys.argv[2])
