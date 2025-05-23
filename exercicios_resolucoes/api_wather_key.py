import requests
import os
from dotenv import load_dotenv
from typing import Optional


load_dotenv()
api_key = os.getenv("WEATHER_KEY")


def obter_temperatura(cidade: str, chave_api: str = api_key) -> Optional[float]:
    """
    Consulta a temperatura atual de uma cidade usando a WeatherAPI.

    Args:
        cidade (str): Nome da cidade.
        chave_api (str): Chave de autenticação da WeatherAPI.

    Returns:
        Optional[float]: Temperatura atual em Celsius ou None em caso de erro.
    """
    url = "https://api.weatherapi.com/v1/current.json"
    params = {"key": chave_api, "q": cidade, "lang": "pt"}

    try:
        resposta = requests.get(url, params=params, timeout=5)
        resposta.raise_for_status()
        dados = resposta.json()
        return dados["current"]["temp_c"]
    except requests.exceptions.RequestException as e:
        print(f"[ERRO DE REDE] Cidade: {cidade} - {e}")
    except KeyError:
        print(f"[ERRO DE FORMATO] Cidade: {cidade} - Resposta inesperada.")
    except Exception as e:
        print(f"[ERRO DESCONHECIDO] Cidade: {cidade} - {e}")
    
    return None
    

if __name__ == "__main__":
    cidade = "Cajuru"
    temperatura = obter_temperatura(cidade)
    print(f"A temperatura atual em {cidade} é de {temperatura} graus Celsius.")
