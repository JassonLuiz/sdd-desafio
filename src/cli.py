import argparse
import json
import sys
from pathlib import Path

from src.motor import processar
from src.parser import carregar_entrada
from src.parser_cambio import carregar_cambio
from src.parser_politica import carregar_politica, nota_fiscal_gatilho, politica_efetiva
from src.serializador import serializar


def _arquivo(caminho_str: str, descricao: str) -> Path:
    caminho = Path(caminho_str)
    if not caminho.exists():
        print(f"Erro: {descricao} não encontrado: {caminho_str}", file=sys.stderr)
        sys.exit(1)
    return caminho


def _calcular(args: argparse.Namespace) -> None:
    caminho_input = _arquivo(args.input, "arquivo de entrada")
    caminho_politica = _arquivo(args.politica, "arquivo de política")
    caminho_cambio = _arquivo(args.cambio, "arquivo de câmbio")

    try:
        colaborador, periodo, despesas = carregar_entrada(caminho_input)
    except (KeyError, ValueError, json.JSONDecodeError) as e:
        print(f"Erro: entrada inválida — {e}", file=sys.stderr)
        sys.exit(1)

    try:
        politica = carregar_politica(caminho_politica)
        tabela_cambio = carregar_cambio(caminho_cambio)
    except (KeyError, ValueError, json.JSONDecodeError) as e:
        print(f"Erro: arquivo de política ou câmbio inválido — {e}", file=sys.stderr)
        sys.exit(1)

    eff = politica_efetiva(politica, colaborador.centro_custo)
    gnf = nota_fiscal_gatilho(politica)

    resultado = processar(
        colaborador, periodo, despesas,
        politica_eff=eff,
        gatilho_nf=gnf,
        tabela_cambio=tabela_cambio,
    )
    saida = serializar(resultado)

    Path(args.output).write_text(saida, encoding="utf-8")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Motor de cálculo de reembolso de despesas")
    sub = parser.add_subparsers(dest="comando")

    calc = sub.add_parser("calcular", help="Processa um lote de despesas")
    calc.add_argument("--input",    required=True, metavar="ARQUIVO", help="JSON de entrada")
    calc.add_argument("--output",   required=True, metavar="ARQUIVO", help="JSON de saída")
    calc.add_argument("--politica", required=True, metavar="ARQUIVO", help="JSON de política de reembolso")
    calc.add_argument("--cambio",   required=True, metavar="ARQUIVO", help="JSON de tabela de câmbio")

    args = parser.parse_args()
    if args.comando is None:
        parser.print_help()
        sys.exit(1)

    _calcular(args)


if __name__ == "__main__":
    main()
