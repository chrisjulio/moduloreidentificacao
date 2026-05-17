# Notas de Implementação — He et al. (2009)

> Registro passo a passo do algoritmo de anonimização estrutural.
> Preencher progressivamente durante a Semana 1 (15–22/05/2026) à medida que
> a leitura do artigo avança. Cada seção deve ser atualizada antes de iniciar
> a implementação correspondente.

## Referência

He, X. et al. (2009). Preserving privacy in social networks: A structure-aware
approach. *Proceedings of the IEEE/WIC/ACM International Joint Conference on
Web Intelligence and Intelligent Agent Technology (WI-IAT)*.
DOI: 10.1109/WI-IAT.2009.108

---

## 1. Conceito central: k-anonimato estrutural

> **Escopo desta seção (issue [#8](https://github.com/chrisjulio/moduloreidentificacao/issues/8)):**
> vocabulário conceitual fundamentado nas três perguntas do esqueleto e nas
> quatro definições formais da Seção 2 do artigo (pp. 647–649).
> A decomposição operacional do algoritmo (partição, grouping, isomorfização,
> reconexão) é objeto das Seções 2 e 3 deste documento — issues subsequentes.

### 1.1 O que constitui um grupo de equivalência em grafos?

O grupo de equivalência é formado pelo conjunto de `k` **Local Structures (LSs)
isomorfas entre si** que o algoritmo produz durante a etapa de grouping
(Seção 3.2 do artigo). Qualquer nó pertencente a uma LS do grupo é
indistinguível dos nós nas demais `k−1` LSs — a condição de isomorfismo entre
subgrafos locais é o critério de equivalência (Def. 2, p. 648, Seção 2.3).

> "[...] node v_i is structure-aware k-anonymous, if there are at least k−1
> other nodes which do not belong to LS(v_i) while having the local structure
> that is isomorphic to LS(v_i)." (Def. 2, p. 648)

### 1.2 Qual a propriedade estrutural que torna dois nós indistinguíveis?

Dois nós são indistinguíveis quando suas Local Structures são **graficamente
isomorfas** (`LS(v_i) ≅ LS(v_j)`): existe uma bijeção `f: V(LS_i) → V(LS_j)`
tal que `(u, w) ∈ E(LS_i)` sse `(f(u), f(w)) ∈ E(LS_j)` (Seção 2.3, p. 648).
O isomorfismo captura simultaneamente grau, adjacências e distâncias locais;
nenhuma informação estrutural de fundo sobre a vizinhança do alvo permite
distinguir os `k` candidatos (Seção 2.2).

> "An isomorphism of graphs from G to H is a bijection f : V(G) → V(H)
> such that any edge (v1, v2) ∈ E(G) if and only if (f(v1), f(v2)) ∈ E(H)."
> (p. 648, Seção 2.3)

### 1.3 k-anonimato aqui refere-se a grau, vizinhança, ou outra assinatura?

Nem grau nem vizinhança de raio fixo: a assinatura é o **isomorfismo do
subgrafo comunitário local de tamanho variável `d`**. O artigo critica
explicitamente as duas abordagens anteriores por insuficiência:

- **k-degree anonymity** (Liu & Terzi [5]): baseia-se só no grau,
  ignorando estrutura. *"[...] this anonymization process completely ignores
  structural information inherent in the graph data."* (p. 648, Seção 1)
- **1-neighborhood isomorphism** (Zhou & Pei [4]): raio fixo (1-hop)
  provoca re-anonimizações em cascata e produz grafos degenerados
  (p. 648, Seção 1).

A garantia formal do modelo: a confiança de reidentificação de qualquer nó
em G' é no máximo `1/k` (Def. 2–3, p. 648, Seção 2.3).

> "[...] the confidence of this node being re-identified from the graph is no
> higher than 1/k." (p. 648, Seção 2.3)

### 1.4 Camada conceitual formal — Definições 1–4 (Seção 2, pp. 647–649)

As quatro definições são encadeadas: cada uma pressupõe a anterior e a
camada 1.1–1.3 acima só é possível porque o artigo as estabelece nesta ordem.

#### Def. 1 — Local Structure (Seção 2.1, p. 648)

Dado um grafo `G = (V, E)` e um nó `v_i ∈ V`, a **Local Structure** de `v_i`,
denotada `LS(v_i)`, é um componente subgrafo **conectado** contendo `v_i`,
com densidade de arestas interna maior do que a densidade das arestas que
ligam os nós de `LS(v_i)` aos nós externos a ela.

- `|LS(v_i)|` denota o tamanho (número de nós) da Local Structure.
- Todos os nós dentro de uma mesma LS **compartilham a mesma Local Structure**.
- A LS é a **unidade de anonimização**: o algoritmo opera sobre ela como um
  bloco único, não nó a nó — o que reduz a perturbação total do grafo.
- O tamanho `d` da LS é variável (Fig. 2, p. 648): o publicador não consegue
  prever qual escopo o adversario conhece, portanto o modelo não o fixa.

#### Def. 2 — Structure-Aware k-Anonymous Node (Seção 2.3, p. 648)

Um nó `v_i` é **structure-aware k-anonymous** se existem pelo menos `k−1`
outros nós que (i) **não pertençam** a `LS(v_i)` e (ii) possuam Local
Structure **isomorfa** a `LS(v_i)`.

- Implicação direta: a confiança de reidentificação de `v_i` é `≤ 1/k`.
- A condição é sobre nós **fora** da própria LS de `v_i` (para evitar
  circularidade: nós dentro da mesma LS já são estruturalmente idênticos).

#### Def. 3 — Structure-Aware Graph k-Anonymity (Seção 2.3, p. 648)

Um grafo anonimizado `G'` é **structure-aware k-anonymous** se **todo nó**
em `G'` satisfaz a Def. 2.

- Garantia global: não basta cobrir a maioria dos nós; a propriedade precisa
  valer universalmente.
- A definição **não impõe requisitos de utilidade** — isso é tratado pela
  Def. 4 como objetivo de otimização.

#### Def. 4 — Structure-Aware kd Graph Anonymity (Seção 2.3, p. 649)

Dado `G = (V, E)` e inteiros positivos `k` e `d`, o objetivo é encontrar
um grafo `G'` structure-aware k-anonymous tal que:

1. a estrutura de `G` seja perturbada o **mínimo possível** (preservação
   de propriedades: APL, CC, distribuição de grau); e
2. sua publicação **não cause violação de privacidade** conforme os
   parâmetros `k` e `d`.

| Parâmetro | Papel | Efeito prático |
|-----------|-------|----------------|
| `k` | nível de privacidade | mínimo de candidatos indistinguíveis por nó |
| `d` | tamanho da LS (nós por partição) | controla granularidade; `c_k = ⌊n/d⌋` partições |

> **Nota para implementação futura:** o verificador `validate_k_anonymity`
> deve checar isomorfismo de subgrafo entre LSs, **não** apenas igualdade de
> grau. O modelo adversarial (Seção 2.2) assume conhecimento multidimensional
> (grau, adjacências, vizinhança, ou combinações), portanto verificar só grau
> seria insuficiente.

---

## 2. Algoritmo principal

*(a preencher — issue subsequente)*

Estrutura esperada (esqueleto a confirmar com o artigo):

```
Entrada:  grafo G = (V, E), parâmetros k e d
Saída:    grafo anonimizado G' = (V, E') com k-anonimato garantido

Passos:
  1. Partição em Local Structures  [Seção 3.1]
  2. Agrupamento de LSs             [Seção 3.2 — Algorithm 1]
  3. Isomorfização dentro do grupo [Seção 3.2 — Fases 1 e 2]
  4. Reconexão                      [Seção 3.3]
```

Complexidade declarada no artigo: *(a preencher)*

---

## 3. Operações de modificação do grafo

*(a preencher — issue subsequente)*

Quões a responder:
- O algoritmo adiciona arestas, remove arestas, ou ambos?
- Há operações sobre nós (inserção, fusão)?
- As operações são determinísticas ou têm componente aleatório (→ impacto nas sementes)?

---

## 4. Critério de parada e garantia de k-anonimato

*(a preencher — issue subsequente)*

Quões a responder:
- Como o algoritmo verifica que k-anonimato foi atingido?
- O que acontece se o grafo não puder ser anonimizado para o k pedido?
- Como implementar o verificador independente (`validate_k_anonymity`)?

---

## 5. Parâmetros e configuração

*(a preencher)*

Mapear para as chaves do YAML de configuração ([config_example.yml](../config_example.yml)):

| Parâmetro do artigo | Chave YAML | Valor(es) usados |
|---|---|---|
| `k` | `anonymization.k_values` | [2, 5, 10, 20] |
| `d` | *(a mapear)* | |
| `σ` (suporte FSM) | *(a mapear)* | |

---

## 6. Casos especiais e limitações documentadas no artigo

*(a preencher)*

Exemplos de casos que podem exigir tratamento especial:
- Grafos desconectados
- Nós isolados
- Grafos muito densos

---

## 7. Decisões de implementação (registrar conforme surgem)

| Data | Decisão | Justificativa |
|---|---|---|
| | | |

---

## 8. Validação: o que "empiricamente atingido" significa

Para o marco de 29/05/2026, a validação de k-anonimato deve ser:

- [ ] Verificador implementado **independentemente** do anonimizador
      (não reutilizar código interno do algoritmo).
- [ ] Verificador aplicado sobre o grafo de saída G', não sobre estruturas
      internas do algoritmo.
- [ ] Resultado registrado em log estruturado, reproduzível via semente.
- [ ] Testado em ao menos uma configuração: k=5, uma ego-rede do Facebook.

Critério de aprovação: verificador retorna `True` para o k configurado em
100% das execuções (3 sementes, mesma configuração).
