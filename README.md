# Motor de Reembolso de Despesas

CLI que lê um lote de despesas corporativas em JSON e emite um JSON com o valor
reembolsável de cada item e a justificativa da decisão.

## Pré-requisitos

- Python 3.11 ou superior
- pytest (único pacote externo)

```bash
pip install pytest
```

## Como rodar

```bash
python -m src.cli calcular --input exemplos/despesas-exemplo.json --output resultado.json
```

| Argumento | Descrição |
|---|---|
| `--input` | Caminho para o JSON de entrada (formato: `exemplos/despesas-exemplo.json`) |
| `--output` | Caminho para o JSON de saída a ser criado |

Arquivo inexistente em `--input` → mensagem de erro no stderr e código de saída `1`.

## Como testar

```bash
pytest
```

75 testes cobrindo RF-01 a RF-16, 17 critérios de aceite de integração e casos de borda.

## Exemplo de saída

Processando `exemplos/despesas-exemplo.json` (14 itens):

```json
{
  "colaborador": {
    "id": "c-0417",
    "nome": "Marina Volpi",
    "centro_custo": "CC-ENG-PLATAFORMA"
  },
  "periodo": {
    "competencia": "2026-07",
    "inicio": "2026-07-01",
    "fim": "2026-07-31"
  },
  "resumo": {
    "total_solicitado": 1861.84,
    "total_reembolsavel": 585.43,
    "total_recusado": 1276.41,
    "itens_processados": 14,
    "itens_aprovados": 3,
    "itens_parciais": 4,
    "itens_recusados": 7
  },
  "itens": [
    {
      "id": "d-001",
      "status": "parcial",
      "valor_original": 72.50,
      "valor_considerado": 72.50,
      "valor_reembolsavel": 60.00,
      "motivo_codigo": "LIMITE_DIARIO",
      "motivo_texto": "limite diário de alimentacao: reembolsado R$ 60,00 de R$ 72,50",
      "duplicata_de": null
    }
  ]
}
```

## Estrutura

```
src/
├── cli.py          — entry point (argparse)
├── parser.py       — leitura do JSON de entrada
├── normalizacao.py — valor half-up 2dp + categoria lowercase+trim
├── regras.py       — verificadores dos passos 2–6 (RF-03 a RF-07)
├── cotas.py        — GerenciadorCotas: passos 7 (RF-08, RF-09, RF-10)
├── motor.py        — pipeline completo (processar)
├── serializador.py — saída JSON com decimais exatos
└── modelos.py      — dataclasses
specs/001-motor-reembolso/
├── spec.md         — o QUÊ e o PORQUÊ
├── plan.md         — o COMO
├── tasks.md        — T-001..T-019 com critérios de aceite
└── DECISIONS.md    — log de decisões e mudanças de spec (D-001..D-004)
```
