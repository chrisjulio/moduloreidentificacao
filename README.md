# Módulo de Avaliação de Risco de Reidentificação em Redes Sociais Anonimizadas

> Aferidor experimental para medir, de forma agregada e reprodutível, a resistência
> efetiva de técnicas de anonimização estrutural de redes sociais a cenários formais
> de reidentificação. Componente preparatório da tese de doutorado em geração de
> redes sociais sintéticas — PPGInf/UFPR.
>
> **Estado:** escopo mínimo (S1–S5) + D-08 (d-sweep k×d) concluídos. Repositório em
> condições de entrega acadêmica. Última revisão: 02/06/2026.

![CI](https://github.com/chrisjulio/moduloreidentificacao/actions/workflows/ci.yml/badge.svg)

---

## 1. Posicionamento

Este repositório implementa o pipeline `anonimização → ataque → métrica` sobre
redes sociais reais, produzindo uma **curva privacidade-vs-utilidade** por
parâmetro de anonimização.

O módulo é um **aferidor**: opera como adversário formal — uma construção
metodológica de pior caso, sem alvo real — contra anonimizações conhecidas, e
produz números sobre a resistência efetiva de cada técnica. O ciclo experimental
é fechado e autocontido: tanto o grafo original quanto o grafo anonimizado são
artefatos que o próprio experimento gera e controla. A "taxa de reidentificação"
mede acerto contra rótulos internos de nós no experimento — **não** identificação
de pessoas reais.

O objetivo **não** é propor um novo mecanismo de privacidade, mas fornecer um
instrumento de aferição que orientará a deliberação metodológica futura sobre o
mecanismo de privacidade do framework integrado da tese. A unidade de progresso
é o **gráfico defensável**.

> A fronteira deste módulo é dupla: para trás, não substitui a deliberação
> metodológica da tese; para o lado, não é uma ferramenta ofensiva. O documento
> [`docs/scope.md`](docs/scope.md) fixa essa distinção de forma citável.
>
> A documentação formal da tese (proposta de pesquisa, artigo decisório, registros
> de orientação) não é publicada neste repositório, por ser ambiente aberto;
> referências a esses documentos devem ser lidas como apontadores internos.

---

## 2. Escopo

| Eixo | Decisão | Justificativa breve |
|---|---|---|
| Temporal | Estático | Replicação direta de [He et al. (2009)](https://doi.org/10.1109/WI-IAT.2009.108); extensão temporal é Fase 2 da tese. |
| Dataset principal | Facebook Ego-Nets (SNAP) | Validação alinhada com a literatura contemporânea de privacidade. |
| Dataset secundário | Email-Enron (SNAP), contingente | Amplia a base de comparação se houver folga; não perseguido no baseline. |
| Anonimização primária | [He et al. (2009)](https://doi.org/10.1109/WI-IAT.2009.108) | Algoritmo mais simples e mais bem documentado; ponto de entrada limpo. |
| Anonimização aspiracional | [Nettleton & Salas (2016)](https://doi.org/10.1016/j.eswa.2016.02.004) | Inclui atributos e t-closeness; fora do escopo do baseline. |
| Ataques | Grau → Subgrafos → Entropia | Ordem de complexidade crescente; os dois primeiros são o compromisso mínimo. |

<details>
<summary>Legenda das colunas</summary>

| Coluna | Significado |
|---|---|
| `Eixo` | Dimensão do escopo sendo definida (ex.: dataset, algoritmo de anonimização, tipo de ataque). |
| `Decisão` | Escolha adotada para esse eixo no escopo corrente do módulo. |
| `Justificativa breve` | Razão objetiva da escolha, com referência bibliográfica quando aplicável. |

Definições completas dos parâmetros em [`docs/data_dictionary.md`](docs/data_dictionary.md).
</details>

### Parâmetro principal

`k ∈ {2, 5, 10, 20}` — da anonimização fraca (k=2) à forte (k=20).

### Métricas

**Privacidade**
- Taxa de reidentificação por ataque (proporção de nós-alvo corretamente
  associados a seu rótulo interno).
- Tamanho médio e mediano dos grupos de equivalência produzidos pela anonimização.

**Utilidade**
- KS-test (estatística D) sobre a distribuição de grau (original vs. anonimizado).
- Variação relativa do coeficiente de clustering médio.

Definições operacionais completas em [`docs/metrics_definitions.md`](docs/metrics_definitions.md).

---

## 3. Como reproduzir o baseline

Procedimento completo, com os dois cenários (ambiente de desenvolvimento existente
e máquina limpa) e troubleshooting, em [`docs/reproducibility.md`](docs/reproducibility.md).
O resumo operacional está abaixo.

### 3.1 Pré-requisitos

| Componente | Requisito |
|---|---|
| Python | 3.11 ou 3.12 (`requires-python = ">=3.11"`; CI testa 3.11 e 3.12) |
| Git | qualquer versão recente |
| Acesso à internet | necessário na etapa de download do dataset (SNAP) |

<details>
<summary>Legenda das colunas</summary>

| Coluna | Significado |
|---|---|
| `Componente` | Nome do software ou recurso necessário para reprodução do experimento. |
| `Requisito` | Versão mínima aceita ou condição de disponibilidade exigida para execução. |

Definições completas dos parâmetros de configuração em [`docs/data_dictionary.md`](docs/data_dictionary.md) §1.
</details>

O backend de particionamento `pymetis` é **opcional**. Quando ausente, o algoritmo
recai automaticamente para o backend Kernighan-Lin (decisão **D-04** — ver
[`docs/decision_log.md`](docs/decision_log.md)). Essa escolha **afeta a
reprodução**: backends diferentes produzem partições diferentes. Em Windows,
`pip install pymetis` falha; consulte [`windows_pymetis.md`](windows_pymetis.md)
para instalar via Conda e configurar o VS Code.

### 3.2 Ambiente

```bash
# Criar e ativar ambiente virtual
python -m venv .venv
source .venv/bin/activate          # Linux/macOS
# .venv\Scripts\Activate.ps1       # Windows (PowerShell)

# Instalar dependências de produção e de desenvolvimento
python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt

# Sanidade do ambiente
ruff check .
pytest -q
```

### 3.3 Pipeline canônico

Todos os comandos rodam a partir da raiz do repositório, com o `.venv` ativado.

```bash
# 1. Download do dataset (uma única vez; saída não versionada)
python -m src.loaders.download

# 2. Experimento baseline (12 runs: k ∈ {2,5,10,20} × 3 sementes)
python -m experiments.run --config experiments/configs/he2009_facebook_baseline.yml

# 3. Gráfico privacidade-vs-utilidade (PDF + PNG em results/plots/)
python -m src.visualization.privacy_utility \
    --logs experiments/logs/he2009_facebook_baseline \
    --dataset facebook --out results/plots

# 4. Tabelas CSV por (dataset, ataque) em results/tables/
python -m src.visualization.tables \
    --logs experiments/logs/he2009_facebook_baseline \
    --dataset facebook --out results/tables

# 5. Verificação automática contra docs/results_baseline.md
python -m scripts.verify_reproduction --tables results/tables
```

Tempo estimado do baseline em hardware típico: ~6–12 min (dominado pelo ataque por
subgrafo). Detalhamento por etapa em [`docs/pipeline.md`](docs/pipeline.md) §5.

### 3.4 Determinismo e reprodutibilidade

- Sementes (`42, 1337, 2718`) fixadas e versionadas no YAML de configuração —
  nunca hardcoded no código.
- Mínimo de 3 execuções independentes por configuração `(k, dataset, ataque)`,
  para barras de erro.
- Outputs (gráficos, tabelas) gerados a partir de logs JSONL estruturados em
  `experiments/logs/`, não de execução interativa.
- Datasets baixados por script versionado; **não** comitados no repositório.
- Reprodutibilidade end-to-end validada (issue #27): clone limpo → `pip install`
  → execução → outputs verificados contra `docs/results_baseline.md`.
- Registro acumulativo de bugs em `/bugs/` (execução + explicação + decisão tomada),
  consultável para diagnóstico de divergências na reprodução.

Três fatores fora das sementes podem fazer os resultados divergirem e devem ser
controlados na reprodução: o backend de partição (D-04), o timeout de 60 s do
ataque por subgrafo (sensível a hardware) e a versão das bibliotecas numéricas.
Ver [`docs/reproducibility.md`](docs/reproducibility.md) §8.

---

## 4. Status do projeto

**Atualizado em 26/05/2026.** Escopo mínimo (S1–S5) concluído — 35 issues fechadas.

| Fase | Período planejado | Status |
|---|---|---|
| S1: Setup + loader + leitura He et al. | 15–22/05 | ✅ Concluída |
| S2: Implementação He et al. + validação k-anonimato | 22–29/05 | ✅ Concluída (marco 29/05 cumprido em 21/05) |
| S3: Ataques + métricas + experimento baseline | 29/05–05/06 | ✅ Concluída (adiantada para 22–23/05) |
| S4: Gráficos, tabelas e documentação técnica | 05–12/06 | ✅ Concluída (adiantada para 25/05) |
| S5: Polimento, reprodutibilidade e entrega | 12–14/06 | ✅ Concluída (em 26/05) |

<details>
<summary>Legenda das colunas</summary>

| Coluna | Significado |
|---|---|
| `Fase` | Sprint de desenvolvimento, identificada por código (`S1`–`S5`) e descrição funcional do escopo da etapa. |
| `Período planejado` | Intervalo de datas originalmente previsto no planejamento inicial. |
| `Status` | Estado de conclusão: ✅ Concluída (com indicação de adiantamento quando aplicável). A data efetiva consta do [`docs/progress.md`](docs/progress.md). |

</details>

**Marco intermediário não-negociável cumprido:** 21/05/2026 (antecipado em 8 dias).
k-anonimato empiricamente atingido em todas as configurações do Mínimo
(k ∈ {2, 5, 10, 20}), com `satisfied_fraction ≥ 0.9962` em k ∈ {2, 5, 10} e
`satisfied_fraction = 0.9774` no pior caso (k=20) — critério DL-01 aprovado em
todas as configurações. Ver [`docs/validacao_k_anonimato.md`](docs/validacao_k_anonimato.md)
e [`docs/decision_log.md`](docs/decision_log.md).

**D-08 — d-sweep (He et al., d > 1): CONCLUÍDO em 02/06/2026.**
Varredura completa do grid k ∈ {2, 5, 10, 20} × d ∈ {1, 2, 5, 10} × 3 sementes
(48 runs, 100% sem erros, backend pymetis em todos). Ciclo composto pelas issues
#72–#78, #80, #88 e #93, encerradas em 7 fases. Decisões D-08, D-09, D-10 e
DL-02 registradas em [`docs/decision_log.md`](docs/decision_log.md). Relatório
consolidado com matriz d×k, análise e ameaças à validade em
[`docs/results_dsweep.md`](docs/results_dsweep.md). Limitação §1.3 de
[`docs/limitations.md`](docs/limitations.md) marcada como **parcialmente resolvida**.
Issue de encaminhamentos pós-D-08: [#99](https://github.com/chrisjulio/moduloreidentificacao/issues/99).

Escopo Desejável (Email-Enron, ataque por entropia) e Aspiracional
([Nettleton & Salas, 2016](https://doi.org/10.1016/j.eswa.2016.02.004)) permanecem abertos como trabalho futuro. Ver
[Seção 12 — Próximos passos](#12-próximos-passos).

### Componentes implementados

**S1–S2 — anonimização e validação**
- `src/anonymization/he2009.py` — pipeline completo: `partition_graph`,
  `_group_local_structures` (FSM+MF), `_modify_structure`, `_reconnect_inter_edges`,
  `anonymize(g, k, d, seed)`. Backend de particionamento em
  `src/anonymization/_partition_backend.py`.
- `src/anonymization/validation.py` — auditor independente
  `validate_k_anonymity(groups, k) → dict` (36 testes). Campos DL-01:
  `coverage_fraction`, `uncovered_fraction`, `deficit_fully_structural`.
- `src/loaders/facebook_ego.py` — loader Facebook Ego-Nets (SNAP).
- `src/loaders/download.py` — script versionado para download automático dos datasets.
- `experiments/run_validacao_k_anonimato.py` — script de validação do k-anonimato
  (marco 21/05; k=5, egonet_id=3437, n=532, m=4812).
- `experiments/run_k_sweep.py` — k-sweep k ∈ {2, 5, 10, 20}; todos aprovados
  pelo critério DL-01.
- `docs/decision_log.md` — registro de decisões técnicas (DL-01, D-04 a D-07).
- `docs/progress.md` — log de progresso sessão a sessão.
- CI: GitHub Actions + pre-commit (ruff v0.15.13).

**S3 — ataques, métricas e experimento baseline**
- `src/attacks/degree.py` — ataque por grau
  (`degree_attack(g_orig, g_anon, target, tolerance=0) → bool`).
- `src/attacks/subgraph.py` — ataque por subgrafos via VF2
  (`subgraph_attack(g_orig, g_anon, target, hop=1, timeout=None) → bool`).
- `src/metrics/` — 4 métricas: `reidentification_rate`, `equivalence_group_size`,
  `ks_test_degree`, `clustering_variation`.
- `experiments/run.py` — runner orquestrador CLI
  (`python -m experiments.run --config <yaml>`).
- `experiments/configs/he2009_facebook_baseline.yml` — config do experimento baseline.
- `docs/results_baseline.md` — tabela bruta e agregações do baseline.

**S4 — visualização e documentação técnica**
- `src/visualization/privacy_utility.py` — gráfico privacidade-vs-utilidade
  (2 painéis, barras de erro), saída PDF+PNG em `results/plots/`.
- `src/visualization/tables.py` — tabelas CSV por `(dataset, ataque)`
  em `results/tables/`.
- `docs/pipeline.md` — documentação técnica do pipeline com diagramas Mermaid,
  comandos reproduzíveis e lista de outputs.
- `docs/limitations.md` — limitações metodológicas documentadas.
- `docs/reproducibility.md` — protocolo de reprodutibilidade end-to-end.
- `docs/preprocessing_decision.md` — decisões de pré-processamento dos datasets.
- `docs/algorithm_notes.md` e `docs/metrics_definitions.md` — revisados e
  cross-referenciados.

**S5 — validação final e entrega**
- `docs/scope.md` — escopo, não-escopo e condições de contorno ética (citável).
- `docs/entregaveis.md` — lista consolidada de entregáveis por nível.
- Revisão global de README, `CLAUDE.md` e `docs/` (issue #28).

**D-08 — d-sweep e diagnóstico (issues #72–#78, #80, #88, #93)**
- `experiments/configs/he2009_facebook_dsweep.yml` — config do d-sweep
  (k ∈ {2,5,10,20} × d ∈ {1,2,5,10}, 3 sementes, pymetis obrigatório via
  `allow_kl_fallback: false`).
- `experiments/configs/he2009_facebook_dsweep_k20_diag.yml` — reexecução
  opcional das 6 células k=20 com instrumentação DL-02 (issue #93).
- `src/attacks/subgraph.py` — atualizado com instrumentação DL-02:
  `subgraph_timeout_count` (nós cujo VF2 atingiu timeout, tratados como
  não-reidentificados) e `subgraph_candidate_counts` (`mean`/`std`/`max`
  de candidatos por nó). Esses campos tornam a distinção entre zero por
  ausência de candidatos e zero por timeout diretamente observável em logs
  pós-PR #97. **Atenção:** logs pré-PR #97 têm semântica diferente de
  `verdict=ERROR` — ver nota de comparabilidade DL-02 em
  [`docs/decision_log.md`](docs/decision_log.md) e
  [`docs/results_dsweep.md`](docs/results_dsweep.md) §5.7.
- `docs/results_dsweep.md` — relatório consolidado final do d-sweep: matriz
  d×k com médias e desvios-padrão de todas as métricas, análise das tendências,
  combos degenerados (d=2 D-08; d=10/k=20 D-10), diagnóstico H3 (zeros de
  reid_sub em k=20) e ameaças à validade.
- `docs/dsweep_previa_garantia_dados.md` — snapshot histórico do estado
  intermediário do d-sweep; substituído por `results_dsweep.md` como
  documento canônico.

---

## 5. Resultados

> **Leitura-chave (achado B1).** No regime `d=1` (baseline mínimo — §5.1), os
> resultados rotulados como "He et al. *structure-aware*" equivalem a
> **k-anonimato de grau**: com `d=1` a estrutura local de cada nó reduz-se ao seu
> próprio grau, e o isomorfismo de vizinhança degenera em igualdade de grau. A
> propriedade *structure-aware* propriamente dita só é exercida no **d-sweep**
> (`d ∈ {5, 10}` — §5.2). **O contraste `d=1` vs. `d ∈ {5, 10}` é a evidência
> empírica de que o módulo afere privacidade estrutural — e deve ser lido como
> tal, não como detalhe de configuração.** Ver D-02 em
> [`docs/decision_log.md`](docs/decision_log.md); `algorithm_notes.md` §5.3, §6.5,
> §9.1; `limitations.md` §1.3.

### 5.1 Baseline — `d=1` (âncora)

**Dataset:** Facebook Ego-Net 3437 (n=532, m=4812). **Parâmetros:** He et al.
(2009), `d=1`, `sigma=0.5`, `k ∈ {2, 5, 10, 20}`, 3 sementes (42, 1337, 2718).
**Ataques:** grau e subgrafo 1-hop (timeout 60 s). Valores: médias sobre sementes.

| k | Veredito | coverage_fraction | rr_grau | rr_subgrafo | KS-D | clustering_var |
|---|---|---|---|---|---|---|
| 2 | SUCCESS_FULL | 1.0000 | 0.026 | 0.791 | 0.000 | 0.000 |
| 5 | SUCCESS_PARTIAL | 0.9962 | 0.008 | 0.406 | 0.048 | 0.067 |
| 10 | SUCCESS_PARTIAL | 0.9962 | 0.023 | 0.140 | 0.236 | 0.158 |
| 20 | SUCCESS_PARTIAL | 0.9774 | 0.099 | 0.000 | 0.649 | 0.090 |

<details>
<summary>Legenda das colunas</summary>

> `rr_grau` e `rr_subgrafo` são taxas de acerto contra rótulos internos de nós no experimento fechado — não identificação de pessoas reais.

| Coluna | Significado |
|---|---|
| `k` | Parâmetro de k-anonimato configurado na anonimização He et al. (2009). Define o tamanho mínimo dos grupos de equivalência estrutural. Valores testados: `{2, 5, 10, 20}` — do mais fraco ao mais forte. |
| `Veredito` | Resultado da auditoria do verificador independente (`validation.py`). `SUCCESS_FULL` = cobertura total (todos os nós em grupos ≥ k). `SUCCESS_PARTIAL` = cobertura ≥ 0.9 com nós residuais atribuíveis ao grupo incompleto estrutural (D-06). |
| `coverage_fraction` | Fração dos nós do grafo anonimizado `G'` em grupos de equivalência com tamanho ≥ k. `1.0` = cobertura total; valores < `1.0` indicam nós residuais do grupo incompleto final (D-06 — aceitável). |
| `rr_grau` | Taxa de reidentificação por grau: `N_correto / N_total` usando apenas a assinatura de grau do nó (`tolerance=0`). Modelo adversarial mais fraco — linha de base. |
| `rr_subgrafo` | Taxa de reidentificação por subgrafo: `N_correto / N_total` por isomorfismo de vizinhança 1-hop (VF2, `timeout=60 s`). Modelo mais próximo do adversarial de He et al. Cota teórica: `≤ 1/k` sob k-anonimato pleno. |
| `KS-D` | Estatística D do KS-test entre distribuições de grau de `G` e `G'`. `0.0` = idênticas (utilidade máxima); `1.0` = completamente distintas. |
| `clustering_var` | Variação relativa do clustering médio: `|CC(G') − CC(G)| / CC(G)`. `0.0` = clustering totalmente preservado. |

Definições operacionais formais em [`docs/metrics_definitions.md`](docs/metrics_definitions.md) e [`docs/data_dictionary.md`](docs/data_dictionary.md) §2–3.
</details>

Análise completa e tabela bruta em [`docs/results_baseline.md`](docs/results_baseline.md).

### 5.2 d-sweep — `d ∈ {1, 2, 5, 10}` (48 runs, backend pymetis)

Varredura completa do grid k × d. Valores `d=1` replicam o baseline com novo
timeout (120 s/nó) e servem de âncora de comparação. **`d=5` é o valor primário**
para análise structure-aware. `d=2` é degenerate para esta ego-rede (D-08) e
`d=10/k=20` é combo deliberadamente extremo (D-10) — ambos documentados, não
excluídos.

**Coluna `d=5` — médias ± dp sobre 3 sementes:**

| k | coverage_fraction | rr_subgrafo | rr_grau | KS-D | clustering_var | veredito |
|---|---|---|---|---|---|---|
| 2 | 0.989 | 0.211 ± 0.016 | 0.036 ± 0.011 | 0.031 ± 0.003 | 0.031 ± 0.009 | SUCCESS_PARTIAL |
| 5 | 0.949 | 0.056 ± 0.005 | 0.012 ± 0.004 | 0.229 ± 0.028 | 0.210 ± 0.020 | SUCCESS_PARTIAL |
| 10 | 0.846 | 0.015 ± 0.015 | 0.219 ± 0.116 | 0.745 ± 0.029 | 0.043 ± 0.027 | ⚠️ FAILURE_LOW_COVERAGE |
| 20 | 0.752 | 0.000 ± 0.000 | 0.055 ± 0.000 | 0.927 ± 0.000 | 0.403 ± 0.007 | ⚠️ FAILURE_LOW_COVERAGE |

<details>
<summary>Legenda das colunas</summary>

> Colunas com formato `média ± dp` reportam média e desvio-padrão sobre as 3 sementes (42, 1337, 2718). `coverage_fraction` não tem desvio-padrão — calculada sobre a estrutura do grafo, não sensível a semente.
>
> `rr_grau` e `rr_subgrafo` são taxas de acerto contra rótulos internos de nós no experimento fechado — não identificação de pessoas reais.

| Coluna | Significado |
|---|---|
| `k` | Parâmetro de k-anonimato (idêntico à tabela baseline). |
| `coverage_fraction` | Fração de nós cobertos por grupos de equivalência com tamanho ≥ k (idêntico à tabela baseline, sem variação por semente). |
| `rr_subgrafo` | Taxa de reidentificação por subgrafo — `média ± dp` sobre 3 sementes. `timeout=120 s/nó` (elevado em relação ao baseline para acomodar grafos mais densos com `d > 1`). |
| `rr_grau` | Taxa de reidentificação por grau — `média ± dp` sobre 3 sementes. |
| `KS-D` | Estatística KS — `média ± dp` sobre 3 sementes. |
| `clustering_var` | Variação do clustering — `média ± dp` sobre 3 sementes. |
| `veredito` | `SUCCESS_PARTIAL` = k-anonimato satisfeito com nós residuais aceitáveis. `⚠️ FAILURE_LOW_COVERAGE` = `coverage_fraction < 0.9` — combinação k×d excessivamente restritiva para esta ego-rede. **Este veredito não aparece no baseline `d=1`** — é específico de configurações com `d > 1`. |

Definições operacionais formais em [`docs/metrics_definitions.md`](docs/metrics_definitions.md) e [`docs/data_dictionary.md`](docs/data_dictionary.md) §2–5.
</details>

**Achados principais:**

- **Tendências opostas dos ataques em k.** `rr_subgrafo` cai com k (de ~0.14–0.21
  em k=2 para ~0.00–0.04 em k=20): grupos maiores criam mais candidatos
  indistinguíveis. `rr_grau` sobe com k (de ~0.02–0.04 em k=2 para ~0.05–0.36
  em k=20): a anonimização para k alto distorce fortemente a distribuição de
  graus (KS-D → 0.75–0.93), criando assinaturas mais singulares. Aumentar `k`
  **desloca** o vetor de ataque mais eficaz — não garante melhora monotônica de
  privacidade.
- **Zeros de `rr_subgrafo` em k=20 são genuínos** (diagnóstico #93 / DL-02).
  Hipótese de timeout mascarando zeros (H3) descartada: nenhum `verdict=ERROR`
  nos 48 runs do log pré-DL-02, provando que nenhuma chamada VF2 atingiu os
  120 s. Os zeros refletem ausência de correspondência única em `G'` sob grupos
  de equivalência grandes (EGS ≈ k·d).
- **Nota de comparabilidade de logs (DL-02).** Em logs **pós-PR #97**, a
  semântica do sentinela de timeout muda: `TimeoutError` é capturado por nó e
  acumulado em `subgraph_timeout_count`; `verdict=ERROR` deixa de ser prova de
  timeout. Comparações cruzadas entre logs de épocas diferentes devem verificar
  o campo `subgraph_timeout_count`, não a ausência de `verdict=ERROR`. Ver
  [`docs/decision_log.md`](docs/decision_log.md) (DL-02) e
  [`docs/results_dsweep.md`](docs/results_dsweep.md) §5.7.

Matriz completa k × d (todas as métricas, combos degenerados, ameaças à
validade) em [`docs/results_dsweep.md`](docs/results_dsweep.md). Gráficos
d-aware em `results/plots/` (não versionados; regeneráveis — ver §3.3).

---

## 6. Entregáveis

Três níveis, com linha firme entre **Mínimo** e **Desejável**. Status consolidado
em [`docs/entregaveis.md`](docs/entregaveis.md).

- **Mínimo defensável (✅ concluído).** Pipeline funcional sobre Facebook Ego-Nets
  aplicando [He et al. (2009)](https://doi.org/10.1109/WI-IAT.2009.108) com `k ∈ {2, 5, 10, 20}`; ataques por grau e por
  subgrafos; quatro métricas; mínimo de 3 sementes por configuração; gráfico
  privacidade-vs-utilidade com barras de erro; repositório versionado com README
  operacional e configuração reproduzível.
- **Desejável (não perseguido).** Execução adicional sobre Email-Enron; ataque
  por entropia.
- **Aspiracional (não perseguido).** Implementação inicial de Nettleton & Salas
  (2016); comparação preliminar das duas anonimizações no mesmo gráfico.

O Mínimo é entregável defensável em si; o Desejável é entregável discutível; o
Aspiracional é bônus que não deve ser perseguido em detrimento do Mínimo.

---

## 7. Estrutura do repositório

```
/data/
  /raw/                      # datasets originais (não versionados; baixados por script)
  /processed/                # datasets após pré-processamento
/src/
  /anonymization/            # [He et al. (2009)](https://doi.org/10.1109/WI-IAT.2009.108) [implementado]; placeholder Nettleton & Salas
  /attacks/                  # ataques por grau e subgrafos
  /metrics/                  # cálculo das quatro métricas
  /loaders/                  # carregadores de dataset (Facebook Ego-Nets) e script de download
  /visualization/            # gráfico privacy-vs-utility e tabelas CSV
/experiments/
  /configs/                  # arquivos de configuração (YAML); inclui baseline, d-sweep e diagnóstico k=20
  /logs/                     # logs estruturados JSONL das execuções (não versionados)
  run.py                     # runner orquestrador CLI
  run_k_sweep.py             # k-sweep k ∈ {2,5,10,20} (issue #17)
  run_validacao_k_anonimato.py  # validação k-anonimato marco 21/05 (issue #16)
/results/
  /tables/                   # tabelas em CSV (não versionadas; regeneráveis)
  /plots/                    # gráficos em PDF/PNG (não versionados; regeneráveis)
/tests/                      # suíte de testes (espelha a estrutura de src/)
/scripts/                    # setup de ambiente e verificação de reprodução
/bugs/                       # registro acumulativo de bugs (execução + explicação + decisão)
/docs/
  scope.md                   # escopo, não-escopo e condições de contorno ética
  algorithm_notes.md         # notas sobre a implementação de He et al. (inclui k-sweep e d>1)
  metrics_definitions.md     # definições operacionais das métricas
  decision_log.md            # registro formal de decisões técnicas (DL-01/DL-02, D-04 a D-10)
  progress.md                # log de progresso sessão a sessão
  validacao_k_anonimato.md   # resultados consolidados da validação empírica de k-anonimato
  results_baseline.md        # tabela bruta + agregações do experimento baseline (d=1)
  results_dsweep.md          # relatório consolidado do d-sweep — matriz k×d, análise, ameaças
  dsweep_previa_garantia_dados.md  # snapshot histórico intermediário do d-sweep (não canônico)
  milestones_moduloreidentificacao.md  # acompanhamento de issues por milestone
  pipeline.md                # documentação técnica do pipeline com diagramas Mermaid
  limitations.md             # limitações metodológicas (§1.3 parcialmente resolvida)
  reproducibility.md         # guia de reprodução end-to-end
  preprocessing_decision.md  # decisões de pré-processamento dos datasets
  entregaveis.md             # entregáveis consolidados por nível
README.md                    # este arquivo — visão operacional canônica
CLAUDE.md                    # instruções de desenvolvimento para sessões de agente
WORKFLOW.md                  # protocolo de orquestração entre interfaces de trabalho
windows_pymetis.md           # ajustes Windows: ambiente Conda e backend pymetis
pyproject.toml               # metadados do projeto + configuração de ruff e pytest
requirements.txt             # dependências de produção
requirements-dev.txt         # dependências de desenvolvimento (lint, testes)
config_example.yml           # modelo de configuração de experimento
environment.yml              # ambiente Conda (caminho alternativo no Windows, com METIS)
.pre-commit-config.yaml      # hooks de pre-commit (ruff)
LICENSE                      # licença do repositório
```

A organização foi pensada para permitir migração futura para o repositório do
framework integrado da tese (EpiCNet) sem refatoração estrutural significativa.
A integração, quando ocorrer, deve dar-se apenas por interfaces explícitas e
schemas documentados — o módulo permanece arquiteturalmente independente.

---

## 8. Limitações e ameaças à validade

Registro completo e categorizado em [`docs/limitations.md`](docs/limitations.md).
Em resumo:

- **Validade interna.** Aproximações na implementação de [He et al. (2009)](https://doi.org/10.1109/WI-IAT.2009.108): FSM
  simplificado, fallback de particionamento (D-04), grupos incompletos residuais
  aceitáveis sob D-06, e custo/timeout do ataque por subgrafo.
- **Validade externa.** Baseline (`d=1`) restrito a uma ego-rede específica; o
  d-sweep (`d ∈ {1,2,5,10}`) resolve parcialmente a limitação §1.3 mas ainda
  opera sobre a mesma ego-rede 3437 — generalização exige replicação em outros
  grafos. Sem Email-Enron, sem redes temporais e sem dados sintéticos nesta fase.
- **Validade de construção.** A "reidentificação" medida é acerto contra rótulos
  internos de nós, não identificação de pessoas; similaridade estrutural não é
  identidade.
- **Validade ética.** O módulo opera apenas com datasets públicos desidentificados,
  em ciclo experimental fechado, sem cruzamento com bases pessoais externas e com
  saídas agregadas.

O baseline é **estático**: generalizações para redes temporais ou sintéticas
exigem novo experimento e pertencem à Fase 2 da tese.

---

## 9. Premissas

- **Linguagem.** Python 3.11+. NetworkX como padrão da área; alternativas
  (igraph, graph-tool) são aceitáveis mas exigem justificativa.
- **Hardware.** Razoável; sem requisito de GPU.
- **Datasets.** Públicos via SNAP, desidentificados pela fonte; uso dentro das
  condições de licença e de propósito acadêmico.

---

## 10. O que este módulo não faz

- Não decide o mecanismo de privacidade do framework integrado da tese — produz
  medições que orientarão essa deliberação metodológica.
- Não estende a anonimização para o contexto temporal (Fase 2 da tese).
- Não implementa o gerador de redes sintéticas.
- Não pretende contribuição original de pesquisa em privacidade — é instrumento
  de validação empírica.
- Não ingere dados de redes sociais "vivas", de produção ou vazados; não realiza
  cruzamento com bases pessoais externas; não tenta identificar pessoas reais.

---

## 11. Licença e uso de dados

A licença do código está no arquivo [`LICENSE`](LICENSE).

O uso de dados públicos desidentificados (Facebook Ego-Nets, SNAP) dispensa
aprovação de Comitê de Ética em Pesquisa nos termos da Resolução CNS 510/2016
(Art. 1º, §único, III). O enquadramento ético completo está registrado em
[`docs/scope.md`](docs/scope.md) §7.

---


> **Usuários Windows:** para instalar `pymetis` via Conda e configurar o VS Code,
> consulte [`windows_pymetis.md`](windows_pymetis.md).

---

## 12. Próximos passos

O escopo mínimo (S1–S5) e o ciclo D-08 (d-sweep) estão concluídos. As issues
abaixo definem as fronteiras abertas do módulo, organizadas por prioridade e
tier. A decisão sobre sequenciamento está em discussão na
[issue #99](https://github.com/chrisjulio/moduloreidentificacao/issues/99).

### Encaminhamentos imediatos (pós-D-08)

| Issue | Título | Natureza |
|---|---|---|
| [#99](https://github.com/chrisjulio/moduloreidentificacao/issues/99) | Encaminhamentos pós-D-08 — próximos passos do módulo | Planejamento |

<details>
<summary>Legenda das colunas (válida para as três subtabelas abaixo)</summary>

| Coluna | Significado |
|---|---|
| `Issue` | Link para a issue correspondente no GitHub com seu número identificador. |
| `Título` | Descrição curta da tarefa ou atividade planejada. |
| `Natureza` *(encaminhamentos imediatos)* | Categoria da issue: `Planejamento`, `Técnica`, etc. |
| `Dependência` *(S6 e Aspiracional)* | Pré-requisito técnico que precisa preceder esta issue; `Nenhuma` indica que pode ser iniciada de forma independente. |

</details>

Pendências específicas identificadas no ciclo D-08:
- Fechar o milestone S7 após conferir que todas as issues estão encerradas.
- Verificar resultado dos testes G3 (issue #80) e atualizar o status da nota
  `algorithm_notes.md §3.2.2` (fórmula k(k−1) — marcada como interpretativa e
  dependente de validação empírica; em avaliação).

### Escopo Desejável — milestone S6

| Issue | Título | Dependência |
|---|---|---|
| [#29](https://github.com/chrisjulio/moduloreidentificacao/issues/29) | Loader Email-Enron como dataset secundário | Nenhuma — ampliar validade externa |
| [#30](https://github.com/chrisjulio/moduloreidentificacao/issues/30) | Ataque por entropia reutilizando grupos de equivalência | Depende de `src/attacks/` existente |

### Escopo Aspiracional

| Issue | Título | Dependência |
|---|---|---|
| [#31](https://github.com/chrisjulio/moduloreidentificacao/issues/31) | Implementação inicial de [Nettleton & Salas (2016)](https://doi.org/10.1016/j.eswa.2016.02.004) | Alto esforço; comparação entre duas anonimizações |

### Horizonte — integração com o EpiCNet

Com o módulo de avaliação de risco consolidado, a integração futura com o
framework central da tese deve ocorrer apenas por interfaces explícitas e schemas
documentados. Pontos de ancoragem:
- `docs/results_dsweep.md` como evidência metodológica para a qualificação.
- Interface de entrada: grafo anonimizado/sintético + metadados de parâmetros.
- Interface de saída: relatório de risco agregado (privacidade-vs-utilidade).
- O módulo permanece arquiteturalmente independente do EpiCNet — ver
  [`docs/scope.md`](docs/scope.md).

---

## 13. Referências
[1] [BACKSTROM, L.; DWORK, C.; KLEINBERG, J.](https://doi.org/10.1145/1242572.1242598) Wherefore art thou R3579X? Anonymized social networks, hidden patterns, and structural steganography. In: *Proceedings of the 16th International Conference on World Wide Web (WWW 2007)*. New York: ACM, 2007. p. 181–190.

[2] [HE, X. et al.](https://doi.org/10.1109/WI-IAT.2009.108) Preserving privacy in social networks: A structure-aware approach. In: *IEEE/WIC/ACM International Joint Conference on Web Intelligence and Intelligent Agent Technology (WI-IAT 2009)*. [S. l.]: IEEE, 2009. p. 647–654.

[3] [KARYPIS, G.; KUMAR, V.](https://doi.org/10.1137/S1064827595287997) A fast and high quality multilevel scheme for partitioning irregular graphs. *SIAM Journal on Scientific Computing*, v. 20, n. 1, p. 359–392, 1998.

[4] [LESKOVEC, J.; MCAULEY, J. J.](https://dl.acm.org/doi/10.5555/2999134.2999195) Learning to discover social circles in ego networks. In: *Advances in Neural Information Processing Systems (NIPS 2012)*. [S. l.]: Curran Associates, 2012. p. 539–547.

[5] [LIU, K.; TERZI, E.](https://doi.org/10.1145/1376616.1376629) Towards identity anonymization on graphs. In: *Proceedings of the 2008 ACM SIGMOD International Conference on Management of Data (SIGMOD 2008)*. New York: ACM, 2008. p. 93–106.

[6] [NARAYANAN, A.; SHMATIKOV, V.](https://doi.org/10.1109/SP.2008.33) Robust de-anonymization of large sparse datasets. In: *IEEE Symposium on Security and Privacy (S&P 2008)*. [S. l.]: IEEE, 2008. p. 111–125.

[7] [NETTLETON, D. F.; SALAS, J.](https://doi.org/10.1016/j.eswa.2016.02.004) A data driven anonymization system for information rich online social network graphs. *Expert Systems with Applications*, v. 55, p. 87–105, 2016.

[8] [SWEENEY, L.](https://doi.org/10.1142/S0218488502001648) k-anonymity: A model for protecting privacy. *International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems*, v. 10, n. 5, p. 557–570, 2002.

[9] [WÖRLEIN, M. et al.](https://doi.org/10.1007/11564126_32) A quantitative comparison of the subgraph miners MoFa, gSpan, FFSM, and Gaston. In: *Knowledge Discovery in Databases: PKDD 2005*. Berlin: Springer, 2005. p. 392–403. (Lecture Notes in Computer Science, v. 3721).

[10] [ZHOU, B.; PEI, J.](https://doi.org/10.1109/ICDE.2008.4497459) Preserving privacy in social networks against neighborhood attacks. In: *2008 IEEE 24th International Conference on Data Engineering (ICDE 2008)*. [S. l.]: IEEE, 2008. p. 506–515.

---

- Documentação interna do projeto (não pública): artigo decisório da tese
  (Seções 4.3 e 7) e proposta original.

---

*Repositório associado à tese de doutorado em geração de redes sociais sintéticas
— PPGInf/UFPR.*
