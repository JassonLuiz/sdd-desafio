import json
from decimal import Decimal
from pathlib import Path


def carregar_politica(caminho) -> dict:
    with open(caminho, encoding="utf-8") as f:
        raw = json.load(f, parse_float=Decimal, parse_int=Decimal)
    _validar_periodicidades(raw)
    return raw


def politica_efetiva(politica: dict, centro_custo: str) -> dict:
    padrao = {cat: dict(entry) for cat, entry in politica["padrao"].items()}
    cc_entry = politica.get("centros_custo", {}).get(centro_custo, {})
    merged = dict(padrao)
    for cat, entry in cc_entry.items():
        merged[cat] = dict(entry)
    return merged


def nota_fiscal_gatilho(politica: dict) -> Decimal:
    return politica["nota_fiscal_obrigatoria_acima_de"]


_PERIODICIDADES_VALIDAS = {"dia", "diaria"}


def _validar_periodicidades(politica: dict) -> None:
    for secao, categorias in [
        ("padrao", politica.get("padrao", {})),
        *((cc, cats) for cc, cats in politica.get("centros_custo", {}).items()),
    ]:
        for cat, entry in categorias.items():
            p = entry.get("periodicidade")
            if p not in _PERIODICIDADES_VALIDAS:
                raise ValueError(
                    f"periodicidade inválida '{p}' em '{secao}.{cat}'; "
                    f"valores aceitos: {sorted(_PERIODICIDADES_VALIDAS)}"
                )
