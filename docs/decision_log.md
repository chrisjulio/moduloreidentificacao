# Registro de Decisões — Desvios e Refinamentos Documentados

> Este arquivo registra decisões que representam **desvios fundamentados** em relação
> ao planejamento original ou **refinamentos de critérios** que não constavam
> explicitamente nos documentos de referência. Desvios não documentados não são
> permitidos (Seção 11 do plano operacional).
>
> As entradas DL-xx registram desvios ou refinamentos de alto impacto sobre o
> planejamento (cronograma, critérios de passagem, escopo). As entradas D-xx
> registram decisões de implementação — lacunas do artigo ou escolhas técnicas
> que não constavam no planejamento, mas que ficaram distribuídas em
> `docs/algorithm_notes.md` e nos PRs. Ambos os conjuntos são consolidados
> aqui para rastreabilidade única.

---

## Índice de decisões

| ID | Data | Tipo | Título resumido |
|---|---|---|---|
| [DL-01](#dl-01) | 2026-05-21 | Desvio de planejamento | Refinamento do critério de passagem do marco #16 |
| [DL-02](#dl-02) | 2026-06-02 | Extensão de schema | Campos de diagnóstico do ataque por subgrafo (timeouts + candidatos) |
| [DL-03](#dl-03) | 2026-06-02 | Interface pública | `config_example.yml` expõe `d`/`sigma`/`s_max`/`isomorphism_mode` (chaves lidas) + correção `k_values`→`k` |
| [D-01](#d-01) | 2026-05-17 *(nota G2: 2026-05-28)* | Implementação | FSM simplificado com `s_max` configurável; nota: comportamento quando d > s_max |
| [D-02](#d-02) | 2026-05-17 | Implementação | `d = 10` como default; variável de configuração YAML |
| [D-03](#d-03) | 2026-05-17 | Implementação | Matching Fase 1: grau primário + desempate lexicográfico |
| [D-04](#d-04) | 2026-05-17 *(rev. 2026-05-20)* | Implementação | Motor de particionamento: pymetis primário, KL fallback |
| [D-05](#d-05) | 2026-05-17 | Implementação | Verificador empírico estrito de k-anonimato |
| [D-06](#d-06) | 2026-05-17 | Implementação | Política para grupos incompletos residuais |
| [D-07](#d-07) | 2026-05-20 | Implementação | Normalização de tamanho de LSs — Opção A adotada |
| [D-08](#d-08) | 2026-05-28 | Implementação | Política de conectividade de LSs — documentar como aproximação |
| [D-09](#d-09) | 2026-05-28 | Implementação | Pré-filtro VF2: documentar como limitação do protótipo |
| [D-10](#d-10) | 2026-05-28 | Implementação | Combo degenerado d=10, k=20: executar e anotar como degenerado no YAML |
| [D-11](#d-11) | 2026-06-03 | Implementação | Email-Enron direcionado → não-direcionado: simetrização por OR |

---

## DL-01 — Refinamento do critério de passagem do marco #16 (k-anonimato estrutural)

**Data:** 2026-05-21  
**Issue relacionada:** #16  
**Decisão sobre:** Seção 4.3 do planejamento ("verificação binária") vs. critério D-06 inserido em #16

### Contexto

O planejamento original (Seção 4.3) tratava a verificação de k-anonimato estrutural
como **binária**: para cada valor de `k`, ou a instância era integralmente coberta
(`valid=True`), ou os resultados eram inválidos. O critério de "sucesso parcial
aceitável" com `satisfied_fraction >= 0.9` foi introduzido na definição de pronto
da issue #16 (campo D-06) sem que o documento de decisões registrasse formalmente
por que essa tolerância era metodologicamente defensável.

A Seção 11 do plano operacional é explícita: *"desvios fundamentados são esperados;
desvios não documentados, não."* Este documento resolve a pendência.

### Problema com a redação original de D-06

O enunciado `satisfied_fraction >= 0.9` como critério de "sucesso parcial aceitável"
cria uma ambiguidade metodológica grave:

- Um valor de `0.9` fixo sugere que até 10% de nós descobertos é tolerável por
  definição, independentemente de quem são esses nós e por quê não foram cobertos.
- 30% de nós descobertos sendo todos folhas de grau 1 em componentes estruturalmente
  impossibilitados de satisfazer k-anonimato para o `k` dado é **algoritmo correto**.
- 5% de nós descobertos incluindo nós de alto grau em regiões densas é **bug ou
  implementação incompleta**, independentemente de o `satisfied_fraction` ser 0,95.
- Sem distinguir as duas situações, a curva privacidade × utilidade — a entrega
  central do módulo — torna-se indefensável.

### Decisão adotada (Opção A)

**Critério substantivo (lógico):**
> 100% do déficit de cobertura de k-anonimato é atribuível a causas estruturais
> identificadas pelo verificador (grupos incompletos, componentes com vizinhança
> isomórfica insuficiente para o `k` configurado — conforme D-06).

**Piso de sanidade operacional:**
> `satisfied_fraction >= 0.9` é rebaixado a **limite operacional mínimo**,
> não a régua lógica do marco. Instâncias com `satisfied_fraction < 0.9` não
> são aceitas como válidas para uso em métricas derivadas, independentemente
> da causa do déficit.

**Condição de passagem completa:**
> Entre `0.9` e `1.0`, a aceitação depende de o déficit ser integralmente
> rotulado como `structural_impossibility` pelo verificador. Qualquer violador
> classificado como `implementation_error` ou `unknown` é tratado como falha,
> independentemente do valor de `satisfied_fraction`.

### Consequências para a saída do verificador

O verificador `validate_k_anonymity` reporta, para cada par (grafo, k):

- `coverage_fraction` — fração de nós cobertos (resultado da execução; não é um percentual fixo);
- `uncovered_fraction` — fração de nós não cobertos (derivada da anterior);
- `deficit_fully_structural` — `True` se 100% do déficit é atribuível a `incomplete_group`;
- lista de nós não cobertos com causa individual (para auditoria).

### Consequências para as métricas e os gráficos

Os relatórios de risco de reidentificação distinguem explicitamente:

- **(a)** taxas calculadas sobre **todos** os nós do grafo;
- **(b)** taxas calculadas apenas sobre o subconjunto com **k-anonimato estrutural estrito**.

### O que não muda

- O critério binário original do planejamento continua válido para o subconjunto de nós **cobertos**.
- A decisão D-06 permanece como política para grupos incompletos residuais.
- O piso `0.9` como limite de sanidade operacional é mantido, rebaixado de critério de passagem a condição necessária (mas não suficiente).

### Referências cruzadas

- Issue #16 (definição de pronto, campo D-06); issue #56 (testes dos campos DL-01)
- `docs/algorithm_notes.md` §4 e §7 (D-06, D-07)
- `docs/metrics_definitions.md` §k-anonymity-verifier
- Plano operacional, Seções 4.3, 7 e 11

---

## DL-02 — Campos de diagnóstico do ataque por subgrafo (timeouts + candidatos)

**Data:** 2026-06-02
**Issue relacionada:** #93 (D-08 / Fase 6 — sanitização diagnóstica dos zeros de
`reidentification_rate_subgraph` em k=20, d ∈ {5, 10})
**Módulo afetado:** `experiments/run.py`, `src/attacks/subgraph.py`

### Contexto

O schema JSONL DL-01 (issue #22) registra `reidentification_rate_subgraph` como
um único `float`. Um valor `0.0` é **interpretativamente ambíguo**: pode refletir
ausência de candidatos isomórficos (privacidade real / degeneração estrutural —
H1/H2), pluralidade de candidatos, ou — hipótese a descartar — timeouts do VF2
mascarados (H3). O log do d-sweep (#88) não distinguia esses casos.

Além disso, o runner anterior chamava `subgraph_attack(...)` por nó sem tratar
`TimeoutError`: um único nó que estourasse o `timeout` propagava a exceção até o
bloco `except Exception` do run inteiro, gravando `verdict=ERROR`. Isso
**contradizia** o comentário do YAML do d-sweep (*"Timeouts NÃO são crash — são
registrados e o nó conta como não reidentificado"*), que descrevia um
comportamento ainda não implementado.

### Passo 1 (diagnóstico, sem reexecução) — H3 descartada

A inspeção do log existente (`he2009_facebook_dsweep.jsonl`, 48 runs) mostrou
**nenhum** `verdict=ERROR` e **nenhum** campo `error` preenchido. Como o
`timeout` era 120 s e qualquer timeout teria produzido `ERROR` no código
anterior, a ausência de `ERROR` **prova** que nenhuma chamada VF2 atingiu 120 s.
**H3 está descartada** e o diagnóstico do Passo 1 é conclusivo — a reexecução
seletiva (Passo 3) torna-se opcional.

### Decisão adotada — estender o schema e alinhar o tratamento de timeout

1. **Novo observável `subgraph_candidate_count`** em `src/attacks/subgraph.py`:
   retorna o número de nós de `G'` cuja vizinhança hop-1 é isomórfica à do alvo.
   `subgraph_attack` passa a ser exatamente o predicado `count == 1` — sem
   mudança de comportamento (API e exceções idênticas; testes preexistentes
   verdes).
2. **Tratamento de timeout por nó** no runner: o `TimeoutError` é capturado por
   nó, contabilizado em `subgraph_timeout_count` e o nó conta como **não
   reidentificado** (`count = 0`). Isso alinha o código ao comentário do YAML e
   elimina o `verdict=ERROR` espúrio por um único nó lento.
3. **Dois campos novos no JSONL** (presentes só quando o ataque por subgrafo
   está habilitado):
   - `subgraph_timeout_count: <int>` — nós cujo VF2 estourou o timeout.
   - `subgraph_candidate_counts: {"mean": <float>, "std": <float>, "max": <int>}`
     — distribuição de candidatos isomórficos por nó, antes de filtrar por
     unicidade. Transforma "por que zero?" em dado observável: zero por ausência
     de candidatos (`max` baixo) vs. zero por timeout (`count > 0`).

### O que não muda

- O comportamento do ataque (valor de `timeout`, estratégia VF2, `hop`) é
  preservado — fora do escopo da issue #93.
- Logs DL-01 anteriores permanecem válidos; os campos novos são aditivos e só
  aparecem em execuções futuras com o ataque por subgrafo habilitado.
- O critério de veredito (`verdict_from_result`) não muda — `FAILURE_LOW_COVERAGE`
  em k=20, d ∈ {5, 10} continua decorrendo de `coverage_fraction < 0.9`, não de
  exceção.

### Referências cruzadas

- DL-01 (schema JSONL base, issue #22)
- D-08 (nota de encerramento do diagnóstico — abaixo), D-06, D-10
- Issue #93 (esta decisão); issue #88 (log do d-sweep); issue #78 (análise)
- `experiments/run.py` — laço do ataque por subgrafo (campos novos)
- `src/attacks/subgraph.py` — `subgraph_candidate_count`
- `experiments/configs/he2009_facebook_dsweep_k20_diag.yml` — reexecução opcional
- `docs/results_dsweep.md` §5.5 (ressalva atualizada para resolvida)

---

## DL-03 — `config_example.yml` expõe `d`/`sigma`/`s_max`/`isomorphism_mode`

**Data:** 2026-06-02
**Issue relacionada:** #106 (S8-3 / B5 — expor as chaves agora lidas)
**Módulo afetado:** `config_example.yml`, `docs/algorithm_notes.md` §5.1–5.3

### Contexto

O achado B5 (`docs/achados_divergencias.md`) registrou que a documentação
conceitual (`algorithm_notes.md` §5.1) mapeava `d`, `σ`, `s_max` e
`isomorphism_mode` como chaves de configuração, mas o `config_example.yml` de
referência **não as expunha** — expunha apenas `k_values`,
`validate_k_anonymity` e `allow_kl_fallback`. Após S8-1 (#104) e S8-2 (#105),
`s_max`/`fsm_max_size` e `isomorphism_mode` passaram a ser **chaves YAML
efetivamente lidas** pelo runner; `d` e `sigma` já eram lidos (presentes nos
YAMLs experimentais). O exemplo de referência ficou, então, atrás da interface
real.

### Decisão adotada — alinhar o exemplo à interface real

1. **Expor no bloco `anonymization` do `config_example.yml`**, com comentários
   e os defaults atuais:
   - `d` (default de referência `1`; nota sobre `d=1` = k-anon de grau vs.
     `d>1` = structure-aware — cross-ref B1; default conceitual do artigo `10`,
     D-02);
   - `sigma` (default `0.5`, D-01);
   - `s_max` (default `4`, D-01/A2; alias `fsm_max_size`, B5/#104);
   - `isomorphism_mode` (`add_or_delete` default | `add_only`, B6/#105).
2. **Corrigir `k_values` → `k`.** O runner lê `anonymization.k`
   (`experiments/run.py`), não `k_values`; o exemplo versionado expunha uma
   chave que o código nunca lê. Como o objetivo da issue é o exemplo refletir a
   **interface real** e **não documentar configurabilidade fantasma** (a mesma
   classe de erro que originou B5/B6), a chave foi renomeada para `k` —
   consistente com os YAMLs experimentais (ex.: `he2009_facebook_dsweep.yml`).

### Verificação de que cada chave exposta é lida

Confirmado em `experiments/run.py::main` (sem documentar configurabilidade
fantasma):

- `k` → `anon_cfg["k"]`; `d` → `anon_cfg["d"]` (ambas obrigatórias);
- `sigma` → `anon_cfg.get("sigma", 0.5)`;
- `s_max` → `anon_cfg.get("s_max", anon_cfg.get("fsm_max_size", 4))`;
- `isomorphism_mode` → `anon_cfg.get("isomorphism_mode", "add_or_delete")`
  (validada contra `_ISOMORPHISM_MODES` antes do laço).

### O que não muda (resíduos conhecidos, fora do escopo de #106)

- **`partition_backend`** permanece **não** exposto como chave YAML (apenas
  `allow_kl_fallback` controla a política de fallback, D-04).
- **`validate_k_anonymity`** segue exposta como documentação de política,
  embora a auditoria do runner atual rode sempre — chave reservada para tornar
  a auditoria opcional no futuro. Comentário no YAML registra essa ressalva.

### Referências cruzadas

- Achado B5 (e B6) em `docs/achados_divergencias.md`
- D-01 (`s_max`/σ), D-02 (`d`), B6/#105 (`isomorphism_mode`), B5/#104 (`s_max`)
- `docs/algorithm_notes.md` §5.1–5.3 (mapeamento atualizado)
- `experiments/run.py::main` (leitura efetiva das chaves)
- `experiments/configs/he2009_facebook_dsweep.yml` (uso real de `k`/`d`/`sigma`)

---

## Nota de milestone — Encerramento do S8 (#111, 2026-06-03)

> Marcador de milestone (não é uma decisão nova). Registra o fechamento da
> trilha S8, encerrada pela issue #111 (S8-8).

O milestone **S8** percorreu, em série, a correção das defasagens registradas em
`docs/achados_divergencias.md` e a revisão documental correspondente:

- **Trilha de código** (eliminou as defasagens 🔧 na raiz): #104 (`s_max`/
  `fsm_max_size` lido do YAML, B5), #105 (`isomorphism_mode` lido do YAML, B6),
  #112 (testes de propagação config→runner), #106 (`config_example.yml` expõe as
  chaves lidas — DL-03).
- **Trilha documental** (tornou explícitos os pontos ⚠️): #107 (A1 — baseline
  `d=1` rodou em KL), #108 (B1 — `d=1` afere k-anon de grau; d-sweep = estrutural),
  #109 (B2 dataset único + B7 timeouts retroativos).
- **Auditoria** #110 (S8-7): 11/11 achados ✅ reverificados, sem regressão.
- **Fechamento** #111 (S8-8): revisão cruzada de consistência (sem afirmação de
  configurabilidade sem respaldo no código; sem contradição KL/pymetis ou
  `d=1`/d-sweep) e migração formal de **todos** os status para ✅ na matriz da §1
  de `achados_divergencias.md`; §4 marcada como executada.

**Desfecho que excede o roteiro original:** B5/B6 (§4, itens 1–2) previam apenas
*anotar* `s_max`/`isomorphism_mode` como constantes hardcoded; foram resolvidos
por **correção de código** (chaves efetivamente lidas), não por reescrita
documental. Ver DL-03 e os achados B5/B6.

---

## D-01 — FSM simplificado com `s_max` configurável

**Data:** 2026-05-17  
**Issues relacionadas:** #8, #9, #12  
**Módulo afetado:** `src/anonymization/he2009.py` — `_group_isomorphic`

### Contexto

O artigo He et al. (2009) cita o uso de Frequent Subgraph Mining (FSM) para
agrupar Local Structures, referenciando Wörlein et al. (2005) [ref. 18] sem
especificar qual implementação usar. A alternativa mais completa (gSpan) tem
manutenção irregular em Python e introduziria dependência externa de difícil
auditoria.

### Decisão

Adotar **FSM simplificado** com tamanho máximo de subgrafo `s_max` configurável
(default: `s_max = 4`). A enumeração de subgrafos conexos induzidos usa hash
Weisfeiler-Lehman como forma canônica, evitando chamadas `nx.is_isomorphic` par
a par durante a fase de FSM. O parâmetro `s_max` limita o espaço de busca de
forma auditável e expõe o trade-off cobertura × custo como variável explícita.

### Consequências

- Declarar como **aproximação do FSM do artigo** no relatório de qualificação.
- O parâmetro `fsm_max_size` deve ser exposto no YAML de configuração
  (`anonymization.fsm.max_size`) para reprodutibilidade.
- Comparação com gSpan completo: fora do escopo mínimo; candidata a trabalho futuro.

### Nota: comportamento quando d > s_max (G2 — issue #75)

**Data da nota:** 2026-05-28

#### Contexto

Na implementação atual, `anonymize()` chama `_group_isomorphic()` sem passar
`fsm_max_size`, que fica no default 4. Quando `d > 4`, cada LS tem mais nós
do que `fsm_max_size` — o FSM nunca vê o padrão completo da LS, apenas
subgrafos conexos induzidos de até 4 nós.

#### Evidências empíricas (G2, issue #75)

Investigação realizada em `cycle_graph(20)` com `d=5`, `k=2`, `sigma=0.5`:

| `fsm_max_size` | Padrões catalogados | Padrões frequentes | Melhor padrão (MF) | Agrupamento |
|---|---|---|---|---|
| 4 (atual) | 4 | 4 (tamanhos 1–4) | P4, 3 arestas, suporte=4 | 2 grupos de 2 LSs |
| 5 (alternativa) | 5 | 5 (tamanhos 1–5) | P5, 4 arestas, suporte=4 | 2 grupos de 2 LSs (idêntico) |

Para LSs homogêneas (todos os padrões ≤4 nós compartilhados por todas as LSs),
o agrupamento é **idêntico** com `fsm_max_size=4` e `fsm_max_size=d`. Os 20
testes e2e de G1 (issue #75) passam com `d=5` confirmando comportamento correto.

#### Decisão adotada — Opção A: manter s_max=4 fixo

`fsm_max_size=4` é mantido como sub-padrão para todos os valores de `d`,
incluindo `d > 4`. Para `d > 4`, o FSM opera sobre sub-padrões de até 4 nós
— esta é uma aproximação documentada, não um bug.

**Razões:**

1. **Corretude garantida por `_modify_structure`** — o isomorfismo intra-grupo
   é garantido pela fase de modificação de arestas, não pelo FSM. O FSM apenas
   orienta a heurística de agrupamento; sub-padrões são suficientes para isso.
2. **Resultado idêntico verificado** — para `cycle_graph(20)` com `d=5`,
   `fsm_max_size∈{4,5}` produz o mesmo agrupamento.
3. **Custo computacional controlado** — `C(d, min(d,4))` subsets por LS vs.
   `C(d,d)=1` mais todos os menores (exponencial em `d`). Para `d=10`,
   elevar `s_max` para 10 poderia encontrar padrões tão específicos que
   nenhuma LS compartilharia, degradando o FSM e forçando agrupamento aleatório.
4. **Consistência do d-sweep** — manter `s_max` constante elimina um
   parâmetro confundente na comparação `d=1` vs `d>1` da issue #72.

**Opção B rejeitada** — elevar automaticamente `s_max` para `max(s_max, d)` via
YAML introduziria custo variável e potencial degradação de qualidade para `d`
grande. Não implementado.

#### Referências cruzadas (nota G2)

- Issue #75 (Checkbox #2 — Decisão s_max vs d)
- `src/anonymization/he2009.py:93` — `_group_within_bucket(fsm_max_size=4)`
- `tests/anonymization/test_he2009_e2e_d.py` — testes e2e G1 (d∈{2,5})

### Referências cruzadas

- `docs/algorithm_notes.md` §2.1 (pseudocódigo, tag `[D-01]`) e §7 (tabela)
- `src/anonymization/he2009.py` — `_group_isomorphic` (PR #49)

---

## D-02 — `d = 10` como default; variável de configuração YAML

**Data:** 2026-05-17  
**Issues relacionadas:** #7, #11  
**Módulo afetado:** `config_example.yml`, `src/anonymization/he2009.py`

### Contexto

O artigo He et al. (2009) não fixa um valor default para `d` (tamanho das
Local Structures em número de nós). Os experimentos do artigo usam valores
variados em função do dataset (p. 652).

### Decisão

Adotar `d = 10` como valor default, consistente com a literatura derivada para
redes de 1.000–10.000 nós. A varredura sobre `d` está **excluída do escopo
mínimo**; o parâmetro é exposto via `anonymization.d` no YAML para que experimentos
desejáveis ou aspiracionais possam variá-lo sem alteração de código.

### Consequências

- Todos os experimentos do escopo mínimo usam `d = 1` (convencionado após
  a seleção da ego-rede — issue #40), o que simplifica a partição a LSs
  individuais por nó e torna o comportamento determinístico para este dataset.
- Experimentos com `d > 1` podem expor o desbalanceamento KL (D-04) e
  violadores adicionais via D-07 — documentar quando realizados.

### Referências cruzadas

- `docs/algorithm_notes.md` §5 (tabela de parâmetros) e §7 (tabela D-02)
- `config_example.yml` (chave `anonymization.d`)

---

## D-03 — Matching Fase 1: grau primário + desempate lexicográfico

**Data:** 2026-05-17  
**Issues relacionadas:** #13  
**Módulo afetado:** `src/anonymization/he2009.py` — `_modify_structure`

### Contexto

A Fase 1 da etapa de isomorfização (He et al., p. 651) prescreve *"based on
nodes degree"* para o matching de nós entre Local Structures do mesmo grupo,
sem especificar critério de desempate quando dois nós têm o mesmo grau.
Ausência de critério determinístico tornaria o grafo `G'` dependente da ordem
de iteração da estrutura de dados, impossibilitando reprodutibilidade bit-a-bit.

### Decisão

Critério de ordenação dos nós dentro de cada LS para o matching:
1. **Primário:** grau do nó (decrescente — `−grau`).
2. **Desempate:** índice do nó (crescente, lexicográfico).

A ordenação é aplicada independentemente em cada LS; a posição `i` na LS_a
corresponde à posição `i` na LS_b. Não há uso de RNG nesta fase.

### Consequências

- O grafo `G'` é **determinístico** dado `G`, `k`, `d` e `seed` (a seed afeta
  apenas a fase de agrupamento, anterior ao matching).
- O critério de desempate é uma **escolha de implementação** não validada
  empiricamente contra alternativas (ex.: grau crescente, centralidade).
  Reportar como parâmetro de reprodutibilidade — não como escolha ótima.
- Diferenças entre critérios de desempate podem afetar o número de arestas
  modificadas na Fase 2; não investigado no escopo mínimo.

### Referências cruzadas

- `docs/algorithm_notes.md` §3.3 (tabela de fontes de não-determinismo) e §7
- `src/anonymization/he2009.py` — `_modify_structure` (PR #50)

---

## D-04 — Motor de particionamento: pymetis primário, KL fallback

**Data:** 2026-05-17 *(revisado em 2026-05-20)*  
**Issues relacionadas:** #11, #43, #44, #45  
**Módulo afetado:** `src/anonymization/_partition_backend.py`

### Contexto

O artigo He et al. (2009) cita explicitamente o algoritmo multilevel k-way
(Karypis & Kumar [ref. 14]) como motor de particionamento (p. 650). A versão
original de D-04 (2026-05-17) adotava `kernighan_lin_bisection` do NetworkX
como motor primário por ser dependência zero; a revisão de 2026-05-20
reconcilia com a referência do artigo após criação do skeleton em #33.

### Decisão (revisada 2026-05-20)

- **Motor primário:** `pymetis` (multilevel k-way, Karypis & Kumar) — fiel ao artigo.
- **Motor fallback:** `networkx.kernighan_lin_bisection` recursivo — ativado
  automaticamente quando `pymetis` não está disponível (CI, Windows sem Conda)
  ou via `anonymization.partition_backend: "networkx-kl"`. Emite `UserWarning`
  com motivo, implicação metodológica e referência D-04.
- **Seleção automática:** `backend="auto"` (default) — usa pymetis se disponível.

### Diferenças entre os motores

| Propriedade | pymetis (multilevel k-way) | KL bisection (fallback) |
|---|---|---|
| Complexidade | `O(\|E\|)` (declarada no artigo) | `O(\|E\| · log\|V\|)` (interpretativa) |
| Balanceamento de partições | Garantido via `tpwgts` | Não garantido para `ck > 2` |
| Disponibilidade | Requer compilação C (via conda-forge no Windows) | Stdlib do NetworkX |
| Fidelidade ao artigo | Alta | Aproximação |

### Limitação do fallback KL

A bissecção KL recursiva garante **contagem** e **cobertura disjunta** das
partições, mas **não balanceamento de tamanho** para `ck > 2`. Partições
individuais podem ser menores que `len(g) / ck`, aumentando violadores via
D-07 (Opção A). Este comportamento está documentado nos testes em
`tests/anonymization/test_partition_backend.py`, que verificam cobertura —
não tamanho exato — de forma consistente com essa limitação.

### Consequências para a qualificação

- A divergência entre os dois motores deve ser reportada como **parâmetro
  metodológico**, não como detalhe de implementação.
- Experimentos do escopo mínimo (d=1) executados com backend KL: impacto nulo
  (d=1 → partição trivial de nós individuais). Confirmado empiricamente no
  marco 29/05 (issue #16, PR #53).
- Experimentos com `d > 1` devem especificar o backend utilizado no log.

### Referências cruzadas

- `docs/algorithm_notes.md` §2.1 (pseudocódigo, tag `[D-04]`), §2.2 (complexidade) e §7
- `src/anonymization/_partition_backend.py` (PR #47)
- `environment.yml` e `scripts/setup_conda_windows.ps1` (PR #46) — solução Windows
- Issues #43 (discussão D-07 Opção A), #44 (pymetis no CI), #45 (implementação backend)

---

## D-05 — Verificador empírico estrito de k-anonimato

**Data:** 2026-05-17  
**Issues relacionadas:** #15, #34, #56  
**Módulo afetado:** `src/anonymization/validation.py`, `docs/metrics_definitions.md`

### Contexto

He et al. (2009) trata o k-anonimato como propriedade **garantida por
construção** — sem propor verificador externo. A garantia depende de três
premissas que a implementação não preserva automaticamente (ver D-06 e D-07).
Um verificador booleano par-a-par (esboço anterior) era estritamente mais
fraco que a Def. 2 do artigo e mascarava violações decorrentes de D-06 e D-07.

### Decisão

Implementar `validate_k_anonymity(groups, k) -> dict` como **auditor
independente**: não importa nada de `he2009.py`; opera sobre os grafos de saída
e a estrutura de grupos produzida pelo algoritmo. Verifica três condições em
orden de precedência:

1. **Disjunção global** — cada nó pertence a exatamente uma LS (`non_disjoint`).
2. **Cardinalidade mínima** — cada grupo completo tem pelo menos `k` LSs (`incomplete_group`).
3. **Isomorfismo mútuo** — todas as LSs de um grupo completo são mutuamente isomorfas via VF2 (`non_isomorphic`).

Retorna relatório estruturado com `valid`, `satisfied_fraction`, `coverage_fraction`,
`uncovered_fraction`, `deficit_fully_structural`, `n_violators`, `violators`,
`violations`. Registra entrada JSONL em `experiments/logs/validate_k_anonymity.jsonl`.

### Separação de responsabilidades

- **`algorithm_notes.md`** descreve o algoritmo e o critério formal.
- **`metrics_definitions.md`** define os instrumentos de avaliação.
- **`validation.py`** é o auditor — independente do anonimizador.

### Risco de desempenho

VF2 não é sabidamente polinomial. Para `d > 20`, avaliar pré-filtro por
invariantes baratos (distribuição de graus, espectro do laplaciano) antes
da chamada a `is_isomorphic`. O custo escala com `c · k²` chamadas (c grupos
de tamanho k). Documentar como limitação do protótipo.

### Referências cruzadas

- `docs/algorithm_notes.md` §4.2–4.3 e §7 (tabela D-05)
- `docs/metrics_definitions.md` §k-anonymity-verifier (issue #34, PR #42)
- `src/anonymization/validation.py` (PR #52)
- `tests/anonymization/test_validation.py` — cobertura dos campos DL-01 (PR #57, issue #56)

---

## D-06 — Política para grupos incompletos residuais

**Data:** 2026-05-17  
**Issues relacionadas:** #13, #15, #16  
**Módulo afetado:** `src/anonymization/he2009.py`, `src/anonymization/validation.py`

### Contexto

O Algorithm 1 de He et al. (2009) não especifica o tratamento para as LSs
restantes após o agrupamento principal — aquelas que não formam um grupo
completo de tamanho `k` (ocorre quando `n mod k ≠ 0` ou quando não há LSs
isomórficas suficientes para completar o último grupo).

### Decisão

Grupos com menos de `k` membros são **mantidos sem modificação** e reportados
como **grupo incompleto** (`incomplete_group`) pelo verificador. Os nós
residentes nesses grupos são registrados como **violadores de k-anonimato**
— desprotegidos estruturalmente para o `k` configurado. O módulo **não forçará**
fusão artificial nem descarte desses grupos no baseline.

### Limite esperado

Para `d = 1` (LSs de tamanho 1), o número esperado de nós residuais é
`n mod k` — no máximo `k − 1` nós. Para `d > 1`, o desbalanceamento KL
(D-04) pode aumentar o número de violadores além desse limite; nesse caso,
o campo `deficit_fully_structural` do verificador retornará `False` se
houver violadores além do grupo incompleto.

### Consequências para DL-01

A existência de grupos incompletos é a principal causa legítima de
`satisfied_fraction < 1.0` na validação empírica. DL-01 formaliza o
critério de distinção entre déficit estruturalmente aceitável (D-06) e
falha de implementação. Ver DL-01 acima.

### Referências cruzadas

- `docs/algorithm_notes.md` §2.1 (pseudocódigo, tag `[D-06]`), §4.1–4.2 e §7
- `src/anonymization/he2009.py` — `_group_isomorphic` (PR #49) e `_modify_structure` (PR #50)
- `src/anonymization/validation.py` — campo `incomplete_group` (PR #52)
- DL-01 (este documento)

---

## D-07 — Normalização de tamanho de LSs: Opção A adotada

**Data:** 2026-05-20  
**Issues relacionadas:** #43, #45, #12  
**Módulo afetado:** `src/anonymization/_partition_backend.py`, `src/anonymization/he2009.py`

### Contexto

O artigo He et al. (2009) pressupõe `|V_i| = d` estrito para todas as LSs
(p. 651: *"Since each of local structures in the same group has the same
number of nodes, this process will terminate quickly"*). Esta premissa é
necessária para que a Fase 1 do matching conclua em tempo finito. Com o
backend KL (D-04), partições podem ter tamanhos distintos, violando a
premissa e potencialmente travando o matching entre LSs com contagens de
nós diferentes.

Três opções foram consideradas em #43:

| Opção | Descrição | Problema |
|---|---|---|
| **A** | Restringir grupos a LSs do mesmo `\|Vi\|` | Aumenta violadores via D-06 |
| B | Preencher LSs menores com nós fictícios | Cria nós sem correspondência no grafo real |
| C | Ignorar a diferença e tentar o matching | Viola a premissa formal do artigo |

### Decisão

Adotar **Opção A**: na etapa de agrupamento (`_group_isomorphic`), LSs são
indexadas por tamanho (`|Vi|`); grupos formam-se **apenas entre LSs com o
mesmo número de nós**. LSs sem grupo completo do mesmo tamanho são tratadas
como grupo incompleto (D-06).

A política é aplicada exclusivamente em `_partition_backend.py` — transparente
para `_partition_neighborhoods`, `_group_isomorphic` e `_modify_structure`.

### Consequências

- Preserva a premissa formal do artigo para os grupos que se formam.
- Não introduz nós fictícios no grafo publicado.
- Pode aumentar o número de violadores via D-06 quando o backend KL produz
  partições desbalanceadas (especialmente para `d > 1`).
- Declarada como **limitação do protótipo** no relatório de qualificação.
- A produção futura pode usar `tpwgts` do pymetis para forçar tamanhos
  exatos, eliminando a necessidade desta política.

### Validação empírica (escopo mínimo com `d = 1`)

Para `d = 1`, todas as LSs têm tamanho 1 — a Opção A não gera violadores
adicionais além do `n mod k` esperado (D-06). Confirmado nos resultados
k∈{2, 5, 10, 20} (issues #16, #17; PRs #53, #54).

### Referências cruzadas

- `docs/algorithm_notes.md` §3.1 (nota ⚠️ D-07 formalizado), §4.1 e §7
- `src/anonymization/_partition_backend.py` — campo `meta["sizes"]` (PR #47)
- `src/anonymization/he2009.py` — `_group_isomorphic` — indexação por tamanho (PR #49)
- Issue #43 (discussão e votação entre opções; fechada 2026-05-20)

---

## D-08 — Política de conectividade de LSs: documentar como aproximação

**Data:** 2026-05-28
**Issue relacionada:** #75 (D-08 / Fase 2, G3)
**Módulo afetado:** `src/anonymization/_partition_backend.py`, `src/anonymization/he2009.py`

### Contexto

He et al. (2009) usa o conceito de *Local Structure* como um subgrafo induzido
conexo — implicitamente, cada LS deveria corresponder a uma vizinhança local
coerente do grafo. O algoritmo `_partition_neighborhoods` constrói as LSs como
subgrafos induzidos das partições geradas pelo pymetis. A questão levantada pela
issue #75 é: **o pymetis garante que cada partição produz um subgrafo induzido
conexo?**

### Evidência empírica (ego-rede 3437, seed=42)

Verificação realizada com `partition_graph(g, ck, seed=42, backend="pymetis")`.
A ego-rede 3437 possui n=534 nós e 2 componentes conexas (532 + 2 nós).

| Parâmetro | ck | Partições vazias | Partições desconexas (não-vazias) | Comportamento |
|---|---|---|---|---|
| d=2 | 267 | **199/267 (74,5%)** | 59/68 (86,8%) | Degenerate — pymetis colapsa em grupos de 7–8 |
| d=5 | 106 | 3/106 (2,8%) | 57/103 (55,3%) | Distribuição razoável (size 5–6), mas conectividade não garantida |

Interpretação do comportamento degenerate em d=2:
pymetis com ck muito grande (267 para n=534) falha no balanceamento — produz
199 partições vazias e concentra nós em grupos de tamanho 7–8 em vez de 2. Isso
é uma limitação conhecida do multilevel k-way para ck ≈ n/2 (partições muito
pequenas relativas ao tamanho do grafo).

Para d=5, a distribuição de tamanhos é razoável (maioria de tamanho 5–6), porém
55% dos subgrafos induzidos não são conexos — resultado esperado para uma
partição que minimiza cortes mas não impõe conectividade.

### Decisão adotada — Opção B: documentar como aproximação

**Não será implementado forçamento de conectividade** no protótipo atual.
O algoritmo `_partition_neighborhoods` continua retornando subgrafos induzidos
sem garantia de conectividade. Consequências:

1. **LS desconexas são tratadas como grafos desconexos normais** pelo restante
   do pipeline (FSM, `_modify_structure`, verificador). Isso é estruturalmente
   coerente com o código, embora desvie da premissa implícita do artigo.
2. **d=2 é inviável** nesta ego-rede com pymetis: o comportamento é degenerate.
   O d-sweep (issue #72) deve usar `d ∈ {5, 10}` ou documentar d=2 como
   caso degenerate com aviso explícito no YAML e nos resultados.
3. **d=5 produz partições razoáveis em tamanho** mas com conectividade parcial
   (~55% desconexas). Aceito como aproximação para o tier desejável; declarar
   como limitação em `docs/results_dsweep.md`.

### Opção A (forçar conectividade) — classificada como tier desejável

A opção A exigiria:
1. Detectar partições desconexas pós-pymetis.
2. Dividir cada partição desconexas em seus componentes conexos.
3. Re-agrupar fragmentos por tamanho para recompor partições de tamanho ≈ d.
Custo adicional: O(ck · d) extra pós-partição. Correto semanticamente mas
fora do escopo do protótipo. Candidato a futura extensão do backend.

### Recomendação operacional para o d-sweep

- **Usar d ∈ {5, 10}** como valores primários do d-sweep (#77).
- Incluir d=2 apenas se explicitamente anotado como "potencialmente degenerate"
  no YAML (`# WARNING: d=2 degenerate for this graph with pymetis`) e nos docs.
- Registrar `partition_backend` no JSONL de log (#77) para rastreabilidade (já
  previsto em D-04).

### Nota de encerramento do diagnóstico (issue #93, 2026-06-02)

A issue #93 (D-08 / Fase 6) fechou a ambiguidade interpretativa dos zeros de
`reidentification_rate_subgraph` em k=20, d ∈ {5, 10}. O Passo 1 (inspeção do
log do d-sweep, sem reexecução) confirmou **ausência de `verdict=ERROR`** nos 48
runs: como o `timeout` era 120 s e qualquer estouro teria gerado `ERROR` no
código então vigente, **nenhuma chamada VF2 atingiu o limite** — a hipótese de
timeout mascarado (H3) está **descartada**. Os zeros decorrem de privacidade
real / degeneração estrutural (H1/H2): sob EGS grande (≈ k·d), a vizinhança
original do alvo deixa de ter correspondência única em `G'` (zero ou múltiplos
candidatos). O runner foi instrumentado (DL-02) com `subgraph_timeout_count` e
`subgraph_candidate_counts` para tornar essa distinção observável em execuções
futuras. Ver DL-02 e `docs/results_dsweep.md` §5.5.

### Nota complementar (issue #80, 2026-06-02): G1 automatizado + esclarecimento da fórmula k(k−1) (G3)

A issue #80 (Fase 2 — Complementar) fechou quatro pendências derivadas dos
comentários pós-merge da #75. Duas geram registro aqui:

**G1 — conectividade das LSs agora é teste automatizado.** A verificação
manual da tabela acima virou `test_local_structures_connected_d_gt_1`
(`tests/anonymization/test_he2009_partition.py`), que mede e registra o
percentual de LSs desconexas por `d` na ego-rede 3437 (LCC, n=532, backend
`auto`/pymetis). O teste **não força** conectividade — apenas mede, coerente
com a Opção B. Valores reproduzidos (seed=0), consistentes com a tabela:

| d | ck | LSs vazias | LSs não-vazias | desconexas (não-vazias) |
|---|---|---|---|---|
| 2 | 266 | 199 (74,8%) | 67 | 58/67 (86,6%) |
| 5 | 106 | 1 (0,9%) | 105 | 59/105 (56,2%) |

O teste é pulado quando `data/raw/facebook/` está ausente (CI sem download);
o artefato é produzido localmente. Pequenas diferenças vs. a tabela original
(seed=42 ali, seed=0 aqui; e LCC vs. grafo bruto de 534 nós) não alteram o
diagnóstico: d=2 permanece degenerate e d=5 ~56% desconexas.

**G3 — a fórmula k(k−1) da reconexão é dependente da posição canônica.**
A validação isolada de `_reconnect_inter_edges` (`TestReconnectKTimesKMinusOne`)
expôs que o exemplo literal esboçado na #80 ("2 LSs de 1 nó cada → k(k−1)=2
arestas") está **incorreto**: ele é degenerate. O número de arestas adicionadas
ao reconectar **uma** inter-aresta de mesmo grupo depende das posições canônicas
(D-03) dos extremos:

- **extremos em posições distintas** → exatamente **k(k−1)** arestas novas
  (caso geral do artigo; verificado para k ∈ {2,3});
- **extremos na mesma posição** → um clique de **C(k,2) = k(k−1)/2** arestas
  entre os nós daquela posição;
- **LSs de 1 nó** (esboço da #80) → ambos os extremos na posição 0; os pares
  ordenados (i,j) colapsam e resta apenas a própria inter-aresta original
  (1 aresta), **não** k(k−1)=2.

Isto é **comportamento correto da construção não-direcionada**, não um bug do
núcleo — por isso a divergência é registrada aqui (conforme instrução da #80:
"divergência é correção de núcleo, não ajuste de teste") e os testes validam a
semântica documentada, não o esboço degenerate. A docstring de
`_reconnect_inter_edges` foi atualizada com essa ressalva, fechando o item
"derivação interpretativa pendente" de `algorithm_notes.md §3.2.2`.

**G5(a) — contadores de modificação por fase** (`edges_modified_phase2_intragroup`,
`edges_added_reconnection`) passam a ser expostos em
`g_prime.graph["metadata"]` por `anonymize()`, sem alterar sua assinatura de
retorno (pré-requisito declarado de G5-b na #77). **G2** acrescentou o caso
adversarial K₄/P₄/K₁,₃ a `_modify_structure`.

### Referências cruzadas

- D-04 (motor de particionamento — pymetis primário, KL fallback)
- D-06 (grupos incompletos residuais)
- D-07 (normalização de tamanho de LSs — Opção A)
- DL-02 (campos de diagnóstico do ataque por subgrafo — encerramento via #93)
- Issue #72 (issue-mãe: d-sweep tier desejável)
- Issue #75 (Fase 2: endurecer núcleo em d>1)
- Issue #80 (Fase 2 — Complementar: G1, G2, G3, G5-a)
- Issue #93 (Fase 6: sanitização diagnóstica dos zeros — H3 descartada)
- `src/anonymization/_partition_backend.py` — `_partition_pymetis`
- `src/anonymization/he2009.py` — `_partition_neighborhoods`

---

## D-09 — Pré-filtro VF2: documentar como limitação do protótipo

**Data:** 2026-05-28
**Issue relacionada:** #76 (checkbox 4)
**Módulo afetado:** `src/anonymization/validation.py` — `validate_k_anonymity`

### Contexto

D-05 registra: *"Para d > 20, avaliar pré-filtro por invariantes baratos
(distribuição de graus, espectro do laplaciano) antes da chamada a
`is_isomorphic`."* A issue #76 solicita avaliação formal para `d ∈ {2, 5, 10}`
sobre o grafo sintético `cycle_graph(20)` e sobre a ego-rede 3437 (n=534).

### Evidências empíricas (G5, issue #76)

Testes em `tests/anonymization/test_he2009_d_validator.py` executam o validador
para `d ∈ {2, 5, 10}` sobre `cycle_graph(20)` sem timeout. O experimento de
baseline completo (issues #23, PR #68) executou `validate_k_anonymity` para
`k ∈ {2, 5, 10, 20}` com `d=1` e 3 sementes sobre a ego-rede 3437 sem problemas.
Para os valores `d ∈ {2, 5}`, o número de chamadas VF2 é `O(k(k-1)/2)` por grupo;
com `k=2` e poucos grupos em `cycle_graph(20)`, o custo é de apenas `1` chamada VF2
por grupo — negativo do pré-filtro.

### Decisão adotada — Documentar como limitação do protótipo

**Não será implementado pré-filtro VF2** no escopo atual. Razões:

1. **Custo irrelevante para o d-sweep:** `d ∈ {2, 5, 10}` — bem abaixo do
   limiar `d > 20` citado em D-05. O custo VF2 para grafos de até 10 nós
   é desprezível.
2. **Grafo de referência pequeno:** A ego-rede 3437 (n=534) gera c_k ≤ 106
   partições para `d=5`. Com `k=2`, o custo máximo é 106 chamadas VF2 sobre
   grafos de 5 nós — sub-segundo.
3. **Escopo do protótipo:** O módulo é instrumento de medição empírica, não
   motor de produção. A substituição futura por pré-filtro é viável sem
   alteração de API.

**Declarar como limitação em `docs/limitations.md`** (seção de desempenho).
A implementação do pré-filtro é candidata a extensão de tier aspiracional.

### Referências cruzadas

- D-05 (verificador empírico estrito — risco de desempenho VF2 documentado)
- Issue #76 (checkbox 4 — avaliação e decisão sobre pré-filtro)
- `src/anonymization/validation.py` — `validate_k_anonymity` (condição 3)
- `tests/anonymization/test_he2009_d_validator.py` — G5(a) testes

---

## D-10 — Combo degenerado d=10, k=20: executar e anotar como degenerado no YAML

**Data:** 2026-05-28
**Issue relacionada:** #76 (checkbox 3)
**Módulo afetado:** `experiments/configs/` — YAML do d-sweep

### Contexto

A issue #76 solicita verificação do comportamento do combo `d=10, k=20` e
uma decisão: *"executar o combo mesmo assim (marcar como degenerado no YAML)
ou excluir da varredura?"*

Para `cycle_graph(20)` (n=20), `d=10` produz c_k = 2 partições. Com `k=20`,
o pipeline forma 1 grupo incompleto com 2 LSs — todas as 20 nós viram
violadores via D-06. Para a ego-rede 3437 (n=534), `d=10` produziria c_k ≈ 53
partições; `k=20` formaria ~2 grupos completos (40 nós protegidos) mais ~13
LSs residuais (~130 nós via D-06).

### Evidências empíricas (G5, issue #76)

`tests/anonymization/test_he2009_d_validator.py::TestDegenerateComboD10K20`
confirma:

- `anonymize(cycle_graph(20), k=20, d=10, seed=0)` completa sem exceção.
- Todas as violações são do tipo `incomplete_group` (D-06).
- `deficit_fully_structural=True` — estado correto, não é bug.
- `n_violators == 20` — todos os nós da rede sintética são residuais.

### Decisão adotada — Incluir no d-sweep com anotação de degenerado

Seguindo o precedente de D-08 (documentar como aproximação em vez de excluir):

1. **Incluir o combo `d=10, k=20` no YAML do d-sweep** com comentário explícito
   de degenerado:
   ```yaml
   # WARNING: d=10, k=20 degenerate for this graph — c_k < k; all nodes
   # are structural violators (D-06). Results are methodologically valid
   # (deficit_fully_structural=True) but provide no k-anonymity guarantees.
   ```
2. **Não excluir:** excluir obscurece o comportamento real do algoritmo em
   configurações extremas — dado relevante para a tese.
3. **Registrar em `docs/results_dsweep.md`** (a criar em #77) que combos com
   `c_k < k` produzem cobertura zero, e discutir o trade-off d vs k.

### Referências cruzadas

- D-06 (grupos incompletos residuais — causa raiz do comportamento)
- D-08 (precedente: documentar como aproximação)
- Issue #76 (checkbox 3 — verificação e decisão)
- Issue #77 (d-sweep — config YAML e logging)
- `tests/anonymization/test_he2009_d_validator.py::TestDegenerateComboD10K20`

---

## D-11 — Email-Enron direcionado → não-direcionado: simetrização por OR

**Data:** 2026-06-03
**Issues relacionadas:** #29 (issue-mãe — dataset secundário Email-Enron), #122 (S9-0 — âncora/enquadramento)
**Módulo afetado:** `src/loaders/` (loader Email-Enron, a implementar em issue posterior do S9)

### Contexto

O escopo `[D]` (desejável) prevê o **Email-Enron** (SNAP, versão estática) como
dataset secundário, reaproveitando a infraestrutura existente (runner, ataques,
métricas, visualização) sem alterar o núcleo de anonimização. O Email-Enron é,
porém, um grafo **direcionado por natureza**: a aresta `A → B` significa "A
enviou e-mail para B". Todo o pipeline foi calibrado e validado em grafos
**não-direcionados** — o Facebook Ego-Nets representa amizade, relação já
simétrica. É necessário, portanto, fixar uma regra de "achatamento" da direção
antes de alimentar o pipeline, e registrá-la como decisão antes de qualquer
código (esta issue trata apenas de decisão e enquadramento — ver "Não-escopo").

### Decisão adotada — simetrização simples (OR)

Cria-se a aresta não-direcionada `A — B` se houver e-mail em **qualquer**
direção: `A → B` **ou** `B → A`. Formalmente, o grafo não-direcionado `G_u`
é a projeção `E(G_u) = { {u, v} : (u → v) ∈ E(G_d) ∨ (v → u) ∈ E(G_d) }`.
Self-loops e multi-arestas resultantes são colapsados.

**Justificativa:**

1. **Comparabilidade** — é a convenção padrão do SNAP e da maioria dos
   trabalhos que usam o Email-Enron, o que torna os números defensáveis na
   qualificação e comparáveis à literatura.
2. **Retenção de estrutura** — o OR preserva o máximo de arestas, em paralelo
   metodológico com a retenção do LCC adotada no Facebook (Seção 3.2 dos docs
   de resultados).
3. **Cenário de risco conservador** — um grafo mais conexo gera mais alvos
   potenciais para os ataques estruturais (grau, subgrafo), ou seja, mede a
   vulnerabilidade agregada no pior caso razoável para a defesa.

### Impacto estrutural

A simetrização por OR **aumenta a densidade e a conectividade** em relação à
alternativa recíproca: toda comunicação unidirecional vira aresta. Isso
desloca a distribuição de grau para cima e tende a inflar o tamanho da maior
componente conexa. Como o pipeline opera sobre grafos não-direcionados, nenhuma
mudança no núcleo de anonimização, nos ataques ou nas métricas é necessária — a
projeção é responsabilidade exclusiva do loader.

### Alternativa considerada e rejeitada — reciprocidade (AND)

Manter `A — B` apenas quando há e-mail mútuo (`A → B` **e** `B → A`) modela um
laço social mais forte (comunicação confirmada nos dois sentidos), porém
descarta a maioria das arestas (e-mail corporativo é majoritariamente
unidirecional), produz um grafo muito mais esparso e foge da convenção do SNAP.
**Rejeitada** para o baseline do dataset secundário; **registrada como candidata
a análise de sensibilidade futura** (comparar OR vs. AND sob os mesmos `k`).

### Terminologia obrigatória

Ao reportar resultados sobre o Email-Enron, manter o enquadramento de aferição
(Seção 5 de `docs/scope.md`): "avaliar risco de reidentificação", "simular
associação controlada", "mensurar vulnerabilidade agregada" — nunca
"desanonimizar" ou "identificar" indivíduos.

### Referências cruzadas

- Issue #29 (issue-mãe — Email-Enron como dataset secundário do tier `[D]`)
- Issue #122 (S9-0 — âncora: decisão e enquadramento, sem código de loader)
- `docs/scope.md` §3 (Enron declarado tier `[D]`) e §7 (condições éticas — dataset público desidentificado)
- `src/loaders/` (loader a implementar em issue posterior do S9)
