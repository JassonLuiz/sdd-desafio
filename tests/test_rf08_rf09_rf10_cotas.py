from datetime import date
from decimal import Decimal

import pytest

from src.cotas import GerenciadorCotas


# --- RF-08: alimentação ---

def test_rf08_agregado_diario_corte(despesa_factory):
    gc = GerenciadorCotas()
    despesa = despesa_factory(categoria="alimentacao", valor=Decimal("72.50"))
    valor, motivo = gc.calcular_reembolso(despesa)
    assert valor == Decimal("60.00")
    assert motivo == "LIMITE_DIARIO"


def test_rf08_cota_esgotada_segundo_item(despesa_factory):
    gc = GerenciadorCotas()
    d1 = despesa_factory(id="d-001", categoria="alimentacao", valor=Decimal("60.00"))
    d2 = despesa_factory(id="d-002", categoria="alimentacao", valor=Decimal("38.00"))
    gc.calcular_reembolso(d1)
    valor, motivo = gc.calcular_reembolso(d2)
    assert valor == Decimal("0.00")
    assert motivo == "COTA_ESGOTADA"


def test_rf08_dentro_do_limite_aprovado(despesa_factory):
    gc = GerenciadorCotas()
    despesa = despesa_factory(categoria="alimentacao", valor=Decimal("30.00"))
    valor, motivo = gc.calcular_reembolso(despesa)
    assert valor == Decimal("30.00")
    assert motivo is None


# --- RF-09: transporte_urbano ---

def test_rf09_agregado_diario_corte(despesa_factory):
    gc = GerenciadorCotas()
    despesa = despesa_factory(categoria="transporte_urbano", valor=Decimal("100.00"))
    valor, motivo = gc.calcular_reembolso(despesa)
    assert valor == Decimal("80.00")
    assert motivo == "LIMITE_DIARIO"


# --- RF-10: hospedagem ---

def test_rf10_limite_por_lancamento(despesa_factory):
    gc = GerenciadorCotas()
    despesa = despesa_factory(categoria="hospedagem", valor=Decimal("480.00"))
    valor, motivo = gc.calcular_reembolso(despesa)
    assert valor == Decimal("250.00")
    assert motivo == "LIMITE_DIARIO"


def test_rf10_descricao_ignorada(despesa_factory):
    gc = GerenciadorCotas()
    despesa = despesa_factory(
        categoria="hospedagem",
        descricao="2 diárias Hotel XYZ",
        valor=Decimal("480.00"),
    )
    valor, motivo = gc.calcular_reembolso(despesa)
    assert valor == Decimal("250.00")
    assert motivo == "LIMITE_DIARIO"


def test_rf10_duas_hospedagens_mesmo_dia_independentes(despesa_factory):
    gc = GerenciadorCotas()
    d1 = despesa_factory(id="d-A", categoria="hospedagem", data=date(2026, 7, 15), valor=Decimal("200.00"))
    d2 = despesa_factory(id="d-B", categoria="hospedagem", data=date(2026, 7, 15), valor=Decimal("200.00"))
    valor1, motivo1 = gc.calcular_reembolso(d1)
    valor2, motivo2 = gc.calcular_reembolso(d2)
    assert valor1 == Decimal("200.00") and motivo1 is None
    assert valor2 == Decimal("200.00") and motivo2 is None


# --- RF-12: corte não recusa ---

def test_rf12_exceder_limite_nao_recusa(despesa_factory):
    gc = GerenciadorCotas()
    despesa = despesa_factory(categoria="alimentacao", valor=Decimal("72.50"))
    valor, motivo = gc.calcular_reembolso(despesa)
    assert valor > Decimal("0.00")
    assert motivo == "LIMITE_DIARIO"
