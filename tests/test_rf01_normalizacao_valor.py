from decimal import Decimal

from src.parser import carregar_entrada
from src.normalizacao import normalizar_valor


def _escrever_entrada(tmp_path, valor_literal: str):
    corpo = f"""{{
  "colaborador": {{"id": "c-0001", "nome": "Teste", "centro_custo": "CC-TEST"}},
  "periodo": {{"competencia": "2026-07", "inicio": "2026-07-01", "fim": "2026-07-31"}},
  "despesas": [
    {{
      "id": "d-001",
      "data": "2026-07-15",
      "categoria": "alimentacao",
      "descricao": "Almoco",
      "fornecedor": "Restaurante X",
      "valor": {valor_literal},
      "tem_nota_fiscal": true
    }}
  ]
}}"""
    arquivo = tmp_path / "entrada.json"
    arquivo.write_text(corpo, encoding="utf-8")
    return arquivo


def test_rf01_valor_original_preservado(tmp_path):
    arquivo = _escrever_entrada(tmp_path, "33.333")
    _, _, despesas = carregar_entrada(arquivo)
    assert despesas[0].valor_original == Decimal("33.333")


def test_rf01_valor_inteiro_da_entrada(tmp_path):
    arquivo = _escrever_entrada(tmp_path, "480")
    _, _, despesas = carregar_entrada(arquivo)
    assert despesas[0].valor_original == Decimal("480")


def test_rf01_valor_333_normaliza_para_33():
    assert normalizar_valor(Decimal("33.333")) == Decimal("33.33")


def test_rf01_valor_335_arredonda_para_34():
    assert normalizar_valor(Decimal("33.335")) == Decimal("33.34")
