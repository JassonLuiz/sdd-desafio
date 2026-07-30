from src.normalizacao import normalizar_categoria


def test_rf02_maiusculas_reconhecidas():
    assert normalizar_categoria("ALIMENTACAO") == "alimentacao"


def test_rf02_espacos_removidos():
    assert normalizar_categoria(" Alimentacao ") == "alimentacao"


def test_rf02_acento_nao_normalizado():
    assert normalizar_categoria("Alimentação") == "alimentação"
