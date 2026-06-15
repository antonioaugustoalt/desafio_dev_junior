import time

from config import ENDPOINTS, INTERVALO_SEGUNDOS, DURACAO_MINUTOS
from api_client import buscar_dados
from validators import validar_inversor, validar_rele, validar_estacao
from criar_log import registrar_descarte
from database import (
    criar_tabelas,
    inserir_inversor,
    inserir_rele,
    inserir_estacao
)


# Mapeia cada tipo de equipamento para sua função de validação
VALIDADORES = {
    "inversor": validar_inversor,
    "rele": validar_rele,
    "estacao": validar_estacao
}


# Mapeia cada tipo de equipamento para sua função de inserção
FUNCOES_INSERCAO = {
    "inversor": inserir_inversor,
    "rele": inserir_rele,
    "estacao": inserir_estacao
}

def processar_endpoint(tipo, endpoint):
    """
    Consulta um endpoint, valida a leitura e salva no banco se estiver válida.
    Registra em log as falhas e leituras descartadas.
    """

    # Busca os dados da API
    dados = buscar_dados(endpoint)

    # Se a API falhar ou retornar algo inválido, registra falha
    if dados is None:
        print(f"[{tipo}] Falha na coleta. Leitura ignorada.")
        registrar_descarte(tipo, "falha_coleta_ou_json_invalido", dados)
        return "falha"

    validador = VALIDADORES[tipo]
    funcao_insercao = FUNCOES_INSERCAO[tipo]

    # Valida antes de salvar no banco
    if validador(dados):
        funcao_insercao(dados)
        print(f"[{tipo}] Leitura válida salva.")
        return "valida"

    # Se não passou na validação, registra o dado descartado
    print(f"[{tipo}] Leitura inválida descartada.")
    registrar_descarte(tipo, "leitura_invalida", dados)
    return "invalida"


if __name__ == "__main__":
    """
    Executa a aplicação principal.
    Cria as tabelas, inicia o loop de coleta e roda pelo tempo configurado.
    """

    criar_tabelas()

    tempo_inicio = time.time()

    duracao_segundos = DURACAO_MINUTOS * 60

    ciclo = 1

    print("Iniciando coleta de telemetria...")
    print(f"Duração configurada: {DURACAO_MINUTOS} minutos")
    print(f"Intervalo entre coletas: {INTERVALO_SEGUNDOS} segundos")

    estatisticas = {
        "validas": 0,
        "invalidas": 0,
        "falhas": 0
    }

    while time.time() - tempo_inicio < duracao_segundos:
        print(f"\n===== CICLO {ciclo} =====")

        # Consulta todos os endpoints configurados
        for tipo, endpoint in ENDPOINTS.items():
            status = processar_endpoint(tipo, endpoint)

            if status == "valida":
                estatisticas["validas"] += 1
            elif status == "invalida":
                estatisticas["invalidas"] += 1
            else:
                estatisticas["falhas"] += 1

        ciclo += 1

        # Evita esperar depois do último ciclo se o tempo já acabou
        if time.time() - tempo_inicio < duracao_segundos:
            print(f"Aguardando {INTERVALO_SEGUNDOS} segundos...")
            time.sleep(INTERVALO_SEGUNDOS)

    print("\n===== RESUMO DA EXECUÇÃO =====")
    print(f"Leituras válidas salvas: {estatisticas['validas']}")
    print(f"Leituras inválidas descartadas: {estatisticas['invalidas']}")
    print(f"Falhas de coleta: {estatisticas['falhas']}")

    print("\nColeta finalizada.")