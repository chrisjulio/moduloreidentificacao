# Notas de Implementação — [He et al. (2009)](https://doi.org/10.1109/WI-IAT.2009.108)

> Registro passo a passo do algoritmo de anonimização estrutural.
> Preencher progressivamente durante a Semana 1 (15–22/05/2026) à medida que
> a leitura do artigo avança. Cada seção deve ser atualizada antes de iniciar
> a implementação correspondente.

## 1. Conceito central: k-anonimato estrutural

> **Escopo desta seção:**
> vocabulário conceitual fundamentado nas três perguntas do esqueleto e nas
> quatro definições formais da Seção 2 do artigo (pp. 647–649).
> A decomposição operacional do algoritmo (partição, grouping, isomorfização,
> reconexão) é objeto das Seções 2 e 3 deste documento — issues subsequentes.

### 1.0 Nota terminológica: "grupo de equivalência" vs. k-group de estruturas locais

O termo **grupo de equivalência** não aparece em [He et al. (2009)](https://doi.org/10.1109/WI-IAT.2009.108). O construto
operacionalmente equivalente no artigo é o conjunto de `k` Local Structures
agrupadas pela etapa de *grouping* (Seção 3.2, p. 650); os autores não
atribuem um nome específico a esse conjunto — ele é simplesmente referenciado
como "a group" ou `G_r` no Algorithm 1.

O vocabulário de **grupo de equivalência** vem da literatura de anonimização
tabular (tipicamente associado a k-anonymity sobre dados relacionais, ex.
[Sweeney, 2002](https://doi.org/10.1142/S0218488502001648)). Usamos a expressão por conveniência, como ponte para
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

- **k-degree anonymity** ([Liu & Terzi](https://doi.org/10.1145/1376616.1376629)): baseia-se só no grau,
  ignorando estrutura. *"[...] this anonymization process completely ignores
  structural information inherent in the graph data."* (p. 647, Seção 1)
- **1-neighborhood isomorphism** ([Zhou & Pei](https://doi.org/10.1109/ICDE.2008.4497459)): raio fixo (1-hop)
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

> **Fonte:** [He et al. (2009)](https://doi.org/10.1109/WI-IAT.2009.108), Seção 3, pp. 649–652.

### 2.1 Visão geral — três etapas encadeadas

> ⚠️ **Nota de reconciliação (20/05/2026):** O pseudocódigo abaixo foi atualizado
> para refletir o contrato do skeleton `src/anonymization/he2009.py` (criado em #33).
> O algoritmo de partição primário passa a ser **multilevel k-way ([Karypis & Kumar](https://doi.org/10.1137/S1064827595287997))**,
> fiel à referência [14] do artigo. `kernighan_lin_bisection` permanece como fallback
> documentado (D-04 revisado). Ver Seção 7.

```
Entrada:  G = (V, E),  k (privacidade),  d (tamanho de cada LS em nós),
          σ (suporte FSM — threshold de frequência),
          s_max (tamanho máximo de subgrafo para FSM simplificado)
Saída:    G' = (V, E')  structure-aware k-anonymous

─────────────────────────────────────────────────────────────
Etapa 1 — PARTIÇÃO  (Seção 3.1)
─────────────────────────────────────────────────────────────
1.1  Calcular ck = ⌊|V| / d⌋          // número de partições
1.2  Aplicar particionamento k-way em G
     → Primário:  multilevel k-way ([Karypis & Kumar](https://doi.org/10.1137/S1064827595287997), via pymetis)
     → Fallback:  kernighan_lin_bisection recursivo (D-04; sem dependência C)
     → produz subconjuntos V₁, V₂, ..., V_{ck} de tamanho ≈ d
        tal que arestas inter-partição são minimizadas
1.3  Para cada i: construir Cᵢ = G.subgraph(Vᵢ)   // subgrafo induzido
1.4  Remover temporariamente as arestas inter-partição de G
     → conjunto de arestas removidas: E_inter
     → saída: {LS₁, LS₂, ..., LS_{ck}}

─────────────────────────────────────────────────────────────
Etapa 2 — AGRUPAMENTO E ISOMORFIZAÇÃO  (Seção 3.2 / Algorithm 1)
─────────────────────────────────────────────────────────────
2.1  Executar FSM simplificado({LS₁..LS_{ck}}, σ, s_max)         [D-01]
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
| Partição (multilevel k-way / METIS) | `O(|E|)` | Declarada no artigo (p. 650) |
| Partição (KL bisection recursivo — fallback D-04) | `O(|E| · log |V|)` | Interpretativa; complexidade padrão de KL na literatura |
| FSM simplificado (enumeração até `s_max`) | `O(|LS|^s_max)` por LS — controlado por `s_max` | Interpretativa — não declarada no artigo |
| Agrupamento (Algorithm 1) | `O(c_k · m)` por iteração; `c_k/k` iterações → `O(n·m / d·k)` | Interpretativa |
| Isomorfização (Fases 1+2) | `O(k · |V(LS)|²)` por grupo | Interpretativa |
| Reconexão | `O(|E_inter| · k²)` | **Confirmada empiricamente** — fórmula k(k−1) validada por `TestReconnectKTimesKMinusOne` (k∈{2,3}, PR #98, G3 issue #80); válida para posições canônicas distintas (caso geral). Ver §3.2.2. |

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

As lacunas identificadas nesta seção geraram as decisões D-01 a D-07
registradas na Seção 7. Referências cruzadas marcadas com `[D-xx]` ao longo
do pseudocódigo acima.

---

## Backend de particionamento (`partition_graph`)

### Comportamento por backend

`partition_graph(g, ck, seed, backend)` particiona o grafo em `ck`
subconjuntos disjuntos. O backend é selecionado assim:

- `backend="pymetis"`: usa pymetis; garante particionamento balanceado.
- `backend="networkx-kl"`: bissecção Kernighan-Lin aplicada
  recursivamente até atingir `ck` partições.
- `backend="auto"`: usa pymetis se disponível; caso contrário recai
  para `networkx-kl` emitindo um `UserWarning` (D-04).

### Limitação conhecida do fallback KL (D-07)

A bissecção KL recursiva garante apenas **contagem de partições** e
**cobertura total e disjunta** dos nós. Ela **não garante balanceamento
de tamanho** para `ck > 2`: partições individuais podem ser menores que
`len(g) / ck`. O balanceamento exato é propriedade exclusiva do backend
pymetis.

Os testes em `tests/anonymization/test_partition_backend.py` verificam,
para o caso KL, contagem e cobertura — não tamanho exato — de forma
consistente com essa limitação.

### Implicação para a validação de k-anonimato (Seção 7 do planejamento)

Como uma partição sob o fallback KL pode ser menor que o tamanho de
grupo pretendido, o k-anonimato pode não ser atingido por esse backend.
Consequências operacionais:

- A verificação de sanidade obrigatória do marco de 29/05 deve rodar
  com `backend="pymetis"`.
- Se for executada com `backend="networkx-kl"`, um grupo de
  equivalência menor que k **não invalida o algoritmo** — apenas
  confirma a limitação documentada aqui. Esse caso deve ser registrado
  explicitamente, não tratado como falha de implementação.

---

## 3. Operações de modificação do grafo

> **Fontes:** [He et al. (2009)](https://doi.org/10.1109/WI-IAT.2009.108), Seções 3.2 (Phase 2, p. 651) e 3.3 (p. 652).

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
> A garantia depende de `|V_i| = d` (igualdade estrita), que com KL (D-04)
> passa a aproximação. LSs no mesmo grupo podem ter contagens de nós distintas.
>
> ⚠️ **D-07 formalizado (20/05/2026):** Adotada a **Opção A** — restrição
> de grupos a LSs do mesmo `|Vi|`. LSs sem grupo completo do mesmo tamanho
> são tratadas como grupo incompleto (D-06). Esta política é aplicada
> exclusivamente em `_partition_backend.py` (issue #45), sendo transparente
> para `_partition_neighborhoods` (#11), `_group_isomorphic` (#12) e
> `_modify_structure` (#13). Declarada como **limitação do protótipo**
> no relatório de qualificação. A produção poderia usar `tpwgts` do pymetis
> para forçar partições exatas, mas essa opção não é mandatória para o marco
> de 29/05/2026. Ver Seção 7 (D-07).

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
resolvido automaticamente pelo algoritmo. Desde B6 (#105) é uma chave YAML
ativa — `anonymization.isomorphism_mode` (`"add_or_delete"` | `"add_only"`;
default `"add_or_delete"`) — lida pelo runner e propagada a
`_modify_structure(add_only=...)`. Mapeamento completo na Seção 5.1.

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

> **Status (G3, issue #80 — confirmado em 02/06/2026, PR #98):** A fórmula
> `k(k−1)` foi validada empiricamente por `TestReconnectKTimesKMinusOne`
> para k ∈ {2, 3}. Aplica-se quando os extremos da inter-aresta ocupam
> **posições canônicas distintas** (D-03) — o caso geral descrito no artigo.
> Dois casos especiais emergem da construção não-direcionada:
>
> - **Mesma posição canônica:** os pares ordenados (i, j) colapsam →
>   C(k,2) = k(k−1)/2 arestas (clique dentro da posição).
> - **LSs de 1 nó (degenerate):** ambos os extremos na posição 0 →
>   apenas a inter-aresta original (1 aresta), não k(k−1). O esboço
>   literal da issue #80 era incorreto; o núcleo está correto.
>
> A estimativa `O(|E_inter| · k²)` permanece válida para o caso geral.
> A docstring de `_reconnect_inter_edges` e a nota sob D-08 em
> `docs/decision_log.md` registram essa distinção de casos.

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

- **Particionamento**: D-04 (revisado em 20/05/2026) define multilevel k-way
  via `pymetis` como primário (aceita `seed` implícito pela inicialização
  aleatória do METIS) e `kernighan_lin_bisection` como fallback (aceita
  parâmetro `seed`). Ver Seção 7.
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
  **Implementado em B6 (#105):** o runner lê `anonymization.isomorphism_mode`
  (`"add_or_delete"` | `"add_only"`; default `"add_or_delete"`) e a propaga a
  `anonymize()` → `_modify_structure(add_only=...)`.
- A variante usada deve ser **registrada no log estruturado** da execução,
  junto com seed e parâmetros, para que comparações entre execuções sejam
  interpretáveis. **Implementado em B6 (#105):** o valor efetivo de
  `isomorphism_mode` é gravado em cada entrada JSONL e no `summary.json`.
- O log estruturado deve registrar também o número de arestas modificadas
  **por fase** (Fase 2 intra-grupo e reconexão) separadamente, para
  permitir que o módulo de avaliação de risco identifique qual fonte de
  perturbação domina — e, por consequência, qual análise de utilidade é
  mais relevante para aquela execução específica.
- `validate_k_anonymity` (Seção 4.2) é **agnóstico à variante**: opera
  sobre o grafo de saída `G'`, não sobre o caminho que o algoritmo seguiu
  para chegar lá.
- A política de D-07 (**Opção A formalizada em 20/05/2026**) é aplicada
  exclusivamente em `_partition_backend.py` (#45), sendo transparente para
  as demais funções do pipeline. Ver Seção 3.1 e D-07 na Seção 7.

---

## 4. Critério de parada e garantia de k-anonimato

> **Fonte:** [He et al. (2009)](https://doi.org/10.1109/WI-IAT.2009.108), Seções 2.3 e 3.2; decisões D-05 e D-06.

### 4.1 Critério formal do artigo

O artigo trata o k-anonimato estrutural como propriedade **garantida por
construção**, não como invariante verificada a posteriori. A garantia é
dedutiva: se (a) cada grupo formado contém exatamente `k` Local Structures,
(b) as LSs em cada grupo têm o mesmo número de nós **— condição que a
Fase 1 pressupõe para terminar o matching** (ver Seção 3.1: *"Since each
of local structures in the same group has the same number of nodes, this
process will terminate quickly"*, p. 651) —, e (c) a Fase 2 da
isomorfização opera corretamente, então todo nó em `G'` satisfaz a Def. 2
(p. 649). O artigo não propõe um verificador separado.

> **As três premissas não são automaticamente preservadas pela
> implementação.** D-06 (grupo final incompleto) viola (a); D-07
> (LSs de tamanhos diferentes no mesmo grupo) potencialmente viola (b).
> D-07 foi formalizado em 20/05/2026 com a **Opção A**: grupos são
> restritos a LSs do mesmo `|Vi|`, e LSs sem grupo completo caem em D-06.
> Isso preserva a premissa (b) para os grupos que se formam, mas pode
> aumentar o número de violadores via D-06. O verificador empírico da
> Seção 4.2 torna esse subconjunto explícito.

### 4.2 Verificação empírica independente

A verificação opera sobre o grafo de saída `G'` e a estrutura de grupos
produzida pelo algoritmo. Ela responde a uma pergunta operacional: dado
o que o algoritmo de fato produziu, quantos nós satisfazem a Def. 2 para
o `k` configurado?

#### 4.2.1 Verificador estrito (Def. 2 no nível do nó)

```python
# Esboço — implementação completa em docs/metrics_definitions.md
def validate_k_anonymity_strict(
    G_prime: nx.Graph,
    groups: list[list[nx.Graph]],   # cada LS é subgrafo induzido em G_prime
    k: int
) -> dict:
    """
    Retorna estatísticas por nó:
      - 'satisfies': fração de nós com >= k-1 outros nós com LS isomorfa
      - 'violators': lista de nós que não satisfazem Def. 2
      - 'per_ls': contagem de candidatos isomorfos disponíveis por LS
    """
    # Nota: iteração restrita ao grupo de anonimização — conservador.
    # A Def. 2 não restringe candidatos ao mesmo grupo; LSs isomorfas em
    # grupos distintos também satisfariam a condição. O verificador pode
    # subestimar 'count' e produzir falsos negativos de violação.
    # Comportamento conservador: aceitável para fins de auditoria.

    # 1. Para cada LS, conta nós em outras LSs isomorfas (no mesmo grupo)
    iso_counts = {}
    for i, group in enumerate(groups):
        for j, ls in enumerate(group):
            count = 0
            for j2, other_ls in enumerate(group):
                if j2 != j and nx.is_isomorphic(ls, other_ls):
                    count += other_ls.number_of_nodes()
            iso_counts[(i, j)] = count

    # 2. Cada nó herda a contagem da LS a que pertence
    violators = [
        node
        for (i, j), count in iso_counts.items()
        for node in groups[i][j].nodes()
        if count < k - 1
    ]
    return {
        'satisfies': 1 - len(violators) / G_prime.number_of_nodes(),
        'violators': violators,
        'per_ls': iso_counts,
    }
```

O verificador estrito é **estritamente mais forte** que o esboço anterior
(que apenas checava isomorfismo par-a-par dentro de cada grupo, retornando
booleano): ele captura corretamente os dois casos em que a garantia por
construção falha — grupo final incompleto (D-06) e LSs com contagens de
nós insuficientes para somar `k−1` candidatos isomorfos fora da LS de
origem (D-07). Com a adoção de D-07 Opção A, os violadores residuais
devem ser atribuíveis exclusivamente a D-06 (grupos incompletos), não
a desbalanceamento de tamanho dentro de um grupo completo.

> → Implementação completa, parâmetros e casos de borda em
> [`docs/metrics_definitions.md` §k-anonymity-verifier](metrics_definitions.md#k-anonymity-verifier) (issue #34).

#### 4.2.2 Critério de passagem do marco intermediário (29/05/2026)

- Para a configuração de validação (sugestão: `k=5`, uma ego-rede do
  Facebook, `d=10`), o verificador estrito retorna `satisfies == 1.0` em
  pelo menos 1 das 3 sementes — **e** o número de violadores nas demais
  sementes **não excede o número de nós no grupo final incompleto** (D-06).
  Caso exceda, a causa é investigada antes de prosseguir.
- Resultado `satisfies < 1.0` em todas as 3 sementes para a configuração
  de validação, ou violadores acima do limite de D-06, dispara
  reformulação do escopo conforme Seção 7 do plano operacional, não
  acomodação.

Diferença em relação à redação anterior do critério: registrar a fração
de nós que satisfazem Def. 2 (não apenas True/False) dá visibilidade ao
subconjunto problemático e permite distinguir falha pequena (poucos
violators, atribuíveis a grupo incompleto) de falha estrutural (muitos
violators, sugerindo bug na isomorfização).

### 4.3 Riscos do verificador

#### 4.3.1 Custo computacional do isomorfismo

> ⚠️ Graph Isomorphism (GI) não é sabidamente polinomial nem NP-completo.
> `networkx.is_isomorphic` (VF2) é eficiente para subgrafos pequenos
> (`d ≤ 20`), mas pode degradar significativamente para LSs maiores. Para
> `d > 20`, avaliar pré-filtro por invariantes baratos (distribuição de
> graus, espectro do laplaciano) antes da chamada a VF2, ou limitar `d`
> via configuração.

O custo do verificador é dominado por chamadas a `is_isomorphic` entre
pares de LSs dentro de cada grupo: para `c` grupos de tamanho `k`, são
`c · k·(k−1)/2` chamadas, cada uma sobre LSs de tamanho aproximadamente
`d`. O custo total escala com `c · k²` chamadas a um procedimento cuja
complexidade depende fortemente de `d` e da estrutura das LSs.

#### 4.3.2 Acoplamento com o algoritmo

O próprio algoritmo de anonimização usa isomorfismo internamente na Fase 2.
Se VF2 é o gargalo, ele é gargalo nos dois lados — não apenas no
verificador. A faixa de `d` viável é, portanto, propriedade conjunta do
par (algoritmo, verificador), não do verificador isoladamente.

#### 4.3.3 Independência do verificador em relação ao algoritmo

O verificador é **independente** no sentido de que não reutiliza a lógica
de isomorfização da Fase 2: ele aplica VF2 sobre os grafos produzidos, não
confia em bookkeeping interno. Mas ele **reutiliza a estrutura de grupos**
que o algoritmo produziu — aceita como entrada o mapeamento
`nó → LS → grupo`. Essa escolha troca independência completa por
reprodutibilidade: re-particionar `G'` independentemente introduziria
não-determinismo adicional (D-04) sem ganho informativo proporcional.

> **Escopo da certificação:** o verificador certifica que *o algoritmo
> cumpriu sua promessa dada a partição produzida*, não que *G' é
> estruturalmente k-anônimo para qualquer particionamento alternativo
> de G'*. A segunda afirmação é mais forte, não está coberta, e deve
> ser listada como ameaça à validade externa no relatório de qualificação.

### 4.4 Relação com os ataques de reidentificação

A verificação de Def. 2 não substitui as métricas de ataque (por grau,
por subgrafos, por entropia) definidas no plano operacional. As duas
avaliações respondem a perguntas distintas:

| Avaliação | Pergunta |
|---|---|
| Verificador estrito de Def. 2 (Seção 4.2) | O algoritmo cumpre sua garantia teórica? |
| Ataques por grau / subgrafos / entropia | Que fração de nós um adversário realista consegue reidentificar? |

A garantia teórica é uma **cota superior** sobre a confiança de
reidentificação (`≤ 1/k`); os ataques medem a confiança **efetiva** sob
modelos adversariais específicos. A diferença entre as duas é, em si, um
dado interessante: se um ataque consegue reidentificação significativamente
acima de `1/k`, isso indica que o modelo adversarial usado tem conhecimento
que escapa do que a Def. 2 considera — e o resultado deve ser reportado
como tal, não como falha do algoritmo.

---

## 5. Parâmetros e configuração

> **Referência cruzada:** `docs/limitations.md` §1.3, §2.1–2.3 (impacto
> metodológico de cada parâmetro); `docs/decision_log.md` (histórico de
> decisões D-01 a D-07).

Esta seção reconcilia os parâmetros formais do artigo com as chaves
concretas do arquivo `config_example.yml`, distinguindo parâmetros já
expostos em YAML, parâmetros ainda internos à implementação e parâmetros
que, embora conceitualmente presentes em [He et al. (2009)](https://doi.org/10.1109/WI-IAT.2009.108), ainda não têm
mapeamento operacional completo no protótipo.

### 5.1 Mapeamento dos parâmetros do artigo para YAML

| Parâmetro do artigo | Papel no algoritmo | Chave YAML | Valor(es) usados / planejados |
|---|---|---|---|
| `k` | nível de privacidade; mínimo de candidatos indistinguíveis por nó | `anonymization.k` (lida pelo runner; aceita int ou lista) | `[2, 5, 10, 20]` no baseline |
| `d` | tamanho pretendido de cada Local Structure / partição | **`anonymization.d`** — **lida do YAML** pelo runner; exposta no `config_example.yml` (S8-3, #106) | `10` como default conceitual (D-02); baseline de validação executado com `d=1` (achado B1) |
| `σ` | suporte mínimo para o FSM | **`anonymization.sigma`** — **lida do YAML** pelo runner; exposta no `config_example.yml` (S8-3, #106) | `0.5` (default) na varredura de k (Seção 9) |
| `s_max` | tamanho máximo de subgrafo no FSM simplificado | **`anonymization.s_max`** (alias `anonymization.fsm_max_size`) — **lida do YAML** pelo runner e propagada a `anonymize()`/`_group_isomorphic()` (B5, #104); exposta no `config_example.yml` (S8-3, #106) | `4` (default) — ver D-01; valor efetivo gravado no JSONL |
| Variante de isomorfização | política de modificação intra-grupo (Phase 2) | **`anonymization.isomorphism_mode`** — **lida do YAML** pelo runner e propagada a `anonymize()` → `_modify_structure(add_only=...)` (B6, #105); exposta no `config_example.yml` (S8-3, #106) | `"add_or_delete"` (default); alternativa `"add_only"`; valor efetivo gravado no JSONL |
| Motor de partição | backend da Etapa 1 | *(não exposto em `config_example.yml` atual; previsto como `anonymization.partition_backend`)* | `"auto"` (default planejado) → pymetis se disponível, KL fallback |
| Verificação empírica do k-anonimato | auditoria pós-anonimização | `anonymization.validate_k_anonymity` | `true` no exemplo atual |
| Sementes aleatórias | controle de reprodutibilidade | `seeds` | `[42, 1337, 2718]` |

### 5.2 Alinhamento entre o YAML de exemplo e o estado do protótipo

Desde S8-3 (#106), o `config_example.yml` de referência expõe `k`, `d`,
`sigma`, `s_max` (alias `fsm_max_size`) e `isomorphism_mode` — todas
**efetivamente lidas** pelo runner (`experiments/run.py`) — além de
`validate_k_anonymity` e `allow_kl_fallback`. A defasagem histórica (a
documentação conceitual adiantada à interface pública) foi assim **fechada**
para esses parâmetros. A chave `k` foi corrigida no exemplo (antes versionada
como `k_values`, que o runner não lê) para refletir a interface real e não
documentar configurabilidade fantasma — a mesma classe de erro que originou
B5/B6.

O único parâmetro de He et al. ainda **não exposto** como chave estável é o
**motor de partição** (`partition_backend`), definido conceitualmente e nas
decisões (D-04) mas não lido como chave YAML — apenas `allow_kl_fallback`
controla a política de fallback. `validate_k_anonymity` permanece exposta como
documentação de política, embora a auditoria do runner atual rode sempre
(chave reservada para tornar a auditoria opcional no futuro).

> **Atualização (B5, #104):** `s_max` deixou de ser fixo no código. O runner
> de experimentos (`experiments/run.py`) agora **lê** a chave
> `anonymization.s_max` (alias `fsm_max_size`) do YAML do experimento, a
> propaga a `anonymize()` → `_group_isomorphic()` e grava o valor efetivo no
> JSONL de saída. A exposição da chave no `config_example.yml` de referência
> é tratada separadamente em S8-3 (#106).

> **Atualização (B6, #105):** a variante de isomorfização deixou de ser uma
> constante `add_only=False` hardcoded. O runner (`experiments/run.py`)
> agora **lê** a chave `anonymization.isomorphism_mode` (valores
> `"add_or_delete"` | `"add_only"`; default `"add_or_delete"`), valida o
> valor antes do laço de execução, a propaga a `anonymize()` (que a converte
> em `add_only`) e ao caminho inline (`_modify_structure(add_only=...)`), e
> grava o valor efetivo no JSONL e no `summary.json`. A exposição da chave no
> `config_example.yml` de referência é tratada em S8-3 (#106).

### 5.3 Parâmetros efetivamente confirmados no baseline

A Seção 9 deste documento registra os parâmetros usados na varredura de `k`
já executada:

- `k ∈ {2, 5, 10, 20}`
- `d = 1`
- `sigma = 0.5`
- sementes `= [42, 1337, 2718]`
- dataset: ego-rede 3437 do Facebook Ego-Nets

Para fins de rastreabilidade metodológica, o estado atual do protótipo
deve ser lido assim:

1. **`k` e validação** já estão representados no YAML público;
2. **`d` e `sigma`** são **lidos do YAML** pelo runner e, desde S8-3 (#106),
   estabilizados também no `config_example.yml` de referência (além dos YAMLs
   experimentais);
3. **`s_max`** (`anonymization.s_max`, alias `fsm_max_size`, B5/#104) e
   **`isomorphism_mode`** (`anonymization.isomorphism_mode`, B6/#105) são
   **lidos do YAML** pelo runner, gravados no JSONL e, desde S8-3 (#106),
   expostos no `config_example.yml` de referência. **`partition_backend`**
   permanece definido conceitualmente e nas decisões do documento, ainda não
   exposto como chave YAML.

### 5.4 Requisitos de documentação para #26-B

A documentação técnica subsequente (#26-B) deve tornar explícitos, para
cada parâmetro exposto:

- nome da chave YAML;
- tipo esperado (`int`, `float`, `list[int]`, `str`, `bool`);
- valor default;
- faixa ou conjunto de valores válidos;
- efeito metodológico do parâmetro;
- impacto esperado em custo computacional, utilidade e privacidade;
- se o parâmetro já está implementado, parcialmente implementado ou apenas
  documentado para versões futuras.

Essa exigência é particularmente importante para `d`, `sigma`,
`partition_backend` e `isomorphism_mode`, porque são precisamente os
parâmetros que mais afetam a interpretação dos resultados e as limitações
registradas em `docs/limitations.md`.

---

## 6. Casos especiais e limitações documentadas no artigo

> **Referência cruzada:** `docs/limitations.md` (classificação formal das
> limitações); esta seção caracteriza os **cenários** em que elas tendem
> a se manifestar com maior clareza.

Esta seção registra casos de borda e classes de grafos para as quais o
artigo ou a implementação atual exigem cautela interpretativa. O objetivo
não é expandir o algoritmo, mas delimitar onde sua aplicação é direta,
onde é apenas plausível e onde depende de validação empírica adicional.

### 6.1 Grafos desconectados

[He et al. (2009)](https://doi.org/10.1109/WI-IAT.2009.108) formulam o algoritmo sobre um grafo geral `G = (V, E)`,
mas a definição de Local Structure pressupõe um subgrafo **conectado**.
Na prática, quando o grafo original é desconectado, o pipeline precisa
escolher entre processar cada componente conexa separadamente ou restringir
a análise à maior componente conexa.

O projeto adotou explicitamente a segunda estratégia no pré-processamento:
`component: lcc` em `config_example.yml`, retendo apenas a maior componente
conexa da ego-rede. Essa decisão simplifica a interpretação estrutural do
algoritmo e evita que componentes triviais ou muito pequenas distorçam o
agrupamento e as métricas de utilidade.

**Implicação metodológica:** os resultados do baseline dizem respeito à
LCC da rede selecionada, não ao grafo bruto integral. Isso deve ser
reportado como recorte deliberado, não como comportamento genérico do
algoritmo sobre grafos arbitrariamente desconectados.

### 6.2 Nós isolados

Nós isolados constituem um caso especial importante porque sua Local
Structure, no limite, coincide com um subgrafo unitário sem arestas.
Sob `d=1`, esse caso é trivial: todos os nós isolados são mutuamente
isomorfos entre si. Sob `d>1`, a incorporação de nós isolados a LSs
maiores pode produzir partições estruturalmente pouco informativas e
artificialmente fáceis de anonimizar.

O pipeline corrente mitiga esse problema indiretamente ao operar sobre a
maior componente conexa (`component: lcc`), o que tende a eliminar nós
isolados do domínio efetivo de análise. Se o módulo vier a ser usado sobre
grafos nos quais nós isolados persistam após o pré-processamento, esse
caso deve ser tratado explicitamente no relatório experimental.

**Implicação metodológica:** anonimização bem-sucedida sobre nós isolados
não constitui evidência forte de preservação de privacidade estrutural em
redes densamente relacionais; é um caso trivial do modelo.

### 6.3 Grafos muito densos

Grafos muito densos representam um caso de atenção por duas razões:

1. a distinção entre adição e remoção de arestas na Fase 2 tende a se
   comportar de forma diferente da observada em grafos esparsos;
2. a reconexão pode impor custo estrutural elevado, especialmente se o
   particionamento inicial não conseguir minimizar suficientemente as
   arestas inter-partição.

He et al. reportam preservação de utilidade em datasets específicos, mas
o artigo não fornece garantia teórica de que a variante `add_or_delete`
terá o mesmo comportamento em grafos muito densos. No protótipo atual,
não há experimento dedicado a esse regime.

**Implicação metodológica:** resultados do baseline em ego-redes do
Facebook (não extremas em densidade) não devem ser extrapolados para
grafos muito densos sem experimentação adicional.

### 6.4 Grafos muito pequenos em relação a `k`

Se o número de LSs disponíveis é pequeno em relação ao `k` configurado,
o agrupamento pode produzir alta proporção de grupos incompletos (D-06),
reduzindo drasticamente `coverage_fraction`. Esse risco é particularmente
agudo em redes pequenas ou após pré-processamentos agressivos.

A decisão de adotar `min_nodes: 200` em `config_example.yml` foi motivada
justamente por esse tipo de risco: manter um tamanho mínimo compatível com
os maiores valores de `k` no escopo mínimo. Ainda assim, o limiar é uma
heurística operacional, não uma garantia formal suficiente para todos os
casos.

**Implicação metodológica:** quando `n` é pequeno relativamente a `k`, a
queda de cobertura pode decorrer da geometria do dataset e não de bug no
anonimizador. O resultado deve ser interpretado à luz de D-06.

### 6.5 Valores de `d > 1`

Embora o artigo formule o modelo para LSs de tamanho variável `d`, a
validação empírica consolidada até o momento foi obtida com `d=1`. Isso
transforma a LS em um caso degenerado, no qual o isomorfismo local se
aproxima da igualdade de grau. Para `d>1`, entram em jogo simultaneamente:

- a qualidade do FSM simplificado (D-01);
- o balanceamento real das partições (D-04/D-07);
- o custo do VF2 no verificador (Seção 4.3.1);
- a possibilidade de violações adicionais além do grupo incompleto.

Portanto, `d>1` não é apenas um novo parâmetro; é uma mudança de regime
experimental. Os resultados já obtidos para `d=1` não devem ser lidos como
prova empírica suficiente do comportamento do algoritmo nesse regime mais
geral.

### 6.6 Relação com `docs/limitations.md`

Os casos especiais desta seção têm interface direta com as limitações
registradas em `docs/limitations.md`:

- grafos desconectados e nós isolados conectam-se ao recorte de escopo do
  dataset e do pré-processamento (§1.1);
- grafos muito densos e `d>1` conectam-se às limitações técnicas relativas
  ao FSM, ao backend de partição e ao custo do VF2 (§2.1, §2.2, §2.5);
- grafos muito pequenos em relação a `k` conectam-se diretamente à decisão
  D-06 (§2.3).

Por essa razão, esta seção deve ser lida como complemento operacional de
`docs/limitations.md`: lá estão classificadas as limitações; aqui estão
caracterizados os cenários em que elas tendem a se manifestar com maior
clareza.

---

## 7. Decisões de implementação

> Registro contínuo. Atualizar à medida que novas decisões forem tomadas
> durante o processo de implementação.

| ID | Data | Decisão | Justificativa | Referência |
|---|---|---|---|---|
| D-01 | 2026-05-17 | FSM simplificado com `s_max` configurável (não gSpan completo) | Pragmatismo de prazo; gSpan Python tem manutenção irregular. `s_max` limita espaço de busca de forma auditável. Declarar como aproximação no relatório. | Artigo cita [18] ([Wörlein et al. 2005](https://doi.org/10.1007/11564126_32)) sem especificar implementação |
| D-02 | 2026-05-17 | `d = 10` como default; variável de configuração YAML (`anonymization.d`) | Valor comum na literatura derivada para redes de 1k–10k nós. Varredura sobre `d` excluída do escopo mínimo. | Artigo não fixa default; experimentos usam valores variados (p. 652) |
| D-03 | 2026-05-17 | Matching Fase 1: grau como critério primário; índice de nó lexicográfico como desempate | Garante determinismo e reprodutibilidade. Artigo diz "based on nodes degree" sem critério de desempate (p. 651). Escolha afeta `G'` e deve ser reportada como parâmetro de reprodutibilidade. | Artigo p. 651, Seção 3.2, Fase 1 |
| D-04 | 2026-05-17 *(revisado 2026-05-20)* | **Motor primário: `pymetis` (multilevel k-way, [Karypis & Kumar](https://doi.org/10.1137/S1064827595287997))**. Motor fallback: `networkx.kernighan_lin_bisection` recursivo, ativado quando `pymetis` não estiver disponível no ambiente (CI sem dependência C) ou via `anonymization.partition_backend: "networkx-kl"`. A divergência entre os dois motores (complexidade `O(\|E\|)` vs `O(\|E\|·log\|V\|)`; qualidade de partição; tamanho de LSs resultante) deve ser reportada como parâmetro metodológico, não como detalhe de implementação. | Artigo cita explicitamente [Karypis & Kumar](https://doi.org/10.1137/S1064827595287997) (p. 650): multilevel k-way é o algoritmo de referência. KL bisection é heurística aparentada mas distinta: opera por bisseção recursiva e não garante `k` partições balanceadas diretamente. Revisão de 20/05/2026 reconcilia D-04 com o skeleton de `_partition_neighborhoods` criado em #33 e com o corpo atualizado da issue #11. | Artigo p. 650, Seção 3.1; skeleton `src/anonymization/he2009.py` (#33); issue #11 (corpo atualizado 20/05/2026) |
| D-05 | 2026-05-17 | Critério formal de k-anonimato registrado na Seção 4.1; **verificador empírico estrito** (Def. 2 no nível do nó, via `nx.is_isomorphic`/VF2) com saída em fração de nós satisfeitos; definido em detalhe em `metrics_definitions.md` | Separação de responsabilidades: `algorithm_notes.md` descreve o algoritmo e o critério; `metrics_definitions.md` define os instrumentos de avaliação. Verificador anterior (booleano par-a-par) era estritamente mais fraco que Def. 2 e mascarava violações decorrentes de D-06 e D-07. Risco de desempenho do VF2 declarado (Seção 4.3). | Seção 4 deste documento; [`docs/metrics_definitions.md` §k-anonymity-verifier](metrics_definitions.md#k-anonymity-verifier) (issue #34) |
| D-06 | 2026-05-17 | Grupos incompletos serão mantidos e reportados como violação parcial; nós residuais tratados como desprotegidos | O verificador estrito captura esses casos como violadores explícitos (count < k-1). O módulo não forçará fusão artificial nem descarte desses grupos no baseline. | Seções 4.1–4.2 deste documento; Def. 2 do artigo |
| D-07 | 2026-05-20 | **Opção A — Restringir grupos a LSs do mesmo `\|Vi\|`.** Na etapa de agrupamento (#12), LSs são indexadas por tamanho; grupos formam-se apenas entre LSs com mesmo número de nós. LSs sem grupo completo do mesmo tamanho → grupo incompleto (D-06). Declarada como **limitação do protótipo** no relatório de qualificação. A política é aplicada exclusivamente em `_partition_backend.py` (#45) — transparente para `_partition_neighborhoods` (#11), `_group_isomorphic` (#12) e `_modify_structure` (#13). Produção futura pode usar `tpwgts` do pymetis para forçar partições exatas de tamanho `d`, mas isso não é mandatório para o marco de 29/05/2026. | Artigo pressupõe `\|V_i\| = d` estrito (p. 651); D-04 produz partições aproximadas. Opção A preserva a premissa formal do artigo para os grupos que se formam, sem introduzir nós fictícios (Opção B) nem violar a premissa (Opção C). Custo: mais violadores via D-06 — já instrumentados pelo verificador estrito (D-05). Discussão completa em issue #43 (fechada 20/05/2026). | Seção 3.1 deste documento; D-04 revisado; issue #43; issue #45 |

---

## 8. Validação: o que "empiricamente atingido" significa

Para o marco de 29/05/2026, a validação de k-anonimato deve ser:

- [x] Verificador estrito implementado **independentemente** do anonimizador
      (não reutilizar código interno do algoritmo).
- [x] Verificador aplicado sobre o grafo de saída G', não sobre estruturas
      internas do algoritmo.
- [x] Resultado registrado em log estruturado, reproduzível via semente.
- [x] Testado em ao menos uma configuração: k=5, uma ego-rede do Facebook,
      `d=1`.

Critério de aprovação: verificador retorna `satisfies == 1.0` em pelo menos
1 das 3 sementes; `violators` nas demais sementes registrados e atribuíveis
a D-06 (grupo final incompleto) — e **não** a desbalanceamento de tamanho
dentro de grupos completos (D-07 Opção A garante que esse segundo caso
não ocorre).

**Marco 29/05/2026: APROVADO** (issue #16, PR #53).
Configuração k=5, d=1, egonet_id=3437: `satisfied_fraction=0.9962` nas 3
sementes; apenas `incomplete_group` (D-06 aceitável).

---

## 9. Resultados da varredura de k — Issue #17

> **Data:** 2026-05-22  
> **Script:** `experiments/run_k_sweep.py`  
> **Configs:** `experiments/configs/he2009_facebook_k_sweep_k{2,10,20}.yml`  
> **Log:** `experiments/logs/k_sweep/sweep_summary.json`  
> **Dataset:** ego-rede 3437 — Facebook Ego-Nets (n_lcc=532, m_lcc=4812)  
> **Parâmetros fixos:** d=1, sigma=0.5, sementes=[42, 1337, 2718]

### 9.1 Tabela de resultados

| k  | Sementes | Veredictos | satisfied_fraction mín. | Status |
|----|----------|------------|------------------------|--------|
| 2  | 42, 1337, 2718 | SUCCESS_FULL × 3 | 1.0000 | **APROVADO** (pleno) |
| 5  | 42, 1337, 2718 | SUCCESS_PARTIAL × 3 | 0.9962 | **APROVADO** (D-06) |
| 10 | 42, 1337, 2718 | SUCCESS_PARTIAL × 3 | 0.9962 | **APROVADO** (D-06) |
| 20 | 42, 1337, 2718 | SUCCESS_PARTIAL × 3 | 0.9774 | **APROVADO** (D-06) |

### 9.2 Análise dos resultados

**k=2 — Sucesso pleno (SUCCESS_FULL):**
Com d=1 e n=532 nós, o algoritmo forma 266 grupos de tamanho exato k=2,
sem grupo incompleto. Cada nó de grau g é emparelhado com outro nó de
mesmo grau (a LS de tamanho 1 é apenas o nó central, cujo isomorfismo
se reduz a igualdade de grau). O resultado `valid=True` e
`satisfied_fraction=1.0000` em todas as 3 sementes confirma que para k=2
o algoritmo satisfaz a garantia formal sem ressalvas.

**k=10 — Sucesso parcial aceitável (D-06):**
Com n=532 e k=10, formam-se 53 grupos completos + 1 grupo incompleto
(nós residuais: 532 − 53×10 = 2 nós). O grupo incompleto gera
`satisfied_fraction = 530/532 ≈ 0.9962`, acima do limiar de 0.9 do
critério DL-01. Resultado idêntico nas 3 sementes — o determinismo do
agrupamento (decisões D-03, D-04) produz partição idêntica para este dataset.
Resultado: APROVADO sob D-06.

**k=20 — Sucesso parcial aceitável (D-06):**
Com n=532 e k=20, formam-se 26 grupos completos + 1 grupo incompleto
(nós residuais: 532 − 26×20 = 12 nós). O grupo incompleto gera
`satisfied_fraction = 520/532 ≈ 0.9774`, ainda acima de 0.9.
Resultado idêntico nas 3 sementes. Nota: à medida que k cresce, a fração
de nós residuais no grupo incompleto aumenta linearmente com k (limitado
por k/n), mas permanece dentro do critério DL-01 para esta ego-rede.
Resultado: APROVADO sob D-06.

### 9.3 Observações metodológicas

1. **Determinismo do agrupamento:** Para todos os valores de k, os veredictos
   foram idênticos nas 3 sementes. Isso indica que a partição primária
   (backend KL, único grupo de tamanho 1 por nó, d=1) é determinística
   para esta ego-rede — a semente afeta apenas a ordem de escolha de LSs
   no `_group_isomorphic`, que com d=1 tem pouca variabilidade. Este
   comportamento deve ser investigado com d>1 onde a partição introduz
   mais variabilidade.

2. **Limite do grupo incompleto:** O padrão `n_residuais = n mod k` é
   esperado para o backend KL com d=1 (cada LS tem tamanho 1). Para d>1,
   o desbalanceamento entre LSs (D-07 Opção A) pode introduzir violações
   adicionais além do grupo incompleto.

3. **Todos os k do escopo Mínimo validados:** k∈{2, 5, 10, 20} aprovados
   sobre egonet_id=3437. O escopo Mínimo de validação empírica está cumprido.

4. **Próximo passo (Semana 3):** Ataques por grau e subgrafos sobre os
   grafos anonimizados gerados por estas configurações. Os logs estruturados
   em `experiments/logs/k_sweep/` servem como entrada para a cadeia de
   análise subsequente.

### 9.4 Resultados da varredura de d (d-sweep) — Issues #88 / #78

> **Data:** 2026-06-02  
> **Experimento:** `he2009_facebook_dsweep` (tier desejável, D-08)  
> **Config:** `experiments/configs/he2009_facebook_dsweep.yml`  
> **Log:** `experiments/logs/he2009_facebook_dsweep/he2009_facebook_dsweep.jsonl`  
> **Dataset:** ego-rede 3437 (n_lcc=532, m_lcc=4812)  
> **Backend:** **pymetis** em todos os 48 runs (D-04); σ=0.5; sementes [42, 1337, 2718]  
> **Grid:** k ∈ {2, 5, 10, 20} × d ∈ {1, 2, 5, 10} × 3 sementes = **48 runs**  
> **Relatório consolidado:** [`docs/results_dsweep.md`](results_dsweep.md)

Enquanto a §9.1 valida a propriedade formal em `d=1`, a varredura de `d`
estende a §1.3 das limitações de *limitação aberta* para *parcialmente
resolvida*: ela é a evidência de que o módulo afere privacidade **estrutural**
(isomorfismo de subgrafo de tamanho `d`), não apenas igualdade de grau.

**Achados principais** (detalhe, tabelas `média ± std` e ameaças à validade
em `results_dsweep.md`):

1. **Déficit sempre estrutural.** `valid=false` nos 48 runs, porém
   `deficit_fully_structural=true` em todos — o déficit decorre de violadores
   estruturais, não de falha do algoritmo (coerente com D-06; verificador
   independente).
2. **`d` controla o tamanho do grupo.** EGS ≈ `k·d` em células completas
   (confirmado: k=2/d=10 → 19.70; k=20/d=10 → 133.0). Aumentar `d` engrossa os
   grupos, em geral reduz a reidentificação por subgrafo e aumenta a degradação
   de utilidade (KS D e Δclust).
3. **Vetores de ataque opostos em k.** O ataque por subgrafo enfraquece com k
   (mais candidatos indistinguíveis); o ataque por grau se fortalece (a
   anonimização distorce a distribuição de graus, KS D → ~0.8–0.95). Aumentar
   `k` desloca o vetor de ataque mais eficaz de subgrafo para grau.
4. **Combos degenerados, mantidos e anotados.** `d=2` é degenerate na 3437 sob
   pymetis (D-08, G3: ≈199/267 partições vazias; números fora da tendência);
   `d=10, k=20` é degenerate esperado (D-10: cobertura 0.752, a menor do grid,
   `FAILURE_LOW_COVERAGE`). Documentados em vez de ocultados.
5. **Ressalva de timeouts.** `reid_sub=0` exato em k=20/d∈{1,5} pode refletir
   timeouts do VF2 (120 s/nó), não segurança real — o JSONL não registra a
   contagem de timeouts. Ver `results_dsweep.md` §5.5 e §5.7.

---

## 10. Referências

[1] [BACKSTROM, L.; DWORK, C.; KLEINBERG, J.](https://doi.org/10.1145/1242572.1242598) Wherefore art thou R3579X? Anonymized social networks, hidden patterns, and structural steganography. In: *Proceedings of the 16th International Conference on World Wide Web (WWW 2007)*. New York: ACM, 2007. p. 181–190.

[2] [HE, X. et al.](https://doi.org/10.1109/WI-IAT.2009.108) Preserving privacy in social networks: A structure-aware approach. In: *IEEE/WIC/ACM International Joint Conference on Web Intelligence and Intelligent Agent Technology (WI-IAT 2009)*. [S. l.]: IEEE, 2009. p. 647–654.

[3] [KARYPIS, G.; KUMAR, V.](https://doi.org/10.1137/S1064827595287997) A fast and high quality multilevel scheme for partitioning irregular graphs. *SIAM Journal on Scientific Computing*, v. 20, n. 1, p. 359–392, 1998.

[4] [LIU, K.; TERZI, E.](https://doi.org/10.1145/1376616.1376629) Towards identity anonymization on graphs. In: *Proceedings of the 2008 ACM SIGMOD International Conference on Management of Data (SIGMOD 2008)*. New York: ACM, 2008. p. 93–106.

[5] [SWEENEY, L.](https://doi.org/10.1142/S0218488502001648) k-anonymity: A model for protecting privacy. *International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems*, v. 10, n. 5, p. 557–570, 2002.

[6] [WÖRLEIN, M. et al.](https://doi.org/10.1007/11564126_32) A quantitative comparison of the subgraph miners MoFa, gSpan, FFSM, and Gaston. In: *Knowledge Discovery in Databases: PKDD 2005*. Berlin: Springer, 2005. p. 392–403. (Lecture Notes in Computer Science, v. 3721).

[7] [ZHOU, B.; PEI, J.](https://doi.org/10.1109/ICDE.2008.4497459) Preserving privacy in social networks against neighborhood attacks. In: *2008 IEEE 24th International Conference on Data Engineering (ICDE 2008)*. [S. l.]: IEEE, 2008. p. 506–515.
