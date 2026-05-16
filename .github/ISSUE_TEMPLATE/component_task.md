---
name: Tarefa de componente
about: Implementação de um módulo ou componente fechado — geralmente um arquivo `.py` completo com seus testes e documentação inline.
title: ""
labels: ["component"]
---

## Objetivo

<!-- O que este componente faz; sua razão de existir no pipeline. -->

## Interface pública

<!--
Funções/classes que outros módulos vão importar. Especificar assinaturas:

```python
def degree_attack(
    G_orig: nx.Graph,
    G_anon: nx.Graph,
    target: int,
    tolerance: int = 0,
) -> bool: ...
```
-->

## Dependências

<!-- Outras issues ou componentes que devem estar prontos antes. -->

## Definição de pronto

- [ ] Componente implementado conforme a interface acima.
- [ ] Testes unitários cobrem caso típico, caso vazio, casos-limite.
- [ ] Docstrings claras (Google ou NumPy style).
- [ ] `ruff check` e `pytest` limpos.
- [ ] CI verde no PR.

## Considerações

<!-- Decisões de design, trade-offs, limitações conhecidas. -->

## Branch sugerida

<!-- ex.: `attack/degree` -->
