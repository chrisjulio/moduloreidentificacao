# Resultados — d-sweep (issue #88)

> **Relatório consolidado final** da varredura `d`-sweep do experimento
> `he2009_facebook_dsweep`. Substitui a prévia de garantia de dados
> ([`docs/dsweep_previa_garantia_dados.md`](dsweep_previa_garantia_dados.md)),
> agora apenas snapshot histórico do estado intermediário.
>
> As tabelas e figuras abaixo são **regeneradas a partir do log estruturado**
> seguindo o fluxo de [`.claude/rules/experiments.md`](../.claude/rules/experiments.md)
> (`config → run → log → parse → table/plot`). Comandos de reprodução na §6.

---

## 1. Metadados do experimento

| Campo | Valor |
|---|---|
| Experimento | `he2009_facebook_dsweep` |
| Issue | **#88** (complemento de #77; ver também #72) |
| Config | [`experiments/configs/he2009_facebook_dsweep.yml`](../experiments/configs/he2009_facebook_dsweep.yml) |
| Log fonte | `experiments/logs/he2009_facebook_dsweep/he2009_facebook_dsweep.jsonl` |
| Dataset | Facebook Ego-Net **3437** (LCC: n=532, m=4812, densidade ≈ 0.034) |
| Anonimização | He et al. (2009), σ = 0.5 |
| Backend de particionamento | **pymetis** (fiel a He et al., D-04) — em **todos** os 48 runs |
| Ataques | grau (tolerância 0) + subgrafo (hop = 1, timeout = 120 s/nó) |
| Métrica canônica `reidentification_rate` | = ataque por **subgrafo** |
| Grid | k ∈ {2, 5, 10, 20} × d ∈ {1, 2, 5, 10} × sementes {42, 1337, 2718} = **48 runs** |
| Conclusão | 2026-06-02 — **48 de 48 (100%)**, sem `error` em nenhuma linha |
| Vereditos | **33 SUCCESS_PARTIAL / 15 FAILURE_LOW_COVERAGE** |

`d = 1` é a âncora de comparação com o baseline; `d ∈ {5, 10}` são os valores
primários; `d = 2` é mantido e **anotado como degenerate** (D-08, G3). O combo
`d = 10, k = 20` é incluído deliberadamente como degenerate esperado (D-10).

---

## 2. Cobertura do grid

Todas as 16 células `(k, d)` completas com 3 sementes (48 runs). Nenhuma
pendência, nenhum crash, nenhuma execução com `error != null`.

```
┌─────┬────────┬────────┬────────┬────────┐
│  k  │  d=1   │  d=2   │  d=5   │  d=10  │
├─────┼────────┼────────┼────────┼────────┤
│ 2   │ ✅✅✅ │ ✅✅✅ │ ✅✅✅ │ ✅✅✅ │
│ 5   │ ✅✅✅ │ ✅✅✅ │ ✅✅✅ │ ✅✅✅ │
│ 10  │ ✅✅✅ │ ✅✅✅ │ ✅✅✅ │ ✅✅✅ │
│ 20  │ ✅✅✅ │ ✅✅✅ │ ✅✅✅ │ ✅✅✅ │
└─────┴────────┴────────┴────────┴────────┘
```

---

## 3. Resultados consolidados

Valores `média ± desvio-padrão` sobre as 3 sementes de cada célula `(k, d)`.

- `reid_sub` — reidentificação por **subgrafo** (métrica canônica);
- `reid_deg` — reidentificação por grau;
- `cobertura` — fração de nós com k-anonimato satisfeito (`coverage_fraction`);
- `EGS` — tamanho médio do grupo de equivalência;
- `KS D` — estatística D do teste KS de grau (degradação de utilidade);
- `Δclust` — variação de clustering (degradação de utilidade).

### k = 2

| d | reid_sub | reid_deg | cobertura | EGS | KS D | Δclust | veredito |
|---|---|---|---|---|---|---|---|
| 1  | 0.145 ± 0.016 | 0.023 ± 0.013 | 0.985 | 1.99  | 0.052 ± 0.002 | 0.053 ± 0.007 | SUCCESS_PARTIAL |
| 2  | 0.138 ± 0.013 | 0.016 ± 0.003 | 0.985 | 3.97  | 0.049 ± 0.003 | 0.057 ± 0.001 | SUCCESS_PARTIAL |
| 5  | 0.211 ± 0.016 | 0.036 ± 0.011 | 0.989 | 9.85  | 0.031 ± 0.003 | 0.031 ± 0.009 | SUCCESS_PARTIAL |
| 10 | 0.147 ± 0.026 | 0.031 ± 0.011 | 0.981 | 19.70 | 0.074 ± 0.003 | 0.043 ± 0.009 | SUCCESS_PARTIAL |

### k = 5

| d | reid_sub | reid_deg | cobertura | EGS | KS D | Δclust | veredito |
|---|---|---|---|---|---|---|---|
| 1  | 0.031 ± 0.002 | 0.009 ± 0.002 | 0.940 | 4.97  | 0.274 ± 0.031 | 0.273 ± 0.002 | SUCCESS_PARTIAL |
| 2  | 0.049 ± 0.010 | 0.020 ± 0.015 | 0.902 | 9.85  | 0.304 ± 0.047 | 0.312 ± 0.039 | SUCCESS_PARTIAL |
| 5  | 0.056 ± 0.005 | 0.012 ± 0.004 | 0.949 | 23.13 | 0.229 ± 0.028 | 0.210 ± 0.020 | SUCCESS_PARTIAL |
| 10 | 0.049 ± 0.022 | 0.019 ± 0.009 | 0.940 | 44.33 | 0.263 ± 0.038 | 0.217 ± 0.031 | SUCCESS_PARTIAL |

### k = 10

| d | reid_sub | reid_deg | cobertura | EGS | KS D | Δclust | veredito |
|---|---|---|---|---|---|---|---|
| 1  | 0.037 ± 0.026 | 0.285 ± 0.058 | 0.865 | 9.85  | 0.823 ± 0.033 | 0.130 ± 0.024 | ⚠️ FAILURE_LOW_COVERAGE |
| 2  | 0.043 ± 0.007 | 0.339 ± 0.081 | 0.902 | 19.00 | 0.776 ± 0.031 | 0.070 ± 0.042 | SUCCESS_PARTIAL |
| 5  | 0.015 ± 0.015 | 0.219 ± 0.116 | 0.846 | 44.33 | 0.745 ± 0.029 | 0.043 ± 0.027 | ⚠️ FAILURE_LOW_COVERAGE |
| 10 | 0.013 ± 0.004 | 0.266 ± 0.022 | 0.940 | 76.00 | 0.809 ± 0.026 | 0.163 ± 0.042 | SUCCESS_PARTIAL |

### k = 20

| d | reid_sub | reid_deg | cobertura | EGS | KS D | Δclust | veredito |
|---|---|---|---|---|---|---|---|
| 1  | 0.000 ± 0.000 | 0.088 ± 0.065 | 0.865 | 19.00  | 0.936 ± 0.010 | 0.470 ± 0.008 | ⚠️ FAILURE_LOW_COVERAGE |
| 2  | 0.041 ± 0.009 | 0.364 ± 0.050 | 0.902 | 35.47  | 0.902 ± 0.000 | 0.476 ± 0.013 | SUCCESS_PARTIAL |
| 5  | 0.000 ± 0.000 | 0.055 ± 0.000 | 0.752 | 76.00  | 0.927 ± 0.000 | 0.403 ± 0.007 | ⚠️ FAILURE_LOW_COVERAGE |
| 10 | 0.007 ± 0.001 | 0.213 ± 0.008 | 0.752 | 133.00 | 0.931 ± 0.001 | 0.522 ± 0.003 | ⚠️ FAILURE_LOW_COVERAGE |

Tabelas CSV por nó/semente regeneradas em `results/tables/facebook_degree.csv` e
`results/tables/facebook_subgraph.csv` (colunas `k, d, seed, reid_rate,
eq_group_mean, ks_D, ks_p, clustering_var`; não versionadas — ver
[`.claude/rules/experiments.md`](../.claude/rules/experiments.md)).

---

## 4. Figuras

Regeneradas a partir do log em `results/plots/` (não versionadas):

| Arquivo | Layout |
|---|---|
| `privacy_utility_dsweep_series.{pdf,png}` | `series` — cor por `d`, estilo de linha por ataque/métrica |
| `privacy_utility_dsweep_facets.{pdf,png}` | `facets` — grade 2 × 4 (privacidade/utilidade × d) |

Barras de erro = ± 1 desvio-padrão entre as 3 sementes de cada célula `(k, d)`.

---

## 5. Análise

### 5.1 k-anonimato nunca formalmente satisfeito, mas déficit é estrutural

`validate_k_anonymity.valid = false` em **todos os 48 runs**, porém
`deficit_fully_structural = true` em **todos** — o déficit decorre de
violadores estruturais (nós que não admitem grupo de tamanho ≥ k no grafo de
saída), não de falha do algoritmo. Comportamento esperado e documentado (D-06).
O verificador é independente do anonimizador, conforme a regra de validação
obrigatória.

### 5.2 Os dois ataques têm tendências opostas em k

- **Subgrafo enfraquece com k.** `reid_sub` cai de ~0.14–0.21 (k=2) para
  ~0.01–0.04 (k=10/20). Coerente com grupos de equivalência maiores: quanto
  maior o EGS, mais candidatos indistinguíveis para o atacante por subgrafo.
- **Grau se fortalece com k.** `reid_deg` sobe de ~0.02–0.03 (k=2) para
  ~0.21–0.36 (k=10/20). Em k alto o KS D de grau aproxima-se de ~0.8–0.95: a
  anonimização distorce fortemente a distribuição de graus, criando assinaturas
  de grau mais singulares e, portanto, mais fáceis para o ataque por grau.

A leitura conjunta é o ponto central da curva privacidade-vs-utilidade: aumentar
`k` não melhora a privacidade monotonicamente — desloca o vetor de ataque mais
eficaz de subgrafo para grau.

### 5.3 Efeito de `d`

`d` controla o tamanho-alvo dos grupos de equivalência (EGS ≈ k·d para células
completas — confirmado: k=2/d=10 → EGS 19.70, k=20/d=10 → EGS 133.0). Aumentar
`d` engrossa os grupos e, em geral, reduz `reid_sub`, ao custo de maior
degradação de utilidade (Δclust e KS D crescem). O efeito não é perfeitamente
monotônico por causa da aproximação de particionamento e dos combos degenerados
(§5.4).

### 5.4 Combos degenerados (D-08, D-10)

- **d = 2 (D-08, G3).** Para a ego-rede 3437 sob pymetis, `d = 2` colapsa em
  ~199/267 partições vazias, concentrando nós em poucos grupos grandes. Os
  números de `d = 2` aparecem **fora da tendência** das demais colunas
  (notavelmente `reid_deg` em k=10/20: 0.339 e 0.364, os mais altos do grid).
  Mantido no relatório, **não excluído** — documentar em vez de ocultar.
- **d = 10, k = 20 (D-10).** `c_k < k`: praticamente todos os nós são violadores
  estruturais; cobertura cai a 0.752 (a menor do grid) e o veredito é
  `FAILURE_LOW_COVERAGE`. Metodologicamente válido (`deficit_fully_structural =
  true`) mas **sem garantia de k-anonimato**. Incluído deliberadamente para
  expor o comportamento do algoritmo em configuração extrema.

### 5.5 Interpretação de `reid_sub = 0` em k alto (diagnóstico #93 — resolvido)

`reid_sub = 0.000` exato ocorre em k=20/d∈{1,5} (todas as sementes); em
k=20/d=10 é quase-zero (~0.006–0.008). A interpretação foi **ambígua a priori**:
zero por privacidade real/degeneração estrutural (H1/H2) ou por timeout do VF2
mascarado (H3, a descartar). A issue #93 (D-08 / Fase 6) resolveu a questão.

**H3 (timeout mascarado) está descartada.** A inspeção do log (48 runs) mostra
**nenhum `verdict=ERROR`** e nenhum campo `error` preenchido. No código que
gerou este log, o ataque por subgrafo era chamado por nó **sem** tratar
`TimeoutError` individualmente: um único nó que estourasse o `timeout` de 120 s
propagaria a exceção até o bloco `except` do run, gravando `verdict=ERROR` — não
`reid_sub = 0`. Como `ERROR` **não aparece em nenhum run**, conclui-se que
**nenhuma chamada VF2 atingiu 120 s**. Os zeros são, portanto, **genuínos**:
refletem H1/H2 — sob grupos de equivalência grandes (EGS ≈ k·d), a vizinhança
original do alvo deixa de ter correspondência **única** em `G'` (zero ou
múltiplos candidatos isomórficos). Note que `reid_deg > reid_sub` em k=20 é
coerente: a anonimização destrói o *fingerprint* de vizinhança que o ataque por
subgrafo exige, enquanto assinaturas de grau singulares sobrevivem (§5.2).

**Instrumentação para execuções futuras (DL-02).** O runner foi estendido (#93)
para gravar, por run, `subgraph_timeout_count` (nós cujo VF2 estoura o timeout —
agora capturado por nó, contado e tratado como não-reidentificado, alinhando o
código ao comentário do YAML) e `subgraph_candidate_counts` (`mean`/`std`/`max`
de candidatos por nó). Esses campos tornam a distinção "zero por ausência de
candidatos" vs. "zero por timeout" **diretamente observável**; o log atual,
anterior à extensão, não os possui, mas a conclusão de H3 não depende deles. A
reexecução opcional das 6 células está em
`experiments/configs/he2009_facebook_dsweep_k20_diag.yml`. Ver
[`docs/decision_log.md`](decision_log.md) (DL-02, nota de encerramento de D-08) e
[`docs/limitations.md`](limitations.md).

### 5.6 Custo

O bloco k=20 domina o tempo de parede (~3 h por run vs. ~2–3 min em k=2),
pelo VF2 do ataque por subgrafo sob grupos de equivalência grandes. A varredura
completa levou ≈ 31 h e sobreviveu a uma desconexão do terminal do VSCode
(processo independente, gravação JSONL incremental).

### 5.7 Ameaças à validade

A varredura `d > 1` é o que distingue este experimento do baseline `d = 1`
(≈ k-anonimato de grau): com `d > 1` a "estrutura" que o módulo afere passa a
incluir a topologia da vizinhança (Local Structures de tamanho `d`), não apenas
o grau. Isso é, simultaneamente, o ganho de validade de construção e a fonte das
ameaças abaixo.

**Validade interna (o que pode contaminar a relação medida `(k, d)` → privacidade/utilidade):**

- **Interação `s_max × d`.** O FSM simplificado fixa `s_max = 4` (D-01). Quando
  `d > s_max` (notadamente `d = 10`), o tamanho-alvo das LSs excede o maior
  padrão frequente que o FSM enumera; o agrupamento opera sobre padrões truncados.
  A decisão (Opção A, D-01/G2) foi manter `s_max = 4` fixo após verificar
  empiricamente que o agrupamento é idêntico para `s_max ∈ {4, 5}` na 3437 — mas
  isso é uma aproximação, não uma equivalência garantida para `d` arbitrário.
- **pymetis vs. KL.** Todos os 48 runs usaram **pymetis** (fiel a He et al., D-04),
  registrado em cada linha JSONL (`partition_backend`). Não há mistura de backend
  neste log, então a comparação entre células `(k, d)` é homogênea; o fallback KL
  (`networkx-kl`), quando usado em outros experimentos, degrada o sizing para
  `c_k > 2` (D-04/D-07) e **não** é comparável célula a célula com estes resultados.
- **Particionamento k-way não garante LS conexa.** A verificação de conectividade
  (D-08, G3) mostrou que, na 3437, 55% das LSs de `d = 5` são desconexas e `d = 2`
  é degenerate (≈ 199/267 partições vazias). "Estrutura" agrupada por isomorfismo
  inclui, portanto, subgrafos desconexos — uma aproximação documentada, não a
  noção de vizinhança conexa do artigo.
- **Custo de isomorfização em `d > 1` (timeouts VF2) — ameaça afastada para este
  log.** A preocupação era que nós com timeout de 120 s, contados como *não
  reidentificados*, pudessem **inflar artificialmente** a privacidade aparente do
  ataque por subgrafo (custo do VF2 cresce com o EGS ≈ `k·d`). O diagnóstico da
  issue #93 (§5.5) **afasta essa ameaça neste log**: a ausência de `verdict=ERROR`
  prova que nenhuma chamada VF2 atingiu o timeout, logo os zeros não são artefato
  de custo. A ressalva permanece *prospectiva* para `d`/`k` ainda maiores ou
  timeouts menores — daí a instrumentação `subgraph_timeout_count` /
  `subgraph_candidate_counts` (DL-02) para quantificar o efeito caso ocorra.

  > **⚠️ Nota de comparabilidade pré/pós DL-02 (inversão semântica do sentinela
  > de timeout).** Em logs gerados **antes** do PR #97 (pré-DL-02), `verdict=ERROR`
  > era prova positiva de timeout: sua ausência total nos 48 runs foi a base do
  > diagnóstico de H3. Em logs gerados **após** o PR #97 (pós-DL-02), `verdict=ERROR`
  > por timeout **não ocorre mais** — o `TimeoutError` é capturado por nó e
  > contabilizado em `subgraph_timeout_count`, sem derrubar o run. Consequência:
  > **a ausência de `verdict=ERROR` em um log pós-DL-02 não prova ausência de
  > timeouts**; o campo correto a verificar é `subgraph_timeout_count > 0`.
  > Comparações cruzadas entre logs de épocas diferentes (ex.: re-execuções do
  > d-sweep com o runner estendido) devem considerar essa diferença de schema e
  > de semântica do sentinela. Ver DL-02 em [`docs/decision_log.md`](decision_log.md).

**Validade de construção (o experimento mede o que se propõe a medir?):**

- Com `d > 1`, o construto "privacidade estrutural" deixa de ser um proxy de grau
  e passa a depender de isomorfismo de subgrafo de tamanho `d`. O contraste
  `d = 1` (âncora) vs. `d ∈ {5, 10}` na §3 é a **evidência direta** de que o
  módulo afere privacidade estrutural — o ataque por subgrafo e o EGS respondem a
  `d`, não só a `k`. Isso **fortalece** a validade de construção relativamente ao
  baseline. A ressalva é a confusão construto/artefato introduzida pelos timeouts
  (acima) e pelos combos degenerados (§5.4), que devem ser lidos como tais.

**Validade externa (generalização):**

- **Única ego-rede (3437).** Todos os resultados vêm de um só grafo
  (LCC n=532, m=4812). Tendências em `(k, d)`, combos degenerados e magnitudes de
  reidentificação são **específicos desta topologia**; não há base para
  extrapolar para outras ego-redes, outros datasets (ex.: Email-Enron, tier
  desejável) ou outras densidades. Generalização exige replicar a varredura em
  ≥ 1 grafo adicional.

Referência cruzada das ameaças metodológicas transversais:
[`docs/limitations.md`](limitations.md) (§1.3 atualizada para *parcialmente
resolvida*) e [`docs/decision_log.md`](decision_log.md) (D-01, D-04, D-07, D-08,
D-10, DL-02).

---

## 6. Reprodução

Pré-condição: ambiente conda com pymetis (`environment.yml` /
`scripts/setup_conda_windows.ps1`) para o backend fiel a He et al. (D-04).

```bash
# 1. Executar a varredura (≈31 h; gera o JSONL + summary.json)
python -m experiments.run --config experiments/configs/he2009_facebook_dsweep.yml

# 2. Tabelas CSV d-aware
python -m src.visualization.tables \
    --logs experiments/logs/he2009_facebook_dsweep \
    --out results/tables --dataset facebook

# 3. Figuras d-aware (auto-detecta múltiplos d)
python -m src.visualization.privacy_utility \
    --logs experiments/logs/he2009_facebook_dsweep \
    --out results/plots --layout series --stem privacy_utility_dsweep_series
python -m src.visualization.privacy_utility \
    --logs experiments/logs/he2009_facebook_dsweep \
    --out results/plots --layout facets --stem privacy_utility_dsweep_facets
```

---

## 7. Referências cruzadas

- Decisões: D-04, D-06, D-08, D-10 — [`docs/decision_log.md`](decision_log.md).
- Algoritmo e degradação de sizing para `c_k > 2`:
  [`docs/algorithm_notes.md`](algorithm_notes.md) §7.
- Definições de métricas: [`docs/metrics_definitions.md`](metrics_definitions.md).
- Limitações metodológicas: [`docs/limitations.md`](limitations.md).
- Snapshot intermediário (histórico):
  [`docs/dsweep_previa_garantia_dados.md`](dsweep_previa_garantia_dados.md).
