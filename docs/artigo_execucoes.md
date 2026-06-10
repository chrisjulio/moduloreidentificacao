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

**Etapas executadas: 6 de 6 — desdobramento S10-W2a..f concluído.**

| Etapa | Escopo | Data | Branch | PR | Status |
|---|---|---|---|---|---|
| W2a | Esqueleto em `academic/artigo.md` + matriz + este registro | 2026-06-10 | `docs/artigo-skeleton-w2a` | [#188](https://github.com/chrisjulio/moduloreidentificacao/pull/188) | ✅ MERGED (2026-06-10) |
| W2b | Seções 1–2: introdução + trabalhos relacionados | 2026-06-10 | `docs/artigo-w2b-intro-relacionados` | [#191](https://github.com/chrisjulio/moduloreidentificacao/pull/191) | ✅ MERGED (2026-06-10; complemento A+B reencaminhado via [#193](https://github.com/chrisjulio/moduloreidentificacao/pull/193), MERGED) |
| W2c | Seção 3: método condensado | 2026-06-10 | `docs/artigo-w2c-metodo` | [#194](https://github.com/chrisjulio/moduloreidentificacao/pull/194) | ✅ MERGED (2026-06-10) |
| W2d | Seção 4: resultados (a mais pesada — sessão própria) | 2026-06-10 | `docs/artigo-w2d-resultados` | [#195](https://github.com/chrisjulio/moduloreidentificacao/pull/195) | ✅ MERGED (2026-06-10) |
| W2e | Seções 5–6: discussão + conclusão + abstract final | 2026-06-10 | `docs/artigo-w2e-discussao-conclusao` | [#196](https://github.com/chrisjulio/moduloreidentificacao/pull/196) | ✅ MERGED (2026-06-10) |
| W2f | Revisão integrada + fechamento da DoD da #175 | 2026-06-10 | `docs/artigo-w2f-revisao-integrada` | — | ✅ executada (PR aberto — **fecha a #175**) |

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
  conteúdo idêntico ao do #192). *Desfecho:* PR **#193** `MERGED` em
  2026-06-10 (`20:45:22Z`) — conteúdo da decisão A+B em `main`.

### W2c — 2026-06-10 — Seção 3 (método condensado)

- **Pré-verificação de bloqueios:** PR **#193** (reencaminhamento da decisão
  A+B) confirmado `MERGED` via `gh pr view 193` (`mergedAt:
  2026-06-10T20:45:22Z`); nenhum PR aberto. Sem dúvidas em aberto na #175
  para esta etapa (3 pontos do desdobramento decididos; achado 2008×2009
  resolvido e mergeado) — pré-condições da W2c satisfeitas.
- **Texto privado (gitignorado, fora do diff):** Seção 3 redigida em
  `academic/artigo.md`, substituindo o checklist do esqueleto (preservado
  como "Cobertura do checklist (W2c)" para a revisão W2f). Compressão de
  §3–§4 do relatório em 5 subseções:
  - **§3.1 Pipeline de aferição** (1 parágrafo + Figura 1): etapas
    `anonimização → ataque → métrica` parametrizadas por YAML; produto =
    logs JSONL; figura Mermaid **condensada** (derivada de `pipeline.md`
    §1–§2) com nota de conversão pandoc.
  - **§3.2 Anonimização** (2 parágrafos + Tabela 1): 5 fases de He et al.
    (2009) em 1 parágrafo; backends METIS/Kernighan-Lin gravados no log;
    tabela dos 5 parâmetros uniformes entre datasets com auditabilidade
    *a posteriori* nos logs (compressão de §3.3 do relatório).
  - **§3.3 Cenários formais de reidentificação** (2 parágrafos): grau
    (linha de base) e subgrafo 1-hop; VF2 no Facebook × WL-bucketing no
    Enron, com a equivalência semântica em **1 parágrafo** (invariante
    necessário/viés conservador; 100% em grafos pequenos; 70 nós/0
    divergências no Enron; ~36 s vs ~70 dias). O gate de timeout do Enron
    (§3.5 do relatório) foi **comprimido na equivalência exata** — sem
    parágrafo próprio no artigo.
  - **§3.4 Métricas e validação** (2 parágrafos): 4 métricas em 1
    parágrafo; verificador independente de k-anonimato com critério
    substantivo em 3 frases.
  - **§3.5 Datasets e desenho experimental** (4 parágrafos): frase canônica
    da assimetria de papéis (tendências, não magnitudes); Facebook ego 3437
    (exclusão do ego, LCC, piso 10×k_max; n=532/m=4.812); Enron
    (simetrização OR conservadora; LCC n=33.696/m=180.811); grade 12
    runs/dataset (3 sementes do YAML); d-sweep 48 runs como exercício da
    propriedade estrutural; reprodutibilidade em 1 parágrafo (sementes do
    YAML; outputs de logs; CI) — **sem** citar `verify_reproduction` como
    script entregue (cuidado anotado na W1f respeitado).
  - **Referências:** +4 do método (Cordella 2004; Shervashidze 2011;
    Karypis & Kumar 1998; Leskovec & McAuley 2012) — todas já em `main`
    (README §12); lista do artigo com **12 entradas**. Terminologia de
    aferição respeitada; nenhum codinome interno no corpo do artigo.
- **Artefatos públicos (versionados no PR):** matriz
  ([`artigo_rastreabilidade.md`](artigo_rastreabilidade.md)) com W2c ✅ (e
  W2b atualizada para MERGED); este registro (3/6); `progress.md`
  atualizado.
- **Verificação:** só docs — código congelado (S10-W) respeitado.
- **Próxima etapa:** W2d (Seção 4 — resultados; a mais pesada, sessão
  própria), após merge do PR desta etapa (bloqueio a verificar via `gh`).

### W2d — 2026-06-10 — Seção 4 (resultados)

- **Pré-verificação de bloqueios:** PR **#194** (W2c) confirmado `MERGED`
  via `gh pr view 194` (`mergedAt: 2026-06-10T21:06:57Z`); nenhum PR
  aberto. Sem dúvidas em aberto na #175 para esta etapa — pré-condições da
  W2d satisfeitas. Etapa executada em **sessão própria**, conforme o
  desdobramento validado (a mais pesada, como a W1d do relatório).
- **Texto privado (gitignorado, fora do diff):** Seção 4 redigida em
  `academic/artigo.md`, substituindo o checklist do esqueleto (preservado
  como "Cobertura do checklist (W2d)" para a revisão W2f). Compressão de
  §5.1–§5.7 do relatório em 6 subseções:
  - **§4.1 Facebook** (k-anonimato atingido): critério substantivo do
    verificador independente descrito sem codinome; **Tabela 2** (agregados
    por k, de `results_baseline.md`); leitura da curva (rr_subgrafo
    0,79→0,00 monotônico; KS-D 0,00→0,65; rr_grau sobe a 0,0990 em k=20);
    **Figura 2** (curva privacidade-utilidade FB, regenerável — nota de
    conversão); nota do motor (Kernighan-Lin no baseline, inócuo em d=1;
    backend gravado no log; implicação residual encaminhada à Seção 5).
  - **§4.2 Achado central:** d=1 ≡ k-anonimato de grau; 0,7914 vs 0,0263
    em k=2 — o grafo satisfaz a definição formal e ~4/5 das vizinhanças
    permanecem únicas.
  - **§4.3 Enron:** **Tabela 3** (agregados por k, de `results_enron.md`);
    rr_subgrafo 0,1241→0,0569 monotônico; rr_grau residual (≤0,0033, ~40×
    menor); utilidade melhor preservada em escala; divergência em k=20
    (colapso a zero no FB vs ~0,057 no Enron = escala, não mecanismo);
    **Figura 3** (curva Enron, regenerável); nota da cota 1/k (pressupõe
    d≥2; violação em k=20 esperada, não anomalia).
  - **§4.4 Resultado generalizável:** critério pré-fixado (gap nos dois
    datasets) satisfeito; **Tabela 4** (gap k=2: FB ~30×; Enron ~38×);
    sinal qualitativo robusto, magnitudes não comparáveis.
  - **§4.5 Painel normalizado:** justificativa de não sobrepor magnitudes
    brutas (3 confundidores: escala; densidade/origem OR; motor
    não-pareado); **Figura 4** = snapshot versionado
    `docs/assets/comparison_fb_enron.png`; painéis (A) fração da cota 1/k
    (FB acima em k∈{2,5,10}, pico ~2,03; Enron cruza só em k=20 ~1,14;
    cruzamento ~k≈14) e (B) decaimento relativo (FB 1,0→0,18→0,0; Enron
    1,0→0,63→0,46); alternativa de eixo log rejeitada (falha no zero).
  - **§4.6 d-sweep como suporte** (1 parágrafo): tendências opostas dos
    dois cenários em k (deslocamento do vetor de ataque de subgrafo para
    grau); EGS ≈ k·d (19,70; 133,0); degenerados documentados (d=2;
    d=10/k=20 cobertura 0,752) e zeros genuínos (sem timeout nas 48
    execuções) — sem codinomes; + **2 frases** sobre a entropia como
    métrica complementar (mapa de compressão), sem reportar valores
    inexistentes.
  - **Referências:** nenhuma nova exigida (lista permanece com 12
    entradas). Terminologia de aferição respeitada; nenhum codinome
    interno no corpo do artigo. Todo número conferido contra
    `results_baseline.md`/`results_enron.md`/`results_dsweep.md` em `main`.
- **Artefatos públicos (versionados no PR):** matriz
  ([`artigo_rastreabilidade.md`](artigo_rastreabilidade.md)) com W2d ✅ (e
  W2c atualizada para MERGED, PR #194); este registro (4/6); `progress.md`
  atualizado.
- **Verificação:** só docs — código congelado (S10-W) respeitado.
- **Próxima etapa:** W2e (Seções 5–6 — discussão + conclusão + abstract
  final), após merge do PR desta etapa (bloqueio a verificar via `gh`).

### W2e — 2026-06-10 — Seções 5–6 (discussão + conclusão) + abstract final

- **Pré-verificação de bloqueios:** PR **#195** (W2d) confirmado `MERGED`
  via `gh pr view 195` (`mergedAt: 2026-06-10T21:19:59Z`); nenhum PR
  aberto. Sem dúvidas em aberto na #175 para esta etapa — pré-condições da
  W2e satisfeitas. Última etapa de **redação substantiva**; resta a revisão
  integrada W2f.
- **Texto privado (gitignorado, fora do diff):** Seções 5–6 redigidas em
  `academic/artigo.md`, substituindo os checklists do esqueleto
  (preservados como "Cobertura do checklist (W2e)" para a revisão W2f);
  **abstract final** reescrito no lugar do provisório da W2b, conforme
  previsto no esqueleto:
  - **Resumo (final):** mantém a tese central e os números k=2 dos dois
    datasets (Facebook 0,7914 vs 0,0263 ~30×; Enron 0,1241 vs 0,0033
    ~38×); acrescenta, à luz das Seções 4–5: os dois cenários adversariais
    explícitos; o deslocamento do vetor de ataque (k alto distorce graus e
    fortalece o cenário por grau); e a leitura de **cota inferior** das
    taxas. Nota de redação registra as diferenças em relação ao provisório.
  - **Seção 5 — Discussão** (4 subseções): §5.1 validade externa — as
    tendências sobrevivem no Enron (rede ~63× maior, origem distinta), gap
    parcialmente fechado; resíduos explícitos (`multiple_egonets` não
    executado — generalização dentro da família de ego-redes não
    demonstrada; d-sweep restrito à ego-rede principal) + limitações
    selecionadas do relatório §6 (algoritmo único — sem afirmações
    comparativas; motor não-pareado KL×METIS, argumento de inocuidade em
    d=1 sólido porém **interpretativo**, baixa magnitude, pareamento
    estrito como verificação futura); §5.2 taxas como **cota inferior**
    (cenários deliberadamente básicos; leitura agrava o achado, não
    atenua; entropia = métrica complementar, não cenário adversarial);
    §5.3 resultado negativo como contribuição defensiva (descompasso entre
    garantia formal declarada e superfície estrutural protegida — é isso
    que o aferidor detecta; deslocamento do vetor de ataque na mesma
    leitura; não é defeito da técnica, é o regime d=1); §5.4 ponte para a
    deliberação metodológica da tese — 4 vias citadas, módulo **não
    escolhe**, fornece a régua; independência como valor de auditoria
    (framework citado genericamente, sem nome interno — coerente com a
    nota de confidencialidade de `scope.md` §8).
  - **Seção 6 — Conclusão e trabalhos futuros** (2 parágrafos): síntese
    (aferidor entregue; achado generalizável ~30–38× como evidência da
    premissa fundadora; cota inferior reiterada); futuros derivados dos
    resíduos da Seção 5 — (i) `multiple_egonets`; (ii) d-sweep no Enron +
    pareamento estrito do motor; (iii) entropia promovida de métrica a
    cenário adversarial (**não executado**); (iv) comparação com outras
    técnicas, Nettleton & Salas 2016 **não executada**; (v) extensão
    temporal (fase seguinte do programa de pesquisa). Fecho preserva o
    enquadramento instrumental (aferição reprodutível; não mecanismo novo,
    não ferramenta ofensiva).
  - **Referências:** nenhuma nova exigida (lista fecha a redação
    substantiva com 12 entradas, todas em `main`); consolidação final na
    W2f. Terminologia de aferição respeitada; nenhum codinome interno no
    corpo do artigo.
- **Artefatos públicos (versionados no PR):** matriz
  ([`artigo_rastreabilidade.md`](artigo_rastreabilidade.md)) com W2e ✅ (e
  W2d atualizada para MERGED, PR #195); este registro (5/6); `progress.md`
  atualizado.
- **Verificação:** só docs — código congelado (S10-W) respeitado.
- **Próxima etapa:** W2f (revisão integrada + DoD da #175 — **fecha a
  issue**), após merge do PR desta etapa (bloqueio a verificar via `gh`).

### W2f — 2026-06-10 — Revisão integrada + DoD da #175 (fecha a issue)

- **Pré-verificação de bloqueios:** PR **#196** (W2e) confirmado `MERGED`
  via `gh pr view 196` (`mergedAt: 2026-06-10T22:17:13Z`); nenhum PR
  aberto — pré-condições da W2f satisfeitas. Sessão orientada pelo
  relatório de validação externo do autor (`validacao_w2f_175.md`,
  2026-06-10), que pré-mapeou 5 itens de ação (1.1–1.5) e 11 itens já
  verificados sem divergência.
- **Revisão integrada (texto privado, gitignorado, fora do diff):**
  conferência integral das Seções 1–6 + abstract de `academic/artigo.md`
  contra `main` — registro detalhado na seção "Revisão integrada (W2f)" do
  próprio documento:
  - **Números:** Tabelas 2–4 **exatas** contra `results_baseline.md` /
    `results_enron.md`; painel normalizado (§4.5) e d-sweep (§4.6)
    conferem com `results_enron.md` / `results_dsweep.md`. Nenhuma
    divergência.
  - **Item 1.1 (referências):** as 3 ausências reais (artigo: 12 de 15 do
    README §12) são **Wörlein 2005, Díaz 2003 e Serjantov & Danezis 2003**
    — a tabela do relatório de validação supunha Leskovec/Karypis/
    Shervashidze, mas essas três **estão** no artigo desde a W2c
    (verificado no corpo §3.2/§3.3/§3.5). Omissões registradas como
    **intencionais**: o artigo não discute a escolha do minerador FSM
    (Wörlein) nem reporta valores de entropia / "degree of anonymity"
    (Díaz; Serjantov). Justificativa na Nota de consolidação das
    Referências (privado) + nota pública na matriz.
  - **Item 1.2 (desvio-padrão zero em k=2):** explicação **adicionada à
    §4.1** (1 parágrafo após a Tabela 2), ancorada nos observáveis da
    tabela bruta de `results_baseline.md` (3 sementes com linhas
    idênticas; KS-D e Δclust exatamente nulos) e na redução d=1 → grau.
  - **Item 1.3 (motor não-pareado):** verificado **já visível** ao par
    revisor sem acesso ao relatório — §4.1 (nota KL×METIS + mecanismo de
    inocuidade em d=1), §4.5 (3º confundidor) e §5.1 ¶2 (argumento
    marcado como interpretativo; pareamento estrito como futuro). Sem
    ajuste necessário.
  - **Item 1.4 (assimetria do adendo [15]):** nota pública adicionada à
    matriz ([`artigo_rastreabilidade.md`](artigo_rastreabilidade.md)) —
    artigo cita Narayanan & Shmatikov 2009 no corpo; relatório só no
    adendo pós-fechamento do Apêndice B; diferença intencional (decisão
    A+B), não inconsistência.
  - **Item 1.5 (arredondamento do abstract):** política fixada —
    **inteiro mais próximo** (30,1× → ~30×; 37,6× → ~38×; arredondamento
    padrão, nenhum viés direcional); quocientes exatos anotados na
    legenda da Tabela 4 do artigo, ao lado dos valores brutos que
    permitem recomputá-los. Opções (a)+(c) do relatório de validação.
  - **Terminologia de aferição:** varredura dos termos proibidos — única
    ocorrência ("de-anonimização", §2 ¶3) nomeia a linha da literatura
    que o trabalho **não** executa (título do próprio paper de 2009);
    precedente do relatório. Conforme.
  - **Citação↔lista:** fechada nos dois sentidos (12/12 citadas no corpo;
    nenhuma citação fora da lista; todas em `main`).
  - **Checklists de cobertura W2b..e:** mantidos como rastro de processo,
    a remover na conversão final (pandoc) — mesmo tratamento do relatório.
  - **DoD emendada da #175 conferida item a item — cumprida** (7/7;
    registro no próprio documento).
- **Artefatos públicos (versionados no PR):** matriz
  ([`artigo_rastreabilidade.md`](artigo_rastreabilidade.md)) com W2f ✅ +
  notas de assimetria [15] e de referências; este registro (6/6; W2e →
  MERGED #196); `progress.md` atualizado.
- **Verificação:** só docs — código congelado (S10-W) respeitado.
- **Desfecho:** desdobramento S10-W2a..f **concluído**. O PR desta etapa
  traz `Closes #175`. Pendências fora do escopo da issue: conversão final
  via pandoc (figuras regeneráveis; remoção dos checklists de processo) — a
  cargo do autor, com venue/template a decidir.
