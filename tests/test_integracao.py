from decimal import Decimal
from pathlib import Path

import pytest

from src.motor import processar
from src.normalizacao import normalizar_categoria
from src.parser import carregar_entrada
from src.serializador import serializar

_EXEMPLO = Path(__file__).parent.parent / "exemplos" / "despesas-exemplo.json"

_LIMITE_V3 = {
    "alimentacao": Decimal("60.00"),
    "transporte_urbano": Decimal("80.00"),
    "hospedagem": Decimal("250.00"),
}


@pytest.fixture(scope="module")
def _resultado():
    colaborador, periodo, despesas = carregar_entrada(_EXEMPLO)
    return processar(colaborador, periodo, despesas)


@pytest.fixture(scope="module")
def _por_id(_resultado):
    return {item.id: item for item in _resultado.itens}


def test_integracao_d001(_por_id):
    # d-001: alimentação R$72,50 → parcial R$60,00 (LIMITE_DIARIO)
    item = _por_id["d-001"]
    assert item.status == "parcial"
    assert item.valor_reembolsavel == Decimal("60.00")
    assert item.motivo_codigo == "LIMITE_DIARIO"


def test_integracao_d002(_por_id):
    # d-002: alimentação R$38,00, segundo de 03/07 → recusado (COTA_ESGOTADA)
    item = _por_id["d-002"]
    assert item.status == "recusado"
    assert item.valor_reembolsavel == Decimal("0.00")
    assert item.motivo_codigo == "COTA_ESGOTADA"


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
    # d-009: transporte -R$45,00 → recusado VALOR_NAO_POSITIVO; motivo VALOR_NAO_POSITIVO
    # prova que passo 7 não foi alcançado → cota de transporte de 11/07 não afetada
    item = _por_id["d-009"]
    assert item.status == "recusado"
    assert item.motivo_codigo == "VALOR_NAO_POSITIVO"


def test_integracao_d010(_por_id):
    # d-010: hospedagem R$480,00 ("Hotel Rio - 2 diárias") → parcial R$250,00;
    # motivo_texto cita "limite de 1 diária" (RF-10, D-004 — num_diarias ausente do schema)
    item = _por_id["d-010"]
    assert item.status == "parcial"
    assert item.valor_reembolsavel == Decimal("250.00")
    assert item.motivo_codigo == "LIMITE_DIARIO"
    assert "limite de 1 diária" in item.motivo_texto


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
    # d-013: hospedagem R$690,00 sem NF → recusado SEM_NF (limite de hospedagem nunca avaliado)
    item = _por_id["d-013"]
    assert item.status == "recusado"
    assert item.motivo_codigo == "SEM_NF"


def test_integracao_d014(_por_id):
    # d-014: "ALIMENTACAO" R$61,00 → normalizada; valor_considerado 61.00; parcial R$60,00
    item = _por_id["d-014"]
    assert item.valor_considerado == Decimal("61.00")
    assert item.status == "parcial"
    assert item.valor_reembolsavel == Decimal("60.00")
    assert item.motivo_codigo == "LIMITE_DIARIO"


def test_integracao_saida_deterministica():
    # Critério 15: duas execuções com a mesma entrada produzem saída byte a byte idêntica
    colaborador, periodo, despesas = carregar_entrada(_EXEMPLO)
    assert (
        serializar(processar(colaborador, periodo, despesas))
        == serializar(processar(colaborador, periodo, despesas))
    )


def test_integracao_nenhum_item_acima_do_limite_da_categoria():
    # Critério 16: para cada item de categoria válida, valor_reembolsavel ≤ limite base
    colaborador, periodo, despesas = carregar_entrada(_EXEMPLO)
    resultado = processar(colaborador, periodo, despesas)
    por_id = {item.id: item for item in resultado.itens}
    for bruta in despesas:
        categoria = normalizar_categoria(bruta.categoria)
        if categoria in _LIMITE_V3:
            assert por_id[bruta.id].valor_reembolsavel <= _LIMITE_V3[categoria]


def test_integracao_viagem_suspensa_sem_ampliacao(_por_id):
    # Critério 17: nenhum item recebe limites ampliados de viagem (RF-16 suspenso)
    # Com viagem ativa: hospedagem → 375,00; transporte → 120,00. Sem ampliação:
    assert _por_id["d-010"].valor_reembolsavel == Decimal("250.00")  # não 375,00
    assert _por_id["d-003"].valor_reembolsavel == Decimal("80.00")   # não 120,00
