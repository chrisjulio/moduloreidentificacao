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
from matplotlib.lines import Line2D

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


#: Metric names produced by the aggregators, in display order.
_METRICS: tuple[str, ...] = ("rr_degree", "rr_subgraph", "clust_var", "ks_d")


def _empty_bucket() -> dict[str, list[float]]:
    return {metric: [] for metric in _METRICS}


def _accumulate(bucket: dict[str, list[float]], rec: dict[str, Any]) -> None:
    """Append the metric values of *rec* to *bucket* (one bucket = one cell)."""
    bucket["rr_degree"].append(_safe_float(rec.get("reidentification_rate_degree")))
    bucket["rr_subgraph"].append(_safe_float(rec.get("reidentification_rate_subgraph")))
    bucket["clust_var"].append(_safe_float(rec.get("clustering_variation")))
    ks = rec.get("ks_test_degree", {})
    ks_d = ks.get("D") if isinstance(ks, dict) else ks
    bucket["ks_d"].append(_safe_float(ks_d))


def _stats(values: list[float]) -> dict[str, float]:
    arr = np.asarray(values, dtype=float)
    return {
        "mean": float(np.mean(arr)),
        "std": float(np.std(arr, ddof=0)) if len(arr) > 1 else 0.0,
    }


def aggregate_by_k_d(
    records: list[dict[str, Any]],
) -> dict[tuple[int, int], dict[str, dict[str, float]]]:
    """Aggregate per-seed records into per-``(k, d)`` statistics.

    Treats the anonymisation sub-grouping depth ``d`` as a first-class
    dimension: each distinct ``(k, d)`` configuration becomes one cell whose
    statistics are computed across its seeds.  Records without a ``d`` field
    (logs predating the DL-01 schema, issue #22) are grouped as ``d=1``.

    Parameters
    ----------
    records:
        Non-empty list of records as returned by :func:`load_jsonl_records`.

    Returns
    -------
    dict
        Nested mapping ``{(k, d): {metric_name: {"mean": …, "std": …}}}``,
        with keys sorted by ``(k, d)``.

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

    buckets: dict[tuple[int, int], dict[str, list[float]]] = {}
    for rec in records:
        key = (int(rec["k"]), int(rec.get("d", 1)))
        if key not in buckets:
            buckets[key] = _empty_bucket()
        _accumulate(buckets[key], rec)

    return {
        key: {metric: _stats(vals) for metric, vals in metrics.items()}
        for key, metrics in sorted(buckets.items())
    }


def aggregate_by_k(
    records: list[dict[str, Any]],
) -> dict[int, dict[str, dict[str, float]]]:
    """Aggregate per-seed records into per-k statistics.

    This is the baseline (d-agnostic) aggregator: all records sharing the same
    ``k`` are pooled together, regardless of ``d``.  Its behaviour is unchanged
    from before the d-sweep work — for baseline logs (uniform ``d=1``) it is
    equivalent to :func:`aggregate_by_k_d` with the ``d`` dimension collapsed.

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
            buckets[k] = _empty_bucket()
        _accumulate(buckets[k], rec)

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
# d-sweep plotting (d-aware)
# ---------------------------------------------------------------------------

#: Supported d-sweep layouts.
DSWEEP_LAYOUTS: tuple[str, ...] = ("series", "facets")


def _save_fig(fig: Any, output_dir: Path, filename_stem: str) -> tuple[Path, Path]:
    """Save *fig* as PDF and PNG under *output_dir*; return the two paths."""
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = output_dir / f"{filename_stem}.pdf"
    png_path = output_dir / f"{filename_stem}.png"
    fig.savefig(str(pdf_path), format="pdf", bbox_inches="tight")
    fig.savefig(str(png_path), format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    return pdf_path, png_path


def _d_color_map(d_values: list[int]) -> dict[int, tuple[float, float, float, float]]:
    """Assign a distinct, deterministic colour to each ``d`` value."""
    cmap = plt.get_cmap("viridis")
    n = max(len(d_values), 1)
    return {d: cmap(0.15 + 0.7 * (i / max(n - 1, 1))) for i, d in enumerate(sorted(d_values))}


def _series_for_d(
    stats: dict[tuple[int, int], dict[str, dict[str, float]]],
    d: int,
    metric: str,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return ``(k, mean, std)`` arrays for one ``d`` and one *metric*, k-sorted."""
    ks = sorted(k for (k, dd) in stats if dd == d)
    k_arr = np.asarray(ks, dtype=float)
    means = np.array([stats[(k, d)][metric]["mean"] for k in ks])
    stds = np.array([stats[(k, d)][metric]["std"] for k in ks])
    return k_arr, means, stds


def plot_privacy_utility_dsweep(
    stats: dict[tuple[int, int], dict[str, dict[str, float]]],
    output_dir: Path,
    title: str = "Privacy vs. Utility (d-sweep) — He et al. (2009)",
    filename_stem: str = "privacy_utility_dsweep",
    layout: str = "series",
) -> tuple[Path, Path]:
    """Generate a d-aware privacy-utility figure from :func:`aggregate_by_k_d` stats.

    Two layouts are supported:

    * ``"series"`` (default) — two stacked panels (privacy + utility).  ``d`` is
      encoded by colour and the two attacks / utility metrics by line style, so
      every curve shares the same x-axis (``k``).  Compact; favours comparing
      trends across ``d``.
    * ``"facets"`` — a ``2 x len(d)`` grid (privacy row + utility row, one column
      per ``d``).  Each subplot plots its metrics vs ``k``.  Favours reading when
      curves would otherwise overlap.

    Error bars are ±1 standard deviation across the seeds of each ``(k, d)`` cell.

    Parameters
    ----------
    stats:
        Output of :func:`aggregate_by_k_d`.
    output_dir:
        Destination directory (created if absent).
    title:
        Figure suptitle.
    filename_stem:
        Base filename without extension.
    layout:
        Either ``"series"`` or ``"facets"``.

    Returns
    -------
    (pdf_path, png_path)
        Absolute paths of the saved files.

    Raises
    ------
    ValueError
        If *stats* is empty or *layout* is not recognised.
    """
    if not stats:
        raise ValueError("No stats to plot — aggregate_by_k_d returned no cells.")
    if layout not in DSWEEP_LAYOUTS:
        raise ValueError(f"Unknown layout: {layout!r}. Expected one of {DSWEEP_LAYOUTS}.")

    d_values = sorted({d for (_k, d) in stats})
    colors = _d_color_map(d_values)

    if layout == "series":
        return _plot_dsweep_series(stats, d_values, colors, output_dir, title, filename_stem)
    return _plot_dsweep_facets(stats, d_values, colors, output_dir, title, filename_stem)


def _plot_dsweep_series(
    stats: dict[tuple[int, int], dict[str, dict[str, float]]],
    d_values: list[int],
    colors: dict[int, tuple[float, float, float, float]],
    output_dir: Path,
    title: str,
    filename_stem: str,
) -> tuple[Path, Path]:
    """Two-panel layout: colour encodes d, line style encodes attack/metric."""
    fig, (ax_priv, ax_util) = plt.subplots(2, 1, figsize=(7.5, 8.5), sharex=True)
    fig.suptitle(title, fontsize=13, fontweight="bold", y=0.98)

    # ---- Panel 1: Privacy (degree dashed, subgraph solid) ----------------
    for d in d_values:
        c = colors[d]
        k_arr, m_sub, s_sub = _series_for_d(stats, d, "rr_subgraph")
        ax_priv.errorbar(
            k_arr,
            m_sub * 100,
            yerr=s_sub * 100,
            marker="s",
            linestyle="-",
            color=c,
            capsize=3,
            linewidth=1.6,
        )
        k_arr, m_deg, s_deg = _series_for_d(stats, d, "rr_degree")
        ax_priv.errorbar(
            k_arr,
            m_deg * 100,
            yerr=s_deg * 100,
            marker="o",
            linestyle="--",
            color=c,
            capsize=3,
            linewidth=1.6,
        )
    ax_priv.set_ylabel("Taxa de Reidentificação (%)", fontsize=11)
    ax_priv.set_ylim(bottom=0)
    ax_priv.grid(True, linestyle="--", alpha=0.4)
    ax_priv.set_title("Privacidade  (↓ melhor)", fontsize=10, color="#444")
    _style_legend(ax_priv, "Subgrafo", "Grau")

    # ---- Panel 2: Utility (clustering solid, KS-D dashed) ----------------
    for d in d_values:
        c = colors[d]
        k_arr, m_cl, s_cl = _series_for_d(stats, d, "clust_var")
        ax_util.errorbar(
            k_arr,
            m_cl,
            yerr=s_cl,
            marker="^",
            linestyle="-",
            color=c,
            capsize=3,
            linewidth=1.6,
        )
        k_arr, m_ks, s_ks = _series_for_d(stats, d, "ks_d")
        ax_util.errorbar(
            k_arr,
            m_ks,
            yerr=s_ks,
            marker="D",
            linestyle="--",
            color=c,
            capsize=3,
            linewidth=1.6,
        )
    ax_util.set_xlabel("k (parâmetro de anonimização)", fontsize=11)
    ax_util.set_ylabel("Degradação de Utilidade", fontsize=11)
    ax_util.set_ylim(bottom=0)
    ax_util.grid(True, linestyle="--", alpha=0.4)
    ax_util.set_title("Utilidade  (↓ melhor)", fontsize=10, color="#444")
    _style_legend(ax_util, "Variação de Clustering", "KS-D (grau)")

    # Shared d-colour legend (one entry per d), placed on the privacy panel.
    d_handles = [
        Line2D([0], [0], color=colors[d], marker="o", linestyle="-", label=f"d={d}")
        for d in d_values
    ]
    leg_d = ax_priv.legend(handles=d_handles, title="d", fontsize=9, loc="upper right")
    ax_priv.add_artist(leg_d)

    all_k = sorted({k for (k, _d) in stats})
    ax_util.set_xticks([float(k) for k in all_k])
    ax_util.set_xticklabels([str(k) for k in all_k])

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    return _save_fig(fig, output_dir, filename_stem)


def _style_legend(ax: Any, solid_label: str, dashed_label: str) -> None:
    """Add a black solid/dashed legend (line-style key) at the upper left of *ax*."""
    handles = [
        Line2D([0], [0], color="#333", linestyle="-", marker="s", label=solid_label),
        Line2D([0], [0], color="#333", linestyle="--", marker="o", label=dashed_label),
    ]
    ax.legend(handles=handles, fontsize=9, loc="upper left")


def _plot_dsweep_facets(
    stats: dict[tuple[int, int], dict[str, dict[str, float]]],
    d_values: list[int],
    colors: dict[int, tuple[float, float, float, float]],
    output_dir: Path,
    title: str,
    filename_stem: str,
) -> tuple[Path, Path]:
    """Grid layout: 2 rows (privacy, utility) x one column per d value."""
    ncols = len(d_values)
    fig, axes = plt.subplots(2, ncols, figsize=(3.6 * ncols + 1.5, 7.5), sharex=True, squeeze=False)
    fig.suptitle(title, fontsize=13, fontweight="bold", y=0.99)

    all_k = sorted({k for (k, _d) in stats})
    k_ticks = [float(k) for k in all_k]

    for col, d in enumerate(d_values):
        c = colors[d]
        ax_priv = axes[0][col]
        ax_util = axes[1][col]

        # Privacy row
        k_arr, m_deg, s_deg = _series_for_d(stats, d, "rr_degree")
        ax_priv.errorbar(
            k_arr,
            m_deg * 100,
            yerr=s_deg * 100,
            marker="o",
            color=_ATTACK_COLORS["degree"],
            capsize=3,
            linewidth=1.6,
            label="Ataque por grau",
        )
        k_arr, m_sub, s_sub = _series_for_d(stats, d, "rr_subgraph")
        ax_priv.errorbar(
            k_arr,
            m_sub * 100,
            yerr=s_sub * 100,
            marker="s",
            color=_ATTACK_COLORS["subgraph"],
            capsize=3,
            linewidth=1.6,
            label="Ataque por subgrafo",
        )
        ax_priv.set_title(f"d = {d}", fontsize=11, color=c, fontweight="bold")
        ax_priv.set_ylim(bottom=0)
        ax_priv.grid(True, linestyle="--", alpha=0.4)

        # Utility row
        k_arr, m_cl, s_cl = _series_for_d(stats, d, "clust_var")
        ax_util.errorbar(
            k_arr,
            m_cl,
            yerr=s_cl,
            marker="^",
            color=_UTILITY_COLORS["clust_var"],
            capsize=3,
            linewidth=1.6,
            label="Variação de Clustering",
        )
        k_arr, m_ks, s_ks = _series_for_d(stats, d, "ks_d")
        ax_util.errorbar(
            k_arr,
            m_ks,
            yerr=s_ks,
            marker="D",
            color=_UTILITY_COLORS["ks_d"],
            capsize=3,
            linewidth=1.6,
            label="KS-D (grau)",
        )
        ax_util.set_ylim(bottom=0)
        ax_util.grid(True, linestyle="--", alpha=0.4)
        ax_util.set_xlabel("k", fontsize=10)
        ax_util.set_xticks(k_ticks)
        ax_util.set_xticklabels([str(k) for k in all_k])

    axes[0][0].set_ylabel("Taxa de Reidentificação (%)", fontsize=10)
    axes[1][0].set_ylabel("Degradação de Utilidade", fontsize=10)
    axes[0][0].legend(fontsize=8, loc="upper right")
    axes[1][0].legend(fontsize=8, loc="upper right")

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    return _save_fig(fig, output_dir, filename_stem)


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
        default=None,
        help="Figure suptitle (default: a mode-appropriate title).",
    )
    p.add_argument(
        "--stem",
        type=str,
        default=None,
        help=(
            "Output filename stem without extension "
            "(default: 'privacy_utility', or 'privacy_utility_dsweep' in d-sweep mode)."
        ),
    )
    p.add_argument(
        "--dsweep",
        action="store_true",
        help=(
            "Force the d-aware plot (per-(k, d) curves). "
            "Auto-enabled when the logs contain more than one distinct d."
        ),
    )
    p.add_argument(
        "--layout",
        choices=list(DSWEEP_LAYOUTS),
        default="series",
        help="d-sweep layout: 'series' (default) or 'facets'. Ignored in baseline mode.",
    )
    return p


def _distinct_d(records: list[dict[str, Any]]) -> list[int]:
    """Return the sorted distinct ``d`` values present in *records* (default 1)."""
    return sorted({int(rec.get("d", 1)) for rec in records})


def main(argv: list[str] | None = None) -> None:
    """Entry point for ``python -m src.visualization.privacy_utility``."""
    args = _build_parser().parse_args(argv)

    print(f"Loading records from: {args.logs}")
    records = load_jsonl_records(args.logs)
    print(f"  {len(records)} records loaded.")

    d_values = _distinct_d(records)
    use_dsweep = args.dsweep or len(d_values) > 1

    if use_dsweep:
        stem = args.stem if args.stem is not None else "privacy_utility_dsweep"
        title = (
            args.title
            if args.title is not None
            else "Privacy vs. Utility (d-sweep) — He et al. (2009)"
        )
        stats = aggregate_by_k_d(records)
        print(f"  d values found: {d_values}  (layout: {args.layout})")
        for k, d in sorted(stats.keys()):
            m = stats[(k, d)]
            print(
                f"  k={k:2d} d={d:2d}  "
                f"rr_deg={m['rr_degree']['mean']:.3f}±{m['rr_degree']['std']:.3f}  "
                f"rr_sub={m['rr_subgraph']['mean']:.3f}±{m['rr_subgraph']['std']:.3f}  "
                f"clust={m['clust_var']['mean']:.3f}±{m['clust_var']['std']:.3f}  "
                f"ks_d={m['ks_d']['mean']:.3f}±{m['ks_d']['std']:.3f}"
            )
        pdf_path, png_path = plot_privacy_utility_dsweep(
            stats,
            output_dir=args.out,
            title=title,
            filename_stem=stem,
            layout=args.layout,
        )
        print(f"\nSaved:\n  {pdf_path}\n  {png_path}")
        return

    stem = args.stem if args.stem is not None else "privacy_utility"
    title = args.title if args.title is not None else "Privacy vs. Utility — He et al. (2009)"
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
        title=title,
        filename_stem=stem,
    )
    print(f"\nSaved:\n  {pdf_path}\n  {png_path}")


if __name__ == "__main__":
    main()
