# Checklist de verificação para escrita — artefatos finais (S10)

> **Propósito.** Este documento acumula **pontos de verificação a resolver ou
> declarar _antes_ da redação de cada seção** do relatório de qualificação e/ou
> do artigo. Cada item (`W-NN`) é uma pendência de escrita: algo que precisa ser
> conferido, decidido ou explicitamente declarado no texto para que aquela seção
> possa ser escrita sem deixar afirmação sem amparo. Fechar todos os itens ativos
> é a **Definição de Pronto (DoD) da milestone S10**.
>
> **Natureza prospectiva (o que distingue este arquivo).** Este é um documento
> *prospectivo* — olha para a frente, para o que ainda falta verificar/declarar
> antes de escrever. Ele **não substitui**:
>
> | Documento | Direção | Papel |
> |---|---|---|
> | [`achados_divergencias.md`](achados_divergencias.md) | Retrospectivo | Síntese das divergências já observadas entre proposto e executado. |
> | [`decision_log.md`](decision_log.md) | Registro | Decisões já tomadas (DL-xx / D-xx), com justificativa e alternativas rejeitadas. |
> | [`limitations.md`](limitations.md) | Retrospectivo | Limitações metodológicas conhecidas do protótipo. |
>
> Quando um item `W-NN` se resolver apontando para uma decisão já registrada,
> **referencie** o item correspondente naqueles arquivos — não copie o conteúdo
> para cá. Este checklist é um índice de pendências de escrita, não a fonte
> primária.

---

## Papéis documentais e fronteiras

Três documentos parecem registrar "pontos em aberto", mas cada um tem um papel
distinto e uma direção no tempo diferente. A regra de fronteira é simples: onde
houver dúvida sobre **onde registrar algo**, o registro vai no artefato novo
(este checklist), não diluído nos docs retrospectivos.

- **[`achados_divergencias.md`](achados_divergencias.md)** — *retrospectivo,
  fechado*: síntese das divergências já observadas entre o que foi **proposto** e
  o que foi **executado**; não recebe novas pendências de escrita.
- **[`decision_log.md`](decision_log.md)** — *registro de decisões já tomadas*
  (`D-01..D-xx` / `DL-xx`), com justificativa e alternativas rejeitadas; **não é
  fila de pendências** — uma entrada só entra aqui depois que a decisão está
  consolidada.
- **`artifact_writing_checklist.md` (este)** — *prospectivo*: fila de
  verificações a **confirmar ou declarar** no texto antes de redigir cada seção,
  abertas até virarem uma decisão (que migra para `decision_log.md`) ou texto no
  artefato final.

Os links acima são apenas ponteiros de localização: este checklist referencia,
mas **não reescreve** o conteúdo daqueles arquivos.

---

## Estrutura de cada item

Cada pendência de escrita é registrada como um item `W-NN` com os campos abaixo.
Todos os campos são obrigatórios.

| Campo | Conteúdo |
|---|---|
| **ID** | Identificador sequencial `W-NN` (ver convenção de numeração abaixo). |
| **Origem** | De onde a pendência veio: issue, achado (`A#`/`B#`/`C#`), decisão (`D-xx`/`DL-xx`), seção de doc, ou observação de revisão. |
| **Tipo** | Um de: `verificação técnica` \| `ponto interpretativo` \| `decisão pendente` \| `nota de método`. |
| **Descrição** | O que precisa ser verificado, decidido ou declarado antes de escrever. |
| **Critério de fechamento** | Condição objetiva que, uma vez satisfeita, permite mover o item para "Itens resolvidos". |
| **Destino no texto** | Onde no relatório/artigo a resolução deste item será incorporada (seção, tabela, figura). |
| **Status** | Um de: `aberto` \| `em verificação` \| `resolvido`. |

### Convenção de numeração `W-NN`

- A numeração é **sequencial** e **global**: `W-01`, `W-02`, `W-03`, … na ordem
  em que os itens são adicionados.
- IDs **nunca são reaproveitados**: ao resolver um item, ele migra para a seção
  "Itens resolvidos" preservando seu ID; o próximo item novo recebe sempre o
  próximo número inédito, mesmo que haja "buracos" deixados por itens removidos.
- A numeração é independente das demais famílias de identificadores do projeto
  (`A#`/`B#`/`C#` dos achados; `D-xx`/`DL-xx` das decisões) — `W-NN` é exclusivo
  deste checklist.

---

## Itens ativos

> Itens com status `aberto` ou `em verificação`. Pendências de escrita a resolver
> antes de redigir as seções correspondentes.

> Os seis itens abaixo (`W-01..W-06`) foram levantados pela **análise transversal
> de comparabilidade Facebook×Enron** (issue #141, S10-V1). A comparabilidade entre
> os dois datasets é algoritmicamente sólida (mesmo anonimizador, mesmas métricas,
> mesmos ataques pós-#139), mas há pontos de **assimetria de pipeline ou de
> interpretação** que precisam estar resolvidos ou declarados antes da redação das
> seções de resultados. O item-piloto `W-00` (EXEMPLO do dry-run #157) foi removido
> ao popular esta faixa real.

### W-01

| Campo | Conteúdo |
|---|---|
| **ID** | `W-01` |
| **Origem** | Análise transversal sobre #139 e #128. |
| **Tipo** | `verificação técnica` |
| **Descrição** | O `he2009_enron_secondary.yml` declara explicitamente `s_max: 4` e `isomorphism_mode: add_or_delete` (B6 / #105). O `he2009_facebook_full.yml` **não** declara essas chaves. Resolver os defaults aplicados pelo anonimizador/runner quando as chaves estão ausentes e confirmar que são idênticos aos valores explícitos do Enron. Se forem, registrar como decisão (anexo a D-01/B6 ou nova entrada `DL-xx` — **não** `D-16`, já usado pelo WL-bucketing). Se não forem, equalizar os configs antes de gerar qualquer tabela comparativa. |
| **Critério de fechamento** | PR com (a) nota em `decision_log.md` declarando equivalência de defaults, **ou** (b) PR equalizando os configs. |
| **Destino no texto** | Seção de método (uniformidade de parâmetros entre datasets) do relatório e do artigo. |
| **Status** | `em verificação` (verificação técnica direta; resolução formal — nota em `decision_log.md` — no PR de resolução desta mesma issue #141). |

### W-02

| Campo | Conteúdo |
|---|---|
| **ID** | `W-02` |
| **Origem** | #139 (DoD, item 2 do escopo). |
| **Tipo** | `nota de método` |
| **Descrição** | Confirmar, após merge da #139, qual ramo da cláusula objetiva de exatidão foi adotado — **(b)** WL puro + verificação ampla (100% de equivalência exata em grafos pequenos) ou **(a)** híbrido WL+VF2 em baldes pequenos (qualquer divergência detectada). Registrar o desfecho de forma que o artigo possa citar a equivalência semântica entre `reidentification_rate_subgraph` no Facebook (VF2) e no Enron (caminho rápido) — não como aproximação heurística. Desfecho conhecido após o merge: **opção (b)** (WL puro), registrada em **D-16**. |
| **Critério de fechamento** | Desfecho registrado no checklist com ponteiro para o PR da #139 e para a entrada **D-16** em `decision_log.md`. |
| **Destino no texto** | Seção de método (ataque por subgrafo, equivalência VF2 ↔ WL) do relatório; nota correspondente no artigo. |
| **Status** | `em verificação` (#139 mergeada; desfecho = WL puro / opção (b) / **D-16** — a recordar na redação do método, S10-W). |

### W-03

| Campo | Conteúdo |
|---|---|
| **ID** | `W-03` |
| **Origem** | #139 (item 3 do escopo — micro-decisão "preservar redação ou afrouxar com nota"). |
| **Tipo** | `nota de método` |
| **Descrição** | No caminho WL-bucketing o custo é agregado, não por nó-alvo, então `subgraph_timeout_count` perde sentido operacional como gate de validade. Documentar a decisão tomada na #139 (preservar redação / afrouxar com nota) e a fundamentação alternativa de validade (prova de equivalência exata WL=VF2, item W-02). Sob D-16 o campo é gravado como `0` e o gate **D-13** (`subgraph_timeout_count == 0`) fica trivialmente satisfeito. |
| **Critério de fechamento** | Decisão registrada no checklist com ponteiro para `decision_log.md` (extensão de D-15 / entrada **D-16**). |
| **Destino no texto** | Seção de método (validade da execução Enron) do relatório; eventual nota no artigo. |
| **Status** | `em verificação` (#139 mergeada; **D-16** grava `subgraph_timeout_count = 0` → D-13 trivialmente satisfeito; redação final em S10-W). |

### W-04

| Campo | Conteúdo |
|---|---|
| **ID** | `W-04` |
| **Origem** | Análise transversal; probe de #139 (`reidentification_rate_subgraph` ≈ 0,123 em k=2 vs ~0,003 do grau). |
| **Tipo** | `ponto interpretativo` |
| **Descrição** | Confirmar que o gap `reidentification_rate_subgraph >> reidentification_rate_degree` em d=1 aparece em **ambos** Facebook e Enron, sustentando a generalização da frase-síntese de B1 ("d=1 anonimiza grau, não estrutura 1-hop"). Se aparecer só em um dataset, B1 perde generalização e a redação precisa recuar a afirmação. |
| **Critério de fechamento** | Valores confirmados nos dois datasets a partir dos JSONL/summary das execuções; registro de coerência (ou divergência) com B1. |
| **Destino no texto** | Seção de resultados / discussão (B1 como achado generalizável) do relatório e do artigo. |
| **Status** | `aberto` |

### W-05

| Campo | Conteúdo |
|---|---|
| **ID** | `W-05` |
| **Origem** | Análise transversal; alinhamento com `docs/scope.md` §3 (Facebook [M] / Enron [D]). |
| **Tipo** | `ponto interpretativo` |
| **Descrição** | Fixar, antes da redação, que Facebook é dataset **principal [M]** e Enron é **secundário [D]** para teste de generalização — não tratar como dois pontos simétricos em curva única. Convergir com a frase-síntese pedida pela DoD de #128. |
| **Critério de fechamento** | Vocabulário definido (uma frase canônica) e referenciado em qualquer S10-W que toque o tema. |
| **Destino no texto** | Seção de método (desenho experimental) e seção de discussão (validade externa) do relatório; nota equivalente no artigo. |
| **Status** | `aberto` |

### W-06

| Campo | Conteúdo |
|---|---|
| **ID** | `W-06` |
| **Origem** | Análise transversal; DoD de #128 ("se não comparável diretamente, justificar (escala/densidade distintas)"). |
| **Tipo** | `decisão pendente` |
| **Descrição** | Decidir entre matriz privacidade-utilidade unificada (Facebook e Enron no mesmo eixo) vs painéis lado a lado (mesma estrutura, escalas independentes), dada a diferença de escala/densidade. A decisão afeta `src/visualization/` e a forma das figuras do artigo. Contexto relevante: **DL-04** (#128) já materializou gráficos **por dataset** + painel normalizado complementar (`comparison_fb_enron`); confirmar na redação se essa escolha encerra W-06 ou se a forma final do artigo ainda decide. |
| **Critério de fechamento** | Decisão registrada no checklist com ponteiro para o PR de #128 (**DL-04**) que materializa a escolha em código. |
| **Destino no texto** | Figuras de resultados do relatório e do artigo. |
| **Status** | `aberto` |

---

## Itens resolvidos

> Itens com status `resolvido`, preservando o ID original (`W-NN` nunca
> reaproveitado). Mantidos como histórico de rastreabilidade.

_(vazio)_
