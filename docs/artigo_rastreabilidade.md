# Matriz de rastreabilidade — Artigo (#175)

> **Propósito.** Rastreabilidade **pública** da redação do artigo (issue
> [#175](https://github.com/chrisjulio/moduloreidentificacao/issues/175),
> S10-W2). O texto substantivo do artigo vive em `academic/` (**privado**,
> gitignorado — PR #176; backup externo do autor) e **não** é versionado neste
> repositório; o que se versiona é esta matriz: seção → insumo no relatório →
> fontes → `W-NN` → figuras, mais o sumário do esqueleto. Mesma regra de
> privacidade do relatório (decisão do autor, 2026-06-09, DoD emendada).
>
> **Insumo primário:** o relatório técnico
> ([#174](https://github.com/chrisjulio/moduloreidentificacao/issues/174),
> concluído e revisado em 2026-06-10 — ver
> [`relatorio_rastreabilidade.md`](relatorio_rastreabilidade.md)). O artigo é
> **derivado**: mesma evidência, narrativa comprimida para par revisor.
>
> Criada na etapa **S10-W2a** (esqueleto + matriz). Atualizada a cada etapa
> de redação (S10-W2b..f). Desdobramento **validado pelo autor na #175 em
> 2026-06-10** (sem sub-issues; agrupamento como proposto; sem venue/template
> por ora — Markdown neutro, conversão posterior).

---

## Sumário do artigo (esqueleto, 6 seções)

Estrutura mínima fixada pela #175:

1. Resumo/abstract e Introdução (problema + contribuição: aferidor formal)
2. Trabalhos relacionados (recorte mínimo citável)
3. Método condensado (pipeline; parâmetros uniformes — DL-05)
4. Resultados (curva privacidade-utilidade; comparativo FB×Enron; B1/W-04)
5. Discussão (validade externa; resultado negativo como contribuição defensiva)
6. Conclusão e trabalhos futuros (Fase 2 temporal; sem comprometer enquadramento)

Tese central: **frase-síntese B1 generalizável (W-04)** — em `d=1`,
`rr_subgrafo ≫ rr_grau` nos dois datasets (~30–38× em k=2); contribuição =
módulo como **aferidor formal** + curva privacidade-utilidade (DL-06 como
premissa fundadora).

Seções do relatório que **não** viram seção no artigo: §7 (reprodutibilidade
→ 1 parágrafo no método), §8 (ética → 2–3 frases na introdução), Apêndice A
(tabelas brutas → artigo usa agregados por k).

---

## Matriz seção → insumo (relatório) → fontes → `W-NN` → figuras

| Artigo | Insumo (relatório #174) | Fontes (docs) | Decisões citáveis | `W-NN` | Figuras/Tabelas | Etapa |
|---|---|---|---|---|---|---|
| 1. Resumo + Introdução | §1.1–§1.4 | [`scope.md`](scope.md) §4/§5/§6 | **DL-06** | — | — | W2b ✅ (abstract final reescrito na W2e ✅) |
| 2. Trabalhos relacionados | §1.3/§2.1; Apêndice B | `README.md` §12 (subconjunto de 7 refs) | — | — | — | W2b ✅ |
| 3. Método condensado | §3–§4 | [`pipeline.md`](pipeline.md); [`metrics_definitions.md`](metrics_definitions.md) | DL-05; D-16; D-11; DL-01 | W-01; W-02; W-03; W-05 | diagrama do pipeline; tabela de parâmetros | W2c ✅ |
| 4. Resultados | §5.1–§5.7 | [`results_baseline.md`](results_baseline.md); [`results_enron.md`](results_enron.md); [`results_dsweep.md`](results_dsweep.md) | DL-04; D-17 (menção) | **W-04**; W-06 | curvas por dataset (Fig. 2–3, regeneráveis); painel normalizado (Fig. 4, [`assets/comparison_fb_enron.png`](assets/comparison_fb_enron.png)); Tabelas 2–4 (agregados por k; gap k=2) | W2d ✅ |
| 5. Discussão | §6.1–§6.3 + §2.3 | [`limitations.md`](limitations.md) §1/§3/§4; [`scope.md`](scope.md) §8 | B2; C2/A1; D-17 (substância, sem codinome) | W-04 (leitura); W-05 | — | W2e ✅ |
| 6. Conclusão + futuros | §2.3/§6.1 | [`scope.md`](scope.md) §8; [`limitations.md`](limitations.md) §4 | DL-06 (fecho) | — | — | W2e ✅ |
| Revisão integrada | relatório completo | [`progress.md`](progress.md) | todas | coerência W-04/W-05 | conferência | W2f ✅ |

Todos os `W-NN` referenciados estão **resolvidos** no
[`artifact_writing_checklist.md`](artifact_writing_checklist.md); a redação
incorpora, não reabre. O inventário de figuras/tabelas citáveis é o mesmo do
relatório — ver [`relatorio_rastreabilidade.md`](relatorio_rastreabilidade.md)
§Inventário (não duplicado aqui).

> **Nota de assimetria intencional (W2f) — Narayanan & Shmatikov 2009
> (README §12 [9]; adendo [15] do Apêndice B do relatório).** O **artigo**
> cita o paper de 2009 no corpo (Seção 2, trabalhos relacionados); o
> **relatório** o registra apenas como adendo pós-fechamento ao Apêndice B,
> **sem citação no corpo** — a #174 estava fechada quando a decisão A+B do
> autor (2026-06-10, #175) adicionou a referência. A diferença é
> **intencional e rastreável** (decisão A+B em
> [`artigo_execucoes.md`](artigo_execucoes.md)), não inconsistência entre os
> dois documentos.
>
> **Nota de referências (W2f).** O artigo fecha com **12** das 15 referências
> do README §12. As 3 ausências — Wörlein 2005 (comparação de mineradores
> FSM), Díaz 2003 e Serjantov & Danezis 2003 (entropia como métrica de
> anonimato) — são **omissões intencionais justificadas**: o artigo não
> discute a escolha do minerador FSM nem reporta valores de entropia
> (justificativa detalhada no texto privado, Nota de consolidação das
> Referências; revisável pelo autor na conversão final).

---

## Estado por etapa (S10-W2a..f — validado pelo autor em 2026-06-10)

| Etapa | Escopo | Status |
|---|---|---|
| W2a | Esqueleto em `academic/artigo.md` + esta matriz + registro de execuções | ✅ concluída (PR #188 MERGED, 2026-06-10) |
| W2b | Seções 1–2 (introdução + trabalhos relacionados; abstract provisório) | ✅ concluída (PR #191 MERGED, 2026-06-10; complemento A+B via PR #193) |
| W2c | Seção 3 (método condensado — compressão de §3–§4 do relatório) | ✅ concluída (PR #194 MERGED, 2026-06-10) |
| W2d | Seção 4 (resultados — a mais pesada; sessão própria) | ✅ concluída (PR #195 MERGED, 2026-06-10) |
| W2e | Seções 5–6 (discussão + conclusão) + abstract final | ✅ concluída (PR #196 MERGED, 2026-06-10) |
| W2f | Revisão integrada (coerência com o relatório e `main`) + DoD da #175 | ✅ concluída (2026-06-10 — **fecha a #175**) |

> Desdobramento espelha o padrão validado do relatório (S10-W1a..f, #174).
> Rastreio: **sem sub-issues** — comentário de execução na #175 +
> [`artigo_execucoes.md`](artigo_execucoes.md), como na #174. **Validado pelo
> autor na #175 em 2026-06-10** (3 pontos abertos decididos: modelo de
> rastreio da #174; agrupamento como proposto; sem venue/template por ora).
