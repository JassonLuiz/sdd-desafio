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
| Desenhar a arquitetura | `<preencher na fase do plan.md>` | |
| Implementar | `<preencher na Fase 2>` | |
| Escrever testes | `<preencher na Fase 2>` | |
| Absorver o envelope | `<preencher no Dia 2>` | |

**Onde deleguei e me arrependi:** `<preencher ao longo do caminho>`

**Onde não deleguei e deveria ter delegado:** `<preencher ao longo do caminho>`

**Usei subagentes / skills / MCP / hooks?** `<preencher; se não usar, dizer por quê>`

**Configuração do agente:** consolidei as regras de trabalho no CLAUDE.md
(spec antes de código; decisões de ambiguidade são do humano; regra de bug de
spec; convenção de commits; lembrete de /export) e o roteiro das fases em
prompt-inicial.md. Commit: `docs(claude): consolida regras de trabalho no
CLAUDE.md e roteiro em prompt-inicial.md` (`<hash>`). Efeito observável: o
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
Evidência: `docs/sessions/01-<nome>.md`, trecho "Ponto fraco que você deve
verificar antes de prosseguir" (final da AMB-016).

---

## Descrição

*Como você transformou requisito ambíguo em requisito verificável.*

`<candidato forte: AMB-001 ("R$ 60 por dia") — do texto do RH à regra com
agregação diária, corte em ordem de lançamento e critério de ordenação
declarado (ordem do arquivo, desempate por id). Colar a versão 1 e a versão
final quando o spec.md for materializado, com o hash do commit.>`

**Versão 1 (minha primeira escrita):**
> ```
> <colar após materializar o spec.md>
> ```

**Versão final:**
> ```
> <colar>
> ```

**O que estava ambíguo:** `<preencher>`

**Como percebi:** `<preencher>`

**Commit da mudança:** `<hash>`

**Padrão de spec estabelecido (evidência de método):** para toda ambiguidade de
dado ausente, adotei o mesmo formato — limitação explícita declarada + cláusula
de escopo negativo + recomendação de evolução do schema. Aplicado uniformemente
em AMB-003 (diárias), AMB-006 (status de viagem), AMB-008 (data de lançamento)
e AMB-009 (estornos/créditos).

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

**Onde está a evidência:** `docs/sessions/01-<nome>.md`, trecho "Antes de
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

**Onde está a evidência:** `docs/sessions/01-<nome>.md`, trecho "Auditoria da
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

**Onde está a evidência:** `docs/sessions/01-<nome>.md`, trecho "Antes de
decidir a AMB-001".

**Padrão que eu notei:** Os erros do agente até aqui são de *consistência
interna* (exemplo vs enum) e de *restrições que moram fora do documento em
foco* (DESAFIO.md vs política). Ele cruza bem política × dados, mas escapam-lhe
restrições de outro arquivo e contradições entre partes da própria resposta.
Meu alerta passou a ser: conferir exemplos contra as regras que os acompanham,
e conferir opções de decisão contra os documentos que o agente não estava
olhando no momento.

---

## Diligência

*O que você verificou antes de aceitar.*

**Meu procedimento de verificação (até aqui):** Cada AMB foi decidida com as
opções e consequências à vista; toda resposta minha levou justificativa em uma
linha, escrita por mim. Para o schema de saída, montei checklist prévia e
auditei a proposta contra ela — foi o que expôs o Caso 2.

**Li o diff inteiro em que porcentagem das entregas?** `<preencher na Fase 2 —
honestamente>`

**O que aceitei sem verificar direito, e o que me custou:** `<preencher ao
longo do caminho>`

**Testes: quem escreveu, e como você sabe que eles testam a coisa certa?**
`<preencher na Fase 2>`

**Pendente registrado:** leitura linha a linha do spec.md materializado antes
do primeiro commit de spec — registrar aqui como foi e o que ajustei.

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