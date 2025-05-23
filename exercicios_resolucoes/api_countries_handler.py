import requests
from rapidfuzz import process


def get_population(country_name: str) -> int | None:
    """
    Obtém a população de um país utilizando a API pública restcountries.com,
    realizando busca aproximada no nome do país para lidar com variações ou
    nomes oficiais e comuns.

    A função consulta todos os países disponíveis na API, tenta encontrar a
    melhor correspondência para o nome informado usando fuzzy matching
    (similaridade textual), e retorna a população do país correspondente.

    Args:
        country_name (str): Nome do país para consulta (pode ser nome comum ou oficial).

    Returns:
        int | None: População do país caso encontrado, ou None se não for possível
        obter a população (nenhuma correspondência próxima, erro na requisição ou
        dados incompletos).

    Observações:
        - Utiliza a biblioteca 'rapidfuzz' para busca fuzzy com score mínimo de 70.
        - Em caso de erro ou ausência de dados, imprime mensagem informativa e retorna None.
    """

    url = "https://restcountries.com/v3.1/all"
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        dados = resposta.json()

        # lista dos nomes possíveis (common + official)
        nomes_paises = []
        for pais in dados:
            nomes_paises.append(pais["name"]["common"])
            nomes_paises.append(pais["name"].get("official", ""))

        # buscar o nome mais próximo
        match, score, idx = process.extractOne(
            country_name, nomes_paises, score_cutoff=70
        )
        if not match:
            print(f"Não encontrou correspondência próxima para {country_name}")
            return None

        # achar o objeto do país que bate com esse nome (match)
        for pais in dados:
            if match in (pais["name"]["common"], pais["name"].get("official", "")):
                return pais.get("population")

        print(f"População não encontrada para o país: {country_name}")
        return None

    except Exception as e:
        print(f"Erro ao obter população para {country_name}: {e}")
        return None
