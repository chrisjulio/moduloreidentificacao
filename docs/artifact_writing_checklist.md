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

> ⚠️ **EXEMPLO removível (dry-run #157).** O item `W-00` abaixo é um **piloto
> ilustrativo**, não uma pendência real de escrita. Ele existe apenas para validar
> que o template `W-NN` acomoda um ponto de assimetria Facebook×Enron (issue #157,
> sub-issue de #140). **Deve ser removido ou substituído** quando a #141 popular os
> itens reais `W-01..W-06`. A numeração `W-00` é deliberadamente fora da faixa
> sequencial real (`W-01`+) para sinalizar seu caráter de exemplo.

### W-00 (EXEMPLO — removível)

| Campo | Conteúdo |
|---|---|
| **ID** | `W-00` (EXEMPLO — não conta na numeração sequencial real). |
| **Origem** | #128 (comparativo Facebook×Enron) e #139 (ataque por subgrafo via WL-bucketing), **ambas fechadas** — entram só como origem; achado C2 (motor não-pareado KL×pymetis); decisão D-11 (simetrização OR do Enron). |
| **Tipo** | `ponto interpretativo` |
| **Descrição** | Ao apresentar o comparativo Facebook×Enron, declarar que as magnitudes de `rr_subgrafo` **não são diretamente comparáveis** entre as redes (escala n≈532 vs n≈33.696; densidade; origem OR/D-11; motor de particionamento KL vs pymetis). Sobrepor as duas curvas num único eixo absoluto é enganoso; o texto deve usar os eixos **normalizados** (`rr·k` vs cota `1/k`; decaimento relativo `rr(k)/rr(k_min)`) e nomear o cruzamento das curvas (~k≈14) sem afirmar que uma rede é "mais privada" que a outra. |
| **Critério de fechamento** | A subseção comparativa dos Resultados (1) declara explicitamente a não-comparabilidade de magnitude, (2) usa o painel normalizado em vez de sobrepor magnitudes absolutas, e (3) cita o cruzamento sem inferir superioridade de privacidade de uma rede. |
| **Destino no texto** | Seção de Resultados — subseção comparativa Facebook×Enron (figura do painel normalizado `comparison_fb_enron`). |
| **Status** | `em verificação` (EXEMPLO) |

> **Resultado do dry-run (#157).** O ponto de assimetria acima foi mapeado nos
> **sete campos** do template sem ambiguidade nem campo faltante: a *Origem*
> acomodou múltiplas referências (issues fechadas + achado + decisão); o *Tipo*
> `ponto interpretativo` classificou bem um ponto de leitura (não técnico, não
> decisão pendente); *Critério de fechamento* expressou uma condição objetiva e
> verificável; *Destino no texto* apontou seção e figura concretas. **Conclusão:
> o template `W-NN` é suficiente — nenhum ajuste de campo necessário** (DoD da
> #157). A "Estrutura de cada item" acima permanece inalterada.

---

## Itens resolvidos

> Itens com status `resolvido`, preservando o ID original (`W-NN` nunca
> reaproveitado). Mantidos como histórico de rastreabilidade.

_(vazio)_
