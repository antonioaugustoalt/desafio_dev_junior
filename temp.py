from api_client import buscar_dados
from config import ENDPOINTS
from validators import validar_inversor, validar_rele, validar_estacao
from database import criar_tabelas, inserir_inversor, inserir_rele, inserir_estacao


criar_tabelas()

# Testa inversor
dados_inversor = buscar_dados(ENDPOINTS["inversor"])

if validar_inversor(dados_inversor):
    inserir_inversor(dados_inversor)
    print("Inversor salvo.")
else:
    print("Inversor inválido. Não salvo.")


# Testa relé
dados_rele = buscar_dados(ENDPOINTS["rele"])

if validar_rele(dados_rele):
    inserir_rele(dados_rele)
    print("Relé salvo.")
else:
    print("Relé inválido. Não salvo.")


# Testa estação
dados_estacao = buscar_dados(ENDPOINTS["estacao"])

if validar_estacao(dados_estacao):
    inserir_estacao(dados_estacao)
    print("Estação salva.")
else:
    print("Estação inválida. Não salva.")