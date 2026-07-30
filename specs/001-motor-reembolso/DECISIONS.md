# Log de Decisões e Mudanças de Spec

> Uma entrada **toda vez** que a spec mudar. Este arquivo é a prova de que a spec
> foi tratada como artefato vivo e não como cerimônia de abertura.
>
> Spec que não muda em dois dias é spec que ninguém consultou. Mudança não é
> demérito — mudança não registrada é.

Ordem cronológica inversa: a mais recente primeiro.

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
