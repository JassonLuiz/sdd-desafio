from decimal import Decimal
from pathlib import Path

from src.motor import processar
from src.parser import carregar_entrada

_EXEMPLO = Path(__file__).parent.parent / "exemplos" / "despesas-exemplo.json"


def _resultado():
    colaborador, periodo, despesas = carregar_entrada(_EXEMPLO)
    return processar(colaborador, periodo, despesas)


def test_rf15_sabado_processado_normalmente():
    resultado = _resultado()
    item = next(i for i in resultado.itens if i.id == "d-012")
    assert item.status == "aprovado"
    assert item.valor_reembolsavel == Decimal("47.20")
