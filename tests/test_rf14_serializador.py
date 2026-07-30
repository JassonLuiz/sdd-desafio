import json
from datetime import date
from decimal import Decimal

from src.modelos import Colaborador, Periodo, Resultado, ResultadoItem, Resumo
from src.serializador import serializar


def _make_resultado(itens, resumo_override=None):
    colaborador = Colaborador(id="c-0001", nome="Teste", centro_custo="CC-TEST")
    periodo = Periodo(competencia="2026-07", inicio=date(2026, 7, 1), fim=date(2026, 7, 31))
    resumo = resumo_override or Resumo(
        total_solicitado=Decimal("0.00"),
        total_reembolsavel=Decimal("0.00"),
        total_recusado=Decimal("0.00"),
        itens_processados=len(itens),
        itens_aprovados=0,
        itens_parciais=0,
        itens_recusados=0,
    )
    return Resultado(colaborador=colaborador, periodo=periodo, resumo=resumo, itens=tuple(itens))


def _item(id="d-001", status="aprovado", valor_original="30.00",
          valor_considerado="30.00", valor_reembolsavel="30.00",
          motivo_codigo=None, motivo_texto=None, duplicata_de=None):
    return ResultadoItem(
        id=id, status=status,
        valor_original=Decimal(valor_original),
        valor_considerado=Decimal(valor_considerado),
        valor_reembolsavel=Decimal(valor_reembolsavel),
        motivo_codigo=motivo_codigo,
        motivo_texto=motivo_texto,
        duplicata_de=duplicata_de,
    )


def test_rf14_saidas_identicas_mesma_entrada():
    resultado = _make_resultado([_item()])
    assert serializar(resultado) == serializar(resultado)


def test_rf14_valor_original_preserva_33_333():
    item = _item(valor_original="33.333", valor_considerado="33.33", valor_reembolsavel="33.33")
    saida = serializar(_make_resultado([item]))
    assert '"valor_original": 33.333' in saida
    assert '"valor_original": 33.33,' not in saida


def test_rf14_campos_calculados_com_2dp():
    item = _item(valor_original="72.50", valor_considerado="72.50", valor_reembolsavel="60.00",
                 status="parcial", motivo_codigo="LIMITE_DIARIO",
                 motivo_texto="limite diário de alimentacao: reembolsado R$ 60,00 de R$ 72,50")
    resumo = Resumo(
        total_solicitado=Decimal("72.50"),
        total_reembolsavel=Decimal("60.00"),
        total_recusado=Decimal("12.50"),
        itens_processados=1, itens_aprovados=0, itens_parciais=1, itens_recusados=0,
    )
    saida = serializar(_make_resultado([item], resumo_override=resumo))
    assert '"valor_reembolsavel": 60.00' in saida
    assert '"valor_considerado": 72.50' in saida
    assert '"total_reembolsavel": 60.00' in saida
    assert '"total_recusado": 12.50' in saida


def test_rf14_valor_original_inteiro_sem_dp():
    item = _item(valor_original="480", valor_considerado="480.00", valor_reembolsavel="250.00",
                 status="parcial", motivo_codigo="LIMITE_DIARIO",
                 motivo_texto="limite diário de hospedagem: reembolsado R$ 250,00 de R$ 480,00")
    saida = serializar(_make_resultado([item]))
    # Verifica a string literal — json.loads() não distingue 480 de 480.0
    assert '"valor_original": 480' in saida
    assert '"valor_original": 480.0' not in saida


def test_rf14_saida_e_json_valido():
    resultado = _make_resultado([_item()])
    saida = serializar(resultado)
    parsed = json.loads(saida)
    assert "colaborador" in parsed
    assert "resumo" in parsed
    assert "itens" in parsed
