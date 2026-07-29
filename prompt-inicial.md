# Roteiro do Desafio SDD

> As regras de trabalho moram no CLAUDE.md e valem para toda sessão.
> Este arquivo é o roteiro das fases — leia no início do desafio e ao
> mudar de fase.

## Contexto

Motor de reembolso: CLI que lê `despesas.json` e escreve `resultado.json`,
aplicando uma política de RH deliberadamente ambígua. **O produto vale 10/100
pontos. Os outros 90 estão na spec, na rastreabilidade, na resposta à mudança
do Dia 2 e no relatório.** Otimize para isso.

Antes de começar, leia nesta ordem: `DESAFIO.md`, `RUBRICA.md`, `FAQ.md`,
`exemplos/despesas-exemplo.json` e os esqueletos em `template/`. Confirme
resumindo em 5 linhas o que está sendo avaliado.

## Fase 1 — Dia 1, manhã (spec → plan → tasks; sem código)

1. **Caça às ambiguidades.** Percorra a política do RH cruzando com
   `exemplos/despesas-exemplo.json` item por item (d-001 a d-014 — cada linha
   existe por um motivo). Três tipos: **unidade de aplicação** (regra vale por
   dia? por despesa? por diária?), **fronteira** (limites inclusivos/exclusivos,
   arredondamento, 100.00 vs 100.01, 33.333) e **dado ausente** (a política
   pressupõe informação que o JSON não traz — ex.: "em viagem"). Atenção também
   a: valores negativos (estorno), datas fora da competência, itens idênticos no
   mesmo dia, categorias fora da lista, variação de caixa (`ALIMENTACAO` vs
   `alimentacao`), multi-diária (hotel 2 diárias em valor único). São no mínimo
   oito; liste todas as candidatas, numeradas. Inclua as transversais: ordem de
   aplicação das regras e schema de saída do resultado.json.
2. **Uma ambiguidade por vez:** texto da política, item do JSON que a expõe,
   2–3 interpretações com consequência prática. Eu escolho; você registra na
   spec como *ambiguidade → decisão adotada → justificativa em uma linha*.
3. **spec.md:** requisitos desambiguados com ID (RF-01...), casos de borda,
   critérios de aceite verificáveis sem ler código, schema de saída do
   resultado.json, escopo negativo explícito.
4. **plan.md:** stack com alternativas descartadas e motivo, arquitetura em
   blocos, modelo de dados, decisões técnicas, estratégia de testes.
5. **tasks.md:** T-001..T-0NN, cada uma do tamanho de um commit, referenciando
   RF-XX, com critério de aceite ("o teste X passa"). Incluir setup e testes
   de borda.
6. Meta: três documentos fechados até meio-dia, mesmo imperfeitos. O que faltar
   entra via DECISIONS.md.

## Fase 2 — Dia 1, tarde (implementação guiada por tasks)

- Uma task por vez, na ordem. Ao final de cada: diff, testes, mensagem de
  commit, task marcada como concluída no tasks.md.
- Surgiu decisão que a spec não cobre? **Pare** → eu decido → spec.md +
  DECISIONS.md → task → só então código.

## Fase 3 — Dia 2 (envelope + relatório)

- ~10h chega a mudança de requisito. Ordem de absorção, sem exceção:
  **spec.md → DECISIONS.md (o que mudou, por quê, o que quebrou, tasks
  afetadas) → novas tasks → código → testes.** Se eu tentar ir direto pro
  código, me impeça.
- Registrar números da absorção: arquivos tocados, quanto veio de reexecutar
  tasks vs edição manual, tempo — vale bônus no relatório.
- Tarde: montar `docs/RELATORIO.md` pelos 4 Ds + envelope, com evidências
  (commits, trechos de sessão, antes/depois de requisitos). Nada de narrativa
  genérica.