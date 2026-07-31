import pytest
from datetime import date
from decimal import Decimal
from pathlib import Path

from src.parser_cambio import (
    carregar_cambio,
    buscar_taxa,
    MoedaNaoSuportadaError,
    TaxaIndisponivelError,
)

_CAMBIO = Path(__file__).parent.parent / "exemplos" / "envelope" / "cambio.json"


@pytest.fixture(scope="module")
def tabela():
    return carregar_cambio(_CAMBIO)


def test_rf18_taxa_data_exata(tabela):
    # EUR em 2026-07-14 existe na tabela — retorna direto
    assert buscar_taxa(tabela, "EUR", date(2026, 7, 14)) == Decimal("5.93")


def test_rf18_fallback_sabado(tabela):
    # 2026-07-18 é sábado — sem publicação; fallback para sexta 2026-07-17 (EUR 5.96)
    assert buscar_taxa(tabela, "EUR", date(2026, 7, 18)) == Decimal("5.96")


def test_rf18_fallback_multiplos_dias(tabela):
    # 2026-07-19 é domingo, 2026-07-18 é sábado — dois dias sem publicação;
    # fallback para sexta 2026-07-17 (USD 5.47)
    assert buscar_taxa(tabela, "USD", date(2026, 7, 19)) == Decimal("5.47")


def test_rf18_moeda_ausente(tabela):
    # GBP não existe em nenhuma entrada da tabela — MOEDA_NAO_SUPORTADA
    with pytest.raises(MoedaNaoSuportadaError):
        buscar_taxa(tabela, "GBP", date(2026, 7, 14))


def test_rf18_sem_data_anterior(tabela):
    # 2026-07-01 é anterior a qualquer data da tabela — TAXA_INDISPONIVEL
    with pytest.raises(TaxaIndisponivelError):
        buscar_taxa(tabela, "USD", date(2026, 7, 1))


def test_rf18_usd_dia_util(tabela):
    # USD em 2026-07-21 (segunda) → 5.48
    assert buscar_taxa(tabela, "USD", date(2026, 7, 21)) == Decimal("5.48")


def test_rf18_usd_20julho(tabela):
    # e-005: USD 40,00 em 2026-07-20 → taxa 5.50
    assert buscar_taxa(tabela, "USD", date(2026, 7, 20)) == Decimal("5.50")
