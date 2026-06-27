# Matriz de rastreabilidade — Relatório técnico (#174)

> **Propósito.** Rastreabilidade **pública** da redação do relatório
> técnico (issue [#174](https://github.com/chrisjulio/moduloreidentificacao/issues/174),
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

Apêndices — decididos na revisão integrada (W1f, 2026-06-10): **Apêndice A**
(tabelas brutas por (k, semente) do baseline Facebook e do Enron, embutidas;
d-sweep referenciado a `results_dsweep.md`) e **Apêndice B** (as 14
referências bibliográficas do README §12, embutidas) entram; o inventário de
entregáveis **não** entra (documento vivo do repositório — referenciado, não
copiado).

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
| Painel comparativo normalizado FB×Enron | [`assets/comparison_fb_enron.png`](assets/comparison_fb_enron.png) (+ [`.pdf`](assets/comparison_fb_enron.pdf) e [`.csv`](assets/comparison_fb_enron.csv)); gerador `src/visualization/comparison.py` | **versionado** (exceção DL-04) |
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
| W1d | Seção 5 (resultados) | ✅ concluída (2026-06-09) |
| W1e | Seções 6–8 (limitações; reprodutibilidade; ética) | ✅ concluída (2026-06-09) |
| W1f | Revisão integrada + DoD da #174 | ✅ concluída (2026-06-10) |

> **W1f executada (2026-06-10):** conferência integral das Seções 1–8
> contra `main` (números × `results_*.md`: exatos; W-01..W-06 nos destinos
> do checklist; terminologia de aferição conforme; artefatos citados todos
> presentes). **Única não-conformidade encontrada e corrigida:** a Seção 7.2
> citava `scripts.verify_reproduction` como verificação automática entregue
> — o script não está versionado em `main` (resíduo documental registrado
> na issue #172); a seção foi reescrita (conferência manual dos agregados
> por k, tolerância 0,02) e a ameaça correspondente adicionada à tabela da
> Seção 6.3. Apêndices decididos (acima); diagrama do pipeline (Mermaid de
> `pipeline.md` §1) incluído para a conversão final. **DoD da #174
> conferida item a item: cumprida.** Registro detalhado em
> [`relatorio_execucoes.md`](relatorio_execucoes.md).

> As etapas seguem a proposta de desdobramento validada pelo autor na #174
> (comentário de 2026-06-09, 5 pontos resolvidos). Decisão do autor
> (2026-06-09): as etapas **não** viram sub-issues no GitHub — cada execução
> é registrada por comentário na #174 e em
> [`relatorio_execucoes.md`](relatorio_execucoes.md) (contabilização e
> registro detalhado por etapa).

---

## Revisões D1–D3 — reposicionamento como baseline + atualização bibliográfica (2026-06-26)

Rodada de revisão pós-entrega orientada pelo retorno dos avaliadores externos
(orientador e coorientador), executada **somente no texto** do relatório
(`academic/relatorio_tecnico.md`, privado), com reflexos públicos em
`README.md` §12 e nas matrizes de rastreabilidade. Sem alteração de números,
tabelas, figuras ou código.

- **D1 (#216) — §1.1:** o trabalho passa a ser declarado explicitamente como
  **baseline de avaliação de risco** para k-anonimato estrutural de grafos, com
  a lacuna metodológica (ausência de baselines padronizados, mesmo diante da
  Privacidade Diferencial) no primeiro parágrafo.
- **D2 (#217) — §2.1:** parágrafo diferenciando DP (consultas/estatísticas
  agregadas; *query release*; garantia semântica/ε) de anonimização estrutural
  por k-anonimato (publicação do grafo completo para *graph mining*; garantia
  sintática). Tom: diferença de premissas, não detrimento da DP.
- **D3 (#218) — §2.1:** atualização bibliográfica > 2020, três referências
  recentes verificadas (DBLP/arXiv) tecidas ao texto — Hao et al. (2024,
  k-degree multinível, **> 2023**), Yuan et al. (2023, PrivGraph, *graph
  release* sob DP) e Mueller et al. (2022, SoK, taxonomia de DP em grafos).

**Reflexo público:** `README.md` §12 passou de 15 → 17 (D2) → **20** (D3)
entradas, renumerada. **BibTeX + links** versionados em `references/README.md`;
PDFs locais do autor (gitignored). Detalhamento espelhado em
[`artigo_rastreabilidade.md`](artigo_rastreabilidade.md) (§Revisões D1–D3).
de Jong et al. (2024) retido para deliberação com os orientadores.

---

## Revisão D7 — adversário aprendido (ML/GNN): Wang et al. (2023) (2026-06-27)

Rodada de aderência bibliográfica, **sem issue vinculada** (rótulo descritivo).
Executada **somente no texto** do relatório (`academic/relatorio_tecnico.md`,
privado), com reflexos públicos em `README.md` §12 e nas matrizes de
rastreabilidade. Sem alteração de números, tabelas, figuras ou código.

- **B1 (§1.1):** o enquadramento da lacuna passa a incluir a de-anonimização
  baseada em aprendizado de máquina ao lado da Privacidade Diferencial.
- **B2 (§1.3):** parágrafo, após a fronteira de Narayanan, situando o adversário
  aprendido contemporâneo (*embeddings* de grafo + aprendizado adversarial
  federado) como **estritamente mais forte** que os cenários estruturais básicos
  medidos — leitura de **cota inferior** (§6.1).
- **Apêndice B — reconciliado à §12:** até D6 o apêndice listava 14 entradas +
  2 adendos ([15] Narayanan 2009, [16] Wang 2023) e não incorporava as 5 refs de
  D2/D3 (Brito, Hao, Mendonça, Mueller, Yuan), já citadas na §2.1. D7 reconcilia
  o apêndice à lista canônica completa: **21 entradas alfabéticas**, mesma
  numeração da §12, sem mecanismo de adendo (Wang = **[18]**).

**Reflexo público:** `README.md` §12 passou de 20 → **21** entradas — Wang et al.
(2023) entra como **[18]** (Wörlein→[19], Yuan→[20], Zhou→[21]). **BibTeX +
link** versionados em `references/README.md`; PDF local do autor (gitignored).
Detalhamento espelhado em
[`artigo_rastreabilidade.md`](artigo_rastreabilidade.md) (§Revisão D7).
Selecionado **apenas Wang et al. (2023)** entre os candidatos (Wang 2023; Yuan
2024; Liu 2025).

---

## Revisão D8 — consolidação de motor: baseline Facebook migrado para pymetis (2026-06-27)

Rodada de **consolidação de motor de particionamento**, **sem issue vinculada**
(fecha o follow-up de D4/D6). **Origem:** apontamento dos avaliadores
(orientador/coorientador) sobre a **incongruência** de o baseline Facebook rodar
em Kernighan-Lin enquanto Enron e d-sweep rodavam em pymetis. A consolidação num
**motor único (pymetis)** foi tratada como **mandatória**, ainda que ao custo de
enfraquecer parcialmente um achado.

- **Texto do relatório (`academic/relatorio_tecnico.md`, privado):** §5.1
  (tabela agregada + leitura da curva + nota do motor "achado A1 → resolvido"),
  §5.2 (leitura B1: 0,79/0,026 → 0,1454/0,0232), §5.5 (tabela B1: ~30× → ~6×),
  §5.6 (painel: faixas, cruzamentos e decaimento em pymetis; degrau ~6× → ~1,2×),
  §6.2 (ameaça C2 "motor não-pareado" → **RESOLVIDA**) e Apêndice A.1 (tabela
  bruta do FB em pymetis) migrados do run KL para o run pymetis (E1/#211, D-19).
- **Marco 29/05 (achado enfraquecido, registrado com fidelidade):** sob pymetis
  o Facebook só atinge cobertura plena em k=2/5; k=10/20 caem a
  `FAILURE_LOW_COVERAGE` (0,8647). O marco fica **certificado sobre o run KL**
  (validação DL-01, fato histórico não retificado), retido como registro
  histórico, **não** como baseline canônico — trade-off aceito pela consistência
  inter-dataset.
- **Figura:** painel `comparison_fb_enron` (canônico + variante `eng-`)
  regenerado em pymetis (D8); ver `artigo_rastreabilidade.md` §Revisão D8.
- **Reflexo público:** `docs/results_baseline.md` (já pymetis, E1),
  `docs/results_enron.md` (migrado), `docs/limitations.md` (C2 + trabalho futuro
  marcados resolvidos), esta seção. **Artigo já consistente** (migrado em D4); o
  relatório agora o acompanha — o artigo é derivado do relatório.
