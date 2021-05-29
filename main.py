import sys
import requests
import os
from pytube import YouTube, Playlist

# importar bibliotecas

"""
@author Andy Taipe 
"""


# función de barra de progreso
def progress_function(chunk=None, file_handle=None, bytes_remaining=None):
    current = ((video.filesize - bytes_remaining) / video.filesize)  # estado actual
    percent = "{0:.1f}".format(current * 100)
    progress = int(50 * current)
    status = '█' * progress + '-' * (50 - progress)
    # barra de progreso de impresión
    sys.stdout.write(' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent))
    sys.stdout.flush()


# creando una nueva carpeta para la lista de reproducción
def folder_name(url):
    try:
        requests.get(url)
    except:
        print("Sin conexión a internet ... :(")
        return 0

    if 'list=' in url:
        return Playlist(url).title

    return 0

# generador de enlaces de video de listas de reproducción
def link_generator(url):
    try:
        requests.get(url)
    except:
        print("Sin conexión a internet ... :(")
        return 0

    if "list=" in url:
        return Playlist(url).videos
    else:
        return [YouTube(url, on_progress_callback=progress_function())]

# ingresando el enlace del video / lista de reproducción
inputted_url = input(
    "Bienvenido a YouTube - Descargar Playlist\nauthor: @AndyTaipe\n" + "Ingrese la lista de reproduccion: ")

os.chdir(os.getcwd())

new_folder = folder_name(inputted_url)
# crear una nueva carpeta para listas de reproducción si no existe
try:
    os.mkdir(new_folder)
except:
    temp = 0

try:
    os.chdir(new_folder)
except:
    temp = 0

downloaded_videos = []
# buscando archivos en la carpeta actual
for path_to_folder, s, files in os.walk('.', topdown=False):
    for name in files:
        if os.path.getsize(os.path.join(path_to_folder, name)) < 1:
            os.remove(os.path.join(path_to_folder, name))
        else:
            downloaded_videos.append(str(name))

videos_links = link_generator(inputted_url)
# descarga de videos uno por uno
for current_video in videos_links:
    try:
        # configuración de la función de devolución de llamada de progreso
        current_video.register_on_progress_callback(progress_function)
        main_title = current_video.title
        main_title = main_title + ".mp4"
        main_title = main_title.replace('|', '')
    except:
        print("Problema de Conexion... :(")
        break

    if main_title not in downloaded_videos:
        video = current_video.streams.filter(progressive=True, file_extension='mp4').order_by(
            'resolution').desc().first()

        if os.path.exists(str(os.getcwd()) + "/" + str(video.default_filename)):
            # comprobando si el video existe en esta carpeta
            print("Existe. . . " + video.default_filename)

            s = input("Ingrese 1 para eliminar el archivo existente y descargar uno nuevo\nIngrese 0 para mantener este archivo y continuar\n")

            # verificar existiendo
            if s == "0":
                continue
            elif s == "1":
                # descargando de nuevo
                os.remove(str(os.getcwd()) + "/" + str(video.default_filename))

        print("Descargando. . . " + video.default_filename + " " + video.resolution)
        video.download(os.getcwd())
        print("Video Descargado!")

print(f"Descarga Finalizada!\nGuardar en: {os.getcwd()}")
# fin del programa
