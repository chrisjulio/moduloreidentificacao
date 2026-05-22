# Validação de k-Anonimato Estrutural — Resultados Consolidados

> Registro consolidado da validação empírica de k-anonimato estrutural
> (He et al., 2009) sobre o Facebook Ego-Nets, k ∈ {2, 5, 10, 20}.
> Critérios de aceite: issue #16, decisão DL-01 ([docs/decision_log.md](decision_log.md)).
> Detalhamento técnico: [docs/algorithm_notes.md](algorithm_notes.md) §§ 8–9.

---

## 1. Identificação

| Campo              | Valor                                                              |
|--------------------|--------------------------------------------------------------------|
| Data de execução   | 2026-05-21 (k=5) e 2026-05-22 (k=2, k=10, k=20)                  |
| Repositório        | `chrisjulio/moduloreidentificacao`                                 |
| Commit marco (k=5) | `88b5c7fa` — Merge pull request #53 from chrisjulio/validation/milestone-29-05 |
| Commit k-sweep     | `1384792` — Merge pull request #54 from chrisjulio/validation/k-sweep          |
| HEAD atual         | `b126497` — docs: atualiza README com status real do projeto (22/05/2026)       |
| Script k=5         | `experiments/run_milestone_29_05.py`                               |
| Script k-sweep     | `experiments/run_k_sweep.py`                                       |

---

## 2. Configuração do experimento

| Parâmetro          | Valor                              |
|--------------------|------------------------------------|
| Dataset            | Facebook Ego-Nets (SNAP), ego-rede 3437 |
| n (LCC)            | 532 nós                            |
| m (LCC)            | 4 812 arestas                      |
| Algoritmo          | He et al. (2009) — `he_2009`       |
| d                  | 1                                  |
| σ (sigma)          | 0.5                                |
| Sementes           | [42, 1337, 2718]                   |
| k testados         | 2, 5, 10, 20                       |

---

## 3. Resultados

### 3.1 Tabela consolidada

| k  | Sementes       | Veredictos         | satisfied_fraction mín. | Observação            | Status           |
|----|----------------|--------------------|-------------------------|-----------------------|------------------|
| 2  | 42, 1337, 2718 | SUCCESS_FULL × 3   | 1.0000                  | 266 grupos exatos     | **APROVADO** (pleno) |
| 5  | 42, 1337, 2718 | SUCCESS_PARTIAL × 3 | 0.9962                 | 1 grupo incompleto (D-06) | **APROVADO** (D-06) |
| 10 | 42, 1337, 2718 | SUCCESS_PARTIAL × 3 | 0.9962                 | 2 nós residuais (D-06)    | **APROVADO** (D-06) |
| 20 | 42, 1337, 2718 | SUCCESS_PARTIAL × 3 | 0.9774                 | 12 nós residuais (D-06)   | **APROVADO** (D-06) |

### 3.2 Detalhamento por k

**k=2 — Sucesso pleno (SUCCESS_FULL):**
532 nós → 266 grupos de tamanho exato k=2. O algoritmo satisfaz a garantia formal
sem ressalvas; `valid=True` e `satisfied_fraction=1.0000` nas 3 sementes.

**k=5 — Configuração obrigatória do marco 29/05 (SUCCESS_PARTIAL / D-06):**
532 nós → 106 grupos completos + 1 grupo incompleto (2 nós residuais).
`satisfied_fraction = 530/532 ≈ 0.9962`, acima do limiar 0.9 do critério DL-01.
Único tipo de violação: `incomplete_group` (aceitável sob D-06).

**k=10 — Sucesso parcial aceitável (D-06):**
532 nós → 53 grupos completos + 1 grupo incompleto (2 nós residuais).
`satisfied_fraction = 530/532 ≈ 0.9962`, acima do limiar 0.9. Resultado
determinístico nas 3 sementes.

**k=20 — Sucesso parcial aceitável (D-06):**
532 nós → 26 grupos completos + 1 grupo incompleto (12 nós residuais).
`satisfied_fraction = 520/532 ≈ 0.9774`, acima do limiar 0.9. A fração de
nós residuais cresce linearmente com k, mas permanece dentro dos limites
aceitáveis para k ≤ 20 neste dataset.

---

## 4. Violações observadas

| Tipo de violação  | Encontrada? | k afetados | Ação sob DL-01 |
|-------------------|-------------|------------|----------------|
| `non_isomorphic`  | Não         | —          | Seria falha imediata |
| `non_disjoint`    | Não         | —          | Seria falha imediata |
| `incomplete_group`| Sim         | 5, 10, 20  | Aceitável sob D-06 (satisfied_fraction ≥ 0.9) |

---

## 5. Decisão

**Marco 29/05/2026: APROVADO.**

Todos os k do escopo Mínimo (k ∈ {2, 5, 10, 20}) produziram resultados dentro
do critério de aceite DL-01 nas 3 sementes obrigatórias, sobre a ego-rede 3437
do Facebook Ego-Nets. Nenhuma violação crítica (`non_isomorphic`, `non_disjoint`)
foi observada. Grupos incompletos (D-06) ocorrem em k ≥ 5 mas ficam abaixo
do limite de 10% de nós residuais.

**Decisão operacional:** prosseguir conforme planejado — Semana 3 (ataques por
grau e subgrafos, issues #19–#22).

Não é necessário acionar a reformulação de escopo prevista no Plano Operacional,
Seção 7.

---

## 6. Rastreabilidade

| Artefato                  | Referência                                     |
|---------------------------|------------------------------------------------|
| Critério de aceite        | issue #16, DL-01 em `docs/decision_log.md`     |
| Implementação validador   | `src/metrics/k_anonymity_verifier.py` (issue #15) |
| Config marco k=5          | `experiments/configs/milestone_29_05.yml`      |
| Config k-sweep k=2        | `experiments/configs/he2009_facebook_k_sweep_k2.yml`  |
| Config k-sweep k=10       | `experiments/configs/he2009_facebook_k_sweep_k10.yml` |
| Config k-sweep k=20       | `experiments/configs/he2009_facebook_k_sweep_k20.yml` |
| Detalhamento técnico      | `docs/algorithm_notes.md` §§ 8–9              |
| PR marco (k=5)            | PR #53                                         |
| PR k-sweep (k=2,10,20)    | PR #54                                         |
| Issue de documentação     | issue #18                                      |
