# Plano Técnico — Motor de Cálculo de Reembolso

**Versão:** 1.0 · **Baseado na spec:** 1.0 · **Última alteração:** 2026-07-29

> Aqui mora o COMO. Este arquivo pode e deve falar de linguagem, biblioteca e
> arquitetura. O que ele **não** pode é introduzir regra de negócio nova — se
> apareceu uma, ela pertence à `spec.md`.

---

## 1. Stack

| Escolha | O quê | Por quê | O que descartei e por quê |
|---|---|---|---|
| Linguagem | Python 3.11+ | Domínio do desenvolvedor; stdlib suficiente para o escopo; sem necessidade de performance extrema | Go: mais rígido para prototipagem; Node.js: ecossistema JSON nativo mas menos familiar para código financeiro |
| Testes | pytest | Fixtures, parametrize e saída legível; padrão de mercado em Python | unittest (stdlib): verboso, sem parametrize nativo; não justifica dependência adicional — mas pytest é leve o suficiente para valer |
| CLI | argparse (stdlib) | Zero dependências externas; interface simples e fixa (`calcular --input --output`) | click: mais ergonômico mas dependência extra desnecessária para uma CLI com dois argumentos |
| Parsing de JSON | json (stdlib) | Leitura e escrita de JSON sem dependência; controle total sobre serialização | pydantic: validação mais rica, mas introduz dependência e o schema de entrada é fixo e simples |
| Aritmética monetária | `decimal.Decimal` com `ROUND_HALF_UP` | Elimina erros de ponto flutuante em comparações e cálculos; implementa diretamente a decisão de arredondamento da spec (AMB-010) | `float`: `0.1 + 0.2 == 0.30000000000000004`; inaceitável para sistema financeiro auditável |

---

## 2. Arquitetura

```
despesas.json
     │
     ▼
┌─────────────────────┐
│  Leitura e parsing  │  json.load → dict Python
└─────────────────────┘
     │
     ▼
┌─────────────────────┐
│   Normalização      │  valor → Decimal(half-up, 2dp)
│   de entrada        │  categoria → lowercase + strip
└─────────────────────┘
     │  lista de DespesaNormalizada
     ▼
┌─────────────────────┐
│  Pipeline de regras │  itera despesas em ordem do arquivo;
│  (RF-11, 7 passos)  │  para no primeiro passo reprovador;
│                     │  mantém estado de cotas e duplicatas
└─────────────────────┘
     │  lista de ResultadoItem
     ▼
┌─────────────────────┐
│  Cálculo do resumo  │  agrega totais e contagens a partir dos itens
└─────────────────────┘
     │
     ▼
┌─────────────────────┐
│  Serialização JSON  │  ordem de campos explícita; Decimal → str com 2dp
│  determinística     │  (exceto valor_original, que preserva a entrada)
└─────────────────────┘
     │
     ▼
resultado.json
```

**Fronteira núcleo / I/O:** tudo entre Normalização e Cálculo do resumo é
núcleo de regra de negócio puro — sem I/O, sem dependência de sistema de
arquivos. A CLI (`cli.py`) faz apenas leitura de arquivo → chama o motor →
escreve o arquivo de saída. Isso permite testar o motor inteiro sem tocar
disco.

---

## 3. Modelo de dados

Todas as estruturas são dataclasses Python (imutáveis onde possível).

### Entrada (após parsing)

```python
@dataclass
class Colaborador:
    id: str
    nome: str
    centro_custo: str

@dataclass
class Periodo:
    competencia: str        # "2026-07"
    inicio: date            # date(2026, 7, 1)
    fim: date               # date(2026, 7, 31)

@dataclass
class DespesaBruta:
    id: str
    data: date
    categoria: str          # valor original, sem normalização
    descricao: str
    fornecedor: str
    valor_original: Decimal  # Decimal literal da entrada (ex.: Decimal("33.333"))
    tem_nota_fiscal: bool
```

### Após normalização (entrada do pipeline)

```python
@dataclass
class Despesa:
    id: str
    data: date
    categoria: str          # lowercase + strip aplicados
    descricao: str
    fornecedor: str
    valor_original: Decimal  # Decimal literal preservado da entrada (para saída)
    valor_considerado: Decimal  # half-up, 2dp
    tem_nota_fiscal: bool
```

### Saída do pipeline

```python
@dataclass
class ResultadoItem:
    id: str
    status: str             # "aprovado" | "parcial" | "recusado"
    valor_original: Decimal  # Decimal literal preservado da entrada
    valor_considerado: Decimal
    valor_reembolsavel: Decimal
    motivo_codigo: str | None
    motivo_texto: str | None
    duplicata_de: str | None
```

### Estado interno do pipeline

```python
# Controle de cotas: {(data, categoria): Decimal já consumido}
Cotas = dict[tuple[date, str], Decimal]

# Registro de itens processados para detecção de duplicatas
# Chave: tupla (data, categoria, descricao, fornecedor, valor_considerado, tem_nota_fiscal)
Vistos = dict[tuple, str]  # chave → id do item mantido
```

---

## 4. Como a política é representada

Os limites diários e o gatilho de NF vivem em **constantes no módulo de
regras** (`src/regras.py`), não espalhados pelas funções:

```python
LIMITE_DIARIO = {
    "alimentacao": Decimal("60.00"),
    "transporte_urbano": Decimal("80.00"),
    "hospedagem": Decimal("250.00"),
}
GATILHO_NF = Decimal("100.00")
```

**Por quê constantes em vez de arquivo de configuração:** o escopo atual tem
três limites fixos e um gatilho; extrair para JSON/YAML adicionaria parsing
sem benefício real. Se a política mudar (envelope do Dia 2 ou evolução
futura), editar as constantes é uma mudança cirúrgica de uma linha por limite.

**Consequência:** uma mudança de limite requer editar `regras.py` e atualizar
a spec + DECISIONS.md. Aceitável para o escopo do desafio.

---

## 5. Decisões técnicas

### DT-001 — Separação estrita entre I/O e motor de regras

**Contexto:** testes de regras de negócio não devem depender de disco.

**Decisão:** `cli.py` faz leitura/escrita de arquivo; `motor.py` recebe e
retorna estruturas Python puras. A função central é
`processar(colaborador, periodo, despesas) → Resultado`.

**Alternativa descartada:** motor que abre o arquivo diretamente — dificulta
testes unitários e viola separação de responsabilidades.

**Consequência:** testes chamam `processar()` com dados em memória; fácil e
rápido. CLI é um wrapper fino que o teste de integração pode exercitar com
arquivos temporários.

---

### DT-002 — Pipeline como sequência de funções de verificação

**Contexto:** a spec define 7 passos com ordem fixa (RF-11). O código deve
refletir essa estrutura.

**Decisão:** cada passo 2–6 é uma função `verificar_XX(despesa, contexto) →
ResultadoItem | None` que retorna o item recusado ou `None` (passou). O
passo 7 é uma função separada que recebe o estado de cotas. O pipeline em
`motor.py` itera a lista de verificadores em ordem.

**Alternativa descartada:** cadeia de `if/elif` em uma função monolítica —
dificulta teste isolado de cada regra e torna a ordem implícita no código.

**Consequência:** adicionar ou reordenar uma regra (ex.: envelope do Dia 2) é
uma mudança de uma linha na lista de verificadores do pipeline.

---

### DT-003 — Serialização JSON com ordem de campos explícita e encoder de Decimal em dois modos

**Contexto:** a spec exige saída determinística byte a byte (RF-14).
`json.dumps` em Python não garante ordem de chaves de dicts arbitrários.
`Decimal` não é serializável por padrão.

**Decisão:** serializar cada estrutura de saída para `dict` com ordem de
campos explícita (construção literal na ordem desejada), depois
`json.dumps(..., ensure_ascii=False, indent=2)` com encoder customizado.
O encoder trata `Decimal` em dois modos:
- **Modo quantizado (2dp):** campos calculados (`valor_considerado`,
  `valor_reembolsavel`, totais do resumo) → `quantize(Decimal("0.01"),
  ROUND_HALF_UP)` → serializado como número JSON com 2dp.
- **Modo literal:** `valor_original` → `normalize()` ou conversão direta para
  `float`/`int` via `str` → serializado preservando os dígitos da entrada
  (ex.: `Decimal("33.333")` → `33.333` no JSON).

**Alternativa descartada:** `dataclasses.asdict()` + `json.dumps(sort_keys=True)` —
`sort_keys` reordena alfabeticamente; `asdict` não controla ordem customizada.

**Consequência:** qualquer mudança no schema de saída requer editar o
serializador explicitamente — mas garante auditabilidade e previsibilidade.

---

### DT-004 — Parsing de `valor` com `parse_float=Decimal`

**Contexto:** a spec exige que `valor_original` ecoe o valor da entrada sem
normalização e que `valor_considerado` seja o arredondamento half-up a 2dp
(RF-01). O aceite inclui `33.335 → valor_considerado 33.34`.

**Problema com float nativo:** `json.load` padrão converte `33.335` para o
float Python `33.334999...`. `Decimal(33.334999...)` com `ROUND_HALF_UP` dá
`33.33`, violando o aceite. O erro não aparece em valores "redondos" e é
silencioso — detectável apenas pelo teste `test_rf01_valor_335_arredonda_para_34`.

**Decisão:** `json.load(f, parse_float=Decimal, parse_int=Decimal)` — tanto
números fracionários quanto inteiros passam pelo construtor `Decimal` a partir
da string literal. `Decimal("33.335")` é exato; `Decimal("480")` é uniforme.
`valor_original` armazena esse `Decimal` literal; `valor_considerado` é
`valor_original.quantize(Decimal("0.01"), ROUND_HALF_UP)`. Ambos são
`Decimal`; o encoder os trata em modos diferentes (DT-003).

**Alternativa descartada:** `parse_float=Decimal` sem `parse_int=Decimal` —
inteiros chegam como `int` Python, quebrando a uniformidade do modelo
(`valor_original: Decimal`) e exigindo tratamento especial no normalizador e
no encoder.

**Consequência:** `valor_original` é sempre `Decimal`. O encoder serializa
`Decimal("480")` como `480` (sem casas) e `Decimal("33.333")` como `33.333`
para `valor_original`, preservando a forma da entrada em ambos os casos.

---

### DT-005 — Estrutura de diretórios

```
src/
  __init__.py
  cli.py          ← argparse; lê arquivo, chama motor, escreve saída
  motor.py        ← processar(): orquestra normalização → pipeline → resumo
  regras.py       ← verificadores de cada passo + constantes de limite
  modelos.py      ← dataclasses de entrada e saída
  serializador.py ← dict de saída com ordem explícita + encoder JSON
tests/
  conftest.py     ← fixtures: periodo padrão, colaborador padrão, helpers
  test_rf01_normalizacao_valor.py
  test_rf02_normalizacao_categoria.py
  test_rf03_dominio_valor.py
  test_rf04_competencia.py
  test_rf05_categoria_invalida.py
  test_rf06_duplicatas.py
  test_rf07_nota_fiscal.py
  test_rf08_limite_alimentacao.py
  test_rf09_limite_transporte.py
  test_rf10_limite_hospedagem.py
  test_rf11_ordem_regras.py
  test_rf12_reembolso_parcial.py
  test_rf13_status_derivado.py
  test_rf14_determinismo.py
  test_rf15_fim_de_semana.py
  test_rf16_viagem_suspensa.py
  test_borda.py   ← casos da seção 7 da spec que cruzam múltiplas regras
  test_integracao.py ← processa despesas-exemplo.json completo, verifica cada item
```

**Alternativa descartada:** um único `test_motor.py` — perde rastreabilidade
direta entre teste e RF; dificulta localizar falha na correção.

---

## 6. Estratégia de testes

**Proporção:** ~80% unitários (regras isoladas), ~20% integração (arquivo
completo). Nenhum teste de ponta a ponta via CLI nos testes automatizados —
a CLI é exercitada manualmente pelo README.

**Nomenclatura:** `test_rfXX_<descricao_do_aceite>` para testes de RF;
`test_borda_<caso>` para casos da seção 7 que cruzam regras.

**Cobertura obrigatória por RF:**

| RF | Teste(s) obrigatório(s) |
|---|---|
| RF-01 | `test_rf01_valor_333_normaliza_para_33`, `test_rf01_valor_335_arredonda_para_34`, `test_rf01_valor_original_preservado`, `test_rf01_valor_inteiro_da_entrada` (480 → `valor_original: Decimal("480")`, `valor_considerado: Decimal("480.00")`) |
| RF-02 | `test_rf02_maiusculas_reconhecidas`, `test_rf02_espacos_removidos`, `test_rf02_acento_nao_normalizado` |
| RF-03 | `test_rf03_valor_negativo_recusado`, `test_rf03_valor_zero_recusado`, `test_rf03_nao_consome_cota` |
| RF-04 | `test_rf04_data_anterior_recusada`, `test_rf04_data_posterior_recusada`, `test_rf04_limite_inclusivo_inicio`, `test_rf04_limite_inclusivo_fim` |
| RF-05 | `test_rf05_coworking_recusado`, `test_rf05_categoria_apos_normalizacao_aceita` |
| RF-06 | `test_rf06_duplicata_exata_recusada`, `test_rf06_primeiro_mantido`, `test_rf06_duplicata_de_recusado_ainda_detectada`, `test_rf06_nao_consome_cota` |
| RF-07 | `test_rf07_fronteira_100_sem_nf_passa`, `test_rf07_fronteira_100_01_sem_nf_recusa`, `test_rf07_com_nf_passa` |
| RF-08 | `test_rf08_agregado_diario_corte`, `test_rf08_cota_esgotada_segundo_item`, `test_rf08_dentro_do_limite_aprovado` |
| RF-09 | `test_rf09_agregado_diario_corte`, `test_rf09_sem_nf_nao_consome_cota` |
| RF-10 | `test_rf10_limite_por_lancamento`, `test_rf10_descricao_ignorada` |
| RF-11 | `test_rf11_competencia_precede_nf`, `test_rf11_duplicata_de_item_sem_nf` |
| RF-12 | `test_rf12_exceder_limite_nao_recusa`, `test_rf12_reembolsa_saldo_disponivel` |
| RF-13 | `test_rf13_status_aprovado`, `test_rf13_status_parcial`, `test_rf13_cota_esgotada_e_recusado` |
| RF-14 | `test_rf14_saidas_identicas_mesma_entrada` |
| RF-15 | `test_rf15_sabado_processado_normalmente` |
| RF-16 | `test_rf16_nenhum_item_com_limite_ampliado` |

**Integração (`test_integracao.py`):** carrega `exemplos/despesas-exemplo.json`,
chama `processar()` e verifica cada um dos 17 critérios de aceite da seção 9
da spec. Um assert por critério, nomeado com o id do item (ex.:
`assert resultado.itens[0].motivo_codigo == "LIMITE_DIARIO"  # d-001`).

**Fixtures em `conftest.py`:**
- `periodo_padrao`: `Periodo(competencia="2026-07", inicio=date(2026,7,1), fim=date(2026,7,31))`
- `colaborador_padrao`: `Colaborador(id="c-0001", nome="Teste", centro_custo="CC-TEST")`
- `despesa_factory`: função que cria `Despesa` com defaults sobrescrevíveis por kwarg

---

## 7. Riscos

| Risco | Probabilidade | O que faço se acontecer |
|---|---|---|
| Envelope do Dia 2 exige novo campo no schema de entrada | Alta (campo `em_viagem` ou `num_diarias` são candidatos óbvios) | Adicionar campo opcional ao parsing com default; regra nova entra como passo no pipeline; constante nova em `regras.py` |
| Envelope exige nova categoria reembolsável | Média | Adicionar à lista canônica em `regras.py` + novo limite em `LIMITE_DIARIO` |
| Serialização JSON não garante 2dp para Decimal em edge case | Baixa | Encoder customizado já cobre; teste `test_rf14_saidas_identicas_mesma_entrada` detecta |
| `parse_int=Decimal` intercepta campos não-monetários (ex.: `itens_processados` na saída) | Baixa | `parse_float` e `parse_int` afetam apenas a leitura da entrada; a saída é construída diretamente de `Decimal` e `int` Python — não há conflito |
