from decimal import Decimal

from src.regras import verificar_duplicata


def test_rf06_duplicata_exata_recusada(despesa_factory):
    vistos = {}
    d1 = despesa_factory(id="d-006")
    d2 = despesa_factory(id="d-007")
    assert verificar_duplicata(d1, vistos) is None
    resultado = verificar_duplicata(d2, vistos)
    assert resultado is not None
    assert resultado.motivo_codigo == "DUPLICATA"
    assert resultado.duplicata_de == "d-006"


def test_rf06_primeiro_mantido(despesa_factory):
    vistos = {}
    d1 = despesa_factory(id="d-006")
    assert verificar_duplicata(d1, vistos) is None


def test_rf06_duplicata_de_recusado_ainda_detectada(despesa_factory):
    # vistos registra todos os itens independentemente do status posterior.
    # TODO (T-012): provar via pipeline completo a interação passos 5→6 —
    # dois itens idênticos com valor > 100 sem NF: primeiro SEM_NF, segundo DUPLICATA
    # (test_rf11_duplicata_de_item_sem_nf).
    vistos = {}
    d1 = despesa_factory(id="d-006")
    d2 = despesa_factory(id="d-007")
    verificar_duplicata(d1, vistos)
    resultado = verificar_duplicata(d2, vistos)
    assert resultado is not None
    assert resultado.duplicata_de == "d-006"


def test_rf06_nao_consome_cota(despesa_factory):
    # Duplicata recusada retorna ResultadoItem sem tocar estado de cotas.
    # TODO (T-012/T-017): provar via pipeline completo que duplicata de item
    # válido não consome cota da categoria no dia.
    vistos = {}
    d1 = despesa_factory(id="d-006")
    d2 = despesa_factory(id="d-007")
    verificar_duplicata(d1, vistos)
    resultado = verificar_duplicata(d2, vistos)
    assert resultado is not None
    assert resultado.status == "recusado"
    assert resultado.valor_reembolsavel == Decimal("0.00")


def test_rf06_itens_diferentes_nao_sao_duplicata(despesa_factory):
    vistos = {}
    d1 = despesa_factory(id="d-001", valor=Decimal("30.00"))
    d2 = despesa_factory(id="d-002", valor=Decimal("45.00"))
    assert verificar_duplicata(d1, vistos) is None
    assert verificar_duplicata(d2, vistos) is None
