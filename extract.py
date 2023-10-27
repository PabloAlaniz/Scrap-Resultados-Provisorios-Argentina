import requests
import os
import logging
import json
from helpers import ensure_directory_exists, decimal_to_custom_hex

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = "https://resultados.gob.ar/backend-difu/scope/data/getScopeData"
MAX_CONSECUTIVE_ERRORS = 10
BASE_DIRECTORY = "municipios"
NACIONALIDADES = {
    "nacional": "X",
    "extranjero": "E"
}

def obtener_datos(provincia, distrito, mesa, categoria, nacionalidad):
    tipo_nacionalidad = NACIONALIDADES.get(nacionalidad, "X")  # Por defecto es "X"
    url = f"{BASE_URL}/{provincia}{distrito}{mesa}{tipo_nacionalidad}/{categoria}"

    logging.info(f"Visitando URL: {url}")  # Logging URL que está siendo visitado

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.HTTPError as e:
        logging.error(f"Error al obtener datos desde {url}. Error: {e}")  # Logging en caso de error
        return None


def recorrer_mesas(provincia, categoria, distrito, nacionalidad):
    errores_consecutivos = 0
    if nacionalidad == "extranjero":
        num_mesa = 9001
    else:
        num_mesa = 1

    distrito_path = os.path.join(BASE_DIRECTORY, distrito)
    ensure_directory_exists(distrito_path)

    categoria_path = os.path.join(distrito_path, categoria)
    ensure_directory_exists(categoria_path)

    while errores_consecutivos < MAX_CONSECUTIVE_ERRORS:
        mesa = f"{num_mesa:05}"
        file_path = os.path.join(categoria_path, f"mesa_{mesa}.json")

        # Si el archivo ya existe, saltamos la escritura
        if os.path.exists(file_path):
            logging.info(f"El archivo para la mesa {mesa} ya existe. Saltando...")
            num_mesa += 1
            continue

        resultado = obtener_datos(provincia, distrito, mesa, categoria, nacionalidad)

        if resultado:
            with open(os.path.join(categoria_path, f"mesa_{mesa}.json"), "w") as file:
                file.write(resultado)
            errores_consecutivos = 0
        else:
            errores_consecutivos += 1

        num_mesa += 1

    logging.info(f"Distrito {distrito} finalizado tras {errores_consecutivos} errores consecutivos.")


def procesar_distrito(provincia, categoria, nacionalidad, distrito=None):
    ensure_directory_exists(BASE_DIRECTORY)

    if distrito is None:
        for d in range(1, 136):
            distrito_str = f"{d:03}"
            recorrer_mesas(provincia, categoria, distrito_str, nacionalidad)
    else:
        recorrer_mesas(provincia, categoria, distrito, nacionalidad)

def get_municipio_stats(municipio_id):
    municipio = decimal_to_custom_hex(municipio_id)
    municipio = municipio.lower()
    url = f'https://resultados.gob.ar/backend-difu/scope/data/getScopeData/00000000000000000000{municipio}/4/1'
    print(url)
    response = requests.get(url)
    with open(f"./municipios/municipio_{municipio_id}.json", "w") as file:
        json.dump(response.text, file, indent=4)


def guardar_stats_municipios():
    for i in range(135, 136):
        municipio_id = str(i).zfill(3)
        print(municipio_id)
        get_municipio_stats(municipio_id)