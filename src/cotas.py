from decimal import Decimal

from src.modelos import Despesa


class GerenciadorCotas:
    def __init__(self, politica_eff: dict) -> None:
        self._politica = politica_eff
        self._consumido: dict[tuple, Decimal] = {}

    def _chave(self, despesa: Despesa) -> tuple:
        periodicidade = self._politica[despesa.categoria]["periodicidade"]
        if periodicidade == "diaria":
            return (despesa.id, despesa.categoria)
        return (despesa.data, despesa.categoria)

    def calcular_reembolso(self, despesa: Despesa) -> tuple[Decimal, str | None]:
        limite = self._politica[despesa.categoria]["limite"]
        chave = self._chave(despesa)
        ja_consumido = self._consumido.get(chave, Decimal("0.00"))
        saldo = limite - ja_consumido

        if saldo <= Decimal("0.00"):
            return Decimal("0.00"), "COTA_ESGOTADA"

        if despesa.valor_considerado > saldo:
            self._consumido[chave] = limite
            return saldo, "LIMITE_DIARIO"

        self._consumido[chave] = ja_consumido + despesa.valor_considerado
        return despesa.valor_considerado, None
