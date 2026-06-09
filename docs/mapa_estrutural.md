# Mapa Estrutural dos Artefatos Documentais — S10

> **Propósito.** Este documento é um **mapa de orientação e rastreabilidade**
> dos produtos documentais gerados pelas issues `A-NN` do milestone **S10**
> (consolidação documental — relatório + artigo). Ele reúne, num único lugar,
> *o que cada issue produziu*, *onde esse produto está no repositório* e *qual
> issue deu origem a cada conteúdo*.
>
> **Escopo coberto.** Issues `A01`–`A06` da S10 (sub-issues da guarda-chuva
> [#140](https://github.com/chrisjulio/moduloreidentificacao/issues/140)).
>
> **Aviso.** Este mapa é **orientador e rastreável — não substitui** as próprias
> issues, os PRs, nem os documentos-fonte. Ele aponta para eles; não replica seu
> conteúdo. Para o teor integral de cada item, vá à issue, ao PR ou ao arquivo
> indicado. A fonte de verdade do *estado de progresso* continua em
> [`progress.md`](progress.md); a do *escopo*, em [`scope.md`](scope.md).

---

## Como ler este mapa

Cinco noções distintas circulam por este documento e não devem ser confundidas:

| Noção | O que é |
|---|---|
| **Issue de origem** | A issue `A-NN` que motivou a criação ou alteração do artefato. É a *causa* documental, não o conteúdo. |
| **Artefato produzido** | O arquivo (ou seção de arquivo) criado/alterado pela issue. É o *produto* concreto no repositório. |
| **Conteúdo consolidado** | Conteúdo que **já existe em `main`** e pode ser lido agora. Ligado explicitamente à issue que o produziu apenas quando o conteúdo de fato existe. |
| **Documentação pendente** | Produção documental ainda **aberta ou em andamento** (issue não concluída). Marcada como tal — nunca inferida como entregue. |
| **Uso futuro na redação** | Como o artefato deve ser aproveitado na escrita do relatório/artigo. É expectativa de uso, não entrega já realizada. |

Regra de leitura: uma issue **fechada** com artefato presente em `main` é
*conteúdo consolidado*; uma issue **aberta** é *documentação pendente*, mesmo
que parte de sua infraestrutura já exista.

---

## Mapa sintético A-NN → produto documental

| ID | Issue | Status | Artefato/documento afetado | Tipo de contribuição | Localização | Uso futuro esperado |
|---|---|---|---|---|---|---|
| A01 | [#154](https://github.com/chrisjulio/moduloreidentificacao/issues/154) | ✅ fechada (PR #159) | `docs/artifact_writing_checklist.md` (criação) | Infraestrutura: esqueleto, template `W-NN`, seções vazias | [`artifact_writing_checklist.md`](artifact_writing_checklist.md) | Estrutura-base onde as pendências de escrita (`W-NN`) foram populadas e resolvidas (#141, fechada). |
| A02 | [#155](https://github.com/chrisjulio/moduloreidentificacao/issues/155) | ✅ fechada (PR #160) | `docs/artifact_writing_checklist.md` (seção) | Conceitual: diferenciação dos 3 papéis documentais | [`artifact_writing_checklist.md` §"Papéis documentais e fronteiras"](artifact_writing_checklist.md) | Regra de fronteira para decidir *onde* registrar cada achado durante a redação. |
| A03 | [#156](https://github.com/chrisjulio/moduloreidentificacao/issues/156) | ✅ fechada (PR #162) | `README.md`, `scope.md`, `progress.md`, `achados_divergencias.md`, `decision_log.md` | Apontadores de localização (links de 1 linha) | índices vivos + docs retrospectivos | Navegação rápida do leitor até o checklist a partir de qualquer doc central. |
| A04 | [#157](https://github.com/chrisjulio/moduloreidentificacao/issues/157) | ✅ fechada (PR #163) | `docs/artifact_writing_checklist.md` (piloto `W-00`) | Validação: dry-run do template `W-NN` | [`artifact_writing_checklist.md` §"Itens ativos"](artifact_writing_checklist.md) | Veredito de suficiência do template; `W-00` é EXEMPLO removível (substituído em #141). |
| A05 | [#158](https://github.com/chrisjulio/moduloreidentificacao/issues/158) | ✅ fechada (PR #164) | `docs/progress.md` + fechamento da #140 | Fechamento de ciclo: DoD da guarda-chuva [#140](https://github.com/chrisjulio/moduloreidentificacao/issues/140) (fechada); habilitação da #141 | [`progress.md`](progress.md); comentário na #141 | Marcou a infraestrutura como pronta — liberou a produção substantiva (#141, depois fechada). |
| A06 | [#161](https://github.com/chrisjulio/moduloreidentificacao/issues/161) | ✅ fechada (PR #166) | `docs/mapa_estrutural.md` (criação) + sanitização documental | Rastreabilidade + sanitização de registros | [`mapa_estrutural.md`](mapa_estrutural.md) (este doc); correções em `scope.md`/`achados_divergencias.md` | Mapa de leitura da S10; insumo de orientação para a redação (S10-W). |

Legenda: ✅ = issue fechada, conteúdo consolidado em `main`; 🔄 = produção em
andamento (não inferir como concluída).

> **Nota de atualização (2026-06-09).** Este mapa foi criado pelo PR #166 (08/06
> 23:02), **46 min antes** do fechamento da #141 (08/06 23:48). Saneamento
> pós-fechamento: as menções a #140/#141 e aos itens `W-NN` foram alinhadas ao
> estado consolidado em `main` (ambas as issues fechadas; `W-01..W-06` resolvidos,
> piloto `W-00` removido — PRs #167–#170). Atualização factual de registro, não
> reescrita retrospectiva de conteúdo.

---

## Entradas detalhadas por issue

### A01 — [#154](https://github.com/chrisjulio/moduloreidentificacao/issues/154) · ✅ fechada (PR #159)

- **Objetivo documental.** Criar a *infraestrutura* do checklist de verificação
  pré-escrita — pontos a resolver/declarar antes da redação de cada seção.
- **Produto.** `docs/artifact_writing_checklist.md`: cabeçalho/propósito
  (documento *prospectivo*, não substitui os retrospectivos), estrutura do item
  `W-NN` (7 campos), convenção de numeração sequencial não reaproveitada, seções
  "Itens ativos"/"Itens resolvidos" vazias.
- **Localização.** [`docs/artifact_writing_checklist.md`](artifact_writing_checklist.md).
- **Estado.** Produzido e em `main`. Itens reais `W-NN` populados e **todos resolvidos** pela #141 (fechada em 2026-06-08; PRs #167–#170).

### A02 — [#155](https://github.com/chrisjulio/moduloreidentificacao/issues/155) · ✅ fechada (PR #160)

- **Objetivo documental.** Tornar explícita, *no checklist*, a diferença entre os
  três documentos que parecem registrar "pontos em aberto".
- **Produto.** Seção **"Papéis documentais e fronteiras"**: `achados_divergencias.md`
  (retrospectivo, fechado), `decision_log.md` (registro de decisões tomadas, não
  fila) e o próprio checklist (fila prospectiva), com a regra de fronteira ("em
  caso de dúvida, registrar no artefato novo").
- **Localização.** [`docs/artifact_writing_checklist.md`](artifact_writing_checklist.md),
  seção "Papéis documentais e fronteiras".
- **Estado.** Produzido e em `main`. Sem reescrita dos docs retrospectivos.

### A03 — [#156](https://github.com/chrisjulio/moduloreidentificacao/issues/156) · ✅ fechada (PR #162)

- **Objetivo documental.** Apontar, dos índices vivos e dos docs retrospectivos,
  para o checklist — sem mover conteúdo.
- **Produto.** Apontadores de 1 linha (links relativos) em `README.md` (bloco S10
  no índice de docs), `scope.md` (cabeçalho), `progress.md`, `achados_divergencias.md`
  e `decision_log.md` (frases de cabeçalho).
- **Localização.** Cabeçalhos/índices dos cinco documentos acima.
- **Estado.** Produzido e em `main`. Nenhuma alteração de conteúdo retrospectivo
  além das linhas de apontamento.

### A04 — [#157](https://github.com/chrisjulio/moduloreidentificacao/issues/157) · ✅ fechada (PR #163)

- **Objetivo documental.** Validar (dry-run) que o template `W-NN` acomoda um ponto
  real de assimetria Facebook×Enron sem campo faltante.
- **Produto.** Item-piloto **`W-00` (EXEMPLO removível)** na seção "Itens ativos",
  ilustrando a não-comparabilidade de magnitude de `rr_subgrafo`; veredito: os 7
  campos acomodaram o ponto → **template suficiente, nenhum ajuste necessário**.
- **Localização.** [`docs/artifact_writing_checklist.md`](artifact_writing_checklist.md),
  seção "Itens ativos" (item `W-00`).
- **Estado.** Produzido e em `main`. `W-00` é EXEMPLO — **deve ser removido ou
  substituído** ao popular os itens reais (#141). Origem citada apenas como
  referência: #128, #139 (fechadas), achado C2, decisão D-11.

### A05 — [#158](https://github.com/chrisjulio/moduloreidentificacao/issues/158) · ✅ fechada (PR #164)

- **Objetivo documental.** Fechar a DoD da guarda-chuva #140 e habilitar a #141.
- **Produto.** Verificação item a item da DoD da #140 contra o checklist em `main`
  (A01–A04 todas mergeadas por PRs separados); entrada de progresso; comentário de
  habilitação na #141. PR #164 (`Closes #140`, `Closes #158`).
- **Localização.** [`docs/progress.md`](progress.md); comentário na #141.
- **Estado.** Produzido e em `main`. Infraestrutura do checklist completa.

### A06 — [#161](https://github.com/chrisjulio/moduloreidentificacao/issues/161) · ✅ fechada (PR #166)

- **Objetivo documental.** **(escopo primário)** criar este mapa de rastreabilidade;
  **(etapa anteposta)** executar uma *sanitização documental* dos artefatos da S10 e
  docs centrais relacionados antes do mapa, conforme o comentário de encaminhamento
  da própria #161.
- **Produto.**
  1. `docs/mapa_estrutural.md` (este documento).
  2. **Sanitização:** correção de registros defasados em `scope.md` (legenda `[D]`,
     d-sweep, entropia e rodapé — issues #72–#78/#29/#77/#88/#30 fechadas, antes
     descritas como "em andamento"/"pendentes"/"não iniciado") e em
     `achados_divergencias.md` §5 (lista de decisões estava em `D-10/DL-03`;
     atualizada para `D-17/DL-04` + `results_enron.md`). Achados que **não** são
     correção de registro foram **encaminhados**, não aplicados aqui (ver §"Lacunas
     e continuidade").
- **Localização.** [`docs/mapa_estrutural.md`](mapa_estrutural.md); diffs em
  [`scope.md`](scope.md) e [`achados_divergencias.md`](achados_divergencias.md);
  lista consolidada da sanitização registrada na própria #161.
- **Estado.** Consolidado em `main` (PR #166, mergeado em 2026-06-08 23:02).

---

## Ligações com documentos centrais

Como o mapa cobre apenas as issues `A-NN`, registra-se aqui a relação de cada
documento central com a S10:

- [`artifact_writing_checklist.md`](artifact_writing_checklist.md) — **núcleo da
  S10**: produzido por A01–A04; populado e **com `W-01..W-06` todos resolvidos** pela
  #141 (fechada; piloto `W-00` removido — PRs #167–#170).
- [`achados_divergencias.md`](achados_divergencias.md) — *retrospectivo, fechado*;
  recebeu apontador (A03) e correção de registro na §5 (A06/sanitização). Não recebe
  novas pendências de escrita.
- [`decision_log.md`](decision_log.md) — *registro de decisões*; recebeu apontador
  (A03). Destino de itens que viram decisão consolidada.
- [`scope.md`](scope.md) — *escopo*; recebeu apontador (A03) e correções de registro
  (A06/sanitização).
- [`progress.md`](progress.md) — *estado de progresso*; fonte de verdade do andamento;
  recebeu apontador (A03) e a entrada de fechamento de A05.
- [`README.md`](../README.md) — *operacional*; recebeu o bloco S10 no índice de docs
  (A03).
- [`results_enron.md`](results_enron.md) — não é produto da S10, mas foi **insumo** das
  verificações `W-NN` (#141, já resolvidas): comparativo Facebook×Enron e validade externa.

---

## Lacunas e continuidade

Este mapa é **orientador**, não um checklist operacional. Pontos que continuam
abertos devem ser resolvidos pelas issues próprias da S10, não aqui:

- **Produção substantiva da escrita (`W-01..W-06`).** Pertencia à **#141**, agora
  **fechada**: os itens reais foram populados no checklist e **todos resolvidos**, e
  o piloto `W-00` foi **removido** (PRs #167–#170). `W-01` resolvido via **DL-05**;
  `W-02..W-06` consolidados a partir de **#128** (DL-04) e **#139** (D-16/D-13) e da
  confirmação empírica de B1 nos dois datasets. Pendência encerrada; o aproveitamento
  na redação segue como tarefa das issues **S10-W**.
- **Sanitização documental — itens encaminhados (não aplicados em A06).** A etapa de
  sanitização desta issue corrigiu diretamente apenas registros defasados (links,
  IDs, status). Os demais achados foram **encaminhados**:
  - *Transição de fase / congelamento de código (06/06, herdada da #99) e
    enquadramento "instrumental"* (o módulo evidencia que anonimizar não basta →
    necessidade do gerador EpiCNet): hoje registrada apenas em comentários de issue
    (#99/#140/#141). É **decisão estratégica** → encaminhar para `decision_log.md`
    e/ou como ponto interpretativo de redação no checklist (#141), **com validação
    humana** (decisão estratégica origina-se no projeto Claude.ai, conforme
    `CLAUDE.md`).
  - A lista consolidada da sanitização (origem → destino → ação) está registrada na
    **#161** como etapa a encaminhar; se o volume crescer, justifica sub-issue
    própria da S10.
- **Verificação de escrita continuada.** Lacunas de redação ou verificação que
  surgirem devem virar itens `W-NN` no checklist (via #141) ou issues `S10` próprias
  — não entradas neste mapa.
