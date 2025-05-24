# ⸻

#   Exercício 8 – Perfil de Clima por Cliente
# 	•	Para cada cliente, crie um perfil com:
# 	•	cidade, temperatura, AQI, total de aluguéis, gasto total.
# 	•	Agrupe os perfis por faixa etária (simulada ou fictícia) e avalie padrões.
# 	•	Objetivo: conectar comportamento de consumo e ambiente.

import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
)

import pandas as pd
from db.db_handler import run_query_from_file
from api.airvisual_api import get_aqi
from api.weather_api import get_temperature

QUERY_LIMIT = 10

def calcula_tempo_medio_por_cidade() -> pd.DataFrame:
    sql_path = "src/db/sql/ex_08_perfil_clientes.sql"
    df_perfil_base = run_query_from_file(sql_path, QUERY_LIMIT)
    return df_perfil_base


def temperatura_cidade(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adiciona a temperatura atual em Celsius a cada cidade do DataFrame.

    Args:
        df (pd.DataFrame): DataFrame contendo uma coluna 'city'.

    Returns:
        pd.DataFrame: DataFrame com coluna 'temperatura_c' adicionada.
    """
    df["temperatura_c"] = df["cidade"].apply(lambda cidade: get_temperature(cidade))
    return df


def obtem_aqi_cidades(cidades_df: pd.DataFrame) -> pd.DataFrame:
    """
    Obtém o AQI das cidades e adiciona ao DataFrame original sem perder linhas.

    Args:
        cidades_df (pd.DataFrame): DataFrame com as cidades, estados e países.

    Returns:
        pd.DataFrame: Mesmo DataFrame com uma coluna extra "aqi".
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


def analisa_perfil(df_perfil: pd.DataFrame) -> pd.DataFrame:
    """
    Cria faixas etárias e realiza agregações para identificar padrões de consumo
    e ambiente por grupo de idade.

    Args:
        df_perfil (pd.DataFrame): DataFrame contendo colunas 'idade', 'temperatura_c',
        'aqi', 'total_alugueis' e 'gasto_total'.

    Returns:
        pd.DataFrame: DataFrame agrupado por faixa etária com médias das métricas analisadas.
    """
    # Define faixas etárias
    bins = [0, 18, 25, 35, 45, 60, 200]
    labels = ["<18", "18-25", "26-35", "36-45", "46-60", "60+"]
    df_perfil["faixa_etaria"] = pd.cut(df_perfil["idade"], bins=bins, labels=labels, right=False)

    # Agrega por faixa etária
    df_agg = (
        df_perfil.groupby("faixa_etaria", observed=False)[["temperatura_c", "aqi", "total_alugueis", "gasto_total"]]
        .mean()
        .reset_index()
        .rename(columns={
            "temperatura_c": "temperatura_media",
            "aqi": "aqi_medio",
            "total_alugueis": "media_alugueis",
            "gasto_total": "media_gastos"
        })
    )

    return df_agg


def main():
    print("Calculando perfil base dos clientes:")
    df_perfil_base = calcula_tempo_medio_por_cidade()
    print(df_perfil_base)
    print("**********************************************************")

    print("Adicionando temperatura às cidades:")
    df_perfil_temperatura = temperatura_cidade(df_perfil_base)
    print(df_perfil_temperatura)
    print("**********************************************************")

    print("Obtendo AQI para as cidades:")
    df_perfil_temperatura_aqi = obtem_aqi_cidades(df_perfil_temperatura)
    print(df_perfil_temperatura_aqi)
    print("**********************************************************")

    print("Analisando perfil agrupado por faixa etária:")
    df_perfil_final = analisa_perfil(df_perfil_temperatura_aqi)
    print(df_perfil_final)
    print("**********************************************************")

if __name__ == "__main__":
    main()