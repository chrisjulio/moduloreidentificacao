# Milestones — Módulo de Reidentificação

**Repositório:** [chrisjulio/moduloreidentificacao](https://github.com/chrisjulio/moduloreidentificacao)
**Atualizado em:** 2026-06-02 (18h43)

---

## S1 — Fundação (ENCERRADO ✅)

| # | Título resumido | Status |
|---|---|---|
| [#4](https://github.com/chrisjulio/moduloreidentificacao/issues/4) | Script de download Facebook Ego-Nets (SNAP) | ✅ |
| [#5](https://github.com/chrisjulio/moduloreidentificacao/issues/5) | Loader `load_facebook_egonet(egonet_id, data_dir)` | ✅ |
| [#6](https://github.com/chrisjulio/moduloreidentificacao/issues/6) | Teste do loader Facebook Ego-Net | ✅ |
| [#7](https://github.com/chrisjulio/moduloreidentificacao/issues/7) | Decidir modo de pré-processamento das ego-redes | ✅ |
| [#8](https://github.com/chrisjulio/moduloreidentificacao/issues/8) | Leitura He et al. (2009) — Seção 1 | ✅ |
| [#9](https://github.com/chrisjulio/moduloreidentificacao/issues/9) | Leitura He et al. (2009) — Seção 2 | ✅ |
| [#10](https://github.com/chrisjulio/moduloreidentificacao/issues/10) | Leitura He et al. (2009) — Seções 3–4 | ✅ |
| [#32](https://github.com/chrisjulio/moduloreidentificacao/issues/32) | Setup local: ambiente Python e dependências | ✅ |
| [#33](https://github.com/chrisjulio/moduloreidentificacao/issues/33) | Esboço da API do anonimizador (skeleton) | ✅ |
| [#34](https://github.com/chrisjulio/moduloreidentificacao/issues/34) | Definir `metrics_definitions.md` §k-anonymity-verifier | ✅ |
| [#40](https://github.com/chrisjulio/moduloreidentificacao/issues/40) | Medir ego-redes e selecionar `egonet_id` mediano | ✅ |

---

## S2 — Implementação do anonimizador He et al. (ENCERRADO ✅)

| # | Título resumido | Status |
|---|---|---|
| [#43](https://github.com/chrisjulio/moduloreidentificacao/issues/43) | D-07: política de normalização de tamanho de LSs | ✅ |
| [#44](https://github.com/chrisjulio/moduloreidentificacao/issues/44) | Adicionar `pymetis` ao `requirements.txt` e validar CI | ✅ |
| [#45](https://github.com/chrisjulio/moduloreidentificacao/issues/45) | `src/anonymization/_partition_backend.py` | ✅ |
| [#11](https://github.com/chrisjulio/moduloreidentificacao/issues/11) | `_partition_neighborhoods(G, d)` | ✅ |
| [#12](https://github.com/chrisjulio/moduloreidentificacao/issues/12) | `_group_isomorphic` (FSM + fator MF) | ✅ |
| [#13](https://github.com/chrisjulio/moduloreidentificacao/issues/13) | `_modify_structure(groups, seed, add_only)` | ✅ |
| [#14](https://github.com/chrisjulio/moduloreidentificacao/issues/14) | `anonymize(G, k, d, seed)` — pipeline completo | ✅ |
| [#15](https://github.com/chrisjulio/moduloreidentificacao/issues/15) | `validate_k_anonymity` — auditor independente | ✅ |
| [#56](https://github.com/chrisjulio/moduloreidentificacao/issues/56) | Testes `validate_k_anonymity`: campos DL-01 | ✅ |
| [#16](https://github.com/chrisjulio/moduloreidentificacao/issues/16) | **MARCO 29/05** — Sanidade k=5, d=1 sobre ego-rede Facebook | ✅ |
| [#17](https://github.com/chrisjulio/moduloreidentificacao/issues/17) | Testes de sanidade adicionais: k=2, k=10, k=20 | ✅ |
| [#18](https://github.com/chrisjulio/moduloreidentificacao/issues/18) | Documentar resultado do marco 29/05 | ✅ |

---

## S3 — Ataques e métricas (ENCERRADO ✅)

| # | Título resumido | Status |
|---|---|---|
| [#19](https://github.com/chrisjulio/moduloreidentificacao/issues/19) | `src/attacks/degree.py` | ✅ |
| [#20](https://github.com/chrisjulio/moduloreidentificacao/issues/20) | `src/attacks/subgraph.py` (VF2) | ✅ |
| [#21](https://github.com/chrisjulio/moduloreidentificacao/issues/21) | `src/metrics/` (4 métricas) | ✅ |
| [#22](https://github.com/chrisjulio/moduloreidentificacao/issues/22) | `experiments/run.py` (runner CLI) | ✅ |
| [#23](https://github.com/chrisjulio/moduloreidentificacao/issues/23) | Execução: experimento baseline Facebook Ego-Nets | ✅ |

---

## S4 — Visualização e documentação técnica (ENCERRADO ✅)

| # | Título resumido | Status |
|---|---|---|
| [#24](https://github.com/chrisjulio/moduloreidentificacao/issues/24) | Gráfico privacy-vs-utility | ✅ |
| [#25](https://github.com/chrisjulio/moduloreidentificacao/issues/25) | Tabelas CSV de resultados | ✅ |
| [#26](https://github.com/chrisjulio/moduloreidentificacao/issues/26) | Documentação técnica final do pipeline | ✅ |
| [#63](https://github.com/chrisjulio/moduloreidentificacao/issues/63) | [#26-A] Revisão documental acadêmica | ✅ |
| [#64](https://github.com/chrisjulio/moduloreidentificacao/issues/64) | [#26-B] Produção técnica codificada | ✅ |

---

## S5 — Validação final e entrega (ENCERRADO ✅)

| # | Título resumido | Status |
|---|---|---|
| [#27](https://github.com/chrisjulio/moduloreidentificacao/issues/27) | Reprodutibilidade end-to-end (do zero) | ✅ Fechada (26/05) |
| [#28](https://github.com/chrisjulio/moduloreidentificacao/issues/28) | README final + revisão da documentação | ✅ Fechada (26/05) |

---

## 🌟 Escopo Mínimo: COMPLETO ✅

Todas as 35 issues do escopo mínimo (S1 a S5) foram fechadas em 2026-05-26.

---

## D-08 — Varredura d>1: k-anonimato structure-aware pleno (ENCERRADO ✅ — 02/06)

Todas as 7 fases concluídas. `docs/results_dsweep.md` publicado com matriz `d×k`. `limitations.md §1.3` marcada como parcialmente resolvida.

| # | Fase | Entregável principal | Status |
|---|---|---|---|
| [#72](https://github.com/chrisjulio/moduloreidentificacao/issues/72) | Issue-mãe D-08 | Critério de conclusão + índice | ✅ Fechada |
| [#73](https://github.com/chrisjulio/moduloreidentificacao/issues/73) | Fase 0 — Enquadramento | D-08 em `decision_log.md`, `scope.md`, `progress.md`, branch | ✅ Fechada |
| [#74](https://github.com/chrisjulio/moduloreidentificacao/issues/74) | Fase 1 — Auditoria | `pytest d>1`, inventário do núcleo | ✅ Fechada |
| [#75](https://github.com/chrisjulio/moduloreidentificacao/issues/75) | Fase 2 — Núcleo | Integração end-to-end `d∈{2,5}`; decisões FSM/conectividade | ✅ Fechada |
| [#76](https://github.com/chrisjulio/moduloreidentificacao/issues/76) | Fase 3 — Validador | `deficit_fully_structural` e métricas em `d>1`; pré-filtro VF2 | ✅ Fechada |
| [#77](https://github.com/chrisjulio/moduloreidentificacao/issues/77) | Fase 4 — Execução | `he2009_facebook_dsweep.yml`; 48 runs | ✅ Fechada |
| [#78](https://github.com/chrisjulio/moduloreidentificacao/issues/78) | Fase 5 — Análise | `results_dsweep.md`; matriz `d×k`; docs atualizados | ✅ Fechada |
| [#80](https://github.com/chrisjulio/moduloreidentificacao/issues/80) | Fase 2-complementar | G1 (conectividade CI), G2 (LSs heterogêneas), G3 (fórmula `k(k-1)`), G5(a) (contadores) | ✅ Fechada |
| [#88](https://github.com/chrisjulio/moduloreidentificacao/issues/88) | Runner d-sweep | Estender runner para `d` como lista; executar varredura completa | ✅ Fechada |

---

## 🔍 Encaminhamentos pós-D-08

| # | Título | Status |
|---|---|---|
| [#99](https://github.com/chrisjulio/moduloreidentificacao/issues/99) | Encaminhamentos pós-conclusão D-08 — próximos passos do módulo | 🔴 Aberta (02/06) |

> Pendências em discussão: encerramento do milestone S7; `algorithm_notes.md §3.2.2` (fórmula `k(k−1)` como interpretativa ou confirmada); integração futura com EpiCNet.

---

## Escopos Desejável / Aspiracional remanescentes

| # | Rótulo | Principal tarefa | Status |
|---|---|---|---|
| [#29](https://github.com/chrisjulio/moduloreidentificacao/issues/29) | DESEJÁVEL | Loader Email-Enron como dataset secundário | 🔴 Aberta |
| [#30](https://github.com/chrisjulio/moduloreidentificacao/issues/30) | DESEJÁVEL | Ataque por entropia reutilizando grupos de equivalência | 🔴 Aberta |
| [#31](https://github.com/chrisjulio/moduloreidentificacao/issues/31) | ASPIRACIONAL | Implementação inicial de Nettleton & Salas (2016) | 🔴 Aberta |

---

*Documento gerado automaticamente a partir da API do GitHub em 2026-06-02.*
