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

**Etapas executadas: 2 de 6.**

| Etapa | Escopo | Data | Branch | PR | Status |
|---|---|---|---|---|---|
| W2a | Esqueleto em `academic/artigo.md` + matriz + este registro | 2026-06-10 | `docs/artigo-skeleton-w2a` | [#188](https://github.com/chrisjulio/moduloreidentificacao/pull/188) | ✅ MERGED (2026-06-10) |
| W2b | Seções 1–2: introdução + trabalhos relacionados | 2026-06-10 | `docs/artigo-w2b-intro-relacionados` | [#191](https://github.com/chrisjulio/moduloreidentificacao/pull/191) | ✅ executada (PR aberto) |
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

### W2b — 2026-06-10 — Seções 1–2 (introdução + trabalhos relacionados)

- **Pré-verificação de bloqueios:** PR **#190** (registro da validação)
  confirmado `MERGED` via `gh pr view 190` (`mergedAt:
  2026-06-10T14:11:15Z`); nenhum PR aberto. Desdobramento já validado pelo
  autor (comentário de 2026-06-10 na #175) — pré-condições da W2b
  satisfeitas.
- **Texto privado (gitignorado, fora do diff):** Seções 1–2 redigidas em
  `academic/artigo.md`, substituindo os checklists do esqueleto (preservados
  como "Cobertura do checklist (W2b)" para a revisão W2f):
  - **Resumo provisório** (a reescrever na W2e): tese central com os números
    de k=2 dos dois datasets (Facebook 0,7914 vs 0,0263 ~30×; Enron 0,1241
    vs 0,0033 ~38×).
  - **Seção 1 — Introdução** (5 parágrafos): premissa fundadora DL-06
    abrindo o texto (topologia como quase-identificador; hipótese demonstrada
    em He et al. 2009 → prova por meios próprios); contribuição tripla
    (aferidor formal reprodutível; curvas privacidade-vs-utilidade; achado
    generalizável ~30–38× em k=2); fronteira aferidor × ferramenta ofensiva
    (4 dimensões; ciclo fechado; análogo a Kerckhoffs; resultado negativo
    como contribuição defensiva); enquadramento ético em 3 frases (SNAP
    desidentificado; sem dado pessoal novo; acerto contra rótulos internos);
    parágrafo de estrutura do artigo.
  - **Seção 2 — Trabalhos relacionados** (4 parágrafos): Sweeney 2002
    (origem tabular do k-anonimato); Backstrom 2007 (ataques ativos/passivos
    como motivação) e a escada grau → vizinhança (Liu & Terzi 2008; Zhou &
    Pei 2008; He et al. 2009 — defesa **e** adversário implementados);
    Narayanan & Shmatikov 2008 como fronteira (movimento que o módulo não
    executa); Nettleton & Salas 2016 como direção futura **sem afirmar
    execução**; posicionamento (instrumento de validação empírica, sem
    mecanismo novo).
  - **Referências iniciadas:** subconjunto de **7** das 14 refs do Apêndice B
    do relatório (Backstrom; He; Liu & Terzi; Narayanan & Shmatikov;
    Nettleton & Salas; Sweeney; Zhou & Pei).
  - Terminologia de aferição respeitada; nenhum codinome interno
    (`B1`/`W-NN`/`D-xx`) no corpo do artigo — rastreabilidade vive nas notas
    de cobertura.
- **Achado de registro (corrigido no esqueleto):** a #175 e o esqueleto W2a
  grafavam "Narayanan & Shmatikov (**2009**)"; a referência consolidada em
  `main` (README §12 / Apêndice B do relatório) é o artigo de **2008**
  (S&P, Netflix). Usado 2008 — nenhuma referência nova introduzida
  (regra "não introduzir referências ausentes em `main`").
- **Artefatos públicos (versionados no PR):** matriz
  ([`artigo_rastreabilidade.md`](artigo_rastreabilidade.md)) com W2b ✅;
  este registro; `progress.md` atualizado.
- **Verificação:** só docs — código congelado (S10-W) respeitado.
- **Próxima etapa:** W2c (Seção 3 — método condensado), após merge do PR
  desta etapa (bloqueio a verificar via `gh`).

### Decisão A+B sobre o achado "2009 × 2008" — 2026-06-10 (follow-up da W2b; não é etapa de redação)

- **Contexto:** a discussão aberta na #175 (comentário de 2026-06-10) expôs
  que Narayanan & Shmatikov têm **dois papers distintos** — 2008 (*Robust
  de-anonymization of large sparse datasets*, S&P 2008, Netflix; consolidado
  em `main`) e 2009 (*De-anonymizing social networks*, S&P 2009, DOI
  `10.1109/SP.2009.22`; ausente de `main`, tematicamente mais próximo do
  artigo). **Decisão do autor: A+B** — manter o 2008 nos papéis que já
  cumpre e **adicionar** o 2009 como referência complementar.
- **Retificação de registro (corrige o registro W2b acima, sem
  sobrescrevê-lo):** o corpo da issue #175 **não traz ano** para Narayanan &
  Shmatikov ("He et al. 2009; Nettleton & Salas; Narayanan & Shmatikov;
  Backstrom") — verificado via `gh issue view 175`. O "2009" foi introduzido
  **apenas no esqueleto W2a** (`academic/artigo.md`), não na issue; a opção
  A, portanto, **não exigiu** `gh issue edit`.
- **Execução da opção B (só docs):**
  - `README.md` §12: nova referência **[9]** (Narayanan & Shmatikov 2009),
    lista renumerada [9]→[15] (15 entradas; numeração não é citada por
    outros docs — verificado por grep); citação inline no corpo (§8,
    validade de construção) preservando a regra C2 (lista de referências
    citadas honesta).
  - `references/`: PDF `Narayanan_2009_DeanonymizingSocialNetworks.pdf`
    baixado do arXiv (preprint `0903.3276`), magic bytes `%PDF` verificados;
    catálogo `references/README.md` atualizado (**15/15 baixadas**).
  - **Artigo (privado):** §2 ¶3 cita o 2009 como extensão do movimento
    ofensivo ao domínio de redes sociais (fronteira mantida: depende de
    informação auxiliar externa, nunca usada aqui); referências do artigo
    com 8 entradas; nota de cobertura atualizada.
  - **Relatório (privado):** **adendo** marcado ao Apêndice B ([15], com
    nota "pós-fechamento, não é reabertura") — a #174 permanece fechada; o
    corpo do relatório não cita o 2009.
- **Sem descongelamento:** nenhuma alteração em `src/` ou testes — o
  congelamento da S10-W cobre código; documentação é o modo ativo da fase.
- **Branch:** `docs/references-narayanan-2009` (empilhada sobre
  `docs/artigo-w2b-intro-relacionados`, `Refs #175`), PR **#192**.
- **Incidente de roteamento do #192 (adendo, 2026-06-10):** o #192 foi
  mergeado às 20:38:36Z **na base original** (a branch da W2b), **depois**
  do merge do #191 em `main` (20:30:22Z); como a branch da W2b não foi
  apagada antes, o GitHub não retargetou a base e o conteúdo **não chegou a
  `main`**. Corrigido por **cherry-pick** do commit `2c9cdeb` em branch
  nova a partir de `main` (`docs/references-narayanan-2009-main`, novo PR;
  conteúdo idêntico ao do #192).
