from extract import *
from transform import *


def main():
    # to do: explicar las categorias en un dict
    procesar_distrito("02", "10", "nacional")

    # df = json_to_df(municipio_target="063")
    # df = transformar_columnas(df)
    # save_to_excel(df, 'mesas-florenciovarela-listas.xls')


def check_irregularidades():
    """
    df = leer_excel('total_mesas_pba.xls')
    df['circuito'] = df['fathers'].apply(extract_circuito)
    print(df)
    print(df['municipio'].dtype)

    # Llamando a la función para cada partido
    df = desvio_circuito(df, 'LA FUERZA DEL CAMBIO')
    df = desvio_circuito(df, 'FALTA MENOS PARA VIVIR SIN MIEDO')

    df = desvio_colegio(df, 'LA FUERZA DEL CAMBIO')
    df = desvio_colegio(df, 'FALTA MENOS PARA VIVIR SIN MIEDO')

    df = desvio_municipio(df, 'LA FUERZA DEL CAMBIO')
    df = desvio_municipio(df, 'FALTA MENOS PARA VIVIR SIN MIEDO')

    df = marcar_alta_participacion(df)

    plot_histogram_participacion(df)
    plot_boxplot_participacion(df)
    plot_histogram_votos(df)
    plot_boxplot_votos(df)
    plot_histogram_special_votes(df)
    plot_boxplot_special_votes(df)
    """

if __name__ == "__main__":
    main()