from decimal import Decimal

from src.normalizacao import normalizar_categoria
from src.regras import verificar_categoria


def test_rf05_coworking_recusado(despesa_factory):
    despesa = despesa_factory(categoria="coworking")
    resultado = verificar_categoria(despesa)
    assert resultado is not None
    assert resultado.motivo_codigo == "CATEGORIA_INVALIDA"
    assert "coworking" in resultado.motivo_texto
    assert resultado.valor_reembolsavel == Decimal("0.00")


def test_rf05_categoria_valida_aceita(despesa_factory):
    despesa = despesa_factory(categoria="alimentacao")
    assert verificar_categoria(despesa) is None


def test_rf05_maiusculas_normalizadas_e_aceitas(despesa_factory):
    # Simula o pipeline em miniatura: normaliza → verifica.
    categoria = normalizar_categoria("ALIMENTACAO")
    despesa = despesa_factory(categoria=categoria)
    assert verificar_categoria(despesa) is None


def test_rf05_taxi_recusado(despesa_factory):
    despesa = despesa_factory(categoria="taxi")
    resultado = verificar_categoria(despesa)
    assert resultado is not None
    assert resultado.motivo_codigo == "CATEGORIA_INVALIDA"
    assert "taxi" in resultado.motivo_texto
