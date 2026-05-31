# Módulo de Avaliação de Risco de Reidentificação em Redes Sociais Anonimizadas

> Aferidor experimental para medir, de forma agregada e reprodutível, a resistência
> efetiva de técnicas de anonimização estrutural de redes sociais a cenários formais
> de reidentificação. Componente preparatório da tese de doutorado em geração de
> redes sociais sintéticas — PPGInf/UFPR.
>
> **Estado:** escopo mínimo concluído (S1–S5). Repositório em condições de entrega
> acadêmica. Última revisão: 26/05/2026.

![CI](https://github.com/chrisjulio/moduloreidentificacao/actions/workflows/ci.yml/badge.svg)

---

## 1. Posicionamento

Este repositório implementa o pipeline `anonimização → ataque → métrica` sobre
redes sociais reais, produzindo uma **curva privacidade-vs-utilidade** por
parâmetro de anonimização.

O módulo é um **aferidor**: opera como adversário formal — uma construção
metodológica de pior caso, sem alvo real — contra anonimizações conhecidas, e
produz números sobre a resistência efetiva de cada técnica. O ciclo experimental
é fechado e autocontido: tanto o grafo original quanto o grafo anonimizado são
artefatos que o próprio experimento gera e controla. A "taxa de reidentificação"
mede acerto contra rótulos internos de nós no experimento — **não** identificação
de pessoas reais.

O objetivo **não** é propor um novo mecanismo de privacidade, mas fornecer um
instrumento de aferição que orientará a deliberação metodológica futura sobre o
mecanismo de privacidade do framework integrado da tese. A unidade de progresso
é o **gráfico defensável**.

> A fronteira deste módulo é dupla: para trás, não substitui a deliberação
> metodológica da tese; para o lado, não é uma ferramenta ofensiva. O documento
> [`docs/scope.md`](docs/scope.md) fixa essa distinção de forma citável.
>
> A documentação formal da tese (proposta de pesquisa, artigo decisório, registros
> de orientação) não é publicada neste repositório, por ser ambiente aberto;
> referências a esses documentos devem ser lidas como apontadores internos.

---

## 2. Escopo

| Eixo | Decisão | Justificativa breve |
|---|---|---|
| Temporal | Estático | Replicação direta de He et al. (2009); extensão temporal é Fase 2 da tese. |
| Dataset principal | Facebook Ego-Nets (SNAP) | Validação alinhada com a literatura contemporânea de privacidade. |
| Dataset secundário | Email-Enron (SNAP), contingente | Amplia a base de comparação se houver folga; não perseguido no baseline. |
| Anonimização primária | He et al. (2009) | Algoritmo mais simples e mais bem documentado; ponto de entrada limpo. |
| Anonimização aspiracional | Nettleton & Salas (2016) | Inclui atributos e t-closeness; fora do escopo do baseline. |
| Ataques | Grau → Subgrafos → Entropia | Ordem de complexidade crescente; os dois primeiros são o compromisso mínimo. |

### Parâmetro principal

`k ∈ {2, 5, 10, 20}` — da anonimização fraca (k=2) à forte (k=20).

### Métricas

**Privacidade**
- Taxa de reidentificação por ataque (proporção de nós-alvo corretamente
  associados a seu rótulo interno).
- Tamanho médio e mediano dos grupos de equivalência produzidos pela anonimização.

**Utilidade**
- KS-test (estatística D) sobre a distribuição de grau (original vs. anonimizado).
- Variação relativa do coeficiente de clustering médio.

Definições operacionais completas em [`docs/metrics_definitions.md`](docs/metrics_definitions.md).

---

## 3. Como reproduzir o baseline

Procedimento completo, com os dois cenários (ambiente de desenvolvimento existente
e máquina limpa) e troubleshooting, em [`docs/reproducibility.md`](docs/reproducibility.md).
O resumo operacional está abaixo.

### 3.1 Pré-requisitos

| Componente | Requisito |
|---|---|
| Python | 3.11 ou 3.12 (`requires-python = ">=3.11"`; CI testa 3.11 e 3.12) |
| Git | qualquer versão recente |
| Acesso à internet | necessário na etapa de download do dataset (SNAP) |

O backend de particionamento `pymetis` é **opcional**. Quando ausente, o algoritmo
recai automaticamente para o backend Kernighan-Lin (decisão **D-04** — ver
[`docs/decision_log.md`](docs/decision_log.md)). Essa escolha **afeta a
reprodução**: backends diferentes produzem partições diferentes. Em Windows,
`pip install pymetis` falha; consulte [`windows_pymetis.md`](windows_pymetis.md)
para instalar via Conda e configurar o VS Code.

### 3.2 Ambiente

```bash
# Criar e ativar ambiente virtual
python -m venv .venv
source .venv/bin/activate          # Linux/macOS
# .venv\Scripts\Activate.ps1       # Windows (PowerShell)

# Instalar dependências de produção e de desenvolvimento
python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt

# Sanidade do ambiente
ruff check .
pytest -q
```

### 3.3 Pipeline canônico

Todos os comandos rodam a partir da raiz do repositório, com o `.venv` ativado.

```bash
# 1. Download do dataset (uma única vez; saída não versionada)
python -m src.loaders.download

# 2. Experimento baseline (12 runs: k ∈ {2,5,10,20} × 3 sementes)
python -m experiments.run --config experiments/configs/he2009_facebook_baseline.yml

# 3. Gráfico privacidade-vs-utilidade (PDF + PNG em results/plots/)
python -m src.visualization.privacy_utility \
    --logs experiments/logs/he2009_facebook_baseline \
    --dataset facebook --out results/plots

# 4. Tabelas CSV por (dataset, ataque) em results/tables/
python -m src.visualization.tables \
    --logs experiments/logs/he2009_facebook_baseline \
    --dataset facebook --out results/tables

# 5. Verificação automática contra docs/results_baseline.md
python -m scripts.verify_reproduction --tables results/tables
```

Tempo estimado do baseline em hardware típico: ~6–12 min (dominado pelo ataque por
subgrafo). Detalhamento por etapa em [`docs/pipeline.md`](docs/pipeline.md) §5.

### 3.4 Determinismo e reprodutibilidade

- Sementes (`42, 1337, 2718`) fixadas e versionadas no YAML de configuração —
  nunca hardcoded no código.
- Mínimo de 3 execuções independentes por configuração `(k, dataset, ataque)`,
  para barras de erro.
- Outputs (gráficos, tabelas) gerados a partir de logs JSONL estruturados em
  `experiments/logs/`, não de execução interativa.
- Datasets baixados por script versionado; **não** comitados no repositório.
- Reprodutibilidade end-to-end validada (issue #27): clone limpo → `pip install`
  → execução → outputs verificados contra `docs/results_baseline.md`.
- Registro acumulativo de bugs em `/bugs/` (execução + explicação + decisão tomada),
  consultável para diagnóstico de divergências na reprodução.

Três fatores fora das sementes podem fazer os resultados divergirem e devem ser
controlados na reprodução: o backend de partição (D-04), o timeout de 60 s do
ataque por subgrafo (sensível a hardware) e a versão das bibliotecas numéricas.
Ver [`docs/reproducibility.md`](docs/reproducibility.md) §8.

---

## 4. Status do projeto

**Atualizado em 26/05/2026.** Escopo mínimo (S1–S5) concluído — 35 issues fechadas.

| Fase | Período planejado | Status |
|---|---|---|
| S1: Setup + loader + leitura He et al. | 15–22/05 | ✅ Concluída |
| S2: Implementação He et al. + validação k-anonimato | 22–29/05 | ✅ Concluída (marco 29/05 cumprido em 21/05) |
| S3: Ataques + métricas + experimento baseline | 29/05–05/06 | ✅ Concluída (adiantada para 22–23/05) |
| S4: Gráficos, tabelas e documentação técnica | 05–12/06 | ✅ Concluída (adiantada para 25/05) |
| S5: Polimento, reprodutibilidade e entrega | 12–14/06 | ✅ Concluída (em 26/05) |

**Marco intermediário não-negociável cumprido:** 21/05/2026 (antecipado em 8 dias).
k-anonimato empiricamente atingido em todas as configurações do Mínimo
(k ∈ {2, 5, 10, 20}), com `satisfied_fraction ≥ 0.9962` em k ∈ {2, 5, 10} e
`satisfied_fraction = 0.9774` no pior caso (k=20) — critério DL-01 aprovado em
todas as configurações. Ver [`docs/validacao_k_anonimato.md`](docs/validacao_k_anonimato.md)
e [`docs/decision_log.md`](docs/decision_log.md).

Escopo Desejável (Email-Enron, ataque por entropia) e Aspiracional
(Nettleton & Salas, 2016) permanecem abertos como trabalho futuro — não foram
perseguidos para não comprometer a consolidação do Mínimo.

### Componentes implementados

**S1–S2 — anonimização e validação**
- `src/anonymization/he2009.py` — pipeline completo: `partition_graph`,
  `_group_local_structures` (FSM+MF), `_modify_structure`, `_reconnect_inter_edges`,
  `anonymize(g, k, d, seed)`. Backend de particionamento em
  `src/anonymization/_partition_backend.py`.
- `src/anonymization/validation.py` — auditor independente
  `validate_k_anonymity(groups, k) → dict` (36 testes). Campos DL-01:
  `coverage_fraction`, `uncovered_fraction`, `deficit_fully_structural`.
- `src/loaders/facebook_ego.py` — loader Facebook Ego-Nets (SNAP).
- `src/loaders/download.py` — script versionado para download automático dos datasets.
- `experiments/run_validacao_k_anonimato.py` — script de validação do k-anonimato
  (marco 21/05; k=5, egonet_id=3437, n=532, m=4812).
- `experiments/run_k_sweep.py` — k-sweep k ∈ {2, 5, 10, 20}; todos aprovados
  pelo critério DL-01.
- `docs/decision_log.md` — registro de decisões técnicas (DL-01, D-04 a D-07).
- `docs/progress.md` — log de progresso sessão a sessão.
- CI: GitHub Actions + pre-commit (ruff v0.15.13).

**S3 — ataques, métricas e experimento baseline**
- `src/attacks/degree.py` — ataque por grau
  (`degree_attack(g_orig, g_anon, target, tolerance=0) → bool`).
- `src/attacks/subgraph.py` — ataque por subgrafos via VF2
  (`subgraph_attack(g_orig, g_anon, target, hop=1, timeout=None) → bool`).
- `src/metrics/` — 4 métricas: `reidentification_rate`, `equivalence_group_size`,
  `ks_test_degree`, `clustering_variation`.
- `experiments/run.py` — runner orquestrador CLI
  (`python -m experiments.run --config <yaml>`).
- `experiments/configs/he2009_facebook_baseline.yml` — config do experimento baseline.
- `docs/results_baseline.md` — tabela bruta e agregações do baseline.

**S4 — visualização e documentação técnica**
- `src/visualization/privacy_utility.py` — gráfico privacidade-vs-utilidade
  (2 painéis, barras de erro), saída PDF+PNG em `results/plots/`.
- `src/visualization/tables.py` — tabelas CSV por `(dataset, ataque)`
  em `results/tables/`.
- `docs/pipeline.md` — documentação técnica do pipeline com diagramas Mermaid,
  comandos reproduzíveis e lista de outputs.
- `docs/limitations.md` — limitações metodológicas documentadas.
- `docs/reproducibility.md` — protocolo de reprodutibilidade end-to-end.
- `docs/preprocessing_decision.md` — decisões de pré-processamento dos datasets.
- `docs/algorithm_notes.md` e `docs/metrics_definitions.md` — revisados e
  cross-referenciados.

**S5 — validação final e entrega**
- `docs/scope.md` — escopo, não-escopo e condições de contorno ética (citável).
- `docs/entregaveis.md` — lista consolidada de entregáveis por nível.
- Revisão global de README, `CLAUDE.md` e `docs/` (issue #28).

---

## 5. Resultados do experimento baseline

**Dataset:** Facebook Ego-Net 3437 (n=532, m=4812). **Parâmetros:** algoritmo
He et al. (2009), `d=1`, `sigma=0.5`, `k ∈ {2, 5, 10, 20}`, 3 sementes
(42, 1337, 2718). **Ataques:** grau e subgrafo 1-hop (timeout 60 s). Valores
abaixo são médias sobre as sementes.

| k | Veredito | coverage_fraction | rr_grau | rr_subgrafo | KS-D | clustering_var |
|---|---|---|---|---|---|---|
| 2 | SUCCESS_FULL | 1.0000 | 0.0263 | 0.7914 | 0.0000 | 0.0000 |
| 5 | SUCCESS_PARTIAL | 0.9962 | 0.0081 | 0.4060 | 0.0482 | 0.0670 |
| 10 | SUCCESS_PARTIAL | 0.9962 | 0.0226 | 0.1397 | 0.2356 | 0.1575 |
| 20 | SUCCESS_PARTIAL | 0.9774 | 0.0990 | 0.0000 | 0.6491 | 0.0904 |

**Leitura preliminar e prudente.** O ataque por subgrafo cai expressivamente com
o aumento de `k`, chegando a zero em `k=20`. O ataque por grau é menos intenso e
**não** perfeitamente monotônico (mínimo em `k=5`, maior valor em `k=20`). O KS-D
cresce fortemente em `k=10` e `k=20`, indicando maior distorção da distribuição
de grau — ou seja, mais privacidade estrutural local custa utilidade topológica.
A variação de clustering não cresce monotonicamente e exige interpretação
separada. A curva privacidade-vs-utilidade deve, portanto, ser lida em múltiplos
eixos, não como narrativa linear única.

Gráficos finais em `results/plots/`; tabelas em `results/tables/` (não versionados;
gerados localmente). Análise completa e tabela bruta em
[`docs/results_baseline.md`](docs/results_baseline.md).

---

## 6. Entregáveis

Três níveis, com linha firme entre **Mínimo** e **Desejável**. Status consolidado
em [`docs/entregaveis.md`](docs/entregaveis.md).

- **Mínimo defensável (✅ concluído).** Pipeline funcional sobre Facebook Ego-Nets
  aplicando He et al. (2009) com `k ∈ {2, 5, 10, 20}`; ataques por grau e por
  subgrafos; quatro métricas; mínimo de 3 sementes por configuração; gráfico
  privacidade-vs-utilidade com barras de erro; repositório versionado com README
  operacional e configuração reproduzível.
- **Desejável (não perseguido).** Execução adicional sobre Email-Enron; ataque
  por entropia.
- **Aspiracional (não perseguido).** Implementação inicial de Nettleton & Salas
  (2016); comparação preliminar das duas anonimizações no mesmo gráfico.

O Mínimo é entregável defensável em si; o Desejável é entregável discutível; o
Aspiracional é bônus que não deve ser perseguido em detrimento do Mínimo.

---

## 7. Estrutura do repositório

```
/data/
  /raw/                      # datasets originais (não versionados; baixados por script)
  /processed/                # datasets após pré-processamento
/src/
  /anonymization/            # He et al. (2009) [implementado]; placeholder Nettleton & Salas
  /attacks/                  # ataques por grau e subgrafos
  /metrics/                  # cálculo das quatro métricas
  /loaders/                  # carregadores de dataset (Facebook Ego-Nets) e script de download
  /visualization/            # gráfico privacy-vs-utility e tabelas CSV
/experiments/
  /configs/                  # arquivos de configuração (YAML)
  /logs/                     # logs estruturados JSONL das execuções (não versionados)
  run.py                     # runner orquestrador CLI
/results/
  /tables/                   # tabelas em CSV (não versionadas; regeneráveis)
  /plots/                    # gráficos em PDF/PNG (não versionados; regeneráveis)
/tests/                      # suíte de testes (espelha a estrutura de src/)
/scripts/                    # setup de ambiente e verificação de reprodução
/bugs/                       # registro acumulativo de bugs (execução + explicação + decisão)
/docs/
  scope.md                   # escopo, não-escopo e condições de contorno ética
  algorithm_notes.md         # notas sobre a implementação de He et al. (inclui k-sweep)
  metrics_definitions.md     # definições operacionais das métricas
  decision_log.md            # registro formal de decisões técnicas (DL-01, D-04 a D-07)
  progress.md                # log de progresso sessão a sessão
  validacao_k_anonimato.md   # resultados consolidados da validação empírica de k-anonimato
  results_baseline.md        # tabela bruta + agregações do experimento baseline
  pipeline.md                # documentação técnica do pipeline com diagramas Mermaid
  limitations.md             # limitações metodológicas do protótipo
  reproducibility.md         # guia de reprodução end-to-end
  preprocessing_decision.md  # decisões de pré-processamento dos datasets
  entregaveis.md             # entregáveis consolidados por nível
README.md                    # este arquivo — visão operacional canônica
CLAUDE.md                    # instruções de desenvolvimento para sessões de agente
WORKFLOW.md                  # protocolo de orquestração entre interfaces de trabalho
windows_pymetis.md           # ajustes Windows: ambiente Conda e backend pymetis
pyproject.toml               # metadados do projeto + configuração de ruff e pytest
requirements.txt             # dependências de produção
requirements-dev.txt         # dependências de desenvolvimento (lint, testes)
config_example.yml           # modelo de configuração de experimento
environment.yml              # ambiente Conda (caminho alternativo no Windows, com METIS)
.pre-commit-config.yaml      # hooks de pre-commit (ruff)
LICENSE                      # licença do repositório
```

A organização foi pensada para permitir migração futura para o repositório do
framework integrado da tese (EpiCNet) sem refatoração estrutural significativa.
A integração, quando ocorrer, deve dar-se apenas por interfaces explícitas e
schemas documentados — o módulo permanece arquiteturalmente independente.

---

## 8. Limitações e ameaças à validade

Registro completo e categorizado em [`docs/limitations.md`](docs/limitations.md).
Em resumo:

- **Validade interna.** Aproximações na implementação de He et al. (2009): FSM
  simplificado, fallback de particionamento (D-04), grupos incompletos residuais
  aceitáveis sob D-06, e custo/timeout do ataque por subgrafo.
- **Validade externa.** Baseline restrito a uma ego-rede específica do Facebook
  Ego-Nets; sem Email-Enron, sem redes temporais e sem dados sintéticos nesta fase.
- **Validade de construção.** A "reidentificação" medida é acerto contra rótulos
  internos de nós, não identificação de pessoas; similaridade estrutural não é
  identidade.
- **Validade ética.** O módulo opera apenas com datasets públicos desidentificados,
  em ciclo experimental fechado, sem cruzamento com bases pessoais externas e com
  saídas agregadas.

O baseline é **estático**: generalizações para redes temporais ou sintéticas
exigem novo experimento e pertencem à Fase 2 da tese.

---

## 9. Premissas

- **Linguagem.** Python 3.11+. NetworkX como padrão da área; alternativas
  (igraph, graph-tool) são aceitáveis mas exigem justificativa.
- **Hardware.** Razoável; sem requisito de GPU.
- **Datasets.** Públicos via SNAP, desidentificados pela fonte; uso dentro das
  condições de licença e de propósito acadêmico.

---

## 10. O que este módulo não faz

- Não decide o mecanismo de privacidade do framework integrado da tese — produz
  medições que orientarão essa deliberação metodológica.
- Não estende a anonimização para o contexto temporal (Fase 2 da tese).
- Não implementa o gerador de redes sintéticas.
- Não pretende contribuição original de pesquisa em privacidade — é instrumento
  de validação empírica.
- Não ingere dados de redes sociais "vivas", de produção ou vazados; não realiza
  cruzamento com bases pessoais externas; não tenta identificar pessoas reais.

---

## 11. Referências

- He, X., Vaidya, J., Shafiq, B., Adam, N., & Atluri, V. (2009). Preserving privacy
  in social networks: A structure-aware approach. *2009 IEEE/WIC/ACM International
  Joint Conference on Web Intelligence and Intelligent Agent Technology (WI-IAT)*,
  pp. 647–654. https://doi.org/10.1109/WI-IAT.2009.108
- Nettleton, D. F. & Salas, J. (2016). A data driven anonymization system for
  information rich online social network graphs. *Expert Systems with Applications*,
  55, 87–105. https://doi.org/10.1016/j.eswa.2016.02.004
- Documentação interna do projeto (não pública): artigo decisório da tese
  (Seções 4.3 e 7) e proposta original.

---

## 12. Licença e uso de dados

A licença do código está no arquivo [`LICENSE`](LICENSE).

O uso de dados públicos desidentificados (Facebook Ego-Nets, SNAP) dispensa
aprovação de Comitê de Ética em Pesquisa nos termos da Resolução CNS 510/2016
(Art. 1º, §único, III). O enquadramento ético completo está registrado em
[`docs/scope.md`](docs/scope.md) §7.

---

> **Usuários Windows:** para instalar `pymetis` via Conda e configurar o VS Code,
> consulte [`windows_pymetis.md`](windows_pymetis.md).

---

*Repositório associado à tese de doutorado em geração de redes sociais sintéticas
— PPGInf/UFPR.*
