# ============================================================
# bootstrap_issues.ps1
# ============================================================
#
# Cria labels, milestones e todas as issues iniciais do projeto.
#
# Pre-requisitos:
#   - gh CLI instalado e autenticado (gh auth status)
#   - Executado na raiz do repositorio
#
# Uso (na raiz do repo):
#   .\.github\scripts\bootstrap_issues.ps1
#
# Idempotencia:
#   - Labels: --force atualiza descricao/cor se ja existir.
#   - Milestones: detectados por titulo; se ja existir, e reutilizado.
#   - Issues: NAO sao deduplicadas. Rodar duas vezes cria issues
#     duplicadas. Verifique antes de re-rodar.
#
# Aborta na primeira falha para evitar estado inconsistente.
# ============================================================

#Requires -Version 5.1

$ErrorActionPreference = "Stop"

# Forca encoding UTF-8 na saida do console (evita lixo em mensagens).
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# ----------------------------------------------------------------------
# Preflight
# ----------------------------------------------------------------------

Write-Host "Verificando autenticacao do gh CLI..." -ForegroundColor Cyan
gh auth status

$repo = gh repo view --json nameWithOwner -q ".nameWithOwner"
Write-Host "Repositorio alvo: $repo" -ForegroundColor Cyan
Write-Host ""

# ----------------------------------------------------------------------
# Labels
# ----------------------------------------------------------------------

Write-Host "Criando/atualizando labels..." -ForegroundColor Yellow

$labels = @(
    @{ name = "atomic";          color = "0E8A16"; description = "Tarefa atomica (uma sessao de Claude Code)" }
    @{ name = "component";       color = "1D76DB"; description = "Componente fechado (modulo ou arquivo)" }
    @{ name = "setup";           color = "FBCA04"; description = "Setup de ambiente, CI, ferramentas" }
    @{ name = "loader";          color = "5319E7"; description = "Carregamento de dataset" }
    @{ name = "algorithm";       color = "B60205"; description = "Algoritmo de anonimizacao" }
    @{ name = "attack";          color = "D93F0B"; description = "Ataque de reidentificacao" }
    @{ name = "metric";          color = "0052CC"; description = "Metrica de privacidade ou utilidade" }
    @{ name = "validation";      color = "C5DEF5"; description = "Validacao empirica de propriedades" }
    @{ name = "documentation";   color = "BFD4F2"; description = "Documentacao tecnica ou de processo" }
    @{ name = "experiment";      color = "006B75"; description = "Configuracao ou execucao de experimento" }
    @{ name = "milestone-29-05"; color = "E11D21"; description = "Bloqueante do marco 29/05" }
    @{ name = "minimo";          color = "5319E7"; description = "Escopo Minimo (obrigatorio)" }
    @{ name = "desejavel";       color = "FBCA04"; description = "Escopo Desejavel (contingente)" }
    @{ name = "aspiracional";    color = "C2E0C6"; description = "Escopo Aspiracional (bonus)" }
)

foreach ($lbl in $labels) {
    try {
        gh label create $lbl.name `
            --color $lbl.color `
            --description $lbl.description `
            --force | Out-Null
        Write-Host "  + $($lbl.name)"
    } catch {
        Write-Host "  ! $($lbl.name): $_" -ForegroundColor Red
        throw
    }
}

Write-Host ""

# ----------------------------------------------------------------------
# Milestones
# ----------------------------------------------------------------------

Write-Host "Criando milestones..." -ForegroundColor Yellow

$milestones = @(
    @{ title = "S1: Setup + Loader (ate 22/05)";
       description = "Setup do ambiente, CI, loader Facebook Ego-Nets, leitura de He et al.";
       due_on = "2026-05-22T23:59:59Z" }
    @{ title = "S2: He et al. + Validacao (ate 29/05) - MARCO";
       description = "Implementacao de He et al. (2009) com k-anonimato empiricamente validado. Marco nao-negociavel.";
       due_on = "2026-05-29T23:59:59Z" }
    @{ title = "S3: Ataques + Experimentos (ate 05/06)";
       description = "Ataques por grau e subgrafos; execucao dos experimentos sobre Facebook Ego-Nets.";
       due_on = "2026-06-05T23:59:59Z" }
    @{ title = "S4: Graficos + Documentacao (ate 12/06)";
       description = "Metricas, graficos privacy-vs-utility, tabelas, documentacao tecnica.";
       due_on = "2026-06-12T23:59:59Z" }
    @{ title = "S5: Entrega Final (ate 14/06)";
       description = "Polimento, reprodutibilidade end-to-end, entrega.";
       due_on = "2026-06-14T23:59:59Z" }
)

$existing = gh api "repos/$repo/milestones?state=all" --paginate | ConvertFrom-Json
$existingTitles = @{}
foreach ($m in $existing) { $existingTitles[$m.title] = $m.number }

foreach ($ms in $milestones) {
    if ($existingTitles.ContainsKey($ms.title)) {
        Write-Host "  = $($ms.title) (ja existe)"
        continue
    }
    try {
        gh api "repos/$repo/milestones" `
            --method POST `
            -f title="$($ms.title)" `
            -f description="$($ms.description)" `
            -f due_on="$($ms.due_on)" | Out-Null
        Write-Host "  + $($ms.title)"
    } catch {
        Write-Host "  ! $($ms.title): $_" -ForegroundColor Red
        throw
    }
}

Write-Host ""

# ----------------------------------------------------------------------
# Helper
# ----------------------------------------------------------------------

function New-Issue {
    param(
        [Parameter(Mandatory)] [string]   $Title,
        [Parameter(Mandatory)] [string]   $Body,
        [Parameter(Mandatory)] [string[]] $Labels,
        [string] $Milestone
    )
    $labelArgs = $Labels -join ","
    try {
        if ($Milestone) {
            gh issue create `
                --title $Title `
                --body $Body `
                --label $labelArgs `
                --milestone $Milestone | Out-Null
        } else {
            gh issue create `
                --title $Title `
                --body $Body `
                --label $labelArgs | Out-Null
        }
        Write-Host "  + $Title"
    } catch {
        Write-Host "  ! $Title : $_" -ForegroundColor Red
        throw
    }
}

$M1 = "S1: Setup + Loader (ate 22/05)"
$M2 = "S2: He et al. + Validacao (ate 29/05) - MARCO"
$M3 = "S3: Ataques + Experimentos (ate 05/06)"
$M4 = "S4: Graficos + Documentacao (ate 12/06)"
$M5 = "S5: Entrega Final (ate 14/06)"

# ============================================================
# ISSUES - Semana 1 (atomicas)
# ============================================================

Write-Host "Criando issues da Semana 1 (atomicas)..." -ForegroundColor Yellow

# --- S1.1 -----------------------------------------------------------
$body = @'
## Objetivo
Garantir que o ambiente local de desenvolvimento esta funcional antes de
qualquer implementacao. Esta issue NAO produz codigo de producao; produz
garantia de que o repositorio roda na maquina local.

## Definicao de pronto
- `.venv/` criado com Python 3.11 ou 3.12 na raiz do repo.
- `pip install -r requirements.txt -r requirements-dev.txt` instala sem erro.
- `python -c "import networkx; print(networkx.__version__)"` retorna >= 3.4.
- `ruff check .` e `ruff format --check .` rodam sem erros.
- `pytest --collect-only` coleta a estrutura de testes sem falhas.

## Arquivos esperados
Nenhum arquivo de codigo novo. Apenas verificacao do ambiente.

## Nao fazer
- Nao comitar `.venv/` (ja esta no `.gitignore`).
- Nao usar `conda` ou `poetry` nesta fase; manter padrao `venv + pip`.

## Branch sugerida
`setup/local-env`
'@
New-Issue -Milestone $M1 -Labels @("atomic","setup","minimo") `
  -Title "[S1] Setup local: ambiente Python e dependencias" `
  -Body $body

# --- S1.2 -----------------------------------------------------------
$body = @'
## Objetivo
Implementar script versionado que baixa o dataset Facebook Ego-Nets do SNAP
e o coloca em `data/raw/facebook/`. Dados brutos nao sao comitados (vide
`.gitignore`); o script e o que fica versionado.

## Contexto
SNAP: https://snap.stanford.edu/data/ego-Facebook.html
Os dados consistem em multiplas ego-redes; cada uma tem arquivos de arestas
e metadados associados.

## Definicao de pronto
- `src/loaders/download.py` implementado.
- Pode ser executado como modulo: `python -m src.loaders.download`.
- Cria `data/raw/facebook/` se nao existir.
- Baixa o tarball, extrai, e organiza por ego-rede.
- Verifica integridade (tamanho ou hash) e relata em log.
- Idempotente: rodar duas vezes nao re-baixa se ja estiver presente.

## Arquivos esperados
- `src/loaders/__init__.py` (vazio, se ainda nao existir).
- `src/loaders/download.py`.

## Nao fazer
- Nao baixar para o working directory raiz; sempre para `data/raw/facebook/`.
- Nao comitar os dados.
- Nao adicionar dependencias novas alem das ja em `requirements.txt` se
  `urllib` + `tarfile` da stdlib forem suficientes.

## Branch sugerida
`loader/snap-download`
'@
New-Issue -Milestone $M1 -Labels @("atomic","loader","minimo") `
  -Title "[S1] Loader: script de download do Facebook Ego-Nets (SNAP)" `
  -Body $body

# --- S1.3 -----------------------------------------------------------
$body = @'
## Objetivo
Implementar funcao que carrega uma ego-rede do Facebook como `nx.Graph`
nao-direcionado.

## Definicao de pronto
- `src/loaders/facebook_ego.py` implementado.
- Assinatura:
  `def load_facebook_egonet(egonet_id: int, data_dir: Path) -> nx.Graph`
- Le a edge list correspondente, retorna grafo nao-direcionado.
- Levanta `FileNotFoundError` se o egonet_id nao existir em `data_dir`.
- Type hints completos; docstring estilo Google ou NumPy.

## Arquivos esperados
- `src/loaders/facebook_ego.py`.

## Nao fazer
- Nao carregar atributos de nos nesta versao; somente edge list.
- Nao tratar como direcionado.
- Nao incluir logica de download aqui.

## Branch sugerida
`loader/facebook-ego`
'@
New-Issue -Milestone $M1 -Labels @("atomic","loader","minimo") `
  -Title "[S1] Loader: load_facebook_egonet(egonet_id, data_dir)" `
  -Body $body

# --- S1.4 -----------------------------------------------------------
$body = @'
## Objetivo
Teste unitario do loader, cobrindo caso tipico, caso ausente e tipo de retorno.

## Dependencias
Issue do `load_facebook_egonet`.

## Definicao de pronto
- `tests/loaders/test_facebook_ego.py` implementado.
- Testa:
  - Carrega ego-rede 0 e verifica `n_nodes > 0`, `n_edges > 0`.
  - Verifica que retorno e `nx.Graph` (nao-direcionado).
  - Verifica que `FileNotFoundError` e levantado para egonet_id inexistente.
- `pytest tests/loaders -v` passa.
- CI verde no PR.

## Observacao sobre dados em CI
Os dados brutos NAO estao versionados. Opcoes para o teste:
1. Skipar com `pytest.mark.skipif` se `data/raw/facebook/` nao existir
   (preferivel para iteracao rapida).
2. Usar um grafo sintetico minusculo de fixture que imita o formato esperado.
Documentar a escolha no docstring do teste.

## Branch sugerida
`loader/facebook-ego-test`
'@
New-Issue -Milestone $M1 -Labels @("atomic","loader","validation","minimo") `
  -Title "[S1] Teste do loader Facebook Ego-Net" `
  -Body $body

# --- S1.5 -----------------------------------------------------------
$body = @'
## Objetivo
Decidir entre `single_egonet`, `multiple_egonets` ou `union` (vide
`config_example.yml`) e registrar a decisao com justificativa.

## Contexto
Plano operacional, Secao 4.1: a decisao deve ser tomada na Semana 1 antes
de iniciar experimentos finais. Cada modo tem implicacao na variancia
amostral e no custo computacional.

## Definicao de pronto
- `docs/preprocessing_decision.md` criado com:
  - Decisao escolhida.
  - Justificativa em prosa (tamanho da ego-rede, custo de subgrafo, etc.).
  - Implicacao para os experimentos.
- `config_example.yml` atualizado se a decisao mudar o valor padrao.

## Nao fazer
- Nao adiar a decisao para a Semana 2; a escolha condiciona a implementacao
  dos ataques.

## Branch sugerida
`docs/preprocessing-decision`
'@
New-Issue -Milestone $M1 -Labels @("atomic","documentation","minimo") `
  -Title "[S1] Decidir e registrar modo de pre-processamento das ego-redes" `
  -Body $body

# --- S1.6 -----------------------------------------------------------
$body = @'
## Objetivo
Preencher a Secao 1 de `docs/algorithm_notes.md` apos leitura focada do
artigo de He et al. (2009).

## Definicao de pronto
- Secao 1 preenchida respondendo as tres perguntas listadas no esqueleto:
  - O que constitui um grupo de equivalencia em grafos?
  - Qual propriedade estrutural torna dois nos indistinguiveis?
  - k-anonimato aqui e sobre grau, vizinhanca, ou outra assinatura?
- Citacoes com pagina ou secao do artigo.

## Branch sugerida
`docs/algorithm-notes-s1`
'@
New-Issue -Milestone $M1 -Labels @("atomic","documentation","milestone-29-05") `
  -Title "[S1] Leitura He et al. (2009) - Secao 1: k-anonimato estrutural" `
  -Body $body

# --- S1.7 -----------------------------------------------------------
$body = @'
## Objetivo
Preencher Secao 2 de `docs/algorithm_notes.md` com pseudocodigo passo a
passo do algoritmo principal e complexidade declarada no artigo.

## Definicao de pronto
- Pseudocodigo registrado em formato de bloco.
- Complexidade O(...) declarada.
- Decisoes sobre estruturas de dados (qual representar onde) anotadas.

## Branch sugerida
`docs/algorithm-notes-s2`
'@
New-Issue -Milestone $M1 -Labels @("atomic","documentation","milestone-29-05") `
  -Title "[S1] Leitura He et al. (2009) - Secao 2: algoritmo principal" `
  -Body $body

# --- S1.8 -----------------------------------------------------------
$body = @'
## Objetivo
Preencher Secoes 3 (operacoes de modificacao) e 4 (criterio de parada) de
`docs/algorithm_notes.md`.

## Definicao de pronto
- Secao 3: o algoritmo adiciona, remove, ou ambos? Ha operacoes em nos?
  Determinismo vs. aleatoriedade (impacta sementes).
- Secao 4: como o algoritmo verifica k-anonimato internamente? O que
  acontece se nao for atingivel? Como projetar o `validate_k_anonymity`
  independente?

## Branch sugerida
`docs/algorithm-notes-s3-s4`
'@
New-Issue -Milestone $M1 -Labels @("atomic","documentation","milestone-29-05") `
  -Title "[S1] Leitura He et al. (2009) - Secoes 3-4: operacoes e parada" `
  -Body $body

# --- S1.9 -----------------------------------------------------------
$body = @'
## Objetivo
Criar `src/anonymization/he2009.py` com a estrutura de funcoes/classes
e docstrings - sem implementacao ainda. Serve para fixar a interface antes
de implementar.

## Definicao de pronto
- `src/anonymization/he2009.py` contem:
  - `def anonymize(G: nx.Graph, k: int, seed: int) -> nx.Graph: ...`
  - `def _partition_neighborhoods(G: nx.Graph) -> dict[int, nx.Graph]: ...`
  - `def _group_isomorphic(neighborhoods: dict[int, nx.Graph]) -> list[list[int]]: ...`
  - `def _modify_structure(G: nx.Graph, groups: list[list[int]], k: int, seed: int) -> nx.Graph: ...`
- Cada funcao tem docstring explicando entrada, saida, e referencia a
  secao do artigo.
- Cada funcao levanta `NotImplementedError` no corpo.
- `ruff check` limpo.
- Import nao quebra (`python -c "from src.anonymization import he2009"`).

## Nao fazer
- Nao implementar a logica nesta issue. So contrato + docstrings.

## Branch sugerida
`anonymization/api-skeleton`
'@
New-Issue -Milestone $M1 -Labels @("atomic","algorithm","milestone-29-05") `
  -Title "[S1] Esboco da API do anonimizador (skeleton sem implementacao)" `
  -Body $body

# ============================================================
# ISSUES - Semana 2 (atomicas, todas no marco)
# ============================================================

Write-Host "Criando issues da Semana 2 (atomicas, marco 29/05)..." -ForegroundColor Yellow

# --- S2.1 -----------------------------------------------------------
$body = @'
## Objetivo
Implementar o particionamento do grafo em vizinhancas locais 1-hop, conforme
He et al. (2009).

## Dependencias
Esboco da API + leitura concluida das Secoes 1-4 de `docs/algorithm_notes.md`.

## Definicao de pronto
- Funcao implementada (`NotImplementedError` removido).
- Retorna mapeamento `node_id -> subgrafo induzido pela vizinhanca`.
- Teste unitario em `tests/anonymization/test_he2009_partition.py` cobrindo:
  - Grafo pequeno conhecido (Petersen): conferir vizinhanca de no especifico.
  - Grafo regular: todas as vizinhancas isomorficas.
  - Grafo de caminho: vizinhancas distintas para nos diferentes.
- `ruff check` e `pytest` limpos.

## Branch sugerida
`anonymization/he2009-partition`
'@
New-Issue -Milestone $M2 -Labels @("atomic","algorithm","milestone-29-05","minimo") `
  -Title "[S2] Implementar _partition_neighborhoods (1-hop)" `
  -Body $body

# --- S2.2 -----------------------------------------------------------
$body = @'
## Objetivo
Agrupar vizinhancas isomorficas usando `nx.is_isomorphic` (ou VF2 direto).
Retorna grupos de nos cujas vizinhancas sao indistinguiveis.

## Dependencias
`_partition_neighborhoods` implementado.

## Definicao de pronto
- Funcao retorna `list[list[int]]` - cada lista interna e um grupo de
  equivalencia.
- Teste unitario:
  - Grafo regular: um unico grupo com todos os nos.
  - Grafo de caminho: grupos por simetria do caminho.
  - Grafo Petersen: agrupamento uniforme (todos os nos no mesmo grupo).
- Documentar custo computacional no docstring (isomorfismo e NP no caso
  geral; aqui aplicado a vizinhancas pequenas).

## Branch sugerida
`anonymization/he2009-grouping`
'@
New-Issue -Milestone $M2 -Labels @("atomic","algorithm","milestone-29-05","minimo") `
  -Title "[S2] Implementar _group_isomorphic" `
  -Body $body

# --- S2.3 -----------------------------------------------------------
$body = @'
## Objetivo
Implementar a modificacao estrutural minima do grafo para que cada grupo
de equivalencia tenha >= k membros, conforme He et al. (2009).

## Dependencias
`_group_isomorphic` implementado.

## Definicao de pronto
- Funcao recebe grafo, grupos de equivalencia, k e seed; retorna grafo
  anonimizado.
- Operacao aleatoria (adicao/remocao de arestas) usa `seed` para
  determinismo. NAO `random.seed()` global; usar `np.random.default_rng(seed)`.
- Teste unitario:
  - Verifica que o grafo de saida ainda e valido (sem self-loops, sem
    multi-arestas).
  - Verifica que tamanho do grafo de saida e proximo ao original
    (modificacao "minima" no sentido pratico).
  - Determinismo: mesma seed produz mesmo grafo de saida.

## Branch sugerida
`anonymization/he2009-modify`
'@
New-Issue -Milestone $M2 -Labels @("atomic","algorithm","milestone-29-05","minimo") `
  -Title "[S2] Implementar _modify_structure (adicao/remocao minima)" `
  -Body $body

# --- S2.4 -----------------------------------------------------------
$body = @'
## Objetivo
Integrar as tres funcoes auxiliares (`_partition_neighborhoods`,
`_group_isomorphic`, `_modify_structure`) em `anonymize()`.

## Dependencias
As tres issues anteriores fechadas.

## Definicao de pronto
- `anonymize` orquestra: particionar -> agrupar -> modificar.
- Teste unitario end-to-end:
  - Anonimiza Petersen com k=2 sem erro.
  - Verifica que o grafo de saida tem o mesmo numero de nos do de entrada.
- `ruff` e `pytest` limpos.

## Branch sugerida
`anonymization/he2009-integrate`
'@
New-Issue -Milestone $M2 -Labels @("atomic","algorithm","milestone-29-05","minimo") `
  -Title "[S2] Integrar anonymize(G, k, seed) - pipeline completo" `
  -Body $body

# --- S2.5 -----------------------------------------------------------
$body = @'
## Objetivo
Implementar o verificador independente de k-anonimato. AUDITOR EXTERNO,
nao reutilizar codigo interno do anonimizador.

## Contexto
Ver `docs/regras_anonimizacao.md` para o contrato completo.

## Definicao de pronto
- `src/anonymization/validation.py` implementado.
- Assinatura:
  `def validate_k_anonymity(G_anon: nx.Graph, k: int) -> bool`
- Deterministico (mesmo grafo -> mesmo resultado).
- NAO importa nada de `he2009.py` exceto tipos.
- Logs o resultado em `experiments/logs/` (formato JSONL).
- Teste:
  - Em grafo regular (todos os nos no mesmo grupo): retorna `True` para
    qualquer k <= n_nodes.
  - Em grafo de caminho (assimetrico): retorna `False` para k > 1.

## Nao fazer
- Nao reutilizar `_group_isomorphic` do anonimizador - implementacao
  separada.
- Nao silenciar resultado False; log claro.

## Branch sugerida
`anonymization/validate`
'@
New-Issue -Milestone $M2 -Labels @("atomic","validation","milestone-29-05","minimo") `
  -Title "[S2] Implementar validate_k_anonymity (auditor independente)" `
  -Body $body

# --- S2.6 -----------------------------------------------------------
$body = @'
## Objetivo
MARCO NAO-NEGOCIAVEL do projeto. Demonstrar empiricamente que
`anonymize(G, k=5, seed)` produz grafo onde `validate_k_anonymity` retorna
`True`, em 3 sementes independentes, sobre ao menos uma ego-rede do Facebook.

## Dependencias
Todas as issues anteriores de S2 fechadas.

## Definicao de pronto
- Configuracao YAML em `experiments/configs/milestone_29_05.yml`.
- Script de execucao roda 3 sementes (e.g., 42, 1337, 2718).
- Log estruturado em `experiments/logs/milestone_29_05/` com:
  - Grafo de entrada (hash ou tamanho).
  - k usado.
  - Seed.
  - Resultado de `validate_k_anonymity`.
- Criterio: `validate_k_anonymity` retorna `True` em 100% das 3 execucoes.

## Se falhar
Documentar em `docs/algorithm_notes.md` Secao 7 (Decisoes de implementacao)
e abrir nova issue de correcao. Acionar protocolo da Secao 7 do plano
operacional: restringir k, usar ego-rede menor, simplificar algoritmo, ou
aceitar entrega parcial.

## Branch sugerida
`validation/milestone-29-05`
'@
New-Issue -Milestone $M2 -Labels @("atomic","validation","milestone-29-05","minimo") `
  -Title "[S2] MARCO 29/05 - Sanidade k=5 sobre ego-rede do Facebook" `
  -Body $body

# --- S2.7 -----------------------------------------------------------
$body = @'
## Objetivo
Estender a validacao do marco para os outros valores de k do escopo Minimo.

## Dependencias
Marco 29/05 atingido (ao menos um k validado).

## Definicao de pronto
- Configuracoes YAML para k=2, k=10, k=20.
- Execucao com 3 sementes cada.
- Log estruturado para cada.
- Resultado documentado em `docs/algorithm_notes.md` Secao 7.

## Se k=10 ou k=20 falharem
Documentar e seguir. O Minimo defensavel exige k em pelo menos 4 valores,
mas a invalidacao de algum k e resultado cientifico valido (mostra o limite
do algoritmo). Reportar nos graficos finais.

## Branch sugerida
`validation/k-sweep`
'@
New-Issue -Milestone $M2 -Labels @("atomic","validation","minimo") `
  -Title "[S2] Testes de sanidade adicionais: k=2, k=10, k=20" `
  -Body $body

# --- S2.8 -----------------------------------------------------------
$body = @'
## Objetivo
Registrar, em `docs/milestone_29_05.md`, o resultado consolidado do marco:
configuracoes que passaram, configuracoes que falharam (se houver), decisao
tomada.

## Definicao de pronto
- Documento criado contendo:
  - Data de execucao.
  - Hash do commit usado.
  - Tabela: k, seeds, resultado, observacao.
  - Decisao sobre prosseguir conforme planejado ou acionar reformulacao
    (Secao 7 do plano operacional).
- Linkado a partir do `CLAUDE.md` (atualizar referencias).

## Branch sugerida
`docs/milestone-29-05`
'@
New-Issue -Milestone $M2 -Labels @("atomic","documentation","minimo") `
  -Title "[S2] Documentar resultado do marco 29/05" `
  -Body $body

# ============================================================
# ISSUES - Semana 3 (componentes)
# ============================================================

Write-Host "Criando issues da Semana 3 (componentes)..." -ForegroundColor Yellow

# --- S3.1 -----------------------------------------------------------
$body = @'
## Objetivo
Implementar ataque de reidentificacao por grau.

## Interface publica
`def degree_attack(G_orig: nx.Graph, G_anon: nx.Graph, target: int, tolerance: int = 0) -> bool`

Retorna `True` se o no-alvo for unicamente identificavel no grafo anonimizado
a partir do conhecimento do seu grau no grafo original (dentro da tolerancia).

## Dependencias
Loader Facebook Ego-Net + anonimizador He et al. validados.

## Definicao de pronto
- [ ] Componente em `src/attacks/degree.py` implementado.
- [ ] Testes em `tests/attacks/test_degree.py`: caso tipico, no isolado,
      tolerancia diferente de zero, no-alvo inexistente.
- [ ] Docstrings claras.
- [ ] `ruff check` e `pytest` limpos.
- [ ] CI verde.

## Branch sugerida
`attack/degree`
'@
New-Issue -Milestone $M3 -Labels @("component","attack","minimo") `
  -Title "[S3] Componente: src/attacks/degree.py" `
  -Body $body

# --- S3.2 -----------------------------------------------------------
$body = @'
## Objetivo
Implementar ataque por subgrafos via isomorfismo de subgrafos induzidos
pela vizinhanca k-hop (k=1 na primeira iteracao). Backend: VF2 via
`networkx.algorithms.isomorphism.GraphMatcher`.

## Interface publica
`def subgraph_attack(G_orig: nx.Graph, G_anon: nx.Graph, target: int, hop: int = 1) -> bool`

## Consideracoes
Custo computacional cresce rapidamente com `hop`; restringir a `hop=1`
nesta primeira iteracao. Adicionar timeout opcional para evitar travamento
em grafos grandes.

## Definicao de pronto
- [ ] Componente implementado.
- [ ] Testes cobrindo caso tipico e timeout.
- [ ] Documentacao do trade-off `hop` vs. custo no docstring.
- [ ] CI verde.

## Branch sugerida
`attack/subgraph`
'@
New-Issue -Milestone $M3 -Labels @("component","attack","minimo") `
  -Title "[S3] Componente: src/attacks/subgraph.py (VF2)" `
  -Body $body

# --- S3.3 -----------------------------------------------------------
$body = @'
## Objetivo
Implementar as quatro metricas conforme definidas em
`docs/metrics_definitions.md`:

1. `reidentification_rate(attack_results) -> float`
2. `equivalence_group_size(G_anon) -> tuple[float, int]` (media, mediana)
3. `ks_test_degree(G_orig, G_anon) -> tuple[float, float]` (D, p-valor)
4. `clustering_variation(G_orig, G_anon) -> float`

## Dependencias
Anonimizacao + ao menos um ataque funcionando.

## Definicao de pronto
- [ ] Cada metrica em arquivo proprio sob `src/metrics/`.
- [ ] `__init__.py` exporta a API publica.
- [ ] Testes unitarios cada um.
- [ ] CI verde.

## Branch sugerida
`metric/all-four`
'@
New-Issue -Milestone $M3 -Labels @("component","metric","minimo") `
  -Title "[S3] Componente: src/metrics/ (4 metricas)" `
  -Body $body

# --- S3.4 -----------------------------------------------------------
$body = @'
## Objetivo
Implementar o runner que orquestra: carrega config YAML, executa anonimizacao
+ ataques + metricas, registra logs estruturados.

## Interface
`python -m experiments.run --config experiments/configs/<nome>.yml`

## Definicao de pronto
- [ ] CLI funcional com argparse.
- [ ] Le YAML, itera sobre seeds e k, executa pipeline.
- [ ] Log JSONL em `experiments/logs/<config_name>/<timestamp>.jsonl`.
- [ ] Tratamento de erros: experimento parado sinaliza no log, nao silencia.
- [ ] CI verde.

## Branch sugerida
`experiment/runner`
'@
New-Issue -Milestone $M3 -Labels @("component","experiment","minimo") `
  -Title "[S3] Componente: experiments/run.py (runner)" `
  -Body $body

# --- S3.5 -----------------------------------------------------------
$body = @'
## Objetivo
Executar o experimento baseline completo: 4 valores de k x 2 ataques x 3
sementes sobre Facebook Ego-Nets.

## Dependencias
Runner + ataques + metricas implementados.

## Definicao de pronto
- [ ] Config em `experiments/configs/he2009_facebook_baseline.yml`.
- [ ] Execucao bem-sucedida, logs gerados em `experiments/logs/`.
- [ ] Verificacao: cada combinacao tem 3 logs (uma por seed).
- [ ] Resultado preliminar (tabela bruta) comitado em `docs/` ou
      anexado ao PR.

## Branch sugerida
`experiment/facebook-baseline`
'@
New-Issue -Milestone $M3 -Labels @("component","experiment","minimo") `
  -Title "[S3] Execucao: experimento baseline Facebook Ego-Nets" `
  -Body $body

# ============================================================
# ISSUES - Semana 4 (componentes)
# ============================================================

Write-Host "Criando issues da Semana 4 (componentes)..." -ForegroundColor Yellow

# --- S4.1 -----------------------------------------------------------
$body = @'
## Objetivo
Gerar o grafico principal do projeto: privacidade (eixo x ou y) vs. utilidade,
com curva por k e barras de erro pelas 3 sementes.

## Definicao de pronto
- [ ] Script em `src/visualization/privacy_utility.py`.
- [ ] Le logs de `experiments/logs/` e produz PDF + PNG em `results/plots/`.
- [ ] Barras de erro visiveis.
- [ ] Legenda clara (qual ataque, qual k).
- [ ] Reproduzivel: `python -m src.visualization.privacy_utility --logs <dir>`.
- [ ] CI verde.

## Branch sugerida
`viz/privacy-utility`
'@
New-Issue -Milestone $M4 -Labels @("component","experiment","minimo") `
  -Title "[S4] Componente: geracao do grafico privacy-vs-utility" `
  -Body $body

# --- S4.2 -----------------------------------------------------------
$body = @'
## Objetivo
Gerar tabelas em CSV resumindo os resultados, em `results/tables/`.

## Definicao de pronto
- [ ] Uma tabela por combinacao `(dataset, ataque)` com colunas:
      `k, seed, reid_rate, eq_group_mean, ks_D, ks_p, clustering_var`.
- [ ] Reproduzivel a partir dos logs.
- [ ] CI verde.

## Branch sugerida
`viz/tables`
'@
New-Issue -Milestone $M4 -Labels @("component","experiment","minimo") `
  -Title "[S4] Componente: geracao das tabelas CSV" `
  -Body $body

# --- S4.3 -----------------------------------------------------------
$body = @'
## Objetivo
Produzir `docs/pipeline.md` documentando o fluxo completo:
config YAML -> anonimizacao -> ataques -> metricas -> graficos.

## Definicao de pronto
- [ ] Diagrama (ASCII ou Mermaid) do pipeline.
- [ ] Comandos para reproduzir cada etapa a partir do zero.
- [ ] Lista de outputs esperados e onde eles aparecem.
- [ ] Limitacoes conhecidas documentadas.
- [ ] `algorithm_notes.md` e `metrics_definitions.md` revisados e
      cross-referenciados.

## Branch sugerida
`docs/pipeline-final`
'@
New-Issue -Milestone $M4 -Labels @("component","documentation","minimo") `
  -Title "[S4] Documentacao tecnica final do pipeline" `
  -Body $body

# ============================================================
# ISSUES - Semana 5 (componentes)
# ============================================================

Write-Host "Criando issues da Semana 5 (componentes)..." -ForegroundColor Yellow

# --- S5.1 -----------------------------------------------------------
$body = @'
## Objetivo
Executar o projeto inteiro a partir de um clone limpo em ambiente novo
(novo `.venv`), seguindo apenas o README e o CLAUDE.md. Validar que os
graficos finais sao reproduzidos.

## Definicao de pronto
- [ ] Clone novo em diretorio separado.
- [ ] `.venv` novo, `pip install`, `python -m src.loaders.download`.
- [ ] Executar config principal e verificar que outputs em `results/`
      batem (hash ou comparacao visual) com a versao em `main`.
- [ ] Eventual gap documentado e corrigido em PR.

## Branch sugerida
`validation/e2e-reproducibility`
'@
New-Issue -Milestone $M5 -Labels @("component","validation","minimo") `
  -Title "[S5] Reprodutibilidade end-to-end (do zero)" `
  -Body $body

# --- S5.2 -----------------------------------------------------------
$body = @'
## Objetivo
Revisao final de toda a documentacao para a entrega de 14/06.

## Definicao de pronto
- [ ] README revisado: status atualizado, links funcionando, comandos
      validados.
- [ ] `CLAUDE.md` atualizado se algo mudou na fase final.
- [ ] `docs/` integralmente revisado.
- [ ] WORKFLOW.md ainda reflete a pratica real (calibragem se necessaria).
- [ ] Lista de entregaveis (Minimo / Desejavel / Aspiracional alcancados)
      em `docs/entregaveis.md`.

## Branch sugerida
`docs/final-review`
'@
New-Issue -Milestone $M5 -Labels @("component","documentation","minimo") `
  -Title "[S5] README final + revisao da documentacao" `
  -Body $body

# ============================================================
# ISSUES - Contingentes (sem milestone)
# ============================================================

Write-Host "Criando issues contingentes (Desejavel/Aspiracional)..." -ForegroundColor Yellow

# --- Contingente 1 -------------------------------------------------
$body = @'
## Objetivo
Estender o pipeline para o dataset Email-Enron (versao estatica do SNAP)
como dataset secundario.

## Condicao
So entra em escopo se o Minimo (Facebook Ego-Nets) estiver consolidado com
folga ate 05/06. Vide plano operacional, Secao 4.2.

## Definicao de pronto
- [ ] Loader implementado convertendo o grafo direcionado para nao-direcionado.
- [ ] Config YAML para Enron.
- [ ] Execucao bem-sucedida com ataques por grau (subgrafo pode ser proibitivo
      em escala maior; restringir a hop=1).
- [ ] Graficos comparativos Facebook vs. Enron, se aplicavel.

## Branch sugerida
`loader/enron`
'@
New-Issue -Labels @("component","loader","desejavel") `
  -Title "[DESEJAVEL] Loader Email-Enron + execucao secundaria" `
  -Body $body

# --- Contingente 2 -------------------------------------------------
$body = @'
## Objetivo
Implementar o ataque por entropia, derivado dos grupos de equivalencia ja
calculados pela metrica de privacidade.

## Condicao
Apos consolidar Minimo. Vide plano operacional, Secao 4.4.

## Definicao de pronto
- [ ] `src/attacks/entropy.py`.
- [ ] Reutiliza grupos de equivalencia ja calculados; nao refaz experimentos.
- [ ] Testes unitarios.
- [ ] CI verde.

## Branch sugerida
`attack/entropy`
'@
New-Issue -Labels @("component","attack","desejavel") `
  -Title "[DESEJAVEL] Ataque por entropia" `
  -Body $body

# --- Contingente 3 -------------------------------------------------
$body = @'
## Objetivo
Esboco inicial do anonimizador Nettleton & Salas (2016) sobre Facebook
Ego-Nets, para comparacao preliminar com He et al. no mesmo grafico.

## Condicao
NAO perseguir em detrimento do Minimo. So entra se Desejavel ja foi
consolidado e ha folga real ate 12/06. Vide plano operacional, Secao 3 (D3).

## Definicao de pronto
- [ ] Leitura focada do paper documentada em `docs/algorithm_notes_nettleton.md`.
- [ ] Implementacao em `src/anonymization/nettleton_salas.py`.
- [ ] `validate_k_anonymity` adaptado (ou novo) para a definicao deles.
- [ ] Execucao em ao menos uma configuracao.
- [ ] Adicionado ao grafico privacy-vs-utility como segunda curva.

## Branch sugerida
`anonymization/nettleton-salas`
'@
New-Issue -Labels @("component","algorithm","aspiracional") `
  -Title "[ASPIRACIONAL] Nettleton & Salas (2016) - implementacao inicial" `
  -Body $body

# ============================================================
# Fim
# ============================================================

Write-Host ""
Write-Host "Bootstrap completo." -ForegroundColor Green
Write-Host "Issues criadas. Conferir em:"
Write-Host "  https://github.com/$repo/issues"
