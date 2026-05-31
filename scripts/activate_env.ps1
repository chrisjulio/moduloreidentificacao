# =============================================================================
# activate_env.ps1
# Ativa o ambiente Conda do projeto e verifica se pymetis está disponível.
#
# Use este script ANTES de rodar o programa principal para garantir que
# o interpretador correto e o backend METIS estão ativos.
#
# Uso (no Anaconda PowerShell Prompt ou PowerShell com conda init):
#   . .\scripts\activate_env.ps1
#
# IMPORTANTE: use o operador ponto-espaço (". ") para que a ativação
# persista no terminal atual. Sem ele, o ambiente ativa e fecha.
#
# Após executar, o prompt mostrará (moduloreidentificacao) e você pode
# rodar normalmente:  python <seu_script>.py
# =============================================================================

$ENV_NAME = "moduloreidentificacao"

# -----------------------------------------------------------------------------
# 1. Verificar que conda está disponível
# -----------------------------------------------------------------------------
if (-not (Get-Command conda -ErrorAction SilentlyContinue)) {
    Write-Host ""
    Write-Host "[ERRO] conda nao encontrado no PATH." -ForegroundColor Red
    Write-Host "       Abra o 'Anaconda PowerShell Prompt' ou execute:" -ForegroundColor Red
    Write-Host "       conda init powershell  (e reinicie o terminal)" -ForegroundColor Red
    Write-Host ""
    return
}

# -----------------------------------------------------------------------------
# 2. Verificar que o ambiente existe
# -----------------------------------------------------------------------------
$envExists = conda env list 2>$null | Select-String -Pattern "^$ENV_NAME"
if (-not $envExists) {
    Write-Host ""
    Write-Host "[ERRO] Ambiente '$ENV_NAME' nao encontrado." -ForegroundColor Red
    Write-Host "       Execute o setup completo primeiro:" -ForegroundColor Red
    Write-Host "       .\scripts\setup_conda_windows.ps1" -ForegroundColor Yellow
    Write-Host ""
    return
}

# -----------------------------------------------------------------------------
# 3. Ativar o ambiente
# -----------------------------------------------------------------------------
Write-Host ""
Write-Host "--> Ativando ambiente: $ENV_NAME" -ForegroundColor Cyan
conda activate $ENV_NAME

# -----------------------------------------------------------------------------
# 4. Verificar pymetis
# -----------------------------------------------------------------------------
Write-Host "--> Verificando pymetis..." -ForegroundColor Cyan

$pymetisOk = conda run -n $ENV_NAME python -c "
try:
    import pymetis
    cut, parts = pymetis.part_graph(2, adjacency=[[1,2],[0,2],[0,1]])
    print('OK')
except Exception as e:
    print(f'FALHA: {e}')
" 2>$null

if ($pymetisOk -eq "OK") {
    Write-Host "    pymetis: OK (backend METIS-C ativo)" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[AVISO] pymetis nao funcional: $pymetisOk" -ForegroundColor Yellow
    Write-Host "        O programa usara o fallback Kernighan-Lin." -ForegroundColor Yellow
    Write-Host "        Para reinstalar:" -ForegroundColor Yellow
    Write-Host "        conda install -n $ENV_NAME -c conda-forge pymetis -y" -ForegroundColor White
    Write-Host ""
}

# -----------------------------------------------------------------------------
# 5. Confirmar ambiente ativo e interpretador
# -----------------------------------------------------------------------------
$pythonPath = (conda run -n $ENV_NAME python -c "import sys; print(sys.executable)" 2>$null)

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host " Ambiente pronto para uso" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host " Ambiente : $ENV_NAME" -ForegroundColor White
Write-Host " Python   : $pythonPath" -ForegroundColor White
Write-Host ""
Write-Host " Pronto. Voce pode rodar o projeto:" -ForegroundColor Yellow
Write-Host "   python <script>.py" -ForegroundColor White
Write-Host ""
