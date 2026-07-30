# Spec — Motor de Cálculo de Reembolso

**Versão:** 1.0 · **Status:** ativo · **Última alteração:** 2026-07-29

> **Regra de ouro deste arquivo:** ele descreve o QUÊ e o PORQUÊ. Nenhuma linha
> aqui pode citar linguagem, biblioteca, classe, função ou estrutura de pasta.
> Se apareceu solução, o lugar dela é o `plan.md`.
>
> **Teste de aceitação da própria spec:** uma pessoa que nunca viu o projeto
> consegue, lendo só este arquivo, verificar se o sistema está correto?

---

## 1. Problema

O processo de reembolso de despesas corporativas é manual: um analista do
financeiro confere cada item contra a política de RH, decide aprovações e
recusas e produz uma lista justificada. O processo é lento, sujeito a erro
humano e gera resultados que variam conforme o analista.

## 2. Objetivo

Dado um lote de despesas de um colaborador em um período, o sistema decide
automaticamente o valor reembolsável de cada item e registra a justificativa
da decisão em formato auditável e reproduzível.

## 3. Fora de escopo

- Este sistema não consulta bases de dados externas, sistemas de RH ou
  histórico de outros períodos.
- Este sistema não infere status de viagem a partir de padrões nas despesas
  — a regra de limites ampliados (regra 6 da política) está suspensa por
  ausência de dado no schema de entrada (ver AMB-006).
- Este sistema não extrai dados de negócio do campo `descricao` (ver AMB-003,
  AMB-009, AMB-011).
- Este sistema não normaliza acentos, não corrige ortografia e não calcula
  similaridade entre strings — apenas normaliza capitalização e espaços
  externos de campos de domínio fechado (ver AMB-011).
- Este sistema não aplica regras diferentes por dia da semana ou feriado
  (ver AMB-014).
- Este sistema não processa múltiplos colaboradores em uma única execução.
- Este sistema não persiste estado entre execuções; cada execução é
  independente.
- Este sistema não valida a existência do colaborador nem do centro de custo.
- Este sistema não valida unicidade de `id` na entrada; ids repetidos com dados
  diferentes passam despercebidos (RF-06 só detecta coincidência de todos os
  campos da chave de duplicata, não de id isolado).
- Este sistema não detecta duplicatas por similaridade — apenas por
  coincidência exata de campos (ver AMB-007).

---

## 4. Entrada e saída

### 4.1 Entrada

Formato definido por `exemplos/despesas-exemplo.json`. O schema de entrada é
fixo; nenhum campo adicional será introduzido por este sistema.

| Campo | Tipo | Significado | Obrigatório |
|---|---|---|---|
| `colaborador.id` | string | Identificador do colaborador | Sim |
| `colaborador.nome` | string | Nome do colaborador | Sim |
| `colaborador.centro_custo` | string | Centro de custo | Sim |
| `periodo.competencia` | string `AAAA-MM` | Identificador do período (informativo) | Sim |
| `periodo.inicio` | string `AAAA-MM-DD` | Início do período autoritativo (inclusive) | Sim |
| `periodo.fim` | string `AAAA-MM-DD` | Fim do período autoritativo (inclusive) | Sim |
| `despesas[].id` | string | Identificador único da despesa | Sim |
| `despesas[].data` | string `AAAA-MM-DD` | Data da despesa (proxy de data de lançamento) | Sim |
| `despesas[].categoria` | string | Categoria da despesa (domínio fechado após normalização) | Sim |
| `despesas[].descricao` | string | Descrição livre — não utilizada em regras de negócio | Sim |
| `despesas[].fornecedor` | string | Fornecedor | Sim |
| `despesas[].valor` | número | Valor em reais (pode ter mais de 2 casas decimais) | Sim |
| `despesas[].tem_nota_fiscal` | booleano | Se nota fiscal foi apresentada | Sim |

**Nota sobre `periodo.competencia` vs `inicio`/`fim`:** quando divergirem,
prevalecem `inicio` e `fim` (ver AMB-008).

### 4.2 Saída

Arquivo `resultado.json`, cujo schema é definido por esta spec. Todos os
valores numéricos com exatamente 2 casas decimais, **exceto `valor_original`,
que ecoa o valor da entrada sem normalização**. A ordem dos itens na saída
é a mesma da entrada. A saída é determinística: mesma entrada produz saída
byte a byte idêntica.

#### Schema da saída

| Campo | Tipo | Significado |
|---|---|---|
| `colaborador` | objeto | Espelho do objeto `colaborador` da entrada |
| `periodo` | objeto | Espelho do objeto `periodo` da entrada |
| `resumo.total_solicitado` | número | Σ `valor_considerado` dos itens com `valor_considerado > 0`; itens com `valor_considerado ≤ 0` contribuem com zero — totais de auditoria não devem ser distorcidos por itens fora do domínio |
| `resumo.total_reembolsavel` | número | Σ `valor_reembolsavel` de todos os itens |
| `resumo.total_recusado` | número | `total_solicitado − total_reembolsavel` |
| `resumo.itens_processados` | inteiro | Total de itens no lote |
| `resumo.itens_aprovados` | inteiro | Contagem de itens com `status = "aprovado"` |
| `resumo.itens_parciais` | inteiro | Contagem de itens com `status = "parcial"` |
| `resumo.itens_recusados` | inteiro | Contagem de itens com `status = "recusado"` |
| `itens[].id` | string | Identificador da despesa, espelho da entrada |
| `itens[].status` | enum | `"aprovado"` / `"parcial"` / `"recusado"` (definição aritmética em RF-13) |
| `itens[].valor_original` | número | Valor exatamente como veio na entrada, sem normalização |
| `itens[].valor_considerado` | número | Valor após normalização half-up a 2 casas (RF-01) |
| `itens[].valor_reembolsavel` | número | Valor a reembolsar após todas as regras |
| `itens[].motivo_codigo` | string \| null | Código do motivo (`null` quando `status = "aprovado"`) |
| `itens[].motivo_texto` | string \| null | Descrição legível do motivo em português (`null` quando `status = "aprovado"`) |
| `itens[].duplicata_de` | string \| null | `id` do item mantido quando `motivo_codigo = "DUPLICATA"`; `null` nos demais |

#### Enum de `motivo_codigo`

| Código | Passo | Quando |
|---|---|---|
| `VALOR_NAO_POSITIVO` | 2 | `valor_considerado ≤ 0,00` |
| `FORA_COMPETENCIA` | 3 | `data` fora de `[periodo.inicio, periodo.fim]` |
| `CATEGORIA_INVALIDA` | 4 | categoria não reconhecida após normalização |
| `DUPLICATA` | 5 | coincidência exata com item anterior na ordem do arquivo |
| `SEM_NF` | 6 | `valor_considerado > 100,00` e `tem_nota_fiscal = false` |
| `LIMITE_DIARIO` | 7 | item cortado parcialmente (saldo disponível > 0,00 mas < `valor_considerado`) |
| `COTA_ESGOTADA` | 7 | item zerado porque saldo da categoria no dia já era 0,00 |

#### Templates de `motivo_texto` por código

O campo `motivo_texto` é destinado à leitura humana (auditoria pelo financeiro).
Testes automatizados verificam `motivo_codigo`; `motivo_texto` só é testado por
substring onde esta tabela exige conteúdo específico.

| Código | Template | Placeholders |
|---|---|---|
| `VALOR_NAO_POSITIVO` | `"valor não positivo: R$ <valor>"` | `<valor>` = `valor_considerado` com 2 casas decimais, vírgula decimal |
| `FORA_COMPETENCIA` | `"data <data> fora do período <inicio> a <fim>"` | datas no formato `AAAA-MM-DD` |
| `CATEGORIA_INVALIDA` | `"categoria fora da política: <categoria>"` | `<categoria>` = valor normalizado |
| `DUPLICATA` | `"duplicata de <id>"` | `<id>` = id do item mantido |
| `SEM_NF` | `"nota fiscal obrigatória para valor acima de R$ 100,00 (valor: R$ <valor>)"` | `<valor>` = `valor_considerado` com 2 casas decimais, vírgula decimal |
| `LIMITE_DIARIO` | `"limite diário de <categoria>: reembolsado R$ <reembolsavel> de R$ <considerado>"` | valores com 2 casas decimais, vírgula decimal; **exceto `hospedagem`** — ver linha abaixo |
| `LIMITE_DIARIO` (hospedagem) | `"limite de 1 diária aplicado (campo num_diarias ausente do schema)"` | exceção: `num_diarias` ausente do schema; `motivo_codigo` permanece `LIMITE_DIARIO` (RF-10, AMB-003, D-004) |
| `COTA_ESGOTADA` | `"cota diária de <categoria> esgotada: R$ <limite> já consumidos por itens anteriores no dia"` | `<limite>` = `LIMITE_DIARIO[categoria]` com 2 casas decimais, vírgula decimal |

#### Exemplo de saída (3 itens ilustrativos)

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
    "total_solicitado": 216.40,
    "total_reembolsavel": 114.90,
    "total_recusado": 101.50,
    "itens_processados": 3,
    "itens_aprovados": 1,
    "itens_parciais": 1,
    "itens_recusados": 1
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
    },
    {
      "id": "d-005",
      "status": "recusado",
      "valor_original": 89.00,
      "valor_considerado": 89.00,
      "valor_reembolsavel": 0.00,
      "motivo_codigo": "CATEGORIA_INVALIDA",
      "motivo_texto": "categoria fora da política: coworking",
      "duplicata_de": null
    },
    {
      "id": "d-006",
      "status": "aprovado",
      "valor_original": 54.90,
      "valor_considerado": 54.90,
      "valor_reembolsavel": 54.90,
      "motivo_codigo": null,
      "motivo_texto": null,
      "duplicata_de": null
    }
  ]
}
```

---

## 5. Requisitos funcionais

### RF-01 — Normalização de valor monetário

**Regra:** O valor de cada despesa é arredondado para 2 casas decimais com
regra half-up antes de qualquer outra regra ser aplicada. Todas as
comparações e cálculos subsequentes operam sobre o valor normalizado. Este é
o único ponto de arredondamento no fluxo de processamento.

**Origem:** AMB-010; política do RH (implícito — não define arredondamento).

**Aceite:**
- Despesa com `valor = 33.333` → `valor_original = 33.333`, `valor_considerado = 33.33`
- Despesa com `valor = 33.335` → `valor_original = 33.335`, `valor_considerado = 33.34`
- Despesa com `valor = 72.50` → `valor_original = 72.50`, `valor_considerado = 72.50` (inalterado)
- d-011 (`valor = 33.333`) → `valor_original: 33.333`, `valor_considerado: 33.33` — divergência visível na saída

---

### RF-02 — Normalização de categoria

**Regra:** O valor do campo `categoria` é convertido para letras minúsculas e
tem espaços externos removidos (trim) antes de qualquer outra regra. Nenhuma
outra transformação é aplicada: acentos não são normalizados, ortografia não
é corrigida, similaridade não é calculada.

**Origem:** AMB-011.

**Aceite:**
- `"ALIMENTACAO"` → `"alimentacao"` (reconhecida)
- `" Alimentacao "` → `"alimentacao"` (reconhecida)
- `"Alimentação"` → `"alimentação"` (acento mantido, não reconhecida → RF-05)

---

### RF-03 — Domínio de valor válido

**Regra:** Despesas com `valor_considerado ≤ 0,00` são recusadas com
`motivo_codigo = "VALOR_NAO_POSITIVO"`. Não consomem cota diária da categoria.

**Origem:** AMB-009; política do RH é silente sobre estornos — o sistema não
infere regra contábil não escrita.

**Aceite:**
- `valor = -45.00` → recusada, `valor_reembolsavel = 0,00`, cota do dia intacta
- `valor = 0.00` → recusada, `valor_reembolsavel = 0,00`
- `valor = 0.01` → não afetado por esta regra

---

### RF-04 — Período de competência

**Regra:** Despesas com `data` fora do intervalo fechado
`[periodo.inicio, periodo.fim]` são recusadas com
`motivo_codigo = "FORA_COMPETENCIA"`. Não consomem cota diária.
Quando `periodo.competencia` e os campos `inicio`/`fim` divergirem,
prevalecem `inicio` e `fim`.

**Limitação declarada:** a política usa o termo "lançadas", mas a data de
lançamento é ausente do schema; o sistema usa o campo `data` da despesa como
proxy. Recomendação de evolução: incluir campo `data_lancamento`.

**Origem:** AMB-008; política do RH, item 7.

**Aceite:**
- Período `2026-07-01` a `2026-07-31`; despesa com `data = 2026-04-15` → recusada
- Despesa com `data = 2026-07-01` → não afetada (limite inclusivo)
- Despesa com `data = 2026-07-31` → não afetada (limite inclusivo)
- Despesa com `data = 2026-08-01` → recusada

---

### RF-05 — Categorias válidas

**Regra:** Após normalização (RF-02), categorias fora da lista canônica são
recusadas com `motivo_codigo = "CATEGORIA_INVALIDA"` e
`motivo_texto = "categoria fora da política: <valor normalizado>"`.
Não consomem cota diária.

**Lista canônica:** `alimentacao`, `transporte_urbano`, `hospedagem`.

**Origem:** AMB-011, AMB-013; política do RH, item 9.

**Aceite:**
- `"coworking"` → recusada (`"categoria fora da política: coworking"`)
- `"ALIMENTACAO"` → normalizada para `"alimentacao"` → reconhecida
- `"taxi"` → não reconhecida → recusada

---

### RF-06 — Detecção e tratamento de duplicatas

**Regra:** Uma despesa é duplicata quando todos os campos a seguir coincidem
com algum item anterior na ordem de processamento: `data`,
`categoria` (pós-normalização), `descricao`, `fornecedor`,
`valor_considerado`, `tem_nota_fiscal`.

O item anterior é mantido; a duplicata é recusada com
`motivo_codigo = "DUPLICATA"` e `duplicata_de = <id do item mantido>`.

A verificação é feita contra todos os itens anteriores independentemente do
status deles. Duplicatas não consomem cota diária.

**Limitação declarada:** o sistema detecta apenas coincidência exata; campos
levemente diferentes (ex.: descrições com espaço a mais) não são detectados
como duplicata.

**Origem:** AMB-007; política do RH, item 8.

**Aceite:**
- d-006 e d-007 (todos os campos iguais) → d-006 mantido, d-007 recusado com
  `duplicata_de = "d-006"`
- Dois itens idênticos com `valor > 100` e sem NF → primeiro recusado por
  `SEM_NF`; segundo recusado por `DUPLICATA` (a comparação ocorre mesmo que
  o original tenha sido recusado)

---

### RF-07 — Obrigatoriedade de nota fiscal

**Regra:** Despesas com `valor_considerado > 100,00` e
`tem_nota_fiscal = false` são recusadas com `motivo_codigo = "SEM_NF"`.
Não consomem cota diária.

**Origem:** AMB-004, AMB-005; política do RH, item 5.

**Aceite:**
- `valor = 100.00`, sem NF → não afetado (limite exclusivo: 100,00 não é
  "acima de 100")
- `valor = 100.01`, sem NF → recusada por `SEM_NF`
- `valor = 150.00`, com NF → não afetado por esta regra
- d-003 (`valor = 100.00`, sem NF) → passa; d-004 (`valor = 100.01`, sem NF)
  → recusada — par de fronteira

---

### RF-08 — Limite diário de alimentação

**Regra:** O total reembolsável da categoria `alimentacao` por dia é limitado
a R$ 60,00. O limite é aplicado sobre o agregado diário. As despesas são
processadas na ordem do arquivo de entrada; desempate por `id` em ordem
lexicográfica crescente.

O saldo disponível para um item é:
`60,00 − Σ(valor_reembolsavel dos itens aprovados ou parciais de alimentacao
no mesmo dia já processados)`.

- Se `saldo > 0` e `valor_considerado > saldo`: reembolsa o saldo disponível,
  `motivo_codigo = "LIMITE_DIARIO"`.
- Se `saldo = 0`: reembolsa R$0,00, `motivo_codigo = "COTA_ESGOTADA"`.
- Se `saldo ≥ valor_considerado`: reembolsa integralmente (sem motivo de corte).

**Origem:** AMB-001, AMB-012, AMB-015; política do RH, item 1.

**Aceite:**
- d-001 (R$72,50, primeiro de alimentação do dia 03/07) → reembolsa R$60,00
  (`LIMITE_DIARIO`)
- d-002 (R$38,00, segundo do dia 03/07) → saldo = 0, reembolsa R$0,00
  (`COTA_ESGOTADA`)
- d-014 (`"ALIMENTACAO"`, R$61,00, único de alimentação do dia 31/07) →
  reembolsa R$60,00 (`LIMITE_DIARIO`)

---

### RF-09 — Limite diário de transporte urbano

**Regra:** Mesma lógica de RF-08, aplicada à categoria `transporte_urbano`,
com limite de R$ 80,00 por dia.

**Origem:** AMB-002, AMB-012, AMB-015; política do RH, item 2.

**Aceite:**
- d-003 (R$100,00, primeiro de transporte no dia 06/07, NF não exigida) →
  reembolsa R$80,00 (`LIMITE_DIARIO`)
- d-004 (R$100,01, sem NF) → recusado por `SEM_NF` no passo 6; não chega ao
  cálculo de limite; cota do dia não é afetada

---

### RF-10 — Limite por lançamento de hospedagem

**Regra:** Cada lançamento da categoria `hospedagem` é reembolsado em até
R$ 250,00. Cada entrada no arquivo conta como 1 diária,
independentemente do conteúdo do campo `descricao`. Não há acumulação diária:
o limite de R$250,00 se aplica por item, não por dia.

**Limitação declarada:** a política diz "por diária", mas o schema não fornece
campo de quantidade de diárias. O sistema degrada "por diária" para "por
lançamento" de forma consciente. O campo `descricao` não é utilizado para
extrair número de diárias (ver AMB-003). Recomendação de evolução: incluir
campo estruturado `num_diarias` na entrada.

**Justificativa na saída:** itens afetados devem ter `motivo_texto` citando
"limite de 1 diária aplicado (campo num_diarias ausente do schema)".

**Origem:** AMB-003; política do RH, item 3.

**Aceite:**
- d-010 ("Hotel Rio - 2 diárias", R$480,00, com NF) → reembolsa R$250,00
  (`LIMITE_DIARIO`)
- d-013 (R$690,00, sem NF) → recusado por `SEM_NF` antes de chegar ao limite
  de hospedagem
- Lançamento de R$200,00 com NF → reembolsa R$200,00 integralmente

---

### RF-11 — Ordem de aplicação das regras

**Regra:** Para cada despesa, as verificações ocorrem na seguinte sequência
fixa. A primeira regra reprovadora encerra o processamento do item
(**política de motivo único**): regras subsequentes não são avaliadas para
item já recusado.

| Passo | Verificação | Resultado em caso de falha |
|---|---|---|
| 1 | Normalização (RF-01, RF-02) | — (não gera recusa) |
| 2 | Domínio de valor (RF-03) | `VALOR_NAO_POSITIVO` |
| 3 | Competência (RF-04) | `FORA_COMPETENCIA` |
| 4 | Categoria (RF-05) | `CATEGORIA_INVALIDA` |
| 5 | Duplicata (RF-06) | `DUPLICATA` |
| 6 | Nota fiscal (RF-07) | `SEM_NF` |
| 7 | Limite diário (RF-08, RF-09, RF-10) | `LIMITE_DIARIO` ou `COTA_ESGOTADA` |

Itens recusados nos passos 2–6 não consomem cota diária da categoria.
O passo 7 é o único que pode gerar reembolso parcial.

**Origem:** AMB-015.

**Aceite:**
- Item com `data` fora de competência E sem NF → motivo `FORA_COMPETENCIA`
  (passo 3 precede passo 6)
- Dois itens idênticos com `valor > 100` e sem NF → primeiro: `SEM_NF`;
  segundo: `DUPLICATA` (passo 5 precede passo 6, e a comparação considera
  o original independentemente de seu status)

---

### RF-12 — Reembolso parcial por limite

**Regra:** Quando o passo 7 é alcançado e o saldo da categoria no dia é
positivo mas insuficiente para cobrir o `valor_considerado`, o item é
reembolsado pelo saldo disponível. O item **nunca é recusado por exceder o
limite** — apenas cortado.

**Origem:** AMB-012; política do RH, item 4 ("reembolsadas parcialmente").

**Aceite:**
- Item de alimentação de R$72,50 como primeiro do dia →
  reembolsado em R$60,00, não recusado
- Item de alimentação de R$30,00 como primeiro do dia →
  reembolsado em R$30,00 integralmente

---

### RF-13 — Definição de status por item

**Regra:** O `status` é derivado aritmeticamente dos valores do próprio item,
independentemente do `motivo_codigo`:

- `"aprovado"`: `valor_reembolsavel = valor_considerado`
- `"parcial"`: `0,00 < valor_reembolsavel < valor_considerado`
- `"recusado"`: `valor_reembolsavel = 0,00`

**Origem:** AMB-016.

**Aceite:**
- Item com `COTA_ESGOTADA` → `valor_reembolsavel = 0,00` → `status = "recusado"`
- Item com `LIMITE_DIARIO` e `valor_reembolsavel > 0` → `status = "parcial"`
- Item com `SEM_NF` → `valor_reembolsavel = 0,00` → `status = "recusado"`
- Item reembolsado integralmente → `status = "aprovado"`, `motivo_codigo = null`

---

### RF-14 — Schema e determinismo da saída

**Regra:** O arquivo de saída segue o schema da seção 4.2. Todos os valores
numéricos com exatamente 2 casas decimais, exceto `valor_original`, que ecoa
o valor da entrada sem normalização. Ordem dos itens = ordem da entrada.
Execuções com a mesma entrada produzem saída byte a byte idêntica (sem
timestamps nem dados voláteis).

**Origem:** AMB-016.

---

### RF-15 — Dias da semana sem distinção

**Regra:** O sistema aplica as mesmas regras independentemente do dia da semana
ou feriado. Despesas de sábado, domingo e feriados seguem o mesmo
processamento dos dias úteis.

**Origem:** AMB-014; política do RH é silente — criar distinção seria inventar
regra não escrita pelo RH.

**Aceite:**
- d-012 (sábado, R$47,20) → processado normalmente, reembolsado integralmente

---

### RF-16 — Regra de viagem suspensa

**Regra:** A regra 6 da política de RH ("colaborador em viagem tem limites
ampliados em 50%") está suspensa nesta versão. Nenhum item recebe limites
ampliados. Os limites aplicados são sempre os valores base:
alimentação R$60,00, transporte R$80,00, hospedagem R$250,00.

**Limitação declarada:** "em viagem" é fato administrativo que só o RH pode
declarar; o schema de entrada não fornece esse dado; inferir por heurística
seria criar regra não escrita. Recomendação de evolução: campo estruturado de
viagem na entrada (ex.: booleano ou lista de períodos de viagem).

**Origem:** AMB-006; política do RH, item 6.

**Aceite:** nenhum item do lote de exemplo aciona ampliação; itens de
hospedagem não alteram os limites de outras categorias.

---

## 6. Ambiguidades identificadas e decisões

> Esta seção é o coração da spec. Uma ambiguidade resolvida no código sem
> registro aqui conta como não resolvida.

| ID | Texto original do RH | O que não estava claro | Decisão | Justificativa |
|---|---|---|---|---|
| AMB-001 | "Alimentação tem limite de R$ 60 por dia." | Limite por despesa ou pelo agregado diário? | Agregado diário; corte na ordem do arquivo, desempate por `id` | "por dia" indica acumulação; ordem de chegada é determinística e auditável — ver RF-08 |
| AMB-002 | "Transporte urbano tem limite de R$ 80 por dia." | Mesma questão de AMB-001 | Mesma lógica da AMB-001 — agregado diário, ordem do arquivo | Redação idêntica à de alimentação; filosofias diferentes entre categorias criariam inconsistência — ver RF-09 |
| AMB-003 | "Hospedagem tem limite de R$ 250 por diária." | Schema não tem campo `num_diarias`; como aplicar limite "por diária"? | Cada lançamento = 1 diária; descrição ignorada | Regra de negócio não pode depender de parsing de texto livre — ver RF-10 |
| AMB-004 | "Nota fiscal é obrigatória acima de R$ 100." | R$ 100,00 exato exige NF? | Não exige; gatilho é `valor > 100,00` (exclusivo) | "Acima de" em leitura literal é exclusivo; "a partir de" seria inclusivo — ver RF-07 |
| AMB-005 | "Nota fiscal é obrigatória acima de R$ 100." | O que acontece quando NF é obrigatória mas ausente? | Recusa total; não consome cota | NF é requisito de compliance; sem comprovante não há justificativa contábil — ver RF-07 |
| AMB-006 | "Colaborador em viagem tem limites ampliados em 50%." | Schema não tem campo de status de viagem | Regra suspensa; nenhum item recebe limites ampliados | "Em viagem" é fato administrativo; inferir por heurística seria criar regra não escrita — ver RF-16 |
| AMB-007 | "Duplicatas devem ser tratadas." | O que define duplicata? O que "tratar" significa? | Coincidência exata de todos os campos exceto `id`; mantém o primeiro, recusa os demais | Coincidência exata é determinística e auditável; similaridade dependeria de interpretação de texto — ver RF-06 |
| AMB-008 | "Despesas devem ser lançadas dentro do período de competência." | `periodo.competencia` ou `periodo.inicio/fim`? "Lançadas" = data da despesa? | `inicio`/`fim` são autoritativos; `competencia` é informativo; `data` da despesa como proxy de lançamento | `inicio`/`fim` são datas concretas; `data_lancamento` é ausente do schema — ver RF-04 |
| AMB-009 | (silêncio da política sobre estornos) | Como tratar valor negativo (d-009, -R$45,00)? | Valor `≤ 0` recusado como fora do domínio; não afeta cota | O sistema detecta valor não positivo, não "estorno"; criar lógica de abatimento seria inventar regra não escrita — ver RF-03 |
| AMB-010 | (silêncio da política sobre arredondamento) | Como tratar valor com mais de 2 casas (d-011: 33,333)? | Half-up a 2 casas; ponto único no início do fluxo | Half-up é o padrão de sistemas financeiros brasileiros e conferível manualmente — ver RF-01 |
| AMB-011 | (categorias listadas na política sem definir capitalização) | `"ALIMENTACAO"` é reconhecida? | Case-insensitive + trim; categoria é enum, não texto livre | Normalizar caixa é tolerância de representação, não interpretação semântica — ver RF-02, RF-05 |
| AMB-012 | "Despesas acima do limite são reembolsadas parcialmente." | "Parcialmente" = corta o excedente ou recusa o item? | Reembolsa até o saldo disponível; nunca recusa por exceder limite | A palavra "parcialmente" na política contradiz recusa total — ver RF-12 |
| AMB-013 | "Categorias fora da política não são reembolsáveis." | Como tratar `coworking` (d-005)? | Recusado por `CATEGORIA_INVALIDA`; consequência direta de AMB-011 | Não pertence à lista canônica; registrada como entrada própria porque o caso existe nos dados — ver RF-05 |
| AMB-014 | (silêncio da política sobre dias da semana) | Despesa de sábado (d-012) é tratada diferente? | Mesmas regras para qualquer dia da semana ou feriado | Criar distinção seria inventar regra não escrita pelo RH — ver RF-15 |
| AMB-015 | (ausência de ordem de precedência entre as 9 regras da política) | Qual regra vence quando múltiplas incidem? | Sequência fixa de 7 passos; política de motivo único | Ordem declarada é necessária para resultado determinístico e auditável — ver RF-11 |
| AMB-016 | (política não define formato de saída) | Qual o schema, o enum de status e o enum de motivos? | Schema da seção 4.2; status derivado aritmeticamente; 7 códigos de motivo | Status aritmético é verificável sem conhecer a regra de origem; códigos estruturados permitem teste automático — ver RF-13, RF-14 |

---

## 7. Casos de borda

| Caso | Item de referência | Comportamento esperado | Regra |
|---|---|---|---|
| Dois itens de alimentação no mesmo dia | d-001 + d-002 (03/07) | d-001: parcial R$60,00 (`LIMITE_DIARIO`); d-002: recusado R$0,00 (`COTA_ESGOTADA`) | RF-08 |
| Fronteira inferior de NF: valor exato R$100,00 | d-003 | NF não exigida; item entra no cálculo de limite normalmente | RF-07 |
| Fronteira superior de NF: R$100,01 | d-004 | Recusado `SEM_NF`; não consome cota de transporte do dia | RF-07 |
| Categoria fora da política | d-005 (`coworking`) | Recusado `CATEGORIA_INVALIDA` | RF-05 |
| Duplicata exata | d-006 + d-007 | d-006 aprovado; d-007 recusado `DUPLICATA` de d-006 | RF-06 |
| Data fora de competência | d-008 (2026-04-15) | Recusado `FORA_COMPETENCIA` | RF-04 |
| Valor negativo | d-009 (-R$45,00) | Recusado `VALOR_NAO_POSITIVO`; cota de transporte de 11/07 intacta | RF-03 |
| Hospedagem multi-diária na descrição | d-010 ("2 diárias", R$480,00) | Trata como 1 diária; reembolsa R$250,00 (`LIMITE_DIARIO`) | RF-10 |
| Valor com 3 casas decimais | d-011 (33,333) | `valor_considerado = 33,33`; aprovado (dentro do limite diário) | RF-01 |
| Despesa de sábado | d-012 (18/07) | Processada normalmente; aprovado R$47,20 | RF-15 |
| Hospedagem sem NF acima de R$100 | d-013 (R$690,00, sem NF) | Recusado `SEM_NF`; limite de hospedagem nunca é avaliado | RF-07, RF-10 |
| Categoria em maiúsculas | d-014 (`"ALIMENTACAO"`, R$61,00) | Normalizada; corte para R$60,00 (`LIMITE_DIARIO`) | RF-02, RF-08 |
| Dois idênticos com valor > R$100 e sem NF | hipotético | Primeiro: `SEM_NF`; segundo: `DUPLICATA` (do primeiro) | RF-06, RF-07, RF-11 |
| Valor zero | hipotético | Recusado `VALOR_NAO_POSITIVO` | RF-03 |
| Cota esgotada por item anterior | d-002 (depois de d-001) | `COTA_ESGOTADA`, R$0,00, `status = "recusado"` | RF-08, RF-13 |

---

## 8. Ordem de aplicação das regras

Declarada em RF-11. Resumo:

```
1. Normalização   (valor half-up 2 casas + categoria lowercase+trim)
2. Domínio valor  →  valor_considerado ≤ 0   →  VALOR_NAO_POSITIVO
3. Competência    →  data fora de período     →  FORA_COMPETENCIA
4. Categoria      →  fora da lista canônica   →  CATEGORIA_INVALIDA
5. Duplicata      →  coincidência exata        →  DUPLICATA
6. Nota fiscal    →  valor > 100 sem NF        →  SEM_NF
7. Limite diário  →  aplica saldo da cota      →  LIMITE_DIARIO ou COTA_ESGOTADA
```

Passos 2–6: recusa total, sem consumo de cota, motivo único.
Passo 7: único que gera reembolso parcial (`status = "parcial"`) ou zera por
cota esgotada (`status = "recusado"`, `motivo_codigo = "COTA_ESGOTADA"`).

---

## 9. Critérios de aceite

O sistema está pronto quando, processando `exemplos/despesas-exemplo.json`:

- [ ] d-001 → `status: "parcial"`, `valor_reembolsavel: 60.00`, `motivo_codigo: "LIMITE_DIARIO"`
- [ ] d-002 → `status: "recusado"`, `valor_reembolsavel: 0.00`, `motivo_codigo: "COTA_ESGOTADA"`
- [ ] d-003 → `status: "parcial"`, `valor_reembolsavel: 80.00`, `motivo_codigo: "LIMITE_DIARIO"` (NF não exigida para R$100,00 exato)
- [ ] d-004 → `status: "recusado"`, `motivo_codigo: "SEM_NF"`; cota de transporte de 06/07 não afetada
- [ ] d-005 → `status: "recusado"`, `motivo_codigo: "CATEGORIA_INVALIDA"`, `motivo_texto` contém `"coworking"`
- [ ] d-006 → `status: "aprovado"`, `valor_reembolsavel: 54.90`
- [ ] d-007 → `status: "recusado"`, `motivo_codigo: "DUPLICATA"`, `duplicata_de: "d-006"`
- [ ] d-008 → `status: "recusado"`, `motivo_codigo: "FORA_COMPETENCIA"`
- [ ] d-009 → `status: "recusado"`, `motivo_codigo: "VALOR_NAO_POSITIVO"`; cota de transporte de 11/07 não afetada
- [ ] d-010 → `status: "parcial"`, `valor_reembolsavel: 250.00`, `motivo_codigo: "LIMITE_DIARIO"`, `motivo_texto` cita "limite de 1 diária aplicado"
- [ ] d-011 → `valor_original: 33.333`, `valor_considerado: 33.33`; `status: "aprovado"`, `valor_reembolsavel: 33.33`
- [ ] d-012 → `status: "aprovado"`, `valor_reembolsavel: 47.20`
- [ ] d-013 → `status: "recusado"`, `motivo_codigo: "SEM_NF"`
- [ ] d-014 → `valor_considerado: 61.00`; `status: "parcial"`, `valor_reembolsavel: 60.00`, `motivo_codigo: "LIMITE_DIARIO"`
- [ ] Executar duas vezes com a mesma entrada produz arquivos de saída byte a byte idênticos
- [ ] Nenhum item recebe `valor_reembolsavel` maior que o limite da categoria (60,00 / 80,00 / 250,00)
- [ ] Nenhum item recebe limites ampliados de viagem

