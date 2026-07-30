# Tasks — Motor de Cálculo de Reembolso

> Cada task é pequena o bastante para virar **um commit**. Se você não consegue
> descrever o critério de aceite como "o teste X passa", a task está grande demais.
>
> Marque `[x]` conforme conclui — ao longo do caminho, não tudo no fim. O histórico
> de quando cada task foi marcada é lido na correção.

**Formato do commit:** `feat(T-003): <descrição>` · `test(T-003): <descrição>`
Documentação: `docs(spec):` · `docs(plan):` · `docs(tasks):`

---

## Fase 1 — Fundação (setup e modelos)

- [x] **T-001** — Estrutura de diretórios e configuração de testes
  - **O que faz:** cria `src/__init__.py`, `tests/__init__.py`, `tests/conftest.py`
    com fixtures `periodo_padrao`, `colaborador_padrao` e `despesa_factory`;
    cria `pytest.ini` ou `pyproject.toml` com `testpaths = tests`.
  - **Atende:** DT-005 (estrutura de diretórios)
  - **Aceite:** `pytest` coleta 0 testes sem erro; fixtures importáveis
  - **Commit:** ` `

- [x] **T-002** — Modelos de dados (`src/modelos.py`)
  - **O que faz:** define os dataclasses `Colaborador`, `Periodo`, `DespesaBruta`,
    `Despesa`, `ResultadoItem` e `Resultado` conforme o modelo de dados do plan.
    Todos os campos monetários tipados como `Decimal`.
  - **Atende:** DT-005; base para RF-01 a RF-16
  - **Aceite:** `from src.modelos import Despesa, ResultadoItem` importa sem erro;
    instanciação manual com valores Decimal funciona
  - **Commit:** ` `

- [ ] **T-003** — Parsing da entrada com `parse_float=Decimal, parse_int=Decimal`
    (`src/parser.py`)
  - **O que faz:** função `carregar_entrada(caminho) → tuple[Colaborador, Periodo,
    list[DespesaBruta]]` que lê JSON via `json.load(f, parse_float=Decimal,
    parse_int=Decimal)`; converte `data` para `date`; armazena `valor` como
    `Decimal` literal sem arredondar.
  - **Atende:** RF-01 (parcial — preservação de `valor_original`), DT-004
  - **Aceite:** `test_rf01_valor_original_preservado` —
    entrada com `"valor": 33.333` → `despesa_bruta.valor_original == Decimal("33.333")`;
    `test_rf01_valor_inteiro_da_entrada` —
    entrada com `"valor": 480` → `despesa_bruta.valor_original == Decimal("480")`
  - **Commit:** ` `

---

## Fase 2 — Normalização

- [ ] **T-004** — Normalização de valor monetário (`src/normalizacao.py`)
  - **O que faz:** função `normalizar_valor(v: Decimal) → Decimal` que aplica
    `quantize(Decimal("0.01"), ROUND_HALF_UP)`. Ponto único de arredondamento
    em todo o sistema.
  - **Atende:** RF-01, AMB-010
  - **Aceite:**
    `test_rf01_valor_333_normaliza_para_33` — `normalizar_valor(Decimal("33.333")) == Decimal("33.33")`;
    `test_rf01_valor_335_arredonda_para_34` — `normalizar_valor(Decimal("33.335")) == Decimal("33.34")`
  - **Commit:** ` `

- [ ] **T-005** — Normalização de categoria (`src/normalizacao.py`)
  - **O que faz:** função `normalizar_categoria(c: str) → str` que aplica
    `c.strip().lower()`. Sem normalização de acentos ou correção ortográfica.
  - **Atende:** RF-02, AMB-011
  - **Aceite:**
    `test_rf02_maiusculas_reconhecidas` — `normalizar_categoria("ALIMENTACAO") == "alimentacao"`;
    `test_rf02_espacos_removidos` — `normalizar_categoria(" Alimentacao ") == "alimentacao"`;
    `test_rf02_acento_nao_normalizado` — `normalizar_categoria("Alimentação") == "alimentação"`
  - **Commit:** ` `

---

## Fase 3 — Verificadores de recusa (passos 2–6 do RF-11)

- [ ] **T-006** — Verificador passo 2: domínio de valor (`src/regras.py`)
  - **O que faz:** função `verificar_dominio_valor(despesa) → ResultadoItem | None`
    que retorna item recusado com `VALOR_NAO_POSITIVO` se
    `valor_considerado ≤ 0`, ou `None` se passou.
  - **Atende:** RF-03, AMB-009
  - **Aceite:**
    `test_rf03_valor_negativo_recusado` — valor `-45.00` → `motivo_codigo == "VALOR_NAO_POSITIVO"`,
    `valor_reembolsavel == Decimal("0.00")`;
    `test_rf03_valor_zero_recusado` — valor `0.00` → recusado;
    `test_rf03_nao_consome_cota` — item recusado não altera estado de cotas
  - **Commit:** ` `

- [ ] **T-007** — Verificador passo 3: competência (`src/regras.py`)
  - **O que faz:** função `verificar_competencia(despesa, periodo) → ResultadoItem | None`
    que retorna `FORA_COMPETENCIA` se `despesa.data < periodo.inicio` ou
    `despesa.data > periodo.fim`.
  - **Atende:** RF-04, AMB-008
  - **Aceite:**
    `test_rf04_data_anterior_recusada` — data `2026-04-15`, período `2026-07-01/31` → recusada;
    `test_rf04_data_posterior_recusada` — data `2026-08-01` → recusada;
    `test_rf04_limite_inclusivo_inicio` — data `2026-07-01` → passa;
    `test_rf04_limite_inclusivo_fim` — data `2026-07-31` → passa
  - **Commit:** ` `

- [ ] **T-008** — Verificador passo 4: categoria inválida (`src/regras.py`)
  - **O que faz:** define constante `CATEGORIAS_VALIDAS = {"alimentacao",
    "transporte_urbano", "hospedagem"}` em `regras.py`; função
    `verificar_categoria(despesa) → ResultadoItem | None` que retorna
    `CATEGORIA_INVALIDA` com `motivo_texto = "categoria fora da política: <valor>"`.
  - **Atende:** RF-05, AMB-011, AMB-013
  - **Aceite:**
    `test_rf05_coworking_recusado` — categoria `"coworking"` → `CATEGORIA_INVALIDA`,
    texto contém `"coworking"`;
    `test_rf05_categoria_apos_normalizacao_aceita` — `"ALIMENTACAO"` normalizada →
    passa no verificador
  - **Commit:** ` `

- [ ] **T-009** — Verificador passo 5: duplicatas (`src/regras.py`)
  - **O que faz:** função `verificar_duplicata(despesa, vistos: dict) → ResultadoItem | None`
    que constrói chave `(data, categoria, descricao, fornecedor, valor_considerado,
    tem_nota_fiscal)`; se chave já existe em `vistos`, retorna `DUPLICATA` com
    `duplicata_de = vistos[chave]`; senão, registra `vistos[chave] = despesa.id`.
    Verificação ocorre independentemente do status do item original.
  - **Atende:** RF-06, AMB-007
  - **Aceite:**
    `test_rf06_duplicata_exata_recusada` — d-006/d-007 idênticos → segundo recusado
    com `duplicata_de == "d-006"`;
    `test_rf06_primeiro_mantido` — primeiro item nunca é recusado como duplicata;
    `test_rf06_duplicata_de_recusado_ainda_detectada` — segundo item idêntico a
    item já recusado por outro motivo → ainda recusado como `DUPLICATA`;
    `test_rf06_nao_consome_cota` — duplicata recusada não afeta cotas
  - **Commit:** ` `

- [ ] **T-010** — Verificador passo 6: nota fiscal (`src/regras.py`)
  - **O que faz:** define constante `GATILHO_NF = Decimal("100.00")`; função
    `verificar_nf(despesa) → ResultadoItem | None` que retorna `SEM_NF` se
    `despesa.valor_considerado > GATILHO_NF` e `not despesa.tem_nota_fiscal`.
  - **Atende:** RF-07, AMB-004, AMB-005
  - **Aceite:**
    `test_rf07_fronteira_100_sem_nf_passa` — valor `100.00`, sem NF → passa (não é
    `> 100.00`);
    `test_rf07_fronteira_100_01_sem_nf_recusa` — valor `100.01`, sem NF → `SEM_NF`;
    `test_rf07_com_nf_passa` — valor `150.00`, com NF → passa
  - **Commit:** ` `

---

## Fase 4 — Passo 7: cotas diárias

- [ ] **T-011** — Cálculo de cotas diárias e reembolso parcial (`src/cotas.py`)
  - **O que faz:** classe ou módulo `GerenciadorCotas` com estado
    `dict[(date, str), Decimal]` (consumido por dia/categoria); define constantes
    `LIMITE_DIARIO = {"alimentacao": Decimal("60.00"), "transporte_urbano":
    Decimal("80.00"), "hospedagem": Decimal("250.00")}`; método
    `calcular_reembolso(despesa) → tuple[Decimal, str]` que retorna
    `(valor_reembolsavel, motivo_codigo)`:
    - saldo > 0 e valor > saldo → reembolsa saldo, `LIMITE_DIARIO`
    - saldo = 0 → reembolsa 0, `COTA_ESGOTADA`
    - saldo ≥ valor → reembolsa integralmente, `None`
    Atualiza estado interno ao reembolsar.
  - **Atende:** RF-08, RF-09, RF-10, RF-12, AMB-001, AMB-002, AMB-003, AMB-012
  - **Aceite:**
    `test_rf08_agregado_diario_corte` — alimentação R$72,50 primeiro do dia →
    reembolsa R$60,00, `LIMITE_DIARIO`;
    `test_rf08_cota_esgotada_segundo_item` — alimentação R$38,00 após R$60,00
    consumidos → R$0,00, `COTA_ESGOTADA`;
    `test_rf08_dentro_do_limite_aprovado` — alimentação R$30,00 único do dia →
    R$30,00, sem motivo;
    `test_rf09_agregado_diario_corte` — transporte R$100,00 → R$80,00;
    `test_rf10_limite_por_lancamento` — hospedagem R$480,00 → R$250,00;
    `test_rf10_descricao_ignorada` — "2 diárias" na descrição não altera limite;
    `test_rf12_exceder_limite_nao_recusa` — item cortado tem `valor_reembolsavel > 0`,
    nunca recusado só por exceder
  - **Commit:** ` `

---

## Fase 5 — Pipeline e status

- [ ] **T-012** — Pipeline completo e status derivado (`src/motor.py`)
  - **O que faz:** função `processar(colaborador, periodo, despesas_brutas) →
    Resultado` que: (1) normaliza cada `DespesaBruta` → `Despesa`; (2) aplica
    os verificadores dos passos 2–6 em ordem, parando no primeiro que retorna
    recusa; (3) aplica passo 7 via `GerenciadorCotas`; (4) deriva `status` a
    partir dos valores (`aprovado` / `parcial` / `recusado` — RF-13); (5) constrói
    `Resultado` com lista de itens em ordem da entrada.
  - **Atende:** RF-11, RF-13, AMB-015
  - **Aceite:**
    `test_rf11_competencia_precede_nf` — item fora de competência E sem NF →
    `FORA_COMPETENCIA` (não `SEM_NF`);
    `test_rf11_duplicata_de_item_sem_nf` — dois itens idênticos com valor > 100
    sem NF → primeiro `SEM_NF`, segundo `DUPLICATA`;
    `test_rf12_reembolsa_saldo_disponivel` — item cortado recebe exatamente o
    saldo disponível, não zero;
    `test_rf09_sem_nf_nao_consome_cota` — item recusado por `SEM_NF` não reduz
    cota de transporte do dia (interação passo 6 → passo 7);
    `test_rf13_status_aprovado` — `valor_reembolsavel == valor_considerado` →
    `"aprovado"`;
    `test_rf13_status_parcial` — `0 < valor_reembolsavel < valor_considerado` →
    `"parcial"`;
    `test_rf13_cota_esgotada_e_recusado` — `COTA_ESGOTADA` com
    `valor_reembolsavel == 0` → `status == "recusado"`
  - **Commit:** ` `

- [ ] **T-013** — Testes de RF-15 e RF-16 (dias da semana e viagem)
  - **O que faz:** adiciona `tests/test_rf15_fim_de_semana.py` e
    `tests/test_rf16_viagem_suspensa.py`. Não requer novo código — os testes
    exercitam o pipeline existente para confirmar comportamento declarado na spec.
  - **Atende:** RF-15 (AMB-014), RF-16 (AMB-006)
  - **Aceite:**
    `test_rf15_sabado_processado_normalmente` — despesa de sábado (d-012) →
    `status == "aprovado"`, `valor_reembolsavel == Decimal("47.20")`;
    `test_rf16_nenhum_item_com_limite_ampliado` — nenhum item do lote de exemplo
    tem `valor_reembolsavel > 60.00` por categoria alimentação (limite nunca
    ampliado para 90,00)
  - **Commit:** ` `

---

## Fase 6 — Resumo, serializador e CLI

- [ ] **T-014** — Cálculo do resumo agregado (`src/motor.py`)
  - **O que faz:** após construir a lista de itens, calcula `Resumo`:
    `total_solicitado = Σ valor_considerado` dos itens com `valor_considerado > 0`;
    `total_reembolsavel = Σ valor_reembolsavel`; `total_recusado = total_solicitado
    - total_reembolsavel`; contagens por status.
  - **Atende:** RF-14 (parcial), AMB-016
  - **Aceite:** processando d-001 (parcial R$60) + d-005 (recusado R$0) + d-006
    (aprovado R$54,90) → `total_solicitado == Decimal("216.40")`,
    `total_reembolsavel == Decimal("114.90")`,
    `itens_aprovados == 1`, `itens_parciais == 1`, `itens_recusados == 1`
  - **Commit:** ` `

- [ ] **T-015** — Serializador determinístico (`src/serializador.py`)
  - **O que faz:** função `serializar(resultado: Resultado) → str` que constrói
    `dict` com ordem de campos explícita e aplica `json.dumps(ensure_ascii=False,
    indent=2)`. Encoder customizado: campos calculados → `quantize("0.01")` → número
    JSON com 2dp; `valor_original` → número JSON com dígitos literais da entrada;
    contagens inteiras → `int`.
  - **Atende:** RF-14, DT-003, AMB-016
  - **Aceite:**
    `test_rf14_saidas_identicas_mesma_entrada` — chamar `serializar()` duas vezes
    com o mesmo `Resultado` produz strings idênticas;
    campos de `valor_original` no JSON preservam `33.333` (não `33.33`);
    campos calculados têm exatamente 2 casas decimais
  - **Commit:** ` `

- [ ] **T-016** — CLI com argparse (`src/cli.py`)
  - **O que faz:** entry point `python -m src.cli calcular --input <arq>
    --output <arq>` que carrega entrada via `parser.carregar_entrada()`,
    chama `motor.processar()`, serializa via `serializador.serializar()` e
    escreve o arquivo de saída. Erros de entrada inválida produzem mensagem
    clara, não traceback.
  - **Atende:** DT-001 (separação I/O / motor), interface do DESAFIO.md
  - **Aceite:** `python -m src.cli calcular --input exemplos/despesas-exemplo.json
    --output /tmp/resultado.json` termina com código 0 e produz JSON válido;
    arquivo inexistente em `--input` imprime mensagem de erro e termina com
    código 1
  - **Commit:** ` `

---

## Fase 7 — Testes de integração e borda

- [ ] **T-017** — Testes de integração: despesas-exemplo.json (`tests/test_integracao.py`)
  - **O que faz:** carrega `exemplos/despesas-exemplo.json` via path derivado de
    `__file__`, chama `motor.processar()` e verifica os 17 critérios de aceite
    da seção 9 da spec. Um assert por item, comentado com o id (ex.:
    `# d-001`).
  - **Atende:** seção 9 da spec — todos os RF
  - **Aceite:** todos os 17 asserts passam sem modificação do arquivo de entrada
  - **Commit:** ` `

- [ ] **T-018** — Testes de casos de borda (`tests/test_borda.py`)
  - **O que faz:** casos da seção 7 da spec que cruzam múltiplas regras e não são
    cobertos pelos testes de RF individuais:
    - `test_borda_dois_identicos_acima_100_sem_nf` — primeiro `SEM_NF`, segundo `DUPLICATA`
    - `test_borda_item_fora_competencia_e_sem_nf` — `FORA_COMPETENCIA` vence
    - `test_borda_cota_esgotada_status_recusado` — `COTA_ESGOTADA` → status `"recusado"`
    - `test_borda_hospedagem_sem_nf_nao_chega_ao_limite` — d-013 recusado em SEM_NF
    - `test_borda_valor_zero_recusado` — valor `0.00` → `VALOR_NAO_POSITIVO`
  - **Atende:** seção 7 da spec, RF-11 (interações entre passos)
  - **Aceite:** todos os 5 testes passam
  - **Commit:** ` `

---

## Fase 8 — Documentação

- [ ] **T-019** — README (`README.md`)
  - **O que faz:** documenta pré-requisitos (Python 3.11+), instalação (`pip install
    pytest`), como rodar (`python -m src.cli calcular --input despesas.json
    --output resultado.json`) e como testar (`pytest`). Inclui exemplo de saída
    mínimo.
  - **Atende:** penalidade de rubrica (README não permite rodar → -3)
  - **Aceite:** seguindo o README, um desenvolvedor sem contexto consegue rodar
    e testar o projeto
  - **Commit:** ` `

---

## Fase 9 — Envelope (criar no Dia 2)

> Novas tasks a partir da mudança de requisito recebida às 10h do Dia 2.
> Numeração continua de T-020 em diante — não reiniciar nem renumerar anteriores.

---

## Cobertura

Preencher ao fechar cada fase.

| Regra da spec | Task | Teste |
|---|---|---|
| RF-01 | T-003, T-004 | `test_rf01_valor_original_preservado`, `test_rf01_valor_inteiro_da_entrada`, `test_rf01_valor_333_normaliza_para_33`, `test_rf01_valor_335_arredonda_para_34` |
| RF-02 | T-005 | `test_rf02_maiusculas_reconhecidas`, `test_rf02_espacos_removidos`, `test_rf02_acento_nao_normalizado` |
| RF-03 | T-006 | `test_rf03_valor_negativo_recusado`, `test_rf03_valor_zero_recusado`, `test_rf03_nao_consome_cota` |
| RF-04 | T-007 | `test_rf04_data_anterior_recusada`, `test_rf04_data_posterior_recusada`, `test_rf04_limite_inclusivo_inicio`, `test_rf04_limite_inclusivo_fim` |
| RF-05 | T-008 | `test_rf05_coworking_recusado`, `test_rf05_categoria_apos_normalizacao_aceita` |
| RF-06 | T-009 | `test_rf06_duplicata_exata_recusada`, `test_rf06_primeiro_mantido`, `test_rf06_duplicata_de_recusado_ainda_detectada`, `test_rf06_nao_consome_cota` |
| RF-07 | T-010 | `test_rf07_fronteira_100_sem_nf_passa`, `test_rf07_fronteira_100_01_sem_nf_recusa`, `test_rf07_com_nf_passa` |
| RF-08 | T-011 | `test_rf08_agregado_diario_corte`, `test_rf08_cota_esgotada_segundo_item`, `test_rf08_dentro_do_limite_aprovado` |
| RF-09 | T-011, T-012 | `test_rf09_agregado_diario_corte`, `test_rf09_sem_nf_nao_consome_cota` |
| RF-10 | T-011 | `test_rf10_limite_por_lancamento`, `test_rf10_descricao_ignorada` |
| RF-11 | T-012 | `test_rf11_competencia_precede_nf`, `test_rf11_duplicata_de_item_sem_nf` |
| RF-12 | T-011, T-012 | `test_rf12_exceder_limite_nao_recusa`, `test_rf12_reembolsa_saldo_disponivel` |
| RF-13 | T-012 | `test_rf13_status_aprovado`, `test_rf13_status_parcial`, `test_rf13_cota_esgotada_e_recusado` |
| RF-14 | T-014, T-015 | `test_rf14_saidas_identicas_mesma_entrada` |
| RF-15 | T-013 | `test_rf15_sabado_processado_normalmente` |
| RF-16 | T-013 | `test_rf16_nenhum_item_com_limite_ampliado` |
| AMB-001 | T-011 | `test_rf08_agregado_diario_corte` |
| AMB-002 | T-011 | `test_rf09_agregado_diario_corte` |
| AMB-003 | T-011 | `test_rf10_descricao_ignorada` |
| AMB-004 | T-010 | `test_rf07_fronteira_100_sem_nf_passa` |
| AMB-005 | T-010 | `test_rf07_fronteira_100_01_sem_nf_recusa` |
| AMB-006 | T-013 | `test_rf16_nenhum_item_com_limite_ampliado` |
| AMB-007 | T-009 | `test_rf06_duplicata_exata_recusada` |
| AMB-008 | T-007 | `test_rf04_data_anterior_recusada` |
| AMB-009 | T-006 | `test_rf03_valor_negativo_recusado` |
| AMB-010 | T-004 | `test_rf01_valor_335_arredonda_para_34` |
| AMB-011 | T-005, T-008 | `test_rf02_maiusculas_reconhecidas`, `test_rf05_coworking_recusado` |
| AMB-012 | T-011 | `test_rf12_exceder_limite_nao_recusa` |
| AMB-013 | T-008 | `test_rf05_coworking_recusado` |
| AMB-014 | T-013 | `test_rf15_sabado_processado_normalmente` |
| AMB-015 | T-012 | `test_rf11_competencia_precede_nf`, `test_rf11_duplicata_de_item_sem_nf` |
| AMB-016 | T-014, T-015 | `test_rf14_saidas_identicas_mesma_entrada` |
