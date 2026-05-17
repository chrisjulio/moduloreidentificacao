# Notas de Implementação — He et al. (2009)

> Registro passo a passo do algoritmo de anonimização estrutural.
> Preencher progressivamente durante a Semana 1 (15–22/05/2026) à medida que
> a leitura do artigo avança. Cada seção deve ser atualizada antes de iniciar
> a implementação correspondente.

## Referência

He, X. et al. (2009). Preserving privacy in social networks: A structure-aware
approach. *Proceedings of the IEEE/WIC/ACM International Joint Conference on
Web Intelligence and Intelligent Agent Technology (WI-IAT)*.

---

## 1. Conceito central: k-anonimato estrutural

### 1.1 O que constitui um "grupo de equivalência" no contexto de grafos?

No modelo de He et al., o grupo de equivalência é formado por **Local Structures
(LSs) isomorfas entre si**. Uma Local Structure `LS(v_i)` é definida como um
subgrafo conectado contendo o nó `v_i`, com densidade de arestas interna maior
do que a densidade de arestas entre `LS(v_i)` e os nós externos
(Def. 1, Seção 2.1). Durante a etapa de grouping (Seção 3.2), o algoritmo
agrupa `k` Local Structures em um mesmo grupo; após a transformação, todas as
LSs do grupo tornam-se isomorfas entre si. Esse conjunto de `k` subgrafos
isomorfos constitui o grupo de equivalência: qualquer nó pertencente a uma LS
do grupo é indistinguível dos nós nas demais `k-1` LSs (Def. 2, Seção 2.3).

> **Citação direta:** "[…] node v_i is structure-aware k-anonymous, if there
> are at least k−1 other nodes which do not belong to LS(v_i) while having the
> local structure that is isomorphic to LS(v_i)." (Def. 2, p. 648, Seção 2.3)

### 1.2 Qual a propriedade estrutural que torna dois nós indistinguíveis?

Dois nós são considerados indistinguíveis quando suas respectivas Local
Structures são **graficamente isomorfas** (`LS(v_i) ≅ LS(v_j)`). O isomorfismo
aqui é de grafos no sentido clássico: existe uma bijeção `f: V(LS_i) → V(LS_j)`
tal que `(u, w) ∈ E(LS_i)` se e somente se `(f(u), f(w)) ∈ E(LS_j)` (Seção 2.3).
Isso implica que grau individual, existência de arestas entre vizinhos e
distância local são identicamente preservados em ambas as LSs — qualquer
informação de fundo estrutural que um adversário possa ter sobre a vizinhança
local do alvo não permite distinguir entre os `k` candidatos (Seção 2.2).

> **Citação direta:** "An isomorphism of graphs from G to H is a bijection
> f : V(G) → V(H) such that any edge (v1, v2) ∈ E(G) if and only if
> (f(v1), f(v2)) ∈ E(H)." (p. 648, Seção 2.3)

> **Nota interpretativa:** a indistinguibilidade não se baseia em um único
> atributo (ex: grau isolado), mas no isomorfismo completo do subgrafo local —
> o que é estruturalmente mais robusto e mais exigente do que k-degree
> anonymity (Liu & Terzi, 2008 [5], citado em Seção 1 do artigo).

### 1.3 k-anonimato aqui refere-se a grau, vizinhança, ou outra assinatura estrutural?

O k-anonimato de He et al. **não é baseado em grau nem em vizinhança de raio
fixo**, mas em **isomorfismo de Local Structure** — um subgrafo de tamanho
variável determinado pela estrutura comunitária do grafo (Seção 2.1). O artigo
explicitamente critica as duas abordagens anteriores:

- **k-degree anonymity** (Liu & Terzi [5]): baseia-se apenas no grau do nó,
  ignorando informação estrutural. "[…] this anonymization process completely
  ignores structural information inherent in the graph data." (p. 648, Seção 1)
- **1-neighborhood isomorphism** (Zhou & Pei [4]): usa vizinhança de raio fixo
  (1-hop), o que pode exigir re-anonimizações em cascata e produzir grafos muito
  densos (p. 648, Seção 1).

A assinatura estrutural empregada aqui é o **subgrafo comunitário local de
tamanho variável `d`**, controlado pelo parâmetro `d` definido pelo usuário, que
controla o tamanho da partição. A garantia formal é: a confiança de re-
identificação de qualquer nó no grafo anonimizado G' é no máximo `1/k`
(Def. 2–3, p. 648, Seção 2.3).

> **Citação direta:** "[…] the confidence of this node being re-identified from
> the graph is no higher than 1/k." (p. 648, Seção 2.3)

> **Parâmetros de controle:** `k` (nível de privacidade — mínimo de candidatos
> indistinguíveis) e `d` (tamanho da Local Structure / número de nós por
> partição). Juntos formam a **Structure-Aware kd-Anonymity** (Def. 4, p. 649,
> Seção 2.3).

---

## 2. Algoritmo principal

*(a preencher)*

Estrutura esperada (esqueleto a confirmar com o artigo):

```
Entrada:  grafo G = (V, E), parâmetro k
Saída:    grafo anonimizado G' = (V, E') com k-anonimato garantido

Passos:
  1. [descrever]
  2. [descrever]
  ...
```

Complexidade declarada no artigo: *(a preencher)*

---

## 3. Operações de modificação do grafo

*(a preencher)*

Questões a responder:
- O algoritmo adiciona arestas, remove arestas, ou ambos?
- Há operações sobre nós (inserção, fusão)?
- As operações são determinísticas ou têm componente aleatório (→ impacto nas sementes)?

---

## 4. Critério de parada e garantia de k-anonimato

*(a preencher)*

Questões a responder:
- Como o algoritmo verifica que k-anonimato foi atingido?
- O que acontece se o grafo não puder ser anonimizado para o k pedido?
- Como implementar o verificador independente (`validate_k_anonymity`)?

---

## 5. Parâmetros e configuração

*(a preencher)*

Mapear para as chaves do YAML de configuração ([config_example.yml](../config_example.yml)):

| Parâmetro do artigo | Chave YAML | Valor(es) usados |
|---|---|---|
| k | `anonymization.k_values` | [2, 5, 10, 20] |
| *(outros)* | | |

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
