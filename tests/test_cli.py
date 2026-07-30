import json
import subprocess
import sys
from pathlib import Path

_EXEMPLO = Path(__file__).parent.parent / "exemplos" / "despesas-exemplo.json"


def _run(*args):
    return subprocess.run(
        [sys.executable, "-m", "src.cli", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def test_cli_arquivo_valido_codigo_0(tmp_path):
    saida = tmp_path / "resultado.json"
    proc = _run("calcular", "--input", str(_EXEMPLO), "--output", str(saida))
    assert proc.returncode == 0
    assert saida.exists()
    dados = json.loads(saida.read_text(encoding="utf-8"))
    assert "colaborador" in dados
    assert "itens" in dados


def test_cli_arquivo_inexistente_codigo_1(tmp_path):
    saida = tmp_path / "resultado.json"
    proc = _run("calcular", "--input", "nao_existe.json", "--output", str(saida))
    assert proc.returncode == 1
    assert "não encontrado" in proc.stderr
    assert not saida.exists()
