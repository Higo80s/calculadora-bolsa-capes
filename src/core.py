from datetime import date
from dateutil.relativedelta import relativedelta

def calcular_prazo_bolsa(ingresso: date, inicio: date, nivel: str) -> dict:
    if nivel not in ('mestrado', 'doutorado'):
        raise ValueError("Nível deve ser 'mestrado' ou 'doutorado'.")

    limite_meses = 24 if nivel == 'mestrado' else 48
    data_limite_periodo = ingresso + relativedelta(months=limite_meses)
    ultimo_dia_periodo = data_limite_periodo - relativedelta(days=1)

    if inicio < ingresso:
        raise ValueError("Data de início da bolsa não pode ser anterior ao ingresso.")

    max_meses = 0
    for m in range(1, limite_meses + 1):
        ultimo_dia_tentativa = (inicio + relativedelta(months=m - 1)).replace(day=1)
        ultimo_dia_tentativa = ultimo_dia_tentativa + relativedelta(months=1, days=-1)
        if ultimo_dia_tentativa <= ultimo_dia_periodo:
            max_meses = m
        else:
            break

    if max_meses == 0:
        ultimo_pagamento = None
    else:
        ultimo_pagamento = (inicio + relativedelta(months=max_meses - 1)).replace(day=1)
        ultimo_pagamento = ultimo_pagamento + relativedelta(months=1, days=-1)

    return {
        "max_meses": max_meses,
        "ultimo_pagamento": ultimo_pagamento,
        "data_limite_periodo": ultimo_dia_periodo,
        "conforme": max_meses > 0
    }
    