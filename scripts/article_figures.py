"""Article-styled (KDMiLe) regeneration of the two LaTeX figures.

This script does **not** replace the canonical generators in
``src.visualization`` — it reuses their *data* layer (log loading and
aggregation, plus the frozen comparison CSV) and applies the article-specific
typography and vector export required by the KDMiLe two-column A4 class.
Keeping it separate leaves the canonical PT/EN figures and their tests
untouched.

Frozen data sources (no new experiments):

* Figure 4.1 — ``experiments/logs/he2009_facebook_baseline`` (via
  :func:`src.visualization.privacy_utility.aggregate_by_k`).
* Figure 4.3 — ``docs/assets/comparison_fb_enron.csv`` (the frozen, committed
  series: ``bound_fraction`` and ``relative_decay`` per dataset x k).

Article styling (applies to both figures):

* Body-matching type: figure base font set so the text renders at ~8 pt once
  LaTeX rescales the figure to the column/text width.
* Thin lines (~0.6 pt on the page), discreet markers.
* No in-image suptitle/panel titles; panels marked "(a)"/"(b)"; one legend per
  figure; English labels, decimal point.
* Vector PDF, ``bbox_inches="tight"``, ``pad_inches=0.01``,
  ``pdf.fonttype=42`` (extractable text). Log x-axis with explicit k ticks.

Colour is the default: series are distinguished by colour + marker. Black-and-
white output (series distinguished by line-style pattern + marker, no colour)
is **opt-in** and must be requested explicitly (``--bw``).

Usage::

    python -m scripts.article_figures            # colour (default)
    python -m scripts.article_figures --bw       # black-and-white patterns
    python scripts/article_figures.py --bw --out docs/assets
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless backend — safe for CI and import-time use
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedFormatter, FixedLocator, NullLocator

from src.visualization.privacy_utility import aggregate_by_k, load_jsonl_records

# Default frozen data locations, relative to the repository root.
_DEFAULT_FB_LOGS = Path("experiments/logs/he2009_facebook_baseline")
_DEFAULT_COMPARISON_CSV = Path("docs/assets/comparison_fb_enron.csv")
_DEFAULT_OUT = Path("docs/assets")

_K_TICKS = [2, 5, 10, 20]
_BLACK = "#000000"


@dataclass(frozen=True)
class SeriesStyle:
    """Visual encoding of one plotted series under both colour and B&W modes.

    In colour mode (default) a series is drawn in its ``color`` with a solid
    line; in black-and-white mode it is drawn in black with the line-style
    pattern ``bw_linestyle``. The ``marker`` is used in both modes.
    """

    label: str
    color: str
    marker: str
    bw_linestyle: str

    def resolve(self, bw: bool) -> tuple[str, str, str]:
        """Return ``(color, linestyle, marker)`` for the requested mode."""
        if bw:
            return _BLACK, self.bw_linestyle, self.marker
        return self.color, "-", self.marker


def _apply_log_k_axis(ax: plt.Axes) -> None:
    """Configure a log x-axis with explicit integer k ticks {2,5,10,20}."""
    ax.set_xscale("log")
    ax.xaxis.set_major_locator(FixedLocator(_K_TICKS))
    ax.xaxis.set_major_formatter(FixedFormatter([str(k) for k in _K_TICKS]))
    ax.xaxis.set_minor_locator(NullLocator())
    ax.set_xlim(1.7, 23.0)


def _save_pdf(fig: plt.Figure, out_dir: Path, stem: str) -> Path:
    """Export *fig* as a vector PDF with extractable text and tight bbox."""
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / f"{stem}.pdf"
    fig.savefig(str(pdf_path), format="pdf", bbox_inches="tight", pad_inches=0.01)
    plt.close(fig)
    return pdf_path


def _legend_handles(styles: list[SeriesStyle], bw: bool) -> list[Line2D]:
    """Build proxy legend handles matching the resolved per-series encoding."""
    handles = []
    for st in styles:
        color, ls, marker = st.resolve(bw)
        handles.append(Line2D([0], [0], color=color, linestyle=ls, marker=marker, label=st.label))
    return handles


# ---------------------------------------------------------------------------
# Figure 4.1 — privacy-utility (Facebook, stacked)
# ---------------------------------------------------------------------------

# Canonical colours mirror src.visualization.privacy_utility (blue/orange/green/red).
_PU_PRIVACY: list[SeriesStyle] = [
    SeriesStyle("Degree scenario", "#1f77b4", "o", "-"),
    SeriesStyle("1-hop subgraph scenario", "#ff7f0e", "s", "--"),
]
_PU_UTILITY: list[SeriesStyle] = [
    SeriesStyle("Clustering variation", "#2ca02c", "^", ":"),
    SeriesStyle("KS-D (degree distribution)", "#d62728", "D", "-."),
]


def build_privacy_utility(fb_logs: Path, out_dir: Path, bw: bool = False) -> Path:
    """Render the article-styled Facebook privacy-utility figure (eng-privacy_utility)."""
    stats = aggregate_by_k(load_jsonl_records(fb_logs))
    k_values = sorted(stats)
    k_arr = np.asarray(k_values, dtype=float)

    def series(metric: str, scale: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
        means = np.array([stats[k][metric]["mean"] for k in k_values]) * scale
        stds = np.array([stats[k][metric]["std"] for k in k_values]) * scale
        return means, stds

    # Side-by-side (1x2) geometry, sized so the tight-bbox native size matches
    # eng-comparison_fb_enron.pdf (~11.55 x 4.97 in). Identical base font and
    # linewidth to Figure 4.3 plus an identical native width means both figures
    # take the same downscale to \textwidth and thus render with identical
    # typography. The four-series legend is laid out in 2 columns (2 rows) so it
    # stays within the canvas width (a single row of these long labels at 16 pt
    # overflows ~13.7 in and inflates the tight bbox).
    base, lw, ms, caps = 16.0, 1.2, 6.0, 3.0

    def draw(ax: plt.Axes, metric: str, st: SeriesStyle, scale: float) -> None:
        color, ls, marker = st.resolve(bw)
        m, s = series(metric, scale)
        ax.errorbar(
            k_arr,
            m,
            yerr=s,
            color=color,
            linestyle=ls,
            marker=marker,
            linewidth=lw,
            markersize=ms,
            capsize=caps,
            elinewidth=0.8,
        )

    with plt.rc_context({"pdf.fonttype": 42, "font.size": base, "axes.linewidth": 0.8}):
        fig, (ax_priv, ax_util) = plt.subplots(1, 2, figsize=(12.0, 5.19))

        # ---- Panel (a): privacy ------------------------------------------
        draw(ax_priv, "rr_degree", _PU_PRIVACY[0], 100.0)
        draw(ax_priv, "rr_subgraph", _PU_PRIVACY[1], 100.0)
        ax_priv.set_ylabel("Re-identification rate (%)")
        ax_priv.set_xlabel("k")
        ax_priv.set_ylim(bottom=0)
        ax_priv.grid(True, linestyle="--", alpha=0.3, linewidth=0.5)

        # ---- Panel (b): utility ------------------------------------------
        draw(ax_util, "clust_var", _PU_UTILITY[0], 1.0)
        draw(ax_util, "ks_d", _PU_UTILITY[1], 1.0)
        ax_util.set_ylabel("Utility degradation")
        ax_util.set_xlabel("k")
        ax_util.set_ylim(bottom=0)
        ax_util.grid(True, linestyle="--", alpha=0.3, linewidth=0.5)

        # Panel labels as left-aligned titles — above the frame, clear of data.
        for ax, tag in ((ax_priv, "(a)"), (ax_util, "(b)")):
            _apply_log_k_axis(ax)
            ax.set_title(tag, loc="left", fontweight="bold")

        fig.legend(
            handles=_legend_handles(_PU_PRIVACY + _PU_UTILITY, bw),
            loc="lower center",
            ncol=2,
            frameon=False,
            bbox_to_anchor=(0.5, -0.02),
        )
        # Reserve a bottom margin so the two-row legend clears the "k" labels.
        fig.tight_layout(rect=[0, 0.16, 1, 1])
        return _save_pdf(fig, out_dir, "eng-privacy_utility")


# ---------------------------------------------------------------------------
# Figure 4.3 — Facebook x Enron normalized comparison (side by side)
# ---------------------------------------------------------------------------

# Canonical colours mirror src.visualization.comparison (blue/orange).
_CMP_STYLES: list[SeriesStyle] = [
    SeriesStyle("Facebook", "#1f77b4", "o", "-"),
    SeriesStyle("Enron", "#ff7f0e", "s", "--"),
]
_CMP_DATASETS = ("facebook", "enron")


def _load_comparison_csv(csv_path: Path) -> dict[str, dict[str, dict[int, float]]]:
    """Read the frozen comparison CSV into ``{dataset: {col: {k: value}}}``."""
    out: dict[str, dict[str, dict[int, float]]] = {}
    with csv_path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            ds = out.setdefault(row["dataset"], {"bound_fraction": {}, "relative_decay": {}})
            k = int(row["k"])
            ds["bound_fraction"][k] = float(row["bound_fraction"])
            ds["relative_decay"][k] = float(row["relative_decay"])
    return out


def build_comparison(csv_path: Path, out_dir: Path, bw: bool = False) -> Path:
    """Render the article-styled Facebook x Enron comparison (eng-comparison_fb_enron)."""
    data = _load_comparison_csv(csv_path)

    # figsize canonical (12, 5); base font ~16 pt and linewidth ~1.2 compensate the
    # ~0.51x rescale to \textwidth (figure* span) so text lands at ~8 pt.
    base, lw, ms = 16.0, 1.2, 6.0
    ref_color = _BLACK if bw else "#555555"

    def draw(ax: plt.Axes, column: str) -> None:
        for name, st in zip(_CMP_DATASETS, _CMP_STYLES, strict=True):
            color, ls, marker = st.resolve(bw)
            ks = sorted(data[name][column])
            ax.plot(
                [float(k) for k in ks],
                [data[name][column][k] for k in ks],
                color=color,
                linestyle=ls,
                marker=marker,
                linewidth=lw,
                markersize=ms,
            )

    with plt.rc_context({"pdf.fonttype": 42, "font.size": base, "axes.linewidth": 0.8}):
        fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(12, 5))

        draw(ax_a, "bound_fraction")
        ax_a.axhline(1.0, color=ref_color, linestyle=":", linewidth=0.8)
        ax_a.set_ylabel("rr·k  (fraction of 1/k bound)")
        ax_a.set_xlabel("k")
        ax_a.set_ylim(bottom=0)
        ax_a.grid(True, linestyle="--", alpha=0.3, linewidth=0.5)

        draw(ax_b, "relative_decay")
        ax_b.set_ylabel("rr(k) / rr(k_min)")
        ax_b.set_xlabel("k")
        ax_b.set_ylim(bottom=0)
        ax_b.grid(True, linestyle="--", alpha=0.3, linewidth=0.5)

        for ax, tag in ((ax_a, "(a)"), (ax_b, "(b)")):
            _apply_log_k_axis(ax)
            ax.text(0.02, 0.96, tag, transform=ax.transAxes, va="top", ha="left")

        handles = _legend_handles(_CMP_STYLES, bw)
        handles.append(Line2D([0], [0], color=ref_color, linestyle=":", label="1/k bound"))
        fig.legend(
            handles=handles, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.06)
        )
        # Reserve a bottom margin so the single figure legend clears the "k" labels.
        fig.tight_layout(rect=[0, 0.08, 1, 1])
        return _save_pdf(fig, out_dir, "eng-comparison_fb_enron")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m scripts.article_figures",
        description="Regenerate the two KDMiLe article figures from frozen data.",
    )
    p.add_argument(
        "--fb-logs",
        type=Path,
        default=_DEFAULT_FB_LOGS,
        help="Facebook baseline logs dir (Figure 4.1 source).",
    )
    p.add_argument(
        "--comparison-csv",
        type=Path,
        default=_DEFAULT_COMPARISON_CSV,
        help="Frozen comparison CSV (Figure 4.3 source).",
    )
    p.add_argument("--out", type=Path, default=_DEFAULT_OUT, help="Output directory.")
    p.add_argument(
        "--bw",
        action="store_true",
        help="Opt in to black-and-white output (series differ by line-style "
        "pattern + marker, no colour). Default is colour.",
    )
    return p


def main(argv: list[str] | None = None) -> None:
    """Entry point: regenerate both article figures."""
    args = _build_parser().parse_args(argv)
    p1 = build_privacy_utility(args.fb_logs, args.out, bw=args.bw)
    p2 = build_comparison(args.comparison_csv, args.out, bw=args.bw)
    print(f"Saved ({'black-and-white' if args.bw else 'colour'}):")
    print(f"  {p1}")
    print(f"  {p2}")


if __name__ == "__main__":
    main()
