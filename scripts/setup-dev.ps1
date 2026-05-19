# scripts/setup-dev.ps1
# Prepara o ambiente local de desenvolvimento do projeto.

# 1. Confirmar que está na raiz do repositório
Get-ChildItem

# Deve aparecer: README.md, CLAUDE.md, requirements.txt, src\, tests\, etc.

# 2. Remover ambiente virtual anterior, se existir
if (Test-Path .venv) {
    Remove-Item -Recurse -Force .venv
}

# 3. Criar novo ambiente virtual
python -m venv .venv

# 4. Ativar ambiente virtual
.\.venv\Scripts\Activate.ps1

# Se aparecer erro de execution policy, rode antes:
# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# 5. Atualizar pip
python -m pip install --upgrade pip

# 6. Instalar dependências
python -m pip install -r requirements.txt -r requirements-dev.txt

# 7. Validar ambiente
python -c "import networkx; print(networkx.__version__)"
ruff check .
ruff format --check .
pytest --collect-only