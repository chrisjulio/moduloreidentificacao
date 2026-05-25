# progress.md — Estado de progresso das sessões

> **Instrução ao agente:** Este arquivo deve ser lido no início de cada sessão
> (`leia docs/progress.md e continue de onde paramos`) e atualizado ao final de
> cada sessão produtiva.
>
> Mantenha o histórico de sessões anteriores — não apague entradas passadas.
> Apenas adicione novas entradas no topo da seção "Histórico".

---

## Estado atual

**Data da última atualização:** 2026-05-25

**Semana corrente:** Semana 4 (05/06/2026) → transição para Semana 5

**Último passo concluído:**
- Issue #26 fechada: toda a documentação técnica do pipeline concluída.
  - PR #68 (issue #64 / #26-B) confirmado mergeado.
  - Sub-issues #63 (#26-A) e #64 (#26-B) encerradas; issue pai #26 fechada.
  - Critérios atendidos: diagrama Mermaid do pipeline (`docs/pipeline.md` §2/§3),
    comandos reproduzíveis (§5), lista de outputs com localização (§7),
    `docs/limitations.md`, cross-referências entre `algorithm_notes.md` e
    `metrics_definitions.md`.

**Próximo passo planejado:**
- Semana 5 (S5): issues #27 (reprodutibilidade end-to-end / cold start) e
  #28 (README final + revisão global da documentação).

**Bloqueios ativos:**
- Nenhum.

**Decisões pendentes de validação humana:**
- Nenhuma.

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
