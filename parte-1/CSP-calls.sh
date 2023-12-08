#!/bin/bash
espacio=" "
CYAN='\033[1;96m'
NC='\033[0m' # No Color

# Prueba 1: No se especifica ningún argumento
msg="-- PRUEBA 1: No se especifica ningún argumento --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py

# Prueba 2: La ruta de argumento no es válida
msg="-- PRUEBA 2: La ruta de argumento no es válida --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/

# Prueba 3: El número de filas del archivo de entrada no es un entero
msg="-- PRUEBA 3: El número de filas del archivo de entrada no es un entero --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/1_NV_filas_no_entero.txt

# Prueba 4: El número de filas del parking debe ser un entero positivo
msg="-- PRUEBA 4: El número de filas del archivo de entrada no es un entero positivo --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/2_NV_filas_no_positivo.txt

# Prueba 5: El número de columnas del archivo de entrada no es un entero
msg="-- PRUEBA 5: El número de columnas del archivo de entrada no es un entero --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/3_NV_columnas_no_entero.txt

# Prueba 6: El número de columnas del parking debe ser un entero positivo.
msg="-- PRUEBA 6: El número de columnas del archivo de entrada no es un entero positivo --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/4_NV_columnas_no_positivo.txt

# Prueba 7: La definición de las plazas eléctricas no empieza por "PE:"
msg="-- PRUEBA 7: La definición de las plazas eléctricas no empieza por 'PE:' --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/5_NV_no_PE_antes_def_pe.txt

# Prueba 8: La declaración de las plazas eléctricas no sigue el formato
# (i,j)(i',j')(i'',j'')...: No tienen '('
msg="-- PRUEBA 8: La definición de las plazas eléctricas no tiene '(' --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/6_NV_formato_incorrecto_pe_parentesis_izq.txt

# Prueba 9: La declaración de las plazas eléctricas no sigue el formato
# (i,j)(i',j')(i'',j'')...: Filas no entero
msg="-- PRUEBA 9: La definición de las filas de las PE no es un entero --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/7_NV_formato_incorrecto_pe_filas_no_entero.txt

# Prueba 10: La declaración de las plazas eléctricas no sigue el formato
# (i,j)(i',j')(i'',j'')...: No tienen ','
msg="-- PRUEBA 10: La definición de las PE no tiene una ',' --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/8_NV_formato_incorrecto_pe_coma.txt

# Prueba 11: La declaración de las plazas eléctricas no sigue el formato
# (i,j)(i',j')(i'',j'')...: Columnas no entero
msg="-- PRUEBA 11: La definición de las columnas de las PE no es un entero --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/9_NV_formato_incorrecto_pe_colum_no_entero.txt

# Prueba 12: La declaración de las plazas eléctricas no sigue el formato
# (i,j)(i',j')(i'',j'')...: No tienen ')'
msg="-- PRUEBA 12: La definición de las PE no tiene ')' --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/10_NV_formato_incorrecto_pe_parentesis_dcho.txt

# Prueba 13: Las plazas enchufables definidas no se encuentran dentro del dominio
msg="-- PRUEBA 13: Las plazas enchufables definidas no se encuentran dentro del dominio --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/11_NV_def_pe_fuera_dominio.txt

# Prueba 14: Las definición de los vehículos no sigue el formato ID(int)-TIPO(TSU o TNU)-
# CONGELADOR(C o X)
msg="-- PRUEBA 14: Las definición de los vehículos no sigue el formato ID(int)-TIPO(TSU o TNU)-CONGELADOR(C o X) --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/12_NV_formato_incorrecto_def_vehiculos.txt

# Prueba 15: Las definición del ID del vehiculo no es entero
msg="-- PRUEBA 15: ID del vehiculo no es entero --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/13_NV_id_no_entero_def_vehiculos.txt

# Prueba 16: Tipo del vehiculo no es 'TSU' o 'TNU'
msg="-- PRUEBA 16: Tipo del vehiculo no es 'TSU' o 'TNU' --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/14_NV_tipo_no_valido_def_vehiculos.txt

# Prueba 17: En la definición de los vehículos no se especifica correctamente si 
# tiene congelador o no (C o X)
msg="-- PRUEBA 17: No se especifica correctamente si tiene congelador o no --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/15_NV_congelador_no_valido_def_vehiculos.txt

# Prueba 18: El ID de un vehículo debe ser único
msg="-- PRUEBA 18: El ID de un vehículo debe ser único --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/16_NV_id_vehiculo_no_unico.txt

# Prueba 19: El problema no tiene solución porque hay más coches que plazas
# Restricción 2: Dos vehículos distintos no pueden ocupar la misma plaza
msg="-- PRUEBA 19: El problema no tiene solución porque hay más coches que plazas --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/17_V_problema_sin_sol_mas_coches_que_plazas.txt

# Prueba 20: El problema no tiene solución porque no hay suficientes plazas eléctricas
# Restricción 3:  Los vehículos provistos de congelador solo pueden ocupar plazas enchufables 
msg="-- PRUEBA 20: El problema no tiene solución porque no hay suficientes plazas eléctricas --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/18_V_problema_sin_sol_no_suficientes_pe.txt

# Prueba 21: El problema no tiene solución porque un TNU iría delante de un TSU
# Restricción 4:  Un vehículo de tipo TSU no puede tener aparcado por delante un TNU
msg="-- PRUEBA 21: El problema no tiene solución porque un TNU iría delante de un TSU --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/19_V_problema_sin_sol_TNU_delante_TSU.txt

# Prueba 22: El problema no tiene solución porque solo hay una fila, no maniobrable
# Restricción 5: Dentro del parking todo vehículo debe tener libre una plaza a izquierda o derecha
msg="-- PRUEBA 22: El problema no tiene solución porque solo hay una fila, no maniobrable --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/20_V_problema_sin_sol_una_fila.txt

# Prueba 23: El problema no tiene solución porque un vehículo no tiene una plaza libre a dcha o izq (1)
# Restricción 5: Dentro del parking todo vehículo debe tener libre una plaza a izquierda o derecha
msg="-- PRUEBA 23: El problema no tiene solución porque un vehículo no tiene una plaza libre a dcha o izq (1)--"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/21_V_problema_sin_sol_no_plaza_libre_lados_1.txt

# Prueba 24: El problema no tiene solución porque un vehículo no tiene una plaza libre a dcha o izq (2)
# Restricción 5: Dentro del parking todo vehículo debe tener libre una plaza a izquierda o derecha
msg="-- PRUEBA 24: El problema no tiene solución porque un vehículo no tiene una plaza libre a dcha o izq (2)--"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/22_V_problema_sin_sol_no_plaza_libre_lados_2.txt

# Prueba 25: El problema tiene 1 solución; 2x2, solo una PE, y un único vehículo con C
msg="-- PRUEBA 25: El problema tiene 1 solución; 2x2, solo una PE, y un único vehículo con C --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/23_V_problema_con_1_sol.txt
