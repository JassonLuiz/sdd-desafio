"""
Casos de borda da seção 7 da spec que cruzam múltiplas regras.

Rastreabilidade — casos já cobertos por testes de RF individuais (T-012):

  test_borda_dois_identicos_acima_100_sem_nf
      → tests/test_motor.py::test_rf11_duplicata_de_item_sem_nf
      Dois itens idênticos, valor > 100, sem NF: primeiro SEM_NF, segundo DUPLICATA
      (passo 5 precede passo 6 — RF-11).

  test_borda_item_fora_competencia_e_sem_nf
      → tests/test_motor.py::test_rf11_competencia_precede_nf
      Item fora de competência E sem NF: FORA_COMPETENCIA vence
      (passo 3 precede passo 6 — RF-11).

  test_borda_cota_esgotada_status_recusado
      → tests/test_motor.py::test_rf13_cota_esgotada_e_recusado
      COTA_ESGOTADA + valor_reembolsavel == 0 → status = "recusado"
      (status derivado aritmeticamente — RF-13).
"""
from datetime import date
from decimal import Decimal

from src.modelos import DespesaBruta
from src.motor import processar

_POL_V3 = {
    "alimentacao":       {"limite": Decimal("60.00"),  "periodicidade": "dia"},
    "transporte_urbano": {"limite": Decimal("80.00"),  "periodicidade": "dia"},
    "hospedagem":        {"limite": Decimal("250.00"), "periodicidade": "diaria"},
}
_GNF_V3 = Decimal("100.00")


def _bruta(id, categoria="alimentacao", valor="30.00", tem_nota_fiscal=True,
           data=date(2026, 7, 14), descricao="Teste", fornecedor="Forn"):
    return DespesaBruta(
        id=id, data=data, categoria=categoria, descricao=descricao,
        fornecedor=fornecedor, valor_original=Decimal(valor),
        tem_nota_fiscal=tem_nota_fiscal,
    )


def test_borda_hospedagem_sem_nf_nao_chega_ao_limite(colaborador_padrao, periodo_padrao):
    # Interação RF-07 × RF-10: SEM_NF (passo 6) precede limite de hospedagem (passo 7).
    # O limite de R$250 nunca é avaliado — prova que os passos não vazam entre si.
    item = processar(
        colaborador_padrao, periodo_padrao,
        [_bruta("d-h01", categoria="hospedagem", valor="690.00", tem_nota_fiscal=False)],
        politica_eff=_POL_V3, gatilho_nf=_GNF_V3,
    ).itens[0]
    assert item.motivo_codigo == "SEM_NF"
    assert item.valor_reembolsavel == Decimal("0.00")
    assert item.status == "recusado"


def test_borda_valor_zero_recusado(colaborador_padrao, periodo_padrao):
    # Valor zero: VALOR_NAO_POSITIVO (passo 2); cota da categoria não é afetada.
    item = processar(
        colaborador_padrao, periodo_padrao,
        [_bruta("d-z01", valor="0.00")],
        politica_eff=_POL_V3, gatilho_nf=_GNF_V3,
    ).itens[0]
    assert item.motivo_codigo == "VALOR_NAO_POSITIVO"
    assert item.valor_reembolsavel == Decimal("0.00")
    assert item.status == "recusado"
