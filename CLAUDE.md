# CLAUDE.md — Ponto de entrada para sessões de Claude Code

> Este arquivo é carregado automaticamente pelo Claude Code no início de cada sessão
> neste repositório. Mantém o agente orientado sem reintroduzão manual de contexto.
>
> Fonte de verdade canônica do escopo: [README.md](README.md).
> Detalhamento algorítmico: [docs/algorithm_notes.md](docs/algorithm_notes.md).
> Definições de métricas: [docs/metrics_definitions.md](docs/metrics_definitions.md).
> Validação de k-anonimato (resultados consolidados): [docs/validacao_k_anonimato.md](docs/validacao_k_anonimato.md).
> Protocolo humano de orquestração entre interfaces: [WORKFLOW.md](WORKFLOW.md).
> Regras escopadas a partes do repositório: [.claude/rules/](.claude/rules/).
> Limitações metodológicas: [docs/limitations.md](docs/limitations.md).
> Entregáveis consolidados: [docs/entregaveis.md](docs/entregaveis.md).

---

## Início de sessão obrigatório

Ao abrir qualquer sessão nova neste repositório:

```
leia docs/progress.md e continue de onde paramos
```

O arquivo `docs/progress.md` é a fonte de verdade do estado de progresso
corrente — último passo concluído, próximo passo planejado, bloqueios ativos
e decisões pendentes. Ele deve ser atualizado ao final de cada sessão produtiva.

---

## Verificação de PRs antes de implementar

Antes de iniciar a implementação de qualquer issue, verifique o estado real
dos PRs listados em `Bloqueios ativos` no `progress.md`.

**Passo 1 — Verificação via `gh` CLI (preferencial):**

```bash
gh pr view <número> --json state,mergedAt
```

Só prossiga se todos os bloqueios retornarem `"state": "MERGED"`
ou se `Bloqueios ativos` já estiver vazio.

**Passo 2 — Fallback via `git log` (se `gh` não disponível):**

```bash
git fetch origin
git log --oneline origin/main | head -20
```

Confirme que os commits dos PRs aparecem em `origin/main`.

**Passo 3 — Fallback humano (se nenhum dos anteriores funcionar):**

Pergunte ao humano antes de continuar. Não aja sobre estado não verificado.

> **Regra:** Se `Bloqueios ativos` listar PRs pendentes e você não conseguir
> confirmar que foram mergeados, **pare e pergunte** — não assuma, não ignore.

---

## Em uma linha

Pipeline `anonimização → ataque → métrica` sobre redes sociais reais, produzindo
curvas privacidade-vs-utilidade. Instrumento de validação empírica para tese de
doutorado (PPGInf/UFPR) — não propõe mecanismo de privacidade novo.

---

## Fase atual

| Período | Semana | Foco | Status |
|---|---|---|---|
| 15-22/05/2026 | 1 | Setup; leitura de He et al. (2009); loader Facebook Ego-Nets | ✅ Concluída |
| 22-29/05/2026 | 2 | Implementação He et al.; **validação obrigatória de k-anonimato** | ✅ Concluída |
| 29/05-05/06 | 3 | Ataques (grau → subgrafos); experimentos | ✅ Concluída |
| 05-12/06 | 4 | Gráficos, tabelas, documentação técnica | ✅ Concluída |
| 12-14/06 | 5 | Polimento e entrega | 🔄 Em andamento |

**Marco não-negociável: 29/05/2026.** Cumprido antecipadamente em 21/05/2026. k-anonimato
empíricamente atingido em todas as configurações do Mínimo (k ∈ {2, 5, 10, 20}).

**Estado atual (S5):** issues #27 (reprodutibilidade end-to-end) e #28 (README final
+ revisão global da documentação). Ver `docs/progress.md` para estado detalhado.

---

## Regras de escopo

A linha entre Mínimo e Desejável é firme.

- **Mínimo (obrigatório):** He et al. (2009) + Facebook Ego-Nets + k ∈ {2,5,10,20}
  + ataques por grau e subgrafos + 4 métricas + ≥3 sementes + gráfico com barras
  de erro + README operacional. **✅ Totalmente implementado.**
- **Desejável (perseguir se houver folga):** Email-Enron + ataque por entropia.
- **Aspiracional (não perseguir em detrimento do Mínimo):** Nettleton & Salas (2016).

Qualquer tarefa que ponha o Mínimo em risco deve ser interrompida e sinalizada
na própria issue antes de prosseguir.

---

## Convenções de código

- **Linguagem:** Python 3.11+. NetworkX como padrão; igraph/graph-tool só com
  justificativa.
- **Estilo:** ruff (configuração em [pyproject.toml](pyproject.toml)). Antes de
  abrir PR: `ruff check .` e `ruff format .` limpos.
- **Tipos:** type hints em assinaturas de funções públicas; estilo PEP 8.
- **Idioma:** identificadores, docstrings, comentários e mensagens de commit em
  **inglês**. Issues, documentação em `/docs/` e arquivos `.md` na raiz em
  **português**.
- **Sementes:** sempre lidas do YAML de configuração — **nunca hardcoded** no
  código de produção. Ver [.claude/rules/seeds.md](.claude/rules/seeds.md).
- **Configuração:** um YAML por experimento em `experiments/configs/`. Modelo:
  [config_example.yml](config_example.yml).
- **Reprodutibilidade:** mínimo 3 sementes por configuração `(k, dataset, ataque)`;
  outputs gerados de logs estruturados, não de execução interativa.
- **Dados brutos:** baixados por script versionado em `src/loaders/`,
  **nunca commitados**. Já protegidos no `.gitignore`.

---

## Estrutura de módulos

```
src/loaders/         # carregadores de dataset (Facebook Ego-Nets, Enron)
src/anonymization/   # He et al. (2009); placeholder Nettleton & Salas (2016)
src/attacks/         # degree_attack, subgraph_attack, (entropy_attack aspiracional)
src/metrics/         # reidentification_rate, equiv_group_size, ks_test, clustering_var
tests/               # estrutura espelha src/
```

Cada módulo é independentemente testável. Não acoplar carregadores a
anonimizadores; passar grafos NetworkX como interface entre módulos.

---

## Workflow de PR (obrigatório)

Toda alteração de código entra via Pull Request — **nunca direto em `main`**.
Para cada issue:

1. **Branch nomeada por categoria/escopo:** `loader/facebook-ego`,
   `anonymization/he2009-partition`, `attack/degree`, `metric/ks-test`,
   `docs/algorithm-notes-s1`, `setup/ci`. Uma issue, uma branch.
2. **Commits pequenos e atômicos** em inglês, no imperativo
   (`add facebook ego loader`, `validate k-anonymity for k=5`).
3. **CI obrigatório:** ruff + pytest rodam automaticamente em todo PR. PRs com
   CI vermelho não são revisados.
4. **Descrição do PR** referencia a issue (`Closes #N`), descreve o que mudou,
   e — quando relevante — anexa output do experimento ou da verificação de
   sanidade que justifica o merge.
5. **Revisão humana:** PR aguarda revisão no VSCode antes do merge.
   Claude Code **não** faz merge.
6. **Issue fechada via PR**, não manualmente.

---

## Convenção de commits

- **Ferramenta correta:** escreva a mensagem e commite pela ferramenta
  **PowerShell**, nunca pela ferramenta **Bash**. Nesta máquina (Windows) a
  ferramenta Bash executa o Git Bash, um shell separado; sintaxe PowerShell
  (here-string `@'...'@`, `Set-Content`, `$env:`) enviada a ela falha com
  `command not found`/`syntax error`. Um hook `PreToolUse`
  (`.claude/hooks/guard_bash_powershell.py`) bloqueia esse erro, mas a regra
  vale por si. Use a ferramenta Bash só para sintaxe POSIX legítima.
- Ao gravar o arquivo de mensagem, evite o BOM que `Set-Content -Encoding utf8`
  injeta no assunto do commit: use
  `[System.IO.File]::WriteAllText($path, $msg, (New-Object System.Text.UTF8Encoding $false))`.
- Nunca passe a mensagem de commit inline (`git commit -m "..."` ou
  here-string `@'...'@`). O parser de comandos tem limite de ~965 bytes
  e mensagens longas falham com "command too long for parsing".
- Em vez disso, sempre escreva a mensagem em um arquivo temporário e
  use `git commit -F <arquivo>`.
- Mantenha QUALQUER comando individual abaixo de 900 bytes. Se a
  escrita do arquivo de mensagem ultrapassar isso, divida em um
  `Set-Content` inicial seguido de um ou mais `Add-Content`.
- Use `$env:TEMP\\commit_msg.txt` como caminho do arquivo e remova-o
  após o commit.
- Revise a mensagem antes de commitar: sem blocos de bullets
  duplicados.

---

## Inspeção de arquivos e busca de conteúdo

Para ler trechos de arquivos ou buscar padrões no código, **prefira as
ferramentas dedicadas `Read` e `Grep`** a one-liners de shell (PowerShell
ou Python embutido via `python -c`). Motivos:

- One-liners complexos para inspecionar arquivos (ex.: `python -c "..."`
  dentro do PowerShell, escrevendo em arquivo temporário e relendo) disparam
  prompts de permissão e, em sessão desacompanhada, **bloqueiam a execução
  indefinidamente** — foi a causa de um travamento de ~23h numa sessão da
  auditoria #74 (29-30/05/2026): 11 min de trabalho seguidos de 23,7h parados
  num prompt de permissão de um one-liner PowerShell.
- `Grep` (ripgrep) é mais rápido, integra com a UI de permissões e dispensa
  arquivos intermediários. Use `glob`/`type` para filtrar e `-A`/`-B`/`-C`
  para contexto.
- `Read` com `offset`/`limit` lê faixas específicas de um arquivo sem montar
  comandos frágeis.

Reserve o shell para o que ele de fato faz: rodar `pytest`, `git`, `gh`,
`ruff`. Não o use como substituto de leitura ou busca de conteúdo.

---

## Validação obrigatória de k-anonimato

Ao implementar qualquer anonimizador, o verificador
`validate_k_anonymity(G_anon, k) -> bool` deve ser implementado de forma
**independente** do anonimizador — não reutilizar código interno do algoritmo.
Aplicado sobre o grafo de saída, não sobre estruturas internas. Resultado em
log estruturado, reproduzível via semente.

Detalhamento e critério de aprovação do marco 29/05:
[.claude/rules/anonymization.md](.claude/rules/anonymization.md).

---

## Registro de bugs

Toda correção de bug identificada durante o desenvolvimento deve ser
documentada em dois arquivos canônicos em `bugs/`:

| Arquivo | O que registra |
|---|---|
| [`bugs/execution.md`](bugs/execution.md) | Registro técnico de execução: sintoma no CI, arquivo(s) alterado(s), diff, saída dos testes pós-fix, lint |
| [`bugs/explanation.md`](bugs/explanation.md) | Explicação em alto nível: causa raiz, por que o bug existia, decisão de onde corrigir, lição extraída |

### Protocolo ao corrigir um bug

1. **Diagnóstico** — identificar causa raiz antes de alterar código.
2. **Fix** — aplicar a correção mínima necessária; confirmar com testes.
3. **Atualizar `bugs/execution.md`** — adicionar nova seção `---` com:
   - Data, commit, branch, teste que falhou, runners afetados.
   - Arquivo(s) alterado(s) com diff e contagem de linhas.
   - Saída dos testes pós-fix (nome do teste + `PASSED`/`FAILED` + totais).
   - Resultado do lint.
4. **Atualizar `bugs/explanation.md`** — adicionar nova seção `---` com:
   - O que o bug causava (impacto observável).
   - Por que acontecia (mecanismo interno).
   - Como foi corrigido (raciocínio da solução).
   - Por que o fix foi feito onde foi (trade-off de localização).
   - Impacto em produção.
   - Lição extraída (padrão a evitar).
5. **Manter referência cruzada** — cada arquivo aponta para o outro no cabeçalho.
6. **Cada bug é uma seção** nos arquivos, separada por `---`, em ordem cronológica.

> Os arquivos `bugs/execution.md` e `bugs/explanation.md` são acumulativos —
> cada novo bug adiciona uma seção; **nunca sobrescrever** registros anteriores.

---

## Comandos frequentes

```bash
# Setup inicial (Linux/macOS; no Windows usar .venv\Scripts\Activate.ps1)
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt

# Lint e formatação
ruff check .
ruff format .

# Testes
pytest
pytest tests/loaders -v        # módulo específico
pytest -k "k_anonymity"        # por padrão de nome

# Download de dataset (uma vez, após implementado)
python -m src.loaders.download

# Executar experimento
python -m experiments.run --config experiments/configs/<nome>.yml

# Gerar gráficos
python -m src.visualization.privacy_utility --logs experiments/logs/<dir>

# Gerar tabelas CSV
python -m src.visualization.tables --logs experiments/logs/<dir> --out results/tables --dataset facebook
```

---

## Sincronização com o projeto Claude.ai

O projeto Claude.ai
("Desenvolvimento de módulo de reidentificação de dados anonimizados") é o
espacio de deliberação estratégica e metodológica. Decisões consolidadas lá
descum para este repositório atualizando, nesta ordem:

1. `README.md` (escopo canônico).
2. Este arquivo (`CLAUDE.md`) — fase atual, convenções, escopo.
3. `docs/algorithm_notes.md` quando a decisão for algorítmica.

O agente parte sempre do estado dos arquivos versionados — não de memória de
sessão anterior. Manter estes documentos atualizados elimina a necessidade de
reintroduzir contexto a cada sessão.

---

## O que este repositório não faz

- Não decide o mecanismo de privacidade do framework integrado da tese.
- Não implementa o gerador (EpiCNet + Nettleton).
- Não estende para contexto temporal (Fase 2 da tese).
- Não pretende contribuição original em privacidade — é instrumento de medição.
