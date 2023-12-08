#!/bin/bash

# Prueba 1: No se especifica ningún argumento
python3 CSPParking.py

# Prueba 2: La ruta de argumento no es válida
python3 CSPParking.py ./CSP-tests/

# Prueba 3: El número de filas del archivo de entrada no es un entero
python3 CSPParking.py ./CSP-tests/1_NV_filas_no_entero.txt

# Prueba 4: El número de columnas del archivo de entrada no es un entero
python3 CSPParking.py ./CSP-tests/2_NV_columnas_no_entero.txt

# Prueba 5: La definición de las plazas eléctricas no empieza por "PE:"
python3 CSPParking.py ./CSP-tests/3_NV_no_PE_antes_def_pe.txt

# Prueba 6: La declaración de las plazas eléctricas no sigue el formato
# (i,j)(i',j')(i'',j'')...: No tienen '('
python3 CSPParking.py ./CSP-tests/4_NV_formato_incorrecto_pe_parentesis_izq.txt

# Prueba 7: La declaración de las plazas eléctricas no sigue el formato
# (i,j)(i',j')(i'',j'')...: Filas no entero
python3 CSPParking.py ./CSP-tests/5_NV_formato_incorrecto_pe_filas_no_entero.txt

# Prueba 8: La declaración de las plazas eléctricas no sigue el formato
# (i,j)(i',j')(i'',j'')...: No tienen ','
python3 CSPParking.py ./CSP-tests/6_NV_formato_incorrecto_pe_coma.txt

# Prueba 9: La declaración de las plazas eléctricas no sigue el formato
# (i,j)(i',j')(i'',j'')...: Columnas no entero
python3 CSPParking.py ./CSP-tests/7_NV_formato_incorrecto_pe_colum_no_entero.txt

# Prueba 10: La declaración de las plazas eléctricas no sigue el formato
# (i,j)(i',j')(i'',j'')...: No tienen ')'
python3 CSPParking.py ./CSP-tests/8_NV_formato_incorrecto_pe_parentesis_dcho.txt

# Prueba 11: Las plazas enchufables definidas no se encuentran dentro del dominio
python3 CSPParking.py ./CSP-tests/9_NV_def_pe_fuera_dominio.txt

# Prueba 12: Las definición de los vehículos no sigue el formato ID(int)-TIPO(TSU o TNU)-
# CONGELADOR(C o X)
python3 CSPParking.py ./CSP-tests/10_NV_formato_incorrecto_def_vehiculos.txt

# Prueba 13: Las definición de los vehículos no sigue el formato ID(int)-TIPO(TSU o TNU)-
# CONGELADOR(C o X): ID del vehiculo no es entero
python3 CSPParking.py ./CSP-tests/11_NV_id_no_entero_def_vehiculos.txt

# Prueba 14: Las definición de los vehículos no sigue el formato ID(int)-TIPO(TSU o TNU)-
# CONGELADOR(C o X): Tipo del vehiculo no es 'TSU' o 'TNU'
python3 CSPParking.py ./CSP-tests/12_NV_tipo_no_valido_def_vehiculos.txt

# Prueba 15: Las definición de los vehículos no sigue el formato ID(int)-TIPO(TSU o TNU)-
# CONGELADOR(C o X): No se especifica correctamente si tiene congelador o no
python3 CSPParking.py ./CSP-tests/13_NV_congelador_no_valido_def_vehiculos.txt

# Prueba 16: El ID de un vehículo debe ser único
python3 CSPParking.py ./CSP-tests/14_NV_id_vehiculo_no_unico.txt

