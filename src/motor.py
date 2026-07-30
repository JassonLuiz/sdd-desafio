from decimal import Decimal

from src.cotas import GerenciadorCotas, LIMITE_DIARIO
from src.modelos import (
    Colaborador, DespesaBruta, Despesa, Periodo,
    Resultado, ResultadoItem, Resumo,
)
from src.normalizacao import normalizar_categoria, normalizar_valor
from src.regras import (
    fmt_valor,
    verificar_categoria,
    verificar_competencia,
    verificar_dominio_valor,
    verificar_duplicata,
    verificar_nf,
)


def _texto_passo7(categoria: str, motivo_codigo: str | None, valor_reembolsavel: Decimal, valor_considerado: Decimal) -> str | None:
    if motivo_codigo is None:
        return None
    if motivo_codigo == "LIMITE_DIARIO":
        return f"limite diário de {categoria}: reembolsado {fmt_valor(valor_reembolsavel)} de {fmt_valor(valor_considerado)}"
    if motivo_codigo == "COTA_ESGOTADA":
        limite = LIMITE_DIARIO[categoria]
        return f"cota diária de {categoria} esgotada: {fmt_valor(limite)} já consumidos por itens anteriores no dia"
    return None


def _derivar_status(valor_reembolsavel: Decimal, valor_considerado: Decimal) -> str:
    if valor_reembolsavel == valor_considerado:
        return "aprovado"
    if valor_reembolsavel == Decimal("0.00"):
        return "recusado"
    return "parcial"


def processar(colaborador: Colaborador, periodo: Periodo, despesas_brutas: list[DespesaBruta]) -> Resultado:
    vistos: dict = {}
    gc = GerenciadorCotas()
    itens: list[ResultadoItem] = []

    for bruta in despesas_brutas:
        despesa = Despesa(
            id=bruta.id,
            data=bruta.data,
            categoria=normalizar_categoria(bruta.categoria),
            descricao=bruta.descricao,
            fornecedor=bruta.fornecedor,
            valor_original=bruta.valor_original,
            valor_considerado=normalizar_valor(bruta.valor_original),
            tem_nota_fiscal=bruta.tem_nota_fiscal,
        )

        item = verificar_dominio_valor(despesa)
        item = item or verificar_competencia(despesa, periodo)
        item = item or verificar_categoria(despesa)
        item = item or verificar_duplicata(despesa, vistos)
        item = item or verificar_nf(despesa)

        if item is None:
            valor_reembolsavel, motivo_codigo = gc.calcular_reembolso(despesa)
            item = ResultadoItem(
                id=despesa.id,
                status=_derivar_status(valor_reembolsavel, despesa.valor_considerado),
                valor_original=despesa.valor_original,
                valor_considerado=despesa.valor_considerado,
                valor_reembolsavel=valor_reembolsavel,
                motivo_codigo=motivo_codigo,
                motivo_texto=_texto_passo7(despesa.categoria, motivo_codigo, valor_reembolsavel, despesa.valor_considerado),
                duplicata_de=None,
            )

        itens.append(item)

    # TODO (T-014): substituir por cálculo completo —
    # total_solicitado = Σ valor_considerado dos itens com valor_considerado > 0
    resumo = Resumo(
        total_solicitado=Decimal("0.00"),
        total_reembolsavel=Decimal("0.00"),
        total_recusado=Decimal("0.00"),
        itens_processados=len(itens),
        itens_aprovados=0,
        itens_parciais=0,
        itens_recusados=0,
    )

    return Resultado(
        colaborador=colaborador,
        periodo=periodo,
        resumo=resumo,
        itens=tuple(itens),
    )
