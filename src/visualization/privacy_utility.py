"""Privacy-utility curve generator for He et al. (2009) experiments.

Reads structured JSONL logs produced by ``experiments/run.py`` and generates
a two-panel figure:

* Panel 1 — Privacy: reidentification rate (%) vs k, one curve per attack type.
* Panel 2 — Utility: clustering variation and KS degree-distribution distance vs k.

Error bars represent ±1 standard deviation across independent seeds.

Usage::

    python -m src.visualization.privacy_utility --logs experiments/logs/
    python -m src.visualization.privacy_utility \\
        --logs experiments/logs/he2009_facebook_baseline \\
        --out results/plots \\
        --title "He et al. (2009) — Facebook Ego-Net"
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")  # headless backend — safe for CI and import-time use
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


def _iter_jsonl_files(logs_dir: Path) -> list[Path]:
    """Return all .jsonl files found recursively under *logs_dir*, sorted."""
    return sorted(logs_dir.rglob("*.jsonl"))


def load_jsonl_records(logs_dir: Path) -> list[dict[str, Any]]:
    """Load every valid JSON line from every .jsonl file under *logs_dir*.

    Parameters
    ----------
    logs_dir:
        Root directory to search.  Must exist.

    Returns
    -------
    list[dict]
        Parsed records.  Lines that are not valid JSON or that lack the
        required fields ``k`` and ``reidentification_rate_degree`` are
        silently skipped.

    Raises
    ------
    FileNotFoundError
        If *logs_dir* does not exist.
    """
    if not logs_dir.exists():
        raise FileNotFoundError(f"logs_dir not found: {logs_dir}")

    records: list[dict[str, Any]] = []
    for path in _iter_jsonl_files(logs_dir):
        with path.open(encoding="utf-8") as fh:
            for raw in fh:
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    rec = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                if "k" not in rec or "reidentification_rate_degree" not in rec:
                    continue
                records.append(rec)
    return records


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------


def _safe_float(value: Any, default: float = 0.0) -> float:
    """Cast *value* to float, returning *default* on failure."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def aggregate_by_k(
    records: list[dict[str, Any]],
) -> dict[int, dict[str, dict[str, float]]]:
    """Aggregate per-seed records into per-k statistics.

    Parameters
    ----------
    records:
        Non-empty list of records as returned by :func:`load_jsonl_records`.

    Returns
    -------
    dict
        Nested mapping ``{k: {metric_name: {"mean": …, "std": …}}}``.

        Metrics:

        - ``rr_degree``   — ``reidentification_rate_degree``
        - ``rr_subgraph`` — ``reidentification_rate_subgraph``
        - ``clust_var``   — ``clustering_variation``
        - ``ks_d``        — ``ks_test_degree["D"]``

    Raises
    ------
    ValueError
        If *records* is empty.
    """
    if not records:
        raise ValueError(
            "No records to aggregate — logs_dir may be empty or contain no valid records."
        )

    buckets: dict[int, dict[str, list[float]]] = {}
    for rec in records:
        k = int(rec["k"])
        if k not in buckets:
            buckets[k] = {
                "rr_degree": [],
                "rr_subgraph": [],
                "clust_var": [],
                "ks_d": [],
            }
        buckets[k]["rr_degree"].append(_safe_float(rec.get("reidentification_rate_degree")))
        buckets[k]["rr_subgraph"].append(_safe_float(rec.get("reidentification_rate_subgraph")))
        buckets[k]["clust_var"].append(_safe_float(rec.get("clustering_variation")))
        ks = rec.get("ks_test_degree", {})
        ks_d = ks.get("D") if isinstance(ks, dict) else ks
        buckets[k]["ks_d"].append(_safe_float(ks_d))

    def _stats(values: list[float]) -> dict[str, float]:
        arr = np.asarray(values, dtype=float)
        return {
            "mean": float(np.mean(arr)),
            "std": float(np.std(arr, ddof=0)) if len(arr) > 1 else 0.0,
        }

    return {
        k: {metric: _stats(vals) for metric, vals in metrics.items()}
        for k, metrics in sorted(buckets.items())
    }


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

_ATTACK_COLORS: dict[str, str] = {
    "degree": "#1f77b4",  # matplotlib blue
    "subgraph": "#ff7f0e",  # matplotlib orange
}
_UTILITY_COLORS: dict[str, str] = {
    "clust_var": "#2ca02c",  # matplotlib green
    "ks_d": "#d62728",  # matplotlib red
}


def plot_privacy_utility(
    stats: dict[int, dict[str, dict[str, float]]],
    output_dir: Path,
    title: str = "Privacy vs. Utility — He et al. (2009)",
    filename_stem: str = "privacy_utility",
) -> tuple[Path, Path]:
    """Generate a two-panel privacy-utility figure and save to *output_dir*.

    The figure contains:

    * **Panel 1 (Privacy):** reidentification rate (%) vs k for each attack
      (degree and subgraph), with ±1 std error bars across seeds.
    * **Panel 2 (Utility):** clustering variation and KS degree-distribution
      D-statistic vs k, with ±1 std error bars across seeds.

    Parameters
    ----------
    stats:
        Output of :func:`aggregate_by_k`.
    output_dir:
        Destination directory (created if absent).
    title:
        Figure suptitle.
    filename_stem:
        Base filename without extension (e.g. ``"privacy_utility"``).

    Returns
    -------
    (pdf_path, png_path)
        Absolute paths of the saved files.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    k_values = sorted(stats.keys())
    k_arr = np.asarray(k_values, dtype=float)

    def _extract(metric: str) -> tuple[np.ndarray, np.ndarray]:
        means = np.array([stats[k][metric]["mean"] for k in k_values])
        stds = np.array([stats[k][metric]["std"] for k in k_values])
        return means, stds

    rr_deg_m, rr_deg_s = _extract("rr_degree")
    rr_sub_m, rr_sub_s = _extract("rr_subgraph")
    clust_m, clust_s = _extract("clust_var")
    ks_m, ks_s = _extract("ks_d")

    fig, (ax_priv, ax_util) = plt.subplots(2, 1, figsize=(7, 8), sharex=True)
    fig.suptitle(title, fontsize=13, fontweight="bold", y=0.98)

    # ---- Panel 1: Privacy ------------------------------------------------
    ax_priv.errorbar(
        k_arr,
        rr_deg_m * 100,
        yerr=rr_deg_s * 100,
        marker="o",
        color=_ATTACK_COLORS["degree"],
        label="Ataque por grau",
        capsize=4,
        linewidth=1.8,
    )
    ax_priv.errorbar(
        k_arr,
        rr_sub_m * 100,
        yerr=rr_sub_s * 100,
        marker="s",
        color=_ATTACK_COLORS["subgraph"],
        label="Ataque por subgrafo",
        capsize=4,
        linewidth=1.8,
    )
    ax_priv.set_ylabel("Taxa de Reidentificação (%)", fontsize=11)
    ax_priv.set_ylim(bottom=0)
    ax_priv.legend(fontsize=10)
    ax_priv.grid(True, linestyle="--", alpha=0.4)
    ax_priv.set_title("Privacidade  (↓ melhor)", fontsize=10, color="#444")

    # ---- Panel 2: Utility ------------------------------------------------
    ax_util.errorbar(
        k_arr,
        clust_m,
        yerr=clust_s,
        marker="^",
        color=_UTILITY_COLORS["clust_var"],
        label="Variação de Clustering",
        capsize=4,
        linewidth=1.8,
    )
    ax_util.errorbar(
        k_arr,
        ks_m,
        yerr=ks_s,
        marker="D",
        color=_UTILITY_COLORS["ks_d"],
        label="KS-D (distribuição de grau)",
        capsize=4,
        linewidth=1.8,
    )
    ax_util.set_xlabel("k (parâmetro de anonimização)", fontsize=11)
    ax_util.set_ylabel("Degradação de Utilidade", fontsize=11)
    ax_util.set_ylim(bottom=0)
    ax_util.legend(fontsize=10)
    ax_util.grid(True, linestyle="--", alpha=0.4)
    ax_util.set_title("Utilidade  (↓ melhor)", fontsize=10, color="#444")

    # x-ticks only at the actual k values used
    ax_util.set_xticks(k_arr)
    ax_util.set_xticklabels([str(k) for k in k_values])

    fig.tight_layout(rect=[0, 0, 1, 0.96])

    pdf_path = output_dir / f"{filename_stem}.pdf"
    png_path = output_dir / f"{filename_stem}.png"
    fig.savefig(str(pdf_path), format="pdf", bbox_inches="tight")
    fig.savefig(str(png_path), format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    return pdf_path, png_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m src.visualization.privacy_utility",
        description="Generate privacy-vs-utility plot from JSONL experiment logs.",
    )
    p.add_argument(
        "--logs",
        type=Path,
        default=Path("experiments/logs"),
        help="Root directory containing JSONL log files (default: experiments/logs).",
    )
    p.add_argument(
        "--out",
        type=Path,
        default=Path("results/plots"),
        help="Output directory for PDF and PNG (default: results/plots).",
    )
    p.add_argument(
        "--title",
        type=str,
        default="Privacy vs. Utility — He et al. (2009)",
        help="Figure suptitle.",
    )
    p.add_argument(
        "--stem",
        type=str,
        default="privacy_utility",
        help="Output filename stem without extension (default: privacy_utility).",
    )
    return p


def main(argv: list[str] | None = None) -> None:
    """Entry point for ``python -m src.visualization.privacy_utility``."""
    args = _build_parser().parse_args(argv)

    print(f"Loading records from: {args.logs}")
    records = load_jsonl_records(args.logs)
    print(f"  {len(records)} records loaded.")

    stats = aggregate_by_k(records)
    k_list = sorted(stats.keys())
    print(f"  k values found: {k_list}")
    for k in k_list:
        m = stats[k]
        print(
            f"  k={k:2d}  "
            f"rr_deg={m['rr_degree']['mean']:.3f}±{m['rr_degree']['std']:.3f}  "
            f"rr_sub={m['rr_subgraph']['mean']:.3f}±{m['rr_subgraph']['std']:.3f}  "
            f"clust={m['clust_var']['mean']:.3f}±{m['clust_var']['std']:.3f}  "
            f"ks_d={m['ks_d']['mean']:.3f}±{m['ks_d']['std']:.3f}"
        )

    pdf_path, png_path = plot_privacy_utility(
        stats,
        output_dir=args.out,
        title=args.title,
        filename_stem=args.stem,
    )
    print(f"\nSaved:\n  {pdf_path}\n  {png_path}")


if __name__ == "__main__":
    main()
