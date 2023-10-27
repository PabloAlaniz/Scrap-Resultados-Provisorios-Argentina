import logging
import os
import json
import pandas as pd
from helpers import *

# Configuración de logging
logging.basicConfig(level=logging.INFO)
pd.set_option('display.max_columns', None)


# Función para convertir la columna 'partidos' en un diccionario
def parties_to_dict(parties):
    result = {}
    for party in parties:
        for lista in party['listas']:
            result[lista['nombre']] = lista['votos']
    return result


def json_to_df(base_path="./municipios", limit=None, municipio_target=None):
    data_dict = {}  # Diccionario que guarda datos por mesa

    if municipio_target:
        municipios_folders = [municipio_target]
    else:
        municipios_folders = [item for item in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, item))]

        if limit is not None:
            municipios_folders = municipios_folders[:limit]

    for municipio in municipios_folders:
        municipio_path = os.path.join(base_path, municipio)

        categoria_folders = [item for item in os.listdir(municipio_path) if
                             os.path.isdir(os.path.join(municipio_path, item))]

        for categoria in categoria_folders:
            categoria_path = os.path.join(municipio_path, categoria)

            archivos_mesas = [f for f in os.listdir(categoria_path) if f.startswith("mesa_") and f.endswith(".json")]

            for archivo in archivos_mesas:
                mesa_number = extraer_numeros(archivo)

                ruta_completa = os.path.join(categoria_path, archivo)

                with open(ruta_completa, 'r', encoding='utf-8') as f:
                    content = f.read()
                    parsed_data = json.loads(content)

                if mesa_number not in data_dict:
                    data_dict[mesa_number] = {'municipio': municipio,
                                              'mesa': mesa_number,
                                              'electores': parsed_data.get('electores', None)}

                    name_level_5 = get_name_from_level(parsed_data, 5.0)
                    name_level_6 = get_name_from_level(parsed_data, 6.0)
                    name_level_7 = get_name_from_level(parsed_data, 7.0)

                    data_dict[mesa_number]['municipio'] = name_level_5
                    data_dict[mesa_number]['circuito'] = name_level_6
                    data_dict[mesa_number]['Establecimiento'] = name_level_7

                data_dict[mesa_number][f'impugnados_{categoria}'] = parsed_data.get('impugnados', None)
                data_dict[mesa_number][f'blancos_{categoria}'] = parsed_data.get('blancos', None)
                data_dict[mesa_number][f'nulos_{categoria}'] = parsed_data.get('nulos', None)
                data_dict[mesa_number][f'recurridos_{categoria}'] = parsed_data.get('recurridos', None)
                data_dict[mesa_number][f'partidos_{categoria}'] = parsed_data.get('partidos', None)
                data_dict[mesa_number][f'electores_{categoria}'] = parsed_data.get('electores', None)
                data_dict[mesa_number][f'sobres_{categoria}'] = parsed_data.get('sobres', None)

    return pd.DataFrame(list(data_dict.values()))


def transformar_columnas(df):
    # Definir las categorías y sus columnas
    categorias = {
        "presidente": "partidos_1",
        "gobernador": "partidos_4",
        "intendente": "partidos_10"
    }

    # Por cada categoría, extraer las listas y crear columnas
    for categoria, columna in categorias.items():
        # Verificar si la columna existe en el DataFrame
        if columna not in df.columns:
            print(f"La columna {columna} no está presente en el DataFrame. Saltando...")
            continue

        # Convertir la columna JSON a diccionario (si es una string)
        df[columna] = df[columna].apply(lambda x: json.loads(x) if isinstance(x, str) else x)

        print(f"Procesando categoría: {categoria}, columna: {columna}")  # Debugging

        # Extraer valores de listas para cada partido
        for index, row in df.iterrows():
            # Verificar que el dato es iterable
            if isinstance(row[columna], list):
                print(f"Procesando fila {index} para columna {columna}")  # Debugging
                for partido_data in row[columna]:
                    partido_name = partido_data['name']
                    for lista_data in partido_data['listas']:
                        lista_name = lista_data['nombre']
                        votos = lista_data['votos']
                        col_name = f"{categoria}_{partido_name}_{lista_name}".replace(" ",
                                                                                      "_")  # Simplificamos el nombre reemplazando espacios con "_"
                        df.at[index, col_name] = votos
                        print(f"Agregando columna {col_name}")  # Debugging
            else:
                print(f"Advertencia: Dato no iterable en fila {index}, columna {columna}. Valor: {row[columna]}")

    # Eliminar las columnas originales que existan en el DataFrame
    cols_to_drop = [col for col in categorias.values() if col in df.columns]
    df = df.drop(columns=cols_to_drop)

    return df


def expand_partidos_column(df):

    # Extraer todas las listas únicas
    all_lists = set()
    for row in df['partidos']:
        print(row)
        for lista in row:
            for item in row:
                all_lists.add(item['lista'])

    # Crear una columna por cada lista y llenarla con los votos
    for lista in all_lists:
        df[lista] = 0  # Inicializar con 0
        for index, row in df.iterrows():
            for item in row['votos']:
                if item['lista'] == lista:
                    df.at[index, lista] = item['votos']

    return df


def agregar_columna_mesa_cargada(df):
    # Lista de claves para verificar
    claves = [
        "electores", "sobres", "nulos", "percNulos",
        "recurridos", "percRecurridos", "blancos", "percBlancos", "comando", "percComando",
        "impugnados", "percImpugnados", "totalVotos", "afirmativos", "percAfirmativos",
        "abstencion", "percAbstencion", "valid", "percValid", "recImpCom", "percRecImpCom",
        "participation"
    ]

    # Función para determinar si una fila tiene todos los valores en 0.0 para las claves especificadas
    def es_mesa_no_cargada(row):
        return all(row[key] == 0.0 for key in claves)

    # Aplicar la función a cada fila y crear la columna 'mesa_cargada'
    df['mesa_cargada'] = df.apply(lambda row: 'NO' if es_mesa_no_cargada(row) else 'SI', axis=1)

    return df


def procesar_municipios():
    archivos_municipios = [f for f in os.listdir('./municipios/') if f.startswith("municipio_") and f.endswith(".json")]

    dfs_list = []  # Esta lista almacenará cada DataFrame individual

    for archivo in archivos_municipios:
        # Definir la ruta completa al archivo en el directorio /mesas
        full_path = os.path.join("./municipios", archivo)

        # Leer el archivo JSON
        with open(full_path, "r") as file:
            content = file.read().strip()  # Leer y quitar espacios en blanco

        parsed_data = json.loads(content)
        if isinstance(parsed_data, str):
            parsed_data = json.loads(parsed_data)

        df = json_municipios_to_dataframe(parsed_data)
        dfs_list.append(df)  # Agregar el DataFrame individual a la lista

    # Concatenar todos los DataFrames en uno solo
    final_df = pd.concat(dfs_list, ignore_index=True)
    return final_df
