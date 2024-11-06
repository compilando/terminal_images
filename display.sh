#!/bin/bash

# Verificar si el archivo ASCII existe
if [ -f "output_colorscript.txt" ]; then
    cat output_colorscript.txt
else
    echo "El archivo output_colorscript.txt no existe. Asegúrate de ejecutar el script de Python primero."
fi
