# =============================================================================
# setup_conda_windows.ps1
# Configuração do ambiente de desenvolvimento no Windows via Miniconda/Conda.
#
# Contexto:
#   pymetis (backend METIS para particionamento de grafos) não pode ser
#   compilado via pip no Windows. O código-fonte da biblioteca GKlib usa
#   headers POSIX (regex.h) incompatíveis com MSVC, causando falha em todas
#   as versões recentes. A solução é instalar via conda-forge, que distribui
#   binários pré-compilados para win-64.
#
# Pré-requisito: Miniconda instalado.
#   winget install Anaconda.Miniconda3
#   (reinicie o terminal após instalar)
#
# Uso:
#   1. Abra o "Anaconda PowerShell Prompt" (menu Iniciar)
#      OU execute no PowerShell comum após rodar: conda init powershell
#   2. Navegue até a raiz do projeto:
#      cd "C:\Users\<usuario>\vs code\moduloreidentificacao"
#   3. Execute:
#      .\scripts\setup_conda_windows.ps1
#
# Após a execução:
#   - Ative o ambiente:  conda activate moduloreidentificacao
#   - No VS Code:        Ctrl+Shift+P -> Python: Select Interpreter
#     Escolha: ...\miniconda3\envs\moduloreidentificacao\python.exe
# =============================================================================

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ENV_NAME = "moduloreidentificacao"
$PYTHON_VERSION = "3.12"

Write-Host ""
Write-Host "=============================================================" -ForegroundColor Cyan
Write-Host " Setup: ambiente Conda para $ENV_NAME" -ForegroundColor Cyan
Write-Host "=============================================================" -ForegroundColor Cyan

# -----------------------------------------------------------------------------
# 1. Verificar que conda está disponível
# -----------------------------------------------------------------------------
Write-Host ""
Write-Host "--> Verificando Conda..." -ForegroundColor Yellow
try {
    $condaVersion = conda --version 2>&1
    Write-Host "    $condaVersion" -ForegroundColor Green
} catch {
    Write-Host "ERRO: conda não encontrado." -ForegroundColor Red
    Write-Host "Instale o Miniconda com: winget install Anaconda.Miniconda3" -ForegroundColor Red
    Write-Host "Depois reinicie o terminal e execute este script novamente." -ForegroundColor Red
    exit 1
}

# -----------------------------------------------------------------------------
# 2. Remover ambiente anterior (se existir)
# -----------------------------------------------------------------------------
$envExists = conda env list | Select-String -Pattern "^$ENV_NAME"
if ($envExists) {
    Write-Host ""
    Write-Host "--> Ambiente '$ENV_NAME' já existe. Removendo para recriar..." -ForegroundColor Yellow
    conda env remove -n $ENV_NAME -y
}

# -----------------------------------------------------------------------------
# 3. Criar ambiente com Python 3.12
# -----------------------------------------------------------------------------
Write-Host ""
Write-Host "--> Criando ambiente Conda '$ENV_NAME' (Python $PYTHON_VERSION)..." -ForegroundColor Yellow
conda create -n $ENV_NAME python=$PYTHON_VERSION -y

# -----------------------------------------------------------------------------
# 4. Instalar pymetis via conda-forge
#    Binário pré-compilado win-64 — sem necessidade de compilador C.
# -----------------------------------------------------------------------------
Write-Host ""
Write-Host "--> Instalando pymetis via conda-forge (binário pré-compilado)..." -ForegroundColor Yellow
conda install -n $ENV_NAME -c conda-forge pymetis -y

# -----------------------------------------------------------------------------
# 5. Instalar demais dependências via pip
# -----------------------------------------------------------------------------
Write-Host ""
Write-Host "--> Instalando dependências do projeto (requirements.txt + requirements-dev.txt)..." -ForegroundColor Yellow
conda run -n $ENV_NAME pip install -r requirements.txt -r requirements-dev.txt

# -----------------------------------------------------------------------------
# 6. Verificar instalação
# -----------------------------------------------------------------------------
Write-Host ""
Write-Host "--> Verificando ambiente..." -ForegroundColor Yellow

conda run -n $ENV_NAME python -c @"
import pymetis
cut, parts = pymetis.part_graph(2, adjacency=[[1,2],[0,2],[0,1]])
print('pymetis funcional -- particoes:', parts)
print('Backend METIS (C) disponivel: OK')

import networkx, numpy, scipy, matplotlib, pandas, yaml, tqdm, pytest, ruff
print('Todas as dependencias do projeto: OK')
"@

# -----------------------------------------------------------------------------
# 7. Instruções finais
# -----------------------------------------------------------------------------
Write-Host ""
Write-Host "=============================================================" -ForegroundColor Green
Write-Host " Ambiente pronto!" -ForegroundColor Green
Write-Host "=============================================================" -ForegroundColor Green
Write-Host ""
Write-Host " Para ativar no terminal:" -ForegroundColor Yellow
Write-Host "   conda activate $ENV_NAME" -ForegroundColor White
Write-Host ""
Write-Host " Para configurar o VS Code:" -ForegroundColor Yellow
Write-Host "   Ctrl+Shift+P -> Python: Select Interpreter" -ForegroundColor White
Write-Host "   Escolha: ...\miniconda3\envs\$ENV_NAME\python.exe" -ForegroundColor White
Write-Host ""
Write-Host " Para rodar os testes:" -ForegroundColor Yellow
Write-Host "   conda activate $ENV_NAME" -ForegroundColor White
Write-Host "   pytest" -ForegroundColor White
Write-Host ""
