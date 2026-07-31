from datetime import date
from decimal import Decimal

import pytest

from src.motor import processar
from src.modelos import DespesaBruta

_POL_V3 = {
    "alimentacao":       {"limite": Decimal("60.00"),  "periodicidade": "dia"},
    "transporte_urbano": {"limite": Decimal("80.00"),  "periodicidade": "dia"},
    "hospedagem":        {"limite": Decimal("250.00"), "periodicidade": "diaria"},
}
_GNF_V3 = Decimal("100.00")


def _bruta(id, data=date(2026, 7, 15), categoria="alimentacao", descricao="Teste",
           fornecedor="Forn", valor="30.00", tem_nota_fiscal=True):
    return DespesaBruta(
        id=id, data=data, categoria=categoria, descricao=descricao,
        fornecedor=fornecedor, valor_original=Decimal(valor),
        tem_nota_fiscal=tem_nota_fiscal,
    )


def test_rf11_competencia_precede_nf(colaborador_padrao, periodo_padrao):
    # Fora de competência E sem NF: FORA_COMPETENCIA vence (passo 3 antes do 6)
    despesa = _bruta("d-001", data=date(2026, 4, 15), valor="150.00", tem_nota_fiscal=False)
    resultado = processar(colaborador_padrao, periodo_padrao, [despesa], politica_eff=_POL_V3, gatilho_nf=_GNF_V3)
    assert resultado.itens[0].motivo_codigo == "FORA_COMPETENCIA"


def test_rf11_duplicata_de_item_sem_nf(colaborador_padrao, periodo_padrao):
    # Dois itens idênticos, valor > 100, sem NF.
    # Passo 5 (duplicata) executa antes do 6 (NF): d-002 é registrado em vistos
    # quando processado, depois SEM_NF o recusa. d-003 cai no passo 5 como DUPLICATA.
    d1 = _bruta("d-002", valor="120.00", tem_nota_fiscal=False)
    d2 = _bruta("d-003", valor="120.00", tem_nota_fiscal=False)
    resultado = processar(colaborador_padrao, periodo_padrao, [d1, d2], politica_eff=_POL_V3, gatilho_nf=_GNF_V3)
    assert resultado.itens[0].motivo_codigo == "SEM_NF"
    assert resultado.itens[1].motivo_codigo == "DUPLICATA"
    assert resultado.itens[1].duplicata_de == "d-002"


def test_rf12_reembolsa_saldo_disponivel(colaborador_padrao, periodo_padrao):
    # Saldo parcial: primeiro item consome parte da cota, segundo recebe o restante.
    d1 = _bruta("d-001", categoria="alimentacao", valor="45.00")
    d2 = _bruta("d-002", categoria="alimentacao", valor="40.00")
    resultado = processar(colaborador_padrao, periodo_padrao, [d1, d2], politica_eff=_POL_V3, gatilho_nf=_GNF_V3)
    assert resultado.itens[0].valor_reembolsavel == Decimal("45.00")
    assert resultado.itens[1].valor_reembolsavel == Decimal("15.00")  # saldo = 60 - 45
    assert resultado.itens[1].motivo_codigo == "LIMITE_DIARIO"


def test_rf09_sem_nf_nao_consome_cota(colaborador_padrao, periodo_padrao):
    # d-SEM_NF recusado no passo 6 — não deve tocar a cota de transporte do dia.
    # d-ok mesmo dia: deve receber cota intacta (R$80 disponíveis).
    d_sem_nf = _bruta("d-001", data=date(2026, 7, 11), categoria="transporte_urbano",
                      valor="120.00", tem_nota_fiscal=False)
    d_ok = _bruta("d-002", data=date(2026, 7, 11), categoria="transporte_urbano",
                  valor="50.00", tem_nota_fiscal=True)
    resultado = processar(colaborador_padrao, periodo_padrao, [d_sem_nf, d_ok], politica_eff=_POL_V3, gatilho_nf=_GNF_V3)
    assert resultado.itens[0].motivo_codigo == "SEM_NF"
    assert resultado.itens[1].valor_reembolsavel == Decimal("50.00")
    assert resultado.itens[1].motivo_codigo is None


def test_rf13_status_aprovado(colaborador_padrao, periodo_padrao):
    despesa = _bruta("d-001", valor="30.00")
    resultado = processar(colaborador_padrao, periodo_padrao, [despesa], politica_eff=_POL_V3, gatilho_nf=_GNF_V3)
    assert resultado.itens[0].status == "aprovado"
    assert resultado.itens[0].valor_reembolsavel == resultado.itens[0].valor_considerado


def test_rf13_status_parcial(colaborador_padrao, periodo_padrao):
    despesa = _bruta("d-001", categoria="alimentacao", valor="72.50")
    resultado = processar(colaborador_padrao, periodo_padrao, [despesa], politica_eff=_POL_V3, gatilho_nf=_GNF_V3)
    assert resultado.itens[0].status == "parcial"
    assert Decimal("0.00") < resultado.itens[0].valor_reembolsavel < resultado.itens[0].valor_considerado


def test_rf13_cota_esgotada_e_recusado(colaborador_padrao, periodo_padrao):
    # Após cota esgotada, valor_reembolsavel == 0 → status "recusado"
    d1 = _bruta("d-001", categoria="alimentacao", valor="60.00")
    d2 = _bruta("d-002", categoria="alimentacao", valor="20.00")
    resultado = processar(colaborador_padrao, periodo_padrao, [d1, d2], politica_eff=_POL_V3, gatilho_nf=_GNF_V3)
    assert resultado.itens[1].motivo_codigo == "COTA_ESGOTADA"
    assert resultado.itens[1].valor_reembolsavel == Decimal("0.00")
    assert resultado.itens[1].status == "recusado"
