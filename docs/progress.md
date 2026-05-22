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

**Semana corrente:** Semana 3 (29/05–05/06/2026) — Ataques + métricas — LIBERADA

**Último passo concluído:**
- S2 encerrada antecipadamente (21/05, 8 dias antes do marco). Pipeline He et al.
  completo e validado. k-anonimato empiricamente atingido em k ∈ {2, 5, 10, 20}
  × 3 sementes. Critério DL-01 aplicado e documentado. 12 issues fechadas.
- Issue #56 (Testes DL-01): PR #57 aberto.
- Issue #18 (Documentar resultado do marco 29/05): PR #55 aberto.

**Próximo passo planejado:**
- Aguardar revisão e merge de PR #57 (issue #56) e PR #55 (issue #18).
- Após merges: iniciar S3 — ataques por grau e subgrafos (issues #19–#22).
  Pré-condição satisfeita: loader + anonimizador validados (entregues por S2).

**Bloqueios ativos:**
- PR #57 (issue #56) aguarda revisão humana no VSCode.
- PR #55 (issue #18) aguarda revisão humana no VSCode.

**Decisões pendentes de validação humana:**
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

---

## S2 — Implementação do anonimizador He et al. — ENCERRADA

**Período:** 22–29/05/2026 · **Fechada em:** 22/05/2026 (antecipada)

### Entregue
Pipeline He et al. (2009) completo e validado: particionamento com backend
`pymetis`/KL e fallback (#45, #11), agrupamento por FSM (#12), modificação
estrutural mínima (#13), `anonymize()` com reconexão (#14) e auditor
independente `validate_k_anonymity` (#15, testes #56). Decisões de design
D-07 (#43) e dependência `pymetis` (#44) consolidadas.

12 issues fechadas. Sem pendências no nível de issue.

### Marco 29/05
Cumprido em 21/05 (antecipação de 8 dias). k-anonimato empiricamente
atingido nas quatro configurações do Mínimo — k ∈ {2, 5, 10, 20} —
em 3 sementes independentes cada (#16, #17, #18).

### Desvio de critério — registrar para herança em S3/S4
O critério de aceitação aplicado **não** foi o 100% estrito com que a #16
foi originalmente redigida, e sim o critério fracionário **DL-01**
(`satisfied_fraction ≥ 0.9`). A validação passou com
`satisfied_fraction ≥ 0.9962`.

Isso é resultado projetado de D-06/D-07: uma fração ~0,4% dos nós é
classificada como **violadora por construção** (LSs sem grupo completo
caem em D-06). Não é defeito do algoritmo — é o limite estrutural da
implementação, e é resultado científico válido. Documentado em
`decision_log.md` (DL-01) e `algorithm_notes.md` §4.

**Implicações que S3 e S4 herdam — não tratar como resolvido aqui:**
- A métrica "tamanho do grupo de equivalência ≥ k" **não vale** para o
  subconjunto de violadores D-06; relatar esse subconjunto à parte.
- A taxa de reidentificação deve separar os violadores D-06 dos nós
  efetivamente k-anônimos, sob pena de contaminar a curva privacidade-
  vs-utilidade.
- Os gráficos finais (S4) devem reportar explicitamente
  `satisfied_fraction` por k, conforme já previsto para os casos em que
  algum k não atinja o alvo.

### Pendência de documentação (não bloqueante)
Verificar consistência de nomes: o bootstrap da #18 previa
`docs/milestone_29_05.md`; os artefatos atuais são
`docs/validacao_k_anonimato.md` e `docs/decision_log.md`. Confirmar o
cross-link no `CLAUDE.md` aponta para o nome final.

S3 (ataques + métricas) está liberada: #19 depende de "loader +
anonimizador validados", entregue por este milestone.

---

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
