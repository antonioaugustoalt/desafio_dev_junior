BASE_URL = "http://localhost:5050"  #URL DA API

INTERVALO_SEGUNDOS = 300   #TEMPO ENTRE CADA COLETA (5 MINUTOS)

DURACAO_MINUTOS = 30 #DURAÇÃO DA APLICAÇÃO EM MINUTOS

DB_NAME = "telemetria.db"  #NOME DO BANCO DE DADOS

#DICIONÁRIO COM OS NOMES LÓGICOS E ROTAS DA API
#
ENDPOINTS = {
    "inversor": "/inversor",
    "rele": "/rele-protecao",
    "estacao": "/estacao-solarimetrica"
}