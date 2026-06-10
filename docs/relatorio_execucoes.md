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

**Etapas executadas: 2 de 6.**

| Etapa | Escopo | Data | Branch | PR | Status |
|---|---|---|---|---|---|
| W1a | Esqueleto em `academic/` + matriz + este registro | 2026-06-09 | `docs/relatorio-skeleton-w1a` | [#181](https://github.com/chrisjulio/moduloreidentificacao/pull/181) | ✅ executada (PR **MERGED**) |
| W1b | Seções 1–2: introdução/posicionamento (DL-06) + independência do EpiCNet | 2026-06-09 | `docs/relatorio-w1b-intro-epicnet` | (a preencher no PR) | ✅ executada (PR em revisão) |
| W1c | Seções 3–4: método + desenho experimental [M]/[D] | — | — | — | ⏳ pendente |
| W1d | Seção 5: resultados (a mais pesada — sessão própria) | — | — | — | ⏳ pendente |
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
