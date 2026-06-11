"""Generate docs/results_enron.md from the Enron secondary experiment JSONL log.

Usage
-----
    python -m experiments.make_enron_table

Input
-----
    experiments/logs/he2009_enron_secondary/he2009_enron_secondary.jsonl
    experiments/logs/he2009_facebook_baseline/he2009_facebook_baseline.jsonl
        (optional — used only for the Facebook x Enron comparison table; when
        absent, the embedded baseline reference values are used instead.)

Output
------
    docs/results_enron.md  — risk x utility tables for the Email-Enron secondary
    dataset (tier [D]), plus the Facebook x Enron methodological comparison.

This mirrors ``experiments/make_baseline_table.py`` so that the two results
documents stay structurally parallel. Outputs come from structured logs, never
from interactive execution (.claude/rules/experiments.md).
"""

# ruff: noqa: RUF001
# This module emits pt-BR Markdown content; the "ambiguous" Unicode characters
# flagged by RUF001 (multiplication sign and en dash for numeric ranges) are
# intentional document typography in string literals, not code identifiers.
from __future__ import annotations

import json
import statistics
from pathlib import Path

ENRON_LOG = Path("experiments/logs/he2009_enron_secondary/he2009_enron_secondary.jsonl")
FACEBOOK_LOG = Path("experiments/logs/he2009_facebook_baseline/he2009_facebook_baseline.jsonl")
OUT_FILE = Path("docs/results_enron.md")

#: Enron LCC after OR symmetrisation (D-11), as measured by the cost probe of
#: issue #127 and recorded in decision_log.md (D-15).
ENRON_N = 33_696
ENRON_M = 180_811

#: Facebook baseline aggregated reference, used only as a fallback for the
#: comparison table when the Facebook log is not present locally.  Source of
#: truth: docs/results_baseline.md (Kernighan-Lin engine, single ego-net 3437).
_FACEBOOK_FALLBACK: dict[int, dict[str, float]] = {
    2: {"rr_degree": 0.0263, "rr_subgraph": 0.7914, "ks_d": 0.0000, "clust_var": 0.0000},
    5: {"rr_degree": 0.0081, "rr_subgraph": 0.4060, "ks_d": 0.0482, "clust_var": 0.0670},
    10: {"rr_degree": 0.0226, "rr_subgraph": 0.1397, "ks_d": 0.2356, "clust_var": 0.1575},
    20: {"rr_degree": 0.0990, "rr_subgraph": 0.0000, "ks_d": 0.6491, "clust_var": 0.0904},
}


def load_results(log_file: Path) -> list[dict]:
    """Load all JSONL entries from an experiment log."""
    results = []
    with log_file.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                results.append(json.loads(line))
    return results


def group_by_k(results: list[dict]) -> dict[int, list[dict]]:
    """Group runs by their k value."""
    by_k: dict[int, list[dict]] = {}
    for r in results:
        by_k.setdefault(r["k"], []).append(r)
    return by_k


def fmt(val: float | None, digits: int = 4) -> str:
    """Format a float to ``digits`` decimal places, or 'N/A' for None."""
    if val is None:
        return "N/A"
    return f"{val:.{digits}f}"


def thousands(n: int) -> str:
    """Format an int with '.' as thousands separator (pt-BR convention)."""
    return f"{n:,}".replace(",", ".")


def mean_std(values: list[float]) -> tuple[float, float]:
    """Return (mean, std) for a list of floats (std=0 if len<2)."""
    m = statistics.mean(values)
    s = statistics.stdev(values) if len(values) > 1 else 0.0
    return m, s


def facebook_means(by_k: dict[int, list[dict]]) -> dict[int, dict[str, float]]:
    """Aggregate the Facebook baseline log into per-k mean reference values."""
    out: dict[int, dict[str, float]] = {}
    for k, runs in by_k.items():
        out[k] = {
            "rr_degree": statistics.mean(r["reidentification_rate_degree"] for r in runs),
            "rr_subgraph": statistics.mean(r["reidentification_rate_subgraph"] for r in runs),
            "ks_d": statistics.mean(r["ks_test_degree"]["D"] for r in runs),
            "clust_var": statistics.mean(
                r["clustering_variation"] for r in runs if r.get("clustering_variation") is not None
            ),
        }
    return out


def main() -> None:
    enron = load_results(ENRON_LOG)
    by_k = group_by_k(enron)
    ks_sorted = sorted(by_k.keys())

    if FACEBOOK_LOG.exists():
        fb = facebook_means(group_by_k(load_results(FACEBOOK_LOG)))
        fb_source = "`experiments/logs/he2009_facebook_baseline/` (carregado)"
    else:
        fb = _FACEBOOK_FALLBACK
        fb_source = "`docs/results_baseline.md` (valores de referência embutidos)"

    lines: list[str] = [
        "# Resultados do experimento secundário — Email-Enron (He et al. 2009)",
        "",
        "> Gerado automaticamente por `experiments/make_enron_table.py`.",
        "> Fonte: `experiments/logs/he2009_enron_secondary/he2009_enron_secondary.jsonl`.",
        "> Issue #128 (S9-6) — comparativo Facebook × Enron + tabelas de risco × utilidade.",
        "> Parte da issue-mãe #29 (dataset secundário do tier **Desejável** `[D]`).",
        "",
        f"**Dataset:** Email-Enron (SNAP), projeção não-direcionada por **OR** (D-11); "
        f"maior componente conexa (LCC) com **n={thousands(ENRON_N)} nós, "
        f"m={thousands(ENRON_M)} arestas** (grau médio ≈ 10,7).",
        "**Sementes:** 42, 1337, 2718",
        "**Algoritmo:** He et al. (2009), d=1, sigma=0.5, s_max=4, isomorphism_mode=add_or_delete",
        "**Motor de particionamento:** pymetis (12/12 execuções) — fiel ao artigo.",
        "**Ataques:** grau (tolerance=0) + subgrafo (hop=1) — subgrafo **full** viável "
        "via bucketing de WL-hash (D-16); `subgraph_timeout_count=0` em todas as runs.",
        "",
        "---",
        "",
        "## Enquadramento metodológico — síntese",
        "",
        "> **Frase-síntese.** O Email-Enron é o dataset **secundário** (tier Desejável "
        "`[D]`) que estende o baseline **Facebook** (tier Mínimo `[M]`) para uma rede de "
        "escala e origem distintas: ~63× mais nós (33,7 k vs. 532), derivada de e-mail "
        "corporativo **direcionado** e projetada para não-direcionada por simetrização OR "
        "(D-11), contra a amizade já-simétrica de uma única ego-rede do Facebook. Ele "
        "**não introduz mecanismo novo** — reusa o mesmo pipeline "
        "`anonimização → ataque → métrica` — e serve para **aferir se o comportamento "
        "privacidade-vs-utilidade do He et al. (2009) se mantém fora da topologia de "
        "ego-rede**. A leitura conjunta deve focar **tendências** (sinal e monotonicidade), "
        "não magnitudes absolutas, que não são diretamente comparáveis (ver abaixo).",
        "",
        "Como no baseline, `d=1` afere **k-anonimato de grau**, não a propriedade "
        "*structure-aware* plena (achado B1): em `d=1` a estrutura local de cada nó "
        "reduz-se ao seu grau. O ataque por **subgrafo** (isomorfismo de vizinhança "
        "1-hop) é, portanto, o termômetro de quanto a estrutura — não anonimizada em "
        "`d=1` — ainda permite associação. Toda a terminologia segue o enquadramento de "
        "aferição (D-11): avalia-se **risco de reidentificação / vulnerabilidade "
        "agregada**, nunca identificação individual.",
        "",
        "---",
        "",
        "## Comparativo Facebook × Enron (médias por k, 3 sementes)",
        "",
        f"> Facebook: {fb_source}. Enron: log desta execução. As duas colunas de cada "
        "métrica compartilham `d=1`, `sigma=0.5` e as mesmas 3 sementes; diferem no "
        "dataset (e no motor: KL no baseline Facebook — achado A1 — vs. pymetis no Enron).",
        "",
        "| k | rr_grau FB | rr_grau Enron | rr_subgrafo FB | rr_subgrafo Enron | "
        "KS-D FB | KS-D Enron | clust_var FB | clust_var Enron |",
        "|---|-----------|--------------|----------------|-------------------|"
        "---------|------------|--------------|-----------------|",
    ]

    for k in ks_sorted:
        runs = by_k[k]
        rr_deg = statistics.mean(r["reidentification_rate_degree"] for r in runs)
        rr_sub = statistics.mean(r["reidentification_rate_subgraph"] for r in runs)
        ks_d = statistics.mean(r["ks_test_degree"]["D"] for r in runs)
        clust = statistics.mean(r["clustering_variation"] for r in runs)
        f = fb.get(k, {})
        lines.append(
            f"| {k} | {fmt(f.get('rr_degree'))} | {fmt(rr_deg)} | "
            f"{fmt(f.get('rr_subgraph'))} | {fmt(rr_sub)} | "
            f"{fmt(f.get('ks_d'))} | {fmt(ks_d)} | "
            f"{fmt(f.get('clust_var'))} | {fmt(clust)} |"
        )

    lines += [
        "",
        "### Por que as magnitudes **não** são diretamente comparáveis",
        "",
        "A comparação direta dos valores absolutos é **confundida** por três diferenças "
        "estruturais, e a tabela acima deve ser lida como contraste de **tendências**, "
        "não de níveis:",
        "",
        "1. **Escala (n).** O Facebook é uma única ego-rede pequena e densa (n=532); o "
        "Enron tem n=33.696. Numa rede pequena, muitas vizinhanças 1-hop são **únicas** → "
        "reidentificação por subgrafo alta (rr≈0,79 em k=2). Numa rede grande, vizinhanças "
        "**colidem** com muito mais frequência → taxa-base baixa (rr≈0,12 em k=2) **antes "
        "mesmo** de qualquer efeito de k. A diferença de ~6× em k=2 é majoritariamente de "
        "escala, não de proteção.",
        "2. **Densidade e origem.** O Enron vem de e-mail **direcionado** achatado por OR "
        "(D-11), o que infla conectividade de modo distinto da amizade simétrica do "
        "Facebook; grau médio e distribuição de grau diferem.",
        "3. **Motor de particionamento.** O baseline Facebook rodou em Kernighan-Lin "
        "(achado A1), o Enron em pymetis. Inócuo em `d=1` (partições triviais de 1 nó), "
        "mas é mais uma variável não-pareada entre as colunas.",
        "",
        "**Conclusão (DoD #128).** Um gráfico com as duas redes **sobrepostas nos mesmos "
        "eixos é enganoso**: a faixa de reidentificação do Facebook (0–79 %) comprimiria "
        "as curvas do Enron (0–12 %) a uma quase-reta, e o mesmo vale para KS-D "
        "(0–0,65 vs. 0–0,13). Os gráficos privacidade-utilidade são gerados **por dataset "
        "separadamente** (`results/plots/privacy_utility_enron.*`, mesmo gerador do "
        "Facebook), e a comparação é feita pela tabela acima e pelas tendências abaixo.",
        "",
        "### O que **é** comparável — tendências robustas em ambas as redes",
        "",
        "- **Subgrafo ≫ grau.** Em toda a faixa de k, o ataque por subgrafo reidentifica "
        "muito mais que o ataque por grau (Enron: ~40× em k=2). Confirma, fora da "
        "ego-rede, que **igualar grau não protege a estrutura de vizinhança** — o cerne "
        "empírico do módulo.",
        "- **Monotonicidade em k.** O `rr_subgrafo` cai de forma monótona com k em ambas "
        "(Enron: 0,124 → 0,102 → 0,079 → 0,057). k-anonimato **reduz** a vulnerabilidade "
        "estrutural mesmo em `d=1`.",
        "- **Grau já residual.** O `rr_grau` é baixíssimo no Enron (≤0,003) — uma ordem de "
        "grandeza abaixo do Facebook — coerente com a escala: assinaturas de grau isoladas "
        "quase nunca são únicas numa rede grande.",
        "- **Utilidade melhor preservada em escala.** O KS-D do Enron permanece baixo "
        "(0,04–0,13) onde o Facebook chega a 0,65: perturbar uma rede grande desloca a "
        "distribuição global de grau proporcionalmente menos. A anonimização é **menos "
        "custosa em utilidade** numa rede grande.",
        "",
        "### Painel comparativo normalizado (gráfico complementar)",
        "",
        "Como sobrepor as magnitudes brutas é enganoso (acima), o painel abaixo torna as "
        "duas redes legíveis nos **mesmos eixos** por **normalização** — é um complemento "
        "ao comparativo, não um substituto dos gráficos por dataset. Gerado por "
        "`python -m src.visualization.comparison` (dados em "
        "`docs/assets/comparison_fb_enron.csv`).",
        "",
        "![Comparativo normalizado Facebook × Enron — ataque por subgrafo]"
        "(assets/comparison_fb_enron.png)",
        "",
        "- **Painel (A) — fração da cota `1/k`** (`rr_subgrafo · k`, linha pontilhada em "
        "`1,0`). Acima de `1,0` a cota teórica `rr ≤ 1/k` é **violada** — esperado no "
        "regime `d=1`, em que o ataque inspeciona a vizinhança 1-hop **não** anonimizada "
        "(B1). **Cruzamentos pertinentes:** o Facebook fica **acima** da cota em "
        "k∈{2,5,10} (pico ~2,03 em k=5) e despenca a 0 em k=20; o Enron sobe "
        "gradualmente e **cruza** a cota só em k=20 (~1,14). As duas curvas se cruzam "
        "por volta de k≈14: abaixo disso o Facebook é proporcionalmente mais vulnerável, "
        "acima disso o Enron passa a sê-lo — efeito de **escala**, não de mecanismo.",
        "- **Painel (B) — decaimento relativo** (`rr_subgrafo(k)/rr_subgrafo(k mínimo)`), "
        "que remove o degrau de magnitude (~6× em k=2) e isola a **forma** da curva. O "
        "Facebook decai abruptamente (1,0 → 0,18 → 0,0), o Enron suavemente (1,0 → 0,63 "
        "→ 0,46): k-anonimato extingue a estrutura distinguível de uma ego-rede pequena, "
        "mas só a atenua numa rede grande — a **tendência** (decaimento monótono) é "
        "comum às duas; a **taxa** de decaimento é o que difere.",
        "",
        "### Ameaça à validade — motor de particionamento não-pareado (C2)",
        "",
        "> O comparativo cruza **motores diferentes**: o baseline Facebook `d=1` rodou em "
        "Kernighan-Lin (achado A1), o Enron em pymetis (12/12). O argumento de inocuidade "
        "em `d=1` (partições triviais de 1 nó → o desbalanceamento do KL para `ck>2`, "
        "D-04, não se manifesta) é **defensável, mas interpretativo** — esta issue **não** "
        "isola experimentalmente o efeito do motor. Registra-se como ameaça à validade "
        "interna de **baixa magnitude**; um pareamento estrito (Facebook em pymetis) fica "
        "como trabalho futuro. Ver `docs/limitations.md`.",
        "",
        "---",
        "",
        "## Tabela bruta por (k, semente)",
        "",
        "> Valores em **6 casas decimais**. A tabela agregada abaixo é a média dos valores "
        "de **precisão plena** do log (não destes valores já arredondados) seguida de "
        "arredondamento para 4 casas; por isso `média(arredondados) ≠ arredondamento(média)` "
        "pode diferir na última casa (ex.: k=10 → 0,0787; k=20 → 0,0569).",
        "",
        "| k | seed | Veredito | coverage_fraction | rr_grau | rr_subgrafo | "
        "EG_mean | EG_median | KS_D | KS_p | clust_var |",
        "|---|------|----------|-------------------|---------|-------------|"
        "--------|-----------|------|------|-----------|",
    ]

    for k in ks_sorted:
        for r in sorted(by_k[k], key=lambda x: x["seed"]):
            validation = r.get("validate_k_anonymity", {})
            cov = validation.get("coverage_fraction")
            eg = r.get("equivalence_group_size", {})
            ks = r.get("ks_test_degree", {})
            lines.append(
                f"| {k} | {r['seed']} | {r.get('verdict', 'UNKNOWN')} | {fmt(cov, 6)} | "
                f"{fmt(r.get('reidentification_rate_degree'), 6)} | "
                f"{fmt(r.get('reidentification_rate_subgraph'), 6)} | "
                f"{fmt(eg.get('mean'), 2)} | {eg.get('median')} | "
                f"{fmt(ks.get('D'), 6)} | {fmt(ks.get('p'))} | "
                f"{fmt(r.get('clustering_variation'), 6)} |"
            )

    lines += [
        "",
        "---",
        "",
        "## Agregação por k (média ± desvio-padrão, 3 sementes)",
        "",
        "| k | Vereditos | coverage_fraction | rr_grau (mean±std) | "
        "rr_subgrafo (mean±std) | EG_mean (mean±std) | KS_D (mean±std) | clust_var (mean±std) |",
        "|---|-----------|-------------------|--------------------|"
        "------------------------|--------------------|-----------------|----------------------|",
    ]

    for k in ks_sorted:
        runs = by_k[k]
        verdict_str = ", ".join(sorted({r.get("verdict", "UNKNOWN") for r in runs}))
        cov_m, cov_s = mean_std([r["validate_k_anonymity"]["coverage_fraction"] for r in runs])
        rd_m, rd_s = mean_std([r["reidentification_rate_degree"] for r in runs])
        rs_m, rs_s = mean_std([r["reidentification_rate_subgraph"] for r in runs])
        eg_m, eg_s = mean_std([r["equivalence_group_size"]["mean"] for r in runs])
        kd_m, kd_s = mean_std([r["ks_test_degree"]["D"] for r in runs])
        cv_m, cv_s = mean_std([r["clustering_variation"] for r in runs])
        lines.append(
            f"| {k} | {verdict_str} | {cov_m:.6f}±{cov_s:.6f} | "
            f"{rd_m:.4f}±{rd_s:.4f} | {rs_m:.4f}±{rs_s:.4f} | "
            f"{eg_m:.2f}±{eg_s:.2f} | {kd_m:.4f}±{kd_s:.4f} | {cv_m:.4f}±{cv_s:.4f} |"
        )

    lines += [
        "",
        "---",
        "",
        "## Interpretação",
        "",
        "- **Ataque por grau** — `rr_grau ∈ [0,0018; 0,0034]`, uma ordem de grandeza "
        "abaixo do Facebook. Numa rede de 33,7 k nós, assinaturas de grau isoladas "
        "raramente são únicas; o ataque mais fraco é quase inócuo já em k=2.",
        "",
        "- **Ataque por subgrafo** (isomorfismo 1-hop, caminho rápido por WL-hash, D-16) "
        "— `rr_subgrafo` cai monotonicamente de **0,124** (k=2) para **0,057** (k=20), "
        "~40× a taxa de grau. Em `d=1` anonimiza-se o grau, **não** a estrutura 1-hop "
        "(B1); o resíduo de ~6 % em k=20 é a vulnerabilidade estrutural que `d=1` não "
        "cobre — coerente com o baseline Facebook, onde o subgrafo também domina o grau.",
        "",
        "- **Cota `rr_subgrafo ≤ 1/k` — não vale em `d=1`.** A cota teórica esperada "
        "(`data_dictionary.md`) pressupõe k-anonimato **da estrutura que o ataque "
        "inspeciona**, i.e. `d ≥ 2`. Em `d=1` só o grau é anonimizado (B1), então a cota "
        "**pode ser violada**: ela vale em k∈{2,5,10} (0,124≤0,5; 0,102≤0,2; 0,079≤0,1) "
        "mas **é violada em k=20** (0,057 > 0,050 = 1/20). Isso é **esperado, não um "
        "bug** — é a assinatura empírica de que `d=1` afere k-anonimato de grau, não "
        "estrutural. Sob `d ≥ 2` (d-sweep) a cota volta a valer. Ver o painel (A) acima.",
        "",
        "- **coverage_fraction ≥ 0,9960** em todas as 12 runs, com "
        "`deficit_fully_structural=True` (vereditos `SUCCESS_PARTIAL`): a incompletude "
        "residual é exclusivamente de **grupos incompletos** (D-06), aceitável pelo "
        "critério DL-01 — nenhuma violação de isomorfismo/disjunção.",
        "",
        "- **Utilidade.** KS-D cresce com k (0,038 → 0,130) e a variação de clustering "
        "idem (0,017 → 0,093), mas ambas permanecem **muito abaixo** das do Facebook: "
        "anonimizar uma rede grande custa proporcionalmente menos utilidade global.",
        "",
        "- **Divergência em k alto.** No Facebook o `rr_subgrafo` colapsa a 0 em k=20 "
        "(a ego-rede inteira cabe em poucos grupos); no Enron permanece em ~0,057 — a rede "
        "grande retém estrutura local distinguível mesmo sob k=20. Reforça que as "
        "magnitudes refletem **escala**, não diferença de mecanismo.",
        "",
        "---",
        "",
        "## Reprodutibilidade",
        "",
        "```bash",
        "# 1. Execução (12 runs: k∈{2,5,10,20} × 3 sementes)",
        "python -m experiments.run --config experiments/configs/he2009_enron_secondary.yml",
        "",
        "# 2. Esta tabela (docs/results_enron.md)",
        "python -m experiments.make_enron_table",
        "",
        "# 3. Tabelas CSV (results/tables/enron_{degree,subgraph}.csv)",
        "python -m src.visualization.tables \\",
        "    --logs experiments/logs/he2009_enron_secondary \\",
        "    --out results/tables --dataset enron",
        "",
        "# 4. Gráfico privacidade-utilidade do Enron (results/plots/privacy_utility_enron.*)",
        "python -m src.visualization.privacy_utility \\",
        "    --logs experiments/logs/he2009_enron_secondary \\",
        "    --out results/plots --stem privacy_utility_enron \\",
        '    --title "Privacy vs. Utility — Email-Enron (He et al. 2009)"',
        "",
        "# 5. Painel comparativo normalizado Facebook × Enron (snapshot em docs/assets/)",
        "python -m src.visualization.comparison \\",
        "    --fb-logs experiments/logs/he2009_facebook_baseline \\",
        "    --enron-logs experiments/logs/he2009_enron_secondary \\",
        "    --out docs/assets --stem comparison_fb_enron",
        "```",
        "",
        "> Logs, tabelas CSV e plots em `results/` são **gitignored** "
        "(`.claude/rules/experiments.md`); versiona-se o YAML de config e os scripts que os "
        "regeneram. **Exceção documentada:** o snapshot comparativo em `docs/assets/` "
        "(`comparison_fb_enron.png` + `.csv`) é versionado por ser artefato auditável "
        "publicamente, e permanece regenerável pelo comando 5. As referências "
        "cruzadas: D-11 (projeção OR), D-15/D-16 (viabilidade do subgrafo), achados A1/B1; "
        "ver `docs/decision_log.md` e `docs/results_baseline.md`.",
    ]

    OUT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Table written to {OUT_FILE}")
    print(f"Processed {len(enron)} Enron runs ({len(by_k)} k values); Facebook source: {fb_source}")


if __name__ == "__main__":
    main()
