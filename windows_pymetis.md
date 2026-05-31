# Configuração do Windows com pymetis (backend METIS)

> Esta seção é relevante apenas para quem utiliza **Windows** e quer o backend
> METIS (`pymetis`) ativo. Em Linux/macOS, o `.venv` padrão já inclui `pymetis`
> via pip; as instruções do README §3.2 são suficientes.

---

## Por que `.vscode/` não está versionado

O diretório `.vscode/` está listado no `.gitignore` do projeto. Cada
desenvolvedor mantém sua própria configuração local — isso evita que caminhos
absolutos específicos de uma máquina entrem no repositório.

---

## Pré-requisito: criar o ambiente Conda

Antes de configurar o VS Code, o ambiente Conda precisa existir. Execute uma
única vez no PowerShell:

```powershell
# A partir da raiz do repositório
.\scripts\setup_conda_windows.ps1
```

O script cria o ambiente `moduloreidentificacao` a partir de `environment.yml`,
que já inclui `pymetis` via conda-forge.

---

## Criar `.vscode/settings.json` localmente

Crie o arquivo `.vscode/settings.json` na raiz do repositório com o conteúdo
abaixo, **ajustando o caminho do seu usuário Windows**:

```json
{
  "python.defaultInterpreterPath": "C:\\Users\\<seu-usuario>\\AppData\\Local\\miniconda3\\envs\\moduloreidentificacao\\python.exe",

  "terminal.integrated.defaultProfile.windows": "PowerShell (Conda)",
  "terminal.integrated.profiles.windows": {
    "PowerShell (Conda)": {
      "source": "PowerShell",
      "args": [
        "-NoExit",
        "-Command",
        "conda activate moduloreidentificacao"
      ]
    }
  },

  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"],
  "python.testing.unittestEnabled": false
}
```

> Substitua `<seu-usuario>` pelo seu nome de usuário Windows. Para descobrir o
> caminho exato do interpretador, execute no PowerShell (com o ambiente ativo):
> ```powershell
> conda activate moduloreidentificacao
> python -c "import sys; print(sys.executable)"
> ```

---

## Criar `.vscode/tasks.json` localmente (opcional)

Para que o VS Code execute `scripts\activate_env.ps1` automaticamente ao abrir
a pasta do projeto, crie `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Verificar ambiente (pymetis)",
      "type": "shell",
      "command": ". '${workspaceFolder}\\scripts\\activate_env.ps1'",
      "options": {
        "shell": {
          "executable": "powershell.exe",
          "args": ["-NoProfile", "-ExecutionPolicy", "RemoteSigned", "-Command"]
        }
      },
      "presentation": {
        "reveal": "always",
        "panel": "shared",
        "showReuseMessage": false
      },
      "runOptions": {
        "runOn": "folderOpen"
      },
      "problemMatcher": []
    }
  ]
}
```

Na primeira abertura, o VS Code perguntará *"Allow automatic tasks to run when
opening this folder?"* — clique em **Allow**.

---

## Verificar que `pymetis` está ativo

Com o ambiente Conda ativo e o interpretador configurado, abra um terminal
integrado (`Ctrl+\``) e execute:

```python
python -c "import pymetis; print('pymetis OK — backend METIS-C ativo')"
```

Se retornar `pymetis OK`, o backend METIS-C está operacional. Caso contrário,
o fallback Kernighan-Lin será usado automaticamente (comportamento padrão e
documentado em D-04).
