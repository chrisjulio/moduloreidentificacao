# progress.md — Estado de progresso das sessões

> **Instrução ao agente:** Este arquivo deve ser lido no início de cada sessão
> (`leia docs/progress.md e continue de onde paramos`) e atualizado ao final de
> cada sessão produtiva.
>
> Mantenha o histórico de sessões anteriores — não apague entradas passadas.
> Apenas adicione novas entradas no topo da seção "Histórico".

---

## Estado atual

**Data da última atualização:** 2026-06-03

**Semana corrente:** Pós S5 — refatoração e funcionalidades desejáveis (D-tier)

**Último passo concluído:**
- **Issue #108 (S8-5 / B1): frase-síntese `d=1` = k-anonimato de grau; d-sweep =
  estrutural — inserida no README e em `results_baseline.md`.** Fechado o achado
  de maior consequência interpretativa (B1). A síntese — "no regime `d=1` os
  resultados rotulados 'He et al. structure-aware' equivalem a k-anonimato de
  grau; a propriedade estrutural só é exercida no d-sweep `d∈{5,10}`; o contraste
  `d=1` vs. `d∈{5,10}` é a evidência empírica de privacidade estrutural" — entrou
  em **dois** pontos de destaque: (1) `README.md` §5, callout "Leitura-chave" no
  topo da seção de Resultados, antes da tabela do baseline; (2)
  `results_baseline.md`, nova seção "Leitura-chave — `d=1` afere k-anonimato de
  grau", junto à apresentação do baseline. Para não contradizer S8-4/A1 (mesmo
  arquivo, PR #117 já mergeado), as duas ressalvas foram declaradas
  **ortogonais**: uma trata do *parâmetro* `d` (grau vs. estrutura), a outra do
  *motor* (KL vs. pymetis). Em `achados_divergencias.md`, status detalhado de B1
  migrado ⚠️→✅ e item 5 das pendências documentais riscado; migração formal na
  tabela-resumo (linha 77) deixada para S8-8/#111. Referências citadas
  verificadas (D-02; `algorithm_notes.md` §5.3/§6.5/§9.1). Somente docs — sem
  alteração em `src/` ou testes; `ruff check .` limpo. Branch
  `docs/synthesis-d1-degree-vs-structural-108`, PR #118 (`Closes #108`).

- **Issue #107 (S8-4 / A1): `results_baseline.md` declara explicitamente que o
  baseline `d=1` rodou no fallback Kernighan-Lin — não pymetis.** O número-título
  do baseline ("k-anonimato atingido") foi produzido pelo motor **não fiel** ao
  artigo: à época (issue #23, 2026-05-23) pymetis estava ausente local e na CI
  (confirmado pela auditoria #74, 30/05), e `backend="auto"` resolveu para o KL;
  o JSONL do baseline é anterior à gravação de `partition_backend` (#84). Nova
  seção **"Motor de particionamento — baseline d=1 rodou em KL"** com (1) o motor
  efetivo, (2) inocuidade para `d=1` (partições triviais de 1 nó → o
  desbalanceamento do KL p/ `ck>2`, D-04, é irrelevante; validação do marco 29/05
  permanece válida) e (3) contraste com o d-sweep (#88: pymetis em 48/48). Bloco
  de metadados ganhou a linha do motor de particionamento. Em
  `achados_divergencias.md`, A1 (status detalhado + item 3 das pendências
  documentais) migrado ⚠️→✅; números de linha da evidência atualizados
  (`he2009.py:338`, `run.py:271`, `config_example.yml:109`); migração formal na
  tabela-resumo deixada para S8-8/#111. Somente docs — sem alteração em `src/` ou
  testes; `ruff check .` limpo. Branch `docs/baseline-declare-kl-fallback-107`,
  PR #117 (`Closes #107`).

- **Issue #106 (S8-3 / B5): `config_example.yml` passa a expor
  `d`/`sigma`/`s_max`/`isomorphism_mode` (chaves agora lidas).** Com S8-1 (#104)
  e S8-2 (#105) tornando `s_max`/`fsm_max_size` e `isomorphism_mode` chaves YAML
  efetivamente lidas pelo runner, o exemplo de referência foi alinhado à
  interface real. O bloco `anonymization` do `config_example.yml` ganhou `d`
  (default de referência `1`; nota B1 d=1 grau vs d>1 estrutural; default
  conceitual 10 = D-02), `sigma` (`0.5`, D-01), `s_max` (`4`, D-01/A2; alias
  `fsm_max_size`) e `isomorphism_mode` (`add_or_delete` | `add_only`, B6), todos
  com comentários e defaults corretos. **Correção adicional:** `k_values` → `k`
  — o runner lê `anonymization.k`, não `k_values` (configurabilidade fantasma,
  mesma classe de erro que originou B5/B6); alinhado aos YAMLs experimentais.
  Cada chave exposta foi **verificada** como lida em `experiments/run.py::main`.
  Decisão registrada como **DL-03** em `decision_log.md`; `algorithm_notes.md`
  §5.1–5.3 atualizadas (mapeamento, divergência fechada, parâmetros
  confirmados); achado **B5** em `achados_divergencias.md` migrado 🔧→✅ (resíduo
  único: `partition_backend` ainda não exposto como chave YAML). Sem alteração em
  `src/`; YAML validado (parse + chaves). `tests/experiments` **65 passed**.
  Branch `docs/config-example-expose-params-106`.

- **Issue #112 (S8-2b): testes de propagação das novas chaves
  (config→anonymize→`_modify_structure`/`_group_isomorphic`) + regressão.**
  Cobertura de teste dedicada à mudança de comportamento de #104 (`s_max`/
  `fsm_max_size`) e #105 (`isomorphism_mode`), que passaram a ser lidas do YAML.
  **`tests/anonymization/test_he2009_modify.py`** estendido com 3 classes
  (+18 testes) cobrindo o caminho via `anonymize()`: `isomorphism_mode="add_only"`
  → `_modify_structure(add_only=True)` (via spy `wraps`) e efeito "nenhuma
  aresta removida"; default `add_or_delete` (add_only=False); valor inválido
  levanta `ValueError`; `fsm_max_size` → `_group_isomorphic` (spy) e default 4;
  grouping idêntico para `s_max∈{4,5}` em `cycle_graph(20)`/d=5 (G2/D-01);
  regressão default==explicit e determinismo do baseline d=1. **Novo
  `tests/experiments/test_run_config_propagation.py`** (12 testes) cobre o
  caminho config→runner: `isomorphism_mode`/`s_max` gravados no JSONL e no
  `summary.json`; ausência da chave usa o default (`add_or_delete`/4); alias
  `fsm_max_size` aceito; `isomorphism_mode` inválido aborta `main()` antes do
  laço; valores efetivos chegam a `_modify_structure`/`_group_isomorphic` (spy
  helper `_SpyWrapper` que registra chamadas e delega à função real); regressão
  do baseline d=1 (duas execuções idênticas). Sem alteração em `src/`. Addenda
  B5/B6 em `achados_divergencias.md` atualizados (propagação coberta por #112).
  Suíte **549 passed**, ruff + format limpos. Branch
  `test/config-propagation-112`.

- **Issue #105 (S8-2 / B6): exposição de `isomorphism_mode` como chave lida
  do YAML.** A variante de isomorfização da Fase 2 deixou de ser
  `add_only=False` hardcoded: `anonymize()` ganhou o parâmetro
  `isomorphism_mode: str = "add_or_delete"` (valida o valor e o converte em
  `add_only = (isomorphism_mode == "add_only")`, repassando a
  `_modify_structure`); o runner (`experiments/run.py`) lê
  `anonymization.isomorphism_mode`, valida-o antes do laço, propaga-o a
  `anonymize()` e ao caminho inline (`_modify_structure(add_only=...)`) e grava
  o valor efetivo no JSONL e no `summary.json`. Constante
  `_ISOMORPHISM_MODES = {"add_or_delete", "add_only"}` adicionada a
  `he2009.py`. Default `add_or_delete` preserva o comportamento histórico.
  Docs: docstring de `anonymize()`, `algorithm_notes.md`
  §3.2.1/§3.4/§5.1/§5.2/§5.3, e addendum B6 em `achados_divergencias.md`
  (status 🔧→✅). Ajuste mínimo no stub `_always_error` de `test_runner.py`
  (novo kwarg; cobertura de propagação é S8-2b/#112). Suíte **525 passed**,
  ruff + format limpos. Branch `anonymization/expose-isomorphism-mode-105`.

- **Issue #104 (S8-1 / B5): exposição de `s_max`/`fsm_max_size` como chave lida
  do YAML.** O tamanho máximo de subgrafo do FSM simplificado deixou de ser
  hardcoded: `anonymize()` e `_group_isomorphic()` passaram a aceitar
  `fsm_max_size` (default 4) e o runner (`experiments/run.py`) lê
  `anonymization.s_max` (alias `fsm_max_size`) do YAML, propaga por `run_one()`
  e grava o valor efetivo no JSONL e no `summary.json`. Docs atualizadas:
  `algorithm_notes.md` §5.1/§5.2/§5.3 (chave YAML lida), `limitations.md` §2.1,
  e addenda em `achados_divergencias.md` (A2, B5). Suíte **525 passed**, ruff
  limpo. Branch `anonymization/expose-smax-104`, PR #113 (`Closes #104`).

- **Issue #80 (D-08 / Fase 2 — Complementar: G1, G2, G3, G5-a), o único trabalho
  de engenharia ainda aberto sob a issue-mãe #72.** As quatro pendências
  derivadas dos comentários pós-merge da #75 foram implementadas em
  `anonymization/dsweep-complementar-80`:
  - **G5(a):** `anonymize()` agora expõe contadores de modificação por fase em
    `g_prime.graph["metadata"]` — `edges_modified_phase2_intragroup` (Fase 2,
    via `_modify_structure(return_counts=True)`, opt-in) e
    `edges_added_reconnection` (reconexão, contado em `_reconnect_inter_edges` e
    gravado no atributo do grafo). Sem mudança na assinatura de retorno
    (pré-requisito de G5-b na #77). +8 testes.
  - **G3:** validação isolada da fórmula `k(k−1)` em `_reconnect_inter_edges`
    (k∈{2,3}). **Achado:** o exemplo literal da #80 (LSs de 1 nó → k(k−1)=2)
    está **incorreto** — é degenerate (extremos na posição 0 colapsam para 1
    aresta). A fórmula k(k−1) vale para extremos em **posições canônicas
    distintas**; mesma posição → clique de C(k,2)=k(k−1)/2. Divergência
    registrada sob **D-08** no `decision_log.md` (correção de núcleo ≠ ajuste de
    teste); docstring de `_reconnect_inter_edges` atualizada (fecha o item
    "derivação interpretativa pendente" de `algorithm_notes §3.2.2`). +5 testes.
  - **G1:** `test_local_structures_connected_d_gt_1` mede e registra o % de LSs
    desconexas na ego-rede 3437 (LCC, backend auto) para d∈{2,5}; não força
    conectividade. Reproduz D-08: d=2 199/266 vazias + 86,6% desconexas
    (degenerate); d=5 56,2% desconexas. Pulado se `data/raw` ausente. +2 testes.
  - **G2:** caso adversarial K₄/P₄/K₁,₃ em `_modify_structure` — assertiva (a)
    mutuamente isomorfos, (b) arestas adicionadas ≤ k·|E(K₄)|=18, (c) sem
    self-loop/multi-aresta. +4 testes.
  Suíte **525 passed** (+19), ruff limpo.

**Próximo passo planejado:**
- Revisão humana e merge do PR #118 (`docs/synthesis-d1-degree-vs-structural-108`)
  → fechar #108. Com S8-4 (#107) já mergeado e S8-5 (#108) entregue, a próxima
  edição de `results_baseline.md` está livre de seriação pendente.
- **S8-8 (#111):** migração formal dos status na tabela-resumo de
  `achados_divergencias.md` (inclui a linha 77 de B1, ⚠️→✅, agora desbloqueada
  por #108, além de A1/B5/etc.).
- Revisão humana e merge do PR `docs/config-example-expose-params-106` → fechar
  #106. Em seguida: S8-8 (#111 — migração formal dos status na tabela-resumo de
  `achados_divergencias.md`), que #106 e #107 desbloqueiam.
- Revisão humana e merge do PR de `test/config-propagation-112` → fechar #112.
- Revisão humana e merge do PR `anonymization/dsweep-complementar-80` → fechar a
  issue #80. Com #80 fechada, **toda a engenharia da issue-mãe #72 (d-sweep) está
  concluída** → fechar #72 (umbrella) com comentário de encerramento.
- Revisão humana e **fechamento manual da issue #74** (não fechada pela auditoria).

**Bloqueios ativos:**
- PR de `test/config-propagation-112` (a abrir) aguardará revisão humana.
  (Dependências #104 e #105 já mergeadas em `main`.)

**Decisões pendentes de validação humana:**
- D-08 (conectividade de LSs): decisão Opção B registrada. O d-sweep **manteve**
  d=2 (anotado como potencialmente degenerate, precedente D-10) em vez de excluir;
  confirmar se essa escolha é a definitiva.

---

## Como atualizar este arquivo

Ao final de cada sessão produtiva, atualize a seção "Estado atual" acima e
adicione uma entrada no Histórico abaixo seguindo o modelo:

```markdown
### AAAA-MM-DD — Título breve da sessão

- **Concluído:** o que foi feito.
- **Próximo:** próximo passo imediato.
- **Bloqueios:** bloqueios que impedem progresso (ou "Nenhum").
- **Decisões pendentes:** pontos que precisam de validação humana (ou "Nenhuma").
```

---

## Histórico de sessões

### 2026-06-03 — Issue #108 (S8-5 / B1): frase-síntese d=1 = k-anon de grau, d-sweep = estrutural

- **Concluído:** Fechado o achado B1 (maior consequência interpretativa). A
  frase-síntese — `d=1` (baseline) afere **k-anonimato de grau**; a propriedade
  *structure-aware* só é exercida no d-sweep `d∈{5,10}`; o contraste é a
  evidência empírica de privacidade estrutural — inserida em dois pontos de
  destaque: `README.md` §5 (callout "Leitura-chave" no topo dos Resultados,
  antes da tabela do baseline) e `results_baseline.md` (nova seção "Leitura-chave
  — `d=1` afere k-anonimato de grau", junto à apresentação do baseline). Para não
  contradizer S8-4/A1 (mesmo arquivo), as duas ressalvas foram declaradas
  **ortogonais** (parâmetro `d` vs. motor KL/pymetis). Em `achados_divergencias.md`,
  status detalhado de B1 ⚠️→✅ e item 5 das pendências riscado; tabela-resumo
  (linha 77) deixada para S8-8/#111. Referências citadas verificadas (D-02;
  `algorithm_notes.md` §5.3/§6.5/§9.1). Somente docs; `ruff check .` limpo.
  Branch `docs/synthesis-d1-degree-vs-structural-108`, PR #118.
- **Próximo:** Merge do PR #118 → fechar #108; depois S8-8 (#111, migração formal
  dos status na tabela-resumo, incl. B1 linha 77). Merges pendentes de #106/#112.
- **Bloqueios:** PR #118 aguarda revisão humana (S8-4/#107 já em `main`).
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-03 — Issue #107 (S8-4 / A1): results_baseline.md declara baseline d=1 em KL

- **Concluído:** Fechado o achado A1 — `results_baseline.md` declara
  explicitamente que o número-título do baseline `d=1` ("k-anonimato atingido")
  veio do fallback Kernighan-Lin, **não** pymetis (ausente local e na CI à época;
  auditoria #74). Nova seção "Motor de particionamento — baseline d=1 rodou em
  KL": (1) motor efetivo (KL via `backend="auto"`; JSONL anterior à gravação de
  `partition_backend`/#84); (2) inocuidade para `d=1` (partições triviais → o
  desbalanceamento do KL p/ `ck>2`, D-04, é irrelevante; validação do marco 29/05
  válida); (3) contraste com o d-sweep (#88: pymetis em 48/48). Linha do motor
  adicionada ao bloco de metadados. Em `achados_divergencias.md`, A1 (status
  detalhado + item 3 das pendências) migrado ⚠️→✅ e line numbers da evidência
  atualizados; migração da tabela-resumo deixada para S8-8/#111. Somente docs;
  `ruff check .` limpo. Branch `docs/baseline-declare-kl-fallback-107`, PR #117.
- **Próximo:** Merge do PR #117 → fechar #107; depois S8-5 (frase-síntese B1,
  também edita `results_baseline.md`). Merges pendentes de #106/#112; depois
  S8-8 (#111, migração formal dos status).
- **Bloqueios:** PR #117 aguarda revisão humana (#104/#105/#106 já em `main`).
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-03 — Issue #106 (S8-3 / B5): config_example.yml expõe d/sigma/s_max/isomorphism_mode

- **Concluído:** Alinhado o `config_example.yml` de referência à interface real
  do runner, fechando a parte `config_example` do achado B5. O bloco
  `anonymization` passou a expor `d` (default `1`; nota B1 d=1 grau vs d>1
  estrutural; conceitual 10 = D-02), `sigma` (`0.5`, D-01), `s_max` (`4`,
  D-01/A2; alias `fsm_max_size`, B5/#104) e `isomorphism_mode`
  (`add_or_delete` | `add_only`, B6/#105) — todos com comentários e defaults
  corretos. `k_values` corrigido para `k` (chave realmente lida pelo runner;
  evita configurabilidade fantasma). Cada chave verificada como lida em
  `experiments/run.py::main`. Decisão DL-03 em `decision_log.md`;
  `algorithm_notes.md` §5.1–5.3 atualizadas; B5 em `achados_divergencias.md`
  migrado 🔧→✅ (resíduo: `partition_backend`). Sem alteração em `src/`; YAML
  validado; `tests/experiments` 65 passed. Branch
  `docs/config-example-expose-params-106`.
- **Próximo:** Merge do PR → fechar #106; depois S8-8 (#111, migração formal dos
  status na tabela-resumo). Merge de `test/config-propagation-112` → fechar #112.
- **Bloqueios:** PR a abrir aguardará revisão humana (#104/#105 já em `main`).
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-02 — Issue #112 (S8-2b): testes de propagação das chaves + regressão

- **Concluído:** Cobertura de teste da mudança de comportamento de #104
  (`s_max`/`fsm_max_size`) e #105 (`isomorphism_mode`), agora lidas do YAML.
  `tests/anonymization/test_he2009_modify.py` +18 testes (3 classes) no caminho
  `anonymize()`: `isomorphism_mode` → `_modify_structure(add_only=...)` via spy
  `wraps` + efeito "nenhuma aresta removida" sob `add_only`; default
  `add_or_delete`; valor inválido → `ValueError`; `fsm_max_size` →
  `_group_isomorphic` (spy) e default 4; grouping idêntico `s_max∈{4,5}` em
  `cycle_graph(20)`/d=5 (G2/D-01); regressão default==explicit e determinismo
  d=1. Novo `tests/experiments/test_run_config_propagation.py` (12 testes) no
  caminho config→runner: chaves gravadas no JSONL e `summary.json`; default na
  ausência; alias `fsm_max_size`; `isomorphism_mode` inválido aborta `main()`;
  valores efetivos chegando a `_modify_structure`/`_group_isomorphic` (helper
  `_SpyWrapper`); regressão baseline d=1. Sem alteração em `src/`. Addenda B5/B6
  de `achados_divergencias.md` atualizados. Suíte **549 passed**, ruff + format
  limpos. Branch `test/config-propagation-112`.
- **Próximo:** Merge do PR → fechar #112; depois S8-3 (#106, `config_example.yml`).
- **Bloqueios:** PR a abrir aguardará revisão humana (#104/#105 já mergeadas).
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-02 — Issue #105 (S8-2 / B6): expor isomorphism_mode lido do YAML

- **Concluído:** Corrigida a defasagem B6 — a variante de isomorfização da
  Fase 2 estava `add_only=False` hardcoded em `anonymize()` e no runner, e a
  chave YAML `isomorphism_mode` nunca era lida. `anonymize()` (he2009.py)
  passou a aceitar `isomorphism_mode: str = "add_or_delete"`, validar o valor
  contra `_ISOMORPHISM_MODES = {"add_or_delete", "add_only"}` (ValueError em
  valor inválido), convertê-lo em `add_only` e repassá-lo a
  `_modify_structure`. `experiments/run.py` lê `anonymization.isomorphism_mode`
  (default `add_or_delete`), valida antes do laço de execução, propaga por
  `run_one()` a `anonymize()` e ao caminho inline
  (`_modify_structure(add_only=...)`), e grava o valor efetivo em cada entrada
  JSONL (`"isomorphism_mode"`) e no `summary.json`. Default preserva o
  comportamento histórico. Docs: docstring de `anonymize()`,
  `algorithm_notes.md` §3.2.1/§3.4/§5.1/§5.2/§5.3 (chave YAML ativa) e addendum
  B6 (🔧→✅) em `achados_divergencias.md` (itens 1–2 das pendências documentais
  marcados como resolvidos). Stub `_always_error` de `test_runner.py` aceita o
  novo kwarg (cobertura de propagação é S8-2b/#112). Suíte **525 passed**,
  ruff + format limpos. Branch `anonymization/expose-isomorphism-mode-105`.
- **Próximo:** Merge do PR → fechar #105; depois S8-2b (#112) e S8-3 (#106).
- **Bloqueios:** PR a abrir aguardará revisão humana.
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-02 — Issue #104 (S8-1 / B5): expor s_max/fsm_max_size lido do YAML

- **Concluído:** Corrigida a defasagem B5 (achado A2) — `s_max`/`fsm_max_size`
  estava hardcoded (nem `anonymize()` nem o runner passavam o parâmetro →
  `_group_within_bucket` usava default 4). `anonymize()` e `_group_isomorphic()`
  passaram a aceitar `fsm_max_size: int = 4` e propagá-lo até
  `_group_within_bucket`; `experiments/run.py` lê `anonymization.s_max` (alias
  `fsm_max_size`) do YAML, propaga por `run_one()` e grava o valor efetivo em
  cada entrada JSONL (`"fsm_max_size"`) e no `summary.json` (sem alterar a
  assinatura de retorno de `anonymize()`; default 4 preserva o comportamento).
  Docs: `algorithm_notes.md` §5.1 (chave YAML lida)/§5.2 (nota B5)/§5.3,
  `limitations.md` §2.1, addenda em `achados_divergencias.md` (A2, B5; migração
  formal do status 🔧→✅ na tabela-resumo deixada para S8-8/#111). Ajuste mínimo
  no stub `_always_error` de `test_runner.py` para aceitar o novo kwarg (nova
  cobertura é S8-2b/#112). Suíte **525 passed**, ruff + format limpos. Branch
  `anonymization/expose-smax-104`, PR #113.
- **Próximo:** Merge do PR #113 → fechar #104. Recomendado mergear S8-1 antes de
  S8-2 (#105, `isomorphism_mode`); depois S8-2b (#112) e S8-3 (#106).
- **Bloqueios:** PR #113 aguarda revisão humana.
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-02 — Issue #80 (D-08 / Fase 2 — Complementar): G1, G2, G3, G5-a

- **Concluído:** Implementadas as quatro pendências da #80 (último trabalho de
  engenharia aberto sob a issue-mãe #72). **G5(a):** contadores por fase
  (`edges_modified_phase2_intragroup`, `edges_added_reconnection`) expostos em
  `g_prime.graph["metadata"]` por `anonymize()`, via `_modify_structure(
  return_counts=True)` (opt-in) e contagem em `_reconnect_inter_edges`, sem
  alterar a assinatura de retorno. **G3:** validação isolada de `k(k−1)` na
  reconexão (k∈{2,3}) — achado de que o exemplo de 1 nó da #80 é degenerate
  (colapsa para 1 aresta); a fórmula vale para extremos em posições canônicas
  distintas (mesma posição → C(k,2)); registrado sob D-08 no `decision_log.md` e
  na docstring. **G1:** `test_local_structures_connected_d_gt_1` mede/registra o
  % de LSs desconexas na 3437 (d∈{2,5}; reproduz D-08: d=2 degenerate, d=5 ~56%),
  pulado sem `data/raw`. **G2:** caso K₄/P₄/K₁,₃ em `_modify_structure` com as
  assertivas (a)(b)(c). +19 testes; suíte **525 passed**, ruff limpo. Branch
  `anonymization/dsweep-complementar-80`.
- **Próximo:** Merge do PR → fechar #80; depois fechar a umbrella #72 (toda a
  engenharia do d-sweep concluída). Fechamento manual da #74.
- **Bloqueios:** PR `anonymization/dsweep-complementar-80` aguarda revisão humana.
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-02 — Issue #93 (D-08 / Fase 6): diagnóstico dos zeros de reid_sub (k=20, d∈{5,10})

- **Concluído:** Sanitização diagnóstica dos zeros de
  `reidentification_rate_subgraph`. **Passo 1** (sem reexecução): log do d-sweep
  (48 runs) sem nenhum `verdict=ERROR` nem campo `error` → como o `timeout` era
  120 s e qualquer estouro produziria `ERROR` no código vigente, **nenhuma
  chamada VF2 atingiu o limite** → **H3 (timeout mascarado) descartada**; zeros
  genuínos (H1/H2). **Passo 2:** `experiments/run.py` — laço do ataque por
  subgrafo captura `TimeoutError` por nó (conta em `subgraph_timeout_count`,
  trata o nó como não-reidentificado, eliminando `verdict=ERROR` espúrio e
  alinhando ao comentário do YAML); novos campos `subgraph_timeout_count` e
  `subgraph_candidate_counts {mean,std,max}` no JSONL; `subgraph_candidate_count`
  adicionado a `src/attacks/subgraph.py` (e exportado), com `subgraph_attack`
  reescrito como `count == 1` (comportamento idêntico). Schema DL-01 no docstring
  atualizado. **DL-02** + nota de encerramento de **D-08** em `decision_log.md`.
  **Passo 3:** opcional (Passo 1 conclusivo) — `he2009_facebook_dsweep_k20_diag.yml`
  criado como artefato de reprodução, não executado (custo ≈3 h/run). **Passo 4:**
  `results_dsweep.md` §5.5 (ressalva → resolvida) e §5.7 (ameaça de timeout
  afastada para este log). +16 testes; suíte **506 passed**, ruff limpo. Branch
  `diag/subgraph-zeros-k20`.
- **Próximo:** Merge do PR `diag/subgraph-zeros-k20` → fechar #93 (comentário com
  verdict do Passo 1). Fechamento manual da #74.
- **Bloqueios:** PR `diag/subgraph-zeros-k20` aguarda revisão humana.
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-02 — Issue #78 (D-08 / Fase 5): docs do d-sweep + ameaças à validade

- **Concluído:** Fechados os itens remanescentes da DoD da #78. As seções 1
  (visualizações d-aware) e 2 (`results_dsweep.md`) já tinham sido entregues por
  #92/#94 e #88; esta sessão cobriu a seção 3 e a seção 4. (a) `results_dsweep.md`:
  nova §5.7 "Ameaças à validade" (interna — interação `s_max × d`, pymetis vs KL,
  k-way não garante LS conexa, custo VF2/timeouts; construção — contraste `d=1` vs
  `d>1` como evidência de privacidade estrutural; externa — única ego-rede 3437).
  (b) `limitations.md §1.3`: rebaixada de limitação aberta para **parcialmente
  resolvida** (resíduo = generalização a outras ego-redes/datasets), com a entrada
  correspondente na tabela de ameaças reclassificada para validade externa.
  (c) `algorithm_notes.md §9`: nova §9.4 com os achados do d-sweep (déficit sempre
  estrutural; EGS ≈ k·d; vetores de ataque opostos em k; combos degenerados
  D-08/D-10; ressalva de timeouts) e ponteiro para o relatório. Sem alteração em
  `src/` — viz e runner d-aware já em `main`. Suíte **490 passed**, ruff limpo.
  Branch `docs/dsweep-analysis-78`.
- **Próximo:** Merge do PR `docs/dsweep-analysis-78` → fechar #78. Fechamento
  manual da #74.
- **Bloqueios:** PR `docs/dsweep-analysis-78` aguarda revisão humana.
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-02 — Relatório consolidado final do d-sweep (#88): docs/results_dsweep.md

- **Concluído:** Fechado o último item pendente da DoD da issue #88. Com a viz
  d-aware (#92/#94) mergeada em `main`, regenerei os artefatos do log do d-sweep
  (48 registros, `experiments/logs/he2009_facebook_dsweep/`) via as ferramentas
  já existentes: tabelas CSV d-aware (`results/tables/facebook_{degree,subgraph}.csv`,
  agora com coluna `d`) e duas figuras (`privacy_utility_dsweep_series` e
  `..._facets`), ambas não versionadas conforme `.claude/rules/experiments.md`.
  Escrevi `docs/results_dsweep.md` (relatório final): metadados, cobertura 16/16
  células, tabelas `média ± std` por `(k,d)`, análise (déficit estrutural em
  48/48 com `valid=false`+`deficit_fully_structural=true`; tendências opostas
  grau×subgrafo em k; efeito de `d`; combos degenerados D-08 d=2 e D-10 d=10/k=20;
  ressalva de que `reid_sub=0` em k alto pode refletir timeouts VF2, não
  segurança — o JSONL não registra contagem de timeouts), comandos de reprodução
  e referências cruzadas. `dsweep_previa_garantia_dados.md` rebaixada a snapshot
  histórico com ponteiro para o relatório final. Branch `docs/results-dsweep`.
- **Próximo:** Merge do PR `docs/results-dsweep` → fechar #88. Fechamento manual da #74.
- **Bloqueios:** PR `docs/results-dsweep` aguarda revisão humana.
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-02 — Visualização ciente de `d` (#92): plots e tabelas d-aware

- **Concluído:** `src/visualization/tables.py` e `privacy_utility.py` estendidos
  para tratar a dimensão `d` do d-sweep. `tables.py`: `"d"` adicionado a
  `CSV_COLUMNS` (após `"k"`, mudança intencional de spec), `record_to_row`
  extrai `record.get("d", 1)`, sort `(k, d, seed)`. `privacy_utility.py`:
  `aggregate_by_k_d` nova (chaves `(k, d)`); `aggregate_by_k` preservada com
  comportamento idêntico (pool por `k`, retrocompatível); `plot_privacy_utility_dsweep`
  nova com dois layouts (`series` — cor por `d`, estilo de linha por ataque/métrica;
  `facets` — grade 2×4); CLI com `--dsweep`/`--layout` + auto-detecção (mais de um
  `d` distinto → modo d-aware). Fallback `d=1` em todos os caminhos para logs
  pré-DL-01. Testes: +6 (tables) e +~30 (privacy_utility), incluindo fixtures de
  grade 4k×4d×3s e checagem de retrocompat. Verificado end-to-end no log real
  (48 registros): 16 células `(k,d)` nas CSVs, plots `series` e `facets` gerados.
  Suíte completa **490 passed**; ruff limpo.
- **Próximo:** Merge do PR `viz/dsweep-d-aware` (#92); gerar artefatos finais e o
  relatório consolidado do d-sweep. Fechamento manual da #74.
- **Bloqueios:** PR `viz/dsweep-d-aware` aguarda revisão humana.
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-02 — d-sweep (#88): execução completa 48/48 + runner d-list

- **Concluído:** O runner (`experiments/run.py`) passou a aceitar
  `anonymization.d` como **lista** (além de escalar), varrendo o produto
  cartesiano `k × d × seed` com uma entrada JSONL por combinação; `summary.json`
  grava `d_values` e vereditos por `(k,d,seed)`. 4 testes novos em
  `tests/experiments/test_runner.py` (produto cartesiano, presença de cada `d`,
  registro no summary, compat. com `d` escalar). O experimento
  `he2009_facebook_dsweep` rodou **48/48 com pymetis em todos os runs**, sem
  erros (≈31 h de parede, dominadas pelo VF2 do ataque por subgrafo em k alto);
  o processo sobreviveu a uma desconexão do terminal do VSCode (processo
  independente, gravação JSONL incremental). Vereditos: 33 SUCCESS_PARTIAL /
  15 FAILURE_LOW_COVERAGE. Consolidação legível em
  `docs/dsweep_previa_garantia_dados.md` (nasceu como prévia de garantia de dados
  a 43/48, atualizada para o estado final).
- **Próximo:** criar issue `viz/dsweep-d-aware` (plots/tabelas ignoram `d`); só
  então gerar artefatos finais e o relatório consolidado.
- **Bloqueios:** Nenhum.
- **Decisões pendentes:** D-08 — d=2 foi mantido (anotado degenerate, D-10) em vez
  de excluído; confirmar se é a escolha definitiva.

### 2026-05-31 — pymetis: explicitação do backend + cobertura na CI (#84, #85, #86)

- **Concluído:** Partindo do achado de que o pymetis **já funciona** no ambiente
  conda local (439→443 passed, 0 skipped), três gaps de visibilidade/cobertura
  foram fechados, cada um em sua branch/PR, **todos mergeados** em `main`
  (`3410e58`), na ordem #84 → #85 → #86, com CI verde:
  - **#84** (gap #2): `partition_backend` gravado em cada entrada JSONL e
    `partition_backends` no `summary.json`; `_partition_neighborhoods` ganhou
    `return_meta`. Resultados passam a ser auto-documentados quanto ao backend.
  - **#85** (gap #1): job `test-pymetis` (micromamba + `environment.yml`,
    conda-forge) exercita o motor primário na CI — os 4 testes antes pulados
    agora rodam. `lint-and-test` (pip) mantém cobertura do fallback KL.
  - **#86** (gap #3): correção do erro factual do README §13 (introduzido por
    #82/#83 — o `.venv` do §3.2 não inclui pymetis em nenhum SO); nota em
    `limitations.md` §2.2; flag opt-in `anonymization.allow_kl_fallback`
    (padrão `true`) + helper `pymetis_available()`; atualização da nota de CI em
    `pipeline.md`; remoção do resíduo rastreado `.vscode/.gitkeep_remove`.
- **Próximo:** Fechamento manual da issue #74; confirmar D-08 / d=2 no d-sweep (#77).
- **Bloqueios:** Nenhum.
- **Decisões pendentes:** D-08 (Opção B registrada; aguarda validação humana).

### 2026-05-30 — Auditoria #74 (Fase 1) + análise de sessão travada

- **Concluído:** Auditoria de prontidão d>1 (issue #74, somente leitura, sem
  alteração em `src/`). Estado de PR/`main`: nenhum PR aberto, working tree limpo
  em `main` @ `74b188c`, `experiment/d-sweep` sincronizada (PR #79 mergeado em
  `a057519`). Backend de particionamento: pymetis ausente local e na CI (não está
  em `requirements*.txt`; só extra `partition-c` no `pyproject.toml`) → ambos usam
  fallback `networkx-kl`; degradação de sizing para `ck>2` confirmada e já
  documentada (D-04/D-07, `algorithm_notes.md §7`). Testes de particionamento
  d=2/d=5: 18 passed sob KL. **Inventário do núcleo diverge do esperado:**
  `_group_isomorphic` (`test_he2009_grouping.py`, 28 testes) e `_modify_structure`
  (`test_he2009_modify.py`, 32 testes) têm cobertura ampla com `|LS|>1`; e2e d>1
  em `test_he2009_e2e_d.py` (TestE2eD2/D5/D10 + TestValidatorCoherence). A lacuna
  prevista para a Fase 2 (#75) já foi preenchida por #75/#76 (PR #79). Suíte: 435
  passed, 4 skipped (exigem pymetis; idêntico local↔CI). Resultado comentado na
  issue #74, **mantida aberta** conforme instrução. Diagnosticada a sessão anterior
  (`d0e51803`, ~23h): ~11 min de trabalho real + travamento de 23,7h num prompt de
  permissão de um one-liner PowerShell, sessão desacompanhada. Subprodutos: regra
  de permissão local read/test (`.claude/settings.local.json`) e nova seção no
  `CLAUDE.md` ("Inspeção de arquivos e busca de conteúdo") preferindo `Grep`/`Read`
  a one-liners de shell.
- **Próximo:** Revisão humana e fechamento manual da #74; confirmar D-08 / d=2 no d-sweep (#77).
- **Bloqueios:** Nenhum.
- **Decisões pendentes:** D-08 (Opção B registrada; aguarda validação humana).

### 2026-05-28 — Issue #76 G5(a): deficit_fully_structural e equivalence_group_size em d>1

- **Concluído:** `tests/anonymization/test_he2009_d_validator.py` criado (23 testes,
  3 classes). `TestDeficitFullyStructuralD`: pipeline d∈{2,5} → violations apenas
  `incomplete_group`; casos sintéticos confirmam `deficit_fully_structural=False` com
  `non_isomorphic` (size mismatch d=2 e d=5; path vs cycle). `TestEquivalenceGroupSizeD`:
  mean=k·d para grupos completos (d=2→4, d=5→10); mean≠k·d para tamanhos mistos
  (KL aproximação — limitação registrada). `TestDegenerateComboD10K20`: cycle_graph(20)
  d=10 k=20 → `deficit_fully_structural=True`, `n_violators=20` — comportamento correto,
  não bug. Decisões D-09 (pré-filtro VF2: limitação) e D-10 (combo degenerado: incluir
  no YAML com aviso) registradas em `docs/decision_log.md`. 439 passed, ruff limpo.
  Branch `experiment/d-sweep`.
- **Próximo:** Abrir PR para a branch `experiment/d-sweep`, cobrindo issues #75 e #76.
- **Bloqueios:** Nenhum.
- **Decisões pendentes:** Confirmar D-08: d=2 excluído ou anotado como degenerate (D-10
  registrado; aguarda validação humana no contexto do YAML do d-sweep).

### 2026-05-28 — Issue #75 e2e d=10: validação da Opção A para d=10

- **Concluído:** `TestE2eD10` adicionada a `test_he2009_e2e_d.py` com 6 testes
  caixa-preta (`anonymize(cycle_graph(20), k=2, d=10, seed∈{0,7})`). `TestValidatorCoherence`
  estendida de `d∈{2,5}` para `d∈{2,5,10}` (4 testes × 3 valores = 12 casos).
  Confirma Opção A (G2): `s_max=4` fixo produz pipeline coerente mesmo com `d=10 > fsm_max_size=4`.
  412 passed, ruff limpo. Commit `47bd872` em `experiment/d-sweep`.
- **Próximo:** G5(a) — início de #76 (validador e métricas em d>1).
- **Bloqueios:** Nenhum.
- **Decisões pendentes:** Confirmar D-08: d=2 excluído ou anotado como degenerate.

### 2026-05-28 — Issue #75 G2: decisão s_max vs d (D-01, Checkbox #2)

- **Concluído:** Investigação empírica do FSM quando `d > fsm_max_size=4`.
  `cycle_graph(20)`, d=5: 4 padrões frequentes (tamanhos 1–4); agrupamento idêntico
  com `fsm_max_size∈{4,5}`. Decisão Opção A registrada em `docs/decision_log.md`
  (nota G2 sob D-01): manter `s_max=4` fixo para todos os valores de d do d-sweep.
  Sem alteração em `src/`. 406 passed, ruff limpo.
- **Próximo:** e2e com d=10 para confirmar Opção A; depois G5(a) / início de #76.
- **Bloqueios:** Nenhum.
- **Decisões pendentes:** Confirmar D-08: d=2 excluído ou anotado como degenerate.

### 2026-05-28 — Issue #75 G1: teste e2e anonymize() d=2 e d=5

- **Concluído:** `tests/anonymization/test_he2009_e2e_d.py` criado com 20 testes
  em 3 classes. `TestE2eD2` e `TestE2eD5` cobrem caixa-preta de `anonymize()`;
  `TestValidatorCoherence` (parametrizado d∈{2,5}) verifica coerência do validador
  (`valid` ou `deficit_fully_structural=True`) e ausência de violações `non_isomorphic`
  (condição 4.3, VF2). Grafo `cycle_graph(20)`, sementes 0 e 7. 406 passed, ruff limpo.
  Commit `ba1c10b` em `experiment/d-sweep`.
- **Próximo:** G2 (Decisão s_max vs d — verificar FSM quando d > fsm_max_size=4;
  registrar em decision_log.md sob D-01).
- **Bloqueios:** Nenhum.
- **Decisões pendentes:** Confirmar D-08: d=2 excluído ou anotado como degenerate no d-sweep.

### 2026-05-28 — Issue #75 G3: verificação de conectividade de LSs + decisão D-08

- **Concluído:** Branch `experiment/d-sweep` criada. G3 (Checkbox #3 de #75):
  verificação empírica de conectividade das LSs geradas por pymetis para d ∈ {2, 5}
  na ego-rede 3437. Achados críticos: (a) ego-rede 3437 é desconexo (2 componentes:
  532 + 2 nós); (b) d=2 degenerate — pymetis produz 199/267 partições vazias e nós
  concentrados em grupos 7–8; (c) d=5 razoável em tamanho (5–6) mas 55% desconexas.
  Decisão D-08 registrada em `docs/decision_log.md`: Opção B (documentar como
  aproximação); forçamento de conectividade = tier desejável futuro.
- **Próximo:** G1 (testes e2e `anonymize(g, k=2, d={2,5})` em grafo pequeno ~20 nós).
- **Bloqueios:** Nenhum.
- **Decisões pendentes:** Confirmar se d=2 deve ser excluído ou apenas anotado no d-sweep.

### 2026-05-25 — Encerramento da issue #26

- **Concluído:** PR #68 (issue #64 / #26-B) confirmado mergeado. Issue #26 fechada com
  comentário de encerramento documentando todos os critérios atendidos. Sub-issues #63 e #64
  cobriram os 5 critérios da definição de pronto: ①②③ pela #64 (diagramas, comandos, outputs),
  ④⑤ pela #63 (limitations.md, revisão e cross-referências dos docs).
- **Próximo:** Semana 5 — issues #27 (reprodutibilidade end-to-end) e #28 (README final + revisão docs).
- **Bloqueios:** Nenhum.
- **Decisões pendentes:** Nenhuma.

### 2026-05-25 — Documentação técnica do pipeline (issue #64)

- **Concluído:** PR #67 (issue #25) confirmado mergeado. Branch `docs/pipeline-technical` criada.
  `docs/pipeline.md` criado com: diagrama Mermaid de fluxo de execução (Config YAML → anonimização
  → ataques → métricas → JSONL → visualizações); diagrama Mermaid de arquitetura de módulos
  (todos os `src/` com dependências); comandos reproduzíveis verificados localmente para cada etapa;
  tabela de parâmetros YAML; tabela de outputs com localização; referências cruzadas para
  `algorithm_notes.md`, `metrics_definitions.md` e `limitations.md`.
  386 passed. Ruff limpo. PR #68 aberto.
- **Próximo:** Merge do PR #68. Avaliar issues #27 (cold start) e #28 (revisão global docs).
- **Bloqueios:** PR #68 aguarda revisão humana.
- **Decisões pendentes:** Revisão humana do PR #68.

### 2026-05-25 — Tabelas CSV de resultados (issue #25)

- **Concluído:** PR #66 (issue #24) confirmado mergeado. Branch `viz/tables` criada.
  `src/visualization/tables.py` implementado com três funções públicas:
  `load_jsonl_records`, `record_to_row`, `generate_tables` + CLI
  `python -m src.visualization.tables --logs <dir> --out results/tables --dataset facebook`.
  Uma tabela CSV por `(dataset, ataque)`, colunas: `k, seed, reid_rate, eq_group_mean, ks_D, ks_p, clustering_var`.
  Saída em `results/tables/` (não versionada). 43 testes em `tests/visualization/test_tables.py`,
  todos passando. Suite completa: 382 passed, 4 skipped. Ruff limpo. PR #67 aberto.
- **Próximo:** Merge do PR #67. Avaliar tarefas remanescentes da Semana 4 (polimento/documentação).
- **Bloqueios:** PR #67 aguarda revisão humana.
- **Decisões pendentes:** Revisão humana do PR #67.

### 2026-05-25 — Gráfico privacy-vs-utility (issue #24)

- **Concluído:** PR #62 (issue #23) confirmado mergeado. Branch `viz/privacy-utility` criada.
  `src/visualization/privacy_utility.py` implementado com três funções públicas:
  `load_jsonl_records`, `aggregate_by_k`, `plot_privacy_utility` + CLI
  `python -m src.visualization.privacy_utility --logs <dir>`.
  Figura de 2 painéis: Privacidade (taxa de reidentificação % vs k, curva por ataque) e
  Utilidade (clustering_variation + KS-D vs k), barras de erro = ±1 std entre sementes.
  PDF + PNG salvos em `results/plots/` (não versionados).
  35 testes em `tests/visualization/test_privacy_utility.py`, todos passando.
  Suite completa: 339 passed, 4 skipped. Ruff limpo. PR #66 aberto.
- **Próximo:** Merge do PR #66. Avaliar tarefas remanescentes da Semana 4.
- **Bloqueios:** PR #66 aguarda revisão humana.
- **Decisões pendentes:** Revisão humana do PR #66.

### 2026-05-25 — Encerramento de S3: PR #65 (#26-A / issue #63)

- **Concluído:** Issue #63 (#26-A) fechada. `docs/limitations.md` produzido;
  cross-referências entre `algorithm_notes.md` e `metrics_definitions.md`
  estabelecidas. PR #65 (`docs/pipeline-academic`) em revisão final.
- **Próximo:** Fechar CI do PR #65; aplicar polimentos ②③④; merge; abrir
  issue #26-B (parâmetros do pipeline, §5.4). Em seguida, S4: issues #24
  (gráficos) e #25 (tabelas CSV).
- **Bloqueios:** CI vermelho no PR #65 (Python 3.11/3.12) — único bloqueio real. [já resolvidos]
- **Decisões pendentes:** Nenhuma.

### 2026-05-23 — Experimento baseline: he2009_facebook_baseline (issue #23)

- **Concluído:** PR #61 (issue #22 — runner) confirmado mergeado. Branch
  `experiment/facebook-baseline` criada. `experiments/configs/he2009_facebook_baseline.yml`
  com ambos os ataques habilitados (degree + subgraph hop=1, timeout=60s),
  k∈{2,5,10,20}, 3 sementes. Experimento executado via
  `python -m experiments.run` — 12 runs completas, exit code 0.
  Resultados: k=2→SUCCESS_FULL×3 (rr_grau=0.026, rr_sub=0.791);
  k=5→SUCCESS_PARTIAL×3 (rr_grau=0.008, rr_sub=0.406);
  k=10→SUCCESS_PARTIAL×3 (rr_grau=0.023, rr_sub=0.140);
  k=20→SUCCESS_PARTIAL×3 (rr_grau=0.099, rr_sub=0.000).
  `experiments/make_baseline_table.py` gerador da tabela criado.
  `docs/results_baseline.md` com tabela bruta + agregações commitado.
  PR a abrir.
- **Próximo:** Merge do PR de issue #23. Semana 4: gráficos/tabelas (issue #24).
- **Bloqueios:** PR de issue #23 aguarda revisão humana.
- **Decisões pendentes:** Revisão humana do PR de issue #23.

### 2026-05-22 — Runner de experimentos: experiments/run.py (issue #22)

- **Concluído:** `experiments/__init__.py` (torna o diretório um pacote Python),
  `experiments/run.py` (runner CLI com argparse, YAML → pipeline → JSONL),
  `experiments/configs/he2009_facebook_full.yml` (config k=[2,5,10,20], 3 sementes),
  `tests/experiments/test_runner.py` (37 testes, todos passando).
  Pipeline por (k, seed): partition → group → modify → reconnect → validate_k_anonymity
  → degree_attack em todos os nós → reidentification_rate, equivalence_group_size,
  ks_test_degree, clustering_variation → JSONL com schema DL-01 completo.
  Ruff limpo. 308 testes passando.
  PR #61 aberto.
- **Próximo:** Merge do PR #61. Executar experimento completo para produzir logs JSONL.
  Semana 4: gráficos/tabelas a partir dos logs.
- **Bloqueios:** PR #61 aguarda revisão humana.
- **Decisões pendentes:** Revisão humana do PR #61.

### 2026-05-22 — Alinhamento documental: registro dos merges e abertura da issue #22

- **Concluído:** PRs #55, #57, #58, #59, #60 mergeados em `main` pelo humano.
  `progress.md` sincronizado com o estado real do repositório. `CLAUDE.md`
  atualizado com regra de verificação de PRs antes de iniciar nova issue.
- **Próximo:** Implementar issue #22 (`experiments/run.py`) a partir de `main`.
- **Bloqueios:** Nenhum.
- **Decisões pendentes:** Nenhuma.

### 2026-05-22 — Métricas: src/metrics/ (issue #21)

- **Concluído:** `src/metrics/reidentification_rate.py` (`reidentification_rate(attack_results) -> float`), `src/metrics/equivalence_group_size.py` (`equivalence_group_size(groups) -> tuple[float, int]` — aceita `list[list[nx.Graph]]` idêntico ao `validate_k_anonymity`), `src/metrics/ks_test_degree.py` (`ks_test_degree(g_orig, g_anon) -> tuple[float, float]` via `scipy.stats.ks_2samp`), `src/metrics/clustering_variation.py` (`clustering_variation(g_orig, g_anon) -> float`). `src/metrics/__init__.py` exporta as 4 funções. 52 novos testes em `tests/metrics/` cobrindo edge cases, valores conhecidos, invariantes de tipo e intervalo. 267 passando, 4 skipped; ruff limpo. PR #60 aberto.
- **Próximo:** Aguardar merge dos PRs #60, #59, #58, #57, #55. Implementar issue #22 (runner).
- **Bloqueios:** PRs #60, #59, #58, #57, #55 aguardam revisão humana.
- **Decisões pendentes:** Revisão humana dos cinco PRs.

### 2026-05-22 — Ataque por subgrafos: subgraph_attack (issue #20)

- **Concluído:** `src/attacks/subgraph.py` criado com `subgraph_attack(g_orig, g_anon, target, hop=1, timeout=None) -> bool`. Backend VF2 via `GraphMatcher.is_isomorphic`. Helper `_k_hop_induced_subgraph` encapsula extração de vizinhança. Timeout opcional via `concurrent.futures`. `src/attacks/__init__.py` atualizado para exportar ambos os ataques. `tests/attacks/test_subgraph.py` com 17 casos cobrindo: identificação única (True), múltiplos candidatos (False), zero candidatos (False), hop=2 discrimina onde hop=1 falha (lollipops assimétricos), timeout via mock, inputs inválidos. 215 passando, 4 skipped; ruff limpo. PR #59 aberto.
- **Próximo:** Aguardar merge de PRs #59, #58. Implementar issue #21 (métricas).
- **Bloqueios:** PRs #59, #58, #57, #55 aguardam revisão humana.
- **Decisões pendentes:** Revisão humana dos quatro PRs.

### 2026-05-22 — Ataque por grau: degree_attack (issue #19)

- **Concluído:** `src/attacks/degree.py` criado com `degree_attack(g_orig, g_anon, target, tolerance=0) -> bool`. `src/attacks/__init__.py` criado. `tests/attacks/test_degree.py` com 10 casos cobrindo: identificação única (True), múltiplos candidatos (False), zero candidatos (False), tolerance != 0, target inválido (ValueError), tolerance negativa (ValueError). 198 passando, 4 skipped; ruff limpo. PR #58 aberto.
- **Próximo:** Aguardar merge de PR #58. Implementar issue #20 (subgraph_attack).
- **Bloqueios:** PR #58, #57, #55 aguardam revisão humana.
- **Decisões pendentes:** Revisão humana dos três PRs.

### 2026-05-22 — Testes DL-01: coverage_fraction, uncovered_fraction, deficit_fully_structural (issue #56)

- **Concluído:** `TestDL01Fields` adicionada a `tests/anonymization/test_validation.py` com 16 novos casos de teste cobrindo os três campos introduzidos por DL-01. Sem alterações em `src/`. 51 testes passando; ruff limpo. PR #57 aberto.
- **Próximo:** Aguardar merge de PR #57 e PR #55. Iniciar Semana 3: ataques por grau e subgrafos.
- **Bloqueios:** PR #57 e PR #55 aguardam revisão humana.
- **Decisões pendentes:** Revisão humana dos dois PRs.

### 2026-05-22 — Documentação do marco 29/05 (issue #18)

- **Concluído:** `docs/validacao_k_anonimato.md` criado com registro consolidado da validação: data, hashes de commits, tabela de configuração, tabela de resultados para k∈{2,5,10,20} × 3 sementes, análise de violações (nenhuma crítica), decisão de prosseguir para Semana 3. `CLAUDE.md` atualizado com link. PR #55 aberto.
- **Próximo:** Aguardar merge do PR #55. Iniciar Semana 3: ataques por grau e subgrafos.
- **Bloqueios:** PR #55 aguarda revisão humana.
- **Decisões pendentes:** Revisão humana do PR #55.

### 2026-05-22 — k-Sweep k∈{2,10,20}: todos os k do escopo Mínimo validados (issue #17)

- **Concluído:** Script `experiments/run_k_sweep.py` + 3 YAMLs (`he2009_facebook_k_sweep_k{2,10,20}.yml`) criados e executados. k=2: SUCCESS_FULL × 3; k=10: SUCCESS_PARTIAL × 3 (sf=0.9962); k=20: SUCCESS_PARTIAL × 3 (sf=0.9774). Resultados documentados em `docs/algorithm_notes.md` Seção 9. PR a abrir.
- **Próximo:** Abrir PR para issue #17. Aguardar merges (#53 e #17). Iniciar Semana 3: ataques por grau e subgrafos.
- **Bloqueios:** PRs #53 e k-sweep aguardam revisão humana.
- **Decisões pendentes:** Revisão humana dos dois PRs.

### 2026-05-21 — Marco 29/05: validação k-anonimato k=5, d=1 (issue #16)

- **Concluído:** Script `experiments/run_milestone_29_05.py` + YAML `experiments/configs/milestone_29_05.yml` criados e executados. Resultado APROVADO nas 3 sementes (satisfaction_fraction=0.9962, apenas incomplete_group). PR #53 aberto.
- **Próximo:** Merge do PR #53 (revisão humana). Semana 3: ataques por grau e subgrafos.
- **Bloqueios:** PR #53 aguarda revisão.
- **Decisões pendentes:** Revisão humana do PR #53.

### 2026-05-21 — Inicialização do repositório e estrutura de sessão

- **Concluído:** Repositório criado com estrutura completa (src, tests, docs, experiments, scripts, data, results), CLAUDE.md, WORKFLOW.md, CI GitHub Actions, pre-commit, environment.yml, pyproject.toml, config_example.yml. Adicionada instrução de continuidade de sessão ao CLAUDE.md e criado este arquivo.
- **Próximo:** Implementar loader das Facebook Ego-Nets (`src/loaders/facebook_ego.py`).
- **Bloqueios:** Nenhum.
- **Decisões pendentes:** Nenhuma.
