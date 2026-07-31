"""
Testes de integração de câmbio no passo 1 do pipeline (RF-18, T-024).
Usa tabela in-memory para isolar do arquivo cambio.json.
"""
from datetime import date
from decimal import Decimal

import pytest

from src.modelos import DespesaBruta
from src.motor import processar

_TABELA = {
    date(2026, 7, 14): {"EUR": Decimal("5.93")},
    date(2026, 7, 15): {"EUR": Decimal("5.88")},
    date(2026, 7, 17): {"EUR": Decimal("5.96"), "USD": Decimal("5.47")},
    date(2026, 7, 20): {"USD": Decimal("5.50")},
    date(2026, 7, 21): {"USD": Decimal("5.48")},
}


def _bruta(id, categoria="alimentacao", valor="30.00", moeda="BRL",
           data=date(2026, 7, 14), tem_nota_fiscal=True):
    return DespesaBruta(
        id=id, data=data, categoria=categoria, descricao="Teste",
        fornecedor="Forn", valor_original=Decimal(valor),
        tem_nota_fiscal=tem_nota_fiscal, moeda=moeda,
    )


def test_rf18_eur_convertido_para_brl(colaborador_padrao, periodo_padrao):
    # EUR 22,00 × 5,93 = 130,46 (half-up)
    item = processar(
        colaborador_padrao, periodo_padrao,
        [_bruta("e-002", valor="22.00", moeda="EUR", data=date(2026, 7, 14))],
        tabela_cambio=_TABELA,
    ).itens[0]
    assert item.valor_original == Decimal("22.00")
    assert item.moeda == "EUR"
    assert item.taxa_cambio_aplicada == Decimal("5.93")
    assert item.valor_considerado == Decimal("130.46")


def test_rf18_valor_original_preservado(colaborador_padrao, periodo_padrao):
    # valor_original ecoa o literal da entrada em moeda estrangeira (AMB-020)
    item = processar(
        colaborador_padrao, periodo_padrao,
        [_bruta("e-x", valor="14.50", moeda="EUR", data=date(2026, 7, 15))],
        tabela_cambio=_TABELA,
    ).itens[0]
    assert item.valor_original == Decimal("14.50")
    assert item.valor_considerado == Decimal("85.26")


def test_rf18_moeda_ausente_recusa_no_passo1(colaborador_padrao, periodo_padrao):
    # GBP ausente da tabela → MOEDA_NAO_SUPORTADA; passos 2-7 não avaliados
    item = processar(
        colaborador_padrao, periodo_padrao,
        [_bruta("e-006", moeda="GBP", valor="55.00", data=date(2026, 7, 21))],
        tabela_cambio=_TABELA,
    ).itens[0]
    assert item.motivo_codigo == "MOEDA_NAO_SUPORTADA"
    assert item.status == "recusado"
    assert item.valor_reembolsavel == Decimal("0.00")
    assert item.moeda == "GBP"
    assert item.taxa_cambio_aplicada is None


def test_rf18_taxa_indisponivel_recusa_no_passo1(colaborador_padrao, periodo_padrao):
    # USD em data anterior a qualquer entrada da tabela → TAXA_INDISPONIVEL
    item = processar(
        colaborador_padrao, periodo_padrao,
        [_bruta("e-x2", moeda="USD", valor="40.00", data=date(2026, 7, 1))],
        tabela_cambio=_TABELA,
    ).itens[0]
    assert item.motivo_codigo == "TAXA_INDISPONIVEL"
    assert item.status == "recusado"
    assert item.moeda == "USD"
    assert item.taxa_cambio_aplicada is None


def test_rf18_brl_nao_converte(colaborador_padrao, periodo_padrao):
    # moeda BRL (ausente na entrada → default) não aciona conversão
    item = processar(
        colaborador_padrao, periodo_padrao,
        [_bruta("d-x", valor="33.333", moeda="BRL")],
        tabela_cambio=_TABELA,
    ).itens[0]
    assert item.moeda == "BRL"
    assert item.taxa_cambio_aplicada is None
    assert item.valor_original == Decimal("33.333")
    assert item.valor_considerado == Decimal("33.33")


def test_rf18_usd_sem_nf_acima_limiar(colaborador_padrao, periodo_padrao):
    # e-005: USD 40,00 × 5,50 = 220,00 > 100 sem NF → SEM_NF (passo 6, não cambio)
    item = processar(
        colaborador_padrao, periodo_padrao,
        [_bruta("e-005", categoria="transporte_urbano", valor="40.00",
                moeda="USD", data=date(2026, 7, 20), tem_nota_fiscal=False)],
        tabela_cambio=_TABELA,
    ).itens[0]
    assert item.motivo_codigo == "SEM_NF"
    assert item.moeda == "USD"
    assert item.taxa_cambio_aplicada == Decimal("5.50")
    assert item.valor_considerado == Decimal("220.00")
