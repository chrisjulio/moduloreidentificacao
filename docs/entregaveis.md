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
| Loader Email-Enron (SNAP) | `src/loaders/` (issue #29) | ⏳ Não iniciado |
| Config YAML para Enron | `experiments/configs/` (issue #29) | ⏳ Não iniciado |
| Execução baseline Email-Enron | — (issue #29) | ⏳ Não iniciado |
| Ataque por entropia | `src/attacks/entropy.py` (issue #30) | ⏳ Não iniciado |

> Não perseguidos: o Mínimo foi consolidado com adiantamento consideraável,
> mas o tempo disponível até 14/06 foi consumido pela profundidade do Mínimo.
> Ambos os itens são resultados científicos válidos para discussão futura.

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
