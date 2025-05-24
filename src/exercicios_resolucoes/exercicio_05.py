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

QUERY_LIMIT = 2


def clientes_em_areas_criticas() -> pd.DataFrame:
    sql_path = "src/db/sql/ex_05_clientes_em_areas_criticas.sql"
    df_clientes_em_areas_criticas = run_query_from_file(sql_path, QUERY_LIMIT)
    return df_clientes_em_areas_criticas


def combina_nomes_cidades_e_paises(df_clientes_em_areas_criticas):
    df = obtem_aqi_cidades(df_clientes_em_areas_criticas)
    return df


if __name__ == "__main__":
    df_clientes_em_areas_criticas = clientes_em_areas_criticas()
    df_clientes_em_areas_criticas = combina_nomes_cidades_e_paises(
        df_clientes_em_areas_criticas
    )
    print(df_clientes_em_areas_criticas)