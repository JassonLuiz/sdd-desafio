from decimal import Decimal
from pathlib import Path

from src.motor import processar
from src.parser import carregar_entrada
from src.parser_cambio import carregar_cambio
from src.parser_politica import carregar_politica, nota_fiscal_gatilho, politica_efetiva

_ENV_PATH = Path(__file__).parent.parent / "exemplos" / "envelope" / "despesas-envelope.json"
_CC_PATH  = Path(__file__).parent.parent / "exemplos" / "envelope" / "despesas-envelope-cc-desconhecido.json"
_POL_PATH = Path(__file__).parent.parent / "exemplos" / "envelope" / "politica-v4.json"
_CAM_PATH = Path(__file__).parent.parent / "exemplos" / "envelope" / "cambio.json"

_pol = carregar_politica(_POL_PATH)
_gnf = nota_fiscal_gatilho(_pol)
_cam = carregar_cambio(_CAM_PATH)


def _processar(path):
    col, per, desp = carregar_entrada(path)
    eff = politica_efetiva(_pol, col.centro_custo)
    return {
        it.id: it
        for it in processar(col, per, desp, politica_eff=eff, gatilho_nf=_gnf, tabela_cambio=_cam).itens
    }


_env = _processar(_ENV_PATH)
_cc  = _processar(_CC_PATH)


# ── e-001..e-010 (CC-COMERCIAL) ────────────────────────────────────────────

def test_e001_representacao_limite_cc():
    # representacao R$340,00 → CC-COMERCIAL limite=300 → parcial R$300 (RF-05, RF-17)
    it = _env["e-001"]
    assert it.status == "parcial"
    assert it.valor_reembolsavel == Decimal("300.00")
    assert it.motivo_codigo == "LIMITE_DIARIO"


def test_e002_eur_conversao_e_limite_cc():
    # EUR 22,00 × 5,93 = R$130,46 → limite alimentacao CC-COMERCIAL 90 → parcial (RF-01, RF-18)
    it = _env["e-002"]
    assert it.moeda == "EUR"
    assert it.taxa_cambio_aplicada == Decimal("5.93")
    assert it.valor_original == Decimal("22.00")
    assert it.valor_considerado == Decimal("130.46")
    assert it.status == "parcial"
    assert it.valor_reembolsavel == Decimal("90.00")
    assert it.motivo_codigo == "LIMITE_DIARIO"


def test_e003_eur_sem_nf_abaixo_limiar_brl():
    # EUR 14,50 × 5,88 = R$85,26 ≤ 100 → NF não exigida (RF-07); 85,26 ≤ 90 → aprovado (RF-18)
    it = _env["e-003"]
    assert it.moeda == "EUR"
    assert it.taxa_cambio_aplicada == Decimal("5.88")
    assert it.valor_original == Decimal("14.50")
    assert it.valor_considerado == Decimal("85.26")
    assert it.status == "aprovado"
    assert it.motivo_codigo is None


def test_e004_fallback_taxa_sabado():
    # sábado 18/07 sem cotação → fallback sexta 17/07 (EUR 5,96) → R$178,80 → parcial R$90 (RF-18, AMB-018)
    it = _env["e-004"]
    assert it.moeda == "EUR"
    assert it.taxa_cambio_aplicada == Decimal("5.96")
    assert it.valor_considerado == Decimal("178.80")
    assert it.status == "parcial"
    assert it.valor_reembolsavel == Decimal("90.00")
    assert it.motivo_codigo == "LIMITE_DIARIO"


def test_e005_usd_sem_nf_acima_limiar_brl():
    # USD 40,00 × 5,50 = R$220,00 > 100, sem NF → SEM_NF (RF-07, RF-18)
    it = _env["e-005"]
    assert it.moeda == "USD"
    assert it.taxa_cambio_aplicada == Decimal("5.50")
    assert it.valor_considerado == Decimal("220.00")
    assert it.status == "recusado"
    assert it.motivo_codigo == "SEM_NF"


def test_e006_moeda_ausente_da_tabela():
    # GBP não listada em cambio.json → MOEDA_NAO_SUPORTADA no passo 1 (RF-18, AMB-019)
    it = _env["e-006"]
    assert it.moeda == "GBP"
    assert it.taxa_cambio_aplicada is None
    assert it.status == "recusado"
    assert it.motivo_codigo == "MOEDA_NAO_SUPORTADA"


def test_e007_hospedagem_limite_cc_comercial():
    # hospedagem R$1200,00 → CC-COMERCIAL limite=400 por diária → parcial R$400 (RF-10, RF-17)
    it = _env["e-007"]
    assert it.valor_considerado == Decimal("1200.00")
    assert it.status == "parcial"
    assert it.valor_reembolsavel == Decimal("400.00")
    assert it.motivo_codigo == "LIMITE_DIARIO"


def test_e008_alimentacao_brl_acima_limite_cc():
    # R$95,00 > limite CC-COMERCIAL alimentacao 90 → parcial R$90 (dia 23/07, cota independente)
    it = _env["e-008"]
    assert it.valor_considerado == Decimal("95.00")
    assert it.status == "parcial"
    assert it.valor_reembolsavel == Decimal("90.00")
    assert it.motivo_codigo == "LIMITE_DIARIO"


def test_e009_categoria_invalida_coworking():
    # coworking não reconhecida em CC-COMERCIAL → CATEGORIA_INVALIDA (RF-05)
    it = _env["e-009"]
    assert it.status == "recusado"
    assert it.motivo_codigo == "CATEGORIA_INVALIDA"
    assert "coworking" in it.motivo_texto


def test_e010_moeda_ausente_assume_brl():
    # campo moeda ausente → assume BRL; R$88,00 ≤ 90 limite CC-COMERCIAL → aprovado (RF-01, AMB-020)
    it = _env["e-010"]
    assert it.moeda == "BRL"
    assert it.taxa_cambio_aplicada is None
    assert it.valor_considerado == Decimal("88.00")
    assert it.status == "aprovado"


# ── f-001..f-004 (CC-SUPORTE-N2 → não em centros_custo → herda padrao) ────

def test_f001_cc_desconhecido_herda_padrao():
    # CC-SUPORTE-N2 não em centros_custo → usa padrao (alimentacao limite=60); 58 ≤ 60 → aprovado (RF-17, AMB-017)
    it = _cc["f-001"]
    assert it.valor_considerado == Decimal("58.00")
    assert it.status == "aprovado"


def test_f002_hospedagem_padrao():
    # R$310,00 → padrao hospedagem limite=250 → parcial R$250; motivo cita "limite de 1 diária" (RF-10)
    it = _cc["f-002"]
    assert it.valor_considerado == Decimal("310.00")
    assert it.status == "parcial"
    assert it.valor_reembolsavel == Decimal("250.00")
    assert it.motivo_codigo == "LIMITE_DIARIO"
    assert "limite de 1 diária" in it.motivo_texto


def test_f003_representacao_ausente_do_padrao():
    # representacao não existe no padrao (CC-SUPORTE-N2 sem registro) → CATEGORIA_INVALIDA (RF-05, RF-17)
    it = _cc["f-003"]
    assert it.status == "recusado"
    assert it.motivo_codigo == "CATEGORIA_INVALIDA"


def test_f004_usd_aprovado_integralmente():
    # USD 12,00 × 5,48 = R$65,76 ≤ 80 limite padrao transporte → aprovado (RF-18, RF-09)
    it = _cc["f-004"]
    assert it.moeda == "USD"
    assert it.taxa_cambio_aplicada == Decimal("5.48")
    assert it.valor_original == Decimal("12.00")
    assert it.valor_considerado == Decimal("65.76")
    assert it.status == "aprovado"
