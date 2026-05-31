# Ajustes Windows — ambiente Conda e backend `pymetis`

> Esta documentação é relevante apenas para quem utiliza Windows e quer o backend
> METIS (`pymetis`) ativo.

---

## Por que `pymetis` não vem no `.venv` padrão

O `requirements.txt` **não** lista `pymetis` (ele não instala via pip de forma
confiável; ver nota no próprio `requirements.txt`). Logo, o ambiente do §3.2 do
README — em **qualquer** sistema operacional, inclusive Linux/macOS — usa o
**fallback Kernighan-Lin** por padrão, com apenas um `UserWarning` transitório.

Para obter o backend `pymetis` (motor primário, fiel a He et al., D-04) há dois
caminhos:

- **Conda (recomendado, todos os SOs):** `environment.yml` /
  `scripts/setup_conda_windows.ps1` — instala o binário do conda-forge.
- **pip no Linux/macOS (compila do fonte):**
  `pip install -e ".[partition-c]"` — exige toolchain C e **falha no
  Windows/MSVC**.

### Como confirmar qual backend está ativo

Cada execução grava `partition_backend` no JSONL (`"pymetis"` ou
`"networkx-kl"`) e o runner avisa no relatório quando o fallback está em uso.

Para **proibir** o fallback (abortar se `pymetis` não estiver disponível),
defina `anonymization.allow_kl_fallback: false` no YAML do experimento. Ver
[`docs/limitations.md`](docs/limitations.md) §2.2.

---

## 1. Por que `.vscode/` não está versionado

O diretório `.vscode/` está listado no `.gitignore` do projeto. Cada
desenvolvedor mantém sua própria configuração local — isso evita que caminhos
absolutos específicos de uma máquina entrem no repositório.

---

## 2. Criar o ambiente Conda

Execute uma única vez no PowerShell, **a partir da raiz do repositório**:

```powershell
.\scripts\setup_conda_windows.ps1
```

O script cria o ambiente `moduloreidentificacao` a partir de `environment.yml`,
que já inclui `pymetis` via conda-forge.

---

## 3. Criar `.vscode/settings.json` localmente

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

## 4. Criar `.vscode/tasks.json` localmente (opcional)

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

## 5. Verificar que `pymetis` está ativo

Com o ambiente Conda ativo e o interpretador configurado, abra um terminal
integrado (`Ctrl+\``) e execute:

```python
python -c "import pymetis; print('pymetis OK — backend METIS-C ativo')"
```

Se retornar `pymetis OK`, o backend METIS-C está operacional. Caso contrário,
o fallback Kernighan-Lin será usado automaticamente (comportamento padrão e
documentado em D-04).

---

*Ver também: [`docs/decision_log.md`](docs/decision_log.md) (D-04) e
[`docs/limitations.md`](docs/limitations.md) §2.2.*
