# Consolidação de dados — d-sweep (issue #88)

> 📄 **O relatório final já existe:** [`docs/results_dsweep.md`](results_dsweep.md).
> Este arquivo é mantido apenas como **snapshot histórico** do estado
> intermediário (prévia de garantia de dados). Para os números canônicos,
> tabelas e figuras regeneradas do log, use o relatório final.

> ⚠️ **ESTE NÃO É O RELATÓRIO FINAL.**
>
> Este documento nasceu como **prévia de garantia de dados (data-preservation
> snapshot)**, gerado com o experimento ainda em execução, para consolidar em
> forma legível os resultados persistidos. **Atualizado em 02/06 para o estado
> final: o experimento concluiu 48/48 execuções.**
>
> Ainda assim, **não é o relatório final**. O relatório final (gráficos com
> barras de erro e tabelas canônicas) depende de ferramentas de visualização
> cientes da dimensão `d`, **ainda não implementadas** — `src/visualization/`
> foi escrito para o baseline de `d` único e ignora `d` (uma issue de extensão
> `viz/dsweep-d-aware` foi especificada para tratar disso). Será regenerado a
> partir do log estruturado conforme o fluxo de `docs/regras_experimentos.md`
> (`config → run → log → parse → table/plot`) quando essas ferramentas existirem.
> Os números abaixo são consolidação legível do log, sujeitos a reapresentação.

---

## Metadados do snapshot

| Campo | Valor |
|---|---|
| Experimento | `he2009_facebook_dsweep` |
| Issue | **#88** (desmembramento/complemento de #77; ver também #72) |
| Config | `experiments/configs/he2009_facebook_dsweep.yml` |
| Dataset | Facebook Ego-Net **3437** (LCC: n=532, m=4812, densidade≈0.034) |
| Anonimização | He et al. (2009), σ=0.5 |
| Backend de particionamento | **pymetis** (fiel a He et al., D-04) — em **todos** os runs |
| Ataques | grau (tolerância 0) + subgrafo (hop=1, timeout=120 s/nó) |
| Métrica canônica `reidentification_rate` | = ataque por **subgrafo** (subgrafo habilitado) |
| Grid | k ∈ {2,5,10,20} × d ∈ {1,2,5,10} × seeds {42,1337,2718} = **48 runs** |
| Snapshot inicial | 2026-06-01 ~15:14 (43/48) |
| **Atualizado para estado final** | 2026-06-02 — **48 de 48 (100%)** |
| Último run concluído | 2026-06-02 ~01:22 (k=20 d=10 seed=2718) |
| `summary.json` | **escrito** ao término (`partition_backends: ["pymetis"]`) |
| Vereditos | **33 SUCCESS_PARTIAL / 15 FAILURE_LOW_COVERAGE** |

### Estado de cobertura do grid

```
┌─────┬────────┬────────┬────────┬────────┐
│  k  │  d=1   │  d=2   │  d=5   │  d=10  │
├─────┼────────┼────────┼────────┼────────┤
│ 2   │ ✅✅✅ │ ✅✅✅ │ ✅✅✅ │ ✅✅✅ │
├─────┼────────┼────────┼────────┼────────┤
│ 5   │ ✅✅✅ │ ✅✅✅ │ ✅✅✅ │ ✅✅✅ │
├─────┼────────┼────────┼────────┼────────┤
│ 10  │ ✅✅✅ │ ✅✅✅ │ ✅✅✅ │ ✅✅✅ │
├─────┼────────┼────────┼────────┼────────┤
│ 20  │ ✅✅✅ │ ✅✅✅ │ ✅✅✅ │ ✅✅✅ │
└─────┴────────┴────────┴────────┴────────┘
```

**Grid completo — todas as 16 células com 3 sementes (48 runs).** Nenhuma pendência.

---

## Resultados consolidados (células com 3 sementes)

Médias sobre as 3 sementes. `reid_sub` = reidentificação por subgrafo (canônica);
`reid_deg` = reidentificação por grau; `cobertura` = fração de nós com k-anonimato
satisfeito (`validate_k_anonymity.coverage_fraction`); `EGS` = tamanho médio do
grupo de equivalência; `KS D` = estatística D do teste KS de grau; `Δclust` =
variação de clustering.

### k = 2

| d | reid_sub (média) | reid_deg (média) | cobertura | EGS | KS D | Δclust |
|---|---|---|---|---|---|---|
| 1  | 0.1454 | 0.0232 | 0.9850 | 1.99  | 0.052 | 0.053 |
| 2  | 0.1378 | 0.0257 | 0.9850 | 3.97  | 0.050 | 0.057 |
| 5  | 0.2105 | 0.0357 | 0.9887 | 9.85  | 0.031 | 0.031 |
| 10 | 0.1466 | 0.0312 | 0.9812 | 19.70 | 0.074 | 0.042 |

### k = 5

| d | reid_sub (média) | reid_deg (média) | cobertura | EGS | KS D | Δclust |
|---|---|---|---|---|---|---|
| 1  | 0.0307 | 0.0094 | 0.9399 | 4.97  | 0.275 | 0.273 |
| 2  | 0.0489 | 0.0200 | 0.9023 | 9.85  | 0.305 | 0.312 |
| 5  | 0.0558 | 0.0119 | 0.9492 | 23.13 | 0.229 | 0.210 |
| 10 | 0.0489 | 0.0187 | 0.9399 | 44.33 | 0.263 | 0.217 |

### k = 10

| d | reid_sub (média) | reid_deg (média) | cobertura | EGS | KS D | Δclust | verdito |
|---|---|---|---|---|---|---|---|
| 1  | 0.0370 | 0.2851 | 0.8647 | 9.85  | 0.823 | 0.118 | ⚠️ FAILURE_LOW_COVERAGE |
| 2  | 0.0432 | 0.3389 | 0.9023 | 19.00 | 0.776 | 0.070 | SUCCESS_PARTIAL |
| 5  | 0.0150 | 0.2193 | 0.8459 | 44.33 | 0.745 | 0.043 | ⚠️ FAILURE_LOW_COVERAGE |
| 10 | 0.0125 | 0.2656 | 0.9399 | 76.00 | 0.809 | 0.163 | SUCCESS_PARTIAL |

### k = 20

| d | reid_sub (média) | reid_deg (média) | cobertura | EGS | KS D | Δclust | verdito |
|---|---|---|---|---|---|---|---|
| 1  | 0.0000 | 0.0882 | 0.8647 | 19.00  | 0.936 | 0.470 | ⚠️ FAILURE_LOW_COVERAGE |
| 2  | 0.0413 | 0.3640 | 0.9023 | 35.47  | 0.902 | 0.476 | SUCCESS_PARTIAL |
| 5  | 0.0000 | 0.0545 | 0.7519 | 76.00  | 0.927 | 0.403 | ⚠️ FAILURE_LOW_COVERAGE |
| 10 | 0.0069 | 0.2130 | 0.7519 | 133.00 | 0.931 | 0.522 | ⚠️ FAILURE_LOW_COVERAGE |

---

## Observações preliminares (sujeitas a revisão na consolidação final)

1. **k-anonimato nunca formalmente satisfeito, mas déficit é estrutural.**
   `validate_k_anonymity.valid = false` em **todos os 48 runs**, porém
   `deficit_fully_structural = true` em todos — o déficit decorre de violadores
   estruturais (nós que não admitem grupo de tamanho ≥ k no grafo), não de falha
   do algoritmo. Comportamento esperado e documentado (D-06).

2. **Ataque por subgrafo enfraquece com k crescente.** `reid_sub` cai de ~0.15–0.21
   (k=2) para ~0.01–0.04 (k=10/20). Coerente com grupos de equivalência maiores.

3. **Ataque por grau se fortalece com k crescente** — tendência oposta. `reid_deg`
   sobe de ~0.02–0.03 (k=2) para ~0.22–0.36 (k=10/20). Note que, com k alto, o KS D
   de grau aproxima-se de ~0.8–0.95: a anonimização distorce fortemente a
   distribuição de graus, criando assinaturas de grau mais singulares.

4. **`reid_sub = 0` exato em k=20 d∈{1,5} (todas as sementes)** e em vários runs de k alto.
   Atenção na interpretação: nós cujo ataque de subgrafo atinge o **timeout de 120 s**
   contam como *não reidentificados*. Em k alto o VF2 é caro e os timeouts são
   frequentes — parte desses zeros pode refletir custo computacional, não segurança
   real. **A consolidação final deve cruzar isso com a contagem de timeouts.**

5. **`FAILURE_LOW_COVERAGE`** aparece em **15 runs** (todas as sementes de k=10 d=1,
   k=10 d=5, k=20 d=1, k=20 d=5 e k=20 d=10): cobertura abaixo do limiar. Não é crash —
   é veredito metodológico de baixa cobertura, esperado em configurações densas/extremas
   (precedente D-08/D-10: documentar em vez de ocultar). Os outros 33 runs são
   `SUCCESS_PARTIAL`.

6. **Custo do bloco k=20.** Tempo por run salta para ~3 h (vs. ~2–3 min em k=2),
   dominado pelo VF2 do ataque por subgrafo sob grupos de equivalência grandes.

---

## Integridade dos dados

- Fonte: `experiments/logs/he2009_facebook_dsweep/he2009_facebook_dsweep.jsonl`
  (gravação incremental append, uma linha por run concluído).
- **48 linhas válidas**, sem entradas com `error != null`.
- Todas com `partition_backend = "pymetis"`.
- `summary.json` **escrito** ao término (n_runs=48, `partition_backends: ["pymetis"]`,
  mapa completo de `verdicts`).

> Reiteração: **consolidação legível do log, não entrega final.** Substituir pela
> consolidação oficial (com barras de erro e tabelas/plots regenerados do log)
> quando as ferramentas de visualização cientes de `d` (`viz/dsweep-d-aware`)
> forem implementadas.
