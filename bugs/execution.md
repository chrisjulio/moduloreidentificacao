# Registro de Execução — fix: guard k<1 em `_group_isomorphic`

> **Relatório de alto nível:** [explanation.md](explanation.md)

---

## Identificação

| Campo | Valor |
|---|---|
| **Data** | 2026-05-25 |
| **Commit** | `bd34883` |
| **Branch** | `main` |
| **Teste que falhou** | `tests/experiments/test_runner.py::TestRunOneErrorHandling::test_invalid_k_zero_serialised_as_error` |
| **Runners afetados** | Python 3.11.15 (linux) · Python 3.12 (linux) |
| **Sintoma no CI** | Job travado após "collected 308 items" — timeout sem nenhum resultado |

---

## Diagnóstico

### Sintoma observado

O CI reportou a saída abaixo antes de ser morto por timeout:

```
collecting ... collected 308 items
```

Nenhuma linha de resultado foi emitida. O processo não retornou.

### Causa

`run_one(g, k=0, ...)` chama `_group_isomorphic(..., k=0, ...)`.
Dentro de `_group_within_bucket`, a condição de parada do loop principal é:

```python
while len(available) >= k:   # k=0 → condição SEMPRE True
```

Com `k=0`, cada iteração forma um grupo `best_sls[:0] == []`, que não remove
nenhum elemento de `available`. O loop não drena e a thread trava
indefinidamente. Nenhuma exceção é levantada, portanto o `except Exception`
de `run_one` nunca é alcançado.

---

## Arquivo alterado

### `src/anonymization/he2009.py`

**Função:** `_group_isomorphic` (linha ~446 antes da edição)

**Diff:**

```diff
     D-01, D-06, D-07 em docs/algorithm_notes.md §7.
     """
+    if k < 1:
+        raise ValueError(f"k must be >= 1, got {k!r}")
+
     rng = np.random.default_rng(seed)

     if not local_structures:
         return []
```

**Inserções:** +3 linhas  
**Remoções:** 0 linhas  
**Outros arquivos:** nenhum — nenhum teste foi criado ou modificado
(o teste `test_invalid_k_zero_serialised_as_error` já existia e estava correto;
o que faltava era a exceção que ele esperava capturar).

---

## Verificação pós-fix

### Teste-alvo

```
tests/experiments/test_runner.py::TestRunOneErrorHandling::test_invalid_k_zero_serialised_as_error  PASSED
tests/experiments/test_runner.py::TestRunOneErrorHandling::test_error_dict_has_required_keys        PASSED
tests/experiments/test_runner.py::TestRunOneErrorHandling::test_verdict_from_error_result_is_error  PASSED
```

### Suite completa (experiments + anonymization)

```
213 passed, 4 skipped, 0 failures  —  2.69s
```

### Lint

```
ruff check src/anonymization/he2009.py  →  All checks passed!
ruff format  (hook de pre-commit)       →  Passed
```

---

## Regressões

Nenhuma. Os 213 testes existentes passaram sem alteração.
