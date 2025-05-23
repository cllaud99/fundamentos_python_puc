import requests
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()
api_key = os.getenv("AIRVISUAL_KEY")



def get_estado_por_cidade(cidade: str, codigo_pais: str) -> Optional[str]:
    """
    Obtém o estado a partir de uma cidade e um código de país usando Nominatim.
    """
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "city": cidade,
            "country": codigo_pais,
            "format": "json",
            "limit": 1
        }
        headers = {"User-Agent": "api-pos/1.0"}
        r = requests.get(url, params=params, headers=headers, timeout=5)
        data = r.json()
        if data and "display_name" in data[0]:
            partes = [p.strip() for p in data[0]["display_name"].split(",")]
            estado = partes[-2]
            return estado
        else:
            return None
    except Exception:
        return None


def get_aqi(city: str, country: str, api_key: str = api_key) -> Optional[float]:
    """
    Consulta o AQI (Air Quality Index) de uma cidade na API AirVisual,
    obtendo o estado automaticamente via get_estado_por_cidade.

    Args:
        city (str): Nome da cidade.
        country (str): Nome do país.
        api_key (str): Chave de acesso à API.

    Returns:
        Optional[float]: Valor do AQI da cidade ou None se não encontrado.
    """
    state = get_estado_por_cidade(city, country)
    if not state:
        print(f"Estado não encontrado para {city}, {country}.")
        return None

    try:
        response = requests.get(
            "http://api.airvisual.com/v2/city",
            params={
                "city": city,
                "state": state,
                "country": country,
                "key": api_key
            },
            timeout=10
        )
        data = response.json()

        if response.status_code != 200 or "data" not in data or "current" not in data["data"]:
            print(f"Resposta inesperada da API para {city}, {state}, {country}: {data}")
            return None

        return data["data"]["current"]["pollution"]["aqius"]

    except requests.exceptions.RequestException as e:
        print(f"Erro de rede ao buscar AQI de {city}, {state}, {country}: {e}")
        return None
    except (KeyError, TypeError) as e:
        print(f"Erro ao processar resposta da API para {city}, {state}, {country}: {e}")
        return None


if __name__ == "__main__":
    city = "Sao Paulo"
    country = "Brazil"
    aqi = get_aqi(city, country)
    print(f"AQI de {city}, {country}: {aqi}")
