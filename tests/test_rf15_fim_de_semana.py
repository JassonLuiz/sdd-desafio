from decimal import Decimal
from pathlib import Path

from src.motor import processar
from src.parser import carregar_entrada
from src.parser_politica import carregar_politica, nota_fiscal_gatilho, politica_efetiva

_EXEMPLO = Path(__file__).parent.parent / "exemplos" / "despesas-exemplo.json"
_POLITICA_PATH = Path(__file__).parent.parent / "exemplos" / "envelope" / "politica-v4.json"

_pol = carregar_politica(_POLITICA_PATH)
_gnf = nota_fiscal_gatilho(_pol)


def _resultado():
    colaborador, periodo, despesas = carregar_entrada(_EXEMPLO)
    eff = politica_efetiva(_pol, colaborador.centro_custo)
    return processar(colaborador, periodo, despesas, politica_eff=eff, gatilho_nf=_gnf)


def test_rf15_sabado_processado_normalmente():
    resultado = _resultado()
    item = next(i for i in resultado.itens if i.id == "d-012")
    assert item.status == "aprovado"
    assert item.valor_reembolsavel == Decimal("47.20")
