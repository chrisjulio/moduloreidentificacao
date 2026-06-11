# Replicação do experimento via terminal

Scripts independentes de IDE (VS Code, Cursor, etc.) para reproduzir, a quente
e pela linha de comando, o pipeline `anonimização → ataque → métrica` de
He et al. (2009). Atende à [issue #184](https://github.com/chrisjulio/moduloreidentificacao/issues/184).

Todos os scripts são apenas invólucros (*wrappers*) finos sobre um único driver
Python — [`replicate.py`](replicate.py) — que por sua vez chama os pontos de
entrada já existentes no projeto (`experiments.run`, `src.loaders.download`,
`src.visualization.*`). Não há reimplementação de lógica científica: o caminho
de replicação e o caminho manual documentado no [README.md](../../README.md) §3
produzem exatamente os mesmos resultados.

> **Observação metodológica.** Estes scripts operam **apenas** sobre os datasets
> acadêmicos já integrados ao projeto (Facebook Ego-Nets e Email-Enron do SNAP —
> públicos, anonimizados na origem). **Não há nenhuma rotina de identificação
> individual.** O objetivo é exclusivamente a replicação controlada das etapas
> agregadas de cálculo e geração de dados experimentais, preservando o
> enquadramento acadêmico e metodológico do módulo.

> ⚠️ **Status de teste dos scripts.** Os wrappers **Bash** (`.sh`) foram
> executados e validados em Linux (Python 3.12) — pipeline completo de ponta a
> ponta. Os wrappers **PowerShell** (`.ps1`) **NÃO foram testados em ambiente
> Windows/PowerShell**: foram preparados por **espelhamento direto** da lógica
> dos wrappers Bash (mesma chamada ao driver Python `replicate.py`) e
> **requerem validação em uma máquina Windows/PowerShell antes de uso em
> demonstração ao vivo**. O driver `replicate.py` em si é multiplataforma e foi
> testado; o risco residual está restrito à camada fina de invólucro PowerShell
> (resolução de caminho, escolha do interpretador, *splatting* de argumentos).

---

## 1. Pré-requisitos

| Item | Requisito |
|---|---|
| Python | **3.11+** (testado em 3.12). Verificado pelo `check-env`. |
| Dependências | `requirements.txt` + `requirements-dev.txt` (NetworkX, NumPy, SciPy, Matplotlib, pandas, PyYAML, tqdm). |
| Ambiente | Virtualenv (`venv`) ou Conda recomendado, **não obrigatório**. |
| `pymetis` *(opcional)* | Backend METIS de particionamento. Sem ele, o pipeline cai automaticamente no fallback Kernighan-Lin (decisão **D-04**) — válido, porém produz partições diferentes. Ver §1.1 e [`windows_pymetis.md`](../../windows_pymetis.md). |

**Específico por sistema operacional:**

- **Windows / PowerShell** — pode ser necessário liberar a execução de scripts
  na sessão atual:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
  ```
- **Linux/macOS / Bash** — dê permissão de execução uma vez:
  ```bash
  chmod +x scripts/replication/*.sh
  ```

### 1.1 `pymetis` em Windows — Conda/Anaconda fortemente recomendado

O `pymetis` é o backend **primário** de particionamento (fiel a He et al.,
decisão **D-04**), mas é uma extensão nativa que liga contra o METIS em C.
Implicações práticas por sistema operacional:

- **Windows.** `pip install pymetis` normalmente **falha**: exige compilar
  código C nativo (toolchain MSVC / Build Tools) e o pacote não fornece *wheels*
  binárias confiáveis para Windows. Por isso, em Windows é **fortemente
  recomendado** (na prática, o caminho seguro) usar **Conda/Anaconda/Miniconda**
  com o canal **conda-forge**, que entrega um binário pré-compilado — evitando a
  compilação nativa. O projeto já provê esse caminho:
  ```powershell
  # a partir da raiz do repositório, no PowerShell
  .\scripts\setup_conda_windows.ps1   # cria o ambiente Conda a partir de environment.yml (inclui pymetis)
  ```
  Detalhes e configuração do interpretador: [`windows_pymetis.md`](../../windows_pymetis.md).
- **Linux/macOS.** `pip install -e ".[partition-c]"` compila do fonte (exige
  toolchain C); Conda/conda-forge também funciona e é igualmente recomendado.

**Comportamento esperado quando `pymetis` está ausente (fallback):** o projeto
**não falha** — recai automaticamente no backend Kernighan-Lin do NetworkX,
emitindo um `UserWarning` transitório (decisão **D-04**). Esse fallback é um
comportamento **real e implementado** no código (não inventado): cada execução
grava o backend efetivamente usado no campo `partition_backend` do log JSONL
(`"pymetis"` ou `"networkx-kl"`), e o relatório do runner avisa explicitamente
quando o fallback está em uso. O `check-env` destes scripts também reporta qual
backend está ativo. O fallback KL produz **partições diferentes** das do METIS,
portanto afeta a reprodução exata dos números — é válido para demonstração, mas
para fidelidade total a He et al. instale o `pymetis`. Para **proibir** o
fallback (abortar se `pymetis` faltar), defina
`anonymization.allow_kl_fallback: false` no YAML do experimento. Ver
[`docs/limitations.md`](../../docs/limitations.md) §2.2 e
[`docs/decision_log.md`](../../docs/decision_log.md) (D-04).

---

## 2. Preparação do ambiente

A partir da **raiz do repositório**:

```bash
# Linux/macOS
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt
```

```powershell
# Windows / PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt
```

Verifique se o ambiente está pronto (ver §3/§4 — comando `check_environment`).

---

## 3. Execução via PowerShell

Os scripts podem ser chamados de qualquer diretório: cada um resolve a raiz do
repositório a partir da própria localização.

```powershell
# 1. Verificar ambiente (Python, dependências, diretórios, backend de partição)
./scripts/replication/check_environment.ps1

# 2. Preparar dados (baixa Facebook Ego-Nets se ausente; cria diretórios de saída)
./scripts/replication/prepare_data.ps1 --dataset facebook

# 3a. Pipeline COMPLETO de ponta a ponta (env → dados → experimento → resultados)
./scripts/replication/run_experiment.ps1 `
    --config experiments/configs/he2009_facebook_baseline.yml --dataset facebook

# 3b. (alternativa) Somente a etapa de experimento, sem env/dados/resultados
./scripts/replication/run_experiment.ps1 --only-run `
    --config experiments/configs/he2009_facebook_baseline.yml

# 4. Gerar gráficos e tabelas a partir dos logs de uma execução concluída
./scripts/replication/generate_results.ps1 `
    --logs experiments/logs/he2009_facebook_baseline --dataset facebook
```

---

## 4. Execução via Bash (Linux/macOS)

```bash
chmod +x scripts/replication/*.sh   # uma única vez

# 1. Verificar ambiente
./scripts/replication/check_environment.sh

# 2. Preparar dados
./scripts/replication/prepare_data.sh --dataset facebook

# 3a. Pipeline COMPLETO de ponta a ponta
./scripts/replication/run_experiment.sh \
    --config experiments/configs/he2009_facebook_baseline.yml --dataset facebook

# 3b. (alternativa) Somente a etapa de experimento
./scripts/replication/run_experiment.sh --only-run \
    --config experiments/configs/he2009_facebook_baseline.yml

# 4. Gerar gráficos e tabelas
./scripts/replication/generate_results.sh \
    --logs experiments/logs/he2009_facebook_baseline --dataset facebook
```

### Invocação direta do driver (qualquer SO)

Os wrappers apenas chamam o driver Python; ele pode ser usado diretamente:

```bash
python scripts/replication/replicate.py check-env
python scripts/replication/replicate.py all \
    --config experiments/configs/he2009_facebook_baseline.yml --dataset facebook
python scripts/replication/replicate.py --help   # ajuda de cada subcomando
```

---

## 5. Ordem de execução e etapas

O fluxo segue o pipeline canônico do projeto ([README.md](../../README.md) §3.3):

```
check-env  →  prepare-data  →  run  →  results
```

| Etapa | Subcomando | Wrapper | Faz |
|---|---|---|---|
| 1 | `check-env` | `check_environment` | Valida Python, pacotes e diretórios; reporta o backend de partição. |
| 2 | `prepare-data` | `prepare_data` | Garante o dataset de entrada (baixa se ausente) e cria os diretórios de saída. |
| 3 | `run` | `run_experiment --only-run` | Executa um YAML de experimento via `experiments.run`. |
| 4 | `results` | `generate_results` | Regenera gráficos e tabelas a partir dos logs JSONL. |
| — | `all` | `run_experiment` | Encadeia 1 → 2 → 3 → 4. |

A **execução completa** (`all` / `run_experiment`) e a **execução por etapas**
(subcomandos individuais) são ambas suportadas — a segunda facilita depuração e
demonstração parcial a avaliadores.

---

## 6. Parâmetros

| Parâmetro | Etapas | Default | Descrição |
|---|---|---|---|
| `--config <yaml>` | `run`, `all` | — (obrigatório) | Caminho do YAML de experimento, relativo à raiz. |
| `--dataset <nome>` | `prepare-data`, `results`, `all` | `facebook` | `facebook` ou `enron`. Em `results`, rotula a saída. |
| `--skip-download` | `prepare-data`, `all` | desligado | Falha em vez de baixar quando o dataset está ausente. |
| `--logs <dir>` | `results`, `all` | derivado do nome do config | Diretório de logs de uma execução concluída. |
| `--only-run` | `run_experiment` (wrapper) | — | Roda apenas a etapa de experimento. |

Os YAMLs disponíveis estão em [`experiments/configs/`](../../experiments/configs/).
Exemplos:
`he2009_facebook_baseline.yml` (Mínimo completo: k ∈ {2,5,10,20}, grau + subgrafo,
3 sementes) e `he2009_enron_secondary.yml` (Desejável). As **sementes nunca são
passadas por linha de comando** — vêm sempre do YAML
([`.claude/rules/seeds.md`](../../.claude/rules/seeds.md)).

---

## 7. Entradas esperadas

- **Facebook Ego-Nets** em `data/raw/facebook/<ego_id>/` (baixado por
  `python -m src.loaders.download`; o `prepare-data` faz isso automaticamente).
- **Email-Enron** em `data/raw/enron/` (baixado por
  `python -m src.loaders.download_enron`).
- Dados brutos **não são versionados** (já protegidos no `.gitignore`); são
  obtidos por script versionado. Use **apenas** os datasets acadêmicos,
  anonimizados e controlados já integrados ao projeto.

---

## 8. Saídas, logs e artefatos

Todos os caminhos são relativos à raiz e previsíveis:

| Tipo | Local | Produzido por |
|---|---|---|
| Logs estruturados do experimento (JSONL) | `experiments/logs/<nome_do_experimento>/<nome>.jsonl` | etapa `run` |
| Resumo do experimento | `experiments/logs/<nome_do_experimento>/summary.json` | etapa `run` |
| **Log de auditoria da replicação** | `experiments/logs/replication/replication_audit.jsonl` | todas as etapas |
| Gráficos privacidade-utilidade | `results/plots/` (PDF + PNG) | etapa `results` |
| Tabelas por (dataset, ataque) | `results/tables/*.csv` | etapa `results` |

O log de auditoria registra, em uma linha JSON por etapa: timestamp (UTC),
etapa, status (`OK`/`FAILED`), versão do Python, raiz do repositório e
parâmetros relevantes (config, dataset, diretórios) — suficiente para
demonstrar o que foi executado. Cada etapa também emite logs textuais no
terminal com data/hora e nível (`INFO`/`ERROR`).

> `experiments/logs/*` e `results/{plots,tables}/*` **não são versionados**
> (ver [`.claude/rules/experiments.md`](../../.claude/rules/experiments.md)).

---

## 9. Verificação da execução

A execução terminou com sucesso quando:

1. Cada script retorna **código de saída 0** (`echo $LASTEXITCODE` no PowerShell;
   `echo $?` no Bash).
2. Após `run`, existem `experiments/logs/<nome>/<nome>.jsonl` e `summary.json`,
   e o relatório no terminal imprime `Status: [PASSED]`.
3. Após `results`, há arquivos novos em `results/plots/` e `results/tables/`.
4. Confira `experiments/logs/replication/replication_audit.jsonl`: a última
   entrada de cada etapa deve ter `"status": "OK"`.
5. Para conferência científica, compare as tabelas em `results/tables/` com os
   valores de referência em `docs/results_baseline.md`
   (procedimento em `docs/reproducibility.md` §6).

---

## 10. Solução de problemas

| Sintoma | Causa provável | Ação |
|---|---|---|
| `Missing packages: ...` | Dependências não instaladas | `pip install -r requirements.txt -r requirements-dev.txt` (com o venv ativo). |
| `Python 3.11+ required` | Interpretador antigo | Instale/ative Python 3.11+ ou um venv apropriado. |
| `Dataset 'facebook' not found ... --skip-download` | Dados ausentes e download desativado | Rode sem `--skip-download` ou `python -m src.loaders.download`. |
| `Config not found` | Caminho errado do YAML | Use caminho relativo à raiz, ex.: `experiments/configs/he2009_facebook_baseline.yml`. |
| `No .jsonl logs under ...` | `results` antes de `run` | Execute a etapa `run` primeiro. |
| `Permission denied` (Bash) | `.sh` sem bit de execução | `chmod +x scripts/replication/*.sh`. |
| `cannot be loaded because running scripts is disabled` (PowerShell) | Política de execução | `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`. |
| `no python interpreter found` | Python fora do PATH | Ative o venv ou instale o Python e reabra o terminal. |
| Aviso `networkx-kl fallback` | `pymetis` ausente | Resultado válido, porém é aproximação KL (D-04). Em Windows, instale `pymetis` via Conda/conda-forge (§1.1); em Linux/macOS via Conda ou `pip install -e ".[partition-c]"`. |
| Comportamento inesperado dos `.ps1` | Wrappers PowerShell **não testados em Windows** (ver nota no topo) | Valide em uma máquina Windows/PowerShell antes de uma demonstração; como alternativa, invoque o driver diretamente: `python scripts/replication/replicate.py ...`. |

---

## 11. Exemplo completo (Bash, do zero)

```bash
cd /caminho/para/moduloreidentificacao
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
chmod +x scripts/replication/*.sh

./scripts/replication/run_experiment.sh \
    --config experiments/configs/he2009_facebook_baseline.yml --dataset facebook

# Saídas esperadas ao final:
#   experiments/logs/he2009_facebook_baseline/he2009_facebook_baseline.jsonl
#   experiments/logs/he2009_facebook_baseline/summary.json   -> "any_failure": false
#   results/plots/*.pdf  results/plots/*.png
#   results/tables/*.csv
#   experiments/logs/replication/replication_audit.jsonl     -> status "OK" por etapa
```

Tempo estimado do baseline em hardware típico: ~6–12 min (dominado pelo ataque
por subgrafo).
