from decimal import Decimal

from src.modelos import Despesa, ResultadoItem


def _recusar(despesa: Despesa, motivo_codigo: str, motivo_texto: str, duplicata_de: str | None = None) -> ResultadoItem:
    return ResultadoItem(
        id=despesa.id,
        status="recusado",
        valor_original=despesa.valor_original,
        valor_considerado=despesa.valor_considerado,
        valor_reembolsavel=Decimal("0.00"),
        motivo_codigo=motivo_codigo,
        motivo_texto=motivo_texto,
        duplicata_de=duplicata_de,
    )


def _fmt_valor(v: Decimal) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def verificar_dominio_valor(despesa: Despesa) -> ResultadoItem | None:
    if despesa.valor_considerado <= Decimal("0.00"):
        texto = f"valor não positivo: {_fmt_valor(despesa.valor_considerado)}"
        return _recusar(despesa, "VALOR_NAO_POSITIVO", texto)
    return None
