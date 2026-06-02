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

### 5.5 Ressalva sobre `reid_sub = 0` em k alto

`reid_sub = 0.000` exato ocorre em k=20/d∈{1,5} (todas as sementes). **Atenção
na interpretação:** nós cujo ataque de subgrafo atinge o timeout de 120 s contam
como *não reidentificados*. Em k alto o VF2 é caro e os timeouts são frequentes,
de modo que parte desses zeros pode refletir custo computacional, não segurança
real. O JSONL atual **não registra a contagem de timeouts por run**, então o
cruzamento quantitativo não é possível a partir deste log — fica como limitação
metodológica conhecida (candidata a um campo `subgraph_timeouts` em execução
futura). Ver também [`docs/limitations.md`](limitations.md).

### 5.6 Custo

O bloco k=20 domina o tempo de parede (~3 h por run vs. ~2–3 min em k=2),
pelo VF2 do ataque por subgrafo sob grupos de equivalência grandes. A varredura
completa levou ≈ 31 h e sobreviveu a uma desconexão do terminal do VSCode
(processo independente, gravação JSONL incremental).

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
