#   Exercício 2 – Receita Bruta em Cidades com Clima Ameno
# 	•	Calcule a receita bruta por cidade.
# 	•	Use a WeatherAPI para consultar a temperatura atual.
# 	•	Filtre apenas cidades com temperatura entre 18°C e 24°C.
# 	•	Resultado: qual o faturamento total vindo dessas cidades?


import os
import sys

import pandas as pd

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
)

from api.weather_api import get_temperature
from db.db_handler import run_query_from_file

QUERY_LIMIT = 10


def receita_bruta_por_cidade() -> pd.DataFrame:
    sql_path = "src/db/sql/ex_02_receita_bruta_cidade.sql"
    df_receita_bruta_cidade = run_query_from_file(sql_path, QUERY_LIMIT)
    return df_receita_bruta_cidade


def temperatura_media_cidade(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adiciona a temperatura atual em Celsius a cada cidade do DataFrame.

    Args:
        df (pd.DataFrame): DataFrame contendo uma coluna 'city'.

    Returns:
        pd.DataFrame: DataFrame com coluna 'temperatura_c' adicionada.
    """
    df["temperatura_c"] = df["city"].apply(lambda cidade: get_temperature(cidade))
    return df


def filtrar_cidades_clima_ameno(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filtra as cidades com temperatura entre 18°C e 24°C.

    Args:
        df (pd.DataFrame): DataFrame com colunas 'city', 'receita_bruta' e 'temperatura_c'.

    Returns:
        pd.DataFrame: Subconjunto do DataFrame com clima ameno.
    """
    return df[(df["temperatura_c"] >= 18) & (df["temperatura_c"] <= 24)]


def main():
    print("**********************************************************")
    print("Recuperar receita bruta por cidade:")
    df_receita = receita_bruta_por_cidade()
    print(df_receita)
    print("**********************************************************")

    print("Buscar temperatura atual para cada cidade:")
    df_com_temperatura = temperatura_media_cidade(df_receita)
    print(df_com_temperatura)
    print("**********************************************************")

    print("Filtrar cidades com clima ameno (18°C a 24°C):")
    df_clima_ameno = filtrar_cidades_clima_ameno(df_com_temperatura)
    print(df_clima_ameno)
    print("**********************************************************")

    print("Calcular receita bruta total dessas cidades:")
    receita_total_amena = df_clima_ameno["receita_bruta"].sum()
    print(f"💰 Receita total de cidades com clima ameno: R$ {receita_total_amena:,.2f}")
    print("**********************************************************")


if __name__ == "__main__":
    main()
