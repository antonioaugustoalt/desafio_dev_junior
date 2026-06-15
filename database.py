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

def inserir_inversor(dados):
    """
    Insere uma leitura válida de inversor no banco.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    # Insere apenas os campos principais definidos na modelagem
    cursor.execute("""
        INSERT INTO leituras_inversor (
            sn,
            tsleitura,
            pac,
            uac,
            iac,
            fac,
            temp
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        dados["sn"],
        dados["tsleitura"],
        float(dados["Pac"]),
        float(dados["Uac"]),
        float(dados["Iac"]),
        float(dados["fac"]),
        float(dados["Temp"])
    ))

    conexao.commit()
    conexao.close()


def inserir_rele(dados):
    """
    Insere uma leitura válida de relé de proteção no banco.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    # Insere os principais campos elétricos do relé
    cursor.execute("""
        INSERT INTO leituras_rele (
            sn,
            tsleitura,
            tplei,
            rfreq,
            rifasea,
            rifaseb,
            rifasec,
            rvfasea,
            rvfaseb,
            rvfasec,
            rpac,
            rtempinterno
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        dados["sn"],
        dados["tsleitura"],
        dados["tpLei"],
        float(dados["rFREQ"]),
        float(dados["rIfaseA"]),
        float(dados["rIfaseB"]),
        float(dados["rIfaseC"]),
        float(dados["rVfaseA"]),
        float(dados["rVfaseB"]),
        float(dados["rVfaseC"]),
        float(dados["rpac"]),
        float(dados["rtempinterno"])
    ))

    conexao.commit()
    conexao.close()

def inserir_estacao(dados):
    """
    Insere uma leitura válida de estação solarimétrica no banco.
    """

    conexao = conectar()
    cursor = conexao.cursor()

    # Na estação, vários valores vêm como string, então convertemos para float
    cursor.execute("""
        INSERT INTO leituras_estacao (
            sn,
            tsleitura,
            tplei,
            irghi,
            irpoa,
            umid,
            tempamb,
            tempmedmod,
            velvento
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        dados["sn"],
        dados["tsleitura"],
        dados["tpLei"],
        float(dados["IrGHI"]),
        float(dados["IrPOA"]),
        float(dados["Umid"]),
        float(dados["tempAmb"]),
        float(dados["tempMedMod"]),
        float(dados["velVento"])
    ))

    conexao.commit()
    conexao.close()