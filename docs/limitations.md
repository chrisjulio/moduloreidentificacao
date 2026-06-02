# Limitações do Pipeline — Módulo de Reidentificação

> **Issue de origem:** [S3][#26-A] Revisão e produção documental acadêmica do pipeline (#63).
> **Última atualização:** 2026-05-23.
> **Referências cruzadas:**
> - `docs/algorithm_notes.md` — Seções 3.1, 4.1–4.4, 7 (decisões D-01 a D-07)
> - `docs/metrics_definitions.md` — Seções 7.1–7.3, §k-anonymity-verifier
> - `docs/results_baseline.md` — resultados do baseline (#23)

---

## Introdução

Este documento registra as limitações conhecidas do pipeline na sua versão
corrente (baseline S3). As limitações estão organizadas em duas categorias
conceituais mutuamente exclusivas:

- **Limitações de escopo** — escolhas deliberadas que restringem o domínio
  de aplicação do protótipo sem comprometer a validade das afirmações feitas
  dentro desse domínio. São elegíveis para expansão em versões futuras, mas
  não constituem defeito do protótipo.
- **Limitações técnicas** — restrições decorrentes de decisões de implementação
  que se desviam das premissas formais do artigo de [He et al. (2009)](https://doi.org/10.1109/WI-IAT.2009.108), ou que
  introduzem aproximações não cobertas pela garantia teórica. Algumas são
  declaradas como aceitáveis para o protótipo; outras são candidatas a
  superação em versões futuras.

Para cada limitação, indica-se também o **impacto sobre a validade dos
resultados do baseline** (#23 / `docs/results_baseline.md`).

---

## 1. Limitações de escopo

Limitações de escopo refletem escolhas de design do protótipo. Elas definem
o que o módulo *propõe-se a avaliar*, não o que ele *falhou em implementar*.

### 1.1 Dataset restrito a Facebook Ego-Nets (SNAP)

**Descrição:** Todo o pipeline de anonimização e avaliação foi desenvolvido
e validado exclusivamente sobre a coleção Facebook Ego-Nets (SNAP),
especificamente a ego-rede de identificador 3437 (n_lcc=532, m_lcc=4812).
Nenhuma outra fonte de dados foi utilizada no baseline.

**Natureza:** Escolha deliberada de escopo mínimo para o protótipo.
O pipeline não é parametrizado por tipo de rede social — a generalização
para outros domínios (redes de coautoria, redes sintéticas, grafos
bipartidos) requer validação adicional fora do escopo atual.

**Impacto no baseline (#23):** Os resultados de `satisfied_fraction`,
`coverage_fraction` e métricas de utilidade (KS-test, ΔCC) são válidos
*para esta ego-rede específica*. Não se pode afirmar que o desempenho
observado (ex.: `satisfied_fraction ≥ 0.977` para k=20) generaliza para
outras redes sem evidência empírica adicional.

**Referência:** `docs/algorithm_notes.md` §9.1; `docs/results_baseline.md`.

---

### 1.2 Escopo restrito ao algoritmo de [He et al. (2009)](https://doi.org/10.1109/WI-IAT.2009.108)

**Descrição:** O pipeline implementa exclusivamente o algoritmo de
k-anonimato estrutural de [He et al. (2009)](https://doi.org/10.1109/WI-IAT.2009.108). Outros modelos de anonimização
de grafos (ex.: k-degree anonymity de [Liu & Terzi](https://doi.org/10.1145/1376616.1376629), 1-neighborhood
isomorphism de [Zhou & Pei](https://doi.org/10.1109/ICDE.2008.4497459), métodos baseados em ruído diferencial) não
estão implementados e não fazem parte do escopo de comparação no baseline.

**Natureza:** Escolha deliberada. A comparação com outros modelos está
prevista como expansão futura, não como requisito do protótipo.

**Impacto no baseline (#23):** As métricas de utilidade e privacidade
produziram resultados relativos a *uma* estratégia de anonimização.
Afirmações comparativas ("He et al. preserva melhor a estrutura do que
alternativa X") não são sustentadas pelos dados do baseline.

---

### 1.3 Varredura de parâmetros restrita a k ∈ {2, 5, 10, 20} e d = 1 — *parcialmente resolvida*

> **Status:** **Parcialmente resolvida** (2026-06-02). A varredura `d > 1`
> foi executada e documentada em
> [`docs/results_dsweep.md`](results_dsweep.md) (experimento
> `he2009_facebook_dsweep`, issue #88). A limitação permanece *parcial* porque
> a validação `d > 1` ainda se restringe a **uma única ego-rede (3437)** — ver
> §1.1 e as ameaças à validade externa em `results_dsweep.md` §5.7.

**Descrição:** A varredura experimental do baseline (#23) cobriu apenas os
valores de k definidos no escopo mínimo, com `d=1` fixo (Local Structures
de tamanho unitário — nó central isolado). A varredura sobre `d > 1` foi
excluída do escopo **mínimo** (decisão D-02) e posteriormente realizada no
tier **desejável** (D-08).

**Natureza:** Escolha deliberada de escopo. A configuração `d=1` simplifica
a implementação e valida a propriedade formal sem introduzir complexidade
adicional de FSM; `d > 1` foi perseguido como funcionalidade desejável.

**Impacto no baseline (#23):** Com `d=1`, a Local Structure de cada nó é
trivial (subgrafo de um único nó), e o isomorfismo reduz-se a igualdade de
grau. A garantia de k-anonimato *estrutural* (no sentido pleno da Def. 2 de
He et al., que considera subgrafos de tamanho variável `d`) **não era**
demonstrada empiricamente para `d > 1` na versão do baseline.

**Resolução parcial (d-sweep, #88):** O experimento `he2009_facebook_dsweep`
varreu o grid `k ∈ {2,5,10,20} × d ∈ {1,2,5,10} × 3 sementes` (48 runs,
backend pymetis em todos). O contraste `d=1` (≈ k-anonimato de grau) vs.
`d ∈ {5,10}` (structure-aware pleno) é a evidência empírica de que o módulo
afere privacidade *estrutural*, não só de grau. Resultados, combos
degenerados (d=2 D-08; d=10/k=20 D-10) e ameaças à validade em
[`docs/results_dsweep.md`](results_dsweep.md); resumo em
`docs/algorithm_notes.md` §9.4. **Resíduo:** generalização a outras
ego-redes/datasets (validade externa, §1.1) permanece aberta.

**Referência:** `docs/algorithm_notes.md` D-02, §9.1, §9.4;
`docs/results_dsweep.md`.

---

### 1.4 Ataques de reidentificação restritos a grau e subgrafos

**Descrição:** O plano operacional do S3 inclui ataques por grau, por
subgrafos e por entropia. O baseline (#23) implementou os dois primeiros;
ataques por entropia e modelos adversariais mais sofisticados (ex.:
correlação de atributos, ataques de background knowledge combinado) estão
fora do escopo desta versão.

**Natureza:** Escolha deliberada de escopo mínimo.

**Impacto no baseline (#23):** A taxa de reidentificação efetiva medida
pelos ataques implementados é uma *cota inferior* da vulnerabilidade real.
Adversários com modelos de conhecimento mais ricos podem obter taxas
maiores do que as reportadas. Declarar como ameaça à validade externa.

---

## 2. Limitações técnicas

Limitações técnicas são desvios das premissas formais do artigo ou
aproximações introduzidas por decisões de implementação. Cada uma é
identificada com a decisão correspondente no `decision_log` ou em
`algorithm_notes.md`.

### 2.1 FSM simplificado com `s_max` configurável (D-01)

**Descrição:** O algoritmo de [He et al. (2009)](https://doi.org/10.1109/WI-IAT.2009.108) cita mineração de subgrafos
frequentes (FSM) sem especificar implementação (referência [Wörlein et al. (2005)](https://doi.org/10.1007/11564126_32)). O protótipo usa um FSM simplificado com limite de tamanho
`s_max` configurável, em lugar de gSpan ou equivalente completo.

**Tipo:** Limitação técnica — aproximação do procedimento original.

**Impacto no baseline (#23):** O FSM simplificado pode deixar de encontrar
subgrafos frequentes de tamanho `> s_max`, reduzindo a qualidade do
agrupamento. Com `d=1` (baseline atual), o impacto é nulo (LSs de tamanho 1
não requerem FSM substantivo). Para `d > 1`, o impacto deve ser avaliado.

**Candidato a superação:** Sim — substituição por gSpan ou implementação
alternativa auditável em versão futura.

**Referência:** `docs/algorithm_notes.md` D-01, §2.1.

---

### 2.2 Motor de particionamento KL como fallback sem garantia de balanceamento (D-04, D-07)

**Descrição:** O artigo de He et al. especifica multilevel k-way
([Karypis & Kumar](https://doi.org/10.1137/S1064827595287997)) como algoritmo de partição. O protótipo usa pymetis
como motor primário e `kernighan_lin_bisection` recursivo como fallback
(D-04). O fallback KL *não garante balanceamento de tamanho* para `ck > 2`:
partições individuais podem ser menores que `|V| / ck` (D-07).

**Tipo:** Limitação técnica — desvio da especificação do artigo no caminho
do fallback.

**Impacto no baseline (#23):** Os resultados do baseline foram produzidos
com `d=1` (uma LS por nó, partições de tamanho 1), tornando o desbalanceamento
irrelevante nesta configuração. Para `d > 1`, o fallback KL pode produzir
LSs de tamanhos distintos dentro de um mesmo grupo, violando a premissa
da Fase 1 de He et al. (*"Since each of local structures in the same group
has the same number of nodes, this process will terminate quickly"*, p. 651).
A política D-07 Opção A mitiga isso restringindo grupos a LSs do mesmo
tamanho, mas aumenta o número de violadores por D-06.

**Candidato a superação:** Sim — forçar partições exatas via `tpwgts` do
pymetis em versão de produção.

**Risco de degradação silenciosa e como detectar/evitar:** o ambiente
padrão do `requirements.txt` (§3.2 do README) **não** instala o `pymetis`
(ele não instala via pip de forma confiável), de modo que uma execução pode
recair no fallback KL emitindo apenas um `UserWarning` transitório — fácil de
passar despercebido pelo pesquisador. Mitigações implementadas:
- **Rastreabilidade no log:** cada execução grava `partition_backend`
  (`"pymetis"` | `"networkx-kl"`) em cada entrada JSONL e em
  `summary.json` (`partition_backends`); o relatório do runner avisa quando o
  fallback está ativo. Resultados ficam auto-documentados quanto ao backend.
- **Opt-in de rigor:** a flag `anonymization.allow_kl_fallback` (padrão
  `true`, preserva o comportamento) pode ser definida como `false` no YAML
  para **abortar** a execução quando o backend resolvido for `networkx-kl` —
  garantindo que resultados de produção venham apenas do motor primário.
- **Como instalar o pymetis:** via conda-forge (`environment.yml` /
  `scripts/setup_conda_windows.ps1`, todos os SOs) ou, no Linux/macOS,
  `pip install -e ".[partition-c]"` (compila do fonte).

**Referência:** `docs/algorithm_notes.md` D-04 (revisado 20/05/2026), D-07.

---

### 2.3 Grupos incompletos no grupo final do Algorithm 1 (D-06)

**Descrição:** O Algorithm 1 de He et al. pode exaurir LSs disponíveis
antes de completar o último grupo, gerando um grupo com `|G_r| < k`. Os
nós desse grupo não satisfazem a Def. 2 (structure-aware k-anonymity) e
são classificados como violadores pelo verificador empírico.

**Tipo:** Limitação técnica — consequência estrutural do algoritmo, não
erro de implementação. Prevista explicitamente em D-06.

**Impacto no baseline (#23):** Nos resultados da varredura de k
(`docs/algorithm_notes.md` §9.1), a `satisfied_fraction` nunca atingiu
1.0 para k ≥ 5 (valores observados: 0.9962 para k∈{5,10} e 0.9774 para
k=20, ego-rede 3437). Toda a fração de violadores é atribuível a D-06
(`deficit_fully_structural=True` em todas as sementes). Esses resultados
devem ser reportados com essa qualificação explícita — não como falha de
implementação, mas como propriedade estrutural do algoritmo.

**Candidato a superação:** Parcialmente — o número de violadores é limitado
a `n mod k` nós (para `d=1`). Estratégias de fusão do grupo incompleto
(ex.: incorporar seus nós ao grupo de maior afinidade estrutural) poderiam
eliminar D-06, mas introduziriam heurísticas não especificadas no artigo.

**Referência:** `docs/algorithm_notes.md` D-06, §4.1–4.2;
`docs/metrics_definitions.md` §5.

---

### 2.4 Verificador de k-anonimato com escopo conservador (D-05)

**Descrição:** O verificador empírico (`validate_k_anonymity`) conta
candidatos isomorfos *restrito ao grupo de anonimização de cada LS*. A
Def. 2 de He et al. não impõe essa restrição — LSs isomorfas em grupos
distintos também satisfariam a condição. O verificador pode, portanto,
subestimar a contagem de candidatos e classificar como violadores nós que,
na prática, satisfazem a Def. 2 considerando todo o grafo `G'`.

**Tipo:** Limitação técnica — escolha metodológica conservadora e auditável.

**Impacto no baseline (#23):** O comportamento conservador é aceitável para
auditoria: ele nunca reporta falsos negativos (nunca certifica um nó
violador como protegido). Pode, contudo, *superestimar* o número de
violadores em cenários onde grupos distintos produzem LSs mutuamente
isomorfas. Em todos os casos do baseline, os violadores são atribuíveis
exclusivamente a D-06, tornando o impacto desta limitação nulo nos dados
observados.

**Candidato a superação:** Sim — varredura global de `G'` para contar
candidatos isomorfos além do grupo de origem, ao custo de `O(c_k²)` chamadas
adicional a VF2.

**Referência:** `docs/algorithm_notes.md` §4.3.3; `docs/metrics_definitions.md`
§7.2.

---

### 2.5 Custo computacional do VF2 para d > 20

**Descrição:** A verificação de isomorfismo usa `networkx.is_isomorphic`
(algoritmo VF2). Graph Isomorphism (GI) não é sabidamente polinomial nem
NP-completo; o custo empírico do VF2 pode crescer exponencialmente para
LSs grandes. O custo total do verificador é `O(c_k · k² · f(d))`, onde
`f(d)` é o custo de uma chamada VF2 sobre LSs de tamanho `d`.

**Tipo:** Limitação técnica — gargalo computacional para valores de `d`
grandes.

**Impacto no baseline (#23):** Com `d=1`, o custo é desprezível (VF2 em
grafos de 1 nó é trivial). Para `d ≤ 20`, o custo permanece aceitável.
Para `d > 20`, pré-filtros por invariantes baratos (distribuição de graus,
espectro do Laplaciano) devem ser aplicados antes de invocar VF2.

**Candidato a superação:** Sim — implementação de pré-filtros e avaliação
de alternativas ao VF2 (ex.: Weisfeiler-Leman para heurística rápida).

**Referência:** `docs/algorithm_notes.md` §4.3.1;
`docs/metrics_definitions.md` §7.1.

---

### 2.6 Critério de matching da Fase 1 por grau com desempate lexicográfico (D-03)

**Descrição:** O artigo de He et al. (p. 651) descreve o matching de Fase 1
apenas como "based on nodes degree", sem critério de desempate. O protótipo
adota índice de nó lexicográfico como desempate (D-03). Esse critério
garante determinismo e reprodutibilidade, mas pode produzir matchings
diferentes dos que uma implementação com critério alternativo produziria.

**Tipo:** Limitação técnica — subespecificação do artigo resolvida por
escolha arbitrária auditável.

**Impacto no baseline (#23):** O matching afeta a identidade do grafo `G'`
produzi (quais arestas são adicionadas/removidas na Fase 2), mas não a
propriedade formal de k-anonimato (que depende do resultado final, não do
caminho). A escolha de desempate deve ser declarada como parâmetro de
reprodutibilidade ao publicar resultados.

**Referência:** `docs/algorithm_notes.md` D-03, §3.3.

---

## 3. Ameaças à validade

As limitações acima traduzem-se nas seguintes ameaças à validade, relevantes
para o relatório de qualificação:

| Ameaça | Tipo | Limitação de origem |
|---|---|---|
| Resultados de `satisfied_fraction` não generalizáveis a outras redes | Validade externa | 1.1 |
| Comparação com outros algoritmos de anonimização não suportada | Validade externa | 1.2 |
| k-anonimato estrutural pleno (d > 1) validado em **uma só** ego-rede (3437); generalização aberta | Validade externa | 1.3 *(parcialmente resolvida)* |
| Taxa de reidentificação efetiva pode ser subestimada (ataques incompletos) | Validade de construto | 1.4 |
| `G'` pode não ser k-anônimo para particionamentos alternativos de `G'` | Validade interna | 2.4 |
| Determinismo dependente de critério de desempate não especificado no artigo | Reprodutibilidade | 2.6 |

---

## 4. Resumo de candidatos a superação por versão

| Limitação | Versão sugerida | Esforço estimado |
|---|---|---|
| FSM completo (gSpan) em lugar do simplificado (D-01) | Pós-qualificação | Médio |
| `tpwgts` para partições exatas (D-07) | Pós-qualificação | Baixo |
| Varredura global de `G'` no verificador (D-05) | Pós-qualificação | Baixo |
| Pré-filtros VF2 para `d > 20` | Pós-qualificação | Médio |
| Validação empírica com `d > 1` e outros datasets | Versão 2 | Alto |
| Ataques por entropia e background knowledge combinado | Versão 2 | Alto |
| Comparação com outros algoritmos de anonimização | Versão 2 | Alto |

---

## 5. Referências

[1] [HE, X. et al.](https://doi.org/10.1109/WI-IAT.2009.108) Preserving privacy in social networks: A structure-aware approach. In: *IEEE/WIC/ACM International Joint Conference on Web Intelligence and Intelligent Agent Technology (WI-IAT 2009)*. [S. l.]: IEEE, 2009. p. 647–654.

[2] [KARYPIS, G.; KUMAR, V.](https://doi.org/10.1137/S1064827595287997) A fast and high quality multilevel scheme for partitioning irregular graphs. *SIAM Journal on Scientific Computing*, v. 20, n. 1, p. 359–392, 1998.

[3] [LIU, K.; TERZI, E.](https://doi.org/10.1145/1376616.1376629) Towards identity anonymization on graphs. In: *Proceedings of the 2008 ACM SIGMOD International Conference on Management of Data (SIGMOD 2008)*. New York: ACM, 2008. p. 93–106.

[4] [WÖRLEIN, M. et al.](https://doi.org/10.1007/11564126_32) A quantitative comparison of the subgraph miners MoFa, gSpan, FFSM, and Gaston. In: *Knowledge Discovery in Databases: PKDD 2005*. Berlin: Springer, 2005. p. 392–403. (Lecture Notes in Computer Science, v. 3721).

[5] [ZHOU, B.; PEI, J.](https://doi.org/10.1109/ICDE.2008.4497459) Preserving privacy in social networks against neighborhood attacks. In: *2008 IEEE 24th International Conference on Data Engineering (ICDE 2008)*. [S. l.]: IEEE, 2008. p. 506–515.
