from decimal import Decimal
from pathlib import Path

from src.motor import processar
from src.normalizacao import normalizar_categoria
from src.parser import carregar_entrada

_EXEMPLO = Path(__file__).parent.parent / "exemplos" / "despesas-exemplo.json"

_LIMITE_V3 = {
    "alimentacao": Decimal("60.00"),
    "transporte_urbano": Decimal("80.00"),
    "hospedagem": Decimal("250.00"),
}


def test_rf16_nenhum_item_com_limite_ampliado():
    # Regra de viagem (limites ampliados) está suspensa por AMB-006.
    # Nenhum item de nenhuma categoria deve receber valor_reembolsavel acima
    # do limite padrão da categoria (60,00 / 80,00 / 250,00).
    colaborador, periodo, despesas_brutas = carregar_entrada(_EXEMPLO)
    resultado = processar(colaborador, periodo, despesas_brutas)

    categoria_por_id = {d.id: normalizar_categoria(d.categoria) for d in despesas_brutas}
    for item in resultado.itens:
        categoria = categoria_por_id[item.id]
        limite = _LIMITE_V3.get(categoria)
        if limite is None:
            continue  # categoria inválida já recusada no passo 4
        assert item.valor_reembolsavel <= limite, (
            f"{item.id} ({categoria}): valor_reembolsavel {item.valor_reembolsavel}"
            f" > limite {limite} — indica limite de viagem aplicado indevidamente"
        )
