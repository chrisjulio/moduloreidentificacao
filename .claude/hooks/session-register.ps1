# UserPromptSubmit hook — registra a sessao no log e (se houver) injeta aviso de sobrecarga.
# Le o JSON do hook via stdin. Portavel: usa CLAUDE_PROJECT_DIR ou o campo cwd como fallback.
$ErrorActionPreference = 'Stop'
try {
    $raw = [Console]::In.ReadToEnd()
    if (-not $raw) { exit 0 }
    $data = $raw | ConvertFrom-Json

    $sid = $data.session_id
    $prompt = [string]$data.prompt

    $projDir = $env:CLAUDE_PROJECT_DIR
    if (-not $projDir) { $projDir = $data.cwd }
    if (-not $projDir) { exit 0 }

    $logDir = Join-Path $projDir '.claude'
    if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Force -Path $logDir | Out-Null }
    $log = Join-Path $logDir 'session-log.md'
    if (-not (Test-Path $log)) {
        Set-Content -Path $log -Value "# Registro de sessoes (gitignored)`n" -Encoding utf8
    }

    # 1) Sinal de sobrecarga deixado por um PreCompact anterior nesta sessao.
    $additionalContext = $null
    if ($sid) {
        $flag = Join-Path $logDir (".overload-" + $sid)
        if (Test-Path $flag) {
            Remove-Item $flag -Force
            $additionalContext = "AVISO DE SESSAO: o contexto desta sessao ja foi compactado pelo menos uma vez (sinal de sobrecarga). De forma breve, recomende ao usuario recomecar numa nova sessao para preservar qualidade/velocidade, oferecendo antes confirmar/curar o assunto atual em .claude/session-log.md."
        }
    }

    # 2) Registra a sessao no log apenas no primeiro prompt (assunto = rascunho do 1o prompt).
    if ($sid) {
        $content = Get-Content -Path $log -Raw -ErrorAction SilentlyContinue
        if (-not $content -or ($content -notmatch [regex]::Escape($sid))) {
            $ts = Get-Date -Format 'yyyy-MM-dd HH:mm'
            $subject = ($prompt -replace '\s+', ' ').Trim()
            if ($subject.Length -gt 140) { $subject = $subject.Substring(0, 140) + ' [...]' }
            if (-not $subject) { $subject = '(sem texto no primeiro prompt)' }
            $entry = "`n## $ts`n- **session_id:** ``$sid```n- **assunto (rascunho):** $subject`n- **status:** ativa`n- **comando:** claude --resume $sid`n"
            Add-Content -Path $log -Value $entry -Encoding utf8
        }
    }

    if ($additionalContext) {
        $out = @{ hookSpecificOutput = @{ hookEventName = 'UserPromptSubmit'; additionalContext = $additionalContext } } | ConvertTo-Json -Compress
        Write-Output $out
    }
    exit 0
} catch {
    # Nunca bloquear o prompt do usuario por falha de logging.
    exit 0
}
