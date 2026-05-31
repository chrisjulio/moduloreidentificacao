# Milestones — Módulo de Reidentificação

**Repositório:** [chrisjulio/moduloreidentificacao](https://github.com/chrisjulio/moduloreidentificacao)
**Atualizado em:** 2026-05-31 (20h10)

---

## S1 — Fundação (ENCERRADO ✅)

Todas as 11 issues de S1 concluídas. Registradas para referência histórica.

| # | Título resumido | Status |
|---|---|---|
| [#4](https://github.com/chrisjulio/moduloreidentificacao/issues/4) | Script de download Facebook Ego-Nets (SNAP) | ✅ Fechada |
| [#5](https://github.com/chrisjulio/moduloreidentificacao/issues/5) | Loader `load_facebook_egonet(egonet_id, data_dir)` | ✅ Fechada |
| [#6](https://github.com/chrisjulio/moduloreidentificacao/issues/6) | Teste do loader Facebook Ego-Net | ✅ Fechada |
| [#7](https://github.com/chrisjulio/moduloreidentificacao/issues/7) | Decidir modo de pré-processamento das ego-redes | ✅ Fechada |
| [#8](https://github.com/chrisjulio/moduloreidentificacao/issues/8) | Leitura He et al. (2009) — Seção 1: k-anonimato estrutural | ✅ Fechada |
| [#9](https://github.com/chrisjulio/moduloreidentificacao/issues/9) | Leitura He et al. (2009) — Seção 2: algoritmo principal | ✅ Fechada |
| [#10](https://github.com/chrisjulio/moduloreidentificacao/issues/10) | Leitura He et al. (2009) — Seções 3–4: operações e parada | ✅ Fechada |
| [#32](https://github.com/chrisjulio/moduloreidentificacao/issues/32) | Setup local: ambiente Python e dependências | ✅ Fechada |
| [#33](https://github.com/chrisjulio/moduloreidentificacao/issues/33) | Esboço da API do anonimizador (skeleton sem implementação) | ✅ Fechada |
| [#34](https://github.com/chrisjulio/moduloreidentificacao/issues/34) | Definir `metrics_definitions.md` §k-anonymity-verifier | ✅ Fechada |
| [#40](https://github.com/chrisjulio/moduloreidentificacao/issues/40) | Medir ego-redes e selecionar `egonet_id` mediano | ✅ Fechada |

---

## S2 — Implementação do anonimizador He et al. (ENCERRADO ✅)

### Decisões de design

| # | Título resumido | Status |
|---|---|---|
| [#43](https://github.com/chrisjulio/moduloreidentificacao/issues/43) | D-07: política de normalização de tamanho de LSs (Opção A adotada) | ✅ Fechada |
| [#44](https://github.com/chrisjulio/moduloreidentificacao/issues/44) | Adicionar `pymetis` ao `requirements.txt` e validar CI | ✅ Fechada |

### Implementação

| # | Título resumido | Principal tarefa | Status |
|---|---|---|---|
| [#45](https://github.com/chrisjulio/moduloreidentificacao/issues/45) | `src/anonymization/_partition_backend.py` | Módulo de particionamento com backends `pymetis`/KL e fallback automático | ✅ Fechada |
| [#11](https://github.com/chrisjulio/moduloreidentificacao/issues/11) | `_partition_neighborhoods(G, d)` | Particionar grafo em Local Structures de tamanho `d` | ✅ Fechada |
| [#12](https://github.com/chrisjulio/moduloreidentificacao/issues/12) | `_group_isomorphic` (FSM + fator MF) | Agrupar Local Structures isomórficas via FSM | ✅ Fechada |
| [#13](https://github.com/chrisjulio/moduloreidentificacao/issues/13) | `_modify_structure(groups, seed, add_only)` | Modificar estruturalmente grupos para satisfazer cardinalidade mínima k | ✅ Fechada |
| [#14](https://github.com/chrisjulio/moduloreidentificacao/issues/14) | `anonymize(G, k, d, seed)` — pipeline completo | Orquestrar as 4 etapas incluindo reconexão | ✅ Fechada |
| [#15](https://github.com/chrisjulio/moduloreidentificacao/issues/15) | `validate_k_anonymity` — auditor independente | Verificador externo de k-anonimato com log de violações | ✅ Fechada |
| [#56](https://github.com/chrisjulio/moduloreidentificacao/issues/56) | Testes `validate_k_anonymity`: campos DL-01 | Cobertura de `coverage_fraction`, `uncovered_fraction`, `deficit_fully_structural` | ✅ Fechada |

### Marco e validação

| # | Título resumido | Status |
|---|---|---|
| [#16](https://github.com/chrisjulio/moduloreidentificacao/issues/16) | **MARCO 29/05** — Sanidade k=5, d=1 sobre ego-rede Facebook | ✅ Fechada |
| [#17](https://github.com/chrisjulio/moduloreidentificacao/issues/17) | Testes de sanidade adicionais: k=2, k=10, k=20 | ✅ Fechada |
| [#18](https://github.com/chrisjulio/moduloreidentificacao/issues/18) | Documentar resultado do marco 29/05 | ✅ Fechada |

---

## S3 — Ataques e métricas (ENCERRADO ✅)

| # | Título resumido | Status |
|---|---|---|
| [#19](https://github.com/chrisjulio/moduloreidentificacao/issues/19) | `src/attacks/degree.py` | ✅ Fechada |
| [#20](https://github.com/chrisjulio/moduloreidentificacao/issues/20) | `src/attacks/subgraph.py` (VF2) | ✅ Fechada |
| [#21](https://github.com/chrisjulio/moduloreidentificacao/issues/21) | `src/metrics/` (4 métricas) | ✅ Fechada |
| [#22](https://github.com/chrisjulio/moduloreidentificacao/issues/22) | `experiments/run.py` (runner CLI) | ✅ Fechada |
| [#23](https://github.com/chrisjulio/moduloreidentificacao/issues/23) | Execução: experimento baseline Facebook Ego-Nets | ✅ Fechada |

---

## S4 — Visualização e documentação técnica (ENCERRADO ✅)

| # | Título resumido | Status |
|---|---|---|
| [#24](https://github.com/chrisjulio/moduloreidentificacao/issues/24) | Gráfico privacy-vs-utility | ✅ Fechada |
| [#25](https://github.com/chrisjulio/moduloreidentificacao/issues/25) | Tabelas CSV de resultados | ✅ Fechada |
| [#26](https://github.com/chrisjulio/moduloreidentificacao/issues/26) | Documentação técnica final do pipeline | ✅ Fechada |
| [#63](https://github.com/chrisjulio/moduloreidentificacao/issues/63) | [#26-A] Revisão documental acadêmica do pipeline | ✅ Fechada |
| [#64](https://github.com/chrisjulio/moduloreidentificacao/issues/64) | [#26-B] Produção técnica codificada da documentação | ✅ Fechada |

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

## D-08 — Varredura d>1: k-anonimato structure-aware pleno (EM ANDAMENTO 🔄)

Extensão desejável que resolve `docs/limitations.md` §1.3. Branch de trabalho: `experiment/d-sweep`.

### Fases originais (#72–#78)

| # | Fase | Principal tarefa | Status |
|---|---|---|---|
| [#72](https://github.com/chrisjulio/moduloreidentificacao/issues/72) | Issue-mãe D-08 | Critério de conclusão geral + índice de fases | 🔴 Aberta |
| [#73](https://github.com/chrisjulio/moduloreidentificacao/issues/73) | Fase 0 — Enquadramento | D-08 em `decision_log.md`, `scope.md`, `progress.md`, branch | ✅ Fechada |
| [#74](https://github.com/chrisjulio/moduloreidentificacao/issues/74) | Fase 1 — Auditoria de prontidão | `pytest d>1`, inventário de testes do núcleo | ✅ Fechada |
| [#75](https://github.com/chrisjulio/moduloreidentificacao/issues/75) | Fase 2 — Endurecer núcleo | Integração end-to-end `d∈{2,5}`; decisões FSM/conectividade | ✅ Fechada |
| [#76](https://github.com/chrisjulio/moduloreidentificacao/issues/76) | Fase 3 — Validador e métricas | `deficit_fully_structural` e `equivalence_group_size` em `d>1`; pré-filtro VF2 | ✅ Fechada |
| [#77](https://github.com/chrisjulio/moduloreidentificacao/issues/77) | Fase 4 — Configuração e execução | `he2009_facebook_dsweep.yml`; 48 runs | 🔴 Aberta |
| [#78](https://github.com/chrisjulio/moduloreidentificacao/issues/78) | Fase 5 — Análise e documentação | `docs/results_dsweep.md`; visualizações com `d`; `limitations.md §1.3` resolvida | 🔴 Aberta |

### Issues complementares abertas em andamento

| # | Título resumido | Principal tarefa | Status |
|---|---|---|---|
| [#80](https://github.com/chrisjulio/moduloreidentificacao/issues/80) | [Fase 2 — Complementar] Pendências G1, G2, G3 e G5(a) | G3: fórmula `k(k-1)` em reconexão; G1: conectividade de LSs; G2: LSs heterogêneas em `_modify_structure`; G5(a): expor contadores em `anonymize()` | 🔴 Aberta |
| [#88](https://github.com/chrisjulio/moduloreidentificacao/issues/88) | [Fase 4 — Runner d-sweep] Estender runner para lista de `d` | Aceitar `d` como lista no YAML; criar `he2009_facebook_dsweep.yml`; executar 48 runs; `results_dsweep.md` | 🔴 Aberta |

> **Nota de sequência:** #80 (G5-a) é pré-requisito de #77 (G5-b — persistir contadores no JSONL). #88 incorpora e substitui parte do escopo da Fase 4 (#77) adicionando suporte a `d` como lista no runner.

---

## Outros Escopos Desejável / Aspiracional

| # | Rótulo | Principal tarefa | Status |
|---|---|---|---|
| [#29](https://github.com/chrisjulio/moduloreidentificacao/issues/29) | DESEJÁVEL | Loader Email-Enron como dataset secundário | 🔴 Aberta |
| [#30](https://github.com/chrisjulio/moduloreidentificacao/issues/30) | DESEJÁVEL | Ataque por entropia reutilizando grupos de equivalência | 🔴 Aberta |
| [#31](https://github.com/chrisjulio/moduloreidentificacao/issues/31) | ASPIRACIONAL | Implementação inicial de Nettleton & Salas (2016) | 🔴 Aberta |

---

*Documento gerado automaticamente a partir da API do GitHub em 2026-05-31.*
