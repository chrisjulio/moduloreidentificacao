# Explicação — Bug do loop infinito com k=0

> **Registro de execução (o que foi alterado):** [execution.md](execution.md)

---

## O que o bug causava

O pipeline de anonimização travava para sempre quando chamado com `k=0`.
No CI, o job inteiro ficava suspenso após a fase de coleta de testes e era
encerrado por timeout, sem produzir nenhum resultado — nem pass, nem fail,
para nenhum dos 308 testes coletados.

---

## Por que o loop não terminava

O algoritmo de agrupamento de He et al. (2009) organiza as Local Structures
em grupos de tamanho `k`. A implementação usa um `while` cuja condição de
parada é:

```
ainda existem LSs disponíveis suficientes para formar pelo menos um grupo
```

Formalmente: `while len(available) >= k`.

O invariante implícito é: *a cada iteração, `k` elementos são removidos de
`available`*. Se `k=0`, o grupo formado é sempre vazio — nenhum elemento
sai de `available` — e a condição `len(available) >= 0` é verdadeira para
qualquer conjunto, incluindo o conjunto vazio. O loop não converge.

Diferente de um crash (que o `except Exception` capturia), um loop infinito
silencia completamente: nenhuma exceção sobe, a thread simplesmente consome
CPU indefinidamente.

---

## Por que o teste existia mas não protegia

O teste `test_invalid_k_zero_serialised_as_error` estava **correto** em sua
intenção: verificar que `run_one(k=0)` não levanta exceção e devolve um dict.
O problema é que o teste pressupunha que `k=0` geraria uma `ValueError`
capturável pelo `except Exception` do runner. Sem a guard clause, o algoritmo
nunca chegava a levantar nada — ficava preso antes disso.

---

## Como foi corrigido

Uma validação foi adicionada **no início** de `_group_isomorphic`, antes de
qualquer inicialização de estado ou entrada em loops:

```python
if k < 1:
    raise ValueError(f"k must be >= 1, got {k!r}")
```

Esse `ValueError` segue o caminho normal de erros do pipeline:

```
_group_isomorphic  →  ValueError
    ↓ (propagado)
run_one (bloco try)
    ↓ (capturado por except Exception)
result["error"] = {"type": "ValueError", "message": ..., "traceback": ...}
    ↓
return result   # dict válido
```

O teste verifica apenas `assert isinstance(result, dict)` — condição agora
satisfeita, pois `run_one` retorna normalmente com o erro serializado.

---

## Por que a correção foi feita em `_group_isomorphic` e não em `run_one`

Havia duas opções:

| Local | Prós | Contras |
|---|---|---|
| `run_one` (antes do `try`) | Isola o fix no runner; não toca algoritmo | Não protege chamadas diretas a `_group_isomorphic` em testes ou notebooks |
| `_group_isomorphic` (**escolhido**) | Defesa na borda correta; protege qualquer chamador | Requer editar o módulo de algoritmo |

`_group_isomorphic` é a função que recebe `k` e entra no loop. É o lugar
correto para validar o contrato do parâmetro. O runner não deveria precisar
conhecer restrições internas do algoritmo.

---

## Impacto em produção

Nulo. `k=0` nunca aparece em configurações reais do experimento
(`k ∈ {2, 5, 10, 20}` conforme `CLAUDE.md`). O bug só era atingível via
teste de erro handling ou por YAML mal formado. A correção adiciona proteção
defensiva sem custo em execuções normais.

---

## Lição

> **Loops com invariante implícito de drenagem precisam de pré-condição
> explícita no parâmetro de controle.**

Qualquer função com `while len(collection) >= k` onde `k` vem de fora deve
validar `k >= 1` antes de iniciar. A condição de parada não é autoevidente
quando `k` pode ser zero.
