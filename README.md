# Baseline de Reidentificação em Redes Sociais Anonimizadas

> Instrumento empírico para medir a resistência efetiva de anonimizações estruturais de redes sociais a ataques de reidentificação. Componente preparatório de tese de doutorado em geração de redes sociais sintéticas — PPGInf/UFPR.

## Posicionamento

Este repositório implementa o pipeline `anonimização → ataque → métrica` sobre redes sociais reais, produzindo uma **curva privacidade-vs-utilidade** por parâmetro de anonimização. O objetivo não é propor um novo mecanismo de privacidade, mas fornecer um aferidor que orientará a deliberação metodológica futura sobre o mecanismo de privacidade do framework integrado da tese (Decisão 4.3 do artigo decisório v19*).

A unidade de progresso é o **gráfico defensável**, não o texto argumentativo.

*Documentação formal da tese e outros artefatos produzidos no escopo acadêmico não serão publicizados aqui em princípio, considerando potencial vazamento.

## Escopo

| Eixo | Decisão | Justificativa breve |
|---|---|---|
| Temporal | Estático | Replicação direta de He et al. (2009); extensão temporal é Fase 2. |
| Dataset principal | Facebook Ego-Nets (SNAP) | Validação alinhada com a literatura contemporânea de privacidade. |
| Dataset secundário | Email-Enron (SNAP), contingente | Amplia a base de comparação se houver folga no cronograma. |
| Anonimização primária | He et al. (2009) | Algoritmo mais simples e mais bem documentado; ponto de entrada limpo. |
| Anonimização aspiracional | Nettleton & Salas (2016) | Inclui atributos e t-closeness; condicionada à estabilização do pipeline. |
| Ataques | Grau → Subgrafos → Entropia | Ordem de complexidade crescente; os dois primeiros são compromisso mínimo. |

### Parâmetro principal

`k ∈ {2, 5, 10, 20}` — da anonimização fraca (k=2) à forte (k=20).

### Métricas

**Privacidade**
- Taxa de reidentificação por ataque (proporção de nós-alvo corretamente identificados).
- Tamanho médio dos grupos de equivalência produzidos pela anonimização.

**Utilidade**
- KS-test (estatística D) sobre a distribuição de grau (original vs. anonimizado).
- Variação relativa do coeficiente de clustering médio.

## Status

**Atualizado em 26/05/2026.**

| Fase | Período | Status |
|---|---|---|
| S1: Setup + loader + leitura He et al. | 15–22/05 | ✅ Concluída |
| S2: Implementação He et al. + validação k-anonimato | 22–29/05 | ✅ Concluída com adiantamento (marco 29/05 cumprido em 21/05) |
| S3: Ataques + métricas + experimento baseline | 29/05–05/06 | ✅ Concluída com adiantamento (todos os ataques, métricas, runner e baseline produzidos em 22-23/05) |
| S4: Gráficos, tabelas e documentação técnica | 05–12/06 | ✅ Concluída com adiantamento (gráficos, tabelas CSV e docs/pipeline.md produzidos em 25/05) |
| S5: Polimento, reprodutibilidade e entrega | 12–14/06 | 🔄 Em andamento |

**Marco intermediário não-negociável cumprido:** 21/05/2026 (antecipado em 8 dias). k-anonimato empiricamente atingido em todas as configurações do Mínimo (k ∈ {2, 5, 10, 20}) com `satisfied_fraction ≥ 0.9962` — critério DL-01 aprovado. Ver `docs/validacao_k_anonimato.md` e `docs/decision_log.md`.

### Componentes implementados

**S1–S2 (anonimização e validação)**
- `src/anonymization/he2009.py` — pipeline completo: `partition_graph`, `_group_local_structures` (FSM+MF), `_modify_structure`, `_reconnect_inter_edges`, `anonymize(g, k, d, seed)`. Backend de particionamento em `src/anonymization/_partition_backend.py`.
- `src/anonymization/validation.py` — auditor independente `validate_k_anonymity(groups, k) → dict` (36 testes unitários). Campos DL-01: `coverage_fraction`, `uncovered_fraction`, `deficit_fully_structural`.
- `src/loaders/facebook_ego.py` — loader Facebook Ego-Nets (SNAP).
- `src/loaders/download.py` — script versionado para download automático dos datasets.
- `experiments/run_validacao_k_anonimato.py` — script de validação do k-anonimato (marco 21/05; k=5, egonet_id=3437, n=532, m=4812).
- `experiments/run_k_sweep.py` — k-sweep k ∈ {2, 5, 10, 20}; todos aprovados pelo critério DL-01.
- `docs/decision_log.md` — registro de decisões técnicas (DL-01, D-05, D-06, D-07).
- `docs/progress.md` — log de progresso sessão a sessão.
- CI: GitHub Actions + pre-commit (ruff v0.15.13).

**S3 (ataques, métricas e experimento baseline)**
- `src/attacks/degree.py` — ataque por grau (`degree_attack(g_orig, g_anon, target, tolerance=0) → bool`).
- `src/attacks/subgraph.py` — ataque por subgrafos via VF2 (`subgraph_attack(g_orig, g_anon, target, hop=1, timeout=None) → bool`).
- `src/metrics/` — 4 métricas: `reidentification_rate`, `equivalence_group_size`, `ks_test_degree`, `clustering_variation`.
- `experiments/run.py` — runner orquestrador CLI (`python -m experiments.run --config <yaml>`).
- `experiments/configs/he2009_facebook_baseline.yml` — config do experimento baseline.
- `docs/results_baseline.md` — tabela bruta e agregações do experimento baseline.

**S4 (visualização e documentação técnica)**
- `src/visualization/privacy_utility.py` — gráfico privacidade-vs-utilidade (2 painéis, barras de erro), saída PDF+PNG em `results/plots/`.
- `src/visualization/tables.py` — geração de tabelas CSV por `(dataset, ataque)` em `results/tables/`.
- `docs/pipeline.md` — documentação técnica do pipeline com diagramas Mermaid, comandos reproduzíveis e lista de outputs.
- `docs/limitations.md` — limitações metodológicas documentadas.
- `docs/reproducibility.md` — protocolo de reprodutibilidade end-to-end.
- `docs/preprocessing_decision.md` — decisões de pré-processamento dos datasets.
- `docs/algorithm_notes.md` e `docs/metrics_definitions.md` — revisados e cross-referenciados.

## Resultados do experimento baseline

**Dataset:** Facebook Ego-Net 3437 (n=532, m=4812) — `k ∈ {2, 5, 10, 20}`, 3 sementes (42, 1337, 2718).

| k | Veredito | coverage_fraction | rr_grau (média) | rr_subgrafo (média) | KS-D (média) |
|---|----------|-------------------|-----------------|---------------------|---------------|
| 2 | SUCCESS_FULL | 1.0000 | 0.0263 | 0.7914 | 0.0000 |
| 5 | SUCCESS_PARTIAL | 0.9962 | 0.0081 | 0.4060 | 0.0482 |
| 10 | SUCCESS_PARTIAL | 0.9962 | 0.0226 | 0.1397 | 0.2356 |
| 20 | SUCCESS_PARTIAL | 0.9774 | 0.0990 | 0.0000 | 0.6491 |

Gráficos finais em `results/plots/`; tabelas em `results/tables/` (não versionados; gerados localmente). Ver `docs/results_baseline.md` para análise completa.

## Entregáveis

Três níveis, com linha firme entre **Mínimo** e **Desejável**. Ver `docs/entregaveis.md` para status consolidado.

- **Mínimo defensável.** Pipeline funcional sobre Facebook Ego-Nets aplicando He et al. (2009) com `k ∈ {2, 5, 10, 20}`; ataques por grau e por subgrafos; quatro métricas; mínimo de 3 sementes por configuração; gráfico privacidade-vs-utilidade com barras de erro; repositório versionado com README operacional e arquivo de configuração reproduzível.
- **Desejável.** Execução adicional sobre Email-Enron; ataque por entropia.
- **Aspiracional.** Implementação inicial de Nettleton & Salas (2016) sobre Facebook Ego-Nets; comparação preliminar das duas anonimizações no mesmo gráfico.

O Mínimo é entregável defensável em si; o Desejável é entregável discutível; o Aspiracional é bônus que não deve ser perseguido em detrimento da consolidação do Mínimo.

## Reprodutibilidade

- Sementes aleatórias fixadas e versionadas em arquivo de configuração único (YAML).
- Mínimo de 3 execuções independentes por configuração `(k, dataset, ataque)` para barras de erro.
- Outputs (gráficos, tabelas) gerados a partir de logs JSONL estruturados em `experiments/logs/`, não de execução interativa.
- Datasets baixados por script versionado; **não** comitados no repositório.
- Reprodutibilidade end-to-end validada (#27): clone limpo → `pip install` → execução → outputs verificados.

## Estrutura do repositório

```
/data/
  /raw/                  # datasets originais (não versionados; baixados por script)
  /processed/            # datasets após pré-processamento
/src/
  /anonymization/        # He et al. (2009) [implementado]; placeholder Nettleton & Salas (2016)
  /attacks/              # ataques por grau, subgrafos, entropia
  /metrics/              # cálculo das quatro métricas
  /loaders/              # carregadores de dataset e script de download
  /visualization/        # gráficos privacy-vs-utility
/experiments/
  /configs/              # arquivos de configuração (YAML)
  /logs/                 # logs estruturados JSONL das execuções
/results/
  /tables/               # tabelas em CSV
  /plots/                # gráficos em PDF/PNG
/scripts/                # scripts auxiliares de setup/download
/docs/
  algorithm_notes.md     # notas sobre implementação de He et al. (inclui Seção 9: k-sweep)
  metrics_definitions.md # definições operacionais das métricas
  decision_log.md        # registro formal de decisões técnicas (DL-01, D-05, D-06, D-07)
  progress.md            # log de progresso por sessão
  validacao_k_anonimato.md # resultados consolidados da validação empírica (k ∈ {2,5,10,20})
  results_baseline.md    # tabela bruta + agregações do experimento baseline
  pipeline.md            # documentação técnica do pipeline com diagramas Mermaid
  limitations.md         # limitações metodológicas do protótipo
  reproducibility.md     # protocolo de reprodutibilidade end-to-end
  preprocessing_decision.md # decisões de pré-processamento dos datasets
  entregaveis.md         # lista consolidada de entregáveis por nível (Mínimo/Desejável/Aspiracional)
requirements.txt
requirements-dev.txt
config_example.yml
CLAUDE.md
WORKFLOW.md
```

A organização foi pensada para permitir migração futura para `SyntheticUForgePR` sem refatoração estrutural significativa.

## Premissas

- **Linguagem.** Python. NetworkX como padrão da área; alternativas (igraph, graph-tool) são aceitáveis mas exigem justificativa.
- **Hardware.** Razoável; sem requisito de GPU.
- **Datasets.** Disponíveis publicamente via SNAP; uso dentro das condições de licença e propósito acadêmico.

## O que este módulo não faz

- Não decide o mecanismo de privacidade do framework integrado da tese.
- Não estende a anonimização para contexto temporal.
- Não implementa o gerador (EpiCNet + Nettleton).
- Não substitui a deliberação metodológica da Decisão 4.3 do v19; produz medições que orientarão essa deliberação.
- Não pretende contribuição original de pesquisa em privacidade — é instrumento de validação que viabilizará a contribuição posterior da tese.

## Referências

- He, X., Vaidya, J., Shafiq, B., Adam, N., & Atluri, V. (2009). Preserving privacy in social networks: A structure-aware approach. *2009 IEEE/WIC/ACM International Joint Conference on Web Intelligence and Intelligent Agent Technology (WI-IAT)*, pp. 647–654. https://doi.org/10.1109/WI-IAT.2009.108
- Nettleton, D. F. & Salas, J. (2016). A data driven anonymization system for information rich online social network graphs. *Expert Systems with Applications*, 55, 87–105. https://doi.org/10.1016/j.eswa.2016.02.004
- Documentação interna do projeto: v19 do artigo decisório (especialmente Seções 4.3 e 7); proposta original da tese.

---

*Repositório associado à tese de doutorado em geração de redes sociais sintéticas — PPGInf/UFPR.*
