import pytest
from datetime import date
from decimal import Decimal, ROUND_HALF_UP


@pytest.fixture
def periodo_padrao():
    from src.modelos import Periodo
    return Periodo(
        competencia="2026-07",
        inicio=date(2026, 7, 1),
        fim=date(2026, 7, 31),
    )


@pytest.fixture
def colaborador_padrao():
    from src.modelos import Colaborador
    return Colaborador(
        id="c-0001",
        nome="Teste",
        centro_custo="CC-TEST",
    )


@pytest.fixture
def despesa_factory():
    def _factory(
        id="d-001",
        data=date(2026, 7, 15),
        categoria="alimentacao",
        descricao="Teste",
        fornecedor="Fornecedor Teste",
        valor=Decimal("30.00"),
        tem_nota_fiscal=True,
        moeda="BRL",
        taxa_cambio_aplicada=None,
    ):
        from src.modelos import Despesa
        valor_considerado = valor.quantize(Decimal("0.01"), ROUND_HALF_UP)
        return Despesa(
            id=id,
            data=data,
            categoria=categoria,
            descricao=descricao,
            fornecedor=fornecedor,
            valor_original=valor,
            valor_considerado=valor_considerado,
            tem_nota_fiscal=tem_nota_fiscal,
            moeda=moeda,
            taxa_cambio_aplicada=taxa_cambio_aplicada,
        )
    return _factory
