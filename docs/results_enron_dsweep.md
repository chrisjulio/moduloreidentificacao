# Resultados — d-sweep Enron (issue #214)

> Gerado automaticamente por `experiments/make_enron_dsweep_table.py`.
> Fonte principal: `experiments/logs/he2009_enron_dsweep/he2009_enron_dsweep.jsonl`.
> Âncora d=1: `experiments/logs/he2009_enron_secondary/` (carregado como âncora d=1).
> Issue #214 (V1) — script de resultados d-sweep Enron.
> Desbloqueia V2 e D5.

**Dataset:** Email-Enron (SNAP), projeção OR (D-11); LCC **n=33.696 nós, m=180.811 arestas** (grau médio ≈ 10,7).
**Sementes:** 42, 1337, 2718
**Algoritmo:** He et al. (2009), sigma=0.5, s_max=4, isomorphism_mode=add_or_delete
**Motor:** pymetis (todos os runs — DL-07 excluiu KL fallback)
**Ataques:** grau (tolerance=0) + subgrafo (hop=1, WL-bucketing D-16)
**Grid d-sweep:** k ∈ {2, 5, 10, 20} × d ∈ {1, 2, 5, 10} × 3 sementes = 36 runs (+ 12 runs d=1 do secundário = 48 total)

---

## 1. Cobertura do grid

| k\d | d=1 | d=2 | d=5 | d=10 |
|-----|--------|--------|--------|--------|
|  2  | ✅✅✅ | ✅✅✅ | ✅✅✅ | ✅✅✅ |
|  5  | ✅✅✅ | ✅✅✅ | ✅✅✅ | ✅✅✅ |
|  10  | ✅✅✅ | ✅✅✅ | ✅✅✅ | ✅✅✅ |
|  20  | ✅✅✅ | ✅✅✅ | ✅✅✅ | ✅✅✅ |

Vereditos (48 runs): **SUCCESS_PARTIAL**: 48.

---

## 2. Resultados consolidados

Valores `média ± desvio-padrão` sobre as 3 sementes de cada célula `(k, d)`.

- `reid_sub` — reidentificação por **subgrafo** (métrica canônica);
- `reid_deg` — reidentificação por grau;
- `cobertura` — `coverage_fraction`;
- `EGS` — tamanho médio do grupo de equivalência;
- `KS D` — estatística D do teste KS de grau (degradação de utilidade);
- `Δclust` — variação de clustering (degradação de utilidade).

### k = 2

| d | reid_sub | reid_deg | cobertura | EGS | KS D | Δclust | veredito |
|---|---|---|---|---|---|---|---|
| 1 | 0.124±0.001 | 0.003±0.000 | 0.9999 | 2.00±0.00 | 0.038±0.001 | 0.017±0.002 | SUCCESS_PARTIAL |
| 2 | 0.098±0.000 | 0.003±0.000 | 0.9996 | 4.00±0.00 | 0.050±0.001 | 0.015±0.001 | SUCCESS_PARTIAL |
| 5 | 0.080±0.001 | 0.004±0.000 | 0.9997 | 10.00±0.00 | 0.069±0.001 | 0.018±0.002 | SUCCESS_PARTIAL |
| 10 | 0.053±0.001 | 0.003±0.000 | 0.9994 | 19.99±0.00 | 0.091±0.000 | 0.045±0.006 | SUCCESS_PARTIAL |

### k = 5

| d | reid_sub | reid_deg | cobertura | EGS | KS D | Δclust | veredito |
|---|---|---|---|---|---|---|---|
| 1 | 0.102±0.002 | 0.002±0.000 | 0.9994 | 5.00±0.00 | 0.027±0.001 | 0.051±0.003 | SUCCESS_PARTIAL |
| 2 | 0.076±0.001 | 0.003±0.000 | 0.9992 | 9.99±0.00 | 0.041±0.001 | 0.111±0.002 | SUCCESS_PARTIAL |
| 5 | 0.049±0.000 | 0.002±0.000 | 0.9992 | 24.96±0.00 | 0.045±0.001 | 0.124±0.002 | SUCCESS_PARTIAL |
| 10 | 0.028±0.001 | 0.003±0.000 | 0.9994 | 49.85±0.00 | 0.057±0.003 | 0.158±0.003 | SUCCESS_PARTIAL |

### k = 10

| d | reid_sub | reid_deg | cobertura | EGS | KS D | Δclust | veredito |
|---|---|---|---|---|---|---|---|
| 1 | 0.079±0.001 | 0.003±0.000 | 0.9983 | 9.99±0.00 | 0.039±0.004 | 0.061±0.005 | SUCCESS_PARTIAL |
| 2 | 0.059±0.003 | 0.002±0.000 | 0.9980 | 19.96±0.00 | 0.043±0.003 | 0.141±0.004 | SUCCESS_PARTIAL |
| 5 | 0.035±0.000 | 0.002±0.000 | 0.9983 | 49.85±0.00 | 0.052±0.002 | 0.148±0.004 | SUCCESS_PARTIAL |
| 10 | 0.022±0.001 | 0.002±0.000 | 0.9966 | 99.40±0.00 | 0.077±0.009 | 0.191±0.002 | SUCCESS_PARTIAL |

### k = 20

| d | reid_sub | reid_deg | cobertura | EGS | KS D | Δclust | veredito |
|---|---|---|---|---|---|---|---|
| 1 | 0.057±0.001 | 0.002±0.000 | 0.9960 | 19.96±0.00 | 0.130±0.001 | 0.093±0.003 | SUCCESS_PARTIAL |
| 2 | 0.045±0.001 | 0.002±0.000 | 0.9948 | 39.88±0.00 | 0.163±0.002 | 0.154±0.006 | SUCCESS_PARTIAL |
| 5 | 0.027±0.001 | 0.002±0.000 | 0.9954 | 99.40±0.00 | 0.184±0.003 | 0.148±0.003 | SUCCESS_PARTIAL |
| 10 | 0.017±0.000 | 0.001±0.000 | 0.9877 | 198.21±0.00 | 0.304±0.005 | 0.241±0.018 | SUCCESS_PARTIAL |

---

## 3. Tabela bruta por (k, d, semente)

| k | d | seed | Veredito | coverage_fraction | rr_grau | rr_subgrafo | EG_mean | EG_median | KS_D | KS_p | clust_var |
|---|---|------|----------|-------------------|---------|-------------|--------|-----------|------|------|-----------|
| 2 | 1 | 42 | SUCCESS_PARTIAL | 0.999881 | 0.003235 | 0.122893 | 2.00 | 0 | 0.038610 | 0.0000 | 0.015644 |
| 2 | 1 | 1337 | SUCCESS_PARTIAL | 0.999881 | 0.003413 | 0.124110 | 2.00 | 0 | 0.039471 | 0.0000 | 0.019141 |
| 2 | 1 | 2718 | SUCCESS_PARTIAL | 0.999881 | 0.003354 | 0.125326 | 2.00 | 0 | 0.036651 | 0.0000 | 0.016224 |
| 2 | 2 | 42 | SUCCESS_PARTIAL | 0.999644 | 0.003413 | 0.098261 | 4.00 | 4 | 0.048670 | 0.0000 | 0.013883 |
| 2 | 2 | 1337 | SUCCESS_PARTIAL | 0.999644 | 0.003027 | 0.097400 | 4.00 | 4 | 0.049620 | 0.0000 | 0.014192 |
| 2 | 2 | 2718 | SUCCESS_PARTIAL | 0.999644 | 0.003413 | 0.098053 | 4.00 | 4 | 0.051282 | 0.0000 | 0.016183 |
| 2 | 5 | 42 | SUCCESS_PARTIAL | 0.999703 | 0.003799 | 0.079861 | 10.00 | 10 | 0.067189 | 0.0000 | 0.018404 |
| 2 | 5 | 1337 | SUCCESS_PARTIAL | 0.999703 | 0.003383 | 0.078615 | 10.00 | 10 | 0.069504 | 0.0000 | 0.019772 |
| 2 | 5 | 2718 | SUCCESS_PARTIAL | 0.999703 | 0.003680 | 0.080158 | 10.00 | 10 | 0.069504 | 0.0000 | 0.015723 |
| 2 | 10 | 42 | SUCCESS_PARTIAL | 0.999406 | 0.003086 | 0.051787 | 19.99 | 20 | 0.090693 | 0.0000 | 0.038383 |
| 2 | 10 | 1337 | SUCCESS_PARTIAL | 0.999406 | 0.003027 | 0.053567 | 19.99 | 20 | 0.090931 | 0.0000 | 0.044950 |
| 2 | 10 | 2718 | SUCCESS_PARTIAL | 0.999406 | 0.002819 | 0.052499 | 19.99 | 20 | 0.090931 | 0.0000 | 0.050565 |
| 5 | 1 | 42 | SUCCESS_PARTIAL | 0.999377 | 0.001929 | 0.101971 | 5.00 | 0 | 0.026027 | 0.0000 | 0.050745 |
| 5 | 1 | 1337 | SUCCESS_PARTIAL | 0.999377 | 0.002493 | 0.104078 | 5.00 | 0 | 0.027451 | 0.0000 | 0.049000 |
| 5 | 1 | 2718 | SUCCESS_PARTIAL | 0.999377 | 0.002434 | 0.101110 | 5.00 | 0 | 0.028342 | 0.0000 | 0.054476 |
| 5 | 2 | 42 | SUCCESS_PARTIAL | 0.999228 | 0.002255 | 0.074697 | 9.99 | 10 | 0.041993 | 0.0000 | 0.111361 |
| 5 | 2 | 1337 | SUCCESS_PARTIAL | 0.999228 | 0.002701 | 0.076151 | 9.99 | 10 | 0.040331 | 0.0000 | 0.108623 |
| 5 | 2 | 2718 | SUCCESS_PARTIAL | 0.999228 | 0.002612 | 0.077576 | 9.99 | 10 | 0.039411 | 0.0000 | 0.112782 |
| 5 | 5 | 42 | SUCCESS_PARTIAL | 0.999228 | 0.001988 | 0.048581 | 24.96 | 25 | 0.043447 | 0.0000 | 0.123388 |
| 5 | 5 | 1337 | SUCCESS_PARTIAL | 0.999228 | 0.002730 | 0.048759 | 24.96 | 25 | 0.045584 | 0.0000 | 0.125614 |
| 5 | 5 | 2718 | SUCCESS_PARTIAL | 0.999228 | 0.002612 | 0.048611 | 24.96 | 25 | 0.045910 | 0.0000 | 0.122719 |
| 5 | 10 | 42 | SUCCESS_PARTIAL | 0.999377 | 0.002760 | 0.027214 | 49.85 | 50 | 0.057959 | 0.0000 | 0.160404 |
| 5 | 10 | 1337 | SUCCESS_PARTIAL | 0.999377 | 0.002612 | 0.027837 | 49.85 | 50 | 0.053716 | 0.0000 | 0.157488 |
| 5 | 10 | 2718 | SUCCESS_PARTIAL | 0.999377 | 0.003057 | 0.028431 | 49.85 | 50 | 0.059028 | 0.0000 | 0.155342 |
| 10 | 1 | 42 | SUCCESS_PARTIAL | 0.998338 | 0.003027 | 0.079594 | 9.99 | 0 | 0.033654 | 0.0000 | 0.055225 |
| 10 | 1 | 1337 | SUCCESS_PARTIAL | 0.998338 | 0.002255 | 0.078259 | 9.99 | 0 | 0.041934 | 0.0000 | 0.063838 |
| 10 | 1 | 2718 | SUCCESS_PARTIAL | 0.998338 | 0.002760 | 0.078377 | 9.99 | 0 | 0.040391 | 0.0000 | 0.063505 |
| 10 | 2 | 42 | SUCCESS_PARTIAL | 0.998041 | 0.002018 | 0.055793 | 19.96 | 20 | 0.046593 | 0.0000 | 0.145356 |
| 10 | 2 | 1337 | SUCCESS_PARTIAL | 0.998041 | 0.002285 | 0.061847 | 19.96 | 20 | 0.040272 | 0.0000 | 0.138616 |
| 10 | 2 | 2718 | SUCCESS_PARTIAL | 0.998041 | 0.002196 | 0.059888 | 19.96 | 20 | 0.041607 | 0.0000 | 0.139883 |
| 10 | 5 | 42 | SUCCESS_PARTIAL | 0.998338 | 0.002523 | 0.034722 | 49.85 | 50 | 0.050332 | 0.0000 | 0.148383 |
| 10 | 5 | 1337 | SUCCESS_PARTIAL | 0.998338 | 0.002523 | 0.035345 | 49.85 | 50 | 0.050778 | 0.0000 | 0.143800 |
| 10 | 5 | 2718 | SUCCESS_PARTIAL | 0.998338 | 0.002255 | 0.034633 | 49.85 | 50 | 0.054368 | 0.0000 | 0.152686 |
| 10 | 10 | 42 | SUCCESS_PARTIAL | 0.996557 | 0.002463 | 0.020863 | 99.40 | 100 | 0.075647 | 0.0000 | 0.192583 |
| 10 | 10 | 1337 | SUCCESS_PARTIAL | 0.996557 | 0.002107 | 0.021694 | 99.40 | 100 | 0.086182 | 0.0000 | 0.191460 |
| 10 | 10 | 2718 | SUCCESS_PARTIAL | 0.996557 | 0.002226 | 0.023386 | 99.40 | 100 | 0.068999 | 0.0000 | 0.188393 |
| 20 | 1 | 42 | SUCCESS_PARTIAL | 0.995964 | 0.002077 | 0.056357 | 19.96 | 0 | 0.129184 | 0.0000 | 0.093835 |
| 20 | 1 | 1337 | SUCCESS_PARTIAL | 0.995964 | 0.001870 | 0.056980 | 19.96 | 0 | 0.130906 | 0.0000 | 0.089811 |
| 20 | 1 | 2718 | SUCCESS_PARTIAL | 0.995964 | 0.001840 | 0.057485 | 19.96 | 0 | 0.130668 | 0.0000 | 0.095031 |
| 20 | 2 | 42 | SUCCESS_PARTIAL | 0.994777 | 0.001514 | 0.045881 | 39.88 | 40 | 0.164203 | 0.0000 | 0.155729 |
| 20 | 2 | 1337 | SUCCESS_PARTIAL | 0.994777 | 0.002077 | 0.044397 | 39.88 | 40 | 0.161117 | 0.0000 | 0.157968 |
| 20 | 2 | 2718 | SUCCESS_PARTIAL | 0.994777 | 0.001751 | 0.043566 | 39.88 | 40 | 0.164856 | 0.0000 | 0.147310 |
| 20 | 5 | 42 | SUCCESS_PARTIAL | 0.995370 | 0.001988 | 0.026887 | 99.40 | 100 | 0.181090 | 0.0000 | 0.144693 |
| 20 | 5 | 1337 | SUCCESS_PARTIAL | 0.995370 | 0.001454 | 0.026591 | 99.40 | 100 | 0.184443 | 0.0000 | 0.150570 |
| 20 | 5 | 2718 | SUCCESS_PARTIAL | 0.995370 | 0.001662 | 0.028490 | 99.40 | 100 | 0.186194 | 0.0000 | 0.148076 |
| 20 | 10 | 42 | SUCCESS_PARTIAL | 0.987654 | 0.001217 | 0.016590 | 198.21 | 200 | 0.310245 | 0.0000 | 0.222799 |
| 20 | 10 | 1337 | SUCCESS_PARTIAL | 0.987654 | 0.001573 | 0.017302 | 198.21 | 200 | 0.300036 | 0.0000 | 0.241163 |
| 20 | 10 | 2718 | SUCCESS_PARTIAL | 0.987654 | 0.001365 | 0.016500 | 198.21 | 200 | 0.302558 | 0.0000 | 0.258663 |

---

## 4. Análise — deslocamento do vetor de ataque

### 4.1 Replicação parcial: metade estrutural sim, deslocamento não

Do padrão central do d-sweep Facebook (§5.2 de `docs/results_dsweep.md`), apenas a **metade estrutural** se replica no Enron:

- **Subgrafo enfraquece com d crescente** (em k fixo) ✔ replica. Grupos de equivalência maiores (EGS ≈ k·d) aumentam a ambiguidade estrutural e dificultam o isomorfismo 1-hop. Ex.: k=2 → 0,124 / 0,098 / 0,080 / 0,053; k=20 → 0,057 / 0,045 / 0,027 / 0,017.
- **Grau NÃO se fortalece com d** ✘ não replica. `reid_deg` fica colado ao piso (~0,002–0,004) em toda a grade — chegando a declinar levemente em k/d altos —, mesmo com anonimização agressiva (KS D até ~0,30). Ex.: k=2 → 0,003 / 0,003 / 0,004 / 0,003; k=20 → 0,002 / 0,002 / 0,002 / 0,001.

**Leitura (replicação parcial / dependente de escala):** não há cruzamento dos vetores de ataque no Enron — o subgrafo permanece dominante nas 16 células (em k=20/d=10: 0,017 subgrafo vs 0,001 grau). Numa rede de ~33,7 k nós, as colisões de grau são abundantes e raramente isolam um grau único; o deslocamento grau↑/subgrafo↓ observado no Facebook é **dependente da escala pequena daquela ego-rede, não uma lei do mecanismo**. O d-sweep Enron confirma (D5) a degradação estrutural do subgrafo com d, mas não o cruzamento.

### 4.2 Escala atenua o efeito de subgrafo

Os valores absolutos de `reid_sub` no Enron são sistematicamente inferiores ao Facebook (ver `docs/results_enron.md` para a comparação d=1). Na rede de 33,7 k nós, vizinhanças 1-hop colidem com maior frequência — o ataque por subgrafo parte de uma taxa-base mais baixa antes mesmo de qualquer efeito de k ou d.

### 4.3 EGS ≈ k·d — confirmado no Enron

A relação EGS ≈ k·d (tamanho médio do grupo de equivalência ≈ produto k×d) observada no Facebook se mantém no Enron: grupos são determinados pelo produto do k-anonimato e da dimensão de estrutura d, independentemente da escala da rede.

### 4.4 Combos degenerados (D-08, D-10)

- **d = 2 (D-08).** No Enron LCC (n=33.696), d=2 gera 16.848 partições-alvo de 2 nós. O comportamento é estruturalmente mais estável que na ego-rede Facebook (n=532 → ~199 partições). Resultados incluídos mas anotados como degenerate por D-08.
- **d = 10, k = 20 (D-10).** c_k = ⌊33.696/10⌋ = 3.369 partições; k=20 exige ≥20 grupos isomorfos de 10 nós. `SUCCESS_PARTIAL` e cobertura ≥ 0.99 indicam que o Enron, por ser maior, absorve melhor este combo que a ego-rede Facebook.

---

## 5. Reprodutibilidade

```bash
# 1. d-sweep Enron (36 runs: k∈{2,5,10,20} × d∈{2,5,10} × 3 sementes)
python -m experiments.run --config experiments/configs/he2009_enron_dsweep.yml

# 2. Esta tabela (docs/results_enron_dsweep.md)
python -m experiments.make_enron_dsweep_table
```

> Logs em `experiments/logs/` são **gitignored** (`docs/regras_experimentos.md`); versiona-se o YAML de config e o script de tabela. O log d=1 de âncora (`he2009_enron_secondary`) é produzido por `experiments/configs/he2009_enron_secondary.yml` (issue #29/S9).
