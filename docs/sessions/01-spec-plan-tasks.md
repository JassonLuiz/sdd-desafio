 ▐▛███▜▌   Claude Code v2.1.138
▝▜█████▛▘  Sonnet 4.6 · Claude Pro
  ▘▘ ▝▝    ~\OneDrive\Documentos\Estudos\Projeto NTT DATA IA\sdd-desafio

  Opus 4.7 xhigh is now available! · /model to switch

> Olá, me confirme em qual pasta você está                                      

● Estou na pasta principal do projeto:

  C:\Users\jasso\OneDrive\Documentos\Estudos\Projeto NTT DATA IA\sdd-desafio

✻ Baked for 4s

> /model                                                                        
  ⎿  Set model to Sonnet 4.6 (default)

> você está logado em qual conta do claude?                                     

● Não tenho acesso direto às informações de autenticação da sessão. Para
  verificar em qual conta o Claude Code está logado, você pode rodar no
  terminal:

  ! claude auth status

  ou

  ! claude config

  Isso mostrará a conta autenticada atual.

✻ Crunched for 4s

> claude auth status                                                            

  Ran 2 shell commands (ctrl+o to expand)

● O comando não está acessível no ambiente do agente. Rode diretamente no seu
  terminal:

  ! claude auth status

  Digite isso no prompt do Claude Code com o ! na frente para executar no seu
  shell local.

✻ Cogitated for 10s

> ! claude auth status                                                          

● O ! prefixado só executa o comando quando digitado no prompt do Claude Code (a
   linha de input do CLI), não como mensagem de chat.

  Para ver o status da autenticação, abra um terminal separado e execute:

  claude auth status

  Ou, se estiver usando o CLI interativo, na linha de prompt do Claude Code
  (onde você digita mensagens), escreva:

  ! claude auth status

  O resultado aparecerá direto na conversa.

✻ Churned for 11s

> clear                                                                         

● Tudo certo! Como posso ajudar?

✻ Sautéed for 2s

> /export docs/sessions/00-teste-export.md                                      
  ⎿  Conversation exported to: C:\Users\jasso\OneDrive\Documentos\Estudos\Projeto
      NTT DATA IA\sdd-desafio\docs\sessions\00-teste-export.md


※ recap: Estamos no projeto de motor de cálculo de reembolso de despesas corporativas. Nenhuma implementação foi iniciada ainda — o próximo passo é ler as specs em `specs/001-motor-reembolso/` antes de qualquer código. (disable recaps in /config)

> sudo npm i -g @anthropic-ai/claude-code                                       

● Parece que você está tentando instalar/atualizar o Claude Code globalmente.
  Quer que eu rode esse comando para você, ou está executando por conta própria
  no terminal?

✻ Cogitated for 2s

> rode para mim                                                                 

● No Windows não existe sudo. Rodando sem ele via PowerShell:

  Ran 1 shell command (ctrl+o to expand)

● Instalação concluída. Houve um aviso de permissão ao tentar remover um arquivo
   temporário (EPERM), mas o update em si foi bem-sucedido — changed 2 packages 
  in 13s.

  Se quiser confirmar a versão instalada:

  Ran 1 shell command (ctrl+o to expand)

● Claude Code atualizado para a versão 2.1.220.

✻ Brewed for 32s

※ recap: Você atualizou o Claude Code para a versão 2.1.220. O projeto ainda não tem implementação iniciada — o próximo passo é começar pela primeira task definida em `specs/001-motor-reembolso/tasks.md`. (disable recaps in /config)
> Leia o arquivo prompt-inicial.md e siga todas as instruções dele a partir de  
  agora. Comece pela leitura dos arquivos que ele manda ler.                    

● Vou localizar e ler o arquivo prompt-inicial.md.

  Searched for 1 pattern, read 1 file (ctrl+o to expand)

● Agora lendo todos os arquivos indicados em paralelo.

  Searched for 1 pattern, read 4 files (ctrl+o to expand)

● Agora lendo os esqueletos do template em paralelo.

  Read 5 files (ctrl+o to expand)
  ⎿  Loaded template\CLAUDE.md

● Li todos os arquivos. Aqui está o resumo em 5 linhas do que está sendo
  avaliado:

  ▎ 1. Qualidade da spec (25pts): as oito+ ambiguidades da política devem ser 
  ▎ identificadas, decididas explicitamente e justificadas — sem vazar solução 
  ▎ técnica para a spec.
  ▎ 2. Rastreabilidade (25pts): cadeia fechada spec → tasks → commits → testes; 
  ▎ cada regra de negócio deve ser rastreável até a linha de código e o teste.
  ▎ 3. Resposta à mudança (20pts): o "envelope lacrado" do Dia 2 deve ser 
  ▎ absorvido pela ordem spec → DECISIONS.md → tasks → código; entrar direto no 
  ▎ código penaliza.
  ▎ 4. Relatório com evidências (20pts): 4 Ds (Delegação, Descrição, 
  ▎ Discernimento, Diligência) + envelope, todos com commits citados, trechos de
  ▎  sessão e pelo menos um erro concreto meu identificado por você.
  ▎ 5. Produto funciona (10pts): CLI rodando, saída coerente com a spec, testes 
  ▎ passando — mas os 90 pontos restantes dependem do processo, não do código.

  ---
  Fase 1 — Passo 1: Caça às ambiguidades

  Cruzei a política do RH com cada item do JSON. Encontrei 13 candidatas,
  organizadas pelos três tipos:

  ---
  Tipo A — Unidade de aplicação

  A-1 | Regra: "Alimentação tem limite de R$ 60 por dia."
  Exposta por: d-001 (R$72,50) + d-002 (R$38,00) no mesmo dia 2026-07-03.
  → O limite é por despesa individual ou pelo agregado do dia?

  A-2 | Regra: "Transporte urbano tem limite de R$ 80 por dia."
  Exposta por: d-003 (R$100,00) + d-004 (R$100,01) no mesmo dia 2026-07-06.
  → Mesma pergunta: limite por corrida ou pelo total do dia?

  A-3 | Regra: "Hospedagem tem limite de R$ 250 por diária."
  Exposta por: d-010 ("Hotel Rio - 2 diárias", R$480,00) e d-013 ("Airbnb 3 
  noites", R$690,00).
  → O JSON não tem campo num_diarias. Como o sistema sabe quantas diárias são
  para aplicar o limite certo?

  ---
  Tipo B — Fronteira

  B-1 | Regra: "Nota fiscal é obrigatória acima de R$ 100."
  Exposta por: d-003 (valor exato R$100,00, sem NF).
  → R$100,00 exige NF? "Acima de" é > 100 (exclusivo) ou ≥ 100 (inclusivo)?

  B-2 | Regra: "Despesas acima do limite são reembolsadas parcialmente."
  Exposta por toda despesa que excede o teto.
  → "Parcialmente" = paga o limite e corta o excedente, ou recusa o item
  inteiro?

  B-3 | Regra: item 5 (NF obrigatória) + item 4 (reembolso parcial).
  Exposta por: d-004 (R$100,01, sem NF) e d-013 (R$690, sem NF).
  → Quando NF é obrigatória mas ausente: recusa total, ou reembolsa até R$100
  (abaixo do gatilho da NF)?

  B-4 | Regra: não há regra sobre casas decimais.
  Exposta por: d-011 (valor R$33,333 — três casas decimais).
  → Como arredondar? Half-up, bankers rounding, truncar?

  B-5 | Regra: não há regra sobre capitalização de categoria.
  Exposta por: d-014 (categoria "ALIMENTACAO" em maiúsculas).
  → Case-sensitive ou case-insensitive? Se case-sensitive, d-014 cairia na regra
   9 (categoria fora da política).

  ---
  Tipo C — Dado ausente

  C-1 | Regra: "Colaborador em viagem tem limites ampliados em 50%."
  Exposta por: nenhum campo no JSON indica status de viagem.
  → Como determinar se o colaborador está em viagem? Inferir pela presença de
  hospedagem? Campo ausente = regra inaplicável?

  C-2 | Regra: "Duplicatas devem ser tratadas."
  Exposta por: d-006 e d-007 (mesma data, categoria, descrição, fornecedor e
  valor — R$54,90 cada).
  → "Tratadas" como? Recusar ambas? Aceitar só a primeira? Sinalizar para
  revisão manual?

  C-3 | Regra: "Despesas dentro do período de competência."
  Exposta por: d-008 (data 2026-04-15, fora do período 2026-07-01 a 2026-07-31).
  → Competência é definida pelo campo periodo.inicio/fim do JSON, ou pelo campo
  periodo.competencia ("2026-07"), ou ambos?

  C-4 | Regra: nenhuma regra sobre estornos/valores negativos.
  Exposta por: d-009 (valor -R$45,00, "Estorno de corrida cancelada").
  → Ignorar? Deduzir do total da categoria/dia? Gerar reembolso negativo?

  ---
  Transversal

  T-1 | Regra: nenhuma regra define a ordem de aplicação.
  → Quando múltiplas regras incidem na mesma despesa (ex: fora de competência +
  sem NF + categoria desconhecida), qual é processada primeiro e qual aparece na
   justificativa?

  ---
  Total: 13 candidatas. Agora vou apresentar uma por vez para você decidir.

  ---
  AMB-001 — Unidade de aplicação do limite diário de alimentação

  Texto original do RH: "Alimentação tem limite de R$ 60 por dia."

  Item que expõe: d-001 (R$72,50) + d-002 (R$38,00), ambos em 2026-07-03,
  categoria alimentacao.

  Interpretações possíveis:

  Column 1: A
  Interpretação: Limite por despesa individual
  Consequência prática: d-001 excede → reembolsa R$60; d-002 fica dentro →
    reembolsa R$38. Total do dia: R$98.
  ────────────────────────────────────────
  Column 1: B
  Interpretação: Limite pelo total agregado do dia
  Consequência prática: Soma do dia = R$110,50 → reembolsa R$60 no total; cada
    item recebe proporção ou o excesso é cortado na segunda despesa.
  ────────────────────────────────────────
  Column 1: C
  Interpretação: Limite pelo total, corte aplicado na ordem de chegada
  Consequência prática: Processa d-001 primeiro: usa R$60 do limite, zera o
    saldo. d-002 fica sem reembolso. Total: R$60.

  Qual você escolhe: A, B ou C? (ou outra interpretação que eu não listei?)

✻ Cogitated for 2m 10s

※ recap: Estamos na Fase 1 do desafio SDD, caçando ambiguidades na política de reembolso antes de escrever qualquer código. Acabei de apresentar AMB-001 (limite de alimentação: por despesa ou por dia?) e aguardo sua escolha entre as opções A, B ou C. (disable recaps in /config)

> Atualizei o CLAUDE.md e o prompt-inicial.md virou o roteiro. Releia os dois e 
   continue.                                                                    

● CLAUDE.md relido. A stack está definida (Python 3, pytest, argparse,
  decimal.Decimal) — vai para o plan.md quando chegarmos lá.

  Continuando de onde paramos:

  ---
  AMB-001 — Unidade de aplicação do limite diário de alimentação

  Texto original do RH: "Alimentação tem limite de R$ 60 por dia."

  Item que expõe: d-001 (R$72,50) + d-002 (R$38,00), ambos em 2026-07-03, mesma
  categoria.

  Column 1: A
  Interpretação: Limite por despesa individual
  Consequência prática: d-001 → reembolsa R$60; d-002 → reembolsa R$38. Total do

    dia: R$98.
  ────────────────────────────────────────
  Column 1: B
  Interpretação: Limite pelo total agregado do dia, excedente cortado
    proporcionalmente
  Consequência prática: Soma = R$110,50 → reembolsa R$60 distribuído entre os
    itens.
  ────────────────────────────────────────
  Column 1: C
  Interpretação: Limite pelo total agregado, corte na ordem de chegada
  Consequência prática: d-001 consome os R$60 inteiros; d-002 fica sem
  reembolso.
    Total: R$60.

  Qual você escolhe?

✻ Churned for 13s

> /config                                                                       
  ⎿  Enabled always copy full response

※ recap: Estamos na Fase 1 do desafio SDD, caçando ambiguidades da política de RH antes de escrever qualquer spec. Acabei de apresentar AMB-001 (limite de alimentação: por despesa ou por dia agregado?) e aguardo sua escolha entre A, B ou C.

> Antes de decidir a AMB-001: adicione à lista de candidatas três itens que     
  faltaram — d-005/coworking (a spec precisa declarar explicitamente o          
  tratamento, mesmo que seja recusa por categoria fora da política),            
  d-012/despesa em fim de semana (a política não distingue dia útil de          
  sábado/plantão), e o schema de saída do resultado.json como decisão           
  transversal (formato da justificativa, códigos de motivo, status por item).   
  Depois disso, volte à AMB-001.                                                

● Bom olho. Três candidatas adicionadas à lista:

  ---
  A-4 | Regra: "Categorias fora da política não são reembolsáveis." (regra 9)
  Exposta por: d-005 (coworking, R$89,00, com NF).
  → A spec precisa declarar explicitamente o tratamento: gera entrada no
  resultado com status "recusado/categoria_nao_coberta"? É silenciado? Qual
  justificativa aparece?

  B-6 | Regra: a política não menciona dias da semana.
  Exposta por: d-012 ("Almoço de sábado — plantão", R$47,20, com NF).
  → Despesas em fim de semana ou feriado seguem as mesmas regras? A política é
  silente. Precisa ser declarado na spec (mesmo que a decisão seja "não
  distingue").

  T-2 | Transversal: schema de saída do resultado.json.
  A política não define formato de saída — essa é uma decisão de spec.
  → Qual o status por item (string livre? enum?)? A justificativa é texto
  narrativo ou código de motivo estruturado? O arquivo de saída tem cabeçalho de
   período/colaborador? Há um campo para valor reembolsável separado do valor
  original?

  ---
  Lista completa agora: 16 candidatas (A-1 a A-4, B-1 a B-6, C-1 a C-4, T-1 a
  T-2).

  ---
  Voltando à AMB-001:

  AMB-001 — Unidade de aplicação do limite diário de alimentação

  Texto original do RH: "Alimentação tem limite de R$ 60 por dia."

  Item que expõe: d-001 (R$72,50) + d-002 (R$38,00), ambos em 2026-07-03.

  Column 1: A
  Interpretação: Limite por despesa individual
  Consequência prática: d-001 → R$60; d-002 → R$38. Total: R$98.
  ────────────────────────────────────────
  Column 1: B
  Interpretação: Limite pelo total agregado do dia, excedente cortado
    proporcionalmente
  Consequência prática: Soma R$110,50 → distribui R$60 entre os itens.
  ────────────────────────────────────────
  Column 1: C
  Interpretação: Limite pelo total agregado, corte na ordem de chegada
  Consequência prática: d-001 consome R$60; d-002 fica com R$0. Total: R$60.

  Qual você escolhe?

✻ Worked for 14s

> C — "por dia" indica agregado diário, e corte em ordem de lançamento é        
  determinístico e auditável. Complemento da decisão: a ordem de processamento  
  é a ordem das despesas no arquivo de entrada, desempate por id; declare isso  
  na spec junto com a resolução, senão o resultado não é reproduzível.          

● Decisão registrada. Seguindo para AMB-002.

  ▎ AMB-001 — Limite diário de alimentação: unidade de aplicação
  ▎ Decisão: Limite de R$60 aplicado sobre o total agregado do dia. Quando o 
  ▎ saldo se esgota, despesas subsequentes ficam sem reembolso. Ordem de 
  ▎ processamento: ordem das despesas no arquivo de entrada; desempate por id 
  ▎ (lexicográfico crescente). Essa ordem deve ser a mesma no arquivo de saída.
  ▎ Justificativa: "por dia" indica acumulação; ordem de chegada é 
  ▎ determinística, auditável e reproduzível por qualquer pessoa que releia o 
  ▎ arquivo.
  ▎ Regra afetada: RN a criar (limite alimentação).

  ---
  AMB-002 — Unidade de aplicação do limite diário de transporte urbano

  Texto original do RH: "Transporte urbano tem limite de R$ 80 por dia."

  Item que expõe: d-003 (R$100,00, sem NF) + d-004 (R$100,01, sem NF), ambos em
  2026-07-06, mesma categoria.

  Nota: d-003 tem valor exato R$100,00 — o limite de NF (AMB de fronteira)
  também incide aqui, mas vamos decidir isso em separado.

  Column 1: A
  Interpretação: Limite por corrida individual
  Consequência prática: d-003 → reembolsa R$80; d-004 → reembolsa R$80. Total do

    dia: R$160.
  ────────────────────────────────────────
  Column 1: B
  Interpretação: Limite pelo total agregado do dia, corte na ordem de chegada
    (consistente com AMB-001)
  Consequência prática: d-003 consome os R$80 inteiros; d-004 fica com R$0.
    Total: R$80.
  ────────────────────────────────────────
  Column 1: C
  Interpretação: Limite pelo total agregado, excedente distribuído
    proporcionalmente
  Consequência prática: R$80 distribuído entre d-003 e d-004 proporcionalmente
  ao
    valor de cada um.

  A decisão de AMB-001 (agregado diário, corte na ordem de chegada) sugere
  consistência com a opção B — mas é você quem decide se a mesma lógica se
  aplica a transporte.

  Qual você escolhe?

✻ Cooked for 12s

※ recap: Estamos na Fase 1 do desafio SDD, caçando ambiguidades da política de RH antes de escrever qualquer código. Acabamos de resolver AMB-001 (limite diário de alimentação = agregado, corte por ordem de chegada) e aguardamos sua escolha entre A, B ou C para AMB-002 (limite diário de transporte urbano).

> B — mesma lógica da AMB-001: "por dia" indica agregado diário, corte na ordem 
   de lançamento, mesma regra de ordenação (ordem do arquivo, desempate por     
  id). As duas regras têm redação idêntica; não há motivo para filosofias       
  diferentes entre categorias.                                                  

● Registrado.

  ▎ AMB-002 — Limite diário de transporte urbano: unidade de aplicação
  ▎ Decisão: Mesma lógica da AMB-001 — limite de R$80 sobre o total agregado do 
  ▎ dia, corte na ordem de chegada (ordem do arquivo, desempate por id).
  ▎ Justificativa: redação idêntica à de alimentação; filosofias diferentes 
  ▎ entre categorias criariam inconsistência sem respaldo na política.
  ▎ Regra afetada: RN a criar (limite transporte).

  ---
  AMB-003 — Hospedagem multi-diária: como aplicar o limite "por diária" sem 
  campo de quantidade

  Texto original do RH: "Hospedagem tem limite de R$ 250 por diária."

  Item que expõe: d-010 ("Hotel Rio - 2 diárias", R$480,00) e d-013 ("Airbnb 3 
  noites", R$690,00). O JSON não tem campo num_diarias — a quantidade está
  apenas na descrição livre.

  Column 1: A
  Interpretação: Tratar cada entrada como 1 diária, ignorar a descrição
  Consequência prática: d-010 → limite R$250, reembolsa R$250; d-013 → limite
    R$250, reembolsa R$250. Penaliza quem lança corretamente em entrada única.
  ────────────────────────────────────────
  Column 1: B
  Interpretação: Exigir campo num_diarias na entrada; sem ele, tratar como 1
    diária
  Consequência prática: Força schema mais rico; entradas sem o campo são
  tratadas
    conservadoramente. d-010 e d-013 seriam tratadas como 1 diária.
  ────────────────────────────────────────
  Column 1: C
  Interpretação: Exigir campo num_diarias na entrada; sem ele, recusar o item
  por
    dado insuficiente
  Consequência prática: Mais rigoroso: falta de dado obrigatório bloqueia o
    reembolso.

  Ponto fraco que você deve verificar: a opção B e C mudam o schema de entrada —
   isso precisa estar declarado na spec junto com o schema, e o
  exemplos/despesas-exemplo.json existente ficaria tecnicamente incompleto (não
  tem o campo). Qual você escolhe?

✻ Sautéed for 12s

> Antes de decidir a AMB-003: as opções B e C conflitam com uma restrição do    
  DESAFIO.md — "A entrada está definida em exemplos/despesas-exemplo.json.      
  Respeite esse formato". O schema de entrada é fixo; os casos ocultos virão    
  sem num_diarias, então B degenera em A e C recusaria toda hospedagem real.    
  Refaça o menu com: (A) cada lançamento = 1 diária, descrição ignorada; (D)    
  extrair quantidade da descrição com formato reconhecido declarado e fallback  
  = 1 diária quando não reconhecer. Aponte os trade-offs de D, incluindo se     
  "noite" equivale a "diária".                                                  

● Você está certo — meu erro. Opções B e C violam a restrição do DESAFIO.md
  ("respeite esse formato"). Refazendo:

  ---
  AMB-003 — Hospedagem multi-diária (revisada)

  Texto original do RH: "Hospedagem tem limite de R$ 250 por diária."

  Item que expõe: d-010 ("Hotel Rio - 2 diárias", R$480,00) e d-013 ("Airbnb 3 
  noites", R$690,00). Schema de entrada é fixo — não há campo num_diarias.

  Column 1: A
  Interpretação: Cada lançamento = 1 diária; descrição ignorada
  Consequência prática: d-010 → limite R$250, reembolsa R$250 (perde R$230
    reembolsável); d-013 → limite R$250, reembolsa R$250. Conservador,
    previsível, mas penaliza sistematicamente quem lança corretamente em entrada

    única.
  ────────────────────────────────────────
  Column 1: D
  Interpretação: Extrair quantidade da descrição com padrão declarado na spec;
    fallback = 1 quando não reconhecer
  Consequência prática: d-010 ("2 diárias") → limite R$500, reembolsa R$480
    inteiros; d-013 ("3 noites") → depende da decisão sobre "noite = diária"
  (ver
     abaixo).

  Trade-offs de D que você deve pesar:

  1. Fragilidade do parsing de texto livre. A spec teria que declarar exatamente
   quais padrões são reconhecidos (ex: "N diárias", "N noites", "N dias").
  Qualquer variação fora do padrão cai no fallback silenciosamente — sem erro,
  sem aviso.
  2. "Noite" equivale a "diária"? A política diz "por diária". Um Airbnb cobra
  por noite; um hotel pode cobrar por diária (check-in a check-out). São
  conceitos próximos mas não idênticos. Se a spec equiparar os dois, d-013 usa 3
   × R$250 = R$750 de limite → reembolsa R$690 inteiros. Se não equiparar,
  "noites" não é reconhecido → fallback = 1 diária → reembolsa R$250.
  3. Casos ocultos do instrutor. Se chegarem lançamentos com "semanas", "dias"
  ou sem menção de quantidade, o comportamento do fallback (= 1 diária) pode
  gerar resultado surpreendente — e o resultado será conferido contra a sua
  spec, então desde que declarado, está correto.
  4. Auditabilidade. A opção A é 100% determinística sem depender de texto. A
  opção D introduce lógica de extração que precisa de teste próprio para cada
  padrão declarado.

  Qual você escolhe — A ou D? E se D: "noite" equivale a "diária"?

✻ Baked for 21s

> A — regra de negócio não pode depender de parsing de texto livre; sem campo   
  estruturado de quantidade, cada lançamento conta como 1 diária. Registre na   
  spec: (1) a limitação explícita — a política pressupõe dado que a entrada não 
   fornece, e o sistema degrada "por diária" para "por lançamento" de forma     
  consciente; (2) no escopo negativo: "este sistema não extrai dados de negócio 
   do campo descricao"; (3) a recomendação de evolução: incluir campo           
  estruturado de diárias na entrada. E a justificativa dos itens afetados na    
  saída deve citar o limite de 1 diária aplicado.                               
● Registrado — com todos os quatro pontos.

  ▎ AMB-003 — Hospedagem multi-diária: unidade de aplicação
  ▎ Decisão: Cada lançamento de hospedagem = 1 diária; limite R$250 por entrada.
  ▎  Descrição ignorada para fins de cálculo.
  ▎ Limitação declarada na spec: a política pressupõe quantidade de diárias que 
  ▎ a entrada não fornece; o sistema degrada "por diária" para "por lançamento" 
  ▎ de forma consciente.
  ▎ Escopo negativo (a inserir): "este sistema não extrai dados de negócio do 
  ▎ campo descricao."
  ▎ Recomendação de evolução (a inserir): incluir campo estruturado num_diarias 
  ▎ na entrada em versão futura.
  ▎ Justificativa de saída: itens afetados (d-010, d-013) devem citar "limite de
  ▎  1 diária aplicado por ausência de campo estruturado".
  ▎ Regra afetada: RN a criar (limite hospedagem).

  ---
  AMB-004 — Fronteira da obrigatoriedade de nota fiscal: R$100,00 exige NF?

  Texto original do RH: "Nota fiscal é obrigatória acima de R$ 100."

  Item que expõe: d-003 (valor exato R$100,00, tem_nota_fiscal: false).

  Column 1: A
  Interpretação: "Acima de" = estritamente maior que R$100 (exclusivo)
  Consequência prática: R$100,00 não exige NF → d-003 passa sem restrição de NF.

    Gatilho: R$100,01.
  ────────────────────────────────────────
  Column 1: B
  Interpretação: "Acima de" inclui R$100,00 (≥ 100, inclusivo)
  Consequência prática: R$100,00 exige NF → d-003 (sem NF) é afetado pela regra
    5. Gatilho: R$100,00.

  Ponto fraco: a escolha muda o tratamento de d-003 e de qualquer caso oculto
  com valor exato R$100,00. Ambas as interpretações são defensáveis; o que
  importa é que a spec declare o valor-gatilho com precisão (ex: "valor >
  100,00" ou "valor ≥ 100,00").

  Qual você escolhe — A ou B?

✻ Churned for 15s

※ recap: Estamos na Fase 1 do desafio SDD, caçando ambiguidades da política de RH antes de escrever qualquer código. Decidimos AMB-001, AMB-002 e AMB-003; aguardando sua escolha na AMB-004: NF obrigatória é "> R$100" (A) ou "≥ R$100" (B)?

> A — "acima de" em leitura literal é estritamente maior; quem quer incluir o   
  valor escreve "a partir de". Gatilho declarado na spec com precisão: NF       
  obrigatória quando valor > 100,00. O par d-003/d-004 vira o caso de teste da  
  fronteira (um de cada lado).                                                  

● Registrado.

  ▎ AMB-004 — Fronteira de NF obrigatória
  ▎ Decisão: NF obrigatória quando valor > 100,00 (estritamente maior). R$100,00
  ▎  exato não exige NF.
  ▎ Justificativa: "acima de" em leitura literal é exclusivo; "a partir de" 
  ▎ seria inclusivo.
  ▎ Caso de teste de fronteira: d-003 (R$100,00, sem NF) → passa; d-004 
  ▎ (R$100,01, sem NF) → afetado pela regra de NF.
  ▎ Regra afetada: RN a criar (NF obrigatória).

  ---
  AMB-005 — O que acontece quando NF é obrigatória mas ausente?

  Texto original do RH: "Nota fiscal é obrigatória acima de R$ 100." + "Despesas
   acima do limite são reembolsadas parcialmente."

  Item que expõe: d-004 (R$100,01, sem NF) e d-013 (R$690,00, sem NF). A
  política impõe NF mas não diz o que fazer quando ela falta.

  Column 1: A
  Interpretação: Recusa total do item
  Consequência prática: d-004 → R$0 reembolsado; d-013 → R$0. Rigoroso; penaliza

    quem esqueceu o comprovante.
  ────────────────────────────────────────
  Column 1: B
  Interpretação: Reembolsa até R$100,00 (abaixo do gatilho da NF)
  Consequência prática: d-004 → reembolsa R$100,00 (o máximo que não exigiria
    NF); d-013 → reembolsa R$100,00. Interpretação "reembolso parcial por
    ausência de NF".
  ────────────────────────────────────────
  Column 1: C
  Interpretação: Reembolsa normalmente mas sinaliza pendência para revisão
  manual
  Consequência prática: d-004 e d-013 recebem valor calculado normalmente, com
    flag pendente_nf na saída. Transfere a decisão para o financeiro.

  Ponto fraco que você deve verificar: a opção B cria uma interação com os
  limites de categoria — d-004 está em transporte (limite R$80/dia); reembolsar
  R$100,00 por ausência de NF ultrapassaria o próprio limite da categoria. A
  spec precisaria declarar qual regra tem precedência quando as duas incidem.

  Qual você escolhe — A, B ou C?

✻ Sautéed for 13s

> A — NF é requisito de compliance: despesa sem comprovante obrigatório não é   
  justificável contabilmente, logo não é reembolsável. Recusa total com motivo  
  explícito na saída. Registre também a interação com os limites diários: item  
  recusado por NF não consome a cota do dia da categoria (a recusa precede o    
  cálculo de limite) — isso alimenta a decisão transversal de ordem de          
  aplicação.                                                                    

● Registrado — e a decisão de ordem de aplicação já está parcialmente resolvida.

  ▎ AMB-005 — NF obrigatória ausente: consequência
  ▎ Decisão: Recusa total do item. Valor reembolsável = R$0. Motivo explícito na
  ▎  saída.
  ▎ Justificativa: NF é requisito de compliance; despesa sem comprovante 
  ▎ obrigatório não é justificável contabilmente.
  ▎ Interação com limites diários: item recusado por NF não consome a cota do 
  ▎ dia da categoria. A verificação de NF precede o cálculo de limite agregado.
  ▎ Caso de teste: d-004 (R$100,01, sem NF, transporte) → recusado; não consome 
  ▎ os R$80 de transporte do dia 2026-07-06. D-003 (R$100,00, sem NF, mesmo dia)
  ▎  → NF não exigida (AMB-004), entra no cálculo de limite normalmente.
  ▎ Regra afetada: RN a criar (NF obrigatória) + ordem de aplicação.

  ---
  AMB-006 — "Colaborador em viagem": dado ausente no schema

  Texto original do RH: "Colaborador em viagem tem limites ampliados em 50%."

  Item que expõe: o JSON não tem campo em_viagem nem equivalente. Nenhum dos 14
  itens do exemplo declara esse status.

  Column 1: A
  Interpretação: Dado ausente = regra inaplicável; limites ampliados nunca são
    acionados
  Consequência prática: Sistema mais simples e determinístico. A regra 6 existe
    na política mas fica declarada como fora de escopo por falta de dado de
    entrada.
  ────────────────────────────────────────
  Column 1: B
  Interpretação: Inferir "em viagem" pela presença de hospedagem no mesmo
  período
  Consequência prática: Heurística: se há ao menos um item de hospedagem no
  lote,
    o colaborador está em viagem e todos os limites do período são ampliados.
    Cobre d-010 e d-013, mas é frágil (e se a hospedagem foi recusada?).
  ────────────────────────────────────────
  Column 1: C
  Interpretação: Inferir "em viagem" por data — dias com hospedagem ou
  transporte
    acima de limiar
  Consequência prática: Mais granular mas ainda heurística; ambíguo sobre quais
    dias contam como "em viagem".

  Ponto fraco que você deve verificar: B e C introduzem lógica inferencial que a
   política não descreve — qualquer heurística que você escolher precisará de
  justificativa explícita na spec, pois os casos ocultos do instrutor serão
  conferidos contra ela. A opção A é a única que não cria novo dado a partir de
  texto ou estrutura não declarados.

  Qual você escolhe — A, B ou C?

✻ Cooked for 16s

※ recap: Estamos na Fase 1 do desafio SDD, caçando ambiguidades da política de reembolso antes de escrever qualquer código. Decidimos AMB-001 a AMB-005; aguardando sua escolha na AMB-006 (colaborador "em viagem": A = ignorar por dado ausente, B = inferir por hospedagem, C = inferir por data).

> A — o sistema não infere dados que a entrada não fornece; "em viagem" é fato  
  administrativo que só o RH pode declarar, não algo a adivinhar por            
  heurística. Registre no mesmo formato da AMB-003: (1) limitação explícita — a 
   regra 6 da política pressupõe dado ausente do schema e fica inaplicável;     
  nenhum item recebe limites ampliados; (2) escopo negativo: "este sistema não  
  infere status de viagem a partir de padrões nas despesas"; (3) recomendação   
  de evolução: campo estruturado de viagem na entrada (ex.: booleano ou         
  períodos de viagem). Caso de teste: nenhum item do exemplo aciona ampliação   
  de 50%.                                                                       

● Registrado.

  ▎ AMB-006 — "Colaborador em viagem": dado ausente
  ▎ Decisão: Regra 6 inaplicável. Nenhum item recebe limites ampliados. Valor 
  ▎ reembolsável calculado sempre com os limites base.
  ▎ Limitação declarada na spec: a regra 6 da política pressupõe dado de status 
  ▎ de viagem que o schema de entrada não fornece; a regra fica suspensa por 
  ▎ falta de insumo.
  ▎ Escopo negativo (a inserir): "este sistema não infere status de viagem a 
  ▎ partir de padrões nas despesas."
  ▎ Recomendação de evolução: campo estruturado na entrada (ex.: em_viagem: bool
  ▎  ou lista de períodos de viagem).
  ▎ Caso de teste: nenhum item do exemplo aciona ampliação de 50%; todos os 
  ▎ limites aplicados são os limites base.
  ▎ Regra afetada: RN a criar (limites base; regra 6 declarada suspensa).

  ---
  AMB-007 — "Duplicatas devem ser tratadas": o que é duplicata e o que fazer com
   ela?

  Texto original do RH: "Duplicatas devem ser tratadas."

  Item que expõe: d-006 e d-007 — mesma data (2026-07-09), mesma categoria
  (alimentacao), mesma descrição ("Almoco"), mesmo fornecedor ("Bistro 
  Central"), mesmo valor (R$54,90), ambos com NF.

  Há duas perguntas encadeadas: o que define duplicata e o que "tratar" 
  significa.

  O que define duplicata:

  Column 1: i
  Critério: Todos os campos iguais exceto id (data + categoria + descrição +
    fornecedor + valor + NF)
  Risco: Mais preciso; dois almoços idênticos em dias diferentes não são
    duplicata.
  ────────────────────────────────────────
  Column 1: ii
  Critério: Apenas data + categoria + valor iguais
  Risco: Mais amplo; pode falso-positivo se dois itens legítimos coincidirem em
    valor.

  O que fazer com a duplicata:

  Column 1: A
  Ação: Manter o primeiro (menor id), recusar os demais com motivo duplicata
  Consequência prática: d-006 reembolsado (dentro do limite diário); d-007
    recusado. Determinístico e auditável.
  ────────────────────────────────────────
  Column 1: B
  Ação: Recusar todos os itens duplicados
  Consequência prática: Ambos d-006 e d-007 recusados. Penaliza inclusive o
    lançamento original.
  ────────────────────────────────────────
  Column 1: C
  Ação: Sinalizar como suspeito e reembolsar normalmente
  Consequência prática: Ambos entram no cálculo; flag suspeito_duplicata na
    saída. Transfere decisão ao financeiro.

  Ponto fraco: o critério i com a ação A é o mais defensável — determinístico,
  auditável, e o id de desempate já foi declarado em AMB-001. A spec precisa
  listar exatamente quais campos compõem a chave de duplicata.

  Qual você escolhe — critério (i ou ii) e ação (A, B ou C)?

✻ Worked for 15s

> Critério i + ação A — duplicata é coincidência exata de todos os campos       
  exceto id (data, categoria, descrição, fornecedor, valor, tem_nota_fiscal);   
  mantém-se a primeira pela ordenação já declarada (ordem do arquivo, desempate 
   por id), demais recusadas com motivo "duplicata de d-XXX" citando o item     
  mantido. Coerência com AMB-005: item recusado por duplicata não consome cota  
  diária. Limitação a declarar na spec: o sistema detecta duplicata exata, não  
  similaridade (descrições levemente diferentes escapam) — mesma filosofia de   
  não interpretar texto livre. Caso de teste: d-006 mantido e reembolsado       
  integral (R$54,90 < limite diário), d-007 recusado.                           

● Registrado.

  ▎ AMB-007 — Duplicatas: definição e tratamento
  ▎ Decisão: Duplicata = coincidência exata de data + categoria + descrição + 
  ▎ fornecedor + valor + tem_nota_fiscal (todos os campos exceto id). Mantém-se 
  ▎ o primeiro pela ordem já declarada (ordem do arquivo, desempate por id); 
  ▎ demais recusados com motivo "duplicata de d-XXX" citando o id mantido.
  ▎ Coerência com AMB-005: item recusado por duplicata não consome cota diária.
  ▎ Limitação declarada na spec: o sistema detecta duplicata exata; descrições 
  ▎ levemente diferentes não são detectadas — mesma filosofia de não interpretar
  ▎  texto livre.
  ▎ Caso de teste: d-006 mantido e reembolsado (R$54,90, dentro do limite diário
  ▎  de alimentação); d-007 recusado com motivo "duplicata de d-006".
  ▎ Regra afetada: RN a criar (duplicatas).

  ---
  AMB-008 — Período de competência: o que define o limite temporal?

  Texto original do RH: "Despesas devem ser lançadas dentro do período de 
  competência."

  Item que expõe: d-008 (data 2026-04-15, categoria alimentacao, R$41,00, com
  NF) — três meses antes do período do lote.

  O JSON tem dois campos temporais: periodo.competencia ("2026-07") e
  periodo.inicio/periodo.fim (2026-07-01 a 2026-07-31).

  Column 1: A
  Interpretação: Competência = intervalo [periodo.inicio, periodo.fim] (datas
    explícitas)
  Consequência prática: Verificação contra datas concretas; d-008 (2026-04-15)
    fora → recusado. Mais flexível: cobre períodos não-calendário (ex:
  quinzena).
  ────────────────────────────────────────
  Column 1: B
  Interpretação: Competência = mês de periodo.competencia ("2026-07") — qualquer

    data no mesmo ano-mês
  Consequência prática: Verificação mais simples; "2026-07" implica 2026-07-01 a

    2026-07-31. Resultado idêntico para este exemplo, mas diverge se inicio/fim
    não coincidirem com o mês cheio.
  ────────────────────────────────────────
  Column 1: C
  Interpretação: Usar periodo.inicio/periodo.fim como fonte primária;
    periodo.competencia apenas informativo
  Consequência prática: Igual a A na prática, mas torna explícita a hierarquia
    dos campos — evita ambiguidade futura se os dois campos divergirem.

  Ponto fraco: A e C são quase idênticas; a diferença é declarar na spec qual
  campo é autoritativo quando os dois divergirem. Isso protege contra entradas
  onde competencia: "2026-07" mas inicio: 2026-07-05 e fim: 2026-07-25 — qual
  prevalece?

  Qual você escolhe — A, B ou C?

✻ Cooked for 14s

※ recap: Estamos na caça às ambiguidades da política de RH (Fase 1 do SDD). Decidimos AMB-001 a AMB-007; aguardo sua escolha entre A, B ou C para AMB-008 (qual campo define o período de competência).

> C — periodo.inicio/fim é a fonte autoritativa do intervalo;                   
  periodo.competencia é informativo. Se os campos divergirem, prevalecem        
  inicio/fim (declarar na spec). Duas camadas adicionais a registrar: (1) a     
  política diz "lançadas" — data de lançamento é dado ausente do schema; o      
  sistema interpreta competência pela data da despesa (campo data), limitação   
  declarada no padrão das AMB-003/006, com recomendação de evolução (campo      
  data_lancamento); (2) despesa com data fora de [inicio, fim] é recusada com   
  motivo "fora do período de competência" e, coerente com AMB-005, não consome  
  cota diária. Caso de teste: d-008 (2026-04-15) recusado.                      

● Registrado.

  ▎ AMB-008 — Período de competência: fonte autoritativa e interpretação de 
  ▎ "lançada"
  ▎ Decisão: Intervalo autoritativo = [periodo.inicio, periodo.fim] (inclusive 
  ▎ em ambas as pontas). periodo.competencia é informativo; se divergir de 
  ▎ inicio/fim, prevalecem as datas explícitas.
  ▎ Limitação declarada: a política diz "lançadas" mas data_lancamento é ausente
  ▎  do schema; o sistema usa o campo data da despesa como proxy — mesma 
  ▎ filosofia das AMB-003/006.
  ▎ Recomendação de evolução: incluir campo data_lancamento para distinguir a 
  ▎ data do gasto da data do lançamento.
  ▎ Consequência: despesa com data fora de [inicio, fim] → recusada, motivo 
  ▎ "fora do período de competência", não consome cota diária.
  ▎ Caso de teste: d-008 (2026-04-15) → recusado.
  ▎ Regra afetada: RN a criar (competência).

  ---
  AMB-009 — Valores negativos (estornos)

  Texto original do RH: a política não menciona estornos.

  Item que expõe: d-009 (2026-07-11, transporte_urbano, valor -R$45,00, "Estorno
   de corrida cancelada", sem NF).

  Column 1: A
  Interpretação: Ignorar completamente — estorno não gera reembolso nem desconto
  Consequência prática: d-009 aparece na saída com valor reembolsável R$0 e
    motivo "valor negativo: estorno não processado". Cota do dia não afetada.
  ────────────────────────────────────────
  Column 1: B
  Interpretação: Deduzir da cota do dia da categoria
  Consequência prática: d-009 abate R$45 da cota de transporte de 2026-07-11 —
    sobram R$35 para outros lançamentos do mesmo dia. Mais "correto"
    contabilmente mas introduz lógica não descrita na política.
  ────────────────────────────────────────
  Column 1: C
  Interpretação: Recusar como categoria inválida de processamento (valor
  negativo
    = erro de entrada)
  Consequência prática: d-009 recusado com motivo "valor inválido: negativo".
    Mais rigoroso mas impede estornos legítimos.

  Ponto fraco que você deve verificar: a opção B é contabilmente mais precisa
  mas a política é silente sobre estornos — qualquer lógica de dedução seria
  invenção de regra não declarada pelo RH. A opção A é consistente com a
  filosofia estabelecida nas AMB anteriores (dado ausente = não inferir).

  Qual você escolhe — A, B ou C?

✻ Crunched for 14s

> A, com ajuste no motivo — o sistema não sabe que é "estorno" (isso está na    
  descrição, texto livre que não interpretamos); o que ele detecta é valor não  
  positivo. Decisão: domínio de despesa reembolsável requer valor > 0,00; itens 
   com valor <= 0 aparecem na saída com reembolso R$0 e motivo "valor não       
  positivo — fora do domínio de despesa reembolsável", sem afetar cota.         
  Limitação declarada no padrão das anteriores: a política é silente sobre      
  estornos/créditos; abater cota seria inventar regra contábil não escrita pelo 
   RH — recomendação de evolução: mecanismo explícito de ajuste/crédito         
  definido pela política. Caso de teste: d-009 (−45,00) → R$0, cota de          
  transporte de 11/07 intacta; cobre também o caso de borda valor = 0,00.       

● Registrado.

  ▎ AMB-009 — Valores não positivos
  ▎ Decisão: Domínio de despesa reembolsável exige valor > 0,00. Itens com valor
  ▎  ≤ 0 → reembolso R$0, motivo "valor não positivo — fora do domínio de 
  ▎ despesa reembolsável", não afetam cota diária.
  ▎ Justificativa: o sistema não interpreta texto livre (descricao); o que 
  ▎ detecta é o valor numérico. Abater cota seria inventar regra contábil não 
  ▎ escrita pelo RH.
  ▎ Limitação declarada: a política é silente sobre estornos/créditos.
  ▎ Recomendação de evolução: mecanismo explícito de ajuste/crédito definido 
  ▎ pela política.
  ▎ Casos de teste: d-009 (-45,00) → R$0, cota de transporte de 2026-07-11 
  ▎ intacta; valor = 0,00 → mesmo tratamento.
  ▎ Regra afetada: RN a criar (domínio de valor válido).

  ---
  AMB-010 — Arredondamento de valores com mais de 2 casas decimais

  Texto original do RH: a política não menciona arredondamento.

  Item que expõe: d-011 (R$33,333 — três casas decimais).

  Column 1: A
  Interpretação: Arredondar para 2 casas decimais, regra half-up (0,005 → sobe)
  Consequência prática: R$33,333 → R$33,33. Comportamento intuitivo e mais comum

    em sistemas financeiros brasileiros.
  ────────────────────────────────────────
  Column 1: B
  Interpretação: Arredondar para 2 casas, banker's rounding (half-even)
  Consequência prática: R$33,333 → R$33,33 (neste caso igual a A; difere em
  casos
    como R$33,335 → R$33,34 em A, R$33,34 em B também — mas R$2,225 → R$2,22 em
  B
     vs R$2,23 em A). Reduz viés acumulado em grandes volumes.
  ────────────────────────────────────────
  Column 1: C
  Interpretação: Truncar para 2 casas decimais
  Consequência prática: R$33,333 → R$33,33 (neste caso igual; difere em R$33,339

    → R$33,33 em vez de R$33,34). Sistemicamente favorece a empresa.

  Ponto fraco que você deve verificar: para d-011 as três opções produzem o
  mesmo resultado (R$33,33) — a diferença só aparece nos casos ocultos com
  dígito de arredondamento exatamente em 5. A decisão precisa estar na spec para
   que o sistema do instrutor possa conferir. O modo de arredondamento escolhido
   é regra de negócio (spec); o decimal.Decimal que o implementa é decisão
  técnica (plan).

  Qual você escolhe — A, B ou C?

✻ Sautéed for 13s

※ recap: Estamos construindo a spec do motor de reembolso, na fase de resolução de ambiguidades (10 de 16 decididas). Próxima ação: você decidir o arredondamento de valores com mais de 2 casas decimais — A (half-up), B (banker's rounding) ou C (truncar).

> A — half-up a 2 casas, padrão de sistemas financeiros brasileiros e           
  conferível de cabeça por auditor. Complemento essencial: declarar na spec     
  ONDE o arredondamento se aplica — na entrada, o valor de cada despesa é       
  normalizado para 2 casas (half-up) antes de qualquer regra; todas as          
  comparações (limites, gatilho de NF) e cálculos operam sobre o valor          
  normalizado. Como as regras adotadas são apenas comparação e subtração,       
  nenhuma operação intermediária gera casas extras — um único ponto de          
  arredondamento no fluxo. Caso de teste: d-011 (33,333) → normalizado 33,33,   
  dentro do limite diário. O half-up e o ponto de aplicação são regra de        
  negócio (spec); Decimal/ROUND_HALF_UP é implementação (plan).                 

● Registrado — e o ponto de aplicação único é uma decisão importante para a
  rastreabilidade.

  ▎ AMB-010 — Arredondamento de valores monetários
  ▎ Decisão: Half-up a 2 casas decimais. Ponto de aplicação único: o valor de 
  ▎ cada despesa é normalizado para 2 casas ao entrar no sistema, antes de 
  ▎ qualquer regra. Todas as comparações e cálculos operam sobre o valor 
  ▎ normalizado.
  ▎ Justificativa: half-up é o padrão de sistemas financeiros brasileiros e 
  ▎ conferível de cabeça por auditor. Ponto único elimina acúmulo de erro 
  ▎ intermediário.
  ▎ Caso de teste: d-011 (33,333) → normalizado R$33,33 → dentro do limite 
  ▎ diário de alimentação.
  ▎ Separação spec/plan: o half-up e o ponto de aplicação são regra de negócio 
  ▎ (spec); decimal.Decimal com ROUND_HALF_UP é implementação (plan).
  ▎ Regra afetada: RN a criar (normalização de valor).

  ---
  AMB-011 — Case sensitivity de categorias

  Texto original do RH: a política lista categorias sem definir capitalização.

  Item que expõe: d-014 (categoria "ALIMENTACAO" em maiúsculas; todos os outros
  itens usam minúsculas).

  Column 1: A
  Interpretação: Case-insensitive: normaliza para minúsculas antes de comparar
  Consequência prática: "ALIMENTACAO" → "alimentacao" → categoria reconhecida.
    d-014 processado normalmente (R$61,00, único almoço de 2026-07-31, excede
    limite → reembolsa R$60,00).
  ────────────────────────────────────────
  Column 1: B
  Interpretação: Case-sensitive: "ALIMENTACAO" não é categoria reconhecida
  Consequência prática: d-014 cai na regra 9 (categoria fora da política) →
    recusado com R$0. Rigoroso mas penaliza variação de caixa que a política não

    proíbe.

  Ponto fraco que você deve verificar: a opção B significa que qualquer variação
   de capitalização nos casos ocultos do instrutor seria recusada — o resultado
  seria conferido contra sua spec, portanto correto se declarado, mas
  potencialmente surpreendente. A opção A é consistente com a filosofia de não
  punir dados que o schema não restringiu formalmente.

  Qual você escolhe — A ou B?

✻ Worked for 13s

> A — categoria é campo de domínio fechado (enum), não texto livre; normalizar  
  caixa é tolerância de representação, não interpretação de texto (registrar    
  essa distinção na justificativa). Fronteira declarada da normalização:        
  lowercase + trim, nada além — sem normalização de acentos ou correção de      
  digitação. Após normalizar, valor fora da lista canônica (alimentacao,        
  transporte_urbano, hospedagem) cai na regra 9: recusado, motivo "categoria    
  fora da política: <valor recebido>", sem consumir cota. Casos de teste: d-014 
   (ALIMENTACAO) → reconhecida, único item do dia 31/07, R$61 → reembolsa R$60  
  e corta R$1 (exercita o corte parcial em item único); d-005 (coworking) →     
  recusado pela regra 9. E confirme: a ambiguidade "reembolsadas parcialmente"  
  da política está registrada como decisão explícita em alguma AMB? Se não,     
  registre agora: parcialmente = reembolsa até o limite, corta o excedente;     
  nunca recusa por exceder.                                                     

● Bom olho — B-2 estava na lista de candidatas mas nunca virou AMB nomeada.
  Registro os dois agora.

  ▎ AMB-011 — Case sensitivity de categorias
  ▎ Decisão: Normalização lowercase + trim antes de comparar com a lista 
  ▎ canônica (alimentacao, transporte_urbano, hospedagem). Fronteira declarada: 
  ▎ apenas caixa e espaços externos — sem normalização de acentos, correção 
  ▎ ortográfica ou similaridade.
  ▎ Justificativa: categoria é enum de domínio fechado, não texto livre; 
  ▎ normalizar caixa é tolerância de representação, não interpretação semântica.
  ▎ Após normalização: valor fora da lista canônica → regra 9, recusado, motivo 
  ▎ "categoria fora da política: <valor recebido>", não consome cota.
  ▎ Casos de teste: d-014 ("ALIMENTACAO") → normalizado "alimentacao", único 
  ▎ item de 2026-07-31, R$61,00 → reembolsa R$60,00, corta R$1,00 (exercita 
  ▎ corte em item único); d-005 ("coworking") → recusado pela regra 9.
  ▎ Regra afetada: RN a criar (normalização de categoria + regra 9).

  ---

  ▎ AMB-012 — "Reembolsadas parcialmente": o que significa parcialmente?
  ▎ Texto original do RH: "Despesas acima do limite são reembolsadas 
  ▎ parcialmente."
  ▎ Decisão: Reembolso parcial = reembolsa até o limite disponível da categoria 
  ▎ no dia, corta o excedente. Nunca recusa o item inteiro por exceder o limite.
  ▎ Justificativa: a política usa "parcialmente" — recusa total seria 
  ▎ contradição direta com o texto.
  ▎ Interação com AMB-001/002: o "limite disponível" é o saldo restante da cota 
  ▎ do dia após processar itens anteriores na ordem declarada; pode ser zero se 
  ▎ a cota já foi esgotada por item anterior.
  ▎ Caso de teste: d-001 (R$72,50, único item de alimentação no dia que chega 
  ▎ primeiro) → reembolsa R$60,00, corta R$12,50.
  ▎ Regra afetada: RN a criar (reembolso parcial por limite).

  ---
  Restam 4 candidatas não decididas: B-6 (fins de semana), T-1 (ordem de
  aplicação), T-2 (schema de saída) e A-4 (coworking — já resolvida
  implicitamente em AMB-011/regra 9, mas precisa de entrada própria?).

  Sigo para B-6 agora, ou você quer consolidar A-4 como consequência de AMB-011
  e ir direto para T-1?

✻ Brewed for 20s

> Consolide A-4 como entrada nomeada e curta, sem menu: "AMB-013 — Categoria    
  coworking (d-005): resolvida pela decisão AMB-011 — 'coworking' não pertence  
  à lista canônica; recusado pela regra 9 com motivo citando o valor recebido,  
  sem consumir cota. Registrada como entrada própria porque o caso existe nos   
  dados de exemplo e a spec não pode ser silente sobre ele." Depois siga para   
  B-6 (fim de semana), depois T-1 e T-2.                                        

● ▎ AMB-013 — Categoria coworking (d-005)
  ▎ Resolvida pela decisão AMB-011 — "coworking" não pertence à lista canônica; 
  ▎ recusado pela regra 9, motivo "categoria fora da política: coworking", sem 
  ▎ consumir cota. Registrada como entrada própria porque o caso existe nos 
  ▎ dados de exemplo e a spec não pode ser silente sobre ele.

  ---
  AMB-014 — Despesas em fim de semana ou feriado

  Texto original do RH: a política não menciona dias da semana nem feriados.

  Item que expõe: d-012 (2026-07-18, sábado, "Almoço de sábado — plantão",
  R$47,20, com NF).

  Aqui não há ambiguidade real de interpretação — a política é silente, o que em
   linguagem regulatória normalmente significa "sem restrição". Mas a spec
  precisa declarar isso explicitamente para que não pareça um buraco.

  Decisão a registrar (sem menu, confirme ou corrija):

  ▎ A política não distingue dias úteis de fins de semana ou feriados. O sistema
  ▎  aplica as mesmas regras independentemente do dia da semana. d-012 (sábado) 
  ▎ é processado como qualquer outro dia: R$47,20 dentro do limite diário de 
  ▎ alimentação (R$60), NF presente, sem outras restrições → reembolsado 
  ▎ integralmente.
  ▎ Escopo negativo (a inserir): "este sistema não aplica regras diferentes por 
  ▎ dia da semana ou feriado."

  Confirma esse registro, ou quer alterar algo?

✻ Cooked for 10s

> Confirmo, com uma adição à justificativa: criar distinção por dia da semana   
  seria inventar regra que o RH não escreveu — mesmo princípio das AMB-009      
  (estorno) e AMB-006 (viagem): o sistema não cria regra a partir de silêncio   
  da política. Registre e siga para T-1.                                        
● ▎ AMB-014 — Despesas em fim de semana ou feriado
  ▎ Decisão: O sistema aplica as mesmas regras independentemente do dia da 
  ▎ semana ou feriado. d-012 (sábado, R$47,20) → processado normalmente, 
  ▎ reembolsado integralmente.
  ▎ Justificativa: criar distinção por dia da semana seria inventar regra que o 
  ▎ RH não escreveu — mesmo princípio das AMB-006 (viagem) e AMB-009 (estorno): 
  ▎ o sistema não cria regra a partir de silêncio da política.
  ▎ Escopo negativo (a inserir): "este sistema não aplica regras diferentes por 
  ▎ dia da semana ou feriado."

  ---
  AMB-015 — Ordem de aplicação das regras

  Texto original do RH: a política lista 9 regras sem definir precedência.

  Quando múltiplas regras incidem sobre a mesma despesa, a ordem importa: uma
  despesa fora de competência com valor negativo sem NF em categoria
  desconhecida só deve gerar um motivo de recusa, e o motivo que aparece na
  saída depende de qual regra foi verificada primeiro.

  As decisões anteriores já fixaram parcialmente a ordem (AMB-005, AMB-007,
  AMB-008, AMB-009 estabelecem que recusas por NF, duplicata, competência e
  valor inválido não consomem cota). O que falta é tornar a sequência completa e
   explícita.

  Ordem proposta para confirmação ou ajuste:

  1. Normalização      → valor (half-up, 2 casas) + categoria (lowercase + trim)
  2. Domínio de valor  → valor ≤ 0 → recusa, para aqui
  3. Competência       → data fora de [inicio, fim] → recusa, para aqui
  4. Categoria         → fora da lista canônica → recusa, para aqui
  5. Duplicata         → coincidência exata com item anterior → recusa, para
  aqui
  6. Nota fiscal       → valor > 100,00 e sem NF → recusa, para aqui
  7. Limite diário     → aplica saldo da cota, reembolso parcial se necessário

  Passos 2–6 são recusas totais que interrompem o processamento do item e não
  consomem cota. Passo 7 é o único que gera reembolso parcial.

  Ponto fraco que você deve verificar: a posição da duplicata (passo 5) após
  categoria e antes de NF significa que uma duplicata de item com categoria
  inválida seria recusada como "fora da política", não como "duplicata" — o
  primeiro motivo válido encontrado vence. Isso pode ser intencional ou não.

  Confirma essa ordem, ajusta algum passo, ou quer trocar posições?

✻ Cooked for 15s

※ recap: Estamos resolvendo as ambiguidades da política de RH antes de escrever qualquer spec. Acabamos de propor a ordem de aplicação das regras (AMB-015) e aguardamos sua confirmação ou ajuste para seguir para T-2 (schema de saída).

> Confirmo a ordem 1–7, com duas declarações explícitas para fechar a AMB-015:  
  (1) política de motivo único — cada item recusado recebe exatamente um        
  motivo, o da primeira regra reprovadora na ordem declarada; regras            
  subsequentes não são avaliadas para item já recusado; (2) a verificação de    
  duplicata (passo 5) compara contra TODOS os itens anteriores na ordem do      
  arquivo, independentemente do status deles — coerente com AMB-007, duplicata  
  é fato sobre coincidência de campos, não sobre o destino do original. Caso de 
   teste adicional: dois itens idênticos > R$100 sem NF → primeiro recusado por 
   NF, segundo recusado como duplicata do primeiro. E o ponto fraco que você    
  apontou é intencional: dupla com categoria inválida → ambos recusados no      
  passo 4, coerente com motivo único. Registre e siga para T-2 (schema de       
  saída).                                                                       

● Registrado.

  ▎ AMB-015 — Ordem de aplicação das regras
  ▎ Decisão: Sequência fixa:
  ▎ 1. Normalização → valor (half-up, 2 casas) + categoria (lowercase + trim)
  ▎ 2. Domínio de valor → valor ≤ 0 → recusa, para aqui
  ▎ 3. Competência → data fora de [inicio, fim] → recusa, para aqui
  ▎ 4. Categoria → fora da lista canônica → recusa, para aqui
  ▎ 5. Duplicata → coincidência exata com qualquer item anterior na ordem do 
  ▎ arquivo (independente do status do original) → recusa, para aqui
  ▎ 6. Nota fiscal → valor > 100,00 e tem_nota_fiscal: false → recusa, para aqui
  ▎ 7. Limite diário → aplica saldo da cota; reembolso parcial se necessário
  ▎
  ▎ Política de motivo único: cada item recebe exatamente um motivo — o da 
  ▎ primeira regra reprovadora. Regras subsequentes não são avaliadas para item 
  ▎ já recusado.
  ▎ Caso de teste: dois itens idênticos com valor > 100 e sem NF → primeiro 
  ▎ recusado no passo 6 ("sem nota fiscal obrigatória"); segundo recusado no 
  ▎ passo 5 ("duplicata de d-XXX").
  ▎ Ponto intencional: dois itens idênticos com categoria inválida → ambos 
  ▎ recusados no passo 4; o segundo nunca chega ao passo 5.

  ---
  AMB-016 — Schema de saída do resultado.json

  A política não define o formato de saída — essa é uma decisão inteira de spec.
   Apresento uma proposta estruturada para você confirmar, ajustar ou rejeitar
  campo a campo.

  Proposta:

  {
    "colaborador": { "id": "c-0417", "nome": "Marina Volpi" },
    "periodo": { "competencia": "2026-07", "inicio": "2026-07-01", "fim":
  "2026-07-31" },
    "processado_em": "2026-07-29T10:00:00",
    "resumo": {
      "total_solicitado": 1900.00,
      "total_reembolsavel": 750.00,
      "total_recusado": 1150.00,
      "itens_processados": 14,
      "itens_aprovados": 8,
      "itens_parciais": 2,
      "itens_recusados": 4
    },
    "itens": [
      {
        "id": "d-001",
        "status": "aprovado",
        "valor_solicitado": 72.50,
        "valor_reembolsavel": 60.00,
        "motivo": "limite diário de alimentação atingido: R$ 60,00 disponível de
   R$ 60,00"
      }
    ]
  }

  Decisões embutidas na proposta que você precisa validar:

  Decisão: Status por item
  Opção proposta: enum: aprovado / parcial / recusado
  Alternativa: string livre
  ────────────────────────────────────────
  Decisão: Motivo
  Opção proposta: texto narrativo em português
  Alternativa: código estruturado (LIMITE_DIARIO, SEM_NF…)
  ────────────────────────────────────────
  Decisão: processado_em
  Opção proposta: timestamp ISO 8601 da execução
  Alternativa: ausente
  ────────────────────────────────────────
  Decisão: Cabeçalho
  Opção proposta: espelha entrada (colaborador + período)
  Alternativa: só os itens
  ────────────────────────────────────────
  Decisão: Resumo agregado
  Opção proposta: presente
  Alternativa: ausente
  ────────────────────────────────────────
  Decisão: valor_solicitado
  Opção proposta: valor normalizado (pós-arredondamento)
  Alternativa: valor original da entrada

  O que você quer manter, remover ou ajustar?

✻ Churned for 18s

> Auditoria da proposta — primeiro, um erro na própria proposta: o exemplo      
  mostra d-001 com status "aprovado", mas 72,50 → 60,00 é corte por limite,     
  logo "parcial" pelo seu próprio enum. Corrija o exemplo. Ajustes: (1) remover 
   processado_em — saída deve ser determinística, byte a byte igual para a      
  mesma entrada; (2) motivo em dois campos: motivo_codigo (enum: LIMITE_DIARIO, 
   SEM_NF, DUPLICATA, FORA_COMPETENCIA, CATEGORIA_INVALIDA, VALOR_NAO_POSITIVO) 
   + motivo_texto em português — código para teste, texto para auditoria        
  humana; (3) campo duplicata_de com o id do item mantido quando motivo_codigo  
  = DUPLICATA; (4) por item, valor_original (como veio na entrada) e            
  valor_considerado (normalizado a 2 casas) — a normalização da AMB-010 fica    
  visível; (5) declarar semântica do status: aprovado = integral, parcial =     
  cortado por limite (único caso do passo 7), recusado = R$0 com motivo; totais 
   do resumo derivam dos itens; (6) manter cabeçalho e resumo; (7) declarar:    
  ordem dos itens da saída = ordem da entrada; valores numéricos com 2 casas.   
  Registre a AMB-016 com o schema final e um exemplo corrigido.                 

● Erro confirmado e corrigido. Registrando AMB-016 com schema final.

  ▎ AMB-016 — Schema de saída do resultado.json
  ▎ Decisão: estrutura abaixo, com as seguintes semânticas declaradas:
  ▎ - status: enum fixo — "aprovado" (integral, valor_reembolsavel = 
  ▎ valor_considerado) · "parcial" (cortado por limite, único caso do passo 7) ·
  ▎  "recusado" (R$0,00, passos 2–6)
  ▎ - valor_original: valor como veio na entrada
  ▎ - valor_considerado: valor normalizado a 2 casas (half-up) — torna AMB-010 
  ▎ visível na saída
  ▎ - duplicata_de: id do item mantido quando motivo_codigo = "DUPLICATA"; null 
  ▎ nos demais
  ▎ - Totais do resumo derivam dos itens: total_solicitado = Σ 
  ▎ valor_considerado; total_reembolsavel = Σ valor_reembolsavel; total_recusado
  ▎  = total_solicitado − total_reembolsavel
  ▎ - Ordem dos itens na saída = ordem da entrada
  ▎ - Todos os valores numéricos com 2 casas decimais
  ▎ - processado_em removido — saída determinística, byte a byte igual para a 
  ▎ mesma entrada

  Schema final com exemplo corrigido (3 itens ilustrando os três status):

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
        "motivo_texto": "limite diário de alimentação: reembolsado R$ 60,00 de 
  R$ 72,50",
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

  ▎ Nota sobre d-011: valor_original = 33.333, valor_considerado = 33.33 — caso 
  ▎ onde os dois campos divergem, tornando a normalização auditável.
  ▎ Nota sobre motivo em item aprovado: motivo_codigo e motivo_texto são null 
  ▎ quando status = "aprovado".

  ---
  Todas as 16 ambiguidades decididas. Temos agora material suficiente para
  escrever a spec.md completa.

  Ponto fraco que você deve verificar antes de prosseguir: na AMB-015,
  motivo_codigo para item com cota esgotada por item anterior (ex.: d-002 após
  d-001 consumir R$60) é "LIMITE_DIARIO" — mas o item não foi cortado, foi
  zerado. O enum atual não distingue "cortado parcialmente" de "zerado por cota
  esgotada". Isso importa? Ou "LIMITE_DIARIO" cobre os dois casos com
  valor_reembolsavel = 0,00 e status = "parcial"?

  Aguardo sua confirmação para iniciar a redação da spec.md.

✻ Cogitated for 1m 10s

> Boa pegada — o buraco é real e a solução é dupla: (1) redefinir status como   
  derivado do valor, não da regra: aprovado = valor_reembolsavel igual a        
  valor_considerado; parcial = entre zero e o integral (exclusivos); recusado = 
   zero, qualquer que seja a regra de origem. Definição aritmética, verificável 
   só com os números do próprio item. (2) Novo código no enum: COTA_ESGOTADA —  
  distingue "havia saldo e o item foi cortado" (LIMITE_DIARIO, ex. d-001) de    
  "saldo já era zero e o item foi zerado" (COTA_ESGOTADA, ex. d-002, texto      
  citando a cota do dia consumida por itens anteriores). Consequência no        
  resumo: as contagens seguem o status derivado (d-002 conta como recusado).    
  Atualize a AMB-016 e a AMB-015 (passo 7 pode emitir LIMITE_DIARIO ou          
  COTA_ESGOTADA) e inicie a redação do spec.md completo: RF-XX derivados das    
  AMB-001 a 016, casos de borda, critérios de aceite verificáveis sem ler       
  código, schema de saída, escopo negativo consolidado e seção de ambiguidades  
  com decisão + justificativa. Me mostre o arquivo completo antes de commitar.  

● Registrando as atualizações antes de iniciar o rascunho.

  ▎ AMB-015 atualizado — passo 7: pode emitir LIMITE_DIARIO (saldo positivo, 
  ▎ item cortado) ou COTA_ESGOTADA (saldo = 0,00, item zerado). Ambos são 
  ▎ resultantes do passo 7; a distinção é necessária para auditoria.

  ▎ AMB-016 atualizado — status derivado aritmeticamente:
  ▎ - "aprovado": valor_reembolsavel = valor_considerado
  ▎ - "parcial": 0,00 < valor_reembolsavel < valor_considerado
  ▎ - "recusado": valor_reembolsavel = 0,00 — qualquer regra de origem, 
  ▎ inclusive COTA_ESGOTADA
  ▎ Enum motivo_codigo inclui COTA_ESGOTADA. Contagens do resumo derivam do 
  ▎ status aritmético.

  Escrevendo o spec.md completo agora.

  Read 1 file, ran 1 shell command (ctrl+o to expand)

● O arquivo existe com o template. Vou escrever o spec.md completo agora.

● Write(specs\001-motor-reembolso\spec.md)
  ⎿  User rejected write to specs\001-motor-reembolso\spec.md
       1 # Spec — Motor de Cálculo de Reembolso
       2 
       3 **Versão:** 1.0 · **Status:** ativo · **Última alteração:** 2026
         -07-29
       4 
       5 > **Regra de ouro deste arquivo:** ele descreve o QUÊ e o PORQUÊ
         . Nenhuma linha
       6 > aqui pode citar linguagem, biblioteca, classe, função ou estru
         tura de pasta.
       7 > Se apareceu solução, o lugar dela é o `plan.md`.
       8 >
       9 > **Teste de aceitação da própria spec:** uma pessoa que nunca v
         iu o projeto
      10 > consegue, lendo só este arquivo, verificar se o sistema está c
         orreto?
     … +590 lines

> yes                                                                           

● Write(specs\001-motor-reembolso\spec.md)
  ⎿  Added 535 lines, removed 41 lines
      1  # Spec — Motor de Cálculo de Reembolso
      2  
      3 -**Versão:** 1.0 · **Status:** rascunho · **Última alteração:** `
        -<data>`                                                         
      3 +**Versão:** 1.0 · **Status:** ativo · **Última alteração:** 2026
        +-07-29                                                          
      4  
      5  > **Regra de ouro deste arquivo:** ele descreve o QUÊ e o PORQUÊ
         . Nenhuma linha
      6  > aqui pode citar linguagem, biblioteca, classe, função ou estru
         tura de pasta.
     ...
       13  
       14  ## 1. Problema
       15  
       16 -<Duas ou três frases. Quem sofre hoje, com o quê, e por quê is
          -so custa caro.>                                               
       16 +O processo de reembolso de despesas corporativas é manual: um 
          +analista do                                                   
       17 +financeiro confere cada item contra a política de RH, decide a
          +provações e                                                   
       18 +recusas e produz uma lista justificada. O processo é lento, su
          +jeito a erro                                                  
       19 +humano e gera resultados que variam conforme o analista.      
       20  
       21  ## 2. Objetivo
       22  
       20 -<Uma frase. O que passa a ser verdade quando isto existir.>   
       23 +Dado um lote de despesas de um colaborador em um período, o si
          +stema decide                                                  
       24 +automaticamente o valor reembolsável de cada item e registra a
          + justificativa                                                
       25 +da decisão em formato auditável e reproduzível.               
       26  
       27  ## 3. Fora de escopo
       28  
       24 -<Lista explícita. Este bloco vale ponto: ele impede o agente d
          -e inventar feature                                            
       25 -e impede você de mover a trave depois.>                       
       29 +- Este sistema não consulta bases de dados externas, sistemas 
          +de RH ou                                                      
       30 +  histórico de outros períodos.                               
       31 +- Este sistema não infere status de viagem a partir de padrões
          + nas despesas                                                 
       32 +  — a regra de limites ampliados (regra 6 da política) está su
          +spensa por                                                    
       33 +  ausência de dado no schema de entrada (ver AMB-006).        
       34 +- Este sistema não extrai dados de negócio do campo `descricao
          +` (ver AMB-003,                                               
       35 +  AMB-009, AMB-011).                                          
       36 +- Este sistema não normaliza acentos, não corrige ortografia e
          + não calcula                                                  
       37 +  similaridade entre strings — apenas normaliza capitalização 
          +e espaços                                                     
       38 +  externos de campos de domínio fechado (ver AMB-011).        
       39 +- Este sistema não aplica regras diferentes por dia da semana 
          +ou feriado                                                    
       40 +  (ver AMB-014).                                              
       41 +- Este sistema não processa múltiplos colaboradores em uma úni
          +ca execução.                                                  
       42 +- Este sistema não persiste estado entre execuções; cada execu
          +ção é                                                         
       43 +  independente.                                               
       44 +- Este sistema não valida a existência do colaborador nem do c
          +entro de custo.                                               
       45 +- Este sistema não detecta duplicatas por similaridade — apena
          +s por                                                         
       46 +  coincidência exata de campos (ver AMB-007).                 
       47  
       27 -- Não faz `<...>`                                             
       28 -- Não faz `<...>`                                             
       48 +---                                                           
       49  
       50  ## 4. Entrada e saída
       51  
       32 -**Entrada:** conforme `exemplos/despesas-exemplo.json`. Campos
          - e significado:                                               
       52 +### 4.1 Entrada                                               
       53  
       54 +Formato definido por `exemplos/despesas-exemplo.json`. O schem
          +a de entrada é                                                
       55 +fixo; nenhum campo adicional será introduzido por este sistema
          +.                                                             
       56 +                                                              
       57  | Campo | Tipo | Significado | Obrigatório |
       58  |---|---|---|---|
       36 -| | | | |                                                     
       59 +| `colaborador.id` | string | Identificador do colaborador | S
          +im |                                                          
       60 +| `colaborador.nome` | string | Nome do colaborador | Sim |   
       61 +| `colaborador.centro_custo` | string | Centro de custo | Sim 
          +|                                                             
       62 +| `periodo.competencia` | string `AAAA-MM` | Identificador do 
          +período (informativo) | Sim |                                 
       63 +| `periodo.inicio` | string `AAAA-MM-DD` | Início do período a
          +utoritativo (inclusive) | Sim |                               
       64 +| `periodo.fim` | string `AAAA-MM-DD` | Fim do período autorit
          +ativo (inclusive) | Sim |                                     
       65 +| `despesas[].id` | string | Identificador único da despesa | 
          +Sim |                                                         
       66 +| `despesas[].data` | string `AAAA-MM-DD` | Data da despesa (p
          +roxy de data de lançamento) | Sim |                           
       67 +| `despesas[].categoria` | string | Categoria da despesa (domí
          +nio fechado após normalização) | Sim |                        
       68 +| `despesas[].descricao` | string | Descrição livre — não util
          +izada em regras de negócio | Sim |                            
       69 +| `despesas[].fornecedor` | string | Fornecedor | Sim |       
       70 +| `despesas[].valor` | número | Valor em reais (pode ter mais 
          +de 2 casas decimais) | Sim |                                  
       71 +| `despesas[].tem_nota_fiscal` | booleano | Se nota fiscal foi
          + apresentada | Sim |                                          
       72  
       38 -**Saída:** definida por mim. Estrutura e significado de cada c
          -ampo:                                                         
       73 +**Nota sobre `periodo.competencia` vs `inicio`/`fim`:** quando
          + divergirem,                                                  
       74 +prevalecem `inicio` e `fim` (ver AMB-008).                    
       75  
       76 +### 4.2 Saída                                                 
       77 +                                                              
       78 +Arquivo `resultado.json`, cujo schema é definido por esta spec
          +. Todos os                                                    
       79 +valores numéricos com exatamente 2 casas decimais. A ordem dos
          + itens na saída                                               
       80 +é a mesma da entrada. A saída é determinística: mesma entrada 
          +produz saída                                                  
       81 +byte a byte idêntica.                                         
       82 +                                                              
       83 +#### Schema da saída                                          
       84 +                                                              
       85  | Campo | Tipo | Significado |
       86  |---|---|---|
       42 -| | | |                                                       
       87 +| `colaborador` | objeto | Espelho do objeto `colaborador` da 
          +entrada |                                                     
       88 +| `periodo` | objeto | Espelho do objeto `periodo` da entrada 
          +|                                                             
       89 +| `resumo.total_solicitado` | número | Σ `valor_considerado` d
          +e todos os itens (itens com `valor_considerado ≤ 0` contribuem
          + com zero) |                                                  
       90 +| `resumo.total_reembolsavel` | número | Σ `valor_reembolsavel
          +` de todos os itens |                                         
       91 +| `resumo.total_recusado` | número | `total_solicitado − total
          +_reembolsavel` |                                              
       92 +| `resumo.itens_processados` | inteiro | Total de itens no lot
          +e |                                                           
       93 +| `resumo.itens_aprovados` | inteiro | Contagem de itens com `
          +status = "aprovado"` |                                        
       94 +| `resumo.itens_parciais` | inteiro | Contagem de itens com `s
          +tatus = "parcial"` |                                          
       95 +| `resumo.itens_recusados` | inteiro | Contagem de itens com `
          +status = "recusado"` |                                        
       96 +| `itens[].id` | string | Identificador da despesa, espelho da
          + entrada |                                                    
       97 +| `itens[].status` | enum | `"aprovado"` / `"parcial"` / `"rec
          +usado"` (definição aritmética em RF-13) |                     
       98 +| `itens[].valor_original` | número | Valor como veio na entra
          +da, normalizado a 2 casas |                                   
       99 +| `itens[].valor_considerado` | número | Valor após normalizaç
          +ão half-up a 2 casas (RF-01) |                                
      100 +| `itens[].valor_reembolsavel` | número | Valor a reembolsar a
          +pós todas as regras |                                         
      101 +| `itens[].motivo_codigo` | string \| null | Código do motivo 
          +(`null` quando `status = "aprovado"`) |                       
      102 +| `itens[].motivo_texto` | string \| null | Descrição legível 
          +do motivo em português (`null` quando `status = "aprovado"`) |
      103 +| `itens[].duplicata_de` | string \| null | `id` do item manti
          +do quando `motivo_codigo = "DUPLICATA"`; `null` nos demais |  
      104  
       44 -<Cole um exemplo de saída para uma entrada pequena. Vale mais 
          -que três parágrafos.>                                         
      105 +#### Enum de `motivo_codigo`                                  
      106  
       46 -## 5. Regras de negócio                                       
      107 +| Código | Passo | Quando |                                   
      108 +|---|---|---|                                                 
      109 +| `VALOR_NAO_POSITIVO` | 2 | `valor_considerado ≤ 0,00` |     
      110 +| `FORA_COMPETENCIA` | 3 | `data` fora de `[periodo.inicio, pe
          +riodo.fim]` |                                                 
      111 +| `CATEGORIA_INVALIDA` | 4 | categoria não reconhecida após no
          +rmalização |                                                  
      112 +| `DUPLICATA` | 5 | coincidência exata com item anterior na or
          +dem do arquivo |                                              
      113 +| `SEM_NF` | 6 | `valor_considerado > 100,00` e `tem_nota_fisc
          +al = false` |                                                 
      114 +| `LIMITE_DIARIO` | 7 | item cortado parcialmente (saldo dispo
          +nível > 0,00 mas < `valor_considerado`) |                     
      115 +| `COTA_ESGOTADA` | 7 | item zerado porque saldo da categoria 
          +no dia já era 0,00 |                                          
      116  
       48 -Cada regra recebe um ID (`RN-001`, ...). As tasks vão referenc
          -iar esses IDs.                                                
      117 +#### Exemplo de saída (3 itens ilustrativos)                  
      118  
       50 -### RN-001 — <nome da regra>                                  
      119 +```json                                                       
      120 +{                                                             
      121 +  "colaborador": {                                            
      122 +    "id": "c-0417",                                           
      123 +    "nome": "Marina Volpi",                                   
      124 +    "centro_custo": "CC-ENG-PLATAFORMA"                       
      125 +  },                                                          
      126 +  "periodo": {                                                
      127 +    "competencia": "2026-07",                                 
      128 +    "inicio": "2026-07-01",                                   
      129 +    "fim": "2026-07-31"                                       
      130 +  },                                                          
      131 +  "resumo": {                                                 
      132 +    "total_solicitado": 216.40,                               
      133 +    "total_reembolsavel": 114.90,                             
      134 +    "total_recusado": 101.50,                                 
      135 +    "itens_processados": 3,                                   
      136 +    "itens_aprovados": 1,                                     
      137 +    "itens_parciais": 1,                                      
      138 +    "itens_recusados": 1                                      
      139 +  },                                                          
      140 +  "itens": [                                                  
      141 +    {                                                         
      142 +      "id": "d-001",                                          
      143 +      "status": "parcial",                                    
      144 +      "valor_original": 72.50,                                
      145 +      "valor_considerado": 72.50,                             
      146 +      "valor_reembolsavel": 60.00,                            
      147 +      "motivo_codigo": "LIMITE_DIARIO",                       
      148 +      "motivo_texto": "limite diário de alimentacao: reembolsa
          +do R$ 60,00 de R$ 72,50",                                     
      149 +      "duplicata_de": null                                    
      150 +    },                                                        
      151 +    {                                                         
      152 +      "id": "d-005",                                          
      153 +      "status": "recusado",                                   
      154 +      "valor_original": 89.00,                                
      155 +      "valor_considerado": 89.00,                             
      156 +      "valor_reembolsavel": 0.00,                             
      157 +      "motivo_codigo": "CATEGORIA_INVALIDA",                  
      158 +      "motivo_texto": "categoria fora da política: coworking",
      159 +      "duplicata_de": null                                    
      160 +    },                                                        
      161 +    {                                                         
      162 +      "id": "d-006",                                          
      163 +      "status": "aprovado",                                   
      164 +      "valor_original": 54.90,                                
      165 +      "valor_considerado": 54.90,                             
      166 +      "valor_reembolsavel": 54.90,                            
      167 +      "motivo_codigo": null,                                  
      168 +      "motivo_texto": null,                                   
      169 +      "duplicata_de": null                                    
      170 +    }                                                         
      171 +  ]                                                           
      172 +}                                                             
      173 +```                                                           
      174  
       52 -**Regra:** <enunciado sem ambiguidade>                        
       53 -**Origem:** política do RH, item `<n>`                        
       54 -**Aceite:** <como verificar que está implementada — normalment
          -e um caso concreto com números>                               
      175 +---                                                           
      176  
       56 -### RN-002 — ...                                              
      177 +## 5. Requisitos funcionais                                   
      178  
      179 +### RF-01 — Normalização de valor monetário                   
      180 +                                                              
      181 +**Regra:** O valor de cada despesa é arredondado para 2 casas 
          +decimais com                                                  
      182 +regra half-up antes de qualquer outra regra ser aplicada. Toda
          +s as                                                          
      183 +comparações e cálculos subsequentes operam sobre o valor norma
          +lizado. Este é                                                
      184 +o único ponto de arredondamento no fluxo de processamento.    
      185 +                                                              
      186 +**Origem:** AMB-010; política do RH (implícito — não define ar
          +redondamento).                                                
      187 +                                                              
      188 +**Aceite:**                                                   
      189 +- Despesa com `valor = 33.333` → `valor_considerado = 33.33`  
      190 +- Despesa com `valor = 33.335` → `valor_considerado = 33.34`  
      191 +- Despesa com `valor = 72.50` → `valor_considerado = 72.50` (i
          +nalterado)                                                    
      192 +                                                              
      193  ---
      194  
       60 -## 6. Ambiguidades identificadas e decisões                   
      195 +### RF-02 — Normalização de categoria                         
      196  
       62 -> **Esta seção é o coração da spec e vale a maior parte dos 25
          - pontos do critério 1.**                                      
       63 -> Uma ambiguidade que você resolveu no código sem registrar aq
          -ui conta como                                                 
       64 -> não resolvida.                                              
      197 +**Regra:** O valor do campo `categoria` é convertido para letr
          +as minúsculas e                                               
      198 +tem espaços externos removidos (trim) antes de qualquer outra 
          +regra. Nenhuma                                                
      199 +outra transformação é aplicada: acentos não são normalizados, 
          +ortografia não                                                
      200 +é corrigida, similaridade não é calculada.                    
      201  
       66 -### AMB-001 — <o que a política deixou em aberto>             
      202 +**Origem:** AMB-011.                                          
      203  
       68 -**Texto original do RH:** "<citação literal>"                 
       69 -**O que não está claro:** <as duas ou mais leituras possíveis>
       70 -**Decisão:** <o que o sistema faz>                            
       71 -**Justificativa:** <por quê — uma linha; critério de negócio, 
          -não de conveniência técnica>                                  
       72 -**Regra afetada:** RN-00X                                     
      204 +**Aceite:**                                                   
      205 +- `"ALIMENTACAO"` → `"alimentacao"` (reconhecida)             
      206 +- `" Alimentacao "` → `"alimentacao"` (reconhecida)           
      207 +- `"Alimentação"` → `"alimentação"` (acento mantido, não recon
          +hecida → RF-05)                                               
      208  
       74 -### AMB-002 — ...                                             
      209 +---                                                           
      210  
       76 -<A política tem no mínimo oito. Se você achou menos, releia   
       77 -`exemplos/despesas-exemplo.json` — cada item daquele arquivo e
          -xiste por um motivo.>                                         
      211 +### RF-03 — Domínio de valor válido                           
      212  
      213 +**Regra:** Despesas com `valor_considerado ≤ 0,00` são recusad
          +as com                                                        
      214 +`motivo_codigo = "VALOR_NAO_POSITIVO"`. Não consomem cota diár
          +ia da categoria.                                              
      215 +                                                              
      216 +**Origem:** AMB-009; política do RH é silente sobre estornos —
          + o sistema não                                                
      217 +infere regra contábil não escrita.                            
      218 +                                                              
      219 +**Aceite:**                                                   
      220 +- `valor = -45.00` → recusada, `valor_reembolsavel = 0,00`, co
          +ta do dia intacta                                             
      221 +- `valor = 0.00` → recusada, `valor_reembolsavel = 0,00`      
      222 +- `valor = 0.01` → não afetado por esta regra                 
      223 +                                                              
      224  ---
      225  
      226 +### RF-04 — Período de competência                            
      227 +                                                              
      228 +**Regra:** Despesas com `data` fora do intervalo fechado      
      229 +`[periodo.inicio, periodo.fim]` são recusadas com             
      230 +`motivo_codigo = "FORA_COMPETENCIA"`. Não consomem cota diária
          +.                                                             
      231 +Quando `periodo.competencia` e os campos `inicio`/`fim` diverg
          +irem,                                                         
      232 +prevalecem `inicio` e `fim`.                                  
      233 +                                                              
      234 +**Limitação declarada:** a política usa o termo "lançadas", ma
          +s a data de                                                   
      235 +lançamento é ausente do schema; o sistema usa o campo `data` d
          +a despesa como                                                
      236 +proxy. Recomendação de evolução: incluir campo `data_lancament
          +o`.                                                           
      237 +                                                              
      238 +**Origem:** AMB-008; política do RH, item 7.                  
      239 +                                                              
      240 +**Aceite:**                                                   
      241 +- Período `2026-07-01` a `2026-07-31`; despesa com `data = 202
          +6-04-15` → recusada                                           
      242 +- Despesa com `data = 2026-07-01` → não afetada (limite inclus
          +ivo)                                                          
      243 +- Despesa com `data = 2026-07-31` → não afetada (limite inclus
          +ivo)                                                          
      244 +- Despesa com `data = 2026-08-01` → recusada                  
      245 +                                                              
      246 +---                                                           
      247 +                                                              
      248 +### RF-05 — Categorias válidas                                
      249 +                                                              
      250 +**Regra:** Após normalização (RF-02), categorias fora da lista
          + canônica são                                                 
      251 +recusadas com `motivo_codigo = "CATEGORIA_INVALIDA"` e        
      252 +`motivo_texto = "categoria fora da política: <valor normalizad
          +o>"`.                                                         
      253 +Não consomem cota diária.                                     
      254 +                                                              
      255 +**Lista canônica:** `alimentacao`, `transporte_urbano`, `hospe
          +dagem`.                                                       
      256 +                                                              
      257 +**Origem:** AMB-011, AMB-013; política do RH, item 9.         
      258 +                                                              
      259 +**Aceite:**                                                   
      260 +- `"coworking"` → recusada (`"categoria fora da política: cowo
          +rking"`)                                                      
      261 +- `"ALIMENTACAO"` → normalizada para `"alimentacao"` → reconhe
          +cida                                                          
      262 +- `"taxi"` → não reconhecida → recusada                       
      263 +                                                              
      264 +---                                                           
      265 +                                                              
      266 +### RF-06 — Detecção e tratamento de duplicatas               
      267 +                                                              
      268 +**Regra:** Uma despesa é duplicata quando todos os campos a se
          +guir coincidem                                                
      269 +com algum item anterior na ordem de processamento: `data`,    
      270 +`categoria` (pós-normalização), `descricao`, `fornecedor`,    
      271 +`valor_considerado`, `tem_nota_fiscal`.                       
      272 +                                                              
      273 +O item anterior é mantido; a duplicata é recusada com         
      274 +`motivo_codigo = "DUPLICATA"` e `duplicata_de = <id do item ma
          +ntido>`.                                                      
      275 +                                                              
      276 +A verificação é feita contra todos os itens anteriores indepen
          +dentemente do                                                 
      277 +status deles. Duplicatas não consomem cota diária.            
      278 +                                                              
      279 +**Limitação declarada:** o sistema detecta apenas coincidência
          + exata; campos                                                
      280 +levemente diferentes (ex.: descrições com espaço a mais) não s
          +ão detectados                                                 
      281 +como duplicata.                                               
      282 +                                                              
      283 +**Origem:** AMB-007; política do RH, item 8.                  
      284 +                                                              
      285 +**Aceite:**                                                   
      286 +- d-006 e d-007 (todos os campos iguais) → d-006 mantido, d-00
          +7 recusado com                                                
      287 +  `duplicata_de = "d-006"`                                    
      288 +- Dois itens idênticos com `valor > 100` e sem NF → primeiro r
          +ecusado por                                                   
      289 +  `SEM_NF`; segundo recusado por `DUPLICATA` (a comparação oco
          +rre mesmo que                                                 
      290 +  o original tenha sido recusado)                             
      291 +                                                              
      292 +---                                                           
      293 +                                                              
      294 +### RF-07 — Obrigatoriedade de nota fiscal                    
      295 +                                                              
      296 +**Regra:** Despesas com `valor_considerado > 100,00` e        
      297 +`tem_nota_fiscal = false` são recusadas com `motivo_codigo = "
          +SEM_NF"`.                                                     
      298 +Não consomem cota diária.                                     
      299 +                                                              
      300 +**Origem:** AMB-004, AMB-005; política do RH, item 5.         
      301 +                                                              
      302 +**Aceite:**                                                   
      303 +- `valor = 100.00`, sem NF → não afetado (limite exclusivo: 10
          +0,00 não é                                                    
      304 +  "acima de 100")                                             
      305 +- `valor = 100.01`, sem NF → recusada por `SEM_NF`            
      306 +- `valor = 150.00`, com NF → não afetado por esta regra       
      307 +- d-003 (`valor = 100.00`, sem NF) → passa; d-004 (`valor = 10
          +0.01`, sem NF)                                                
      308 +  → recusada — par de fronteira                               
      309 +                                                              
      310 +---                                                           
      311 +                                                              
      312 +### RF-08 — Limite diário de alimentação                      
      313 +                                                              
      314 +**Regra:** O total reembolsável da categoria `alimentacao` por
          + dia é limitado                                               
      315 +a R$ 60,00. O limite é aplicado sobre o agregado diário. As de
          +spesas são                                                    
      316 +processadas na ordem do arquivo de entrada; desempate por `id`
          + em ordem                                                     
      317 +lexicográfica crescente.                                      
      318 +                                                              
      319 +O saldo disponível para um item é:                            
      320 +`60,00 − Σ(valor_reembolsavel dos itens aprovados ou parciais 
          +de alimentacao                                                
      321 +no mesmo dia já processados)`.                                
      322 +                                                              
      323 +- Se `saldo > 0` e `valor_considerado > saldo`: reembolsa o sa
          +ldo disponível,                                               
      324 +  `motivo_codigo = "LIMITE_DIARIO"`.                          
      325 +- Se `saldo = 0`: reembolsa R$0,00, `motivo_codigo = "COTA_ESG
          +OTADA"`.                                                      
      326 +- Se `saldo ≥ valor_considerado`: reembolsa integralmente (sem
          + motivo de corte).                                            
      327 +                                                              
      328 +**Origem:** AMB-001, AMB-012, AMB-015; política do RH, item 1.
      329 +                                                              
      330 +**Aceite:**                                                   
      331 +- d-001 (R$72,50, primeiro de alimentação do dia 03/07) → reem
          +bolsa R$60,00                                                 
      332 +  (`LIMITE_DIARIO`)                                           
      333 +- d-002 (R$38,00, segundo do dia 03/07) → saldo = 0, reembolsa
          + R$0,00                                                       
      334 +  (`COTA_ESGOTADA`)                                           
      335 +- d-014 (`"ALIMENTACAO"`, R$61,00, único de alimentação do dia
          + 31/07) →                                                     
      336 +  reembolsa R$60,00 (`LIMITE_DIARIO`)                         
      337 +                                                              
      338 +---                                                           
      339 +                                                              
      340 +### RF-09 — Limite diário de transporte urbano                
      341 +                                                              
      342 +**Regra:** Mesma lógica de RF-08, aplicada à categoria `transp
          +orte_urbano`,                                                 
      343 +com limite de R$ 80,00 por dia.                               
      344 +                                                              
      345 +**Origem:** AMB-002, AMB-012, AMB-015; política do RH, item 2.
      346 +                                                              
      347 +**Aceite:**                                                   
      348 +- d-003 (R$100,00, primeiro de transporte no dia 06/07, NF não
          + exigida) →                                                   
      349 +  reembolsa R$80,00 (`LIMITE_DIARIO`)                         
      350 +- d-004 (R$100,01, sem NF) → recusado por `SEM_NF` no passo 6;
          + não chega ao                                                 
      351 +  cálculo de limite; cota do dia não é afetada                
      352 +                                                              
      353 +---                                                           
      354 +                                                              
      355 +### RF-10 — Limite por lançamento de hospedagem               
      356 +                                                              
      357 +**Regra:** Cada lançamento da categoria `hospedagem` é reembol
          +sado em até                                                   
      358 +R$ 250,00. Cada entrada no arquivo conta como 1 diária,       
      359 +independentemente do conteúdo do campo `descricao`. Não há acu
          +mulação diária:                                               
      360 +o limite de R$250,00 se aplica por item, não por dia.         
      361 +                                                              
      362 +**Limitação declarada:** a política diz "por diária", mas o sc
          +hema não fornece                                              
      363 +campo de quantidade de diárias. O sistema degrada "por diária"
          + para "por                                                    
      364 +lançamento" de forma consciente. O campo `descricao` não é uti
          +lizado para                                                   
      365 +extrair número de diárias (ver AMB-003). Recomendação de evolu
          +ção: incluir                                                  
      366 +campo estruturado `num_diarias` na entrada.                   
      367 +                                                              
      368 +**Justificativa na saída:** itens afetados devem ter `motivo_t
          +exto` citando                                                 
      369 +"limite de 1 diária aplicado (campo num_diarias ausente do sch
          +ema)".                                                        
      370 +                                                              
      371 +**Origem:** AMB-003; política do RH, item 3.                  
      372 +                                                              
      373 +**Aceite:**                                                   
      374 +- d-010 ("Hotel Rio - 2 diárias", R$480,00, com NF) → reembols
          +a R$250,00                                                    
      375 +  (`LIMITE_DIARIO`)                                           
      376 +- d-013 (R$690,00, sem NF) → recusado por `SEM_NF` antes de ch
          +egar ao limite                                                
      377 +  de hospedagem                                               
      378 +- Lançamento de R$200,00 com NF → reembolsa R$200,00 integralm
          +ente                                                          
      379 +                                                              
      380 +---                                                           
      381 +                                                              
      382 +### RF-11 — Ordem de aplicação das regras                     
      383 +                                                              
      384 +**Regra:** Para cada despesa, as verificações ocorrem na segui
          +nte sequência                                                 
      385 +fixa. A primeira regra reprovadora encerra o processamento do 
          +item                                                          
      386 +(**política de motivo único**): regras subsequentes não são av
          +aliadas para                                                  
      387 +item já recusado.                                             
      388 +                                                              
      389 +| Passo | Verificação | Resultado em caso de falha |          
      390 +|---|---|---|                                                 
      391 +| 1 | Normalização (RF-01, RF-02) | — (não gera recusa) |     
      392 +| 2 | Domínio de valor (RF-03) | `VALOR_NAO_POSITIVO` |       
      393 +| 3 | Competência (RF-04) | `FORA_COMPETENCIA` |              
      394 +| 4 | Categoria (RF-05) | `CATEGORIA_INVALIDA` |              
      395 +| 5 | Duplicata (RF-06) | `DUPLICATA` |                       
      396 +| 6 | Nota fiscal (RF-07) | `SEM_NF` |                        
      397 +| 7 | Limite diário (RF-08, RF-09, RF-10) | `LIMITE_DIARIO` ou
          + `COTA_ESGOTADA` |                                            
      398 +                                                              
      399 +Itens recusados nos passos 2–6 não consomem cota diária da cat
          +egoria.                                                       
      400 +O passo 7 é o único que pode gerar reembolso parcial.         
      401 +                                                              
      402 +**Origem:** AMB-015.                                          
      403 +                                                              
      404 +**Aceite:**                                                   
      405 +- Item com `data` fora de competência E sem NF → motivo `FORA_
          +COMPETENCIA`                                                  
      406 +  (passo 3 precede passo 6)                                   
      407 +- Dois itens idênticos com `valor > 100` e sem NF → primeiro: 
          +`SEM_NF`;                                                     
      408 +  segundo: `DUPLICATA` (passo 5 precede passo 6, e a comparaçã
          +o considera                                                   
      409 +  o original independentemente de seu status)                 
      410 +                                                              
      411 +---                                                           
      412 +                                                              
      413 +### RF-12 — Reembolso parcial por limite                      
      414 +                                                              
      415 +**Regra:** Quando o passo 7 é alcançado e o saldo da categoria
          + no dia é                                                     
      416 +positivo mas insuficiente para cobrir o `valor_considerado`, o
          + item é                                                       
      417 +reembolsado pelo saldo disponível. O item **nunca é recusado p
          +or exceder o                                                  
      418 +limite** — apenas cortado.                                    
      419 +                                                              
      420 +**Origem:** AMB-012; política do RH, item 4 ("reembolsadas par
          +cialmente").                                                  
      421 +                                                              
      422 +**Aceite:**                                                   
      423 +- Item de alimentação de R$72,50 como primeiro do dia →       
      424 +  reembolsado em R$60,00, não recusado                        
      425 +- Item de alimentação de R$30,00 como primeiro do dia →       
      426 +  reembolsado em R$30,00 integralmente                        
      427 +                                                              
      428 +---                                                           
      429 +                                                              
      430 +### RF-13 — Definição de status por item                      
      431 +                                                              
      432 +**Regra:** O `status` é derivado aritmeticamente dos valores d
          +o próprio item,                                               
      433 +independentemente do `motivo_codigo`:                         
      434 +                                                              
      435 +- `"aprovado"`: `valor_reembolsavel = valor_considerado`      
      436 +- `"parcial"`: `0,00 < valor_reembolsavel < valor_considerado`
      437 +- `"recusado"`: `valor_reembolsavel = 0,00`                   
      438 +                                                              
      439 +**Origem:** AMB-016.                                          
      440 +                                                              
      441 +**Aceite:**                                                   
      442 +- Item com `COTA_ESGOTADA` → `valor_reembolsavel = 0,00` → `st
          +atus = "recusado"`                                            
      443 +- Item com `LIMITE_DIARIO` e `valor_reembolsavel > 0` → `statu
          +s = "parcial"`                                                
      444 +- Item com `SEM_NF` → `valor_reembolsavel = 0,00` → `status = 
          +"recusado"`                                                   
      445 +- Item reembolsado integralmente → `status = "aprovado"`, `mot
          +ivo_codigo = null`                                            
      446 +                                                              
      447 +---                                                           
      448 +                                                              
      449 +### RF-14 — Schema e determinismo da saída                    
      450 +                                                              
      451 +**Regra:** O arquivo de saída segue o schema da seção 4.2. Tod
          +os os valores                                                 
      452 +numéricos com exatamente 2 casas decimais. Ordem dos itens = o
          +rdem da entrada.                                              
      453 +Execuções com a mesma entrada produzem saída byte a byte idênt
          +ica (sem                                                      
      454 +timestamps nem dados voláteis).                               
      455 +                                                              
      456 +**Origem:** AMB-016.                                          
      457 +                                                              
      458 +---                                                           
      459 +                                                              
      460 +### RF-15 — Dias da semana sem distinção                      
      461 +                                                              
      462 +**Regra:** O sistema aplica as mesmas regras independentemente
          + do dia da semana                                             
      463 +ou feriado. Despesas de sábado, domingo e feriados seguem o me
          +smo                                                           
      464 +processamento dos dias úteis.                                 
      465 +                                                              
      466 +**Origem:** AMB-014; política do RH é silente — criar distinçã
          +o seria inventar                                              
      467 +regra não escrita pelo RH.                                    
      468 +                                                              
      469 +**Aceite:**                                                   
      470 +- d-012 (sábado, R$47,20) → processado normalmente, reembolsad
          +o integralmente                                               
      471 +                                                              
      472 +---                                                           
      473 +                                                              
      474 +### RF-16 — Regra de viagem suspensa                          
      475 +                                                              
      476 +**Regra:** A regra 6 da política de RH ("colaborador em viagem
          + tem limites                                                  
      477 +ampliados em 50%") está suspensa nesta versão. Nenhum item rec
          +ebe limites                                                   
      478 +ampliados. Os limites aplicados são sempre os valores base:   
      479 +alimentação R$60,00, transporte R$80,00, hospedagem R$250,00. 
      480 +                                                              
      481 +**Limitação declarada:** "em viagem" é fato administrativo que
          + só o RH pode                                                 
      482 +declarar; o schema de entrada não fornece esse dado; inferir p
          +or heurística                                                 
      483 +seria criar regra não escrita. Recomendação de evolução: campo
          + estruturado de                                               
      484 +viagem na entrada (ex.: booleano ou lista de períodos de viage
          +m).                                                           
      485 +                                                              
      486 +**Origem:** AMB-006; política do RH, item 6.                  
      487 +                                                              
      488 +**Aceite:** nenhum item do lote de exemplo aciona ampliação; i
          +tens de                                                       
      489 +hospedagem não alteram os limites de outras categorias.       
      490 +                                                              
      491 +---                                                           
      492 +                                                              
      493 +## 6. Ambiguidades identificadas e decisões                   
      494 +                                                              
      495 +> Esta seção é o coração da spec. Uma ambiguidade resolvida no
          + código sem                                                   
      496 +> registro aqui conta como não resolvida.                     
      497 +                                                              
      498 +| ID | Texto original do RH | O que não estava claro | Decisão
          + | Justificativa |                                            
      499 +|---|---|---|---|---|                                         
      500 +| AMB-001 | "Alimentação tem limite de R$ 60 por dia." | Limit
          +e por despesa ou pelo agregado diário? | Agregado diário; cort
          +e na ordem do arquivo, desempate por `id` | "por dia" indica a
          +cumulação; ordem de chegada é determinística e auditável — ver
          + RF-08 |                                                      
      501 +| AMB-002 | "Transporte urbano tem limite de R$ 80 por dia." |
          + Mesma questão de AMB-001 | Mesma lógica da AMB-001 — agregado
          + diário, ordem do arquivo | Redação idêntica à de alimentação;
          + filosofias diferentes entre categorias criariam inconsistênci
          +a — ver RF-09 |                                               
      502 +| AMB-003 | "Hospedagem tem limite de R$ 250 por diária." | Sc
          +hema não tem campo `num_diarias`; como aplicar limite "por diá
          +ria"? | Cada lançamento = 1 diária; descrição ignorada | Regra
          + de negócio não pode depender de parsing de texto livre — ver 
          +RF-10 |                                                       
      503 +| AMB-004 | "Nota fiscal é obrigatória acima de R$ 100." | R$ 
          +100,00 exato exige NF? | Não exige; gatilho é `valor > 100,00`
          + (exclusivo) | "Acima de" em leitura literal é exclusivo; "a p
          +artir de" seria inclusivo — ver RF-07 |                       
      504 +| AMB-005 | "Nota fiscal é obrigatória acima de R$ 100." | O q
          +ue acontece quando NF é obrigatória mas ausente? | Recusa tota
          +l; não consome cota | NF é requisito de compliance; sem compro
          +vante não há justificativa contábil — ver RF-07 |             
      505 +| AMB-006 | "Colaborador em viagem tem limites ampliados em 50
          +%." | Schema não tem campo de status de viagem | Regra suspens
          +a; nenhum item recebe limites ampliados | "Em viagem" é fato a
          +dministrativo; inferir por heurística seria criar regra não es
          +crita — ver RF-16 |                                           
      506 +| AMB-007 | "Duplicatas devem ser tratadas." | O que define du
          +plicata? O que "tratar" significa? | Coincidência exata de tod
          +os os campos exceto `id`; mantém o primeiro, recusa os demais 
          +| Coincidência exata é determinística e auditável; similaridad
          +e dependeria de interpretação de texto — ver RF-06 |          
      507 +| AMB-008 | "Despesas devem ser lançadas dentro do período de 
          +competência." | `periodo.competencia` ou `periodo.inicio/fim`?
          + "Lançadas" = data da despesa? | `inicio`/`fim` são autoritati
          +vos; `competencia` é informativo; `data` da despesa como proxy
          + de lançamento | `inicio`/`fim` são datas concretas; `data_lan
          +camento` é ausente do schema — ver RF-04 |                    
      508 +| AMB-009 | (silêncio da política sobre estornos) | Como trata
          +r valor negativo (d-009, -R$45,00)? | Valor `≤ 0` recusado com
          +o fora do domínio; não afeta cota | O sistema detecta valor nã
          +o positivo, não "estorno"; criar lógica de abatimento seria in
          +ventar regra não escrita — ver RF-03 |                        
      509 +| AMB-010 | (silêncio da política sobre arredondamento) | Como
          + tratar valor com mais de 2 casas (d-011: 33,333)? | Half-up a
          + 2 casas; ponto único no início do fluxo | Half-up é o padrão 
          +de sistemas financeiros brasileiros e conferível manualmente —
          + ver RF-01 |                                                  
      510 +| AMB-011 | (categorias listadas na política sem definir capit
          +alização) | `"ALIMENTACAO"` é reconhecida? | Case-insensitive 
          ++ trim; categoria é enum, não texto livre | Normalizar caixa é
          + tolerância de representação, não interpretação semântica — ve
          +r RF-02, RF-05 |                                              
      511 +| AMB-012 | "Despesas acima do limite são reembolsadas parcial
          +mente." | "Parcialmente" = corta o excedente ou recusa o item?
          + | Reembolsa até o saldo disponível; nunca recusa por exceder 
          +limite | A palavra "parcialmente" na política contradiz recusa
          + total — ver RF-12 |                                          
      512 +| AMB-013 | "Categorias fora da política não são reembolsáveis
          +." | Como tratar `coworking` (d-005)? | Recusado por `CATEGORI
          +A_INVALIDA`; consequência direta de AMB-011 | Não pertence à l
          +ista canônica; registrada como entrada própria porque o caso e
          +xiste nos dados — ver RF-05 |                                 
      513 +| AMB-014 | (silêncio da política sobre dias da semana) | Desp
          +esa de sábado (d-012) é tratada diferente? | Mesmas regras par
          +a qualquer dia da semana ou feriado | Criar distinção seria in
          +ventar regra não escrita pelo RH — ver RF-15 |                
      514 +| AMB-015 | (ausência de ordem de precedência entre as 9 regra
          +s da política) | Qual regra vence quando múltiplas incidem? | 
          +Sequência fixa de 7 passos; política de motivo único | Ordem d
          +eclarada é necessária para resultado determinístico e auditáve
          +l — ver RF-11 |                                               
      515 +| AMB-016 | (política não define formato de saída) | Qual o sc
          +hema, o enum de status e o enum de motivos? | Schema da seção 
          +4.2; status derivado aritmeticamente; 7 códigos de motivo | St
          +atus aritmético é verificável sem conhecer a regra de origem; 
          +códigos estruturados permitem teste automático — ver RF-13, RF
          +-14 |                                                         
      516 +                                                              
      517 +---                                                           
      518 +                                                              
      519  ## 7. Casos de borda
      520  
       83 -| Caso | Entrada | Comportamento esperado | Regra |           
      521 +| Caso | Item de referência | Comportamento esperado | Regra |
      522  |---|---|---|---|
       85 -| | | | |                                                     
      523 +| Dois itens de alimentação no mesmo dia | d-001 + d-002 (03/0
          +7) | d-001: parcial R$60,00 (`LIMITE_DIARIO`); d-002: recusado
          + R$0,00 (`COTA_ESGOTADA`) | RF-08 |                           
      524 +| Fronteira inferior de NF: valor exato R$100,00 | d-003 | NF 
          +não exigida; item entra no cálculo de limite normalmente | RF-
          +07 |                                                          
      525 +| Fronteira superior de NF: R$100,01 | d-004 | Recusado `SEM_N
          +F`; não consome cota de transporte do dia | RF-07 |           
      526 +| Categoria fora da política | d-005 (`coworking`) | Recusado 
          +`CATEGORIA_INVALIDA` | RF-05 |                                
      527 +| Duplicata exata | d-006 + d-007 | d-006 aprovado; d-007 recu
          +sado `DUPLICATA` de d-006 | RF-06 |                           
      528 +| Data fora de competência | d-008 (2026-04-15) | Recusado `FO
          +RA_COMPETENCIA` | RF-04 |                                     
      529 +| Valor negativo | d-009 (-R$45,00) | Recusado `VALOR_NAO_POSI
          +TIVO`; cota de transporte de 11/07 intacta | RF-03 |          
      530 +| Hospedagem multi-diária na descrição | d-010 ("2 diárias", R
          +$480,00) | Trata como 1 diária; reembolsa R$250,00 (`LIMITE_DI
          +ARIO`) | RF-10 |                                              
      531 +| Valor com 3 casas decimais | d-011 (33,333) | `valor_conside
          +rado = 33,33`; aprovado (dentro do limite diário) | RF-01 |   
      532 +| Despesa de sábado | d-012 (18/07) | Processada normalmente; 
          +aprovado R$47,20 | RF-15 |                                    
      533 +| Hospedagem sem NF acima de R$100 | d-013 (R$690,00, sem NF) 
          +| Recusado `SEM_NF`; limite de hospedagem nunca é avaliado | R
          +F-07, RF-10 |                                                 
      534 +| Categoria em maiúsculas | d-014 (`"ALIMENTACAO"`, R$61,00) |
          + Normalizada; corte para R$60,00 (`LIMITE_DIARIO`) | RF-02, RF
          +-08 |                                                         
      535 +| Dois idênticos com valor > R$100 e sem NF | hipotético | Pri
          +meiro: `SEM_NF`; segundo: `DUPLICATA` (do primeiro) | RF-06, R
          +F-07, RF-11 |                                                 
      536 +| Valor zero | hipotético | Recusado `VALOR_NAO_POSITIVO` | RF
          +-03 |                                                         
      537 +| Cota esgotada por item anterior | d-002 (depois de d-001) | 
          +`COTA_ESGOTADA`, R$0,00, `status = "recusado"` | RF-08, RF-13 
          +|                                                             
      538  
      539 +---                                                           
      540 +                                                              
      541  ## 8. Ordem de aplicação das regras
      542  
       89 -<Quando duas regras incidem sobre a mesma despesa, qual vale p
          -rimeiro? A ordem                                              
       90 -muda o resultado. Declarar isso separa spec boa de spec média.
          ->                                                             
      543 +Declarada em RF-11. Resumo:                                   
      544  
      545 +```                                                           
      546 +1. Normalização   (valor half-up 2 casas + categoria lowercase
          ++trim)                                                        
      547 +2. Domínio valor  →  valor_considerado ≤ 0   →  VALOR_NAO_POSI
          +TIVO                                                          
      548 +3. Competência    →  data fora de período     →  FORA_COMPETEN
          +CIA                                                           
      549 +4. Categoria      →  fora da lista canônica   →  CATEGORIA_INV
          +ALIDA                                                         
      550 +5. Duplicata      →  coincidência exata        →  DUPLICATA   
      551 +6. Nota fiscal    →  valor > 100 sem NF        →  SEM_NF      
      552 +7. Limite diário  →  aplica saldo da cota      →  LIMITE_DIARI
          +O ou COTA_ESGOTADA                                            
      553 +```                                                           
      554 +                                                              
      555 +Passos 2–6: recusa total, sem consumo de cota, motivo único.  
      556 +Passo 7: único que gera reembolso parcial (`status = "parcial"
          +`) ou zera por                                                
      557 +cota esgotada (`status = "recusado"`, `motivo_codigo = "COTA_E
          +SGOTADA"`).                                                   
      558 +                                                              
      559 +---                                                           
      560 +                                                              
      561  ## 9. Critérios de aceite
      562  
       94 -O sistema está pronto quando:                                 
      563 +O sistema está pronto quando, processando `exemplos/despesas-e
          +xemplo.json`:                                                 
      564  
       96 -- [ ] <critério verificável, sem ler código>                  
       97 -- [ ] <...>                                                   
      565 +- [ ] d-001 → `status: "parcial"`, `valor_reembolsavel: 60.00`
          +, `motivo_codigo: "LIMITE_DIARIO"`                            
      566 +- [ ] d-002 → `status: "recusado"`, `valor_reembolsavel: 0.00`
          +, `motivo_codigo: "COTA_ESGOTADA"`                            
      567 +- [ ] d-003 → `status: "parcial"`, `valor_reembolsavel: 80.00`
          +, `motivo_codigo: "LIMITE_DIARIO"` (NF não exigida para R$100,
          +00 exato)                                                     
      568 +- [ ] d-004 → `status: "recusado"`, `motivo_codigo: "SEM_NF"`;
          + cota de transporte de 06/07 não afetada                      
      569 +- [ ] d-005 → `status: "recusado"`, `motivo_codigo: "CATEGORIA
          +_INVALIDA"`, `motivo_texto` contém `"coworking"`              
      570 +- [ ] d-006 → `status: "aprovado"`, `valor_reembolsavel: 54.90
          +`                                                             
      571 +- [ ] d-007 → `status: "recusado"`, `motivo_codigo: "DUPLICATA
          +"`, `duplicata_de: "d-006"`                                   
      572 +- [ ] d-008 → `status: "recusado"`, `motivo_codigo: "FORA_COMP
          +ETENCIA"`                                                     
      573 +- [ ] d-009 → `status: "recusado"`, `motivo_codigo: "VALOR_NAO
          +_POSITIVO"`; cota de transporte de 11/07 não afetada          
      574 +- [ ] d-010 → `status: "parcial"`, `valor_reembolsavel: 250.00
          +`, `motivo_codigo: "LIMITE_DIARIO"`, `motivo_texto` cita "limi
          +te de 1 diária aplicado"                                      
      575 +- [ ] d-011 → `valor_considerado: 33.33`; `status: "aprovado"`
          +, `valor_reembolsavel: 33.33`                                 
      576 +- [ ] d-012 → `status: "aprovado"`, `valor_reembolsavel: 47.20
          +`                                                             
      577 +- [ ] d-013 → `status: "recusado"`, `motivo_codigo: "SEM_NF"` 
      578 +- [ ] d-014 → `valor_considerado: 61.00`; `status: "parcial"`,
          + `valor_reembolsavel: 60.00`, `motivo_codigo: "LIMITE_DIARIO"`
      579 +- [ ] Executar duas vezes com a mesma entrada produz arquivos 
          +de saída byte a byte idênticos                                
      580 +- [ ] Nenhum item recebe `valor_reembolsavel` maior que o limi
          +te da categoria (60,00 / 80,00 / 250,00)                      
      581 +- [ ] Nenhum item recebe limites ampliados de viagem          
      582  
      583 +---                                                           
      584 +                                                              
      585  ## 10. O que fica em aberto
      586  
      101 -<Perguntas que você não conseguiu responder e a decisão provis
          -ória que tomou.                                               
      102 -Honestidade aqui vale ponto — spec que finge não ter buraco é 
          -spec que esconde buraco.>                                     
      587 +**Ponto aberto — `total_solicitado` e itens com valor não posi
          +tivo:** itens                                                 
      588 +com `valor_considerado ≤ 0` contribuem com zero para `total_so
          +licitado`                                                     
      589 +(não reduzem o total). Decisão provisória adotada por clareza 
          +de auditoria;                                                 
      590 +se o instrutor apresentar caso de teste que exija comportament
          +o diferente,                                                  
      591 +atualizar via `DECISIONS.md`.                                 
      592 +                                                              
      593 +**Ponto aberto — `valor_original` vs `valor_considerado`:** ne
          +sta versão os                                                 
      594 +dois campos são sempre iguais (ambos normalizados a 2 casas). 
          +O campo                                                       
      595 +`valor_original` foi mantido para auditabilidade futura, quand
          +o a entrada                                                   
      596 +puder preservar o valor bruto antes da normalização.          

● spec.md escrito. Aqui estão os pontos fracos que você deve verificar antes de
  aprovar:

  1. d-003 no critério de aceite: declarei status: "parcial",
  valor_reembolsavel: 80.00 — confirme que está de acordo com a decisão (NF não
  exigida para R$100,00 exato, entra no passo 7, corte para R$80 de limite de
  transporte).
  2. valor_original redundante: na seção 10 declarei o ponto em aberto. Se
  quiser remover o campo agora para simplificar, basta dizer — é mais fácil
  antes de escrever o plan.
  3. Tabela de AMB-015 na seção 6: a decisão está resumida como uma linha — se
  quiser que o texto da justificativa seja mais explícito no lugar em que a
  rubrica vai olhar primeiro, posso expandir.
  4. total_solicitado para d-009: a definição adotada (itens com valor ≤ 0
  contribuem com zero) está declarada na seção 10 como ponto em aberto. Se
  preferir decisão fechada agora, defina e registro.

  Aguardando sua revisão para prosseguir com o plan.md. Lembre também de rodar
  /export ao final desta sessão para salvar em docs/sessions/.

✻ Baked for 3m 14s

※ recap: Estamos construindo a spec do motor de reembolso no desafio SDD. A spec.md está escrita e aguarda sua revisão antes de seguir para o plan.md.

> Revisão da spec — aprovo com 4 ajustes antes do commit:                       
                                                                                
  1. valor_original: a spec contradiz a decisão da AMB-016. Decidimos que       
  valor_original ecoa a entrada COMO VEIO (ex.: 33.333) e valor_considerado é o 
   normalizado (33.33) — é isso que torna a AMB-010 auditável na saída, e você  
  mesmo registrou "caso onde os dois campos divergem". Corrija: (a) tabela do   
  schema: valor_original = "valor exatamente como veio na entrada, sem          
  normalização"; (b) regra dos 2 casas na seção 4.2 e no RF-14 ganha a exceção  
  declarada: "todos os valores numéricos com 2 casas, exceto valor_original,    
  que ecoa o valor da entrada"; (c) novo aceite no RF-01 e no checklist da      
  seção 9: d-011 → valor_original: 33.333, valor_considerado: 33.33; (d)        
  remover o segundo parágrafo da seção 10.                                      
                                                                                
  2. d-003: confirmado como está (parcial, 80.00, LIMITE_DIARIO).               
                                                                                
  3. Tabela da seção 6: manter como está, sem expandir.                         
                                                                                
  4. total_solicitado: promover a decisão a definitiva — itens com              
  valor_considerado ≤ 0 contribuem com zero para total_solicitado (não reduzem  
  o total), justificativa: totais de auditoria não devem ser distorcidos por    
  itens fora do domínio. Mover da seção 10 para a definição do resumo na 4.2; a 
   seção 10 deixa de existir se ficar vazia.                                    
                                                                                
  Depois dos ajustes, me mostre só o diff das mudanças e sugira o commit.       

● Fazendo os 4 ajustes agora.

● Update(specs\001-motor-reembolso\spec.md)
  ⎿  Added 1 line, removed 1 line
      86  |---|---|---|
      87  | `colaborador` | objeto | Espelho do objeto `colaborador` da e
          ntrada |
      88  | `periodo` | objeto | Espelho do objeto `periodo` da entrada |
      89 -| `resumo.total_solicitado` | número | Σ `valor_considerado` de
         - todos os itens (itens com `valor_considerado ≤ 0` contribuem c
         -om zero) |                                                     
      89 +| `resumo.total_solicitado` | número | Σ `valor_considerado` do
         +s itens com `valor_considerado > 0`; itens com `valor_considera
         +do ≤ 0` contribuem com zero — totais de auditoria não devem ser
         + distorcidos por itens fora do domínio |                       
      90  | `resumo.total_reembolsavel` | número | Σ `valor_reembolsavel`
           de todos os itens |
      91  | `resumo.total_recusado` | número | `total_solicitado − total_
          reembolsavel` |
      92  | `resumo.itens_processados` | inteiro | Total de itens no lote
           |

● Update(specs\001-motor-reembolso\spec.md)
  ⎿  Added 1 line, removed 1 line
       95  | `resumo.itens_recusados` | inteiro | Contagem de itens com `
           status = "recusado"` |
       96  | `itens[].id` | string | Identificador da despesa, espelho da
            entrada |
       97  | `itens[].status` | enum | `"aprovado"` / `"parcial"` / `"rec
           usado"` (definição aritmética em RF-13) |
       98 -| `itens[].valor_original` | número | Valor como veio na entra
          -da, normalizado a 2 casas |                                   
       98 +| `itens[].valor_original` | número | Valor exatamente como ve
          +io na entrada, sem normalização |                             
       99  | `itens[].valor_considerado` | número | Valor após normalizaç
           ão half-up a 2 casas (RF-01) |
      100  | `itens[].valor_reembolsavel` | número | Valor a reembolsar a
           pós todas as regras |
      101  | `itens[].motivo_codigo` | string \| null | Código do motivo 
           (`null` quando `status = "aprovado"`) |

● Update(specs\001-motor-reembolso\spec.md)
  ⎿  Added 2 lines, removed 1 line
      76  ### 4.2 Saída
      77  
      78  Arquivo `resultado.json`, cujo schema é definido por esta spec.
           Todos os
      79 -valores numéricos com exatamente 2 casas decimais. A ordem dos 
         -itens na saída                                                 
      79 +valores numéricos com exatamente 2 casas decimais, **exceto `va
         +lor_original`,                                                 
      80 +que ecoa o valor da entrada sem normalização**. A ordem dos ite
         +ns na saída                                                    
      81  é a mesma da entrada. A saída é determinística: mesma entrada p
          roduz saída
      82  byte a byte idêntica.
      83  

● Update(specs\001-motor-reembolso\spec.md)
  ⎿  Added 4 lines, removed 3 lines
      187  **Origem:** AMB-010; política do RH (implícito — não define ar
           redondamento).
      188  
      189  **Aceite:**
      190 -- Despesa com `valor = 33.333` → `valor_considerado = 33.33`  
      191 -- Despesa com `valor = 33.335` → `valor_considerado = 33.34`  
      192 -- Despesa com `valor = 72.50` → `valor_considerado = 72.50` (i
          -nalterado)                                                    
      190 +- Despesa com `valor = 33.333` → `valor_original = 33.333`, `v
          +alor_considerado = 33.33`                                     
      191 +- Despesa com `valor = 33.335` → `valor_original = 33.335`, `v
          +alor_considerado = 33.34`                                     
      192 +- Despesa com `valor = 72.50` → `valor_original = 72.50`, `val
          +or_considerado = 72.50` (inalterado)                          
      193 +- d-011 (`valor = 33.333`) → `valor_original: 33.333`, `valor_
          +considerado: 33.33` — divergência visível na saída            
      194  
      195  ---
      196  

● Update(specs\001-motor-reembolso\spec.md)
  ⎿  Added 2 lines, removed 1 line
      451  ### RF-14 — Schema e determinismo da saída
      452  
      453  **Regra:** O arquivo de saída segue o schema da seção 4.2. Tod
           os os valores
      454 -numéricos com exatamente 2 casas decimais. Ordem dos itens = o
          -rdem da entrada.                                              
      454 +numéricos com exatamente 2 casas decimais, exceto `valor_origi
          +nal`, que ecoa                                                
      455 +o valor da entrada sem normalização. Ordem dos itens = ordem d
          +a entrada.                                                    
      456  Execuções com a mesma entrada produzem saída byte a byte idênt
           ica (sem
      457  timestamps nem dados voláteis).
      458  

● Update(specs\001-motor-reembolso\spec.md)  ⎿  Added 1 line, removed 1 line
      575  - [ ] d-008 → `status: "recusado"`, `motivo_codigo: "FORA_COMP
           ETENCIA"`
      576  - [ ] d-009 → `status: "recusado"`, `motivo_codigo: "VALOR_NAO
           _POSITIVO"`; cota de transporte de 11/07 não afetada
      577  - [ ] d-010 → `status: "parcial"`, `valor_reembolsavel: 250.00
           `, `motivo_codigo: "LIMITE_DIARIO"`, `motivo_texto` cita "limi
           te de 1 diária aplicado"
      578 -- [ ] d-011 → `valor_considerado: 33.33`; `status: "aprovado"`
          -, `valor_reembolsavel: 33.33`                                 
      578 +- [ ] d-011 → `valor_original: 33.333`, `valor_considerado: 33
          +.33`; `status: "aprovado"`, `valor_reembolsavel: 33.33`       
      579  - [ ] d-012 → `status: "aprovado"`, `valor_reembolsavel: 47.20
           `
      580  - [ ] d-013 → `status: "recusado"`, `motivo_codigo: "SEM_NF"`
      581  - [ ] d-014 → `valor_considerado: 61.00`; `status: "parcial"`,
            `valor_reembolsavel: 60.00`, `motivo_codigo: "LIMITE_DIARIO"`

● Update(specs\001-motor-reembolso\spec.md)
  ⎿  Removed 14 lines
      583  - [ ] Nenhum item recebe `valor_reembolsavel` maior que o limi
           te da categoria (60,00 / 80,00 / 250,00)
      584  - [ ] Nenhum item recebe limites ampliados de viagem
      585  
      586 ----                                                           
      587 -                                                              
      588 -## 10. O que fica em aberto                                   
      589 -                                                              
      590 -**Ponto aberto — `total_solicitado` e itens com valor não posi
          -tivo:** itens                                                 
      591 -com `valor_considerado ≤ 0` contribuem com zero para `total_so
          -licitado`                                                     
      592 -(não reduzem o total). Decisão provisória adotada por clareza 
          -de auditoria;                                                 
      593 -se o instrutor apresentar caso de teste que exija comportament
          -o diferente,                                                  
      594 -atualizar via `DECISIONS.md`.                                 
      595 -                                                              
      596 -**Ponto aberto — `valor_original` vs `valor_considerado`:** ne
          -sta versão os                                                 
      597 -dois campos são sempre iguais (ambos normalizados a 2 casas). 
          -O campo                                                       
      598 -`valor_original` foi mantido para auditabilidade futura, quand
          -o a entrada                                                   
      599 -puder preservar o valor bruto antes da normalização.          

● Diff das mudanças:

  Ran 1 shell command (ctrl+o to expand)

● O diff inclui o arquivo inteiro (escrito do zero vs. template). Resumindo
  apenas as mudanças dos 4 ajustes desta revisão:

  # Ajuste 1a — valor_original sem normalização
  - | `itens[].valor_original` | número | Valor como veio na entrada, 
  normalizado a 2 casas |
  + | `itens[].valor_original` | número | Valor exatamente como veio na entrada,
   sem normalização |

  # Ajuste 1b — exceção na regra de 2 casas (seção 4.2 e RF-14)
  - Todos os valores numéricos com exatamente 2 casas decimais.
  + Todos os valores numéricos com exatamente 2 casas decimais, **exceto
  + `valor_original`, que ecoa o valor da entrada sem normalização**.

  # Ajuste 1c — aceite RF-01 e checklist seção 9
  + - d-011 (`valor = 33.333`) → `valor_original: 33.333`, `valor_considerado: 
  33.33`
  - - [ ] d-011 → `valor_considerado: 33.33`; status aprovado, 33.33
  + - [ ] d-011 → `valor_original: 33.333`, `valor_considerado: 33.33`; status 
  aprovado, 33.33

  # Ajuste 1d — parágrafo redundante da seção 10 removido
  # Ajuste 4 — total_solicitado promovido a decisão definitiva na tabela 4.2
  - Σ `valor_considerado` de todos os itens (itens com ≤ 0 contribuem com zero)
  + Σ `valor_considerado` dos itens com `valor_considerado > 0`; itens com
  + `valor_considerado ≤ 0` contribuem com zero — totais de auditoria não devem
  + ser distorcidos por itens fora do domínio

  # Seção 10 removida (ficou vazia após ajuste 4 e 1d)

  ---
  Mensagem de commit sugerida:

  docs(spec): spec.md v1.0 — 16 ambiguidades resolvidas, schema de saída
  definido

  Posso rodar o commit agora, ou você quer revisar o arquivo completo antes?

✻ Baked for 1m 11s

> Pode commitar com essa mensagem.                                              

  Committed dce072 (ctrl+o to expand)

● Commitado. dce0728 — docs(spec): spec.md v1.0.

  Próximo passo: plan.md. A stack já está fixada no CLAUDE.md (Python 3, pytest,
   argparse, decimal.Decimal) — o plan.md documenta as decisões técnicas, a
  arquitetura em blocos, o modelo de dados e a estratégia de testes.

  Posso iniciar o rascunho do plan.md agora, ou quer fazer uma pausa primeiro?

✻ Churned for 7s

> Inicie o plan.md: stack Python 3 + pytest + argparse + decimal.Decimal, cada  
  escolha com a alternativa descartada e o motivo; arquitetura em blocos        
  (leitura/validação da entrada → pipeline de regras na ordem do RF-11 →        
  cálculo de cotas por dia/categoria → serialização determinística da saída);   
  modelo de dados; decisões técnicas; estratégia de testes (um teste por aceite 
   dos RFs, nomeados test_rfXX_descricao, mais os casos de borda da seção 7).   
  Me mostre o arquivo completo antes de commitar.                               

  Read 1 file (ctrl+o to expand)

● Write(specs\001-motor-reembolso\plan.md)
  ⎿  Added 290 lines, removed 30 lines
      1  # Plano Técnico — Motor de Cálculo de Reembolso
      2  
      3 -**Versão:** 1.0 · **Baseado na spec:** 1.0                      
      3 +**Versão:** 1.0 · **Baseado na spec:** 1.0 · **Última alteração:
        +** 2026-07-29                                                   
      4  
      5  > Aqui mora o COMO. Este arquivo pode e deve falar de linguagem,
          biblioteca e
      6  > arquitetura. O que ele **não** pode é introduzir regra de negó
         cio nova — se
     ...
       12  
       13  | Escolha | O quê | Por quê | O que descartei e por quê |
       14  |---|---|---|---|
       15 -| Linguagem | | | |                                           
       16 -| Testes | | | |                                              
       17 -| Parsing/validação | | | |                                   
       18 -| Aritmética monetária | | | |                                
       15 +| Linguagem | Python 3.11+ | Domínio do desenvolvedor; stdlib 
          +suficiente para o escopo; sem necessidade de performance extre
          +ma | Go: mais rígido para prototipagem; Node.js: ecossistema J
          +SON nativo mas menos familiar para código financeiro |        
       16 +| Testes | pytest | Fixtures, parametrize e saída legível; pad
          +rão de mercado em Python | unittest (stdlib): verboso, sem par
          +ametrize nativo; não justifica dependência adicional — mas pyt
          +est é leve o suficiente para valer |                          
       17 +| CLI | argparse (stdlib) | Zero dependências externas; interf
          +ace simples e fixa (`calcular --input --output`) | click: mais
          + ergonômico mas dependência extra desnecessária para uma CLI c
          +om dois argumentos |                                          
       18 +| Parsing de JSON | json (stdlib) | Leitura e escrita de JSON 
          +sem dependência; controle total sobre serialização | pydantic:
          + validação mais rica, mas introduz dependência e o schema de e
          +ntrada é fixo e simples |                                     
       19 +| Aritmética monetária | `decimal.Decimal` com `ROUND_HALF_UP`
          + | Elimina erros de ponto flutuante em comparações e cálculos;
          + implementa diretamente a decisão de arredondamento da spec (A
          +MB-010) | `float`: `0.1 + 0.2 == 0.30000000000000004`; inaceit
          +ável para sistema financeiro auditável |                      
       20  
       20 -<A linha de aritmética monetária não é decoração. Ponto flutua
          -nte em dinheiro é                                             
       21 -a fonte de bug mais previsível deste projeto.>                
       21 +---                                                           
       22  
       23  ## 2. Arquitetura
       24  
       25 -<Diagrama em blocos ou lista. Quais são as peças, o que cada u
          -ma faz, como                                                  
       26 -conversam. Uma tela, não uma tese.>                           
       27 -                                                              
       25  ```
       29 -entrada JSON → <...> → <...> → saída JSON                     
       26 +despesas.json                                                 
       27 +     │                                                        
       28 +     ▼                                                        
       29 +┌─────────────────────┐                                       
       30 +│  Leitura e parsing  │  json.load → dict Python              
       31 +└─────────────────────┘                                       
       32 +     │                                                        
       33 +     ▼                                                        
       34 +┌─────────────────────┐                                       
       35 +│   Normalização      │  valor → Decimal(half-up, 2dp)        
       36 +│   de entrada        │  categoria → lowercase + strip        
       37 +└─────────────────────┘                                       
       38 +     │  lista de DespesaNormalizada                           
       39 +     ▼                                                        
       40 +┌─────────────────────┐                                       
       41 +│  Pipeline de regras │  itera despesas em ordem do arquivo;  
       42 +│  (RF-11, 7 passos)  │  para no primeiro passo reprovador;   
       43 +│                     │  mantém estado de cotas e duplicatas  
       44 +└─────────────────────┘                                       
       45 +     │  lista de ResultadoItem                                
       46 +     ▼                                                        
       47 +┌─────────────────────┐                                       
       48 +│  Cálculo do resumo  │  agrega totais e contagens a partir do
          +s itens                                                       
       49 +└─────────────────────┘                                       
       50 +     │                                                        
       51 +     ▼                                                        
       52 +┌─────────────────────┐                                       
       53 +│  Serialização JSON  │  ordem de campos explícita; Decimal → 
          +str com 2dp                                                   
       54 +│  determinística     │  (exceto valor_original, que preserva 
          +a entrada)                                                    
       55 +└─────────────────────┘                                       
       56 +     │                                                        
       57 +     ▼                                                        
       58 +resultado.json                                                
       59  ```
       60  
       32 -**Fronteiras:** <o que é núcleo de regra de negócio puro e o q
          -ue é I/O. Onde                                                
       33 -essa linha está desenhada determina o quanto o sistema vai res
          -istir a mudança                                               
       34 -de requisito.>                                                
       61 +**Fronteira núcleo / I/O:** tudo entre Normalização e Cálculo 
          +do resumo é                                                   
       62 +núcleo de regra de negócio puro — sem I/O, sem dependência de 
          +sistema de                                                    
       63 +arquivos. A CLI (`cli.py`) faz apenas leitura de arquivo → cha
          +ma o motor →                                                  
       64 +escreve o arquivo de saída. Isso permite testar o motor inteir
          +o sem tocar                                                   
       65 +disco.                                                        
       66  
       67 +---                                                           
       68 +                                                              
       69  ## 3. Modelo de dados
       70  
       38 -<Estruturas internas. Como uma despesa é representada, como um
          - resultado de                                                 
       39 -avaliação é representado, o que carrega a justificativa.>     
       71 +Todas as estruturas são dataclasses Python (imutáveis onde pos
          +sível).                                                       
       72  
       73 +### Entrada (após parsing)                                    
       74 +                                                              
       75 +```python                                                     
       76 +@dataclass                                                    
       77 +class Colaborador:                                            
       78 +    id: str                                                   
       79 +    nome: str                                                 
       80 +    centro_custo: str                                         
       81 +                                                              
       82 +@dataclass                                                    
       83 +class Periodo:                                                
       84 +    competencia: str        # "2026-07"                       
       85 +    inicio: date            # date(2026, 7, 1)                
       86 +    fim: date               # date(2026, 7, 31)               
       87 +                                                              
       88 +@dataclass                                                    
       89 +class DespesaBruta:                                           
       90 +    id: str                                                   
       91 +    data: date                                                
       92 +    categoria: str          # valor original, sem normalização
       93 +    descricao: str                                            
       94 +    fornecedor: str                                           
       95 +    valor_original: object  # preserva o valor exato da entrad
          +a (int ou float)                                              
       96 +    tem_nota_fiscal: bool                                     
       97 +```                                                           
       98 +                                                              
       99 +### Após normalização (entrada do pipeline)                   
      100 +                                                              
      101 +```python                                                     
      102 +@dataclass                                                    
      103 +class Despesa:                                                
      104 +    id: str                                                   
      105 +    data: date                                                
      106 +    categoria: str          # lowercase + strip aplicados     
      107 +    descricao: str                                            
      108 +    fornecedor: str                                           
      109 +    valor_original: object  # preservado da entrada (para saíd
          +a)                                                            
      110 +    valor_considerado: Decimal  # half-up, 2dp                
      111 +    tem_nota_fiscal: bool                                     
      112 +```                                                           
      113 +                                                              
      114 +### Saída do pipeline                                         
      115 +                                                              
      116 +```python                                                     
      117 +@dataclass                                                    
      118 +class ResultadoItem:                                          
      119 +    id: str                                                   
      120 +    status: str             # "aprovado" | "parcial" | "recusa
          +do"                                                           
      121 +    valor_original: object  # preservado da entrada           
      122 +    valor_considerado: Decimal                                
      123 +    valor_reembolsavel: Decimal                               
      124 +    motivo_codigo: str | None                                 
      125 +    motivo_texto: str | None                                  
      126 +    duplicata_de: str | None                                  
      127 +```                                                           
      128 +                                                              
      129 +### Estado interno do pipeline                                
      130 +                                                              
      131 +```python                                                     
      132 +# Controle de cotas: {(data, categoria): Decimal já consumido}
      133 +Cotas = dict[tuple[date, str], Decimal]                       
      134 +                                                              
      135 +# Registro de itens processados para detecção de duplicatas   
      136 +# Chave: tupla (data, categoria, descricao, fornecedor, valor_
          +considerado, tem_nota_fiscal)                                 
      137 +Vistos = dict[tuple, str]  # chave → id do item mantido       
      138 +```                                                           
      139 +                                                              
      140 +---                                                           
      141 +                                                              
      142  ## 4. Como a política é representada
      143  
       43 -<Os limites vivem onde? Constantes no código, arquivo de confi
          -guração, tabela?                                              
       44 -Esta decisão é a que mais barato ou mais caro vai custar se a 
          -política mudar.>                                              
      144 +Os limites diários e o gatilho de NF vivem em **constantes no 
          +módulo de                                                     
      145 +regras** (`src/regras.py`), não espalhados pelas funções:     
      146  
      147 +```python                                                     
      148 +LIMITE_DIARIO = {                                             
      149 +    "alimentacao": Decimal("60.00"),                          
      150 +    "transporte_urbano": Decimal("80.00"),                    
      151 +    "hospedagem": Decimal("250.00"),                          
      152 +}                                                             
      153 +GATILHO_NF = Decimal("100.00")                                
      154 +```                                                           
      155 +                                                              
      156 +**Por quê constantes em vez de arquivo de configuração:** o es
          +copo atual tem                                                
      157 +três limites fixos e um gatilho; extrair para JSON/YAML adicio
          +naria parsing                                                 
      158 +sem benefício real. Se a política mudar (envelope do Dia 2 ou 
          +evolução                                                      
      159 +futura), editar as constantes é uma mudança cirúrgica de uma l
          +inha por limite.                                              
      160 +                                                              
      161 +**Consequência:** uma mudança de limite requer editar `regras.
          +py` e atualizar                                               
      162 +a spec + DECISIONS.md. Aceitável para o escopo do desafio.    
      163 +                                                              
      164 +---                                                           
      165 +                                                              
      166  ## 5. Decisões técnicas
      167  
       48 -### DT-001 — <decisão>                                        
      168 +### DT-001 — Separação estrita entre I/O e motor de regras    
      169  
       50 -**Contexto:** <o que forçou a escolha>                        
       51 -**Decisão:** <o que foi decidido>                             
       52 -**Alternativa descartada:** <e por quê>                       
       53 -**Consequência:** <o que isso torna fácil e o que torna difíci
          -l>                                                            
      170 +**Contexto:** testes de regras de negócio não devem depender d
          +e disco.                                                      
      171  
       55 -### DT-002 — ...                                              
      172 +**Decisão:** `cli.py` faz leitura/escrita de arquivo; `motor.p
          +y` recebe e                                                   
      173 +retorna estruturas Python puras. A função central é           
      174 +`processar(colaborador, periodo, despesas) → Resultado`.      
      175  
      176 +**Alternativa descartada:** motor que abre o arquivo diretamen
          +te — dificulta                                                
      177 +testes unitários e viola separação de responsabilidades.      
      178 +                                                              
      179 +**Consequência:** testes chamam `processar()` com dados em mem
          +ória; fácil e                                                 
      180 +rápido. CLI é um wrapper fino que o teste de integração pode e
          +xercitar com                                                  
      181 +arquivos temporários.                                         
      182 +                                                              
      183 +---                                                           
      184 +                                                              
      185 +### DT-002 — Pipeline como sequência de funções de verificação
      186 +                                                              
      187 +**Contexto:** a spec define 7 passos com ordem fixa (RF-11). O
          + código deve                                                  
      188 +refletir essa estrutura.                                      
      189 +                                                              
      190 +**Decisão:** cada passo 2–6 é uma função `verificar_XX(despesa
          +, contexto) →                                                 
      191 +ResultadoItem | None` que retorna o item recusado ou `None` (p
          +assou). O                                                     
      192 +passo 7 é uma função separada que recebe o estado de cotas. O 
          +pipeline em                                                   
      193 +`motor.py` itera a lista de verificadores em ordem.           
      194 +                                                              
      195 +**Alternativa descartada:** cadeia de `if/elif` em uma função 
          +monolítica —                                                  
      196 +dificulta teste isolado de cada regra e torna a ordem implícit
          +a no código.                                                  
      197 +                                                              
      198 +**Consequência:** adicionar ou reordenar uma regra (ex.: envel
          +ope do Dia 2) é                                               
      199 +uma mudança de uma linha na lista de verificadores do pipeline
          +.                                                             
      200 +                                                              
      201 +---                                                           
      202 +                                                              
      203 +### DT-003 — Serialização JSON com ordem de campos explícita  
      204 +                                                              
      205 +**Contexto:** a spec exige saída determinística byte a byte (R
          +F-14).                                                        
      206 +`json.dumps` em Python não garante ordem de chaves de dicts ar
          +bitrários.                                                    
      207 +                                                              
      208 +**Decisão:** serializar cada estrutura de saída para `dict` co
          +m ordem de                                                    
      209 +campos explícita (construção literal na ordem desejada), depoi
          +s                                                             
      210 +`json.dumps(..., ensure_ascii=False, indent=2)`. `Decimal` é c
          +onvertido para                                                
      211 +`str` e depois para `float` via encoder customizado para prese
          +rvar 2dp.                                                     
      212 +`valor_original` é serializado como recebido da entrada.      
      213 +                                                              
      214 +**Alternativa descartada:** `dataclasses.asdict()` + `json.dum
          +ps(sort_keys=True)` —                                         
      215 +`sort_keys` reordena alfabeticamente, não na ordem da spec; `a
          +sdict` não                                                    
      216 +controla ordem de campos customizada.                         
      217 +                                                              
      218 +**Consequência:** qualquer mudança no schema de saída requer e
          +ditar o                                                       
      219 +serializador explicitamente — mas garante que a saída seja aud
          +itável e                                                      
      220 +previsível.                                                   
      221 +                                                              
      222 +---                                                           
      223 +                                                              
      224 +### DT-004 — `valor_original` preservado como tipo nativo da e
          +ntrada                                                        
      225 +                                                              
      226 +**Contexto:** a spec exige que `valor_original` ecoe o valor d
          +a entrada sem                                                 
      227 +normalização (AMB-010, RF-01). O JSON de entrada pode trazer `
          +33.333` (float                                                
      228 +Python) ou `72.5` (float) ou `480` (int).                     
      229 +                                                              
      230 +**Decisão:** `valor_original` é armazenado como o valor Python
          + nativo                                                       
      231 +resultante do `json.load` (int ou float) e serializado diretam
          +ente para JSON                                                
      232 +sem conversão. `valor_considerado` é sempre `Decimal` com 2dp.
      233 +                                                              
      234 +**Alternativa descartada:** converter `valor_original` para `D
          +ecimal` também                                                
      235 +— perderia a forma original (`33.333` viraria `33.33`), esvazi
          +ando o                                                        
      236 +propósito do campo.                                           
      237 +                                                              
      238 +**Consequência:** o serializador precisa tratar `valor_origina
          +l` como caso                                                  
      239 +especial (não passa pelo encoder de `Decimal`).               
      240 +                                                              
      241 +---                                                           
      242 +                                                              
      243 +### DT-005 — Estrutura de diretórios                          
      244 +                                                              
      245 +```                                                           
      246 +src/                                                          
      247 +  __init__.py                                                 
      248 +  cli.py          ← argparse; lê arquivo, chama motor, escreve
          + saída                                                        
      249 +  motor.py        ← processar(): orquestra normalização → pipe
          +line → resumo                                                 
      250 +  regras.py       ← verificadores de cada passo + constantes d
          +e limite                                                      
      251 +  modelos.py      ← dataclasses de entrada e saída            
      252 +  serializador.py ← dict de saída com ordem explícita + encode
          +r JSON                                                        
      253 +tests/                                                        
      254 +  conftest.py     ← fixtures: periodo padrão, colaborador padr
          +ão, helpers                                                   
      255 +  test_rf01_normalizacao_valor.py                             
      256 +  test_rf02_normalizacao_categoria.py                         
      257 +  test_rf03_dominio_valor.py                                  
      258 +  test_rf04_competencia.py                                    
      259 +  test_rf05_categoria_invalida.py                             
      260 +  test_rf06_duplicatas.py                                     
      261 +  test_rf07_nota_fiscal.py                                    
      262 +  test_rf08_limite_alimentacao.py                             
      263 +  test_rf09_limite_transporte.py                              
      264 +  test_rf10_limite_hospedagem.py                              
      265 +  test_rf11_ordem_regras.py                                   
      266 +  test_rf12_reembolso_parcial.py                              
      267 +  test_rf13_status_derivado.py                                
      268 +  test_rf14_determinismo.py                                   
      269 +  test_rf15_fim_de_semana.py                                  
      270 +  test_rf16_viagem_suspensa.py                                
      271 +  test_borda.py   ← casos da seção 7 da spec que cruzam múltip
          +las regras                                                    
      272 +  test_integracao.py ← processa despesas-exemplo.json completo
          +, verifica cada item                                          
      273 +```                                                           
      274 +                                                              
      275 +**Alternativa descartada:** um único `test_motor.py` — perde r
          +astreabilidade                                                
      276 +direta entre teste e RF; dificulta localizar falha na correção
          +.                                                             
      277 +                                                              
      278 +---                                                           
      279 +                                                              
      280  ## 6. Estratégia de testes
      281  
       59 -- **Nível:** <unitário, integração, ponta a ponta — e a propor
          -ção entre eles>                                               
       60 -- **Cada `RN-NNN` da spec tem teste?** <como você garante isso
          ->                                                             
       61 -- **Casos de borda da seção 7 da spec:** <cobertos como>      
       62 -- **Nomenclatura:** <como o nome do teste remete ao requisito 
          -— isso é o que                                                
       63 -  fecha a rastreabilidade na correção>                        
      282 +**Proporção:** ~80% unitários (regras isoladas), ~20% integraç
          +ão (arquivo                                                   
      283 +completo). Nenhum teste de ponta a ponta via CLI nos testes au
          +tomatizados —                                                 
      284 +a CLI é exercitada manualmente pelo README.                   
      285  
      286 +**Nomenclatura:** `test_rfXX_<descricao_do_aceite>` para teste
          +s de RF;                                                      
      287 +`test_borda_<caso>` para casos da seção 7 que cruzam regras.  
      288 +                                                              
      289 +**Cobertura obrigatória por RF:**                             
      290 +                                                              
      291 +| RF | Teste(s) obrigatório(s) |                              
      292 +|---|---|                                                     
      293 +| RF-01 | `test_rf01_valor_333_normaliza_para_33`, `test_rf01_
          +valor_335_arredonda_para_34`, `test_rf01_valor_original_preser
          +vado` |                                                       
      294 +| RF-02 | `test_rf02_maiusculas_reconhecidas`, `test_rf02_espa
          +cos_removidos`, `test_rf02_acento_nao_normalizado` |          
      295 +| RF-03 | `test_rf03_valor_negativo_recusado`, `test_rf03_valo
          +r_zero_recusado`, `test_rf03_nao_consome_cota` |              
      296 +| RF-04 | `test_rf04_data_anterior_recusada`, `test_rf04_data_
          +posterior_recusada`, `test_rf04_limite_inclusivo_inicio`, `tes
          +t_rf04_limite_inclusivo_fim` |                                
      297 +| RF-05 | `test_rf05_coworking_recusado`, `test_rf05_categoria
          +_apos_normalizacao_aceita` |                                  
      298 +| RF-06 | `test_rf06_duplicata_exata_recusada`, `test_rf06_pri
          +meiro_mantido`, `test_rf06_duplicata_de_recusado_ainda_detecta
          +da`, `test_rf06_nao_consome_cota` |                           
      299 +| RF-07 | `test_rf07_fronteira_100_sem_nf_passa`, `test_rf07_f
          +ronteira_100_01_sem_nf_recusa`, `test_rf07_com_nf_passa` |    
      300 +| RF-08 | `test_rf08_agregado_diario_corte`, `test_rf08_cota_e
          +sgotada_segundo_item`, `test_rf08_dentro_do_limite_aprovado` |
      301 +| RF-09 | `test_rf09_agregado_diario_corte`, `test_rf09_sem_nf
          +_nao_consome_cota` |                                          
      302 +| RF-10 | `test_rf10_limite_por_lancamento`, `test_rf10_descri
          +cao_ignorada` |                                               
      303 +| RF-11 | `test_rf11_competencia_precede_nf`, `test_rf11_dupli
          +cata_de_item_sem_nf` |                                        
      304 +| RF-12 | `test_rf12_exceder_limite_nao_recusa`, `test_rf12_re
          +embolsa_saldo_disponivel` |                                   
      305 +| RF-13 | `test_rf13_status_aprovado`, `test_rf13_status_parci
          +al`, `test_rf13_cota_esgotada_e_recusado` |                   
      306 +| RF-14 | `test_rf14_saidas_identicas_mesma_entrada` |        
      307 +| RF-15 | `test_rf15_sabado_processado_normalmente` |         
      308 +| RF-16 | `test_rf16_nenhum_item_com_limite_ampliado` |       
      309 +                                                              
      310 +**Integração (`test_integracao.py`):** carrega `exemplos/despe
          +sas-exemplo.json`,                                            
      311 +chama `processar()` e verifica cada um dos 17 critérios de ace
          +ite da seção 9                                                
      312 +da spec. Um assert por critério, nomeado com o id do item (ex.
          +:                                                             
      313 +`assert resultado.itens[0].motivo_codigo == "LIMITE_DIARIO"  #
          + d-001`).                                                     
      314 +                                                              
      315 +**Fixtures em `conftest.py`:**                                
      316 +- `periodo_padrao`: `Periodo(competencia="2026-07", inicio=dat
          +e(2026,7,1), fim=date(2026,7,31))`                            
      317 +- `colaborador_padrao`: `Colaborador(id="c-0001", nome="Teste"
          +, centro_custo="CC-TEST")`                                    
      318 +- `despesa_factory`: função que cria `Despesa` com defaults so
          +brescrevíveis por kwarg                                       
      319 +                                                              
      320 +---                                                           
      321 +                                                              
      322  ## 7. Riscos
      323  
      324  | Risco | Probabilidade | O que faço se acontecer |
      325  |---|---|---|
       69 -| | | |                                                       
      326 +| Envelope do Dia 2 exige novo campo no schema de entrada | Al
          +ta (campo `em_viagem` ou `num_diarias` são candidatos óbvios) 
          +| Adicionar campo opcional ao parsing com default; regra nova 
          +entra como passo no pipeline; constante nova em `regras.py` | 
      327 +| Envelope exige nova categoria reembolsável | Média | Adicion
          +ar à lista canônica em `regras.py` + novo limite em `LIMITE_DI
          +ARIO` |                                                       
      328 +| Serialização JSON não garante 2dp para Decimal em edge case 
          +| Baixa | Encoder customizado já cobre; teste `test_rf14_saida
          +s_identicas_mesma_entrada` detecta |                          
      329 +| `valor_original` float de entrada perde precisão no round-tr
          +ip JSON | Baixa | `json.dumps` preserva float Python → JSON fl
          +oat sem reprocessamento; testado em `test_rf01_valor_original_
          +preservado` |                                                 

● plan.md escrito. Aqui estão os pontos fracos que você deve verificar:

  1. DT-004 / valor_original como float nativo: json.load vai trazer 33.333 como
   float Python 33.333 — mas floats têm precisão finita e 33.333 pode virar
  33.33300000000000001 no repr. Precisa testar se json.dumps serializa de volta
  para 33.333 limpo. Se não, pode ser necessário preservar o valor como string
  na leitura.
  2. Estrutura de arquivos de teste: propus um arquivo por RF (16 arquivos). Se
  preferir consolidar em menos arquivos (ex.: por fase de implementação), avise
  antes de escrever as tasks.
  3. test_integracao.py carrega o arquivo do disco: é o único teste com I/O; se
  o path relativo causar problema no pytest, precisará de fixture com tmp_path
  ou path absoluto derivado de __file__.
  4. Risco do envelope: listei em_viagem e num_diarias como candidatos — mas se
  o envelope for outra coisa, a arquitetura de pipeline absorve qualquer novo
  passo sem cirurgia.

  Posso commitar agora com:

  docs(plan): plan.md v1.0 — stack, arquitetura, modelo de dados, estratégia de
  testes

✻ Cogitated for 1m 59s

> Revisão do plan — aprovo com 1 correção e 3 confirmações:                     
                                                                                
  1. DT-004 tem problema maior que o apontado: não é só o round-trip — é a      
  construção. json.load traz 33.335 como float 33.334999..., e Decimal desse    
  float com half-up dá 33.33, violando o aceite do RF-01 (33.335 → 33.34).      
  Correção: json.load com parse_float=Decimal — o parser recebe a string        
  literal, Decimal("33.335") é exato, e como Decimal preserva os dígitos        
  literais, valor_original vira Decimal ecoando a entrada (33.333 serializa     
  como 33.333), sem caso especial de float. Reescreva DT-004 com essa decisão   
  (alternativa descartada: float nativo, pelo motivo acima) e ajuste o modelo   
  de dados (valor_original: Decimal) e o DT-003 (encoder trata Decimal em dois  
  modos: quantizado a 2dp para os campos calculados, dígitos literais para      
  valor_original). Adicione teste: test_rf01_valor_335_arredonda_para_34 é o    
  que pega essa regressão.                                                      
                                                                                
  2. Estrutura de testes: manter um arquivo por RF como proposto — a            
  rastreabilidade teste↔RF vale mais que a economia de arquivos.                
                                                                                
  3. test_integracao com path derivado de __file__: aprovado.                   
                                                                                
  4. Riscos do envelope: bom como está.                                         
                                                                                
  Depois dos ajustes, commite com a mensagem sugerida.                          

● Fazendo os 3 ajustes em paralelo.

● Update(specs\001-motor-reembolso\plan.md)
  ⎿  Added 1 line, removed 1 line
      92      categoria: str          # valor original, sem normalização
      93      descricao: str
      94      fornecedor: str
      95 -    valor_original: object  # preserva o valor exato da entrada
         - (int ou float)                                                
      95 +    valor_original: Decimal  # Decimal literal da entrada (ex.:
         + Decimal("33.333"))                                            
      96      tem_nota_fiscal: bool
      97  ```
      98  

● Update(specs\001-motor-reembolso\plan.md)
  ⎿  Added 1 line, removed 1 line
      106      categoria: str          # lowercase + strip aplicados
      107      descricao: str
      108      fornecedor: str
      109 -    valor_original: object  # preservado da entrada (para saíd
          -a)                                                            
      109 +    valor_original: Decimal  # Decimal literal preservado da e
          +ntrada (para saída)                                           
      110      valor_considerado: Decimal  # half-up, 2dp
      111      tem_nota_fiscal: bool
      112  ```

● Update(specs\001-motor-reembolso\plan.md)
  ⎿  Added 1 line, removed 1 line
      118  class ResultadoItem:
      119      id: str
      120      status: str             # "aprovado" | "parcial" | "recusa
           do"
      121 -    valor_original: object  # preservado da entrada           
      121 +    valor_original: Decimal  # Decimal literal preservado da e
          +ntrada                                                        
      122      valor_considerado: Decimal
      123      valor_reembolsavel: Decimal
      124      motivo_codigo: str | None

● Update(specs\001-motor-reembolso\plan.md)
  ⎿  Error editing file

  Searched for 1 pattern (ctrl+o to expand)

● O ResultadoItem já foi atualizado. Agora DT-003 e DT-004:

  Read 1 file (ctrl+o to expand)

● Update(specs\001-motor-reembolso\plan.md)
  ⎿  Added 31 lines, removed 19 lines
      200  
      201  ---
      202  
      203 -### DT-003 — Serialização JSON com ordem de campos explícita  
      203 +### DT-003 — Serialização JSON com ordem de campos explícita e
          + encoder de Decimal em dois modos                             
      204  
      205  **Contexto:** a spec exige saída determinística byte a byte (R
           F-14).
      206  `json.dumps` em Python não garante ordem de chaves de dicts ar
           bitrários.
      207 +`Decimal` não é serializável por padrão.                      
      208  
      209  **Decisão:** serializar cada estrutura de saída para `dict` co
           m ordem de
      210  campos explícita (construção literal na ordem desejada), depoi
           s
      210 -`json.dumps(..., ensure_ascii=False, indent=2)`. `Decimal` é c
          -onvertido para                                                
      211 -`str` e depois para `float` via encoder customizado para prese
          -rvar 2dp.                                                     
      212 -`valor_original` é serializado como recebido da entrada.      
      211 +`json.dumps(..., ensure_ascii=False, indent=2)` com encoder cu
          +stomizado.                                                    
      212 +O encoder trata `Decimal` em dois modos:                      
      213 +- **Modo quantizado (2dp):** campos calculados (`valor_conside
          +rado`,                                                        
      214 +  `valor_reembolsavel`, totais do resumo) → `quantize(Decimal(
          +"0.01"),                                                      
      215 +  ROUND_HALF_UP)` → serializado como número JSON com 2dp.     
      216 +- **Modo literal:** `valor_original` → `normalize()` ou conver
          +são direta para                                               
      217 +  `float`/`int` via `str` → serializado preservando os dígitos
          + da entrada                                                   
      218 +  (ex.: `Decimal("33.333")` → `33.333` no JSON).              
      219  
      220  **Alternativa descartada:** `dataclasses.asdict()` + `json.dum
           ps(sort_keys=True)` —
      215 -`sort_keys` reordena alfabeticamente, não na ordem da spec; `a
          -sdict` não                                                    
      216 -controla ordem de campos customizada.                         
      221 +`sort_keys` reordena alfabeticamente; `asdict` não controla or
          +dem customizada.                                              
      222  
      223  **Consequência:** qualquer mudança no schema de saída requer e
           ditar o
      219 -serializador explicitamente — mas garante que a saída seja aud
          -itável e                                                      
      220 -previsível.                                                   
      224 +serializador explicitamente — mas garante auditabilidade e pre
          +visibilidade.                                                 
      225  
      226  ---
      227  
      224 -### DT-004 — `valor_original` preservado como tipo nativo da e
          -ntrada                                                        
      228 +### DT-004 — Parsing de `valor` com `parse_float=Decimal`     
      229  
      230  **Contexto:** a spec exige que `valor_original` ecoe o valor d
           a entrada sem
      227 -normalização (AMB-010, RF-01). O JSON de entrada pode trazer `
          -33.333` (float                                                
      228 -Python) ou `72.5` (float) ou `480` (int).                     
      231 +normalização e que `valor_considerado` seja o arredondamento h
          +alf-up a 2dp                                                  
      232 +(RF-01). O aceite inclui `33.335 → valor_considerado 33.34`.  
      233  
      230 -**Decisão:** `valor_original` é armazenado como o valor Python
          - nativo                                                       
      231 -resultante do `json.load` (int ou float) e serializado diretam
          -ente para JSON                                                
      232 -sem conversão. `valor_considerado` é sempre `Decimal` com 2dp.
      234 +**Problema com float nativo:** `json.load` padrão converte `33
          +.335` para o                                                  
      235 +float Python `33.334999...`. `Decimal(33.334999...)` com `ROUN
          +D_HALF_UP` dá                                                 
      236 +`33.33`, violando o aceite. O erro não aparece em valores "red
          +ondos" e é                                                    
      237 +silencioso — detectável apenas pelo teste `test_rf01_valor_335
          +_arredonda_para_34`.                                          
      238  
      234 -**Alternativa descartada:** converter `valor_original` para `D
          -ecimal` também                                                
      235 -— perderia a forma original (`33.333` viraria `33.33`), esvazi
          -ando o                                                        
      236 -propósito do campo.                                           
      239 +**Decisão:** `json.load(f, parse_float=Decimal)` — o parser pa
          +ssa a string                                                  
      240 +literal `"33.335"` diretamente para `Decimal`, produzindo `Dec
          +imal("33.335")`                                               
      241 +exato. `valor_original` armazena esse `Decimal` literal; `valo
          +r_considerado`                                                
      242 +é `valor_original.quantize(Decimal("0.01"), ROUND_HALF_UP)`. A
          +mbos são                                                      
      243 +`Decimal`; o encoder os trata em modos diferentes (DT-003).   
      244  
      238 -**Consequência:** o serializador precisa tratar `valor_origina
          -l` como caso                                                  
      239 -especial (não passa pelo encoder de `Decimal`).               
      245 +**Alternativa descartada:** float nativo do `json.load` — `Dec
          +imal(float)`                                                  
      246 +herda a imprecisão do float; `33.335` via float não arredonda 
          +para `33.34`.                                                 
      247  
      248 +**Consequência:** `valor_original` é sempre `Decimal`, não `fl
          +oat` ou `int`.                                                
      249 +Inteiros da entrada (`480`) chegam como `Decimal("480")` — com
          +portamento                                                    
      250 +correto e uniforme. O encoder serializa `Decimal("480")` como 
          +`480` (sem                                                    
      251 +casas) para `valor_original`.                                 
      252 +                                                              
      253  ---
      254  
      255  ### DT-005 — Estrutura de diretórios

● Agora atualizando o risco que mencionava float no round-trip:

● Update(specs\001-motor-reembolso\plan.md)
  ⎿  Added 1 line, removed 1 line
      338  | Envelope do Dia 2 exige novo campo no schema de entrada | Al
           ta (campo `em_viagem` ou `num_diarias` são candidatos óbvios) 
           | Adicionar campo opcional ao parsing com default; regra nova 
           entra como passo no pipeline; constante nova em `regras.py` |
      339  | Envelope exige nova categoria reembolsável | Média | Adicion
           ar à lista canônica em `regras.py` + novo limite em `LIMITE_DI
           ARIO` |
      340  | Serialização JSON não garante 2dp para Decimal em edge case 
           | Baixa | Encoder customizado já cobre; teste `test_rf14_saida
           s_identicas_mesma_entrada` detecta |
      341 -| `valor_original` float de entrada perde precisão no round-tr
          -ip JSON | Baixa | `json.dumps` preserva float Python → JSON fl
          -oat sem reprocessamento; testado em `test_rf01_valor_original_
          -preservado` |                                                 
      341 +| `parse_float=Decimal` altera comportamento de inteiros na en
          +trada | Baixa | Inteiros JSON chegam como `Decimal("480")` — u
          +niforme e correto; encoder serializa de volta como `480` sem c
          +asas decimais |                                               

● Commitando:
  Ran 1 shell command (ctrl+o to expand)

> Correção no DT-004 antes do commit: a afirmação "inteiros chegam como         
  Decimal('480')" está errada — parse_float só intercepta números com parte     
  fracionária; 480 passa pelo parse_int e chega como int Python, quebrando a    
  uniformidade prometida (valor_original: Decimal no modelo) e qualquer         
  quantize sobre ele. Corrija para json.load(f, parse_float=Decimal,            
  parse_int=Decimal) no DT-004 e ajuste a última linha da tabela de riscos.     
  Adicione o aceite correspondente na estratégia de testes:                     
  test_rf01_valor_inteiro_da_entrada (480 → valor_original 480,                 
  valor_considerado 480.00). Depois commite com a mensagem que você sugeriu.    

● Bom catch. Três edições cirúrgicas:

● Update(specs\001-motor-reembolso\plan.md)
  ⎿  Added 12 lines, removed 10 lines
      236  `33.33`, violando o aceite. O erro não aparece em valores "red
           ondos" e é
      237  silencioso — detectável apenas pelo teste `test_rf01_valor_335
           _arredonda_para_34`.
      238  
      239 -**Decisão:** `json.load(f, parse_float=Decimal)` — o parser pa
          -ssa a string                                                  
      240 -literal `"33.335"` diretamente para `Decimal`, produzindo `Dec
          -imal("33.335")`                                               
      241 -exato. `valor_original` armazena esse `Decimal` literal; `valo
          -r_considerado`                                                
      242 -é `valor_original.quantize(Decimal("0.01"), ROUND_HALF_UP)`. A
          -mbos são                                                      
      239 +**Decisão:** `json.load(f, parse_float=Decimal, parse_int=Deci
          +mal)` — tanto                                                 
      240 +números fracionários quanto inteiros passam pelo construtor `D
          +ecimal` a partir                                              
      241 +da string literal. `Decimal("33.335")` é exato; `Decimal("480"
          +)` é uniforme.                                                
      242 +`valor_original` armazena esse `Decimal` literal; `valor_consi
          +derado` é                                                     
      243 +`valor_original.quantize(Decimal("0.01"), ROUND_HALF_UP)`. Amb
          +os são                                                        
      244  `Decimal`; o encoder os trata em modos diferentes (DT-003).
      245  
      245 -**Alternativa descartada:** float nativo do `json.load` — `Dec
          -imal(float)`                                                  
      246 -herda a imprecisão do float; `33.335` via float não arredonda 
          -para `33.34`.                                                 
      246 +**Alternativa descartada:** `parse_float=Decimal` sem `parse_i
          +nt=Decimal` —                                                 
      247 +inteiros chegam como `int` Python, quebrando a uniformidade do
          + modelo                                                       
      248 +(`valor_original: Decimal`) e exigindo tratamento especial no 
          +normalizador e                                                
      249 +no encoder.                                                   
      250  
      248 -**Consequência:** `valor_original` é sempre `Decimal`, não `fl
          -oat` ou `int`.                                                
      249 -Inteiros da entrada (`480`) chegam como `Decimal("480")` — com
          -portamento                                                    
      250 -correto e uniforme. O encoder serializa `Decimal("480")` como 
          -`480` (sem                                                    
      251 -casas) para `valor_original`.                                 
      251 +**Consequência:** `valor_original` é sempre `Decimal`. O encod
          +er serializa                                                  
      252 +`Decimal("480")` como `480` (sem casas) e `Decimal("33.333")` 
          +como `33.333`                                                 
      253 +para `valor_original`, preservando a forma da entrada em ambos
          + os casos.                                                    
      254  
      255  ---
      256  

● Update(specs\001-motor-reembolso\plan.md)
  ⎿  Added 1 line, removed 1 line
      340  | Envelope do Dia 2 exige novo campo no schema de entrada | Al
           ta (campo `em_viagem` ou `num_diarias` são candidatos óbvios) 
           | Adicionar campo opcional ao parsing com default; regra nova 
           entra como passo no pipeline; constante nova em `regras.py` |
      341  | Envelope exige nova categoria reembolsável | Média | Adicion
           ar à lista canônica em `regras.py` + novo limite em `LIMITE_DI
           ARIO` |
      342  | Serialização JSON não garante 2dp para Decimal em edge case 
           | Baixa | Encoder customizado já cobre; teste `test_rf14_saida
           s_identicas_mesma_entrada` detecta |
      343 -| `parse_float=Decimal` altera comportamento de inteiros na en
          -trada | Baixa | Inteiros JSON chegam como `Decimal("480")` — u
          -niforme e correto; encoder serializa de volta como `480` sem c
          -asas decimais |                                               
      343 +| `parse_int=Decimal` intercepta campos não-monetários (ex.: `
          +itens_processados` na saída) | Baixa | `parse_float` e `parse_
          +int` afetam apenas a leitura da entrada; a saída é construída 
          +diretamente de `Decimal` e `int` Python — não há conflito |   

● Update(specs\001-motor-reembolso\plan.md)
  ⎿  Added 1 line, removed 1 line
      304  
      305  | RF | Teste(s) obrigatório(s) |
      306  |---|---|
      307 -| RF-01 | `test_rf01_valor_333_normaliza_para_33`, `test_rf01_
          -valor_335_arredonda_para_34`, `test_rf01_valor_original_preser
          -vado` |                                                       
      307 +| RF-01 | `test_rf01_valor_333_normaliza_para_33`, `test_rf01_
          +valor_335_arredonda_para_34`, `test_rf01_valor_original_preser
          +vado`, `test_rf01_valor_inteiro_da_entrada` (480 → `valor_orig
          +inal: Decimal("480")`, `valor_considerado: Decimal("480.00")`)
          + |                                                            
      308  | RF-02 | `test_rf02_maiusculas_reconhecidas`, `test_rf02_espa
           cos_removidos`, `test_rf02_acento_nao_normalizado` |
      309  | RF-03 | `test_rf03_valor_negativo_recusado`, `test_rf03_valo
           r_zero_recusado`, `test_rf03_nao_consome_cota` |
      310  | RF-04 | `test_rf04_data_anterior_recusada`, `test_rf04_data_
           posterior_recusada`, `test_rf04_limite_inclusivo_inicio`, `tes
           t_rf04_limite_inclusivo_fim` |

  Committed f8fec9 (ctrl+o to expand)

● Commitado. f8fec92 — docs(plan): plan.md v1.0.

  Dois erros corrigidos por você neste arquivo — ambos merecem registro para a
  seção Discernimento do relatório: (1) DT-004 original com float nativo
  quebraria 33.335 → 33.34 silenciosamente; (2) parse_float sem parse_int
  quebraria uniformidade do modelo. Os testes
  test_rf01_valor_335_arredonda_para_34 e test_rf01_valor_inteiro_da_entrada são
   os que teriam pegado esses bugs.

  Próximo passo: tasks.md. Posso iniciar agora.

✻ Brewed for 38s

※ recap: Estamos construindo o motor de reembolso de despesas usando Spec Driven Development. Spec e plan estão commitados; o próximo passo é escrever o tasks.md.

> Agora o tasks.md: T-001..T-0NN a partir da spec e do plan. Cada task: o que   
  faz, quais RF-XX atende, critério de aceite ("o teste X passa"). Tamanho de   
  um commit cada. Ordem de implementação: modelos e parsing primeiro (DT-004),  
  depois normalização, depois os verificadores dos passos 2–6 um a um, depois o 
   passo 7 (cotas), serializador, CLI, integração. Inclua task para o README.   
  Me mostre antes de commitar.                                                  

  Read 1 file (ctrl+o to expand)

● Write(specs\001-motor-reembolso\tasks.md)
  ⎿  Added 304 lines, removed 24 lines
        7  > de quando cada task foi marcada é lido na correção.
        8  
        9  **Formato do commit:** `feat(T-003): <descrição>` · `test(T-00
           3): <descrição>`
       10 +Documentação: `docs(spec):` · `docs(plan):` · `docs(tasks):`  
       11  
       12  ---
       13  
       13 -## Fase 1 — Fundação                                          
       14 +## Fase 1 — Fundação (setup e modelos)                        
       15  
       15 -- [ ] **T-001** — <o que faz>                                 
       16 -  - **Atende:** RN-001                                        
       17 -  - **Aceite:** <o teste que precisa passar>                  
       18 -  - **Commit:** `<hash preenchido depois>`                    
       16 +- [ ] **T-001** — Estrutura de diretórios e configuração de te
          +stes                                                          
       17 +  - **O que faz:** cria `src/__init__.py`, `tests/__init__.py`
          +, `tests/conftest.py`                                         
       18 +    com fixtures `periodo_padrao`, `colaborador_padrao` e `des
          +pesa_factory`;                                                
       19 +    cria `pytest.ini` ou `pyproject.toml` com `testpaths = tes
          +ts`.                                                          
       20 +  - **Atende:** DT-005 (estrutura de diretórios)              
       21 +  - **Aceite:** `pytest` coleta 0 testes sem erro; fixtures im
          +portáveis                                                     
       22 +  - **Commit:** ` `                                           
       23  
       20 -- [ ] **T-002** — <...>                                       
       21 -  - **Atende:**                                               
       24 +- [ ] **T-002** — Modelos de dados (`src/modelos.py`)         
       25 +  - **O que faz:** define os dataclasses `Colaborador`, `Perio
          +do`, `DespesaBruta`,                                          
       26 +    `Despesa`, `ResultadoItem` e `Resultado` conforme o modelo
          + de dados do plan.                                            
       27 +    Todos os campos monetários tipados como `Decimal`.        
       28 +  - **Atende:** DT-005; base para RF-01 a RF-16               
       29 +  - **Aceite:** `from src.modelos import Despesa, ResultadoIte
          +m` importa sem erro;                                          
       30 +    instanciação manual com valores Decimal funciona          
       31 +  - **Commit:** ` `                                           
       32 +                                                              
       33 +- [ ] **T-003** — Parsing da entrada com `parse_float=Decimal,
          + parse_int=Decimal`                                           
       34 +    (`src/parser.py`)                                         
       35 +  - **O que faz:** função `carregar_entrada(caminho) → tuple[C
          +olaborador, Periodo,                                          
       36 +    list[DespesaBruta]]` que lê JSON via `json.load(f, parse_f
          +loat=Decimal,                                                 
       37 +    parse_int=Decimal)`; converte `data` para `date`; armazena
          + `valor` como                                                 
       38 +    `Decimal` literal sem arredondar.                         
       39 +  - **Atende:** RF-01 (parcial — preservação de `valor_origina
          +l`), DT-004                                                   
       40 +  - **Aceite:** `test_rf01_valor_original_preservado` —       
       41 +    entrada com `"valor": 33.333` → `despesa_bruta.valor_origi
          +nal == Decimal("33.333")`;                                    
       42 +    `test_rf01_valor_inteiro_da_entrada` —                    
       43 +    entrada com `"valor": 480` → `despesa_bruta.valor_original
          + == Decimal("480")`                                           
       44 +  - **Commit:** ` `                                           
       45 +                                                              
       46 +---                                                           
       47 +                                                              
       48 +## Fase 2 — Normalização                                      
       49 +                                                              
       50 +- [ ] **T-004** — Normalização de valor monetário (`src/normal
          +izacao.py`)                                                   
       51 +  - **O que faz:** função `normalizar_valor(v: Decimal) → Deci
          +mal` que aplica                                               
       52 +    `quantize(Decimal("0.01"), ROUND_HALF_UP)`. Ponto único de
          + arredondamento                                               
       53 +    em todo o sistema.                                        
       54 +  - **Atende:** RF-01, AMB-010                                
       55    - **Aceite:**
       23 -  - **Commit:**                                               
       56 +    `test_rf01_valor_333_normaliza_para_33` — `normalizar_valo
          +r(Decimal("33.333")) == Decimal("33.33")`;                    
       57 +    `test_rf01_valor_335_arredonda_para_34` — `normalizar_valo
          +r(Decimal("33.335")) == Decimal("33.34")`                     
       58 +  - **Commit:** ` `                                           
       59  
       25 -## Fase 2 — Regras de negócio                                 
       60 +- [ ] **T-005** — Normalização de categoria (`src/normalizacao
          +.py`)                                                         
       61 +  - **O que faz:** função `normalizar_categoria(c: str) → str`
          + que aplica                                                   
       62 +    `c.strip().lower()`. Sem normalização de acentos ou correç
          +ão ortográfica.                                               
       63 +  - **Atende:** RF-02, AMB-011                                
       64 +  - **Aceite:**                                               
       65 +    `test_rf02_maiusculas_reconhecidas` — `normalizar_categori
          +a("ALIMENTACAO") == "alimentacao"`;                           
       66 +    `test_rf02_espacos_removidos` — `normalizar_categoria(" Al
          +imentacao ") == "alimentacao"`;                               
       67 +    `test_rf02_acento_nao_normalizado` — `normalizar_categoria
          +("Alimentação") == "alimentação"`                             
       68 +  - **Commit:** ` `                                           
       69  
       27 -- [ ] **T-00N** — <...>                                       
       28 -  - **Atende:** RN-00X, AMB-00Y                               
       70 +---                                                           
       71 +                                                              
       72 +## Fase 3 — Verificadores de recusa (passos 2–6 do RF-11)     
       73 +                                                              
       74 +- [ ] **T-006** — Verificador passo 2: domínio de valor (`src/
          +regras.py`)                                                   
       75 +  - **O que faz:** função `verificar_dominio_valor(despesa) → 
          +ResultadoItem | None`                                         
       76 +    que retorna item recusado com `VALOR_NAO_POSITIVO` se     
       77 +    `valor_considerado ≤ 0`, ou `None` se passou.             
       78 +  - **Atende:** RF-03, AMB-009                                
       79    - **Aceite:**
       30 -  - **Commit:**                                               
       80 +    `test_rf03_valor_negativo_recusado` — valor `-45.00` → `mo
          +tivo_codigo == "VALOR_NAO_POSITIVO"`,                         
       81 +    `valor_reembolsavel == Decimal("0.00")`;                  
       82 +    `test_rf03_valor_zero_recusado` — valor `0.00` → recusado;
       83 +    `test_rf03_nao_consome_cota` — item recusado não altera es
          +tado de cotas                                                 
       84 +  - **Commit:** ` `                                           
       85  
       32 -## Fase 3 — Casos de borda                                    
       86 +- [ ] **T-007** — Verificador passo 3: competência (`src/regra
          +s.py`)                                                        
       87 +  - **O que faz:** função `verificar_competencia(despesa, peri
          +odo) → ResultadoItem | None`                                  
       88 +    que retorna `FORA_COMPETENCIA` se `despesa.data < periodo.
          +inicio` ou                                                    
       89 +    `despesa.data > periodo.fim`.                             
       90 +  - **Atende:** RF-04, AMB-008                                
       91 +  - **Aceite:**                                               
       92 +    `test_rf04_data_anterior_recusada` — data `2026-04-15`, pe
          +ríodo `2026-07-01/31` → recusada;                             
       93 +    `test_rf04_data_posterior_recusada` — data `2026-08-01` → 
          +recusada;                                                     
       94 +    `test_rf04_limite_inclusivo_inicio` — data `2026-07-01` → 
          +passa;                                                        
       95 +    `test_rf04_limite_inclusivo_fim` — data `2026-07-31` → pas
          +sa                                                            
       96 +  - **Commit:** ` `                                           
       97  
       34 -- [ ] **T-00N** — <...>                                       
       98 +- [ ] **T-008** — Verificador passo 4: categoria inválida (`sr
          +c/regras.py`)                                                 
       99 +  - **O que faz:** define constante `CATEGORIAS_VALIDAS = {"al
          +imentacao",                                                   
      100 +    "transporte_urbano", "hospedagem"}` em `regras.py`; função
      101 +    `verificar_categoria(despesa) → ResultadoItem | None` que 
          +retorna                                                       
      102 +    `CATEGORIA_INVALIDA` com `motivo_texto = "categoria fora d
          +a política: <valor>"`.                                        
      103 +  - **Atende:** RF-05, AMB-011, AMB-013                       
      104 +  - **Aceite:**                                               
      105 +    `test_rf05_coworking_recusado` — categoria `"coworking"` →
          + `CATEGORIA_INVALIDA`,                                        
      106 +    texto contém `"coworking"`;                               
      107 +    `test_rf05_categoria_apos_normalizacao_aceita` — `"ALIMENT
          +ACAO"` normalizada →                                          
      108 +    passa no verificador                                      
      109 +  - **Commit:** ` `                                           
      110  
       36 -## Fase 4 — Saída e CLI                                       
      111 +- [ ] **T-009** — Verificador passo 5: duplicatas (`src/regras
          +.py`)                                                         
      112 +  - **O que faz:** função `verificar_duplicata(despesa, vistos
          +: dict) → ResultadoItem | None`                               
      113 +    que constrói chave `(data, categoria, descricao, fornecedo
          +r, valor_considerado,                                         
      114 +    tem_nota_fiscal)`; se chave já existe em `vistos`, retorna
          + `DUPLICATA` com                                              
      115 +    `duplicata_de = vistos[chave]`; senão, registra `vistos[ch
          +ave] = despesa.id`.                                           
      116 +    Verificação ocorre independentemente do status do item ori
          +ginal.                                                        
      117 +  - **Atende:** RF-06, AMB-007                                
      118 +  - **Aceite:**                                               
      119 +    `test_rf06_duplicata_exata_recusada` — d-006/d-007 idêntic
          +os → segundo recusado                                         
      120 +    com `duplicata_de == "d-006"`;                            
      121 +    `test_rf06_primeiro_mantido` — primeiro item nunca é recus
          +ado como duplicata;                                           
      122 +    `test_rf06_duplicata_de_recusado_ainda_detectada` — segund
          +o item idêntico a                                             
      123 +    item já recusado por outro motivo → ainda recusado como `D
          +UPLICATA`;                                                    
      124 +    `test_rf06_nao_consome_cota` — duplicata recusada não afet
          +a cotas                                                       
      125 +  - **Commit:** ` `                                           
      126  
       38 -- [ ] **T-00N** — <...>                                       
      127 +- [ ] **T-010** — Verificador passo 6: nota fiscal (`src/regra
          +s.py`)                                                        
      128 +  - **O que faz:** define constante `GATILHO_NF = Decimal("100
          +.00")`; função                                                
      129 +    `verificar_nf(despesa) → ResultadoItem | None` que retorna
          + `SEM_NF` se                                                  
      130 +    `despesa.valor_considerado > GATILHO_NF` e `not despesa.te
          +m_nota_fiscal`.                                               
      131 +  - **Atende:** RF-07, AMB-004, AMB-005                       
      132 +  - **Aceite:**                                               
      133 +    `test_rf07_fronteira_100_sem_nf_passa` — valor `100.00`, s
          +em NF → passa (não é                                          
      134 +    `> 100.00`);                                              
      135 +    `test_rf07_fronteira_100_01_sem_nf_recusa` — valor `100.01
          +`, sem NF → `SEM_NF`;                                         
      136 +    `test_rf07_com_nf_passa` — valor `150.00`, com NF → passa 
      137 +  - **Commit:** ` `                                           
      138  
      139  ---
      140  
       42 -## Fase 5 — Envelope (criar no Dia 2)                         
      141 +## Fase 4 — Passo 7: cotas diárias                            
      142  
       44 -<Novas tasks a partir da mudança de requisito. Numeração conti
          -nua de onde parou —                                           
       45 -não reinicie e não renumere as antigas: a numeração é o eixo d
          -a rastreabilidade.>                                           
      143 +- [ ] **T-011** — Cálculo de cotas diárias e reembolso parcial
          + (`src/cotas.py`)                                             
      144 +  - **O que faz:** classe ou módulo `GerenciadorCotas` com est
          +ado                                                           
      145 +    `dict[(date, str), Decimal]` (consumido por dia/categoria)
          +; define constantes                                           
      146 +    `LIMITE_DIARIO = {"alimentacao": Decimal("60.00"), "transp
          +orte_urbano":                                                 
      147 +    Decimal("80.00"), "hospedagem": Decimal("250.00")}`; métod
          +o                                                             
      148 +    `calcular_reembolso(despesa) → tuple[Decimal, str]` que re
          +torna                                                         
      149 +    `(valor_reembolsavel, motivo_codigo)`:                    
      150 +    - saldo > 0 e valor > saldo → reembolsa saldo, `LIMITE_DIA
          +RIO`                                                          
      151 +    - saldo = 0 → reembolsa 0, `COTA_ESGOTADA`                
      152 +    - saldo ≥ valor → reembolsa integralmente, `None`         
      153 +    Atualiza estado interno ao reembolsar.                    
      154 +  - **Atende:** RF-08, RF-09, RF-10, RF-12, AMB-001, AMB-002, 
          +AMB-003, AMB-012                                              
      155 +  - **Aceite:**                                               
      156 +    `test_rf08_agregado_diario_corte` — alimentação R$72,50 pr
          +imeiro do dia →                                               
      157 +    reembolsa R$60,00, `LIMITE_DIARIO`;                       
      158 +    `test_rf08_cota_esgotada_segundo_item` — alimentação R$38,
          +00 após R$60,00                                               
      159 +    consumidos → R$0,00, `COTA_ESGOTADA`;                     
      160 +    `test_rf08_dentro_do_limite_aprovado` — alimentação R$30,0
          +0 único do dia →                                              
      161 +    R$30,00, sem motivo;                                      
      162 +    `test_rf09_agregado_diario_corte` — transporte R$100,00 → 
          +R$80,00;                                                      
      163 +    `test_rf09_sem_nf_nao_consome_cota` — item recusado por SE
          +M_NF não reduz cota;                                          
      164 +    `test_rf10_limite_por_lancamento` — hospedagem R$480,00 → 
          +R$250,00;                                                     
      165 +    `test_rf10_descricao_ignorada` — "2 diárias" na descrição 
          +não altera limite;                                            
      166 +    `test_rf12_exceder_limite_nao_recusa` — item cortado tem `
          +valor_reembolsavel > 0`,                                      
      167 +    nunca recusado só por exceder                             
      168 +  - **Commit:** ` `                                           
      169  
      170  ---
      171  
      172 +## Fase 5 — Pipeline e status                                 
      173 +                                                              
      174 +- [ ] **T-012** — Pipeline completo e status derivado (`src/mo
          +tor.py`)                                                      
      175 +  - **O que faz:** função `processar(colaborador, periodo, des
          +pesas_brutas) →                                               
      176 +    Resultado` que: (1) normaliza cada `DespesaBruta` → `Despe
          +sa`; (2) aplica                                               
      177 +    os verificadores dos passos 2–6 em ordem, parando no prime
          +iro que retorna                                               
      178 +    recusa; (3) aplica passo 7 via `GerenciadorCotas`; (4) der
          +iva `status` a                                                
      179 +    partir dos valores (`aprovado` / `parcial` / `recusado` — 
          +RF-13); (5) constrói                                          
      180 +    `Resultado` com lista de itens em ordem da entrada.       
      181 +  - **Atende:** RF-11, RF-13, AMB-015                         
      182 +  - **Aceite:**                                               
      183 +    `test_rf11_competencia_precede_nf` — item fora de competên
          +cia E sem NF →                                                
      184 +    `FORA_COMPETENCIA` (não `SEM_NF`);                        
      185 +    `test_rf11_duplicata_de_item_sem_nf` — dois itens idêntico
          +s com valor > 100                                             
      186 +    sem NF → primeiro `SEM_NF`, segundo `DUPLICATA`;          
      187 +    `test_rf12_reembolsa_saldo_disponivel` — item cortado rece
          +be exatamente o                                               
      188 +    saldo disponível, não zero;                               
      189 +    `test_rf13_status_aprovado` — `valor_reembolsavel == valor
          +_considerado` →                                               
      190 +    `"aprovado"`;                                             
      191 +    `test_rf13_status_parcial` — `0 < valor_reembolsavel < val
          +or_considerado` →                                             
      192 +    `"parcial"`;                                              
      193 +    `test_rf13_cota_esgotada_e_recusado` — `COTA_ESGOTADA` com
      194 +    `valor_reembolsavel == 0` → `status == "recusado"`        
      195 +  - **Commit:** ` `                                           
      196 +                                                              
      197 +- [ ] **T-013** — Testes de RF-15 e RF-16 (dias da semana e vi
          +agem)                                                         
      198 +  - **O que faz:** adiciona `tests/test_rf15_fim_de_semana.py`
          + e                                                            
      199 +    `tests/test_rf16_viagem_suspensa.py`. Não requer novo códi
          +go — os testes                                                
      200 +    exercitam o pipeline existente para confirmar comportament
          +o declarado na spec.                                          
      201 +  - **Atende:** RF-15 (AMB-014), RF-16 (AMB-006)              
      202 +  - **Aceite:**                                               
      203 +    `test_rf15_sabado_processado_normalmente` — despesa de sáb
          +ado (d-012) →                                                 
      204 +    `status == "aprovado"`, `valor_reembolsavel == Decimal("47
          +.20")`;                                                       
      205 +    `test_rf16_nenhum_item_com_limite_ampliado` — nenhum item 
          +do lote de exemplo                                            
      206 +    tem `valor_reembolsavel > 60.00` por categoria alimentação
          + (limite nunca                                                
      207 +    ampliado para 90,00)                                      
      208 +  - **Commit:** ` `                                           
      209 +                                                              
      210 +---                                                           
      211 +                                                              
      212 +## Fase 6 — Resumo, serializador e CLI                        
      213 +                                                              
      214 +- [ ] **T-014** — Cálculo do resumo agregado (`src/motor.py`) 
      215 +  - **O que faz:** após construir a lista de itens, calcula `R
          +esumo`:                                                       
      216 +    `total_solicitado = Σ valor_considerado` dos itens com `va
          +lor_considerado > 0`;                                         
      217 +    `total_reembolsavel = Σ valor_reembolsavel`; `total_recusa
          +do = total_solicitado                                         
      218 +    - total_reembolsavel`; contagens por status.              
      219 +  - **Atende:** RF-14 (parcial), AMB-016                      
      220 +  - **Aceite:** processando d-001 (parcial R$60) + d-005 (recu
          +sado R$0) + d-006                                             
      221 +    (aprovado R$54,90) → `total_solicitado == Decimal("216.40"
          +)`,                                                           
      222 +    `total_reembolsavel == Decimal("114.90")`,                
      223 +    `itens_aprovados == 1`, `itens_parciais == 1`, `itens_recu
          +sados == 1`                                                   
      224 +  - **Commit:** ` `                                           
      225 +                                                              
      226 +- [ ] **T-015** — Serializador determinístico (`src/serializad
          +or.py`)                                                       
      227 +  - **O que faz:** função `serializar(resultado: Resultado) → 
          +str` que constrói                                             
      228 +    `dict` com ordem de campos explícita e aplica `json.dumps(
          +ensure_ascii=False,                                           
      229 +    indent=2)`. Encoder customizado: campos calculados → `quan
          +tize("0.01")` → número                                        
      230 +    JSON com 2dp; `valor_original` → número JSON com dígitos l
          +iterais da entrada;                                           
      231 +    contagens inteiras → `int`.                               
      232 +  - **Atende:** RF-14, DT-003, AMB-016                        
      233 +  - **Aceite:**                                               
      234 +    `test_rf14_saidas_identicas_mesma_entrada` — chamar `seria
          +lizar()` duas vezes                                           
      235 +    com o mesmo `Resultado` produz strings idênticas;         
      236 +    campos de `valor_original` no JSON preservam `33.333` (não
          + `33.33`);                                                    
      237 +    campos calculados têm exatamente 2 casas decimais         
      238 +  - **Commit:** ` `                                           
      239 +                                                              
      240 +- [ ] **T-016** — CLI com argparse (`src/cli.py`)             
      241 +  - **O que faz:** entry point `python -m src.cli calcular --i
          +nput <arq>                                                    
      242 +    --output <arq>` que carrega entrada via `parser.carregar_e
          +ntrada()`,                                                    
      243 +    chama `motor.processar()`, serializa via `serializador.ser
          +ializar()` e                                                  
      244 +    escreve o arquivo de saída. Erros de entrada inválida prod
          +uzem mensagem                                                 
      245 +    clara, não traceback.                                     
      246 +  - **Atende:** DT-001 (separação I/O / motor), interface do D
          +ESAFIO.md                                                     
      247 +  - **Aceite:** `python -m src.cli calcular --input exemplos/d
          +espesas-exemplo.json                                          
      248 +    --output /tmp/resultado.json` termina com código 0 e produ
          +z JSON válido;                                                
      249 +    arquivo inexistente em `--input` imprime mensagem de erro 
          +e termina com                                                 
      250 +    código 1                                                  
      251 +  - **Commit:** ` `                                           
      252 +                                                              
      253 +---                                                           
      254 +                                                              
      255 +## Fase 7 — Testes de integração e borda                      
      256 +                                                              
      257 +- [ ] **T-017** — Testes de integração: despesas-exemplo.json 
          +(`tests/test_integracao.py`)                                  
      258 +  - **O que faz:** carrega `exemplos/despesas-exemplo.json` vi
          +a path derivado de                                            
      259 +    `__file__`, chama `motor.processar()` e verifica os 17 cri
          +térios de aceite                                              
      260 +    da seção 9 da spec. Um assert por item, comentado com o id
          + (ex.:                                                        
      261 +    `# d-001`).                                               
      262 +  - **Atende:** seção 9 da spec — todos os RF                 
      263 +  - **Aceite:** todos os 17 asserts passam sem modificação do 
          +arquivo de entrada                                            
      264 +  - **Commit:** ` `                                           
      265 +                                                              
      266 +- [ ] **T-018** — Testes de casos de borda (`tests/test_borda.
          +py`)                                                          
      267 +  - **O que faz:** casos da seção 7 da spec que cruzam múltipl
          +as regras e não são                                           
      268 +    cobertos pelos testes de RF individuais:                  
      269 +    - `test_borda_dois_identicos_acima_100_sem_nf` — primeiro 
          +`SEM_NF`, segundo `DUPLICATA`                                 
      270 +    - `test_borda_item_fora_competencia_e_sem_nf` — `FORA_COMP
          +ETENCIA` vence                                                
      271 +    - `test_borda_cota_esgotada_status_recusado` — `COTA_ESGOT
          +ADA` → status `"recusado"`                                    
      272 +    - `test_borda_hospedagem_sem_nf_nao_chega_ao_limite` — d-0
          +13 recusado em SEM_NF                                         
      273 +    - `test_borda_valor_zero_recusado` — valor `0.00` → `VALOR
          +_NAO_POSITIVO`                                                
      274 +  - **Atende:** seção 7 da spec, RF-11 (interações entre passo
          +s)                                                            
      275 +  - **Aceite:** todos os 5 testes passam                      
      276 +  - **Commit:** ` `                                           
      277 +                                                              
      278 +---                                                           
      279 +                                                              
      280 +## Fase 8 — Documentação                                      
      281 +                                                              
      282 +- [ ] **T-019** — README (`README.md`)                        
      283 +  - **O que faz:** documenta pré-requisitos (Python 3.11+), in
          +stalação (`pip install                                        
      284 +    pytest`), como rodar (`python -m src.cli calcular --input 
          +despesas.json                                                 
      285 +    --output resultado.json`) e como testar (`pytest`). Inclui
          + exemplo de saída                                             
      286 +    mínimo.                                                   
      287 +  - **Atende:** penalidade de rubrica (README não permite roda
          +r → -3)                                                       
      288 +  - **Aceite:** seguindo o README, um desenvolvedor sem contex
          +to consegue rodar                                             
      289 +    e testar o projeto                                        
      290 +  - **Commit:** ` `                                           
      291 +                                                              
      292 +---                                                           
      293 +                                                              
      294 +## Fase 9 — Envelope (criar no Dia 2)                         
      295 +                                                              
      296 +> Novas tasks a partir da mudança de requisito recebida às 10h
          + do Dia 2.                                                    
      297 +> Numeração continua de T-020 em diante — não reiniciar nem re
          +numerar anteriores.                                           
      298 +                                                              
      299 +---                                                           
      300 +                                                              
      301  ## Cobertura
      302  
       51 -Preencha ao fechar cada fase. É a sua própria checagem de rast
          -reabilidade — e é                                             
       52 -exatamente a matriz que a correção vai montar.                
      303 +Preencher ao fechar cada fase.                                
      304  
      305  | Regra da spec | Task | Teste |
      306  |---|---|---|
       56 -| RN-001 | T-00X | `<nome do teste>` |                        
       57 -| RN-002 | | |                                                
       58 -| AMB-001 | | |                                               
      307 +| RF-01 | T-003, T-004 | `test_rf01_valor_original_preservado`
          +, `test_rf01_valor_inteiro_da_entrada`, `test_rf01_valor_333_n
          +ormaliza_para_33`, `test_rf01_valor_335_arredonda_para_34` |  
      308 +| RF-02 | T-005 | `test_rf02_maiusculas_reconhecidas`, `test_r
          +f02_espacos_removidos`, `test_rf02_acento_nao_normalizado` |  
      309 +| RF-03 | T-006 | `test_rf03_valor_negativo_recusado`, `test_r
          +f03_valor_zero_recusado`, `test_rf03_nao_consome_cota` |      
      310 +| RF-04 | T-007 | `test_rf04_data_anterior_recusada`, `test_rf
          +04_data_posterior_recusada`, `test_rf04_limite_inclusivo_inici
          +o`, `test_rf04_limite_inclusivo_fim` |                        
      311 +| RF-05 | T-008 | `test_rf05_coworking_recusado`, `test_rf05_c
          +ategoria_apos_normalizacao_aceita` |                          
      312 +| RF-06 | T-009 | `test_rf06_duplicata_exata_recusada`, `test_
          +rf06_primeiro_mantido`, `test_rf06_duplicata_de_recusado_ainda
          +_detectada`, `test_rf06_nao_consome_cota` |                   
      313 +| RF-07 | T-010 | `test_rf07_fronteira_100_sem_nf_passa`, `tes
          +t_rf07_fronteira_100_01_sem_nf_recusa`, `test_rf07_com_nf_pass
          +a` |                                                          
      314 +| RF-08 | T-011 | `test_rf08_agregado_diario_corte`, `test_rf0
          +8_cota_esgotada_segundo_item`, `test_rf08_dentro_do_limite_apr
          +ovado` |                                                      
      315 +| RF-09 | T-011 | `test_rf09_agregado_diario_corte`, `test_rf0
          +9_sem_nf_nao_consome_cota` |                                  
      316 +| RF-10 | T-011 | `test_rf10_limite_por_lancamento`, `test_rf1
          +0_descricao_ignorada` |                                       
      317 +| RF-11 | T-012 | `test_rf11_competencia_precede_nf`, `test_rf
          +11_duplicata_de_item_sem_nf` |                                
      318 +| RF-12 | T-011, T-012 | `test_rf12_exceder_limite_nao_recusa`
          +, `test_rf12_reembolsa_saldo_disponivel` |                    
      319 +| RF-13 | T-012 | `test_rf13_status_aprovado`, `test_rf13_stat
          +us_parcial`, `test_rf13_cota_esgotada_e_recusado` |           
      320 +| RF-14 | T-014, T-015 | `test_rf14_saidas_identicas_mesma_ent
          +rada` |                                                       
      321 +| RF-15 | T-013 | `test_rf15_sabado_processado_normalmente` | 
      322 +| RF-16 | T-013 | `test_rf16_nenhum_item_com_limite_ampliado` 
          +|                                                             
      323 +| AMB-001 | T-011 | `test_rf08_agregado_diario_corte` |       
      324 +| AMB-002 | T-011 | `test_rf09_agregado_diario_corte` |       
      325 +| AMB-003 | T-011 | `test_rf10_descricao_ignorada` |          
      326 +| AMB-004 | T-010 | `test_rf07_fronteira_100_sem_nf_passa` |  
      327 +| AMB-005 | T-010 | `test_rf07_fronteira_100_01_sem_nf_recusa`
          + |                                                            
      328 +| AMB-006 | T-013 | `test_rf16_nenhum_item_com_limite_ampliado
          +` |                                                           
      329 +| AMB-007 | T-009 | `test_rf06_duplicata_exata_recusada` |    
      330 +| AMB-008 | T-007 | `test_rf04_data_anterior_recusada` |      
      331 +| AMB-009 | T-006 | `test_rf03_valor_negativo_recusado` |     
      332 +| AMB-010 | T-004 | `test_rf01_valor_335_arredonda_para_34` | 
      333 +| AMB-011 | T-005, T-008 | `test_rf02_maiusculas_reconhecidas`
          +, `test_rf05_coworking_recusado` |                            
      334 +| AMB-012 | T-011 | `test_rf12_exceder_limite_nao_recusa` |   
      335 +| AMB-013 | T-008 | `test_rf05_coworking_recusado` |          
      336 +| AMB-014 | T-013 | `test_rf15_sabado_processado_normalmente` 
          +|                                                             
      337 +| AMB-015 | T-012 | `test_rf11_competencia_precede_nf`, `test_
          +rf11_duplicata_de_item_sem_nf` |                              
      338 +| AMB-016 | T-014, T-015 | `test_rf14_saidas_identicas_mesma_e
          +ntrada` |                                                     

● tasks.md pronto. Pontos fracos que você deve verificar:

  1. T-011 acumula 8 testes — é a maior task (cotas para 3 categorias +
  reembolso parcial). Se quiser dividir em T-011a (alimentação), T-011b
  (transporte), T-011c (hospedagem), é defensável; mantive junto porque o
  GerenciadorCotas é uma única estrutura de estado.
  2. T-013 não produz código novo — só testes que confirmam comportamento
  existente. Se isso parecer task "vazia", os testes podem ser absorvidos em
  T-017 (integração). Mantive separado para que RF-15 e RF-16 tenham
  rastreabilidade própria na tabela de cobertura.
  3. T-016 (CLI) só tem aceite manual — não há teste automatizado para o
  __main__ / argparse. O teste de integração (T-017) cobre o motor, mas não o
  argparse em si. Aceitável para o escopo.
  4. Tabela de cobertura está pré-preenchida — a instrução original diz
  "preencher ao fechar cada fase", mas preenchi antecipadamente para facilitar a
   correção. Se preferir a progressão gradual, posso deixar em branco.

  Posso commitar agora com:

  docs(tasks): tasks.md v1.0 — T-001..T-019, cobertura RF-01..RF-16

✻ Brewed for 2m 42s

> Aprovo com os 4 pontos assim: (1) T-011 unida — GerenciadorCotas é uma        
  estrutura só; (2) T-013 separada, commit como test(T-013); (3) CLI sem teste  
  automatizado aceito, coerente com o plan; (4) tabela pré-preenchida mantida — 
   a progressão gradual fica nos checkboxes das tasks. Uma correção: mover      
  test_rf09_sem_nf_nao_consome_cota do aceite da T-011 para a T-012 — ele testa 
   a interação passo 6 → passo 7, que só existe quando o pipeline conecta os    
  verificadores às cotas; na T-011 isolada não roda. Ajuste na task e na tabela 
   de cobertura, e commite com a mensagem sugerida.                             

● Update(specs\001-motor-reembolso\tasks.md)
  ⎿  Removed 1 line
      160      `test_rf08_dentro_do_limite_aprovado` — alimentação R$30,0
           0 único do dia →
      161      R$30,00, sem motivo;
      162      `test_rf09_agregado_diario_corte` — transporte R$100,00 → 
           R$80,00;
      163 -    `test_rf09_sem_nf_nao_consome_cota` — item recusado por SE
          -M_NF não reduz cota;                                          
      163      `test_rf10_limite_por_lancamento` — hospedagem R$480,00 → 
           R$250,00;
      164      `test_rf10_descricao_ignorada` — "2 diárias" na descrição 
           não altera limite;
      165      `test_rf12_exceder_limite_nao_recusa` — item cortado tem `
           valor_reembolsavel > 0`,

● Update(specs\001-motor-reembolso\tasks.md)
  ⎿  Added 2 lines
      185      sem NF → primeiro `SEM_NF`, segundo `DUPLICATA`;
      186      `test_rf12_reembolsa_saldo_disponivel` — item cortado rece
           be exatamente o
      187      saldo disponível, não zero;
      188 +    `test_rf09_sem_nf_nao_consome_cota` — item recusado por `S
          +EM_NF` não reduz                                              
      189 +    cota de transporte do dia (interação passo 6 → passo 7);  
      190      `test_rf13_status_aprovado` — `valor_reembolsavel == valor
           _considerado` →
      191      `"aprovado"`;
      192      `test_rf13_status_parcial` — `0 < valor_reembolsavel < val
           or_considerado` →

● Update(specs\001-motor-reembolso\tasks.md)
  ⎿  Added 1 line, removed 1 line
      313  | RF-06 | T-009 | `test_rf06_duplicata_exata_recusada`, `test_
           rf06_primeiro_mantido`, `test_rf06_duplicata_de_recusado_ainda
           _detectada`, `test_rf06_nao_consome_cota` |
      314  | RF-07 | T-010 | `test_rf07_fronteira_100_sem_nf_passa`, `tes
           t_rf07_fronteira_100_01_sem_nf_recusa`, `test_rf07_com_nf_pass
           a` |
      315  | RF-08 | T-011 | `test_rf08_agregado_diario_corte`, `test_rf0
           8_cota_esgotada_segundo_item`, `test_rf08_dentro_do_limite_apr
           ovado` |
      316 -| RF-09 | T-011 | `test_rf09_agregado_diario_corte`, `test_rf0
          -9_sem_nf_nao_consome_cota` |                                  
      316 +| RF-09 | T-011, T-012 | `test_rf09_agregado_diario_corte`, `t
          +est_rf09_sem_nf_nao_consome_cota` |                           
      317  | RF-10 | T-011 | `test_rf10_limite_por_lancamento`, `test_rf1
           0_descricao_ignorada` |
      318  | RF-11 | T-012 | `test_rf11_competencia_precede_nf`, `test_rf
           11_duplicata_de_item_sem_nf` |
      319  | RF-12 | T-011, T-012 | `test_rf12_exceder_limite_nao_recusa`
           , `test_rf12_reembolsa_saldo_disponivel` |

  Committed 85c701 (ctrl+o to expand)

● Commitado. 85c7014 — docs(tasks): tasks.md v1.0.

  Fase 1 da manhã concluída. Temos spec, plan e tasks commitados. Histórico
  limpo:

  85c7014  docs(tasks): tasks.md v1.0
  f8fec92  docs(plan):  plan.md v1.0
  dce0728  docs(spec):  spec.md v1.0

  Prontos para a Fase 2 (implementação). Próxima task: T-001 — setup do projeto.
   Lembre de rodar /export antes de começar a tarde para salvar esta sessão em
  docs/sessions/01-spec-plan-tasks.md.

✻ Baked for 24s