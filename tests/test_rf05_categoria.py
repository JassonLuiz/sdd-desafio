from decimal import Decimal

from src.normalizacao import normalizar_categoria
from src.regras import verificar_categoria

_POLITICA_PADRAO = {
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


def test_rf05_coworking_recusado(despesa_factory):
    despesa = despesa_factory(categoria="coworking")
    resultado = verificar_categoria(despesa, _POLITICA_PADRAO)
    assert resultado is not None
    assert resultado.motivo_codigo == "CATEGORIA_INVALIDA"
    assert "coworking" in resultado.motivo_texto
    assert resultado.valor_reembolsavel == Decimal("0.00")


def test_rf05_categoria_valida_aceita(despesa_factory):
    despesa = despesa_factory(categoria="alimentacao")
    assert verificar_categoria(despesa, _POLITICA_PADRAO) is None


def test_rf05_maiusculas_normalizadas_e_aceitas(despesa_factory):
    # Simula o pipeline em miniatura: normaliza → verifica.
    categoria = normalizar_categoria("ALIMENTACAO")
    despesa = despesa_factory(categoria=categoria)
    assert verificar_categoria(despesa, _POLITICA_PADRAO) is None


def test_rf05_taxi_recusado(despesa_factory):
    despesa = despesa_factory(categoria="taxi")
    resultado = verificar_categoria(despesa, _POLITICA_PADRAO)
    assert resultado is not None
    assert resultado.motivo_codigo == "CATEGORIA_INVALIDA"
    assert "taxi" in resultado.motivo_texto


def test_rf05_representacao_cc_comercial_aceita(despesa_factory):
    # representacao existe em CC-COMERCIAL mas não no padrao
    despesa = despesa_factory(categoria="representacao")
    assert verificar_categoria(despesa, _POLITICA_CC_COMERCIAL) is None


def test_rf05_representacao_cc_suporte_recusada(despesa_factory):
    # representacao ausente do padrao → CATEGORIA_INVALIDA
    despesa = despesa_factory(categoria="representacao")
    resultado = verificar_categoria(despesa, _POLITICA_PADRAO)
    assert resultado is not None
    assert resultado.motivo_codigo == "CATEGORIA_INVALIDA"
    assert "representacao" in resultado.motivo_texto


def test_rf05_coworking_qualquer_cc_recusado(despesa_factory):
    # coworking ausente em todos os CCs, incluindo CC-COMERCIAL
    despesa = despesa_factory(categoria="coworking")
    resultado = verificar_categoria(despesa, _POLITICA_CC_COMERCIAL)
    assert resultado is not None
    assert resultado.motivo_codigo == "CATEGORIA_INVALIDA"
