from datetime import date
from decimal import Decimal

import pytest

from src.cotas import GerenciadorCotas

_POLITICA_V3 = {
    "alimentacao":       {"limite": Decimal("60.00"),  "periodicidade": "dia"},
    "transporte_urbano": {"limite": Decimal("80.00"),  "periodicidade": "dia"},
    "hospedagem":        {"limite": Decimal("250.00"), "periodicidade": "diaria"},
}

_POLITICA_CC_COMERCIAL = {
    "alimentacao":       {"limite": Decimal("90.00"),  "periodicidade": "dia"},
    "transporte_urbano": {"limite": Decimal("150.00"), "periodicidade": "dia"},
    "hospedagem":        {"limite": Decimal("400.00"), "periodicidade": "diaria"},
    "representacao":     {"limite": Decimal("300.00"), "periodicidade": "dia"},
}

_POLITICA_CC_ENG = {
    "alimentacao":       {"limite": Decimal("60.00"),  "periodicidade": "dia"},
    "transporte_urbano": {"limite": Decimal("80.00"),  "periodicidade": "dia"},
    "hospedagem":        {"limite": Decimal("0.00"),   "periodicidade": "diaria"},
}


# --- RF-08: alimentação ---

def test_rf08_agregado_diario_corte(despesa_factory):
    gc = GerenciadorCotas(_POLITICA_V3)
    despesa = despesa_factory(categoria="alimentacao", valor=Decimal("72.50"))
    valor, motivo = gc.calcular_reembolso(despesa)
    assert valor == Decimal("60.00")
    assert motivo == "LIMITE_DIARIO"


def test_rf08_cota_esgotada_segundo_item(despesa_factory):
    gc = GerenciadorCotas(_POLITICA_V3)
    d1 = despesa_factory(id="d-001", categoria="alimentacao", valor=Decimal("60.00"))
    d2 = despesa_factory(id="d-002", categoria="alimentacao", valor=Decimal("38.00"))
    gc.calcular_reembolso(d1)
    valor, motivo = gc.calcular_reembolso(d2)
    assert valor == Decimal("0.00")
    assert motivo == "COTA_ESGOTADA"


def test_rf08_dentro_do_limite_aprovado(despesa_factory):
    gc = GerenciadorCotas(_POLITICA_V3)
    despesa = despesa_factory(categoria="alimentacao", valor=Decimal("30.00"))
    valor, motivo = gc.calcular_reembolso(despesa)
    assert valor == Decimal("30.00")
    assert motivo is None


# --- RF-09: transporte_urbano ---

def test_rf09_agregado_diario_corte(despesa_factory):
    gc = GerenciadorCotas(_POLITICA_V3)
    despesa = despesa_factory(categoria="transporte_urbano", valor=Decimal("100.00"))
    valor, motivo = gc.calcular_reembolso(despesa)
    assert valor == Decimal("80.00")
    assert motivo == "LIMITE_DIARIO"


# --- RF-10: hospedagem ---

def test_rf10_limite_por_lancamento(despesa_factory):
    gc = GerenciadorCotas(_POLITICA_V3)
    despesa = despesa_factory(categoria="hospedagem", valor=Decimal("480.00"))
    valor, motivo = gc.calcular_reembolso(despesa)
    assert valor == Decimal("250.00")
    assert motivo == "LIMITE_DIARIO"


def test_rf10_descricao_ignorada(despesa_factory):
    gc = GerenciadorCotas(_POLITICA_V3)
    despesa = despesa_factory(
        categoria="hospedagem",
        descricao="2 diárias Hotel XYZ",
        valor=Decimal("480.00"),
    )
    valor, motivo = gc.calcular_reembolso(despesa)
    assert valor == Decimal("250.00")
    assert motivo == "LIMITE_DIARIO"


def test_rf10_duas_hospedagens_mesmo_dia_independentes(despesa_factory):
    gc = GerenciadorCotas(_POLITICA_V3)
    d1 = despesa_factory(id="d-A", categoria="hospedagem", data=date(2026, 7, 15), valor=Decimal("200.00"))
    d2 = despesa_factory(id="d-B", categoria="hospedagem", data=date(2026, 7, 15), valor=Decimal("200.00"))
    valor1, motivo1 = gc.calcular_reembolso(d1)
    valor2, motivo2 = gc.calcular_reembolso(d2)
    assert valor1 == Decimal("200.00") and motivo1 is None
    assert valor2 == Decimal("200.00") and motivo2 is None


# --- RF-12: corte não recusa ---

def test_rf12_exceder_limite_nao_recusa(despesa_factory):
    gc = GerenciadorCotas(_POLITICA_V3)
    despesa = despesa_factory(categoria="alimentacao", valor=Decimal("72.50"))
    valor, motivo = gc.calcular_reembolso(despesa)
    assert valor > Decimal("0.00")
    assert motivo == "LIMITE_DIARIO"


# --- RF-17 + T-027: política efetiva por CC ---

def test_rf10_periodicidade_diaria_por_lancamento(despesa_factory):
    # periodicidade="diaria" → cada lançamento tem saldo próprio (chave por id, não por data)
    gc = GerenciadorCotas(_POLITICA_V3)
    d1 = despesa_factory(id="h-001", categoria="hospedagem", data=date(2026, 7, 20), valor=Decimal("250.00"))
    d2 = despesa_factory(id="h-002", categoria="hospedagem", data=date(2026, 7, 20), valor=Decimal("250.00"))
    valor1, motivo1 = gc.calcular_reembolso(d1)
    valor2, motivo2 = gc.calcular_reembolso(d2)
    assert valor1 == Decimal("250.00") and motivo1 is None
    assert valor2 == Decimal("250.00") and motivo2 is None


def test_rf08_cc_comercial_limite_90(despesa_factory):
    # alimentacao CC-COMERCIAL: limite 90,00 → valor de R$95 cortado em 90
    gc = GerenciadorCotas(_POLITICA_CC_COMERCIAL)
    despesa = despesa_factory(categoria="alimentacao", valor=Decimal("95.00"))
    valor, motivo = gc.calcular_reembolso(despesa)
    assert valor == Decimal("90.00")
    assert motivo == "LIMITE_DIARIO"


def test_rf09_cc_comercial_transporte_150(despesa_factory):
    # transporte CC-COMERCIAL: limite 150,00 → valor de R$180 cortado em 150
    gc = GerenciadorCotas(_POLITICA_CC_COMERCIAL)
    despesa = despesa_factory(categoria="transporte_urbano", valor=Decimal("180.00"))
    valor, motivo = gc.calcular_reembolso(despesa)
    assert valor == Decimal("150.00")
    assert motivo == "LIMITE_DIARIO"


def test_rf10_cc_eng_hospedagem_zero_cota_esgotada(despesa_factory):
    # limite 0,00 → saldo = 0 desde o início → sempre COTA_ESGOTADA (D-005)
    gc = GerenciadorCotas(_POLITICA_CC_ENG)
    despesa = despesa_factory(categoria="hospedagem", valor=Decimal("150.00"))
    valor, motivo = gc.calcular_reembolso(despesa)
    assert valor == Decimal("0.00")
    assert motivo == "COTA_ESGOTADA"
