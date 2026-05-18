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

> **Escopo desta seção:**
> vocabulário conceitual fundamentado nas três perguntas do esqueleto e nas
> quatro definições formais da Seção 2 do artigo (pp. 647–649).
> A decomposição operacional do algoritmo (partição, grouping, isomorfização,
> reconexão) é objeto das Seções 2 e 3 deste documento — issues subsequentes.

### 1.0 Nota terminológica: "grupo de equivalência" vs. k-group de estruturas locais

O termo **grupo de equivalência** não aparece em He et al. (2009). O construto
operacionalmente equivalente no artigo é o conjunto de `k` Local Structures
agrupadas pela etapa de *grouping* (Seção 3.2, p. 650); os autores não
atribuem um nome específico a esse conjunto — ele é simplesmente referenciado
como "a group" ou `G_r` no Algorithm 1.

O vocabulário de **grupo de equivalência** vem da literatura de anonimização
tabular (tipicamente associado a k-anonymity sobre dados relacionais, ex.
Sweeney, 2002). Usamos a expressão por conveniência, como ponte para
leitores familiarizados com aquele vocabulário.

Neste documento, adotamos a expressão **grupo de equivalência estrutural**
como ponte vocabular explícita: ela designa o conjunto de `k` LSs isomorfas
produzido pelo algoritmo de He et al., e será o ponto de comparação com os
construtos correspondentes em Nettleton & Salas (2016) — cujo vocabulário
será reconciliado no issue correspondente àquele artigo.

### 1.1 O que constitui um grupo de equivalência em grafos?

O **grupo de equivalência estrutural** (no sentido da Seção 1.0) é formado
pelo conjunto de `k` **Local Structures** que, ao **final do algoritmo**,
são mutualmente isomorfas. Operacionalmente, o conjunto é determinado pela
etapa de grouping (Seção 3.2 do artigo), e a propriedade de isomorfismo é
estabelecida pela etapa de transformação subsequente (fases 1 e 2 da Seção
3.2). Qualquer nó pertencente a uma LS do grupo é indistinguível dos nós nas
demais `k−1` LSs — o isomorfismo entre subgrafos locais é o critério de
equivalência (Def. 2, p. 649, Seção 2.3).

> "[...] node v_i is structure-aware k-anonymous, if there are at least k−1
> other nodes which do not belong to LS(v_i) while having the local structure
> that is isomorphic to LS(v_i)." (Def. 2, p. 649)

### 1.2 Qual a propriedade estrutural que torna dois nós indistinguíveis?

Dois nós são indistinguíveis quando suas Local Structures são **graficamente
isomorfas** (`LS(v_i) ≅ LS(v_j)`): existe uma bijeção `f: V(LS_i) → V(LS_j)`
tal que `(u, w) ∈ E(LS_i)` sse `(f(u), f(w)) ∈ E(LS_j)` (Seção 2.3, p. 649).
O isomorfismo captura simultaneamente grau, adjacências e distâncias locais;
nenhuma informação estrutural de fundo sobre a vizinhança do alvo permite
distinguir os `k` candidatos (Seção 2.2).

> "An isomorphism of graphs from G to H is a bijection f : V(G) → V(H)
> such that any edge (v1, v2) ∈ E(G) if and only if (f(v1), f(v2)) ∈ E(H)."
> (p. 649, Seção 2.3)

### 1.3 k-anonimato aqui refere-se a grau, vizinhança, ou outra assinatura?

Nem grau nem vizinhança de raio fixo: a assinatura é o **isomorfismo do
subgrafo comunitário local de tamanho variável `d`**. O artigo critica
explicitamente as duas abordagens anteriores por insuficiência:

- **k-degree anonymity** (Liu & Terzi [5]): baseia-se só no grau,
  ignorando estrutura. *"[...] this anonymization process completely ignores
  structural information inherent in the graph data."* (p. 647, Seção 1)
- **1-neighborhood isomorphism** (Zhou & Pei [4]): raio fixo (1-hop)
  provoca re-anonimizações em cascata e produz grafos degenerados
  (p. 647, Seção 1).

A garantia formal do modelo: a confiança de reidentificação de qualquer nó
em G' é no máximo `1/k` (Def. 2–3, p. 649, Seção 2.3).

> "[...] the confidence of this node being re-identified from the graph is no
> higher than 1/k." (p. 649, Seção 2.3)

### 1.4 Camada conceitual formal — Definições 1–4 (Seção 2, pp. 647–649)

As quatro definições são encadeadas: cada uma pressupõe a anterior e a
camada 1.1–1.3 acima só é possível porque o artigo as estabelece nesta ordem.

#### Def. 1 — Local Structure (Seção 2.1, p. 649)

Dado um grafo `G = (V, E)` e um nó `v_i ∈ V`, a **Local Structure** de `v_i`,
denotada `LS(v_i)`, é um componente subgrafo **conectado** contendo `v_i`,
com densidade de arestas interna maior do que a densidade das arestas que
ligam os nós de `LS(v_i)` aos nós externos a ela.

- `|LS(v_i)|` denota o tamanho (número de nós) da Local Structure.
- Todos os nós dentro de uma mesma LS **compartilham a mesma Local Structure**.
- A LS é a **unidade de anonimização**: o algoritmo opera sobre ela como um
  bloco único, não nó a nó — o que reduz a perturbação total do grafo.
- O tamanho `d` da LS é variável (Fig. 2, p. 649): o publicador não consegue
  prever qual escopo o adversário conhece, portanto o modelo não o fixa.

#### Def. 2 — Structure-Aware k-Anonymous Node (Seção 2.3, p. 649)

Um nó `v_i` é **structure-aware k-anonymous** se existem pelo menos `k−1`
outros nós que (i) **não pertençam** a `LS(v_i)` e (ii) possuam Local
Structure **isomorfa** a `LS(v_i)`.

- Implicação direta: a confiança de reidentificação de `v_i` é `≤ 1/k`.
- A condição é sobre nós **fora** da própria LS de `v_i` (para evitar
  circularidade: nós dentro da mesma LS já são estruturalmente idênticos).

#### Def. 3 — Structure-Aware Graph k-Anonymity (Seção 2.3, p. 649)

Um grafo anonimizado `G'` é **structure-aware k-anonymous** se **todo nó**
em `G'` satisfaz a Def. 2.

- Garantia global: não basta cobrir a maioria dos nós; a propriedade precisa
  valer universalmente.
- A definição **não impõe requisitos de utilidade** — isso é tratado pela
  Def. 4 como objetivo de otimização.

#### Def. 4 — Structure-Aware kd Graph Anonymity (Seção 2.3, p. 649)

Dado `G = (V, E)` e inteiros positivos `k` e `d`, o objetivo é encontrar
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

> **Fonte:** He et al. (2009), Seção 3, pp. 649–652.

### 2.1 Visão geral — três etapas encadeadas

```
Entrada:  G = (V, E),  k (privacidade),  d (tamanho máximo de LS),
          σ (suporte FSM — threshold de frequência),
          s_max (tamanho máximo de subgrafo para FSM simplificado)
Saída:    G' = (V, E')  structure-aware k-anonymous

─────────────────────────────────────────────────────────────
Etapa 1 — PARTIÇÃO  (Seção 3.1)
─────────────────────────────────────────────────────────────
1.1  Calcular c_k = ⌊|V| / d⌋          // número de partições
1.2  Aplicar particionamento k-way em G via Kernighan-Lin bisseção recursiva
     → produz subconjuntos V₁, V₂, ..., V_{c_k}
        tal que |Vᵢ| ≤ d  e  arestas inter-partição minimizadas   [D-04]
1.3  Para cada i: construir Cᵢ = (Vᵢ, Eᵢ)   // subgrafo induzido
1.4  Remover temporariamente as arestas inter-partição de G
     → conjunto de arestas removidas: E_inter
     → saída: {LS₁, LS₂, ..., LS_{c_k}}

─────────────────────────────────────────────────────────────
Etapa 2 — AGRUPAMENTO E ISOMORFIZAÇÃO  (Seção 3.2 / Algorithm 1)
─────────────────────────────────────────────────────────────
2.1  Executar FSM simplificado({LS₁..LS_{c_k}}, σ, s_max)         [D-01]
     → subgrafos frequentes g₁..gₘ com |V(gᵢ)| ≤ s_max
     → SLS(gᵢ): conjunto de LSs que contêm gᵢ

2.2  Repetir até todas as LSs estarem agrupadas:
     a) Para cada gᵢ ∈ S, calcular MF(gᵢ):
           MF(gᵢ) = |E(gᵢ)| · k           se |SLS(gᵢ)| ≥ k
           MF(gᵢ) = |E(gᵢ)| · |SLS(gᵢ)|  caso contrário
     b) Escolher gⱼ com maior MF
     c) Formar grupo G_r de tamanho k:
           se |SLS(gⱼ)| ≥ k  →  escolher k LSs aleatoriamente de SLS(gⱼ)
           se |SLS(gⱼ)| < k  →  completar com LSs de SLS(g_complementar)
                                  ou LSs livres em S
     d) Remover G_r de S e de todos SLS
2.3  LSs restantes (< k) → grupo final possivelmente incompleto   [D-06]

2.4  Para cada grupo G_r de k LSs:

     FASE 1 — Matching e numeração de nós:                         [D-03]
       a) Identificar subgrafo comum gⱼ presente nas LSs do grupo
       b) Atribuir numeração 1..|V(gⱼ)| aos nós de gⱼ em cada LS
       c) Para LSs sem gⱼ: matching por grau;
          desempate por índice de nó (lexicográfico, crescente)
       d) Propagar numeração para vizinhos não numerados,
          em ordem crescente de número já atribuído;
          desempate por grau → índice lexicográfico

     FASE 2 — Tornar isomorfas (adicionar e/ou remover arestas):
       a) Para cada par numerado (u_i, u_j) em LSs distintas do grupo:
          - contar existência/não-existência da aresta em cada LS
          - escolher add ou delete — o que requerer menos mudanças

─────────────────────────────────────────────────────────────
Etapa 3 — RECONEXÃO  (Seção 3.3)
─────────────────────────────────────────────────────────────
3.1  Para cada aresta inter-partição (u, v) ∈ E_inter:
     - u ∈ LSᵢ pertencente ao grupo G_r
     - para manter isomorfismo: adicionar k(k-1) arestas complementares
       (uma por cada par de cópias do nó nas k LSs do grupo)
3.2  G' = união de todas as LSs transformadas
          + arestas inter-partição originais
          + arestas adicionadas no passo 3.1

Retornar G'
```

### 2.2 Complexidade declarada

| Etapa | Complexidade | Classificação |
|---|---|---|
| Partição (Kernighan-Lin k-way) | `O(|E| · log |V|)` | Interpretativa (complexidade padrão de KL na literatura); METIS é a declarada no artigo, com `O(|E|)` (p. 650) |
| FSM simplificado (enumeração até `s_max`) | `O(|LS|^s_max)` por LS — controlado por `s_max` | Interpretativa — não declarada no artigo |
| Agrupamento (Algorithm 1) | `O(c_k · m)` por iteração; `c_k/k` iterações → `O(n·m / d·k)` | Interpretativa |
| Isomorfização (Fases 1+2) | `O(k · |V(LS)|²)` por grupo | Interpretativa |
| Reconexão | `O(|E_inter| · k²)` | Interpretativa — artigo cita "k(k-1) edges per inter-edge" (p. 652) |

> ⚠️ **Atenção:** apenas a complexidade da partição via METIS é **declarada
> explicitamente** no artigo (`O(|E|)`). Todas as demais são **interpretativas**
> derivadas da descrição do algoritmo. Classificar como tal para fins de
> qualificação e relatório metodológico.

### 2.3 Decisões de estrutura de dados

| Estrutura | Representação escolhida | Justificativa |
|---|---|---|
| Grafo `G` | `networkx.Graph` | Padrão do módulo; suporte a atributos de nó/aresta |
| Local Structures `{LSᵢ}` | lista de `networkx.Graph` (subgrafos induzidos) | Isomorfismo via `nx.is_isomorphic` (VF2) — ver Seção 4 |
| Grupos `G_r` | lista de listas de índices de LS | Estrutura leve; lookup O(1) |
| Arestas inter-partição `E_inter` | conjunto de tuplas `(u, v)` | Remoção e reinserção O(1) |
| Mapeamento nó → número (Fase 1) | `dict[node_id → int]` por LS | Matching e numeração sequencial; determinístico com critério D-03 |

### 2.4 Lacunas do artigo — pontos decididos

As lacunas identificadas nesta seção geraram as decisões D-01 a D-06
registradas na Seção 7. Referências cruzadas marcadas com `[D-xx]` ao longo
do pseudocódigo acima.

---

## 3. Operações de modificação do grafo

> **Fontes:** He et al. (2009), Seções 3.2 (Phase 2, p. 651) e 3.3 (p. 652).

### 3.1 O que o algoritmo modifica

He et al. produzem `G'` modificando **exclusivamente o conjunto de arestas**
de `G`. O conjunto de vértices é preservado: nenhum nó é adicionado,
removido ou fundido ao longo das três etapas (partição, agrupamento/
isomorfização, reconexão). A renumeração interna durante a Fase 1
(Seção 3.2 do artigo) é uma correspondência computacional entre LSs e
**não afeta** a identidade dos nós nem o grafo publicado.

> **Premissa que sustenta "sem operações em nós".** O artigo, na Fase 1
> da Seção 3.2 (p. 651), afirma: *"Since each of local structures in the same
> group has the same number of nodes, this process will terminate quickly."*
> A garantia depende de `|V_i| = d` (igualdade estrita), que com KL (D-04;
> ver `decisions.md`) passa a aproximação. LSs no mesmo grupo podem ter
> contagens de nós distintas, e a implementação precisa de uma política
> explícita para lidar com isso. Ver D-07 (a decidir; ver Seção 7).
> Dependendo da política escolhida — em particular, se envolver padding com
> nós isolados — a afirmação desta seção precisa ser revisada.

### 3.2 Três pontos do algoritmo onde arestas são modificadas

A modificação de arestas ocorre em **três contextos distintos**, cada um
com regras próprias:

#### 3.2.1 Fase de isomorfização intra-grupo (Seção 3.2, Phase 2)

Após o agrupamento, cada grupo de `k` LSs precisa ter suas estruturas
tornadas isomorfas entre si. O artigo propõe duas variantes:

| Variante | Operação | Critério |
|---|---|---|
| **Edge-adding only** | Apenas adição de arestas | Adiciona-se o que falta para tornar pares de LSs isomorfos |
| **Edge-adding/deleting** | Adição **ou** remoção | Para cada par de nós correspondentes entre LSs do grupo, escolhe-se a operação que incorre em **menos modificações totais** |

> *"For each matched pair of nodes in the local structures of the same
> group, we compare the number of edge existence and non-existence between
> these matched pair of nodes in the group. We always choose either adding
> edges or deleting edges, whichever would incur less edge changes for the
> isomorphism."* (p. 651)

> **Nota — greedy por par, não por grupo:** A escolha add vs. del é feita
> independentemente para cada par de nós correspondentes (greedy por par),
> não por otimização global do grupo. A variante edge-adding/deleting não
> garante minimização global de modificações — apenas local por par.

A variante edge-adding/deleting **tende a perturbar menos a estrutura**,
dado que minimiza o número de modificações por par de nós correspondentes.
O artigo não afirma diretamente a preservação de APL/CC/grau como
consequência teórica — a correlação é razoável, mas é inferência, não
afirmação do artigo. Empiricamente, os experimentos (Figuras 3b–d e 4b–d)
confirmam essa correlação para os datasets testados (CompGeo e GBA), sem
garantia teórica extensível a outros grafos.

A escolha entre as duas variantes é **parâmetro de execução**, não
resolvido automaticamente pelo algoritmo. Mapeamento para a configuração
YAML em Seção 5.

#### 3.2.2 Fase de reconexão (Seção 3.3)

Após a partição (Etapa 1) ter removido as arestas inter-LS, e após a
isomorfização (Fase 2) ter sido aplicada intra-grupo, o algoritmo precisa
religar as LSs em um único grafo. Simplesmente reinserir as inter-arestas
removidas quebraria o isomorfismo conquistado: as posições "equivalentes"
de um nó em LSs distintas do mesmo grupo passariam a ter vizinhanças
externas distintas.

Para preservar o isomorfismo, o artigo prescreve a adição de arestas
complementares:

> *"In general, for each original inter-edge, a total of k(k − 1) edges
> have to be added."* (p. 652)

| Propriedade | Valor |
|---|---|
| Tipo de operação | Apenas adição (não há variante "delete" aqui) |
| Custo por inter-aresta | `k(k−1)` arestas adicionais |
| Custo total | `O(|E_inter| · k²)` |

> **Nota de implementação (a verificar):** O artigo não demonstra a
> derivação de `k(k−1)`. A interpretação mais natural é: cada inter-aresta
> `(u, v)` entre `LS_a` e `LS_b` precisa ser replicada para todos os pares
> de posições equivalentes nos `k` grupos que contêm `LS_a` e `LS_b`
> respectivamente, resultando em `k² − k = k(k−1)` arestas adicionais.
> Esta interpretação deve ser validada durante a implementação. Se
> incorreta, a estimativa de `O(|E_inter| · k²)` também precisa ser
> revisada.

Esta é a **terceira fonte de modificação estrutural** e não está coberta
pelas variantes da Seção 3.2.1 — a reconexão é obrigatoriamente aditiva.
Para grafos com muitas inter-arestas (que o particionamento minimiza, mas
não zera), esta fonte pode dominar a perturbação total do grafo final.

#### 3.2.3 Contabilidade da utilidade

As métricas de utilidade definidas no plano operacional (KS-test sobre
distribuição de grau, ΔCC) medem o efeito agregado de **duas** das três
fontes acima — a partição original não modifica arestas, apenas as
redistribui temporariamente. Ao reportar resultados, registrar
separadamente o número de arestas modificadas em cada fase (Fase 2
intra-grupo vs. reconexão) facilita o diagnóstico: se a perturbação total
for dominada pela reconexão, a escolha entre variantes de Phase 2 importa
pouco para a utilidade final.

### 3.3 Determinismo vs. aleatoriedade

O algoritmo contém **cinco fontes de não-determinismo** que precisam ser
controladas para reprodutibilidade:

| # | Fonte | Localização | Mitigação |
|---|---|---|---|
| 1 | Escolha aleatória de `k` LSs de `SLS(g_j)` | Algorithm 1, linha 15 | `random.Random(seed)` único |
| 2 | Escolha aleatória de `k` LSs de `S \ SLS(g_i)` | Algorithm 1, linha 17 | mesmo seed |
| 3 | Escolha aleatória de `k` LSs de `SLS(g_i)` | Algorithm 1, linha 21 | mesmo seed |
| 4 | Desempate em "largest MF value" | Algorithm 1, linha 12 | ordem crescente de identificador do subgrafo frequente |
| 5 | Ordem de iteração sobre `g_i ∈ S` | Algorithm 1, linha 5 | ordem crescente de identificador |

> **Nota sobre dependência entre fontes:** As Fontes 4 e 5 são
> pré-condições do caminho de execução que leva às Fontes 1–3; fixá-las
> reduz (mas não elimina) a variabilidade. O controle completo requer
> fixar todas as cinco.

Fontes adicionais já tratadas por decisões anteriores:

- **Particionamento**: D-04 substituiu METIS (que tem componentes
  não-determinísticos dependendo da build) por
  `networkx.algorithms.community.kernighan_lin_bisection`, que aceita
  parâmetro `seed` (ver Seção 7).
- **Matching da Fase 1**: D-03 fixa grau como critério primário e índice
  lexicográfico como desempate, eliminando o não-determinismo residual
  (ver Seção 7).

A Fase 2 (isomorfização) é **determinística** dado o agrupamento, a
numeração da Fase 1 e a variante escolhida. A reconexão (Seção 3.3) é
determinística dado o agrupamento e a numeração — não há escolha aleatória
residual.

### 3.4 Implicações para o módulo

- A configuração YAML deve expor a variante de isomorfização como parâmetro
  explícito (`anonymization.isomorphism_mode`), não decisão hardcoded.
- A variante usada deve ser **registrada no log estruturado** da execução,
  junto com seed e parâmetros, para que comparações entre execuções sejam
  interpretáveis.
- O log estruturado deve registrar também o número de arestas modificadas
  **por fase** (Fase 2 intra-grupo e reconexão) separadamente, para
  permitir que o módulo de avaliação de risco identifique qual fonte de
  perturbação domina — e, por consequência, qual análise de utilidade é
  mais relevante para aquela execução específica.
- `validate_k_anonymity` (Seção 4.2) é **agnóstico à variante**: opera
  sobre o grafo de saída `G'`, não sobre o caminho que o algoritmo seguiu
  para chegar lá.
- A política de D-07 (tratamento de LSs com tamanhos diferentes no mesmo
  grupo, a decidir; ver Seção 7) afeta a Fase 1 e potencialmente
  a Seção 3.1 deste documento.

---

## 4. Critério de parada e garantia de k-anonimato

> **Fonte:** He et al. (2009), Seções 2.3 e 3.2; decisões D-05 e D-06.

### 4.1 Critério formal (artigo)

O k-anonimato estrutural é garantido **por construção**: se o algoritmo
termina com todos os grupos formados, se os grupos são disjuntos e se todas
as LSs de cada grupo completo são isomorfizadas entre si, então todo nó em
`G'` satisfaz a Def. 2 (p. 649). O artigo não propõe um verificador separado
— a garantia é dedutiva, não verificada a posteriori.

### 4.2 Verificação empírica independente

Para fins deste módulo (avaliação de risco de reidentificação), a garantia
teórica é necessária mas não suficiente. O esboço ingênuo de checar apenas
isomorfismo par-a-par dentro de cada grupo é **mais fraco** que a Def. 2.
A equivalência só vale se duas premissas forem satisfeitas simultaneamente:

1. todo grupo tem cardinalidade `≥ k`; e
2. os grupos são disjuntos.

A primeira premissa **não vale** para o grupo incompleto previsto ao final do
Algorithm 1. Portanto, o verificador empírico precisa checar três condições:

- cardinalidade mínima do grupo (`|G_r| ≥ k`);
- isomorfismo mútuo dentro de cada grupo completo;
- disjunção entre LSs (invariante da partição).

```python
# esboço — implementação completa em metrics_definitions.md
def validate_k_anonymity(groups: list[list[nx.Graph]], k: int) -> dict:
    result = {"valid": True, "violations": []}

    # Condição 1: disjunção global entre LSs
    seen_nodes = set()
    for i, group in enumerate(groups):
        for ls in group:
            overlap = seen_nodes & set(ls.nodes())
            if overlap:
                result["violations"].append(
                    {"type": "non_disjoint", "group": i, "nodes": sorted(overlap)}
                )
                result["valid"] = False
            seen_nodes.update(ls.nodes())

    # Condições 2 e 3: cardinalidade + isomorfismo
    for i, group in enumerate(groups):
        if len(group) < k:
            result["violations"].append(
                {"type": "incomplete_group", "group": i,
                 "size": len(group), "required": k,
                 "status": "partially_unprotected"}
            )
            result["valid"] = False
            continue

        reference = group[0]
        for j, ls in enumerate(group[1:], 1):
            if not nx.is_isomorphic(reference, ls):
                result["violations"].append(
                    {"type": "non_isomorphic", "group": i, "ls_index": j}
                )
                result["valid"] = False

    return result
```

> → Implementação completa, parâmetros, logging e casos de borda definidos em
> `docs/metrics_definitions.md` §k-anonymity-verifier.

### 4.3 Grupo incompleto — decisão operacional

**Decisão D-06:** grupos incompletos serão mantidos e reportados como
**violação parcial de k-anonimato**, com nós residuais tratados como
**desprotegidos** do ponto de vista da garantia formal. O módulo não forçará
fusão artificial nem descarte desses grupos no baseline.

Implicação: o verificador nunca deve retornar `True` para um conjunto de
saída que contenha grupo com `|G_r| < k`, ainda que as LSs desse grupo sejam
mutuamente isomorfas.

### 4.4 Risco declarado do verificador

> ⚠️ **Risco metodológico 1:** Graph Isomorphism (GI) não é sabidamente
> polinomial nem NP-completo. Na prática, `networkx.is_isomorphic` (VF2)
> é eficiente para subgrafos pequenos (`d ≤ 20` nós), mas pode apresentar
> degradação significativa de desempenho para LSs maiores. Para `d > 20`,
> avaliar substituição por heurísticas de isomorfismo aproximado ou limitar
> `d` via configuração.
>
> ⚠️ **Risco metodológico 2:** um verificador que cheque apenas isomorfismo
> intra-grupo pode produzir falso positivo metodológico — "verde" para uma
> medida auxiliar mais fraca que a Def. 2. Por isso, a checagem de
> cardinalidade mínima e disjunção é obrigatória.

---

## 5. Parâmetros e configuração

*(a preencher)*

Mapear para as chaves do YAML de configuração ([config_example.yml](../config_example.yml)):

| Parâmetro do artigo | Chave YAML | Valor(es) usados |
|---|---|---|
| `k` | `anonymization.k_values` | [2, 5, 10, 20] |
| `d` | `anonymization.d` | 10 (default) — ver D-02 |
| `σ` (suporte FSM) | *(a mapear)* | |
| `s_max` (FSM simplificado) | `anonymization.fsm.max_size` | 4 (proposto) — ver D-01 |
| Variante de isomorfização | `anonymization.isomorphism_mode` | `"add_or_delete"` (default) — alternativa: `"add_only"` |

---

## 6. Casos especiais e limitações documentadas no artigo

*(a preencher)*

Exemplos de casos que podem exigir tratamento especial:
- Grafos desconectados
- Nós isolados
- Grafos muito densos

---

## 7. Decisões de implementação

> Registro contínuo. Atualizar à medida que novas decisões forem tomadas
> durante o processo de implementação.

| ID | Data | Decisão | Justificativa | Referência |
|---|---|---|---|---|
| D-01 | 2026-05-17 | FSM simplificado com `s_max` configurável (não gSpan completo) | Pragmatismo de prazo; gSpan Python tem manutenção irregular. `s_max` limita espaço de busca de forma auditável. Declarar como aproximação no relatório. | Artigo cita [18] (Wörlein et al. 2005) sem especificar implementação |
| D-02 | 2026-05-17 | `d = 10` como default; variável de configuração YAML (`anonymization.d`) | Valor comum na literatura derivada para redes de 1k–10k nós. Varredura sobre `d` excluída do escopo mínimo. | Artigo não fixa default; experimentos usam valores variados (p. 652) |
| D-03 | 2026-05-17 | Matching Fase 1: grau como critério primário; índice de nó lexicográfico como desempate | Garante determinismo e reprodutibilidade. Artigo diz "based on nodes degree" sem critério de desempate (p. 651). Escolha afeta `G'` e deve ser reportada como parâmetro de reprodutibilidade. | Artigo p. 651, Seção 3.2, Fase 1 |
| D-04 | 2026-05-17 | Substituir METIS por `networkx.algorithms.community.kernighan_lin_bisection` recursivo | Zero dependência C externa; portabilidade em CI/CD. Substituição explicitamente autorizada pelo artigo: "though any other technique could also be used" (p. 650). Complexidade KL: `O(|E|·log|V|)` vs `O(|E|)` do METIS — aceitável para protótipo. | Artigo p. 650, Seção 3.1 |
| D-05 | 2026-05-17 | Critério formal de k-anonimato registrado neste documento (Seção 4.1); verificador empírico (`nx.is_isomorphic` / VF2) definido em `metrics_definitions.md` | Separação de responsabilidades: `algorithm_notes.md` descreve o algoritmo; `metrics_definitions.md` define os instrumentos de avaliação. Risco de desempenho do VF2 para `d > 20` declarado (Seção 4.4). | Seção 4 deste documento; `docs/metrics_definitions.md` §k-anonymity-verifier |
| D-06 | 2026-05-17 | Grupos incompletos serão mantidos e reportados como violação parcial; nós residuais tratados como desprotegidos | O esboço de verificação por isomorfismo intra-grupo é mais fraco que a Def. 2. Como o Algorithm 1 admite grupo final com `|G_r| < k`, o módulo deve marcar esses casos como falha parcial da garantia, não como sucesso. | Seções 4.2–4.3 deste documento; Def. 2 do artigo |
| D-07 | *(a decidir antes da Semana 2)* | Política para LSs de tamanhos diferentes no mesmo grupo (consequência operacional de D-04) | Artigo assume `\|V_i\| = d`; KL aproxima. Opções: restringir grupos a LSs do mesmo tamanho; padding com nós isolados; outra. Escolha afeta Seção 3.1 e Fase 1 da isomorfização. | Seção 3.1 deste documento; D-04 |

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
