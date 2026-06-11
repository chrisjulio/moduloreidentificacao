# Decisão de pré-processamento das ego-redes do Facebook

> **Issue:** [S1] Decidir e registrar modo de pré-processamento das ego-redes (#7).
> **Referência:** Plano operacional, Seção 4.1 — a decisão deve ser fixada na Semana 1, antes do início dos experimentos finais.
> **Status:** Decidido. Consolidado em 20/05/2026.

---

## 1. Decisão

O modo de pré-processamento adotado é **`multiple_egonets`** para os experimentos
finais, com **`single_egonet`** como sub-configuração de desenvolvimento.

- **Experimentos finais (Semana 3 em diante):** `multiple_egonets`. O pipeline
  `anonimização → ataque → métrica` é executado sobre cada ego-rede listada em
  `egonet_ids`, e os resultados são agregados por valor de `k`.
- **Desenvolvimento e marco de 29/05:** `single_egonet`. Uma única ego-rede
  representativa é usada para iterar sobre a implementação e para a verificação
  obrigatória de k-anonimato exigida pela Seção 7 do plano operacional, que pede
  explicitamente “k=5 sobre uma ego-rede do Facebook”.

O modo `union` foi **descartado**. A justificativa está na Seção 2.

---

## 2. Justificativa

Os três modos previstos no `config_example.yml` não têm o mesmo valor probatório
para o entregável-alvo, cujo critério declarado é uma curva privacidade-vs-utilidade
*defensável*.

**`single_egonet`.** As barras de erro derivam apenas das sementes aleatórias.
Elas medem a estabilidade do algoritmo de [He et al. (2009)](https://doi.org/10.1109/WI-IAT.2009.108) sobre *uma* rede, dada
a aleatoriedade interna da etapa de modificação estrutural. Não respondem, porém,
à pergunta de robustez que orientadores e avaliadores naturalmente levantam: a curva
observada é uma propriedade de He et al. + k-anonimato, ou um artefato da
ego-rede específica escolhida? Para um baseline cujo critério de qualidade é
“defensável”, essa limitação é relevante.

**`multiple_egonets`.** Cada ego-rede do Facebook Ego-Nets é um grafo
independente. Executar o pipeline completo sobre várias delas transforma a barra
de erro em uma afirmação estrutural: “entre ego-redes reais, a taxa de
reidentificação em k=5 é X ± Y”. Essa é exatamente a forma de robustez que torna
a curva defensável. O custo é um laço em torno de um pipeline que não muda — não
há redesenho nem decisão metodológica nova. Como as ego-redes são de tamanho
modesto e o ataque por subgrafos está restrito a vizinhanças 1-hop (plano
operacional, Seção 8), o custo adicional é tempo de CPU, não esforço de
engenharia.

**`union`.** O arquivo `facebook_combined.txt` do SNAP é uma união real e
legítima das dez ego-redes (4.039 nós, 88.234 arestas). Ainda assim, foi
descartado por três razões: (a) colapsa o experimento de volta a um único grafo,
produzindo uma única curva e eliminando a variância estrutural, que é justamente
o ganho buscado; (b) é o maior grafo único disponível, ou seja, o pior caso para
o custo do ataque por subgrafos — exatamente o risco identificado na Seção 8 do
plano operacional; (c) descarta a estrutura ego-cêntrica que torna a análise por
ego-rede interpretável. Em suma, `union` incorre no custo da escala sem entregar
o benefício da variância.

**Compatibilidade com o marco de 29/05.** O faseamento não conflita com o marco
intermediário. A verificação de k-anonimato exigida na Seção 7 do plano é feita
sobre uma única ego-rede; `single_egonet` é o modo apropriado para essa etapa e
para a depuração do pipeline. A troca para `multiple_egonets` ocorre apenas nos
experimentos finais, após a estabilização do pipeline. A decisão registrada nesta
issue é, portanto: **modo final = `multiple_egonets`**, com `single_egonet`
documentado como modo de desenvolvimento.

---

## 3. Sub-decisões de pré-processamento

O “modo” não esgota o pré-processamento. As quatro sub-decisões abaixo são
fixadas aqui porque, sem elas, o experimento não é reprodutível nem comparável
com a literatura. Todas devem ser implementadas no loader (`src/loaders/`) e
expostas no arquivo de configuração.

### 3.1 Nó ego: excluído

Os arquivos `.edges` do SNAP contêm apenas as arestas entre os *alters* de cada
ego-rede; o nó ego não aparece no arquivo. **Decisão: excluir o nó ego** do
grafo analisado, trabalhando com o subgrafo induzido pelos alters tal como
entregue pelo `.edges`.

Reincluir o ego criaria um nó de grau n−1 (conectado a todos os demais por
construção). Esse nó é trivialmente reidentificável — possui grau único e
máximo — e impossível de anonimizar sob k-anonimato estrutural: não há como
inseri-lo em um grupo de equivalência de tamanho k sem fabricar k−1 nós
universais adicionais, o que destruiria a estrutura do grafo. Como `read_edgelist`
sobre o `.edges` já entrega o grafo sem o ego por padrão, é fácil esquecer que
essa foi uma escolha; por isso ela é registrada explicitamente.

### 3.2 Componentes conexos: maior componente conexo (LCC)

A remoção do ego pode desconectar o grafo de alters, já que o ego frequentemente
funcionava como ponte entre sub-círculos. **Decisão: reter o maior componente
conexo (LCC)** de cada ego-rede após a remoção do ego.

[He et al. (2009)](https://doi.org/10.1109/WI-IAT.2009.108), operando sobre vizinhanças 1-hop, tolera grafos desconexos.
No entanto, o coeficiente de clustering médio e o ataque por subgrafos produzem
resultados mais limpos sobre um grafo conexo, e nós isolados (grau 0 após a
remoção do ego) são degenerados para ambos os ataques. A estrutura de componentes
de cada ego-rede — número de componentes e tamanho de cada um — deve ser
registrada nos logs antes do recorte, para que a fração descartada seja auditável.

### 3.3 Filtro de tamanho mínimo relativo a k_max

O valor máximo do parâmetro é `k_max = 20`, o que exige grupos de equivalência
com pelo menos 20 nós estruturalmente idênticos. Em uma ego-rede pequena, isso
força um número muito baixo de grupos e uma distorção estrutural massiva: o ponto
k=20 da curva passaria a refletir “o grafo é pequeno demais”, e não o
comportamento do algoritmo.

**Decisão: incluir no modo `multiple_egonets` apenas as ego-redes com
`n ≥ 10 · k_max = 200` nós** (após exclusão do ego e recorte ao LCC), de modo
a permitir ao menos cerca de dez grupos de equivalência no valor de `k` mais
forte. O limiar de 200 é uma regra prática e deve ser **confirmado empiricamente
na Semana 1**, após a medição das dez ego-redes (Seção 3.5).

Os IDs das ego-redes aprovadas e o limiar efetivamente aplicado devem ser
registrados no arquivo de configuração do experimento. A lista `egonet_ids` é,
portanto, o **resultado da etapa de seleção da Semana 1** (Seção 3.5); o loader
apenas **afere** que cada grafo listado satisfaz a pré-condição `n ≥ min_nodes`
e falha ruidosamente caso a configuração esteja inconsistente com os dados.
O loader não filtra nem seleciona — a config é a fonte de verdade.

### 3.4 Normalização para grafo simples

**Decisão: garantir grafo simples** — remover self-loops e deduplicar arestas
paralelas — no loader, por meio de asserção. Os arquivos `.edges` do Facebook
Ego-Nets já devem ser simples e não-direcionados, mas a verificação é barata e
evita falhas silenciosas. O grafo é tratado como não-direcionado (`nx.Graph`).

### 3.5 Seleção da ego-rede para o modo de desenvolvimento

A ego-rede usada no modo `single_egonet` não deve ser escolhida por intuição.
**Procedimento:** na Semana 1, computar para as dez ego-redes do dataset
(IDs 0, 107, 348, 414, 686, 698, 1684, 1912, 3437, 3980) as métricas básicas —
número de nós, número de arestas, densidade e número de componentes conexos
após exclusão do ego — e selecionar uma ego-rede de **tamanho mediano** que
satisfaça o filtro da Seção 3.3. O objetivo é que o marco de 29/05 seja
representativo, e não sorteado em um extremo da distribuição de tamanhos.

O `config_example.yml` atualmente fixa `egonet_id: 0`. A ego-rede do nó 0 está
entre as menores do dataset; o valor padrão deve ser revisto após a medição
(ver issue #40).

A etapa de medição da Semana 1 é responsável por duas saídas de configuração:

- **`egonet_id`** — ID da ego-rede mediana aprovada, para o modo `single_egonet`.
- **`egonet_ids`** — lista de todos os IDs aprovados pelo filtro da Seção 3.3,
  para o modo `multiple_egonets`.

A configuração (`egonet_id`, `egonet_ids` e `min_nodes`) passa a ser a fonte de
verdade para o loader. Qualquer reprovação na aferição do loader indica
divergência entre configuração e dados — e deve ser corrigida na config, não
contornada no código.

---

## 4. Procedimento de pré-processamento (especificação para o loader)

Para cada ego-rede solicitada pela configuração, o loader (`src/loaders/`) deve
executar, nesta ordem:

1. Ler o arquivo `<ego_id>.edges` como grafo não-direcionado (`nx.Graph`).
2. Remover self-loops e arestas paralelas; afirmar que o resultado é um grafo
   simples.
3. Não reintroduzir o nó ego (Seção 3.1).
4. Computar e registrar nos logs a estrutura de componentes conexos.
5. Reter o maior componente conexo (Seção 3.2).
6. **Aferir a pré-condição de tamanho:** verificar se o número de nós do grafo
   processado é maior ou igual a `min_nodes` (Seção 3.3).
   - Se `n < min_nodes`, **lançar exceção fatal** — a configuração solicitou
     um grafo que não satisfaz a pré-condição do algoritmo para `k_max`.
   - A aferição é **idêntica nos modos `single_egonet` e `multiple_egonets`**:
     `egonet_id` e `egonet_ids` já são, por contrato, o conjunto aprovado pela
     etapa de medição da Semana 1 (Seção 3.5). O loader não filtra; ele valida
     o contrato entre configuração e dados. Reprovação aqui é sinal de que a
     config está inconsistente com os dados — deve aparecer ruidosamente, não
     ser engolida em silêncio.
   - Para desabilitar a pré-condição durante iterações de desenvolvimento
     (antes do limiar estar confirmado), definir `min_nodes: 0` ou
     `min_nodes: null` no YAML. Isso torna a desabilitação uma escolha explícita
     e versionada, não um ramo silencioso de código.
7. Persistir o grafo processado em `data/processed/facebook/` e registrar nos
   logs `n`, `m`, densidade e coeficiente de clustering médio do grafo final.

O pré-processamento é mantido deliberadamente simples, conforme a mitigação
prevista na Seção 8 do plano operacional (“manter o pré-processamento o mais
simples possível”).

---

## 5. Implicação para os experimentos

A adoção de `multiple_egonets` introduz **duas fontes aninhadas de variância**
nos resultados:

- **Estrutural** — entre ego-redes distintas.
- **Algorítmica** — entre sementes aleatórias, para uma mesma ego-rede.

Para os gráficos, ambas as fontes são agregadas (*pooled*): para cada valor de
`k`, os resultados de todas as execuções `(ego-rede × semente)` são reunidos,
e reporta-se média e desvio padrão. No gráfico privacidade-vs-utilidade, cada
ponto corresponde a um valor de `k` e tem coordenadas `(utilidade média,
privacidade média)`, com barras de erro em ambos os eixos. Não é necessária,
para este baseline, uma decomposição formal da variância entre as duas fontes;
basta que o documento de resultados declare que as fontes estão agregadas e
quais são.

O número mínimo de 3 sementes por configuração `(k, dataset, ataque)` permanece
válido (plano operacional, Seção 4.6). No modo `multiple_egonets`, a
“configuração” passa a incluir também a ego-rede: cada par `(ego-rede, k)` é
executado com as 3 sementes.

---

## 6. Registro no arquivo de configuração

A decisão é codificada nas chaves abaixo, a serem adicionadas ao
`config_example.yml` e aos arquivos de configuração de experimento em
`experiments/configs/`:

```yaml
dataset:
  name: facebook_ego_nets
  source: snap
  data_path: data/processed/facebook/

  # Modo de pré-processamento (cf. docs/preprocessing_decision.md).
  #   - single_egonet:    desenvolvimento e marco de 29/05
  #   - multiple_egonets: experimentos finais
  preprocessing_mode: multiple_egonets

  # Usado apenas quando preprocessing_mode == single_egonet.
  # Definir após a medição da Semana 1 (Seção 3.5 + issue #40); 0 é provisório.
  egonet_id: 0

  # Usado apenas quando preprocessing_mode == multiple_egonets.
  # Preenchido pela etapa de seleção da Semana 1 (Seção 3.5 + issue #40).
  # ATENCAO: lista vazia causa excecao fatal no loader. Nao executar com [].
  egonet_ids: []  # TODO: preencher apos filtro de tamanho (Semana 1)

  # Sub-decisões de pré-processamento (Seção 3).
  include_ego: false   # Seção 3.1 — nó ego excluído
  component: lcc       # Seção 3.2 — reter maior componente conexo
  min_nodes: 200       # Seção 3.3 — limiar = 10 * k_max; confirmar na Semana 1.
                       # Use 0 ou null para desabilitar em YAMLs de desenvolvimento.
```

Observação: o `config_example.yml` é um *exemplo* de execução de referência sobre
uma única ego-rede e pode manter `preprocessing_mode: single_egonet` como valor
ilustrativo, desde que as chaves acima estejam documentadas. A decisão canônica
de escopo — modo final = `multiple_egonets` — é a registrada neste documento.

---

## 7. Itens em aberto

- Confirmar empiricamente, na Semana 1, o limiar de tamanho da Seção 3.3 e a
  ego-rede mediana da Seção 3.5, a partir da medição das dez ego-redes
  (ver issue #40).
- Atualizar `egonet_ids` e `egonet_id` no `config_example.yml` após essa medição.
- Registrar como comentário na issue #7 o resultado da medição (ego-redes
  aprovadas, limiar confirmado ou revisado, `egonet_id` selecionado).

---

## 8. Referências

- Plano operacional do módulo de reidentificação (baseline), Seções 4.1, 4.6, 7 e 8.

[1] [HE, X. et al.](https://doi.org/10.1109/WI-IAT.2009.108) Preserving privacy in social networks: A structure-aware approach. In: *IEEE/WIC/ACM International Joint Conference on Web Intelligence and Intelligent Agent Technology (WI-IAT 2009)*. [S. l.]: IEEE, 2009. p. 647–654.

[2] [LESKOVEC, J.; MCAULEY, J. J.](https://dl.acm.org/doi/10.5555/2999134.2999195) Learning to discover social circles in ego networks. In: *Advances in Neural Information Processing Systems (NIPS 2012)*. [S. l.]: Curran Associates, 2012. p. 539–547.

[3] SNAP — Stanford Network Analysis Platform. Dataset *[ego-Facebook](https://snap.stanford.edu/data/ego-Facebook.html)* (10 ego-redes; arquivos `.edges`, `.circles`, `.feat`, `.egofeat`, `.featnames`; união em `facebook_combined.txt`). Disponível em: <https://snap.stanford.edu/data/ego-Facebook.html>.
