from decimal import Decimal

from src.regras import verificar_nf


def test_rf07_fronteira_100_sem_nf_passa(despesa_factory):
    despesa = despesa_factory(valor=Decimal("100.00"), tem_nota_fiscal=False)
    assert verificar_nf(despesa) is None


def test_rf07_fronteira_100_01_sem_nf_recusa(despesa_factory):
    despesa = despesa_factory(valor=Decimal("100.01"), tem_nota_fiscal=False)
    resultado = verificar_nf(despesa)
    assert resultado is not None
    assert resultado.motivo_codigo == "SEM_NF"
    assert resultado.valor_reembolsavel == Decimal("0.00")


def test_rf07_com_nf_passa(despesa_factory):
    despesa = despesa_factory(valor=Decimal("150.00"), tem_nota_fiscal=True)
    assert verificar_nf(despesa) is None
