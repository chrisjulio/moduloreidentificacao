# Referências — Privacidade Diferencial em Grafos

Bloco complementar ao catálogo principal (`README.md`). Cobre os 4 artigos
identificados na busca temática de junho/2026, destinados a sustentar o
**posicionamento diferencial entre k-anonimato estrutural e DP em grafos**
(issues #216 e #217) e a **lacuna nacional** no tema.

> ⚠️ **Aviso de copyright:** mesmas condições do catálogo principal. PDFs
> devem ser salvos localmente e **não commitados** (ver `.gitignore`).
> Use a convenção `AutorPrincipal_Ano_PalavraChaveDoTitulo.pdf`.

---

## Contexto de uso no artigo

Estes 4 artigos cobrem os quatro grupos de busca definidos para a #217:

| Grupo | Finalidade no texto | Artigos aqui |
|---|---|---|
| **A** — Survey de DP em grafos | Contextualizar estado da arte, citar edge-DP vs. node-DP | Mendonça et al. 2023 |
| **C** — DP que libera grafo (*ponte*) | Demarcar linha existente, mas em maturação; premissas divergentes | Brito & Machado 2024 |
| **D** — Graph mining + data publishing | Âncora da subárea; evidência de nicho emergente no Brasil | Oliveira et al. 2024 |
| **Lacuna nacional** | Evidência de que KDMILE/ENIAC não cobrem o tema; originalidade | todos os 4 combinados |

---

## Catálogo

### 1. Mendonça et al. (SBBD 2023) — Tutorial: Privacy-Preserving Techniques for Social Network Analysis

| Campo | Valor |
|---|---|
| **Arquivo sugerido** | `Mendonca_2023_PrivacyPreservingTechniquesSocialNetworkAnalysis.pdf` |
| **Autores** | Mendonça, A. L. C.; Brito, F. T.; Machado, J. C. |
| **Título** | *Privacy-Preserving Techniques for Social Network Analysis* |
| **Venue** | Anais Estendidos do XXXVIII SBBD (Simpósio Brasileiro de Bancos de Dados), 2023, p. 174–178 |
| **Instituição** | Grupo LSBD — Universidade Federal do Ceará (UFC) |
| **Link direto (acesso aberto)** | https://sol.sbc.org.br/index.php/sbbd_estendido/article/download/25632/25450 |
| **DOI / página** | https://sol.sbc.org.br/index.php/sbbd_estendido/article/view/25632 |
| **Acesso** | ✅ Acesso aberto (SBC Open Library / SOL) |

**Por que entra no projeto:**
- É o **survey nacional citável** que organiza o espaço de DP em grafos no
  vocabulário canônico: *edge-DP vs. node-DP*, *query release vs. graph release*.
- Distingue explicitamente a garantia **sintática** (k-anonimato) da garantia
  **semântica/probabilística** (DP com parâmetro ε) — sustenta o Eixo 1 da
  tabela comparativa da #217.
- Trata o modelo de adversário de pior caso da DP em contraste com o modelo
  de conhecimento limitado do k-anonimato estrutural — sustenta o Eixo 3.
- Produzido pelo principal polo nacional de DP em grafos (LSBD/UFC); citar
  este trabalho ancora o projeto no estado da arte brasileiro sem exigir entrar
  no mérito técnico dos mecanismos de DP.
- Publicado no SBBD, evento SBC com escopo adjacente ao KDMILE/BRACIS —
  reforça a lacuna ao mostrar que o tema migrou para o SBBD, não para o BRACIS.

**Pontos de conexão com o módulo:**
- A distinção *query release* (DP responde consultas com ruído; grafo bruto não
  é entregue) vs. *graph release* (DP perturba e publica o grafo) mapeia
  diretamente sobre o **Eixo 2 — Objeto protegido/liberado** da tabela da #217.
- O tutorial lista métricas de utilidade estrutural (distribuição de graus,
  clustering coefficient, centralidade) que se sobrepõem ao escopo de métricas
  do módulo (seção 6 do CLAUDE.md) — útil para justificar a escolha das
  mesmas métricas no contexto de avaliação privacidade-utilidade.

---

### 2. Brito & Machado (SBBD 2024) — Differentially Private Release of Count-Weighted Graphs

| Campo | Valor |
|---|---|
| **Arquivo sugerido** | `Brito_2024_DifferentiallyPrivateReleaseCountWeightedGraphs.pdf` |
| **Autores** | Brito, F. T.; Machado, J. C. |
| **Título** | *Differentially Private Release of Count-Weighted Graphs* |
| **Venue** | Companion Proceedings of the 39th Brazilian Symposium on Databases (SBBD 2024), p. 183–189 |
| **Instituição** | Grupo LSBD — Universidade Federal do Ceará (UFC) |
| **Link direto (acesso aberto)** | https://sol.sbc.org.br/index.php/sbbd_estendido/article/download/30791/30594/ |
| **DOI / página** | https://sol.sbc.org.br/index.php/sbbd_estendido/article/view/30791 |
| **Acesso** | ✅ Acesso aberto (SBC Open Library / SOL) |

**Por que entra no projeto:**
- Representa a **linha de DP que libera o grafo completo** (*graph release* sob
  DP) — o ramo mais próximo ao caso de uso deste projeto e que precisa ser
  citado como "linha existente, ainda em maturação", para justificar a
  continuidade do k-anonimato estrutural.
- Resume a tese de doutorado de Brito (UFC, 2023) — referência rastreável e
  auditável para o Eixo 5 da tabela da #217 (*granularidade/composição*).
- Propõe DP para grafos ponderados por contagem com topologia desconhecida —
  cenário diferente do grafo social com atributos do EpiCNet/módulo, o que
  reforça a divergência de premissas.
- Lista como métricas de utilidade: **clustering coefficient, shortest paths,
  PageRank, distribuição de graus e centralidade** — as mesmas previstas na
  seção 6 do CLAUDE.md do módulo, permitindo comparação metodológica direta.
- Disponibiliza datasets no Kaggle — citar isso demonstra que a linha existe
  em nível de artefato publicado, sem que o módulo precise reproduzir o
  trabalho.

**Pontos de conexão com o módulo:**
- O argumento defensável da #217 ("premissas divergem; nenhum método domina o
  outro") se ancora precisamente aqui: Brito & Machado publicam o grafo sob DP,
  mas com foco em grafos ponderados por contagem e topologia desconhecida —
  premissa diferente de grafo social com estrutura de comunidades conhecida.
- A comparação das métricas de utilidade usadas neste paper com as do módulo
  pode compor parte da **matriz privacidade-utilidade** (seção 5 do escopo
  funcional).

---

### 3. Oliveira, Pimentel & Marcacini (ENIAC 2024) — Privacy-Preserving k-NN Graphs with Autoencoder-Based Representations

| Campo | Valor |
|---|---|
| **Arquivo sugerido** | `Oliveira_2024_PrivacyPreservingKNNGraphsAutoencoder.pdf` |
| **Autores** | Oliveira, G. L.; Pimentel, M. G. C.; Marcacini, R. M. |
| **Título** | *Privacy-Preserving k-NN Graphs with Autoencoder-Based Representations for Sensitive Features* |
| **Venue** | Anais do XXI ENIAC (Encontro Nacional de Inteligência Artificial e Computacional), BRACIS 2024, Belém/PA, p. 683–694 |
| **Link direto (acesso aberto)** | https://sol.sbc.org.br/index.php/eniac/article/view/33835 |
| **DOI** | https://doi.org/10.5753/eniac.2024.245212 |
| **Acesso** | ✅ Acesso aberto (SBC Open Library / SOL) |

**Por que entra no projeto:**
- É o **único paper diretamente no ecossistema BRACIS** (o evento-alvo do
  módulo) que trata de privacidade em estruturas de grafo (2020–2024).
- Trabalha com preservação de privacidade em grafos k-NN via representação
  latente (autoencoders) — paradigma diferente do k-anonimato estrutural e
  da DP clássica em grafos, o que demonstra a diversidade da subárea e reforça
  a originalidade do nicho do projeto.
- Sua presença no ENIAC 2024 é evidência de que o tema **está chegando ao
  BRACIS**, mas ainda sem cobertura de k-anonimato estrutural nem DP em grafos
  — argumento de lacuna para a qualificação.
- Instituição: USP/ICMC (Marcacini) — grupo reconhecido em mineração de textos
  e grafos; citar este trabalho localiza o projeto no contexto da comunidade
  brasileira de IA.

**Pontos de conexão com o módulo:**
- A abordagem de representação latente como mecanismo de anonimização é
  conceitualmente diferente, mas as métricas de utilidade (preservação de
  estrutura de vizinhança, qualidade do grafo resultante) são comparáveis às
  do módulo — útil para a seção de **ameaças à validade** e de **trabalhos
  relacionados**.
- O paper opera sobre features sensíveis — tema que se conecta ao **risco
  atributivo** do módulo, complementando a visão estrutural.

---

### 4. Adeola et al. / arXiv 2024 — A Systematic Comparison of Measures for k-Anonymity in Networks

| Campo | Valor |
|---|---|
| **Arquivo sugerido** | `Adeola_2024_SystematicComparisonKAnonymityNetworks.pdf` |
| **Autores** | Adeola, O. et al. |
| **Título** | *A systematic comparison of measures for k-anonymity in networks* |
| **Venue** | arXiv preprint, 2024 |
| **Link direto (acesso aberto)** | https://arxiv.org/pdf/2407.02290.pdf |
| **arXiv** | https://arxiv.org/abs/2407.02290 |
| **Acesso** | ✅ Acesso aberto (arXiv) |

**Por que entra no projeto:**
- É o **survey de comparação sistemática de medidas de k-anonimato em redes**
  mais recente localizado (2024) — diretamente no paradigma deste projeto
  (*publicar dataset completo anonimizado para graph mining*).
- Propõe um conjunto de aspectos para escolha de medida de privacidade:
  tipo de privacidade desejada, cenário de adversário, utilidade dos dados,
  tipo de output e complexidade computacional — vocabulário que mapeia sobre
  a **matriz de métricas** (seção 6 do CLAUDE.md) e sobre os **requisitos
  não funcionais** do módulo.
- Analisa múltiplas medidas baseadas em k-anonimato que contabilizam a
  estrutura de vizinhança do nó em diferentes graus de alcance e completude
  — amplia o referencial além de He et al. (2009) sem abandonar o paradigma.
- Disponível no arXiv — preprint de acesso imediato, sem necessidade de acesso
  institucional.

**Pontos de conexão com o módulo:**
- Os "aspectos para escolha de medida" propostos no paper se alinham
  diretamente com o **plano experimental** (seção 8 do CLAUDE.md): o módulo
  precisará justificar a escolha de medidas de k-anonimato estrutural em
  detrimento de outras — este survey fornece o framework metodológico para
  isso.
- A distinção *completude e alcance da informação estrutural* usada no survey
  conecta-se ao Eixo 5 da tabela comparativa (#217) — *granularidade/composição*.
- É candidato a compor o **checklist de métricas iniciais** (unicidade de
  registros, frequência de combinações de atributos, k-anonymity) na camada 3
  da arquitetura do módulo (Extração de atributos e métricas).

---

## BibTeX

```bibtex
@inproceedings{Mendonca2023PrivacyPreservingSNA,
  author    = {Mendon{\c{c}}a, Ana Luiza C. and Brito, Filipe T. and Machado, Javam C.},
  title     = {Privacy-Preserving Techniques for Social Network Analysis},
  booktitle = {Anais Estendidos do XXXVIII Simp{\'o}sio Brasileiro de Bancos de Dados (SBBD)},
  year      = {2023},
  pages     = {174--178},
  publisher = {SBC},
  url       = {https://sol.sbc.org.br/index.php/sbbd_estendido/article/view/25632},
  note      = {Tutorial. Grupo LSBD/UFC.}
}

@inproceedings{Brito2024DPCountWeightedGraphs,
  author    = {Brito, Filipe T. and Machado, Javam C.},
  title     = {Differentially Private Release of Count-Weighted Graphs},
  booktitle = {Companion Proceedings of the 39th Brazilian Symposium on Databases (SBBD)},
  year      = {2024},
  pages     = {183--189},
  publisher = {SBC},
  url       = {https://sol.sbc.org.br/index.php/sbbd_estendido/article/view/30791},
  note      = {Resumo de tese de doutorado, Brito 2023, UFC/LSBD.}
}

@inproceedings{Oliveira2024PrivacyKNNGraphsAutoencoder,
  author    = {Oliveira, Gustavo L. de and Pimentel, Maria da Gra{\c{c}}a C. and Marcacini, Ricardo M.},
  title     = {Privacy-Preserving k-{NN} Graphs with Autoencoder-Based Representations for Sensitive Features},
  booktitle = {Anais do XXI Encontro Nacional de Intelig{\^e}ncia Artificial e Computacional (ENIAC)},
  year      = {2024},
  pages     = {683--694},
  publisher = {SBC},
  doi       = {10.5753/eniac.2024.245212},
  url       = {https://sol.sbc.org.br/index.php/eniac/article/view/33835}
}

@misc{Adeola2024SystematicKAnonymityNetworks,
  author        = {Adeola, Oluwaseun and others},
  title         = {A systematic comparison of measures for k-anonymity in networks},
  year          = {2024},
  eprint        = {2407.02290},
  archivePrefix = {arXiv},
  primaryClass  = {cs.CR},
  url           = {https://arxiv.org/abs/2407.02290}
}
```

---

## Status de download

| Arquivo | Status | Fonte |
|---|---|---|
| `Mendonca_2023_PrivacyPreservingTechniquesSocialNetworkAnalysis.pdf` | ⬜ pendente | SOL/SBC (acesso aberto) |
| `Brito_2024_DifferentiallyPrivateReleaseCountWeightedGraphs.pdf` | ⬜ pendente | SOL/SBC (acesso aberto) |
| `Oliveira_2024_PrivacyPreservingKNNGraphsAutoencoder.pdf` | ⬜ pendente | SOL/SBC — DOI 10.5753/eniac.2024.245212 |
| `Adeola_2024_SystematicComparisonKAnonymityNetworks.pdf` | ⬜ pendente | arXiv 2407.02290 (acesso aberto) |
