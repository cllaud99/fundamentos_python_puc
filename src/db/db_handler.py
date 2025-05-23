import os
from typing import Optional

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def get_engine() -> Engine:
    """
    Cria e retorna uma engine de conexão com o banco de dados PostgreSQL,
    utilizando variáveis de ambiente.

    Returns:
        Engine: engine do SQLAlchemy para conexão com o banco.
    """
    user = os.getenv("PG_USER")
    password = os.getenv("PG_PASSWORD")
    host = os.getenv("PG_HOST")
    db_name = os.getenv("PG_DB")

    return create_engine(f"postgresql://{user}:{password}@{host}/{db_name}")


def read_sql_file(file_path: str) -> str:
    """
    Lê um arquivo .sql e retorna seu conteúdo como string.

    Args:
        file_path (str): Caminho para o arquivo SQL.

    Returns:
        str: Conteúdo do arquivo SQL.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def run_query_from_file(file_path: str, limit: Optional[int] = None) -> pd.DataFrame:
    """
    Executa uma query SQL a partir de um arquivo e retorna os resultados como DataFrame.

    Args:
        file_path (str): Caminho para o arquivo .sql contendo a query.
        limit (Optional[int], optional): Limite de linhas a serem retornadas. Padrão é None.

    Returns:
        pd.DataFrame: Resultado da query em formato DataFrame.
    """
    base_query = read_sql_file(file_path).strip().rstrip(";")

    if limit is not None:
        base_query += f" LIMIT {limit}"

    base_query += ";"

    engine = get_engine()
    return pd.read_sql(base_query, engine)


# Exemplo de uso
if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    sql_path = "src/db/sql/ex_01_clientes_mais_10_trasacoes.sql"

    df = run_query_from_file(sql_path, limit=2)

    print(df.head())
