# Pendência diferida — asserções do teste de auditoria `dsweep` (rótulo↔cor↔dado)

> **Status:** DIFERIDO — não aplicado. Registrado durante o congelamento de
> código para aplicação **pós-revisão** com os orientadores.
>
> **Natureza:** isto **não** é um bug de produção corrigido. Por isso vive num
> arquivo próprio e **não** entra em [`execution.md`](execution.md) /
> [`explanation.md`](explanation.md), que são acumulativos e reservados a fixes
> já aplicados. Quando a correção for feita, mover o registro para aqueles dois
> arquivos seguindo o protocolo do `CLAUDE.md`.

---

## Identificação

| Campo | Valor |
|---|---|
| **Data do registro** | 2026-06-13 |
| **Branch** | `main` (código congelado) |
| **Componente** | `src/visualization/privacy_utility.py` — `_plot_dsweep_facets`, `_plot_dsweep_series`, `_series_for_d` |
| **Figuras** | `results/plots/privacy_utility_dsweep_facets.{png,pdf}`, `privacy_utility_dsweep_series.{png,pdf}` |
| **Dados** | `results/tables/facebook_dsweep_degree.csv`, `facebook_dsweep_subgraph.csv` |
| **Gatilho de aplicação** | após a revisão com os orientadores (texto do relatório/artigo já sob avaliação) |

---

## Resumo

Uma auditoria da correspondência **rótulo ↔ cor ↔ dado** nas figuras de
d-sweep (grau × subgrafo por painel de `d`) confirmou que **a figura já está
correta**: a série rotulada "Ataque por grau" usa a cor de grau e a coluna
`rr_degree`; idem para subgrafo. Nenhuma inversão. **Não há swap a fazer.**

O que ficou pendente é um **teste de regressão** que travaria essa
correspondência. A proposta de asserções, como redigida, **reprova sobre dados
corretos** em três pontos. Aplicar o teste agora exigiria reformular as
asserções (mexer em arquivo versionado durante o congelamento). Decisão:
**assumir a pendência e diferir** para depois da revisão, evitando refatoração
sobre o que já está em texto e sob visão dos orientadores.

---

## Auditoria (read-only) — o que está correto hoje

1. **Cores** (`privacy_utility.py:228-231`): `_ATTACK_COLORS = {"degree":
   "#1f77b4" (azul), "subgraph": "#ff7f0e" (laranja)}`. ✅
2. **Fiação código → dado**:
   - `_plot_dsweep_facets`: `rr_degree` → cor de grau + label "Ataque por grau";
     `rr_subgraph` → cor de subgrafo + label "Ataque por subgrafo". ✅
   - `_plot_dsweep_series`: **não usa `_ATTACK_COLORS`** — cor codifica `d`, e o
     ataque é codificado por **estilo de linha/marcador** (subgrafo sólido `-`/`s`,
     grau tracejado `--`/`o`), com label via `_style_legend(ax, "Subgrafo",
     "Grau")`. Também correto, mas por mecanismo diferente.
3. **Cruzamento com os CSVs** (média das 3 sementes por `(k,d)`):

   GRAU (`facebook_dsweep_degree.csv`, coluna `reid_rate`):

   | k | d=1 | d=2 | d=5 | d=10 |
   |---|-----|-----|-----|------|
   | 2 | 0,023 | 0,016 | 0,036 | 0,031 |
   | 5 | 0,009 | 0,020 | 0,012 | 0,019 |
   | **10** | **0,285** | **0,339** | **0,219** | **0,266** |
   | 20 | 0,088 | 0,364 | 0,055 | 0,213 |

   SUBGRAFO (`facebook_dsweep_subgraph.csv`, coluna `reid_rate`):

   | k | d=1 | d=2 | d=5 | d=10 |
   |---|-----|-----|-----|------|
   | 2 | 0,145 | 0,138 | 0,211 | 0,147 |
   | 5 | 0,031 | 0,049 | 0,056 | 0,049 |
   | 10 | 0,037 | 0,043 | 0,015 | 0,013 |
   | 20 | 0,000 | 0,041 | 0,000 | 0,007 |

   A curva que **estoura em k=10** (~22–34%) é a de **grau** — exatamente a série
   azul rotulada "Ataque por grau". O subgrafo é alto em k=2 (~14–21%) e cai para
   ~0–4% em k=10/20. ✅ Os dados confirmam os rótulos.

---

## Problema diferido — asserções do teste reprovam sobre dados corretos

A proposta de teste (travar a correspondência via CSV + introspecção do código)
contém três asserções problemáticas:

1. **`argmax_k(rr_degree médio) == 10`** — válido **só** se `médio` for a média
   **sobre todos os `d` e sementes** (agregado: k=10 → 0,277 é o máximo).
   **Por-d, falha em d=2**, onde o pico é k=20 (0,364 > 0,339).

2. **`rr_subgraph médio decrescente em k para cada d até k=10`** — **falha em
   d=1**: 0,145 (k=2) → 0,031 (k=5) → 0,037 (k=10), i.e. **sobe** de k=5 para
   k=10. É ruído de semente (uma das 3 sementes dá 0,0 em k=10; as outras
   ~0,05–0,06). Agregado sobre `d` é monótono (0,160 → 0,046 → 0,027), mas
   "para cada d" é falso.

3. **Guarda de código** `rr_degree usa _ATTACK_COLORS["degree"] + "Ataque por
   grau"` — verdadeiro **só** para `_plot_dsweep_facets`. Em
   `_plot_dsweep_series` o ataque é codificado por **estilo de linha**, não por
   `_ATTACK_COLORS`; aplicar a mesma asserção à série quebra.

> Asserção robusta (pode manter sem alteração): **`rr_degree(k=2)` e
> `rr_degree(k=5)` < `rr_degree(k=10)` por ampla margem** — vale em qualquer
> granularidade e em todo `d`.

---

## Correção a aplicar (pós-revisão) — no TESTE, não na figura

A figura está correta; **não alterar cor/label/dado**. A correção é só na
especificação do teste de regressão:

1. **Asserção de pico de grau:** comparar a **média agregada sobre todos os `d`**
   (`argmax_k == 10`), ou fixar `d=1` (também dá 10). **Não** fazer argmax por-d
   sem excluir d=2.
2. **Asserção de monotonicidade do subgrafo:** usar a **média agregada sobre
   `d`**, ou afirmar monotonicidade por-d **apenas para `d ∈ {2,5,10}`**, ou
   afrouxar para "k=2 > k=10 por ampla margem" (vale em todo `d`). A
   monotonicidade estrita por-d **não é propriedade verdadeira de d=1**.
3. **Guarda de código:** asserir `_ATTACK_COLORS` **só** sobre
   `_plot_dsweep_facets`. Para `_plot_dsweep_series`, a guarda correta é
   "grau = `--`/marker `o`, e `_style_legend` mapeia tracejado → 'Grau'".
4. **Manter** a asserção robusta (margem k=2,k=5 ≪ k=10).

Após aplicar, **regenerar** `privacy_utility_dsweep_{facets,series}.{png,pdf}`
pelos comandos registrados em `docs/results_dsweep.md` (§ reprodutibilidade,
linhas ~299–305) e registrar o fix em `execution.md` / `explanation.md`.

---

## Por que diferir (decisão registrada)

O relatório técnico e o artigo já citam essas figuras e descrevem as tendências
(grau estoura em k=10; subgrafo decai) e estão sob revisão dos orientadores.
Reformular asserções e regenerar artefatos agora é refatoração sobre material
fora das mãos do autor. A correspondência **está correta** na figura — a
pendência é puramente de cobertura de teste. Diferir mantém o congelamento sem
risco de regressão visual. **Prioridade: baixa. Impacto em produção: nenhum**
(figura correta; ausência de teste de regressão é a única lacuna).
