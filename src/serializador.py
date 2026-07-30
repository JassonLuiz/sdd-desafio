import json
import re
import uuid
from decimal import Decimal, ROUND_HALF_UP

from src.modelos import Resultado, ResultadoItem


def _item_dict(item: ResultadoItem, q, lit) -> dict:
    return {
        "id": item.id,
        "status": item.status,
        "valor_original": lit(item.valor_original),
        "valor_considerado": q(item.valor_considerado),
        "valor_reembolsavel": q(item.valor_reembolsavel),
        "motivo_codigo": item.motivo_codigo,
        "motivo_texto": item.motivo_texto,
        "duplicata_de": item.duplicata_de,
    }


def serializar(resultado: Resultado) -> str:
    # Token único por chamada — elimina colisão com texto de entrada não controlado
    # (descricao, fornecedor, nome) por construção, não por suposição.
    mark = uuid.uuid4().hex

    def q(v: Decimal) -> str:
        return mark + str(v.quantize(Decimal("0.01"), ROUND_HALF_UP))

    def lit(v: Decimal) -> str:
        return mark + str(v)

    d = {
        "colaborador": {
            "id": resultado.colaborador.id,
            "nome": resultado.colaborador.nome,
            "centro_custo": resultado.colaborador.centro_custo,
        },
        "periodo": {
            "competencia": resultado.periodo.competencia,
            "inicio": str(resultado.periodo.inicio),
            "fim": str(resultado.periodo.fim),
        },
        "resumo": {
            "total_solicitado": q(resultado.resumo.total_solicitado),
            "total_reembolsavel": q(resultado.resumo.total_reembolsavel),
            "total_recusado": q(resultado.resumo.total_recusado),
            "itens_processados": resultado.resumo.itens_processados,
            "itens_aprovados": resultado.resumo.itens_aprovados,
            "itens_parciais": resultado.resumo.itens_parciais,
            "itens_recusados": resultado.resumo.itens_recusados,
        },
        "itens": [_item_dict(item, q, lit) for item in resultado.itens],
    }
    raw = json.dumps(d, ensure_ascii=False, indent=2)
    return re.sub(f'"{re.escape(mark)}([^"]+)"', r'\1', raw)
