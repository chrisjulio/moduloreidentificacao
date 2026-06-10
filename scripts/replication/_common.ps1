# Shared helpers for the PowerShell replication wrappers (issue #184).
# Resolves the repository root from this file's location and picks a Python
# interpreter, so the wrappers work regardless of the caller's CWD and never
# depend on an IDE or a user-local absolute path.
$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $ScriptDir '..\..')).Path
$Driver = Join-Path $ScriptDir 'replicate.py'

function Get-PythonExe {
    # Prefer an activated virtualenv, then 'python', then 'py -3'. Fail explicitly.
    if ($env:VIRTUAL_ENV) {
        $venvPy = Join-Path $env:VIRTUAL_ENV 'Scripts\python.exe'
        if (Test-Path $venvPy) { return $venvPy }
    }
    $py = Get-Command python -ErrorAction SilentlyContinue
    if ($py) { return $py.Source }
    $pyLauncher = Get-Command py -ErrorAction SilentlyContinue
    if ($pyLauncher) { return 'py' }
    Write-Error 'ERROR: no python interpreter found on PATH.'
    exit 3
}

function Invoke-Stage {
    param([Parameter(ValueFromRemainingArguments = $true)] [string[]] $StageArgs)
    $python = Get-PythonExe
    # Always invoke from the repo root so the driver's relative paths resolve.
    Push-Location $RepoRoot
    try {
        if ($python -eq 'py') {
            & py -3 $Driver @StageArgs
        }
        else {
            & $python $Driver @StageArgs
        }
        exit $LASTEXITCODE
    }
    finally {
        Pop-Location
    }
}
