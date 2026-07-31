from decimal import Decimal
from pathlib import Path

from src.motor import processar
from src.normalizacao import normalizar_categoria
from src.parser import carregar_entrada
from src.parser_politica import carregar_politica, nota_fiscal_gatilho, politica_efetiva

_EXEMPLO = Path(__file__).parent.parent / "exemplos" / "despesas-exemplo.json"
_POLITICA_PATH = Path(__file__).parent.parent / "exemplos" / "envelope" / "politica-v4.json"

_pol = carregar_politica(_POLITICA_PATH)
_gnf = nota_fiscal_gatilho(_pol)


def test_rf16_nenhum_item_com_limite_ampliado():
    # Regra de viagem (limites ampliados) está suspensa por AMB-006.
    # Nenhum item deve receber valor_reembolsavel acima do limite efetivo da categoria.
    colaborador, periodo, despesas_brutas = carregar_entrada(_EXEMPLO)
    eff = politica_efetiva(_pol, colaborador.centro_custo)
    resultado = processar(colaborador, periodo, despesas_brutas, politica_eff=eff, gatilho_nf=_gnf)

    categoria_por_id = {d.id: normalizar_categoria(d.categoria) for d in despesas_brutas}
    for item in resultado.itens:
        categoria = categoria_por_id[item.id]
        if categoria not in eff:
            continue  # categoria inválida já recusada no passo 4
        limite = eff[categoria]["limite"]
        assert item.valor_reembolsavel <= limite, (
            f"{item.id} ({categoria}): valor_reembolsavel {item.valor_reembolsavel}"
            f" > limite {limite} — indica limite de viagem aplicado indevidamente"
        )
