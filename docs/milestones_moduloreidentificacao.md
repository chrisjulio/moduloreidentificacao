# Milestones — Módulo de Reidentificação

**Repositório:** [chrisjulio/moduloreidentificacao](https://github.com/chrisjulio/moduloreidentificacao)
**Atualizado em:** 2026-05-23 (11h12)

---

## S1 — Fundação (ENCERRADO ✅)

Todas as 11 issues de S1 concluídas. Registradas para referência histórica.

| # | Título resumido | Status |
|---|---|---|
| [#4](https://github.com/chrisjulio/moduloreidentificacao/issues/4) | Script de download Facebook Ego-Nets (SNAP) | ✅ Fechada |
| [#5](https://github.com/chrisjulio/moduloreidentificacao/issues/5) | Loader `load_facebook_egonet(egonet_id, data_dir)` | ✅ Fechada |
| [#6](https://github.com/chrisjulio/moduloreidentificacao/issues/6) | Teste do loader Facebook Ego-Net | ✅ Fechada |
| [#7](https://github.com/chrisjulio/moduloreidentificacao/issues/7) | Decidir modo de pré-processamento das ego-redes | ✅ Fechada |
| [#8](https://github.com/chrisjulio/moduloreidentificacao/issues/8) | Leitura He et al. (2009) — Seção 1: k-anonimato estrutural | ✅ Fechada |
| [#9](https://github.com/chrisjulio/moduloreidentificacao/issues/9) | Leitura He et al. (2009) — Seção 2: algoritmo principal | ✅ Fechada |
| [#10](https://github.com/chrisjulio/moduloreidentificacao/issues/10) | Leitura He et al. (2009) — Seções 3–4: operações e parada | ✅ Fechada |
| [#32](https://github.com/chrisjulio/moduloreidentificacao/issues/32) | Setup local: ambiente Python e dependências | ✅ Fechada |
| [#33](https://github.com/chrisjulio/moduloreidentificacao/issues/33) | Esboço da API do anonimizador (skeleton sem implementação) | ✅ Fechada |
| [#34](https://github.com/chrisjulio/moduloreidentificacao/issues/34) | Definir `metrics_definitions.md` §k-anonymity-verifier | ✅ Fechada |
| [#40](https://github.com/chrisjulio/moduloreidentificacao/issues/40) | Medir ego-redes e selecionar `egonet_id` mediano | ✅ Fechada |

---

## S2 — Implementação do anonimizador He et al. (ENCERRADO ✅)

### Decisões de design

| # | Título resumido | Status |
|---|---|---|
| [#43](https://github.com/chrisjulio/moduloreidentificacao/issues/43) | D-07: política de normalização de tamanho de LSs (Opção A adotada) | ✅ Fechada |
| [#44](https://github.com/chrisjulio/moduloreidentificacao/issues/44) | Adicionar `pymetis` ao `requirements.txt` e validar CI | ✅ Fechada |

### Implementação

| # | Título resumido | Principal tarefa | Status |
|---|---|---|---|
| [#45](https://github.com/chrisjulio/moduloreidentificacao/issues/45) | `src/anonymization/_partition_backend.py` | Módulo de particionamento com backends `pymetis`/KL e fallback automático | ✅ Fechada |
| [#11](https://github.com/chrisjulio/moduloreidentificacao/issues/11) | `_partition_neighborhoods(G, d)` | Particionar grafo em Local Structures de tamanho `d`, minimizando inter-arestas | ✅ Fechada |
| [#12](https://github.com/chrisjulio/moduloreidentificacao/issues/12) | `_group_isomorphic` (FSM + fator MF) | Agrupar Local Structures isomórficas via Frequent Subgraph Mining | ✅ Fechada |
| [#13](https://github.com/chrisjulio/moduloreidentificacao/issues/13) | `_modify_structure(groups, seed, add_only)` | Modificar estruturalmente grupos de equivalência para satisfazer cardinalidade mínima k | ✅ Fechada |
| [#14](https://github.com/chrisjulio/moduloreidentificacao/issues/14) | `anonymize(G, k, d, seed)` — pipeline completo com reconexão | Orquestrar as 4 etapas do pipeline incluindo reconexão pós-modificação | ✅ Fechada |
| [#15](https://github.com/chrisjulio/moduloreidentificacao/issues/15) | `validate_k_anonymity` — auditor independente → dict | Verificador externo de k-anonimato com log estruturado de violações | ✅ Fechada |
| [#56](https://github.com/chrisjulio/moduloreidentificacao/issues/56) | Testes `validate_k_anonymity`: cobertura dos campos DL-01 | Estender suite de testes para cobrir `coverage_fraction`, `uncovered_fraction` e `deficit_fully_structural` | ✅ Fechada (22/05) |

### Marco e validação

| # | Título resumido | Principal tarefa | Status |
|---|---|---|---|
| [#16](https://github.com/chrisjulio/moduloreidentificacao/issues/16) | **MARCO 29/05** — Sanidade k=5, d=1 sobre ego-rede Facebook | Executar anonimização com 3 sementes e validar resultado (sucesso pleno ou parcial ≥ 0,9) | ✅ Fechada (22/05) |
| [#17](https://github.com/chrisjulio/moduloreidentificacao/issues/17) | Testes de sanidade adicionais: k=2, k=10, k=20 | Estender validação para os demais valores de k do escopo mínimo | ✅ Fechada (22/05) |
| [#18](https://github.com/chrisjulio/moduloreidentificacao/issues/18) | Documentar resultado do marco 29/05 | Registrar em `docs/milestone_29_05.md` configurações, hashes, resultados e decisão | ✅ Fechada (22/05) |

---

## S3 — Ataques e métricas (ENCERRADO ✅)

| # | Título resumido | Principal tarefa | Status |
|---|---|---|---|
| [#19](https://github.com/chrisjulio/moduloreidentificacao/issues/19) | `src/attacks/degree.py` | Ataque de reidentificação por grau do nó | ✅ Fechada (22/05) |
| [#20](https://github.com/chrisjulio/moduloreidentificacao/issues/20) | `src/attacks/subgraph.py` (VF2) | Ataque por isomorfismo de subgrafo induzido via VF2 (1-hop) | ✅ Fechada (22/05) |
| [#21](https://github.com/chrisjulio/moduloreidentificacao/issues/21) | `src/metrics/` (4 métricas) | Taxa de reidentificação, tamanho de grupo de equivalência, KS-test de grau e variação de clustering | ✅ Fechada (22/05) |
| [#22](https://github.com/chrisjulio/moduloreidentificacao/issues/22) | `experiments/run.py` (runner CLI) | CLI que orquestra anonimização + ataques + métricas com log JSONL | ✅ Fechada (22/05) |
| [#23](https://github.com/chrisjulio/moduloreidentificacao/issues/23) | Execução: experimento baseline Facebook Ego-Nets | 4k × 2 ataques × 3 sementes, logs estruturados em `experiments/logs/` | ✅ Fechada (23/05) |

---

## S4 — Visualização e documentação técnica (EM ANDAMENTO 🔄)

| # | Título resumido | Principal tarefa | Status |
|---|---|---|---|
| [#24](https://github.com/chrisjulio/moduloreidentificacao/issues/24) | Gráfico privacy-vs-utility | Curvas por k com barras de erro — PDF + PNG em `results/plots/` | 🔴 Aberta |
| [#25](https://github.com/chrisjulio/moduloreidentificacao/issues/25) | Tabelas CSV de resultados | Uma tabela por `(dataset, ataque)` em `results/tables/` | 🔴 Aberta |
| [#26](https://github.com/chrisjulio/moduloreidentificacao/issues/26) | Documentação técnica final do pipeline | `docs/pipeline.md` com diagrama e comandos de reprodução end-to-end | 🔴 Aberta |

---

## S5 — Validação final e entrega (14/06)

| # | Título resumido | Principal tarefa | Status |
|---|---|---|---|
| [#27](https://github.com/chrisjulio/moduloreidentificacao/issues/27) | Reprodutibilidade end-to-end (do zero) | Clonar em ambiente limpo e verificar que todos os outputs se reproduzem | 🔴 Aberta |
| [#28](https://github.com/chrisjulio/moduloreidentificacao/issues/28) | README final + revisão da documentação | Revisar README, CLAUDE.md, docs/ e gerar `docs/entregaveis.md` | 🔴 Aberta |

---

## Escopo Desejável / Aspiracional (condicionais)

> Só entram em escopo se o Mínimo estiver consolidado com folga.

| # | Rótulo | Condição de entrada | Principal tarefa |
|---|---|---|---|
| [#29](https://github.com/chrisjulio/moduloreidentificacao/issues/29) | DESEJÁVEL | Mínimo consolidado com folga até 05/06 | Loader Email-Enron como dataset secundário |
| [#30](https://github.com/chrisjulio/moduloreidentificacao/issues/30) | DESEJÁVEL | Após consolidar Mínimo | Ataque por entropia reutilizando grupos de equivalência |
| [#31](https://github.com/chrisjulio/moduloreidentificacao/issues/31) | ASPIRACIONAL | Desejável consolidado com folga real até 12/06 | Implementação inicial de Nettleton & Salas (2016) |

---

*Documento gerado automaticamente a partir da API do GitHub em 2026-05-23.*
