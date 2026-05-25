"""CSV table generator for He et al. (2009) experiment results.

Reads structured JSONL logs produced by ``experiments/run.py`` and writes one
CSV file per ``(dataset, attack)`` combination to ``results/tables/``.

Each CSV row represents one ``(k, seed)`` run and contains:

    k, seed, reid_rate, eq_group_mean, ks_D, ks_p, clustering_var

Usage::

    python -m src.visualization.tables --logs experiments/logs/
    python -m src.visualization.tables \\
        --logs experiments/logs/he2009_facebook_baseline \\
        --out results/tables \\
        --dataset facebook \\
        --attack degree
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Schema constants
# ---------------------------------------------------------------------------

#: Column names in the output CSV (order is fixed and part of the spec).
CSV_COLUMNS: tuple[str, ...] = (
    "k",
    "seed",
    "reid_rate",
    "eq_group_mean",
    "ks_D",
    "ks_p",
    "clustering_var",
)

#: Attack types recognised by the loader.  Each type produces one CSV file.
KNOWN_ATTACKS: tuple[str, ...] = ("degree", "subgraph")


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
        required field ``k`` are silently skipped.

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
                if "k" not in rec:
                    continue
                records.append(rec)
    return records


# ---------------------------------------------------------------------------
# Row extraction
# ---------------------------------------------------------------------------


def _safe_float(value: Any, default: float | None = None) -> float | None:
    """Cast *value* to float, returning *default* on failure."""
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def record_to_row(record: dict[str, Any], attack: str) -> dict[str, Any] | None:
    """Extract a CSV row dict from one JSONL *record* for the given *attack*.

    Parameters
    ----------
    record:
        A parsed JSONL record (one ``(k, seed)`` run).
    attack:
        Either ``"degree"`` or ``"subgraph"``.

    Returns
    -------
    dict or None
        A mapping ``{column: value}`` ready to be written by :class:`csv.DictWriter`,
        or ``None`` if the attack is absent from this record (so that callers
        can skip records without the requested attack field).
    """
    if attack not in KNOWN_ATTACKS:
        raise ValueError(f"Unknown attack type: {attack!r}. Expected one of {KNOWN_ATTACKS}.")

    rr_key = f"reidentification_rate_{attack}"
    if rr_key not in record:
        return None

    ks = record.get("ks_test_degree", {})
    ks_d: float | None = None
    ks_p: float | None = None
    if isinstance(ks, dict):
        ks_d = _safe_float(ks.get("D"))
        ks_p = _safe_float(ks.get("p"))

    eq = record.get("equivalence_group_size", {})
    eq_mean: float | None = None
    if isinstance(eq, dict):
        eq_mean = _safe_float(eq.get("mean"))

    return {
        "k": int(record["k"]),
        "seed": int(record.get("seed", -1)),
        "reid_rate": _safe_float(record[rr_key]),
        "eq_group_mean": eq_mean,
        "ks_D": ks_d,
        "ks_p": ks_p,
        "clustering_var": _safe_float(record.get("clustering_variation")),
    }


# ---------------------------------------------------------------------------
# Table generation
# ---------------------------------------------------------------------------


def generate_tables(
    records: list[dict[str, Any]],
    output_dir: Path,
    dataset: str,
    attacks: tuple[str, ...] = KNOWN_ATTACKS,
) -> dict[str, Path]:
    """Write one CSV per ``(dataset, attack)`` combination to *output_dir*.

    Each CSV is sorted by ``(k, seed)`` for reproducibility.

    Parameters
    ----------
    records:
        Non-empty list of records as returned by :func:`load_jsonl_records`.
    output_dir:
        Destination directory (created if absent).
    dataset:
        Dataset identifier used in the output filename, e.g. ``"facebook"``.
    attacks:
        Sequence of attack names to produce tables for.  Defaults to all
        known attacks (``"degree"`` and ``"subgraph"``).

    Returns
    -------
    dict[str, Path]
        Mapping ``{attack: csv_path}`` for every attack that produced at
        least one row.

    Raises
    ------
    ValueError
        If *records* is empty or *attacks* is empty.
    """
    if not records:
        raise ValueError("No records provided — logs_dir may be empty or contain no valid records.")
    if not attacks:
        raise ValueError("attacks must be a non-empty sequence.")

    output_dir.mkdir(parents=True, exist_ok=True)

    produced: dict[str, Path] = {}

    for attack in attacks:
        rows: list[dict[str, Any]] = []
        for rec in records:
            row = record_to_row(rec, attack)
            if row is not None:
                rows.append(row)

        if not rows:
            continue  # attack not present in this log set — skip silently

        # Sort by (k, seed) for deterministic output
        rows.sort(key=lambda r: (r["k"], r["seed"]))

        csv_path = output_dir / f"{dataset}_{attack}.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(CSV_COLUMNS))
            writer.writeheader()
            writer.writerows(rows)

        produced[attack] = csv_path

    return produced


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m src.visualization.tables",
        description="Generate per-(dataset, attack) CSV tables from JSONL experiment logs.",
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
        default=Path("results/tables"),
        help="Output directory for CSV files (default: results/tables).",
    )
    p.add_argument(
        "--dataset",
        type=str,
        default="facebook",
        help="Dataset identifier used in output filenames (default: facebook).",
    )
    p.add_argument(
        "--attacks",
        nargs="+",
        choices=list(KNOWN_ATTACKS),
        default=list(KNOWN_ATTACKS),
        help="Attack types to produce tables for (default: all).",
    )
    return p


def main(argv: list[str] | None = None) -> None:
    """Entry point for ``python -m src.visualization.tables``."""
    args = _build_parser().parse_args(argv)

    print(f"Loading records from: {args.logs}")
    records = load_jsonl_records(args.logs)
    print(f"  {len(records)} records loaded.")

    produced = generate_tables(
        records,
        output_dir=args.out,
        dataset=args.dataset,
        attacks=tuple(args.attacks),
    )

    if not produced:
        print("  No tables produced (no matching records found).")
        return

    print(f"\nSaved {len(produced)} table(s):")
    for attack, path in produced.items():
        print(f"  [{attack}] {path}")


if __name__ == "__main__":
    main()
