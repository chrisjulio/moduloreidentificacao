# Notas de Implementação — He et al. (2009)

> Registro passo a passo do algoritmo de anonimização estrutural.
> Preencher progressivamente durante a Semana 1 (15–22/05/2026) à medida que
> a leitura do artigo avança. Cada seção deve ser atualizada antes de iniciar
> a implementação correspondente.

## Referência

He, X. et al. (2009). Preserving privacy in social networks: A structure-aware
approach. *Proceedings of the IEEE/WIC/ACM International Joint Conference on
Web Intelligence and Intelligent Agent Technology (WI-IAT)*.

---

## 1. Conceito central: k-anonimato estrutural

*(a preencher)*

Questões a responder na leitura:
- O que constitui um "grupo de equivalência" no contexto de grafos?
- Qual a propriedade estrutural que torna dois nós indistinguíveis?
- k-anonimato aqui refere-se a grau, vizinhança, ou outra assinatura estrutural?

---

## 2. Algoritmo principal

*(a preencher)*

Estrutura esperada (esqueleto a confirmar com o artigo):

```
Entrada:  grafo G = (V, E), parâmetro k
Saída:    grafo anonimizado G' = (V, E') com k-anonimato garantido

Passos:
  1. [descrever]
  2. [descrever]
  ...
```

Complexidade declarada no artigo: *(a preencher)*

---

## 3. Operações de modificação do grafo

*(a preencher)*

Questões a responder:
- O algoritmo adiciona arestas, remove arestas, ou ambos?
- Há operações sobre nós (inserção, fusão)?
- As operações são determinísticas ou têm componente aleatório (→ impacto nas sementes)?

---

## 4. Critério de parada e garantia de k-anonimato

*(a preencher)*

Questões a responder:
- Como o algoritmo verifica que k-anonimato foi atingido?
- O que acontece se o grafo não puder ser anonimizado para o k pedido?
- Como implementar o verificador independente (`validate_k_anonymity`)?

---

## 5. Parâmetros e configuração

*(a preencher)*

Mapear para as chaves do YAML de configuração ([config_example.yml](../config_example.yml)):

| Parâmetro do artigo | Chave YAML | Valor(es) usados |
|---|---|---|
| k | `anonymization.k_values` | [2, 5, 10, 20] |
| *(outros)* | | |

---

## 6. Casos especiais e limitações documentadas no artigo

*(a preencher)*

Exemplos de casos que podem exigir tratamento especial:
- Grafos desconectados
- Nós isolados
- Grafos muito densos

---

## 7. Decisões de implementação (registrar conforme surgem)

| Data | Decisão | Justificativa |
|---|---|---|
| | | |

---

## 8. Validação: o que "empiricamente atingido" significa

Para o marco de 29/05/2026, a validação de k-anonimato deve ser:

- [ ] Verificador implementado **independentemente** do anonimizador
      (não reutilizar código interno do algoritmo).
- [ ] Verificador aplicado sobre o grafo de saída G', não sobre estruturas
      internas do algoritmo.
- [ ] Resultado registrado em log estruturado, reproduzível via semente.
- [ ] Testado em ao menos uma configuração: k=5, uma ego-rede do Facebook.

Critério de aprovação: verificador retorna `True` para o k configurado em
100% das execuções (3 sementes, mesma configuração).
