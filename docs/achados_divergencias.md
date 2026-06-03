# Achados — Divergências entre o proposto e o executado

> **Propósito.** Documento consolidado de achados para compor relatório de
> qualificação e/ou artigo posterior. Reúne, em um único lugar, as divergências
> entre (A) o que o artigo de [He et al. (2009)](https://doi.org/10.1109/WI-IAT.2009.108)
> propõe e o que o protótipo efetivamente implementa; e (B) o que o
> planejamento/escopo previu e o que foi de fato executado.
>
> **Data:** 2026-06-02. **Estado:** rascunho para revisão conjunta (achados
> primeiro; a revisão das defasagens nos demais documentos é etapa subsequente).
>
> **Natureza.** Este é um documento de *síntese*, não a fonte primária. Cada
> achado aponta para onde a decisão já está registrada
> (`docs/decision_log.md`, `docs/limitations.md`, `docs/algorithm_notes.md`) e
> para a evidência no código (`arquivo:linha`). Nada aqui substitui aqueles
> registros — o objetivo é dar ao texto do artigo uma matéria-prima única,
> rastreável e com a moldura metodológica correta ("desvio fundamentado",
> "aproximação documentada", "escopo deliberado").
>
> **Como ler.** Cada achado tem: o que foi **proposto**, o que foi
> **executado**, a **evidência**, o **impacto metodológico** e o **status**
> (onde já está documentado e o que ainda precisa ser corrigido nos docs).

---

## 0. Sumário executivo — os quatro achados de maior peso para o artigo

Antes do inventário completo, os pontos que mais afetam a leitura dos
resultados e que merecem destaque no texto:

1. **O baseline mínimo (`d=1`) afere k-anonimato de _grau_, não _estrutural_
   pleno.** Com `d=1` cada Local Structure é um nó isolado e o isomorfismo de
   subgrafo degenera em igualdade de grau. A propriedade *structure-aware* que
   distingue [He et al. (2009)](https://doi.org/10.1109/WI-IAT.2009.108) das
   abordagens de Liu & Terzi só foi exercida no **d-sweep** (tier desejável,
   `d ∈ {5,10}`). → Achado **B1**.
2. **O motor de partição fiel ao artigo (METIS/pymetis) não rodou no baseline
   formal.** A validação de k-anonimato de `d=1` (marco 29/05, k-sweep) usou o
   **fallback Kernighan-Lin**, que não é o algoritmo do artigo e não garante
   balanceamento. Para `d=1` isso é inócuo (partições triviais), mas precisa ser
   declarado. O d-sweep posterior rodou com pymetis. → Achado **A1**.
3. **A premissa de Local Structure conexa do artigo não é garantida.** As
   partições do pymetis não são forçadas a ser conexas (~56% desconexas em
   `d=5`; `d=2` degenerate na ego-rede 3437). Documentado como aproximação, não
   corrigido. → Achado **A4**.
4. **O verificador de k-anonimato é uma adição do projeto, não do artigo** — e é
   deliberadamente conservador. He et al. tratam o k-anonimato como garantido
   por construção; o projeto acrescentou um auditor empírico independente, mais
   forte que a garantia teórica em alguns aspectos e mais conservador em outro
   (conta candidatos só dentro do grupo). → Achado **A5**.

---

## 1. Matriz de divergências

Legenda de status: ✅ já documentado e fiel · ⚠️ documentado mas disperso/parcial ·
🔧 defasagem a corrigir nos docs (etapa 2).

### Grupo A — Artigo (He et al. 2009) × implementação

| ID | Ponto | Proposto | Executado | Status |
|----|-------|----------|-----------|--------|
| A1 | Motor de partição | multilevel k-way (Karypis & Kumar / METIS) | pymetis primário, mas baseline `d=1` rodou no **fallback KL** (sem balanceamento p/ ck>2); d-sweep rodou pymetis | ⚠️ |
| A2 | FSM | mineração de subgrafos frequentes (Wörlein 2005 / gSpan) | FSM simplificado, `s_max=4` **hardcoded** + hash Weisfeiler-Lehman | ✅ |
| A3 | Premissa \|Vᵢ\|=d estrita | LSs de um grupo têm o mesmo nº de nós | KL não garante → Opção A restringe grupos por tamanho (↑ grupos incompletos) | ✅ |
| A4 | LS = subgrafo conexo | conectividade implícita (Def. 1) | partições **não forçadas conexas** (~56% desconexas em d=5) | ✅ |
| A5 | k-anonimato por construção | sem verificador externo | verificador empírico independente **adicionado**; conservador (escopo intra-grupo) | ✅ |
| A6 | Grupo final incompleto | tratamento não especificado | mantido sem modificação; nós contados como violadores | ✅ |
| A7 | Matching Fase 1 | "based on nodes degree", sem desempate | desempate **lexicográfico** adicionado (determinismo) | ✅ |
| A8 | Reconexão `k(k−1)` | "k(k−1) arestas por inter-aresta" | confirmado só p/ posições canônicas distintas; casos especiais distintos | ✅ |
| A9 | Complexidades | só partição `O(\|E\|)` é declarada | demais são interpretativas; reconexão confirmada empiricamente | ✅ |

### Grupo B — Plano/escopo × execução

| ID | Ponto | Planejado | Executado | Status |
|----|-------|-----------|-----------|--------|
| B1 | `d=1` no baseline | Def. 2 sobre subgrafo de tamanho `d` | baseline mínimo = **d=1** → isomorfismo ≡ igualdade de grau | ⚠️ |
| B2 | Datasets | Facebook (principal) + Email-Enron (secundário) | **só ego-rede 3437**; Enron não executado | ⚠️ |
| B3 | Ataque por entropia | tier aspiracional | **não implementado** | ✅ |
| B4 | Nettleton & Salas (2016) | tier aspiracional | **placeholder apenas** | ✅ |
| B5 | YAML público | expor d, σ, s_max, partition_backend, isomorphism_mode | `config_example.yml` agora expõe d, σ, s_max, isomorphism_mode (#106); só `partition_backend` resta | ✅ |
| B6 | Variante de isomorfização | add_only vs add_or_delete como parâmetro | ambas implementadas+testadas, mas `add_or_delete` **hardcoded**; chave YAML nunca lida | 🔧 |
| B7 | Diagnóstico de `reid_sub=0` | — | log do d-sweep gerado **sem** contagem de timeouts; campos adicionados depois | ⚠️ |
| B8 | Critério do marco | verificação binária | rebaixado p/ `satisfied_fraction≥0.9` + `deficit_fully_structural` | ✅ |

---

## 2. Achados detalhados — Grupo A (artigo × implementação)

### A1 — Motor de partição: METIS proposto, KL no baseline formal

- **Proposto.** He et al. (p. 650) citam explicitamente multilevel k-way de
  Karypis & Kumar (ref. [14]) como o algoritmo de partição, com complexidade
  declarada `O(|E|)`.
- **Executado.** O protótipo adota pymetis como motor primário e
  `networkx.kernighan_lin_bisection` recursivo como fallback (D-04). O `pip`
  padrão (`requirements.txt`) **não instala** pymetis de forma confiável, então
  o fallback KL é facilmente acionado emitindo apenas um `UserWarning`. À época
  do marco 29/05 e da varredura de `k` (auditoria #74, 30/05), pymetis estava
  ausente local e na CI → **o baseline `d=1` rodou em KL**. O d-sweep posterior
  (#88) rodou **pymetis em 48/48** (gravado em `partition_backend` no JSONL).
- **Evidência.** `_partition_neighborhoods(... backend="auto")`
  (`src/anonymization/he2009.py:294`, `run.py:255`); flag
  `anonymization.allow_kl_fallback` (`config_example.yml:77`); D-04 em
  `docs/decision_log.md`.
- **Impacto.** O KL não garante balanceamento de tamanho p/ `ck>2`, divergindo
  da premissa do artigo. **Para `d=1` o impacto é nulo** (partições triviais de
  1 nó), de modo que a validação formal de k-anonimato permanece válida — mas o
  texto deve declarar que o número-título ("k-anonimato atingido") foi produzido
  pelo motor *não fiel*, e que a fidelidade ao artigo (pymetis) só foi exercida
  no d-sweep.
- **Status.** ⚠️ Documentado (D-04, limitations §2.2), mas a frase "qual backend
  rodou em qual experimento" está implícita. Sugestão p/ etapa 2: tornar
  explícito no `results_baseline.md` que o baseline d=1 rodou em KL.

### A2 — FSM simplificado com `s_max=4` fixo

- **Proposto.** FSM genérico (Wörlein et al. 2005, família gSpan), sem
  implementação especificada.
- **Executado.** FSM simplificado por enumeração de subgrafos conexos induzidos
  até `s_max`, com forma canônica via hash Weisfeiler-Lehman (evita
  `is_isomorphic` par a par na fase de FSM). `s_max=4` é **hardcoded**: nem
  `anonymize()` nem o runner passam `fsm_max_size` → default 4. Para `d>4`, o
  FSM nunca enxerga o padrão completo da LS, só subgrafos de até 4 nós.
- **Evidência.** `_group_isomorphic(... sigma=sigma)` sem `fsm_max_size`
  (`run.py:273`, `he2009.py:299`); D-01 + nota G2 em `docs/decision_log.md`.
- **Impacto.** Aproximação do procedimento original. Para `d=1` o impacto é nulo
  (LS de 1 nó não exige FSM substantivo). Para `d>4`, justificado empiricamente
  como inócuo no caso testado (`cycle_graph(20)`, d=5 → mesmo agrupamento com
  `s_max∈{4,5}`), pois a corretude do isomorfismo é garantida por
  `_modify_structure`, não pelo FSM.
- **Atualização (B5 / #104).** O `s_max=4` **deixou de ser hardcoded**:
  `anonymize()` e `_group_isomorphic()` passaram a aceitar `fsm_max_size`
  (default 4) e o runner lê `anonymization.s_max` (alias `fsm_max_size`) do
  YAML, propaga-o e grava o valor efetivo no JSONL. A descrição "Executado"
  acima reflete o estado **anterior** a #104; o achado permanece fiel como
  registro histórico. Ver B5.
- **Status.** ✅ Bem documentado (D-01, nota G2, limitations §2.1).

### A3 — Premissa `|Vᵢ| = d` estrita (Opção A)

- **Proposto.** A Fase 1 do artigo pressupõe que todas as LSs de um grupo têm o
  mesmo número de nós (p. 651: *"Since each of local structures in the same
  group has the same number of nodes, this process will terminate quickly"*).
- **Executado.** Com KL, as partições podem ter tamanhos distintos. Opção A
  (D-07): grupos formam-se **apenas entre LSs de mesmo `|Vᵢ|`**; as demais caem
  em grupo incompleto (D-06). Preserva a premissa formal para os grupos que se
  formam, ao custo de mais violadores.
- **Evidência.** D-07 em `docs/decision_log.md`; `algorithm_notes.md` §3.1, §4.1.
- **Impacto.** Desvio do caminho ideal do artigo no fallback; mitigado pela
  Opção A. Para `d=1` não gera violadores além do `n mod k` esperado.
- **Status.** ✅ Documentado.

### A4 — Local Structure conexa não é garantida

- **Proposto.** A Def. 1 do artigo define LS como subgrafo induzido **conexo**.
- **Executado.** `_partition_neighborhoods` devolve subgrafos induzidos das
  partições do pymetis **sem forçar conectividade**. Medição na ego-rede 3437
  (D-08): `d=2` degenerate (≈199/267 partições vazias, nós concentrados em
  grupos de 7–8); `d=5` razoável em tamanho mas **~56% das LSs desconexas**.
  Decisão (Opção B): documentar como aproximação, não corrigir no protótipo.
- **Evidência.** D-08 em `docs/decision_log.md`; teste automatizado
  `test_local_structures_connected_d_gt_1`
  (`tests/anonymization/test_he2009_partition.py`); `algorithm_notes.md` §6.
- **Impacto.** Desvio da premissa implícita do artigo. LSs desconexas são
  tratadas como grafos desconexos normais pelo resto do pipeline — coerente com
  o código, mas afasta-se da noção de "vizinhança local coerente". Forçar
  conectividade é candidato a tier desejável futuro.
- **Status.** ✅ Documentado (D-08, §6, teste).

### A5 — Verificador empírico: adição do projeto, conservador por desenho

- **Proposto.** He et al. tratam k-anonimato como **garantido por construção**;
  não propõem verificador externo.
- **Executado.** O projeto **adicionou** `validate_k_anonymity` como auditor
  independente (não reutiliza código do anonimizador), exigido pela metodologia
  (regra `.claude/rules/anonymization.md`). Ele é **mais forte** que a garantia
  teórica em um aspecto (expõe violações de D-06/D-07 que a construção mascara) e
  **mais conservador** em outro: conta candidatos isomorfos só **dentro do grupo
  de anonimização**, podendo superestimar violadores (a Def. 2 não restringe ao
  grupo).
- **Evidência.** D-05 e DL-01 em `docs/decision_log.md`; limitations §2.4;
  `algorithm_notes.md` §4.2–4.3; `src/anonymization/validation.py`.
- **Impacto.** Diferença de método em relação ao artigo, favorável à auditoria
  (nunca certifica violador como protegido). O conservadorismo nunca produziu
  falso positivo de proteção no baseline (todos os violadores atribuíveis a
  D-06).
- **Status.** ✅ Documentado.

### A6 — Grupo final incompleto

- **Proposto.** O Algorithm 1 não especifica o tratamento das LSs que sobram
  após o agrupamento principal.
- **Executado.** Grupos com `<k` membros são mantidos sem modificação; seus nós
  são reportados como violadores (`incomplete_group`). Sem fusão artificial nem
  descarte (D-06).
- **Evidência.** D-06 em `docs/decision_log.md`; `algorithm_notes.md` §4.1–4.2.
- **Impacto.** Principal causa legítima de `satisfied_fraction < 1.0`. Limitado
  a `n mod k` nós para `d=1`.
- **Status.** ✅ Documentado.

### A7 — Desempate lexicográfico no matching da Fase 1

- **Proposto.** Matching "based on nodes degree" (p. 651), sem critério de
  desempate.
- **Executado.** Desempate por índice de nó lexicográfico crescente (D-03),
  para determinismo bit-a-bit.
- **Evidência.** D-03 em `docs/decision_log.md`; `algorithm_notes.md` §3.3.
- **Impacto.** Afeta a identidade de `G'` (quais arestas mudam), não a
  propriedade formal. Reportar como parâmetro de reprodutibilidade, não como
  escolha ótima.
- **Status.** ✅ Documentado.

### A8 — Fórmula `k(k−1)` da reconexão depende da posição canônica

- **Proposto.** *"In general, for each original inter-edge, a total of k(k−1)
  edges have to be added."* (p. 652).
- **Executado.** Confirmado empiricamente (`TestReconnectKTimesKMinusOne`,
  k∈{2,3}) **apenas para extremos em posições canônicas distintas** (caso geral).
  Casos especiais da construção não-direcionada: mesma posição → clique de
  `C(k,2)=k(k−1)/2`; LSs de 1 nó → apenas a inter-aresta original (1 aresta). O
  exemplo literal esboçado na issue #80 estava **incorreto** (degenerate).
- **Evidência.** `algorithm_notes.md` §3.2.2; D-08 nota G3 em
  `docs/decision_log.md`; docstring de `_reconnect_inter_edges`.
- **Impacto.** Esclarecimento (não correção de bug): a estimativa
  `O(|E_inter|·k²)` vale no caso geral. Achado interessante para o artigo por
  ser uma precisão sobre uma fórmula citada sem ressalva no original.
- **Status.** ✅ Documentado.

### A9 — Complexidades: só a da partição é declarada no artigo

- **Proposto/Executado.** Apenas a partição via METIS tem complexidade declarada
  (`O(|E|)`). FSM, agrupamento, isomorfização e reconexão têm complexidades
  **interpretativas** derivadas da descrição. A da reconexão foi confirmada
  empiricamente (A8).
- **Evidência.** `algorithm_notes.md` §2.2 (tabela com a marca "Interpretativa").
- **Impacto.** Relevante para a seção de complexidade do relatório: distinguir o
  que é afirmação do artigo do que é inferência do protótipo.
- **Status.** ✅ Documentado.

---

## 3. Achados detalhados — Grupo B (plano × execução)

### B1 — Baseline executado com `d=1`: k-anonimato de grau, não estrutural pleno

- **Planejado.** A Def. 2 de He et al. é sobre isomorfismo de subgrafo local de
  tamanho variável `d`; `d=10` foi o default conceitual (D-02).
- **Executado.** Todo o escopo **mínimo** (marco 29/05, k-sweep, baseline #23)
  usou **`d=1`** — convencionado após a seleção da ego-rede (issue #40). Com
  `d=1`, a LS de cada nó é um subgrafo de um único nó e o isomorfismo reduz-se a
  **igualdade de grau**. A propriedade *structure-aware* só foi exercida no
  d-sweep (`d∈{5,10}`, tier desejável).
- **Evidência.** D-02 em `docs/decision_log.md`; `algorithm_notes.md` §5.3, §6.5,
  §9.1; limitations §1.3; configs `he2009_facebook_*` com `d=1`.
- **Impacto.** É o achado de maior consequência interpretativa: os resultados do
  baseline rotulados como "He et al. structure-aware" são, no regime `d=1`,
  equivalentes a k-anonimato de grau. O contraste `d=1` vs. `d∈{5,10}` do
  d-sweep é a evidência empírica de que o módulo afere privacidade estrutural — e
  deve ser apresentado como tal, não como detalhe.
- **Status.** ⚠️ Documentado, mas espalhado entre D-02, §6.5, §9.4 e
  limitations §1.3. Vale uma frase única e direta no texto do artigo.

### B2 — Um único dataset (ego-rede 3437); Enron não executado

- **Planejado.** Facebook Ego-Nets como principal e Email-Enron como secundário
  contingente (escopo, §3); `multiple_egonets` previsto em config.
- **Executado.** Apenas a **ego-rede 3437** (n_lcc=532). Nenhuma execução com
  Enron nem com múltiplas ego-redes do Facebook.
- **Evidência.** `scope.md` §3; limitations §1.1; `config_example.yml:46`
  (`egonet_ids` previsto, não usado).
- **Impacto.** Ameaça à validade externa: resultados (incl. a resolução parcial
  de `d>1`) restritos a uma rede. Generalização aberta.
- **Status.** ⚠️ Documentado como limitação de escopo (§1.1, ameaça à validade
  externa). Convém reafirmar que nem o secundário contingente (Enron) nem
  `multiple_egonets` chegaram a rodar.

### B3 — Ataque por entropia não implementado

- **Planejado.** Tier aspiracional/desejável (escopo §3 `[A]`).
- **Executado.** Não implementado. Apenas grau e subgrafo.
- **Evidência.** `scope.md` §3; limitations §1.4; ausência em `src/attacks/`.
- **Impacto.** A taxa de reidentificação medida é cota inferior da
  vulnerabilidade real (adversários mais ricos poderiam superá-la).
- **Status.** ✅ Documentado.

### B4 — Nettleton & Salas (2016): apenas placeholder

- **Planejado.** Tier aspiracional, segundo ponto de comparação na curva.
- **Executado.** Placeholder; não implementado. Sem comparação entre
  anonimizadores.
- **Evidência.** `scope.md` §3/§4; limitations §1.2; `src/anonymization/`
  (placeholder).
- **Impacto.** Afirmações comparativas ("He et al. preserva melhor que X") não
  são sustentadas pelos dados.
- **Status.** ✅ Documentado.

### B5 — Parâmetros não expostos no YAML público

- **Planejado.** `algorithm_notes.md` §5.1 mapeia d, σ, `s_max`,
  `partition_backend` e `isomorphism_mode` como chaves de configuração.
- **Executado.** `config_example.yml` expõe apenas `k_values`,
  `validate_k_anonymity` e `allow_kl_fallback`. Os YAMLs experimentais (d-sweep)
  acrescentam `d` e `sigma`, mas **`s_max`/`fsm_max_size` e `isomorphism_mode`
  não aparecem em nenhum YAML** — são fixos no código (ver A2, B6).
- **Evidência.** `config_example.yml` (linhas 63–95);
  `experiments/configs/he2009_facebook_dsweep.yml` (linhas 75–80);
  `algorithm_notes.md` §5.2 (reconhece a divergência, atribuída a #26-B).
- **Impacto.** A documentação conceitual está à frente da interface pública.
  `s_max` e `isomorphism_mode` documentados como parâmetros "configuráveis" são,
  na prática, constantes — afirmar configurabilidade é impreciso.
- **Atualização (#104, parte `s_max`).** Em vez de marcar `s_max` como "fixo
  no código", optou-se por **expor a chave de verdade**: `anonymize()`/
  `_group_isomorphic()` recebem `fsm_max_size` e o runner lê
  `anonymization.s_max` (alias `fsm_max_size`) do YAML, propaga-o e grava o
  valor efetivo no JSONL. `algorithm_notes.md` §5.1/§5.2 atualizadas. Restam,
  sob B5: expor `d`/`sigma`/`s_max` no `config_example.yml` (S8-3 / #106) e
  `isomorphism_mode` (B6 / S8-2 / #105).
- **Atualização (#112, S8-2b).** A propagação de `s_max`/`fsm_max_size`
  (config→runner→`_group_isomorphic`, e `anonymize()`→`_group_isomorphic`)
  ganhou cobertura de teste dedicada — ver detalhamento sob B6.
- **Atualização (#106, S8-3).** O `config_example.yml` de referência passou a
  **expor** `d`, `sigma`, `s_max` (alias `fsm_max_size`) e `isomorphism_mode`,
  todas com comentários e defaults corretos e **todas efetivamente lidas** pelo
  runner. A chave `k` foi corrigida no exemplo (antes `k_values`, que o runner
  não lê → configurabilidade fantasma) para refletir a interface real. Decisão
  registrada em `docs/decision_log.md` (DL-03); `algorithm_notes.md` §5.1–5.3
  atualizadas. Resta apenas `partition_backend` não exposto como chave YAML.
- **Status.** 🔧→✅ Defasagem resolvida: `s_max` (#104) e `isomorphism_mode`
  (#105) lidas do YAML e cobertas por testes (#112); exposição no
  `config_example.yml` estabilizada por #106 (DL-03). Resíduo único:
  `partition_backend` ainda não é chave YAML (só `allow_kl_fallback`).

### B6 — Variante de isomorfização: implementada, mas hardcoded e não exposta

- **Planejado.** A escolha add_only vs. add_or_delete é "parâmetro de execução"
  (`algorithm_notes.md` §3.1/§3.4/§5.1), a ser exposto como
  `anonymization.isomorphism_mode`.
- **Executado.** As **duas variantes existem e são testadas** em
  `_modify_structure(add_only=...)`, mas tanto o `anonymize()` público quanto o
  pipeline inline do runner chamam com **`add_only=False` (add_or_delete)
  hardcoded**. A chave YAML `isomorphism_mode` **nunca é lida** em lugar nenhum.
- **Evidência.** `src/anonymization/he2009.py:305` e `:503` (`_modify_structure`,
  ambas as variantes); `experiments/run.py:289` (`add_only=False`);
  `tests/anonymization/test_he2009_modify.py` (testa as duas);
  ausência de leitura de `isomorphism_mode` (grep).
- **Impacto.** Misto: a capacidade existe (não é dívida de implementação do
  algoritmo), mas operacionalmente o experimento só exerce `add_or_delete`. O
  texto deve dizer "variante add_or_delete (a de menor perturbação); a
  alternativa add_only está implementada e testada, mas não foi varrida".
- **Atualização (#105).** Corrigida na raiz, não só documentalmente:
  `anonymize()` ganhou o parâmetro `isomorphism_mode: str = "add_or_delete"`
  (valida o valor; converte para `add_only = (isomorphism_mode == "add_only")`
  e repassa a `_modify_structure`). O runner (`experiments/run.py`) **lê** a
  chave `anonymization.isomorphism_mode`, valida-a antes do laço de execução,
  propaga-a a `anonymize()` e ao caminho inline (`_modify_structure(add_only=...)`)
  e grava o valor efetivo em cada entrada JSONL e no `summary.json`. Default
  `add_or_delete` preserva o comportamento histórico. Docstring de `anonymize()`,
  `algorithm_notes.md` §3.2.1/§3.4/§5.1/§5.2/§5.3 atualizadas. Resta, sob B5:
  expor a chave no `config_example.yml` (S8-3 / #106).
- **Atualização (#112, S8-2b).** A propagação de `isomorphism_mode` (e de
  `s_max`/`fsm_max_size`, ver B5) ganhou cobertura de teste dedicada:
  `tests/anonymization/test_he2009_modify.py` verifica o caminho
  `anonymize() → _modify_structure(add_only=...)` (via spy), o default
  `add_or_delete`, o efeito "nenhuma aresta removida" sob `add_only` e o erro
  para valor inválido; `tests/experiments/test_run_config_propagation.py`
  verifica o caminho config→runner (chave YAML gravada no JSONL/`summary.json`,
  default na ausência da chave, valor efetivo chegando a `_modify_structure`, e
  regressão do baseline `d=1`).
- **Status.** 🔧→✅ Defasagem resolvida na raiz por #105 (chave YAML lida e
  propagada, não mais constante de código) e coberta por testes em #112.
  Pendência residual: estabilizar a chave no `config_example.yml` (#106).
  Migração formal do status na tabela-resumo deixada para S8-8 (#111).

### B7 — Log do d-sweep sem contagem de timeouts (campos retroativos)

- **Planejado.** O comentário do YAML do d-sweep afirma "timeouts não são crash
  — são registrados e o nó conta como não reidentificado".
- **Executado.** No código vigente quando o d-sweep rodou, um `TimeoutError` por
  nó propagava-se até gravar `verdict=ERROR` no run inteiro (contradizendo o
  comentário). O log dos 48 runs **não registra contagem de timeouts**. A
  inspeção (issue #93, Passo 1) mostrou ausência de `verdict=ERROR` → nenhum VF2
  atingiu 120 s → os `reid_sub=0` são genuínos (privacidade real/degeneração),
  **não** timeouts mascarados (H3 descartada). Os campos
  `subgraph_timeout_count` e `subgraph_candidate_counts` foram adicionados
  **depois** (DL-02), e só aparecerão em execuções futuras.
- **Evidência.** DL-02 e D-08 (nota de encerramento) em `docs/decision_log.md`;
  `results_dsweep.md` §5.5, §5.7; `experiments/run.py` (laço do subgrafo).
- **Impacto.** Para o log atual, a ambiguidade foi resolvida por inspeção
  (conclusiva), não por reexecução. Os zeros do d-sweep são confiáveis, mas a
  rastreabilidade só fica completa em execuções futuras (instrumentadas).
- **Status.** ⚠️ Documentado (DL-02, results_dsweep §5.5/§5.7).

### B8 — Critério do marco refinado (binário → fração + causa)

- **Planejado.** Verificação binária de k-anonimato por `k` (`valid=True/False`).
- **Executado.** Refinado em DL-01: `satisfied_fraction ≥ 0.9` como piso de
  sanidade **e** déficit 100% atribuível a causa estrutural
  (`deficit_fully_structural=True`) como régua lógica. Distingue déficit
  estrutural aceitável (D-06) de falha de implementação.
- **Evidência.** DL-01 em `docs/decision_log.md`; `algorithm_notes.md` §4.2.2,
  §8.
- **Impacto.** Desvio fundamentado do plano operacional; torna a curva
  privacidade-vs-utilidade defensável. Bem motivado.
- **Status.** ✅ Documentado.

---

## 4. Pendências de revisão documental (insumo para a etapa 2)

Pontos onde a documentação existente ainda descreve o *proposto* como se fosse o
*executado* e deveriam ser ajustados depois de revisarmos estes achados:

1. ~~**`algorithm_notes.md` §5.1 (B5/B6).** Marcar `s_max`/`fsm_max_size` e
   `isomorphism_mode` como fixos no código.~~ **Resolvido de forma oposta:**
   em vez de marcar como "fixos no código", as duas chaves passaram a ser
   **lidas de verdade do YAML** — `s_max` por #104 e `isomorphism_mode` por
   #105. §5.1 agora descreve ambas como chaves YAML ativas.
2. ~~**`he2009.py` docstring de `anonymize()` (B6).**~~ **Resolvido (#105):**
   `anonymize()` recebe `isomorphism_mode` como parâmetro real e a docstring
   descreve a chave YAML como a via de configuração efetiva (não mais
   constante de código).
3. **`results_baseline.md` (A1).** Tornar explícito que o baseline `d=1` rodou no
   **fallback KL** (não pymetis), e que isso é inócuo para `d=1`.
4. ~~**`config_example.yml` (B5).** Decidir se vale expor `d`/`sigma` no exemplo
   de referência (hoje só nos YAMLs experimentais) para alinhar exemplo e
   prática — ou documentar por que o exemplo permanece mínimo.~~ **Resolvido
   (#106 / DL-03):** o exemplo passou a expor `d`, `sigma`, `s_max` e
   `isomorphism_mode` (todas lidas pelo runner) e a chave `k` foi corrigida
   (`k_values`→`k`). Resíduo: `partition_backend` segue não exposto.
5. **Frase-síntese de B1.** Inserir, no README e/ou `results_baseline.md`, uma
   afirmação direta de que o baseline `d=1` afere k-anonimato de grau e que o
   d-sweep é o que exercita a propriedade estrutural.

> Esta seção é deliberadamente **não-acionada** neste documento: corrigir os
> docs acima é a etapa seguinte, após revisão conjunta destes achados.

---

## 5. Referências cruzadas

- `docs/decision_log.md` — D-01 a D-10, DL-01, DL-02 (fonte primária das decisões).
- `docs/limitations.md` — classificação formal (escopo × técnica) e ameaças à validade.
- `docs/algorithm_notes.md` — §2 (algoritmo), §3 (modificações), §4 (verificador),
  §5 (parâmetros), §6 (casos especiais), §9 (resultados k-sweep e d-sweep).
- `docs/results_baseline.md` — resultados `d=1` (baseline #23).
- `docs/results_dsweep.md` — resultados `d∈{1,2,5,10}` (d-sweep #88) e ameaças à validade §5.7.
- `docs/scope.md` — fronteira de escopo e não-escopo; tiers [M]/[D]/[A].

---

## 6. Referências bibliográficas

[1] [HE, X. et al.](https://doi.org/10.1109/WI-IAT.2009.108) Preserving privacy in social networks: A structure-aware approach. In: *WI-IAT 2009*. IEEE, 2009. p. 647–654.

[2] [KARYPIS, G.; KUMAR, V.](https://doi.org/10.1137/S1064827595287997) A fast and high quality multilevel scheme for partitioning irregular graphs. *SIAM J. Sci. Comput.*, v. 20, n. 1, p. 359–392, 1998.

[3] [LIU, K.; TERZI, E.](https://doi.org/10.1145/1376616.1376629) Towards identity anonymization on graphs. In: *SIGMOD 2008*. ACM, 2008. p. 93–106.

[4] [NETTLETON, D. F.; SALAS, J.](https://doi.org/10.1016/j.eswa.2016.02.004) A data driven anonymization system for information rich online social network graphs. *Expert Systems with Applications*, v. 55, p. 87–105, 2016.

[5] [WÖRLEIN, M. et al.](https://doi.org/10.1007/11564126_32) A quantitative comparison of the subgraph miners MoFa, gSpan, FFSM, and Gaston. In: *PKDD 2005*. Springer, 2005. p. 392–403.

[6] [ZHOU, B.; PEI, J.](https://doi.org/10.1109/ICDE.2008.4497459) Preserving privacy in social networks against neighborhood attacks. In: *ICDE 2008*. IEEE, 2008. p. 506–515.
