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

**Atualizado em 22/05/2026.**

| Fase | Período | Status |
|---|---|---|
| S1: Setup + loader + leitura He et al. | 15–22/05 | ✅ Concluída |
| S2: Implementação He et al. + validação k-anonimato | 22–29/05 | ✅ Concluída com adiantamento (marco 29/05 cumprido em 21/05) |
| S3: Ataques + métricas + experimento baseline | 29/05–05/06 | 🔄 Em andamento |
| S4: Gráficos, tabelas e documentação técnica | 05–12/06 | ⏳ Pendente |
| S5: Polimento, reprodutibilidade e entrega | 12–14/06 | ⏳ Pendente |

**Marco intermediário não-negociável cumprido:** 21/05/2026 (antecipado em 8 dias). k-anonimato empiricamente atingido em todas as configurações do Mínimo (k ∈ {2, 5, 10, 20}) com `satisfied_fraction ≥ 0.9962` — critério DL-01 aprovado. Ver `docs/milestone_29_05.md` e `docs/decision_log.md`.

### Componentes implementados

- `src/anonymization/he2009.py` — pipeline completo: `partition_graph`, `_group_local_structures` (FSM+MF), `_modify_structure`, `_reconnect_inter_edges`, `anonymize(g, k, d, seed)`.
- `src/anonymization/validation.py` — auditor independente `validate_k_anonymity(groups, k) → dict` (36 testes unitários).
- `src/loaders/` — loader Facebook Ego-Nets (SNAP).
- `experiments/run_milestone_29_05.py` — script de validação do marco (k=5, egonet_id=3437, n=532, m=4812).
- `experiments/run_k_sweep.py` — k-sweep k ∈ {2, 5, 10, 20}; todos aprovados pelo critério DL-01.
- `docs/decision_log.md` — registro de decisões técnicas (DL-01, D-05, D-06, D-07).
- `docs/progress.md` — log de progresso sessão a sessão.
- CI: GitHub Actions + pre-commit (ruff 0.15.13).

### Próximos componentes (S3)

- `src/attacks/degree.py` — ataque por grau (issue #19)
- `src/attacks/subgraph.py` — ataque por subgrafos via VF2 (issue #20)
- `src/metrics/` — 4 métricas: reidentification_rate, equivalence_group_size, ks_test_degree, clustering_variation (issue #21)
- `experiments/run.py` — runner orquestrador CLI (issue #22)
- Experimento baseline Facebook Ego-Nets: 4k × 2 ataques × 3 sementes (issue #23)

## Entregáveis

Três níveis, com linha firme entre **Mínimo** e **Desejável**.

- **Mínimo defensável.** Pipeline funcional sobre Facebook Ego-Nets aplicando He et al. (2009) com `k ∈ {2, 5, 10, 20}`; ataques por grau e por subgrafos; quatro métricas; mínimo de 3 sementes por configuração; gráfico privacidade-vs-utilidade com barras de erro; repositório versionado com README operacional e arquivo de configuração reproduzível.
- **Desejável.** Execução adicional sobre Email-Enron; ataque por entropia.
- **Aspiracional.** Implementação inicial de Nettleton & Salas (2016) sobre Facebook Ego-Nets; comparação preliminar das duas anonimizações no mesmo gráfico.

O Mínimo é entregável defensável em si; o Desejável é entregável discutível; o Aspiracional é bônus que não deve ser perseguido em detrimento da consolidação do Mínimo.

## Reprodutibilidade

- Sementes aleatórias fixadas e versionadas em arquivo de configuração único (YAML).
- Mínimo de 3 execuções independentes por configuração `(k, dataset, ataque)` para barras de erro.
- Outputs (gráficos, tabelas) gerados a partir de logs JSONL estruturados em `experiments/logs/`, não de execução interativa.
- Datasets baixados por script versionado; **não** comitados no repositório.

## Estrutura do repositório

```
/data/
  /raw/                  # datasets originais (não versionados; baixados por script)
  /processed/            # datasets após pré-processamento
/src/
  /anonymization/        # He et al. (2009) [implementado]; placeholder Nettleton & Salas (2016)
  /attacks/              # ataques por grau, subgrafos, entropia
  /metrics/              # cálculo das quatro métricas
  /loaders/              # carregadores de dataset
  /visualization/        # gráficos privacy-vs-utility
/experiments/
  /configs/              # arquivos de configuração (YAML)
  /logs/                 # logs estruturados JSONL das execuções
/results/
  /tables/               # tabelas em CSV
  /plots/                # gráficos em PDF/PNG
/docs/
  algorithm_notes.md     # notas sobre implementação de He et al. (inclui Seção 9: k-sweep)
  metrics_definitions.md # definições operacionais das métricas
  decision_log.md        # registro formal de decisões técnicas (DL-01, D-05, D-06, D-07)
  progress.md            # log de progresso por sessão
  milestone_29_05.md     # resultado do marco 29/05 (cumprido em 21/05)
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

- He, X. et al. (2009). Preserving privacy in social networks: A structure-aware approach. *Proceedings of the IEEE/WIC/ACM International Joint Conference on Web Intelligence and Intelligent Agent Technology (WI-IAT)*.
- Nettleton, D. F. & Salas, J. (2016). A data driven anonymization system for information rich online social network graphs. *Expert Systems with Applications*, 55, 87–105.
- Documentação interna do projeto: v19 do artigo decisório (especialmente Seções 4.3 e 7); proposta original da tese.

---

*Repositório associado à tese de doutorado em geração de redes sociais sintéticas — PPGInf/UFPR.*
