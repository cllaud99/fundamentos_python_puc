from db_handler import main_extract_sql
from api_wather_key import obter_temperatura
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def calcula_tempo_medio_por_cidade():
    query = """
    SELECT
        c2.city,
        AVG(EXTRACT(EPOCH FROM (r.return_date - r.rental_date)) / 86400) AS tempo_medio_aluguel_dias
    FROM
        rental r
    JOIN
        customer c ON c.customer_id = r.customer_id
    JOIN
        address a ON a.address_id = c.address_id
    JOIN
        city c2 ON c2.city_id = a.city_id
    GROUP BY
        c2.city
    ORDER BY
        tempo_medio_aluguel_dias DESC
    LIMIT 30
    """

    df_tempo_medio_por_cidade = main_extract_sql(query)
    return df_tempo_medio_por_cidade


def enriquecer_com_temperatura(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enriquece um DataFrame com a temperatura atual de cada cidade presente na coluna 'city'.

    Args:
        df (pd.DataFrame): DataFrame contendo uma coluna chamada 'city'.

    Returns:
        pd.DataFrame: DataFrame original com a coluna 'temperatura_c' adicionada.
    """
    df["temperatura_c"] = df["city"].apply(lambda cidade: obter_temperatura(cidade))
    return df


def plot_correlacao_temperatura_aluguel(df: pd.DataFrame, salvar_arquivo: str | None = None) -> None:
    """
    Gera um gráfico de dispersão entre temperatura e tempo médio de aluguel,
    incluindo uma linha de tendência (regressão linear).

    Args:
        df (pd.DataFrame): DataFrame contendo as colunas 'temperatura_c' e 'tempo_medio_aluguel_dias'.
        salvar_arquivo (str | None): Caminho para salvar a imagem do gráfico. Se None, exibe o gráfico.
        
    Returns:
        None
    """
    matplotlib.use('Agg')

    df_limpo = df.dropna(subset=["temperatura_c", "tempo_medio_aluguel_dias"])

    plt.figure(figsize=(10, 6))
    sns.regplot(
        data=df_limpo,
        x="temperatura_c",
        y="tempo_medio_aluguel_dias",
        scatter_kws={"alpha": 0.6},
        line_kws={"color": "red"},
        ci=None
    )
    plt.title("Correlação entre Temperatura e Tempo Médio de Aluguel")
    plt.xlabel("Temperatura Média (°C)")
    plt.ylabel("Tempo Médio de Aluguel (dias)")
    plt.grid(True)
    plt.tight_layout()

    if salvar_arquivo:
        plt.savefig(salvar_arquivo)
        print(f"Gráfico salvo em {salvar_arquivo}")
    else:
        try:
            plt.show()
        except Exception as e:
            print(f"Erro ao exibir gráfico: {e}")

    plt.close()


if __name__ == "__main__":
    print(f"Calcular o tempo médio de aluguel por cidade:")
    df_tempo_medio_por_cidade = calcula_tempo_medio_por_cidade()
    print(df_tempo_medio_por_cidade)
    print(f"*****************************************************")


    print(f"Combinar cidade com a temperatura atual:")
    df_cidades_e_temperatura = enriquecer_com_temperatura(df_tempo_medio_por_cidade)
    print(df_cidades_e_temperatura)
    print(f"*****************************************************")


    print("Visualize a correlação entre temperatura e tempo médio de aluguel (scatterplot + linha de tendência).")
    salvar_arquivo="exercicios_resolucoes/exercicio_7_grafico/scatterplot + linha de tendência.png"
    plot_correlacao_temperatura_aluguel(df_cidades_e_temperatura, salvar_arquivo)