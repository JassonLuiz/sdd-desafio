from datetime import date
from decimal import Decimal

from src.regras import verificar_competencia


def test_rf04_data_anterior_recusada(despesa_factory, periodo_padrao):
    despesa = despesa_factory(data=date(2026, 4, 15))
    resultado = verificar_competencia(despesa, periodo_padrao)
    assert resultado is not None
    assert resultado.motivo_codigo == "FORA_COMPETENCIA"
    assert resultado.valor_reembolsavel == Decimal("0.00")


def test_rf04_data_posterior_recusada(despesa_factory, periodo_padrao):
    despesa = despesa_factory(data=date(2026, 8, 1))
    resultado = verificar_competencia(despesa, periodo_padrao)
    assert resultado is not None
    assert resultado.motivo_codigo == "FORA_COMPETENCIA"


def test_rf04_limite_inclusivo_inicio(despesa_factory, periodo_padrao):
    despesa = despesa_factory(data=date(2026, 7, 1))
    assert verificar_competencia(despesa, periodo_padrao) is None


def test_rf04_limite_inclusivo_fim(despesa_factory, periodo_padrao):
    despesa = despesa_factory(data=date(2026, 7, 31))
    assert verificar_competencia(despesa, periodo_padrao) is None
