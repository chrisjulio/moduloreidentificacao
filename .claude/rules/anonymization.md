---
paths:
  - "src/anonymization/**/*.py"
  - "tests/anonymization/**/*.py"
---

# Regras escopadas — Anonimização

## Validação obrigatória de k-anonimato

Toda anonimização produzida pelo módulo precisa ser **empiricamente validada**
antes de ser usada em experimentos.

O verificador `validate_k_anonymity(G_anon, k) -> bool` deve ser:

1. **Independente do anonimizador.** Não reutilizar código interno do algoritmo
   de He et al. (ou de qualquer outro anonimizador). O verificador é um auditor
   externo, não uma rotina interna do mesmo algoritmo. Se o anonimizador estiver
   errado de uma forma que afete a verificação, queremos que o verificador
   detecte — só consegue se for implementação separada.
2. **Aplicado sobre o grafo de saída.** Recebe `G_anon` como entrada — nunca
   estruturas intermediárias do algoritmo.
3. **Determinístico para um dado `G_anon`.** Não depende de semente; a
   anonimização depende de semente, a verificação não.
4. **Registrado em log estruturado.** Resultado vai para `experiments/logs/`
   com timestamp, hash do grafo de entrada, parâmetros, e resultado booleano.

## Critério de aprovação do marco 29/05

`validate_k_anonymity` retorna `True` em **100% das execuções** (3 sementes,
mesma configuração) para ao menos um `k ∈ {2, 5, 10, 20}` sobre uma ego-rede
do Facebook. Sugestão: começar por `k=5`.

Se o verificador retorna `False` para algum `k`, os resultados associados
àquele `k` são **inválidos** e não podem ser usados em gráficos finais.
Documentar a falha em `docs/algorithm_notes.md` (Seção 7) e abrir issue de
correção.

## Não fazer

- Não implementar o verificador como wrapper trivial sobre o anonimizador.
- Não validar k-anonimato por amostragem aleatória de nós; a verificação é
  sobre **todos** os nós.
- Não silenciar falhas: se `validate_k_anonymity` retorna `False`, o
  experimento para e a issue é reaberta.
