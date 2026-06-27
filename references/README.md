# Referências Bibliográficas — Módulo de Reidentificação

Esta pasta centraliza os PDFs e documentos da bibliografia **citada** do
módulo — as referências da §12 do [`README.md`](../README.md) raiz mais as do
método, efetivamente citadas no artigo e/ou no relatório técnico.

> **Fronteira com [`publications/`](../publications/README.md):** aqui ficam as
> obras **citadas** (espinha de citação, fecha citação↔lista). Leitura mais
> ampla, de contexto/horizonte da tese e **não citada** como referência direta,
> vai para `publications/`. Critério: *foi citado → `references/`; é leitura/
> horizonte → `publications/`*. Uma obra ainda **pendente** de decisão de
> citação pode existir como stub aqui (`_*_pendente.local.md`) enquanto o PDF
> repousa em `publications/` — não é duplicação, é a obra atravessando a
> fronteira.

> ⚠️ **Aviso de copyright:** os arquivos aqui armazenados podem ser privados ou
> protegidos por direitos autorais. Seu uso é restrito a leitura acadêmica
> individual e não comercial. **Não redistribuir.** Por isso o conteúdo desta
> pasta é ignorado pelo Git (ver `.gitignore`); apenas este catálogo e o
> `.gitkeep` são versionados.

## Como obter os arquivos

1. Acesse a referência pelo **DOI** ou link oficial listado no catálogo abaixo.
2. Prefira a versão de **acesso aberto** (repositório institucional / manuscrito
   aceito) quando disponível, em vez da versão do editor.
3. Se houver paywall, utilize acesso institucional (proxy da universidade /
   federação CAFe / VPN) ou solicite a cópia ao autor.
4. Salve o PDF nesta pasta usando a convenção de nomes abaixo.

## Convenção de nomes

```
AutorPrincipal_Ano_PalavraChaveDoTitulo.pdf
```

Três campos separados por `_`:

| Campo | Regra |
|---|---|
| `AutorPrincipal` | Sobrenome do **primeiro** autor, sem acento, capitalizado. Apenas o sobrenome (`Yuan`, `Liu`, `Wang`) — nunca iniciais nem coautores. |
| `Ano` | Ano de publicação com 4 dígitos (`2023`). Para preprint, o ano da versão usada. |
| `PalavraChaveDoTitulo` | 3–6 palavras significativas do título em **CamelCase**, sem espaços, sem acentos, sem artigos/preposições soltos. Acrônimo do método pode liderar (`PGB...`, `PrivGraph...`). |

Sem espaços, hífens ou caracteres especiais no nome. Extensão `.pdf` minúscula.

**Exemplos válidos (acervo atual):**

```
He_2009_PrivacyPreservingStructureAware.pdf
Nettleton_2016_DataDrivenAnonymizationOSN.pdf
Yuan_2023_PrivGraphDifferentiallyPrivateGraphPublication.pdf
Wang_2023_AnchorLinkPredictionDeanonymization.pdf
Liu_2025_PGBBenchmarkingDPSyntheticGraphGeneration.pdf
```

**Não fazer:**

```
3637528.3672013.pdf                         ← DOI/ID do editor, não descreve nada
Anchor_Link_Prediction_for_Privacy...pdf    ← título cru, com espaços/artigos
yuan2023.pdf                                 ← sem título; minúsculo
Yuan_Q_2023_PrivGraph.pdf                    ← não inserir iniciais no campo de autor
```

### Desambiguação de homônimos

Sobrenomes repetem. O acervo já tem casos:

- `Liu_2008_...` (Liu, K.) **vs** `Liu_2025_...` (Liu, S.) — anos distintos, sem conflito.
- `Yuan_2023_...` (Yuan, **Q**uan — PrivGraph) **vs** `Yuan_2024_...` (Yuan, **H**anyang — KDD) — autores **diferentes**.

Regra:

1. No **nome do arquivo**, o ano normalmente já desambigua. Se dois homônimos
   publicarem no **mesmo ano**, acrescente a inicial ao campo de título como
   último recurso (`Yuan_2024_H_UnveilingPrivacy...`), nunca ao campo de autor.
2. Na **citação / BibTeX é obrigatório desambiguar** quando "Sobrenome et al.
   Ano" puder confundir dois trabalhos: use iniciais (`Yuan, H. 2024` vs
   `Yuan, Q. 2023`) e chaves BibTeX distintas (`Yuan2023PrivGraph`,
   `Yuan2024Unveiling`).

### Checklist de inserção

1. **Identificar metadados** na 1ª página do PDF (primeiro autor, ano, título,
   venue, DOI). Para extrair texto sem rasterizar: `pdftotext -f 1 -l 1 arquivo.pdf -`.
2. **Renomear** conforme a convenção acima.
3. **Confirmar que está gitignored** — PDFs nunca são commitados:
   `git check-ignore references/Novo_Arquivo.pdf` deve ecoar o caminho.
4. **Catalogar** na tabela abaixo (arquivo, referência completa, DOI/link,
   estado de acesso) e, se for citado no artigo, adicionar o bloco **BibTeX**.
5. **Versionar apenas texto** (este `README.md` e o `.gitkeep`); conferir com
   `git status` que nenhum `.pdf` aparece rastreado.
6. **Preferir acesso aberto** (arXiv, repositório institucional, cópia de autor)
   à versão do editor — ver §[Orientações](#orientações-e-condições-para-localização-e-download).

### Entradas pendentes

Referência levantada mas ainda **não** incorporada à §12 do `README.md` raiz
fica em arquivo local gitignored com sufixo `.local.md`
(ex.: `_dejong_2024_pendente.local.md`), preservando os metadados até a
deliberação. Não citar no artigo antes da decisão.

## Catálogo

Cobre as 21 referências da seção 12 do [`README.md`](../README.md) raiz.
Estado do download em 2026-06-10: **15/15 baixadas** — 12 de fontes de acesso
aberto legítimas (arXiv, páginas de autor, repositórios institucionais, JMLR)
e 3 obtidas manualmente pelo autor (He 2009 e Cordella 2004 via acesso
institucional ao IEEE Xplore; Nettleton 2016 = manuscrito aceito da O2/UOC,
baixado em navegador). A 15ª (Narayanan & Shmatikov 2009) foi adicionada em
2026-06-10 por decisão do autor na issue #175 (discussão W2b — paper distinto
do Narayanan & Shmatikov 2008, complementar a ele).

**Atualização 2026-06-26 (issues #216/#217, defesa conceitual contra DP):**
duas referências de Privacidade Diferencial em grafos formalmente
incorporadas à §12 do README e citadas no artigo — Mendonça et al. (2023,
survey de DP em grafos) e Brito & Machado (2024, *graph release* sob DP),
ambas SBC/SOL de acesso aberto, **17/17 baixadas**. Material de apoio
adicional (não citado / não incorporado) permanece em catálogo local
gitignored (`DP_GRAPH_REFERENCES.md`), pendente de deliberação com os
orientadores.

**Atualização 2026-06-26 (issue #218, atualização bibliográfica > 2020):**
três referências recentes (> 2020, sendo uma de 2024) incorporadas à §12 do
README e citadas no artigo, uma por subárea — Hao et al. (2024, anonimização
estrutural k-degree), Yuan et al. (2023, publicação de grafo sob DP) e
Mueller et al. (2022, taxonomia de DP em grafos). Por decisão da issue, ao
**versionamento** vão **apenas BibTeX e links** — **nenhum PDF é commitado**
(direitos autorais). Os PDFs foram obtidos **localmente pelo autor**
(gitignored, não commitados), como o restante do acervo. BibTeX das três em
[`#bibtex-218`](#bibtex-recentes-218). Total da §12: **20** entradas.

**Atualização 2026-06-27 (rodada D7, adversário aprendido ML/GNN):** uma
referência de de-anonimização baseada em aprendizado de máquina incorporada à
§12 do README e citada no artigo (§2, após Narayanan) e no relatório (§1.3) —
Wang et al. (2023, *anchor link prediction* via *graph embedding* + aprendizado
adversarial federado, IEEE TDSC). Entra como **[18]** na §12 (renumerando
Wörlein→[19], Yuan→[20], Zhou→[21]); total da §12: **21** entradas. Como nas
rodadas anteriores, ao versionamento vão **apenas BibTeX e link** — o PDF foi
obtido **localmente pelo autor** (gitignored, não commitado). BibTeX em
[`#bibtex-d7`](#bibtex-d7-adversario-aprendido). Sem issue vinculada.

| Arquivo | Referência | DOI / Link | Acesso |
|---|---|---|---|
| `Backstrom_2007_WhereforeArtThouR3579X.pdf` | Backstrom, L.; Dwork, C.; Kleinberg, J. *Wherefore art thou R3579X? Anonymized social networks, hidden patterns, and structural steganography.* WWW 2007. | https://doi.org/10.1145/1242572.1242598 — cópia de autor: https://www.cs.cornell.edu/home/kleinber/www07-anon.pdf | ✅ baixado (cópia de autor, Cornell) |
| `Brito_2024_DifferentiallyPrivateReleaseCountWeightedGraphs.pdf` | Brito, F. T.; Machado, J. C. *Differentially Private Release of Count-Weighted Graphs.* SBBD 2024 (Companion), p. 183–189. | https://sol.sbc.org.br/index.php/sbbd_estendido/article/view/30791 | ✅ baixado (SOL/SBC, acesso aberto) |
| `Cordella_2004_SubgraphIsomorphismVF2.pdf` | Cordella, L.P.; Foggia, P.; Sansone, C.; Vento, M. *A (sub)graph isomorphism algorithm for matching large graphs.* IEEE TPAMI 26(10), 2004. | https://doi.org/10.1109/TPAMI.2004.75 | ✅ baixado manualmente (IEEE Xplore, VoR, acesso institucional) |
| `Diaz_2003_TowardsMeasuringAnonymity.pdf` | Díaz, C.; Seys, S.; Claessens, J.; Preneel, B. *Towards measuring anonymity.* PET 2002, LNCS 2482. | https://doi.org/10.1007/3-540-36467-6_5 — cópia: https://www.freehaven.net/anonbib/cache/Diaz02.pdf | ✅ baixado (anonbib/freehaven, pré-print) |
| `Hao_2024_MLDAMultiLevelKDegreeAnonymity.pdf` | Hao, Y.; Li, L.; Chang, L.; Gu, T. *MLDA: a multi-level k-degree anonymity scheme on directed social network graphs.* Frontiers of Computer Science, 18(2):182814, 2024. | https://doi.org/10.1007/s11704-023-2759-8 | ✅ baixado (local pelo autor, gitignored — #218) |
| `He_2009_PrivacyPreservingStructureAware.pdf` | He, X.; Vaidya, J.; Shafiq, B.; Adam, N.; Atluri, V. *Preserving Privacy in Social Networks: A Structure-Aware Approach.* WI-IAT 2009. | https://doi.org/10.1109/WI-IAT.2009.108 | ✅ baixado manualmente (IEEE Xplore, VoR, acesso institucional) |
| `Karypis_1998_MultilevelGraphPartitioning.pdf` | Karypis, G.; Kumar, V. *A fast and high quality multilevel scheme for partitioning irregular graphs.* SIAM J. Sci. Comput. 20(1), 1998. | https://doi.org/10.1137/S1064827595287997 — cópia: https://www.cs.utexas.edu/~pingali/CS395T/2009fa/papers/metis.pdf | ✅ baixado (espelho de curso, UT Austin) |
| `Leskovec_2012_SocialCirclesEgoNetworks.pdf` | Leskovec, J.; McAuley, J.J. *Learning to discover social circles in ego networks.* NIPS 2012. | https://dl.acm.org/doi/10.5555/2999134.2999195 — cópia de autor: https://cs.stanford.edu/people/jure/pubs/circles-nips12.pdf | ✅ baixado (cópia de autor, Stanford) |
| `Liu_2008_IdentityAnonymizationGraphs.pdf` | Liu, K.; Terzi, E. *Towards identity anonymization on graphs.* SIGMOD 2008. | https://doi.org/10.1145/1376616.1376629 — cópia de autora: https://cs-people.bu.edu/evimaria/cs591/sigmod_privacy_graph.pdf | ✅ baixado (cópia de autora, BU) |
| `Mendonca_2023_PrivacyPreservingTechniquesSocialNetworkAnalysis.pdf` | Mendonça, A. L. C.; Brito, F. T.; Machado, J. C. *Privacy-Preserving Techniques for Social Network Analysis.* SBBD 2023 (Estendido), p. 174–178. | https://sol.sbc.org.br/index.php/sbbd_estendido/article/view/25632 | ✅ baixado (SOL/SBC, acesso aberto) |
| `Mueller_2022_SoKDifferentialPrivacyGraphStructuredData.pdf` | Mueller, T. T.; Usynin, D.; Paetzold, J. C.; Rueckert, D.; Kaissis, G. *SoK: Differential Privacy on Graph-Structured Data.* arXiv:2203.09205, 2022. | https://arxiv.org/abs/2203.09205 | ✅ baixado (local pelo autor, gitignored — #218) |
| `Narayanan_2008_RobustDeanonymization.pdf` | Narayanan, A.; Shmatikov, V. *Robust de-anonymization of large sparse datasets.* IEEE S&P 2008. | https://doi.org/10.1109/SP.2008.33 — preprint: https://arxiv.org/abs/cs/0610105 | ✅ baixado (arXiv, preprint) |
| `Narayanan_2009_DeanonymizingSocialNetworks.pdf` | Narayanan, A.; Shmatikov, V. *De-anonymizing social networks.* IEEE S&P 2009, p. 173–187. | https://doi.org/10.1109/SP.2009.22 — preprint: https://arxiv.org/abs/0903.3276 | ✅ baixado (arXiv, preprint) |
| `Nettleton_2016_DataDrivenAnonymizationOSN.pdf` | Nettleton, D.F.; Salas, J. *A data driven anonymization system for information rich online social network graphs.* Expert Systems with Applications, 55, 87–105, 2016. | https://doi.org/10.1016/j.eswa.2016.02.004 — manuscrito aceito (AAM): http://hdl.handle.net/10609/150625 (CC BY-NC-ND) | ✅ baixado manualmente (AAM, O2/UOC, via navegador) |
| `Serjantov_2003_InformationTheoreticMetricAnonymity.pdf` | Serjantov, A.; Danezis, G. *Towards an information theoretic metric for anonymity.* PET 2002, LNCS 2482. | https://doi.org/10.1007/3-540-36467-6_4 — cópia de autor: http://www0.cs.ucl.ac.uk/staff/g.danezis/papers/set.pdf | ✅ baixado (cópia de autor, UCL) |
| `Shervashidze_2011_WeisfeilerLehmanGraphKernels.pdf` | Shervashidze, N. et al. *Weisfeiler-Lehman graph kernels.* JMLR 12, 2539–2561, 2011. | https://www.jmlr.org/papers/v12/shervashidze11a.html | ✅ baixado (JMLR, VoR aberto) |
| `Sweeney_2002_KAnonymity.pdf` | Sweeney, L. *k-anonymity: A model for protecting privacy.* IJUFKS 10(5), 557–570, 2002. | https://doi.org/10.1142/S0218488502001648 — cópia de autora: https://dataprivacylab.org/dataprivacy/projects/kanonymity/kanonymity.pdf | ✅ baixado (cópia de autora, Data Privacy Lab) |
| `Wang_2023_AnchorLinkPredictionDeanonymization.pdf` | Wang, H.; Yang, W.; Man, D.; Wang, W.; Lv, J. *Anchor Link Prediction for Privacy Leakage via De-Anonymization in Multiple Social Networks.* IEEE Transactions on Dependable and Secure Computing, 20(6):5197–5213, 2023. | https://doi.org/10.1109/TDSC.2023.3242009 | ✅ baixado (local pelo autor, gitignored — D7) |
| `Worlein_2005_SubgraphMinersComparison.pdf` | Wörlein, M. et al. *A quantitative comparison of the subgraph miners MoFa, gSpan, FFSM, and Gaston.* PKDD 2005, LNCS 3721, 392–403. | https://doi.org/10.1007/11564126_39 | ✅ baixado (Springer, VoR de acesso aberto) |
| `Yuan_2023_PrivGraphDifferentiallyPrivateGraphPublication.pdf` | Yuan, Q.; Zhang, Z.; Du, L.; Chen, M.; Cheng, P.; Sun, M. *PrivGraph: Differentially Private Graph Data Publication by Exploiting Community Information.* USENIX Security 2023, p. 3241–3258. | https://www.usenix.org/conference/usenixsecurity23/presentation/yuan-quan | ✅ baixado (local pelo autor, gitignored — #218) |
| `Zhou_2008_NeighborhoodAttacks.pdf` | Zhou, B.; Pei, J. *Preserving privacy in social networks against neighborhood attacks.* ICDE 2008. | https://doi.org/10.1109/ICDE.2008.4497459 — cópia de autor: https://www.cs.sfu.ca/~jpei/publications/NeighborhoodAnonymization-ICDE08.pdf | ✅ baixado (cópia de autor, SFU) |

> **Nota de DOI (Wörlein 2005):** o DOI correto é `10.1007/11564126_39`,
> confirmado via Crossref. O `README.md` raiz listava `10.1007/11564126_32`,
> que resolve para outro capítulo do mesmo volume LNCS ("Weka4WS") — corrigido
> junto com esta atualização de catálogo.

## Orientações e condições para localização e download

1. **DOI primeiro.** Sempre que houver DOI, use-o como ponto de partida — ele
   resolve para a página oficial do artigo.
2. **Prefira acesso aberto.** Para Nettleton & Salas (2016), o manuscrito aceito
   está no repositório O2 da UOC (`hdl.handle.net/10609/150625`) sob licença
   CC BY-NC-ND — download e uso permitidos com atribuição, sem alteração e sem
   fins comerciais.
3. **Paywall.** Quando o artigo só estiver disponível no site do editor
   (ex.: Elsevier/ScienceDirect), use o **acesso institucional** (proxy da
   universidade, federação CAFe ou VPN). Não armazene credenciais no repositório.
4. **Versão correta.** Registre no catálogo se o PDF é a versão do editor
   (Version of Record), o manuscrito aceito (AAM) ou um preprint, pois isso
   afeta citação e legalidade da cópia.
5. **Não comitar.** Após salvar os PDFs, confirme com `git status` que nenhum
   aparece como rastreado. Se aparecer, revise o `.gitignore`.

## BibTeX — referências recentes (#218, > 2020) {#bibtex-recentes-218}

Referências incorporadas pela issue **#218** (atualização bibliográfica
> 2020). Ao **versionamento** vão **apenas BibTeX e links** — **nenhum PDF é
commitado** (direitos autorais). Os PDFs já foram obtidos **localmente pelo
autor** e salvos em `references/` (gitignored), como o restante do acervo.

```bibtex
@article{Hao2024MLDA,
  author  = {Hao, Yuanjing and Li, Long and Chang, Liang and Gu, Tianlong},
  title   = {{MLDA}: a multi-level k-degree anonymity scheme on directed
             social network graphs},
  journal = {Frontiers of Computer Science},
  volume  = {18},
  number  = {2},
  pages   = {182814},
  year    = {2024},
  doi     = {10.1007/s11704-023-2759-8},
  url     = {https://doi.org/10.1007/s11704-023-2759-8}
}

@inproceedings{Yuan2023PrivGraph,
  author    = {Yuan, Quan and Zhang, Zhikun and Du, Linkang and Chen, Min
               and Cheng, Peng and Sun, Mingyang},
  title     = {{PrivGraph}: Differentially Private Graph Data Publication by
               Exploiting Community Information},
  booktitle = {Proceedings of the 32nd USENIX Security Symposium
               (USENIX Security 23)},
  pages     = {3241--3258},
  year      = {2023},
  publisher = {USENIX Association},
  url       = {https://www.usenix.org/conference/usenixsecurity23/presentation/yuan-quan}
}

@misc{Mueller2022SoKDPGraphs,
  author        = {Mueller, Tamara T. and Usynin, Dmitrii and
                   Paetzold, Johannes C. and Rueckert, Daniel and
                   Kaissis, Georgios},
  title         = {{SoK}: Differential Privacy on Graph-Structured Data},
  year          = {2022},
  eprint        = {2203.09205},
  archivePrefix = {arXiv},
  primaryClass  = {cs.CR},
  url           = {https://arxiv.org/abs/2203.09205}
}
```

## BibTeX — adversário aprendido (D7) {#bibtex-d7-adversario-aprendido}

Referência incorporada pela **rodada D7** (2026-06-27, adversário aprendido
ML/GNN; sem issue vinculada). De-anonimização baseada em aprendizado de
máquina, citada no artigo (§2) e no relatório (§1.3) como adversário mais
forte que os cenários estruturais básicos — leitura de cota inferior. Ao
versionamento vão **apenas BibTeX e link**; o PDF é local do autor
(gitignored). Desambiguação: **Wang, H.** (2023) é distinto de outros autores
homônimos; chave BibTeX própria `Wang2023AnchorLink`.

```bibtex
@article{Wang2023AnchorLink,
  author  = {Wang, Huanran and Yang, Wu and Man, Dapeng and
             Wang, Wei and Lv, Jiguang},
  title   = {Anchor Link Prediction for Privacy Leakage via
             De-Anonymization in Multiple Social Networks},
  journal = {IEEE Transactions on Dependable and Secure Computing},
  volume  = {20},
  number  = {6},
  pages   = {5197--5213},
  year    = {2023},
  doi     = {10.1109/TDSC.2023.3242009},
  url     = {https://doi.org/10.1109/TDSC.2023.3242009}
}
```
