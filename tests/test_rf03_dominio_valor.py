from decimal import Decimal

from src.regras import verificar_dominio_valor, _fmt_valor


# --- testes de _fmt_valor ---

def test_fmt_valor_tipico():
    assert _fmt_valor(Decimal("690.00")) == "R$ 690,00"


def test_fmt_valor_com_milhar():
    assert _fmt_valor(Decimal("1234.56")) == "R$ 1.234,56"


def test_fmt_valor_negativo_com_milhar():
    assert _fmt_valor(Decimal("-1234.56")) == "R$ -1.234,56"


# --- testes de verificar_dominio_valor (RF-03) ---

def test_rf03_valor_negativo_recusado(despesa_factory):
    despesa = despesa_factory(valor=Decimal("-45.00"))
    resultado = verificar_dominio_valor(despesa)
    assert resultado is not None
    assert resultado.motivo_codigo == "VALOR_NAO_POSITIVO"
    assert resultado.valor_reembolsavel == Decimal("0.00")


def test_rf03_valor_zero_recusado(despesa_factory):
    despesa = despesa_factory(valor=Decimal("0.00"))
    resultado = verificar_dominio_valor(despesa)
    assert resultado is not None
    assert resultado.motivo_codigo == "VALOR_NAO_POSITIVO"


def test_rf03_nao_consome_cota(despesa_factory):
    # Prova ausência de efeito colateral na função isolada.
    # TODO (T-012/T-017): verificar via pipeline completo com dois itens no mesmo
    # dia — item recusado por VALOR_NAO_POSITIVO não deve reduzir cota da categoria.
    despesa = despesa_factory(valor=Decimal("-45.00"))
    resultado = verificar_dominio_valor(despesa)
    assert resultado is not None
    assert resultado.status == "recusado"
    assert resultado.duplicata_de is None


def test_rf03_valor_positivo_passa(despesa_factory):
    despesa = despesa_factory(valor=Decimal("0.01"))
    assert verificar_dominio_valor(despesa) is None
