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
            print('\033[32m'+"EL PROBLEMA TIENE SOLUCIÓN REPRESENTADA EN " + self.ruta_output +
                  "\n\n" + "CUYAS ESTADÍSTICAS SE ENCUENTRAN EN " + self.ruta_stat + "\n" + '\033[0m')
        else:
            print('\033[93m'+"EL PROBLEMA NO TIENE SOLUCIÓN \n" + '\033[0m')


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

    def h1(self, estado: tuple) -> float:
        """
        Esta heurística tiene en cuenta la energía restante y el número de pacientes pendientes. 
        La distancia manhattan entre la posición actual y el próximo paciente por recoger/dejar se 
        pondera con la energía restante, para considerar la capacidad del vehículo y la necesidad de recargar.

        La distancia manhattan asegura que se esté avanzando hacia el siguiente paciente, y la ponderación 
        por la energía garantiza que se tenga en cuenta la capacidad y la necesidad de recarga del vehículo.
        Además, agregar el número de pacientes pendientes mejora la eficiencia al dar prioridad a las paradas 
        con más pacientes por recoger o dejar (=pacientes_pendientes).

        h1 = distanciaMan((i,j),próximo paciente)*(1+(energía_restante/energía_máxima))+pacientes_pendientes
        """
        indice_actual = estado[0]
        energia_actual = estado[1]
        pacientes_restantes_por_dejar = estado[4]
        mapa_estado = estado[5]
        # Estado ((i, j), energía, num_C, num_N, pacientes_restantes_por_dejar, mapa)

        # Calculamos el número de pacientes que queda por recoger
        pacientes_restantes_por_recoger = 0
        for fila in mapa_estado:
            for celda in fila:
                if celda == 'C':
                    pacientes_restantes_por_recoger += 1
                elif celda == 'N':
                    pacientes_restantes_por_recoger += 1
        
        # Si no quedan pacientes por recoger en el mapa, la heurística será 
        # (1+(energía_restante/energía_máxima))+pacientes_pendientes
        if pacientes_restantes_por_recoger == 0:
            return (1+(energia_actual/50)) + pacientes_restantes_por_dejar
        # Si quedan pacientes por recoger en el mapa, la heurística será
        # distanciaMan((i,j),próximo paciente)*(1+(energía_restante/energía_máxima))+pacientes_pendientes
        else:
            # Calculamos la distancia hasta el paciente más cercano:
            c_mas_cercano = self.entidadMasCercana(indice_actual, 'C')
            if c_mas_cercano:
                posibilidad_c = self.distanciaMan(indice_actual, c_mas_cercano)
            
            n_mas_cercano = self.entidadMasCercana(indice_actual, 'N')
            if n_mas_cercano:
                posibilidad_n = self.distanciaMan(indice_actual, n_mas_cercano)
            
            if c_mas_cercano and n_mas_cercano:
                paciente_mas_cercano = min(posibilidad_c, posibilidad_n)
            elif c_mas_cercano:
                paciente_mas_cercano = posibilidad_c
            elif n_mas_cercano:
                paciente_mas_cercano = posibilidad_n

            # La heurística será la distancia al paciente más cercano ponderada por la energía restante
            # más los pacientes que quedan por dejar
            return (paciente_mas_cercano*(1+(energia_actual/50))) + pacientes_restantes_por_dejar
            

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


    
    def h2(self, estado: tuple) -> int:
        """
        Heurística que dado un estado, devuelve el camino mínimo usando la distancia Manhatan
        (sin tener en cuenta los costes y las paredes, coste unitario siempre) que debería hacer 
        el bus para dejar y recoger pacientes en el centro más cercano. O volver al parking en 
        caso de que no queden pacientes por dejar. Es decir, primero buscamos el centro que yendo
        desde estado y del centro al parking su distancia sea la menor (para no sobreestimar). Luego,
        vemos si del estado a ese centro se puede recoger a pacientes. Si se puede pero son más de 10,
        solo se recoge a diez antes del centro. Si se puede pero al dejarlos en el centro siguen quedando 
        pacientes, se le sumará a la heurística ese número de pacientes, ya que como mínimo el autobús 
        debería hacer un viaje para recoger a los restantes.


        Si restantes = 0 -> h2(estado) = distanciaMan(a P)
        Si restantes > 0 -> h2(estado) = distanciaMan(a CENTRO <el más rentable>) +
                                         distanciaMan(a P desde ese CENTRO) + 
                                         (pacientes_que_quedan_por_recoger - 
                                         pacientes_que_puedes_recoger_en_el_trayecto_al_centro)                          
        """    

        indice_actual = estado[0]
        num_C_recogidos = estado[2]
        num_N_recogidos = estado[3]
        pacientes_restantes_por_dejar = estado[4]
        mapa_estado = estado[5]

        if pacientes_restantes_por_dejar == 0:
            return self.distanciaMan(indice_actual, self.pos_parking)
        else:
            # Calculamos el número de pacientes que queda por recoger
            pacientes_restantes_por_recoger = 0
            for fila in mapa_estado:
                for celda in fila:
                    if celda == 'C':
                        pacientes_restantes_por_recoger += 1
                    elif celda == 'N':
                        pacientes_restantes_por_recoger += 1

            # Calculamos pacientes que quedan por dejar en sus centros
            quedan_por_recoger = max(pacientes_restantes_por_recoger - (num_C_recogidos + num_N_recogidos), 0)
            
            # Calculamos la distancia Manhattan desde donde estamos 
            # hasta cualquier centro en el mapa
            distancia_centros = {}
            i = 0
            while i < self.num_filas:
                j = 0
                while j < self.num_columnas:
                    if self.mapa[i][j] == 'CC' or self.mapa[i][j] == 'CN':
                        distancia_centros[(i, j)] = self.distanciaMan(indice_actual, (i, j))
                    j += 1
                i+=1

            # Calculamos cuál es la distancia más rentable desde
            # posicion_actual -> centro -> parking 
            min_distancia_pos_centro_parking = None
            min_distancia_pos_centro = None
            for centro in distancia_centros.keys():
                distancia_pos_centro = distancia_centros[centro]
                distancia_centro_parking = self.distanciaMan(centro, self.pos_parking)
                posibilidad = distancia_pos_centro + distancia_centro_parking
                if min_distancia_pos_centro_parking is None:
                    min_distancia_pos_centro_parking = posibilidad
                    min_distancia_pos_centro = distancia_pos_centro
                elif posibilidad < min_distancia_pos_centro_parking:
                    min_distancia_pos_centro_parking = posibilidad
                    min_distancia_pos_centro = distancia_pos_centro

            # La heurística devolverá la distancia más rentable desde la posición actual hasta el parking (pasando
            # por el centro más rentable) más los pacientes que quedan por recoger, teniendo en cuenta que
            # en el trayecto desde la posición actual hasta el centro más rentable se pueden recoger pacientes
            # (de ahí la parte --- quedan_por_recoger - min(min_distancia_pos_centro, 10) ---)
            return min_distancia_pos_centro_parking + max(quedan_por_recoger - min(min_distancia_pos_centro, 10), 0)
            

    def distanciaMan(self, indice1: tuple, indice2: tuple) -> int:
        """
        Distancia Manhattan entre dos elementos del mapa dados sus índices
        (suponiendo costes unitarios).
        """
        diferencia_filas = abs(indice1[0] - indice2[0])
        diferencia_columnas = abs(indice1[1] - indice2[1])
        return abs(diferencia_filas - diferencia_columnas)
        
   
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
            ABIERTA.append((self.estado_inicial, 0, self.h2(self.estado_inicial), None))
        else:
            ABIERTA.append((self.estado_inicial, 0, self.h3(), None))

        # Hasta que ABIERTA esté vacía o ÉXITO
        EXITO = False
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
                        ABIERTA.append((sucesor_1, coste_padre+coste_hijo, self.h2(sucesor_1), tupla_estado)) 
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
                        ABIERTA.append((sucesor_2, coste_padre+coste_hijo, self.h2(sucesor_2), tupla_estado)) 
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
                        ABIERTA.append((sucesor_3, coste_padre+coste_hijo, self.h2(sucesor_3), tupla_estado)) 
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
                        ABIERTA.append((sucesor_4, coste_padre+coste_hijo, self.h2(sucesor_4), tupla_estado)) 
                    else:
                        ABIERTA.append((sucesor_4, coste_padre+coste_hijo, self.h3(), tupla_estado)) 
                
                # Ordenamos la lista por función de evaluación
                ABIERTA.sort(key=self.f)
        
        final_contador = time.time()
        tiempo_total = round(final_contador - inicio_contador, 4)

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
            
            self.generar_solucion_output(solucion)
            # Le pasamos la solución para obtener el coste total, le pasamos el tiempo total
            # ya calculado, la longitud del plan que es la longitud de la lista que contiene la
            # solución y el número de nodos expandidos que es la longitud de la lista CERRADA
            self.generar_estadisticas_stat(solucion, tiempo_total, len(solucion), len(CERRADA))
        else:
            # Si no hay solución, sacamos el fichero .output y las .stat
            # idnicando que no tiene solución
            self.generar_fichero_output_sin_sol()
            self.generar_estadisticas_stat_sin_sol(tiempo_total, len(CERRADA))

        return EXITO
    
    def generar_estadisticas_stat_sin_sol(self, tiempo_total, nodos_expandidos):
        """
        Generamos un fichero .stat que contiene informacion relativa al proceso de 
        búsqueda en el problema SIN solución, como el tiempo total, coste total, 
        longitud de la solución y los nodos expandidos. 
        """
        tiempo = 'Tiempo total: ' + str(tiempo_total) + '\n'
        coste = 'Coste total: inf' + '\n'
        longitud = 'Longitud del plan: inf' + '\n'
        expandidos = 'Nodos expandidos: ' + str(nodos_expandidos)

        with open(self.ruta_stat, mode='w') as file: 
            file.write(tiempo)
            file.write(coste)
            file.write(longitud)
            file.write(expandidos)

    def generar_fichero_output_sin_sol(self):
        """
        Generamos un fichero .output en el que indicamos que no hay solución.
        """
        with open(self.ruta_output, mode='w') as file: 
            file.write('NO HAY SOLUCIÓN')
    
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
