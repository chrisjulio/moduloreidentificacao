# WORKFLOW.md — Protocolo de orquestração entre interfaces

> Manual de operação **humano**, não do agente. Documenta qual interação acontece
> em qual ferramenta, para evitar duplicação de esforço e perda de rastreabilidade.
> Versionado no repositório porque é parte integrante do método de trabalho deste
> projeto.

---

## Cinco interfaces

| # | Interface | Papel primário |
|---|---|---|
| 1 | **GitHub** | Centralizador. Estado canônico do código e da documentação. Tudo que importa termina aqui. |
| 2 | **VSCode** | Intervenção direta. Edição manual, leitura de código, revisão de PRs antes de merge. |
| 3 | **Claude Code** | Geração e controle de código. Implementação de issues; abertura de PRs; execução local de testes e lint. |
| 4 | **Claude Projects** (este chat) | Deliberação estratégica e metodológica; planejamento operacional; revisão de decisões; produção de documentação não trivial. |
| 5 | **Comet / Perplexity** | Espace acadêmico. Bibliografia, busca de papers, ajustes acadêmicos, verificação de referências. |
| 6 | **ChatGPT** | Catch-all. Qualquer interação não coberta pelas anteriores. |

---

## Roteamento por tipo de tarefa

| Tarefa | Interface primária | Saída esperada |
|---|---|---|
| Decidir mudança de escopo, revisar plano operacional | Claude Projects | Atualização documental que sobe ao GitHub |
| Implementar uma issue | Claude Code | PR aberto no GitHub |
| Revisar PR antes do merge | VSCode (ou GitHub web) | Merge (humano) ou comentários no PR |
| Editar código pontualmente (typo, ajuste rápido) | VSCode | Commit direto na branch ativa |
| Buscar referência bibliográfica, conferir citação | Comet/Perplexity | Texto/citação que entra em `docs/` ou no artigo |
| Discussão metodológica longa, deliberação | Claude Projects | Documento consolidado ou seção do README atualizada |
| Tirar dúvida pontual sobre Python/biblioteca | ChatGPT ou Claude Code | Resposta aplicada, sem registro no repo |
| Atualizar `docs/algorithm_notes.md` durante leitura do paper | Claude Code (após leitura humana) ou VSCode | Commit em branch `docs/algorithm-notes-*` |
| Bootstrap inicial do projeto (CI, templates, scripts) | Claude Projects → Claude Code | Pacote gerado aqui, aplicado no repo |

---

## Sentido único do fluxo: tudo termina no GitHub

```
[Deliberação no Projects]  →  [Consolidação documental]  →  [Push para GitHub]
                                                                    ↓
                                                          [Claude Code lê do repo]
                                                                    ↓
                                                          [Implementação em PR]
                                                                    ↓
                                                       [Revisão humana no VSCode]
                                                                    ↓
                                                                  [Merge]
```

**Não há atalho lateral.** Decisão tomada em conversa não-registrada que não chega
ao GitHub não existe operacionalmente. Se uma decisão importante surgiu no
ChatGPT ou no Comet, ela vira commit na documentação **aqui** antes de virar
premissa de execução.

---

## Anti-padrões a evitar

- Implementar código direto no chat (Projects ou ChatGPT) em vez de abrir
  issue + delegar ao Claude Code. Perde rastreabilidade.
- Decisão estratégica tomada dentro de uma sessão do Claude Code. O Code
  executa; deliberação acontece no Projects e desce via documentação.
- Revisar PR no Claude Code. Revisão é humana, no VSCode (ou na interface web
  do GitHub).
- Manter referências bibliográficas só na cabeça ou em sessões do Comet.
  Citações que importam vão para `docs/` ou para o artigo decisório.
- Pular abertura de issue para tarefas "pequenas demais". Atomicidade existe
  justamente para que tarefas pequenas sejam visíveis e auditáveis.

---

## Quando há sobreposição

Algumas tarefas cabem em mais de uma interface. Regra prática:

- **Edição rápida (1-2 linhas):** VSCode. Não vale a fricção de abrir issue/PR
  via Claude Code para um typo.
- **Edição estrutural ou multi-arquivo:** Claude Code via issue.
- **Documentação curta (uma seção, uma justificativa):** VSCode ou Projects,
  conforme o esforço cognitivo envolvido.
- **Documentação longa (capítulo, nota técnica, revisão):** Projects, depois
  commit.

A pergunta de teste: *isso vai me poupar tempo se eu repetir daqui a duas
semanas?* Se sim, vai para o GitHub via PR. Se não, edição rápida no VSCode
basta.

---

## Calibração

Este documento descreve o protocolo em 16/05/2026. Não é imutável. Se durante
a execução uma rotina diferente mostrar-se melhor, **atualize aqui antes de
adotar** — caso contrário, o protocolo vira ficção e a orquestração degrada.
