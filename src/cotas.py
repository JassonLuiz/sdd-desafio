from decimal import Decimal
from datetime import date

from src.modelos import Despesa

LIMITE_DIARIO: dict[str, Decimal] = {
    "alimentacao": Decimal("60.00"),
    "transporte_urbano": Decimal("80.00"),
    "hospedagem": Decimal("250.00"),
}

CATEGORIAS_LIMITE_POR_LANCAMENTO = {"hospedagem"}


def _chave(despesa: Despesa) -> tuple:
    if despesa.categoria in CATEGORIAS_LIMITE_POR_LANCAMENTO:
        return (despesa.id, despesa.categoria)
    return (despesa.data, despesa.categoria)


class GerenciadorCotas:
    def __init__(self) -> None:
        self._consumido: dict[tuple, Decimal] = {}

    def calcular_reembolso(self, despesa: Despesa) -> tuple[Decimal, str | None]:
        limite = LIMITE_DIARIO[despesa.categoria]
        chave = _chave(despesa)
        ja_consumido = self._consumido.get(chave, Decimal("0.00"))
        saldo = limite - ja_consumido

        if saldo <= Decimal("0.00"):
            # ja_consumido + 0 == ja_consumido — escrita seria redundante
            return Decimal("0.00"), "COTA_ESGOTADA"

        if despesa.valor_considerado > saldo:
            self._consumido[chave] = limite
            return saldo, "LIMITE_DIARIO"

        self._consumido[chave] = ja_consumido + despesa.valor_considerado
        return despesa.valor_considerado, None
