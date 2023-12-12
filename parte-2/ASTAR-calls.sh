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
python3 ASTARTraslados.py

# Prueba 2: La ruta de argumento no es válida
msg="-- PRUEBA 2: La ruta de argumento no es válida --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 ASTARTraslados.py ./ASTAR-tests/

# Prueba 3: Sólo se especifica la ruta
msg="-- PRUEBA 3: Sólo se especifica la ruta --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 ASTARTraslados.py ./ASTAR-tests/mapa.csv

# Prueba 4: Sólo se especifica la heurística
msg="-- PRUEBA 4: Sólo se especifica la heurística --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 ASTARTraslados.py 1

# Prueba 5: Se especifica la ruta y la heurística pero ésta no es un valor entero
msg="-- PRUEBA 5: Se especifica la ruta y la heurística pero ésta no es un valor entero --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 ASTARTraslados.py ./ASTAR-tests/mapa.csv 2.1

# Prueba 6: Se especifica la ruta y la heurística pero ésta != 1 y != 2 y != 3
msg="-- PRUEBA 6: Se especifica la ruta y la heurística pero ésta != 1 y != 2 y != 3 --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 ASTARTraslados.py ./ASTAR-tests/mapa.csv 4

# Prueba 7: El mapa tiene algún valor no válido (disinto de 'C', 'N', 'P', 'CC', 'CN' o un entero)
msg="-- PRUEBA 7: El mapa tiene algún valor no válido (disinto de 'C', 'N', 'P', 'CC', 'CN' o un entero) --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 ASTARTraslados.py ./ASTAR-tests/1_NV_caracter_invalido.csv 3

# Prueba 8: El mapa no es rectangular
msg="-- PRUEBA 8: El mapa no es rectangular --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 ASTARTraslados.py ./ASTAR-tests/2_NV_mapa_no_rectangular.csv 3

# Prueba 9: El mapa tiene más de un parking
msg="-- PRUEBA 9: El mapa tiene más de un parking --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 ASTARTraslados.py ./ASTAR-tests/3_NV_mapa_mas_de_un_parking.csv 3

# Prueba 10: El mapa no tiene CC o CN
msg="-- PRUEBA 10: El mapa no tiene CC o CN --"
echo "$espacio"
echo "$espacio"
echo -e "${CYAN}$msg${NC}"
echo "$espacio"
python3 ASTARTraslados.py ./ASTAR-tests/4_NV_mapa_sin_CC.csv 3
