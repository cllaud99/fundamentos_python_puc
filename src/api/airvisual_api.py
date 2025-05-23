import os
from time import sleep
from typing import Optional

import requests
from requests.exceptions import HTTPError


def get_air_quality(
    city: str, state: str, country: str, wait: int = 10
) -> Optional[dict]:
    """
    Consulta a qualidade do ar de uma cidade utilizando a API do AirVisual.

    Args:
        city (str): Nome da cidade.
        state (str): Nome do estado ou distrito.
        country (str): Nome do país.
        wait (int): Tempo de espera em segundos em caso de limite de requisições (padrão: 10).

    Returns:
        Optional[dict]: Dados da qualidade do ar, ou None em caso de erro ou ausência de dados.
    """
    try:
        url = "http://api.airvisual.com/v2/city"
        params = {
            "city": city,
            "state": state,
            "country": country,
            "key": os.environ.get("AIRVISUAL_KEY"),
        }
        response = requests.get(url=url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()

    except HTTPError as e:
        if e.response.status_code == 429 and wait <= 60:
            print(
                f"[LIMITE ALCANÇADO] Aguardando {wait} segundos antes de tentar novamente..."
            )
            sleep(wait)
            return get_air_quality(
                city=city, state=state, country=country, wait=wait + 10
            )
        print(f"[ERRO HTTP] Código {e.response.status_code} - {e}")

    except Exception as e:
        print(
            f"[ERRO DESCONHECIDO] Não foi possível obter dados de qualidade do ar: {e}"
        )

    return None


def get_aqi(city: str, state: str, country: str) -> Optional[int]:
    """
    Retorna somente o índice de qualidade do ar (AQI) em padrão US para uma determinada cidade.

    Args:
        city (str): Nome da cidade.
        state (str): Nome do estado ou distrito.
        country (str): Nome do país.

    Returns:
        Optional[int]: Valor do AQI ou None caso não consiga obter o dado.
    """
    air_quality_data = get_air_quality(city=city, state=state, country=country)
    if not air_quality_data:
        return None

    try:
        return air_quality_data["data"]["current"]["pollution"]["aqius"]
    except (KeyError, TypeError):
        # Estrutura inesperada ou dados faltantes
        return None


if __name__ == "__main__":
    city = "São Paulo"
    state = "São Paulo"
    country = "Brazil"

    air_quality_data = get_air_quality(city=city, state=state, country=country)

    if air_quality_data:
        try:
            pollution = air_quality_data["data"]["current"]["pollution"]
            weather = air_quality_data["data"]["current"]["weather"]

            print(f"\n[QUALIDADE DO AR EM {city.upper()}]")
            print(f"Índice de Qualidade do Ar (AQI - US): {pollution['aqius']}")
            print(f"Principal Poluente: {pollution['mainus']}")
            print(f"Temperatura: {weather['tp']}°C")
            print(f"Umidade: {weather['hu']}%")
            print(f"Velocidade do vento: {weather['ws']} m/s")

        except KeyError:
            print("[ERRO] Estrutura inesperada no retorno da API.")
    else:
        print("[ERRO] Não foi possível obter os dados de qualidade do ar.")
