from typing import Optional, Union

import requests
from rapidfuzz import process


def _get_country_data(country_name: str) -> Optional[dict]:
    """
    Obtém os dados completos de um país a partir de seu nome, usando fuzzy matching
    com dados da API pública restcountries.com.

    Args:
        country_name (str): Nome do país (comum ou oficial) a ser consultado.

    Returns:
        dict | None: Dicionário com os dados do país, ou None se não encontrado.
    """
    try:
        response = requests.get("https://restcountries.com/v3.1/all", timeout=10)
        response.raise_for_status()
        countries_data = response.json()

        country_names = []
        for country in countries_data:
            country_names.append(country["name"]["common"])
            country_names.append(country["name"].get("official", ""))

        match, score, _ = process.extractOne(
            country_name, country_names, score_cutoff=70
        )
        if not match:
            print(f"Não encontrou correspondência próxima para '{country_name}'.")
            return None

        for country in countries_data:
            if match in (
                country["name"]["common"],
                country["name"].get("official", ""),
            ):
                return country

        print(f"País correspondente a '{country_name}' não encontrado nos dados.")
        return None

    except requests.RequestException as e:
        print(f"Erro de requisição ao consultar dados do país: {e}")
    except Exception as e:
        print(f"Erro inesperado ao buscar dados do país: {e}")

    return None


def get_population(country_name: str) -> Optional[int]:
    """
    Obtém a população de um país, a partir de seu nome, consultando a API restcountries.com.

    Args:
        country_name (str): Nome do país para consulta (pode ser nome comum ou oficial).

    Returns:
        int | None: População do país, ou None caso não encontrada ou erro na requisição.
    """
    country_data = _get_country_data(country_name)
    if country_data:
        return country_data.get("population")
    return None


def get_continent(country_name: str) -> Optional[str]:
    """
    Obtém o continente de um país, a partir de seu nome, consultando a API restcountries.com.

    Args:
        country_name (str): Nome do país para consulta (pode ser nome comum ou oficial).

    Returns:
        str | None: Continente do país, ou None caso não encontrado ou erro na requisição.
    """
    country_data = _get_country_data(country_name)
    if country_data:
        continents = country_data.get("continents")
        if continents:
            return continents[0]
        print(f"Continente não encontrado para '{country_name}'.")
    return None


if __name__ == "__main__":
    country = "Brasil"

    population = get_population(country)
    if population:
        print(f"População de {country}: {population:,}")
    else:
        print("População não disponível.")

    continent = get_continent(country)
    if continent:
        print(f"{country} está localizado no continente: {continent}")
    else:
        print("Continente não disponível.")
