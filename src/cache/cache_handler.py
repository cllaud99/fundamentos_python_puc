import csv
import os
from datetime import datetime, timedelta
from typing import Dict, Tuple, Callable, Optional

CACHE_EXPIRATION_HOURS = 10
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def load_cache(csv_path: str) -> Dict[str, Tuple[str, datetime]]:
    """
    Carrega o cache de um arquivo CSV, incluindo o timestamp de cada item.

    Args:
        csv_path (str): Caminho do arquivo de cache.

    Returns:
        Dict[str, Tuple[str, datetime]]: Dicionário com chave, resultado e horário.
    """
    cache: Dict[str, Tuple[str, datetime]] = {}
    if os.path.exists(csv_path):
        with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                timestamp = datetime.strptime(row['timestamp'], DATETIME_FORMAT)
                cache[row['key']] = (row['result'], timestamp)
    return cache


def save_cache(csv_path: str, cache: Dict[str, Tuple[str, datetime]]) -> None:
    """
    Salva o cache em um arquivo CSV com timestamp.

    Args:
        csv_path (str): Caminho do arquivo CSV.
        cache (Dict[str, Tuple[str, datetime]]): Cache com resultado e horário.
    """
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['key', 'result', 'timestamp']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for key, (result, timestamp) in cache.items():
            writer.writerow({
                'key': key,
                'result': result,
                'timestamp': timestamp.strftime(DATETIME_FORMAT)
            })


def get_result(
    key: str,
    cache: Dict[str, Tuple[str, datetime]],
    fetch_func: Optional[Callable[[], str]] = None
) -> Optional[str]:
    """
    Retorna o resultado do cache se válido, ou usa fetch_func para obter e atualizar o cache.

    Args:
        key (str): Chave de identificação do item.
        cache (Dict[str, Tuple[str, datetime]]): Dicionário do cache atual.
        fetch_func (Callable[[], str], opcional): Função para buscar o dado real se cache inválido.

    Returns:
        Optional[str]: Resultado do cache ou do fetch_func.
    """
    now = datetime.now()
    if key in cache:
        result, timestamp = cache[key]
        if now - timestamp < timedelta(hours=CACHE_EXPIRATION_HOURS):
            print(f"[CACHE VÁLIDO] Usando cache para '{key}'")
            return result
        else:
            print(f"[CACHE EXPIRADO] Cache expirado para '{key}'")

    if fetch_func:
        print(f"[CACHE MISS] Buscando dado real para '{key}'")
        result = fetch_func()
        cache[key] = (result, now)
        return result

    print(f"[CACHE MISS SEM FETCH_FUNC] Nenhum dado encontrado e nenhuma função de busca fornecida para '{key}'")
    return None


if __name__ == "__main__":
    CSV_PATH = 'data/cache/cache.csv'
    cache_data = load_cache(CSV_PATH)

    for input_key in ['abc', '123', 'abc']:
        # Simulação de busca real apenas se cache inválido
        def fetch_real():
            return input_key[::-1]

        result = get_result(input_key, cache_data, fetch_func=fetch_real)
        print(f"Resultado: {result}")

    save_cache(CSV_PATH, cache_data)
