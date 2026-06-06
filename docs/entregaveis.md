# Entregáveis — Lista consolidada por nível

> Gerado na S5 (issue #28) para registro da entrega final de 14/06/2026.
> Atualizado em: 26/05/2026.

---

## Mínimo defensável

Condição: obrigatório para entrega acadêmica.

### Anonimização e validação

| Entregável | Arquivo/Componente | Status |
|---|---|---|
| Pipeline He et al. (2009) | `src/anonymization/he2009.py` | ✅ Implementado |
| Backend de particionamento (METIS + KL fallback) | `src/anonymization/_partition_backend.py` | ✅ Implementado |
| Auditor independente de k-anonimato | `src/anonymization/validation.py` | ✅ Implementado (36 testes) |
| Validação empírica k ∈ {2, 5, 10, 20} | `docs/validacao_k_anonimato.md` | ✅ Aprovado (DL-01) |

### Loader e pré-processamento

| Entregável | Arquivo/Componente | Status |
|---|---|---|
| Loader Facebook Ego-Nets (SNAP) | `src/loaders/` | ✅ Implementado |
| Pré-processamento (ego exclusão, LCC, grafo simples) | `src/loaders/facebook_ego.py` | ✅ Implementado |
| Script de download | `python -m src.loaders.download` | ✅ Implementado |

### Ataques

| Entregável | Arquivo/Componente | Status |
|---|---|---|
| Ataque por grau | `src/attacks/degree.py` | ✅ Implementado |
| Ataque por subgrafos (VF2, hop=1) | `src/attacks/subgraph.py` | ✅ Implementado |

### Métricas

| Entregável | Arquivo/Componente | Status |
|---|---|---|
| Taxa de reidentificação | `src/metrics/reidentification_rate.py` | ✅ Implementado |
| Tamanho médio dos grupos de equivalência | `src/metrics/equivalence_group_size.py` | ✅ Implementado |
| KS-test sobre distribuição de grau | `src/metrics/ks_test_degree.py` | ✅ Implementado |
| Variação do coeficiente de clustering | `src/metrics/clustering_variation.py` | ✅ Implementado |

### Experimento e visualização

| Entregável | Arquivo/Componente | Status |
|---|---|---|
| Runner orquestrador CLI | `experiments/run.py` | ✅ Implementado |
| Experimento baseline (4k × 2 ataques × 3 sementes) | `experiments/configs/he2009_facebook_baseline.yml` | ✅ Executado |
| Logs JSONL estruturados | `experiments/logs/he2009_facebook_baseline/` | ✅ Gerados |
| Gráfico privacidade-vs-utilidade (2 painéis, barras de erro) | `src/visualization/privacy_utility.py` | ✅ Implementado |
| Tabelas CSV por (dataset, ataque) | `src/visualization/tables.py` | ✅ Implementado |
| Arquivo de configuração reproduzível (exemplo) | `config_example.yml` | ✅ Presente |

### Documentação e infra

| Entregável | Arquivo/Componente | Status |
|---|---|---|
| README operacional | `README.md` | ✅ Atualizado (S5) |
| Notas algorítmicas | `docs/algorithm_notes.md` | ✅ Revisado (S3) |
| Definições de métricas | `docs/metrics_definitions.md` | ✅ Revisado (S3) |
| Log de decisões técnicas | `docs/decision_log.md` | ✅ Atualizado até DL-01 |
| Documentação do pipeline | `docs/pipeline.md` | ✅ Criado (S4) |
| Limitações metodológicas | `docs/limitations.md` | ✅ Criado (S4) |
| Resultados do baseline | `docs/results_baseline.md` | ✅ Criado (S3) |
| Reprodutibilidade end-to-end | `docs/reproducibility.md` | ✅ Criado (S5/#27) |
| CI (ruff + pytest) | `.github/workflows/` | ✅ Ativo |
| Pre-commit | `.pre-commit-config.yaml` | ✅ Ativo |

---

## Desejável

Condição: perseguir se houver folga após consolidação do Mínimo.

| Entregável | Arquivo/Componente | Status |
|---|---|---|
| Download Email-Enron (SNAP) | `src/loaders/download_enron.py` (issue #123, S9-1) | ✅ Implementado |
| Loader Email-Enron (direcionado→não-dir., OR) | `src/loaders/enron.py` (issue #124, S9-2) | ✅ Implementado |
| Integração runner (`enron` em `load_dataset`) | `experiments/run.py` (issue #125, S9-3) | ✅ Implementado |
| Config YAML para Enron | `experiments/configs/he2009_enron_secondary.yml` (issue #126, S9-4) | ✅ Implementado |
| Execução secundária Email-Enron (grau + subgrafo hop=1 full) | `experiments/logs/he2009_enron_secondary/` (issues #127/#139, S9-5) | ✅ Concluída |
| Comparativo Facebook vs. Enron + `results_enron.md` | `docs/results_enron.md` (issue #128, S9-6) | ✅ Implementado |
| Ataque por entropia | `src/attacks/entropy.py` (issue #30) | ⏳ Não iniciado |

> Atualização (S9, 06/06/2026): o tier Desejável teve o **dataset secundário
> Email-Enron integralmente concluído** — download, loader (simetrização OR/D-11),
> integração ao runner, config YAML, execução das 12 runs (grau + subgrafo hop=1
> *full* via bucketing de WL-hash/D-16, `subgraph_timeout_count=0`) e comparativo
> Facebook × Enron em `results_enron.md`. Milestone S9 fechado (9/9 issues
> #122–#129, #139); issue-mãe #29 encerrada. Decisões D-11 a D-16 e DL-04. O ataque
> por entropia (#30) permanece não iniciado — único item aberto do tier Desejável.

---

## Aspiracional

Condição: bônus — não perseguir em detrimento do Mínimo.

| Entregável | Arquivo/Componente | Status |
|---|---|---|
| Implementação Nettleton & Salas (2016) | `src/anonymization/nettleton_salas.py` (issue #31) | ⏳ Não iniciado |
| Comparação He et al. vs. Nettleton no mesmo gráfico | — (issue #31) | ⏳ Não iniciado |

> Não perseguidos: condição não atingida. Possível extensão na Fase 2 da tese.

---

## Resumo

| Nível | Total | Concluídos | Não iniciados |
|---|---|---|---|
| Mínimo | 27 | 27 | 0 |
| Desejável | 4 | 0 | 4 |
| Aspiracional | 2 | 0 | 2 |

**Conclusão:** Mínimo 100% concluído. Reprodutibilidade end-to-end validada (#27).
Repositório está em condições de entrega acadêmica.
