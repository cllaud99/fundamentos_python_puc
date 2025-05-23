import pandas as pd
from api_countries_handler import get_population
from db_handler import main_extract_sql


def paises_mais_alugueis(limit: int | None = None) -> pd.DataFrame:
    """
    Executa uma consulta SQL para obter os países com maior número de aluguéis.

    Args:
        limit (int | None, opcional): Quantidade máxima de registros a serem retornados.
            Se None, retorna todos os países. Default é None.

    Returns:
        pd.DataFrame: DataFrame contendo duas colunas:
            - 'country': nome do país
            - 'total_rentals': total de aluguéis realizados por clientes desse país
    """
    base_query = """
    SELECT
        co.country,
        COUNT(r.rental_id) AS total_rentals
    FROM
        rental r
    JOIN customer c ON
        r.customer_id = c.customer_id
    JOIN address a ON
        c.address_id = a.address_id
    JOIN city ci ON
        a.city_id = ci.city_id
    JOIN country co ON
        ci.country_id = co.country_id
    GROUP BY
        co.country
    ORDER BY
        total_rentals DESC
    """

    if limit is not None:
        query = base_query + f"LIMIT {limit};"
    else:
        query = base_query + ";"

    df_paises_mais_alugueis = main_extract_sql(query)
    return df_paises_mais_alugueis


def obtem_populacao_por_pais(df_paises_mais_alugueis: pd.DataFrame) -> pd.DataFrame:
    """
    Recebe um DataFrame com países e o total de aluguéis e retorna um DataFrame
    com a população correspondente de cada país.

    Args:
        df_paises_mais_alugueis (pd.DataFrame): DataFrame contendo ao menos a coluna 'country',
            com os nomes dos países.

    Returns:
        pd.DataFrame: O DataFrame original com uma nova coluna 'population' contendo a população de cada país,
            obtida via API.
    """
    df_populacao_por_pais = df_paises_mais_alugueis.copy()
    df_populacao_por_pais["population"] = df_populacao_por_pais["country"].apply(
        get_population
    )
    return df_populacao_por_pais


def calcula_alugueis_por_mil_habitantes(
    df_populacao_por_pais: pd.DataFrame,
) -> pd.DataFrame:
    """
    Recebe um DataFrame com a população e aluguéis de cada país e retorna um DataFrame
    com o número de aluguéis por mil habitantes

    Args:
        df_populacao_por_pais (pd.DataFrame): DataFrame com as colunas 'total_rentals' e 'population'.

    Returns:
        pd.DataFrame: DataFrame com a coluna 'alugueis_por_mil_habitantes' adicionada e ordenada.
    """
    df_alugueis_mil_habitantes = df_populacao_por_pais.copy()
    df_alugueis_mil_habitantes["alugueis_por_mil_habitantes"] = (
        df_alugueis_mil_habitantes["total_rentals"]
        / df_alugueis_mil_habitantes["population"]
        * 1000
    )

    return df_alugueis_mil_habitantes


def obtem_top_paises_cinefilos(df_alugueis_mil: pd.DataFrame, n: int = 5) -> list:
    """
    Recebe um DataFrame com a coluna 'alugueis_por_mil_habitantes' e retorna
    os top N países mais 'cinéfilos', ordenados do maior para o menor. Também
    imprime país, população e alugueis por mil habitantes.

    Args:
        df_alugueis_mil (pd.DataFrame): DataFrame com as colunas 'country', 'population',
                                        'total_rentals' e 'alugueis_por_mil_habitantes'.
        n (int, optional): Número de países a retornar. Default é 5.

    Returns:
        list: Lista com os nomes únicos dos países no top N.
    """
    df_sorted = df_alugueis_mil.sort_values(
        by="alugueis_por_mil_habitantes", ascending=False
    ).reset_index(drop=True)
    top_paises = df_sorted.head(n)

    for _, row in top_paises.iterrows():
        print(
            f"{row['country']}: população = {row['population']}, alugueis por mil habitantes = {row['alugueis_por_mil_habitantes']:.5f}"
        )

    return top_paises["country"].unique().tolist()


if __name__ == "__main__":

    LIMITE_DE_PAISES = 20

    df_paises_mais_alugueis = paises_mais_alugueis(LIMITE_DE_PAISES)
    print(f"Paises com mais alugueis:")
    print(df_paises_mais_alugueis)
    print("*******************************************")

    df_populacao_por_pais = obtem_populacao_por_pais(df_paises_mais_alugueis)
    print("Dados enriquecidos com população")
    print(df_populacao_por_pais.head(10))
    print("*******************************************")

    df_alugueis_mil_habitantes = calcula_alugueis_por_mil_habitantes(
        df_populacao_por_pais
    )
    print("Alugueis por mil habitantes")
    print(df_alugueis_mil_habitantes.head(10))
    print("*******************************************")

    paises_cinefolos = obtem_top_paises_cinefilos(df_alugueis_mil_habitantes, n=5)
    print("Paises cinéfilos:")
    print(paises_cinefolos)
    print("*******************************************")
