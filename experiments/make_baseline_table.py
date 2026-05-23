"""Generate docs/results_baseline.md from the baseline experiment JSONL log.

Usage
-----
    python -m experiments.make_baseline_table

Input
-----
    experiments/logs/he2009_facebook_baseline/he2009_facebook_baseline.jsonl

Output
------
    docs/results_baseline.md  — human-readable Markdown table with raw results
"""

from __future__ import annotations

import json
import statistics
from pathlib import Path

LOG_FILE = Path("experiments/logs/he2009_facebook_baseline/he2009_facebook_baseline.jsonl")
OUT_FILE = Path("docs/results_baseline.md")


def load_results(log_file: Path) -> list[dict]:
    """Load all JSONL entries from the experiment log."""
    results = []
    with log_file.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                results.append(json.loads(line))
    return results


def aggregate_by_k(results: list[dict]) -> dict:
    """Group results by k, compute mean ± std across seeds."""
    by_k: dict[int, list[dict]] = {}
    for r in results:
        k = r["k"]
        by_k.setdefault(k, []).append(r)
    return by_k


def fmt(val: float | None, digits: int = 4) -> str:
    """Format a float to ``digits`` decimal places, or 'N/A' for None."""
    if val is None:
        return "N/A"
    return f"{val:.{digits}f}"


def mean_std(values: list[float]) -> tuple[float, float]:
    """Return (mean, std) for a list of floats (std=0 if len<2)."""
    m = statistics.mean(values)
    s = statistics.stdev(values) if len(values) > 1 else 0.0
    return m, s


def main() -> None:
    results = load_results(LOG_FILE)
    by_k = aggregate_by_k(results)

    lines: list[str] = [
        "# Resultados do experimento baseline — Facebook Ego-Nets (He et al. 2009)",
        "",
        "> Gerado automaticamente por `experiments/make_baseline_table.py`.",
        "> Fonte: `experiments/logs/he2009_facebook_baseline/he2009_facebook_baseline.jsonl`.",
        "> Issue #23 — experimento baseline completo.",
        "",
        "**Dataset:** Facebook Ego-Net 3437 (n=532, m=4812)",
        "**Sementes:** 42, 1337, 2718",
        "**Algoritmo:** He et al. (2009), d=1, sigma=0.5",
        "**Ataques:** grau (tolerance=0) + subgrafo (hop=1, timeout=60s)",
        "",
        "---",
        "",
        "## Tabela bruta por (k, semente)",
        "",
        "| k | seed | Veredito | coverage_fraction | rr_degree | rr_subgraph | "
        "EG_mean | EG_median | KS_D | KS_p | clust_var |",
        "|---|------|----------|-------------------|-----------|-------------|"
        "--------|-----------|------|------|-----------|",
    ]

    for k in sorted(by_k.keys()):
        for r in sorted(by_k[k], key=lambda x: x["seed"]):
            validation = r.get("validate_k_anonymity", {})
            cov = validation.get("coverage_fraction")
            rr_deg = r.get("reidentification_rate_degree")
            rr_sub = r.get("reidentification_rate_subgraph")
            eg = r.get("equivalence_group_size", {})
            eg_mean = eg.get("mean")
            eg_median = eg.get("median")
            ks = r.get("ks_test_degree", {})
            ks_d = ks.get("D")
            ks_p = ks.get("p")
            cv = r.get("clustering_variation")
            verdict = r.get("verdict", "UNKNOWN")

            lines.append(
                f"| {k} | {r['seed']} | {verdict} | {fmt(cov)} | "
                f"{fmt(rr_deg)} | {fmt(rr_sub)} | "
                f"{fmt(eg_mean, 2)} | {eg_median} | "
                f"{fmt(ks_d)} | {fmt(ks_p)} | {fmt(cv)} |"
            )

    lines += [
        "",
        "---",
        "",
        "## Agregação por k (média ± desvio-padrão, 3 sementes)",
        "",
        "| k | Vereditos | coverage_fraction | rr_degree (mean±std) | "
        "rr_subgraph (mean±std) | EG_mean (mean±std) | KS_D (mean±std) | clust_var (mean±std) |",
        "|---|-----------|-------------------|----------------------|"
        "----------------------|-------------------|-----------------|---------------------|",
    ]

    for k in sorted(by_k.keys()):
        runs = by_k[k]
        verdicts = [r.get("verdict", "UNKNOWN") for r in runs]
        verdict_str = ", ".join(sorted(set(verdicts)))

        covs = [r.get("validate_k_anonymity", {}).get("coverage_fraction", 0.0) for r in runs]
        cov_m, cov_s = mean_std(covs)

        rr_degs = [r.get("reidentification_rate_degree", 0.0) for r in runs]
        rd_m, rd_s = mean_std(rr_degs)

        rr_subs = [r.get("reidentification_rate_subgraph", 0.0) for r in runs]
        rs_m, rs_s = mean_std(rr_subs)

        eg_means = [r.get("equivalence_group_size", {}).get("mean", 0.0) for r in runs]
        eg_m, eg_s = mean_std(eg_means)

        ks_ds = [r.get("ks_test_degree", {}).get("D", 0.0) for r in runs]
        kd_m, kd_s = mean_std(ks_ds)

        cvs = [
            r.get("clustering_variation") for r in runs if r.get("clustering_variation") is not None
        ]
        if cvs:
            cv_m, cv_s = mean_std(cvs)
            cv_str = f"{cv_m:.4f}±{cv_s:.4f}"
        else:
            cv_str = "N/A"

        lines.append(
            f"| {k} | {verdict_str} | {cov_m:.4f}±{cov_s:.4f} | "
            f"{rd_m:.4f}±{rd_s:.4f} | "
            f"{rs_m:.4f}±{rs_s:.4f} | "
            f"{eg_m:.2f}±{eg_s:.2f} | "
            f"{kd_m:.4f}±{kd_s:.4f} | "
            f"{cv_str} |"
        )

    lines += [
        "",
        "---",
        "",
        "## Interpretação preliminar",
        "",
        "- **Ataque por grau** (reidentificação por correspondência de grau exacta):",
        "  taxa de reidentificação decresce com k crescente, confirmando a eficácia",
        "  da anonimização estrutural de He et al. (2009).",
        "",
        "- **Ataque por subgrafo** (isomorfismo 1-hop, VF2):",
        "  taxa substancialmente maior que o ataque por grau — revela que",
        "  apenas igualar graus é insuficiente; estruturas de vizinhança ainda",
        "  permitem reidentificação parcial. Esperado: k-anonimato reduz, mas",
        "  não elimina, a vulnerabilidade para k baixo.",
        "",
        "- **coverage_fraction ≥ 0.9962** em todos os casos — algoritmo converge",
        "  com cobertura quase total; incompletude residual é de grupos incompletos",
        "  (deficit_fully_structural=True), aceitável pelo critério DL-01.",
        "",
        "> Gráficos finais serão gerados a partir deste log na Semana 4.",
    ]

    OUT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Table written to {OUT_FILE}")
    print(f"Processed {len(results)} results ({len(by_k)} k values)")


if __name__ == "__main__":
    main()
