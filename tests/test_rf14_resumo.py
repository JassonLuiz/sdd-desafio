from datetime import date
from decimal import Decimal

from src.modelos import DespesaBruta
from src.motor import processar

_POL_V3 = {
    "alimentacao":       {"limite": Decimal("60.00"),  "periodicidade": "dia"},
    "transporte_urbano": {"limite": Decimal("80.00"),  "periodicidade": "dia"},
    "hospedagem":        {"limite": Decimal("250.00"), "periodicidade": "diaria"},
}
_GNF_V3 = Decimal("100.00")


def _bruta(id, categoria="alimentacao", valor="30.00", data=date(2026, 7, 15),
           descricao="Teste", fornecedor="Forn", tem_nota_fiscal=True):
    return DespesaBruta(
        id=id, data=data, categoria=categoria, descricao=descricao,
        fornecedor=fornecedor, valor_original=Decimal(valor),
        tem_nota_fiscal=tem_nota_fiscal,
    )


def test_rf14_resumo_tres_itens(colaborador_padrao, periodo_padrao):
    # d-001: alimentação R$72,50 → parcial R$60,00 (LIMITE_DIARIO)
    # d-005: categoria coworking → recusado R$0,00 (CATEGORIA_INVALIDA)
    # d-006: alimentação R$54,90, dia diferente → aprovado R$54,90
    despesas = [
        _bruta("d-001", categoria="alimentacao", valor="72.50"),
        _bruta("d-005", categoria="coworking", valor="89.00"),
        _bruta("d-006", categoria="alimentacao", valor="54.90", data=date(2026, 7, 16)),
    ]
    resultado = processar(colaborador_padrao, periodo_padrao, despesas, politica_eff=_POL_V3, gatilho_nf=_GNF_V3)
    resumo = resultado.resumo

    assert resumo.total_solicitado == Decimal("216.40")   # 72.50 + 89.00 + 54.90
    assert resumo.total_reembolsavel == Decimal("114.90") # 60.00 + 0.00 + 54.90
    assert resumo.total_recusado == Decimal("101.50")     # 216.40 - 114.90
    assert resumo.itens_processados == 3
    assert resumo.itens_aprovados == 1
    assert resumo.itens_parciais == 1
    assert resumo.itens_recusados == 1


def test_rf14_valor_negativo_excluido_do_total_solicitado(colaborador_padrao, periodo_padrao):
    # Item com valor_considerado <= 0 não entra em total_solicitado (spec seção 4.2)
    despesas = [
        _bruta("d-neg", valor="-45.00"),
        _bruta("d-pos", valor="30.00", data=date(2026, 7, 16)),
    ]
    resultado = processar(colaborador_padrao, periodo_padrao, despesas, politica_eff=_POL_V3, gatilho_nf=_GNF_V3)
    assert resultado.resumo.total_solicitado == Decimal("30.00")
    assert resultado.resumo.itens_recusados == 1
    assert resultado.resumo.itens_aprovados == 1
