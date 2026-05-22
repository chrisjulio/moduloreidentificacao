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

**Semana corrente:** Semana 2 (22–29/05/2026) — He et al. + validação obrigatória de k-anonimato

**Último passo concluído:**
- Issue #17 (k-sweep k∈{2,10,20}): `experiments/run_k_sweep.py` executado com sucesso.
  - k=2: SUCCESS_FULL × 3 sementes (satisfied_fraction=1.0000).
  - k=10: SUCCESS_PARTIAL × 3 sementes (satisfied_fraction=0.9962, D-06 aceitável).
  - k=20: SUCCESS_PARTIAL × 3 sementes (satisfied_fraction=0.9774, D-06 aceitável).
  - Todos os k do escopo Mínimo (k∈{2,5,10,20}) agora validados empiricamente.
  - PR a abrir em `validation/k-sweep` aguardando revisão humana.
- Issue #16 (Marco 29/05): APROVADO. PR #53 aberto, aguarda revisão humana.

**Próximo passo planejado:**
- Abrir PR de `validation/k-sweep` para issue #17.
- Aguardar revisão e merge dos PRs #53 (issue #16) e #17.
- Após merges: Semana 3 — ataques por grau e subgrafos.

**Bloqueios ativos:**
- PR #53 (issue #16) aguarda revisão humana no VSCode.
- PR de issue #17 (k-sweep) a abrir — requer revisão humana.

**Decisões pendentes de validação humana:**
- Revisão e merge do PR #53 (marco 29/05, issue #16).
- Revisão e merge do PR de issue #17 (k-sweep).

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
