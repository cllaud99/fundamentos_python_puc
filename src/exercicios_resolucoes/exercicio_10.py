#   Exercício 10 – API Cache Inteligente (Desafio)
# 	•	Implemente uma lógica que salve os dados de clima e AQI localmente em CSV.
# 	•	Ao consultar novamente a mesma cidade, busque do CSV ao invés da API.
# 	•	Evite chamadas redundantes — bom para práticas de performance e economia de requisições.

import os
import sys
from typing import Callable

import pandas as pd

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
)

from db.db_handler import run_query_from_file
from api.airvisual_api import get_aqi  # Função que busca AQI real da API
from cache.cache_handler import get_result, load_cache, save_cache


def exemplo_funcionamento_cache(df_tempo_medio_por_cidade: pd.DataFrame):
    """
    Função para demonstrar funcionamento do cache inteligente usando CSV.

    Args:
        df_tempo_medio_por_cidade (pd.DataFrame): DataFrame com as cidades a consultar.
    """
    CSV_PATH = "data/cache/aqi_cache_exemplo.csv"
    cache_data = load_cache(CSV_PATH)

    for _, row in df_tempo_medio_por_cidade.iterrows():
        cidade = row["city"]
        estado = row["district"]
        country = row["country"]

        fetch_func: Callable[[], str] = lambda: get_aqi(cidade, estado, country)

        resultado = get_result(cidade, cache_data, fetch_func=fetch_func)
        save_cache(CSV_PATH, cache_data)
        print(f"Resultado para {cidade}: {resultado}")


def main():


    sql_path = "src/db/sql/ex_10_lista_cidades_cache_exemplo.sql"
    df_tempo_medio_por_cidade = run_query_from_file(sql_path, 40)

    exemplo_funcionamento_cache(df_tempo_medio_por_cidade)

if __name__ == "__main__":
    main()