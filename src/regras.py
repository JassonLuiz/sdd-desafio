from decimal import Decimal

from src.modelos import Despesa, Periodo, ResultadoItem


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


CATEGORIAS_VALIDAS = {"alimentacao", "transporte_urbano", "hospedagem"}
GATILHO_NF = Decimal("100.00")


def verificar_nf(despesa: Despesa) -> ResultadoItem | None:
    if despesa.valor_considerado > GATILHO_NF and not despesa.tem_nota_fiscal:
        texto = f"nota fiscal obrigatória para valor acima de R$ 100,00 (valor: {_fmt_valor(despesa.valor_considerado)})"
        return _recusar(despesa, "SEM_NF", texto)
    return None


def verificar_duplicata(despesa: Despesa, vistos: dict) -> ResultadoItem | None:
    chave = (
        despesa.data,
        despesa.categoria,
        despesa.descricao,
        despesa.fornecedor,
        despesa.valor_considerado,
        despesa.tem_nota_fiscal,
    )
    if chave in vistos:
        return _recusar(despesa, "DUPLICATA", f"duplicata de {vistos[chave]}", duplicata_de=vistos[chave])
    vistos[chave] = despesa.id
    return None


def verificar_categoria(despesa: Despesa) -> ResultadoItem | None:
    if despesa.categoria not in CATEGORIAS_VALIDAS:
        texto = f"categoria fora da política: {despesa.categoria}"
        return _recusar(despesa, "CATEGORIA_INVALIDA", texto)
    return None


def verificar_competencia(despesa: Despesa, periodo: Periodo) -> ResultadoItem | None:
    if despesa.data < periodo.inicio or despesa.data > periodo.fim:
        texto = f"data {despesa.data} fora do período {periodo.inicio} a {periodo.fim}"
        return _recusar(despesa, "FORA_COMPETENCIA", texto)
    return None


def verificar_dominio_valor(despesa: Despesa) -> ResultadoItem | None:
    if despesa.valor_considerado <= Decimal("0.00"):
        texto = f"valor não positivo: {_fmt_valor(despesa.valor_considerado)}"
        return _recusar(despesa, "VALOR_NAO_POSITIVO", texto)
    return None
