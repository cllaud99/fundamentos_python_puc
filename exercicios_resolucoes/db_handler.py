import os

import pandas as pd
import requests
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def get_engine() -> Engine:
    """
    Cria e retorna a engine de conexão com o banco de dados PostgreSQL.

    Returns:
        Engine: engine do SQLAlchemy para conexão com o banco.
    """
    user = os.getenv("PG_USER")
    password = os.getenv("PG_PASSWORD")
    host = os.getenv("PG_HOST")
    db = os.getenv("PG_DB")
    return create_engine(f"postgresql://{user}:{password}@{host}/{db}")


def run_query_to_df(query: str, engine: Engine) -> pd.DataFrame:
    """
    Executa uma query SQL e retorna o resultado como DataFrame.

    Args:
        query (str): Query SQL a ser executada.
        engine (Engine): Engine de conexão com o banco de dados.

    Returns:
        pd.DataFrame: Resultado da query em formato DataFrame.
    """
    return pd.read_sql(query, engine)


def main_extract_sql(query: str) -> pd.DataFrame:
    """
    Função principal para extrair dados do banco de dados via SQL.

    Args:
        query (str): Query SQL a ser executada.

    Returns:
        pd.DataFrame: Resultado da query em DataFrame.
    """
    engine = get_engine()
    df = run_query_to_df(query, engine)
    return df


def get_population(nome_pais: str) -> int:
    """
    Retorna a quantidade de habitantes (população) de um país usando a API restcountries.com.

    Args:
        nome_pais (str): Nome do país a ser consultado (pode ser em inglês ou no idioma oficial).

    Returns:
        int: Quantidade de habitantes do país.

    Raises:
        ValueError: Se o país não for encontrado ou a API retornar erro.
    """
    url = f"https://restcountries.com/v3.1/name/{nome_pais}"

    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        dados = resposta.json()

        populacao = dados[0].get("population")
        if populacao is not None:
            return populacao
        else:
            raise ValueError("População não encontrada para o país informado.")

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Erro na requisição HTTP: {e}")
    except (IndexError, KeyError):
        raise ValueError("País não encontrado ou dados indisponíveis.")


if __name__ == "__main__":
    print(get_population("Brazil"))
