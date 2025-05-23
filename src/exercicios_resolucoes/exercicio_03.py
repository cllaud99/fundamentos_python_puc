#   Exercício 3 – Aluguel de Filmes por Região e População
# 	•	Identifique os países dos clientes com maior número de aluguéis.
# 	•	Use a REST Countries API para obter a população desses países.
# 	•	Calcule o número de aluguéis por 1.000 habitantes.
# 	•	Análise: quais países são mais “cinéfilos” proporcionalmente?

import os
import sys

import pandas as pd

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
)

from api.countries_api import get_population
from db.db_handler import run_query_from_file

QUERY_LIMIT = 10


def paises_mais_alugueis() -> pd.DataFrame:
    sql_path = "src/db/sql/ex_03_quantidade_alugueis_pais.sql"
    df_paises_mais_alugueis = run_query_from_file(sql_path, QUERY_LIMIT)
    return df_paises_mais_alugueis


def obtem_populacao_por_pais(df_paises_mais_alugueis: pd.DataFrame) -> pd.DataFrame:
    """
    Enriquecimento do DataFrame com a população de cada país via API.

    Args:
        df_paises_mais_alugueis (pd.DataFrame): DataFrame com a coluna 'country'.

    Returns:
        pd.DataFrame: DataFrame com a coluna adicional 'population'.
    """
    df = df_paises_mais_alugueis.copy()
    df["population"] = df["country"].apply(get_population)
    return df


def calcula_alugueis_por_mil_habitantes(
    df_populacao_por_pais: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calcula o número de aluguéis por mil habitantes para cada país.

    Args:
        df_populacao_por_pais (pd.DataFrame): DataFrame com 'total_rentals' e 'population'.

    Returns:
        pd.DataFrame: DataFrame com coluna adicional 'alugueis_por_mil_habitantes'.
    """
    df = df_populacao_por_pais.copy()
    df["alugueis_por_mil_habitantes"] = (df["total_rentals"] / df["population"]) * 1000
    return df


def obtem_top_paises_cinefilos(df_alugueis_mil: pd.DataFrame, n: int = 5) -> list:
    """
    Imprime e retorna os top N países com mais aluguéis por mil habitantes.

    Args:
        df_alugueis_mil (pd.DataFrame): DataFrame com dados populacionais e de aluguel.
        n (int, optional): Número de países no ranking. Default é 5.

    Returns:
        list: Lista dos países mais "cinéfilos".
    """
    df_sorted = df_alugueis_mil.sort_values(
        by="alugueis_por_mil_habitantes", ascending=False
    ).reset_index(drop=True)
    top_paises = df_sorted.head(n)

    print("Top países cinéfilos (proporcional à população):")
    for _, row in top_paises.iterrows():
        print(
            f"- {row['country']}: população = {row['population']}, "
            f"alugueis por mil habitantes = {row['alugueis_por_mil_habitantes']:.5f}"
        )
    print("**********************************************************")

    return top_paises["country"].unique().tolist()


def main():
    print("Recuperar países com maior número de aluguéis:")
    df_paises_mais_alugueis = paises_mais_alugueis()
    print(df_paises_mais_alugueis)
    print("**********************************************************")

    print("Enriquecer dados com a população dos países:")
    df_populacao_por_pais = obtem_populacao_por_pais(df_paises_mais_alugueis)
    print(df_populacao_por_pais)
    print("**********************************************************")

    print("Calcular aluguéis por mil habitantes:")
    df_alugueis_mil_habitantes = calcula_alugueis_por_mil_habitantes(
        df_populacao_por_pais
    )
    print(df_alugueis_mil_habitantes)
    print("**********************************************************")

    paises_cinefilos = obtem_top_paises_cinefilos(df_alugueis_mil_habitantes, n=5)
    print("Lista final de países mais cinéfilos:")
    print(paises_cinefilos)
    print("**********************************************************")


if __name__ == "__main__":
    main()
