# process.md — Âncora operacional para Claude Code

> Este arquivo é o ponto de entrada para sessões de Claude Code neste repositório.
> O README.md é a fonte de verdade canônica; este arquivo traduz o README em
> instruções operacionais e registra o estado corrente de trabalho.
> Quando uma decisão consolidada no projeto Claude.ai ("Desenvolvimento de módulo
> de reidentificação de dados anonimizados") mudar algo relevante, atualize o
> README primeiro, depois reflita aqui.

---

## Contexto em uma linha

Pipeline `anonimização → ataque → métrica` sobre redes sociais reais, produzindo
curvas privacidade-vs-utilidade. Instrumento de validação para tese de doutorado
(PPGInf/UFPR) — não propõe mecanismo de privacidade novo.

Referência completa: [README.md](README.md)

---

## Fase atual

| Data | Semana | Foco |
|---|---|---|
| 15–22/05/2026 | 1 | Setup; leitura de He et al. (2009); loader Facebook Ego-Nets |
| 22–29/05/2026 | 2 | Implementação He et al.; **validação obrigatória de k-anonimato** |
| 29/05–05/06 | 3 | Ataques (grau → subgrafos); experimentos |
| 05–12/06 | 4 | Gráficos, tabelas, documentação técnica |
| 12–14/06 | 5 | Polimento e entrega |

**Marco não-negociável: 29/05/2026** — k-anonimato empiricamente atingido em ao
menos uma configuração (sugestão: k=5, uma ego-rede do Facebook). Se falhar,
reformular escopo imediatamente — não adiar.

---

## Regras de escopo

Há três níveis. A linha entre **Mínimo** e **Desejável** é firme.

- **Mínimo (obrigatório):** He et al. (2009) + Facebook Ego-Nets + k ∈ {2,5,10,20}
  + ataques por grau e subgrafos + 4 métricas + ≥3 sementes + gráfico com barras
  de erro + README operacional.
- **Desejável (perseguir se houver folga):** Email-Enron + ataque por entropia.
- **Aspiracional (não perseguir a custo do Mínimo):** Nettleton & Salas (2016).

Qualquer tarefa que ponha o Mínimo em risco deve ser interrompida e sinalizada.

---

## Convenções de código

- **Linguagem:** Python. NetworkX como padrão; igraph/graph-tool só com justificativa.
- **Sementes:** sempre lidas do arquivo YAML de configuração — nunca fixadas no código.
- **Configuração:** um arquivo YAML por experimento em `experiments/configs/`.
  Modelo: [config_example.yml](config_example.yml).
- **Reprodutibilidade:** mínimo 3 sementes independentes por configuração
  `(k, dataset, ataque)`; outputs gerados de logs estruturados, não de execução
  interativa.
- **Validação de k-anonimato:** obrigatória antes de qualquer experimento.
  Flag `validate_k_anonymity: true` no YAML; implementar verificador independente
  da anonimização.
- **Dados brutos:** nunca commitados; baixados por script versionado em `src/loaders/`.

---

## Estrutura de módulos

```
src/loaders/         # carregadores de dataset (Facebook Ego-Nets, Enron)
src/anonymization/   # He et al. (2009); placeholder Nettleton & Salas (2016)
src/attacks/         # degree_attack, subgraph_attack, (entropy_attack aspiracional)
src/metrics/         # reidentification_rate, equiv_group_size, ks_test, clustering_var
```

Cada módulo deve ser independentemente testável. Não acople carregadores a
anonimizadores; passe grafos NetworkX como interface entre módulos.

---

## Documentação técnica

- [docs/algorithm_notes.md](docs/algorithm_notes.md) — implementação passo a passo
  de He et al. (2009); atualizar durante a Semana 1.
- [docs/metrics_definitions.md](docs/metrics_definitions.md) — definições
  operacionais das métricas; considerar completo, alterar só se houver revisão
  de escopo.

---

## Sincronização com o projeto Claude.ai

O projeto Claude.ai ("Desenvolvimento de módulo de reidentificação de dados
anonimizados") é o espaço de deliberação metodológica. Quando uma decisão for
consolidada lá:

1. Atualizar o README.md com a decisão.
2. Refletir o impacto neste arquivo (fase atual, escopo, convenções).
3. Atualizar `docs/algorithm_notes.md` se for decisão algorítmica.

Claude Code parte sempre do estado atual dos arquivos — não de memória de sessão
anterior. Manter estes arquivos atualizados elimina a necessidade de reintroduzir
contexto a cada sessão.

---

## O que este repositório não faz

- Não decide o mecanismo de privacidade do framework integrado da tese.
- Não implementa o gerador (EpiCNet + Nettleton).
- Não estende para contexto temporal (Fase 2 da tese).
- Não pretende contribuição original em privacidade.
