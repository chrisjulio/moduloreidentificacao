# PreCompact hook — sinal de sobrecarga: o harness vai compactar o contexto.
# Anota no log, deixa um flag pro proximo UserPromptSubmit e mostra mensagem ao usuario.
$ErrorActionPreference = 'Stop'
try {
    $raw = [Console]::In.ReadToEnd()
    $data = if ($raw) { $raw | ConvertFrom-Json } else { $null }

    $sid = if ($data) { $data.session_id } else { $null }
    $trigger = if ($data -and $data.trigger) { $data.trigger } else { 'auto' }

    $projDir = $env:CLAUDE_PROJECT_DIR
    if (-not $projDir -and $data) { $projDir = $data.cwd }
    if (-not $projDir) { exit 0 }

    $logDir = Join-Path $projDir '.claude'
    if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Force -Path $logDir | Out-Null }
    $log = Join-Path $logDir 'session-log.md'
    if (-not (Test-Path $log)) {
        Set-Content -Path $log -Value "# Registro de sessoes (gitignored)`n" -Encoding utf8
    }

    $ts = Get-Date -Format 'yyyy-MM-dd HH:mm'
    $note = "  - **[$ts] sobrecarga:** compactacao ($trigger) disparada - considere recomecar em nova sessao.`n"
    Add-Content -Path $log -Value $note -Encoding utf8

    if ($sid) {
        $flag = Join-Path $logDir (".overload-" + $sid)
        Set-Content -Path $flag -Value $ts -Encoding utf8
    }

    $out = @{ systemMessage = "Sessao sobrecarregada: o contexto foi compactado ($trigger). Vale recomecar em nova sessao - o assunto esta em .claude/session-log.md." } | ConvertTo-Json -Compress
    Write-Output $out
    exit 0
} catch {
    exit 0
}
