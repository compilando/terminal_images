from PIL import Image, ImageChops
from colorama import Fore, Style, init
import subprocess
import tempfile
import os
import sys

# Inicializar colorama para el soporte de colores en la terminal
init(autoreset=True)

# Definir los caracteres ASCII para la representación de la imagen
ascii_chars = " .:-=+*#%@"

def rgb_to_ansi(r, g, b):
    """Convierte un color RGB a su código ANSI equivalente.

    Args:
        r (int): Valor rojo (0-255).
        g (int): Valor verde (0-255).
        b (int): Valor azul (0-255).

    Returns:
        str: Código ANSI para el color RGB especificado.
    """
    return f'\033[38;2;{r};{g};{b}m'

def trim_image(image):
    """Recorta los bordes de color uniforme de una imagen.

    Args:
        image (Image): Imagen PIL a recortar.

    Returns:
        Image: Imagen PIL recortada.
    """
    # Obtener el color de la esquina superior izquierda como color de fondo
    bg_color = image.getpixel((0, 0))
    # Crear una nueva imagen con el color de fondo
    bg = Image.new(image.mode, image.size, bg_color)
    # Calcular la diferencia entre la imagen original y la imagen de fondo
    diff = ImageChops.difference(image, bg)
    # Obtener el cuadro delimitador de la diferencia (área no uniforme)
    bbox = diff.getbbox()
    # Recortar la imagen original usando el cuadro delimitador si existe, de lo contrario, devolver la imagen original
    return image.crop(bbox) if bbox else image

# Modo ASCII: Convierte la imagen a arte ASCII y lo muestra o guarda en disco
def convert_image_to_ascii(image_path, width=100, save_to_disk=False):
    """Convierte una imagen a arte ASCII y la muestra en la terminal o la guarda en un archivo.

    Args:
        image_path (str): Ruta a la imagen.
        width (int, optional): Ancho deseado de la salida ASCII. Por defecto es 100.
        save_to_disk (bool, optional): Si es True, guarda la salida en un archivo. Por defecto es False.
    """
    # Abrir la imagen y convertirla a RGB
    image = Image.open(image_path).convert("RGB")
    # Recortar los bordes uniformes de la imagen
    trimmed_image = trim_image(image)
    # Calcular la relación de aspecto de la imagen recortada
    aspect_ratio = trimmed_image.height / trimmed_image.width
    # Calcular la nueva altura en función de la relación de aspecto y el ancho deseado
    new_height = int(aspect_ratio * width * 0.55)
    # Redimensionar la imagen recortada a las nuevas dimensiones
    resized_image = trimmed_image.resize((width, new_height))

    # Guardar la salida en un archivo si save_to_disk es True
    if save_to_disk:
        # Crear un archivo temporal para guardar la salida
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
            output_path = tmp_file.name
            # Escribir la salida ASCII en el archivo
            with open(output_path, "w") as f:
                for y in range(resized_image.height):
                    line = ""
                    for x in range(resized_image.width):
                        # Obtener el valor RGB del píxel actual
                        r, g, b = resized_image.getpixel((x, y))
                        # Calcular el valor de escala de grises del píxel
                        grayscale = int((r + g + b) / 3)
                        # Obtener el carácter ASCII correspondiente al valor de escala de grises
                        ascii_char = ascii_chars[grayscale * len(ascii_chars) // 256]
                        # Obtener el código ANSI para el color del píxel
                        color = rgb_to_ansi(r, g, b)
                        # Agregar el carácter ASCII coloreado a la línea
                        line += f"{color}{ascii_char}"
                    # Escribir la línea en el archivo, seguida de un salto de línea
                    f.write(line + "\n")
            # Imprimir la ruta del archivo donde se guardó la salida
            print(f"ASCII colorscript saved to {output_path}")
    # Mostrar la salida en la terminal si save_to_disk es False
    else:
        for y in range(resized_image.height):
            line = ""
            for x in range(resized_image.width):
                # Obtener el valor RGB del píxel actual
                r, g, b = resized_image.getpixel((x, y))
                # Calcular el valor de escala de grises del píxel
                grayscale = int((r + g + b) / 3)
                # Obtener el carácter ASCII correspondiente al valor de escala de grises
                ascii_char = ascii_chars[grayscale * len(ascii_chars) // 256]
                # Obtener el código ANSI para el color del píxel
                color = rgb_to_ansi(r, g, b)
                # Agregar el carácter ASCII coloreado a la línea
                line += f"{color}{ascii_char}"
            # Imprimir la línea en la terminal, seguida de un restablecimiento de estilo
            print(line + Style.RESET_ALL)

def display_real_image_in_terminal(image_path, width=100, save_to_disk=False):
    """Muestra una imagen en la terminal usando 'timg' o la guarda en un archivo.

    Args:
        image_path (str): Ruta a la imagen.
        width (int, optional): Ancho deseado de la imagen. Por defecto es 100.
        save_to_disk (bool, optional): Si es True, guarda la imagen en un archivo. Por defecto es False.
    """
    # Abrir la imagen y convertirla a RGB
    image = Image.open(image_path).convert("RGB")
    # Recortar los bordes uniformes de la imagen
    trimmed_image = trim_image(image)
    # Mantener la relación de aspecto original
    aspect_ratio = 1
    # Calcular la nueva altura en función de la relación de aspecto y el ancho deseado
    new_height = int(aspect_ratio * width * trimmed_image.height / trimmed_image.width)
    # Redimensionar la imagen recortada a las nuevas dimensiones
    resized_image = trimmed_image.resize((width, new_height))

    # Guardar la imagen en un archivo si save_to_disk es True
    if save_to_disk:
        # Crear un archivo temporal para guardar la imagen
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
            output_path = tmp_file.name
            # Guardar la imagen redimensionada en el archivo temporal
            resized_image.save(output_path)
            # Imprimir la ruta del archivo donde se guardó la imagen
            print(f"Image saved to {output_path}")
    # Mostrar la imagen en la terminal usando 'timg' si save_to_disk es False
    else:
        # Crear un archivo temporal para guardar la imagen
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
            temp_image_path = tmp_file.name
            # Guardar la imagen redimensionada en el archivo temporal
            resized_image.save(temp_image_path)
            # Usar 'timg' para mostrar la imagen en la terminal
            subprocess.run(["timg", temp_image_path])
            # Eliminar el archivo temporal
            os.remove(temp_image_path)

def display_image_in_terminal(image_path, width=100, save_to_disk=False):
    """Muestra una imagen en la terminal usando bloques de color o la guarda en un archivo.

    Args:
        image_path (str): Ruta a la imagen.
        width (int, optional): Ancho deseado de la imagen. Por defecto es 100.
        save_to_disk (bool, optional): Si es True, guarda la imagen en un archivo. Por defecto es False.
    """
    # Abrir la imagen y convertirla a RGB
    image = Image.open(image_path).convert("RGB")
    # Recortar los bordes uniformes de la imagen
    trimmed_image = trim_image(image)
    # Ajustar la relación de aspecto para la salida de la terminal
    aspect_ratio = 0.5
    # Calcular la nueva altura en función de la relación de aspecto y el ancho deseado
    new_height = int(aspect_ratio * width * trimmed_image.height / trimmed_image.width)
    # Redimensionar la imagen recortada a las nuevas dimensiones
    resized_image = trimmed_image.resize((width, new_height))

    # Guardar la salida en un archivo si save_to_disk es True
    if save_to_disk:
        # Crear un archivo temporal para guardar la salida
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
            output_path = tmp_file.name
            # Escribir la salida en el archivo
            with open(output_path, "w") as f:
                for y in range(resized_image.height):
                    line = ""
                    for x in range(resized_image.width):
                        # Obtener el valor RGB del píxel actual
                        r, g, b = resized_image.getpixel((x, y))
                        # Agregar un bloque de color al texto de salida
                        line += f"{rgb_to_ansi(r, g, b)}█"
                    # Escribir la línea en el archivo, seguida de un salto de línea
                    f.write(line + "\n")
            # Imprimir la ruta del archivo donde se guardó la salida
            print(f"Real image ASCII saved to {output_path}")
    # Mostrar la salida en la terminal si save_to_disk es False
    else:
        for y in range(resized_image.height):
            for x in range(resized_image.width):
                # Obtener el valor RGB del píxel actual
                r, g, b = resized_image.getpixel((x, y))
                # Imprimir un bloque de color en la terminal
                print(rgb_to_ansi(r, g, b) + "█", end="")
            # Imprimir un salto de línea y restablecer el estilo después de cada línea
            print(Style.RESET_ALL)

if __name__ == "__main__":
    # Verificar si se proporcionaron suficientes argumentos de línea de comandos
    if len(sys.argv) < 3:
        # Imprimir instrucciones de uso si no hay suficientes argumentos
        print("Uso: python script.py <modo> <ruta_imagen> [width] [save]")
        print("Modos: 'ascii', 'image', 'real_image'")
        print("El parámetro 'save' es opcional. Usa 'save' para save en disco.")
        # Salir del script con un código de error
        sys.exit(1)

    # Obtener el modo, la ruta de la imagen, el ancho y el indicador de guardar desde los argumentos de línea de comandos
    mode = sys.argv[1]
    image_path = sys.argv[2]
    width = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    save_to_disk = len(sys.argv) > 4 and sys.argv[4].lower() == "save"

    # Llamar a la función apropiada según el modo especificado
    if mode == "ascii":
        convert_image_to_ascii(image_path, width, save_to_disk)
    elif mode == "image":
        display_image_in_terminal(image_path, width, save_to_disk)
    elif mode == "real_image":
        display_real_image_in_terminal(image_path, width, save_to_disk)
    # Imprimir un mensaje de error si se especifica un modo desconocido
    else:
        print("Modo desconocido. Usa 'ascii', 'image' o 'real_image'.")
