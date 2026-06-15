import sqlite3

from config import DB_NAME


def conectar():
    """
    Cria e retorna uma conexão com o banco SQLite.
    Se o arquivo .db não existir, ele será criado automaticamente.
    """

    conexao = sqlite3.connect(DB_NAME)
    return conexao


def criar_tabelas():
    """
    Cria as tabelas necessárias para armazenar as leituras válidas.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    # Tabela para leituras dos inversores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leituras_inversor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sn TEXT NOT NULL,
            tsleitura TEXT NOT NULL,
            pac REAL NOT NULL,
            uac REAL NOT NULL,
            iac REAL NOT NULL,
            fac REAL NOT NULL,
            temp REAL NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabela para leituras dos relés de proteção
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leituras_rele (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sn TEXT NOT NULL,
            tsleitura TEXT NOT NULL,
            tplei TEXT NOT NULL,
            rfreq REAL NOT NULL,
            rifasea REAL NOT NULL,
            rifaseb REAL NOT NULL,
            rifasec REAL NOT NULL,
            rvfasea REAL NOT NULL,
            rvfaseb REAL NOT NULL,
            rvfasec REAL NOT NULL,
            rpac REAL NOT NULL,
            rtempinterno REAL NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabela para leituras da estação solarimétrica
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leituras_estacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sn TEXT NOT NULL,
            tsleitura TEXT NOT NULL,
            tplei TEXT NOT NULL,
            irghi REAL NOT NULL,
            irpoa REAL NOT NULL,
            umid REAL NOT NULL,
            tempamb REAL NOT NULL,
            tempmedmod REAL NOT NULL,
            velvento REAL NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conexao.commit()
    conexao.close()