# Log de Decisões e Mudanças de Spec

> Uma entrada **toda vez** que a spec mudar. Este arquivo é a prova de que a spec
> foi tratada como artefato vivo e não como cerimônia de abertura.
>
> Spec que não muda em dois dias é spec que ninguém consultou. Mudança não é
> demérito — mudança não registrada é.

Ordem cronológica inversa: a mais recente primeiro.

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
