# Registro de execuções — Relatório de qualificação (#174)

> **Propósito.** Contabiliza e registra as **execuções das etapas de redação**
> do relatório de qualificação ([#174](https://github.com/chrisjulio/moduloreidentificacao/issues/174),
> desdobramento S10-W1a..f validado pelo autor em 2026-06-09). Decisão do autor
> (2026-06-09): as etapas **não** são formalizadas como sub-issues no GitHub —
> o rastreio é feito por **comentário de execução na própria #174** + este
> registro versionado. Complementa a matriz de rastreabilidade
> ([`relatorio_rastreabilidade.md`](relatorio_rastreabilidade.md)), que mapeia
> seção → fontes → `W-NN` → figuras.
>
> **Regra de atualização:** cada etapa executada adiciona (1) uma linha na
> tabela de contabilização, (2) uma seção de registro detalhado abaixo, em
> ordem cronológica, e (3) um comentário espelho na #174. Nunca sobrescrever
> registros anteriores.

---

## Contabilização

**Etapas executadas: 4 de 6.**

| Etapa | Escopo | Data | Branch | PR | Status |
|---|---|---|---|---|---|
| W1a | Esqueleto em `academic/` + matriz + este registro | 2026-06-09 | `docs/relatorio-skeleton-w1a` | [#181](https://github.com/chrisjulio/moduloreidentificacao/pull/181) | ✅ executada (PR **MERGED**) |
| W1b | Seções 1–2: introdução/posicionamento (DL-06) + independência do EpiCNet | 2026-06-09 | `docs/relatorio-w1b-intro-epicnet` | [#182](https://github.com/chrisjulio/moduloreidentificacao/pull/182) | ✅ executada (PR **MERGED**) |
| W1c | Seções 3–4: método + desenho experimental [M]/[D] | 2026-06-09 | `docs/relatorio-w1c-metodo-desenho` | [#183](https://github.com/chrisjulio/moduloreidentificacao/pull/183) | ✅ executada (PR **MERGED**) |
| W1d | Seção 5: resultados (a mais pesada — sessão própria) | 2026-06-09 | `docs/relatorio-w1d-resultados` | [#185](https://github.com/chrisjulio/moduloreidentificacao/pull/185) | ✅ executada (PR em revisão) |
| W1e | Seções 6–8: limitações, reprodutibilidade, ética | — | — | — | ⏳ pendente |
| W1f | Revisão integrada + fechamento da DoD da #174 | — | — | — | ⏳ pendente |

---

## Registros de execução

### W1a — 2026-06-09 — Esqueleto do relatório + rastreabilidade pública

- **Pré-verificação de bloqueios:** PRs #176 (infraestrutura `academic/`) e
  #179 (DL-06) confirmados `MERGED` via `gh`; nenhum PR aberto.
- **Artefato privado (gitignorado, fora do diff):**
  `academic/relatorio_qualificacao.md` — esqueleto com as 8 seções da
  estrutura mínima da #174 + apêndices candidatos; cada seção com checklist
  de conteúdo, fontes citáveis (docs/decisões `D-xx`/`DL-xx`), destinos
  `W-NN` e figuras a inserir; regra global de terminologia de aferição;
  DL-06 abrindo a introdução. Sem texto substantivo (cabe a W1b..e).
  Backup externo a cargo do autor.
- **Artefatos públicos (versionados no PR #181):**
  - [`relatorio_rastreabilidade.md`](relatorio_rastreabilidade.md) — sumário
    do esqueleto, matriz seção → fontes → `W-NN` → figuras → etapa,
    inventário de figuras/tabelas citáveis (versionadas × regeneráveis).
  - Este registro de execuções.
  - `progress.md` atualizado (estado + histórico).
- **Decisão de rastreio (autor, 2026-06-09):** sem sub-issues no GitHub;
  comentário de execução na #174 + este registro são suficientes.
- **Verificação:** `git check-ignore` confirma privacidade do esqueleto;
  `ruff check .` limpo; só docs — código congelado (S10-W) respeitado.
- **Próxima etapa:** W1b, após merge do PR #181.

### W1b — 2026-06-09 — Seções 1–2: introdução/posicionamento + independência do EpiCNet

- **Pré-verificação de bloqueios:** PR #181 (W1a) confirmado `MERGED` via
  `gh pr view 181` (`mergedAt: 2026-06-10T00:32:33Z`); nenhum PR aberto.
- **Artefato privado (gitignorado, fora do diff):** redação substantiva das
  Seções 1 e 2 em `academic/relatorio_qualificacao.md`, substituindo os
  placeholders do esqueleto; cabeçalho de status atualizado para
  "EM REDAÇÃO (S10-W1b)". Backup externo a cargo do autor.
  - **Seção 1 — Introdução e posicionamento** (4 subseções): §1.1 premissa
    fundadora **DL-06** ("anonimizar não é o suficiente") abrindo o texto,
    com a cadeia argumentativa hipótese → replicação por meios próprios →
    evidência empírica (B1, cross-ref Seção 5) → motivação do EpiCNet no
    nível da tese; §1.2 o módulo como aferidor/adversário formal e ciclo
    experimental fechado (`scope.md` §2; `README.md` §1); §1.3 fronteira
    instrumento × ferramenta ofensiva (dimensões de `scope.md` §5; exemplo
    canônico Narayanan & Shmatikov); §1.4 não-escopo (`scope.md` §4) e
    necessidade metodológica (análogo de Kerckhoffs, `scope.md` §6).
  - **Seção 2 — Independência em relação ao EpiCNet** (3 subseções): §2.1
    separação de responsabilidades (4 vias da tese, módulo não escolhe;
    fronteira tripla de `README.md` §10 — Nettleton & Salas citado apenas
    como trabalho futuro, sem afirmar execução); §2.2 reprodutibilidade como
    condição verificável de independência (configs/sementes/logs/CI; #27);
    §2.3 uso futuro como benchmark/auditoria do framework integrado
    (`scope.md` §8).
  - Checklists do esqueleto preservados em cada seção como "Cobertura do
    checklist (W1b)" com itens marcados — insumo da revisão integrada W1f.
  - **Terminologia de aferição** respeitada (sem "quebrar anonimização",
    "identificar usuários", "desanonimizar pessoas").
- **Artefatos públicos (versionados neste PR):** matriz
  ([`relatorio_rastreabilidade.md`](relatorio_rastreabilidade.md)) com W1b
  marcada concluída; este registro; `progress.md` atualizado.
- **Verificação:** `git check-ignore academic/relatorio_qualificacao.md`
  confirma privacidade; diff público contém só docs de rastreabilidade —
  código congelado (S10-W) respeitado.
- **Próxima etapa:** W1c (Seções 3–4: método + desenho experimental), após
  merge do PR desta etapa.

### W1c — 2026-06-09 — Seções 3–4: método + desenho experimental [M]/[D]

- **Pré-verificação de bloqueios:** PR #182 (W1b) confirmado `MERGED` via
  `gh` (`mergedAt: 2026-06-10T00:45:44Z`); nenhum PR aberto.
- **Artefato privado (gitignorado, fora do diff):** redação substantiva das
  Seções 3 e 4 em `academic/relatorio_qualificacao.md`, substituindo os
  placeholders do esqueleto; cabeçalho de status atualizado para
  "EM REDAÇÃO (S10-W1c)". Backup externo a cargo do autor.
  - **Seção 3 — Método** (7 subseções): §3.1 visão geral do pipeline
    (config → anonimização → ataque → métrica → visualização; outputs
    gerados de logs JSONL, `pipeline.md` §1); §3.2 anonimizador He et al.
    (2009) — 5 fases, FSM simplificado, backends pymetis/Kernighan-Lin com
    `partition_backend` gravado no JSONL; §3.3 uniformidade de parâmetros
    entre datasets (**W-01/DL-05**) — tabela dos 5 parâmetros
    (k∈{2,5,10,20}, d=1, sigma=0.5, s_max=4, `add_or_delete`), defaults do
    runner idênticos aos valores explícitos do Enron, valor efetivo
    auditável nos logs; §3.4 cenários formais de reidentificação — grau
    (tolerance=0) e subgrafo 1-hop, VF2 (Facebook) × WL-bucketing (Enron,
    **D-16**), com a **equivalência semântica VF2↔WL** (**W-02**) em três
    camadas (invariante necessário com viés conservador; 100% de
    equivalência exata em grafos pequenos; 70 nós estratificados no Enron,
    0 divergências) — não aproximação heurística; §3.5 validade da execução
    Enron (**W-03/D-13**) — custo agregado ⇒ `subgraph_timeout_count = 0`,
    gate trivialmente satisfeito, validade repousa na prova WL=VF2; §3.6 as
    4 métricas com definição operacional (`metrics_definitions.md`;
    `data_dictionary.md` §2–§3); §3.7 validação independente de k-anonimato
    (**DL-01** — critério substantivo `deficit_fully_structural`, piso 0,9
    rebaixado a limite operacional; `validation.py` sem import de
    `he2009.py`).
  - **Seção 4 — Desenho experimental** (5 subseções): §4.1 frase canônica
    de **W-05** verbatim + consequência de leitura (tendências, não
    magnitudes; `data_dictionary.md` §1.1); §4.2 Facebook [M] — ego-rede
    3437, exclusão do ego, LCC, piso `10 × k_max`
    (`preprocessing_decision.md` §3), n=532/m=4.812; resíduo
    `multiple_egonets` encaminhado à Seção 6 (B2); §4.3 Enron [D] —
    simetrização **OR** (**D-11**) com justificativa tripla e alternativa
    AND rejeitada, LCC n=33.696/m=180.811; §4.4 configs YAML versionados,
    3 sementes [42, 1337, 2718], 12 runs por dataset; §4.5 d-sweep como
    exercício da propriedade estrutural — **grade corrigida para
    d∈{1,2,5,10}** (48 runs, `results_dsweep.md`; o esqueleto listava
    {1,5,10}), d=2 anotado degenerate (D-08/D-10), cross-ref Seção 5.
  - Checklists do esqueleto preservados em cada seção como "Cobertura do
    checklist (W1c)" com itens marcados — insumo da revisão integrada W1f.
  - **Terminologia de aferição** respeitada (sem "quebrar anonimização",
    "identificar usuários", "desanonimizar pessoas").
- **Artefatos públicos (versionados neste PR):** matriz
  ([`relatorio_rastreabilidade.md`](relatorio_rastreabilidade.md)) com W1c
  marcada concluída; este registro; `progress.md` atualizado.
- **Verificação:** `git check-ignore academic/relatorio_qualificacao.md`
  confirma privacidade; diff público contém só docs de rastreabilidade —
  código congelado (S10-W) respeitado.
- **Próxima etapa:** W1d (Seção 5: resultados — a mais pesada, sessão
  própria), após merge do PR desta etapa.

### W1d — 2026-06-09 — Seção 5: resultados

- **Pré-verificação de bloqueios:** PR #183 (W1c) confirmado `MERGED` via
  `gh` (`mergedAt: 2026-06-10T00:59:45Z`); nenhum PR aberto.
- **Artefato privado (gitignorado, fora do diff):** redação substantiva da
  Seção 5 em `academic/relatorio_qualificacao.md`, substituindo o
  placeholder do esqueleto; cabeçalho de status atualizado para
  "EM REDAÇÃO (S10-W1d)". Backup externo a cargo do autor.
  - **Seção 5 — Resultados** (7 subseções, todo número proveniente dos
    relatórios versionados `results_baseline.md` / `results_dsweep.md` /
    `results_enron.md`, regeneráveis dos logs JSONL): §5.1 baseline
    Facebook [M] (d=1) — k-anonimato empiricamente atingido em
    k∈{2,5,10,20} pelo critério DL-01 (SUCCESS_FULL em k=2; cobertura
    ≥0,9774; déficit 100% estrutural, D-06), tabela agregada por k
    embutida, leitura da curva (trade-off canônico; rr_grau cresce em k
    alto) e **nota do motor** (achado A1: baseline em Kernighan-Lin,
    inócuo em d=1 — partições triviais de 1 nó; d-sweep/Enron em pymetis;
    implicação encaminhada à Seção 6/C2); §5.2 leitura-chave **B1** — d=1
    afere k-anonimato de grau; contraste d=1 vs d∈{5,10} como evidência
    empírica de privacidade estrutural; §5.3 d-sweep (48 runs, pymetis
    48/48, 33 SP / 15 FLC com déficit estrutural em todos) — tendências
    opostas dos dois ataques em k (deslocamento do vetor de ataque),
    efeito de d (EGS ≈ k·d), combos degenerados documentados (D-08/D-10),
    zeros genuínos (diagnóstico #93/DL-02); §5.4 Enron [D] — 12 runs
    SUCCESS_PARTIAL, tabela agregada embutida, rr_subgrafo monotônico
    0,124→0,057, rr_grau residual (~40× menor), utilidade melhor
    preservada em escala, divergência em k alto (escala, não mecanismo),
    **nota da cota 1/k** (violação esperada em k=20, não bug); §5.5 **B1
    generalizável** (**W-04**) — critério do checklist satisfeito nos dois
    datasets (FB k=2: 0,7914 vs 0,0263; Enron k=2: 0,1241 vs 0,0033),
    sinal qualitativo robusto, magnitudes não comparáveis; §5.6 painel
    normalizado FB×Enron (**DL-04/W-06**) — por que sobrepor magnitudes é
    enganoso (3 confundidores), painéis (A) fração da cota 1/k com
    cruzamentos e (B) decaimento relativo, alternativa log rejeitada,
    snapshot versionado `docs/assets/comparison_fb_enron.{png,csv}`; §5.7
    métrica de entropia baseline uniforme (**D-17**) — métrica, não
    ataque; grau de anonimato normalizado como acréscimo não-redundante;
    nota explícita de que os logs consolidados **antecedem** a métrica e
    não reportam entropia (sem citar dado inexistente); extensão não
    uniforme registrada (#148).
  - Checklist do esqueleto preservado como "Cobertura do checklist (W1d)"
    com itens marcados — insumo da revisão integrada W1f; tabela de
    figuras/tabelas atualizada (embutidas × referenciadas; inserção física
    na conversão final, W1f).
  - **Terminologia de aferição** respeitada (sem "quebrar anonimização",
    "identificar usuários", "desanonimizar pessoas").
- **Artefatos públicos (versionados neste PR):** matriz
  ([`relatorio_rastreabilidade.md`](relatorio_rastreabilidade.md)) com W1d
  marcada concluída; este registro; `progress.md` atualizado.
- **Verificação:** `git check-ignore academic/relatorio_qualificacao.md`
  confirma privacidade; diff público contém só docs de rastreabilidade —
  código congelado (S10-W) respeitado.
- **Próxima etapa:** W1e (Seções 6–8: limitações, reprodutibilidade,
  ética), após merge do PR desta etapa.
