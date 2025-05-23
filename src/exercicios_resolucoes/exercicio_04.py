#   Exercício 4 – Filmes Mais Populares em Cidades Poluídas
# 	•	Liste as 10 cidades com maior número de clientes.
# 	•	Use a AirVisual API para consultar o AQI dessas cidades.
# 	•	Relacione os filmes mais alugados em cidades com AQI > 150.
# 	•	Discussão: poluição impacta preferências de filmes?


import os
import sys

import pandas as pd

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..",".." , "src"))
)

from api.airvisual_api import get_aqi
from db.db_handler import run_query_from_file

QUERY_LIMIT = 10

def cidades_mais_clientes() -> pd.DataFrame:
   sql_path = "src/db/sql/ex_04_qtd_clientes_cidade.sql"
   df_cidades_mais_clientes = run_query_from_file(sql_path, QUERY_LIMIT)
   return df_cidades_mais_clientes


def obtem_aqi_cidades(cidades_df: pd.DataFrame) -> pd.DataFrame:
    """
    Obtém o AQI das cidades com maior número de clientes, usando a API AirVisual.

    Args:
        cidades_df (pd.DataFrame): DataFrame com as cidades, estados e países.

    Returns:
        pd.DataFrame: DataFrame com as cidades, país, distrito e AQI.
    """
    resultados = []

    for _, row in cidades_df.iterrows():
        cidade = row["city"]
        pais = row["country"]
        estado = row["district"]

        aqi = get_aqi(cidade,  estado, pais)

        resultados.append({
            "city": cidade,
            "country": pais,
            "aqi": aqi,
            "costumers": row["costumers"]
        })
    return pd.DataFrame(resultados)



if __name__ == "__main__":
    df_cidades = cidades_mais_clientes()
    df_cidades_aqi = obtem_aqi_cidades(df_cidades)
    print(df_cidades_aqi)
