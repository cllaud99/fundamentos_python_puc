#   Exercício 7 – Tempo Médio de Aluguel vs Clima
# 	•	Calcule o tempo médio de aluguel por cidade (entre rental_date e return_date).
# 	•	Combine com a temperatura atual dessas cidades.
# 	•	Visualize a correlação entre temperatura e tempo médio de aluguel (scatterplot + linha de tendência).

import os
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import pearsonr

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
)

from api.weather_api import get_temperature
from db.db_handler import run_query_from_file

QUERY_LIMIT = 10


def calcula_tempo_medio_por_cidade() -> pd.DataFrame:
    sql_path = "src/db/sql/ex_07_tempo_medio_aluguel.sql"
    df_tempo_medio_por_cidade = run_query_from_file(sql_path, QUERY_LIMIT)
    return df_tempo_medio_por_cidade


def enriquecer_com_temperatura(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enriquece um DataFrame com a temperatura atual de cada cidade presente na coluna 'city'.

    Args:
        df (pd.DataFrame): DataFrame contendo uma coluna chamada 'city'.

    Returns:
        pd.DataFrame: DataFrame original com a coluna 'temperatura_c' adicionada.
    """

    def obter_segura(cidade: str) -> float | None:
        try:
            return get_temperature(cidade)
        except Exception as e:
            print(f"Erro ao obter temperatura de {cidade}: {e}")
            return None

    df["temperatura_c"] = df["city"].apply(obter_segura)
    return df


def plot_correlacao_temperatura_aluguel(
    df: pd.DataFrame, salvar_arquivo: str | None = None
) -> None:
    """
    Gera um gráfico de dispersão entre temperatura e tempo médio de aluguel,
    incluindo linha de tendência (regressão linear) e valor da correlação.
    Pode salvar o gráfico como imagem PNG ou exibi-lo.

    Args:
        df (pd.DataFrame): DataFrame contendo as colunas 'temperatura_c' e 'tempo_medio_aluguel_dias'.
        salvar_arquivo (str | None): Caminho para salvar a imagem do gráfico. Se None, exibe o gráfico.

    Returns:
        None
    """
    colunas_necessarias = {"temperatura_c", "tempo_medio_aluguel_dias"}
    if not colunas_necessarias.issubset(df.columns):
        print(f"As colunas {colunas_necessarias} são obrigatórias no DataFrame.")
        return

    df_limpo = df.dropna(subset=list(colunas_necessarias))

    plt.figure(figsize=(10, 6))
    sns.regplot(
        data=df_limpo,
        x="temperatura_c",
        y="tempo_medio_aluguel_dias",
        scatter_kws={"alpha": 0.6},
        line_kws={"color": "red"},
        ci=None,
    )

    corr, _ = pearsonr(df_limpo["temperatura_c"], df_limpo["tempo_medio_aluguel_dias"])
    plt.title(f"Correlação entre Temperatura e Tempo Médio de Aluguel (r = {corr:.2f})")
    plt.xlabel("Temperatura Atual (°C)")
    plt.ylabel("Tempo Médio de Aluguel (dias)")
    plt.grid(True)
    plt.tight_layout()

    if salvar_arquivo:
        output_dir = os.path.dirname(salvar_arquivo)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        plt.savefig(salvar_arquivo)
        plt.close()
        print(f"Gráfico salvo em: {salvar_arquivo}")
    else:
        try:
            plt.show()
        except Exception as e:
            print(f"Erro ao exibir gráfico: {e}")
        finally:
            plt.close()


def main():
    print("**********************************************************")
    print("1. Calcular o tempo médio de aluguel por cidade:")
    df_tempo_medio_por_cidade = calcula_tempo_medio_por_cidade()
    print(df_tempo_medio_por_cidade)
    print("**********************************************************")

    print("2. Combinar cada cidade com a sua temperatura atual:")
    df_com_temperatura = enriquecer_com_temperatura(df_tempo_medio_por_cidade)
    print(df_com_temperatura)
    print("**********************************************************")

    print(
        "3. Visualizar a correlação entre temperatura e tempo médio de aluguel (scatterplot com linha de tendência):"
    )
    salvar_arquivo = "data/pics/scatterplot_linha_tendencia.png"
    plot_correlacao_temperatura_aluguel(df_com_temperatura, salvar_arquivo)
    print("**********************************************************")


if __name__ == "__main__":
    main()
