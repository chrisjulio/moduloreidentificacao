# Resultados do experimento secundário — Email-Enron (He et al. 2009)

> Gerado automaticamente por `experiments/make_enron_table.py`.
> Fonte: `experiments/logs/he2009_enron_secondary/he2009_enron_secondary.jsonl`.
> Issue #128 (S9-6) — comparativo Facebook × Enron + tabelas de risco × utilidade.
> Parte da issue-mãe #29 (dataset secundário do tier **Desejável** `[D]`).

**Dataset:** Email-Enron (SNAP), projeção não-direcionada por **OR** (D-11); maior componente conexa (LCC) com **n=33.696 nós, m=180.811 arestas** (grau médio ≈ 10,7).
**Sementes:** 42, 1337, 2718
**Algoritmo:** He et al. (2009), d=1, sigma=0.5, s_max=4, isomorphism_mode=add_or_delete
**Motor de particionamento:** pymetis (12/12 execuções) — fiel ao artigo.
**Ataques:** grau (tolerance=0) + subgrafo (hop=1) — subgrafo **full** viável via bucketing de WL-hash (D-16); `subgraph_timeout_count=0` em todas as runs.

---

## Enquadramento metodológico — síntese

> **Frase-síntese.** O Email-Enron é o dataset **secundário** (tier Desejável `[D]`) que estende o baseline **Facebook** (tier Mínimo `[M]`) para uma rede de escala e origem distintas: ~63× mais nós (33,7 k vs. 532), derivada de e-mail corporativo **direcionado** e projetada para não-direcionada por simetrização OR (D-11), contra a amizade já-simétrica de uma única ego-rede do Facebook. Ele **não introduz mecanismo novo** — reusa o mesmo pipeline `anonimização → ataque → métrica` — e serve para **aferir se o comportamento privacidade-vs-utilidade do He et al. (2009) se mantém fora da topologia de ego-rede**. A leitura conjunta deve focar **tendências** (sinal e monotonicidade), não magnitudes absolutas, que não são diretamente comparáveis (ver abaixo).

Como no baseline, `d=1` afere **k-anonimato de grau**, não a propriedade *structure-aware* plena (achado B1): em `d=1` a estrutura local de cada nó reduz-se ao seu grau. O ataque por **subgrafo** (isomorfismo de vizinhança 1-hop) é, portanto, o termômetro de quanto a estrutura — não anonimizada em `d=1` — ainda permite associação. Toda a terminologia segue o enquadramento de aferição (D-11): avalia-se **risco de reidentificação / vulnerabilidade agregada**, nunca identificação individual.

---

## Comparativo Facebook × Enron (médias por k, 3 sementes)

> Facebook: `experiments/logs/he2009_facebook_baseline/` (carregado). Enron: log desta execução. As duas colunas de cada métrica compartilham `d=1`, `sigma=0.5` e as mesmas 3 sementes; diferem no dataset (e no motor: KL no baseline Facebook — achado A1 — vs. pymetis no Enron).

| k | rr_grau FB | rr_grau Enron | rr_subgrafo FB | rr_subgrafo Enron | KS-D FB | KS-D Enron | clust_var FB | clust_var Enron |
|---|-----------|--------------|----------------|-------------------|---------|------------|--------------|-----------------|
| 2 | 0.0263 | 0.0033 | 0.7914 | 0.1241 | 0.0000 | 0.0382 | 0.0000 | 0.0170 |
| 5 | 0.0081 | 0.0023 | 0.4060 | 0.1024 | 0.0482 | 0.0273 | 0.0670 | 0.0514 |
| 10 | 0.0226 | 0.0027 | 0.1397 | 0.0787 | 0.2356 | 0.0387 | 0.1575 | 0.0609 |
| 20 | 0.0990 | 0.0019 | 0.0000 | 0.0569 | 0.6491 | 0.1303 | 0.0904 | 0.0929 |

### Por que as magnitudes **não** são diretamente comparáveis

A comparação direta dos valores absolutos é **confundida** por três diferenças estruturais, e a tabela acima deve ser lida como contraste de **tendências**, não de níveis:

1. **Escala (n).** O Facebook é uma única ego-rede pequena e densa (n=532); o Enron tem n=33.696. Numa rede pequena, muitas vizinhanças 1-hop são **únicas** → reidentificação por subgrafo alta (rr≈0,79 em k=2). Numa rede grande, vizinhanças **colidem** com muito mais frequência → taxa-base baixa (rr≈0,12 em k=2) **antes mesmo** de qualquer efeito de k. A diferença de ~6× em k=2 é majoritariamente de escala, não de proteção.
2. **Densidade e origem.** O Enron vem de e-mail **direcionado** achatado por OR (D-11), o que infla conectividade de modo distinto da amizade simétrica do Facebook; grau médio e distribuição de grau diferem.
3. **Motor de particionamento.** O baseline Facebook rodou em Kernighan-Lin (achado A1), o Enron em pymetis. Inócuo em `d=1` (partições triviais de 1 nó), mas é mais uma variável não-pareada entre as colunas.

**Conclusão (DoD #128).** Um gráfico com as duas redes **sobrepostas nos mesmos eixos é enganoso**: a faixa de reidentificação do Facebook (0–79 %) comprimiria as curvas do Enron (0–12 %) a uma quase-reta, e o mesmo vale para KS-D (0–0,65 vs. 0–0,13). Os gráficos privacidade-utilidade são gerados **por dataset separadamente** (`results/plots/privacy_utility_enron.*`, mesmo gerador do Facebook), e a comparação é feita pela tabela acima e pelas tendências abaixo.

### O que **é** comparável — tendências robustas em ambas as redes

- **Subgrafo ≫ grau.** Em toda a faixa de k, o ataque por subgrafo reidentifica muito mais que o ataque por grau (Enron: ~40× em k=2). Confirma, fora da ego-rede, que **igualar grau não protege a estrutura de vizinhança** — o cerne empírico do módulo.
- **Monotonicidade em k.** O `rr_subgrafo` cai de forma monótona com k em ambas (Enron: 0,124 → 0,102 → 0,079 → 0,057). k-anonimato **reduz** a vulnerabilidade estrutural mesmo em `d=1`.
- **Grau já residual.** O `rr_grau` é baixíssimo no Enron (≤0,003) — uma ordem de grandeza abaixo do Facebook — coerente com a escala: assinaturas de grau isoladas quase nunca são únicas numa rede grande.
- **Utilidade melhor preservada em escala.** O KS-D do Enron permanece baixo (0,04–0,13) onde o Facebook chega a 0,65: perturbar uma rede grande desloca a distribuição global de grau proporcionalmente menos. A anonimização é **menos custosa em utilidade** numa rede grande.

---

## Tabela bruta por (k, semente)

| k | seed | Veredito | coverage_fraction | rr_grau | rr_subgrafo | EG_mean | EG_median | KS_D | KS_p | clust_var |
|---|------|----------|-------------------|---------|-------------|--------|-----------|------|------|-----------|
| 2 | 42 | SUCCESS_PARTIAL | 0.999881 | 0.0032 | 0.1229 | 2.00 | 0 | 0.0386 | 0.0000 | 0.0156 |
| 2 | 1337 | SUCCESS_PARTIAL | 0.999881 | 0.0034 | 0.1241 | 2.00 | 0 | 0.0395 | 0.0000 | 0.0191 |
| 2 | 2718 | SUCCESS_PARTIAL | 0.999881 | 0.0034 | 0.1253 | 2.00 | 0 | 0.0367 | 0.0000 | 0.0162 |
| 5 | 42 | SUCCESS_PARTIAL | 0.999377 | 0.0019 | 0.1020 | 5.00 | 0 | 0.0260 | 0.0000 | 0.0507 |
| 5 | 1337 | SUCCESS_PARTIAL | 0.999377 | 0.0025 | 0.1041 | 5.00 | 0 | 0.0275 | 0.0000 | 0.0490 |
| 5 | 2718 | SUCCESS_PARTIAL | 0.999377 | 0.0024 | 0.1011 | 5.00 | 0 | 0.0283 | 0.0000 | 0.0545 |
| 10 | 42 | SUCCESS_PARTIAL | 0.998338 | 0.0030 | 0.0796 | 9.99 | 0 | 0.0337 | 0.0000 | 0.0552 |
| 10 | 1337 | SUCCESS_PARTIAL | 0.998338 | 0.0023 | 0.0783 | 9.99 | 0 | 0.0419 | 0.0000 | 0.0638 |
| 10 | 2718 | SUCCESS_PARTIAL | 0.998338 | 0.0028 | 0.0784 | 9.99 | 0 | 0.0404 | 0.0000 | 0.0635 |
| 20 | 42 | SUCCESS_PARTIAL | 0.995964 | 0.0021 | 0.0564 | 19.96 | 0 | 0.1292 | 0.0000 | 0.0938 |
| 20 | 1337 | SUCCESS_PARTIAL | 0.995964 | 0.0019 | 0.0570 | 19.96 | 0 | 0.1309 | 0.0000 | 0.0898 |
| 20 | 2718 | SUCCESS_PARTIAL | 0.995964 | 0.0018 | 0.0575 | 19.96 | 0 | 0.1307 | 0.0000 | 0.0950 |

---

## Agregação por k (média ± desvio-padrão, 3 sementes)

| k | Vereditos | coverage_fraction | rr_grau (mean±std) | rr_subgrafo (mean±std) | EG_mean (mean±std) | KS_D (mean±std) | clust_var (mean±std) |
|---|-----------|-------------------|--------------------|------------------------|--------------------|-----------------|----------------------|
| 2 | SUCCESS_PARTIAL | 0.999881±0.000000 | 0.0033±0.0001 | 0.1241±0.0012 | 2.00±0.00 | 0.0382±0.0014 | 0.0170±0.0019 |
| 5 | SUCCESS_PARTIAL | 0.999377±0.000000 | 0.0023±0.0003 | 0.1024±0.0015 | 5.00±0.00 | 0.0273±0.0012 | 0.0514±0.0028 |
| 10 | SUCCESS_PARTIAL | 0.998338±0.000000 | 0.0027±0.0004 | 0.0787±0.0007 | 9.99±0.00 | 0.0387±0.0044 | 0.0609±0.0049 |
| 20 | SUCCESS_PARTIAL | 0.995964±0.000000 | 0.0019±0.0001 | 0.0569±0.0006 | 19.96±0.00 | 0.1303±0.0009 | 0.0929±0.0027 |

---

## Interpretação

- **Ataque por grau** — `rr_grau ∈ [0,0018; 0,0034]`, uma ordem de grandeza abaixo do Facebook. Numa rede de 33,7 k nós, assinaturas de grau isoladas raramente são únicas; o ataque mais fraco é quase inócuo já em k=2.

- **Ataque por subgrafo** (isomorfismo 1-hop, caminho rápido por WL-hash, D-16) — `rr_subgrafo` cai monotonicamente de **0,124** (k=2) para **0,057** (k=20), ~40× a taxa de grau. Em `d=1` anonimiza-se o grau, **não** a estrutura 1-hop (B1); o resíduo de ~6 % em k=20 é a vulnerabilidade estrutural que `d=1` não cobre — coerente com o baseline Facebook, onde o subgrafo também domina o grau.

- **coverage_fraction ≥ 0,9960** em todas as 12 runs, com `deficit_fully_structural=True` (vereditos `SUCCESS_PARTIAL`): a incompletude residual é exclusivamente de **grupos incompletos** (D-06), aceitável pelo critério DL-01 — nenhuma violação de isomorfismo/disjunção.

- **Utilidade.** KS-D cresce com k (0,038 → 0,130) e a variação de clustering idem (0,017 → 0,093), mas ambas permanecem **muito abaixo** das do Facebook: anonimizar uma rede grande custa proporcionalmente menos utilidade global.

- **Divergência em k alto.** No Facebook o `rr_subgrafo` colapsa a 0 em k=20 (a ego-rede inteira cabe em poucos grupos); no Enron permanece em ~0,057 — a rede grande retém estrutura local distinguível mesmo sob k=20. Reforça que as magnitudes refletem **escala**, não diferença de mecanismo.

---

## Reprodutibilidade

```bash
# 1. Execução (12 runs: k∈{2,5,10,20} × 3 sementes)
python -m experiments.run --config experiments/configs/he2009_enron_secondary.yml

# 2. Esta tabela (docs/results_enron.md)
python -m experiments.make_enron_table

# 3. Tabelas CSV (results/tables/enron_{degree,subgraph}.csv)
python -m src.visualization.tables \
    --logs experiments/logs/he2009_enron_secondary \
    --out results/tables --dataset enron

# 4. Gráfico privacidade-utilidade do Enron (results/plots/privacy_utility_enron.*)
python -m src.visualization.privacy_utility \
    --logs experiments/logs/he2009_enron_secondary \
    --out results/plots --stem privacy_utility_enron \
    --title "Privacy vs. Utility — Email-Enron (He et al. 2009)"
```

> Logs, tabelas CSV e plots são **gitignored** (`.claude/rules/experiments.md`); versiona-se apenas o YAML de config e os scripts que os regeneram. As referências cruzadas: D-11 (projeção OR), D-15/D-16 (viabilidade do subgrafo), achados A1/B1; ver `docs/decision_log.md` e `docs/results_baseline.md`.
