import re
import pandas as pd
import json
import logging
import os

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extraer_numeros(s):
    result = re.findall(r'\d+', s)
    return result[0] if result else None


def save_to_excel(df, filename, municipio=None):
    """
    Guarda un DataFrame de pandas en un archivo de Excel (.xlsx).

    Args:
    - df (pd.DataFrame): DataFrame que deseas guardar.
    - filename (str): Nombre del archivo donde deseas guardar el DataFrame.
    - municipio (int/str, optional): ID del municipio para filtrar el DataFrame. Si es None, procesa todo el df.

    Returns:
    None
    """

    # Si se proporciona un municipio, verificar si el DataFrame tiene la columna 'municipio' y filtrar por ella
    if municipio is not None:
        if 'municipio' in df.columns:
            df = df[df['municipio'] == int(municipio)]
        else:
            logging.error("La columna 'municipio' no se encuentra en el DataFrame.")
            return

    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
            logging.info(f"DataFrame guardado con éxito en {filename}")
    except Exception as e:
        logging.error(f"Error al guardar el archivo {filename}. Detalles: {e}")

def extract_name_colegio(row):
    data = json.loads(row)  # Convertir la cadena a una lista
    for item in data:
        if item['level'] == 7.0:
            return item['name']


def extract_circuito(row):
    data = json.loads(row)  # Convertir la cadena a una lista
    for item in data:
        if item['level'] == 6.0:
            return item['name']

def leer_excel(nombre_archivo, limit=None):
    """
    Lee un archivo de Excel y devuelve un DataFrame de pandas con la cantidad de filas especificada por 'limit'.

    Parámetros:
        - nombre_archivo (str): La ruta o nombre del archivo Excel a leer.
        - limit (int, opcional): El número de filas a devolver. Si no se especifica, devuelve todas las filas.

    Devuelve:
        - DataFrame: Contenido del archivo Excel limitado por el parámetro 'limit'.
    """

    # Usar pandas para leer el archivo de Excel
    df = pd.read_excel(nombre_archivo)

    # Si se especifica un límite, devolver solo esas filas
    if limit is not None:
        df = df.head(limit)

    return df


def completar_mesas_no_cargadas(data):
    # 1. Filtrar las filas donde "mesa_cargada" es "SI".
    mesas_cargadas = data[data['mesa_cargada'] == 'SI']

    # 2. Calcular el promedio de votos por colegio para ambas listas.
    promedios = mesas_cargadas.groupby('colegio')[['LA FUERZA DEL CAMBIO', 'FALTA MENOS PARA VIVIR SIN MIEDO']].mean()

    # 3. Utilizar estos promedios para llenar las mesas donde "mesa_cargada" es "NO".
    for index, row in data.iterrows():
        if row['mesa_cargada'] == 'NO':
            colegio = row['colegio']
            if colegio in promedios.index:
                data.at[index, 'LA FUERZA DEL CAMBIO'] = round(promedios.loc[colegio, 'LA FUERZA DEL CAMBIO'])
                data.at[index, 'FALTA MENOS PARA VIVIR SIN MIEDO'] = round(promedios.loc[colegio, 'FALTA MENOS PARA VIVIR SIN MIEDO'])

    return data


def get_name_from_level(parsed_data, level_target):
    for father in parsed_data['fathers']:
        if father["level"] == level_target:
            return father["name"]
    return None  # Retorna None si no encuentra el nivel


def decimal_to_custom_hex(number):
    # Añadir un "2" al frente y un "4" al final
    modified_number = int(f"2{number}4")

    # Convertir el número modificado a hexadecimal
    hex_value = hex(modified_number).replace("0x", "").upper()

    return hex_value

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def json_municipios_to_dataframe(json_data):
    # Primero, aplanamos las claves anidadas en el objeto 'id'
    data = {**json_data, **json_data['id'], **json_data['id']['idAmbito']}
    # Eliminamos la clave 'id' original y 'idAmbito' para evitar duplicación
    del data['id']
    del data['idAmbito']

    # Convertimos el diccionario aplanado en un DataFrame
    df = pd.DataFrame([data])

    return df
