import argparse
import json
import sys
from pathlib import Path

from src.motor import processar
from src.parser import carregar_entrada
from src.serializador import serializar


def _calcular(args: argparse.Namespace) -> None:
    caminho_input = Path(args.input)
    if not caminho_input.exists():
        print(f"Erro: arquivo de entrada não encontrado: {args.input}", file=sys.stderr)
        sys.exit(1)

    try:
        colaborador, periodo, despesas = carregar_entrada(caminho_input)
    except (KeyError, ValueError, json.JSONDecodeError) as e:
        print(f"Erro: entrada inválida — {e}", file=sys.stderr)
        sys.exit(1)

    resultado = processar(colaborador, periodo, despesas)
    saida = serializar(resultado)

    caminho_output = Path(args.output)
    caminho_output.write_text(saida, encoding="utf-8")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Motor de cálculo de reembolso de despesas")
    sub = parser.add_subparsers(dest="comando")

    calc = sub.add_parser("calcular", help="Processa um lote de despesas")
    calc.add_argument("--input", required=True, metavar="ARQUIVO", help="JSON de entrada")
    calc.add_argument("--output", required=True, metavar="ARQUIVO", help="JSON de saída")

    args = parser.parse_args()
    if args.comando is None:
        parser.print_help()
        sys.exit(1)

    _calcular(args)


if __name__ == "__main__":
    main()
