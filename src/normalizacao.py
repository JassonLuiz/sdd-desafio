from decimal import Decimal, ROUND_HALF_UP


def normalizar_valor(v: Decimal) -> Decimal:
    return v.quantize(Decimal("0.01"), ROUND_HALF_UP)


def normalizar_categoria(c: str) -> str:
    return c.strip().lower()
