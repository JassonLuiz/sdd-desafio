import json
from datetime import date
from decimal import Decimal
from pathlib import Path

from src.modelos import Colaborador, DespesaBruta, Periodo


def carregar_entrada(caminho: str | Path) -> tuple[Colaborador, Periodo, list[DespesaBruta]]:
    with open(caminho, encoding="utf-8") as f:
        dados = json.load(f, parse_float=Decimal, parse_int=Decimal)

    colaborador = Colaborador(
        id=str(dados["colaborador"]["id"]),
        nome=str(dados["colaborador"]["nome"]),
        centro_custo=str(dados["colaborador"]["centro_custo"]),
    )

    periodo = Periodo(
        competencia=str(dados["periodo"]["competencia"]),
        inicio=date.fromisoformat(str(dados["periodo"]["inicio"])),
        fim=date.fromisoformat(str(dados["periodo"]["fim"])),
    )

    despesas = [
        DespesaBruta(
            id=str(item["id"]),
            data=date.fromisoformat(str(item["data"])),
            categoria=str(item["categoria"]),
            descricao=str(item["descricao"]),
            fornecedor=str(item["fornecedor"]),
            valor_original=item["valor"],
            tem_nota_fiscal=bool(item["tem_nota_fiscal"]),
            moeda=str(item.get("moeda", "BRL")),
        )
        for item in dados["despesas"]
    ]

    return colaborador, periodo, despesas
