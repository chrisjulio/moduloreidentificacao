# Registro de Decisões — Desvios e Refinamentos Documentados

> Este arquivo registra decisões que representam **desvios fundamentados** em relação
> ao planejamento original ou **refinamentos de critérios** que não constavam
> explicitamente nos documentos de referência. Desvios não documentados não são
> permitidos (Seção 11 do plano operacional).

---

## DL-01 — Refinamento do critério de passagem do marco #16 (k-anonimato estrutural)

**Data:** 2026-05-21  
**Issue relacionada:** #16  
**Decisão sobre:** Seção 4.3 do planejamento ("verificação binária") vs. critério D-06 inserido em #16

### Contexto

O planejamento original (Seção 4.3) tratava a verificação de k-anonimato estrutural
como **binária**: para cada valor de `k`, ou a instância era integralmente coberta
(`valid=True`), ou os resultados eram inválidos. O critério de "sucesso parcial
aceitável" com `satisfied_fraction >= 0.9` foi introduzido na definição de pronto
da issue #16 (campo D-06) sem que o documento de decisões registrasse formalmente
por que essa tolerância era metodologicamente defensável.

A Seção 11 do plano operacional é explícita: *"desvios fundamentados são esperados;
desvios não documentados, não."* Este documento resolve a pendência.

### Problema com a redação original de D-06

O enunciado `satisfied_fraction >= 0.9` como critério de "sucesso parcial aceitável"
cria uma ambiguidade metodológica grave:

- Um valor de `0.9` fixo sugere que até 10% de nós descobertos é tolerável por
  definição, independentemente de quem são esses nós e por quê não foram cobertos.
- 30% de nós descobertos sendo todos folhas de grau 1 em componentes estruturalmente
  impossibilitados de satisfazer k-anonimato para o `k` dado é **algoritmo correto**.
- 5% de nós descobertos incluindo nós de alto grau em regiões densas é **bug ou
  implementação incompleta**, independentemente de o `satisfied_fraction` ser 0,95.
- Sem distinguir as duas situações, a curva privacidade × utilidade — a entrega
  central do módulo — torna-se indefensável: uma taxa de reidentificação alta em
  `k=20` pode parecer "algoritmo fraco" quando na verdade reflete nós
  estruturalmente improtegíveis.

### Decisão adotada (Opção A)

O critério de passagem do marco #16 é **refinado** da seguinte forma:

**Critério substantivo (lógico):**
> 100% do déficit de cobertura de k-anonimato — isto é, a fração de nós não
> cobertos — é atribuível a causas estruturais identificadas pelo verificador
> (por exemplo: nós de grau 1, componentes com vizinhança isomórfica insuficiente
> para o `k` configurado, ou grupos incompletos residuais conforme D-06).

**Piso de sanidade operacional:**
> `satisfied_fraction >= 0.9` é rebaixado a **limite operacional mínimo**,
> não a régua lógica do marco. Instâncias com `satisfied_fraction < 0.9` não
> são aceitas como válidas para uso em métricas derivadas, independentemente
> da causa do déficit.

**Condição de passagem completa:**
> Entre `0.9` e `1.0`, a aceitação depende de o déficit ser integralmente
> rotulado como `structural_impossibility` pelo verificador. Qualquer violador
> classificado como `implementation_error` ou `unknown` é tratado como falha,
> independentemente do valor de `satisfied_fraction`.

### Consequências para a saída do verificador

O verificador `validate_k_anonymity` passa a reportar, para cada par (grafo, k):

- `coverage_fraction` — fração de nós cobertos (saída real do verificador,
  pode ser 0,83, 0,97, 1,0 etc.; **não é um percentual fixo pré-definido**);
- `uncovered_fraction` — fração de nós não cobertos (derivada da anterior);
- rótulo de causa para o déficit: `structural_impossibility`, `implementation_error`,
  ou `unknown`;
- lista de nós não cobertos com causa individual (para auditoria).

> **Importante:** o percentual de nós não cobertos é sempre resultado da execução
> do verificador sobre o grafo concreto. Não existe um "10% fixo" descartado a
> priori — o valor real depende do grafo e do `k`, e pode ser 2%, 7%, 15% etc.

### Consequências para as métricas e os gráficos

Os relatórios de risco de reidentificação passam a distinguir explicitamente:

- **(a)** taxas calculadas sobre **todos** os nós do grafo;
- **(b)** taxas calculadas apenas sobre o subconjunto de nós com
  **k-anonimato estrutural estrito** (nós cobertos, excluindo violadores
  classificados como `structural_impossibility`).

Essa distinção preserva a interpretabilidade da curva privacidade × utilidade:
uma taxa de reidentificação alta em `k=20` pode ser corretamente lida como
"5% dos nós eram estruturalmente improtegíveis" em vez de "algoritmo fraco",
desde que o déficit esteja integralmente rotulado pelo verificador.

### O que não muda

- O **critério binário original** do planejamento continua válido para o
  subconjunto de nós **cobertos**: dentro desse subconjunto, ou há k-anonimato
  estrutural completo (grupos de `k` LSs isomorfas) ou há falha.
- A decisão D-06 (`algorithm_notes.md`) permanece como política para grupos
  incompletos residuais — este documento apenas especifica que D-06 é uma
  causa estrutural legítima de `uncovered_fraction > 0`, desde que identificada
  e rotulada pelo verificador.
- O piso `0.9` como limite de sanidade operacional é mantido, rebaixado de
  critério de passagem a condição necessária (mas não suficiente).

### Referências cruzadas

- Issue #16 (definição de pronto, campo D-06)
- `docs/algorithm_notes.md` §4 (critério de k-anonimato e verificador)
- `docs/algorithm_notes.md` §7 (D-06, D-07)
- `docs/metrics_definitions.md` §k-anonymity-verifier
- Plano operacional, Seções 4.3, 7 e 11
