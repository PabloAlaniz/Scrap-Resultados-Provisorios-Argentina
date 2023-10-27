import pandas as pd
import matplotlib.pyplot as plt


def desvio_circuito(df, partido):
    # Calcula el promedio de votos por circuito
    promedio_circuito = df.groupby('circuito')[partido].mean()

    # Calcula el desvío para cada mesa respecto al promedio de su circuito
    df['desvio_circuito_' + partido] = df.apply(lambda row: row[partido] - promedio_circuito[row['circuito']], axis=1)
    return df


def desvio_colegio(df, partido):
    # Calcula el promedio de votos por colegio
    promedio_colegio = df.groupby('colegio')[partido].mean()

    # Calcula el desvío para cada mesa respecto al promedio de su colegio
    df['desvio_colegio_' + partido] = df.apply(lambda row: row[partido] - promedio_colegio[row['colegio']], axis=1)
    return df


def desvio_municipio(df, partido):
    # Calcula el promedio de votos del municipio
    promedio_municipio = df[partido].mean()

    # Calcula el desvío para cada mesa respecto al promedio del municipio
    df['desvio_municipio_' + partido] = df.apply(lambda row: row[partido] - promedio_municipio, axis=1)
    return df


def marcar_alta_participacion(df, umbral=90):
    """
    Marca las mesas con alta participación.

    Args:
    - df: DataFrame con los datos de las mesas.
    - umbral: porcentaje de participación para considerar alta participación. Por defecto es 90.

    Returns:
    DataFrame modificado con la columna adicional 'alta_participacion'.
    """

    df['alta_participacion'] = df['participation'].apply(lambda x: 'SI' if x >= umbral else 'NO')
    return df


def plot_histogram_participacion(df, column='participation', bins=20):
    """
    Crea un histograma para visualizar la distribución de la participación.

    Args:
    - df: DataFrame con los datos de las mesas.
    - column: Nombre de la columna con la participación. Por defecto es 'participation'.
    - bins: Número de intervalos en el histograma.
    """

    plt.hist(df[column], bins=bins, edgecolor='black')
    plt.title('Distribución de Participación por Mesa')
    plt.xlabel('Porcentaje de Participación')
    plt.ylabel('Número de Mesas')
    plt.show()


def plot_boxplot_participacion(df, column='participation'):
    """
    Crea un boxplot para visualizar la distribución de la participación.

    Args:
    - df: DataFrame con los datos de las mesas.
    - column: Nombre de la columna con la participación. Por defecto es 'participation'.
    """

    plt.boxplot(df[column])
    plt.title('Boxplot de Participación por Mesa')
    plt.ylabel('Porcentaje de Participación')
    plt.show()


def plot_histogram_votos(df, columns=['LA FUERZA DEL CAMBIO', 'FALTA MENOS PARA VIVIR SIN MIEDO']):
    """
    Crea un histograma para visualizar la distribución de votos de cada candidato.

    Args:
    - df: DataFrame con los datos de las mesas.
    - columns: Lista de columnas que representan los votos de cada candidato o partido.
    """

    for column in columns:
        plt.hist(df[column], bins=20, alpha=0.5, label=column)

    plt.title('Distribución General de Votos por Candidato')
    plt.xlabel('Número de Votos')
    plt.ylabel('Número de Mesas')
    plt.legend(loc='upper right')
    plt.show()


def plot_boxplot_votos(df, columns=['LA FUERZA DEL CAMBIO', 'FALTA MENOS PARA VIVIR SIN MIEDO']):
    """
    Crea un boxplot para visualizar la distribución de votos de cada candidato.

    Args:
    - df: DataFrame con los datos de las mesas.
    - columns: Lista de columnas que representan los votos de cada candidato o partido.
    """

    data = [df[column] for column in columns]
    plt.boxplot(data, vert=True, patch_artist=True, labels=columns)
    plt.title('Boxplot de Distribución de Votos por Candidato')
    plt.ylabel('Número de Votos')
    plt.show()


def plot_histogram_special_votes(df, columns=['percNulos', 'percRecurridos', 'percBlancos']):
    """
    Crea un histograma para visualizar la distribución de votos nulos, recurridos y en blanco.

    Args:
    - df: DataFrame con los datos de las mesas.
    - columns: Lista de columnas que representan los porcentajes de votos nulos, recurridos y en blanco.
    """

    for column in columns:
        plt.hist(df[column], bins=20, alpha=0.5, label=column)

    plt.title('Distribución de Votos Especiales')
    plt.xlabel('Porcentaje de Votos')
    plt.ylabel('Número de Mesas')
    plt.legend(loc='upper right')
    plt.show()


def plot_boxplot_special_votes(df, columns=['percNulos', 'percRecurridos', 'percBlancos']):
    """
    Crea un boxplot para visualizar la distribución de votos nulos, recurridos y en blanco.

    Args:
    - df: DataFrame con los datos de las mesas.
    - columns: Lista de columnas que representan los porcentajes de votos nulos, recurridos y en blanco.
    """

    data = [df[column] for column in columns]
    plt.boxplot(data, vert=True, patch_artist=True, labels=columns)
    plt.title('Boxplot de Distribución de Votos Especiales')
    plt.ylabel('Porcentaje de Votos')
    plt.show()