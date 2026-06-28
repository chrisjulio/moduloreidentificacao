# progress.md — Estado de progresso das sessões

> **Instrução ao agente:** Este arquivo deve ser lido no início de cada sessão
> (`leia docs/progress.md e continue de onde paramos`) e atualizado ao final de
> cada sessão produtiva.
>
> **Onde está o estado de retomada.** A leitura tem teto (~25 mil tokens ≈ as
> primeiras ~640 linhas); um `Read` único **não** carrega o arquivo inteiro.
> Por isso o que importa para retomar — **"Estado atual"**, **"Último passo
> concluído"** e **"Próximo passo"** — vive no **topo**. O que está mais abaixo
> (Histórico) é referência, consultável por `Grep`/paginação, não pela leitura
> inicial.
>
> **Histórico e repaginação.** Mantenha o histórico — não apague entradas;
> adicione novas no topo da seção "Histórico". **Regra de transição:** quando
> este arquivo atingir **2500 linhas**, repagine — migre as entradas de sessão
> **mais antigas** para [`progress_archive.md`](progress_archive.md)
> (mais novas no topo lá também), preservando aqui a era de trabalho corrente,
> até o arquivo voltar com folga abaixo de 2500. Registre a data e o intervalo
> migrado no cabeçalho do `progress_archive.md`.

---

## Estado atual

**Data da última atualização:** 2026-06-27

**Semana corrente:** S10 — **concluída**: relatório técnico (#174, fechada em
2026-06-10) e artigo (#175, fechada em 2026-06-10 via PR #197/W2f — MERGED).
Código **congelado** — somente análise e documentação. Issues de visualização
Desejável (#214 e #215) concluídas em 2026-06-25. Issue E1 (#211) concluída em
2026-06-25 (reexecução baseline Facebook com pymetis). **Rodada D1–D3
(#216/#217/#218)** — revisão pós-entrega do conteúdo acadêmico — concluída em
2026-06-26 (reposicionamento como baseline + defesa frente à DP + atualização
bibliográfica > 2020). **Rodada D4 (#219)** — revisão metodológica do artigo
(migração KL → pymetis + motor unificado + baseline canônico + escala Enron) —
concluída em 2026-06-26 (PR `docs/artigo-revisao-metodologia`). **Rodada D5
(#220)** — §4.6 do artigo expandida com o d-sweep Enron — concluída em
2026-06-26 (PR `docs/artigo-revisao-dsweep-enron`). **Rodada D6 (#221)** —
revisão integrada final do artigo (consistência numérica + terminologia +
referências + reconciliação de coerência pós-D5) — concluída em 2026-06-26
(PR #232, `docs/artigo-revisao-final`). **Rodada D8 (sem issue)** — painel
comparativo `comparison_fb_enron` regenerado em pymetis (canônica + `eng-`) e
`results_enron.md` migrado para pymetis (mesmos motores), fechando o follow-up
de D4/D6 — concluída em 2026-06-27 (branch `viz/comparison-fb-enron-pymetis`).

**Último passo concluído:**
- **Correção da §4.1 de `results_enron_dsweep.md` — replicação parcial do
  d-sweep (2026-06-27). ✅ (docs, PR #236 `docs/enron-dsweep-s41-partial-replication`).**
  A prosa da §4.1 contradizia a própria tabela da §2 do arquivo: afirmava que
  "grau se fortalece com d crescente" e que o deslocamento grau↑/subgrafo↓ "se
  confirma no Enron". A tabela mostra `reid_sub` enfraquecendo com d (✔), mas
  `reid_deg` **colado ao piso** (~0,002–0,004) em toda a grade — sem cruzamento
  de vetores; o subgrafo permanece dominante nas 16 células (k=20/d=10: 0,017
  subgrafo vs 0,001 grau). **Causa:** numa rede de ~33,7 k nós, colisões de grau
  são abundantes e mesmo anonimização agressiva (KS D até ~0,30) raramente isola
  um grau único — o deslocamento visto no Facebook é dependente da escala pequena
  daquela ego-rede, não lei do mecanismo. §4.1 reescrita para declarar replicada
  **só a metade estrutural** (subgrafo↓ com d; EGS ≈ k·d) e ler o
  deslocamento/cruzamento como **replicação parcial / dependente de escala**
  (título da §4 e §4.2 mantidos). Como a prosa vive no gerador
  `experiments/make_enron_dsweep_table.py` (fonte de verdade), editados o gerador
  **e** o doc; tabela regenerada — saída bate com a edição manual. Alinha a §4.1
  ao artigo LaTeX (§4.6) e ao `relatorio_mudancas_orientadores.md` (Parte I §5 /
  Parte II item 3). Sem alteração de código de produção, números ou figuras.
- **Release `v1.0.0` publicado + terminologia baseline (ponto A) — 2026-06-27.
  ✅ (GitHub + academic).** PR #233 mergeado em `main` (`cd0c4cb`); **release
  [`v1.0.0`](https://github.com/chrisjulio/moduloreidentificacao/releases/tag/v1.0.0)**
  publicado a partir de `main`. **Nota de execução:** o 1º release **não
  arquivou** (toggle do repo no Zenodo estava OFF; vincular o login ≠ ligar o
  repo); após ligar o toggle, o `v1.0.0` foi **apagado e recriado** (autorizado)
  e o Zenodo arquivou, cunhando o **concept DOI `10.5281/zenodo.20973364`**
  (todas as versões). Embutido em `CITATION.cff`, no badge do `README.md` e na
  ref Brito (2026). **Ponto A da orientação aplicado:**
  "benchmark" → "baseline" nos entregáveis (conclusão do artigo §6; cabeçalho +
  checklist da §2.3 do relatório). **Mantidos por decisão do autor:** o título
  do paper Liu et al. (2025, *PGB: Benchmarking…*, citação direta) e 3 menções
  em logs históricos (`relatorio_execucoes.md`, `progress.md`) ao antigo título
  da §2.3 (regra de não reescrever histórico). Mudança nos entregáveis vive em
  `academic/` (gitignored); reflexo público na §Revisão D7 de
  `artigo_rastreabilidade.md`. **Resolvido (2026-06-27):** PR
  `docs/v1.0.1-baseline-and-doi` mergeado (`0401a68`), DOI embutido (`7fe0176`)
  e Zenodo arquivado — a pendência do identificador estável da ref Brito (2026)
  está **fechada**.
- **Rodada D8 — painel comparativo regenerado em pymetis + `results_enron.md`
  migrado (2026-06-27). ✅ (docs, branch `viz/comparison-fb-enron-pymetis`).**
  Fecha o follow-up de D4/D6. **Diagnóstico (git):** o painel canônico
  `comparison_fb_enron.{png,pdf,csv}` estava intocado desde antes de 21/06
  (`4f5668b`/`c3a72fa`, **KL**); a variante `eng-comparison_fb_enron.pdf`
  **deriva do CSV canônico** (a re-gravação de E1 `14097e5` foi no-op,
  12545→12545 bytes) — logo **ambas estavam em KL**. Logs pymetis de E1/#211
  (`he2009_facebook_baseline_pymetis`, 12 runs) confirmados — **sem reabrir
  experimentos**. **(1)** As duas figuras regeneradas em pymetis, cada uma no seu
  estilo (canônica PT/cor via `comparison.py`; `eng-` EN/B&W via
  `scripts/article_figures.py`); `eng-privacy_utility.pdf` (já pymetis) não
  tocado. Conferidas contra o §4.5 (FB k=2 rr_subgrafo 0,1454; `bound_fraction`
  do FB toda < 1; subgrafo não-monótono). **(2)** O mesmo asset ancorava o
  `results_enron.md` (#128), de narrativa **KL** (tabela + prosa + seção C2 do
  motor não-pareado). Por decisão do autor (consolidação, mesmos motores), o
  gerador `experiments/make_enron_table.py` passou a ler os logs pymetis e o doc
  foi regenerado. **Inversões registradas com fidelidade:** gap FB×Enron k=2
  ~6×→~1,2×; FB deixa de violar a cota 1/k (só Enron cruza, k=20); FB
  `FAILURE_LOW_COVERAGE` em k∈{10,20} (marco 29/05 segue ancorado no run KL);
  "subgrafo ≫ grau"/monotonicidade limpos só no Enron; **seção C2 → RESOLVIDA**.
  **(3) Consolidação de motor no relatório técnico (mandato dos avaliadores).**
  Os avaliadores apontaram a incongruência KL×pymetis; a consolidação num motor
  único (pymetis) foi tratada como **mandatória**, mesmo enfraquecendo o marco.
  Como o artigo é derivado do relatório, o relatório técnico
  (`academic/relatorio_tecnico.md`) foi migrado para pymetis —
  §5.1/§5.2/§5.5/§5.6/§6.2/Apêndice A.1, ameaça C2 → resolvida — espelhando
  `results_baseline.md` (E1): **marco 29/05 certificado sobre o run KL**
  (histórico, não retificado), run KL arquivado; sob pymetis o FB só atinge
  cobertura plena em k=2/5 — achado parcialmente enfraquecido, trade-off aceito.
  Artigo já estava em pymetis (D4) e segue consistente; nota de pendência do
  §4.5 marcada resolvida. Reflexo público: §Revisão D8 de
  `artigo_rastreabilidade.md` e `relatorio_rastreabilidade.md`; `limitations.md`
  (C2 + trabalho futuro resolvidos); pendência do identificador Brito (2026)
  também resolvida (Zenodo DOI). PR docs-only com **nota de degelo** (figuras +
  docs/relatórios + gerador de tabela; código de produção congelado intacto).
  648 testes passam; ruff limpo.
- **Preparação para citação Zenodo+GitHub do software (Brito 2026) — D7,
  2026-06-27. ✅ (raiz + docs).** Ajustes possíveis **antes** do passo Zenodo,
  para o snapshot arquivado nascer auto-consistente. **(1) URL canônica
  decidida:** o repositório citado é `chrisjulio/moduloreidentificacao` (o nome
  `reidentificacao`, antes cogitado, foi **descartado**) — corrigida a ref
  Brito (2026) em `academic/artigo.md` e a nota em
  `docs/artigo_rastreabilidade.md` (item 8). **(2) Metadados de citação:**
  criados `CITATION.cff` (widget "Cite this repository" + export BibTeX) e
  `.zenodo.json` (autor, título, licença MIT, keywords), ambos com o **concept
  DOI** como única pendência (slot comentado/marcado). **(3) Papéis das pastas**
  publicados na §7 do README (`/publications/` inserido; `/references/`
  reescrito como bibliografia **citada**) + nota das "duas prateleiras
  bibliográficas". **Modelo de atualização registrado:** a versão estática do
  Zenodo é imutável, mas o **concept DOI** (o que se cita no paper) sempre
  resolve para a versão mais recente — qualquer esquecimento pós-arquivamento se
  resolve com um **novo release**, não com retrabalho do estático; metadados
  (autor/título/descrição) são editáveis no Zenodo sem nova versão. **Pendência
  única, a cargo do autor:** ligar Zenodo↔GitHub, publicar release, reservar o
  concept DOI e preencher o slot em `CITATION.cff` + ref Brito (2026).
- **Rodada D7 (sem issue) — aderência ML/GNN: Wang et al. (2023) citado
  (2026-06-27). ✅ (docs + academic).** Aplicado o ponto **B** da orientação
  A/B/C do autor: inserção da referência de de-anonimização baseada em
  aprendizado de máquina (o "paper GNN"). Entre os candidatos avaliados (Wang
  2023, IEEE TDSC; Yuan 2024, KDD; Liu 2025, ICDE), **só Wang 2023** foi
  citado — *anchor link prediction* via *graph embedding* + aprendizado
  adversarial federado, o adversário aprendido que reassocia nós por
  similaridade tolerando o ruído da anonimização. **B1** (§1 artigo / §1.1
  relatório): enquadramento da lacuna estendido (ML ao lado da DP). **B2**
  (§2 artigo, após Narayanan / §1.3 relatório): parágrafo do adversário
  aprendido **estritamente mais forte** que grau+subgrafo → reforça **cota
  inferior** (§5.2/§6.1). **Referência canônica:** `README.md` §12 **20 →
  21** (Wang **[18]**; Wörlein→[19], Yuan→[20], Zhou→[21]); lista do artigo
  18 → 19; catálogo `references/README.md` linha + BibTeX
  (`Wang2023AnchorLink`). **Apêndice B do relatório reconciliado à §12** na
  mesma rodada: de 14 entradas + 2 adendos ([15] Narayanan 2009, [16] Wang)
  para a lista alfabética completa de **21** — incorpora também as 5 refs de
  D2/D3 que estavam citadas na §2.1 mas ausentes do apêndice. Também
  normalizada a nomenclatura dos 3 PDFs novos em `references/` (Yuan 2024,
  Liu 2025, Wang 2023) e a regra de nomenclatura+inserção embutida no
  `references/README.md` (versionado). PDFs **não commitados** (gitignored).
  Sem alteração de números, tabelas, figuras ou código. Portabilidade às
  versões Overleaf a cargo do autor.
- **Rodada D6 (#221) — revisão integrada final do artigo (2026-06-26). ✅
  (docs, PR #232 `docs/artigo-revisao-final`).** Bloqueios D1–D5 (#216–#220)
  verificados **MERGED** via `gh`; nenhum PR aberto. Passagem final de
  consistência sobre `academic/artigo.md` (privado, gitignored) com reflexo
  público na rastreabilidade. **(1) Números** reconferidos contra os
  relatórios versionados — Tabela 2 (`results_baseline.md` pymetis), Tabela 3
  (`results_enron.md`), Tabela 4/tese central (k=2: 6,3×/37,6× → ~6×/~38×),
  §4.6 d-sweep Enron (`results_enron_dsweep.md`: EGS 19,99/198,21, cobertura
  ≥ 0,9877) e Facebook (`results_dsweep.md`: EGS 19,70/133,0, cobertura mínima
  0,752): **nenhuma divergência**; mantida a divergência **intencional** da
  §4.6 vs. prosa de `results_enron_dsweep.md` §4.1 (o artigo segue o dado: só
  a metade estrutural replica). **(2) Coerência pós-D5** (pendência herdada de
  D5): §3.5 — d-sweep agora "sobre os dois datasets"; §5.1 ¶1 — removida "no
  Enron, apenas d=1 foi medido" (resta 1 resíduo: múltiplas ego-redes); §6 ¶2
  — replicação do d-sweep no 2º dataset sai dos futuros (feita em D5), futuros
  renumerados (i)–(iv). **(3) Terminologia** uniforme (baseline D1; DP vs.
  anonimização estrutural D2; cota inferior). **(4) Referências — achado
  central:** as 5 refs de D2/D3 (Brito & Machado 2024; Hao 2024; Mendonça
  2023; Mueller 2022; Yuan 2023) estavam **citadas na §2 mas ausentes da
  lista** do artigo (fechara em 12 na W2f); adicionadas em ordem alfabética
  (metadados conferidos contra README §12) → lista do artigo **18 entradas**;
  citação↔lista fechada nos dois sentidos; 3 omissões intencionais (Wörlein,
  Díaz, Serjantov) permanecem. PR **docs-only**; código/assets congelados
  intactos. **Pendências herdadas, não resolvidas (autor):** regen do asset
  `comparison_fb_enron` para pymetis (follow-up D4); identificador estável da
  ref Brito (2026).
- **Rodada D5 (#220) — §4.6 do artigo expandida com o d-sweep Enron
  (2026-06-26). ✅ (docs, PR `docs/artigo-revisao-dsweep-enron`).**
  Desbloqueada por E3 (#213), V1 (#214) e V2 (#215) — todas CLOSED,
  verificadas via `gh`; nenhum PR aberto. A §4.6 (que cobria só o Facebook)
  foi estendida no texto privado (`academic/artigo.md`, gitignored) com o
  d-sweep do Enron, respondendo à **questão de pesquisa central**: o
  deslocamento do vetor de ataque com `d` crescente se replica numa rede ~63×
  maior? **Resposta parcial, registrada com fidelidade ao dado** (divergindo
  da prosa de `results_enron_dsweep.md` §4.1, que afirma que "se confirma"):
  só a **metade estrutural** se replica. (i) EGS ≈ k·d vale quase exatamente
  no Enron (k=20/d=10 → 198,21 vs 133,0 no FB), sem `FAILURE_LOW_COVERAGE` na
  grade; (ii) o ataque por subgrafo enfraquece monotonicamente com d em todo k
  (k=2: 0,124→0,053; k=20: 0,057→0,017), ao custo de utilidade (KS-D até
  0,304); (iii) **o ataque por grau não se fortalece** — colado ao piso
  (~0,002–0,003) em toda a grade —, logo **não há cruzamento** e o subgrafo
  permanece dominante nas 16 células: o deslocamento é **dependente de
  escala**. **Figura 5** inserida (V2/#215, `docs/assets/enron_dsweep_series`)
  e `docs/results_enron_dsweep.md` (V1/#214) referenciada. Reflexo público:
  seção D5 + linha da matriz em `docs/artigo_rastreabilidade.md`. PR docs-only
  (assets e código congelados intactos). **Coerência pendente p/ D6 (#221):**
  §5.1 ("Enron só d=1") e §6 (d-sweep Enron como futuro) ficaram superadas —
  reconciliação na revisão integrada final.
- **Rodada D4 (#219) — revisão metodológica do artigo (2026-06-26). ✅ (docs,
  PR `docs/artigo-revisao-metodologia`).** Resposta a três limitações
  percebidas pelos avaliadores (orientador/coorientador), com **recontextualização
  metodológica**. **Diferente de D1–D3, altera números e tabelas:** incorpora
  o dado canônico inter-dataset de E1 (#211, D-19) — o run **pymetis** do
  baseline Facebook substitui o **Kernighan-Lin**. **No texto privado
  (`academic/artigo.md`, gitignored):** (i) Tabela 2 + propagação total
  (abstract, §1, §4.2, §4.4/Tabela 4, §6, tese central) KL → pymetis — **gap
  Facebook k=2 cai de ~30× para ~6×** (0,1454 vs 0,0232); headline passa a
  "~6× Facebook / ~38× Enron" (Enron inalterado, já era pymetis); (ii) **motor
  unificado pymetis** nos dois datasets como decisão metodológica (§3.2, §4.1,
  §5.1) — confundidor "motor não-pareado KL×METIS" eliminado (§4.5: 3 → 2
  confundidores); (iii) He et al. (2009)/algoritmo único reenquadrados como
  **baseline canônico deliberado** (§3.2, §5.1); (iv) escala do Enron ~63×
  explícita (§3.5, §4.3). **Consequências narrativas registradas com
  fidelidade:** sob pymetis o Facebook **não** atinge k-anonimato em k=10/20
  (FAILURE_LOW_COVERAGE, cob. 0,8647; marco 29/05 permanece válido sobre o run
  KL); punch "quatro em cada cinco" vira leitura de gap; Facebook não viola
  mais a cota 1/k (sobrevive só em Enron/k=20); taxa por subgrafo do FB deixa
  de ser estritamente monótona. **Figura 4 (painel `comparison_fb_enron`):**
  prosa atualizada para pymetis, **regeneração do asset = follow-up sinalizado**
  (PR docs-only, sem tocar assets nem código congelado). **Reflexo público:**
  seção D4 + sumário/matriz em `docs/artigo_rastreabilidade.md`. Escopo limitado
  a este repo (local + GitHub); portabilidade às versões Overleaf a cargo do
  autor.
- **Rodada D1–D3 (#216, #217, #218) — revisão pós-entrega do conteúdo
  acadêmico (2026-06-26). ✅ (docs, PRs #227/#229).** Revisão orientada pelo
  retorno dos avaliadores externos (orientador e coorientador), no texto
  privado (`academic/`, gitignored — Overleaf captura daqui) com reflexos
  públicos. **D1 (#216):** abstract + §1 do artigo e §1.1 do relatório
  reposicionam o trabalho como **baseline de avaliação de risco** para
  k-anonimato estrutural, com lacuna metodológica (vs. Privacidade Diferencial)
  no 1º parágrafo. **D2 (#217):** §2/§2.1 ganham parágrafo diferenciando DP
  (consultas/estatísticas agregadas; *query release*; garantia semântica/ε) de
  anonimização estrutural (publicação do grafo completo p/ *graph mining*;
  garantia sintática) — tom de diferença de premissas. **D3 (#218):**
  atualização bibliográfica > 2020 — 3 refs recentes verificadas (DBLP/arXiv)
  citadas no §2: Hao et al. (2024, MLDA k-degree multinível — **> 2023**),
  Yuan et al. (2023, PrivGraph — *graph release* sob DP, USENIX Sec) e Mueller
  et al. (2022, SoK — taxonomia DP em grafos). **Reflexo público:** `README.md`
  §12 de **15 → 20** entradas (D2 +Mendonça/Brito; D3 +Hao/Mueller/Yuan;
  renumerada — Narayanan 2009 [9]→[13]); catálogo `references/README.md` +
  BibTeX (PDFs locais do autor, gitignored, **não commitados**);
  `docs/{artigo,relatorio}_rastreabilidade.md` com seção D1–D3. **Material DP
  retido:** catálogo `references/DP_GRAPH_REFERENCES.md` **destrackeado** (PR
  #227, local-only) e de Jong et al. (2024) fora do registro — pendentes de
  deliberação com os orientadores. **Incidente de PR empilhado:** a #228
  (incorporação D2) foi mergeada na base intermediária e **não chegou a
  `main`** (padrão #192/#193); re-roteada por cherry-pick → **PR #229** (base
  `main`). PR #229 leva D2+D3 + coerência.
- **Issue #211 (E1) — reexecução baseline Facebook com pymetis (2026-06-25).
  ✅ (experiment, PR #225 aberto).** Config
  `he2009_facebook_baseline_pymetis.yml` criado com `allow_kl_fallback: false`.
  12 runs concluídas: pymetis 12/12, sem crashes; k=2/5 SUCCESS_PARTIAL, k=10/20
  FAILURE_LOW_COVERAGE (cobertura 86,5%). **Achado:** motor afeta resultados mesmo
  em d=1 — rr_subgrafo k=2 cai de 0.7914 (KL) para 0.1454 (pymetis); gap ~6×
  (era ~30× KL). `docs/results_baseline.md` atualizado com tabelas pymetis e seção
  histórica KL; D-19 adicionado ao `decision_log.md`;
  `docs/assets/eng-privacy_utility.pdf` regenerado. 648 testes passando; ruff limpo.
- **Issue #215 (V2) — figuras Enron d-sweep em `docs/assets/` (2026-06-25).
  ✅ (viz, PR #224 MERGED).** Geração dos 4 assets canônicos do d-sweep Enron:
  `enron_dsweep_series.{pdf,png}` (layout `series`, cor por d) e
  `enron_dsweep_facets.{pdf,png}` (layout `facets`, grade 2×d). Convenção
  canônica: `plot_privacy_utility_dsweep` com defaults (`pt`, sem modificadores
  de artigo). Dados: 48 registros, combinando `he2009_enron_secondary` (d=1,
  âncora) + `he2009_enron_dsweep` (d∈{2,5,10}) via nova função
  `load_jsonl_records_combined(logs_dirs)` e flag CLI `--anchor-logs DIR`
  adicionadas a `src/visualization/privacy_utility.py`. Testes: 11 novos
  (`TestLoadJsonlRecordsCombined` 5 + `TestEnronDSweepPlot` 5 +
  `TestMain.test_main_anchor_logs_combined_with_dsweep_dir` 1); total 80
  testes passando; ruff limpo.
- **Issue #214 (V1) — tabela de resultados Enron d-sweep (2026-06-25).
  ✅ (experiments, PR #223 MERGED).** Script
  `experiments/make_enron_dsweep_table.py` criado: parseia
  `he2009_enron_dsweep.jsonl` (d∈{2,5,10}) e mescla opcionalmente
  `he2009_enron_secondary.jsonl` como âncora d=1; gera
  `docs/results_enron_dsweep.md` com 48 runs agregados (média±dp por célula
  (k,d), grid de cobertura, tabela bruta, análise de tendências). 16 testes
  em `tests/experiments/test_make_enron_dsweep_table.py`; ruff limpo.
- **Figuras do artigo (KDMiLe) regeneradas com tipografia/estilo dedicados +
  B&W opt-in (2026-06-21). ✅ (viz, branch `viz/article-figures-typography`).**
  A pedido do autor, regeração das duas figuras do artigo LaTeX (classe
  KDMiLe, duas colunas A4; `\textwidth` = 6.1 in, `\columnwidth` ≈ 2.98 in;
  corpo das figuras a 8 pt na página final). **Sem dados novos** — fontes
  congeladas: Figura 4.1 dos logs `he2009_facebook_baseline` (via
  `aggregate_by_k`); Figura 4.3 do CSV congelado `comparison_fb_enron.csv`
  (colunas `bound_fraction`/`relative_decay`). Implementado como script
  dedicado `scripts/article_figures.py` que **reaproveita a camada de dados**
  dos geradores canônicos sem alterá-los (preserva figuras PT/EN canônicas e
  seus testes). Tipografia do artigo: fonte-base compensando o reescalonamento
  do LaTeX (≈19 pt fig 4.1 / ≈16 pt fig 4.3), linhas finas (~0.6 pt na página),
  sem suptitle/títulos de painel, rótulos `(a)`/`(b)`, uma legenda por figura,
  eixo x de k em **escala log** com ticks explícitos {2,5,10,20}, export PDF
  vetorial (`bbox_inches=tight`, `pad_inches=0.01`, `pdf.fonttype=42`).
  **Cor é o default; preto-e-branco (séries diferenciadas por padrão de linha
  + marcador) é opt-in via `--bw`** — espelha o padrão opt-in do repo. **Ambas
  as figuras** são lado a lado 1×2, dimensionadas para `\textwidth` (inclusão
  via `figure*`): Figura 4.1 — (a) privacy / (b) utility, com barras de erro
  ±1 dp; Figura 4.3 — (a) `bound_fraction` com linha de referência pontilhada
  em 1.0 / (b) `relative_decay`. A Figura 4.1 começou a sessão empilhada 2×1
  7×8, mas o autor pediu lado a lado por estourar o orçamento de páginas
  (altura ~8 in) — decisão final: lado a lado, encerrando de vez a variante
  side-by-side compacta de 2026-06-18 e a tentativa empilhada. **Calibração de
  proporção (último ajuste):** a 4.1 saía com largura nativa 13.7 in (legenda
  de 4 colunas em linha única transbordava o canvas e inflava o `bbox tight`),
  contra 11.55 in da 4.3 — downscale maior em `\textwidth` deixava sua fonte
  ~16% menor. Corrigido: `figsize=(12.0, 5.19)`, legenda em **2 colunas/2
  linhas** (cabe no canvas), e rótulos `(a)`/`(b)` movidos para título à
  esquerda (fora da área de plotagem, sem colidir com dados). Resultado: largura
  nativa **11.554 in idêntica** à 4.3 (alturas 4.963 vs 4.969) → tipografia
  idêntica nas duas em `\textwidth`. Fonte-base 16 pt e linewidth 1.2 iguais nas
  duas.
  PDFs gerados em `--bw` (o artigo declara expressamente "sem cores"):
  `docs/assets/eng-privacy_utility.pdf` e `eng-comparison_fb_enron.pdf`. Nomes
  canônicos confirmados com o autor para uso espelhado no Overleaf
  (`eng-privacy_utility.pdf`, `eng-comparison_fb_enron.pdf`). 621 testes passam;
  ruff limpo. **Nota de degelo:** novo script utilitário em `scripts/` durante o
  congelamento — só regeneração de figuras a partir de dados congelados, sem
  reabrir experimentos.
- **Layout side-by-side opt-in para a figura `privacy_utility` (2026-06-18).
  ✅ (viz, PR #207 aberto).** Manutenção de figuras a pedido do autor: a
  figura baseline "Privacy vs. Utility — He et al. (2009)" era empilhada
  (2×1, 7×8 in retrato) e sua altura de ~8 in estourava o orçamento de
  páginas do artigo coluna-única (KDMiLe, `\textwidth` = 6.1 in). Adicionado
  um layout **`side-by-side`** (1×2, `figsize=(6.1, 2.7)` = `\textwidth` em
  escala ≈1:1, fontes reduzidas) como variante **opt-in**, espelhando o
  padrão do `--lang`: o layout `stacked` canônico permanece o **default**
  (saída PT em `results/plots` inalterada), o compacto é pedido
  explicitamente. `plot_privacy_utility` ganhou os parâmetros `layout`
  (`{stacked, side-by-side}`, validado) e `show_suptitle` (default `True`;
  suprime o suptitle na inclusão LaTeX, onde a `\caption` nomeia a figura);
  CLI com flags `--side-by-side` e `--no-suptitle` (baseline apenas). Figuras
  do artigo regeneradas em side-by-side sem suptitle dos logs congelados
  (sem reprocessamento experimental): `docs/assets/eng-privacy_utility.{pdf,png}`
  (Facebook) e `eng-privacy_utility_enron.{pdf,png}` (Enron) — ambas usam
  `plot_privacy_utility`. PDF resultante ~5,97×2,58 in → a `width=\textwidth`
  escala ~1,02 (≈1:1), altura final ~2,64 in (era ~8 in). Plots d-sweep
  (`series`/`facets`) intactos. +4 testes (geometria de cada layout via
  captura de `figsize`, layout inválido, caminho no-suptitle); 137 testes de
  visualização passam; ruff limpo. Branch `viz/privacy-utility-side-by-side`.
  **Nota de degelo:** alteração em `src/` durante o congelamento de código da
  S10-W, autorizada pelo autor como manutenção de figuras para o artigo (não
  reabre experimentos — só geometria de plot e regeneração dos PDFs).
- **Rodada pós-W2f de correções do artigo (2026-06-11). ✅ (docs, PR a
  abrir).** Aplicação das decisões consolidadas do autor sobre a versão
  compilada de 11/06 e o fonte privado: (i) claim de disponibilidade da
  §3.5 reescrito (opção B — "relatórios consolidados gerados dos logs"
  como artefato público; logs brutos regeneráveis); (ii) referência Brito
  2026 com descrição "relatórios dos experimentos"; (iii) terminologia —
  corpo adota **ataque por grau / ataque por subgrafo** com ponte de
  nomenclatura na §3.3, âncoras preservadas; (iv) setas padronizadas em
  `->`; (v) ano 2003 harmonizado nos docs internos (relatório §5.7,
  `metrics_definitions.md`, `algorithm_notes.md`; errata no D-17); (vi)
  folha de rosto sem placeholders e legenda da Figura 3.1 limpa (versão
  compilada); (vii) Figura 4.3 vetorial no compilado usando o PDF do
  snapshot (PR #200). Registro completo na seção "Rodada pós-W2f" de
  `artigo_rastreabilidade.md`. **Pendência aberta:** identificador estável
  (tag/release ou DOI) da referência Brito 2026 — o PR #199 tratou do D-18
  (sigma), não do identificador; repositório sem tags/releases e endereço
  público `chrisjulio/reidentificacao` ainda inativo (decisão do autor).
- **PDF do painel comparativo FB×Enron adicionado ao snapshot versionado. ✅
  (docs, PR a abrir).** A pedido do autor: o snapshot em `docs/assets/`
  (exceção DL-04 ao gitignore de `results/`) passou a incluir
  `comparison_fb_enron.pdf` além do `.png` e `.csv`, em paridade com os demais
  gráficos (`results/plots/` sempre gera PNG+PDF). PDF regenerado dos logs
  congelados via `--pdf` do gerador (CSV e PNG resultantes byte-idênticos aos
  versionados — logs intactos). Comando de regeneração em `results_enron.md`
  (via `make_enron_table.py`) atualizado com `--pdf`; menções `{png,csv}`
  atualizadas em README e `relatorio_rastreabilidade.md`. Sem reprocessamento
  experimental. Ver entrada de sessão 2026-06-11 no Histórico.
- **D-18 — registro retroativo da escolha `sigma = 0.5`. ✅ (docs, PR a
  abrir).** Auditoria da origem do default `sigma=0.5` do FSM (fixado no
  commit `90dd035`/issue #14 sem critério registrado) e nova entrada D-18 no
  `decision_log.md`: escolha de implementação sem ancoragem registrada na
  literatura; não afeta a garantia de k-anonimato; sensibilidade não medida.
  Pendência do autor: verificar o σ experimental de He et al. (2009) antes
  de citá-lo. Ver entrada de sessão 2026-06-11 no Histórico.

**Próximo passo planejado:**
- **Merge do PR da atualização documental pós-S10-W** (README + CLAUDE.md +
  progress.md + saneamento de terminologia) — revisão humana; Claude Code
  não faz merge. Escopo do saneamento validado pelo autor (2026-06-10):
  somente arquivos produzidos (locais e versionados); issues fechadas e
  estruturas de processo/controle ficam como estão.
- **Fora do escopo da #175 (pendências anotadas na revisão W2f):**
  conversão final do artigo via pandoc (inserção física das figuras
  regeneráveis; remoção dos checklists de processo W2b..e; venue/template
  a decidir) — a cargo do autor. As 3 referências omitidas (Wörlein; Díaz;
  Serjantov & Danezis) são revisáveis pelo autor na conversão.
- **Fora do escopo da #174 (pendências anotadas na revisão W1f):**
  conversão final do relatório via pandoc (inserção física das figuras
  regeneráveis; remoção dos checklists de processo W1b..e) — a cargo do
  autor; versionamento de `scripts/verify_reproduction.py` (resíduo
  documental da #172) — exigiria degelo de código, decisão humana.
- **Issue #148 (entropia não uniforme, sem milestone):** congelada; exige decisão
  D-xx (esquema de pesos) antes de implementar — não iniciar sem o humano.
  Código congelado na fase S10-W.

**Bloqueios ativos:**
- **PR #207 aberto** (`viz/privacy-utility-side-by-side`, 2026-06-18) —
  layout side-by-side opt-in da figura `privacy_utility`; aguarda revisão
  humana e merge (Claude Code não faz merge). CI (ruff + pytest) deve rodar
  automaticamente. Não bloqueia outras frentes.
- PR **#197** (W2f, `Closes #175`) **MERGED** em 2026-06-10
  (`22:53Z`); **#175 CLOSED** — desdobramento S10-W2a..f integralmente em
  `main`; nenhum PR de produção acadêmica aberto (verificado via `gh` em
  2026-06-10).
- PR **#196** (W2e) **MERGED** em 2026-06-10 (`22:17:13Z`) — Seções 5–6 +
  abstract final e rastreabilidade em `main`; bloqueio anterior da W2f
  resolvido.
- PR **#195** (W2d) **MERGED** em 2026-06-10 (`21:19:59Z`) — Seção 4 do
  artigo e rastreabilidade em `main`; bloqueio anterior da W2e resolvido.
- PR **#194** (W2c) **MERGED** em 2026-06-10 (`21:06:57Z`) — Seção 3 do
  artigo e rastreabilidade em `main`; bloqueio anterior da W2d resolvido.
- PR **#193** (reencaminhamento da decisão A+B) **MERGED** em 2026-06-10
  (`20:45:22Z`) — incidente de roteamento do #192 **encerrado**: conteúdo
  da decisão A+B em `main`.
- PR **#191** (W2b) **MERGED** em 2026-06-10 — Seções 1–2 do artigo e
  rastreabilidade em `main`.
- PR **#190** (registro da validação) **MERGED** em 2026-06-10 — bloqueio
  anterior da W2b resolvido.
- PR **#188** (W2a) **MERGED** em 2026-06-10 e **desdobramento S10-W2a..f
  validado pelo autor** na #175 (2026-06-10; sem sub-issues, agrupamento
  como proposto, sem venue/template por ora) — bloqueios anteriores da W2b
  resolvidos.
- Relatório (#174) **fechado** em 2026-06-10: PRs #181–#183, #185–#187
  (W1a..f) todos **MERGED** — bloqueios anteriores resolvidos.
- **Sub-issues S10-W1a..f: dispensadas** (decisão do autor, 2026-06-09) —
  rastreio oficial por comentário na #174 + `docs/relatorio_execucoes.md` +
  matriz em `docs/relatorio_rastreabilidade.md`.
- #176 (infraestrutura `academic/`) e #179 (DL-06) **MERGED** em 2026-06-09 —
  bloqueios anteriores resolvidos.
- #30 (PR #149) e a auditoria bibliográfica (PR #150) mergeadas em `main`;
  #30 fechada (`COMPLETED`). A entropia (baseline uniforme) está em `main`.
- Ciclo S9 totalmente encerrado (#122–#129, #139 em `main`; #29 fechada; milestone
  S9 `closed`). Milestones S8 e S9 concluídos.

**Decisões pendentes de validação humana:**
- **Achado W2b "Narayanan & Shmatikov 2009 × 2008": RESOLVIDO** — autor
  decidiu **A+B** (2026-06-10) e a execução está no PR empilhado
  `docs/references-narayanan-2009` (ver "Último passo concluído" e
  `artigo_execucoes.md`). Sem pendência restante.
- D-08 (conectividade de LSs): decisão Opção B registrada. O d-sweep **manteve**
  d=2 (anotado como potencialmente degenerate, precedente D-10) em vez de excluir;
  confirmar se essa escolha é a definitiva.

---

## Como atualizar este arquivo

Ao final de cada sessão produtiva, atualize a seção "Estado atual" acima e
adicione uma entrada no Histórico abaixo seguindo o modelo:

```markdown
### AAAA-MM-DD — Título breve da sessão

- **Concluído:** o que foi feito.
- **Próximo:** próximo passo imediato.
- **Bloqueios:** bloqueios que impedem progresso (ou "Nenhum").
- **Decisões pendentes:** pontos que precisam de validação humana (ou "Nenhuma").
```

---

## Histórico de sessões

### 2026-06-27 — D8: painel comparativo em pymetis + migração do results_enron.md

- **Concluído:** Fechado o follow-up de D4/D6 (asset `comparison_fb_enron` em KL
  contra prosa pymetis do §4.5). Diagnóstico via git confirmou que **ambas** as
  figuras comparativas estavam em KL (a `eng-` deriva do CSV canônico; a
  re-gravação de E1 fora no-op). As duas regeneradas em pymetis a partir dos logs
  **já existentes** de E1/#211 — sem reabrir experimentos —, cada uma no seu
  estilo (canônica PT/cor; `eng-` EN/B&W). Como o mesmo asset ancorava o
  `results_enron.md` (#128, narrativa KL com seção C2 do motor não-pareado), o
  autor decidiu **consolidar**: `make_enron_table.py` migrado para os logs pymetis
  e o doc regenerado. Inversões narrativas registradas com fidelidade (gap k=2
  ~6×→~1,2×; FB deixa de violar a cota 1/k; FB `FAILURE_LOW_COVERAGE` em
  k∈{10,20}; dominância subgrafo/monotonicidade limpas só no Enron; C2
  → RESOLVIDA). **Consolidação de motor no relatório (mandato dos avaliadores):**
  apontada por eles a incongruência KL×pymetis, a consolidação em motor único
  (pymetis) foi tratada como mandatória; o relatório técnico
  (`academic/relatorio_tecnico.md`) foi migrado para pymetis
  (§5.1/§5.2/§5.5/§5.6/§6.2/Apêndice A.1; C2 resolvida), com o marco 29/05 retido
  como registro histórico no run KL (achado parcialmente enfraquecido — trade-off
  aceito). Artigo já em pymetis (D4), consistente. Reflexo público: §Revisão D8
  de `artigo_rastreabilidade.md` e `relatorio_rastreabilidade.md`;
  `limitations.md` (C2 + trabalho futuro resolvidos); pendência do identificador
  Brito (2026) marcada resolvida (Zenodo DOI). Checklist privado
  `academic/propagacao.md` atualizado.
  648 testes passam; ruff limpo. Branch `viz/comparison-fb-enron-pymetis`.
- **Próximo:** revisão humana + merge do PR docs-only (Claude não faz merge);
  propagar as duas figuras pymetis e o `results_enron.md` consolidado às versões
  Overleaf PT/EN (a cargo do autor).
- **Bloqueios:** Nenhum novo (PR a abrir; PR #207 segue aguardando merge humano).
- **Decisões pendentes:** Nenhuma nova.

### 2026-06-18 — Layout side-by-side opt-in para a figura privacy_utility

- **Concluído:** A pedido do autor (manutenção de figuras para o artigo
  LaTeX/Overleaf), a figura baseline "Privacy vs. Utility — He et al. (2009)"
  ganhou um layout **`side-by-side`** opt-in para não estourar o orçamento de
  páginas do artigo coluna-única (KDMiLe, `\textwidth` = 6.1 in): a versão
  empilhada (2×1, 7×8 in) tinha ~8 in de altura. `plot_privacy_utility` agora
  aceita `layout` (`{stacked, side-by-side}`, default `stacked` canônico,
  validado) e `show_suptitle` (default `True`); CLI com `--side-by-side` e
  `--no-suptitle` (baseline apenas), espelhando o padrão opt-in do `--lang`.
  Figuras do artigo regeneradas em side-by-side sem suptitle dos logs
  congelados (sem reprocessamento): `docs/assets/eng-privacy_utility.{pdf,png}`
  (Facebook) e `eng-privacy_utility_enron.{pdf,png}` (Enron). PDF ~5,97×2,58 in
  → a `width=\textwidth` escala ~1,02 (≈1:1), altura final ~2,64 in. Default PT
  (`results/plots`) e plots d-sweep intactos. +4 testes; 137 testes de
  visualização passam; ruff limpo. Branch `viz/privacy-utility-side-by-side`,
  PR #207. Degelo de código pontual autorizado pelo autor (geometria de plot +
  regeneração de PDFs; não reabre experimentos).
- **Próximo:** merge humano do PR #207 (após CI verde); validar os PDFs no
  Overleaf e medir o ganho de páginas.
- **Bloqueios:** PR #207 aguardando revisão/merge humano. Nenhum outro.
- **Decisões pendentes:** Nenhuma para esta frente.

### 2026-06-11 — Rodada pós-W2f: correções do artigo decididas pelo autor

- **Concluído:** Aplicadas as 11 decisões consolidadas do autor
  (orientação de 2026-06-11) sobre o artigo — fonte privado
  (`academic/artigo.md`), versão compilada (projeto LaTeX/Overleaf) e docs
  internos. No texto: claim de logs da §3.5 reescrito (opção B), referência
  Brito 2026 com "relatórios dos experimentos", ponte de nomenclatura na
  §3.3 + substituição "cenário por X" → "ataque por X" (§3.3, §4.2, §4.3,
  §4.5 incl. legenda da Figura 4.3, §5.3; âncoras intactas), setas `→`
  padronizadas em `->` (§4.5, §4.6 — demais seções já conformes), folha de
  rosto sem placeholders (titulações Prof. Dr. confirmadas) e legenda da
  Figura 3.1 sem rastro de conversão. Figura 4.3 passou a vetorial no
  compilado, reutilizando `docs/assets/comparison_fb_enron.pdf` (PR #200 —
  sem regeneração nova, sem mudança de código). Docs internos: ano 2003
  (PET 2002/LNCS 2482) harmonizado em `metrics_definitions.md`,
  `algorithm_notes.md` e relatório técnico §5.7; errata na D-17;
  nota Díaz/Serjantov da matriz atualizada (superada pela inclusão na
  compilação de 11/06 — Wörlein 2005 única omissão intencional); seção
  "Rodada pós-W2f" criada em `artigo_rastreabilidade.md` (itens i–v +
  origem nominal `moduloreidentificacao` × `reidentificacao`). Itens 4 e 6
  da orientação: sem ação, por decisão do autor. Números/resultados
  intocados; código congelado respeitado.
- **Próximo:** Merge do PR desta rodada; criação do identificador estável
  (tag/release ou DOI) e preenchimento do campo de versão na referência
  Brito 2026; ativação do endereço público `chrisjulio/reidentificacao`.
- **Bloqueios:** Nenhum (PRs #199 e #200 MERGED em 2026-06-11).
- **Decisões pendentes:** Identificador estável da autorreferência (o
  PR #199 mergeado tratou do D-18/sigma — o identificador segue
  inexistente); momento de publicação/renomeação do repositório público.

### 2026-06-11 — PDF do painel comparativo FB×Enron no snapshot versionado

- **Concluído:** A pedido do autor, o snapshot versionado do painel
  comparativo normalizado (DL-04, `docs/assets/`) ganhou a versão **PDF**
  (`comparison_fb_enron.pdf`), em paridade com os demais gráficos do
  pipeline, que sempre produzem PNG+PDF em `results/plots/`. O PDF foi
  regenerado dos logs congelados (`he2009_facebook_baseline` +
  `he2009_enron_secondary`) com o flag `--pdf` já existente em
  `src/visualization/comparison.py` (nenhuma mudança de código de
  visualização); sanidade: o CSV e o PNG regenerados na mesma execução
  saíram **byte-idênticos** aos versionados, confirmando logs intactos e
  render determinístico. Atualizações documentais: comando de regeneração
  nº 5 e nota de exceção em `results_enron.md` (editados na fonte,
  `experiments/make_enron_table.py`, e doc regenerado), menções
  `comparison_fb_enron.{png,csv}` → `{png,pdf,csv}` no README (2 pontos) e
  ponteiro `.pdf` na tabela de artefatos de `relatorio_rastreabilidade.md`.
  DL-04 e entradas históricas não retro-editadas. Sem reprocessamento
  experimental — congelamento respeitado. `ruff check`/`format` limpos.
  Branch `docs/comparison-pdf-asset`.
- **Próximo:** Merge do PR. Contexto registrado: a localização em
  `docs/assets/` (e não `results/plots/`) é a exceção documentada DL-04 —
  `results/` é gitignored e o painel precisa ser versionado por ser
  referenciado como figura nos textos acadêmicos e auditável publicamente.
- **Bloqueios:** PR de D-18 e PR deste passo aguardando CI + revisão humana.
- **Decisões pendentes:** Nenhuma nova.

### 2026-06-11 — D-18: registro retroativo da escolha `sigma = 0.5` (lacuna de rastreabilidade)

- **Concluído:** Auditoria da origem do default `sigma = 0.5` do FSM
  simplificado, a pedido do autor (dúvida sobre amparo na literatura).
  Verificado: o valor foi fixado no commit `90dd035` (2026-05-21, issue
  #14) como "parâmetro interno fixo", com justificativa apenas
  qualitativa no docstring de `anonymize()` ("valor conservador");
  nenhuma entrada de decisão dedicada ao valor existia. O exemplo
  "0.20 para 20%" no docstring de `_group_isomorphic()` entrou via
  commit `a30ad7f` (2026-05-18, issue #33 — docstrings conforme o
  artigo); a atribuição de σ=0,2 a He et al. (2009) permanece **não
  verificada** no repositório. Registrada a entrada **D-18** no
  `docs/decision_log.md` (registro retroativo): escolha de implementação
  sem ancoragem registrada na literatura; baixo impacto metodológico
  (garantia de k-anonimato independe do FSM — D-01 nota G2 / achado A2;
  valor uniforme em todas as execuções — DL-05); sensibilidade a sigma
  não medida (trabalho futuro). Branch `docs/decision-log-d18-sigma`.
- **Próximo:** Merge do PR de D-18. Pendência do autor registrada na
  entrada: conferir o valor de σ usado nos experimentos de He et al.
  (2009) antes de citá-lo nos textos acadêmicos.
- **Bloqueios:** PR de D-18 aguardando CI + revisão humana.
- **Decisões pendentes:** Nenhuma nova (D-08 segue como única pendência
  herdada).


### Sessões anteriores a 2026-06-11 — arquivadas

> O Histórico de **2026-06-10 e anteriores** e os resumos antigos de "Último
> passo concluído" foram migrados para
> [`progress_archive.md`](progress_archive.md) nas repaginações de 2026-06-27
> (regra no cabeçalho deste arquivo). Consulte lá ou via `Grep`.
