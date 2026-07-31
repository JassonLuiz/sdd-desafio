import json
from datetime import date
from decimal import Decimal


class MoedaNaoSuportadaError(Exception):
    pass


class TaxaIndisponivelError(Exception):
    pass


def carregar_cambio(caminho) -> dict:
    with open(caminho, encoding="utf-8") as f:
        raw = json.load(f, parse_float=Decimal, parse_int=Decimal)
    # Converte chaves de data de str para date
    return {
        date.fromisoformat(d): taxas
        for d, taxas in raw["taxas"].items()
    }


def buscar_taxa(tabela: dict, moeda: str, data_despesa: date) -> Decimal:
    # AMB-019: moeda inteiramente ausente de todas as entradas
    if not any(moeda in taxas for taxas in tabela.values()):
        raise MoedaNaoSuportadaError(moeda)

    # AMB-018: busca data exata ou anterior mais próxima
    candidatas = sorted(
        (d for d in tabela if d <= data_despesa and moeda in tabela[d]),
        reverse=True,
    )
    if not candidatas:
        raise TaxaIndisponivelError(moeda, data_despesa)

    return tabela[candidatas[0]][moeda]
