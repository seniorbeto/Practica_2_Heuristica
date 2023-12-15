#!/bin/bash
espacio=" "
CYAN='\033[1;96m'
AMARILLO='\033[1;93m'
NC='\033[0m' # No Color
h1="h1: "
h2="h2: "
h3="h3: "

# Prueba 1: No tiene solución, una fila y no puedes llegar al parking
# antes de quedarte sin energía
msg="-- PRUEBA 1: No tiene solución, una fila y no puedes llegar al parking antes de quedarte sin energía --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
echo "$h1"
python3 ASTARTraslados.py ./ASTAR-tests/1_no_sol_una_fila.csv 1
echo "$h2"
python3 ASTARTraslados.py ./ASTAR-tests/1_no_sol_una_fila.csv 2
echo "$h3"
python3 ASTARTraslados.py ./ASTAR-tests/1_no_sol_una_fila.csv 3

# Prueba 2: No tiene solución, nada más salir del parkiing coste 49
msg="-- PRUEBA 2: No tiene solución, nada más salir del parkiing coste 49 --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
echo "$h1"
python3 ASTARTraslados.py ./ASTAR-tests/2_no_sol_coste_alto.csv 1
echo "$h2"
python3 ASTARTraslados.py ./ASTAR-tests/2_no_sol_coste_alto.csv 2
echo "$h3"
python3 ASTARTraslados.py ./ASTAR-tests/2_no_sol_coste_alto.csv 3

# Prueba 3: No tiene solución, un único paciente C cuyo centro CC es inaccesible
msg="-- PRUEBA 3: No tiene solución, un único paciente C cuyo centro CC es inaccesible --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
echo "$h1"
python3 ASTARTraslados.py ./ASTAR-tests/3_no_sol_cc_inaccesible.csv 1
echo "$h2"
python3 ASTARTraslados.py ./ASTAR-tests/3_no_sol_cc_inaccesible.csv 2
echo "$h3"
python3 ASTARTraslados.py ./ASTAR-tests/3_no_sol_cc_inaccesible.csv 3

# Prueba 4: No tiene solución, un pacientes N cuyo centro CN es inaccesible
msg="-- PRUEBA 4: No tiene solución, un pacientes N cuyo centro CN es inaccesible --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
echo "$h1"
python3 ASTARTraslados.py ./ASTAR-tests/4_no_sol_cn_inaccesible.csv 1
echo "$h2"
python3 ASTARTraslados.py ./ASTAR-tests/4_no_sol_cn_inaccesible.csv 2
echo "$h3"
python3 ASTARTraslados.py ./ASTAR-tests/4_no_sol_cn_inaccesible.csv 3

# Prueba 5: No hay pacientes que dejar, estado inicial = final
msg="-- PRUEBA 5: No hay pacientes que dejar, estado inicial = final --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
echo "$h1"
python3 ASTARTraslados.py ./ASTAR-tests/5_sin_pacientes.csv 1
echo "$h2"
python3 ASTARTraslados.py ./ASTAR-tests/5_sin_pacientes.csv 2
echo "$h3"
python3 ASTARTraslados.py ./ASTAR-tests/5_sin_pacientes.csv 3


# Prueba 6: Hay más de 10 pacientes N
msg="-- PRUEBA 6: Hay más de 10 pacientes N --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
echo "$h1"
python3 ASTARTraslados.py ./ASTAR-tests/6_mas_10_pacientes_n.csv 1
echo "$h2"
python3 ASTARTraslados.py ./ASTAR-tests/6_mas_10_pacientes_n.csv 2
echo "$h3"
python3 ASTARTraslados.py ./ASTAR-tests/6_mas_10_pacientes_n.csv 3

# Prueba 7: Hay más de 2 pacientes C
msg="-- PRUEBA 7: Hay más de 2 pacientes C --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
echo "$h1"
python3 ASTARTraslados.py ./ASTAR-tests/7_mas_2_pacientes_c.csv 1
echo "$h2"
python3 ASTARTraslados.py ./ASTAR-tests/7_mas_2_pacientes_c.csv 2
echo "$h3"
python3 ASTARTraslados.py ./ASTAR-tests/7_mas_2_pacientes_c.csv 3

# Prueba 8: Obligatoriamente se coge un C primero, y hay
# 1 N y 1 C más
msg="-- PRUEBA 8: Obligatoriamente se coge un C primero, y hay 1 N y 1 C más --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
echo "$h1"
python3 ASTARTraslados.py ./ASTAR-tests/8_c_primero.csv 1
echo "$h2"
python3 ASTARTraslados.py ./ASTAR-tests/8_c_primero.csv 2


# Prueba 9: Obligatoriamente se coge un N primero, y hay
# 3 N's y 1 C más
msg="-- PRUEBA 9: Obligatoriamente se coge un N primero, y hay 3 N's y 1 C más --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
echo "$h1"
python3 ASTARTraslados.py ./ASTAR-tests/9_n_primero.csv 1
echo "$h2"
python3 ASTARTraslados.py ./ASTAR-tests/9_n_primero.csv 2
echo "$h3"
python3 ASTARTraslados.py ./ASTAR-tests/9_n_primero.csv 3

# Prueba 10: 8 N's y 2 C's seguidas
msg="-- PRUEBA 10: 8 N's y 2 C's seguidas --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
echo "$h1"
python3 ASTARTraslados.py ./ASTAR-tests/10_8_n_2_c_seguidos.csv 1
echo "$h2"
python3 ASTARTraslados.py ./ASTAR-tests/10_8_n_2_c_seguidos.csv 2
echo "$h3"
python3 ASTARTraslados.py ./ASTAR-tests/10_8_n_2_c_seguidos.csv 3

# Prueba 11: 9 N's y 2 C's seguidas
msg="-- PRUEBA 11: 9 N's y 2 C's seguidas --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
echo "$h1"
python3 ASTARTraslados.py ./ASTAR-tests/11_9_n_2_c_seguidos.csv 1
echo "$h2"
python3 ASTARTraslados.py ./ASTAR-tests/11_9_n_2_c_seguidos.csv 2
echo "$h3"
python3 ASTARTraslados.py ./ASTAR-tests/11_9_n_2_c_seguidos.csv 3

# Prueba 12: 8 N's y 3 C's seguidas
msg="-- PRUEBA 12: 8 N's y 3 C's seguidas --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
echo "$h1"
python3 ASTARTraslados.py ./ASTAR-tests/12_8_n_3_c_seguidos.csv 1
echo "$h2"
python3 ASTARTraslados.py ./ASTAR-tests/12_8_n_3_c_seguidos.csv 2

# Prueba 13: Alguna celda con mucho coste, debe rodear
msg="-- PRUEBA 13: Alguna celda con mucho coste, debe rodear --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
echo "$h1"
python3 ASTARTraslados.py ./ASTAR-tests/13_celda_gran_coste.csv 1
echo "$h2"
python3 ASTARTraslados.py ./ASTAR-tests/13_celda_gran_coste.csv 2
echo "$h3"
python3 ASTARTraslados.py ./ASTAR-tests/13_celda_gran_coste.csv 3

# Prueba 14: Hay más de un CC, debe ir por el óptimo
msg="-- PRUEBA 14: Hay más de un CC, debe ir por el óptimo --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
echo "$h1"
python3 ASTARTraslados.py ./ASTAR-tests/14_mas_de_un_cc.csv 1
echo "$h2"
python3 ASTARTraslados.py ./ASTAR-tests/14_mas_de_un_cc.csv 2
echo "$h3"
python3 ASTARTraslados.py ./ASTAR-tests/14_mas_de_un_cc.csv 3

# Prueba 15: Hay más de un CN, debe ir por el óptimo
msg="-- PRUEBA 15: Hay más de un CN, debe ir por el óptimo --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
echo "$h1"
python3 ASTARTraslados.py ./ASTAR-tests/15_mas_de_un_cn.csv 1
echo "$h2"
python3 ASTARTraslados.py ./ASTAR-tests/15_mas_de_un_cn.csv 2
echo "$h3"
python3 ASTARTraslados.py ./ASTAR-tests/15_mas_de_un_cn.csv 3

# Prueba 16: Hay más de un CN y un CC, debe ir por los óptimos
msg="-- PRUEBA 16: Hay más de un CN y un CC, debe ir por los óptimo --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
echo "$h1"
python3 ASTARTraslados.py ./ASTAR-tests/16_mas_de_un_cn_y_un_cc.csv 1
echo "$h2"
python3 ASTARTraslados.py ./ASTAR-tests/16_mas_de_un_cn_y_un_cc.csv 2
echo "$h3"
python3 ASTARTraslados.py ./ASTAR-tests/16_mas_de_un_cn_y_un_cc.csv 3

# Prueba 17: Caso más normal, 1 CC, 1 CN, 2 N's, 2 C's
msg="-- PRUEBA 17: 1 CC, 2 CN, 4 N's, 2 C's --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
echo "$h1"
python3 ASTARTraslados.py ./ASTAR-tests/17_normal.csv 1
echo "$h2"
python3 ASTARTraslados.py ./ASTAR-tests/17_normal.csv 2
echo "$h3"
python3 ASTARTraslados.py ./ASTAR-tests/17_normal.csv 3