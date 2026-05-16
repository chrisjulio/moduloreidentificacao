## Issue relacionada

Closes #

## O que muda

<!-- Descrição concisa do que este PR implementa ou altera. Uma a três frases. -->

## Como verificar

<!--
Comandos ou passos para reproduzir a verificação local. Exemplos:

- `pytest tests/anonymization -v`
- `ruff check src/anonymization`
- `python -m experiments.run --config experiments/configs/example.yml`
-->

## Sanidade (quando aplicável)

<!--
Para PRs que tocam anonimização, ataques ou métricas: anexar output de
validação, log estruturado, ou referência ao experimento que justifica o merge.

Para anonimização em particular: anexar resultado de `validate_k_anonymity`
para o(s) k(s) afetado(s).
-->

## Checklist

- [ ] CI verde (`ruff` + `pytest`).
- [ ] Branch nomeada por categoria/escopo (`<categoria>/<escopo-curto>`).
- [ ] Commits atômicos, em inglês, no imperativo.
- [ ] Issue será fechada automaticamente pelo merge (via `Closes #N`).
- [ ] Documentação atualizada se a alteração mudar interface pública ou convenção.
- [ ] Se tocou anonimização: `validate_k_anonymity` permanece passando.
- [ ] Se tocou pipeline experimental: outputs reproduzíveis a partir do YAML.
