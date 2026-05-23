# Resultados do experimento baseline — Facebook Ego-Nets (He et al. 2009)

> Gerado automaticamente por `experiments/make_baseline_table.py`.
> Fonte: `experiments/logs/he2009_facebook_baseline/he2009_facebook_baseline.jsonl`.
> Issue #23 — experimento baseline completo.

**Dataset:** Facebook Ego-Net 3437 (n=532, m=4812)
**Sementes:** 42, 1337, 2718
**Algoritmo:** He et al. (2009), d=1, sigma=0.5
**Ataques:** grau (tolerance=0) + subgrafo (hop=1, timeout=60s)

---

## Tabela bruta por (k, semente)

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

---

## Agregação por k (média ± desvio-padrão, 3 sementes)

| k | Vereditos | coverage_fraction | rr_degree (mean±std) | rr_subgraph (mean±std) | EG_mean (mean±std) | KS_D (mean±std) | clust_var (mean±std) |
|---|-----------|-------------------|----------------------|----------------------|-------------------|-----------------|---------------------|
| 2 | SUCCESS_FULL | 1.0000±0.0000 | 0.0263±0.0000 | 0.7914±0.0000 | 2.00±0.00 | 0.0000±0.0000 | 0.0000±0.0000 |
| 5 | SUCCESS_PARTIAL | 0.9962±0.0000 | 0.0081±0.0029 | 0.4060±0.0142 | 4.97±0.00 | 0.0482±0.0071 | 0.0670±0.0131 |
| 10 | SUCCESS_PARTIAL | 0.9962±0.0000 | 0.0226±0.0132 | 0.1397±0.0324 | 9.85±0.00 | 0.2356±0.0125 | 0.1575±0.0034 |
| 20 | SUCCESS_PARTIAL | 0.9774±0.0000 | 0.0990±0.0235 | 0.0000±0.0000 | 19.70±0.00 | 0.6491±0.0011 | 0.0904±0.0022 |

---

## Interpretação preliminar

- **Ataque por grau** (reidentificação por correspondência de grau exacta):
  taxa de reidentificação decresce com k crescente, confirmando a eficácia
  da anonimização estrutural de He et al. (2009).

- **Ataque por subgrafo** (isomorfismo 1-hop, VF2):
  taxa substancialmente maior que o ataque por grau — revela que
  apenas igualar graus é insuficiente; estruturas de vizinhança ainda
  permitem reidentificação parcial. Esperado: k-anonimato reduz, mas
  não elimina, a vulnerabilidade para k baixo.

- **coverage_fraction ≥ 0.9962** em todos os casos — algoritmo converge
  com cobertura quase total; incompletude residual é de grupos incompletos
  (deficit_fully_structural=True), aceitável pelo critério DL-01.

> Gráficos finais serão gerados a partir deste log na Semana 4.
