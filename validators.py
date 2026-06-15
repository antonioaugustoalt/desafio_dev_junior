# Lista de SNs válidos do simulador
SNS_VALIDOS = {
    "inversor": [
        "A2351801217",
        "A2351801218",
        "A2351801219",
        "A23518012110",
        "A23518012111",
    ],
    "rele": [
        "releprote_18746926",
        "releprote_18746927",
        "releprote_18746928",
        "releprote_18746929",
        "releprote_18746930",
    ],
    "estacao": [
        "estacao_18746410",
        "estacao_18746411",
        "estacao_18746412",
        "estacao_18746413",
        "estacao_18746414",
    ],
}


def eh_dicionario(dados):
    """
    Verifica se a resposta recebida é um dicionário.
    Respostas inválidas podem vir como texto ou outros formatos.
    """
    return isinstance(dados, dict)


def tem_campos_obrigatorios(dados, campos):
    """
    Verifica se todos os campos obrigatórios existem no dicionário.
    """
    for campo in campos:
        if campo not in dados:
            return False

    return True


def sn_valido(tipo, sn):
    """
    Verifica se o serial number pertence à lista esperada daquele tipo.
    """
    return sn in SNS_VALIDOS[tipo]


def pode_converter_float(valor):
    """
    Verifica se um valor pode ser convertido para float.
    """
    try:
        float(valor)
        return True
    except (TypeError, ValueError):
        return False
    

def validar_inversor(dados):
    """
    Valida uma leitura do endpoint /inversor.
    Retorna True se a leitura for íntegra, senão False.
    """

    # Garante que a resposta tem formato de dicionário
    if not eh_dicionario(dados):
        return False

    campos_obrigatorios = ["sn", "tsleitura", "Pac"]

    # Garante que os campos essenciais existem
    if not tem_campos_obrigatorios(dados, campos_obrigatorios):
        return False

    # Garante que o SN pertence aos inversores conhecidos
    if not sn_valido("inversor", dados["sn"]):
        return False

    campos_numericos = ["Pac", "Uac", "Iac", "fac", "Temp"]

    # Garante que os principais campos de medição são numéricos
    for campo in campos_numericos:
        if campo not in dados:
            return False

        if not pode_converter_float(dados[campo]):
            return False

    # Evita salvar leitura zerada/anômala
    if float(dados["Pac"]) == 0:
        return False

    return True

def validar_rele(dados):
    """
    Valida uma leitura do endpoint /rele-protecao.
    Retorna True se a leitura for íntegra, senão False.
    """

    # Garante que a resposta tem formato de dicionário
    if not eh_dicionario(dados):
        return False

    campos_obrigatorios = ["sn", "tsleitura", "tpLei"]

    # Garante que os campos essenciais existem
    if not tem_campos_obrigatorios(dados, campos_obrigatorios):
        return False

    # Garante que o SN pertence aos relés conhecidos
    if not sn_valido("rele", dados["sn"]):
        return False

    # Confirma se o tipo da leitura é realmente de relé
    if dados["tpLei"] != "rele":
        return False

    campos_numericos = [
        "rFREQ",
        "rIfaseA",
        "rIfaseB",
        "rIfaseC",
        "rVfaseA",
        "rVfaseB",
        "rVfaseC",
        "rpac",
        "rtempinterno"
    ]

    # Garante que os campos principais de medição são numéricos
    for campo in campos_numericos:
        if campo not in dados:
            return False

        if not pode_converter_float(dados[campo]):
            return False

    # Evita salvar leitura zerada/anômala
    if float(dados["rpac"]) == 0:
        return False

    return True

def validar_estacao(dados):
    """
    Valida uma leitura do endpoint /estacao-solarimetrica.
    Retorna True se a leitura for íntegra, senão False.
    """

    # Garante que a resposta tem formato de dicionário
    if not eh_dicionario(dados):
        return False

    campos_obrigatorios = [
        "sn",
        "tsleitura",
        "tpLei",
        "IrGHI",
        "IrPOA",
        "velVento",
        "tempAmb"
    ]

    # Garante que os campos essenciais existem
    if not tem_campos_obrigatorios(dados, campos_obrigatorios):
        return False

    # Garante que o SN pertence às estações conhecidas
    if not sn_valido("estacao", dados["sn"]):
        return False

    # Confirma se o tipo da leitura é realmente meteorológica
    if dados["tpLei"] != "meteo":
        return False

    campos_numericos = [
        "IrGHI",
        "IrPOA",
        "velVento",
        "tempAmb",
        "Umid",
        "tempMedMod"
    ]

    # Na estação, vários números vêm como texto.
    # O importante é conseguir converter para float.
    for campo in campos_numericos:
        if campo not in dados:
            return False

        if not pode_converter_float(dados[campo]):
            return False

    # Evita salvar leitura zerada/anômala
    if float(dados["IrGHI"]) == 0 and float(dados["IrPOA"]) == 0:
        return False

    return True