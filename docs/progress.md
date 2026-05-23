# progress.md — Estado de progresso das sessões

> **Instrução ao agente:** Este arquivo deve ser lido no início de cada sessão
> (`leia docs/progress.md e continue de onde paramos`) e atualizado ao final de
> cada sessão produtiva.
>
> Mantenha o histórico de sessões anteriores — não apague entradas passadas.
> Apenas adicione novas entradas no topo da seção "Histórico".

---

## Estado atual

**Data da última atualização:** 2026-05-23

**Semana corrente:** Semana 3 (29/05/2026 – início antecipado) — Ataques + Métricas

**Último passo concluído:**
- Issue #23 implementada: experimento baseline Facebook Ego-Nets.
  - PR #61 (issue #22 — runner) mergeado em main.
  - `experiments/configs/he2009_facebook_baseline.yml` criado (ambos os ataques).
  - Experimento executado: 12 runs (4k × 3 sementes), todas SUCCESS_FULL/PARTIAL.
  - `docs/results_baseline.md` gerado com tabela bruta + agregações.
  - `experiments/make_baseline_table.py` script de geração da tabela.
  - PR a abrir na branch `experiment/facebook-baseline`.

**Próximo passo planejado:**
- Revisão humana e merge do PR de issue #23.
- Semana 4: gráficos e tabelas a partir dos logs JSONL (issue #24 planejada).

**Bloqueios ativos:**
- PR de issue #23 aguarda revisão humana.

**Decisões pendentes de validação humana:**
- Revisão e merge do PR de issue #23.

---

## Como atualizar este arquivo

Ao final de cada sessão produtiva, atualize a seção "Estado atual" acima e
adicione uma entrada no Histórico abaixo seguindo o modelo:

```markdown
### AAAA-MM-DD — Título breve da sessão

- **Concluído:** o que foi feito.
- **Próximo:** próximo passo imediato.
- **Bloqueios:** problemas que impedem progresso (ou "Nenhum").
- **Decisões pendentes:** pontos que precisam de validação humana (ou "Nenhuma").
```

---

## Histórico de sessões

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
