# Resultados do experimento baseline — Facebook Ego-Nets (He et al. 2009)

> Tabelas geradas de `experiments/logs/he2009_facebook_baseline_pymetis/`.
> Issue #211 (E1) — reexecução com motor pymetis (substitui KL para o artigo).
> Resultados KL originais (issue #23) preservados na
> [seção histórica](#resultados-historicos-kl--issue-23) ao final deste arquivo.

**Dataset:** Facebook Ego-Net 3437 (n=532, m=4812)
**Sementes:** 42, 1337, 2718
**Algoritmo:** He et al. (2009), d=1, sigma=0.5
**Motor de particionamento:** pymetis (multilevel k-way, Karypis & Kumar) — fiel a He et al. (2009). Ver [D-19](decision_log.md#d-19).
**Ataques:** grau (tolerance=0) + subgrafo (hop=1, WL-bucketing)

---

## Leitura-chave — `d=1` afere k-anonimato de grau (achado B1)

> **Síntese interpretativa (achado B1).** Neste baseline `d=1` os resultados
> rotulados como "He et al. *structure-aware*" equivalem a **k-anonimato de
> grau**. Com `d=1`, a estrutura local (Local Structure) de cada nó é um subgrafo
> de um único nó e o isomorfismo de vizinhança reduz-se a **igualdade de grau** —
> a propriedade *structure-aware* que distingue He et al. (2009) de Liu & Terzi
> **não** é exercida aqui.

A propriedade estrutural propriamente dita só é exercida no **d-sweep**
(`d ∈ {5, 10}`, ver [`results_dsweep.md`](results_dsweep.md)). **O contraste
`d=1` vs. `d ∈ {5, 10}` é a evidência empírica de que o módulo afere privacidade
estrutural — e deve ser apresentado como tal, não como detalhe de
configuração.** Esta ressalva é ortogonal à do motor de particionamento abaixo:
uma trata do *parâmetro* `d` (grau vs. estrutura), a outra do *motor* que
executou o particionamento (KL vs. pymetis); ambas valem para este baseline.

**Referências:** D-02 em [`decision_log.md`](decision_log.md); `algorithm_notes.md`
§5.3, §6.5, §9.1; `limitations.md` §1.3; configs `he2009_facebook_*` com `d=1`.

---

## Reexecução com pymetis — D-19

> **Substituição para o artigo (issue #211 / D-19).** A execução original
> (issue #23, 2026-05-23) usou o fallback Kernighan-Lin por ausência de pymetis
> no ambiente à época. O Enron foi executado com pymetis (#126). Para eliminar
> essa ameaça à validade interna, este baseline foi reexecutado com
> `allow_kl_fallback: false` (config `he2009_facebook_baseline_pymetis.yml`),
> garantindo backend=pymetis em 12/12 runs.

**Diferenças observadas em relação ao run KL.** Embora d=1 degenere
localmente em k-anonimato de grau, o motor de particionamento afeta a
cobertura e os grupos formados. Com pymetis:
- k=2: cobertura caiu de 1.0000 (SUCCESS_FULL) para 0.9850 (SUCCESS_PARTIAL),
  com 8 nós residuais em grupos incompletos; rr_subgrafo: 0.7914 → 0.1454.
- k=5: cobertura de 0.9962 para 0.9398; rr_subgrafo: 0.4060 → 0.0307.
- k=10 e k=20: passaram de SUCCESS_PARTIAL para FAILURE_LOW_COVERAGE (cobertura
  0.8647), indicando que pymetis produz grupos menores/menos balanceados neste grafo.

**Validade do marco 29/05.** A validação formal de k-anonimato (DL-01) foi
executada sobre o run KL e permanece válida para aquele experimento — o marco
29/05 não é retificado. Este run pymetis é o dado **canônico para comparação
inter-dataset no artigo**; o run KL fica arquivado como referência histórica.

**Referências:** D-04 (motor de particionamento); D-19 (decisão de substituição
para o artigo) em `docs/decision_log.md`; config
`experiments/configs/he2009_facebook_baseline_pymetis.yml`.

---

## Validade externa — dataset único (achado B2)

> **Ressalva de generalização (achado B2).** Todos os números deste baseline vêm
> de uma **única** ego-rede do Facebook (a 3437; LCC n=532, m=4812). Nem o
> dataset secundário **contingente** previsto (Email-Enron, tier desejável) nem a
> varredura de **múltiplas** ego-redes
> (`preprocessing_mode = multiple_egonets`, chave `egonet_ids` em
> `config_example.yml:46`) chegaram a ser executados.

Os resultados — `coverage_fraction`, vereditos e métricas de utilidade (KS-D,
Δclust) — são válidos **para esta topologia específica**; não há base empírica
para extrapolá-los a outras ego-redes, ao Enron ou a outras densidades de rede.
A generalização permanece em aberto e exige replicar o pipeline em ≥ 1 grafo
adicional. Esta ressalva é ortogonal às demais: trata da *amostra de
redes* (uma só), não do *parâmetro* `d` (B1) nem do *motor* de particionamento (D-19).

**Referências:** `scope.md` §3 (tiers de dataset [M]/[D]/[A]); `limitations.md`
§1.1 (dataset restrito); `config_example.yml:46` (`egonet_ids` previsto, não
usado).

---

## Tabela bruta por (k, semente) — run pymetis (issue #211)

| k | seed | Veredito | coverage_fraction | rr_degree | rr_subgraph | EG_mean | EG_median | KS_D | KS_p | clust_var |
|---|------|----------|-------------------|-----------|-------------|--------|-----------|------|------|-----------|
| 2 | 42 | SUCCESS_PARTIAL | 0.9850 | 0.0056 | 0.1617 | 1.99 | 0 | 0.0508 | 0.5001 | 0.0440 |
| 2 | 1337 | SUCCESS_PARTIAL | 0.9850 | 0.0282 | 0.1241 | 1.99 | 0 | 0.0508 | 0.5001 | 0.0539 |
| 2 | 2718 | SUCCESS_PARTIAL | 0.9850 | 0.0357 | 0.1504 | 1.99 | 0 | 0.0545 | 0.4083 | 0.0609 |
| 5 | 42 | SUCCESS_PARTIAL | 0.9398 | 0.0113 | 0.0282 | 4.97 | 0 | 0.2989 | 0.0000 | 0.2739 |
| 5 | 1337 | SUCCESS_PARTIAL | 0.9398 | 0.0075 | 0.0320 | 4.97 | 0 | 0.2312 | 0.0000 | 0.2710 |
| 5 | 2718 | SUCCESS_PARTIAL | 0.9398 | 0.0094 | 0.0320 | 4.97 | 0 | 0.2932 | 0.0000 | 0.2756 |
| 10 | 42 | FAILURE_LOW_COVERAGE | 0.8647 | 0.3609 | 0.0508 | 9.85 | 0 | 0.7951 | 0.0000 | 0.1030 |
| 10 | 1337 | FAILURE_LOW_COVERAGE | 0.8647 | 0.2744 | 0.0602 | 9.85 | 0 | 0.8045 | 0.0000 | 0.1261 |
| 10 | 2718 | FAILURE_LOW_COVERAGE | 0.8647 | 0.2199 | 0.0000 | 9.85 | 0 | 0.8684 | 0.0000 | 0.1613 |
| 20 | 42 | FAILURE_LOW_COVERAGE | 0.8647 | 0.0338 | 0.0000 | 19.00 | 0 | 0.9474 | 0.0000 | 0.4639 |
| 20 | 1337 | FAILURE_LOW_COVERAGE | 0.8647 | 0.1805 | 0.0000 | 19.00 | 0 | 0.9229 | 0.0000 | 0.4649 |
| 20 | 2718 | FAILURE_LOW_COVERAGE | 0.8647 | 0.0508 | 0.0000 | 19.00 | 0 | 0.9380 | 0.0000 | 0.4821 |

> **Nota — EG_median=0.** O campo `median` no JSONL inclui nós não cobertos
> (EGS=0), o que puxa a mediana para zero mesmo quando a maioria dos nós está
> em grupos de tamanho ≥k. Ver `equivalence_group_size.mean` para a tendência
> central dos nós cobertos.

---

## Agregação por k (média ± desvio-padrão, 3 sementes) — run pymetis

| k | Vereditos | coverage_fraction | rr_degree (mean±std) | rr_subgraph (mean±std) | EG_mean (mean±std) | KS_D (mean±std) | clust_var (mean±std) |
|---|-----------|-------------------|----------------------|----------------------|-------------------|-----------------|---------------------|
| 2 | SUCCESS_PARTIAL | 0.9850±0.0000 | 0.0232±0.0157 | 0.1454±0.0193 | 1.99±0.00 | 0.0520±0.0022 | 0.0529±0.0085 |
| 5 | SUCCESS_PARTIAL | 0.9398±0.0000 | 0.0094±0.0019 | 0.0307±0.0022 | 4.97±0.00 | 0.2744±0.0375 | 0.2735±0.0023 |
| 10 | FAILURE_LOW_COVERAGE | 0.8647±0.0000 | 0.2851±0.0711 | 0.0370±0.0324 | 9.85±0.00 | 0.8227±0.0399 | 0.1301±0.0294 |
| 20 | FAILURE_LOW_COVERAGE | 0.8647±0.0000 | 0.0883±0.0802 | 0.0000±0.0000 | 19.00±0.00 | 0.9361±0.0123 | 0.4703±0.0102 |

---

## Interpretação (run pymetis)

- **Ataque por grau** (rr_degree): decresce de k=2→k=5 (0.023→0.009), sobe em
  k=10 (0.285 — artefato de FAILURE_LOW_COVERAGE: nós residuais em grupos únicos
  ficam vulneráveis), e cai novamente em k=20 (0.088). O comportamento em k=10/20
  reflete cobertura insuficiente (~86%), não degradação dos grupos cobertos.

- **Ataque por subgrafo** (rr_subgraph): decresce monotonicamente com k:
  0.145 → 0.031 → 0.037 → 0.000. O sinal principal é o gap **rr_sub ≫ rr_deg**
  em k=2 (~6×), evidenciando que k-anonimato de grau (d=1) não protege contra
  ataque por subgrafo.

- **Cobertura:** k=2 e k=5 têm SUCCESS_PARTIAL (98,5% e 93,9%); k=10 e k=20
  têm FAILURE_LOW_COVERAGE (86,5%). Pymetis produz partições com menos balanço
  neste grafo do que o KL original, resultando em mais nós residuais para k≥10.

- **Achado B1 (d=1 afere k-anonimato de grau) permanece válido**: a propriedade
  matemática é independente do motor; o que muda são os valores numéricos das
  taxas de ataque, não o sinal qualitativo.

---

## Resultados históricos KL — issue #23

> Resultados do run original (Kernighan-Lin fallback, issue #23, 2026-05-23),
> arquivados como referência. **Não usar para comparação inter-dataset no artigo**
> — use os números pymetis acima (D-19).
> Log: `experiments/logs/he2009_facebook_baseline/he2009_facebook_baseline.jsonl`

| k | seed | Veredito | coverage_fraction | rr_degree | rr_subgraph | EG_mean | EG_median | KS_D | KS_p | clust_var |
|---|------|----------|-------------------|-----------|-------------|--------|-----------|------|------|-----------|
| 2 | 42 | SUCCESS_FULL | 1.0000 | 0.0263 | 0.7914 | 2.00 | 2 | 0.0000 | 1.0000 | 0.0000 |
| 2 | 1337 | SUCCESS_FULL | 1.0000 | 0.0263 | 0.7914 | 2.00 | 2 | 0.0000 | 1.0000 | 0.0000 |
| 2 | 2718 | SUCCESS_FULL | 1.0000 | 0.0263 | 0.7914 | 2.00 | 2 | 0.0000 | 1.0000 | 0.0000 |
| 5 | 42 | SUCCESS_PARTIAL | 0.9962 | 0.0075 | 0.4192 | 4.97 | 5 | 0.0451 | 0.6516 | 0.0527 |
| 5 | 1337 | SUCCESS_PARTIAL | 0.9962 | 0.0113 | 0.3910 | 4.97 | 5 | 0.0564 | 0.3664 | 0.0783 |
| 5 | 2718 | SUCCESS_PARTIAL | 0.9962 | 0.0056 | 0.4079 | 4.97 | 5 | 0.0432 | 0.7032 | 0.0701 |
| 10 | 42 | SUCCESS_PARTIAL | 0.9962 | 0.0094 | 0.1259 | 9.85 | 10 | 0.2274 | 0.0000 | 0.1554 |
| 10 | 1337 | SUCCESS_PARTIAL | 0.9962 | 0.0357 | 0.1767 | 9.85 | 10 | 0.2500 | 0.0000 | 0.1614 |
| 10 | 2718 | SUCCESS_PARTIAL | 0.9962 | 0.0226 | 0.1165 | 9.85 | 10 | 0.2293 | 0.0000 | 0.1556 |
| 20 | 42 | SUCCESS_PARTIAL | 0.9774 | 0.0752 | 0.0000 | 19.70 | 20 | 0.6485 | 0.0000 | 0.0903 |
| 20 | 1337 | SUCCESS_PARTIAL | 0.9774 | 0.1222 | 0.0000 | 19.70 | 20 | 0.6504 | 0.0000 | 0.0882 |
| 20 | 2718 | SUCCESS_PARTIAL | 0.9774 | 0.0996 | 0.0000 | 19.70 | 20 | 0.6485 | 0.0000 | 0.0926 |

**Agregação KL por k:**

| k | Vereditos | coverage_fraction | rr_degree (mean±std) | rr_subgraph (mean±std) | EG_mean (mean±std) | KS_D (mean±std) | clust_var (mean±std) |
|---|-----------|-------------------|----------------------|----------------------|-------------------|-----------------|---------------------|
| 2 | SUCCESS_FULL | 1.0000±0.0000 | 0.0263±0.0000 | 0.7914±0.0000 | 2.00±0.00 | 0.0000±0.0000 | 0.0000±0.0000 |
| 5 | SUCCESS_PARTIAL | 0.9962±0.0000 | 0.0081±0.0029 | 0.4060±0.0142 | 4.97±0.00 | 0.0482±0.0071 | 0.0670±0.0131 |
| 10 | SUCCESS_PARTIAL | 0.9962±0.0000 | 0.0226±0.0132 | 0.1397±0.0324 | 9.85±0.00 | 0.2356±0.0125 | 0.1575±0.0034 |
| 20 | SUCCESS_PARTIAL | 0.9774±0.0000 | 0.0990±0.0235 | 0.0000±0.0000 | 19.70±0.00 | 0.6491±0.0011 | 0.0904±0.0022 |
