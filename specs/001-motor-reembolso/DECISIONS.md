# Log de Decisões e Mudanças de Spec

> Uma entrada **toda vez** que a spec mudar. Este arquivo é a prova de que a spec
> foi tratada como artefato vivo e não como cerimônia de abertura.
>
> Spec que não muda em dois dias é spec que ninguém consultou. Mudança não é
> demérito — mudança não registrada é.

Ordem cronológica inversa: a mais recente primeiro.

---

## D-014 — `_POLITICA_V3`: fallback temporário em `motor.py` durante migração para política externalizada · `2026-07-30`

**Gatilho:** T-025 refatorou `verificar_categoria` para receber `politica_eff`
como parâmetro. O motor passou a exigir uma política para verificar categorias,
mas `test_integracao.py` (que testa o lote v3 `despesas-exemplo.json`) ainda
chama `processar()` sem passar `politica_eff` — e continuará assim até T-028
tornar `--politica` obrigatório no CLI.

**Decisão:** `motor.py` define `_POLITICA_V3` — um dict com as três categorias
e limites da v3, no mesmo formato que `politica_efetiva()` retorna. Usado como
fallback quando `processar(politica_eff=None)`. Não é uma constante de negócio:
é scaffolding de migração.

**Por quê:** A alternativa (passar politica_eff em todos os testes existentes
de uma vez) acoplaria T-025 a T-028 e tornaria o diff maior e mais difícil de
revisar. Migração incremental é preferível quando cada task deve caber em um
commit revisável.

**Quando será removido:** em T-028, quando `processar` receber `politica_eff`
obrigatoriamente via CLI. Nesse ponto `_POLITICA_V3` é deletado e
`test_integracao.py` atualizado para passar a política v4 carregada do arquivo.

---

## D-013 — Argumentos `--politica` e `--cambio` são obrigatórios em toda execução · `2026-07-30`

**Gatilho:** AMB-025 — motor v2 precisa de dois arquivos novos na CLI. A
questão era se `--cambio` deveria ser condicional (só quando houver moeda
estrangeira na entrada).

**Decisão:** Ambos obrigatórios em toda execução. Sem condicional.

**Por quê:** Erro condicional (descoberto após leitura de `--input`) exige que o
processo já tenha carregado o JSON de entrada para saber que `--cambio` faz
falta — diagnóstico mais difícil. Obrigatório sempre é simples, consistente e
reproduzível em scripts.

**O que mudou na spec:** Seção 4.1 menciona três argumentos obrigatórios.
AMB-025 registrada na seção 6.

---

## D-012 — `periodicidade` controla o regime de agregação, não o número de diárias · `2026-07-30`

**Gatilho:** AMB-024 — campo `periodicidade` nas entradas de categoria da
política poderia ser interpretado como controle de quantas diárias contar por
lançamento (resolveria AMB-003) ou como regime de agregação (por dia vs por
lançamento).

**Decisão:** `periodicidade` controla apenas o regime: `"dia"` = acumula por
data; `"diaria"` = por lançamento. A limitação de `num_diarias` (AMB-003)
permanece ortogonal — cada lançamento ainda conta como 1 diária porque o schema
de entrada não possui o campo. Remove `CATEGORIAS_LIMITE_POR_LANCAMENTO`
hardcoded do código.

**Por quê:** Confundir os dois conceitos quebraria hospedagem (per-item) e
alimentação (por-dia) de forma não óbvia. Manter separação permite evoluir
AMB-003 independentemente quando `num_diarias` entrar no schema.

**O que mudou na spec:** RF-10 e RF-17 documentam a separação; AMB-024 na
seção 6.

---

## D-011 — `acrescimo_em_viagem_percentual` em politica-v4.json não ativa RF-16 · `2026-07-30`

**Gatilho:** AMB-023 — arquivo `politica-v4.json` contém
`"acrescimo_em_viagem_percentual": 50`. A dúvida era se o campo autoriza
aplicar RF-16.

**Decisão:** Motor ignora o campo. RF-16 continua suspensa. Campo existe para
referência futura.

**Por quê:** O comunicado do Dia 2 não menciona ativação de RF-16. Silêncio
sobre uma mudança de +50% em todos os limites não é autorização implícita. O
campo no arquivo antecipa uso futuro quando o schema de entrada ganhar campo de
status de viagem.

**O que mudou na spec:** RF-16 atualizado mencionando que o campo existe mas
é ignorado. AMB-023 na seção 6.

---

## D-010 — Limiar de NF é global do arquivo de política, sem override por CC · `2026-07-30`

**Gatilho:** AMB-022 — `nota_fiscal_obrigatoria_acima_de = 100.00` está no
campo raiz de `politica-v4.json`. A questão era se podia ter override por CC.

**Decisão:** Global, sem override. Comparação sempre sobre `valor_considerado`
em BRL (após conversão, se aplicável).

**Por quê:** Campo no raiz do arquivo (sem estrutura de CC) indica intenção
global. Consistente com AMB-021: BRL é a única referência após passo 1. Remove
constante `GATILHO_NF` hardcoded do código.

**O que mudou na spec:** RF-07 atualizado com referência ao campo raiz da
política. AMB-022 na seção 6.

---

## D-009 — Conversão de moeda ocorre no passo 1, `valor_considerado` é sempre BRL · `2026-07-30`

**Gatilho:** AMB-021 — onde entra a conversão de câmbio no pipeline?

**Decisão:** Passo 1, junto com o arredondamento half-up.
`valor_considerado` é sempre BRL. Todos os passos 2–7 operam sobre BRL
sem exceção.

**Por quê:** Ponto único de normalização (mesma filosofia de AMB-010). Passos
de negócio não precisam conhecer câmbio. Falha de câmbio rejeita o item antes
de qualquer regra de negócio, o que é correto: sem valor em BRL não há base de
cálculo.

**O que mudou na spec:** RF-01 reformulado com dois sub-passos explícitos.
RF-11 atualizado com passo 1 capaz de rejeitar. AMB-021 na seção 6.

---

## D-008 — `valor_original` ecoa moeda original; novos campos `moeda` e `taxa_cambio_aplicada` · `2026-07-30`

**Gatilho:** AMB-020 — colaborador submeteu EUR 22,00; o que entra em
`valor_original` na saída?

**Decisão:** `valor_original` ecoa o literal da entrada na moeda original
(22,00, não 130,46). Dois novos campos obrigatórios na saída por item:
`moeda` (ISO 4217, `"BRL"` quando ausente na entrada) e
`taxa_cambio_aplicada` (valor literal do arquivo de câmbio; `null` quando
`moeda = "BRL"`).

**Por quê:** "Original" significa o que o colaborador registrou. Alterar para
BRL tornaria o campo opaco e quebraria a auditoria. Os novos campos expõem a
conversão de forma rastreável.

**O que mudou na spec:** Seção 4.1 adicionou campo `moeda` na entrada.
Seção 4.2 adicionou `itens[].moeda` e `itens[].taxa_cambio_aplicada`.
AMB-020 na seção 6.

---

## D-007 — `MOEDA_NAO_SUPORTADA` para moeda ausente; `TAXA_INDISPONIVEL` para ausência de cotação · `2026-07-30`

**Gatilho:** AMB-019 — GBP ausente do `cambio.json`. A dúvida era se deveria
usar o mesmo código de TAXA_INDISPONIVEL ou um código distinto.

**Decisão:** Dois códigos distintos:
- `MOEDA_NAO_SUPORTADA`: moeda inteiramente ausente como chave da tabela.
- `TAXA_INDISPONIVEL`: moeda presente na tabela, mas sem cotação anterior ou
  na data da despesa (caso extremo de AMB-018).

**Por quê:** Mesmo princípio que separou `LIMITE_DIARIO` de `COTA_ESGOTADA`:
condição diferente → código distinto → diagnóstico operacional diferente.
"GBP não está no contrato" vs "taxa de USD ainda não foi publicada nessa data"
são problemas distintos para a equipe de RH.

**O que mudou na spec:** Enum de `motivo_codigo` (seção 4.2) ganhou duas
linhas em passo 1. Templates correspondentes adicionados. AMB-019 na seção 6.

---

## D-006 — Fallback de taxa câmbio: data anterior mais próxima, sem limite de dias · `2026-07-30`

**Gatilho:** AMB-018 — despesa de sábado (e-004, EUR 30,00 em 2026-07-18)
sem cotação PTAX porque fins de semana não são publicados.

**Decisão:** Busca a data exata; se ausente, busca a data imediatamente
anterior disponível para aquela moeda, sem limite de dias para trás. Se não
houver nenhuma data anterior no arquivo, rejeita com `TAXA_INDISPONIVEL`.

**Por quê:** Câmbio não muda no fim de semana, apenas não é republicado. Usar
a sexta como referência para sábado e domingo é o comportamento padrão de
sistemas PTAX. Lookback sem limite reflete que uma moeda pode não ter cotação
por períodos longos (feriados nacionais estrangeiros, etc.).

**O que mudou na spec:** RF-18 documenta o algoritmo de busca. AMB-018 na
seção 6.

---

## D-005 — Política de CC: merge com padrao; `limite: 0.00` é declaração explícita, não exclusão · `2026-07-30`

**Gatilho:** AMB-017 — `politica-v4.json` introduz `centros_custo`. CC-ENG-PLATAFORMA
declara `hospedagem.limite = 0.00` com observação "nao reembolsavel". A questão
era se ausência de categoria no CC significa exclusão ou herança do padrão.

**Decisão:** Merge: categoria ausente no CC herda do `padrao`; `limite: 0.00`
é declaração explícita (categoria reconhecida; passo 7 a processa, com cota
zero desde o início → sempre `COTA_ESGOTADA`). CC sem entrada em
`centros_custo` usa `padrao` integralmente.

**Por quê:** CC-ENG-PLATAFORMA declara a categoria com valor e observação
textual — se "ausência = exclusão" fosse a convenção, eles não precisariam
fazer isso. Consistente com a distinção entre `LIMITE_DIARIO` e `COTA_ESGOTADA`:
cota zero não elimina a categoria, apenas garante que toda despesa a zera.

**O que mudou na spec:** RF-05 e RF-17 documentam o merge. AMB-017 na seção 6.

---

## D-004 — Template de LIMITE_DIARIO para hospedagem é exceção ao padrão · `2026-07-30`

**Gatilho:** Revisão pré-T-017. Ao montar os critérios de aceite do item d-010,
foi detectada contradição entre três fontes na spec: RF-10/AMB-003 exigia
`motivo_texto` citando `"limite de 1 diária aplicado"` desde a decisão original;
a tabela D-001 generalizou `LIMITE_DIARIO` com um template único sem essa exceção;
e a seção 9 (critério 10) ainda citava `"limite de 1 diária aplicado"` — herdado
de RF-10, mas incompatível com D-001.

**Decisão:** Honrar AMB-003 — a decisão mais antiga e a razão de existir do
código de motivo `LIMITE_DIARIO` para hospedagem. Quando `categoria == "hospedagem"`
e `motivo_codigo == "LIMITE_DIARIO"`, `motivo_texto` é sempre
`"limite de 1 diária aplicado (campo num_diarias ausente do schema)"`.
Para todas as outras categorias, `LIMITE_DIARIO` usa o template genérico de D-001.

**O que mudou na spec:** Tabela de templates (seção 4.2) ganhou uma linha
separada para `LIMITE_DIARIO (hospedagem)`. RF-10 e critério 9.10 já estavam
corretos e foram mantidos.

**Por quê:** AMB-003 é a decisão que justificou a existência do limite por
lançamento (em vez de por dia) para hospedagem. O texto especial carrega a
justificativa arquitetural — sem ele o financeiro não sabe por que R$480 virou
R$250 sem referência à "2 diárias" descrita no campo.

**O que isso invalidou:** Template genérico de D-001 para `LIMITE_DIARIO`
permanece válido para `alimentacao` e `transporte_urbano`. Nenhum teste
existente cai.

**Tasks afetadas:** T-012 (`_texto_passo7` em `motor.py`) precisa de uma linha
adicional; T-017 verifica `motivo_texto` de d-010 por substring `"limite de 1 diária"`.

---

## D-003 — Template de COTA_ESGOTADA refinado com valor do limite · `2026-07-30`

**Gatilho:** Revisão de desenho da T-012 (pipeline). O template inicial de
`COTA_ESGOTADA` dizia apenas `"cota diária de <cat> esgotada"`. A revisão
lembrou que COTA_ESGOTADA e LIMITE_DIARIO foram criados como códigos distintos
(AMB-016) precisamente porque o texto deve explicar ao financeiro *por que* o
item foi zerado — e "esgotada" sem contexto não comunica o valor já consumido,
deixando a auditoria incompleta.

**O que mudou na spec:** Template de `COTA_ESGOTADA` na tabela de `motivo_texto`
(seção 4.2) alterado de `"cota diária de <cat> esgotada"` para
`"cota diária de <cat> esgotada: R$ <limite> já consumidos por itens anteriores no dia"`.

**Por quê:** Auditabilidade humana — o financeiro entende a recusa lendo a saída
(critério desde AMB-001). Citar o limite consumido torna a explicação completa
sem exigir consulta a tabelas externas.

**O que isso invalidou:** Nada — template era omisso, não errado. Nenhum teste
cai; nenhum código existente muda (T-012 ainda não estava implementada).

**Tasks afetadas:** T-012 implementa o template corrigido.

---

## D-002 — Escopo negativo: unicidade de id não validada · `2026-07-30`

**Gatilho:** Revisão de desenho da T-011 (`GerenciadorCotas`). A chave de
bucket de hospedagem usa `despesa.id` para garantir limite por lançamento
(RF-10/AMB-003). Isso expôs que dois itens com o mesmo `id` mas dados
diferentes compartilhariam o bucket — e que RF-06 (duplicatas) não pegaria
esse caso porque sua chave inclui os demais campos, não só o id.

**O que mudou na spec:** Adicionada linha ao escopo negativo (seção 3):
"Este sistema não valida unicidade de `id` na entrada".

**Por quê:** A garantia "id único no lote" era implícita e nunca declarada.
Torná-la explícita no escopo negativo deixa claro que comportamento com ids
repetidos é indefinido — e isenta o sistema de responsabilidade por isso.

**O que isso invalidou:** Nada — era omissão, não contradição. Nenhum teste
cai; nenhum código muda.

**Tasks afetadas:** Nenhuma refeita; T-011 implementa com ciência da limitação.

---

## D-001 — Templates de `motivo_texto` formalizados · `2026-07-30`

**Gatilho:** Início da implementação de T-006 (verificador passo 2). A spec
definia `motivo_codigo` e `motivo_texto` como campos obrigatórios de saída, mas
especificava o texto exato apenas para `CATEGORIA_INVALIDA` e `LIMITE_DIARIO`.
Os outros cinco códigos (`VALOR_NAO_POSITIVO`, `FORA_COMPETENCIA`, `DUPLICATA`,
`SEM_NF`, `COTA_ESGOTADA`) ficavam sem template — lacuna detectada antes de
escrever código.

**O que mudou na spec:** Adicionada tabela "Templates de `motivo_texto` por código"
na seção 4.2, logo após o enum de `motivo_codigo`. Todos os 7 códigos agora têm
template explícito com placeholders nomeados.

**Por quê:** Auditabilidade humana é critério do projeto desde AMB-001 (o
financeiro entende a recusa lendo a saída). Textos interpolados com valores reais
são mais informativos do que textos genéricos. Estratégia de teste mantida
consistente com AMB-016: testes afirmam `motivo_codigo`; `motivo_texto` só é
verificado por substring onde a spec define conteúdo específico.

**O que isso invalidou:** Nada — era lacuna, não contradição. Nenhum teste
existente cai; nenhum código existente precisou mudar.

**Tasks afetadas:** T-006 a T-010 implementam os templates ao construir
`ResultadoItem`; T-011 implementa `LIMITE_DIARIO` e `COTA_ESGOTADA`.
