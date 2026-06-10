# Registro de execuções — Artigo (#175)

> **Propósito.** Contabiliza e registra as **execuções das etapas de redação**
> do artigo ([#175](https://github.com/chrisjulio/moduloreidentificacao/issues/175),
> desdobramento S10-W2a..f — proposto e **validado pelo autor em 2026-06-10**
> na #175). Rastreio no mesmo molde da #174 (decisão do autor): as etapas não
> são formalizadas como sub-issues no GitHub — comentário de execução na
> própria #175 + este registro versionado. Complementa a matriz de
> rastreabilidade ([`artigo_rastreabilidade.md`](artigo_rastreabilidade.md)),
> que mapeia seção → insumo (relatório) → fontes → `W-NN` → figuras.
>
> **Regra de atualização:** cada etapa executada adiciona (1) uma linha na
> tabela de contabilização, (2) uma seção de registro detalhado abaixo, em
> ordem cronológica, e (3) um comentário espelho na #175. Nunca sobrescrever
> registros anteriores.

---

## Contabilização

**Etapas executadas: 1 de 6.**

| Etapa | Escopo | Data | Branch | PR | Status |
|---|---|---|---|---|---|
| W2a | Esqueleto em `academic/artigo.md` + matriz + este registro | 2026-06-10 | `docs/artigo-skeleton-w2a` | [#188](https://github.com/chrisjulio/moduloreidentificacao/pull/188) | ✅ MERGED (2026-06-10) |
| W2b | Seções 1–2: introdução + trabalhos relacionados | — | — | — | ⏳ pendente |
| W2c | Seção 3: método condensado | — | — | — | ⏳ pendente |
| W2d | Seção 4: resultados (a mais pesada — sessão própria) | — | — | — | ⏳ pendente |
| W2e | Seções 5–6: discussão + conclusão + abstract final | — | — | — | ⏳ pendente |
| W2f | Revisão integrada + fechamento da DoD da #175 | — | — | — | ⏳ pendente |

---

## Registros de execução

### W2a — 2026-06-10 — Esqueleto do artigo + rastreabilidade pública

- **Pré-verificação de bloqueios:** PR #187 (W1f do relatório) confirmado
  `MERGED` via `gh pr view 187` (`mergedAt: 2026-06-10T13:17:15Z`); issue
  **#174 CLOSED** (`2026-06-10T13:17:16Z`) — a dependência declarada na #175
  (relatório consolidado antes do artigo) está satisfeita; nenhum PR aberto.
- **Artefato privado (gitignorado, fora do diff):** `academic/artigo.md` —
  esqueleto com as 6 seções da estrutura mínima da #175, cada uma com
  checklist de conteúdo, fontes citáveis e cuidados ("não fazer"); tese
  central (B1/W-04) fixada no cabeçalho com a tabela k=2 dos dois datasets;
  **mapa de compressão relatório → artigo** (o diferencial deste esqueleto
  em relação ao do relatório: cada seção do artigo aponta o trecho do
  relatório que comprime e o que corta); regra global de terminologia de
  aferição; DoD emendada da #175 reproduzida. Sem texto substantivo
  (cabe a W2b..e). Backup externo a cargo do autor.
- **Artefatos públicos (versionados no PR):**
  - [`artigo_rastreabilidade.md`](artigo_rastreabilidade.md) — sumário do
    esqueleto, matriz seção → insumo → fontes → `W-NN` → figuras → etapa,
    estado por etapa.
  - Este registro de execuções.
  - `progress.md` atualizado (estado + histórico).
- **Proposta de desdobramento (aguardando validação na #175):** 6 etapas
  W2a..f espelhando o padrão validado da #174; sem sub-issues (comentário de
  execução + este registro). Racional do corte: W2d (resultados) isolada em
  sessão própria, como a W1d (a etapa mais pesada do relatório); W2b agrupa
  introdução + trabalhos relacionados (ambos derivados de §1–§2 do
  relatório); W2e agrupa discussão + conclusão + abstract (escrito por
  último, prática padrão).
- **Verificação:** `git check-ignore` confirma privacidade do esqueleto;
  só docs — código congelado (S10-W) respeitado.
- **Próxima etapa:** W2b, após merge deste PR **e** validação do
  desdobramento pelo autor na #175.

### Validação do desdobramento — 2026-06-10 (não é etapa de redação)

- **Pré-verificação:** PR **#188** (W2a) confirmado `MERGED` via `gh pr view
  188` (`mergedAt: 2026-06-10T13:52:52Z`); nenhum PR aberto.
- **Decisões do autor sobre os 3 pontos abertos da proposta** (registradas em
  [comentário na #175](https://github.com/chrisjulio/moduloreidentificacao/issues/175#issuecomment-4671084769)):
  1. **Modelo de rastreio:** mantido o da #174 — sem sub-issues; comentário
     de execução na #175 + este registro.
  2. **Agrupamento das etapas:** mantido como proposto (W2b..f, com W2d em
     sessão própria).
  3. **Venue/template:** sem template por ora — Markdown neutro, conversão
     posterior (pandoc); limites de página tratados quando houver venue-alvo.
- **Decisão de ritmo:** esta sessão registra **apenas a validação** (decisão
  do autor); a **W2b** fica liberada para a próxima sessão — 1 etapa por
  sessão, bloqueio verificado via `gh` antes de iniciar.
