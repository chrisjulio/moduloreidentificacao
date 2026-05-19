# WORKFLOW.md — Protocolo de orquestração entre interfaces

> Manual de operação **humano**, não do agente. Documenta qual interação acontece
> em qual ferramenta, para evitar duplicação de esforço e perda de rastreabilidade.
> Versionado no repositório porque é parte integrante do método de trabalho deste
> projeto.
>
> **v2 — 16/05/2026.** Primeira calibração após uso prático; adiciona seção
> "Verificação de propagação" e dois anti-padrões surgidos durante o bootstrap
> inicial das issues.

---

## Cinco interfaces

| # | Interface | Papel primário |
|---|---|---|
| 1 | **GitHub** | Centralizador. Estado canônico do código e da documentação. Tudo que importa termina aqui. |
| 2 | **VSCode** | Intervenção direta. Edição manual, leitura de código, revisão de PRs antes de merge, substituição de arquivos gerados em outras interfaces. |
| 3 | **Claude Code** | Geração e controle de código. Implementação de issues; abertura de PRs; execução local de testes e lint. |
| 4 | **Claude Projects** | Deliberação estratégica e metodológica; planejamento operacional; revisão de decisões; produção de documentação não trivial; geração de scripts/artefatos para serem aplicados ao repositório. |
| 5 | **Comet / Perplexity** | Espaço acadêmico. Bibliografia, busca de papers, ajustes acadêmicos, verificação de referências. |
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
| Bootstrap inicial do projeto (CI, templates, scripts) | Claude Projects → Claude Code/VSCode | Pacote gerado aqui, aplicado no repo |
| Aplicar artefato gerado no Projects ao repositório | VSCode (cópia manual, GitHub web) | Commit + verificação de propagação (ver seção abaixo) |

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

## Verificação de propagação

Quando um artefato nasce no Projects (script, documento, arquivo de configuração)
e desce para o repositório, **a transição entre interfaces é o ponto frágil do
fluxo**. O editor pode mostrar um buffer em memória que difere do que está no
disco; o disco pode diferir do que o Git considera estado canônico; o Git local
pode diferir do `origin/main`. Cada divergência silenciosa custa tempo de
diagnóstico depois.

Antes de delegar uma tarefa que dependa do artefato propagado, confirmar três
coisas, nessa ordem:

1. **O Git reconhece a mudança?** `git status` deve mostrar o arquivo como
   modificado (ou já comitado, se foi via web). Se está "working tree clean" e
   você esperava ver mudança, o arquivo no disco é idêntico ao último commit —
   provável que a substituição ainda não tenha acontecido, ou ocorreu em outro
   caminho.
2. **O conteúdo bate com o esperado?** Para arquivos de texto:
   `(Get-Content file).Count` retorna número de linhas físicas;
   `(Get-Item file).Length` retorna bytes. Comparar com o esperado. Para
   scripts gerados aqui, eu informo as duas métricas; se não baterem, o arquivo
   ainda é o velho.
3. **Para scripts executáveis (`.ps1`, `.py`)**, rodar com um caso pequeno antes
   de delegar tarefa real. Erros de encoding, parsing ou ambiente afloram
   imediatamente e baratos de corrigir.

Nada disso é paranoia: foi exatamente o que faltou na primeira tentativa de
substituir o `bootstrap_issues.ps1`, gerando vinte minutos de diagnóstico
recorrendo a hash e contagem de linhas para descobrir que o arquivo no disco
ainda era o velho enquanto o VSCode mostrava o novo (buffer não salvo, ou
arquivo baixado em outro diretório).

---

## Anti-padrões a evitar

- **Implementar código direto no chat** (Projects ou ChatGPT) em vez de abrir
  issue + delegar ao Claude Code. Perde rastreabilidade.
- **Decisão estratégica tomada dentro de uma sessão do Claude Code.** O Code
  executa; deliberação acontece no Projects e desce via documentação.
- **Revisar PR no Claude Code.** Revisão é humana, no VSCode (ou na interface
  web do GitHub).
- **Manter referências bibliográficas só na cabeça ou em sessões do Comet.**
  Citações que importam vão para `docs/` ou para o artigo decisório.
- **Pular abertura de issue para tarefas "pequenas demais".** Atomicidade existe
  justamente para que tarefas pequenas sejam visíveis e auditáveis.
- **Assumir que um arquivo foi substituído sem verificar identidade.** O editor
  pode estar mostrando um buffer não salvo, ou apontando para outro arquivo, ou
  refletindo o estado do remoto via integração Git em vez do disco. `git status`,
  contagem de linhas e hash são a única fonte confiável.
- **Rodar um script gerado em outra interface sem teste sanitário.** Encoding
  (BOM UTF-8 ausente, line endings mistos) e quoting (especialmente em
  PowerShell passando argumentos para executáveis externos como `gh` CLI)
  causam falhas silenciosas ou erros que parecem o mesmo bug recorrente quando
  na verdade são uma cadeia diferente. Antes de delegar volume, rodar uma vez
  com um caso mínimo.

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

Este documento descreve o protocolo em prática. Não é imutável. Se durante a
execução uma rotina diferente mostrar-se melhor, **atualize aqui antes de
adotar** — caso contrário, o protocolo vira ficção e a orquestração degrada.

| Versão | Data       | Mudanças principais |
|--------|------------|---------------------|
| v1     | 15/05/2026 | Documento inicial.  |
| v2     | 16/05/2026 | Adicionado: seção "Verificação de propagação"; dois anti-padrões (assumir substituição sem verificar; rodar script gerado sem teste sanitário); linha de roteamento para aplicação de artefatos. Motivação: armadilhas surgidas no bootstrap das issues. |
