# Relatório — Desafio SDD

**Aluno:** Jasson Luiz · **Repositório:** https://github.com/JassonLuiz/sdd-desafio · **Data:** 31/07/2026

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
| Escrever testes | Claude escreve o teste junto com o código de cada task; eu confiro se o corpo do teste exercita de fato o que o nome promete (Casos 6, 9) antes de aprovar | Escrever é rápido; a fidelidade nome↔comportamento é o ponto cego mais recorrente do dia, então a checagem é minha |
| Absorver o envelope | Mesma divisão da manhã — Claude propõe ambiguidades e desenho, eu decido e reviso todo diff antes do commit; 9 ambiguidades novas, 10 tasks, ~1509 linhas | Processo já validado na manhã; nenhuma mudança de papel foi necessária |

**Onde deleguei e me arrependi:** Confiar em resumos textuais do agente em
vez de exigir o texto literal do arquivo, no início de cada rodada de
revisão. Isso se repetiu pelo menos três vezes (a materialização da spec
v2, a conclusão do D-014, o fechamento da T-029) — em cada uma, o resumo
inicial era coerente e plausível, mas só a leitura do texto literal
confirmava (ou, no Caso 4, desmentia) o que havia sido decidido. Deveria ter
estabelecido "sempre mostre o arquivo completo, nunca resuma" como regra
fixa desde a primeira rodada da tarde, em vez de precisar reafirmar isso a
cada vez que um resumo aparecia no lugar do texto.

**Onde não deleguei e deveria ter delegado:** A aprovação de permissões do
Claude Code para comandos repetitivos e de baixo risco (variações de
`python -m pytest ...`, leituras de arquivo, comandos de verificação). Em
vez de configurar uma regra ampla de permissão (`/permissions`) logo no
início da Fase 2, aprovei prompt por prompt ao longo do dia inteiro — um
custo de atenção real e evitável, sem ganho de segurança correspondente,
já que o verdadeiro portão de controle sempre foi a leitura do diff antes
do commit, não a autorização de cada execução de teste.

**Usei subagentes / skills / MCP / hooks?** Não cheguei a usar, por
dificuldades no processo de configuração/descoberta desses recursos dentro
do fluxo do desafio. Ficou como oportunidade não explorada — não sei dizer
se teria valido a pena sem ter testado.

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
importa mais que o resultado do caso feliz. Evidência: `docs/sessions/02-implementacao-base-v3.md`, trecho
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

**Onde está a evidência:** `docs/sessions/02-implementacao-base-v3.md`, trecho "Antes de aprovar: o teste
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

### Caso 8 — Bug real de portabilidade escondido atrás de correção de ambiente

**O que ele propôs:** Na T-016 (CLI), os testes passaram depois de uma
correção que ele descreveu apenas como "corrigir o encoding do subprocess" —
sem detalhar onde a correção morava.

**Por que estava errado:** A correção real estava só no ambiente de teste
(`PYTHONIOENCODING=utf-8` passado no `subprocess.run` do pytest), não no
código do `cli.py`. Isso escondia um bug real de portabilidade: qualquer
pessoa rodando `python -m src.cli` diretamente no Windows sem essa variável
receberia mensagens de erro em `cp1252`, quebrando qualquer captura de
`stderr` esperando UTF-8 — exatamente o tipo de coisa que travaria a correção
do instrutor se rodada em Windows sem configuração extra.

**Como eu detectei:** Recusei aceitar "corrigi o encoding" sem a localização
exata da correção — a mesma exigência de prova nova do episódio do
`replace_all` (T-012, ver Diligência). Perguntei diretamente se a correção
estava no código ou só no ambiente de teste.

**O que eu fiz:** Mandei mover a correção para dentro do `cli.py`
(`sys.stdout.reconfigure(encoding="utf-8")` e `sys.stderr.reconfigure(...)`)
e exigi que o teste comprovasse funcionar **sem** a variável de ambiente —
removendo o `PYTHONIOENCODING` do teste para provar que o código, e não o
ambiente, resolvia o problema.

**Onde está a evidência:** commit `39c218`; `docs/sessions/02-implementacao-base-v3.md`, trecho "Antes de
aprovar, falta a resposta mais importante: o que exatamente causou o erro de
encoding".

### Caso 9 — Decisão original perdida na consolidação, pega antes do teste nascer

**O que ele propôs:** Preparando a T-017 (testes de integração), o agente
detectou uma contradição de três vias na própria spec sobre o `motivo_texto`
de `LIMITE_DIARIO` para hospedagem: RF-10 e o critério 9.10 exigiam citar
"limite de 1 diária aplicado (campo num_diarias ausente do schema)"; a tabela
de templates do D-001 (T-006) havia generalizado `LIMITE_DIARIO` com um único
template para todas as categorias, sem essa exceção. O código implementado
seguia o D-001, contradizendo RF-10/critério 9.10. Ele apresentou três
opções (manter a generalização, restaurar a exceção, ou um texto híbrido) e
pediu minha decisão antes de escrever qualquer teste.

**Por que estava errado:** A exigência do texto específico para hospedagem
não era um detalhe esquecível — era decisão explícita da AMB-003, registrada
desde a manhã do Dia 1: *"a justificativa dos itens afetados na saída deve
citar o limite de 1 diária aplicado"*. Quando a tabela de templates unificada
foi criada na T-006 (D-001), ela generalizou `LIMITE_DIARIO` sem incorporar
essa exceção anterior — a mesma família de erro do Caso 4 (decisão registrada,
perdida numa consolidação posterior), desta vez entre duas partes da própria
spec em vez de entre chat e documento.

**Como eu detectei:** O próprio agente detectou a contradição, cruzando RF-10,
o critério 9.10 e a tabela D-001 antes de escrever os testes de integração —
e parou para pedir decisão em vez de silenciar o conflito (regra 3 do
CLAUDE.md em ação outra vez). Minha parte foi resolver a favor da decisão mais
antiga (AMB-003), com a justificativa de que ela carregava informação de
negócio (a limitação do schema) que o template genérico não substitui.

**O que eu fiz:** Mandei registrar D-004 no DECISIONS.md, atualizar a tabela
4.2 com a exceção de hospedagem explícita, e implementar a condição em
`motor.py` (`_texto_passo7`) — uma linha extra para `categoria == "hospedagem"`
antes do template genérico. Os 17 testes de integração da T-017 confirmaram
o comportamento correto de ponta a ponta (17/17), incluindo d-010 com o texto
restaurado.

**Onde está a evidência:** commits `3f8c32` (docs/spec: D-004) e `e571ff`
(feat/T-017: texto especial + 17 testes de integração); `docs/sessions/02-implementacao-base-v3.md`, trecho
"Encontrei uma inconsistência de três vias na spec antes de escrever T-017".

### Caso 10 — Números inventados no README, corrigidos por iniciativa própria

**O que ele propôs:** Na T-019 (README), o exemplo de saída trazia valores de
`resumo` plausíveis mas nunca verificados contra a execução real
(`total_solicitado: 1122.52`, `itens_aprovados: 4`).

**Por que estava errado:** Os valores reais, obtidos rodando a CLI contra
`exemplos/despesas-exemplo.json`, eram diferentes (`total_solicitado: 1861.84`,
`itens_aprovados: 3`). Um README com números plausíveis mas falsos não quebra
teste nenhum — é o tipo de erro que sobrevive silenciosamente até alguém
comparar manualmente, corroendo a credibilidade do documento sem nenhum sinal
de alarme.

**Como eu detectei:** Não detectei — esta foi a instância em que o próprio
agente aplicou por iniciativa própria o princípio de "prova, não afirmação"
que vinha sendo exigido dele o dia inteiro (episódios do `replace_all`, do
sentinel de serialização, do encoding). Antes de eu revisar o diff, ele rodou
a CLI, comparou os números do README com a saída real, encontrou a divergência
e corrigiu sozinho, relatando "os valores que coloquei no README estavam
errados. Corrijo antes de commitar."

**O que eu fiz:** Confirmei a correção e aprovei o commit. Registro este caso
não como falha minha em pegar o erro, mas como evidência de que a disciplina
de verificação exigida ao longo do dia foi internalizada e generalizada para
uma tarefa (README) onde ninguém tinha pedido explicitamente essa checagem.

**Onde está a evidência:** commit `d2a3b6`; `docs/sessions/02-implementacao-base-v3.md`, trecho "Os valores que
coloquei no README estavam errados. Corrijo antes de commitar."

### Caso 11 — Reincidência do `replace_all` corrompendo string literal (T-027)

**O que ele propôs:** Na T-027 (`GerenciadorCotas` com política efetiva),
renomear a constante `LIMITE_DIARIO` para `_LIMITE_V3` nos arquivos de teste
via substituição automatizada corrompeu, de novo, as ocorrências da **string
literal** `"LIMITE_DIARIO"` usada como valor de `motivo_codigo` em quatro
asserções de `test_integracao.py` (`assert item.motivo_codigo ==
"_LIMITE_V3"`, quando deveria continuar `"LIMITE_DIARIO"`).

**Por que estava errado:** É a mesma classe de erro do episódio do
`replace_all` na T-012 (ver Diligência): um identificador de código
(`LIMITE_DIARIO`, a constante Python) e uma string literal homônima de dado de
negócio (`"LIMITE_DIARIO"`, o valor do enum `motivo_codigo` definido na spec)
compartilham o texto, e uma substituição automatizada sem distinção semântica
corrompe as duas juntas.

**Como eu detectei:** O teste falhou (`assert "LIMITE_DIARIO" ==
"_LIMITE_V3"`), e reconheci o padrão imediatamente pela recorrência — apontei
a causa raiz antes mesmo do agente rodar o comando de debug que ele havia
proposto.

**O que eu fiz:** Mandei reverter as quatro linhas para o valor correto, e
exigi (não sugeri) duas varreduras completas por grep — uma por `_LIMITE_V3`
(confirmando que só aparece como identificador correto) e outra por
`"LIMITE_DIARIO"` (confirmando as 14 ocorrências corretas em todos os arquivos
de teste, sem nenhuma sobra corrompida) — antes de aceitar a correção como
completa. As duas vieram limpas.

**Onde está a evidência:** `docs/sessions/03-envelope-v4.md`, linha ~816,
trecho "_LIMITE_V3 — 5 ocorrências, todas corretas: 2 definições de dict...".

**Padrão que eu notei — reincidência:** Este é o mesmo erro do episódio do
`replace_all` (T-012), reincidente aqui na T-027 — não um incidente isolado.
"Encontrar e substituir" automatizado em texto que mistura identificador de
código e string literal de dado continua sendo o ponto cego técnico mais
recorrente do dia, mesmo após ter sido pego e corrigido explicitamente na
primeira ocorrência. Isso reforça uma conclusão de processo, não só de
código: a exigência de prova nova (grep completo, não afirmação de "corrigi")
precisa ser sistemática toda vez que uma substituição textual em massa
acontecer, independentemente de já ter sido ensinada uma vez.

### Caso 12 — Deriva entre estado real e estado declarado, pega na auditoria final

**O que ele propôs:** Nada — o `tasks.md` simplesmente nunca foi atualizado
com os checkboxes `[x]` ao longo do dia, embora T-003 a T-029 estivessem
todas implementadas, testadas e commitadas havia horas.

**Por que estava errado:** O arquivo declarava apenas 3 de 29 tasks
concluídas, uma contradição direta com o próprio histórico de commits
(`feat(T-XXX)`/`test(T-XXX)` para cada uma). Isso é exatamente o tipo de
"deriva silenciosa" que a rubrica pune — tasks não marcadas ao longo do
caminho sugerem processo encenado, mesmo quando o trabalho real foi feito
de forma legítima e rastreável.

**Como eu detectei:** Numa auditoria final antes da entrega, revisando o
`tasks.md` completo em vez de assumir que os checkboxes acompanhavam os
commits automaticamente.

**O que eu fiz:** Mandei confirmar, task por task, o hash de commit real
correspondente antes de marcar qualquer checkbox — nenhuma marcação sem
evidência. As 26 tasks pendentes foram verificadas contra 26 hashes reais
(coincidentes com os que já havíamos revisado ao longo do dia) antes da
edição.

**Onde está a evidência:** commit `2f76cfe`, cujo diff mostra os 26
checkboxes alterados na mesma ordem dos 26 hashes confirmados.

**Padrão que eu notei:** Os erros do agente se distribuem em seis famílias:
(1) *consistência interna* — exemplo contradizendo o enum que o acompanha
(Caso 2), decisão registrada e depois invertida na redação (Caso 4);
(2) *restrições fora do documento em foco* — opções que violavam o DESAFIO.md
enquanto ele olhava só a política (Caso 1); (3) *generalização técnica além do
que a ferramenta faz* — parse_float estendido mentalmente a inteiros (Caso 5b);
(4) *teste que não exercita o que o nome promete* — cobertura aparente sem
cobertura real (Caso 6); (5) *desenho que generaliza uma regra que não deveria
ser generalizada* — mesma estrutura de estado aplicada a categorias com
semânticas diferentes (Caso 7); (6) *correção de sintoma em vez de causa* —
ambiente de teste ajustado para mascarar um bug que continuava vivo no código
de produção (Caso 8). O Caso 7 continua o mais valioso por ter sido pego na
etapa de desenho, antes de qualquer código existir. Meus alertas passaram a
ser: conferir exemplos contra as regras que os acompanham, reler documentos
materializados contra as decisões originais, rastrear o fluxo de dados de
ponta a ponta em decisões de precisão numérica, ler o corpo de cada teste
contra o nome, confrontar toda estrutura de estado proposta contra o texto da
spec categoria por categoria, e perguntar sempre "essa correção está no
código ou só no ambiente que a está testando?".

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

**Li o diff inteiro em que porcentagem das entregas?** Estimativa honesta:
cerca de 75%. Nas ~30 tasks (base v3 + envelope), a leitura foi completa e
linha a linha nas tasks estruturais (T-002, T-006, T-011, T-012, T-015,
T-017, T-022, T-023, T-027, T-028) — foi aí que os 11 casos de Discernimento
apareceram. Nas tasks mais mecânicas e de baixo risco (normalização,
verificadores simples, T-013, T-021) a leitura foi mais rápida, apoiada nos
pontos fracos que o próprio agente levantava, sem reler cada linha do zero.

**O que aceitei sem verificar direito, e o que me custou:** No início da
tarde, aceitei alguns resumos de diff sem pedir o texto literal (a T-028 e
a materialização da spec v2 são os exemplos mais claros) — nos dois casos
tive que voltar atrás e pedir o conteúdo real antes de aprovar, o que
custou uma rodada extra de mensagens cada vez. O padrão só ficou consistente
depois de eu tratar "mostre o texto literal" como exigência fixa, não
pedido pontual.

**Testes: quem escreveu, e como você sabe que eles testam a coisa certa?**
O Claude Code, sob minha revisão linha a linha aprovando cada task. A
confiança de que testam a coisa certa vem de três práticas usadas o dia
inteiro: (1) exigir que testes de precisão comparem contra a saída real do
sistema, não estimativa mental (o episódio dos 17 asserts recalculados
contra `CC-ENG-PLATAFORMA` é o exemplo mais claro); (2) checar se o corpo
do teste corresponde ao que o nome promete, não só se ele passa (Casos 6 e
9); (3) exigir grep de verificação após qualquer edição em massa (Casos
"replace_all" da T-012 e T-027, ambos confirmados limpos por varredura, não
por afirmação).

**Leitura de documentos materializados:** feita linha a linha no spec.md antes
do commit — expôs a inversão do `valor_original` (Caso 4 do Discernimento) e
resultou em 4 ajustes pré-commit (`dce0728`). Mesmo procedimento aplicado ao
plan.md, em dois rounds de revisão (Caso 5, `f8fec92`).

---

## O envelope

*A mudança de requisito do Dia 2.* Recebida no grupo da turma na manhã do
Dia 2 (entrega adiada em um dia, mas o envelope chegou na data original):
política de reembolso passa a ser externalizada por centro de custo
(`politica-v4.json`), com uma categoria nova (`representacao`), um centro de
custo que zera hospedagem (`limite: 0.00`), e suporte a despesas em moeda
estrangeira com conversão via tabela de câmbio (`cambio.json`) e fallback de
data. O item C (fila de aprovação manual acima de R$500) foi descartado
conscientemente, registrado como decisão explícita — o comunicado deixava
isso opcional e sem penalidade.

**Quantos arquivos toquei na mão:** 28 arquivos (3 de spec: `spec.md`,
`plan.md`/`tasks.md`, `DECISIONS.md`; 10 de código-fonte em `src/`; 15 de
teste em `tests/`).

**Quanto tempo levou:** Cerca de 5 horas, do recebimento do envelope pelo
grupo da turma até o commit final da T-029 (testes de integração).

**Diff de absorção:** 28 arquivos, +1509/-215 linhas
(`git diff --stat 73a1ec~1..HEAD`). Dois módulos novos criados do zero
(`parser_politica.py`, `parser_cambio.py`); nenhum módulo da base v3 foi
descartado — todos foram estendidos.

**Absorveu de graça:** A separação núcleo/I/O do plan.md (DT-001) permitiu
plugar `politica_efetiva()` e `buscar_taxa()` como funções puras, sem tocar
na estrutura do pipeline. O padrão de pipeline como lista de verificadores
(DT-002) absorveu a conversão de moeda como um "passo 1b" sem reescrever a
ordem dos passos 2–7. O padrão de decisão para dado ausente (limitação
declarada + escopo negativo + recomendação de evolução), estabelecido na
manhã do Dia 1 para AMB-003/006/008/009, foi reaproveitado sem alteração
para as ambiguidades novas do envelope (AMB-018, AMB-019, AMB-023). A
convenção de commits e o formato do DECISIONS.md (gatilho → decisão → por
quê → o que invalidou → tasks afetadas) também foram usados sem ajuste,
gerando D-005 a D-015 no mesmo padrão de D-001 a D-004.

**Resistiu:** A chave de bucket do `GerenciadorCotas`, hardcoded para
`categoria == "hospedagem"` (Caso 7, manhã), teve que ser generalizada para
ler `periodicidade` da política em vez da categoria — refatoração real, não
extensão trivial (T-027). A migração dos ~15 pontos de chamada de
`processar()` para os novos parâmetros obrigatórios (`politica_eff`,
`gatilho_nf`) exigiu scaffolding temporário (D-014) para não acoplar tasks
que deveriam ser revisáveis independentemente — dívida técnica documentada
e removida na T-028. O recálculo dos 17 asserts de `test_integracao.py`
contra os novos limites de `CC-ENG-PLATAFORMA` foi o ponto de maior atrito:
a vigência retroativa da política significava que praticamente todos os
valores esperados do teste mais importante do projeto mudaram (d-001, d-002,
d-010, d-014 e os totais do resumo).

**Ordem em que fiz:** Rigorosamente spec → DECISIONS.md → tasks → código,
sem exceção, incluindo nas correções que apareceram no meio da
implementação (ex.: o template de `motivo_texto` para `LIMITE_DIARIO` de
hospedagem, D-004; os códigos de saída da CLI e o texto de `COTA_ESGOTADA`
com limite zero, D-015 — ambos discutidos e registrados em spec antes do
código correspondente ser escrito).

**Se eu tivesse escrito a spec original sabendo desta mudança:** Teria
desenhado o `GerenciadorCotas` recebendo a chave de bucket como uma função
injetada (estratégia), não como um `if categoria == "hospedagem"` — a
mesma classe de generalização que a T-027 acabou fazendo de qualquer forma,
só que sem o custo de descobrir o hardcoding tarde. Também teria projetado
`processar()` com `politica_eff` e `gatilho_nf` como obrigatórios desde a
v3, com um objeto "política v3" default explícito no `plan.md`, evitando
o scaffolding temporário do D-014 por completo.

**O que a spec me poupou, em concreto:** A separação núcleo/I/O e o padrão
de pipeline de verificadores fizeram com que nenhuma regra de negócio nova
(RF-17, RF-18) exigisse reescrever regras existentes — apenas estendê-las
com parâmetros novos. O padrão de decisão para dado ausente, já validado em
4 ambiguidades da manhã, tornou as 3 ambiguidades análogas do envelope
(fallback de câmbio, moeda ausente, viagem ainda suspensa) rápidas de
decidir — a estrutura da decisão já existia, só o conteúdo mudou.

---

## Fechamento

**Para qual tamanho de projeto isto valeu a pena?** Para este projeto —
uma regra de negócio real e ambígua, com mudança de requisito no meio do
caminho — o processo se pagou várias vezes: as duas revisões de desenho
antes de codar (T-011, T-012) pegaram bugs que só apareceriam em produção
com dados que o exemplo não cobria: cotas de hospedagem em dois lançamentos
no mesmo dia e a interação viagem/moeda. Vale a pena para qualquer sistema
onde "o que a regra de negócio realmente quer dizer" é mais incerto que "como
implementar a regra depois de decidida" — que é a maioria dos sistemas
financeiros e de compliance.

**Para qual não valeria?** Para um script de uso único, um protótipo
descartável, ou uma regra de negócio já 100% não ambígua e estável (ex.:
converter um CSV num formato fixo), o overhead de spec + DECISIONS.md +
tasks numeradas seria puro custo sem contrapartida — a ambiguidade é o que
justifica o processo, não o tamanho do código.

**O que eu faria diferente:** Teria desenhado `GerenciadorCotas` e a
assinatura de `processar()` já pensando em política/gatilho como parâmetros
de primeira classe desde a T-011, mesmo sem saber que o envelope viria —
"os limites podem vir de algum lugar externo algum dia" é uma suposição
barata de fazer em qualquer sistema financeiro, e teria evitado o
scaffolding do D-014 por completo.

**A coisa mais desconfortável que aprendi sobre como eu trabalho com IA:**
Que minha maior contribuição no dia não foi escrever nenhuma linha de
código — foi recusar aceitar "afirmei que funciona" como prova, repetidamente
(o `replace_all` da T-012 e da T-027, o sentinel de serialização, o encoding
da CLI, os números do README). Sem essa disciplina de exigir prova nova a
cada correção, pelo menos 4 dos 11 casos de Discernimento teriam passado
despercebidos até a integração — ou pior, até depois da entrega.