# progress.md — Estado de progresso das sessões

> **Instrução ao agente:** Este arquivo deve ser lido no início de cada sessão
> (`leia docs/progress.md e continue de onde paramos`) e atualizado ao final de
> cada sessão produtiva.
>
> Mantenha o histórico de sessões anteriores — não apague entradas passadas.
> Apenas adicione novas entradas no topo da seção "Histórico".

---

## Estado atual

**Data da última atualização:** 2026-06-09

**Semana corrente:** S10 — fase de redação (S10-W): relatório de qualificação
(#174, guarda-chuva) e artigo (#175, dependente). Código **congelado** — somente
análise e documentação.

**Último passo concluído:**
- **Etapa W1a da #174 — esqueleto do relatório + matriz de rastreabilidade
  pública. ✅ (docs, PR aberto).** Primeira etapa do desdobramento S10-W1a..f
  validado na #174 (autor, 2026-06-09). Bloqueios verificados antes de iniciar:
  PRs **#176** e **#179** ambos `MERGED`; nenhum PR aberto. **(1) Esqueleto
  privado:** `academic/relatorio_qualificacao.md` criado (gitignorado, fora do
  diff; backup externo a cargo do autor) — 8 seções da estrutura mínima da
  #174 + apêndices candidatos, cada seção com checklist de conteúdo, fontes
  citáveis (docs/decisões `D-xx`/`DL-xx`), destinos `W-NN` e figuras a
  inserir; regra global de terminologia de aferição no cabeçalho; DL-06 na
  abertura da introdução. **(2) Rastreabilidade pública:**
  `docs/relatorio_rastreabilidade.md` (versionado) — sumário do esqueleto,
  matriz seção → fontes → `W-NN` → figuras → etapa, inventário de
  figuras/tabelas citáveis (versionadas × regeneráveis) e estado por etapa
  (W1a ✅; W1b..f pendentes). **(3) Sub-issues S10-W1a..f não criadas:** a
  criação via `gh` foi bloqueada pelo classifier de permissão (sessão
  executou somente a 1ª etapa, conforme pedido) — formalização das sub-issues
  no GitHub fica a cargo do autor; rastreio das etapas vive na matriz. Só
  docs; código congelado respeitado. Branch `docs/relatorio-skeleton-w1a`
  (`Refs #174`).
- **Complemento manual da #177 — população de `/references/` + catálogo
  completo. ✅ (docs, PR aberto).** A #177 (fechada via PR #178) deixou pendente
  o item manual de download da bibliografia. **(1) Downloads:** 11 das 14
  referências do `README.md` §12 baixadas para `/references/` (gitignored;
  `git status` limpo) a partir de fontes de acesso aberto legítimas — arXiv
  (Narayanan), JMLR (Shervashidze), Springer VoR aberto (Wörlein), páginas de
  autor (Backstrom/Cornell, Leskovec/Stanford, Liu-Terzi/BU, Zhou-Pei/SFU,
  Serjantov-Danezis/UCL, Sweeney/DataPrivacyLab), anonbib (Díaz) e espelho de
  curso (Karypis/UT Austin); todos verificados por magic bytes `%PDF`.
  **(2) Pendências manuais (3):** He 2009 e Cordella 2004 só existem no IEEE
  Xplore (VoR, paywall — exige acesso institucional CAFe/VPN); o AAM do
  Nettleton 2016 (CC BY-NC-ND, O2/UOC) está atrás de verificação anti-bot
  (Anubis) que exige navegador real. *Resolvidas na mesma sessão:* os 3 PDFs
  foram baixados manualmente pelo autor, renomeados para a convenção
  `Autor_Ano_PalavraChave.pdf` e o catálogo passou a registrar **14/14
  baixadas**. **(3) Catálogo:** `references/README.md`
  atualizado com as 14 entradas (arquivo, referência, DOI/link, status de
  acesso e fonte usada). **(4) Achado bibliográfico:** o DOI do Wörlein no
  `README.md` §12 estava **errado** (`10.1007/11564126_32` resolve para
  "Weka4WS", outro capítulo do mesmo LNCS 3721; confirmado via Crossref e
  Semantic Scholar) — corrigido para `10.1007/11564126_39`. Só docs; código
  congelado respeitado. Branch `docs/references-catalog-populate`
  (`Refs #177`).
- **Discussão de desdobramento da #174 — 5 pontos resolvidos pelo autor;
  enquadramento instrumental validado (DL-06). ✅ (docs, PR empilhado).**
  Respostas do autor aos pontos abertos no comentário de proposta: **(1)** formato
  do relatório = **Markdown** (conversão posterior, ex.: pandoc); **(2)** proteção
  do texto privado = **backup externo do autor**; **(3)** rastreabilidade pública
  (matriz seção→fontes em `docs/`) = **sim**; **(4)** enquadramento instrumental =
  **validado** — a premissa fundadora do projeto ("**anonimizar não é o
  suficiente**": hipótese demonstrada no artigo de referência, a provar por meios
  próprios pela replicação do experimento) entra na introdução do relatório e do
  artigo. Registrado como **DL-06** no `decision_log.md` (índice + entrada) e
  lacuna correspondente **encerrada** no `mapa_estrutural.md` §Lacunas; **(5)**
  prioridade de privacidade da produção acadêmica — **DoDs das issues #174 e #175
  emendadas** via `gh issue edit`: o item "arquivo versionado no repositório via
  PR" foi substituído por "texto consolidado em `academic/` (privado) +
  rastreabilidade pública versionada em `docs/`". As sub-issues S10-W1a..f serão
  criadas em **nova sessão** (decisão do autor — não iniciadas aqui). Só docs;
  código congelado. Branch `docs/dl06-instrumental-framing` (empilhada sobre
  `docs/academic-dir-174`, `Refs #174`).
- **Issue #174 (S10-W1) — análise, infraestrutura `academic/` e proposta de
  desdobramento. ✅ (docs/setup, PR aberto).** **(1) Análise da #174** contra o
  estado de `main`: bloqueios zerados (nenhum PR aberto; PRs #167–#170 e #164
  todos MERGED), `W-01..W-06` todos resolvidos no checklist, mapa estrutural
  consolidado — pré-condições da redação satisfeitas. **(2) Infraestrutura
  `academic/`** (decisão do autor, 2026-06-09): criada a pasta `/academic` para
  abrigar os documentos acadêmicos (relatório #174, artigo #175), que são
  sujeitos a **avaliação qualificada** e não podem ser públicos (o repositório é
  aberto). Regra no `.gitignore` (`/academic/*` + `!/academic/README.md`): só o
  `academic/README.md` é versionado — documenta a existência e a regra, não o
  conteúdo. Apontador adicionado ao `README.md` §7 (estrutura). **Implicação na
  DoD da #174:** o item "arquivo do relatório versionado no repositório via PR"
  fica **substituído** — o texto do relatório vive em `academic/` (privado);
  o que se versiona publicamente é a rastreabilidade (esqueleto/sumário e
  matriz seção→fontes em `docs/`, se validado pelo humano). **(3) Proposta de
  desdobramento da #174 em sub-issues (S10-W1a..f)** postada como comentário na
  própria #174 para discussão/validação humana — a redação não cabe em uma
  sessão única. Pontos pendentes de decisão humana sinalizados no comentário:
  formato do documento (Markdown vs LaTeX/DOCX), destino público da
  rastreabilidade e o **enquadramento instrumental** (#99/#140/#141 — exige
  validação humana antes de entrar no texto, cf. mapa_estrutural §Lacunas).
  Sem alteração em `src/` ou testes. Branch `docs/academic-dir-174`
  (`Refs #174`).
- **Saneamento pós-fechamento da #141 (S10-V1): resolver W-02..W-06 no checklist. ✅
  (docs, PR #170 aberto).** Regularização de **rastreabilidade**, não reabertura: a
  #141 cumpriu sua DoD original (popular `W-01..W-06` + resolver `W-01`/DL-05); esta
  PR alinha `docs/artifact_writing_checklist.md` ao estado já consolidado em `main`
  por **#128**/DL-04 e **#139**/D-16/D-13 e à confirmação empírica de **B1**. Move os
  cinco itens de "Itens ativos" para "Itens resolvidos" com ponteiro de fechamento:
  **W-02** (WL puro / opção (b), **D-16**, PR #139); **W-03** (`subgraph_timeout_count
  == 0` → **D-13** trivialmente satisfeito); **W-04** (B1 generaliza — gap `rr_subgrafo
  ≫ rr_grau` em `d=1` nos dois datasets: Facebook k=2 0,7914 vs 0,0263 em
  `results_baseline.md`; Enron k=2 0,123 vs 0,003 em `results_enron.md`; magnitudes
  distintas por escala/densidade, sinal qualitativo robusto); **W-05** (frase canônica
  fixada — Facebook principal `[M]` / Enron secundário `[D]` para validade externa, não
  réplica simétrica nem ponto de curva única; `scope.md` §3); **W-06** (painéis por
  dataset + painel normalizado complementar, **DL-04**/#128). "Itens ativos" passa a
  declarar explicitamente que **não há itens ativos**; resolução de redação migra para
  S10-W. Argumento de consistência: o `DL-05` já apontava para W-02/W-03 como local de
  rastreamento — o laço fica fechado. Só docs; `ruff check .` limpo. Branch
  `docs/writing-checklist-w02-w06-sanitize` (`Refs #141`).
- **Issue #141 (S10-V1): popular W-01..W-06 + resolver W-01. ✅ (docs, 2 PRs
  empilhados).** Primeira issue de *verificação* (S10-V) do milestone S10, sobre a
  infraestrutura criada por #140/#154. Executada em **dois PRs em sequência** (a
  pedido), com o PR 2 empilhado sobre a branch do PR 1 para não sobrescrever o
  registro. **(PR 1 — #167, `docs/writing-checklist-facebook-enron`, registro):**
  removido o item-piloto `W-00` (EXEMPLO do dry-run #157) e populados os **seis**
  itens reais `W-01..W-06` em `docs/artifact_writing_checklist.md`, cada um com os
  7 campos do template. Status conforme a DoD: **W-02/W-03** `em verificação` com
  ponteiro a #139/D-16 (decisão humana: manter fiel à DoD mesmo com #139 já
  mergeada); **W-04/W-05/W-06** `aberto` (resolução migra para S10-W ou follow-ups
  de #128/#139). **(PR 2 — #168, `docs/writing-checklist-w01-resolve`, resolução de
  W-01):** verificação técnica direta — o `he2009_facebook_full.yml` **omite**
  `s_max`/`isomorphism_mode`, mas o runner aplica defaults `4` (`run.py:610`) e
  `add_or_delete` (`run.py:614`) **idênticos** aos valores explícitos do
  `he2009_enron_secondary.yml`; com `k`/`d`/`sigma` já iguais, os 5 parâmetros do
  anonimizador coincidem e o valor efetivo é auditável no JSONL/`summary.json`. Logo
  a config **efetiva** é idêntica e **não** há equalização a fazer (opção (a) do
  W-01). Registrado como **DL-05** em `decision_log.md` (índice + corpo, tabela por
  parâmetro); W-01 movido para *Itens resolvidos* do checklist. **Nota de
  numeração:** o `D-16` sugerido no texto da #141 já estava em uso (WL-bucketing),
  então usou-se DL-05. PR 2 traz `Closes #141`. Só docs; sem alteração em `src/` ou
  testes.
- **Issue #161 (S10 / A06): mapa estrutural + sanitização documental. ✅ (docs).**
  Sexta sub-issue de infraestrutura do milestone **S10** (#140). Executada em **duas
  fases** conforme o comentário de encaminhamento da própria #161 — sanitização
  **antes** do escopo primário. **(1) Sanitização — correções de registro aplicadas
  diretamente:** `scope.md` (legenda `[D]`, bullet do d-sweep, bullet da entropia e
  rodapé descreviam como "em andamento"/"pendentes"/"não iniciado" issues já
  **fechadas** — #72–#78, #77/#88, #29, #30/D-17/PR #149; todas corrigidas, data do
  rodapé alinhada ao cabeçalho) e `achados_divergencias.md` §5 (lista de decisões
  parava em `D-10/DL-03` → atualizada para `D-17/DL-04`; `results_enron.md`
  acrescentado às refs cruzadas). **(2) Escopo primário (A06):** criado
  `docs/mapa_estrutural.md` — mapa de rastreabilidade A01–A06 → produto documental,
  localização, status e uso futuro (orientador; **não** duplica as issues). Achados
  que **não** são correção de registro (transição de fase / enquadramento instrumental
  herdado da #99/#140; população de `W-01..W-06`) foram **encaminhados**, não aplicados
  (boundary). Lista consolidada da sanitização registrada na #161. Só docs; sem
  alteração em `src/` ou testes. Branch `docs/mapa-estrutural` (`Closes #161`).
- **Issue #158 (S10 / A05): fechar a DoD da #140 (guarda-chuva) e habilitar a #141.
  ✅ (docs).** Quinta e última sub-issue de infraestrutura do milestone **S10**
  (#140). A premissa literal da #158 ("garantir a branch `docs/writing-checklist`
  com o trabalho de #154–#157 e abrir um PR consolidador") **estava obsoleta**: as
  quatro sub-issues já foram mergeadas em `main` por **PRs separados** — #154
  (PR #159), #155 (PR #160), #156 (PR #162), #157 (PR #163), todos **MERGED**
  (verificado via `gh pr list` + `git log origin/main`). Logo, a DoD substantiva da
  #140 já estava cumprida em `main` antes desta issue. **(1) DoD da #140 verificada
  item a item** contra o `artifact_writing_checklist.md` em `main`: arquivo/esqueleto
  criado (#154); seção "Papéis documentais e fronteiras" diferenciando os 3 papéis
  (#155); apontadores de localização em README/scope/progress/achados/decision_log
  (#156); template `W-NN` validado pelo piloto removível `W-00` com veredito de
  suficiência (#157). **(2)** Esta entrada de progresso dá conteúdo ao PR que fecha
  formalmente **#140** (guarda-chuva) e **#158** (A05). **(3) Comentário de
  habilitação deixado na #141** sinalizando infraestrutura pronta e pré-requisitos
  maduros (transição de fase de 06/06 herdada do encerramento da #99: #128 e #139
  fechadas). **Não** populados itens reais `W-01..W-06` (isso é da #141; o `W-00`
  EXEMPLO deve ser removido/substituído lá). Só docs; sem alteração em `src/` ou
  testes. Branch `docs/s10-x1-umbrella-close` (`Closes #140`, `Closes #158`).
- **Issue #157 (S10 / A04): dry-run do template `W-NN` contra assimetrias
  Facebook×Enron. ✅ (docs).** Quarta sub-issue do milestone **S10** (#140); depende
  de #154 (esqueleto, PR #159 **MERGED** — verificado em `origin/main` antes de
  começar). Inserido **1 item-piloto `W-00` (EXEMPLO removível)** na seção "Itens
  ativos" do `docs/artifact_writing_checklist.md`, ilustrando um ponto de
  assimetria Facebook×Enron: não-comparabilidade de magnitude de `rr_subgrafo`
  (escala/densidade/origem OR-D-11/motor KL×pymetis) → usar painel **normalizado**
  em vez de sobrepor magnitudes absolutas. Origem citada só como referência: **#128**
  e **#139** (ambas fechadas), achado **C2**, decisão **D-11** — nenhuma reaberta ou
  refatorada. **Veredito do dry-run:** os **7 campos** do template (ID, Origem, Tipo,
  Descrição, Critério de fechamento, Destino no texto, Status) acomodaram o ponto
  **sem campo faltante** → template suficiente, **nenhum ajuste em #154 necessário**.
  Item marcado como EXEMPLO removível (`W-00` fora da faixa real `W-01`+) com nota de
  remoção/substituição pela #141 — "Itens ativos" pronta para a popular. **Não**
  populados itens reais W-01..W-06 (isso é da #141). Só docs; sem alteração em `src/`
  ou testes. Branch `docs/checklist-dryrun` (`Closes #157`).
- **Issue #156 (S10 / A03): apontadores de localização do checklist nos índices
  vivos e docs retrospectivos. ✅ (docs).** Terceira sub-issue do milestone **S10**
  (#140); depende de #154 (arquivo-alvo, PR #159 **MERGED**) e complementa #155
  (PR #160 **MERGED**) — ambos verificados em `origin/main` antes de começar.
  Inseridos **apontadores de 1 linha** (links relativos) para
  `docs/artifact_writing_checklist.md`, **sem reescrever** conteúdo retrospectivo:
  **(1)** `README.md` — novo bloco **S10** no índice de docs (§4); **(2)**
  `docs/scope.md` — linha no blockquote de cabeçalho; **(3)** `docs/progress.md` —
  esta entrada de S10; **(4)** `docs/achados_divergencias.md` — frase de cabeçalho
  (retrospectivo/fechado → fila prospectiva no checklist); **(5)**
  `docs/decision_log.md` — frase de cabeçalho (registro de decisões tomadas, não
  fila → checklist). Nenhuma alteração de conteúdo retrospectivo além das
  linhas/frases de apontamento. Só docs; sem alteração em `src/` ou testes. Branch
  `docs/checklist-pointers` (`Closes #156`).
- **Issue #155 (S10 / A02): diferenciação dos 3 papéis documentais no checklist. ✅
  (docs).** Segunda sub-issue do milestone **S10** (#140), depende de #154
  (esqueleto, PR #159 **MERGED**). Adicionada a seção **"Papéis documentais e
  fronteiras"** ao `docs/artifact_writing_checklist.md`, com 1 frase por papel +
  ponteiros de ida (links relativos): **(1)** `achados_divergencias.md` —
  retrospectivo, fechado (proposto × executado); **(2)** `decision_log.md` —
  registro de decisões já tomadas, **não** fila de pendências; **(3)** o próprio
  checklist — fila **prospectiva** de verificações a confirmar/declarar até virarem
  decisão (migra p/ `decision_log.md`) ou texto no artefato final. Regra de
  fronteira explicitada (dúvida sobre "onde registrar" → artefato novo). **Nenhuma
  reescrita** de conteúdo em `achados_divergencias.md`/`decision_log.md` (apontadores
  ficam na #156). Só docs; sem alteração em `src/` ou testes. Branch
  `docs/checklist-doc-roles`, PR #160 (`Closes #155`).
- **Issue #154 (S10 / A01): esqueleto de `docs/artifact_writing_checklist.md`. ✅
  (docs).** Primeira sub-issue do milestone **S10** (consolidação documental, #140).
  Criada apenas a **infraestrutura** do checklist de verificação pré-escrita —
  pontos a resolver/declarar **antes** da redação de cada seção (DoD da S10).
  **(1) Cabeçalho/propósito**: documento *prospectivo* que **não substitui**
  `achados_divergencias.md` (retrospectivo), `decision_log.md` (decisões) nem
  `limitations.md` (limitações) — referencia, não copia. **(2) "Estrutura de cada
  item"**: campos do item `W-NN` (ID, Origem, Tipo `[verificação técnica | ponto
  interpretativo | decisão pendente | nota de método]`, Descrição, Critério de
  fechamento, Destino no texto, Status `[aberto | em verificação | resolvido]`).
  **(3) Convenção de numeração** `W-NN` sequencial e **não reaproveitada**,
  documentada no próprio arquivo. **(4)** Seções **"Itens ativos"** e **"Itens
  resolvidos"** vazias. Itens W-NN **não** populados (fica na #141); **nenhum**
  conteúdo movido dos docs retrospectivos. Só docs; sem alteração em `src/` ou
  testes. Branch `docs/writing-checklist`, PR #159 (`Closes #154`).
- **Sanitização de fim de issue (#30): auditoria de amparo bibliográfico. ✅
  (docs).** Verificação de que toda técnica/metodologia/processo formalmente
  nomeada está amparada na literatura apresentada (item 1) + consistência
  bibliografia↔uso (item 3). **Dois achados** (novo **Grupo C** em
  `achados_divergencias.md`): **C1** — **VF2** (Cordella et al. 2004) e **hash
  Weisfeiler-Lehman** (Shervashidze et al. 2011) eram nomeados em todo o repo
  **sem referência**; adicionados ao README §13 e citados no ponto de uso em
  `algorithm_notes` §2.3, `limitations` §2.5, `achados` A2, `decision_log`
  D-09/D-16, `scope` e `metrics_definitions` §7.1. **C2** — o corpo do README
  citava só **4 das 12** refs da §13; citações inline acrescentadas (Leskovec,
  Karypis, Wörlein, Sweeney, Liu, Zhou, Backstrom, Narayanan) → as **14** entradas
  da §13 (12 + VF2 + WL) passam a ser citadas no corpo, tornando-a lista de
  *referências citadas* honesta. **KL e KS** deixados **sem** referência primária
  por decisão (função de biblioteca / teste de manual). Resíduo menor:
  Díaz/Serjantov acrescentados à lista §10 de `algorithm_notes` (citados em §4.4,
  faltavam na lista). Também migrado **B3** (ataque por entropia) para
  *implementado* (#30/D-17, baseline uniforme; em `main` via PR #149). Só docs;
  sem alteração em `src/` ou testes.
- **Issue #30 (S6 / D-17): métrica de entropia — baseline uniforme. ✅ (código +
  testes).** Implementada a parte decidida por D-17 (caminho uniforme). **(1)**
  `src/metrics/entropy.py` (**lar primário**): `entropy_metrics(groups, tau=0.0)`
  reusa os grupos de equivalência (não refaz experimentos) e retorna `entropy_mean`
  (média node-weighted de `H=log2(n_r)`), `degree_of_anonymity` (Díaz et al.,
  `H/H_max ∈ [0,1]`), `reidentification_rate_entropy` (fração com `H≤τ`) e `tau`.
  **(2)** `src/attacks/entropy.py`: **apontador** de leitura adversarial que
  reexporta a métrica (satisfaz o checkbox `src/attacks/entropy.py` da #30 sem
  duplicar lógica — D-17, métrica ≠ ataque autônomo). **(3)** Runner: bloco
  `entropy` no JSONL; `τ` lido de `metrics.entropy_tau` (D-E3). **(4)**
  `config_example.yml` (métrica + `entropy_tau`; comentário do ataque reclassificado)
  e `tables.py` (colunas `degree_of_anonymity`/`reid_rate_entropy` anexadas). **(5)**
  Testes: 15 (métrica) + 2 (apontador) + 3 (propagação config→runner) + ajustes nos
  testes de schema (`test_tables`, stub `_always_error`). **Suíte 615 passed, ruff
  limpo.** **(6)** Caminho **não uniforme** (D-E2(b)) — decisão do humano: **deixado
  para depois**, formalizado como **issue #148 (sem milestone)**; D-17 ganhou seção
  "Status final" + cross-ref a #148. Branch `attack/entropy` (`Closes #30`).
- **Fechamento administrativo do milestone S9. ✅** Conferência final dos DoDs de
  todas as 9 sub-issues (#122–#129, #139) contra o `main` — todos atendidos, CI
  verde nos 3 check-runs. **Opção A aplicada** à #29: comentário de conferência
  postado marcando os 4 itens da DoD com `[x]` e rastreabilidade
  (loader OR/D-11/#124, config/#126, execução grau+subgrafo hop=1/D-16/#127/#139,
  gráficos comparativos/#128). **Issue-mãe #29 fechada** (`state_reason:
  completed`) e **milestone S9 `closed`** (9/9 fechadas). A pendência cosmética da
  marcação da DoD da #29 (antes bloqueada pelo classifier) está resolvida.
- **Issue #129 (S9-7): fechamento do ciclo S9 — revisão cruzada + Definição de
  Pronto da #29. ✅ (docs).** Última issue do milestone S9. Verifiquei os
  bloqueios via `gh` antes de começar: **todos os PRs do ciclo S9 estão `MERGED`**
  — #143 (S9-6, `2026-06-05`) e #144 (#128 follow-up, `2026-06-06T11:16:36Z`)
  inclusive (o `progress.md` os listava como pendentes; estado corrigido). **(1)
  Cross-review de fidelidade** código↔config↔logs↔`results_enron.md`: config
  `he2009_enron_secondary.yml` (d=1, σ=0,5, s_max=4, add_or_delete, sementes
  [42,1337,2718], k∈{2,5,10,20}) bate com `summary.json` (12 runs, `any_failure:
  false`, pymetis 12/12) e com o JSONL — spot-check k=2/seed=42 →
  `rr_subgrafo=0,122893`, `rr_grau=0,003235`, `clust_var=0,015644`, `tmo=0`,
  idênticos à tabela bruta de `results_enron.md`; `subgraph_timeout_count=0` nas
  12 runs (gate D-13 trivial). **Nenhuma divergência silenciosa** entre os
  artefatos do S9. **(2) Definição de Pronto da #29** conferida — 4/4 itens
  cumpridos: loader OR (#124), config YAML (#126), execução grau+subgrafo hop=1
  (#127/#139, 12 runs SUCCESS_PARTIAL), gráficos comparativos FB×Enron (#128).
  *Edição do corpo da #29 (marcar checkboxes) bloqueada pelo classifier de
  permissão — pendente de ação humana; veredito registrado aqui e no PR.* **(3)
  D-11 (regra OR)** ganhou seção **"Status final (S9-7/#129) — Implementado e em
  produção"** no `decision_log.md`: cadeia loader→testes→execução em `main`,
  projeção aplicada às 12 runs (LCC n=33.696/m=180.811); alternativa AND
  rejeitada e não executada; decisão encerrada. **(4) Achado B2** atualizado em
  `achados_divergencias.md` (gap de validade externa **parcialmente fechado**: o
  Enron foi executado no S9, reforçando a validade externa antes só declarada;
  resíduo aberto = `multiple_egonets` ainda não executado) — linha-resumo e seção
  detalhada. Somente docs; sem alteração em `src/` ou testes. Branch
  `loader/enron-close` (`Closes #129`).

- **Issue #128 — follow-up (revisão pós-merge do PR #143). ✅ (docs + nova
  visualização + testes).** Responde aos pontos da revisão de completude/acuidade
  feita na #128. **(1) D1/DL-04 — painel comparativo normalizado:** novo módulo
  `src/visualization/comparison.py` (+14 testes em `tests/visualization/`) gera um
  painel de 2 eixos **normalizados** — (A) `rr_subgrafo·k` = fração da cota `1/k`
  (linha em 1,0; mostra os cruzamentos: FB acima da cota em k∈{2,5,10}, Enron
  cruzando em k=20; curvas se cruzam ~k≈14) e (B) decaimento relativo
  `rr(k)/rr(k_min)` (forma da curva, magnitude removida). Snapshot **versionado**
  em `docs/assets/comparison_fb_enron.{png,csv}` (exceção documentada à regra de
  gitignore — artefato auditável da banca, regenerável). Embed + explicação +
  cruzamentos em `results_enron.md`; decisão registrada como **DL-04**
  (`decision_log.md`). **(2) C1 — cota `1/k`:** nota explícita de que `rr_subgrafo
  ≤ 1/k` pressupõe k-anon da estrutura inspecionada (`d≥2`) e **não vale em `d=1`**
  (B1) → violação esperada em k=20 (0,057>0,050), não bug; em `results_enron.md`
  e `data_dictionary.md`. **(3) C2 — motor não-pareado:** ameaça à validade interna
  (KL×pymetis, baixa magnitude) em `results_enron.md` e `limitations.md` §3/§4.
  **(4) B/D4 — arredondamento:** tabela bruta de `make_enron_table.py` agora em 6
  casas + nota de que o agregado usa precisão plena (`média(arredondados) ≠
  arredondamento(média)`). Suíte **595 passed** (+14), ruff limpo. Branch
  `docs/results-enron-followup`.

- **Issue #128 (S9-6): comparativo Facebook × Enron + `docs/results_enron.md`
  (tier desejável, issue-mãe #29). ✅ (gerador + docs).** Consome os 12 runs do
  Enron já com a curva **grau × subgrafo** (D-16). **(1) Gerador**
  `experiments/make_enron_table.py` (espelha `make_baseline_table.py`): lê o JSONL
  do Enron e produz `docs/results_enron.md` por completo — header, síntese
  metodológica, comparativo Facebook×Enron, tabela bruta (k,semente), agregação
  por k e interpretação. Carrega o log do Facebook baseline quando presente para
  a tabela comparativa (fallback embutido a partir de `results_baseline.md` se
  ausente). **(2) `docs/results_enron.md`**: agregados por k — `rr_subgrafo` cai
  monotonicamente 0,124→0,102→0,079→0,057; `rr_grau` ∈ [0,0019; 0,0033] (~40×
  menor); KS-D 0,038→0,130; clust 0,017→0,093; cobertura ≥0,9960, todas
  `SUCCESS_PARTIAL` (déficit estrutural D-06). **(3) Comparativo**: as magnitudes
  **não** são diretamente comparáveis (escala n=532 vs 33.696; densidade; origem
  OR/D-11; motor KL vs pymetis) — DoD satisfeito justificando que **sobrepor as
  duas redes num só gráfico é enganoso** (faixas 0–79% vs 0–12%); gráficos gerados
  **por dataset** (`results/plots/privacy_utility_enron.*`, gerador existente sem
  alteração). Tendências robustas em ambas: subgrafo≫grau, monotonicidade em k,
  utilidade melhor preservada em escala. **(4) `docs/data_dictionary.md`**: nova
  §1.1 "Datasets" com Facebook [M] e Enron [D] (origem SNAP, regra OR/D-11, LCC
  n=33.696/m=180.811, nota de comparabilidade). **(5)** Tabelas/plots gerados em
  `results/{tables,plots}/` (gitignored) via tooling existente; ao gerá-los
  descobri que o `rglob` recursivo capturava o backup só-grau da #127 (24 vs 12
  runs, `rr_subgrafo` contaminado p/ 0,062) — backup gitignored realocado de
  `he2009_enron_secondary/_pre139_degree_only_backup/` para
  `experiments/logs/_pre139_degree_only_backup/`. Suíte **581 passed**, ruff limpo
  (file-level `noqa: RUF001` no gerador — emite tipografia pt-BR ×/–). Branch
  `loader/enron-results` (`Closes #128`).

- **Issue #139 (S9-8): ataque por subgrafo via bucketing de WL-hash — viabiliza
  o subgrafo FULL no Enron (resolve D-15). ✅ (código + testes + execução +
  decisão D-16).** A inviabilidade de ~70 dias registrada em D-15 foi **superada
  por engenharia**, não por adiamento. **(1) Caminho rápido**
  (`src/attacks/subgraph.py::subgraph_candidate_counts` + `_AnonNeighbourhoodIndex`):
  pré-computa o WL-hash das n vizinhanças 1-hop do `g_anon` **uma vez**,
  indexa-as em baldes por hash e resolve cada alvo por **lookup** — O(n)
  precompute + O(n) lookups, substituindo o O(n²) de re-extração. **(2)
  Salvaguarda de exatidão** pelo critério objetivo da #139: o WL **puro** bateu
  **100%** com o VF2 brute-force (contagens E vereditos `count==1`) na bateria de
  grafos pequenos (`tests/attacks/test_subgraph.py`) → adota-se WL puro (opção
  (b)); refinamento híbrido VF2 disponível (`refine_max_size`), **hubs nunca
  refinados** (explosão de automorfismos). Argumento de correção: WL é invariante
  **necessário** (isomorfos ⇒ mesmo hash) → nenhum isomorfo é perdido; único erro
  teórico é sobrecontagem por colisão, descartada empiricamente. **(3)
  Verificação ampla** no Enron LCC (k=2/seed=42): amostra estratificada por grau
  de **70 nós, 0 divergências** (ALL MATCH) vs. VF2 brute-force; `subgraph_candidate_counts`
  dos 33.696 alvos em **35,9 s** (~15.000× vs. brute). **(4) Runner**
  (`experiments/run.py`): laço do subgrafo passa a usar o caminho rápido;
  `subgraph_timeout_count` gravado como **0** (sem timeout por nó) → gate D-13
  trivialmente satisfeito. **(5) Config**: `attacks.subgraph.enabled: true`
  (hop=1) reabilitado, comentário atualizado (D-15 resolvido por D-16). **(6)
  Execução FULL**: 12 runs (k∈{2,5,10,20} × 3 sementes), **todas SUCCESS_PARTIAL,
  0 falhas, 0 timeouts**, pymetis; `reidentification_rate_subgraph` **cai
  monotonicamente com k** — k=2 ≈ 0,124; k=5 ≈ 0,102; k=10 ≈ 0,079; k=20 ≈ 0,057
  — ~40× a taxa de grau (~0,002–0,003), coerente com B1 (em `d=1` anonimiza-se
  grau, não a estrutura 1-hop). Logs limpos em
  `experiments/logs/he2009_enron_secondary/` (12 linhas + `summary.json`;
  gitignored; logs só-grau da #127 movidos para `_pre139_degree_only_backup/`).
  **(7) Docs**: `decision_log.md` — índice + entrada **D-16** (método, correção,
  evidência, gate D-13) + **extensão de D-15** (resolvido por otimização;
  caminho de amostragem agora OBSOLETO). `results_enron.md` **não** editado
  (responsabilidade da #128). Suíte **581 passed** (+16 no subgrafo), ruff limpo.
  Branch `attack/subgraph-wl-bucketing` (`Closes #139`).

- **Issue #127 (S9-5): execução secundária Enron — SÓ-GRAU (subgrafo full
  inviável, D-15). ✅ (execução + config + decisão).** Probe de custo empírico
  sobre o Enron LCC (n=33.696, m=180.811, pymetis) mediu o ataque por subgrafo
  full em **~15 s/nó-alvo × 33.696 ≈ 5,85 dias/run → ~70 dias** nas 12 runs —
  proibitivo; o timeout de 120 s (D-12) **não** limita (nenhum nó é patológico;
  custo agregado, O(n²) de re-extração de vizinhanças). Decisão **D-15**: a #127
  roda **só o ataque por grau** (viável, ~404 s/run); subgrafo `enabled: false`
  na config canônica com justificativa inline; subgrafo adiado para issue de
  continuação (**S10**, amostragem de nós-alvo — descritivo preparado). **(1)**
  `experiments/configs/he2009_enron_secondary.yml`: `attacks.subgraph.enabled:
  false` + bloco de comentário com o achado e o caminho de amostragem. **(2)**
  `docs/decision_log.md`: índice + entrada **D-15** (evidência, por que o timeout
  não resolve, decisão só-grau, continuação por amostragem, alternativa
  VF2-cache rejeitada nesta issue). **(3) Execução:** 12 runs (k∈{2,5,10,20} ×
  3 sementes), **todas SUCCESS_PARTIAL** (coverage 0,996–0,9999, déficit
  estrutural D-06), **0 erros**, backend pymetis; `reidentification_rate_degree`
  ∈ [0,0018; 0,0034] (cai levemente com k); logs em
  `experiments/logs/he2009_enron_secondary/` (`.jsonl` 12 linhas + `summary.json`,
  `any_failure: false`) — gitignored por `.claude/rules/experiments.md`. D-13
  (`subgraph_timeout_count == 0`) não se aplica (subgrafo desabilitado); ataque
  por grau não usa VF2/timeout. Branch `loader/enron-run` (`Closes #127`).

- **Issue #126 (S9-4): config YAML do experimento secundário Enron —
  `he2009_enron_secondary.yml`, subgrafo restrito a hop=1. ✅ (só config).**
  Espelha `he2009_facebook_baseline.yml` com valores específicos do Enron.
  `dataset.name: enron`, `data_path: data/raw/enron/`, `component: lcc`,
  `min_nodes: 200` (= 10 × k_max); o ramo `enron` de `load_dataset` (#125) usa
  apenas `data_path` + `component`/`min_nodes` genéricos. Sementes
  `[42, 1337, 2718]` lidas do YAML (≥3). `anonymization`: `k: [2,5,10,20]`,
  `d: 1`, `sigma: 0.5`, `s_max: 4`, `isomorphism_mode: add_or_delete` (chaves
  auditadas no S8, lidas em `run.py:588/592`). `attacks.degree.enabled: true`;
  `attacks.subgraph` com `enabled: true`, `hop: 1` explícito e `timeout: 120`s
  por nó (margem VF2 na escala maior do Enron; DoD #29/#126 — **não** habilitar
  hop>1). Cabeçalho documenta o enquadramento secundário [D], a projeção OR
  (D-11) e cita #29. YAML validado por `yaml.safe_load` (UTF-8, como o runner);
  `ruff check .` limpo. Sem alteração em `src/`/testes. Branch
  `loader/enron-config`, PR #134 (`Closes #126`).

- **Issue #125 (S9-3): integração no runner — ramo `enron` em `load_dataset()`.
  ✅ (código + teste).** Único ponto de contato do loader Enron com o núcleo do
  pipeline. **(1)** `experiments/run.py`: `load_dataset()` ganha o ramo
  `elif name == "enron"`, que chama `load_enron(Path(dataset_cfg["data_path"]))`
  e loga `n`/`m` do grafo bruto (espelhando o Facebook); `import load_enron`
  adicionado. Mensagem de erro de dataset desconhecido passa a listar os dois
  datasets suportados: `facebook_ego_nets, enron`. O pós-processamento
  `component` (LCC) / `min_nodes` **não foi duplicado** — já é genérico e roda
  após `load_dataset`. Sem toque em ataques/métricas/visualização. **(2)**
  `tests/experiments/test_run_enron_dataset.py` (6 testes, espelha
  `test_run_config_propagation.py`): dispatch `name: enron` → `load_enron` com
  simetrização OR (D-11); LCC + `min_nodes` fluindo pelo novo ramo; edge list
  ausente → `FileNotFoundError`; mensagem de erro lista ambos os datasets;
  `main()` end-to-end com config Enron (edge list real em `tmp_path`) → SUCCESS +
  `summary.json`/JSONL. Suíte completa **568 passed**; `ruff check`/`format`
  limpos. Branch `loader/enron-runner`, PR #133 (`Closes #125`).

- **Issue #124 (S9-2): loader `load_enron` — conversão direcionado→não-dir. por
  simetrização OR (D-11). ✅ (código + teste).** Segundo código de loader do ciclo
  S9, espelhando o contrato de `load_facebook_egonet`. **(1)** `src/loaders/enron.py`:
  `load_enron(data_dir: Path) -> nx.Graph` lê `data_dir/email-Enron.txt` (edgelist
  SNAP, comentários `#` ignorados pelo `read_edgelist`); lê em `nx.DiGraph` e aplica
  `.to_undirected()` — **simetrização OR (D-11)**: `{u, v}` existe se `u→v` **ou**
  `v→u`; pares recíprocos e de mão única colapsam para 1 aresta; rótulos inteiros;
  `FileNotFoundError` com caminho claro (padrão Facebook). `lcc`/`min_nodes` ficam
  com o runner (fora de escopo, agnóstico ao dataset). Docstring NumPy-style citando
  D-11. **(2)** `tests/loaders/test_enron.py` (fixtures sintéticas, sem rede, 6
  testes): não-direcionado, rótulos inteiros, OR par recíproco, OR par de mão única,
  comentários ignorados, arquivo ausente. `ruff check .` limpo; loaders **24 passed**.
  Branch `loader/enron-load`, PR #132 (`Closes #124`).

- **Issue #123 (S9-1): download idempotente do Email-Enron (SNAP) — SHA-256 +
  gzip. ✅ (código + teste).** Primeiro código de loader do ciclo S9, espelhando
  `src/loaders/download.py` (Facebook). **(1)** `src/loaders/download_enron.py`:
  `download_enron(dest=RAW_DIR)` baixa `email-Enron.txt.gz` de
  `https://snap.stanford.edu/data/email-Enron.txt.gz` e descompacta para
  `data/raw/enron/email-Enron.txt`; idempotente (sai cedo se o arquivo já existe);
  loga **SHA-256** e tamanho do `.gz` (rastreabilidade, como no Facebook); reusa
  `_ProgressHook` e `_sha256` importados de `download.py` (sem duplicação);
  rejeita payload não-gzip cedo (`BadGzipFile`). Diferença vs. Facebook: arquivo
  único `.gz` via `gzip`, não tar. **(2)** `tests/loaders/test_download_enron.py`
  (rede mockada, 7 testes). **(3)** `data/raw/enron/.gitkeep` versionado; regra de
  negação adicionada ao `.gitignore` (`!/data/raw/enron/` + `/data/raw/enron/*` +
  `!/data/raw/enron/.gitkeep`) — dados brutos seguem ignorados. A projeção OR
  (D-11) é responsabilidade do **loader**, não deste downloader. `ruff check .`
  limpo; suíte de loaders **18 passed**. Branch `loader/enron-download`, PR #131
  (`Closes #123`).

- **Issue #122 (S9-0): âncora do Loader Email-Enron — decisão direcionado→não-dir.
  (OR) + enquadramento. ✅ (somente docs/setup; sem código de loader).** Abertura do
  ciclo S9 espelhando o padrão de âncora do S7/S8. **(1) Decisão D-11** registrada em
  `docs/decision_log.md` (índice + entrada): simetrização **OR** (aresta `A — B` se
  houver e-mail em qualquer direção) como projeção direcionado→não-direcionado do
  Email-Enron, com justificativa (convenção SNAP/comparabilidade; retenção de
  estrutura, paralelo ao LCC do Facebook; cenário de risco conservador), impacto
  estrutural (densidade/conectividade maiores; núcleo intocado — projeção é
  responsabilidade do loader) e **alternativa rejeitada** (reciprocidade AND →
  candidata a análise de sensibilidade futura). **(2) `docs/scope.md` §3** atualizado:
  Facebook permanece `[M]` (principal); **Enron destacado em linha própria `[D]`**
  (secundário do tier desejável, simetrização OR, cross-ref D-11/#29/#122); header e
  rodapé com data/estado de S9. **(3) Branch base `loader/enron`** criada a partir de
  `main` (PR #121/S8 já em `main`). Sem alteração em `src/` ou testes; `ruff check .`
  limpo. Branch `loader/enron` (`Closes #122`).

- **Issue #111 (S8-8): fechamento do milestone S8 — revisão cruzada + migração
  formal dos status em `achados_divergencias.md` (§4 executada). ✅** Última issue
  do milestone. **(1) Revisão cruzada de consistência** das mudanças S8 verificada
  no código: `experiments/run.py` lê `anonymization.s_max` (alias `fsm_max_size`,
  `run.py:577`) e `anonymization.isomorphism_mode` (`run.py:581`, validado contra
  `_ISOMORPHISM_MODES`), propaga ambos a `anonymize()`/`_modify_structure`/
  `_group_isomorphic` e grava no JSONL+`summary.json`; `anonymize()` expõe os
  params (`he2009.py:243-244`); `config_example.yml` expõe `k`/`d`/`sigma`/`s_max`/
  `isomorphism_mode` (linhas 69–94). **Nenhuma afirmação de configurabilidade sem
  respaldo no código** e nenhuma contradição KL/pymetis ou `d=1`/d-sweep —
  os "hardcoded" remanescentes nos docs são descrições históricas de "Executado"
  com a respectiva "Atualização" de fechamento. **(2) `achados_divergencias.md`:**
  matriz da §1 migrada — **A1 ⚠️→✅** (#107), **B1 ⚠️→✅** (#108), **B2 ⚠️→✅**
  e **B7 ⚠️→✅** (#109), **B6 🔧→✅** (#105, corrigido no código); B5 já ✅ (#106).
  Agora **17/17 achados ✅**. Notas de "deixada para S8-8/#111" nas seções
  detalhadas (A1/B1/B2/B6/B7) atualizadas para "concluída em S8-8/#111". §4
  ("Pendências de revisão documental") marcada **✅ EXECUTADA** com nota de que
  B5/B6 foram resolvidos por **correção de código** (chaves efetivamente lidas),
  além da intenção original (apenas anotar). Header e §5 (DL-03) atualizados.
  **(3) Encerramento de S8** registrado em `decision_log.md` ("Nota de milestone —
  Encerramento do S8") e neste `progress.md`. Somente docs; sem alteração em `src/`
  ou testes. Branch `docs/s8-closure-cross-review-111` (`Closes #111`).

- **Issue #110 (S8-7): auditoria de fidelidade dos achados ✅ (A2–A9, B3, B4, B8).**
  Auditoria leve (não-edição, salvo regressão) confirmando que os achados marcados
  ✅ em `achados_divergencias.md` continuam coerentes com código/docs após as
  edições das Fases 1 e 2. **Veredito: 11/11 fiéis — nenhuma regressão.** Evidência
  reverificada item a item: **A2** `fsm_max_size: int = 4` default
  (`he2009.py:103/243/461`; "Executado" histórico já anotado com a atualização
  B5/#104); **A3** D-07 (`decision_log.md`) + §3.1/§4.1; **A4** D-08, teste
  `test_local_structures_connected_d_gt_1` (`test_he2009_partition.py`), §6; **A5**
  `validation.py:101` declara "does not import anything from he2009.py" — auditor
  independente; **A6** D-06, `incomplete_group` reportado como violador
  (`validation.py:165/206`); **A7** desempate lexicográfico ativo
  (`he2009.py:668/798` `key=lambda v: (-ls.degree(v), v)`), D-03, §3.3; **A8**
  `TestReconnectKTimesKMinusOne` (`test_he2009_anonymize.py`), §3.2.2, docstring;
  **A9** §2.2 marca complexidades "Interpretativa" (linhas 230–233); **B3** sem
  ataque por entropia em `src/attacks/` (só `degree`/`subgraph`); **B4** Nettleton
  não implementado (sem arquivo em `src/`; scope §3/§4); **B8** DL-01 +
  `satisfied_fraction`/`deficit_fully_structural` em `validation.py`. **Observação
  (não-regressão):** a evidência de B4 cita "`src/anonymization/` (placeholder)",
  mas não há arquivo placeholder concreto — a própria ausência confirma o
  "não implementado"; wording pré-existente, não introduzido pelas Fases 1/2.
  Somente docs (`progress.md`); sem alteração em `src/`/testes. Branch
  `docs/audit-checkmarks-110` (`Closes #110`).

- **Issue #109 (S8-6 / B2+B7): reafirmação de dataset único + nota de timeouts
  retroativos.** Tornados explícitos no texto público dois pontos de validade
  antes dispersos. **B2:** `results_baseline.md` ganhou a seção "Validade externa
  — dataset único (achado B2)" (única ego-rede 3437; nem Enron contingente nem
  `multiple_egonets` rodaram; generalização aberta; declarada ortogonal às
  ressalvas de B1/`d` e A1/motor); `results_dsweep.md` §5.7 passou a **nomear
  explicitamente** Enron e `multiple_egonets` como planejados-mas-não-executados.
  **B7:** o esclarecimento já estava completo em `results_dsweep.md` §5.5/§5.7
  (zeros genuínos — H3 descartada por inspeção, não reexecução; campos
  `subgraph_timeout_count`/`subgraph_candidate_counts` retroativos, DL-02) — texto
  existente satisfaz o critério; nada a acrescentar. Em `achados_divergencias.md`,
  status detalhado de B2 e B7 migrado ⚠️→✅; migração formal na tabela-resumo
  (linhas 78/83) deixada para S8-8/#111. Evidência citada verificada (`scope.md`
  §3; `limitations.md` §1.1; `config_example.yml:46`; DL-02/D-08). Somente docs —
  sem alteração em `src/` ou testes; `ruff check .` limpo. Branch
  `docs/reaffirm-dataset-timeouts-109`, PR #119 (`Closes #109`).

- **Issue #108 (S8-5 / B1): frase-síntese `d=1` = k-anonimato de grau; d-sweep =
  estrutural — inserida no README e em `results_baseline.md`.** Fechado o achado
  de maior consequência interpretativa (B1). A síntese — "no regime `d=1` os
  resultados rotulados 'He et al. structure-aware' equivalem a k-anonimato de
  grau; a propriedade estrutural só é exercida no d-sweep `d∈{5,10}`; o contraste
  `d=1` vs. `d∈{5,10}` é a evidência empírica de privacidade estrutural" — entrou
  em **dois** pontos de destaque: (1) `README.md` §5, callout "Leitura-chave" no
  topo da seção de Resultados, antes da tabela do baseline; (2)
  `results_baseline.md`, nova seção "Leitura-chave — `d=1` afere k-anonimato de
  grau", junto à apresentação do baseline. Para não contradizer S8-4/A1 (mesmo
  arquivo, PR #117 já mergeado), as duas ressalvas foram declaradas
  **ortogonais**: uma trata do *parâmetro* `d` (grau vs. estrutura), a outra do
  *motor* (KL vs. pymetis). Em `achados_divergencias.md`, status detalhado de B1
  migrado ⚠️→✅ e item 5 das pendências documentais riscado; migração formal na
  tabela-resumo (linha 77) deixada para S8-8/#111. Referências citadas
  verificadas (D-02; `algorithm_notes.md` §5.3/§6.5/§9.1). Somente docs — sem
  alteração em `src/` ou testes; `ruff check .` limpo. Branch
  `docs/synthesis-d1-degree-vs-structural-108`, PR #118 (`Closes #108`).

- **Issue #107 (S8-4 / A1): `results_baseline.md` declara explicitamente que o
  baseline `d=1` rodou no fallback Kernighan-Lin — não pymetis.** O número-título
  do baseline ("k-anonimato atingido") foi produzido pelo motor **não fiel** ao
  artigo: à época (issue #23, 2026-05-23) pymetis estava ausente local e na CI
  (confirmado pela auditoria #74, 30/05), e `backend="auto"` resolveu para o KL;
  o JSONL do baseline é anterior à gravação de `partition_backend` (#84). Nova
  seção **"Motor de particionamento — baseline d=1 rodou em KL"** com (1) o motor
  efetivo, (2) inocuidade para `d=1` (partições triviais de 1 nó → o
  desbalanceamento do KL p/ `ck>2`, D-04, é irrelevante; validação do marco 29/05
  permanece válida) e (3) contraste com o d-sweep (#88: pymetis em 48/48). Bloco
  de metadados ganhou a linha do motor de particionamento. Em
  `achados_divergencias.md`, A1 (status detalhado + item 3 das pendências
  documentais) migrado ⚠️→✅; números de linha da evidência atualizados
  (`he2009.py:338`, `run.py:271`, `config_example.yml:109`); migração formal na
  tabela-resumo deixada para S8-8/#111. Somente docs — sem alteração em `src/` ou
  testes; `ruff check .` limpo. Branch `docs/baseline-declare-kl-fallback-107`,
  PR #117 (`Closes #107`).

- **Issue #106 (S8-3 / B5): `config_example.yml` passa a expor
  `d`/`sigma`/`s_max`/`isomorphism_mode` (chaves agora lidas).** Com S8-1 (#104)
  e S8-2 (#105) tornando `s_max`/`fsm_max_size` e `isomorphism_mode` chaves YAML
  efetivamente lidas pelo runner, o exemplo de referência foi alinhado à
  interface real. O bloco `anonymization` do `config_example.yml` ganhou `d`
  (default de referência `1`; nota B1 d=1 grau vs d>1 estrutural; default
  conceitual 10 = D-02), `sigma` (`0.5`, D-01), `s_max` (`4`, D-01/A2; alias
  `fsm_max_size`) e `isomorphism_mode` (`add_or_delete` | `add_only`, B6), todos
  com comentários e defaults corretos. **Correção adicional:** `k_values` → `k`
  — o runner lê `anonymization.k`, não `k_values` (configurabilidade fantasma,
  mesma classe de erro que originou B5/B6); alinhado aos YAMLs experimentais.
  Cada chave exposta foi **verificada** como lida em `experiments/run.py::main`.
  Decisão registrada como **DL-03** em `decision_log.md`; `algorithm_notes.md`
  §5.1–5.3 atualizadas (mapeamento, divergência fechada, parâmetros
  confirmados); achado **B5** em `achados_divergencias.md` migrado 🔧→✅ (resíduo
  único: `partition_backend` ainda não exposto como chave YAML). Sem alteração em
  `src/`; YAML validado (parse + chaves). `tests/experiments` **65 passed**.
  Branch `docs/config-example-expose-params-106`.

- **Issue #112 (S8-2b): testes de propagação das novas chaves
  (config→anonymize→`_modify_structure`/`_group_isomorphic`) + regressão.**
  Cobertura de teste dedicada à mudança de comportamento de #104 (`s_max`/
  `fsm_max_size`) e #105 (`isomorphism_mode`), que passaram a ser lidas do YAML.
  **`tests/anonymization/test_he2009_modify.py`** estendido com 3 classes
  (+18 testes) cobrindo o caminho via `anonymize()`: `isomorphism_mode="add_only"`
  → `_modify_structure(add_only=True)` (via spy `wraps`) e efeito "nenhuma
  aresta removida"; default `add_or_delete` (add_only=False); valor inválido
  levanta `ValueError`; `fsm_max_size` → `_group_isomorphic` (spy) e default 4;
  grouping idêntico para `s_max∈{4,5}` em `cycle_graph(20)`/d=5 (G2/D-01);
  regressão default==explicit e determinismo do baseline d=1. **Novo
  `tests/experiments/test_run_config_propagation.py`** (12 testes) cobre o
  caminho config→runner: `isomorphism_mode`/`s_max` gravados no JSONL e no
  `summary.json`; ausência da chave usa o default (`add_or_delete`/4); alias
  `fsm_max_size` aceito; `isomorphism_mode` inválido aborta `main()` antes do
  laço; valores efetivos chegam a `_modify_structure`/`_group_isomorphic` (spy
  helper `_SpyWrapper` que registra chamadas e delega à função real); regressão
  do baseline d=1 (duas execuções idênticas). Sem alteração em `src/`. Addenda
  B5/B6 em `achados_divergencias.md` atualizados (propagação coberta por #112).
  Suíte **549 passed**, ruff + format limpos. Branch
  `test/config-propagation-112`.

- **Issue #105 (S8-2 / B6): exposição de `isomorphism_mode` como chave lida
  do YAML.** A variante de isomorfização da Fase 2 deixou de ser
  `add_only=False` hardcoded: `anonymize()` ganhou o parâmetro
  `isomorphism_mode: str = "add_or_delete"` (valida o valor e o converte em
  `add_only = (isomorphism_mode == "add_only")`, repassando a
  `_modify_structure`); o runner (`experiments/run.py`) lê
  `anonymization.isomorphism_mode`, valida-o antes do laço, propaga-o a
  `anonymize()` e ao caminho inline (`_modify_structure(add_only=...)`) e grava
  o valor efetivo no JSONL e no `summary.json`. Constante
  `_ISOMORPHISM_MODES = {"add_or_delete", "add_only"}` adicionada a
  `he2009.py`. Default `add_or_delete` preserva o comportamento histórico.
  Docs: docstring de `anonymize()`, `algorithm_notes.md`
  §3.2.1/§3.4/§5.1/§5.2/§5.3, e addendum B6 em `achados_divergencias.md`
  (status 🔧→✅). Ajuste mínimo no stub `_always_error` de `test_runner.py`
  (novo kwarg; cobertura de propagação é S8-2b/#112). Suíte **525 passed**,
  ruff + format limpos. Branch `anonymization/expose-isomorphism-mode-105`.

- **Issue #104 (S8-1 / B5): exposição de `s_max`/`fsm_max_size` como chave lida
  do YAML.** O tamanho máximo de subgrafo do FSM simplificado deixou de ser
  hardcoded: `anonymize()` e `_group_isomorphic()` passaram a aceitar
  `fsm_max_size` (default 4) e o runner (`experiments/run.py`) lê
  `anonymization.s_max` (alias `fsm_max_size`) do YAML, propaga por `run_one()`
  e grava o valor efetivo no JSONL e no `summary.json`. Docs atualizadas:
  `algorithm_notes.md` §5.1/§5.2/§5.3 (chave YAML lida), `limitations.md` §2.1,
  e addenda em `achados_divergencias.md` (A2, B5). Suíte **525 passed**, ruff
  limpo. Branch `anonymization/expose-smax-104`, PR #113 (`Closes #104`).

- **Issue #80 (D-08 / Fase 2 — Complementar: G1, G2, G3, G5-a), o único trabalho
  de engenharia ainda aberto sob a issue-mãe #72.** As quatro pendências
  derivadas dos comentários pós-merge da #75 foram implementadas em
  `anonymization/dsweep-complementar-80`:
  - **G5(a):** `anonymize()` agora expõe contadores de modificação por fase em
    `g_prime.graph["metadata"]` — `edges_modified_phase2_intragroup` (Fase 2,
    via `_modify_structure(return_counts=True)`, opt-in) e
    `edges_added_reconnection` (reconexão, contado em `_reconnect_inter_edges` e
    gravado no atributo do grafo). Sem mudança na assinatura de retorno
    (pré-requisito de G5-b na #77). +8 testes.
  - **G3:** validação isolada da fórmula `k(k−1)` em `_reconnect_inter_edges`
    (k∈{2,3}). **Achado:** o exemplo literal da #80 (LSs de 1 nó → k(k−1)=2)
    está **incorreto** — é degenerate (extremos na posição 0 colapsam para 1
    aresta). A fórmula k(k−1) vale para extremos em **posições canônicas
    distintas**; mesma posição → clique de C(k,2)=k(k−1)/2. Divergência
    registrada sob **D-08** no `decision_log.md` (correção de núcleo ≠ ajuste de
    teste); docstring de `_reconnect_inter_edges` atualizada (fecha o item
    "derivação interpretativa pendente" de `algorithm_notes §3.2.2`). +5 testes.
  - **G1:** `test_local_structures_connected_d_gt_1` mede e registra o % de LSs
    desconexas na ego-rede 3437 (LCC, backend auto) para d∈{2,5}; não força
    conectividade. Reproduz D-08: d=2 199/266 vazias + 86,6% desconexas
    (degenerate); d=5 56,2% desconexas. Pulado se `data/raw` ausente. +2 testes.
  - **G2:** caso adversarial K₄/P₄/K₁,₃ em `_modify_structure` — assertiva (a)
    mutuamente isomorfos, (b) arestas adicionadas ≤ k·|E(K₄)|=18, (c) sem
    self-loop/multi-aresta. +4 testes.
  Suíte **525 passed** (+19), ruff limpo.

**Próximo passo planejado:**
- **Etapa W1b (#174):** redigir as seções 1–2 do relatório em
  `academic/relatorio_qualificacao.md` — introdução/posicionamento (abre com
  DL-06: "anonimizar não é o suficiente") e independência do EpiCNet. Fontes:
  `scope.md` §4/§5/§8, `decision_log.md`. Pré-requisito: merge do PR da W1a
  (matriz de rastreabilidade).
- **Formalização das sub-issues S10-W1a..f no GitHub:** a cargo do autor
  (criação via agente bloqueada pelo classifier nesta sessão).
- **Issue #175 (artigo, S10-W2):** bloqueada pela #174 — não iniciar antes do
  relatório consolidado.
- **Issue #148 (entropia não uniforme, sem milestone):** congelada; exige decisão
  D-xx (esquema de pesos) antes de implementar — não iniciar sem o humano.
  Código congelado na fase S10-W.

**Bloqueios ativos:**
- **PR da W1a (`docs/relatorio-skeleton-w1a`) aguardando CI + revisão humana.**
  Claude Code não faz merge. W1b não inicia antes do merge.
- **Sub-issues S10-W1a..f ainda não formalizadas no GitHub** (criação via
  agente bloqueada pelo classifier; a cargo do autor). Rastreio provisório em
  `docs/relatorio_rastreabilidade.md`.
- #176 (infraestrutura `academic/`) e #179 (DL-06) **MERGED** em 2026-06-09 —
  bloqueios anteriores resolvidos.
- #30 (PR #149) e a auditoria bibliográfica (PR #150) mergeadas em `main`;
  #30 fechada (`COMPLETED`). A entropia (baseline uniforme) está em `main`.
- Ciclo S9 totalmente encerrado (#122–#129, #139 em `main`; #29 fechada; milestone
  S9 `closed`). Milestones S8 e S9 concluídos.

**Decisões pendentes de validação humana:**
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

### 2026-06-09 — Etapa W1a da #174: esqueleto do relatório + matriz de rastreabilidade

- **Concluído:** Primeira etapa do desdobramento S10-W1a..f (validado na #174).
  Bloqueios verificados via `gh`: #176 e #179 `MERGED`, nenhum PR aberto.
  Criados: **(1)** `academic/relatorio_qualificacao.md` (esqueleto privado,
  gitignorado) — 8 seções da estrutura mínima + apêndices candidatos, cada uma
  com checklist de conteúdo, fontes, decisões citáveis, destinos `W-NN` e
  figuras; terminologia de aferição como regra global; DL-06 abrindo a
  introdução; **(2)** `docs/relatorio_rastreabilidade.md` (público) — matriz
  seção → fontes → `W-NN` → figuras, inventário de figuras citáveis e estado
  por etapa. Sub-issues **não** criadas (bloqueio do classifier de permissão;
  escopo da sessão era só a 1ª etapa). Só docs. Branch
  `docs/relatorio-skeleton-w1a` (`Refs #174`).
- **Próximo:** Revisão humana + merge do PR da W1a; depois **W1b** (seções 1–2).
  Autor formaliza as sub-issues S10-W1a..f se desejar.
- **Bloqueios:** PR da W1a aguardando CI + revisão.
- **Decisões pendentes:** D-08 (d=2 mantido, anotado degenerate) — confirmar.

### 2026-06-08 — Issue #141 (S10-V1): popular W-01..W-06 + resolver W-01

- **Concluído:** Primeira issue de verificação (S10-V) do milestone S10, em **2 PRs
  empilhados**. **PR #167** (registro): removido o piloto `W-00` e populados os seis
  itens `W-01..W-06` em `artifact_writing_checklist.md` (7 campos cada); W-02/W-03
  `em verificação` (ponteiro #139/D-16), W-04/W-05/W-06 `aberto` — fiel à DoD.
  **PR #168** (empilhado, resolução de W-01): verificado que o Facebook omite
  `s_max`/`isomorphism_mode` mas o runner aplica defaults (`run.py:610/614`)
  idênticos aos do Enron → config efetiva idêntica; registrado como **DL-05** no
  `decision_log.md`; W-01 movido para *Itens resolvidos*; `Closes #141`. Decisões
  humanas: corte em 2 Prs (registro + resolução de W-01); W-02/W-03 mantidos
  `em verificação` (fiéis à DoD apesar de #139 já mergeada). Só docs.
- **Próximo:** Revisão humana + merge de #167 e #168 (o #168 re-aponta para `main`
  ao mergear o #167). Resolução de W-04/W-05/W-06 migra para issues S10-W.
- **Bloqueios:** Nenhum.
- **Decisões pendentes:** Nenhuma nova (DL-05 fecha W-01).

### 2026-06-08 — Issue #161 (S10 / A06): mapa estrutural + sanitização

- **Concluído:** Sexta sub-issue do milestone **S10** (#140), em duas fases.
  *Sanitização* (correções de registro aplicadas diretamente): `scope.md`
  (statuses defasados de issues fechadas — d-sweep #77/#88, entropia #30/D-17,
  legenda `[D]` e rodapé) e `achados_divergencias.md` §5 (`D-10/DL-03` →
  `D-17/DL-04` + `results_enron.md`). *Escopo primário:* criado
  `docs/mapa_estrutural.md` (mapa de rastreabilidade A01–A06 → produto documental,
  localização, status, uso futuro). Itens não-correção (enquadramento instrumental
  da #99/#140; `W-01..W-06`) **encaminhados**, não aplicados. Lista consolidada da
  sanitização registrada na #161. Só docs. Branch `docs/mapa-estrutural`
  (`Closes #161`).
- **Próximo:** Revisão humana + merge. Depois **#141** (popular `W-01..W-06`,
  remover/substituir `W-00`). Encaminhar a decisão de enquadramento instrumental
  (decision_log / #141) com validação humana.
- **Bloqueios:** Nenhum.
- **Decisões pendentes:** D-08 (d=2 mantido, anotado degenerate). Enquadramento
  instrumental (#99/#140) a consolidar em `decision_log.md` com validação humana.

### 2026-06-08 — Issue #158 (S10 / A05): fechar DoD da #140 e habilitar #141

- **Concluído:** Última sub-issue de infraestrutura do milestone **S10**. A premissa
  literal da #158 (consolidar #154–#157 numa branch e abrir PR consolidador) estava
  **obsoleta**: as quatro já foram mergeadas em `main` por PRs separados — #154
  (PR #159), #155 (PR #160), #156 (PR #162), #157 (PR #163), todos **MERGED**
  (verificado via `gh pr list` + `git log origin/main`). DoD da #140 verificada item
  a item no `artifact_writing_checklist.md` em `main`: esqueleto (#154), papéis
  documentais (#155), apontadores (#156), template validado pelo `W-00` (#157). PR
  desta issue (`docs/s10-x1-umbrella-close`) leva a entrada de progresso como
  conteúdo e fecha **#140** (guarda-chuva) + **#158** (`Closes`). Comentário de
  habilitação deixado na **#141**. Só docs; sem alteração em `src/` ou testes.
- **Próximo:** Revisão humana + merge → fechar #140 e #158. Depois **#141** (popular
  `W-01..W-06`, removendo/substituindo o `W-00` EXEMPLO). Housekeeping: #74 e (se
  aberta) #72.
- **Bloqueios:** Nenhum — infraestrutura #154–#157 em `main`; PR aguarda CI + revisão.
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-08 — Issue #157 (S10 / A04): dry-run do template W-NN

- **Concluído:** Quarta sub-issue do milestone **S10** (#140). Verificado via `gh`
  que a dependência #154 (PR #159) está **MERGED** antes de começar. Inserido **1
  item-piloto `W-00` (EXEMPLO removível)** na seção "Itens ativos" do
  `docs/artifact_writing_checklist.md`, ilustrando um ponto de assimetria
  Facebook×Enron (não-comparabilidade de magnitude de `rr_subgrafo` → usar painel
  normalizado). Origem citada apenas como referência: **#128** e **#139** (fechadas),
  achado **C2**, decisão **D-11** — nenhuma reaberta. **Veredito:** os 7 campos do
  template acomodaram o ponto sem campo faltante → template suficiente, **nenhum
  ajuste em #154**. Item marcado EXEMPLO removível + nota de remoção pela #141.
  **Não** populados W-01..W-06 (é da #141). Só docs. Branch `docs/checklist-dryrun`
  (`Closes #157`).
- **Próximo:** Revisão humana + merge → fechar #157. Depois #141 (popular
  W-01..W-06, removendo/substituindo o `W-00` EXEMPLO). Housekeeping: #74 e (se
  aberta) #72.
- **Bloqueios:** Nenhum — dependência #154/#159 em `main`; PR aguarda CI + revisão.
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-07 — Issue #156 (S10 / A03): apontadores de localização do checklist

- **Concluído:** Terceira sub-issue do milestone **S10** (#140). Verificado via
  `git log origin/main` que as dependências #154 (PR #159) e #155 (PR #160) estão
  **MERGED** antes de começar. Inseridos **apontadores de 1 linha** (links
  relativos) para `docs/artifact_writing_checklist.md` em cinco arquivos, **sem
  reescrever** conteúdo retrospectivo: `README.md` (novo bloco S10 no índice §4),
  `docs/scope.md` (blockquote de cabeçalho), `docs/progress.md` (esta entrada),
  `docs/achados_divergencias.md` (frase de cabeçalho: retrospectivo → fila
  prospectiva) e `docs/decision_log.md` (frase de cabeçalho: registro de decisões,
  não fila). DoD satisfeita. Só docs. Branch `docs/checklist-pointers`
  (`Closes #156`).
- **Próximo:** Revisão humana + merge → fechar #156. Depois #141 (popular
  W-01..W-06 no checklist). Housekeeping: #74 e (se aberta) #72.
- **Bloqueios:** Nenhum — dependências #154/#155 em `main`; PR aguarda CI + revisão.
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-07 — Issue #155 (S10 / A02): diferenciação dos 3 papéis documentais

- **Concluído:** Segunda sub-issue do milestone **S10** (#140). Verificado via `gh`
  que a dependência #154 (PR #159) está **MERGED** e #154 fechada antes de começar.
  Adicionada a seção **"Papéis documentais e fronteiras"** ao
  `docs/artifact_writing_checklist.md`: 1 frase por papel + ponteiros de ida (links
  relativos) — `achados_divergencias.md` (retrospectivo, fechado), `decision_log.md`
  (decisões tomadas, não fila), e o próprio checklist (fila prospectiva). Regra de
  fronteira ("onde registrar" → artefato novo) explicitada. **Nenhuma reescrita**
  nos docs retrospectivos (apontadores ficam na #156). Só docs. Branch
  `docs/checklist-doc-roles`, PR #160 (`Closes #155`).
- **Próximo:** Revisão humana + merge do PR #160 → fechar #155. Depois #156
  (apontadores de volta) e #141 (popular W-01..W-06). Housekeeping: #74 e (se
  aberta) #72.
- **Bloqueios:** Nenhum — dependência #154/#159 em `main`; PR #160 aguarda CI +
  revisão humana.
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-07 — Issue #154 (S10 / A01): esqueleto de artifact_writing_checklist.md

- **Concluído:** Abertura do milestone **S10** (consolidação documental, #140).
  Criado `docs/artifact_writing_checklist.md` apenas como **infraestrutura** do
  checklist de verificação pré-escrita: cabeçalho/propósito (documento
  *prospectivo*, DoD da S10, não substitui `achados_divergencias.md`/
  `decision_log.md`/`limitations.md`), seção "Estrutura de cada item" (campos do
  item `W-NN`: ID, Origem, Tipo, Descrição, Critério de fechamento, Destino no
  texto, Status), convenção de numeração `W-NN` sequencial e não reaproveitada, e
  seções "Itens ativos"/"Itens resolvidos" vazias. Itens W-NN **não** populados
  (fica na #141); nenhum conteúdo movido dos docs retrospectivos. Só docs. Branch
  `docs/writing-checklist`, PR #159 (`Closes #154`).
- **Próximo:** Revisão humana + merge do PR #159 → fechar #154. Depois #141
  (popular W-01..W-06 no esqueleto). Housekeeping herdado: #74 e (se aberta) #72.
- **Bloqueios:** Nenhum — #154 independe de PRs anteriores; PR #159 aguarda CI +
  revisão humana.
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-06 — Limpeza cosmética pós-merge da #30

- **Concluído:** Após o merge de **PR #149** (entropia, *Closes #30*) e **PR #150**
  (auditoria bibliográfica), removidas as pontas soltas "branch `attack/entropy`
  aguardando merge" dos docs vivos: B3 (`achados_divergencias.md` matriz + detalhe)
  e D-17 (`decision_log.md`) passam a citar "em `main` via PR #149"; "Próximo passo"
  e "Bloqueios ativos" do Estado atual atualizados (#30 mergeada e fechada
  `COMPLETED`; sem bloqueios). Entradas de Histórico preservadas (snapshots). Só docs.
- **Próximo:** Continuação #148 (não iniciar sem D-xx). Housekeeping: #74 e (se
  aberta) #72.
- **Bloqueios:** Nenhum.
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-06 — Sanitização de fim de issue (#30): auditoria de amparo bibliográfico

- **Concluído:** Auditoria de literatura (itens 1 e 3): toda técnica formalmente
  nomeada × amparo, e bibliografia × uso. Achados no novo **Grupo C** de
  `achados_divergencias.md` — **C1** (VF2/WL sem referência → [Cordella et al. 2004]
  + [Shervashidze et al. 2011] adicionados ao README §13 e citados no ponto de uso
  em 6 docs) e **C2** (corpo do README citava 4/12 refs → citações inline para as 8
  restantes; §13 com 14 entradas, todas citadas). KL/KS mantidos sem referência
  primária (biblioteca/manual). README atualizado (§13 + citações inline em
  §2/§3/§4/§5/§8). Resíduo menor: Díaz/Serjantov acrescentados à lista §10 de
  `algorithm_notes`. Migrado também **B3** (ataque por entropia) para
  *implementado* (#30/D-17, baseline uniforme; branch `attack/entropy` aguardando
  merge). Só docs; sem alteração em `src/` ou testes.
- **Próximo:** Revisão humana dos docs; merge do PR de entropia (#30) — Claude Code
  não faz merge. Não iniciar #148 sem decisão D-xx. Housekeeping: fechar #74 e (se
  aberta) #72.
- **Bloqueios:** Nenhum novo (auditoria é só-docs). PR `attack/entropy` (#30) segue
  aguardando CI + revisão humana.
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-06 — Issue #30 (S6 / D-17): métrica de entropia — baseline uniforme

- **Concluído:** Implementada a codificação da issue #30 (os pontos documental,
  processual e metodológico já estavam tratados em D-17). **Baseline uniforme:**
  `src/metrics/entropy.py` (lar primário — `entropy_metrics(groups, tau)` →
  `entropy_mean`, `degree_of_anonymity` de Díaz et al., `reidentification_rate_entropy`,
  `tau`; reusa os grupos de equivalência, não refaz experimentos); `src/attacks/entropy.py`
  como apontador de leitura adversarial (reexporta a métrica — D-17 classifica como
  métrica, não ataque autônomo); gancho no runner (bloco `entropy` no JSONL, `τ` de
  `metrics.entropy_tau`); `config_example.yml` + `tables.py` (colunas novas). Testes:
  20 novos (15 métrica + 2 apontador + 3 propagação) + ajustes de schema; **suíte 615
  passed, ruff limpo**. **Decisão do humano:** caminho **não uniforme** (D-E2(b))
  deixado para depois e formalizado como **issue #148 (sem milestone)**, com DoD que
  exige decisão D-xx (esquema de pesos) antes de implementar. D-17 ganhou seção
  "Status final" + cross-ref #148. Branch `attack/entropy` (`Closes #30`).
- **Próximo:** Revisão humana do PR → merge → fechar #30. Não iniciar #148 sem a
  decisão D-xx. Housekeeping herdado: fechar #74 e (se aberta) #72.
- **Bloqueios:** PR `attack/entropy` aguarda CI + revisão humana.
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-06 — Fechamento administrativo do milestone S9 (DoD #29 via opção A)

- **Concluído:** Auditoria final dos DoDs de todas as 9 sub-issues do S9
  (#122–#129, #139) contra o `main` — todos os itens substantivos atendidos e
  verificáveis; CI verde nos 3 check-runs (`Lint+Test 3.11/3.12`, `pymetis`).
  Único resíduo identificado: a DoD da issue-mãe **#29** continuava com os 4
  checkboxes desmarcados (a edição do corpo havia sido bloqueada pelo classifier
  no #129). **Opção A aplicada:** comentário de conferência postado na #29
  marcando os 4 itens com `[x]` e rastreabilidade (loader OR/D-11/#124,
  config/#126, execução grau+subgrafo hop=1/D-16/#127/#139, gráficos
  comparativos/#128) + resíduo não-bloqueante (`multiple_egonets`). Em seguida:
  **#29 fechada** (`state_reason: completed`) e **milestone S9 marcado `closed`**
  (9/9 issues fechadas). Sub-issues #122–#129 e #139 confirmadas fechadas.
- **Próximo:** Definir escopo do ciclo S10 + issue âncora. Itens herdados de
  housekeeping: fechar #74 e (se aberta) #72.
- **Bloqueios:** Nenhum — milestone S9 totalmente encerrado.
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-06 — Issue #129 (S9-7): fechamento do ciclo S9 — cross-review + DoD da #29

- **Concluído:** Fechamento do milestone **S9** (Loader Email-Enron). Verifiquei
  via `gh` que **todos os PRs do ciclo S9 estão `MERGED`** (incl. #143 e o
  follow-up #144, `2026-06-06T11:16:36Z`) — `progress.md` os listava como
  pendentes; corrigido. **(1) Cross-review de fidelidade**
  código↔config↔logs↔`results_enron.md`: `he2009_enron_secondary.yml` bate com
  `summary.json` (12 runs, `any_failure: false`, pymetis 12/12) e o JSONL
  (spot-check k=2/seed=42 → rr_subgrafo=0,122893, rr_grau=0,003235,
  clust_var=0,015644; `subgraph_timeout_count=0` nas 12 runs). **Sem divergências
  silenciosas.** **(2) DoD da #29** conferida 4/4 (loader OR/#124, config/#126,
  execução grau+subgrafo hop=1/#127/#139, gráficos comparativos/#128); edição dos
  checkboxes no corpo da #29 **bloqueada pelo classifier** → veredito aqui e no
  PR, marcação fica para o humano. **(3) D-11** com seção "Status final" no
  `decision_log.md` (implementado e em produção; AND rejeitada/não executada;
  encerrada). **(4) B2** atualizado em `achados_divergencias.md` (validade externa
  parcialmente fechada pelo Enron; resíduo = `multiple_egonets`). Somente docs.
  Branch `loader/enron-close` (`Closes #129`).
- **Próximo:** Revisão humana + merge do PR → fechar #129. Ação humana: marcar
  DoD da #29 e avaliar encerramento da issue-mãe #29; fechar #74 e (se aberta) #72.
- **Bloqueios:** Nenhum — todo o ciclo S9 em `main`; PR `loader/enron-close`
  aguarda CI + revisão humana.
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-06 — Issue #128 follow-up: painel normalizado + notas de revisão (C1/C2/B), DL-04

- **Concluído:** Resolvi os pontos da revisão pós-merge da #128 (PR #143 já em
  `main`). **D1/DL-04:** novo `src/visualization/comparison.py` (+14 testes) gera o
  painel comparativo **normalizado** FB×Enron — (A) `rr_subgrafo·k` (fração da cota
  1/k, com cruzamentos: FB acima da cota em k∈{2,5,10}, Enron cruza em k=20, curvas
  se cruzam ~k≈14) e (B) decaimento relativo (forma da curva). Snapshot versionado
  em `docs/assets/comparison_fb_enron.{png,csv}` (exceção documentada ao gitignore,
  regenerável). Embed/explicação em `results_enron.md`; **DL-04** no `decision_log.md`.
  **C1:** nota de que `rr_subgrafo ≤ 1/k` só vale sob k-anon da estrutura atacada
  (`d≥2`), não em `d=1` (B1) → violação esperada em k=20, não bug
  (`results_enron.md` + `data_dictionary.md`). **C2:** ameaça à validade interna
  KL×pymetis (baixa) em `results_enron.md` + `limitations.md` §3/§4. **B/D4:** tabela
  bruta em 6 casas + nota de precisão plena no agregado. Suíte **595 passed**, ruff
  limpo. Branch `docs/results-enron-followup`.
- **Próximo:** Revisão humana do PR de follow-up → merge. **#128 segue aberta** até
  o merge (condição do humano). Depois #129 (fechamento S9).
- **Bloqueios:** PR `docs/results-enron-followup` aguarda CI + revisão humana.
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-05 — Issue #128 (S9-6): comparativo Facebook × Enron + results_enron.md

- **Concluído:** Comparativo Facebook×Enron e documentação dos resultados
  secundários (tier desejável, issue-mãe #29), agora com a curva **grau ×
  subgrafo** do Enron (D-16). Verifiquei os bloqueios via `gh` antes de começar:
  #142/#139, #138/#127 e #122–#126 todos `MERGED`/em `main`. **(1)** Novo gerador
  `experiments/make_enron_table.py` (espelha `make_baseline_table.py`) produz
  `docs/results_enron.md` completo a partir do JSONL do Enron — header, síntese
  metodológica, comparativo, tabela bruta (k,semente), agregação por k,
  interpretação e bloco de reprodutibilidade; carrega o log Facebook baseline
  quando presente (fallback embutido de `results_baseline.md`). **(2)**
  `docs/results_enron.md`: `rr_subgrafo` 0,124→0,057 (monótono), `rr_grau`
  ~0,002–0,003 (~40× menor), KS-D 0,038→0,130, clust 0,017→0,093, cobertura
  ≥0,9960, 12/12 `SUCCESS_PARTIAL`. **(3)** Comparativo justifica que as
  magnitudes não são diretamente comparáveis (escala 532 vs 33.696; densidade;
  OR/D-11; KL vs pymetis) → sobrepor num só gráfico é enganoso; gráficos por
  dataset via tooling existente (`privacy_utility_enron.*`). Tendências robustas:
  subgrafo≫grau, monotonicidade, utilidade melhor preservada em escala. **(4)**
  `docs/data_dictionary.md` §1.1 "Datasets" (Facebook [M] / Enron [D]: SNAP, OR,
  LCC n/m). **(5)** Ao gerar tabelas/plots, corrigi contaminação do `rglob`
  recursivo pelo backup só-grau da #127 (24→12 runs) realocando o backup
  gitignored p/ fora do dir varrido. Suíte **581 passed**, ruff limpo. Branch
  `loader/enron-results`.
- **Próximo:** Revisão humana do PR → fechar #128 (**não antes da análise do PR,
  a pedido do humano**). Depois #129 (fechamento S9).
- **Bloqueios:** PR `loader/enron-results` aguarda CI + revisão humana (todas as
  dependências S9 já em `main`).
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-05 — Issue #139 (S9-8): subgrafo via bucketing de WL-hash — full viável no Enron (D-16)

- **Concluído:** Resolvida por engenharia a inviabilidade de D-15 (~70 dias). **(1)**
  Caminho rápido `subgraph_candidate_counts` + `_AnonNeighbourhoodIndex` em
  `src/attacks/subgraph.py`: WL-hash das n vizinhanças 1-hop do `g_anon`
  pré-computado **uma vez** em baldes; cada alvo resolvido por lookup — O(n)+O(n)
  no lugar de O(n²). **(2)** Salvaguarda de exatidão pelo critério objetivo: WL
  puro = VF2 brute-force **100%** (contagens E vereditos) na bateria de grafos
  pequenos → adota-se WL puro; refinamento híbrido VF2 disponível p/ baldes
  pequenos, **hubs nunca refinados** (blow-up). WL é invariante necessário ⇒
  nenhum isomorfo perdido; só sobrecontagem por colisão, descartada. **(3)**
  Verificação ampla no Enron LCC k=2/seed=42: 70 nós estratificados, **0
  divergências** (ALL MATCH); 33.696 alvos em 35,9 s (~15.000× vs. brute). **(4)**
  Runner usa o caminho rápido; `subgraph_timeout_count=0` → gate D-13 trivial.
  **(5)** Config `attacks.subgraph.enabled: true` (hop=1) reabilitada. **(6)**
  Execução FULL: **12 runs, todas SUCCESS_PARTIAL, 0 falhas/timeouts**, pymetis;
  `reidentification_rate_subgraph` cai com k (k=2≈0,124 → k=20≈0,057), ~40× o
  grau (B1). Logs limpos (12 linhas + summary); só-grau da #127 em
  `_pre139_degree_only_backup/`. **(7)** `decision_log.md`: D-16 + extensão de
  D-15 (amostragem agora OBSOLETA). `results_enron.md` não tocado (#128). Suíte
  **581 passed**, ruff limpo. Branch `attack/subgraph-wl-bucketing`.
- **Próximo:** Merge do PR → fechar #139. Depois #128 (results_enron.md AGORA com
  curva grau × subgrafo) e #129 (fechamento S9).
- **Bloqueios:** PR `attack/subgraph-wl-bucketing` aguarda CI + revisão humana
  (#127 já em `main` via PR #138).
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-04 — Issue #127 (S9-5): execução secundária Enron — só-grau (subgrafo inviável, D-15)

- **Concluído:** Antes de atacar o cerne, fiz **análise prévia de custo empírica**
  (probe real sobre o Enron LCC: n=33.696, m=180.811, pymetis) e **proposta de
  continuidade**. Achado: o ataque por **subgrafo full** é **O(n²)** (~15 s/nó-alvo
  × 33.696 ≈ 5,85 dias/run → **~70 dias** nas 12 runs); o timeout de 120 s (D-12)
  **não** limita — nenhum nó é patológico (15 s < 120 s), `subgraph_timeout_count`
  seria 0 (válido por D-13) e ainda assim 70 dias; custo agregado, não por nó.
  Reduzir o timeout abaixo de 15 s estouraria todos → inválido por D-13. Decisão
  **D-15** registrada (índice + entrada no `decision_log.md`): #127 roda **só o
  ataque por grau** (~404 s/run, viável); `attacks.subgraph.enabled: false` na
  config canônica com justificativa inline; subgrafo adiado para **S10**
  (amostragem de nós-ALVO — estimador não-enviesado da taxa com IC, candidatos =
  população inteira; ~532 alvos ≈ 1,1 dia; descritivo de issue preparado para o
  humano criar fora do milestone S9). **Execução:** `python -m experiments.run
  --config experiments/configs/he2009_enron_secondary.yml` → **12 runs**
  (k∈{2,5,10,20} × sementes [42,1337,2718]), **todas SUCCESS_PARTIAL** (coverage
  0,996–0,9999, déficit estrutural D-06), **0 erros**, pymetis;
  `reidentification_rate_degree` ∈ [0,0018; 0,0034]; logs em
  `experiments/logs/he2009_enron_secondary/` (12 linhas + `summary.json`,
  `any_failure: false`; gitignored). Continuidade: para a run só-grau (~1,2 h) o
  resume não foi necessário; ele entra junto da S10 (multi-dia). Branch
  `loader/enron-run` (`Closes #127`).
- **Próximo:** Merge do PR → fechar #127. Depois #128 (comparativo/`results_enron.md`
  a partir dos logs só-grau) e #129 (fechamento S9). Criar a issue S10 (descritivo
  pronto).
- **Bloqueios:** PR `loader/enron-run` aguarda CI + revisão humana (#122–#126 em `main`).
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-03 — Issue #126 (S9-4): config YAML he2009_enron_secondary — subgrafo hop=1

- **Concluído:** Config do experimento **secundário** Email-Enron (tier
  desejável, issue-mãe #29 / S9-4) — `experiments/configs/he2009_enron_secondary.yml`,
  espelhando `he2009_facebook_baseline.yml` com valores específicos do Enron.
  `dataset.name: enron`, `data_path: data/raw/enron/`, `component: lcc`,
  `min_nodes: 200` (= 10 × k_max); o ramo `enron` de `load_dataset` (#125) lê só
  `data_path` + `component`/`min_nodes` genéricos. Sementes `[42, 1337, 2718]`
  lidas do YAML (≥3). `anonymization`: `k: [2,5,10,20]`, `d: 1`, `sigma: 0.5`,
  `s_max: 4`, `isomorphism_mode: add_or_delete` (chaves do S8, lidas em
  `run.py:588/592`). `attacks.degree.enabled: true`; `attacks.subgraph` com
  `enabled: true`, `hop: 1` explícito e `timeout: 120`s por nó (margem VF2 na
  escala maior do Enron; DoD #29/#126 — **não** habilitar hop>1). Cabeçalho
  documenta o enquadramento secundário [D], a projeção OR (D-11) e cita #29. YAML
  validado por `yaml.safe_load` (UTF-8); `ruff check .` limpo. Sem alteração em
  `src/`/testes. Branch `loader/enron-config`, PR #134 (`Closes #126`).
- **Próximo:** Merge do PR #134 → fechar #126. Depois: executar o experimento
  secundário Enron com esta config (≥3 sementes), gráficos/tabelas e validação de
  k-anonimato no Enron.
- **Bloqueios:** PR #134 aguarda CI + revisão humana (S9-3/#125 já em `main`,
  PR #133 mergeado `2026-06-03T17:45:09Z`).
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-03 — Issue #125 (S9-3): integração runner — ramo enron em load_dataset()

- **Concluído:** Integração do loader Email-Enron ao runner (S9-3, parte de #29),
  no único ponto de contato com o núcleo do pipeline. **(1)** `experiments/run.py`:
  `load_dataset()` ganha o ramo `elif name == "enron"` → `load_enron(Path(
  dataset_cfg["data_path"]))`, com log de `n`/`m` do grafo bruto (espelha o
  Facebook); `import load_enron` adicionado. Mensagem de erro de dataset
  desconhecido agora lista `facebook_ego_nets, enron`. Pós-processamento
  `component`/`min_nodes` **não duplicado** (genérico, roda após `load_dataset`).
  Sem toque em ataques/métricas/viz. **(2)**
  `tests/experiments/test_run_enron_dataset.py` (6 testes, espelha
  `test_run_config_propagation.py`): dispatch `enron` → `load_enron` com OR
  (D-11); LCC/`min_nodes` pelo novo ramo; edge list ausente → `FileNotFoundError`;
  erro lista ambos os datasets; `main()` end-to-end com config Enron (edge list
  real em `tmp_path`) → SUCCESS + `summary.json`/JSONL. Suíte **568 passed**;
  `ruff check`/`format` limpos. Branch `loader/enron-runner`, PR #133.
- **Próximo:** Merge do PR #133 → fechar #125. Depois: config YAML do Enron
  (`he2009_enron_*.yml`) e execução do experimento secundário.
- **Bloqueios:** PR #133 aguarda CI + revisão humana (S9-2/#124 já em `main`).
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-03 — Issue #124 (S9-2): loader load_enron — conversão direcionado→não-dir. (OR)

- **Concluído:** Segundo código de loader do ciclo **S9** (Email-Enron, tier
  desejável, issue-mãe #29), espelhando o contrato de `load_facebook_egonet`.
  **(1)** `src/loaders/enron.py`: `load_enron(data_dir) -> nx.Graph` lê
  `data_dir/email-Enron.txt` (edgelist SNAP; comentários `#` ignorados pelo
  `read_edgelist`); lê em `nx.DiGraph` e aplica `.to_undirected()` —
  **simetrização OR (D-11)**: `{u, v}` existe se `u→v` **ou** `v→u`; pares
  recíprocos e de mão única colapsam para 1 aresta; rótulos inteiros;
  `FileNotFoundError` com caminho claro (padrão Facebook). `lcc`/`min_nodes`
  ficam com o runner (fora de escopo). Docstring NumPy-style citando D-11.
  **(2)** `tests/loaders/test_enron.py` (fixtures sintéticas, sem rede, 6
  testes): não-direcionado, rótulos inteiros, OR par recíproco, OR par de mão
  única, comentários ignorados, arquivo ausente. `ruff check .` limpo; loaders
  **24 passed**. Branch `loader/enron-load`, PR #132 (`Closes #124`).
- **Próximo:** Merge do PR #132 → fechar #124. Depois: integração no runner
  (`load_dataset` despacha `name: enron` → `load_enron`) e config YAML do Enron.
- **Bloqueios:** PR #132 aguarda CI + revisão humana (S9-0/#122 e S9-1/#123 já
  em `main`).
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-03 — Issue #123 (S9-1): download idempotente do Email-Enron (SNAP) — SHA-256

- **Concluído:** Primeiro código de loader do ciclo **S9** (Email-Enron, tier
  desejável, issue-mãe #29), espelhando `src/loaders/download.py` (Facebook).
  **(1)** `src/loaders/download_enron.py`: `download_enron(dest=RAW_DIR)` baixa
  `email-Enron.txt.gz` de `https://snap.stanford.edu/data/email-Enron.txt.gz` e
  descompacta para `data/raw/enron/email-Enron.txt`; **idempotente** (sai cedo se
  o arquivo já existe); loga **SHA-256** e tamanho do `.gz` (rastreabilidade);
  reusa `_ProgressHook`/`_sha256` importados de `download.py` (sem duplicação);
  rejeita payload não-gzip cedo (`BadGzipFile`). Diferença vs. Facebook: arquivo
  único `.gz` via `gzip`, não tar. **(2)** `tests/loaders/test_download_enron.py`
  (rede mockada, 7 testes). **(3)** `data/raw/enron/.gitkeep` versionado + regra
  de negação no `.gitignore` (dados brutos seguem ignorados). A projeção OR (D-11)
  fica para o loader, não para este downloader. `ruff check .` limpo; loaders
  **18 passed**. Branch `loader/enron-download`, PR #131.
- **Próximo:** Merge do PR #131 → fechar #123. Depois: parser/loader Email-Enron
  (`email-Enron.txt` → grafo NetworkX, projeção OR/D-11) e config YAML.
- **Bloqueios:** PR #131 aguarda CI + revisão humana (S9-0/#122 já em `main`).
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-03 — Issue #122 (S9-0): âncora do Loader Email-Enron — decisão OR + enquadramento

- **Concluído:** Abertura do ciclo **S9** (Loader Email-Enron, tier desejável,
  issue-mãe #29), espelhando o padrão de âncora do S7/S8 — **somente docs/setup,
  sem código de loader** (conforme "Não fazer" da #122). **(1) Decisão D-11** em
  `docs/decision_log.md` (índice + entrada completa): simetrização **OR** (aresta
  `A — B` se houver e-mail em qualquer direção) como projeção direcionado→não-dir.
  do Email-Enron; justificativa (convenção SNAP/comparabilidade; retenção de
  estrutura, paralelo ao LCC do Facebook; cenário de risco conservador); impacto
  estrutural (maior densidade/conectividade; núcleo de anonimização/ataques/métricas
  intocado — projeção é responsabilidade do loader); **alternativa rejeitada**
  (reciprocidade AND, candidata a análise de sensibilidade futura); nota de
  terminologia de aferição. **(2) `docs/scope.md` §3:** Facebook segue `[M]`
  (principal); **Enron promovido a linha própria `[D]`** (secundário do tier
  desejável, com a regra OR e cross-ref D-11/#29/#122); header e rodapé atualizados
  para 03/06/2026 / S9. **(3) Branch base `loader/enron`** criada de `main`. Sem
  alteração em `src/`/testes; `ruff check .` limpo. Branch `loader/enron`.
- **Próximo:** Merge do PR `loader/enron` → fechar #122. Depois, sub-issues do S9:
  loader em `src/loaders/` (download versionado + projeção OR por D-11) e config YAML.
- **Bloqueios:** Nenhum (S8 concluído; PR #121 em `main`).
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-03 — Issue #111 (S8-8): fechamento do milestone S8 — revisão cruzada + §4 executada

- **Concluído:** Última issue do milestone S8. **(1) Revisão cruzada de
  consistência** das mudanças S8 verificada no código: `run.py` lê
  `anonymization.s_max` (alias `fsm_max_size`, `run.py:577`) e
  `anonymization.isomorphism_mode` (`run.py:581`, validado contra
  `_ISOMORPHISM_MODES`), propaga ambos e grava no JSONL+`summary.json`;
  `anonymize()` expõe os params (`he2009.py:243-244`); `config_example.yml` expõe
  `k`/`d`/`sigma`/`s_max`/`isomorphism_mode` (69–94). Nenhuma afirmação de
  configurabilidade sem respaldo no código; sem contradição KL/pymetis ou
  `d=1`/d-sweep (os "hardcoded" restantes nos docs são "Executado" histórico com
  "Atualização" de fechamento). **(2) `achados_divergencias.md`:** matriz da §1
  migrada — A1⚠️→✅ (#107), B1⚠️→✅ (#108), B2/B7⚠️→✅ (#109), B6🔧→✅ (#105,
  no código); B5 já ✅ (#106) → **17/17 achados ✅**. Notas "deixada para
  S8-8/#111" (A1/B1/B2/B6/B7) → "concluída em S8-8/#111". §4 marcada
  **✅ EXECUTADA** com nota de que B5/B6 foram resolvidos por **correção de
  código**, além da intenção original. Header e §5 (DL-03) atualizados.
  **(3) Encerramento de S8** registrado em `decision_log.md` (nota de milestone) e
  no `progress.md`. Somente docs; sem alteração em `src/`/testes; `ruff check .`
  limpo. Branch `docs/s8-closure-cross-review-111`.
- **Próximo:** Merge do PR → fechar #111 e **concluir o milestone S8**. Depois:
  fechamento manual da #74; se ainda aberta, fechar a umbrella #72.
- **Bloqueios:** PR `docs/s8-closure-cross-review-111` aguarda revisão humana
  (todas as dependências serial #104–#110 já em `main`).
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-03 — Issue #110 (S8-7): auditoria de fidelidade dos achados ✅ (A2–A9, B3, B4, B8)

- **Concluído:** Auditoria leve (não-edição salvo regressão) verificando que os 11
  achados marcados ✅ em `achados_divergencias.md` seguem coerentes com código/docs
  após as Fases 1 e 2. **Veredito: 11/11 fiéis — nenhuma regressão.** Reverificação
  item a item: **A2** `fsm_max_size: int = 4` default (`he2009.py:103/243/461`;
  texto histórico anotado com B5/#104); **A3** D-07 + §3.1/§4.1; **A4** D-08, teste
  `test_local_structures_connected_d_gt_1`, §6; **A5** `validation.py:101` "does not
  import anything from he2009.py" (auditor independente); **A6** D-06,
  `incomplete_group` como violador (`validation.py:165/206`); **A7** desempate
  lexicográfico ativo (`he2009.py:668/798`), D-03, §3.3; **A8**
  `TestReconnectKTimesKMinusOne`, §3.2.2, docstring; **A9** §2.2 "Interpretativa"
  (linhas 230–233); **B3** sem ataque por entropia em `src/attacks/`; **B4**
  Nettleton não implementado (sem arquivo em `src/`; scope §3/§4); **B8** DL-01 +
  `satisfied_fraction`/`deficit_fully_structural`. **Observação (não-regressão):** a
  evidência de B4 cita "`src/anonymization/` (placeholder)" mas não há arquivo
  placeholder — a ausência confirma o "não implementado"; wording pré-existente, não
  introduzido pelas Fases 1/2. Somente docs (`progress.md`); sem alteração em `src/`.
  Branch `docs/audit-checkmarks-110`.
- **Próximo:** Merge do PR → fechar #110; depois S8-8 (#111, migração formal dos
  status na tabela-resumo), que consome este relatório de fidelidade.
- **Bloqueios:** PR `docs/audit-checkmarks-110` aguarda revisão humana.
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-03 — Issue #109 (S8-6 / B2+B7): reafirmar dataset único + timeouts retroativos

- **Concluído:** Tornados explícitos no texto público dois pontos de validade
  antes dispersos. **B2:** `results_baseline.md` ganhou a seção "Validade externa
  — dataset único (achado B2)" (única ego-rede 3437; Enron contingente e
  `multiple_egonets` não rodaram; generalização aberta; ortogonal às ressalvas de
  B1/`d` e A1/motor); `results_dsweep.md` §5.7 passou a nomear explicitamente
  Enron e `multiple_egonets` como planejados-mas-não-executados. **B7:** o
  esclarecimento já estava completo em `results_dsweep.md` §5.5/§5.7 (zeros
  genuínos — H3 descartada por inspeção, não reexecução; campos
  `subgraph_timeout_count`/`subgraph_candidate_counts` retroativos, DL-02) — texto
  existente satisfaz o critério. Em `achados_divergencias.md`, status detalhado de
  B2 e B7 migrado ⚠️→✅; tabela-resumo (linhas 78/83) deixada para S8-8/#111.
  Evidência verificada (`scope.md` §3; `limitations.md` §1.1;
  `config_example.yml:46`; DL-02/D-08). Somente docs; `ruff check .` limpo.
  Branch `docs/reaffirm-dataset-timeouts-109`, PR #119.
- **Próximo:** Merge do PR #119 → fechar #109; depois S8-8 (#111, migração formal
  dos status na tabela-resumo, incl. B2 linha 78 e B7 linha 83).
- **Bloqueios:** PR #119 aguarda revisão humana (S8-4/#107 e S8-5/#108 já em `main`).
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-03 — Issue #108 (S8-5 / B1): frase-síntese d=1 = k-anon de grau, d-sweep = estrutural

- **Concluído:** Fechado o achado B1 (maior consequência interpretativa). A
  frase-síntese — `d=1` (baseline) afere **k-anonimato de grau**; a propriedade
  *structure-aware* só é exercida no d-sweep `d∈{5,10}`; o contraste é a
  evidência empírica de privacidade estrutural — inserida em dois pontos de
  destaque: `README.md` §5 (callout "Leitura-chave" no topo dos Resultados,
  antes da tabela do baseline) e `results_baseline.md` (nova seção "Leitura-chave
  — `d=1` afere k-anonimato de grau", junto à apresentação do baseline). Para não
  contradizer S8-4/A1 (mesmo arquivo), as duas ressalvas foram declaradas
  **ortogonais** (parâmetro `d` vs. motor KL/pymetis). Em `achados_divergencias.md`,
  status detalhado de B1 ⚠️→✅ e item 5 das pendências riscado; tabela-resumo
  (linha 77) deixada para S8-8/#111. Referências citadas verificadas (D-02;
  `algorithm_notes.md` §5.3/§6.5/§9.1). Somente docs; `ruff check .` limpo.
  Branch `docs/synthesis-d1-degree-vs-structural-108`, PR #118.
- **Próximo:** Merge do PR #118 → fechar #108; depois S8-8 (#111, migração formal
  dos status na tabela-resumo, incl. B1 linha 77). Merges pendentes de #106/#112.
- **Bloqueios:** PR #118 aguarda revisão humana (S8-4/#107 já em `main`).
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-03 — Issue #107 (S8-4 / A1): results_baseline.md declara baseline d=1 em KL

- **Concluído:** Fechado o achado A1 — `results_baseline.md` declara
  explicitamente que o número-título do baseline `d=1` ("k-anonimato atingido")
  veio do fallback Kernighan-Lin, **não** pymetis (ausente local e na CI à época;
  auditoria #74). Nova seção "Motor de particionamento — baseline d=1 rodou em
  KL": (1) motor efetivo (KL via `backend="auto"`; JSONL anterior à gravação de
  `partition_backend`/#84); (2) inocuidade para `d=1` (partições triviais → o
  desbalanceamento do KL p/ `ck>2`, D-04, é irrelevante; validação do marco 29/05
  válida); (3) contraste com o d-sweep (#88: pymetis em 48/48). Linha do motor
  adicionada ao bloco de metadados. Em `achados_divergencias.md`, A1 (status
  detalhado + item 3 das pendências) migrado ⚠️→✅ e line numbers da evidência
  atualizados; migração da tabela-resumo deixada para S8-8/#111. Somente docs;
  `ruff check .` limpo. Branch `docs/baseline-declare-kl-fallback-107`, PR #117.
- **Próximo:** Merge do PR #117 → fechar #107; depois S8-5 (frase-síntese B1,
  também edita `results_baseline.md`). Merges pendentes de #106/#112; depois
  S8-8 (#111, migração formal dos status).
- **Bloqueios:** PR #117 aguarda revisão humana (#104/#105/#106 já em `main`).
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-03 — Issue #106 (S8-3 / B5): config_example.yml expõe d/sigma/s_max/isomorphism_mode

- **Concluído:** Alinhado o `config_example.yml` de referência à interface real
  do runner, fechando a parte `config_example` do achado B5. O bloco
  `anonymization` passou a expor `d` (default `1`; nota B1 d=1 grau vs d>1
  estrutural; conceitual 10 = D-02), `sigma` (`0.5`, D-01), `s_max` (`4`,
  D-01/A2; alias `fsm_max_size`, B5/#104) e `isomorphism_mode`
  (`add_or_delete` | `add_only`, B6/#105) — todos com comentários e defaults
  corretos. `k_values` corrigido para `k` (chave realmente lida pelo runner;
  evita configurabilidade fantasma). Cada chave verificada como lida em
  `experiments/run.py::main`. Decisão DL-03 em `decision_log.md`;
  `algorithm_notes.md` §5.1–5.3 atualizadas; B5 em `achados_divergencias.md`
  migrado 🔧→✅ (resíduo: `partition_backend`). Sem alteração em `src/`; YAML
  validado; `tests/experiments` 65 passed. Branch
  `docs/config-example-expose-params-106`.
- **Próximo:** Merge do PR → fechar #106; depois S8-8 (#111, migração formal dos
  status na tabela-resumo). Merge de `test/config-propagation-112` → fechar #112.
- **Bloqueios:** PR a abrir aguardará revisão humana (#104/#105 já em `main`).
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-02 — Issue #112 (S8-2b): testes de propagação das chaves + regressão

- **Concluído:** Cobertura de teste da mudança de comportamento de #104
  (`s_max`/`fsm_max_size`) e #105 (`isomorphism_mode`), agora lidas do YAML.
  `tests/anonymization/test_he2009_modify.py` +18 testes (3 classes) no caminho
  `anonymize()`: `isomorphism_mode` → `_modify_structure(add_only=...)` via spy
  `wraps` + efeito "nenhuma aresta removida" sob `add_only`; default
  `add_or_delete`; valor inválido → `ValueError`; `fsm_max_size` →
  `_group_isomorphic` (spy) e default 4; grouping idêntico `s_max∈{4,5}` em
  `cycle_graph(20)`/d=5 (G2/D-01); regressão default==explicit e determinismo
  d=1. Novo `tests/experiments/test_run_config_propagation.py` (12 testes) no
  caminho config→runner: chaves gravadas no JSONL e `summary.json`; default na
  ausência; alias `fsm_max_size`; `isomorphism_mode` inválido aborta `main()`;
  valores efetivos chegando a `_modify_structure`/`_group_isomorphic` (helper
  `_SpyWrapper`); regressão baseline d=1. Sem alteração em `src/`. Addenda B5/B6
  de `achados_divergencias.md` atualizados. Suíte **549 passed**, ruff + format
  limpos. Branch `test/config-propagation-112`.
- **Próximo:** Merge do PR → fechar #112; depois S8-3 (#106, `config_example.yml`).
- **Bloqueios:** PR a abrir aguardará revisão humana (#104/#105 já mergeadas).
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-02 — Issue #105 (S8-2 / B6): expor isomorphism_mode lido do YAML

- **Concluído:** Corrigida a defasagem B6 — a variante de isomorfização da
  Fase 2 estava `add_only=False` hardcoded em `anonymize()` e no runner, e a
  chave YAML `isomorphism_mode` nunca era lida. `anonymize()` (he2009.py)
  passou a aceitar `isomorphism_mode: str = "add_or_delete"`, validar o valor
  contra `_ISOMORPHISM_MODES = {"add_or_delete", "add_only"}` (ValueError em
  valor inválido), convertê-lo em `add_only` e repassá-lo a
  `_modify_structure`. `experiments/run.py` lê `anonymization.isomorphism_mode`
  (default `add_or_delete`), valida antes do laço de execução, propaga por
  `run_one()` a `anonymize()` e ao caminho inline
  (`_modify_structure(add_only=...)`), e grava o valor efetivo em cada entrada
  JSONL (`"isomorphism_mode"`) e no `summary.json`. Default preserva o
  comportamento histórico. Docs: docstring de `anonymize()`,
  `algorithm_notes.md` §3.2.1/§3.4/§5.1/§5.2/§5.3 (chave YAML ativa) e addendum
  B6 (🔧→✅) em `achados_divergencias.md` (itens 1–2 das pendências documentais
  marcados como resolvidos). Stub `_always_error` de `test_runner.py` aceita o
  novo kwarg (cobertura de propagação é S8-2b/#112). Suíte **525 passed**,
  ruff + format limpos. Branch `anonymization/expose-isomorphism-mode-105`.
- **Próximo:** Merge do PR → fechar #105; depois S8-2b (#112) e S8-3 (#106).
- **Bloqueios:** PR a abrir aguardará revisão humana.
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-02 — Issue #104 (S8-1 / B5): expor s_max/fsm_max_size lido do YAML

- **Concluído:** Corrigida a defasagem B5 (achado A2) — `s_max`/`fsm_max_size`
  estava hardcoded (nem `anonymize()` nem o runner passavam o parâmetro →
  `_group_within_bucket` usava default 4). `anonymize()` e `_group_isomorphic()`
  passaram a aceitar `fsm_max_size: int = 4` e propagá-lo até
  `_group_within_bucket`; `experiments/run.py` lê `anonymization.s_max` (alias
  `fsm_max_size`) do YAML, propaga por `run_one()` e grava o valor efetivo em
  cada entrada JSONL (`"fsm_max_size"`) e no `summary.json` (sem alterar a
  assinatura de retorno de `anonymize()`; default 4 preserva o comportamento).
  Docs: `algorithm_notes.md` §5.1 (chave YAML lida)/§5.2 (nota B5)/§5.3,
  `limitations.md` §2.1, addenda em `achados_divergencias.md` (A2, B5; migração
  formal do status 🔧→✅ na tabela-resumo deixada para S8-8/#111). Ajuste mínimo
  no stub `_always_error` de `test_runner.py` para aceitar o novo kwarg (nova
  cobertura é S8-2b/#112). Suíte **525 passed**, ruff + format limpos. Branch
  `anonymization/expose-smax-104`, PR #113.
- **Próximo:** Merge do PR #113 → fechar #104. Recomendado mergear S8-1 antes de
  S8-2 (#105, `isomorphism_mode`); depois S8-2b (#112) e S8-3 (#106).
- **Bloqueios:** PR #113 aguarda revisão humana.
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-02 — Issue #80 (D-08 / Fase 2 — Complementar): G1, G2, G3, G5-a

- **Concluído:** Implementadas as quatro pendências da #80 (último trabalho de
  engenharia aberto sob a issue-mãe #72). **G5(a):** contadores por fase
  (`edges_modified_phase2_intragroup`, `edges_added_reconnection`) expostos em
  `g_prime.graph["metadata"]` por `anonymize()`, via `_modify_structure(
  return_counts=True)` (opt-in) e contagem em `_reconnect_inter_edges`, sem
  alterar a assinatura de retorno. **G3:** validação isolada de `k(k−1)` na
  reconexão (k∈{2,3}) — achado de que o exemplo de 1 nó da #80 é degenerate
  (colapsa para 1 aresta); a fórmula vale para extremos em posições canônicas
  distintas (mesma posição → C(k,2)); registrado sob D-08 no `decision_log.md` e
  na docstring. **G1:** `test_local_structures_connected_d_gt_1` mede/registra o
  % de LSs desconexas na 3437 (d∈{2,5}; reproduz D-08: d=2 degenerate, d=5 ~56%),
  pulado sem `data/raw`. **G2:** caso K₄/P₄/K₁,₃ em `_modify_structure` com as
  assertivas (a)(b)(c). +19 testes; suíte **525 passed**, ruff limpo. Branch
  `anonymization/dsweep-complementar-80`.
- **Próximo:** Merge do PR → fechar #80; depois fechar a umbrella #72 (toda a
  engenharia do d-sweep concluída). Fechamento manual da #74.
- **Bloqueios:** PR `anonymization/dsweep-complementar-80` aguarda revisão humana.
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-02 — Issue #93 (D-08 / Fase 6): diagnóstico dos zeros de reid_sub (k=20, d∈{5,10})

- **Concluído:** Sanitização diagnóstica dos zeros de
  `reidentification_rate_subgraph`. **Passo 1** (sem reexecução): log do d-sweep
  (48 runs) sem nenhum `verdict=ERROR` nem campo `error` → como o `timeout` era
  120 s e qualquer estouro produziria `ERROR` no código vigente, **nenhuma
  chamada VF2 atingiu o limite** → **H3 (timeout mascarado) descartada**; zeros
  genuínos (H1/H2). **Passo 2:** `experiments/run.py` — laço do ataque por
  subgrafo captura `TimeoutError` por nó (conta em `subgraph_timeout_count`,
  trata o nó como não-reidentificado, eliminando `verdict=ERROR` espúrio e
  alinhando ao comentário do YAML); novos campos `subgraph_timeout_count` e
  `subgraph_candidate_counts {mean,std,max}` no JSONL; `subgraph_candidate_count`
  adicionado a `src/attacks/subgraph.py` (e exportado), com `subgraph_attack`
  reescrito como `count == 1` (comportamento idêntico). Schema DL-01 no docstring
  atualizado. **DL-02** + nota de encerramento de **D-08** em `decision_log.md`.
  **Passo 3:** opcional (Passo 1 conclusivo) — `he2009_facebook_dsweep_k20_diag.yml`
  criado como artefato de reprodução, não executado (custo ≈3 h/run). **Passo 4:**
  `results_dsweep.md` §5.5 (ressalva → resolvida) e §5.7 (ameaça de timeout
  afastada para este log). +16 testes; suíte **506 passed**, ruff limpo. Branch
  `diag/subgraph-zeros-k20`.
- **Próximo:** Merge do PR `diag/subgraph-zeros-k20` → fechar #93 (comentário com
  verdict do Passo 1). Fechamento manual da #74.
- **Bloqueios:** PR `diag/subgraph-zeros-k20` aguarda revisão humana.
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-02 — Issue #78 (D-08 / Fase 5): docs do d-sweep + ameaças à validade

- **Concluído:** Fechados os itens remanescentes da DoD da #78. As seções 1
  (visualizações d-aware) e 2 (`results_dsweep.md`) já tinham sido entregues por
  #92/#94 e #88; esta sessão cobriu a seção 3 e a seção 4. (a) `results_dsweep.md`:
  nova §5.7 "Ameaças à validade" (interna — interação `s_max × d`, pymetis vs KL,
  k-way não garante LS conexa, custo VF2/timeouts; construção — contraste `d=1` vs
  `d>1` como evidência de privacidade estrutural; externa — única ego-rede 3437).
  (b) `limitations.md §1.3`: rebaixada de limitação aberta para **parcialmente
  resolvida** (resíduo = generalização a outras ego-redes/datasets), com a entrada
  correspondente na tabela de ameaças reclassificada para validade externa.
  (c) `algorithm_notes.md §9`: nova §9.4 com os achados do d-sweep (déficit sempre
  estrutural; EGS ≈ k·d; vetores de ataque opostos em k; combos degenerados
  D-08/D-10; ressalva de timeouts) e ponteiro para o relatório. Sem alteração em
  `src/` — viz e runner d-aware já em `main`. Suíte **490 passed**, ruff limpo.
  Branch `docs/dsweep-analysis-78`.
- **Próximo:** Merge do PR `docs/dsweep-analysis-78` → fechar #78. Fechamento
  manual da #74.
- **Bloqueios:** PR `docs/dsweep-analysis-78` aguarda revisão humana.
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-02 — Relatório consolidado final do d-sweep (#88): docs/results_dsweep.md

- **Concluído:** Fechado o último item pendente da DoD da issue #88. Com a viz
  d-aware (#92/#94) mergeada em `main`, regenerei os artefatos do log do d-sweep
  (48 registros, `experiments/logs/he2009_facebook_dsweep/`) via as ferramentas
  já existentes: tabelas CSV d-aware (`results/tables/facebook_{degree,subgraph}.csv`,
  agora com coluna `d`) e duas figuras (`privacy_utility_dsweep_series` e
  `..._facets`), ambas não versionadas conforme `.claude/rules/experiments.md`.
  Escrevi `docs/results_dsweep.md` (relatório final): metadados, cobertura 16/16
  células, tabelas `média ± std` por `(k,d)`, análise (déficit estrutural em
  48/48 com `valid=false`+`deficit_fully_structural=true`; tendências opostas
  grau×subgrafo em k; efeito de `d`; combos degenerados D-08 d=2 e D-10 d=10/k=20;
  ressalva de que `reid_sub=0` em k alto pode refletir timeouts VF2, não
  segurança — o JSONL não registra contagem de timeouts), comandos de reprodução
  e referências cruzadas. `dsweep_previa_garantia_dados.md` rebaixada a snapshot
  histórico com ponteiro para o relatório final. Branch `docs/results-dsweep`.
- **Próximo:** Merge do PR `docs/results-dsweep` → fechar #88. Fechamento manual da #74.
- **Bloqueios:** PR `docs/results-dsweep` aguarda revisão humana.
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-02 — Visualização ciente de `d` (#92): plots e tabelas d-aware

- **Concluído:** `src/visualization/tables.py` e `privacy_utility.py` estendidos
  para tratar a dimensão `d` do d-sweep. `tables.py`: `"d"` adicionado a
  `CSV_COLUMNS` (após `"k"`, mudança intencional de spec), `record_to_row`
  extrai `record.get("d", 1)`, sort `(k, d, seed)`. `privacy_utility.py`:
  `aggregate_by_k_d` nova (chaves `(k, d)`); `aggregate_by_k` preservada com
  comportamento idêntico (pool por `k`, retrocompatível); `plot_privacy_utility_dsweep`
  nova com dois layouts (`series` — cor por `d`, estilo de linha por ataque/métrica;
  `facets` — grade 2×4); CLI com `--dsweep`/`--layout` + auto-detecção (mais de um
  `d` distinto → modo d-aware). Fallback `d=1` em todos os caminhos para logs
  pré-DL-01. Testes: +6 (tables) e +~30 (privacy_utility), incluindo fixtures de
  grade 4k×4d×3s e checagem de retrocompat. Verificado end-to-end no log real
  (48 registros): 16 células `(k,d)` nas CSVs, plots `series` e `facets` gerados.
  Suíte completa **490 passed**; ruff limpo.
- **Próximo:** Merge do PR `viz/dsweep-d-aware` (#92); gerar artefatos finais e o
  relatório consolidado do d-sweep. Fechamento manual da #74.
- **Bloqueios:** PR `viz/dsweep-d-aware` aguarda revisão humana.
- **Decisões pendentes:** D-08 — d=2 mantido (anotado degenerate, D-10); confirmar.

### 2026-06-02 — d-sweep (#88): execução completa 48/48 + runner d-list

- **Concluído:** O runner (`experiments/run.py`) passou a aceitar
  `anonymization.d` como **lista** (além de escalar), varrendo o produto
  cartesiano `k × d × seed` com uma entrada JSONL por combinação; `summary.json`
  grava `d_values` e vereditos por `(k,d,seed)`. 4 testes novos em
  `tests/experiments/test_runner.py` (produto cartesiano, presença de cada `d`,
  registro no summary, compat. com `d` escalar). O experimento
  `he2009_facebook_dsweep` rodou **48/48 com pymetis em todos os runs**, sem
  erros (≈31 h de parede, dominadas pelo VF2 do ataque por subgrafo em k alto);
  o processo sobreviveu a uma desconexão do terminal do VSCode (processo
  independente, gravação JSONL incremental). Vereditos: 33 SUCCESS_PARTIAL /
  15 FAILURE_LOW_COVERAGE. Consolidação legível em
  `docs/dsweep_previa_garantia_dados.md` (nasceu como prévia de garantia de dados
  a 43/48, atualizada para o estado final).
- **Próximo:** criar issue `viz/dsweep-d-aware` (plots/tabelas ignoram `d`); só
  então gerar artefatos finais e o relatório consolidado.
- **Bloqueios:** Nenhum.
- **Decisões pendentes:** D-08 — d=2 foi mantido (anotado degenerate, D-10) em vez
  de excluído; confirmar se é a escolha definitiva.

### 2026-05-31 — pymetis: explicitação do backend + cobertura na CI (#84, #85, #86)

- **Concluído:** Partindo do achado de que o pymetis **já funciona** no ambiente
  conda local (439→443 passed, 0 skipped), três gaps de visibilidade/cobertura
  foram fechados, cada um em sua branch/PR, **todos mergeados** em `main`
  (`3410e58`), na ordem #84 → #85 → #86, com CI verde:
  - **#84** (gap #2): `partition_backend` gravado em cada entrada JSONL e
    `partition_backends` no `summary.json`; `_partition_neighborhoods` ganhou
    `return_meta`. Resultados passam a ser auto-documentados quanto ao backend.
  - **#85** (gap #1): job `test-pymetis` (micromamba + `environment.yml`,
    conda-forge) exercita o motor primário na CI — os 4 testes antes pulados
    agora rodam. `lint-and-test` (pip) mantém cobertura do fallback KL.
  - **#86** (gap #3): correção do erro factual do README §13 (introduzido por
    #82/#83 — o `.venv` do §3.2 não inclui pymetis em nenhum SO); nota em
    `limitations.md` §2.2; flag opt-in `anonymization.allow_kl_fallback`
    (padrão `true`) + helper `pymetis_available()`; atualização da nota de CI em
    `pipeline.md`; remoção do resíduo rastreado `.vscode/.gitkeep_remove`.
- **Próximo:** Fechamento manual da issue #74; confirmar D-08 / d=2 no d-sweep (#77).
- **Bloqueios:** Nenhum.
- **Decisões pendentes:** D-08 (Opção B registrada; aguarda validação humana).

### 2026-05-30 — Auditoria #74 (Fase 1) + análise de sessão travada

- **Concluído:** Auditoria de prontidão d>1 (issue #74, somente leitura, sem
  alteração em `src/`). Estado de PR/`main`: nenhum PR aberto, working tree limpo
  em `main` @ `74b188c`, `experiment/d-sweep` sincronizada (PR #79 mergeado em
  `a057519`). Backend de particionamento: pymetis ausente local e na CI (não está
  em `requirements*.txt`; só extra `partition-c` no `pyproject.toml`) → ambos usam
  fallback `networkx-kl`; degradação de sizing para `ck>2` confirmada e já
  documentada (D-04/D-07, `algorithm_notes.md §7`). Testes de particionamento
  d=2/d=5: 18 passed sob KL. **Inventário do núcleo diverge do esperado:**
  `_group_isomorphic` (`test_he2009_grouping.py`, 28 testes) e `_modify_structure`
  (`test_he2009_modify.py`, 32 testes) têm cobertura ampla com `|LS|>1`; e2e d>1
  em `test_he2009_e2e_d.py` (TestE2eD2/D5/D10 + TestValidatorCoherence). A lacuna
  prevista para a Fase 2 (#75) já foi preenchida por #75/#76 (PR #79). Suíte: 435
  passed, 4 skipped (exigem pymetis; idêntico local↔CI). Resultado comentado na
  issue #74, **mantida aberta** conforme instrução. Diagnosticada a sessão anterior
  (`d0e51803`, ~23h): ~11 min de trabalho real + travamento de 23,7h num prompt de
  permissão de um one-liner PowerShell, sessão desacompanhada. Subprodutos: regra
  de permissão local read/test (`.claude/settings.local.json`) e nova seção no
  `CLAUDE.md` ("Inspeção de arquivos e busca de conteúdo") preferindo `Grep`/`Read`
  a one-liners de shell.
- **Próximo:** Revisão humana e fechamento manual da #74; confirmar D-08 / d=2 no d-sweep (#77).
- **Bloqueios:** Nenhum.
- **Decisões pendentes:** D-08 (Opção B registrada; aguarda validação humana).

### 2026-05-28 — Issue #76 G5(a): deficit_fully_structural e equivalence_group_size em d>1

- **Concluído:** `tests/anonymization/test_he2009_d_validator.py` criado (23 testes,
  3 classes). `TestDeficitFullyStructuralD`: pipeline d∈{2,5} → violations apenas
  `incomplete_group`; casos sintéticos confirmam `deficit_fully_structural=False` com
  `non_isomorphic` (size mismatch d=2 e d=5; path vs cycle). `TestEquivalenceGroupSizeD`:
  mean=k·d para grupos completos (d=2→4, d=5→10); mean≠k·d para tamanhos mistos
  (KL aproximação — limitação registrada). `TestDegenerateComboD10K20`: cycle_graph(20)
  d=10 k=20 → `deficit_fully_structural=True`, `n_violators=20` — comportamento correto,
  não bug. Decisões D-09 (pré-filtro VF2: limitação) e D-10 (combo degenerado: incluir
  no YAML com aviso) registradas em `docs/decision_log.md`. 439 passed, ruff limpo.
  Branch `experiment/d-sweep`.
- **Próximo:** Abrir PR para a branch `experiment/d-sweep`, cobrindo issues #75 e #76.
- **Bloqueios:** Nenhum.
- **Decisões pendentes:** Confirmar D-08: d=2 excluído ou anotado como degenerate (D-10
  registrado; aguarda validação humana no contexto do YAML do d-sweep).

### 2026-05-28 — Issue #75 e2e d=10: validação da Opção A para d=10

- **Concluído:** `TestE2eD10` adicionada a `test_he2009_e2e_d.py` com 6 testes
  caixa-preta (`anonymize(cycle_graph(20), k=2, d=10, seed∈{0,7})`). `TestValidatorCoherence`
  estendida de `d∈{2,5}` para `d∈{2,5,10}` (4 testes × 3 valores = 12 casos).
  Confirma Opção A (G2): `s_max=4` fixo produz pipeline coerente mesmo com `d=10 > fsm_max_size=4`.
  412 passed, ruff limpo. Commit `47bd872` em `experiment/d-sweep`.
- **Próximo:** G5(a) — início de #76 (validador e métricas em d>1).
- **Bloqueios:** Nenhum.
- **Decisões pendentes:** Confirmar D-08: d=2 excluído ou anotado como degenerate.

### 2026-05-28 — Issue #75 G2: decisão s_max vs d (D-01, Checkbox #2)

- **Concluído:** Investigação empírica do FSM quando `d > fsm_max_size=4`.
  `cycle_graph(20)`, d=5: 4 padrões frequentes (tamanhos 1–4); agrupamento idêntico
  com `fsm_max_size∈{4,5}`. Decisão Opção A registrada em `docs/decision_log.md`
  (nota G2 sob D-01): manter `s_max=4` fixo para todos os valores de d do d-sweep.
  Sem alteração em `src/`. 406 passed, ruff limpo.
- **Próximo:** e2e com d=10 para confirmar Opção A; depois G5(a) / início de #76.
- **Bloqueios:** Nenhum.
- **Decisões pendentes:** Confirmar D-08: d=2 excluído ou anotado como degenerate.

### 2026-05-28 — Issue #75 G1: teste e2e anonymize() d=2 e d=5

- **Concluído:** `tests/anonymization/test_he2009_e2e_d.py` criado com 20 testes
  em 3 classes. `TestE2eD2` e `TestE2eD5` cobrem caixa-preta de `anonymize()`;
  `TestValidatorCoherence` (parametrizado d∈{2,5}) verifica coerência do validador
  (`valid` ou `deficit_fully_structural=True`) e ausência de violações `non_isomorphic`
  (condição 4.3, VF2). Grafo `cycle_graph(20)`, sementes 0 e 7. 406 passed, ruff limpo.
  Commit `ba1c10b` em `experiment/d-sweep`.
- **Próximo:** G2 (Decisão s_max vs d — verificar FSM quando d > fsm_max_size=4;
  registrar em decision_log.md sob D-01).
- **Bloqueios:** Nenhum.
- **Decisões pendentes:** Confirmar D-08: d=2 excluído ou anotado como degenerate no d-sweep.

### 2026-05-28 — Issue #75 G3: verificação de conectividade de LSs + decisão D-08

- **Concluído:** Branch `experiment/d-sweep` criada. G3 (Checkbox #3 de #75):
  verificação empírica de conectividade das LSs geradas por pymetis para d ∈ {2, 5}
  na ego-rede 3437. Achados críticos: (a) ego-rede 3437 é desconexo (2 componentes:
  532 + 2 nós); (b) d=2 degenerate — pymetis produz 199/267 partições vazias e nós
  concentrados em grupos 7–8; (c) d=5 razoável em tamanho (5–6) mas 55% desconexas.
  Decisão D-08 registrada em `docs/decision_log.md`: Opção B (documentar como
  aproximação); forçamento de conectividade = tier desejável futuro.
- **Próximo:** G1 (testes e2e `anonymize(g, k=2, d={2,5})` em grafo pequeno ~20 nós).
- **Bloqueios:** Nenhum.
- **Decisões pendentes:** Confirmar se d=2 deve ser excluído ou apenas anotado no d-sweep.

### 2026-05-25 — Encerramento da issue #26

- **Concluído:** PR #68 (issue #64 / #26-B) confirmado mergeado. Issue #26 fechada com
  comentário de encerramento documentando todos os critérios atendidos. Sub-issues #63 e #64
  cobriram os 5 critérios da definição de pronto: ①②③ pela #64 (diagramas, comandos, outputs),
  ④⑤ pela #63 (limitations.md, revisão e cross-referências dos docs).
- **Próximo:** Semana 5 — issues #27 (reprodutibilidade end-to-end) e #28 (README final + revisão docs).
- **Bloqueios:** Nenhum.
- **Decisões pendentes:** Nenhuma.

### 2026-05-25 — Documentação técnica do pipeline (issue #64)

- **Concluído:** PR #67 (issue #25) confirmado mergeado. Branch `docs/pipeline-technical` criada.
  `docs/pipeline.md` criado com: diagrama Mermaid de fluxo de execução (Config YAML → anonimização
  → ataques → métricas → JSONL → visualizações); diagrama Mermaid de arquitetura de módulos
  (todos os `src/` com dependências); comandos reproduzíveis verificados localmente para cada etapa;
  tabela de parâmetros YAML; tabela de outputs com localização; referências cruzadas para
  `algorithm_notes.md`, `metrics_definitions.md` e `limitations.md`.
  386 passed. Ruff limpo. PR #68 aberto.
- **Próximo:** Merge do PR #68. Avaliar issues #27 (cold start) e #28 (revisão global docs).
- **Bloqueios:** PR #68 aguarda revisão humana.
- **Decisões pendentes:** Revisão humana do PR #68.

### 2026-05-25 — Tabelas CSV de resultados (issue #25)

- **Concluído:** PR #66 (issue #24) confirmado mergeado. Branch `viz/tables` criada.
  `src/visualization/tables.py` implementado com três funções públicas:
  `load_jsonl_records`, `record_to_row`, `generate_tables` + CLI
  `python -m src.visualization.tables --logs <dir> --out results/tables --dataset facebook`.
  Uma tabela CSV por `(dataset, ataque)`, colunas: `k, seed, reid_rate, eq_group_mean, ks_D, ks_p, clustering_var`.
  Saída em `results/tables/` (não versionada). 43 testes em `tests/visualization/test_tables.py`,
  todos passando. Suite completa: 382 passed, 4 skipped. Ruff limpo. PR #67 aberto.
- **Próximo:** Merge do PR #67. Avaliar tarefas remanescentes da Semana 4 (polimento/documentação).
- **Bloqueios:** PR #67 aguarda revisão humana.
- **Decisões pendentes:** Revisão humana do PR #67.

### 2026-05-25 — Gráfico privacy-vs-utility (issue #24)

- **Concluído:** PR #62 (issue #23) confirmado mergeado. Branch `viz/privacy-utility` criada.
  `src/visualization/privacy_utility.py` implementado com três funções públicas:
  `load_jsonl_records`, `aggregate_by_k`, `plot_privacy_utility` + CLI
  `python -m src.visualization.privacy_utility --logs <dir>`.
  Figura de 2 painéis: Privacidade (taxa de reidentificação % vs k, curva por ataque) e
  Utilidade (clustering_variation + KS-D vs k), barras de erro = ±1 std entre sementes.
  PDF + PNG salvos em `results/plots/` (não versionados).
  35 testes em `tests/visualization/test_privacy_utility.py`, todos passando.
  Suite completa: 339 passed, 4 skipped. Ruff limpo. PR #66 aberto.
- **Próximo:** Merge do PR #66. Avaliar tarefas remanescentes da Semana 4.
- **Bloqueios:** PR #66 aguarda revisão humana.
- **Decisões pendentes:** Revisão humana do PR #66.

### 2026-05-25 — Encerramento de S3: PR #65 (#26-A / issue #63)

- **Concluído:** Issue #63 (#26-A) fechada. `docs/limitations.md` produzido;
  cross-referências entre `algorithm_notes.md` e `metrics_definitions.md`
  estabelecidas. PR #65 (`docs/pipeline-academic`) em revisão final.
- **Próximo:** Fechar CI do PR #65; aplicar polimentos ②③④; merge; abrir
  issue #26-B (parâmetros do pipeline, §5.4). Em seguida, S4: issues #24
  (gráficos) e #25 (tabelas CSV).
- **Bloqueios:** CI vermelho no PR #65 (Python 3.11/3.12) — único bloqueio real. [já resolvidos]
- **Decisões pendentes:** Nenhuma.

### 2026-05-23 — Experimento baseline: he2009_facebook_baseline (issue #23)

- **Concluído:** PR #61 (issue #22 — runner) confirmado mergeado. Branch
  `experiment/facebook-baseline` criada. `experiments/configs/he2009_facebook_baseline.yml`
  com ambos os ataques habilitados (degree + subgraph hop=1, timeout=60s),
  k∈{2,5,10,20}, 3 sementes. Experimento executado via
  `python -m experiments.run` — 12 runs completas, exit code 0.
  Resultados: k=2→SUCCESS_FULL×3 (rr_grau=0.026, rr_sub=0.791);
  k=5→SUCCESS_PARTIAL×3 (rr_grau=0.008, rr_sub=0.406);
  k=10→SUCCESS_PARTIAL×3 (rr_grau=0.023, rr_sub=0.140);
  k=20→SUCCESS_PARTIAL×3 (rr_grau=0.099, rr_sub=0.000).
  `experiments/make_baseline_table.py` gerador da tabela criado.
  `docs/results_baseline.md` com tabela bruta + agregações commitado.
  PR a abrir.
- **Próximo:** Merge do PR de issue #23. Semana 4: gráficos/tabelas (issue #24).
- **Bloqueios:** PR de issue #23 aguarda revisão humana.
- **Decisões pendentes:** Revisão humana do PR de issue #23.

### 2026-05-22 — Runner de experimentos: experiments/run.py (issue #22)

- **Concluído:** `experiments/__init__.py` (torna o diretório um pacote Python),
  `experiments/run.py` (runner CLI com argparse, YAML → pipeline → JSONL),
  `experiments/configs/he2009_facebook_full.yml` (config k=[2,5,10,20], 3 sementes),
  `tests/experiments/test_runner.py` (37 testes, todos passando).
  Pipeline por (k, seed): partition → group → modify → reconnect → validate_k_anonymity
  → degree_attack em todos os nós → reidentification_rate, equivalence_group_size,
  ks_test_degree, clustering_variation → JSONL com schema DL-01 completo.
  Ruff limpo. 308 testes passando.
  PR #61 aberto.
- **Próximo:** Merge do PR #61. Executar experimento completo para produzir logs JSONL.
  Semana 4: gráficos/tabelas a partir dos logs.
- **Bloqueios:** PR #61 aguarda revisão humana.
- **Decisões pendentes:** Revisão humana do PR #61.

### 2026-05-22 — Alinhamento documental: registro dos merges e abertura da issue #22

- **Concluído:** PRs #55, #57, #58, #59, #60 mergeados em `main` pelo humano.
  `progress.md` sincronizado com o estado real do repositório. `CLAUDE.md`
  atualizado com regra de verificação de PRs antes de iniciar nova issue.
- **Próximo:** Implementar issue #22 (`experiments/run.py`) a partir de `main`.
- **Bloqueios:** Nenhum.
- **Decisões pendentes:** Nenhuma.

### 2026-05-22 — Métricas: src/metrics/ (issue #21)

- **Concluído:** `src/metrics/reidentification_rate.py` (`reidentification_rate(attack_results) -> float`), `src/metrics/equivalence_group_size.py` (`equivalence_group_size(groups) -> tuple[float, int]` — aceita `list[list[nx.Graph]]` idêntico ao `validate_k_anonymity`), `src/metrics/ks_test_degree.py` (`ks_test_degree(g_orig, g_anon) -> tuple[float, float]` via `scipy.stats.ks_2samp`), `src/metrics/clustering_variation.py` (`clustering_variation(g_orig, g_anon) -> float`). `src/metrics/__init__.py` exporta as 4 funções. 52 novos testes em `tests/metrics/` cobrindo edge cases, valores conhecidos, invariantes de tipo e intervalo. 267 passando, 4 skipped; ruff limpo. PR #60 aberto.
- **Próximo:** Aguardar merge dos PRs #60, #59, #58, #57, #55. Implementar issue #22 (runner).
- **Bloqueios:** PRs #60, #59, #58, #57, #55 aguardam revisão humana.
- **Decisões pendentes:** Revisão humana dos cinco PRs.

### 2026-05-22 — Ataque por subgrafos: subgraph_attack (issue #20)

- **Concluído:** `src/attacks/subgraph.py` criado com `subgraph_attack(g_orig, g_anon, target, hop=1, timeout=None) -> bool`. Backend VF2 via `GraphMatcher.is_isomorphic`. Helper `_k_hop_induced_subgraph` encapsula extração de vizinhança. Timeout opcional via `concurrent.futures`. `src/attacks/__init__.py` atualizado para exportar ambos os ataques. `tests/attacks/test_subgraph.py` com 17 casos cobrindo: identificação única (True), múltiplos candidatos (False), zero candidatos (False), hop=2 discrimina onde hop=1 falha (lollipops assimétricos), timeout via mock, inputs inválidos. 215 passando, 4 skipped; ruff limpo. PR #59 aberto.
- **Próximo:** Aguardar merge de PRs #59, #58. Implementar issue #21 (métricas).
- **Bloqueios:** PRs #59, #58, #57, #55 aguardam revisão humana.
- **Decisões pendentes:** Revisão humana dos quatro PRs.

### 2026-05-22 — Ataque por grau: degree_attack (issue #19)

- **Concluído:** `src/attacks/degree.py` criado com `degree_attack(g_orig, g_anon, target, tolerance=0) -> bool`. `src/attacks/__init__.py` criado. `tests/attacks/test_degree.py` com 10 casos cobrindo: identificação única (True), múltiplos candidatos (False), zero candidatos (False), tolerance != 0, target inválido (ValueError), tolerance negativa (ValueError). 198 passando, 4 skipped; ruff limpo. PR #58 aberto.
- **Próximo:** Aguardar merge de PR #58. Implementar issue #20 (subgraph_attack).
- **Bloqueios:** PR #58, #57, #55 aguardam revisão humana.
- **Decisões pendentes:** Revisão humana dos três PRs.

### 2026-05-22 — Testes DL-01: coverage_fraction, uncovered_fraction, deficit_fully_structural (issue #56)

- **Concluído:** `TestDL01Fields` adicionada a `tests/anonymization/test_validation.py` com 16 novos casos de teste cobrindo os três campos introduzidos por DL-01. Sem alterações em `src/`. 51 testes passando; ruff limpo. PR #57 aberto.
- **Próximo:** Aguardar merge de PR #57 e PR #55. Iniciar Semana 3: ataques por grau e subgrafos.
- **Bloqueios:** PR #57 e PR #55 aguardam revisão humana.
- **Decisões pendentes:** Revisão humana dos dois PRs.

### 2026-05-22 — Documentação do marco 29/05 (issue #18)

- **Concluído:** `docs/validacao_k_anonimato.md` criado com registro consolidado da validação: data, hashes de commits, tabela de configuração, tabela de resultados para k∈{2,5,10,20} × 3 sementes, análise de violações (nenhuma crítica), decisão de prosseguir para Semana 3. `CLAUDE.md` atualizado com link. PR #55 aberto.
- **Próximo:** Aguardar merge do PR #55. Iniciar Semana 3: ataques por grau e subgrafos.
- **Bloqueios:** PR #55 aguarda revisão humana.
- **Decisões pendentes:** Revisão humana do PR #55.

### 2026-05-22 — k-Sweep k∈{2,10,20}: todos os k do escopo Mínimo validados (issue #17)

- **Concluído:** Script `experiments/run_k_sweep.py` + 3 YAMLs (`he2009_facebook_k_sweep_k{2,10,20}.yml`) criados e executados. k=2: SUCCESS_FULL × 3; k=10: SUCCESS_PARTIAL × 3 (sf=0.9962); k=20: SUCCESS_PARTIAL × 3 (sf=0.9774). Resultados documentados em `docs/algorithm_notes.md` Seção 9. PR a abrir.
- **Próximo:** Abrir PR para issue #17. Aguardar merges (#53 e #17). Iniciar Semana 3: ataques por grau e subgrafos.
- **Bloqueios:** PRs #53 e k-sweep aguardam revisão humana.
- **Decisões pendentes:** Revisão humana dos dois PRs.

### 2026-05-21 — Marco 29/05: validação k-anonimato k=5, d=1 (issue #16)

- **Concluído:** Script `experiments/run_milestone_29_05.py` + YAML `experiments/configs/milestone_29_05.yml` criados e executados. Resultado APROVADO nas 3 sementes (satisfaction_fraction=0.9962, apenas incomplete_group). PR #53 aberto.
- **Próximo:** Merge do PR #53 (revisão humana). Semana 3: ataques por grau e subgrafos.
- **Bloqueios:** PR #53 aguarda revisão.
- **Decisões pendentes:** Revisão humana do PR #53.

### 2026-05-21 — Inicialização do repositório e estrutura de sessão

- **Concluído:** Repositório criado com estrutura completa (src, tests, docs, experiments, scripts, data, results), CLAUDE.md, WORKFLOW.md, CI GitHub Actions, pre-commit, environment.yml, pyproject.toml, config_example.yml. Adicionada instrução de continuidade de sessão ao CLAUDE.md e criado este arquivo.
- **Próximo:** Implementar loader das Facebook Ego-Nets (`src/loaders/facebook_ego.py`).
- **Bloqueios:** Nenhum.
- **Decisões pendentes:** Nenhuma.
