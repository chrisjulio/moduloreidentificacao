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
`rr_subgrafo ≫ rr_grau` nos dois datasets (**~6× no Facebook e ~38× no
Enron** em k=2, sob **motor de particionamento unificado (pymetis)** — ver
Revisão D4 abaixo; os valores anteriores ~30–38× referiam-se ao run
Kernighan-Lin do Facebook, substituído por pymetis em E1/#211, D-19);
contribuição = módulo como **aferidor formal** + curva privacidade-utilidade
(DL-06 como premissa fundadora).

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
| 4. Resultados | §5.1–§5.7 | [`results_baseline.md`](results_baseline.md); [`results_enron.md`](results_enron.md); [`results_dsweep.md`](results_dsweep.md) | DL-04; D-17 (menção); **D-19** (motor pymetis) | **W-04**; W-06 | curvas por dataset (Fig. 2–3, regeneráveis); painel normalizado (Fig. 4, [`assets/comparison_fb_enron.png`](assets/comparison_fb_enron.png) — **asset ainda em KL, regen pendente, D4**); **d-sweep Enron (Fig. 5, [`assets/enron_dsweep_series.png`](assets/enron_dsweep_series.png), V2/#215; tabela [`results_enron_dsweep.md`](results_enron_dsweep.md), V1/#214 — §4.6 expandida em D5)**; Tabelas 2–4 (agregados por k, **Facebook em pymetis após D4**; gap k=2) | W2d ✅; **D4 ✅**; **D5 ✅** |
| 5. Discussão | §6.1–§6.3 + §2.3 | [`limitations.md`](limitations.md) §1/§3/§4; [`scope.md`](scope.md) §8 | B2; C2/A1; D-17 (substância, sem codinome) | W-04 (leitura); W-05 | — | W2e ✅ |
| 6. Conclusão + futuros | §2.3/§6.1 | [`scope.md`](scope.md) §8; [`limitations.md`](limitations.md) §4 | DL-06 (fecho) | — | — | W2e ✅ |
| Revisão integrada | relatório completo | [`progress.md`](progress.md) | todas | coerência W-04/W-05 | conferência | W2f ✅; **revisão final D6 ✅** |

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
>
> **Atualização (D6/#221, 2026-06-26):** a revisão integrada final **fechou a
> lacuna citação↔lista** que D2/D3 haviam aberto no fonte Markdown
> (`academic/artigo.md`): as 5 referências de D2/D3 (Brito & Machado 2024;
> Hao et al. 2024; Mendonça et al. 2023; Mueller et al. 2022; Yuan et al.
> 2023) estavam citadas na §2 mas **ausentes** da lista de Referências do
> artigo (que fechara em 12 na W2f). Foram adicionadas em ordem alfabética,
> com metadados conferidos contra o README §12 de `main`. A lista do artigo
> passa a **18 entradas** (17 da literatura + autorreferência Brito 2026). As
> omissões intencionais reduzem-se a **três** — Wörlein 2005, Díaz 2003 e
> Serjantov & Danezis 2003 —, as únicas ausências mesmo com o README §12 já em
> 20 entradas.

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
   substituídos (orientador e coorientador — titulações confirmadas); legenda
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

Rodada de revisão orientada pelo retorno do orientador e do coorientador,
executada **somente no texto** (academic/, privado) com os reflexos
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

---

## Revisão metodológica D4 (#219) — migração KL → pymetis e reenquadramento (2026-06-26)

Rodada orientada pelo retorno dos avaliadores externos (orientador e
coorientador), respondendo a limitações percebidas que pediam
**recontextualização metodológica**. **Diferentemente das rodadas D1–D3,
esta altera números e tabelas** — incorpora o dado canônico inter-dataset
fixado em E1 ([#211](https://github.com/chrisjulio/moduloreidentificacao/issues/211),
decisão **D-19** em [`decision_log.md`](decision_log.md)): o run **pymetis**
do baseline Facebook substitui o run **Kernighan-Lin**. Os números do Enron
**não** mudam (já corria em pymetis, #126).

Escopo: **apenas este repositório** — texto privado (`academic/artigo.md`,
gitignored, fora do diff) + esta rastreabilidade pública. As versões
compiladas (Overleaf) são portadas pelo autor, cada uma no seu contexto.

**Ajustes no texto do artigo (privado):**

- **§3.2 — baseline canônico + motor unificado.** He et al. (2009) e a técnica
  única reenquadrados como **escolha deliberada de baseline canônico** (régua
  reprodutível, não esgotamento do espaço de técnicas); particionamento
  reescrito de "METIS com fallback Kernighan-Lin" para **pymetis unificado nos
  dois datasets**, com fallback KL desabilitado (`allow_kl_fallback: false`).
- **§3.5 / §4.3 — escala do Enron explícita.** Razão **~63×** tornada explícita
  (n=33.696 vs n=532), evidenciando o Enron como dataset secundário **já no
  pipeline**.
- **§4 — propagação total KL → pymetis.** Tabela 2 e todos os números
  dependentes (abstract, §1, §4.2, §4.4/Tabela 4, §6, tese central) migrados
  para pymetis. **Gap Facebook k=2: ~30× → ~6×** (0,1454 vs 0,0232); headline
  passa a **"~6× Facebook / ~38× Enron"**.
- **§5 — reenquadramento metodológico.** O "motor não-pareado KL×METIS",
  antes ameaça à validade com argumento interpretativo de inocuidade em d=1,
  passa a **motor unificado (pymetis)** — decisão metodológica, não correção;
  o confundidor é eliminado (§4.5 cai de 3 para 2 confundidores). Técnica
  única reafirmada como escolha de baseline, não limitação acidental.

**Consequências narrativas registradas (fidelidade ao dado canônico, sem
suavização):** sob pymetis o Facebook **não** atinge k-anonimato em k=10/20
(FAILURE_LOW_COVERAGE, cobertura 0,8647 — só k=2/5 passam; o marco 29/05
permanece válido sobre o run KL, D-19); a punch "quatro em cada cinco" (0,7914)
vira leitura de gap (~6×); o Facebook **não** viola mais a cota 1/k (a violação
empírica de d=1 sobrevive só em Enron/k=20); a taxa por subgrafo do Facebook
deixa de ser estritamente monótona.

**Figura 4 (painel normalizado) — pendência sinalizada.** A prosa do §4.5 já
usa valores pymetis; o **asset versionado**
[`assets/comparison_fb_enron.{png,pdf,csv}`](assets/comparison_fb_enron.png)
ainda reflete o Facebook em KL. Por decisão do autor (D4), a regeneração do
asset para pymetis fica como **follow-up sinalizado** — este PR é **docs-only**
(não toca assets versionados nem o código congelado). Os checklists de
cobertura W2b..e do texto privado permanecem como rastro histórico do estado
pré-D4.

---

## Revisão D5 (#220) — §4.6 expandida com o d-sweep Enron (2026-06-26)

Issue [D5](https://github.com/chrisjulio/moduloreidentificacao/issues/220).
Desbloqueada por **E3** (#213, d-sweep Enron concluído), **V1** (#214, tabela
[`results_enron_dsweep.md`](results_enron_dsweep.md)) e **V2** (#215, figuras
[`assets/enron_dsweep_series.{pdf,png}`](assets/enron_dsweep_series.png) e
`enron_dsweep_facets.{pdf,png}`) — as três **CLOSED**, verificadas antes de
iniciar; nenhum PR aberto.

**Escopo:** §4.6 do artigo (texto privado `academic/artigo.md`, gitignorado,
fora do diff). Até D4 a §4.6 cobria **apenas o Facebook**; D5 a estende com o
d-sweep do Enron, respondendo à **questão de pesquisa central** do
experimento: o deslocamento do vetor de ataque com `d` crescente se replica
numa rede ~63× maior?

**Resposta registrada (fidelidade ao dado):** **parcial**. A §4.6 agora
contrasta os dois datasets e **diverge explicitamente da prosa de
[`results_enron_dsweep.md`](results_enron_dsweep.md) §4.1** (que afirma que o
deslocamento "se confirma"): a tabela consolidada mostra que **apenas a
metade estrutural se replica**.

- **Replica (robusto à escala):** EGS ≈ k·d vale quase exatamente no Enron
  (k=2/d=10 → 19,99; k=20/d=10 → 198,21), mais limpo que no Facebook (133,0)
  e **sem `FAILURE_LOW_COVERAGE`** na grade (48/48 `SUCCESS_PARTIAL`,
  cobertura ≥ 0,987); o ataque por subgrafo **enfraquece monotonicamente com
  d em todo k** (k=2: 0,124→0,053; k=20: 0,057→0,017), ao custo de utilidade
  crescente (KS-D até 0,304).
- **Não replica (efeito de rede pequena):** o ataque por grau **não se
  fortalece** — fica colado ao piso (~0,002–0,003) em toda a grade,
  declinando levemente em k alto, mesmo sob forte distorção de graus. Logo
  **não há cruzamento**: o subgrafo permanece o vetor dominante nas 16
  células (k=20/d=10: 0,017 subgrafo vs. 0,001 grau). O *deslocamento* é
  **dependente de escala**.

**Figuras/tabelas:** **Figura 5** inserida e referenciada (V2/#215, snapshot
versionado `docs/assets/enron_dsweep_series.{pdf,png}`); tabela completa em
`docs/results_enron_dsweep.md` (V1/#214) referenciada. PR **docs-only** —
não toca assets versionados nem o código/experimentos congelados.

**Coerência pendente para D6 (#221, revisão integrada final):** §5.1 ("no
Enron, apenas o regime d=1 foi medido") e §6 (d-sweep Enron listado como
trabalho futuro) ficaram **superadas** por D5 e devem ser reconciliadas na
revisão integrada — fora do escopo de D5, sinalizadas aqui e na nota D5 do
texto privado.

---

## Revisão integrada final D6 (#221) — conferência de consistência (2026-06-26)

Issue [D6](https://github.com/chrisjulio/moduloreidentificacao/issues/221) —
passagem final de consistência do artigo após a rodada D1–D5. **Bloqueada por
D1–D5** (#216–#220): todas verificadas **CLOSED e mergeadas em `main`** via
`gh` antes de iniciar (#231 — D5 — é o último merge); nenhum PR aberto.

**Escopo:** apenas este repositório — texto privado (`academic/artigo.md`,
gitignorado, fora do diff) + esta rastreabilidade pública. Sem código
(congelado), sem novos experimentos. PR **docs-only**.

### Consistência numérica — conferida, nenhuma divergência

Reconferência de todos os números do artigo contra os relatórios versionados
em `main` (regeneráveis dos logs JSONL): **Tabela 2** = `results_baseline.md`
(run pymetis E1/#211, exata); **Tabela 3** = `results_enron.md` (exata);
**Tabela 4 + tese central** = k=2 dos dois datasets (FB 0,1454/0,0232 → 6,3×;
Enron 0,1241/0,0033 → 37,6×; razões ~6×/~38×); **§4.6 d-sweep Enron** =
`results_enron_dsweep.md` (subgrafo, EGS 19,99 / 198,21, KS-D, cobertura
≥ 0,9877, piso de grau — exatos); **§4.6 d-sweep Facebook** =
`results_dsweep.md` (EGS 19,70 / 133,0; cobertura mínima 0,752; zero
timeouts). A divergência **intencional** da §4.6 em relação à prosa de
`results_enron_dsweep.md` §4.1 (que afirma que o deslocamento "se confirma")
foi mantida — o artigo segue o dado da tabela (só a metade estrutural
replica), já assinalada em D5.

### Reconciliação de coerência pós-D5 (pendência herdada)

As duas passagens **superadas** por D5 foram reconciliadas no texto privado:

- **§3.5** — a varredura `d ∈ {1,2,5,10}` (48 execuções por dataset) passou de
  "sobre o Facebook" para **"sobre os dois datasets"**, coerente com a §4.6.
- **§5.1 ¶1** — removida a frase "no Enron, apenas o regime `d=1` foi medido";
  o parágrafo incorpora o achado do d-sweep Enron (metade estrutural robusta à
  escala; deslocamento dependente de escala pequena) e **resta um único
  resíduo** (múltiplas ego-redes).
- **§6 ¶2** — a "replicação da varredura de profundidade no segundo dataset"
  saiu da enumeração de futuros (já executada, D5) e foi registrada como
  verificação **já realizada**; futuros renumerados (i)–(iv).

### Terminologia — uniforme

Baseline de avaliação de risco (D1) consistente do abstract à discussão;
distinção DP vs. anonimização estrutural (D2) coerente em todas as ocorrências
(§2, abstract, §1, §5.4), sempre como diferença de premissas; "cota inferior"
uniforme (abstract, §4.3, §5.2, §6).

### Referências — completude citação↔lista fechada

**Achado central de D6:** as 5 referências de D2/D3 (Brito & Machado 2024; Hao
et al. 2024; Mendonça et al. 2023; Mueller et al. 2022; Yuan et al. 2023)
estavam **citadas na §2 mas ausentes da lista de Referências** do artigo (que
fechara em 12 na W2f, antes de D2/D3). Foram **adicionadas em ordem
alfabética**, metadados conferidos contra o README §12 de `main`; a lista do
artigo passa a **18 entradas** (17 da literatura + autorreferência Brito
2026). Verificação bidirecional refeita: toda entrada citada no corpo; nenhuma
citação fora da lista. As 3 omissões intencionais (Wörlein 2005; Díaz 2003;
Serjantov & Danezis 2003) seguem como as únicas ausências.

### Pendências herdadas, não resolvidas em D6 (decisão do autor)

- Regeneração do asset `docs/assets/comparison_fb_enron.{png,pdf,csv}` para
  pymetis (follow-up sinalizado em D4) — a prosa do §4.5 já usa pymetis.
- Identificador estável (tag/release ou DOI) da autorreferência Brito (2026).

**Definição de pronto (#221):** números conferidos e consistentes ✅;
terminologia uniforme ✅; referências completas e citadas ✅;
`artigo_rastreabilidade.md` atualizado ✅; PR em `docs/artigo-revisao-final`
✅.
