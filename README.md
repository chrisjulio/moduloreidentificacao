# Baseline de Reidentificação em Redes Sociais Anonimizadas

> Instrumento empírico para medir a resistência efetiva de anonimizações estruturais de redes sociais a ataques de reidentificação. Componente preparatório de tese de doutorado em geração de redes sociais sintéticas — PPGInf/UFPR.

## Posicionamento

Este repositório implementa o pipeline `anonimização → ataque → métrica` sobre redes sociais reais, produzindo uma **curva privacidade-vs-utilidade** por parâmetro de anonimização. O objetivo não é propor um novo mecanismo de privacidade, mas fornecer um aferidor que orientará a deliberação metodológica futura sobre o mecanismo de privacidade do framework integrado da tese (Decisão 4.3 do artigo decisório v19*).

A unidade de progresso é o **gráfico defensável**, não o texto argumentativo.

*Documentação formal da tese e outros artefatos produzidos no escopo acadêmico não serão publicizados aqui em princípio, considerando potencial vazamento.

## Escopo

| Eixo | Decisão | Justificativa breve |
|---|---|---|
| Temporal | Estático | Replicação direta de He et al. (2009); extensão temporal é Fase 2. |
| Dataset principal | Facebook Ego-Nets (SNAP) | Validação alinhada com a literatura contemporânea de privacidade. |
| Dataset secundário | Email-Enron (SNAP), contingente | Amplia a base de comparação se houver folga no cronograma. |
| Anonimização primária | He et al. (2009) | Algoritmo mais simples e mais bem documentado; ponto de entrada limpo. |
| Anonimização aspiracional | Nettleton & Salas (2016) | Inclui atributos e t-closeness; condicionada à estabilização do pipeline. |
| Ataques | Grau → Subgrafos → Entropia | Ordem de complexidade crescente; os dois primeiros são compromisso mínimo. |

### Parâmetro principal

`k ∈ {2, 5, 10, 20}` — da anonimização fraca (k=2) à forte (k=20).

### Métricas

**Privacidade**
- Taxa de reidentificação por ataque (proporção de nós-alvo corretamente identificados).
- Tamanho médio dos grupos de equivalência produzidos pela anonimização.

**Utilidade**
- KS-test (estatística D) sobre a distribuição de grau (original vs. anonimizado).
- Variação relativa do coeficiente de clustering médio.

## Entregáveis

Três níveis, com linha firme entre **Mínimo** e **Desejável**.

- **Mínimo defensável.** Pipeline funcional sobre Facebook Ego-Nets aplicando He et al. (2009) com `k ∈ {2, 5, 10, 20}`; ataques por grau e por subgrafos; quatro métricas; mínimo de 3 sementes por configuração; gráfico privacidade-vs-utilidade com barras de erro; repositório versionado com README operacional e arquivo de configuração reproduzível.
- **Desejável.** Execução adicional sobre Email-Enron; ataque por entropia.
- **Aspiracional.** Implementação inicial de Nettleton & Salas (2016) sobre Facebook Ego-Nets; comparação preliminar das duas anonimizações no mesmo gráfico.

O Mínimo é entregável defensável em si; o Desejável é entregável discutível; o Aspiracional é bônus que não deve ser perseguido em detrimento da consolidação do Mínimo.

## Cronograma

| Período | Foco |
|---|---|
| 15–22/05 | Setup; leitura aprofundada de He et al. (2009) com extração passo a passo do algoritmo; loader para Facebook Ego-Nets. |
| 22–29/05 | Implementação de He et al. (2009); **validação obrigatória** de que o k-anonimato pretendido é empiricamente atingido. |
| 29/05–05/06 | Ataques por grau e por subgrafos; experimentos sobre Facebook Ego-Nets. |
| 05–12/06 | Geração de gráficos e tabelas; documentação técnica do pipeline. |
| 12–14/06 | Polimento; margem para imprevistos; finalização da entrega. |

**Marco intermediário não-negociável:** 29/05/2026. O k-anonimato pretendido deve ser empiricamente atingido em pelo menos uma configuração (sugerido: k=5 sobre uma ego-rede do Facebook); caso contrário, o escopo é reformulado imediatamente. Adiar o marco elimina a margem de manobra e deve ser tratado como falha de planejamento, não como acomodação.

## Estrutura do repositório

```
/data/
  /raw/                  # datasets originais (não versionados; baixados por script)
  /processed/            # datasets após pré-processamento
/src/
  /anonymization/        # He et al. (2009); placeholder Nettleton & Salas (2016)
  /attacks/              # ataques por grau, subgrafos, entropia
  /metrics/              # cálculo das quatro métricas
  /loaders/              # carregadores de dataset
/experiments/
  /configs/              # arquivos de configuração (YAML)
  /logs/                 # logs estruturados das execuções
/results/
  /tables/               # tabelas em CSV
  /plots/                # gráficos em PDF/PNG
/docs/
  algorithm_notes.md     # notas sobre implementação de He et al.
  metrics_definitions.md # definições operacionais das métricas
requirements.txt
config_example.yml
```

A organização foi pensada para permitir migração futura para `SyntheticUForgePR` sem refatoração estrutural significativa.

## Reprodutibilidade

- Sementes aleatórias fixadas e versionadas em arquivo de configuração único (YAML ou TOML).
- Mínimo de 3 execuções independentes por configuração `(k, dataset, ataque)` para barras de erro.
- Outputs (gráficos, tabelas) gerados a partir de logs estruturados, não de execução interativa.
- Datasets baixados por script versionado; **não** comitados no repositório.

## Premissas

- **Linguagem.** Python. NetworkX como padrão da área; alternativas (igraph, graph-tool) são aceitáveis mas exigem justificativa.
- **Hardware.** Razoável; sem requisito de GPU.
- **Datasets.** Disponíveis publicamente via SNAP; uso dentro das condições de licença e propósito acadêmico.

## O que este módulo não faz

- Não decide o mecanismo de privacidade do framework integrado da tese.
- Não estende a anonimização para contexto temporal.
- Não implementa o gerador (EpiCNet + Nettleton).
- Não substitui a deliberação metodológica da Decisão 4.3 do v19; produz medições que orientarão essa deliberação.
- Não pretende contribuição original de pesquisa em privacidade — é instrumento de validação que viabilizará a contribuição posterior da tese.

## Status

Em desenvolvimento. Planejamento operacional consolidado em 15/05/2026. Entrega prevista para 14/06/2026.

## Referências

- He, X. et al. (2009). Preserving privacy in social networks: A structure-aware approach. *Proceedings of the IEEE/WIC/ACM International Joint Conference on Web Intelligence and Intelligent Agent Technology (WI-IAT)*.
- Nettleton, D. F. & Salas, J. (2016). A data driven anonymization system for information rich online social network graphs. *Expert Systems with Applications*, 55, 87–105.
- Documentação interna do projeto: v19 do artigo decisório (especialmente Seções 4.3 e 7); proposta original da tese.

---

*Repositório associado à tese de doutorado em geração de redes sociais sintéticas — PPGInf/UFPR.*
