"""Facebook x Enron normalised comparison figure for He et al. (2009) experiments.

Reads two structured JSONL log sets (the Facebook baseline and the Enron
secondary experiment) and produces a single comparison figure whose two panels
are *normalised* so that the two networks become legible on shared axes despite
their very different absolute scales (subgraph reidentification spans 0-79 % on
Facebook vs 0-12 % on Enron — an overlaid raw plot would crush the Enron curve
to a near-flat line).

Panels
------
* **Panel A — "fração da cota 1/k"**: ``rr_subgraph * k``.  A horizontal line at
  ``1.0`` marks the theoretical k-anonymity bound ``rr <= 1/k``.  Points above
  ``1.0`` flag the ``d=1`` degree-only regime (achado B1): the 1-hop structure
  the subgraph attack inspects is **not** anonymised at ``d=1``, so the bound
  need not hold.  This panel makes the bound — and its crossings — explicit.
* **Panel B — "decaimento relativo"**: ``rr_subgraph(k) / rr_subgraph(k0)`` with
  ``k0`` the smallest k.  Removing the absolute-level gap (~6x at k=2) exposes
  the *shape* of the privacy gain with k — the genuinely comparable quantity
  across datasets.

Outputs a PNG (and optionally a PDF) plus a tidy CSV of the plotted series.  The
CSV also carries the per-k mean KS-D (utility) so the frozen artefact is a
self-contained risk x utility snapshot.

Usage::

    python -m src.visualization.comparison \\
        --fb-logs experiments/logs/he2009_facebook_baseline \\
        --enron-logs experiments/logs/he2009_enron_secondary \\
        --out docs/assets --stem comparison_fb_enron
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")  # headless backend — safe for CI and import-time use
import matplotlib.pyplot as plt
import numpy as np

from src.visualization.privacy_utility import load_jsonl_records

# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------


def _safe_float(value: Any, default: float = 0.0) -> float:
    """Cast *value* to float, returning *default* on failure."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def mean_by_k(records: list[dict[str, Any]], field: str) -> dict[int, float]:
    """Mean of a top-level numeric *field* per k across seeds.

    Records lacking the field contribute ``0.0`` (consistent with the lenient
    aggregation of :mod:`src.visualization.privacy_utility`).

    Raises
    ------
    ValueError
        If *records* is empty.
    """
    if not records:
        raise ValueError("No records to aggregate.")
    buckets: dict[int, list[float]] = {}
    for rec in records:
        buckets.setdefault(int(rec["k"]), []).append(_safe_float(rec.get(field)))
    return {k: float(np.mean(vals)) for k, vals in sorted(buckets.items())}


def mean_ks_d_by_k(records: list[dict[str, Any]]) -> dict[int, float]:
    """Mean KS-D (``ks_test_degree["D"]``) per k across seeds."""
    if not records:
        raise ValueError("No records to aggregate.")
    buckets: dict[int, list[float]] = {}
    for rec in records:
        ks = rec.get("ks_test_degree", {})
        d = ks.get("D") if isinstance(ks, dict) else ks
        buckets.setdefault(int(rec["k"]), []).append(_safe_float(d))
    return {k: float(np.mean(vals)) for k, vals in sorted(buckets.items())}


def bound_fraction(rr_by_k: dict[int, float]) -> dict[int, float]:
    """``rr * k`` per k — the fraction of the theoretical ``1/k`` bound."""
    return {k: rr * k for k, rr in rr_by_k.items()}


def relative_decay(rr_by_k: dict[int, float]) -> dict[int, float]:
    """``rr(k) / rr(k0)`` per k, with ``k0`` the smallest k (base = 1.0)."""
    if not rr_by_k:
        return {}
    k0 = min(rr_by_k)
    base = rr_by_k[k0]
    return {k: (rr / base if base else 0.0) for k, rr in rr_by_k.items()}


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

_DATASET_STYLE: dict[str, dict[str, str]] = {
    "facebook": {"color": "#1f77b4", "marker": "o", "label": "Facebook (ego-rede 3437)"},
    "enron": {"color": "#ff7f0e", "marker": "s", "label": "Email-Enron (LCC)"},
}


def plot_comparison(
    fb_rr_by_k: dict[int, float],
    en_rr_by_k: dict[int, float],
    output_dir: Path,
    title: str = "Facebook x Enron — comparativo normalizado (ataque por subgrafo)",
    filename_stem: str = "comparison_fb_enron",
    write_pdf: bool = False,
) -> dict[str, Path]:
    """Render the two-panel normalised comparison figure to *output_dir*.

    Parameters
    ----------
    fb_rr_by_k, en_rr_by_k:
        ``{k: mean rr_subgraph}`` for Facebook and Enron respectively.
    output_dir:
        Destination directory (created if absent).
    title:
        Figure suptitle.
    filename_stem:
        Base filename without extension.
    write_pdf:
        Also save a PDF alongside the PNG.

    Returns
    -------
    dict[str, Path]
        Mapping with keys ``"png"`` (always) and ``"pdf"`` (only if requested).
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    series = {"facebook": fb_rr_by_k, "enron": en_rr_by_k}
    fig, (ax_bound, ax_decay) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle(title, fontsize=13, fontweight="bold", y=0.99)

    # ---- Panel A: fraction of the 1/k bound ------------------------------
    for name, rr_by_k in series.items():
        style = _DATASET_STYLE[name]
        ks = sorted(rr_by_k)
        vals = [bound_fraction(rr_by_k)[k] for k in ks]
        ax_bound.plot(
            ks,
            vals,
            marker=style["marker"],
            color=style["color"],
            label=style["label"],
            linewidth=1.8,
        )
    ax_bound.axhline(1.0, color="#555", linestyle=":", linewidth=1.4, label="cota 1/k (rr·k = 1)")
    ax_bound.set_xlabel("k", fontsize=11)
    ax_bound.set_ylabel("rr_subgrafo · k  (fração da cota 1/k)", fontsize=11)
    ax_bound.set_title(
        "(A) Fração da cota 1/k — acima de 1 viola a cota (B1, d=1)", fontsize=10, color="#444"
    )
    ax_bound.grid(True, linestyle="--", alpha=0.4)
    ax_bound.legend(fontsize=9)

    # ---- Panel B: relative decay -----------------------------------------
    for name, rr_by_k in series.items():
        style = _DATASET_STYLE[name]
        ks = sorted(rr_by_k)
        vals = [relative_decay(rr_by_k)[k] for k in ks]
        ax_decay.plot(
            ks,
            vals,
            marker=style["marker"],
            color=style["color"],
            label=style["label"],
            linewidth=1.8,
        )
    ax_decay.set_xlabel("k", fontsize=11)
    ax_decay.set_ylabel("rr_subgrafo(k) / rr_subgrafo(k mínimo)", fontsize=11)
    ax_decay.set_title(
        "(B) Decaimento relativo — forma da curva (magnitude removida)", fontsize=10, color="#444"
    )
    ax_decay.set_ylim(bottom=0)
    ax_decay.grid(True, linestyle="--", alpha=0.4)
    ax_decay.legend(fontsize=9)

    all_k = sorted(set(fb_rr_by_k) | set(en_rr_by_k))
    for ax in (ax_bound, ax_decay):
        ax.set_xticks(all_k)
        ax.set_xticklabels([str(k) for k in all_k])

    fig.tight_layout(rect=[0, 0, 1, 0.95])

    paths: dict[str, Path] = {}
    png_path = output_dir / f"{filename_stem}.png"
    fig.savefig(str(png_path), format="png", dpi=150, bbox_inches="tight")
    paths["png"] = png_path
    if write_pdf:
        pdf_path = output_dir / f"{filename_stem}.pdf"
        fig.savefig(str(pdf_path), format="pdf", bbox_inches="tight")
        paths["pdf"] = pdf_path
    plt.close(fig)
    return paths


# ---------------------------------------------------------------------------
# CSV
# ---------------------------------------------------------------------------

CSV_COLUMNS: tuple[str, ...] = (
    "dataset",
    "k",
    "rr_subgraph",
    "bound_fraction",
    "relative_decay",
    "ks_d",
)


def write_comparison_csv(
    fb_rr_by_k: dict[int, float],
    en_rr_by_k: dict[int, float],
    fb_ks_by_k: dict[int, float],
    en_ks_by_k: dict[int, float],
    csv_path: Path,
) -> Path:
    """Write the plotted series as a tidy CSV (one row per dataset x k)."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    for name, rr_by_k, ks_by_k in (
        ("facebook", fb_rr_by_k, fb_ks_by_k),
        ("enron", en_rr_by_k, en_ks_by_k),
    ):
        bf = bound_fraction(rr_by_k)
        rd = relative_decay(rr_by_k)
        for k in sorted(rr_by_k):
            rows.append(
                {
                    "dataset": name,
                    "k": k,
                    "rr_subgraph": round(rr_by_k[k], 6),
                    "bound_fraction": round(bf[k], 6),
                    "relative_decay": round(rd[k], 6),
                    "ks_d": round(ks_by_k.get(k, 0.0), 6),
                }
            )
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(CSV_COLUMNS))
        writer.writeheader()
        writer.writerows(rows)
    return csv_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m src.visualization.comparison",
        description="Generate the Facebook x Enron normalised comparison figure and CSV.",
    )
    p.add_argument("--fb-logs", type=Path, required=True, help="Facebook baseline logs directory.")
    p.add_argument("--enron-logs", type=Path, required=True, help="Enron secondary logs directory.")
    p.add_argument("--out", type=Path, default=Path("docs/assets"), help="Output directory.")
    p.add_argument("--stem", type=str, default="comparison_fb_enron", help="Output filename stem.")
    p.add_argument("--title", type=str, default=None, help="Figure suptitle.")
    p.add_argument("--pdf", action="store_true", help="Also write a PDF.")
    return p


def main(argv: list[str] | None = None) -> None:
    """Entry point for ``python -m src.visualization.comparison``."""
    args = _build_parser().parse_args(argv)

    fb_records = load_jsonl_records(args.fb_logs)
    en_records = load_jsonl_records(args.enron_logs)
    print(f"Facebook: {len(fb_records)} records from {args.fb_logs}")
    print(f"Enron:    {len(en_records)} records from {args.enron_logs}")

    fb_rr = mean_by_k(fb_records, "reidentification_rate_subgraph")
    en_rr = mean_by_k(en_records, "reidentification_rate_subgraph")
    fb_ks = mean_ks_d_by_k(fb_records)
    en_ks = mean_ks_d_by_k(en_records)

    title = args.title or "Facebook x Enron — comparativo normalizado (ataque por subgrafo)"
    paths = plot_comparison(
        fb_rr, en_rr, output_dir=args.out, title=title, filename_stem=args.stem, write_pdf=args.pdf
    )
    csv_path = write_comparison_csv(fb_rr, en_rr, fb_ks, en_ks, args.out / f"{args.stem}.csv")

    print("\nSaved:")
    for kind, path in paths.items():
        print(f"  [{kind}] {path}")
    print(f"  [csv] {csv_path}")


if __name__ == "__main__":
    main()
