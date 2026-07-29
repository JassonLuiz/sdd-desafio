# CLAUDE.md

## O projeto

Motor de cálculo de reembolso de despesas corporativas. CLI que lê um JSON de
despesas e emite um JSON com o valor reembolsável e a justificativa de cada item.

## Fonte da verdade

`specs/001-motor-reembolso/spec.md` define **o que** o sistema faz.
`specs/001-motor-reembolso/plan.md` define **como**.
`specs/001-motor-reembolso/tasks.md` define **em que ordem**.

Quando o código e a spec discordarem, a spec está certa e o código é o bug —
a menos que a spec esteja errada, e nesse caso corrigimos a spec primeiro e
registramos em `DECISIONS.md`.

**Antes de implementar qualquer coisa, leia a task correspondente em `tasks.md`.**
Se o que eu pedi não está coberto por nenhuma task, me avise em vez de implementar.

## Regras de trabalho

- **Spec antes de código.** Nada em `src/` ou `tests/` antes de spec.md, plan.md
  e tasks.md fecharem. Se eu pedir código antes disso, recuse e me lembre.
- **Decisões de ambiguidade são do humano.** Apresente 2–3 interpretações com
  prós/contras e espere minha escolha. Nunca decida sozinho; se perceber que
  assumiu uma interpretação sem decisão minha explícita, pare e pergunte.
- Toda regra de negócio vive na spec, não no chat e não em comentário de código.
  Se eu te explicar uma regra que não está na spec, **pare e me diga isso** antes
  de escrever código. Isso é um bug de spec → corrigir spec + DECISIONS.md, só
  então continuar.
- Todo commit referencia uma task: `feat(T-003): <descrição>`,
  `test(T-003): <descrição>`. Mudanças de documentação: `docs(spec):`,
  `docs(plan):`, `docs(tasks):`. Commits pequenos, um por task. Sugira a
  mensagem ao final de cada task.
- Nenhuma regra de negócio entra sem teste. Testes nomeados remetendo ao
  requisito: `test_rf03_limite_diario_alimentacao_agrega_por_data`.
- **spec.md não sabe que código existe.** Nome de biblioteca, classe, pasta ou
  linguagem na spec → mover para plan.md e me avisar. Teste: "se eu trocasse de
  linguagem amanhã, isso mudaria?" Se muda, é plan.
- **Ao final de cada sessão, me lembre de rodar `/export`**, salvar em
  `docs/sessions/NN-descricao-curta.md` e commitar.
- Quando você errar e eu apontar, me ajude a documentar o episódio na hora
  (o que propôs, por que estava errado, como detectei) — vai para a seção
  Discernimento do relatório.

## Estilo de trabalho

- Português. Respostas diretas.
- Decisões sempre em formato "opção A / B / C + consequência", nunca tomadas
  por você.
- Antes de qualquer entrega sua (spec, código, teste), aponte você mesmo os
  pontos fracos que eu deveria verificar.

## Stack e comandos

- Linguagem: Python 3
- Rodar: `python -m src.cli calcular --input despesas.json --output resultado.json`
- Testes: `pytest`
- CLI: argparse (stdlib). Sem dependências além do necessário.

## Convenções de código

- Valores monetários: `decimal.Decimal`, nunca float. A regra de arredondamento
  (casas, modo) é definida na spec; o Decimal é só a implementação dela.
- Tratamento de erro: entrada inválida falha com mensagem clara, não com traceback.

## Fora de escopo

- Ver "escopo negativo" na spec.md — é a spec quem declara o que o sistema não
  faz. Não invente feature que não esteja coberta por task.