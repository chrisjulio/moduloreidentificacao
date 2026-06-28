# Regras de projeto — Sementes aleatórias

> Aplica-se a `src/**/*.py`, `experiments/**/*.py` e `tests/**/*.py`.

## Princípio

Sementes nunca são hardcoded no código de produção. Vêm do arquivo YAML de
configuração da execução.

## Padrão obrigatório

```python
# certo:
def some_random_op(graph: nx.Graph, seed: int) -> nx.Graph:
    rng = np.random.default_rng(seed)
    ...

# errado:
def some_random_op(graph: nx.Graph) -> nx.Graph:
    rng = np.random.default_rng(42)   # NÃO
    ...
```

## No nível de experimento

```python
import yaml

config = yaml.safe_load(open(config_path))
for seed in config["seeds"]:
    result = run_experiment(graph, seed=seed, ...)
```

Cada `seed` produz uma execução independente. Múltiplas sementes geram as
barras de erro nos gráficos finais.

## Em testes

Sementes podem ser fixadas em testes (ex.: `seed=0`), pois testes precisam
ser determinísticos. Isso é exceção controlada, não regra. Justificar no
docstring do teste por que aquela semente foi escolhida quando relevante
para o comportamento testado.
