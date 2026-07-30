# Relatório — Desafio SDD

**Aluno:** Jasson `<completar sobrenome>` · **Repositório:** `<link do fork>` · **Data:** `<data da entrega>`

> Isto não é redação. São **evidências**. Toda afirmação deve vir acompanhada de
> arquivo, hash de commit ou trecho de sessão exportada.

---

## Delegação

*O que você fez, o que o Claude fez, e por que dividiu assim.*

**A divisão:**

| Atividade | Quem | Por quê |
|---|---|---|
| Identificar ambiguidades | Claude propôs candidatas cruzando política × JSON; eu auditei a lista e completei 3 lacunas (d-005/coworking, d-012/fim de semana, schema de saída como decisão transversal) | Varredura sistemática é força do agente; garantir cobertura crítica é responsabilidade minha |
| Decidir as ambiguidades | Eu, sempre — o agente foi proibido de decidir via CLAUDE.md (apresenta 2–3 opções + consequência e aguarda) | As decisões são o que este relatório defende; regra 2 das invioláveis |
| Escrever a spec | Claude materializa a partir das minhas decisões; eu leio linha a linha antes do commit | Redação é rápida para ele; fidelidade à decisão é minha |
| Desenhar a arquitetura | Claude propôs (pipeline de verificadores, separação I/O/motor); eu auditei em dois rounds — as duas correções de precisão numérica do Caso 5 saíram dessa auditoria | Desenho técnico é força dele; a responsabilidade pelo fluxo do dado (leitura → Decimal) foi minha |
| Implementar | Claude escreve o código task por task; eu revisei o desenho por escrito antes de qualquer `Write` nas tasks críticas (regra do CLAUDE.md) — foi essa pausa que expôs o Caso 7 | Escrita é rápida para ele; desenho de estado é onde bugs silenciosos se escondem, e revisar por escrito antes do código é mais barato que depurar depois |
| Escrever testes | `<preencher na Fase 2>` | |
| Absorver o envelope | `<preencher no Dia 2>` | |

**Onde deleguei e me arrependi:** `<preencher ao longo do caminho>`

**Onde não deleguei e deveria ter delegado:** `<preencher ao longo do caminho>`

**Usei subagentes / skills / MCP / hooks?** `<preencher; se não usar, dizer por quê>`

**Configuração do agente:** consolidei as regras de trabalho no CLAUDE.md
(spec antes de código; decisões de ambiguidade são do humano; regra de bug de
spec; convenção de commits; lembrete de /export) e o roteiro das fases em
prompt-inicial.md. Commit: `docs(claude): consolida regras de trabalho no
CLAUDE.md e roteiro em prompt-inicial.md` (154f361). Efeito observável: o
agente passou a apresentar toda ambiguidade em formato opções + consequência e
a separar sozinho spec de plan (ex.: na AMB-010, apontou que half-up é spec e
decimal.Decimal é plan).

**Evidência da configuração funcionando (o outro lado do Discernimento):** na
AMB-016, o agente detectou proativamente uma lacuna semântica no enum de
motivos — o código LIMITE_DIARIO não distinguia "item cortado por limite"
(d-001, havia saldo) de "item zerado por cota já esgotada" (d-002, saldo zero
ao chegar) — e trouxe a questão para decisão em vez de resolver silenciosamente.
Comportamento induzido pela regra 2 do CLAUDE.md ("decisões de ambiguidade são
do humano"). Minha decisão: status derivado aritmeticamente do valor
(aprovado = integral; parcial = entre zero e o integral, exclusivos;
recusado = zero) + novo código COTA_ESGOTADA no enum.
Evidência: `docs/sessions/01-spec-plan-tasks.md`, trecho "Ponto fraco que você deve
verificar antes de prosseguir" (final da AMB-016).

**Mais um caso da configuração em ação (Fase 2):** T-006: o agente detectou
que a spec era omissa sobre `motivo_texto` para 4 dos 7 códigos de motivo
(definia apenas `CATEGORIA_INVALIDA` e `LIMITE_DIARIO`/`COTA_ESGOTADA`
explicitamente) e parou para pedir decisão em vez de inventar texto —
comportamento induzido pela regra 3 do CLAUDE.md ("explicação que não está na
spec é bug de spec"). Virou a primeira entrada do `DECISIONS.md` do projeto
(commit `7919f17`).

---

## Descrição

*Como você transformou requisito ambíguo em requisito verificável.*

**Requisito escolhido:** limite diário de alimentação (AMB-001 → RF-08).

**Versão 1 (o texto do RH, ponto de partida):**
> ```
> Alimentação tem limite de R$ 60 por dia.
> ```

**Versão final (RF-08 na spec, commit dce0728):**
> ```
> O total reembolsável da categoria alimentacao por dia é limitado a R$ 60,00.
> O limite é aplicado sobre o agregado diário. As despesas são processadas na
> ordem do arquivo de entrada; desempate por id em ordem lexicográfica
> crescente. O saldo disponível para um item é: 60,00 − Σ(valor_reembolsavel
> dos itens aprovados ou parciais de alimentacao no mesmo dia já processados).
> - Se saldo > 0 e valor_considerado > saldo: reembolsa o saldo disponível
>   (LIMITE_DIARIO).
> - Se saldo = 0: reembolsa R$0,00 (COTA_ESGOTADA).
> - Se saldo ≥ valor_considerado: reembolsa integralmente.
> ```

**O que estava ambíguo:** três coisas empilhadas na mesma frase: a unidade de
aplicação ("por dia" = por despesa ou pelo agregado?), a distribuição do corte
quando o agregado excede (proporcional? ordem de chegada?) e o critério de
ordenação que torna o resultado reproduzível (a política não diz o que é
"primeiro").

**Como percebi:** d-001 (R$72,50) e d-002 (R$38,00) no mesmo dia 03/07 tornam
as leituras divergentes em dinheiro: por despesa → R$98 no dia; agregado →
R$60. O par existe no JSON exatamente para forçar a decisão. A terceira camada
(ordenação) apareceu ao escolher corte por ordem de chegada: sem critério de
desempate declarado, a mesma entrada reordenada daria distribuição diferente.

**Commit da mudança:** `dce0728` (spec v1.0). A distinção
LIMITE_DIARIO/COTA_ESGOTADA foi refinamento posterior dentro da mesma sessão,
a partir de lacuna que o próprio agente levantou (ver Delegação).

**Padrão de spec estabelecido (evidência de método):** para toda ambiguidade de
dado ausente, adotei o mesmo formato — limitação explícita declarada + cláusula
de escopo negativo + recomendação de evolução do schema. Aplicado uniformemente
em AMB-003 (diárias), AMB-006 (status de viagem), AMB-008 (data de lançamento)
e AMB-009 (estornos/créditos).

**Candidato reserva para esta seção:** o episódio de `motivo_texto` (T-006)
também serve como exemplo de "Descrição" — a spec ganhou uma tabela de
templates por código que não existia na v1.0, motivada por uma lacuna
descoberta durante a implementação, não antecipada na manhã. Ilustra o FAQ do
desafio: "spec que não muda em dois dias é spec que ninguém consultou".

---

## Discernimento

*Onde o Claude errou e você pegou.*

### Caso 1 — Opções de decisão que violavam restrição do enunciado

**O que ele propôs:** Na AMB-003 (hospedagem multi-diária), as opções B e C
exigiam campo `num_diarias` no schema de entrada.

**Por que estava errado:** O DESAFIO.md fixa a interface: "A entrada está
definida em exemplos/despesas-exemplo.json. Respeite esse formato." O schema de
entrada não é meu para mudar; os casos ocultos virão sem o campo — B
degeneraria em A na prática e C recusaria toda hospedagem real.

**Como eu detectei:** Confrontando as opções com o enunciado antes de decidir.
A restrição mora no DESAFIO.md, não na política do RH — o agente cruzou apenas
a política com o JSON.

**O que eu fiz:** Mandei refazer o menu citando o trecho do DESAFIO.md. Ele
reconheceu o erro ("Você está certo — meu erro") e reapresentou com opções
válidas (A: 1 lançamento = 1 diária; D: extração da descrição com fallback).

**Onde está a evidência:** `docs/sessions/01-spec-plan-tasks.md`, trecho "Antes de
decidir a AMB-003".

### Caso 2 — Exemplo do schema contradizendo o próprio enum

**O que ele propôs:** Na AMB-016 (schema de saída), a proposta trazia um
exemplo com d-001 `status: "aprovado"` e valores 72,50 → 60,00.

**Por que estava errado:** Corte por limite é `"parcial"` pelo enum que a
própria proposta definia dois campos acima — o exemplo contradizia o schema
que o acompanhava.

**Como eu detectei:** Auditando o exemplo contra o enum, usando uma checklist
prévia do que a saída precisava refletir (status, motivos, duplicata_de,
valores original/considerado, determinismo).

**O que eu fiz:** Apontei a contradição, mandei corrigir o exemplo e apliquei
mais 7 ajustes na proposta (remoção de timestamp para garantir determinismo,
motivo em código + texto, campo duplicata_de, valor_original vs
valor_considerado, semântica do status declarada, ordem preservada, 2 casas).

**Onde está a evidência:** `docs/sessions/01-spec-plan-tasks.md`, trecho "Auditoria da
proposta".

### Caso 3 — Lacunas na lista inicial de candidatas

**O que ele propôs:** Lista inicial com 13 candidatas, sem d-005 (coworking),
d-012 (despesa em fim de semana) e o schema de saída como decisão transversal.

**Por que estava errado:** O FAQ do desafio é explícito: caso presente nos
dados de exemplo exige declaração explícita na spec — silêncio conta como
buraco.

**Como eu detectei:** Mantive um mapa próprio de estranhezas do JSON (feito
antes de abrir a sessão) e conferi a lista do agente contra ele.

**O que eu fiz:** Mandei incluir os 3 itens antes de decidir a primeira AMB.

**Onde está a evidência:** `docs/sessions/01-spec-plan-tasks.md`, trecho "Antes de
decidir a AMB-001".

### Caso 4 — Decisão invertida silenciosamente na materialização da spec

**O que ele propôs:** No spec.md materializado, `valor_original` apareceu como
"valor como veio na entrada, **normalizado a 2 casas**" — e a então seção 10
confessava "nesta versão os dois campos são sempre iguais".

**Por que estava errado:** A decisão registrada na AMB-016 era o oposto:
`valor_original` ecoa a entrada como veio (33.333) justamente para tornar a
normalização da AMB-010 auditável na saída — o próprio agente havia registrado
na hora "caso onde os dois campos divergem". Na redação, a decisão virou o
contrário dela mesma e o campo ficou decorativo.

**Como eu detectei:** Leitura linha a linha da spec materializada contra as
decisões do chat, antes do commit — exatamente o procedimento declarado na
seção Diligência.

**O que eu fiz:** Mandei 4 ajustes antes do commit: restaurar `valor_original`
sem normalização; declarar a exceção na regra de 2 casas (4.2 e RF-14); novos
aceites no RF-01 e na seção 9 (d-011 → 33.333 / 33.33); e fechar a decisão de
`total_solicitado` que estava registrada como "ponto em aberto".

**Onde está a evidência:** commit `dce0728` (spec já corrigida);
`docs/sessions/01-spec-plan-tasks.md`, trecho "Revisão da spec — aprovo com 4 ajustes".

### Caso 5 — Precisão numérica: o erro em duas camadas no plan.md

**O que ele propôs:** (a) No plan.md v1, o DT-004 armazenava `valor_original`
como float nativo do `json.load`. (b) Na correção, o agente generalizou:
afirmou que `parse_float=Decimal` faria inteiros da entrada (`480`) chegarem
como `Decimal("480")`.

**Por que estava errado:** (a) O float mais próximo de `33.335` é
`33.334999...`; `Decimal` construído desse float, com half-up a 2 casas, dá
33.33 — violando o aceite do RF-01 (`33.335 → 33.34`). O agente havia notado o
sintoma (round-trip da serialização) mas não a causa raiz (precisão perdida na
construção, antes de qualquer Decimal). (b) `parse_float` só intercepta
números com parte fracionária; `480` passa pelo `parse_int` e chega como `int`
Python — quebrando a uniformidade do modelo (`valor_original: Decimal`) que a
própria correção prometia.

**Como eu detectei:** Rastreando o fluxo do valor desde a string literal do
JSON até o Decimal, nos dois rounds de revisão do plan — antes de cada commit.

**O que eu fiz:** (a) Mandei reescrever o DT-004 com
`json.load(parse_float=Decimal)` — o parser recebe a string literal e
`Decimal("33.335")` é exato. (b) No segundo round, estendi para
`parse_float=Decimal, parse_int=Decimal` e exigi o teste de aceite
`test_rf01_valor_inteiro_da_entrada`. O teste
`test_rf01_valor_335_arredonda_para_34` é o que pegaria a regressão (a).

**Onde está a evidência:** commit do plan.md (f8fec92);
`docs/sessions/01-spec-plan-tasks.md`, trechos "Revisão do plan" e "Correção no DT-004
antes do commit".

**Adendo (Fase 2):** a mesma família de erro reapareceu no código de *teste* —
na T-003, o helper de fixtures passava o valor por float Python antes de
serializar o JSON, e o agente defendeu a suficiência com o argumento do repr
mínimo. Barrado pelo mesmo princípio: em precisão numérica, o caminho do dado
importa mais que o resultado do caso feliz. Evidência: sessão 02, trecho
"Quase aprovado — um ajuste no helper".

### Caso 6 — Teste cujo nome prometia mais do que exercitava

**O que ele propôs:** Na T-008 (verificador de categoria inválida), o teste
`test_rf05_categoria_apos_normalizacao_aceita` usava `categoria="alimentacao"`
já em minúscula na factory — não exercitava nenhuma normalização, apenas
confirmava que uma categoria já válida passa.

**Por que estava errado:** O aceite original da task era `"ALIMENTACAO"`
normalizada → aceita, que prova a cadeia `normalizar_categoria() →
verificar_categoria()`. Um teste verde com esse nome escondia a ausência real
de cobertura: se o pipeline (T-012) um dia esquecesse de normalizar antes de
verificar, este teste continuaria passando, e o buraco só apareceria (se
apareceu) na integração — longe da causa.

**Como eu detectei:** Lendo o corpo do teste contra o que o nome prometia, não
apenas confirmando que ele passava. "Teste verde" não é sinônimo de "teste
certo".

**O que eu fiz:** Mandei renomear o teste trivial para o que ele de fato faz
(`test_rf05_categoria_valida_aceita`) e adicionar um teste novo que simula o
pipeline em miniatura — chama `normalizar_categoria("ALIMENTACAO")` e só então
`verificar_categoria()` com o resultado, provando a cadeia real
(`test_rf05_maiusculas_normalizadas_e_aceitas`).

**Onde está a evidência:** sessão 02, trecho "Antes de aprovar: o teste
test_rf05_categoria_apos_normalizacao_aceita não testa o que o nome promete".

### Caso 7 — Bug de desenho pego antes de qualquer código nascer (T-011)

**O que ele propôs:** Antes de implementar o `GerenciadorCotas` (T-011), o
desenho usava a chave `(data, categoria)` para todas as três categorias
(alimentação, transporte, hospedagem) no dicionário de estado de cotas.

**Por que estava errado:** RF-10/AMB-003 declaram explicitamente que
hospedagem **não** tem acumulação diária — "o limite de R$ 250,00 se aplica
por item, não por dia". Com a chave `(data, categoria)` compartilhada, duas
despesas de hospedagem no mesmo dia dividiriam incorretamente um único limite
de R$ 250,00 em vez de ter R$ 250,00 cada. O bug era silencioso com os dados
do `exemplos/despesas-exemplo.json` (d-010 e d-013 caem em dias diferentes),
mas ativo com qualquer caso oculto ou do envelope que trouxesse duas
hospedagens no mesmo dia.

**Como eu detectei:** Pedi o desenho por escrito *antes* de qualquer `Write`
(regra do CLAUDE.md: pausa obrigatória antes da T-011) e confrontei a
estrutura de chave proposta contra o texto do RF-10, não contra os testes —
o bug não aparecia em nenhum teste possível com os dados do exemplo.

**O que eu fiz:** Mandei corrigir a chave para hospedagem: `(despesa.id,
categoria)` em vez de `(data, categoria)`, garantindo bucket único por
lançamento, nunca compartilhado entre itens do mesmo dia. Exigi um teste novo
na T-011 cobrindo exatamente esse caso (duas hospedagens no mesmo dia, ambas
dentro do limite, ambas aprovadas integralmente) —
`test_rf10_duas_hospedagens_mesmo_dia_independentes`. A revisão de desenho
também expôs uma segunda lacuna (unicidade de `id` nunca validada), registrada
como D-002 no DECISIONS.md e como linha nova do escopo negativo da spec.

**Onde está a evidência:** commit `e7c8a3` (`src/cotas.py`,
`tests/test_rf08_rf09_rf10_cotas.py`, spec.md e DECISIONS.md D-002); sessão
02, trecho "Antes de codar, um problema real no desenho".

**Padrão que eu notei:** Os erros do agente se distribuem em cinco famílias:
(1) *consistência interna* — exemplo contradizendo o enum que o acompanha
(Caso 2), decisão registrada e depois invertida na redação (Caso 4);
(2) *restrições fora do documento em foco* — opções que violavam o DESAFIO.md
enquanto ele olhava só a política (Caso 1); (3) *generalização técnica além do
que a ferramenta faz* — parse_float estendido mentalmente a inteiros (Caso 5b);
(4) *teste que não exercita o que o nome promete* — cobertura aparente sem
cobertura real (Caso 6); (5) *desenho que generaliza uma regra que não deveria
ser generalizada* — mesma estrutura de estado aplicada a categorias com
semânticas diferentes (Caso 7). Este último é o mais valioso: foi pego na
etapa de desenho, antes de qualquer código ou teste existir — evidência de que
a pausa obrigatória antes de tasks críticas (regra do CLAUDE.md) funciona na
prática. Meus alertas passaram a ser: conferir exemplos contra as regras que
os acompanham, reler documentos materializados contra as decisões originais,
rastrear o fluxo de dados de ponta a ponta em decisões de precisão numérica,
ler o corpo de cada teste contra o nome, e confrontar toda estrutura de estado
proposta contra o texto da spec categoria por categoria, não só contra os
dados de exemplo disponíveis.

---

## Diligência

*O que você verificou antes de aceitar.*

**Meu procedimento de verificação (até aqui):** Cada AMB foi decidida com as
opções e consequências à vista; toda resposta minha levou justificativa em uma
linha, escrita por mim. Para o schema de saída, montei checklist prévia e
auditei a proposta contra ela — foi o que expôs o Caso 2.

**Fase 2 — verificação de código (em andamento):** T-003: o agente defendeu
que passar o valor por float no helper de teste era suficiente "porque o repr
do Python emite o literal mínimo"; apontei que isso era acidente de
representação, não garantia — o mesmo arquivo receberia o teste do 33,335 na
T-004, e teste de precisão cujo insumo passa por float é frágil por definição.
Helper corrigido para escrever literais numéricos como texto cru no JSON.

**Fase 2 — exigindo evidência antes de aceitar (T-006):** o agente afirmou que
`_fmt_valor` (formatação de moeda brasileira por substituição de separadores)
funcionava para milhares "testado mentalmente" — pedi teste explícito antes de
aprovar o commit. Os 3 testes (típico, milhar, negativo com milhar) passaram,
confirmando a formatação. Nenhum bug encontrado desta vez, mas a verificação
virou evidência permanente reaproveitável, já que `_fmt_valor` é usado em
todos os verificadores seguintes (T-007 a T-010).

**Fase 2 — exigindo prova nova em vez de afirmação de correção (T-012):** o
agente relatou um bug de `replace_all` (renomeação de `_fmt_valor` para
`fmt_valor`) que teria sido "detectado e corrigido antes do commit" — recusei
aceitar a afirmação sozinha, porque a suíte de 45/45 mostrada era anterior à
correção. Exigi: (1) nova rodada completa da suíte, do zero, pós-correção;
(2) grep no repositório inteiro por resquícios do nome corrompido. As duas
vieram limpas (45/45, zero ocorrências) antes de eu aprovar o commit. O
princípio: até um erro auto-reportado de boa-fé precisa de prova nova, não de
confiança na palavra de quem o cometeu.

**Fase 2 — exigindo eliminação estrutural de risco em vez de suposição de
improbabilidade (T-015):** o serializador usava um sentinel fixo (`"##NUM##"`)
para preservar dígitos literais de `Decimal` na saída JSON — risco real de
colisão com texto de entrada não controlado (`descricao`, `fornecedor`,
`nome`), aceito pelo agente como "não acontece na prática". Exigi token
aleatório por chamada (`uuid.uuid4().hex`), que elimina a colisão por
construção matemática, não por suposição sobre os dados. Também exigi que os
testes de precisão verificassem a string literal do JSON, não o valor após
`json.loads()` — que não distingue `480` de `480.0`, escondendo exatamente a
falha que a técnica existe para evitar.

**Li o diff inteiro em que porcentagem das entregas?** `<preencher na Fase 2 —
honestamente>`

**O que aceitei sem verificar direito, e o que me custou:** `<preencher ao
longo do caminho>`

**Testes: quem escreveu, e como você sabe que eles testam a coisa certa?**
`<preencher na Fase 2>`

**Leitura de documentos materializados:** feita linha a linha no spec.md antes
do commit — expôs a inversão do `valor_original` (Caso 4 do Discernimento) e
resultou em 4 ajustes pré-commit (`dce0728`). Mesmo procedimento aplicado ao
plan.md, em dois rounds de revisão (Caso 5, `f8fec92`).

---

## O envelope

*A mudança de requisito do Dia 2.* `<preencher no Dia 2>`

**Quantos arquivos toquei na mão:** `<n>`
**Quanto tempo levou:** `<...>`
**Diff de absorção:** `<n> arquivos, +<n>/-<n> linhas`

**Absorveu de graça:** `<...>`

**Resistiu:** `<...>`

**Ordem em que fiz:** `<...>`

**Se eu tivesse escrito a spec original sabendo desta mudança:** `<...>`

**O que a spec me poupou, em concreto:** `<...>`

---

## Fechamento

`<preencher ao final do Dia 2>`

**Para qual tamanho de projeto isto valeu a pena?**

**Para qual não valeria?**

**O que eu faria diferente:**

**A coisa mais desconfortável que aprendi sobre como eu trabalho com IA:**