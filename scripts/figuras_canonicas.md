# Regras canônicas de geração das figuras

Fonte de verdade para **como** as figuras versionadas em `docs/assets/` são
geradas. Toda regeneração deve seguir os comandos e convenções abaixo — nunca
produzir figuras por execução interativa não rastreável (ver
[`docs/regras_experimentos.md`](../docs/regras_experimentos.md)).

Há **dois conjuntos** de figuras, com geradores e estilos distintos:

| Conjunto | Gerador | Estilo | Saída |
|---|---|---|---|
| **Assets canônicos** | `src/visualization/` | cor, com suptitle, PT (e EN) | `docs/assets/*.{png,pdf,csv}` |
| **Figuras do artigo** | `scripts/article_figures.py` | B&W, sem suptitle, EN (KDMiLe) | `docs/assets/eng-*.{pdf,png}` |

---

## Motor canônico: pymetis

Pós-E1 (#211) / D8, o motor de particionamento canônico é **pymetis**. Os logs
de origem são:

| Papel | Diretório de logs |
|---|---|
| Facebook baseline | `experiments/logs/he2009_facebook_baseline_pymetis` |
| Enron (âncora d=1) | `experiments/logs/he2009_enron_secondary` |
| Enron d-sweep (d∈{2,5,10}) | `experiments/logs/he2009_enron_dsweep` |

> **Default já canônico.** O default embutido em `article_figures.py`
> (`_DEFAULT_FB_LOGS`) aponta para `he2009_facebook_baseline_pymetis` (pymetis),
> então `python -m scripts.article_figures --bw` já produz o Facebook no motor
> canônico. O log KL histórico (`he2009_facebook_baseline`) só deve ser usado
> via `--fb-logs` explícito para reproduzir artefatos antigos.

---

## Figuras do artigo (B&W, EN) — `scripts/article_figures.py`

Um único comando regenera as três. Sempre em `--bw` (o artigo declara "sem cores"):

```bash
python -m scripts.article_figures --bw --out docs/assets
```

| Figura | Função | Fonte de dados |
|---|---|---|
| `eng-privacy_utility.{pdf,png}` | `build_privacy_utility` | FB baseline (pymetis) |
| `eng-comparison_fb_enron.pdf` | `build_comparison` | `docs/assets/comparison_fb_enron.csv` (congelado, pymetis) |
| `eng-enron_dsweep_series.{pdf,png}` | `build_enron_dsweep_series` | `he2009_enron_secondary` (d=1) + `he2009_enron_dsweep` (d∈{2,5,10}) |

### Convenções de estilo (obrigatórias)

- **Geometria:** 1×2 lado a lado, `figsize ≈ (12, 5)`, incluída como `figure*` a
  `\textwidth`. Tipografia: fonte-base 16 pt, linhas ~1,2 pt, `pdf.fonttype=42`
  (texto extraível), `bbox_inches="tight"`, `pad_inches=0.01`.
- **B&W (`--bw`):** séries distinguidas por estilo de linha + marcador, sem cor.
- **`(a)/(b)`:** sempre como **título à esquerda, acima do frame**
  (`ax.set_title(tag, loc="left")`) — **nunca** dentro da área de dados. A
  enumeração também vive na `\caption` do LaTeX.
- **Legendas:** preferencialmente **fora dos eixos** (embaixo, `fig.legend`),
  nunca sobrepondo dados. Exceção: chaves auxiliares que caibam num canto livre
  podem ficar **dentro** do painel (ex.: a chave de `d` da `eng-enron_dsweep_series`
  fica no canto superior-esquerdo do painel (b), poupando uma fileira inferior).
- **Eixo k:** logarítmico, ticks fixos `{2, 5, 10, 20}`. O rótulo "k" fica
  **inline**, à esquerda do primeiro tick (`k  2  5  10  20`), via
  `_inline_k_label` — não centralizado abaixo do eixo (poupa altura).
- **d (d-sweep):** codificado por **cor** (modo cor) ou por **marcador** em B&W
  (`d=1→○, d=2→□, d=5→△, d=10→◇`); o ataque/métrica fica no estilo de linha.

---

## Assets canônicos (cor) — `src/visualization/`

### Comparativo Facebook × Enron

```bash
# PT (canônico) e EN — rodar uma vez por idioma
python -m src.visualization.comparison --lang pt \
  --stem comparison_fb_enron --pdf --out docs/assets \
  --fb-logs experiments/logs/he2009_facebook_baseline_pymetis \
  --enron-logs experiments/logs/he2009_enron_secondary

python -m src.visualization.comparison --lang en \
  --stem eng-comparison_fb_enron --pdf --out docs/assets \
  --fb-logs experiments/logs/he2009_facebook_baseline_pymetis \
  --enron-logs experiments/logs/he2009_enron_secondary
```

- Gera `{stem}.png`, `{stem}.csv` (e `.pdf` com `--pdf`). O `eng-comparison_fb_enron.csv`
  é **idêntico** ao `comparison_fb_enron.csv` — **remover** o duplicado após gerar.
- O `.png` (canônico, cor, com suptitle e títulos "(A)/(B)") e o `.pdf` do artigo
  (B&W, `article_figures.py`) vêm de geradores diferentes **por design**; manter
  ambos em pymetis.

### Série d-sweep Enron (PT)

```bash
python -m src.visualization.privacy_utility \
  --logs experiments/logs/he2009_enron_dsweep \
  --anchor-logs experiments/logs/he2009_enron_secondary \
  --layout series --out docs/assets --stem enron_dsweep_series
```

---

## Checklist de regeneração

1. Confirmar logs pymetis presentes (ver tabela do motor canônico).
2. Rodar o(s) comando(s) acima com os `--fb-logs` pymetis explícitos.
3. Remover CSVs `eng-*` duplicados.
4. Conferir visualmente o `.png` (dados pymetis: FB `bound_fraction` toda < 1; só
   Enron cruza a cota em k=20).
5. `ruff check .` e `ruff format .` limpos antes do PR.
