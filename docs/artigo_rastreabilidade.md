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
> (README §12 [13]; adendo [15] do Apêndice B do relatório).** O **artigo**
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
>
> **Atualização (rodada pós-W2f, 2026-06-11):** a parte desta nota relativa
> a Díaz/Serjantov ficou **superada** — a compilação de 11/06/2026 (versão
> LaTeX) **incluiu** Díaz et al. 2003 e Serjantov & Danezis 2003 (citadas na
> §4.6, no enquadramento da métrica de entropia) e a autorreferência Brito
> 2026, fechando a lista compilada em **15 entradas** (citação↔lista nos
> dois sentidos). **Wörlein 2005 permanece como a única omissão
> intencional.**

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

---

## Rodada pós-W2f (2026-06-11) — correções do autor sobre a versão compilada

Decisões consolidadas pelo autor em 2026-06-11, aplicadas ao texto privado
(`academic/artigo.md`) e à versão compilada (projeto LaTeX/Overleaf; PDF de
11/06/2026). Sem alteração de números, tabelas ou resultados (congelados);
sem alteração de código.

1. **Claim de disponibilidade (§3.5 — opção B do autor):** a frase final do
   método passou a afirmar como artefato público os **relatórios
   consolidados gerados dos logs** — não os logs brutos, que não são
   versionados (README §7; `scripts/replication/README.md` §8); os logs
   brutos são descritos como **regeneráveis** a partir das configurações
   versionadas, pelo pipeline de replicação documentado. A abertura da
   Seção 4 ("consolidados em relatórios versionados") já era compatível e
   não foi alterada.
2. **Referência Brito (2026):** descrição alinhada ao item 1 — "código-fonte,
   configurações e **relatórios** dos experimentos". **Pendência aberta:**
   o identificador estável (tag/release ou DOI) **ainda não existe** — o
   PR [#199](https://github.com/chrisjulio/moduloreidentificacao/pull/199)
   mergeado em 2026-06-11 tratou do registro D-18 (sigma do FSM), não do
   identificador, e o repositório não possui tags nem releases. O campo de
   versão da referência será preenchido quando o identificador for criado.
3. **Terminologia cenário × ataque (decisão do autor):** o corpo do artigo
   adota os rótulos das legendas das figuras — **ataque por grau / ataque
   por subgrafo** —, com **ponte de nomenclatura** inserida na §3.3
   (sentido de simulação controlada interna ao ciclo experimental fechado,
   nunca procedimento ofensivo contra indivíduos). Âncoras do enquadramento
   preservadas: título da §3.3 ("Cenários formais de reidentificação"),
   abstract ("dois cenários formais de reidentificação"), parágrafo de
   fronteira do Capítulo 1 e §3.4 ("taxa de reidentificação por cenário").
   **Substitui** a recomendação anterior de renomear as legendas das
   Figuras 4.1/4.2/4.4 — nenhuma figura foi regenerada.
4. **Setas tipográficas:** padronização global de `→` (U+2192) para `->`
   no corpo do artigo (§4.1, §4.5, §4.6; abstract, §1, §3.1 e §6 já usavam
   `->`).
5. **Ano 2003 (PET 2002 / LNCS 2482):** o artigo já estava correto;
   harmonizados os documentos internos que citavam 2002 — relatório técnico
   §5.7, [`metrics_definitions.md`](metrics_definitions.md),
   [`algorithm_notes.md`](algorithm_notes.md) — e **errata** anotada ao
   final da entrada D-17 do [`decision_log.md`](decision_log.md) (registro
   histórico não reescrito).
6. **Folha de rosto e Figura 3.1 (versão compilada):** placeholders da capa
   substituídos (orientador Prof. Dr. André Luís Vignatti; coorientador
   Prof. Dr. Sidgley Camargo de Andrade — titulações confirmadas); legenda
   da Figura 3.1 sem o rastro "[Convertida do diagrama Mermaid...]".
7. **Figura 4.3 vetorial:** a versão compilada passou a usar o **PDF
   vetorial** do painel comparativo — o mesmo artefato versionado em
   [`assets/comparison_fb_enron.pdf`](assets/comparison_fb_enron.pdf)
   (PR [#200](https://github.com/chrisjulio/moduloreidentificacao/pull/200),
   regenerado dos logs congelados pelo gerador existente, sem mudança de
   código; PNG e CSV byte-idênticos).
8. **Origem nominal:** o endereço público do repositório citado no artigo é
   `github.com/chrisjulio/reidentificacao` (URL confirmada pelo autor); a
   documentação interna usa `chrisjulio/moduloreidentificacao` como origem.
   Fica registrado o alinhamento — relatório e artigo apontam para o mesmo
   repositório. *(Verificação de 2026-06-11: o endereço público ainda não
   estava ativo; pendência associada ao identificador do item 2.)*

---

## Revisões D1–D3 — reposicionamento como baseline + atualização bibliográfica (2026-06-26)

Rodada de revisão orientada pelo retorno dos professores André Vignatti e
Sidgley, executada **somente no texto** (academic/, privado) com os reflexos
públicos abaixo. Sem alteração de números, tabelas, figuras ou código.

- **D1 (issue #216) — abstract + §1 do artigo e §1.1 do relatório:**
  reposicionamento explícito do trabalho como **baseline de avaliação de
  risco** para k-anonimato estrutural de grafos, com a **lacuna metodológica**
  (ausência de baselines padronizados na subárea, mesmo diante do avanço da
  Privacidade Diferencial) declarada desde o primeiro parágrafo. Reflexo
  público: nenhum (texto em `academic/`).
- **D2 (issue #217) — §2 do artigo (trabalhos relacionados) e §2.1 do
  relatório:** parágrafo diferenciando **Privacidade Diferencial** (proteção
  de consultas/estatísticas agregadas; *query release*; garantia
  semântica/ε) de **anonimização estrutural por k-anonimato** (publicação do
  grafo completo para *graph mining*; garantia sintática). Tom: diferença de
  premissas e casos de uso, não detrimento da DP.
- **Incorporação formal de referências (público):** duas referências de DP em
  grafos citadas no texto foram adicionadas à lista canônica `README.md` §12 e
  ao catálogo `references/README.md`, com PDFs de acesso aberto (SOL/SBC)
  baixados:
  - **[2]** Brito & Machado (2024) — *Differentially Private Release of
    Count-Weighted Graphs* (SBBD 2024).
  - **[10]** Mendonça, Brito & Machado (2023) — *Privacy-Preserving Techniques
    for Social Network Analysis* (SBBD 2023, survey). *(Entrou como [9] no D2;
    renumerada para [10] pelo D3 — ver abaixo.)*
  A §12 passou de 15 para 17 entradas no D2 (e a **20** no D3) e foi
  **renumerada** (ordem alfabética preservada).
- **D3 (issue #218) — atualização bibliográfica > 2020 (§2 do artigo e §2.1 do
  relatório):** três referências recentes verificadas (metadados via
  DBLP/arXiv), uma por subárea, citadas inline no §2 e incorporadas à
  `README.md` §12 + catálogo `references/README.md`:
  - **[5]** Hao, Li, Chang & Gu (2024) — *MLDA: a multi-level k-degree
    anonymity scheme on directed social network graphs* (Frontiers of Computer
    Science) — anonimização estrutural, **2024** (> 2023).
  - **[11]** Mueller, Usynin, Paetzold, Rueckert & Kaissis (2022) — *SoK:
    Differential Privacy on Graph-Structured Data* (arXiv) — taxonomia DP em
    grafos.
  - **[19]** Yuan, Zhang, Du, Chen, Cheng & Sun (2023) — *PrivGraph:
    Differentially Private Graph Data Publication...* (USENIX Security) —
    publicação de grafo sob DP.
  A §12 passou de 17 para **20** entradas (renumerada): Mendonça migrou
  **[9]→[10]** e Narayanan & Shmatikov 2009 **[11]→[13]** (atualizada na nota
  de assimetria desta matriz). **Apenas BibTeX e links** versionados — os PDFs
  foram obtidos **localmente pelo autor** (gitignored, não commitados). de Jong
  et al. (2024, arXiv) **descartado** — mesmo grupo retido para deliberação com
  os orientadores. Meta da issue cumprida: ≥3 refs > 2020; ≥1 > 2023 (Hao 2024).
