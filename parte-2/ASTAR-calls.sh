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