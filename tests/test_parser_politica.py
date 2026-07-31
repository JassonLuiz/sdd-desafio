import json
import pytest
from decimal import Decimal
from pathlib import Path

from src.parser_politica import carregar_politica, politica_efetiva, nota_fiscal_gatilho

_POLITICA_V4 = Path(__file__).parent.parent / "exemplos" / "envelope" / "politica-v4.json"


@pytest.fixture(scope="module")
def politica():
    return carregar_politica(_POLITICA_V4)


def test_rf17_cc_comercial_alimentacao_limite_90(politica):
    eff = politica_efetiva(politica, "CC-COMERCIAL")
    assert eff["alimentacao"]["limite"] == Decimal("90.00")


def test_rf17_cc_comercial_representacao_reconhecida(politica):
    eff = politica_efetiva(politica, "CC-COMERCIAL")
    assert "representacao" in eff


def test_rf17_cc_eng_hospedagem_zero(politica):
    eff = politica_efetiva(politica, "CC-ENG-PLATAFORMA")
    assert eff["hospedagem"]["limite"] == Decimal("0.00")


def test_rf17_cc_desconhecido_usa_padrao(politica):
    # CC-SUPORTE-N2 não está em centros_custo — deve ser idêntico ao padrao puro
    eff_desconhecido = politica_efetiva(politica, "CC-SUPORTE-N2")
    eff_inexistente = politica_efetiva(politica, "__inexistente__")
    assert eff_desconhecido == eff_inexistente


def test_rf17_representacao_ausente_do_padrao(politica):
    eff = politica_efetiva(politica, "CC-SUPORTE-N2")
    assert "representacao" not in eff


def test_rf17_padrao_alimentacao_limite_60(politica):
    # padrao (CC desconhecido) mantém o limite original
    eff = politica_efetiva(politica, "__inexistente__")
    assert eff["alimentacao"]["limite"] == Decimal("60.00")


def test_rf17_nota_fiscal_gatilho(politica):
    assert nota_fiscal_gatilho(politica) == Decimal("100.00")


def test_rf17_cc_adm_herda_hospedagem_completo_do_padrao(politica):
    # CC-ADM não lista hospedagem — deve herdar limite E periodicidade do padrao
    eff = politica_efetiva(politica, "CC-ADM")
    assert eff["hospedagem"]["limite"] == Decimal("250.00")
    assert eff["hospedagem"]["periodicidade"] == "diaria"


def test_rf17_periodicidade_invalida_erro():
    politica_invalida = {
        "padrao": {
            "alimentacao": {"limite": 60.0, "periodicidade": "semana"}
        },
        "centros_custo": {},
        "nota_fiscal_obrigatoria_acima_de": 100.0,
        "acrescimo_em_viagem_percentual": 50,
    }
    with pytest.raises(ValueError, match="periodicidade inválida"):
        from src.parser_politica import _validar_periodicidades
        _validar_periodicidades(politica_invalida)
