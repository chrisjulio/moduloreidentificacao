# Escopo e Não-Escopo — Módulo de Reidentificação (Baseline)

> Documento de escopo do repositório. Complementa o `README.md` (operacional) e o
> `CLAUDE.md` (instruções de desenvolvimento). Onde o README responde *como rodar* e o
> CLAUDE.md responde *como desenvolver*, este documento responde **o que este módulo é,
> o que ele deliberadamente não é, e por que essa distinção importa**.
>
> Estado: atualizado em 03/06/2026. S4 (visualizações) e S5 (testes e documentação
> complementar) estão encerrados. Escopo mínimo (`[M]`) integralmente implementado.
> Varredura de `d > 1` (d-sweep) promovida para tier `[D]` (desejável) conforme D-08
> (issue #73, issue-mãe #72). Email-Enron declarado dataset secundário do tier `[D]`,
> com simetrização OR (D-11, issue-mãe #29, âncora #122). Alterações de escopo devem
> ser registradas aqui antes de serem implementadas.

---

## 1. Propósito deste documento

Este módulo implementa ataques de reidentificação contra grafos sociais anonimizados.
Lida fora de contexto, a frase "ferramenta que reidentifica pessoas em redes sociais"
descreve igualmente bem este módulo e uma ferramenta ofensiva de desanonimização. Essa
sobreposição é tecnicamente incorreta, mas não é autoevidente: ela precisa ser desfeita
de forma explícita. Numa qualificação de doutorado cujo objeto é privacidade, deixá-la
implícita é um custo retórico desnecessário e evitável.

O documento existe para fixar, de forma verificável e citável, a fronteira entre o que
este módulo faz e o que ele não faz — e, em particular, para tornar explícito por que um
instrumento de **aferição** de anonimização não é uma ferramenta de **ataque** à
privacidade, ainda que ambos compartilhem mecanismos algorítmicos. Destina-se a três
leitores: a banca de qualificação, colaboradores eventuais do repositório, e o próprio
autor em fase posterior da tese, quando o módulo migrar para o contexto temporal e para
o framework integrado.

A tese deste documento é simples e deve ser sustentável sob arguição: **medir a
resistência de uma anonimização a ataques é parte constitutiva da pesquisa de
privacidade, não um desvio dela.** Uma técnica de anonimização sem um adversário que a
teste não tem afirmação de privacidade que possa ser defendida.

---

## 2. O módulo como instrumento de aferição

O módulo é um **aferidor**. Sua função é operar como adversário formal contra
anonimizações conhecidas e produzir números sobre a resistência efetiva de cada técnica.
O produto da tarefa é uma curva privacidade-vs-utilidade defensável; a unidade de
progresso é o gráfico defensável, não o texto argumentativo nem o indivíduo
reidentificado.

"Adversário formal" tem aqui o sentido preciso que a literatura de privacidade lhe dá:
um modelo de pior caso do conhecimento e da capacidade de um atacante hipotético,
implementado para que a defesa possa ser avaliada contra ele. O adversário é uma
construção metodológica. Ele não é uma parte interessada real, não tem alvos, e não
persegue nenhuma pessoa. [He et al. (2009)](https://doi.org/10.1109/WI-IAT.2009.108) já define, no próprio texto, o adversário
estrutural que sua técnica busca neutralizar; este módulo apenas **implementa** o
adversário que a literatura de anonimização pressupõe — sem essa implementação, não
existe eixo de privacidade a ser medido.

---

## 3. Escopo — o que o módulo faz

> **Legenda de estado de implementação:**
> `[M]` = mínimo (implementado — S1 a S5 encerrados em 28/05/2026);
> `[D]` = desejável (tier ativo — d-sweep em andamento, issues #72–#78);
> `[A]` = aspiracional (fora do escopo do baseline, candidato a trabalho futuro).

Dentro do recorte do baseline (estático, prazo de 14/06/2026), o módulo:

- `[M]` Carrega grafos de **datasets públicos de pesquisa** — Facebook Ego-Nets (SNAP)
  como dataset **principal** do baseline.
- `[D]` Carrega o **Email-Enron** (SNAP, versão estática) como dataset **secundário**
  do tier desejável, reaproveitando a infraestrutura existente (runner, ataques,
  métricas, visualização) sem alterar o núcleo. Por ser um grafo direcionado por
  natureza (`A → B` = "A enviou e-mail para B"), é projetado para não-direcionado
  por **simetrização OR** (aresta `A — B` se houver e-mail em qualquer direção) —
  decisão **D-11** em `docs/decision_log.md` (issue-mãe #29, âncora #122).
- `[M]` Aplica o algoritmo de anonimização **[He et al. (2009)](https://doi.org/10.1109/WI-IAT.2009.108)** sobre esses grafos,
  com suporte a k∈{2, 5, 10, 20} e **d=1** (âncora do baseline, escopo mínimo).
- `[D]` Executa **varredura de d** (d-sweep) sobre [He et al. (2009)](https://doi.org/10.1109/WI-IAT.2009.108) com d∈{1, 2, 5, 10},
  avaliando k-anonimato structure-aware pleno. Decisão D-08 registrada em
  `docs/decision_log.md` (issue #73, issue-mãe #72). Branch `experiment/d-sweep`
  (PR #79) já mergeada; configuração YAML e logging pendentes (issue #77).
- `[A]` Aplica o algoritmo de anonimização **[Nettleton & Salas (2016)](https://doi.org/10.1016/j.eswa.2016.02.004)** como segundo
  ponto de comparação na curva privacidade-vs-utilidade.
- `[M]` Executa ataque de reidentificação **por grau** contra a saída do pipeline.
- `[M]` Executa ataque de reidentificação **por subgrafos** (isomorfismo de vizinhança
  k-hop via VF2) contra a saída do pipeline.
- `[A]` Executa ataque de reidentificação **por entropia** como terceiro nível de
  complexidade adversarial.
- `[M]` Calcula quatro métricas: taxa de reidentificação, tamanho médio dos grupos de
  equivalência, estatística D do teste KS sobre distribuição de grau, variação do
  coeficiente de clustering médio.
- `[D]` Produz a curva privacidade-vs-utilidade traçada por valor de *k*, com barras
  de erro sobre as sementes.
- `[M]` Faz tudo isso de forma reprodutível: sementes fixadas, configuração versionada,
  experimentos em lote a partir de logs estruturados JSONL.

O ciclo experimental é **fechado e autocontido**: grafo original → anonimização →
ataque → métrica. Ambas as pontas da comparação — o grafo original e o grafo
anonimizado — são artefatos que o próprio pesquisador gera e controla. O módulo não
ataca um conjunto de dados anonimizado por terceiros nem encontrado "em produção".

---

## 4. Não-escopo — o que o módulo não faz

O módulo **não**:

- **Não decide o mecanismo de privacidade** do framework integrado da tese. Produz
  medições que orientarão a deliberação metodológica da pesquisa; não a substitui.
- **Não estende a anonimização ao contexto temporal.** Isso é a Fase 2, posterior a
  14/06/2026.
- **Não implementa o gerador** de redes sintéticas (EpiCNet + Nettleton).
- **Não pretende contribuição original de pesquisa em privacidade.** É instrumento de
  validação que viabilizará a contribuição posterior da tese.
- **Não ingere dados de redes sociais reais "vivas" ou de produção.** Opera
  exclusivamente sobre datasets públicos já desidentificados e amplamente usados em
  pesquisa acadêmica de privacidade.
- **Não cruza os datasets com informação auxiliar externa.** O módulo nunca liga um
  grafo anonimizado a qualquer fonte externa de dados com o objetivo de recuperar
  identidades civis. O mundo do experimento é fechado.
- **Não produz a identificação de indivíduos como saída.** A saída são estatísticas
  agregadas (taxas de reidentificação por *k*, com barras de erro). O módulo é desenhado
  de modo a não conseguir emitir um "dossiê" sobre qualquer nó.
- **Não é uma ferramenta operacional nem implantável.** É um aparato experimental,
  voltado a medição reprodutível em lote, sem qualquer capacidade de operar contra um
  alvo vivo.
- **Não desanonimiza dados de terceiros.** Só ataca grafos que o próprio pipeline
  anonimizou; nunca um artefato anonimizado por outra parte.

---

## 5. A distinção central — instrumento de aferição × ferramenta ofensiva de desanonimização

Esta é a fronteira que o documento existe para tornar explícita. Instrumento de
aferição e ferramenta ofensiva podem compartilhar o mesmo algoritmo de ataque por
subgrafos — e ainda assim são objetos diferentes em todas as dimensões que importam
ética e metodologicamente:

| Dimensão | Instrumento de aferição (este módulo) | Ferramenta ofensiva de desanonimização |
|---|---|---|
| **Objeto do ataque** | Uma *técnica* de anonimização (ex.: "He et al. 2009, k=5") | Uma *pessoa* ou *população* real |
| **Dados de entrada** | Datasets públicos de pesquisa, já desidentificados pela fonte (SNAP) | Dados de produção, vazados ou capturados; dados de vítimas |
| **Informação auxiliar externa** | Nunca utilizada — mundo fechado, ciclo autocontido | Central à operação — o cruzamento com fontes externas é o que recupera a identidade |
| **"Identidade" recuperada** | Rótulo de nó dentro do mesmo grafo público; não há identidade civil em jogo | Identidade civil de uma pessoa real |
| **Ground truth do acerto** | O mapeamento conhecido original↔anonimizado, ambos artefatos gerados pelo pesquisador | Atributos do mundo real da vítima |
| **Produto final** | Estatística agregada: taxa de reidentificação por *k*, com desvio padrão | Lista de indivíduos identificados; dossiê |
| **Finalidade** | Certificar e comparar *defesas*; orientar a escolha de anonimização | Comprometer a privacidade de alvos |
| **Modo de operação** | Experimento offline, reprodutível, em lote, com sementes fixas | Operação dirigida contra um alvo, sob condições reais |
| **Destino do conhecimento produzido** | Realimenta o projeto de anonimização da tese | Realimenta a capacidade ofensiva |

O critério decisivo está nas linhas **objeto do ataque**, **informação auxiliar
externa** e **destino do conhecimento**. Uma ferramenta ofensiva define-se precisamente
pelo movimento de ligar um dado anonimizado a informação externa para reatar uma
identidade real — o ataque de [Narayanan & Shmatikov](https://doi.org/10.1109/SP.2008.33) ao dataset da Netflix é o exemplo
canônico. Este módulo nunca executa esse movimento. O "acerto" de uma reidentificação
aqui é verificado contra um mapeamento que o próprio pesquisador conhece de antemão,
porque foi ele quem anonimizou o grafo. Nenhum nó passa a estar exposto que não
estivesse já num dataset público. Nenhuma pessoa é identificada que não estivesse já
desidentificada pela SNAP antes de o módulo tocar nos dados.

---

## 6. Por que a reidentificação é metodologicamente necessária à pesquisa de privacidade

A objeção natural — "por que construir o ataque?" — tem uma resposta que deve ser
sustentável sob arguição.

A afirmação de privacidade de uma técnica de anonimização vale exatamente o que vale o
adversário contra o qual ela foi testada. Isto é o análogo, na pesquisa de privacidade,
do princípio de Kerckhoffs em criptografia: uma defesa só é avaliável sob a hipótese de
um adversário capaz e explícito. Uma anonimização que nunca foi submetida a um ataque
não tem grau de proteção conhecido — tem, no máximo, uma proteção alegada.

Disso decorre que **o eixo "privacidade" da curva privacidade-vs-utilidade não existe
sem um ataque que o meça.** A taxa de reidentificação é a operacionalização da
privacidade neste baseline. Sem o módulo de ataque, o gráfico defensável que é a entrega
central da tarefa seria, na melhor hipótese, meio gráfico: utilidade medida, privacidade
suposta.

Há ainda um ponto sobre o sinal do resultado. Um resultado negativo — uma técnica de
anonimização que se revela frágil sob ataque — é, em si, uma contribuição defensiva:
adverte contra a adoção de uma técnica fraca e redireciona a deliberação metodológica da
tese. O módulo serve à privacidade tanto quando confirma uma defesa quanto quando a
refuta.

---

## 7. Condições de contorno ética

- **Datasets.** Facebook Ego-Nets e Email-Enron são datasets públicos, desidentificados
  pela fonte, amplamente utilizados em pesquisa acadêmica de privacidade — inclusive na
  literatura de anonimização ([Nettleton & Salas](https://doi.org/10.1016/j.eswa.2016.02.004)) e de de-anonimização ([Backstrom](https://doi.org/10.1145/1242572.1242598),
  [Narayanan & Shmatikov](https://doi.org/10.1109/SP.2008.33)). O uso aqui está dentro das condições de licença e de
  propósito. O `README.md` registra essa condição explicitamente.
- **Sem reatamento de identidade.** O módulo não dispõe de — e não deve adquirir —
  qualquer capacidade de ligar um nó a uma pessoa real do mundo. O ciclo experimental
  permanece fechado por desenho, não por configuração; ampliar o módulo nessa direção é
  uma mudança de escopo que contraria este documento.
- **Sem dados de produção.** Nenhum dado de rede social viva, capturada ou vazada entra
  no pipeline. Datasets futuros, se incorporados, devem satisfazer a mesma condição
  (público, desidentificado, licença de pesquisa) e ser registrados aqui.
- **Dispensa de aprovação de CEP.** O uso de dados públicos desidentificados não requer
  aprovação de Comitê de Ética em Pesquisa nos termos da Resolução CNS 510/2016
  (Art. 1º, §único, III — pesquisa com bancos de dados cujas informações são agregadas,
  sem possibilidade de identificação individual). Este documento é o registro formal da
  justificativa ética adotada pelo pesquisador responsável.
- **Enquadramento na escrita da tese.** Ao reportar os resultados, o texto deve
  apresentar o módulo pelo que ele é — aferidor de defesas — e evitar formulação que o
  descreva como ferramenta de ataque a indivíduos. Este documento é a referência para
  esse enquadramento.

---

## 8. Relação com a tese e com a deliberação metodológica sobre privacidade

Este módulo é o baseline da Fase 1. O projeto de pesquisa da tese lista quatro vias de
tratamento da privacidade: k-anonimato estrutural via [He et al. (2009)](https://doi.org/10.1109/WI-IAT.2009.108); preservação de
vizinhança com t-closeness via [Nettleton & Salas (2016)](https://doi.org/10.1016/j.eswa.2016.02.004); privacidade diferencial; e
privacy by design. O módulo **não escolhe** entre elas. Ele aplica as duas primeiras a
dados reais, mede sua resistência empírica a ataques, e deixa os números orientarem a
deliberação — incluindo o caminho futuro de extensão ao contexto temporal, que é o caso
de interesse da tese e pertence à Fase 2.

> **Nota de confidencialidade:** os documentos formais da tese (proposta de pesquisa,
> artigo decisório e registros de orientação) não estão disponíveis neste repositório
> público. Essa omissão é deliberada — o repositório é aberto e os documentos acadêmicos
> internos pertencem ao ambiente institucional da pesquisa. Leitores com acesso
> institucional ao projeto podem solicitar ao autor. Referências a versões específicas
> desses documentos neste repositório devem ser lidas como apontadores internos, não
> como documentação pública esperada.

A fronteira firme deste módulo, portanto, é dupla: para trás, ele não substitui a
deliberação metodológica da tese; para o lado, ele não é uma ferramenta ofensiva. Entre
essas duas fronteiras, sua função é única e bem delimitada — produzir medições
defensáveis da resistência de anonimizações conhecidas.

---

*Documento de escopo. Atualizado em 03/06/2026 (issue #122). S1–S5 encerrados;
d-sweep tier `[D]` concluído (issues #72–#78); Email-Enron (tier `[D]`) em
enquadramento (S9, issue-mãe #29). Desvios fundamentados são esperados;
desvios não documentados, não. Toda alteração de escopo é registrada aqui antes de ser
implementada.*

---

## 9. Referências

[1] [BACKSTROM, L.; DWORK, C.; KLEINBERG, J.](https://doi.org/10.1145/1242572.1242598) Wherefore art thou R3579X? Anonymized social networks, hidden patterns, and structural steganography. In: *Proceedings of the 16th International Conference on World Wide Web (WWW 2007)*. New York: ACM, 2007. p. 181–190.

[2] [HE, X. et al.](https://doi.org/10.1109/WI-IAT.2009.108) Preserving privacy in social networks: A structure-aware approach. In: *IEEE/WIC/ACM International Joint Conference on Web Intelligence and Intelligent Agent Technology (WI-IAT 2009)*. [S. l.]: IEEE, 2009. p. 647–654.

[3] [NARAYANAN, A.; SHMATIKOV, V.](https://doi.org/10.1109/SP.2008.33) Robust de-anonymization of large sparse datasets. In: *IEEE Symposium on Security and Privacy (S&P 2008)*. [S. l.]: IEEE, 2008. p. 111–125.

[4] [NETTLETON, D. F.; SALAS, J.](https://doi.org/10.1016/j.eswa.2016.02.004) A data driven anonymization system for information rich online social network graphs. *Expert Systems with Applications*, v. 55, p. 87–105, 2016.
