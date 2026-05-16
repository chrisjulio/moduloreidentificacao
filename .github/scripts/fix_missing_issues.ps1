# ============================================================
# fix_missing_issues.ps1
# ============================================================
# Cria as duas issues que falharam no bootstrap original
# (corpos com aspas duplas internas quebraram o parsing de
# argumentos do PowerShell -> gh CLI).
#
# Solucao: passar o body via --body-file (arquivo temporario)
# em vez de --body inline.
#
# Idempotente: nao faz nada se as issues ja existirem (checa por titulo).
# ============================================================

#Requires -Version 5.1
$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$M1 = "S1: Setup + Loader (ate 22/05)"

function New-IssueSafe {
    param(
        [Parameter(Mandatory)] [string]   $Title,
        [Parameter(Mandatory)] [string]   $Body,
        [Parameter(Mandatory)] [string[]] $Labels,
        [string] $Milestone
    )

    # Idempotencia: ja existe?
    $existing = gh issue list --state all --search "in:title `"$Title`"" `
        --json title --limit 5 | ConvertFrom-Json
    if ($existing | Where-Object { $_.title -eq $Title }) {
        Write-Host "  = $Title (ja existe; pulando)"
        return
    }

    $labelArgs = $Labels -join ","
    $tmp = [System.IO.Path]::GetTempFileName()
    try {
        # Grava body em UTF-8 sem BOM (gh CLI espera UTF-8 puro)
        [System.IO.File]::WriteAllText(
            $tmp, $Body, [System.Text.UTF8Encoding]::new($false))

        if ($Milestone) {
            gh issue create `
                --title $Title `
                --body-file $tmp `
                --label $labelArgs `
                --milestone $Milestone | Out-Null
        } else {
            gh issue create `
                --title $Title `
                --body-file $tmp `
                --label $labelArgs | Out-Null
        }
        if ($LASTEXITCODE -ne 0) {
            throw "gh issue create falhou (exit code $LASTEXITCODE)"
        }
        Write-Host "  + $Title"
    } finally {
        Remove-Item $tmp -ErrorAction SilentlyContinue
    }
}

Write-Host "Recriando issues que falharam no bootstrap..." -ForegroundColor Yellow

# --- S1.1: Setup local ----------------------------------------------
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
New-IssueSafe -Milestone $M1 -Labels @("atomic","setup","minimo") `
  -Title "[S1] Setup local: ambiente Python e dependencias" `
  -Body $body

# --- S1.9: Esboco da API --------------------------------------------
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
New-IssueSafe -Milestone $M1 -Labels @("atomic","algorithm","milestone-29-05") `
  -Title "[S1] Esboco da API do anonimizador (skeleton sem implementacao)" `
  -Body $body

Write-Host ""
Write-Host "Pronto." -ForegroundColor Green