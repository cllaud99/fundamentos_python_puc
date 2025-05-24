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
    aqi_list = []

    for _, row in cidades_df.iterrows():
        try:
            aqi = get_aqi(row["cidade"], row["estado"], row["pais"])
        except Exception:
            aqi = None
        aqi_list.append(aqi)

    cidades_df = cidades_df.copy()
    cidades_df["aqi"] = aqi_list

    return cidades_df


def filtra_cidades_alto_aqi(cidades_aqi_df: pd.DataFrame, limite_aqi: int = 150) -> pd.DataFrame:
    """
    Filtra cidades com AQI maior que o limite especificado.

    Args:
        cidades_aqi_df (pd.DataFrame): DataFrame contendo colunas incluindo 'aqi'.
        limite_aqi (int, opcional): Valor limite para filtrar o AQI. Default é 150.

    Returns:
        pd.DataFrame: DataFrame filtrado com cidades cujo AQI é maior que o limite.
    """
    # Remover linhas onde AQI é None ou NaN para evitar erros na comparação
    cidades_aqi_df = cidades_aqi_df.dropna(subset=["aqi"])

    # Filtra as cidades com AQI > limite
    cidades_alto_aqi = cidades_aqi_df[cidades_aqi_df["aqi"] > limite_aqi].copy()

    return cidades_alto_aqi


def filmes_mais_alugados_nas_cidades(cidades_filtradas_df: pd.DataFrame) -> pd.DataFrame:
    """
    Retorna os filmes mais alugados filtrados pelas cidades passadas.

    Args:
        cidades_filtradas_df (pd.DataFrame): DataFrame com a coluna 'cidade' das cidades de interesse.

    Returns:
        pd.DataFrame: DataFrame com os filmes mais alugados nessas cidades.
    """
    sql_path = "src/db/sql/ex_04_qtd_filmes_alugados.sql"
    df_filmes_alugados = run_query_from_file(sql_path)

    # Filtra apenas os filmes cujas cidades estão na lista filtrada
    cidades_alto_aqi = cidades_filtradas_df["city"].unique()
    df_filmes_filtrados = df_filmes_alugados[df_filmes_alugados["cidade"].isin(cidades_alto_aqi)].copy()

    return df_filmes_filtrados.head(QUERY_LIMIT)




def main():
    print("Listando as 10 cidades com maior número de clientes:")
    df_cidades = cidades_mais_clientes()
    print(df_cidades)
    print("**********************************************************")

    print("Consultando AQI dessas cidades usando a AirVisual API:")
    df_cidades_aqi = obtem_aqi_cidades(df_cidades)
    print(df_cidades_aqi)
    print("**********************************************************")

    print("Filtrando cidades com AQI maior que 150:")
    df_cidades_alto_aqi = filtra_cidades_alto_aqi(df_cidades_aqi)
    print(df_cidades_alto_aqi)
    print("**********************************************************")


    print("Buscando os filmes mais alugados em cidades com AQI > 150:")
    df_filmes_populares = filmes_mais_alugados_nas_cidades(df_cidades_alto_aqi)
    print(df_filmes_populares)
    print("**********************************************************")

if __name__ == "__main__":
    main()