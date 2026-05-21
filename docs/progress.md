# progress.md — Estado de progresso das sessões

> **Instrução ao agente:** Este arquivo deve ser lido no início de cada sessão
> (`leia docs/progress.md e continue de onde paramos`) e atualizado ao final de
> cada sessão produtiva.
>
> Mantenha o histórico de sessões anteriores — não apague entradas passadas.
> Apenas adicione novas entradas no topo da seção "Histórico".

---

## Estado atual

**Data da última atualização:** 2026-05-21

**Semana corrente:** Semana 2 (22–29/05/2026) — He et al. + validação obrigatória de k-anonimato

**Último passo concluído:**
- Issue #16 (Marco 29/05): script `experiments/run_milestone_29_05.py` executado com sucesso.
  - Resultado: `SUCCESS_PARTIAL` nas 3 sementes (42, 1337, 2718).
  - `satisfied_fraction=0.9962`, apenas `incomplete_group` (D-06 aceitável).
  - PR #53 aberto em `validation/milestone-29-05` aguardando revisão humana.
- Issues #11–#15 (pipeline He et al. + validador independente) todas fechadas.
- Decision log DL-01 documentado em `docs/decision_log.md`.

**Próximo passo planejado:**
- Aguardar merge do PR #53 (revisão humana obrigatória).
- Após merge: iniciar Semana 3 — ataques (grau e subgrafos), issue a abrir.

**Bloqueios ativos:**
- PR #53 aguarda revisão humana no VSCode antes do merge.

**Decisões pendentes de validação humana:**
- Revisão e merge do PR #53 (marco 29/05).

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
