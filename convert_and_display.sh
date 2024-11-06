#!/bin/bash

# Verificar si se han proporcionado los argumentos necesarios
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Uso: $0 <modo> <archivo_png> [ancho] [save]"
    echo "Modos: 'ascii', 'image', 'real_image'"
    echo "El parámetro 'save' es opcional y permite guardar el resultado en disco."
    exit 1
fi

# Asignar el modo, archivo de entrada y ancho (opcional)
MODE="$1"
PNG_FILE="$2"
WIDTH="${3:-100}"  # Ancho opcional, con valor predeterminado de 100
SAVE_OPTION="${4:-mostrar}"  # Si se pasa 'guardar', se guarda en disco; si no, se muestra en pantalla

# Ejecutar el script de Python según el modo seleccionado y el parámetro de guardar/mostrar
echo "Ejecutando en modo $MODE con ancho $WIDTH y opción de guardado: $SAVE_OPTION..."

python3 -c "
from png_to_ascii_colorscript import convert_image_to_ascii, display_image_in_terminal, display_real_image_in_terminal

mode = '$MODE'
image_path = '$PNG_FILE'
width = int($WIDTH)
save_to_disk = True if '$SAVE_OPTION' == 'save' else False

if mode == 'ascii':
    convert_image_to_ascii(image_path, width, save_to_disk)
elif mode == 'image':
    display_image_in_terminal(image_path, width, save_to_disk)
elif mode == 'real_image':
    display_real_image_in_terminal(image_path, width, save_to_disk)
else:
    print('Modo desconocido. Usa ascii, image o real_image.')
"
