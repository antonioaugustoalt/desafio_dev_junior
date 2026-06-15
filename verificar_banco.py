import sqlite3

from config import DB_NAME


conexao = sqlite3.connect(DB_NAME)
cursor = conexao.cursor()

# Conta quantos registros existem em cada tabela
tabelas = [
    "leituras_inversor",
    "leituras_rele",
    "leituras_estacao"
]

for tabela in tabelas:
    cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
    total = cursor.fetchone()[0]

    print(f"{tabela}: {total} registros")

print("\nÚltimas leituras de inversor:")

# Mostra as últimas 5 leituras salvas do inversor
cursor.execute("""
    SELECT *
    FROM leituras_inversor
    ORDER BY id DESC
    LIMIT 5
""")

linhas = cursor.fetchall()

for linha in linhas:
    print(linha)

conexao.close()