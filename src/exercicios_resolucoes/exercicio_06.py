#   Exercício 6 – Receita por Continente
# 	•	Use a REST Countries API para mapear o continente de cada país.
# 	•	Agrupe a receita total por continente.
# 	•	Exiba os resultados em um gráfico de pizza com matplotlib.

import os
import sys

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
)

from api.countries_api import get_continent
from db.db_handler import run_query_from_file

QUERY_LIMIT = 10


def mapeia_continente_pais() -> pd.DataFrame:
    """
    Executa uma consulta SQL para obter o total de receita por país e
    mapeia cada país ao seu respectivo continente.

    Returns:
        pd.DataFrame: DataFrame com as colunas 'country_name', 'amount' e 'continent'.
    """
    sql_path = "src/db/sql/ex_06_receita_bruta_pais.sql"
    df_receita_bruta_pais = run_query_from_file(sql_path, QUERY_LIMIT)

    # Adiciona a coluna de continente com base no nome do país
    df_receita_bruta_pais["continent"] = df_receita_bruta_pais["country_name"].apply(
        get_continent
    )

    return df_receita_bruta_pais


def agrega_receita_por_continente(df_paises: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa os valores de receita total por continente.

    Args:
        df_paises (pd.DataFrame): DataFrame com as colunas 'continent' e 'amount'.

    Returns:
        pd.DataFrame: DataFrame com as colunas 'continent' e 'total_amount'.
    """
    colunas_necessarias = {"continent", "amount"}
    if not colunas_necessarias.issubset(df_paises.columns):
        print("As colunas 'continent' e 'amount' são obrigatórias.")
        return pd.DataFrame(columns=["continent", "total_amount"])

    df_agrupado = (
        df_paises.groupby("continent", as_index=False)
        .agg(total_amount=("amount", "sum"))
        .sort_values("total_amount", ascending=False)
    )

    return df_agrupado


def salva_grafico_pizza(df_agregado_continente: pd.DataFrame) -> None:
    """
    Gera um gráfico de pizza com a distribuição de receita por continente
    e salva o gráfico como uma imagem PNG.

    Args:
        df_agregado_continente (pd.DataFrame): DataFrame com as colunas
            'continent' e 'total_amount'.

    Returns:
        None
    """
    if not {"continent", "total_amount"}.issubset(df_agregado_continente.columns):
        print("As colunas 'continent' e 'total_amount' são obrigatórias.")
        return

    df = df_agregado_continente.dropna(subset=["continent"])

    # Cria diretório de saída
    output_dir = "data/pics"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"grafico_pizza.png")

    # Criação do gráfico
    plt.figure(figsize=(8, 8))
    plt.pie(
        df["total_amount"], labels=df["continent"], autopct="%1.1f%%", startangle=140
    )
    plt.title("Distribuição de Receita por Continente")
    plt.tight_layout()

    # Salva imagem
    plt.savefig(output_path)
    plt.close()

    print(f"Gráfico salvo em: {output_path}")


def main():
    print("***********************************************")
    print("Etapa 1: Mapeando continentes para os países...")
    df_paises = mapeia_continente_pais()
    print(df_paises)
    print("***********************************************")

    print("Etapa 2: Agregando receita total por continente...")
    df_continente = agrega_receita_por_continente(df_paises)
    print(df_continente)
    print("***********************************************")

    print("Etapa 3: Gerando gráfico de pizza...")
    salva_grafico_pizza(df_continente)
    print("***********************************************")


if __name__ == "__main__":
    main()
