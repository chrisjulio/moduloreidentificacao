# Definições Operacionais das Métricas

> Definições precisas das métricas de privacidade e utilidade usadas no pipeline.

## Métricas de Privacidade

- **Taxa de reidentificação por ataque**: proporção de nós-alvo corretamente identificados pelo ataque.
- **Tamanho médio dos grupos de equivalência**: média do número de nós por grupo após anonimização.

## Métricas de Utilidade

- **KS-test (estatística D)**: teste de Kolmogorov-Smirnov sobre a distribuição de grau (original vs. anonimizado).
- **Variação relativa do clustering**: variação relativa do coeficiente de clustering médio (original vs. anonimizado).

## Parâmetro principal

`k ∈ {2, 5, 10, 20}`

---

## k-anonymity-verifier

> **Issue:** [S1] Definir metrics_definitions.md §k-anonymity-verifier (#34).
> **Referências cruzadas:** `docs/algorithm_notes.md` §4 (decisões D-05 e D-06).
> **Status:** Definido. Consolidado em 20/05/2026. Schema atualizado em 22/05/2026 (DL-01).

O verificador de k-anonimato estrutural é um instrumento de auditoria
**independente do anonimizador**. Ele opera sobre o grafo de saída `G'` e
sobre a estrutura de grupos produzida pelo algoritmo de He et al. (2009),
respondendo à pergunta: *dado o que o algoritmo de fato produziu, quantos
nós satisfazem a Definição 2 para o `k` configurado?*

A distinção entre **critério formal** (garantia por construção, Seção 4.1 de
`algorithm_notes.md`) e **verificação empírica** (este verificador) é
deliberada e necessária: o artigo pressupõe condições que a implementação
pode violar parcialmente (ver D-06 e D-07 em `algorithm_notes.md` §7).

---

### 1. Critério formal vs. verificação empírica

| Dimensão | Critério formal (He et al.) | Verificação empírica (este verificador) |
|---|---|---|
| **Fonte** | Garantia por construção (Seções 2.3 e 3.2 do artigo) | Aplicação direta da Def. 2 sobre `G'` produzido |
| **Pressuposto** | Grupos com exatamente `k` LSs isomorfas de mesmo tamanho | Nenhum — audita o que foi produzido |
| **Saída** | Implícita (o algoritmo garante) | Explícita: fração satisfeita + lista de violadores |
| **Casos de borda** | Grupo final incompleto (D-06) quebra a garantia | Violadores capturados e quantificados |
| **Acoplamento** | Interno ao algoritmo | Zero reutilização de código interno do anonimizador |

---

### 2. Assinatura do verificador

```python
def validate_k_anonymity(
    groups: list[list[nx.Graph]],  # groups[r][j] = subgrafo induzido em G' da j-ésima LS do grupo r
    k: int,
) -> dict:
    """Verify structure-aware k-anonymity of G' independently of the anonymizer."""
```

**Entrada esperada:**
- `groups` — lista de grupos; cada grupo é uma lista de subgrafos induzidos em `G'`
  (não cópias independentes), preservando a identidade dos nós.
- `k` — inteiro positivo; mesmo valor configurado no anonimizador.

**Saída:** dict com os campos da Seção 3.

---

### 3. Estrutura de retorno

```python
{
    # --- Campos originais (compatíveis com versões anteriores) ---
    "valid":               bool,   # True somente se NENHUMA violação existir
    "satisfied_fraction":  float,  # fração de nós que satisfazem Def. 2 (mantido para BC)
    "n_violators":         int,    # número de nós violadores
    "violators":           list,   # IDs dos nós violadores (ordenados)
    "violations":          list,   # log estruturado (ver Seção 5)

    # --- Campos novos — DL-01 (22/05/2026) ---
    "coverage_fraction":          float,  # alias de satisfied_fraction; fração coberta
    "uncovered_fraction":         float,  # 1 - coverage_fraction; sempre == n_violators / n_total
    "deficit_fully_structural":   bool,   # ver abaixo
}
```

#### `coverage_fraction`
Alias direto de `satisfied_fraction`. Fração de nós do grafo `G'` que satisfazem
a Def. 2 para o `k` configurado. Valor real calculado pelo verificador — pode ser
`0.98`, `0.94`, `1.0` etc., dependendo do grafo e de `k`. **Não existe um percentual
fixo pré-definido de nós descartados.**

#### `uncovered_fraction`
Fração de nós não cobertos (`1 - coverage_fraction`). Campo explícito para
facilitar filtragem e relatórios sem requerer cálculo externo.

#### `deficit_fully_structural`
`True` sse **todas** as violações registradas em `violations` são do tipo
`"incomplete_group"` (causa estrutural, D-06), e **nenhuma** é do tipo
`"non_isomorphic"` ou `"non_disjoint"` (que indicariam bugs de implementação).

Este campo suporta diretamente o **critério lógico do marco #16** (decisão DL-01
em `docs/decision_log.md`):

| `coverage_fraction` | `deficit_fully_structural` | Veredicto do marco |
|---|---|---|
| `>= 0.9` | `True` | **APROVADO** — déficit integralmente estrutural |
| `>= 0.9` | `False` | **REPROVADO** — há violações não estruturais (bug) |
| `< 0.9` | qualquer | **REPROVADO** — piso de sanidade não atingido |
| `1.0` | `True` (vacuamente) | **APROVADO** — sucesso pleno |

> **Nota:** quando `valid == True` (sem nenhuma violação), `deficit_fully_structural`
> é `True` por vacuidade (`violation_types ⊆ {"incomplete_group"}`
> com conjunto vazio). Isso é correto: sem déficit, o campo não é relevante
> mas não é falso.

---

### 4. Condições obrigatórias de validação

O verificador avalia **três condições**, nesta ordem de precedência:

#### 4.1 Disjunção global entre LSs

Cada nó de `G'` deve pertencer a exatamente uma LS em `groups`.

```
Para todo v ∈ V(G'):
    |{(r, j) : v ∈ V(groups[r][j])}| == 1
```

- **Violação:** `type = "non_disjoint"`, `status = "unprotected"`.
- Se detectada, as demais condições ainda são verificadas (para diagnóstico
  completo), mas `valid` é forçado a `False` independentemente dos demais resultados.
- **Nota:** o algoritmo de He et al. garante disjunção por construção (partição
  de `V` pela Etapa 1). Violação indica bug na implementação do anonimizador, não
  caso normal de operação.

#### 4.2 Cardinalidade mínima por grupo

Cada grupo `G_r` deve conter pelo menos `k` LSs.

```
Para todo grupo G_r em groups:
    len(G_r) >= k
```

- **Violação:** `type = "incomplete_group"`, `status = "partially_unprotected"`.
- O grupo final do Algorithm 1 pode ter `|G_r| < k` (decisão D-06 em
  `algorithm_notes.md` §7). Todos os nós pertencentes a LSs de grupos incompletos
  são registrados como violadores.
- **`valid` nunca retorna `True` se houver ao menos um grupo incompleto**, mesmo
  que todos os nós do grupo incompleto sejam minoria pequena.
- O relatório reporta `satisfied_fraction` / `coverage_fraction < 1.0` e lista
  explicitamente os violadores, permitindo distinguir falha pequena (grupo final
  de D-06) de falha estrutural (muitos grupos incompletos, sugerindo bug).

#### 4.3 Isomorfismo mútuo nos grupos completos

Para cada grupo `G_r` com `|G_r| >= k`, todas as `k` LSs devem ser
**mutuamente isomorfas** entre si.

```
Para todo par (LS_i, LS_j) no mesmo grupo G_r com i ≠ j:
    nx.is_isomorphic(LS_i, LS_j) == True
```

- **Violação:** `type = "non_isomorphic"`, `status = "unprotected"`.
- Na implementação, a verificação usa `nx.is_isomorphic` (VF2) para cada par
  ordenado. Por simetria do isomorfismo, basta verificar os `k(k-1)/2` pares
  não-ordenados.
- Nós de qualquer LS não-isomorfa às demais em seu grupo são registrados como
  violadores (contagem de candidatos isomorfos insuficiente para satisfazer Def. 2).

---

### 5. Tratamento de grupos incompletos

Grupos incompletos (`|G_r| < k`) são o caso normal de borda previsto por D-06:
o Algorithm 1 pode exaurir LSs disponíveis antes de completar o último grupo.

**Protocolo:**

1. Registrar uma `ViolationRecord` com:
   ```
   type    = "incomplete_group"
   status  = "partially_unprotected"
   detail  = f"group {r}: size {len(G_r)} < k={k}; {n_affected} nodes unprotected"
   ```
2. Marcar todos os nós das LSs do grupo como violadores em `violators`.
3. **Nunca retornar `valid = True`** na presença de grupo incompleto.
4. Registrar `satisfied_fraction` / `coverage_fraction` com precisão (ex.: `0.986`
   em vez de `False`) — isso permite ao módulo de experimentos distinguir:
   - falha pequena atribuível a D-06 (poucos violadores, dentro do limite
     esperado de `d` nós)
   - falha estrutural (muitos violadores, sugerindo bug na isomorfização)

**Limite esperado de violadores por D-06:**
O grupo final incompleto tem no máximo `d − 1` nós (onde `d` é o tamanho máximo
de LS configurado). Se `n_violators > d − 1`, a causa é provavelmente outra e
deve ser investigada antes de prosseguir.

---

### 6. Log estruturado de violações

Cada violação é registrada como um dict com os campos da Seção 3.
Os três tipos possíveis são:

| `type` | Causa | `status` | Quando ocorre |
|---|---|---|---|
| `"non_disjoint"` | Nó em mais de uma LS | `"unprotected"` | Bug no anonimizador |
| `"incomplete_group"` | Grupo com `\|G_r\| < k` | `"partially_unprotected"` | Caso normal (D-06) |
| `"non_isomorphic"` | Par de LSs no mesmo grupo não isomorfas | `"unprotected"` | Bug na isomorfização |

**Exemplo de saída em log estruturado (JSON) — após DL-01:**

```json
{
  "valid": false,
  "satisfied_fraction": 0.9962,
  "coverage_fraction": 0.9962,
  "uncovered_fraction": 0.0038,
  "deficit_fully_structural": true,
  "n_violators": 2,
  "violators": [104, 387],
  "violations": [
    {
      "type": "incomplete_group",
      "status": "partially_unprotected",
      "nodes": [104, 387]
    }
  ]
}
```

Leitura: `coverage_fraction=0.9962 >= 0.9` e `deficit_fully_structural=true`
→ instância **APROVADA** pelo critério DL-01.

---

### 7. Riscos metodológicos

#### 7.1 Custo computacional do VF2 para `d > 20`

Graph Isomorphism (GI) não é sabidamente polinomial nem NP-completo.
`networkx.is_isomorphic` (VF2) é eficiente para LSs pequenas (`d ≤ 20`), mas
pode degradar significativamente para `d` maiores:

- Para `d ≤ 20`: custo por par de LSs é negligenciável na prática.
- Para `d > 20`: avaliar pré-filtro por invariantes baratos antes de chamar VF2:
  - número de nós e arestas (condição necessária, O(1))
  - sequência de graus ordenada (condição necessária, O(d log d))
  - espectro do Laplaciano (condição necessária mais forte, O(d²) ou O(d³))
- O custo total do verificador é `O(c_k · k² · f(d))` onde `c_k = ⌊n/d⌋` é
  o número de grupos e `f(d)` é o custo de uma chamada VF2 sobre LSs de
  tamanho `d`.
- Para os valores de `d` usados no baseline (`d = 10`, configuração default),
  o custo é aceitável. Documentar como limitação se `d` for aumentado.

#### 7.2 Risco de falso positivo metodológico

Um verificador ingênuo que cheque apenas **isomorfismo par-a-par** dentro de
cada grupo e retorne booleano único mede uma condição **mais fraca** que a
Def. 2:

- **Condição ingênua:** "existe ao menos uma outra LS isomorfa no mesmo grupo"
- **Def. 2 (correta):** "existem ao menos `k−1` nós **fora da própria LS**
  com LS isomorfa"

As condições são equivalentes somente quando (a) todos os grupos têm `|G_r| = k`
exatamente **e** (b) os grupos são disjuntos. Se qualquer uma falhar (D-06,
D-07), o verificador ingênuo retorna `True` mascarando violações reais.

O verificador definido nesta seção contorna o problema contando, para cada LS
`(r, j)`, o número de nós em LSs isomorfas **distintas** dentro do mesmo grupo.
O nó `v ∈ LS(r,j)` satisfaz Def. 2 sse o grupo de `v` é completo (`len >= k`)
e todas as LSs do grupo são mutuamente isomorfas.

#### 7.3 Escopo da certificação

O verificador certifica que *o algoritmo cumpriu sua promessa dada a partição
produzida*, não que *`G'` é estruturalmente k-anônimo para qualquer
particionamento alternativo de `G'`*. A segunda afirmação é mais forte, não
está coberta, e deve ser listada como **ameaça à validade externa** no relatório
de qualificação.

---

### 8. Critério de passagem do marco intermediário (29/05/2026)

Para a configuração de validação (`k = 5`, `egonet_id = 3437`, `d = 10`):

1. O verificador retorna `valid = True` (`coverage_fraction == 1.0`) em
   **ao menos 1 das 3 sementes**; **ou**
2. Em todas as sementes em que `valid = False`:
   - `coverage_fraction >= 0.9`, **e**
   - `deficit_fully_structural == True`
   (ou seja, 100% do déficit é atribuível a grupo incompleto D-06).
3. Se nenhuma das duas condições for satisfeita, ou se
   `deficit_fully_structural == False` em qualquer semente, disparar
   reformulação de escopo (conforme Seção 7 do plano operacional) —
   não acomodar.

**Reprodutibilidade:** resultado registrado em log estruturado com semente,
`k`, `d` e `egonet_id` explícitos.

**Marco 29/05/2026: APROVADO** (issue #16, PR #53).
Configuração k=5, d=1, egonet_id=3437: `coverage_fraction=0.9962`,
`deficit_fully_structural=True` nas 3 sementes; apenas `incomplete_group` (D-06).
