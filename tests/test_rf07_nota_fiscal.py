from decimal import Decimal

from src.regras import verificar_nf

_GATILHO = Decimal("100.00")


def test_rf07_fronteira_100_sem_nf_passa(despesa_factory):
    despesa = despesa_factory(valor=Decimal("100.00"), tem_nota_fiscal=False)
    assert verificar_nf(despesa, _GATILHO) is None


def test_rf07_fronteira_100_01_sem_nf_recusa(despesa_factory):
    despesa = despesa_factory(valor=Decimal("100.01"), tem_nota_fiscal=False)
    resultado = verificar_nf(despesa, _GATILHO)
    assert resultado is not None
    assert resultado.motivo_codigo == "SEM_NF"
    assert resultado.valor_reembolsavel == Decimal("0.00")


def test_rf07_com_nf_passa(despesa_factory):
    despesa = despesa_factory(valor=Decimal("150.00"), tem_nota_fiscal=True)
    assert verificar_nf(despesa, _GATILHO) is None


def test_rf07_gatilho_lido_da_politica(despesa_factory):
    # gatilho 100,00 passado explicitamente — fronteira idêntica ao hardcoded anterior
    gatilho = Decimal("100.00")
    assert verificar_nf(despesa_factory(valor=Decimal("100.00"), tem_nota_fiscal=False), gatilho) is None
    resultado = verificar_nf(despesa_factory(valor=Decimal("100.01"), tem_nota_fiscal=False), gatilho)
    assert resultado is not None
    assert resultado.motivo_codigo == "SEM_NF"


def test_rf07_gatilho_alternativo(despesa_factory):
    # com gatilho 50,00, R$50,01 sem NF deve ser recusado
    gatilho = Decimal("50.00")
    resultado = verificar_nf(despesa_factory(valor=Decimal("50.01"), tem_nota_fiscal=False), gatilho)
    assert resultado is not None
    assert resultado.motivo_codigo == "SEM_NF"
