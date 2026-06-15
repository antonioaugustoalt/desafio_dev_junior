from datetime import datetime
from pathlib import Path


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "leituras_descartadas.log"


def registrar_descarte(tipo, motivo, dados):
    """
    Registra leituras descartadas para auditoria.
    """

    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as arquivo:
        arquivo.write(
            f"{horario} | {tipo} | {motivo} | {dados}\n"
        )