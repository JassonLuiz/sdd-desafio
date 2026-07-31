from decimal import Decimal
from pathlib import Path

import pytest

from src.motor import processar
from src.normalizacao import normalizar_categoria
from src.parser import carregar_entrada
from src.parser_politica import carregar_politica, nota_fiscal_gatilho, politica_efetiva
from src.serializador import serializar

_EXEMPLO = Path(__file__).parent.parent / "exemplos" / "despesas-exemplo.json"
_POLITICA_PATH = Path(__file__).parent.parent / "exemplos" / "envelope" / "politica-v4.json"

_pol = carregar_politica(_POLITICA_PATH)
_gnf = nota_fiscal_gatilho(_pol)


@pytest.fixture(scope="module")
def _resultado():
    colaborador, periodo, despesas = carregar_entrada(_EXEMPLO)
    eff = politica_efetiva(_pol, colaborador.centro_custo)
    return processar(colaborador, periodo, despesas, politica_eff=eff, gatilho_nf=_gnf)


@pytest.fixture(scope="module")
def _por_id(_resultado):
    return {item.id: item for item in _resultado.itens}


def test_integracao_d001(_por_id):
    # d-001: alimentação R$72,50 → aprovado (CC-ENG-PLATAFORMA limite=75; 72,50 < 75)
    item = _por_id["d-001"]
    assert item.status == "aprovado"
    assert item.valor_reembolsavel == Decimal("72.50")
    assert item.motivo_codigo is None


def test_integracao_d002(_por_id):
    # d-002: alimentação R$38,00, mesmo dia de d-001 — saldo restante = 75 - 72,50 = 2,50
    item = _por_id["d-002"]
    assert item.status == "parcial"
    assert item.valor_reembolsavel == Decimal("2.50")
    assert item.motivo_codigo == "LIMITE_DIARIO"


def test_integracao_d003(_por_id):
    # d-003: transporte R$100,00 sem NF → parcial R$80,00 (NF não exigida para R$100,00 exato)
    item = _por_id["d-003"]
    assert item.status == "parcial"
    assert item.valor_reembolsavel == Decimal("80.00")
    assert item.motivo_codigo == "LIMITE_DIARIO"


def test_integracao_d004(_por_id):
    # d-004: transporte R$100,01 sem NF → recusado SEM_NF; motivo SEM_NF prova que
    # passo 7 não foi alcançado → cota de transporte de 06/07 não afetada por este item
    item = _por_id["d-004"]
    assert item.status == "recusado"
    assert item.motivo_codigo == "SEM_NF"


def test_integracao_d005(_por_id):
    # d-005: coworking → recusado CATEGORIA_INVALIDA; motivo_texto cita "coworking"
    item = _por_id["d-005"]
    assert item.status == "recusado"
    assert item.motivo_codigo == "CATEGORIA_INVALIDA"
    assert "coworking" in item.motivo_texto


def test_integracao_d006(_por_id):
    # d-006: alimentação R$54,90 (09/07) → aprovado
    item = _por_id["d-006"]
    assert item.status == "aprovado"
    assert item.valor_reembolsavel == Decimal("54.90")


def test_integracao_d007(_por_id):
    # d-007: duplicata exata de d-006 → recusado DUPLICATA; duplicata_de = "d-006"
    item = _por_id["d-007"]
    assert item.status == "recusado"
    assert item.motivo_codigo == "DUPLICATA"
    assert item.duplicata_de == "d-006"


def test_integracao_d008(_por_id):
    # d-008: data 2026-04-15 fora do período → recusado FORA_COMPETENCIA
    item = _por_id["d-008"]
    assert item.status == "recusado"
    assert item.motivo_codigo == "FORA_COMPETENCIA"


def test_integracao_d009(_por_id):
    # d-009: transporte -R$45,00 → recusado VALOR_NAO_POSITIVO
    item = _por_id["d-009"]
    assert item.status == "recusado"
    assert item.motivo_codigo == "VALOR_NAO_POSITIVO"


def test_integracao_d010(_por_id):
    # d-010: hospedagem R$480,00 → CC-ENG-PLATAFORMA limite=0,00 → COTA_ESGOTADA (template limite=0)
    item = _por_id["d-010"]
    assert item.status == "recusado"
    assert item.valor_reembolsavel == Decimal("0.00")
    assert item.motivo_codigo == "COTA_ESGOTADA"
    assert "não reembolsável pela política do centro de custo" in item.motivo_texto


def test_integracao_d011(_por_id):
    # d-011: valor 33.333 → valor_original preservado, valor_considerado 33.33; aprovado
    item = _por_id["d-011"]
    assert item.valor_original == Decimal("33.333")
    assert item.valor_considerado == Decimal("33.33")
    assert item.status == "aprovado"
    assert item.valor_reembolsavel == Decimal("33.33")


def test_integracao_d012(_por_id):
    # d-012: sábado 18/07, alimentação R$47,20 → aprovado (dias da semana sem distinção)
    item = _por_id["d-012"]
    assert item.status == "aprovado"
    assert item.valor_reembolsavel == Decimal("47.20")


def test_integracao_d013(_por_id):
    # d-013: hospedagem R$690,00 sem NF → recusado SEM_NF (NF check antes de cotas)
    item = _por_id["d-013"]
    assert item.status == "recusado"
    assert item.motivo_codigo == "SEM_NF"


def test_integracao_d014(_por_id):
    # d-014: "ALIMENTACAO" R$61,00 → normalizada; CC-ENG limite=75; 61 < 75 → aprovado
    item = _por_id["d-014"]
    assert item.valor_considerado == Decimal("61.00")
    assert item.status == "aprovado"
    assert item.valor_reembolsavel == Decimal("61.00")
    assert item.motivo_codigo is None


def test_integracao_saida_deterministica():
    # Critério 15: duas execuções com a mesma entrada produzem saída byte a byte idêntica
    colaborador, periodo, despesas = carregar_entrada(_EXEMPLO)
    eff = politica_efetiva(_pol, colaborador.centro_custo)
    assert (
        serializar(processar(colaborador, periodo, despesas, politica_eff=eff, gatilho_nf=_gnf))
        == serializar(processar(colaborador, periodo, despesas, politica_eff=eff, gatilho_nf=_gnf))
    )


def test_integracao_nenhum_item_acima_do_limite_da_categoria():
    # Critério 16: para cada item de categoria válida, valor_reembolsavel ≤ limite efetivo
    colaborador, periodo, despesas = carregar_entrada(_EXEMPLO)
    eff = politica_efetiva(_pol, colaborador.centro_custo)
    resultado = processar(colaborador, periodo, despesas, politica_eff=eff, gatilho_nf=_gnf)
    por_id = {item.id: item for item in resultado.itens}
    for bruta in despesas:
        categoria = normalizar_categoria(bruta.categoria)
        if categoria in eff:
            limite = eff[categoria]["limite"]
            assert por_id[bruta.id].valor_reembolsavel <= limite


def test_integracao_rf16_suspenso_e_cc_exclusao(_por_id):
    # Critério 17: RF-16 suspenso (sem ampliação) + RF-17 exclusão por CC
    # d-003 prova RF-16: transporte limite=80 (seria 120 com RF-16 ativo); motor usa limite padrão
    assert _por_id["d-003"].valor_reembolsavel == Decimal("80.00")  # não 120,00
    # d-010 prova RF-17 (D-005): hospedagem CC-ENG-PLATAFORMA limite=0,00 → COTA_ESGOTADA imediata
    assert _por_id["d-010"].valor_reembolsavel == Decimal("0.00")   # não 375,00 nem 250,00
