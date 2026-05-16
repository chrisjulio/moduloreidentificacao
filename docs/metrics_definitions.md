# Definições Operacionais das Métricas

> Definições precisas das métricas de privacidade e utilidade usadas no pipeline.

## Métricas de Privacidade

- **Taxa de reidentificação por ataque**: proporção de nós-alvo corretamente identificados pelo ataque.
- **Tamanho médio dos grupos de equivalência**: média do número de nós por grupo após anonimização.

## Métricas de Utilidade

- **KS-test (estatística D)**: teste de Kolmogorov-Smirnov sobre a distribuição de grau (original vs. anonimizado).
- **Variação relativa do clustering**: variação relativa do coeficiente de clustering médio (original vs. anonimizado).

## Parâmetro principal

`k ∈ {2, 5, 10, 20}`
