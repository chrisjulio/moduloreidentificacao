# Regras de projeto — Experimentos e outputs

> Aplica-se a `experiments/**/*` e `src/**/*.py`.

## Outputs vêm de logs

Gráficos e tabelas finais (em `results/plots/` e `results/tables/`) são
**regenerados** a partir de logs estruturados em `experiments/logs/`. Nunca
produzidos por execução interativa não rastreável.

Fluxo padrão:

```
config YAML  →  run experiment  →  write structured log  →  parse log  →  write table/plot
```

Cada etapa é um comando reproduzível. Notebooks Jupyter, se usados, ficam
fora deste fluxo e fora do repositório (`.ipynb_checkpoints/` já está no
`.gitignore`).

## Configuração por experimento

Cada experimento tem seu próprio YAML em `experiments/configs/`. Não rodar
diretamente com `config_example.yml` — esse arquivo é referência, não config
executável.

Convenção de nome: `experiments/configs/<descricao_curta>.yml`. Exemplos:

- `he2009_facebook_baseline.yml`
- `he2009_enron_secondary.yml`
- `he2009_facebook_k_sweep.yml`

## Mínimo de execuções

Cada configuração `(k, dataset, ataque)` roda no mínimo **3 sementes**
independentes, para barras de erro. Configurações com menos de 3 sementes
não entram em gráficos finais — produzem apenas resultados exploratórios
de bancada.

## Não comitar

- `data/raw/*` e `data/processed/*` (já em `.gitignore`).
- `experiments/logs/*` (já em `.gitignore`).
- `results/tables/*` e `results/plots/*` (já em `.gitignore`).

Versionar **apenas** os YAMLs de configuração em `experiments/configs/` e os
scripts que regeneram os outputs.
