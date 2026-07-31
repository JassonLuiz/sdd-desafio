 ▐▛███▜▌   Claude Code v2.1.138
▝▜█████▛▘  Sonnet 4.6 · Claude Pro
  ▘▘ ▝▝    ~\OneDrive\Documentos\Estudos\Projeto NTT DATA IA\sdd-desafio

  Opus 4.7 xhigh is now available! · /model to switch
  ⎿  Read specs\001-motor-reembolso\DECISIONS.md (314 lines)
  ⎿  Read src\motor.py (160 lines)
  ⎿  Read tests\test_rf05_categoria.py (70 lines)
  ⎿  Read src\regras.py (69 lines)
  ⎿  Read tests\test_rf18_motor.py (107 lines)

● Lendo tasks.md e os testes existentes de RF-07 para confirmar o escopo antes
  de tocar no código.

  Searched for 2 patterns, read 1 file (ctrl+o to expand)

● Verificando se GATILHO_NF é importada em algum outro lugar antes de removê-la.

  Searched for 2 patterns (ctrl+o to expand)

● GATILHO_NF só existe em regras.py. Vou aplicar as três mudanças de T-026 em
  paralelo.

● Update(src\regras.py)
  ⎿  Added 3 lines, removed 6 lines
      22      return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").r
          eplace("X", ".")
      23  
      24  
      25 -GATILHO_NF = Decimal("100.00")                                 
      26 -                                                               
      27 -                                                               
      28 -def verificar_nf(despesa: Despesa) -> ResultadoItem | None:    
      29 -    if despesa.valor_considerado > GATILHO_NF and not despesa.t
         -em_nota_fiscal:                                                
      30 -        texto = f"nota fiscal obrigatória para valor acima de R
         -$ 100,00 (valor: {fmt_valor(despesa.valor_considerado)})"      
      25 +def verificar_nf(despesa: Despesa, gatilho_nf: Decimal) -> Resu
         +ltadoItem | None:                                              
      26 +    if despesa.valor_considerado > gatilho_nf and not despesa.t
         +em_nota_fiscal:                                                
      27 +        texto = f"nota fiscal obrigatória para valor acima de {
         +fmt_valor(gatilho_nf)} (valor: {fmt_valor(despesa.valor_conside
         +rado)})"                                                       
      28          return _recusar(despesa, "SEM_NF", texto)
      29      return None
      30  

● Update(src\motor.py)
  ⎿  Added 2 lines
      67      despesas_brutas: list[DespesaBruta],
      68      tabela_cambio: dict | None = None,
      69      politica_eff: dict | None = None,
      70 +    gatilho_nf: Decimal | None = None,                         
      71  ) -> Resultado:
      72      _eff = politica_eff if politica_eff is not None else _POLIT
          ICA_V3
      73 +    _gnf = gatilho_nf if gatilho_nf is not None else Decimal("1
         +00.00")                                                        
      74      if tabela_cambio is None and any(b.moeda != "BRL" for b in 
          despesas_brutas):
      75          raise ValueError(
      76              "tabela_cambio é obrigatória quando o lote contém d
          espesas em moeda estrangeira"

● Update(src\motor.py)
  ⎿  Added 1 line, removed 1 line
      119          item = item or verificar_competencia(despesa, periodo)
      120          item = item or verificar_categoria(despesa, _eff)
      121          item = item or verificar_duplicata(despesa, vistos)
      122 -        item = item or verificar_nf(despesa)                  
      122 +        item = item or verificar_nf(despesa, _gnf)            
      123  
      124          if item is None:
      125              valor_reembolsavel, motivo_codigo = gc.calcular_re
           embolso(despesa)

● Agora atualizo os testes existentes e adiciono os dois novos:

● Write(tests\test_rf07_nota_fiscal.py)
  ⎿  Added 22 lines, removed 3 lines
       2  
       3  from src.regras import verificar_nf
       4  
       5 +_GATILHO = Decimal("100.00")                                   
       6  
       7 +                                                               
       8  def test_rf07_fronteira_100_sem_nf_passa(despesa_factory):
       9      despesa = despesa_factory(valor=Decimal("100.00"), tem_nota
          _fiscal=False)
       8 -    assert verificar_nf(despesa) is None                       
      10 +    assert verificar_nf(despesa, _GATILHO) is None             
      11  
      12  
      13  def test_rf07_fronteira_100_01_sem_nf_recusa(despesa_factory):
      14      despesa = despesa_factory(valor=Decimal("100.01"), tem_nota
          _fiscal=False)
      13 -    resultado = verificar_nf(despesa)                          
      15 +    resultado = verificar_nf(despesa, _GATILHO)                
      16      assert resultado is not None
      17      assert resultado.motivo_codigo == "SEM_NF"
      18      assert resultado.valor_reembolsavel == Decimal("0.00")
     ...
      20  
      21  def test_rf07_com_nf_passa(despesa_factory):
      22      despesa = despesa_factory(valor=Decimal("150.00"), tem_nota
          _fiscal=True)
      21 -    assert verificar_nf(despesa) is None                       
      23 +    assert verificar_nf(despesa, _GATILHO) is None             
      24 +                                                               
      25 +                                                               
      26 +def test_rf07_gatilho_lido_da_politica(despesa_factory):       
      27 +    # gatilho 100,00 passado explicitamente — fronteira idêntic
         +a ao hardcoded anterior                                        
      28 +    gatilho = Decimal("100.00")                                
      29 +    assert verificar_nf(despesa_factory(valor=Decimal("100.00")
         +, tem_nota_fiscal=False), gatilho) is None                     
      30 +    resultado = verificar_nf(despesa_factory(valor=Decimal("100
         +.01"), tem_nota_fiscal=False), gatilho)                        
      31 +    assert resultado is not None                               
      32 +    assert resultado.motivo_codigo == "SEM_NF"                 
      33 +                                                               
      34 +                                                               
      35 +def test_rf07_gatilho_alternativo(despesa_factory):            
      36 +    # com gatilho 50,00, R$50,01 sem NF deve ser recusado      
      37 +    gatilho = Decimal("50.00")                                 
      38 +    resultado = verificar_nf(despesa_factory(valor=Decimal("50.
         +01"), tem_nota_fiscal=False), gatilho)                         
      39 +    assert resultado is not None                               
      40 +    assert resultado.motivo_codigo == "SEM_NF"                 

  Ran 2 shell commands (ctrl+o to expand)

● 102 passando. Antes de sugerir o commit, dois pontos para você verificar:

  O que mudou em T-026:
  1. GATILHO_NF removido de regras.py; verificar_nf agora exige gatilho_nf: 
  Decimal
  2. processar ganhou gatilho_nf: Decimal | None = None; fallback inline
  Decimal("100.00") (mesmo padrão do _POLITICA_V3) — será removido em T-028
  junto com o outro fallback
  3. motivo_texto do SEM_NF agora interpola o gatilho: "nota fiscal obrigatória 
  para valor acima de R$ 100,00..." — se o gatilho mudar, o texto reflete

  Ponto fraco para você checar: o motivo_texto agora usa fmt_valor(gatilho_nf)
  em vez do literal "R$ 100,00". Os testes existentes de RF-07 não verificam o
  texto (só motivo_codigo), então não há regressão — mas se algum teste de
  integração posterior verificar o texto exato do SEM_NF, precisará usar o valor
   da política, não um hardcoded.

  Mensagem de commit sugerida: feat(T-026): verificar_nf com limiar da política

✻ Worked for 7m 6s

> Enquanto os testes rodam: o default Decimal("100.00") para gatilho_nf em      
  processar() é o mesmo padrão de scaffolding do _POLITICA_V3 (D-014) — precisa 
   de uma entrada própria no DECISIONS.md, ou você vai consolidar os dois num   
  único D-014 atualizado (já que a razão de existir e o prazo de remoção —      
  T-028, CLI obrigatório — são idênticos para os dois)? Se for consolidar,      
  prefiro isso a duas entradas quase idênticas.                                 

● Consolido em D-014 — mesma razão, mesmo prazo, entrada única mais clara.

● Update(specs\001-motor-reembolso\DECISIONS.md)
  ⎿  Added 20 lines, removed 16 lines
      10  
      11  ---
      12  
      13 -## D-014 — `_POLITICA_V3`: fallback temporário em `motor.py` du
         -rante migração para política externalizada · `2026-07-30`      
      13 +## D-014 — Fallbacks de migração em `motor.py`: `_POLITICA_V3` 
         +e `gatilho_nf=Decimal("100.00")` · `2026-07-30`                
      14  
      15  **Gatilho:** T-025 refatorou `verificar_categoria` para receber
           `politica_eff`
      16 -como parâmetro. O motor passou a exigir uma política para verif
         -icar categorias,                                               
      17 -mas `test_integracao.py` (que testa o lote v3 `despesas-exemplo
         -.json`) ainda                                                  
      18 -chama `processar()` sem passar `politica_eff` — e continuará as
         -sim até T-028                                                  
      19 -tornar `--politica` obrigatório no CLI.                        
      16 +como parâmetro; T-026 refatorou `verificar_nf` para receber `ga
         +tilho_nf`.                                                     
      17 +Em ambos os casos o motor passou a exigir valores externos, mas
      18 +`test_integracao.py` e os testes de câmbio ainda chamam `proces
         +sar()` sem esses                                               
      19 +parâmetros — e continuarão assim até T-028 tornar `--politica` 
         +obrigatório no CLI.                                            
      20  
      21 -**Decisão:** `motor.py` define `_POLITICA_V3` — um dict com as 
         -três categorias                                                
      22 -e limites da v3, no mesmo formato que `politica_efetiva()` reto
         -rna. Usado como                                                
      23 -fallback quando `processar(politica_eff=None)`. Não é uma const
         -ante de negócio:                                               
      24 -é scaffolding de migração.                                     
      21 +**Decisão:** Dois fallbacks em `motor.py`, com a mesma filosofi
         +a:                                                             
      22 +- `_POLITICA_V3` — dict com as três categorias e limites v3, us
         +ado quando                                                     
      23 +  `processar(politica_eff=None)`.                              
      24 +- `Decimal("100.00")` inline — limiar de NF v3, usado quando   
      25 +  `processar(gatilho_nf=None)`.                                
      26  
      26 -**Por quê:** A alternativa (passar politica_eff em todos os tes
         -tes existentes                                                 
      27 -de uma vez) acoplaria T-025 a T-028 e tornaria o diff maior e m
         -ais difícil de                                                 
      28 -revisar. Migração incremental é preferível quando cada task dev
         -e caber em um                                                  
      29 -commit revisável.                                              
      27 +Nenhum é constante de negócio: são scaffolding de migração incr
         +emental.                                                       
      28  
      31 -**Quando será removido:** em T-028, quando `processar` receber 
         -`politica_eff`                                                 
      32 -obrigatoriamente via CLI. Nesse ponto `_POLITICA_V3` é deletado
         - e                                                             
      33 -`test_integracao.py` atualizado para passar a política v4 carre
         -gada do arquivo.                                               
      29 +**Por quê:** A alternativa — propagar os dois parâmetros em tod
         +os os chamadores                                               
      30 +de uma vez — acoplaria T-025/T-026 a T-028 e tornaria cada diff
         + maior e mais                                                  
      31 +difícil de revisar. Migração incremental é preferível quando ca
         +da task deve                                                   
      32 +caber em um commit revisável.                                  
      33  
      34 +**Quando serão removidos:** em T-028, quando `processar` recebe
         +r ambos                                                        
      35 +obrigatoriamente via CLI. Nesse ponto `_POLITICA_V3` é deletado
         +, o fallback                                                   
      36 +inline de `gatilho_nf` é removido, e `test_integracao.py` é atu
         +alizado para                                                   
      37 +passar a política v4 carregada do arquivo.                     
      38 +                                                               
      39  ---
      40  
      41  ## D-013 — Argumentos `--politica` e `--cambio` são obrigatório
          s em toda execução · `2026-07-30`

● D-014 atualizado — uma entrada, dois scaffoldings, mesmo prazo de remoção.
  Pronto para commitar feat(T-026): verificar_nf com limiar da política quando
  quiser.

✻ Cooked for 25s

> Aprovado. D-014 consolidado ficou claro — mesma filosofia, mesmo prazo de     
  remoção, sem duplicação. O ponto do motivo_texto está corretamente            
  identificado como não-regressão agora, mas real atenção futura; anotado para  
  conferir quando os testes de integração do envelope chegarem. Commita com     
  feat(T-026): verificar_nf com limiar da política (RF-17) e segue para a       
  T-027.                                                                        

  Committed 4ecf82 (ctrl+o to expand)

● Commitado. Lendo T-027 agora.

  Searched for 1 pattern, read 1 file (ctrl+o to expand)
● Entendendo o estado atual antes de qualquer mudança.

  Searched for 3 patterns, read 1 file (ctrl+o to expand)

● Tenho tudo que preciso. As mudanças de T-027 são:

  src/cotas.py: remove LIMITE_DIARIO e CATEGORIAS_LIMITE_POR_LANCAMENTO;
  GerenciadorCotas recebe politica_eff: dict no construtor; _chave usa
  periodicidade da política.

  src/motor.py: remove import de LIMITE_DIARIO; passa _eff ao construtor de
  GerenciadorCotas; _texto_passo7 recebe politica_eff para obter o limite no
  template de COTA_ESGOTADA.

  tests/test_rf08_rf09_rf10_cotas.py: 7 testes existentes recebem
  GerenciadorCotas(_POLITICA_V3); 4 novos testes do critério de aceite.

● Write(src\cotas.py)
  ⎿  Added 10 lines, removed 19 lines
       1  from decimal import Decimal
       2 -from datetime import date                                      
       2  
       3  from src.modelos import Despesa
       4  
       6 -LIMITE_DIARIO: dict[str, Decimal] = {                          
       7 -    "alimentacao": Decimal("60.00"),                           
       8 -    "transporte_urbano": Decimal("80.00"),                     
       9 -    "hospedagem": Decimal("250.00"),                           
      10 -}                                                              
       5  
      12 -CATEGORIAS_LIMITE_POR_LANCAMENTO = {"hospedagem"}              
      13 -                                                               
      14 -                                                               
      15 -def _chave(despesa: Despesa) -> tuple:                         
      16 -    if despesa.categoria in CATEGORIAS_LIMITE_POR_LANCAMENTO:  
      17 -        return (despesa.id, despesa.categoria)                 
      18 -    return (despesa.data, despesa.categoria)                   
      19 -                                                               
      20 -                                                               
       6  class GerenciadorCotas:
      22 -    def __init__(self) -> None:                                
       7 +    def __init__(self, politica_eff: dict) -> None:            
       8 +        self._politica = politica_eff                          
       9          self._consumido: dict[tuple, Decimal] = {}
      10  
      11 +    def _chave(self, despesa: Despesa) -> tuple:               
      12 +        periodicidade = self._politica[despesa.categoria]["peri
         +odicidade"]                                                    
      13 +        if periodicidade == "diaria":                          
      14 +            return (despesa.id, despesa.categoria)             
      15 +        return (despesa.data, despesa.categoria)               
      16 +                                                               
      17      def calcular_reembolso(self, despesa: Despesa) -> tuple[Dec
          imal, str | None]:
      26 -        limite = LIMITE_DIARIO[despesa.categoria]              
      27 -        chave = _chave(despesa)                                
      18 +        limite = self._politica[despesa.categoria]["limite"]   
      19 +        chave = self._chave(despesa)                           
      20          ja_consumido = self._consumido.get(chave, Decimal("0.00
          "))
      21          saldo = limite - ja_consumido
      22  
      23          if saldo <= Decimal("0.00"):
      32 -            # ja_consumido + 0 == ja_consumido — escrita seria 
         -redundante                                                     
      24              return Decimal("0.00"), "COTA_ESGOTADA"
      25  
      26          if despesa.valor_considerado > saldo:

● Agora atualizo motor.py — remove import de LIMITE_DIARIO, passa _eff ao
  GerenciadorCotas, e adiciona politica_eff ao _texto_passo7:

● Update(src\motor.py)
  ⎿  Added 1 line, removed 1 line
      1  from decimal import Decimal
      2  
      3 -from src.cotas import GerenciadorCotas, LIMITE_DIARIO           
      3 +from src.cotas import GerenciadorCotas                          
      4  from src.modelos import (
      5      Colaborador, DespesaBruta, Despesa, Periodo,
      6      Resultado, ResultadoItem, Resumo,

● Update(src\motor.py)
  ⎿  Added 2 lines, removed 2 lines
      25  }
      26  
      27  
      28 -def _texto_passo7(categoria: str, motivo_codigo: str | None, va
         -lor_reembolsavel: Decimal, valor_considerado: Decimal) -> str |
         - None:                                                         
      28 +def _texto_passo7(categoria: str, motivo_codigo: str | None, va
         +lor_reembolsavel: Decimal, valor_considerado: Decimal, politica
         +_eff: dict) -> str | None:                                     
      29      if motivo_codigo is None:
      30          return None
      31      if motivo_codigo == "LIMITE_DIARIO":
     ...
      33              return "limite de 1 diária aplicado (campo num_diar
          ias ausente do schema)"
      34          return f"limite diário de {categoria}: reembolsado {fmt
          _valor(valor_reembolsavel)} de {fmt_valor(valor_considerado)}"
      35      if motivo_codigo == "COTA_ESGOTADA":
      36 -        limite = LIMITE_DIARIO[categoria]                      
      36 +        limite = politica_eff[categoria]["limite"]             
      37          return f"cota diária de {categoria} esgotada: {fmt_valo
          r(limite)} já consumidos por itens anteriores no dia"
      38      return None
      39  

● Update(src\motor.py)
  ⎿  Error editing file

  Searched for 1 pattern, read 1 file (ctrl+o to expand)

● Update(src\motor.py)
  ⎿  Added 1 line, removed 1 line
      77          )
      78  
      79      vistos: dict = {}
      80 -    gc = GerenciadorCotas()                                    
      80 +    gc = GerenciadorCotas(_eff)                                
      81      itens: list[ResultadoItem] = []
      82  
      83      for bruta in despesas_brutas:

● Agora atualizo a chamada de _texto_passo7 para passar _eff:

● Update(src\motor.py)
  ⎿  Added 1 line, removed 1 line
      130                  valor_considerado=despesa.valor_considerado,
      131                  valor_reembolsavel=valor_reembolsavel,
      132                  motivo_codigo=motivo_codigo,
      133 -                motivo_texto=_texto_passo7(despesa.categoria, 
          -motivo_codigo, valor_reembolsavel, despesa.valor_considerado),
      133 +                motivo_texto=_texto_passo7(despesa.categoria, 
          +motivo_codigo, valor_reembolsavel, despesa.valor_considerado, 
          +_eff),                                                        
      134                  duplicata_de=None,
      135                  moeda=despesa.moeda,
      136                  taxa_cambio_aplicada=despesa.taxa_cambio_aplic
           ada,

● Agora os testes — atualizo os 7 existentes e adiciono os 4 novos:

● Write(tests\test_rf08_rf09_rf10_cotas.py)
  ⎿  Added 67 lines, removed 8 lines
       5  
       6  from src.cotas import GerenciadorCotas
       7  
       8 +_POLITICA_V3 = {                                               
       9 +    "alimentacao":       {"limite": Decimal("60.00"),  "periodi
         +cidade": "dia"},                                               
      10 +    "transporte_urbano": {"limite": Decimal("80.00"),  "periodi
         +cidade": "dia"},                                               
      11 +    "hospedagem":        {"limite": Decimal("250.00"), "periodi
         +cidade": "diaria"},                                            
      12 +}                                                              
      13  
      14 +_POLITICA_CC_COMERCIAL = {                                     
      15 +    "alimentacao":       {"limite": Decimal("90.00"),  "periodi
         +cidade": "dia"},                                               
      16 +    "transporte_urbano": {"limite": Decimal("150.00"), "periodi
         +cidade": "dia"},                                               
      17 +    "hospedagem":        {"limite": Decimal("400.00"), "periodi
         +cidade": "diaria"},                                            
      18 +    "representacao":     {"limite": Decimal("300.00"), "periodi
         +cidade": "dia"},                                               
      19 +}                                                              
      20 +                                                               
      21 +_POLITICA_CC_ENG = {                                           
      22 +    "alimentacao":       {"limite": Decimal("60.00"),  "periodi
         +cidade": "dia"},                                               
      23 +    "transporte_urbano": {"limite": Decimal("80.00"),  "periodi
         +cidade": "dia"},                                               
      24 +    "hospedagem":        {"limite": Decimal("0.00"),   "periodi
         +cidade": "diaria"},                                            
      25 +}                                                              
      26 +                                                               
      27 +                                                               
      28  # --- RF-08: alimentação ---
      29  
      30  def test_rf08_agregado_diario_corte(despesa_factory):
      12 -    gc = GerenciadorCotas()                                    
      31 +    gc = GerenciadorCotas(_POLITICA_V3)                        
      32      despesa = despesa_factory(categoria="alimentacao", valor=De
          cimal("72.50"))
      33      valor, motivo = gc.calcular_reembolso(despesa)
      34      assert valor == Decimal("60.00")
     ...
      36  
      37  
      38  def test_rf08_cota_esgotada_segundo_item(despesa_factory):
      20 -    gc = GerenciadorCotas()                                    
      39 +    gc = GerenciadorCotas(_POLITICA_V3)                        
      40      d1 = despesa_factory(id="d-001", categoria="alimentacao", v
          alor=Decimal("60.00"))
      41      d2 = despesa_factory(id="d-002", categoria="alimentacao", v
          alor=Decimal("38.00"))
      42      gc.calcular_reembolso(d1)
     ...
      46  
      47  
      48  def test_rf08_dentro_do_limite_aprovado(despesa_factory):
      30 -    gc = GerenciadorCotas()                                    
      49 +    gc = GerenciadorCotas(_POLITICA_V3)                        
      50      despesa = despesa_factory(categoria="alimentacao", valor=De
          cimal("30.00"))
      51      valor, motivo = gc.calcular_reembolso(despesa)
      52      assert valor == Decimal("30.00")
     ...
      56  # --- RF-09: transporte_urbano ---
      57  
      58  def test_rf09_agregado_diario_corte(despesa_factory):
      40 -    gc = GerenciadorCotas()                                    
      59 +    gc = GerenciadorCotas(_POLITICA_V3)                        
      60      despesa = despesa_factory(categoria="transporte_urbano", va
          lor=Decimal("100.00"))
      61      valor, motivo = gc.calcular_reembolso(despesa)
      62      assert valor == Decimal("80.00")
     ...
      66  # --- RF-10: hospedagem ---
      67  
      68  def test_rf10_limite_por_lancamento(despesa_factory):
      50 -    gc = GerenciadorCotas()                                    
      69 +    gc = GerenciadorCotas(_POLITICA_V3)                        
      70      despesa = despesa_factory(categoria="hospedagem", valor=Dec
          imal("480.00"))
      71      valor, motivo = gc.calcular_reembolso(despesa)
      72      assert valor == Decimal("250.00")
     ...
      74  
      75  
      76  def test_rf10_descricao_ignorada(despesa_factory):
      58 -    gc = GerenciadorCotas()                                    
      77 +    gc = GerenciadorCotas(_POLITICA_V3)                        
      78      despesa = despesa_factory(
      79          categoria="hospedagem",
      80          descricao="2 diárias Hotel XYZ",
     ...
      86  
      87  
      88  def test_rf10_duas_hospedagens_mesmo_dia_independentes(despesa_
          factory):
      70 -    gc = GerenciadorCotas()                                    
      89 +    gc = GerenciadorCotas(_POLITICA_V3)                        
      90      d1 = despesa_factory(id="d-A", categoria="hospedagem", data
          =date(2026, 7, 15), valor=Decimal("200.00"))
      91      d2 = despesa_factory(id="d-B", categoria="hospedagem", data
          =date(2026, 7, 15), valor=Decimal("200.00"))
      92      valor1, motivo1 = gc.calcular_reembolso(d1)
     ...
       98  # --- RF-12: corte não recusa ---
       99  
      100  def test_rf12_exceder_limite_nao_recusa(despesa_factory):
       82 -    gc = GerenciadorCotas()                                   
      101 +    gc = GerenciadorCotas(_POLITICA_V3)                       
      102      despesa = despesa_factory(categoria="alimentacao", valor=D
           ecimal("72.50"))
      103      valor, motivo = gc.calcular_reembolso(despesa)
      104      assert valor > Decimal("0.00")
      105      assert motivo == "LIMITE_DIARIO"
      106 +                                                              
      107 +                                                              
      108 +# --- RF-17 + T-027: política efetiva por CC ---              
      109 +                                                              
      110 +def test_rf10_periodicidade_diaria_por_lancamento(despesa_fact
          +ory):                                                         
      111 +    # periodicidade="diaria" → cada lançamento tem saldo própr
          +io (chave por id, não por data)                               
      112 +    gc = GerenciadorCotas(_POLITICA_V3)                       
      113 +    d1 = despesa_factory(id="h-001", categoria="hospedagem", d
          +ata=date(2026, 7, 20), valor=Decimal("250.00"))               
      114 +    d2 = despesa_factory(id="h-002", categoria="hospedagem", d
          +ata=date(2026, 7, 20), valor=Decimal("250.00"))               
      115 +    valor1, motivo1 = gc.calcular_reembolso(d1)               
      116 +    valor2, motivo2 = gc.calcular_reembolso(d2)               
      117 +    assert valor1 == Decimal("250.00") and motivo1 is None    
      118 +    assert valor2 == Decimal("250.00") and motivo2 is None    
      119 +                                                              
      120 +                                                              
      121 +def test_rf08_cc_comercial_limite_90(despesa_factory):        
      122 +    # alimentacao CC-COMERCIAL: limite 90,00 → valor de R$95 c
          +ortado em 90                                                  
      123 +    gc = GerenciadorCotas(_POLITICA_CC_COMERCIAL)             
      124 +    despesa = despesa_factory(categoria="alimentacao", valor=D
          +ecimal("95.00"))                                              
      125 +    valor, motivo = gc.calcular_reembolso(despesa)            
      126 +    assert valor == Decimal("90.00")                          
      127 +    assert motivo == "LIMITE_DIARIO"                          
      128 +                                                              
      129 +                                                              
      130 +def test_rf09_cc_comercial_transporte_150(despesa_factory):   
      131 +    # transporte CC-COMERCIAL: limite 150,00 → valor de R$180 
          +cortado em 150                                                
      132 +    gc = GerenciadorCotas(_POLITICA_CC_COMERCIAL)             
      133 +    despesa = despesa_factory(categoria="transporte_urbano", v
          +alor=Decimal("180.00"))                                       
      134 +    valor, motivo = gc.calcular_reembolso(despesa)            
      135 +    assert valor == Decimal("150.00")                         
      136 +    assert motivo == "LIMITE_DIARIO"                          
      137 +                                                              
      138 +                                                              
      139 +def test_rf10_cc_eng_hospedagem_zero_cota_esgotada(despesa_fac
          +tory):                                                        
      140 +    # limite 0,00 → saldo = 0 desde o início → sempre COTA_ESG
          +OTADA (D-005)                                                 
      141 +    gc = GerenciadorCotas(_POLITICA_CC_ENG)                   
      142 +    despesa = despesa_factory(categoria="hospedagem", valor=De
          +cimal("150.00"))                                              
      143 +    valor, motivo = gc.calcular_reembolso(despesa)            
      144 +    assert valor == Decimal("0.00")                           
      145 +    assert motivo == "COTA_ESGOTADA"                          

  Ran 1 shell command (ctrl+o to expand)

● Dois arquivos importam LIMITE_DIARIO. Vejo o que usam:

  Searched for 2 patterns, read 2 files (ctrl+o to expand)

● Ambos usam LIMITE_DIARIO para verificar limites v3. Substituo por dicts locais
   nos dois arquivos:

● Update(tests\test_rf16_viagem_suspensa.py)
  ⎿  Removed 1 line
      1  from decimal import Decimal
      2  from pathlib import Path
      3  
      4 -from src.cotas import LIMITE_DIARIO                             
      4  from src.motor import processar
      5  from src.normalizacao import normalizar_categoria
      6  from src.parser import carregar_entrada

● Update(tests\test_rf16_viagem_suspensa.py)
  ⎿  Added 6 lines
       7  
       8  _EXEMPLO = Path(__file__).parent.parent / "exemplos" / "despesa
          s-exemplo.json"
       9  
      10 +_LIMITE_V3 = {                                                 
      11 +    "alimentacao": Decimal("60.00"),                           
      12 +    "transporte_urbano": Decimal("80.00"),                     
      13 +    "hospedagem": Decimal("250.00"),                           
      14 +}                                                              
      15  
      16 +                                                               
      17  def test_rf16_nenhum_item_com_limite_ampliado():
      18      # Regra de viagem (limites ampliados) está suspensa por AMB
          -006.
      19      # Nenhum item de nenhuma categoria deve receber valor_reemb
          olsavel acima

● Update(tests\test_rf16_viagem_suspensa.py)
  ⎿  Added 1 line, removed 1 line
      24      categoria_por_id = {d.id: normalizar_categoria(d.categoria)
           for d in despesas_brutas}
      25      for item in resultado.itens:
      26          categoria = categoria_por_id[item.id]
      27 -        limite = LIMITE_DIARIO.get(categoria)                  
      27 +        limite = _LIMITE_V3.get(categoria)                     
      28          if limite is None:
      29              continue  # categoria inválida já recusada no passo
           4
      30          assert item.valor_reembolsavel <= limite, (

● Agora test_integracao.py:

● Update(tests\test_integracao.py)
  ⎿  Removed 1 line
      3  
      4  import pytest
      5  
      6 -from src.cotas import LIMITE_DIARIO                             
      6  from src.motor import processar
      7  from src.normalizacao import normalizar_categoria
      8  from src.parser import carregar_entrada

● Update(tests\test_integracao.py)  ⎿  Added 6 lines
      10  
      11  _EXEMPLO = Path(__file__).parent.parent / "exemplos" / "despesa
          s-exemplo.json"
      12  
      13 +_LIMITE_V3 = {                                                 
      14 +    "alimentacao": Decimal("60.00"),                           
      15 +    "transporte_urbano": Decimal("80.00"),                     
      16 +    "hospedagem": Decimal("250.00"),                           
      17 +}                                                              
      18  
      19 +                                                               
      20  @pytest.fixture(scope="module")
      21  def _resultado():
      22      colaborador, periodo, despesas = carregar_entrada(_EXEMPLO)

● Update(tests\test_integracao.py)
  ⎿  Added 7 lines, removed 7 lines
      29  
      30  
      31  def test_integracao_d001(_por_id):
      32 -    # d-001: alimentação R$72,50 → parcial R$60,00 (LIMITE_DIAR
         -IO)                                                            
      32 +    # d-001: alimentação R$72,50 → parcial R$60,00 (_LIMITE_V3)
      33      item = _por_id["d-001"]
      34      assert item.status == "parcial"
      35      assert item.valor_reembolsavel == Decimal("60.00")
      36 -    assert item.motivo_codigo == "LIMITE_DIARIO"               
      36 +    assert item.motivo_codigo == "_LIMITE_V3"                  
      37  
      38  
      39  def test_integracao_d002(_por_id):
     ...
      49      item = _por_id["d-003"]
      50      assert item.status == "parcial"
      51      assert item.valor_reembolsavel == Decimal("80.00")
      52 -    assert item.motivo_codigo == "LIMITE_DIARIO"               
      52 +    assert item.motivo_codigo == "_LIMITE_V3"                  
      53  
      54  
      55  def test_integracao_d004(_por_id):
     ...
      104      item = _por_id["d-010"]
      105      assert item.status == "parcial"
      106      assert item.valor_reembolsavel == Decimal("250.00")
      107 -    assert item.motivo_codigo == "LIMITE_DIARIO"              
      107 +    assert item.motivo_codigo == "_LIMITE_V3"                 
      108      assert "limite de 1 diária" in item.motivo_texto
      109  
      110  
     ...
      137      assert item.valor_considerado == Decimal("61.00")
      138      assert item.status == "parcial"
      139      assert item.valor_reembolsavel == Decimal("60.00")
      140 -    assert item.motivo_codigo == "LIMITE_DIARIO"              
      140 +    assert item.motivo_codigo == "_LIMITE_V3"                 
      141  
      142  
      143  def test_integracao_saida_deterministica():
     ...
      156      por_id = {item.id: item for item in resultado.itens}
      157      for bruta in despesas:
      158          categoria = normalizar_categoria(bruta.categoria)
      159 -        if categoria in LIMITE_DIARIO:                        
      160 -            assert por_id[bruta.id].valor_reembolsavel <= LIMI
          -TE_DIARIO[categoria]                                          
      159 +        if categoria in _LIMITE_V3:                           
      160 +            assert por_id[bruta.id].valor_reembolsavel <= _LIM
          +ITE_V3[categoria]                                             
      161  
      162  
      163  def test_integracao_viagem_suspensa_sem_ampliacao(_por_id):

  Ran 2 shell commands (ctrl+o to expand)

● O replace_all substituiu também as strings literais "LIMITE_DIARIO" nas
  asserções. Preciso reverter apenas essas ocorrências.

  Read 1 file, ran 1 shell command (ctrl+o to expand)

● Quatro asserções e um comentário afetados. Corrijo com substituições precisas:

● Update(tests\test_integracao.py)
  ⎿  Added 2 lines, removed 2 lines
      29  
      30  
      31  def test_integracao_d001(_por_id):
      32 -    # d-001: alimentação R$72,50 → parcial R$60,00 (_LIMITE_V3)
      32 +    # d-001: alimentação R$72,50 → parcial R$60,00 (LIMITE_DIAR
         +IO)                                                            
      33      item = _por_id["d-001"]
      34      assert item.status == "parcial"
      35      assert item.valor_reembolsavel == Decimal("60.00")
      36 -    assert item.motivo_codigo == "_LIMITE_V3"                  
      36 +    assert item.motivo_codigo == "LIMITE_DIARIO"               
      37  
      38  
      39  def test_integracao_d002(_por_id):

● Update(tests\test_integracao.py)
  ⎿  Added 1 line, removed 1 line
      49      item = _por_id["d-003"]
      50      assert item.status == "parcial"
      51      assert item.valor_reembolsavel == Decimal("80.00")
      52 -    assert item.motivo_codigo == "_LIMITE_V3"                  
      52 +    assert item.motivo_codigo == "LIMITE_DIARIO"               
      53  
      54  
      55  def test_integracao_d004(_por_id):

● Update(tests\test_integracao.py)
  ⎿  Added 1 line, removed 1 line
      104      item = _por_id["d-010"]
      105      assert item.status == "parcial"
      106      assert item.valor_reembolsavel == Decimal("250.00")
      107 -    assert item.motivo_codigo == "_LIMITE_V3"                 
      107 +    assert item.motivo_codigo == "LIMITE_DIARIO"              
      108      assert "limite de 1 diária" in item.motivo_texto
      109  
      110  

● Update(tests\test_integracao.py)
  ⎿  Added 1 line, removed 1 line
      137      assert item.valor_considerado == Decimal("61.00")
      138      assert item.status == "parcial"
      139      assert item.valor_reembolsavel == Decimal("60.00")
      140 -    assert item.motivo_codigo == "_LIMITE_V3"                 
      140 +    assert item.motivo_codigo == "LIMITE_DIARIO"              
      141  
      142  
      143  def test_integracao_saida_deterministica():

  Ran 1 shell command (ctrl+o to expand)

● 106 passando. Antes de sugerir o commit, pontos para você verificar:

  O que mudou em T-027:
  1. LIMITE_DIARIO e CATEGORIAS_LIMITE_POR_LANCAMENTO removidos de cotas.py.
  GerenciadorCotas recebe politica_eff: dict obrigatoriamente; _chave usa
  periodicidade do dict.
  2. motor.py: remove import de LIMITE_DIARIO; passa _eff ao construtor;
  _texto_passo7 recebe politica_eff e lê politica_eff[categoria]["limite"] para
  o template de COTA_ESGOTADA.
  3. test_integracao.py e test_rf16_viagem_suspensa.py: substituição de import
  por _LIMITE_V3 local (limites v3 hardcoded nos testes — serão removidos em
  T-028 quando os testes passarem a carregar politica-v4.json).
  4. 4 novos testes de aceite: limite 90 (CC-COMERCIAL alimentação), limite 150
  (CC-COMERCIAL transporte), limite 0 → COTA_ESGOTADA, periodicidade diaria →
  independência por lançamento.

  Ponto fraco para conferir: o erro com replace_all que substituiu strings
  literais "LIMITE_DIARIO" em asserções — revertidas com substituições pontuais.
   Verifique test_integracao.py se quiser confirmar que nenhuma outra string
  literal foi afetada.

  Mensagem de commit sugerida: feat(T-027): GerenciadorCotas com política 
  efetiva e periodicidade

✻ Worked for 4m 38s

> Antes de aprovar: a varredura por resquícios não é opcional, é obrigatória —  
  já é a segunda vez hoje que um replace_all corrompe string literal (T-012 foi 
   a primeira). Rode:                                                           
                                                                                
  1. grep -rn "_LIMITE_V3" tests/ src/ — para confirmar que a constante         
  renomeada só aparece onde deveria (as definições locais e usos corretos), sem 
   sobra de confusão com o motivo_codigo.                                       
  2. grep -rn '"LIMITE_DIARIO"' tests/ — para eu ver TODAS as ocorrências da    
  string literal correta de uma vez, e confirmar visualmente que nenhuma outra  
  ficou corrompida (test_rf16_viagem_suspensa.py também foi tocado nesta task — 
   confirme que ele não tem o mesmo problema, já que você mencionou tê-lo       
  editado também).                                                              
                                                                                
  Cole os dois resultados de grep aqui antes do commit.                         

  Ran 2 shell commands (ctrl+o to expand)

● Resultados limpos:

  _LIMITE_V3 — 5 ocorrências, todas corretas: 2 definições de dict (linhas 13 e
  10) e 3 usos como variável (linhas 159, 160, 27). Nenhuma em src/.

  "LIMITE_DIARIO" — 14 ocorrências, todas string literal de motivo_codigo:
  - test_integracao.py: 4 linhas (36, 52, 107, 140) — corrigidas após o
  replace_all corrompido
  - test_motor.py: 1 linha (45) — não foi tocado nesta task, correto
  - test_rf08_rf09_rf10_cotas.py: 7 linhas — todos assert motivo == 
  "LIMITE_DIARIO" nos testes novos e existentes, correto
  - test_rf14_serializador.py: 2 linhas — campos de fixture, correto

  test_rf16_viagem_suspensa.py não contém "LIMITE_DIARIO" como string literal —
  esse arquivo só usava o dict como variável (.get(categoria)), sem asserções de
   motivo_codigo, então o replace_all não criou corrupção lá.

  Tudo limpo. Pode aprovar o commit.

✻ Worked for 16s

> Aprovado — os dois greps confirmam limpeza total, sem resquício em nenhum     
  arquivo. Commita com feat(T-027): GerenciadorCotas com política efetiva e     
  periodicidade (RF-17) e segue para a próxima task.                            

  Committed 7d933e (ctrl+o to expand)

● Commitado. Lendo T-028.

  Searched for 1 pattern, ran 1 shell command (ctrl+o to expand)

● Preciso ver test_motor.py para estimar o impacto da remoção de _POLITICA_V3 em
   todos os chamadores de processar().

  Searched for 1 pattern, read 1 file (ctrl+o to expand)

● T-028 tem um ponto de ambiguidade de escopo que preciso levantar antes de
  implementar.

  O que tasks.md diz explicitamente para T-028:
  - Serializador: adicionar moeda e taxa_cambio_aplicada por item
  - CLI: --politica e --cambio obrigatórios; carrega os três arquivos; erro
  claro em arquivo ausente

  O que D-014 diz que acontece em T-028:

  ▎ "_POLITICA_V3 é deletado, o fallback inline de gatilho_nf é removido, e 
  ▎ test_integracao.py é atualizado para passar a política v4 carregada do 
  ▎ arquivo."

  Se eu remover _POLITICA_V3 de motor.py, os testes que chamam processar() sem
  politica_eff precisam de atualização. Contagem atual:

  ┌──────────────────────────────┬──────────────────────────┐
  │           Arquivo            │     Testes afetados      │
  ├──────────────────────────────┼──────────────────────────┤
  │ test_motor.py                │ 7 (todos)                │
  ├──────────────────────────────┼──────────────────────────┤
  │ test_rf18_motor.py           │ 6 (todos)                │
  ├──────────────────────────────┼──────────────────────────┤
  │ test_integracao.py           │ fixture + 1 teste avulso │
  ├──────────────────────────────┼──────────────────────────┤
  │ test_rf16_viagem_suspensa.py │ 1                        │
  └──────────────────────────────┴──────────────────────────┘

  Total: ~15 call sites. A solução seria definir um _POL_V3 = {...} local em
  cada arquivo de teste que precisa de isolamento, e atualizar
  test_integracao.py para carregar politica-v4.json de verdade.

  Três opções:

  A) T-028 = serializador + CLI apenas — _POLITICA_V3 permanece em motor.py
  (contradiz D-014, mas mantém o diff pequeno)

  B) T-028 = serializador + CLI + remoção completa do D-014 — inclui as ~15
  atualizações de call site; test_integracao.py passa politica-v4 real. Honra
  D-014 integralmente.

  C) T-028 = serializador + CLI + atualiza test_integracao.py — remove
  _POLITICA_V3 de motor.py mas deixa politica_eff: dict | None = None com
  ValueError explícito quando None; os testes unitários (test_motor,
  test_rf18_motor) precisariam ser atualizados também, então não poupa trabalho
  vs opção B.

  Minha recomendação é B: D-014 foi aprovado por você e o escopo real é
  gerenciável (~15 substituições pontuais com dict inline). Mas a decisão é sua.

✻ Brewed for 3m 17s

> Opção B — e bom que você trouxe a contradição em vez de escolher sozinho      
  (regra 2 em ação, mesmo agora). A opção A deixaria uma lacuna de cobertura    
  real: test_integracao.py, o teste mais importante do projeto, nunca chegaria  
  a exercitar o caminho de política externa de verdade — a CLI funcionaria, mas 
   o teste que deveria provar isso continuaria rodando contra dados hardcoded.  
                                                                                
  Distinção a aplicar nas ~15 atualizações: test_motor.py e test_rf18_motor.py  
  são testes UNITÁRIOS de mecanismo — um dict de teste local (_POL_V3, valores  
  da v3, só para isolamento) é apropriado e correto ali, porque eles não        
  deveriam se importar com política real. Mas test_integracao.py precisa        
  carregar politica-v4.json DE VERDADE via carregar_politica() +                
  politica_efetiva() — não um dict inventado — porque é ele quem prova que o    
  sistema funciona com o arquivo real do envelope. Confirme essa distinção      
  antes de implementar as ~15 mudanças.                                         
                                                                                
  Implemente a T-028 completa: serializador (moeda + taxa_cambio_aplicada), CLI 
   (--politica/--cambio obrigatórios, erro claro em arquivo ausente), remoção   
  de _POLITICA_V3 de motor.py, e as ~15 atualizações de call site conforme a    
  distinção acima. Rode a suite completa antes de me mostrar o diff.            

● Distinção confirmada. Antes de escrever uma linha de código, leio os dois
  arquivos de referência para saber o centro_custo do colaborador de
  despesas-exemplo.json e os limites do padrao em politica-v4.json — isso
  determina se os asserts existentes em test_integracao.py precisam de ajuste
  numérico.

  Ran 2 shell commands (ctrl+o to expand)
● Antes de implementar, preciso levantar uma inconsistência que vai impactar
  várias asserções em test_integracao.py.

  O que descobri: o colaborador em despesas-exemplo.json tem centro_custo = 
  "CC-ENG-PLATAFORMA". Com politica_efetiva(politica, "CC-ENG-PLATAFORMA"), os
  limites efetivos são:

  Categoria: alimentacao
  Limite atual (v3 / _POL_V3): 60,00
  Limite com v4 + CC-ENG: 75,00
  ────────────────────────────────────────
  Categoria: transporte_urbano
  Limite atual (v3 / _POL_V3): 80,00
  Limite com v4 + CC-ENG: 80,00
  ────────────────────────────────────────
  Categoria: hospedagem
  Limite atual (v3 / _POL_V3): 250,00
  Limite com v4 + CC-ENG: 0,00 (não reembolsável)

  Consequências diretas nos testes existentes:

  - d-001 (alimentacao R$72,50): hoje parcial / R$60,00 → com v4 seria aprovado 
  / R$72,50 (72,50 < 75)
  - d-010 (hospedagem R$480): hoje LIMITE_DIARIO / R$250,00 → com v4 seria
  COTA_ESGOTADA / R$0,00
  - d-014 (alimentacao R$61,00): hoje parcial / R$60,00 → com v4 seria aprovado 
  / R$61,00
  - resumo.total_reembolsavel e totais mudam em cascata

  Três opções:

  A) Mudar o CC em despesas-exemplo.json para um inexistente na política v4
  (ex.: "CC-SUPORTE") → usa padrao → limites idênticos ao v3 → zero mudanças nas
   asserções de test_integracao.py

  B) Atualizar as asserções de test_integracao.py para refletir o comportamento
  real de CC-ENG-PLATAFORMA com v4 — d-001 aprovado, d-010 COTA_ESGOTADA, novos
  totais. Mais trabalho, mas os testes provam o sistema real.

  C) test_integracao.py continua com dict local _POL_V3 (como test_motor.py); só
   test_integracao_envelope.py (T-029) usa a política real. Contradiz D-014 mas
  preserva clareza de propósito entre os dois arquivos.

  Minha leitura: D-014 diz explicitamente "test_integracao.py atualizado para
  passar a política v4", então C está fora. Entre A e B — A é cirurgicamente 
  menor e não muda o que o teste prova (o sistema ainda exercita o pipeline real
   com arquivo real, a única coisa que muda é o CC); B é mais honesto mas exige 
  recalcular ~8 asserções e os totais do resumo.

  Qual das três?

✻ Worked for 2m 51s

> Antes de recalcular os asserts: confirmo que test_integracao.py deve refletir 
   os NOVOS valores de CC-ENG-PLATAFORMA (alimentação 75,00, hospedagem 0,00    
  sempre COTA_ESGOTADA) — a vigência retroativa do envelope é real, não         
  hipotética, e Marina está sujeita a ela como qualquer colaborador. Isso       
  significa que praticamente todos os itens de d-001 a d-014 vão ter            
  valor_reembolsavel diferente do original v3, e alguns motivos_codigo também   
  podem mudar (ex.: qualquer item de hospedagem vira COTA_ESGOTADA agora, não   
  LIMITE_DIARIO).                                                               
                                                                                
  Depois de recalcular, não confie só no cálculo mental — rode o pipeline real  
  contra despesas-exemplo.json com a política v4 carregada, imprima os 14 itens 
   resultantes, e use ESSA saída real (não uma estimativa) para escrever os     
  novos asserts. É o mesmo princípio de "prova, não afirmação" de sempre —      
  recalcular na cabeça e depois só confirmar com o sistema é como o bug do      
  README aconteceu ao contrário.                                                

● Exato. Primeiro rodo o pipeline real, capturo os 14 itens e uso a saída para
  escrever os asserts. Nada de estimativa mental.

  Ran 1 shell command (ctrl+o to expand)

● Preciso ver o motivo_texto de cada item e o conteúdo completo de
  test_integracao.py para saber quais asserções de texto também mudam.

  Read 1 file, ran 1 shell command (ctrl+o to expand)

● Tenho todos os dados reais. Agora vejo rapidamente test_rf14_serializador.py
  antes de começar — o serializador vai mudar e pode ter testes que verificam o
  JSON de saída campo a campo.

  Read 2 files (ctrl+o to expand)

● Tenho tudo. Agora sei exatamente o que muda em cada arquivo. Implemento na
  ordem: serializador → CLI → motor.py → testes.

  Mapa de mudanças em test_integracao.py baseado na saída real:
  - d-001: parcial/60.00/LIMITE_DIARIO → aprovado/72.50/None
  - d-002: recusado/0.00/COTA_ESGOTADA → parcial/2.50/LIMITE_DIARIO
  - d-010: parcial/250.00/LIMITE_DIARIO/"limite de 1 diária" →
  recusado/0.00/COTA_ESGOTADA/"R$ 0,00"
  - d-014: parcial/60.00/LIMITE_DIARIO → aprovado/61.00/None
  - resumo: total_solicitado=1861.84, total_reembolsavel=351.43, 
  total_recusado=1510.41, aprovados=5, parciais=2, recusados=7

● Update(src\serializador.py)
  ⎿  File must be read first

  Read 1 file (ctrl+o to expand)

● Update(src\serializador.py)
  ⎿  Added 2 lines
      11          "id": item.id,
      12          "status": item.status,
      13          "valor_original": lit(item.valor_original),
      14 +        "moeda": item.moeda,                                   
      15 +        "taxa_cambio_aplicada": q(item.taxa_cambio_aplicada) if
         + item.taxa_cambio_aplicada is not None else None,              
      16          "valor_considerado": q(item.valor_considerado),
      17          "valor_reembolsavel": q(item.valor_reembolsavel),
      18          "motivo_codigo": item.motivo_codigo,

● Agora o CLI:

● Write(src\cli.py)
  ⎿  Error writing file

  Read 1 file (ctrl+o to expand)

● Write(src\cli.py)
  ⎿  Added 34 lines, removed 9 lines
       5  
       6  from src.motor import processar
       7  from src.parser import carregar_entrada
       8 +from src.parser_cambio import carregar_cambio                  
       9 +from src.parser_politica import carregar_politica, nota_fiscal_
         +gatilho, politica_efetiva                                      
      10  from src.serializador import serializar
      11  
      12  
      11 -def _calcular(args: argparse.Namespace) -> None:               
      12 -    caminho_input = Path(args.input)                           
      13 -    if not caminho_input.exists():                             
      14 -        print(f"Erro: arquivo de entrada não encontrado: {args.
         -input}", file=sys.stderr)                                      
      13 +def _arquivo(caminho_str: str, descricao: str) -> Path:        
      14 +    caminho = Path(caminho_str)                                
      15 +    if not caminho.exists():                                   
      16 +        print(f"Erro: {descricao} não encontrado: {caminho_str}
         +", file=sys.stderr)                                            
      17          sys.exit(1)
      18 +    return caminho                                             
      19  
      20 +                                                               
      21 +def _calcular(args: argparse.Namespace) -> None:               
      22 +    caminho_input = _arquivo(args.input, "arquivo de entrada") 
      23 +    caminho_politica = _arquivo(args.politica, "arquivo de polí
         +tica")                                                         
      24 +    caminho_cambio = _arquivo(args.cambio, "arquivo de câmbio")
      25 +                                                               
      26      try:
      27          colaborador, periodo, despesas = carregar_entrada(camin
          ho_input)
      28      except (KeyError, ValueError, json.JSONDecodeError) as e:
      29          print(f"Erro: entrada inválida — {e}", file=sys.stderr)
      30          sys.exit(1)
      31  
      23 -    resultado = processar(colaborador, periodo, despesas)      
      32 +    try:                                                       
      33 +        politica = carregar_politica(caminho_politica)         
      34 +        tabela_cambio = carregar_cambio(caminho_cambio)        
      35 +    except (KeyError, ValueError, json.JSONDecodeError) as e:  
      36 +        print(f"Erro: arquivo de política ou câmbio inválido — 
         +{e}", file=sys.stderr)                                         
      37 +        sys.exit(1)                                            
      38 +                                                               
      39 +    eff = politica_efetiva(politica, colaborador.centro_custo) 
      40 +    gnf = nota_fiscal_gatilho(politica)                        
      41 +                                                               
      42 +    resultado = processar(                                     
      43 +        colaborador, periodo, despesas,                        
      44 +        politica_eff=eff,                                      
      45 +        gatilho_nf=gnf,                                        
      46 +        tabela_cambio=tabela_cambio,                           
      47 +    )                                                          
      48      saida = serializar(resultado)
      49  
      26 -    caminho_output = Path(args.output)                         
      27 -    caminho_output.write_text(saida, encoding="utf-8")         
      50 +    Path(args.output).write_text(saida, encoding="utf-8")      
      51  
      52  
      53  def main() -> None:
     ...
      57      sub = parser.add_subparsers(dest="comando")
      58  
      59      calc = sub.add_parser("calcular", help="Processa um lote de
           despesas")
      37 -    calc.add_argument("--input", required=True, metavar="ARQUIV
         -O", help="JSON de entrada")                                    
      38 -    calc.add_argument("--output", required=True, metavar="ARQUI
         -VO", help="JSON de saída")                                     
      60 +    calc.add_argument("--input",    required=True, metavar="ARQ
         +UIVO", help="JSON de entrada")                                 
      61 +    calc.add_argument("--output",   required=True, metavar="ARQ
         +UIVO", help="JSON de saída")                                   
      62 +    calc.add_argument("--politica", required=True, metavar="ARQ
         +UIVO", help="JSON de política de reembolso")                   
      63 +    calc.add_argument("--cambio",   required=True, metavar="ARQ
         +UIVO", help="JSON de tabela de câmbio")                        
      64  
      65      args = parser.parse_args()
      66      if args.comando is None:

● Agora motor.py — remove _POLITICA_V3, muda assinatura para * keyword-only:

● Update(src\motor.py)
  ⎿  Removed 7 lines
      17  )
      18  
      19  
      20 -# Fallback v3 — removido quando T-028 tornar --politica obrigat
         -ório no CLI                                                    
      21 -_POLITICA_V3 = {                                               
      22 -    "alimentacao":       {"limite": Decimal("60.00"),  "periodi
         -cidade": "dia"},                                               
      23 -    "transporte_urbano": {"limite": Decimal("80.00"),  "periodi
         -cidade": "dia"},                                               
      24 -    "hospedagem":        {"limite": Decimal("250.00"), "periodi
         -cidade": "diaria"},                                            
      25 -}                                                              
      20  
      27 -                                                               
      21  def _texto_passo7(categoria: str, motivo_codigo: str | None, va
          lor_reembolsavel: Decimal, valor_considerado: Decimal, politica
          _eff: dict) -> str | None:
      22      if motivo_codigo is None:
      23          return None

● Update(src\motor.py)
  ⎿  Added 3 lines, removed 4 lines
      58      colaborador: Colaborador,
      59      periodo: Periodo,
      60      despesas_brutas: list[DespesaBruta],
      61 +    *,                                                         
      62 +    politica_eff: dict,                                        
      63 +    gatilho_nf: Decimal,                                       
      64      tabela_cambio: dict | None = None,
      62 -    politica_eff: dict | None = None,                          
      63 -    gatilho_nf: Decimal | None = None,                         
      65  ) -> Resultado:
      65 -    _eff = politica_eff if politica_eff is not None else _POLIT
         -ICA_V3                                                         
      66 -    _gnf = gatilho_nf if gatilho_nf is not None else Decimal("1
         -00.00")                                                        
      66      if tabela_cambio is None and any(b.moeda != "BRL" for b in 
          despesas_brutas):
      67          raise ValueError(
      68              "tabela_cambio é obrigatória quando o lote contém d
          espesas em moeda estrangeira"

● Update(src\motor.py)
  ⎿  Added 1 line, removed 1 line
      69          )
      70  
      71      vistos: dict = {}
      72 -    gc = GerenciadorCotas(_eff)                                
      72 +    gc = GerenciadorCotas(politica_eff)                        
      73      itens: list[ResultadoItem] = []
      74  
      75      for bruta in despesas_brutas:

● Update(src\motor.py)
  ⎿  Added 1 line, removed 1 line
      109  
      110          item = verificar_dominio_valor(despesa)
      111          item = item or verificar_competencia(despesa, periodo)
      112 -        item = item or verificar_categoria(despesa, _eff)     
      112 +        item = item or verificar_categoria(despesa, politica_e
          +ff)                                                           
      113          item = item or verificar_duplicata(despesa, vistos)
      114          item = item or verificar_nf(despesa, _gnf)
      115  

● Update(src\motor.py)
  ⎿  Added 1 line, removed 1 line
      111          item = item or verificar_competencia(despesa, periodo)
      112          item = item or verificar_categoria(despesa, politica_e
           ff)
      113          item = item or verificar_duplicata(despesa, vistos)
      114 -        item = item or verificar_nf(despesa, _gnf)            
      114 +        item = item or verificar_nf(despesa, gatilho_nf)      
      115  
      116          if item is None:
      117              valor_reembolsavel, motivo_codigo = gc.calcular_re
           embolso(despesa)

● Update(src\motor.py)
  ⎿  Added 1 line, removed 1 line
      122                  valor_considerado=despesa.valor_considerado,
      123                  valor_reembolsavel=valor_reembolsavel,
      124                  motivo_codigo=motivo_codigo,
      125 -                motivo_texto=_texto_passo7(despesa.categoria, 
          -motivo_codigo, valor_reembolsavel, despesa.valor_considerado, 
          -_eff),                                                        
      125 +                motivo_texto=_texto_passo7(despesa.categoria, 
          +motivo_codigo, valor_reembolsavel, despesa.valor_considerado, 
          +politica_eff),                                                
      126                  duplicata_de=None,
      127                  moeda=despesa.moeda,
      128                  taxa_cambio_aplicada=despesa.taxa_cambio_aplic
           ada,

● Agora os testes unitários — test_motor.py e test_rf18_motor.py com _POL_V3
  local:
● Update(tests\test_motor.py)
  ⎿  Added 7 lines
       6  from src.motor import processar
       7  from src.modelos import DespesaBruta
       8  
       9 +_POL_V3 = {                                                    
      10 +    "alimentacao":       {"limite": Decimal("60.00"),  "periodi
         +cidade": "dia"},                                               
      11 +    "transporte_urbano": {"limite": Decimal("80.00"),  "periodi
         +cidade": "dia"},                                               
      12 +    "hospedagem":        {"limite": Decimal("250.00"), "periodi
         +cidade": "diaria"},                                            
      13 +}                                                              
      14 +_GNF_V3 = Decimal("100.00")                                    
      15  
      16 +                                                               
      17  def _bruta(id, data=date(2026, 7, 15), categoria="alimentacao",
           descricao="Teste",
      18             fornecedor="Forn", valor="30.00", tem_nota_fiscal=Tr
          ue):
      19      return DespesaBruta(

● Update(tests\test_motor.py)
  ⎿  Added 7 lines, removed 7 lines
      26  def test_rf11_competencia_precede_nf(colaborador_padrao, period
          o_padrao):
      27      # Fora de competência E sem NF: FORA_COMPETENCIA vence (pas
          so 3 antes do 6)
      28      despesa = _bruta("d-001", data=date(2026, 4, 15), valor="15
          0.00", tem_nota_fiscal=False)
      29 -    resultado = processar(colaborador_padrao, periodo_padrao, [
         -despesa])                                                      
      29 +    resultado = processar(colaborador_padrao, periodo_padrao,[d
         +espesa])                                                       
      30      assert resultado.itens[0].motivo_codigo == "FORA_COMPETENCI
          A"
      31  
      32  
     ...
      36      # quando processado, depois SEM_NF o recusa. d-003 cai no p
          asso 5 como DUPLICATA.
      37      d1 = _bruta("d-002", valor="120.00", tem_nota_fiscal=False)
      38      d2 = _bruta("d-003", valor="120.00", tem_nota_fiscal=False)
      39 -    resultado = processar(colaborador_padrao, periodo_padrao, [
         -d1, d2])                                                       
      39 +    resultado = processar(colaborador_padrao, periodo_padrao,[d
         +1, d2])                                                        
      40      assert resultado.itens[0].motivo_codigo == "SEM_NF"
      41      assert resultado.itens[1].motivo_codigo == "DUPLICATA"
      42      assert resultado.itens[1].duplicata_de == "d-002"
     ...
      46      # Saldo parcial: primeiro item consome parte da cota, segun
          do recebe o restante.
      47      d1 = _bruta("d-001", categoria="alimentacao", valor="45.00"
          )
      48      d2 = _bruta("d-002", categoria="alimentacao", valor="40.00"
          )
      49 -    resultado = processar(colaborador_padrao, periodo_padrao, [
         -d1, d2])                                                       
      49 +    resultado = processar(colaborador_padrao, periodo_padrao,[d
         +1, d2])                                                        
      50      assert resultado.itens[0].valor_reembolsavel == Decimal("45
          .00")
      51      assert resultado.itens[1].valor_reembolsavel == Decimal("15
          .00")  # saldo = 60 - 45
      52      assert resultado.itens[1].motivo_codigo == "LIMITE_DIARIO"
     ...
      59                        valor="120.00", tem_nota_fiscal=False)
      60      d_ok = _bruta("d-002", data=date(2026, 7, 11), categoria="t
          ransporte_urbano",
      61                    valor="50.00", tem_nota_fiscal=True)
      62 -    resultado = processar(colaborador_padrao, periodo_padrao, [
         -d_sem_nf, d_ok])                                               
      62 +    resultado = processar(colaborador_padrao, periodo_padrao,[d
         +_sem_nf, d_ok])                                                
      63      assert resultado.itens[0].motivo_codigo == "SEM_NF"
      64      assert resultado.itens[1].valor_reembolsavel == Decimal("50
          .00")
      65      assert resultado.itens[1].motivo_codigo is None
     ...
      67  
      68  def test_rf13_status_aprovado(colaborador_padrao, periodo_padra
          o):
      69      despesa = _bruta("d-001", valor="30.00")
      70 -    resultado = processar(colaborador_padrao, periodo_padrao, [
         -despesa])                                                      
      70 +    resultado = processar(colaborador_padrao, periodo_padrao,[d
         +espesa])                                                       
      71      assert resultado.itens[0].status == "aprovado"
      72      assert resultado.itens[0].valor_reembolsavel == resultado.i
          tens[0].valor_considerado
      73  
      74  
      75  def test_rf13_status_parcial(colaborador_padrao, periodo_padrao
          ):
      76      despesa = _bruta("d-001", categoria="alimentacao", valor="7
          2.50")
      77 -    resultado = processar(colaborador_padrao, periodo_padrao, [
         -despesa])                                                      
      77 +    resultado = processar(colaborador_padrao, periodo_padrao,[d
         +espesa])                                                       
      78      assert resultado.itens[0].status == "parcial"
      79      assert Decimal("0.00") < resultado.itens[0].valor_reembolsa
          vel < resultado.itens[0].valor_considerado
      80  
     ...
      83      # Após cota esgotada, valor_reembolsavel == 0 → status "rec
          usado"
      84      d1 = _bruta("d-001", categoria="alimentacao", valor="60.00"
          )
      85      d2 = _bruta("d-002", categoria="alimentacao", valor="20.00"
          )
      86 -    resultado = processar(colaborador_padrao, periodo_padrao, [
         -d1, d2])                                                       
      86 +    resultado = processar(colaborador_padrao, periodo_padrao,[d
         +1, d2])                                                        
      87      assert resultado.itens[1].motivo_codigo == "COTA_ESGOTADA"
      88      assert resultado.itens[1].valor_reembolsavel == Decimal("0.
          00")
      89      assert resultado.itens[1].status == "recusado"

  Read 1 file (ctrl+o to expand)

● Preciso adicionar os kwargs a cada chamada de processar. Vou usar replace_all
  para os dois padrões repetidos e uma edição pontual para o terceiro:

● Update(tests\test_motor.py)
  ⎿  Added 3 lines, removed 3 lines
      26  def test_rf11_competencia_precede_nf(colaborador_padrao, period
          o_padrao):
      27      # Fora de competência E sem NF: FORA_COMPETENCIA vence (pas
          so 3 antes do 6)
      28      despesa = _bruta("d-001", data=date(2026, 4, 15), valor="15
          0.00", tem_nota_fiscal=False)
      29 -    resultado = processar(colaborador_padrao, periodo_padrao,[d
         -espesa])                                                       
      29 +    resultado = processar(colaborador_padrao, periodo_padrao, [
         +despesa], politica_eff=_POL_V3, gatilho_nf=_GNF_V3)            
      30      assert resultado.itens[0].motivo_codigo == "FORA_COMPETENCI
          A"
      31  
      32  
     ...
      67  
      68  def test_rf13_status_aprovado(colaborador_padrao, periodo_padra
          o):
      69      despesa = _bruta("d-001", valor="30.00")
      70 -    resultado = processar(colaborador_padrao, periodo_padrao,[d
         -espesa])                                                       
      70 +    resultado = processar(colaborador_padrao, periodo_padrao, [
         +despesa], politica_eff=_POL_V3, gatilho_nf=_GNF_V3)            
      71      assert resultado.itens[0].status == "aprovado"
      72      assert resultado.itens[0].valor_reembolsavel == resultado.i
          tens[0].valor_considerado
      73  
      74  
      75  def test_rf13_status_parcial(colaborador_padrao, periodo_padrao
          ):
      76      despesa = _bruta("d-001", categoria="alimentacao", valor="7
          2.50")
      77 -    resultado = processar(colaborador_padrao, periodo_padrao,[d
         -espesa])                                                       
      77 +    resultado = processar(colaborador_padrao, periodo_padrao, [
         +despesa], politica_eff=_POL_V3, gatilho_nf=_GNF_V3)            
      78      assert resultado.itens[0].status == "parcial"
      79      assert Decimal("0.00") < resultado.itens[0].valor_reembolsa
          vel < resultado.itens[0].valor_considerado
      80  

● Update(tests\test_motor.py)
  ⎿  Added 3 lines, removed 3 lines
      36      # quando processado, depois SEM_NF o recusa. d-003 cai no p
          asso 5 como DUPLICATA.
      37      d1 = _bruta("d-002", valor="120.00", tem_nota_fiscal=False)
      38      d2 = _bruta("d-003", valor="120.00", tem_nota_fiscal=False)
      39 -    resultado = processar(colaborador_padrao, periodo_padrao,[d
         -1, d2])                                                        
      39 +    resultado = processar(colaborador_padrao, periodo_padrao, [
         +d1, d2], politica_eff=_POL_V3, gatilho_nf=_GNF_V3)             
      40      assert resultado.itens[0].motivo_codigo == "SEM_NF"
      41      assert resultado.itens[1].motivo_codigo == "DUPLICATA"
      42      assert resultado.itens[1].duplicata_de == "d-002"
     ...
      46      # Saldo parcial: primeiro item consome parte da cota, segun
          do recebe o restante.
      47      d1 = _bruta("d-001", categoria="alimentacao", valor="45.00"
          )
      48      d2 = _bruta("d-002", categoria="alimentacao", valor="40.00"
          )
      49 -    resultado = processar(colaborador_padrao, periodo_padrao,[d
         -1, d2])                                                        
      49 +    resultado = processar(colaborador_padrao, periodo_padrao, [
         +d1, d2], politica_eff=_POL_V3, gatilho_nf=_GNF_V3)             
      50      assert resultado.itens[0].valor_reembolsavel == Decimal("45
          .00")
      51      assert resultado.itens[1].valor_reembolsavel == Decimal("15
          .00")  # saldo = 60 - 45
      52      assert resultado.itens[1].motivo_codigo == "LIMITE_DIARIO"
     ...
      83      # Após cota esgotada, valor_reembolsavel == 0 → status "rec
          usado"
      84      d1 = _bruta("d-001", categoria="alimentacao", valor="60.00"
          )
      85      d2 = _bruta("d-002", categoria="alimentacao", valor="20.00"
          )
      86 -    resultado = processar(colaborador_padrao, periodo_padrao,[d
         -1, d2])                                                        
      86 +    resultado = processar(colaborador_padrao, periodo_padrao, [
         +d1, d2], politica_eff=_POL_V3, gatilho_nf=_GNF_V3)             
      87      assert resultado.itens[1].motivo_codigo == "COTA_ESGOTADA"
      88      assert resultado.itens[1].valor_reembolsavel == Decimal("0.
          00")
      89      assert resultado.itens[1].status == "recusado"

● Update(tests\test_motor.py)
  ⎿  Added 1 line, removed 1 line
      59                        valor="120.00", tem_nota_fiscal=False)
      60      d_ok = _bruta("d-002", data=date(2026, 7, 11), categoria="t
          ransporte_urbano",
      61                    valor="50.00", tem_nota_fiscal=True)
      62 -    resultado = processar(colaborador_padrao, periodo_padrao,[d
         -_sem_nf, d_ok])                                                
      62 +    resultado = processar(colaborador_padrao, periodo_padrao, [
         +d_sem_nf, d_ok], politica_eff=_POL_V3, gatilho_nf=_GNF_V3)     
      63      assert resultado.itens[0].motivo_codigo == "SEM_NF"
      64      assert resultado.itens[1].valor_reembolsavel == Decimal("50
          .00")
      65      assert resultado.itens[1].motivo_codigo is None

● Agora test_rf18_motor.py:

● Update(tests\test_rf18_motor.py)
  ⎿  Added 7 lines
      10  from src.modelos import DespesaBruta
      11  from src.motor import processar
      12  
      13 +_POL_V3 = {                                                    
      14 +    "alimentacao":       {"limite": Decimal("60.00"),  "periodi
         +cidade": "dia"},                                               
      15 +    "transporte_urbano": {"limite": Decimal("80.00"),  "periodi
         +cidade": "dia"},                                               
      16 +    "hospedagem":        {"limite": Decimal("250.00"), "periodi
         +cidade": "diaria"},                                            
      17 +}                                                              
      18 +_GNF_V3 = Decimal("100.00")                                    
      19 +                                                               
      20  _TABELA = {
      21      date(2026, 7, 14): {"EUR": Decimal("5.93")},
      22      date(2026, 7, 15): {"EUR": Decimal("5.88")},

● Update(tests\test_rf18_motor.py)
  ⎿  Added 12 lines
      41          colaborador_padrao, periodo_padrao,
      42          [_bruta("e-002", valor="22.00", moeda="EUR", data=date(
          2026, 7, 14))],
      43          tabela_cambio=_TABELA,
      44 +        politica_eff=_POL_V3,                                  
      45 +        gatilho_nf=_GNF_V3,                                    
      46      ).itens[0]
      47      assert item.valor_original == Decimal("22.00")
      48      assert item.moeda == "EUR"
     ...
      56          colaborador_padrao, periodo_padrao,
      57          [_bruta("e-x", valor="14.50", moeda="EUR", data=date(20
          26, 7, 15))],
      58          tabela_cambio=_TABELA,
      59 +        politica_eff=_POL_V3,                                  
      60 +        gatilho_nf=_GNF_V3,                                    
      61      ).itens[0]
      62      assert item.valor_original == Decimal("14.50")
      63      assert item.valor_considerado == Decimal("85.26")
     ...
      69          colaborador_padrao, periodo_padrao,
      70          [_bruta("e-006", moeda="GBP", valor="55.00", data=date(
          2026, 7, 21))],
      71          tabela_cambio=_TABELA,
      72 +        politica_eff=_POL_V3,                                  
      73 +        gatilho_nf=_GNF_V3,                                    
      74      ).itens[0]
      75      assert item.motivo_codigo == "MOEDA_NAO_SUPORTADA"
      76      assert item.status == "recusado"
     ...
      85          colaborador_padrao, periodo_padrao,
      86          [_bruta("e-x2", moeda="USD", valor="40.00", data=date(2
          026, 7, 1))],
      87          tabela_cambio=_TABELA,
      88 +        politica_eff=_POL_V3,                                  
      89 +        gatilho_nf=_GNF_V3,                                    
      90      ).itens[0]
      91      assert item.motivo_codigo == "TAXA_INDISPONIVEL"
      92      assert item.status == "recusado"
     ...
      100          colaborador_padrao, periodo_padrao,
      101          [_bruta("d-x", valor="33.333", moeda="BRL")],
      102          tabela_cambio=_TABELA,
      103 +        politica_eff=_POL_V3,                                 
      104 +        gatilho_nf=_GNF_V3,                                   
      105      ).itens[0]
      106      assert item.moeda == "BRL"
      107      assert item.taxa_cambio_aplicada is None
     ...
      116          [_bruta("e-005", categoria="transporte_urbano", valor=
           "40.00",
      117                  moeda="USD", data=date(2026, 7, 20), tem_nota_
           fiscal=False)],
      118          tabela_cambio=_TABELA,
      119 +        politica_eff=_POL_V3,                                 
      120 +        gatilho_nf=_GNF_V3,                                   
      121      ).itens[0]
      122      assert item.motivo_codigo == "SEM_NF"
      123      assert item.moeda == "USD"

● Agora test_integracao.py — reescrita completa com política real e assertions
  baseadas na saída real:

● Write(tests\test_integracao.py)
  ⎿  Added 37 lines, removed 36 lines
       6  from src.motor import processar
       7  from src.normalizacao import normalizar_categoria
       8  from src.parser import carregar_entrada
       9 +from src.parser_politica import carregar_politica, nota_fiscal_
         +gatilho, politica_efetiva                                      
      10  from src.serializador import serializar
      11  
      12  _EXEMPLO = Path(__file__).parent.parent / "exemplos" / "despesa
          s-exemplo.json"
      13 +_POLITICA_PATH = Path(__file__).parent.parent / "exemplos" / "e
         +nvelope" / "politica-v4.json"                                  
      14  
      13 -_LIMITE_V3 = {                                                 
      14 -    "alimentacao": Decimal("60.00"),                           
      15 -    "transporte_urbano": Decimal("80.00"),                     
      16 -    "hospedagem": Decimal("250.00"),                           
      17 -}                                                              
      15 +_pol = carregar_politica(_POLITICA_PATH)                       
      16 +_gnf = nota_fiscal_gatilho(_pol)                               
      17  
      18  
      19  @pytest.fixture(scope="module")
      20  def _resultado():
      21      colaborador, periodo, despesas = carregar_entrada(_EXEMPLO)
      23 -    return processar(colaborador, periodo, despesas)           
      22 +    eff = politica_efetiva(_pol, colaborador.centro_custo)     
      23 +    return processar(colaborador, periodo, despesas, politica_e
         +ff=eff, gatilho_nf=_gnf)                                       
      24  
      25  
      26  @pytest.fixture(scope="module")
     ...
      29  
      30  
      31  def test_integracao_d001(_por_id):
      32 -    # d-001: alimentação R$72,50 → parcial R$60,00 (LIMITE_DIAR
         -IO)                                                            
      32 +    # d-001: alimentação R$72,50 → aprovado (CC-ENG-PLATAFORMA 
         +limite=75; 72,50 < 75)                                         
      33      item = _por_id["d-001"]
      34 -    assert item.status == "parcial"                            
      35 -    assert item.valor_reembolsavel == Decimal("60.00")         
      36 -    assert item.motivo_codigo == "LIMITE_DIARIO"               
      34 +    assert item.status == "aprovado"                           
      35 +    assert item.valor_reembolsavel == Decimal("72.50")         
      36 +    assert item.motivo_codigo is None                          
      37  
      38  
      39  def test_integracao_d002(_por_id):
      40 -    # d-002: alimentação R$38,00, segundo de 03/07 → recusado (
         -COTA_ESGOTADA)                                                 
      40 +    # d-002: alimentação R$38,00, mesmo dia de d-001 — saldo re
         +stante = 75 - 72,50 = 2,50                                     
      41      item = _por_id["d-002"]
      42 -    assert item.status == "recusado"                           
      43 -    assert item.valor_reembolsavel == Decimal("0.00")          
      44 -    assert item.motivo_codigo == "COTA_ESGOTADA"               
      42 +    assert item.status == "parcial"                            
      43 +    assert item.valor_reembolsavel == Decimal("2.50")          
      44 +    assert item.motivo_codigo == "LIMITE_DIARIO"               
      45  
      46  
      47  def test_integracao_d003(_por_id):
     ...
       91  
       92  
       93  def test_integracao_d009(_por_id):
       94 -    # d-009: transporte -R$45,00 → recusado VALOR_NAO_POSITIVO
          -; motivo VALOR_NAO_POSITIVO                                   
       95 -    # prova que passo 7 não foi alcançado → cota de transporte
          - de 11/07 não afetada                                         
       94 +    # d-009: transporte -R$45,00 → recusado VALOR_NAO_POSITIVO
       95      item = _por_id["d-009"]
       96      assert item.status == "recusado"
       97      assert item.motivo_codigo == "VALOR_NAO_POSITIVO"
       98  
       99  
      100  def test_integracao_d010(_por_id):
      102 -    # d-010: hospedagem R$480,00 ("Hotel Rio - 2 diárias") → p
          -arcial R$250,00;                                              
      103 -    # motivo_texto cita "limite de 1 diária" (RF-10, D-004 — n
          -um_diarias ausente do schema)                                 
      101 +    # d-010: hospedagem R$480,00 → CC-ENG-PLATAFORMA limite=0,
          +00 → COTA_ESGOTADA                                            
      102      item = _por_id["d-010"]
      105 -    assert item.status == "parcial"                           
      106 -    assert item.valor_reembolsavel == Decimal("250.00")       
      107 -    assert item.motivo_codigo == "LIMITE_DIARIO"              
      108 -    assert "limite de 1 diária" in item.motivo_texto          
      103 +    assert item.status == "recusado"                          
      104 +    assert item.valor_reembolsavel == Decimal("0.00")         
      105 +    assert item.motivo_codigo == "COTA_ESGOTADA"              
      106 +    assert "R$ 0,00" in item.motivo_texto                     
      107  
      108  
      109  def test_integracao_d011(_por_id):
     ...
      123  
      124  
      125  def test_integracao_d013(_por_id):
      128 -    # d-013: hospedagem R$690,00 sem NF → recusado SEM_NF (lim
          -ite de hospedagem nunca avaliado)                             
      126 +    # d-013: hospedagem R$690,00 sem NF → recusado SEM_NF (NF 
          +check antes de cotas)                                         
      127      item = _por_id["d-013"]
      128      assert item.status == "recusado"
      129      assert item.motivo_codigo == "SEM_NF"
      130  
      131  
      132  def test_integracao_d014(_por_id):
      135 -    # d-014: "ALIMENTACAO" R$61,00 → normalizada; valor_consid
          -erado 61.00; parcial R$60,00                                  
      133 +    # d-014: "ALIMENTACAO" R$61,00 → normalizada; CC-ENG limit
          +e=75; 61 < 75 → aprovado                                      
      134      item = _por_id["d-014"]
      135      assert item.valor_considerado == Decimal("61.00")
      138 -    assert item.status == "parcial"                           
      139 -    assert item.valor_reembolsavel == Decimal("60.00")        
      140 -    assert item.motivo_codigo == "LIMITE_DIARIO"              
      136 +    assert item.status == "aprovado"                          
      137 +    assert item.valor_reembolsavel == Decimal("61.00")        
      138 +    assert item.motivo_codigo is None                         
      139  
      140  
      141  def test_integracao_saida_deterministica():
      142      # Critério 15: duas execuções com a mesma entrada produzem
            saída byte a byte idêntica
      143      colaborador, periodo, despesas = carregar_entrada(_EXEMPLO
           )
      144 +    eff = politica_efetiva(_pol, colaborador.centro_custo)    
      145      assert (
      147 -        serializar(processar(colaborador, periodo, despesas)) 
      148 -        == serializar(processar(colaborador, periodo, despesas
          -))                                                            
      146 +        serializar(processar(colaborador, periodo, despesas, p
          +olitica_eff=eff, gatilho_nf=_gnf))                            
      147 +        == serializar(processar(colaborador, periodo, despesas
          +, politica_eff=eff, gatilho_nf=_gnf))                         
      148      )
      149  
      150  
      151  def test_integracao_nenhum_item_acima_do_limite_da_categoria()
           :
      153 -    # Critério 16: para cada item de categoria válida, valor_r
          -eembolsavel ≤ limite base                                     
      152 +    # Critério 16: para cada item de categoria válida, valor_r
          +eembolsavel ≤ limite efetivo                                  
      153      colaborador, periodo, despesas = carregar_entrada(_EXEMPLO
           )
      155 -    resultado = processar(colaborador, periodo, despesas)     
      154 +    eff = politica_efetiva(_pol, colaborador.centro_custo)    
      155 +    resultado = processar(colaborador, periodo, despesas, poli
          +tica_eff=eff, gatilho_nf=_gnf)                                
      156      por_id = {item.id: item for item in resultado.itens}
      157      for bruta in despesas:
      158          categoria = normalizar_categoria(bruta.categoria)
      159 -        if categoria in _LIMITE_V3:                           
      160 -            assert por_id[bruta.id].valor_reembolsavel <= _LIM
          -ITE_V3[categoria]                                             
      159 +        if categoria in eff:                                  
      160 +            limite = eff[categoria]["limite"]                 
      161 +            assert por_id[bruta.id].valor_reembolsavel <= limi
          +te                                                            
      162  
      163  
      164  def test_integracao_viagem_suspensa_sem_ampliacao(_por_id):
      165      # Critério 17: nenhum item recebe limites ampliados de via
           gem (RF-16 suspenso)
      165 -    # Com viagem ativa: hospedagem → 375,00; transporte → 120,
          -00. Sem ampliação:                                            
      166 -    assert _por_id["d-010"].valor_reembolsavel == Decimal("250
          -.00")  # não 375,00                                           
      167 -    assert _por_id["d-003"].valor_reembolsavel == Decimal("80.
          -00")   # não 120,00                                           
      166 +    # CC-ENG-PLATAFORMA: transporte limite=80 (seria 120 com R
          +F-16); hospedagem limite=0                                    
      167 +    assert _por_id["d-010"].valor_reembolsavel == Decimal("0.0
          +0")   # não 375,00 nem 250,00                                 
      168 +    assert _por_id["d-003"].valor_reembolsavel == Decimal("80.
          +00")  # não 120,00                                            

● Agora test_rf16_viagem_suspensa.py com política real:

● Write(tests\test_rf16_viagem_suspensa.py)
  ⎿  Added 9 lines, removed 10 lines
       4  from src.motor import processar
       5  from src.normalizacao import normalizar_categoria
       6  from src.parser import carregar_entrada
       7 +from src.parser_politica import carregar_politica, nota_fiscal_
         +gatilho, politica_efetiva                                      
       8  
       9  _EXEMPLO = Path(__file__).parent.parent / "exemplos" / "despesa
          s-exemplo.json"
      10 +_POLITICA_PATH = Path(__file__).parent.parent / "exemplos" / "e
         +nvelope" / "politica-v4.json"                                  
      11  
      10 -_LIMITE_V3 = {                                                 
      11 -    "alimentacao": Decimal("60.00"),                           
      12 -    "transporte_urbano": Decimal("80.00"),                     
      13 -    "hospedagem": Decimal("250.00"),                           
      14 -}                                                              
      12 +_pol = carregar_politica(_POLITICA_PATH)                       
      13 +_gnf = nota_fiscal_gatilho(_pol)                               
      14  
      15  
      16  def test_rf16_nenhum_item_com_limite_ampliado():
      17      # Regra de viagem (limites ampliados) está suspensa por AMB
          -006.
      19 -    # Nenhum item de nenhuma categoria deve receber valor_reemb
         -olsavel acima                                                  
      20 -    # do limite padrão da categoria (60,00 / 80,00 / 250,00).  
      18 +    # Nenhum item deve receber valor_reembolsavel acima do limi
         +te efetivo da categoria.                                       
      19      colaborador, periodo, despesas_brutas = carregar_entrada(_E
          XEMPLO)
      22 -    resultado = processar(colaborador, periodo, despesas_brutas
         -)                                                              
      20 +    eff = politica_efetiva(_pol, colaborador.centro_custo)     
      21 +    resultado = processar(colaborador, periodo, despesas_brutas
         +, politica_eff=eff, gatilho_nf=_gnf)                           
      22  
      23      categoria_por_id = {d.id: normalizar_categoria(d.categoria)
           for d in despesas_brutas}
      24      for item in resultado.itens:
      25          categoria = categoria_por_id[item.id]
      27 -        limite = _LIMITE_V3.get(categoria)                     
      28 -        if limite is None:                                     
      26 +        if categoria not in eff:                               
      27              continue  # categoria inválida já recusada no passo
           4
      28 +        limite = eff[categoria]["limite"]                      
      29          assert item.valor_reembolsavel <= limite, (
      30              f"{item.id} ({categoria}): valor_reembolsavel {item
          .valor_reembolsavel}"
      31              f" > limite {limite} — indica limite de viagem apli
          cado indevidamente"

● Por fim, o teste de aceite test_rf14_campos_moeda_na_saida no serializador:

● Update(tests\test_rf14_serializador.py)
  ⎿  Added 26 lines
       81      assert "colaborador" in parsed
       82      assert "resumo" in parsed
       83      assert "itens" in parsed
       84 +                                                              
       85 +                                                              
       86 +def test_rf14_campos_moeda_na_saida():                        
       87 +    # BRL: moeda="BRL", taxa_cambio_aplicada=null             
       88 +    item_brl = _item()                                        
       89 +    saida_brl = json.loads(serializar(_make_resultado([item_br
          +l])))                                                         
       90 +    item_json = saida_brl["itens"][0]                         
       91 +    assert item_json["moeda"] == "BRL"                        
       92 +    assert item_json["taxa_cambio_aplicada"] is None          
       93 +                                                              
       94 +    # EUR: moeda="EUR", taxa_cambio_aplicada=5.93 (2dp)       
       95 +    item_eur = ResultadoItem(                                 
       96 +        id="e-001", status="aprovado",                        
       97 +        valor_original=Decimal("22.00"),                      
       98 +        valor_considerado=Decimal("130.46"),                  
       99 +        valor_reembolsavel=Decimal("60.00"),                  
      100 +        motivo_codigo="LIMITE_DIARIO",                        
      101 +        motivo_texto=None,                                    
      102 +        duplicata_de=None,                                    
      103 +        moeda="EUR",                                          
      104 +        taxa_cambio_aplicada=Decimal("5.93"),                 
      105 +    )                                                         
      106 +    saida_eur = json.loads(serializar(_make_resultado([item_eu
          +r])))                                                         
      107 +    item_eur_json = saida_eur["itens"][0]                     
      108 +    assert item_eur_json["moeda"] == "EUR"                    
      109 +    assert item_eur_json["taxa_cambio_aplicada"] == 5.93      

● Suite completa:

  Ran 1 shell command (ctrl+o to expand)

● Mais 4 arquivos de teste a corrigir. Leio os três restantes em paralelo:

  Read 4 files (ctrl+o to expand)

● Agora corrijo os 4 arquivos restantes em paralelo:

  test_borda.py e test_rf14_resumo.py recebem _POL_V3 local (testes de
  mecanismo); test_rf15_fim_de_semana.py usa política v4 real (carrega o mesmo
  despesas-exemplo.json); test_cli.py precisa de --politica + --cambio nos
  testes existentes e teste novo para --politica ausente.

● Update(tests\test_borda.py)
  ⎿  Added 7 lines
      24  from src.modelos import DespesaBruta
      25  from src.motor import processar
      26  
      27 +_POL_V3 = {                                                    
      28 +    "alimentacao":       {"limite": Decimal("60.00"),  "periodi
         +cidade": "dia"},                                               
      29 +    "transporte_urbano": {"limite": Decimal("80.00"),  "periodi
         +cidade": "dia"},                                               
      30 +    "hospedagem":        {"limite": Decimal("250.00"), "periodi
         +cidade": "diaria"},                                            
      31 +}                                                              
      32 +_GNF_V3 = Decimal("100.00")                                    
      33  
      34 +                                                               
      35  def _bruta(id, categoria="alimentacao", valor="30.00", tem_nota
          _fiscal=True,
      36             data=date(2026, 7, 14), descricao="Teste", fornecedo
          r="Forn"):
      37      return DespesaBruta(

● Update(tests\test_borda.py)
  ⎿  Added 1 line
      47      item = processar(
      48          colaborador_padrao, periodo_padrao,
      49          [_bruta("d-h01", categoria="hospedagem", valor="690.00"
          , tem_nota_fiscal=False)],
      50 +        politica_eff=_POL_V3, gatilho_nf=_GNF_V3,              
      51      ).itens[0]
      52      assert item.motivo_codigo == "SEM_NF"
      53      assert item.valor_reembolsavel == Decimal("0.00")

● Update(tests\test_borda.py)  ⎿  Added 1 line
      59      item = processar(
      60          colaborador_padrao, periodo_padrao,
      61          [_bruta("d-z01", valor="0.00")],
      62 +        politica_eff=_POL_V3, gatilho_nf=_GNF_V3,              
      63      ).itens[0]
      64      assert item.motivo_codigo == "VALOR_NAO_POSITIVO"
      65      assert item.valor_reembolsavel == Decimal("0.00")

● Update(tests\test_rf14_resumo.py)
  ⎿  Added 7 lines
       4  from src.modelos import DespesaBruta
       5  from src.motor import processar
       6  
       7 +_POL_V3 = {                                                    
       8 +    "alimentacao":       {"limite": Decimal("60.00"),  "periodi
         +cidade": "dia"},                                               
       9 +    "transporte_urbano": {"limite": Decimal("80.00"),  "periodi
         +cidade": "dia"},                                               
      10 +    "hospedagem":        {"limite": Decimal("250.00"), "periodi
         +cidade": "diaria"},                                            
      11 +}                                                              
      12 +_GNF_V3 = Decimal("100.00")                                    
      13  
      14 +                                                               
      15  def _bruta(id, categoria="alimentacao", valor="30.00", data=dat
          e(2026, 7, 15),
      16             descricao="Teste", fornecedor="Forn", tem_nota_fisca
          l=True):
      17      return DespesaBruta(

● Update(tests\test_rf14_resumo.py)
  ⎿  Added 2 lines, removed 2 lines
      30          _bruta("d-005", categoria="coworking", valor="89.00"),
      31          _bruta("d-006", categoria="alimentacao", valor="54.90",
           data=date(2026, 7, 16)),
      32      ]
      33 -    resultado = processar(colaborador_padrao, periodo_padrao, d
         -espesas)                                                       
      33 +    resultado = processar(colaborador_padrao, periodo_padrao, d
         +espesas, politica_eff=_POL_V3, gatilho_nf=_GNF_V3)             
      34      resumo = resultado.resumo
      35  
      36      assert resumo.total_solicitado == Decimal("216.40")   # 72.
          50 + 89.00 + 54.90
     ...
      48          _bruta("d-neg", valor="-45.00"),
      49          _bruta("d-pos", valor="30.00", data=date(2026, 7, 16)),
      50      ]
      51 -    resultado = processar(colaborador_padrao, periodo_padrao, d
         -espesas)                                                       
      51 +    resultado = processar(colaborador_padrao, periodo_padrao, d
         +espesas, politica_eff=_POL_V3, gatilho_nf=_GNF_V3)             
      52      assert resultado.resumo.total_solicitado == Decimal("30.00"
          )
      53      assert resultado.resumo.itens_recusados == 1
      54      assert resultado.resumo.itens_aprovados == 1

● Write(tests\test_rf15_fim_de_semana.py)
  ⎿  Added 7 lines, removed 1 line
       3  
       4  from src.motor import processar
       5  from src.parser import carregar_entrada
       6 +from src.parser_politica import carregar_politica, nota_fiscal_
         +gatilho, politica_efetiva                                      
       7  
       8  _EXEMPLO = Path(__file__).parent.parent / "exemplos" / "despesa
          s-exemplo.json"
       9 +_POLITICA_PATH = Path(__file__).parent.parent / "exemplos" / "e
         +nvelope" / "politica-v4.json"                                  
      10  
      11 +_pol = carregar_politica(_POLITICA_PATH)                       
      12 +_gnf = nota_fiscal_gatilho(_pol)                               
      13  
      14 +                                                               
      15  def _resultado():
      16      colaborador, periodo, despesas = carregar_entrada(_EXEMPLO)
      12 -    return processar(colaborador, periodo, despesas)           
      17 +    eff = politica_efetiva(_pol, colaborador.centro_custo)     
      18 +    return processar(colaborador, periodo, despesas, politica_e
         +ff=eff, gatilho_nf=_gnf)                                       
      19  
      20  
      21  def test_rf15_sabado_processado_normalmente():

● Write(tests\test_cli.py)
  ⎿  Added 29 lines, removed 3 lines
       3  import sys
       4  from pathlib import Path
       5  
       6 -_EXEMPLO = Path(__file__).parent.parent / "exemplos" / "despesa
         -s-exemplo.json"                                                
       6 +_EXEMPLO   = Path(__file__).parent.parent / "exemplos" / "despe
         +sas-exemplo.json"                                              
       7 +_POLITICA  = Path(__file__).parent.parent / "exemplos" / "envel
         +ope" / "politica-v4.json"                                      
       8 +_CAMBIO    = Path(__file__).parent.parent / "exemplos" / "envel
         +ope" / "cambio.json"                                           
       9  
      10  
      11  def _run(*args):
     ...
      19  
      20  def test_cli_arquivo_valido_codigo_0(tmp_path):
      21      saida = tmp_path / "resultado.json"
      20 -    proc = _run("calcular", "--input", str(_EXEMPLO), "--output
         -", str(saida))                                                 
      22 +    proc = _run(                                               
      23 +        "calcular",                                            
      24 +        "--input",    str(_EXEMPLO),                           
      25 +        "--output",   str(saida),                              
      26 +        "--politica", str(_POLITICA),                          
      27 +        "--cambio",   str(_CAMBIO),                            
      28 +    )                                                          
      29      assert proc.returncode == 0
      30      assert saida.exists()
      31      dados = json.loads(saida.read_text(encoding="utf-8"))
     ...
      35  
      36  def test_cli_arquivo_inexistente_codigo_1(tmp_path):
      37      saida = tmp_path / "resultado.json"
      30 -    proc = _run("calcular", "--input", "nao_existe.json", "--ou
         -tput", str(saida))                                             
      38 +    proc = _run(                                               
      39 +        "calcular",                                            
      40 +        "--input",    "nao_existe.json",                       
      41 +        "--output",   str(saida),                              
      42 +        "--politica", str(_POLITICA),                          
      43 +        "--cambio",   str(_CAMBIO),                            
      44 +    )                                                          
      45      assert proc.returncode == 1
      46      assert "não encontrado" in proc.stderr
      47      assert not saida.exists()
      48 +                                                               
      49 +                                                               
      50 +def test_cli_sem_politica_erro(tmp_path):                      
      51 +    saida = tmp_path / "resultado.json"                        
      52 +    proc = _run(                                               
      53 +        "calcular",                                            
      54 +        "--input",  str(_EXEMPLO),                             
      55 +        "--output", str(saida),                                
      56 +        "--cambio", str(_CAMBIO),                              
      57 +    )                                                          
      58 +    assert proc.returncode != 0                                
      59 +    assert "--politica" in proc.stderr                         

  Ran 1 shell command (ctrl+o to expand)

● 108 passando, zero falhas. Antes de sugerir o commit, pontos para você
  verificar:

  O que mudou em T-028:

  1. src/serializador.py: moeda e taxa_cambio_aplicada adicionados em _item_dict
   após valor_original; null para BRL, 2dp para moeda estrangeira.
  2. src/cli.py: reescrito com --politica e --cambio obrigatórios; _arquivo()
  para verificação de existência com mensagem clara e exit 1; carrega política +
   câmbio e passa ao motor.
  3. src/motor.py: _POLITICA_V3 removido; assinatura usa * — politica_eff e
  gatilho_nf agora são keyword-only required; tabela_cambio permanece
  keyword-only opcional.
  4. Testes com isolamento (_POL_V3 local): test_motor.py, test_rf18_motor.py,
  test_borda.py, test_rf14_resumo.py — testam mecanismo, não política real.
  5. Testes com política v4 real: test_integracao.py,
  test_rf15_fim_de_semana.py, test_rf16_viagem_suspensa.py — carregam
  politica-v4.json de fato.
  6. Assertions atualizadas a partir da saída real (não estimativa): d-001
  aprovado/72.50, d-002 parcial/2.50, d-010 COTA_ESGOTADA/0.00, d-014
  aprovado/61.00.

  Ponto fraco para conferir: test_cli_sem_politica_erro verifica returncode != 0
   (argparse retorna 2, não 1, para argumento faltando). O critério da spec
  dizia "código 1" mas argparse usa 2 para erros de parsing — assers != 0 é
  correto para o que o código realmente faz.

  Mensagem de commit sugerida: feat(T-028): serializador e CLI com campos v2 e 
  novos argumentos (RF-14, AMB-025, D-013)

✻ Cooked for 9m 59s

※ recap: Implementando o motor de reembolso v2 (política externalizada + câmbio) em Python. T-028 está pronto e aguarda aprovação para commit antes de seguir para T-029, os testes de integração do envelope.

> Aprovo a maior parte, com três pendências antes do commit:                    
                                                                                
  1. O != 0 para --politica ausente está correto tecnicamente, mas expõe uma    
  decisão de spec nunca declarada: agora existem 2 códigos de saída de erro (1  
  = arquivo/dado inválido; 2 = argumento CLI ausente, nativo do argparse).      
  Registre isso como uma linha no RF-16/CLI da spec ou uma entrada curta no     
  DECISIONS.md — comportamento observável sem declaração é exatamente o padrão  
  que temos caçado o dia inteiro.                                               
                                                                                
  2. Mostre o motivo_texto REAL e completo gerado para d-010 (COTA_ESGOTADA com 
   limite 0,00) — não só confirmar que contém "R$ 0,00". Quero ler a frase      
  inteira e avaliar se "já consumidos por itens anteriores no dia" ainda faz    
  sentido quando o limite nasce zerado (ninguém consumiu nada, o limite já era  
  zero). Se soar estranho, pode precisar de um terceiro caso no template do     
  D-003/D-014 para "limite igual a zero" versus "esgotado por consumo real".    
                                                                                
  3. test_integracao_viagem_suspensa_sem_ampliacao (critério 17): com d-010     
  agora em 0,00 por exclusão de CC, esse item deixou de provar isoladamente     
  "viagem suspensa" — ele prova "categoria excluída", que é outra coisa (RF-17, 
   não RF-16). O teste continua tecnicamente correto, mas fica mais fraco como  
  prova do RF-16. Considere se vale adicionar outro exemplo (ex.: alimentação   
  ou transporte de um CC que NÃO zera a categoria) para provar de forma mais    
  limpa que a ampliação de viagem não está sendo aplicada, distinto de exclusão 
   por política.                                                                
                                                                                
  Depois desses três pontos, aprovo e commitamos.                               
  ⎿  You're out of extra usage · resets 3:30am (America/Fortaleza)
     /upgrade or /extra-usage to finish what you’re working on.

✻ Baked for 0s

> Aprovo a maior parte, com três pendências antes do commit:                    
                                                                                
  1. O != 0 para --politica ausente está correto tecnicamente, mas expõe uma    
  decisão de spec nunca declarada: agora existem 2 códigos de saída de erro (1  
  = arquivo/dado inválido; 2 = argumento CLI ausente, nativo do argparse).      
  Registre isso como uma linha no RF-16/CLI da spec ou uma entrada curta no     
  DECISIONS.md — comportamento observável sem declaração é exatamente o padrão  
  que temos caçado o dia inteiro.                                               
                                                                                
  2. Mostre o motivo_texto REAL e completo gerado para d-010 (COTA_ESGOTADA com 
   limite 0,00) — não só confirmar que contém "R$ 0,00". Quero ler a frase      
  inteira e avaliar se "já consumidos por itens anteriores no dia" ainda faz    
  sentido quando o limite nasce zerado (ninguém consumiu nada, o limite já era  
  zero). Se soar estranho, pode precisar de um terceiro caso no template do     
  D-003/D-014 para "limite igual a zero" versus "esgotado por consumo real".    
                                                                                
  3. test_integracao_viagem_suspensa_sem_ampliacao (critério 17): com d-010     
  agora em 0,00 por exclusão de CC, esse item deixou de provar isoladamente     
  "viagem suspensa" — ele prova "categoria excluída", que é outra coisa (RF-17, 
   não RF-16). O teste continua tecnicamente correto, mas fica mais fraco como  
  prova do RF-16. Considere se vale adicionar outro exemplo (ex.: alimentação   
  ou transporte de um CC que NÃO zera a categoria) para provar de forma mais    
  limpa que a ampliação de viagem não está sendo aplicada, distinto de exclusão 
   por política.                                                                
                                                                                
  Depois desses três pontos, aprovo e commitamos.                               

● Três pontos examinados. Respondo cada um com proposta concreta.

  ---
  Ponto 1 — Códigos de saída CLI

  O texto completo do motivo_texto de d-010:
  cota diária de hospedagem esgotada: R$ 0,00 já consumidos por itens anteriores
   no dia

  Rascunho de entrada para DECISIONS.md (D-015, nova):

  ▎ D-015 — Códigos de saída CLI: 1 = erro de dado/arquivo; 2 = argumento 
  ▎ ausente (argparse nativo)
  ▎
  ▎ Decisão: O motor CLI usa dois códigos de erro distintos: 1 para arquivos não
  ▎  encontrados ou dados inválidos (controlado pelo código); 2 para argumentos 
  ▎ obrigatórios ausentes (comportamento padrão do argparse, não intercetado). 
  ▎ Nenhum wrapper captura o SystemExit(2) do argparse.
  ▎
  ▎ Por quê: Interceptar o argparse para converter 2 → 1 exige sobrescrever 
  ▎ error() no parser, adicionando código sem valor operacional. 2 já sinaliza 
  ▎ erro de invocação no shell; 1 sinaliza erro de dado — a distinção é padrão 
  ▎ Unix e o observador de logs pode agir diferente em cada caso.

  ---
  Ponto 2 — "já consumidos por itens anteriores" com limite zero

  "Já consumidos por itens anteriores no dia" quando o limite nasce zero é
  semanticamente errado — ninguém consumiu nada, é uma exclusão de política, não
   um esgotamento por uso.

  Precisaria de um terceiro caso no template de _texto_passo7 e um registro em
  DECISIONS.md. Proposta:

  if motivo_codigo == "COTA_ESGOTADA":
      limite = politica_eff[categoria]["limite"]
      if limite == Decimal("0.00"):
          return f"cota diária de {categoria} esgotada: categoria não
  reembolsável pela política (limite R$ 0,00)"
      return f"cota diária de {categoria} esgotada: {fmt_valor(limite)} já
  consumidos por itens anteriores no dia"

  Isso exige: atualizar spec.md (tabela de templates seção 4.2), DECISIONS.md
  (D-015 ou D-016, separado de exit codes), e test_integracao_d010 (novo texto
  esperado). É uma mudança de spec — precisa da sua aprovação antes de
  implementar.

  ---
  Ponto 3 — test_integracao_viagem_suspensa_sem_ampliacao fraco para RF-16

  Concordo com o diagnóstico: d-010 = 0,00 prova RF-17 (exclusão por CC), não
  RF-16 (não-ampliação). A única prova de RF-16 no teste é d-003 (transporte
  R$80,00 — seria R$100 com RF-16 ativo).

  O problema é que despesas-exemplo.json não tem um item de alimentação ou
  transporte com valor entre o limite-base e o limite-ampliado (por exemplo,
  R$70 de alimentação seria aprovado sem RF-16 mas cortado com ele se
  limite=60*1.5=90 não capturasse). Adicionar dados ao JSON de exemplo está fora
   do escopo.

  Recomendo opção A: manter o teste, dividir as asserções em comentários
  explícitos que isolam o que cada item prova:

  # d-003: transporte R$100,00 → R$80,00 (limite base); RF-16 daria R$120,00 → 
  prova RF-16 suspenso
  assert _por_id["d-003"].valor_reembolsavel == Decimal("80.00")
  # d-010: hospedagem limite=0,00 (CC-ENG-PLATAFORMA) → 0,00; prova RF-17 
  (exclusão por política)
  assert _por_id["d-010"].valor_reembolsavel == Decimal("0.00")

  E renomear o teste para test_integracao_rf16_suspenso_e_cc_exclusao para
  refletir o que ele realmente prova.

  ---
  Resumo das perguntas para aprovação:

  1. D-015 sobre exit codes: texto ok para commitar?
  2. Template de COTA_ESGOTADA para limite=0: aprovar a mudança de spec + novo
  template? (Se sim, implemento antes do commit de T-028.)
  3. Renomear/comentar o teste de viagem: opção A aprovada?

✻ Churned for 1m 18s

> Aprovado nos três, com dois ajustes:                                          
                                                                                
  1. D-015: aprovado. Acrescente uma frase deixando explícito que a spec        
  original ("código 1") estava incompleta, não errada — não previa a existência 
   de erro de invocação (argparse) separado de erro de dado.                    
                                                                                
  2. Template de limite zero: aprovado no conceito, ajuste no texto. Elimine    
  "esgotada" do ramo de limite=0.00 — não há cota para esgotar, é exclusão      
  categórica. Sugestão: "{categoria} não reembolsável pela política do centro   
  de custo (limite R$ 0,00)". Atualize spec.md (tabela 4.2), registre como      
  parte do D-015 ou nova entrada (sua escolha, mas prefiro consolidar com D-015 
   já que o gatilho é o mesmo momento de revisão), e atualize o assert de       
  test_integracao_d010.                                                         
                                                                                
  3. Renomeação e comentários do teste de viagem: aprovado como proposto, sem   
  alteração.                                                                    
                                                                                
  Implemente os três, rode a suite completa, e me mostre o diff antes do commit 
   final da T-028.                                                              
  ⎿  Read tests\test_cli.py (60 lines)
  ⎿  Read tests\test_rf15_fim_de_semana.py (26 lines)
  ⎿  Read tests\test_rf14_resumo.py (55 lines)
  ⎿  Read tests\test_borda.py (67 lines)
  ⎿  Read tests\test_rf14_serializador.py (110 lines)

● Vou ler os arquivos que precisam ser modificados antes de implementar.

  Read 4 files (ctrl+o to expand)

● Agora vou implementar os três fixes aprovados em paralelo onde possível.

● Update(src\motor.py)
  ⎿  Added 2 lines
      27          return f"limite diário de {categoria}: reembolsado {fmt
          _valor(valor_reembolsavel)} de {fmt_valor(valor_considerado)}"
      28      if motivo_codigo == "COTA_ESGOTADA":
      29          limite = politica_eff[categoria]["limite"]
      30 +        if limite == Decimal("0.00"):                          
      31 +            return f"{categoria} não reembolsável pela política
         + do centro de custo (limite R$ 0,00)"                          
      32          return f"cota diária de {categoria} esgotada: {fmt_valo
          r(limite)} já consumidos por itens anteriores no dia"
      33      return None
      34  

● Update(tests\test_integracao.py)
  ⎿  Added 2 lines, removed 2 lines
       98  
       99  
      100  def test_integracao_d010(_por_id):
      101 -    # d-010: hospedagem R$480,00 → CC-ENG-PLATAFORMA limite=0,
          -00 → COTA_ESGOTADA                                            
      101 +    # d-010: hospedagem R$480,00 → CC-ENG-PLATAFORMA limite=0,
          +00 → COTA_ESGOTADA (template limite=0)                        
      102      item = _por_id["d-010"]
      103      assert item.status == "recusado"
      104      assert item.valor_reembolsavel == Decimal("0.00")
      105      assert item.motivo_codigo == "COTA_ESGOTADA"
      106 -    assert "R$ 0,00" in item.motivo_texto                     
      106 +    assert "não reembolsável pela política do centro de custo"
          + in item.motivo_texto                                         
      107  
      108  
      109  def test_integracao_d011(_por_id):

● Update(tests\test_integracao.py)
  ⎿  Added 5 lines, removed 4 lines
      161              assert por_id[bruta.id].valor_reembolsavel <= limi
           te
      162  
      163  
      164 -def test_integracao_viagem_suspensa_sem_ampliacao(_por_id):   
      165 -    # Critério 17: nenhum item recebe limites ampliados de via
          -gem (RF-16 suspenso)                                          
      166 -    # CC-ENG-PLATAFORMA: transporte limite=80 (seria 120 com R
          -F-16); hospedagem limite=0                                    
      167 -    assert _por_id["d-010"].valor_reembolsavel == Decimal("0.0
          -0")   # não 375,00 nem 250,00                                 
      164 +def test_integracao_rf16_suspenso_e_cc_exclusao(_por_id):     
      165 +    # Critério 17: RF-16 suspenso (sem ampliação) + RF-17 excl
          +usão por CC                                                   
      166 +    # d-003 prova RF-16: transporte limite=80 (seria 120 com R
          +F-16 ativo); motor usa limite padrão                          
      167      assert _por_id["d-003"].valor_reembolsavel == Decimal("80.
           00")  # não 120,00
      168 +    # d-010 prova RF-17 (D-005): hospedagem CC-ENG-PLATAFORMA 
          +limite=0,00 → COTA_ESGOTADA imediata                          
      169 +    assert _por_id["d-010"].valor_reembolsavel == Decimal("0.0
          +0")   # não 375,00 nem 250,00                                 
● Agora atualizo spec.md (tabela de templates) e DECISIONS.md em paralelo.

● Update(specs\001-motor-reembolso\spec.md)
  ⎿  Added 2 lines, removed 1 line
      150  | `SEM_NF` | `"nota fiscal obrigatória para valor acima de R$ 
           100,00 (valor: R$ <valor>)"` | `<valor>` = `valor_considerado`
            com 2 casas decimais, vírgula decimal |
      151  | `LIMITE_DIARIO` | `"limite diário de <categoria>: reembolsad
           o R$ <reembolsavel> de R$ <considerado>"` | valores com 2 casa
           s decimais, vírgula decimal; **exceto `hospedagem`** — ver lin
           ha abaixo |
      152  | `LIMITE_DIARIO` (hospedagem) | `"limite de 1 diária aplicado
            (campo num_diarias ausente do schema)"` | exceção: `num_diari
           as` ausente do schema; `motivo_codigo` permanece `LIMITE_DIARI
           O` (RF-10, AMB-003, D-004) |
      153 -| `COTA_ESGOTADA` | `"cota diária de <categoria> esgotada: R$ 
          -<limite> já consumidos por itens anteriores no dia"` | `<limit
          -e>` = `LIMITE_DIARIO[categoria]` com 2 casas decimais, vírgula
          - decimal |                                                    
      153 +| `COTA_ESGOTADA` | `"cota diária de <categoria> esgotada: R$ 
          +<limite> já consumidos por itens anteriores no dia"` | `<limit
          +e>` = `LIMITE_DIARIO[categoria]` com 2 casas decimais, vírgula
          + decimal; somente quando `limite > 0,00` |                    
      154 +| `COTA_ESGOTADA` (limite = 0,00) | `"<categoria> não reembols
          +ável pela política do centro de custo (limite R$ 0,00)"` | qua
          +ndo o limite efetivo do CC é 0,00 — categoria reconhecida mas 
          +não reembolsável nesse CC (D-005, D-015) |                    
      155  
      156  #### Exemplo de saída (3 itens ilustrativos)
      157  

● Update(specs\001-motor-reembolso\DECISIONS.md)
  ⎿  Added 28 lines
      10  
      11  ---
      12  
      13 +## D-015 — Códigos de saída da CLI e template de COTA_ESGOTADA 
         +quando limite=0,00 · `2026-07-31`                              
      14 +                                                               
      15 +**Gatilho (códigos de saída):** T-028 tornou `--politica` e `--
         +cambio` obrigatórios.                                          
      16 +A spec original (seção 4.1) descrevia apenas "código 1 para arq
         +uivo não encontrado"                                           
      17 +sem distinguir erros de arquivo (dados) de erros de invocação (
         +argumento ausente).                                            
      18 +A spec estava **incompleta, não errada** — não antecipou que o 
         +CLI teria argumentos                                           
      19 +obrigatórios cujo valor sequer seria passado.                  
      20 +                                                               
      21 +**Decisão (códigos de saída):**                                
      22 +- Código 1: erro de dado/arquivo — arquivo não encontrado ou il
         +egível.                                                        
      23 +- Código 2: erro de argumento — emitido por argparse quando arg
         +umento obrigatório                                             
      24 +  está ausente (comportamento padrão, sem código extra).       
      25 +                                                               
      26 +**Gatilho (COTA_ESGOTADA com limite=0,00):** CC-ENG-PLATAFORMA 
         +declara                                                        
      27 +`hospedagem.limite = 0.00`. O template de `COTA_ESGOTADA` (D-00
         +3) usa a expressão                                             
      28 +"esgotada: R$ \<limite\> já consumidos por itens anteriores no 
         +dia", que é semanticamente                                     
      29 +incorreta quando o limite nunca foi positivo — a cota não foi *
         +esgotada* por ninguém,                                         
      30 +a categoria simplesmente não é reembolsável nesse CC.          
      31 +                                                               
      32 +**Decisão (COTA_ESGOTADA com limite=0,00):** Template separado 
         +para `limite = 0,00`:                                          
      33 +`"<categoria> não reembolsável pela política do centro de custo
         + (limite R$ 0,00)"`.                                           
      34 +O ramo padrão ("cota diária de ... esgotada: ...") permanece in
         +alterado para limites > 0.                                     
      35 +                                                               
      36 +**O que mudou na spec:** Tabela de templates (seção 4.2) ganhou
         + linha adicional para                                          
      37 +`COTA_ESGOTADA (limite = 0,00)`.                               
      38 +                                                               
      39 +---                                                            
      40 +                                                               
      41  ## D-014 — Fallbacks de migração em `motor.py`: `_POLITICA_V3` 
          e `gatilho_nf=Decimal("100.00")` · `2026-07-30`
      42  
      43  **Gatilho:** T-025 refatorou `verificar_categoria` para receber
           `politica_eff`

● Rodando a suite completa:

  Ran 1 shell command (ctrl+o to expand)

● 108/108. Agora o diff antes do commit:

  Read 1 file, ran 1 shell command (ctrl+o to expand)

● O diff está limpo — todos os três fixes estão exatamente como aprovados. Posso
   confirmar as mudanças relevantes:

  - DECISIONS.md: D-015 adicionado (exit codes + template limite=0, com
  "incompleta não errada")
  - src/motor.py: branch if limite == Decimal("0.00") em _texto_passo7
  - spec.md: nova linha na tabela de templates para COTA_ESGOTADA (limite = 
  0,00)
  - test_integracao_d010: assert agora verifica "não reembolsável pela política 
  do centro de custo"
  - test_integracao_viagem_suspensa_sem_ampliacao →
  test_integracao_rf16_suspenso_e_cc_exclusao com comentários separados (d-003
  prova RF-16, d-010 prova RF-17)

  Suite: 108/108 verde. Mensagem sugerida para o commit:

  feat(T-028): serializador e CLI com campos v2 e novos argumentos (RF-14,
  AMB-025, D-013)

✻ Sautéed for 7m 44s

> Você parou no meio da implementação dos três ajustes. Terminou? Me mostre o   
  diff completo (spec.md, DECISIONS.md, motor.py, e os testes atualizados) e    
  confirme se a suite completa está passando antes de eu aprovar o commit.      

● Os três fixes já estão implementados e a suite passou 108/108. Deixa eu
  mostrar o diff completo dos arquivos relevantes de forma clara.

  Ran 5 shell commands (ctrl+o to expand)

● Resumo completo dos diffs:

  DECISIONS.md — D-015 inserido no topo (cronologia inversa):
  - Dois gatilhos documentados: exit codes (spec incompleta não errada) +
  COTA_ESGOTADA limite=0
  - Decisão de exit codes: 1 = arquivo/dado, 2 = argparse (comportamento padrão)
  - Decisão de template: ramo separado para limite = 0,00, sem "esgotada"

  spec.md — tabela de templates (seção 4.2):
  - Linha existente de COTA_ESGOTADA ganhou cláusula "somente quando limite > 
  0,00"
  - Nova linha COTA_ESGOTADA (limite = 0,00) com o template aprovado +
  referências D-005 e D-015

  src/motor.py — _texto_passo7:
  - Branch if limite == Decimal("0.00") antes do return padrão de COTA_ESGOTADA
  - (O resto do diff é a remoção do scaffolding D-014 já feita anteriormente)

  tests/test_integracao.py:
  - test_integracao_d010: assert agora verifica "não reembolsável pela política 
  do centro de custo"
  - test_integracao_viagem_suspensa_sem_ampliacao →
  test_integracao_rf16_suspenso_e_cc_exclusao com comentários separados (d-003 =
   RF-16, d-010 = RF-17)

  Suite: 108/108 verde. Pronto para o commit.

✻ Baked for 1m 27s

> Preciso ver o texto literal, não resumo — mesma exigência de sempre. Cole     
  aqui:                                                                         
                                                                                
  1. O trecho exato de motor.py com o novo branch (a função _texto_passo7       
  inteira, para eu ver o if/else completo).                                     
  2. A entrada D-015 completa do DECISIONS.md, do início ao fim.                
  3. As duas linhas da tabela 4.2 do spec.md para COTA_ESGOTADA (a existente    
  com a cláusula nova + a linha nova para limite=0,00).                         
  4. O corpo completo de test_integracao_d010 e                                 
  test_integracao_rf16_suspenso_e_cc_exclusao, como estão agora.                
                                                                                
  Antes de aprovar o commit.                                                    

  Read 4 files (ctrl+o to expand)

● Aqui estão os quatro itens literais:

  ---
  1. _texto_passo7 completa (motor.py, linhas 21–33):

  def _texto_passo7(categoria: str, motivo_codigo: str | None, 
  valor_reembolsavel: Decimal, valor_considerado: Decimal, politica_eff: dict)
  -> str | None:
      if motivo_codigo is None:
          return None
      if motivo_codigo == "LIMITE_DIARIO":
          if categoria == "hospedagem":
              return "limite de 1 diária aplicado (campo num_diarias ausente do 
  schema)"
          return f"limite diário de {categoria}: reembolsado
  {fmt_valor(valor_reembolsavel)} de {fmt_valor(valor_considerado)}"
      if motivo_codigo == "COTA_ESGOTADA":
          limite = politica_eff[categoria]["limite"]
          if limite == Decimal("0.00"):
              return f"{categoria} não reembolsável pela política do centro de
  custo (limite R$ 0,00)"
          return f"cota diária de {categoria} esgotada: {fmt_valor(limite)} já
  consumidos por itens anteriores no dia"
      return None

  ---
  2. D-015 completo (DECISIONS.md, linhas 13–38):

  ## D-015 — Códigos de saída da CLI e template de COTA_ESGOTADA quando
  limite=0,00 · `2026-07-31`

  **Gatilho (códigos de saída):** T-028 tornou `--politica` e `--cambio`
  obrigatórios.
  A spec original (seção 4.1) descrevia apenas "código 1 para arquivo não
  encontrado"
  sem distinguir erros de arquivo (dados) de erros de invocação (argumento
  ausente).
  A spec estava **incompleta, não errada** — não antecipou que o CLI teria
  argumentos
  obrigatórios cujo valor sequer seria passado.

  **Decisão (códigos de saída):**
  - Código 1: erro de dado/arquivo — arquivo não encontrado ou ilegível.
  - Código 2: erro de argumento — emitido por argparse quando argumento
  obrigatório
    está ausente (comportamento padrão, sem código extra).

  **Gatilho (COTA_ESGOTADA com limite=0,00):** CC-ENG-PLATAFORMA declara
  `hospedagem.limite = 0.00`. O template de `COTA_ESGOTADA` (D-003) usa a
  expressão
  "esgotada: R$ \<limite\> já consumidos por itens anteriores no dia", que é
  semanticamente
  incorreta quando o limite nunca foi positivo — a cota não foi *esgotada* por
  ninguém,
  a categoria simplesmente não é reembolsável nesse CC.

  **Decisão (COTA_ESGOTADA com limite=0,00):** Template separado para `limite =
  0,00`:
  `"<categoria> não reembolsável pela política do centro de custo (limite R$
  0,00)"`.
  O ramo padrão ("cota diária de ... esgotada: ...") permanece inalterado para
  limites > 0.

  **O que mudou na spec:** Tabela de templates (seção 4.2) ganhou linha
  adicional para
  `COTA_ESGOTADA (limite = 0,00)`.

  ---
  3. Duas linhas de COTA_ESGOTADA na tabela 4.2 (spec.md, linhas 153–154):

  | `COTA_ESGOTADA` | `"cota diária de <categoria> esgotada: R$ <limite> já
  consumidos por itens anteriores no dia"` | `<limite>` =
  `LIMITE_DIARIO[categoria]` com 2 casas decimais, vírgula decimal; somente
  quando `limite > 0,00` |
  | `COTA_ESGOTADA` (limite = 0,00) | `"<categoria> não reembolsável pela
  política do centro de custo (limite R$ 0,00)"` | quando o limite efetivo do CC
   é 0,00 — categoria reconhecida mas não reembolsável nesse CC (D-005, D-015) |

  ---
  4. Corpos dos dois testes (test_integracao.py):

  def test_integracao_d010(_por_id):
      # d-010: hospedagem R$480,00 → CC-ENG-PLATAFORMA limite=0,00 → 
  COTA_ESGOTADA (template limite=0)
      item = _por_id["d-010"]
      assert item.status == "recusado"
      assert item.valor_reembolsavel == Decimal("0.00")
      assert item.motivo_codigo == "COTA_ESGOTADA"
      assert "não reembolsável pela política do centro de custo" in
  item.motivo_texto


  def test_integracao_rf16_suspenso_e_cc_exclusao(_por_id):
      # Critério 17: RF-16 suspenso (sem ampliação) + RF-17 exclusão por CC
      # d-003 prova RF-16: transporte limite=80 (seria 120 com RF-16 ativo); 
  motor usa limite padrão
      assert _por_id["d-003"].valor_reembolsavel == Decimal("80.00")  # não 
  120,00
      # d-010 prova RF-17 (D-005): hospedagem CC-ENG-PLATAFORMA limite=0,00 → 
  COTA_ESGOTADA imediata
      assert _por_id["d-010"].valor_reembolsavel == Decimal("0.00")   # não 
  375,00 nem 250,00

  ---
  Suite: 108/108 verde. Aguardando sua aprovação para o commit.

✻ Baked for 2m 42s

※ recap: Implementando o motor de reembolso via SDD. T-028 está completo e aprovado — os três ajustes finais foram feitos e 108 testes passam. Próximo passo: commit com a mensagem `feat(T-028): serializador e CLI com campos v2 e novos argumentos (RF-14, AMB-025, D-013)`.

> Aprovado — os quatro trechos conferem exatamente com o que combinamos, e a    
  separação em duas linhas na tabela 4.2 resolveu bem a ambiguidade que eu      
  temia entre disparo do código e escolha do texto. Commita com feat(T-028):    
  serializador e CLI com campos v2 e novos argumentos (RF-14, AMB-025, D-013,   
  D-015).                                                                       

  Committed 1c9091, ran 1 shell command (ctrl+o to expand)

● Commitado. 1c90910 — 14 arquivos, 237 inserções, 86 deleções.

  T-028 encerrada. Próxima é T-029: testes de integração do envelope
  (tests/test_integracao_envelope.py) cobrindo e-001..e-010 e f-001..f-004.
  Antes de começar, lembro: ao final da sessão, rodar /export, salvar em
  docs/sessions/ e commitar.

✻ Cogitated for 34s

> Implemente a T-029: testes de integração contra os dois arquivos do envelope. 
   Antes de escrever qualquer assert, rode o pipeline real contra os dois lotes 
   (despesas-envelope.json com politica_efetiva para CC-COMERCIAL, e            
  despesas-envelope-cc-desconhecido.json para CC-SUPORTE-N2) e me mostre a      
  saída real de cada item — não estime os valores, mesmo sabendo a lógica de    
  cor. Depois disso, escreva os asserts a partir da saída capturada.            

● Vou ler a task e localizar os arquivos antes de rodar o pipeline.

  Searched for 1 pattern, read 5 files, ran 1 shell command (ctrl+o to expand)

● Agora vou rodar o pipeline real contra os dois lotes e capturar a saída item a
   item.

  Ran 2 shell commands (ctrl+o to expand)

● Tenho a saída real dos dois lotes. Vou verificar a seção 9 da spec antes de
  escrever os asserts.

  Ran 1 shell command (ctrl+o to expand)

● Saída capturada, tudo confere com a seção 9 da spec. Vou agora verificar se há
   conftest.py com fixtures relevantes e escrever o arquivo.
  Searched for 1 pattern, read 1 file (ctrl+o to expand)

● Conftest sem fixtures relevantes para estes testes. Escrevo o arquivo a partir
   da saída real capturada.

● Write(tests\test_integracao_envelope.py)
  ⎿  Wrote 163 lines to tests\test_integracao_envelope.py
       1 from decimal import Decimal
       2 from pathlib import Path
       4 from src.motor import processar
       5 from src.parser import carregar_entrada
       6 from src.parser_cambio import carregar_cambio
         atilho, politica_efetiva
       8 
       9 _ENV_PATH = Path(__file__).parent.parent / "exemplos" / "envelop
      10 _CC_PATH  = Path(__file__).parent.parent / "exemplos" / "envelop
         e" / "despesas-envelope-cc-desconhecido.json"
     … +175 lines (ctrl+o to expand)

  Ran 2 shell commands (ctrl+o to expand)

● 14/14 novos testes verdes, suite completa 122/122.

  Aqui estão os resultados reais que guiaram os asserts (resumo para
  conferência):

  id: e-001
  moeda: BRL
  taxa: —
  valor_considerado: 340.00
  status: parcial
  valor_reembolsavel: 300.00
  motivo_codigo: LIMITE_DIARIO
  ────────────────────────────────────────
  id: e-002
  moeda: EUR
  taxa: 5.93
  valor_considerado: 130.46
  status: parcial
  valor_reembolsavel: 90.00
  motivo_codigo: LIMITE_DIARIO
  ────────────────────────────────────────
  id: e-003
  moeda: EUR
  taxa: 5.88
  valor_considerado: 85.26
  status: aprovado
  valor_reembolsavel: 85.26
  motivo_codigo: —
  ────────────────────────────────────────
  id: e-004
  moeda: EUR
  taxa: 5.96 (fallback 17/07)
  valor_considerado: 178.80
  status: parcial
  valor_reembolsavel: 90.00
  motivo_codigo: LIMITE_DIARIO
  ────────────────────────────────────────
  id: e-005
  moeda: USD
  taxa: 5.50
  valor_considerado: 220.00
  status: recusado
  valor_reembolsavel: 0.00
  motivo_codigo: SEM_NF
  ────────────────────────────────────────
  id: e-006
  moeda: GBP
  taxa: null
  valor_considerado: —
  status: recusado
  valor_reembolsavel: 0.00
  motivo_codigo: MOEDA_NAO_SUPORTADA
  ────────────────────────────────────────
  id: e-007
  moeda: BRL
  taxa: —
  valor_considerado: 1200.00
  status: parcial
  valor_reembolsavel: 400.00
  motivo_codigo: LIMITE_DIARIO
  ────────────────────────────────────────
  id: e-008
  moeda: BRL
  taxa: —
  valor_considerado: 95.00
  status: parcial
  valor_reembolsavel: 90.00
  motivo_codigo: LIMITE_DIARIO
  ────────────────────────────────────────
  id: e-009
  moeda: BRL
  taxa: —
  valor_considerado: 120.00
  status: recusado
  valor_reembolsavel: 0.00
  motivo_codigo: CATEGORIA_INVALIDA
  ────────────────────────────────────────
  id: e-010
  moeda: BRL (ausente→BRL)
  taxa: null
  valor_considerado: 88.00
  status: aprovado
  valor_reembolsavel: 88.00
  motivo_codigo: —
  ────────────────────────────────────────
  id: f-001
  moeda: BRL
  taxa: —
  valor_considerado: 58.00
  status: aprovado
  valor_reembolsavel: 58.00
  motivo_codigo: —
  ────────────────────────────────────────
  id: f-002
  moeda: BRL
  taxa: —
  valor_considerado: 310.00
  status: parcial
  valor_reembolsavel: 250.00
  motivo_codigo: LIMITE_DIARIO
  ────────────────────────────────────────
  id: f-003
  moeda: BRL
  taxa: —
  valor_considerado: 190.00
  status: recusado
  valor_reembolsavel: 0.00
  motivo_codigo: CATEGORIA_INVALIDA
  ────────────────────────────────────────
  id: f-004
  moeda: USD
  taxa: 5.48
  valor_considerado: 65.76
  status: aprovado
  valor_reembolsavel: 65.76
  motivo_codigo: —

  Mensagem sugerida para o commit: test(T-029): integração envelope — 
  e-001..e-010, f-001..f-004

✻ Churned for 6m 35s

※ recap: Motor de reembolso SDD, T-029 implementada e 122 testes verdes. Próxima ação: aprovar e commitar com `test(T-029): integração envelope — e-001..e-010, f-001..f-004`.

> Conferido item a item contra a lógica esperada — os 14 resultados batem       
  exatamente com as decisões das AMB-017 a 025. Destaque para e-005 (conversão  
  antes do gatilho de NF, prova da AMB-021) e f-003 (representacao não vaza     
  para CC sem entrada, prova do merge da AMB-017). Commita com test(T-029):     
  integração envelope — e-001..e-010, f-001..f-004.                             

  Committed d7bca0 (ctrl+o to expand)

● Commitado. d7bca09 — 1 arquivo, 163 inserções.

  Lembro de rodar /export, salvar em docs/sessions/ e commitar antes de encerrar
   a sessão.

✻ Churned for 14s