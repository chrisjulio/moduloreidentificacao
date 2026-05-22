# progress.md — Estado de progresso das sessões

> **Instrução ao agente:** Este arquivo deve ser lido no início de cada sessão
> (`leia docs/progress.md e continue de onde paramos`) e atualizado ao final de
> cada sessão produtiva.
>
> Mantenha o histórico de sessões anteriores — não apague entradas passadas.
> Apenas adicione novas entradas no topo da seção "Histórico".

---

## Estado atual

**Data da última atualização:** 2026-05-22

**Semana corrente:** Semana 3 (29/05/2026 – início antecipado) — Ataques por grau e subgrafos

**Último passo concluído:**
- Issue #19 (degree_attack): PR #58 aberto.
  - `src/attacks/degree.py` implementado; `src/attacks/__init__.py` criado.
  - `tests/attacks/test_degree.py`: 10 casos de teste (DoD completo).
  - 198 testes passando, 4 skipped (pymetis); ruff limpo.

**Próximo passo planejado:**
- Aguardar revisão e merge de PR #58 (issue #19).
- Implementar issue #20 (subgraph_attack: `src/attacks/subgraph.py`) — pré-requisito de #21.
- Aguardar também revisão de PR #57 (issue #56) e PR #55 (issue #18).

**Bloqueios ativos:**
- PR #58 (issue #19) aguarda revisão humana no VSCode.
- PR #57 (issue #56) aguarda revisão humana no VSCode.
- PR #55 (issue #18) aguarda revisão humana no VSCode.

**Decisões pendentes de validação humana:**
- Revisão e merge do PR #58 (degree_attack, issue #19).
- Revisão e merge do PR #57 (testes DL-01, issue #56).
- Revisão e merge do PR #55 (docs marco 29/05, issue #18).

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
