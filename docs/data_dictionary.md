# Data Dictionary — Variáveis e Parâmetros

> Definições de todas as variáveis, colunas de tabelas e parâmetros de configuração
> usados no README, nos experimentos e nos arquivos YAML deste módulo.
>
> **Referências cruzadas:**
> - [`docs/metrics_definitions.md`](metrics_definitions.md) — definições operacionais formais das métricas.
> - [`docs/decision_log.md`](decision_log.md) — decisões técnicas citadas por código (D-xx, DL-xx).
> - [`docs/algorithm_notes.md`](algorithm_notes.md) — notas de implementação do algoritmo He et al.
> - [`docs/results_baseline.md`](results_baseline.md) — tabela bruta do baseline (`d=1`).
> - [`docs/results_dsweep.md`](results_dsweep.md) — matriz completa k×d do d-sweep.

---

## 1. Parâmetros experimentais (arquivos YAML)

| Variável | Onde aparece | Definição |
|---|---|---|
| `k` | YAML `anonymization.k`, tabelas de resultados | Parâmetro de k-anonimato estrutural (He et al., 2009). Define o tamanho mínimo dos grupos de equivalência: cada grupo deve conter pelo menos `k` estruturas locais (LSs) mutuamente isomorfas. Valores do baseline: `{2, 5, 10, 20}`. Quanto maior, mais forte a anonimização — e maior a distorção estrutural potencial. |
| `d` | YAML `anonymization.d`, cabeçalhos de seção | Tamanho máximo das estruturas locais (LSs) em número de nós. `d=1` = baseline (âncora); `d=5` = valor primário do d-sweep; `d=2` e `d=10` incluídos com anotação de degeneração (D-08, D-10). Controla o granulado da anonimização estrutural. |
| `sigma` | YAML `anonymization.sigma` | Suporte mínimo do minerador de subgrafos frequentes (FSM) simplificado, usado para enumerar padrões de LS. Valor adotado: `0.5` (decisão D-01). Intervalo: `(0, 1]`; valores menores ampliam o conjunto de padrões candidatos. |
| `seeds` | YAML `seeds` | Lista de sementes de aleatoriedade fixadas para reprodutibilidade. Padrão: `[42, 1337, 2718]`. Nunca hardcoded no código — sempre lidas do YAML. Garantem que resultados com a mesma configuração sejam idênticos entre execuções independentes. |
| `tolerance` | YAML `attacks.degree.tolerance` | Margem de tolerância do ataque por grau. `0` = correspondência exata de grau (baseline conservador). Valores positivos permitem associar nós com diferença de até `tolerance` no grau do nó. |
| `hop` | YAML `attacks.subgraph.hop` | Raio da vizinhança usada pelo ataque por subgrafo. `1` = vizinhança 1-hop (todos os nós a distância ≤ 1 do nó-alvo). Valores maiores aumentam a sofisticação do ataque e o custo computacional (VF2). |
| `timeout` | YAML `attacks.subgraph.timeout` | Tempo máximo em segundos por nó-alvo para o algoritmo de isomorfismo VF2 no ataque por subgrafo. `60 s` no baseline; `120 s` no d-sweep (grafos anonimizados tendem a ser mais densos com `d > 1`). Nós cujo VF2 atinge o limite são contabilizados como não-reidentificados — não como erro. |
| `egonet_id` | YAML `dataset.egonet_id` | Identificador numérico da ego-rede do Facebook Ego-Nets (SNAP) usada no experimento. `3437` = grafo com `n=532` nós e `m=4812` arestas na maior componente conexa (LCC). |
| `include_ego` | YAML `dataset.include_ego` | Booleano. `false` = nó ego (hub central da ego-rede) excluído antes do experimento (decisão de pré-processamento documentada em [`docs/preprocessing_decision.md`](preprocessing_decision.md) §3.1). |
| `component` | YAML `dataset.component` | Componente do grafo retida após carregamento. `lcc` = maior componente conexa. Garante que o grafo seja conexo, pré-condição dos algoritmos de particionamento. |
| `min_nodes` | YAML `dataset.min_nodes` | Número mínimo de nós exigido após pré-processamento. Calculado como `10 × k_max = 10 × 20 = 200`. Funciona como validação de sanidade do dataset antes da execução. |
| `allow_kl_fallback` | YAML `anonymization.allow_kl_fallback` | Booleano. `true` = o backend de particionamento pode recuar para Kernighan-Lin (NetworkX) se `pymetis` não estiver disponível (decisão D-04). `false` = exige `pymetis` obrigatoriamente (usado no d-sweep para garantir comparabilidade entre runs). Backends diferentes produzem partições — e portanto métricas — diferentes; controlar este campo é essencial para reprodutibilidade cruzada. |

---

## 2. Métricas de privacidade

| Variável | Coluna nas tabelas | Definição |
|---|---|---|
| `coverage_fraction` | `coverage_fraction` | Fração dos nós do grafo anonimizado `G'` alocados em grupos de equivalência com tamanho ≥ k. Alias de `satisfied_fraction`, introduzido em DL-01. `1.0` = cobertura total; valores < `1.0` indicam nós residuais do grupo incompleto final (D-06 — aceitável). Definição operacional completa em [`docs/metrics_definitions.md`](metrics_definitions.md) §k-anonymity-verifier. |
| `uncovered_fraction` | — (calculada) | Complemento de `coverage_fraction`: `1 − coverage_fraction`. Fração de nós não cobertos. Campo explícito nos logs para facilitar filtragem sem cálculo externo. |
| `reidentification_rate` (grau) | `rr_grau` | Taxa de reidentificação pelo ataque por grau: `N_correto / N_total`, onde `N_correto` é o número de nós-alvo corretamente associados ao seu rótulo interno usando apenas a assinatura de grau do nó (`degree_attack`, `tolerance=0`). Modelo adversarial mais fraco — linha de base para comparação. Quanto menor, maior a resistência ao ataque de grau. |
| `reidentification_rate` (subgrafo) | `rr_subgrafo` | Taxa de reidentificação pelo ataque por subgrafo: `N_correto / N_total`, onde a associação usa isomorfismo de vizinhança 1-hop (VF2). Modelo mais próximo do adversarial de He et al. (2009). Cota teórica esperada: `≤ 1/k` sob k-anonimato pleno. Quanto menor, maior a resistência. |
| `equivalence_group_size` (mean) | — (logs) | Média do tamanho dos grupos de equivalência em número de nós. Em grupos completos sem degeneração, o valor esperado é `k × d`. Desvios indicam grupo incompleto (D-06) ou desbalanceamento de LSs (D-07). |
| `equivalence_group_size` (median) | — (logs) | Mediana do tamanho dos grupos de equivalência. Mais robusta a outliers que a média quando há grupo incompleto residual. |

---

## 3. Métricas de utilidade

| Variável | Coluna nas tabelas | Definição |
|---|---|---|
| `ks_test_degree` | `KS-D` | Estatística D do teste Kolmogorov-Smirnov entre as distribuições empíricas de grau de `G` (original) e `G'` (anonimizado): `D = sup_x |F_G(x) − F_{G'}(x)|`. `0.0` = distribuições idênticas (utilidade máxima); `1.0` = completamente distintas. Mede degradação global da distribuição de grau. |
| `clustering_variation` | `clustering_var` | Variação relativa do coeficiente de clustering médio: `ΔCC = |CC(G') − CC(G)| / CC(G)`. `0.0` = clustering totalmente preservado; valores altos indicam distorção das propriedades de agrupamento local da rede. Indefinido se `CC(G) = 0` (grafos sem triângulos) — reportar `null` nesses casos. |

---

## 4. Campos dos logs JSONL e do verificador de k-anonimato

| Campo | Onde aparece | Definição |
|---|---|---|
| `valid` | Saída do verificador (`validation.py`) | `True` somente se nenhuma violação de k-anonimato for detectada — cobertura total e todos os grupos completos com LSs mutuamente isomorfas. |
| `satisfied_fraction` | Saída do verificador (campo legado) | Fração de nós satisfazendo a Def. 2 de He et al. Mantido por compatibilidade retroativa (BC); equivalente a `coverage_fraction`. |
| `n_violators` | Saída do verificador | Número absoluto de nós classificados como violadores (não cobertos ou pertencentes a grupo com violação de isomorfismo ou disjunção). |
| `violators` | Saída do verificador | Lista ordenada dos IDs dos nós violadores. |
| `deficit_fully_structural` | Saída do verificador (DL-01) | `True` se e somente se todas as violações são do tipo `"incomplete_group"` (causa estrutural esperada, D-06) e nenhuma é `"non_isomorphic"` ou `"non_disjoint"` (que indicariam bugs de implementação). Suporta o critério lógico do marco DL-01. |
| `subgraph_timeout_count` | Log JSONL pós-PR #97 | Número de nós-alvo cujo VF2 atingiu o `timeout` durante o ataque por subgrafo. Introduzido em DL-02 (issue #93). Nós com timeout são contabilizados como não-reidentificados, não como erro. **Atenção:** este campo não existe em logs anteriores ao PR #97 — não comparar diretamente entre épocas sem verificar sua presença. |
| `subgraph_candidate_counts` | Log JSONL pós-PR #97 | Estatísticas descritivas (`mean`, `std`, `max`) do número de candidatos isomórficos encontrados por nó-alvo pelo ataque por subgrafo. Introduzido em DL-02 para distinguir zeros por ausência de candidatos (privacidade real — H1) de zeros por timeout (limitação computacional — H3, descartada). |
| `verdict` | Log JSONL | Estado da execução do run. `SUCCESS_FULL` / `SUCCESS_PARTIAL` indicam execução normal (ver Seção 5.1 do README). **Compatibilidade de épocas:** em logs pré-PR #97, `verdict=ERROR` indicava timeout do VF2 no ataque por subgrafo. Em logs pós-PR #97, `verdict=ERROR` deixa de ser indicador de timeout (capturado por `subgraph_timeout_count`). Comparações entre épocas devem verificar o campo `subgraph_timeout_count`, não a ausência de `verdict=ERROR`. Ver DL-02 em [`docs/decision_log.md`](decision_log.md). |
| `partition_backend` | Log JSONL | Backend de particionamento usado na execução: `pymetis` ou `networkx-kl`. Gravado em cada linha para rastreabilidade. Backends diferentes produzem partições e métricas diferentes (D-04) — controlar ao comparar runs de máquinas ou ambientes distintos. |

---

## 5. Vereditos do verificador de k-anonimato

| Veredito | Condição | Ocorre em |
|---|---|---|
| `SUCCESS_FULL` | `coverage_fraction = 1.0`, nenhuma violação | Baseline `d=1`, k=2 |
| `SUCCESS_PARTIAL` | `coverage_fraction ≥ 0.9` e `deficit_fully_structural = True` | Baseline `d=1`, k∈{5,10,20}; d-sweep k∈{2,5} com `d=5` |
| `⚠️ FAILURE_LOW_COVERAGE` | `coverage_fraction < 0.9` | Exclusivo do d-sweep — combinações k×d excessivamente restritivas para a ego-rede 3437 (k=10 e k=20 com `d=5`; combo extremo d=10/k=20) |

> **Nota:** `FAILURE_LOW_COVERAGE` não aparece no baseline `d=1` — é específico de
> configurações com `d > 1` onde os grupos de equivalência exigidos excedem a
> capacidade estrutural da rede. Resultados com esse veredito são metodologicamente
> válidos e documentados (D-10), não excluídos.

---

## 6. Tipos de violação do verificador

| `type` | Causa | `status` | Quando ocorre |
|---|---|---|---|
| `"non_disjoint"` | Nó pertence a mais de uma LS simultaneamente | `"unprotected"` | Indica bug no anonimizador — não é caso normal de operação |
| `"incomplete_group"` | Grupo com `\|G_r\| < k` LSs | `"partially_unprotected"` | Caso normal esperado (D-06): grupo final pode ser incompleto quando as LSs disponíveis se esgotam |
| `"non_isomorphic"` | Par de LSs no mesmo grupo não são isomorfas | `"unprotected"` | Indica bug na etapa de isomorfização — não é caso normal |

---

## 7. Hipóteses do diagnóstico d-sweep (issue #93 / DL-02)

Usadas para interpretar zeros de `rr_subgrafo` em k=20, d∈{5,10}.

| Hipótese | Descrição | Status |
|---|---|---|
| H1 | Zeros refletem privacidade real — grupos de equivalência grandes tornam a correspondência VF2 ambígua entre múltiplos candidatos, sem vencedor único | Compatível com os dados — hipótese principal |
| H2 | Zeros decorrem parcialmente da degeneração estrutural documentada (D-06/D-10) — grupos incompletos reduzem candidatos disponíveis | Compatível, complementar a H1 |
| H3 | Zeros são artefato de timeout do VF2 mascarando ausência de correspondência (falso negativo computacional) | **Descartada** — ausência de `verdict=ERROR` nos 48 runs do log original prova que nenhuma chamada VF2 atingiu os 120 s configurados |
