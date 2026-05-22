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
| [D-01](#d-01) | 2026-05-17 | Implementação | FSM simplificado com `s_max` configurável |
| [D-02](#d-02) | 2026-05-17 | Implementação | `d = 10` como default; variável de configuração YAML |
| [D-03](#d-03) | 2026-05-17 | Implementação | Matching Fase 1: grau primário + desempate lexicográfico |
| [D-04](#d-04) | 2026-05-17 *(rev. 2026-05-20)* | Implementação | Motor de particionamento: pymetis primário, KL fallback |
| [D-05](#d-05) | 2026-05-17 | Implementação | Verificador empírico estrito de k-anonimato |
| [D-06](#d-06) | 2026-05-17 | Implementação | Política para grupos incompletos residuais |
| [D-07](#d-07) | 2026-05-20 | Implementação | Normalização de tamanho de LSs — Opção A adotada |

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
