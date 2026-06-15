import requests

from config import BASE_URL


def buscar_dados(endpoint):
    """
    Consulta um endpoint da API e retorna o JSON recebido.
    Se ocorrer erro, retorna None.
    """

    # Monta a URL completa da requisição
    url = BASE_URL + endpoint

    try:
        # Timeout evita que o programa fique travado esperando a API
        resposta = requests.get(url, timeout=10)

        # Se o status for erro HTTP, lança exceção
        resposta.raise_for_status()

        # Tenta converter a resposta para JSON
        dados = resposta.json()

        return dados

    except requests.exceptions.JSONDecodeError:
        # A API pode retornar texto inválido, mesmo com status 200
        print(f"Resposta não JSON recebida em {endpoint}")
        return None

    except requests.exceptions.RequestException as erro:
        # Captura erro de conexão, timeout ou status HTTP inválido
        print(f"Erro ao consultar {endpoint}: {erro}")
        return None