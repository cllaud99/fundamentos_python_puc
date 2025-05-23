#   Exercício 1 – Temperatura Média das Capitais dos Clientes
# 	•	Recupere as cidades dos clientes com mais de 10 transações.
# 	•	Use a WeatherAPI para buscar a temperatura atual dessas cidades.
# 	•	Calcule a temperatura média ponderada por número de clientes.
# 	•	Insight esperado: quais cidades concentram clientes e temperaturas extremas?

import os
import sys

import pandas as pd

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
)


QUERY_LIMIT = 10

from api.weather_api import get_temperature
from db.db_handler import run_query_from_file


def cidades_clientes_mais_10_trasacoes():
    sql_path = "src/db/sql/ex_01_clientes_mais_10_trasacoes.sql"
    df_cidades_clientes_mais_10_trasacoes = run_query_from_file(sql_path, QUERY_LIMIT)
    return df_cidades_clientes_mais_10_trasacoes


def temperatura_cidade(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adiciona a temperatura atual em Celsius a cada cidade do DataFrame.

    Args:
        df (pd.DataFrame): DataFrame contendo uma coluna 'city'.

    Returns:
        pd.DataFrame: DataFrame com coluna 'temperatura_c' adicionada.
    """
    df["temperatura_c"] = df["city"].apply(lambda cidade: get_temperature(cidade))
    return df


def calcular_temperatura_media_ponderada(df: pd.DataFrame) -> float:
    """
    Calcula a temperatura média ponderada com base no número de clientes por cidade.

    Args:
        df (pd.DataFrame): DataFrame com colunas 'temperatura_c' e 'num_clientes'.

    Returns:
        float: Temperatura média ponderada.
    """
    return (df["temperatura_c"] * df["num_clientes"]).sum() / df["num_clientes"].sum()


def main():
    print("Recuperar cidades com mais de 10 transações por clientes:")
    df_cidades_mais_clientes_10_transacoes = cidades_clientes_mais_10_trasacoes()
    print(df_cidades_mais_clientes_10_transacoes)
    print("**********************************************************")

    print("Buscar temperatura atual das cidades:")
    df_temperatura_cidade = temperatura_cidade(df_cidades_mais_clientes_10_transacoes)
    print(df_temperatura_cidade)
    print("**********************************************************")

    print("Calcular temperatura média ponderada por número de clientes:")
    temperatura_media_ponderada = calcular_temperatura_media_ponderada(
        df_temperatura_cidade
    )
    print(f"Temperatura média ponderada: {temperatura_media_ponderada:.2f} °C")
    print("**********************************************************")

    print(
        "Gerar insights sobre as cidades com base na temperatura e número de clientes:"
    )
    cidade_mais_quente = df_temperatura_cidade.sort_values(
        "temperatura_c", ascending=False
    ).iloc[0]
    cidade_mais_fria = df_temperatura_cidade.sort_values("temperatura_c").iloc[0]
    cidade_mais_clientes = df_temperatura_cidade.sort_values(
        "num_clientes", ascending=False
    ).iloc[0]
    print(
        f"🔴 Cidade mais quente: {cidade_mais_quente['city']} com {cidade_mais_quente['temperatura_c']} °C "
        f"e {cidade_mais_quente['num_clientes']} clientes."
    )
    print(
        f"🔵 Cidade mais fria: {cidade_mais_fria['city']} com {cidade_mais_fria['temperatura_c']} °C "
        f"e {cidade_mais_fria['num_clientes']} clientes."
    )
    print(
        f"👥 Cidade com mais clientes: {cidade_mais_clientes['city']} com {cidade_mais_clientes['num_clientes']} clientes "
        f"e temperatura de {cidade_mais_clientes['temperatura_c']} °C."
    )
    print("**********************************************************")


if __name__ == "__main__":
    main()
