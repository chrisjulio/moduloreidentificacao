# Matriz de rastreabilidade — Relatório de qualificação (#174)

> **Propósito.** Rastreabilidade **pública** da redação do relatório de
> qualificação (issue [#174](https://github.com/chrisjulio/moduloreidentificacao/issues/174),
> S10-W1). O texto substantivo do relatório vive em `academic/` (**privado**,
> gitignorado — PR #176; backup externo do autor) e **não** é versionado neste
> repositório; o que se versiona é esta matriz: seção → fontes → `W-NN` →
> figuras, mais o sumário do esqueleto. Decisão do autor (2026-06-09),
> registrada na DoD emendada da #174.
>
> Criado na etapa **S10-W1a** (esqueleto + matriz). Atualizado a cada etapa de
> redação (S10-W1b..f).

---

## Sumário do relatório (esqueleto, 8 seções)

Estrutura mínima fixada pela #174:

1. Introdução e posicionamento
2. Independência em relação ao EpiCNet
3. Método: pipeline anonimização → ataque → métrica
4. Desenho experimental
5. Resultados
6. Limitações e ameaças à validade
7. Reprodutibilidade
8. Enquadramento ético

Apêndices (decisão na revisão integrada): tabelas brutas, inventário de
entregáveis, referências bibliográficas (README §12/§13).

---

## Matriz seção → fontes → `W-NN` → figuras

| Seção | Fontes (docs) | Decisões citáveis | `W-NN` (destino no texto) | Figuras/Tabelas | Etapa |
|---|---|---|---|---|---|
| 1. Introdução e posicionamento | [`scope.md`](scope.md) §4/§5; `README.md` | **DL-06** (premissa "anonimizar não é o suficiente") | — | — | S10-W1b |
| 2. Independência do EpiCNet | [`scope.md`](scope.md) §8; `README.md` ("o que não faz") | — | — | — | S10-W1b |
| 3. Método | [`pipeline.md`](pipeline.md); [`metrics_definitions.md`](metrics_definitions.md); [`algorithm_notes.md`](algorithm_notes.md) | DL-05; D-16; D-13; DL-01 | **W-01** (uniformidade de parâmetros); **W-02** (equivalência VF2↔WL); **W-03** (validade da execução Enron) | diagrama do pipeline (opcional) | S10-W1c |
| 4. Desenho experimental | [`scope.md`](scope.md) §3; [`data_dictionary.md`](data_dictionary.md) §1.1; [`preprocessing_decision.md`](preprocessing_decision.md) | D-11 (simetrização OR) | **W-05** (frase canônica [M]/[D]) | — | S10-W1c |
| 5. Resultados | [`results_baseline.md`](results_baseline.md); [`results_dsweep.md`](results_dsweep.md); [`results_enron.md`](results_enron.md); [`data_dictionary.md`](data_dictionary.md) | DL-04; D-16; D-11; D-17 | **W-04** (B1 generalizável); **W-06** (painéis por dataset + normalizado) | ver inventário abaixo | S10-W1d |
| 6. Limitações e ameaças à validade | [`limitations.md`](limitations.md); [`achados_divergencias.md`](achados_divergencias.md) (B1, B2, C2) | D-06 | — | — | S10-W1e |
| 7. Reprodutibilidade | [`reproducibility.md`](reproducibility.md); `README.md` | — | — | fluxogramas (`img/`) | S10-W1e |
| 8. Enquadramento ético | [`scope.md`](scope.md) §7 | — | — | — | S10-W1e |
| Revisão integrada | [`progress.md`](progress.md); [`entregaveis.md`](entregaveis.md); [`mapa_estrutural.md`](mapa_estrutural.md) | todas | conferência W-01..W-06 | conferência | S10-W1f |

Todos os `W-NN` referenciados estão **resolvidos** no
[`artifact_writing_checklist.md`](artifact_writing_checklist.md); a coluna
indica o **destino no texto** de cada resolução — a redação incorpora, não
reabre.

---

## Inventário de figuras e tabelas citáveis

| Artefato | Origem / comando | Versionamento |
|---|---|---|
| Curva privacidade-utilidade Facebook | `python -m src.visualization.privacy_utility --logs experiments/logs/he2009_facebook_baseline` → `results/plots/privacy_utility_facebook.*` | regenerável (gitignored) |
| Curva privacidade-utilidade Enron | idem com logs do Enron → `results/plots/privacy_utility_enron.*` | regenerável (gitignored) |
| Figuras do d-sweep | regeneradas do log (ver [`results_dsweep.md`](results_dsweep.md)) | regenerável (gitignored) |
| Painel comparativo normalizado FB×Enron | [`assets/comparison_fb_enron.png`](assets/comparison_fb_enron.png) (+ [`.csv`](assets/comparison_fb_enron.csv)); gerador `src/visualization/comparison.py` | **versionado** (exceção DL-04) |
| Tabelas CSV por (dataset, ataque) | `python -m src.visualization.tables --logs <dir> --out results/tables` | regenerável (gitignored) |
| Tabelas agregadas por k | `experiments/make_baseline_table.py` / `make_enron_table.py`; embutidas em `results_*.md` | versionadas nos docs |
| Fluxogramas de reprodutibilidade | [`img/fluxograma1_reproducibilidade.jpg`](img/fluxograma1_reproducibilidade.jpg), [`img/fluxograma2_reproducibilidade.jpg`](img/fluxograma2_reproducibilidade.jpg) | versionados |

---

## Estado por etapa (S10-W1a..f)

| Etapa | Escopo | Status |
|---|---|---|
| W1a | Esqueleto em `academic/` + esta matriz | ✅ concluída (2026-06-09) |
| W1b | Seções 1–2 (introdução; EpiCNet) | ✅ concluída (2026-06-09) |
| W1c | Seções 3–4 (método; desenho experimental) | ✅ concluída (2026-06-09) |
| W1d | Seção 5 (resultados) | ⏳ pendente |
| W1e | Seções 6–8 (limitações; reprodutibilidade; ética) | ⏳ pendente |
| W1f | Revisão integrada + DoD da #174 | ⏳ pendente |

> As etapas seguem a proposta de desdobramento validada pelo autor na #174
> (comentário de 2026-06-09, 5 pontos resolvidos). Decisão do autor
> (2026-06-09): as etapas **não** viram sub-issues no GitHub — cada execução
> é registrada por comentário na #174 e em
> [`relatorio_execucoes.md`](relatorio_execucoes.md) (contabilização e
> registro detalhado por etapa).
