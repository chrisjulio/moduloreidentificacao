# Referências Bibliográficas — Módulo de Reidentificação

Esta pasta centraliza os PDFs e documentos da bibliografia do módulo.

> ⚠️ **Aviso de copyright:** os arquivos aqui armazenados podem ser privados ou
> protegidos por direitos autorais. Seu uso é restrito a leitura acadêmica
> individual e não comercial. **Não redistribuir.** Por isso o conteúdo desta
> pasta é ignorado pelo Git (ver `.gitignore`); apenas este catálogo e o
> `.gitkeep` são versionados.

## Como obter os arquivos

1. Acesse a referência pelo **DOI** ou link oficial listado no catálogo abaixo.
2. Prefira a versão de **acesso aberto** (repositório institucional / manuscrito
   aceito) quando disponível, em vez da versão do editor.
3. Se houver paywall, utilize acesso institucional (proxy da universidade /
   federação CAFe / VPN) ou solicite a cópia ao autor.
4. Salve o PDF nesta pasta usando a convenção de nomes abaixo.

## Convenção de nomes

```
AutorPrincipal_Ano_PalavraChaveDoTitulo.pdf
```

Exemplos:
- `He_2009_PrivacyPreservingStructureAware.pdf`
- `Nettleton_2016_DataDrivenAnonymizationOSN.pdf`

## Catálogo

| Arquivo | Referência | DOI / Link | Acesso |
|---|---|---|---|
| `He_2009_PrivacyPreservingStructureAware.pdf` | He, X. et al. *Preserving Privacy in Social Networks: A Structure-Aware Approach.* | _(preencher DOI/link)_ | _(aberto/proxy)_ |
| `Nettleton_2016_DataDrivenAnonymizationOSN.pdf` | Nettleton, D.F.; Salas, J. *A data driven anonymization system for information rich online social network graphs.* Expert Systems with Applications, 55, 87–105, 2016. | https://doi.org/10.1016/j.eswa.2016.02.004 — manuscrito aceito: http://hdl.handle.net/10609/150625 (CC BY-NC-ND) | aberto (O2 UOC) |
| _(adicionar demais referências conforme a revisão de literatura avança)_ | | | |

## Orientações e condições para localização e download

1. **DOI primeiro.** Sempre que houver DOI, use-o como ponto de partida — ele
   resolve para a página oficial do artigo.
2. **Prefira acesso aberto.** Para Nettleton & Salas (2016), o manuscrito aceito
   está no repositório O2 da UOC (`hdl.handle.net/10609/150625`) sob licença
   CC BY-NC-ND — download e uso permitidos com atribuição, sem alteração e sem
   fins comerciais.
3. **Paywall.** Quando o artigo só estiver disponível no site do editor
   (ex.: Elsevier/ScienceDirect), use o **acesso institucional** (proxy da
   universidade, federação CAFe ou VPN). Não armazene credenciais no repositório.
4. **Versão correta.** Registre no catálogo se o PDF é a versão do editor
   (Version of Record), o manuscrito aceito (AAM) ou um preprint, pois isso
   afeta citação e legalidade da cópia.
5. **Não comitar.** Após salvar os PDFs, confirme com `git status` que nenhum
   aparece como rastreado. Se aparecer, revise o `.gitignore`.
