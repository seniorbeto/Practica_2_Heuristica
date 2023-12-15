#!/bin/bash
espacio=" "
CYAN='\033[1;96m'
NC='\033[0m' # No Color



# Prueba 1: El problema no tiene solución porque hay más coches que plazas
# Restricción 2: Dos vehículos distintos no pueden ocupar la misma plaza
msg="-- PRUEBA 1: El problema no tiene solución porque hay más coches que plazas --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/1_V_problema_sin_sol_mas_coches_que_plazas.txt

# Prueba 2: El problema no tiene solución porque no hay suficientes plazas eléctricas
# Restricción 3:  Los vehículos provistos de congelador solo pueden ocupar plazas enchufables 
msg="-- PRUEBA 2: El problema no tiene solución porque no hay suficientes plazas eléctricas --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/2_V_problema_sin_sol_no_suficientes_pe.txt

# Prueba 3: El problema no tiene solución porque un TNU iría delante de un TSU
# Restricción 4:  Un vehículo de tipo TSU no puede tener aparcado por delante un TNU
msg="-- PRUEBA 3: El problema no tiene solución porque un TNU iría delante de un TSU --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/3_V_problema_sin_sol_TNU_delante_TSU.txt

# Prueba 4: El problema no tiene solución porque solo hay una fila, no maniobrable
# Restricción 5: Dentro del parking todo vehículo debe tener libre una plaza a izquierda o derecha
msg="-- PRUEBA 4: El problema no tiene solución porque solo hay una fila, no maniobrable --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/4_V_problema_sin_sol_una_fila.txt

# Prueba 5: El problema no tiene solución porque un vehículo no tiene una plaza libre a dcha o izq (1)
# Restricción 5: Dentro del parking todo vehículo debe tener libre una plaza a izquierda o derecha
msg="-- PRUEBA 5: El problema no tiene solución porque un vehículo no tiene una plaza libre a dcha o izq (1)--"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/5_V_problema_sin_sol_no_plaza_libre_lados_1.txt

# Prueba 6: El problema no tiene solución porque un vehículo no tiene una plaza libre a dcha o izq (2)
# Restricción 5: Dentro del parking todo vehículo debe tener libre una plaza a izquierda o derecha
msg="-- PRUEBA 6: El problema no tiene solución porque un vehículo no tiene una plaza libre a dcha o izq (2)--"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/6_V_problema_sin_sol_no_plaza_libre_lados_2.txt

# Prueba 7: El problema tiene 1 solución; 2x2, solo una PE, y un único vehículo con C
msg="-- PRUEBA 7: El problema tiene 1 solución; 2x2, solo una PE, y un único vehículo con C --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/7_V_problema_con_1_sol.txt

# Prueba 8: El problema tiene 2 soluciones; 3x1, una PE, dos vehículos sin congelador X
msg="-- PRUEBA 8: El problema tiene 2 soluciones; 3x1, una PE, dos vehículos sin congelador X --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/8_V_problema_con_2_sols.txt

# Prueba 9: El problema tiene 4 soluciones; 2x2, dos PE, un vehículo TNU con C y otro TSU con X
msg="-- PRUEBA 9: El problema tiene 4 soluciones; 2x2, dos PE, un vehículo TNU con C y otro TSU con X --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/9_V_problema_con_4_sols.txt

# Prueba 10: El problema tiene 6 soluciones; 2x2, dos PE, un vehículo TSU con X y otro TNU con X
msg="-- PRUEBA 10: El problema tiene 6 soluciones; 2x2, dos PE, un vehículo TSU con X y otro TNU con X --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/10_V_problema_con_6_sols.txt

# Prueba 11: El problema tiene 8 soluciones; 2x2, dos PE, dos vehículos TSU con X 
msg="-- PRUEBA 11: El problema tiene 8 soluciones; 2x2, dos PE, dos vehículos TSU con X --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/11_V_problema_con_8_sols.txt

# Prueba 12: El problema tiene 4*4=16 soluciones; 4x4, tres PE, un vehiculo TSU con X
msg="-- PRUEBA 12: El problema tiene 4*4=16 soluciones; 4x4, tres PE, un vehiculo TSU con X --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/12_V_problema_con_16_sols.txt

# Prueba 13: El problema tiene 5 soluciones; 4x4, cinco PE, un vehiculo TSU con C
msg="-- PRUEBA 13: El problema tiene 5 soluciones; 4x4, cinco PE, un vehiculo TSU con C --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/13_V_problema_con_5_sols.txt

# Prueba 14: El problema tiene 7*2+6=20 soluciones; 3x3, tres PE, un vehiculo TNU con C y un TSU con X
msg="-- PRUEBA 14: El problema tiene 7*2+6=20 soluciones; 3x3, tres PE, un vehiculo TNU con C y un TSU con X --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/14_V_problema_con_20_sols.txt

# Prueba 15: El problema tiene 164 soluciones; 4x5, cuatro PE, un vehiculo TNU con C, un TNU con X y un TSU con C
# NOTA: En este caso, no se muestran en el .csv las 164 soluciónes. En su lugar, se muestran 50 soluciones escogidas
# de forma aleatoria de entre esas 164. Es posible que alguna de las 50 soluciones esté repetida en el .csv.
msg="-- PRUEBA 15: El problema tiene 164 soluciones; 4x5, cuatro PE, un vehiculo TNU con C, un TNU con X y un TSU con C --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 CSPParking.py ./CSP-tests/15_V_problema_con_164_sols.txt

