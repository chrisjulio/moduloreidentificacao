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

_(vazio — a popular em #141)_

---

## Itens resolvidos

> Itens com status `resolvido`, preservando o ID original (`W-NN` nunca
> reaproveitado). Mantidos como histórico de rastreabilidade.

_(vazio)_
