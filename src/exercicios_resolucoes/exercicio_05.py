#   Exercício 5 – Clientes em Áreas Críticas
# 	•	Recupere os clientes com endereço em cidades com AQI acima de 130.
# 	•	Combine nome do cliente, cidade, país, temperatura e AQI.
# 	•	Classifique os clientes em “zona de atenção” com base nos critérios ambientais.


import os
import sys

import pandas as pd

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
)

from api.airvisual_api import get_aqi
from api.weather_api import get_temperature
from db.db_handler import run_query_from_file
from exercicios_resolucoes.exercicio_04 import obtem_aqi_cidades

QUERY_LIMIT = 10


def clientes_em_areas_criticas() -> pd.DataFrame:
    """
    Executa consulta SQL para buscar clientes com informações de cidade e país.

    Returns:
        pd.DataFrame: Dados dos clientes com suas respectivas localizações.
    """
    sql_path = "src/db/sql/ex_05_clientes_em_areas_criticas.sql"
    return run_query_from_file(sql_path, QUERY_LIMIT)


def combina_nomes_cidades_e_paises(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enriquecer DataFrame com dados de AQI e temperatura.

    Args:
        df (pd.DataFrame): DataFrame com colunas ['nome', 'cidade', 'pais']

    Returns:
        pd.DataFrame: DataFrame com AQI e temperatura incluídos.
    """
    df = obtem_aqi_cidades(df)
    return df


def clientes_aqui_acima_de_130(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filtra os clientes com AQI acima de 130.

    Args:
        df (pd.DataFrame): DataFrame com coluna 'aqi'

    Returns:
        pd.DataFrame: Apenas clientes em áreas críticas.
    """
    return df[df["aqi"] > 130].reset_index(drop=True)


def classifica_clientes_por_aqui(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adiciona uma coluna de classificação para clientes com base no AQI.

    Args:
        df (pd.DataFrame): DataFrame com coluna 'aqi'

    Returns:
        pd.DataFrame: DataFrame com nova coluna 'classificacao'
    """
    df["classificacao"] = df["aqi"].apply(
        lambda aqi: "zona de atenção" if aqi > 130 else "seguro"
    )
    return df


def main():
    print("1. Recuperando clientes com cidade e país:")
    df_clientes = clientes_em_areas_criticas()
    print(df_clientes)
    print("**********************************************************")

    print("2. Combinando nome, cidade, país, temperatura e AQI:")
    df_enriquecido = combina_nomes_cidades_e_paises(df_clientes)
    print(df_enriquecido)
    print("**********************************************************")

    print("3. Filtrando apenas clientes com AQI acima de 130 (áreas críticas):")
    df_filtrado = clientes_aqui_acima_de_130(df_enriquecido)
    print(df_filtrado)
    print("**********************************************************")

    print('4. Classificando clientes como "zona de atenção" com base no AQI:')
    df_classificado = classifica_clientes_por_aqui(df_filtrado)
    print(df_classificado)
    print("**********************************************************")


if __name__ == "__main__":
    main()
