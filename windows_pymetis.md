# Ajustes Windows — ambiente Conda e backend `pymetis`

> Estas instruções são relevantes **apenas** para quem utiliza Windows e quer
> o backend METIS (`pymetis`) ativo. Em Linux/macOS, o `.venv` padrão já inclui
> `pymetis` via pip; as instruções do §3.2 do README são suficientes.

---

## Por que `pymetis` é opcional

Em Windows, `pip install pymetis` falha porque o pacote depende de extensões C
sem wheel oficial para a plataforma. A solução é instalar via conda-forge, que
distribui binários pré-compilados compatíveis.

Quando `pymetis` está ausente, o algoritmo recai automaticamente para o backend
**Kernighan-Lin** (decisão **D-04** — ver `docs/decision_log.md`). Essa escolha
**afeta a reprodução**: backends diferentes produzem partições diferentes, por
isso deve ser controlada ao comparar resultados entre máquinas.

---

## 1. Criar o ambiente Conda

Execute uma única vez no PowerShell, **a partir da raiz do repositório**:

```powershell
.\scripts\setup_conda_windows.ps1
```

O script cria o ambiente `moduloreidentificacao` a partir de `environment.yml`,
que já inclui `pymetis` via conda-forge.

---

## 2. Configurar o VS Code

O diretório `.vscode/` está listado no `.gitignore` — cada desenvolvedor mantém
sua própria configuração local para evitar que caminhos absolutos específicos de
uma máquina entrem no repositório.

### 2.1 `settings.json`

Crie `.vscode/settings.json` na raiz do repositório com o conteúdo abaixo,
**ajustando o caminho do seu usuário Windows**:

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

> Para descobrir o caminho exato do interpretador, execute no PowerShell (com o
> ambiente ativo):
> ```powershell
> conda activate moduloreidentificacao
> python -c "import sys; print(sys.executable)"
> ```

### 2.2 `tasks.json` (opcional)

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

## 3. Verificar que `pymetis` está ativo

Com o ambiente Conda ativo e o interpretador configurado, abra um terminal
integrado (`Ctrl+\``) e execute:

```python
python -c "import pymetis; print('pymetis OK — backend METIS-C ativo')"
```

Se retornar `pymetis OK`, o backend METIS-C está operacional. Caso contrário,
o fallback Kernighan-Lin será usado automaticamente (comportamento padrão,
documentado em D-04).

---

*Ver também: `docs/decision_log.md` (D-04) e `docs/reproducibility.md` §8.*
