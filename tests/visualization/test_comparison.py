"""Tests for src/visualization/comparison.py.

Seeds in fixtures are fixed only to produce distinguishable records; their
values are irrelevant to the assertions.
"""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from src.visualization.comparison import (
    bound_fraction,
    mean_by_k,
    mean_ks_d_by_k,
    plot_comparison,
    relative_decay,
    write_comparison_csv,
)


def _make_record(k: int, seed: int, rr_subgraph: float, ks_d: float = 0.1) -> dict:
    return {
        "k": k,
        "seed": seed,
        "reidentification_rate_subgraph": rr_subgraph,
        "ks_test_degree": {"D": ks_d, "p": 0.5},
    }


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------


class TestMeanByK:
    def test_averages_across_seeds(self):
        recs = [
            _make_record(2, 42, 0.10),
            _make_record(2, 1337, 0.20),
            _make_record(5, 42, 0.05),
        ]
        out = mean_by_k(recs, "reidentification_rate_subgraph")
        assert out == {2: pytest.approx(0.15), 5: pytest.approx(0.05)}

    def test_missing_field_counts_as_zero(self):
        recs = [_make_record(2, 42, 0.10), {"k": 2, "seed": 1}]
        out = mean_by_k(recs, "reidentification_rate_subgraph")
        assert out[2] == pytest.approx(0.05)

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            mean_by_k([], "reidentification_rate_subgraph")

    def test_keys_sorted(self):
        recs = [_make_record(20, 1, 0.01), _make_record(2, 1, 0.5), _make_record(10, 1, 0.1)]
        out = mean_by_k(recs, "reidentification_rate_subgraph")
        assert list(out) == [2, 10, 20]


class TestMeanKsDByK:
    def test_extracts_nested_d(self):
        recs = [_make_record(2, 42, 0.1, ks_d=0.3), _make_record(2, 1, 0.1, ks_d=0.5)]
        out = mean_ks_d_by_k(recs)
        assert out[2] == pytest.approx(0.4)


# ---------------------------------------------------------------------------
# Normalisations
# ---------------------------------------------------------------------------


class TestNormalisations:
    def test_bound_fraction_is_rr_times_k(self):
        assert bound_fraction({2: 0.124, 20: 0.057}) == {
            2: pytest.approx(0.248),
            20: pytest.approx(1.14),
        }

    def test_bound_fraction_flags_violation_above_one(self):
        # Enron k=20 crosses the 1/k bound under d=1 (achado B1).
        assert bound_fraction({20: 0.0569})[20] > 1.0

    def test_relative_decay_base_is_one(self):
        out = relative_decay({2: 0.8, 5: 0.4, 20: 0.0})
        assert out[2] == pytest.approx(1.0)
        assert out[5] == pytest.approx(0.5)
        assert out[20] == pytest.approx(0.0)

    def test_relative_decay_zero_base_is_safe(self):
        assert relative_decay({2: 0.0, 5: 0.0}) == {2: 0.0, 5: 0.0}

    def test_relative_decay_empty(self):
        assert relative_decay({}) == {}


# ---------------------------------------------------------------------------
# Plot + CSV (smoke)
# ---------------------------------------------------------------------------


class TestPlotComparison:
    def test_writes_png(self, tmp_path: Path):
        paths = plot_comparison(
            {2: 0.79, 5: 0.41, 20: 0.0}, {2: 0.12, 5: 0.10, 20: 0.057}, output_dir=tmp_path
        )
        assert paths["png"].exists()
        assert "pdf" not in paths

    def test_writes_pdf_when_requested(self, tmp_path: Path):
        paths = plot_comparison({2: 0.79}, {2: 0.12}, output_dir=tmp_path, write_pdf=True)
        assert paths["png"].exists() and paths["pdf"].exists()

    def test_creates_output_dir(self, tmp_path: Path):
        out = tmp_path / "nested" / "assets"
        plot_comparison({2: 0.5}, {2: 0.1}, output_dir=out)
        assert out.exists()


class TestWriteComparisonCsv:
    def test_csv_has_one_row_per_dataset_k(self, tmp_path: Path):
        path = write_comparison_csv(
            {2: 0.79, 20: 0.0},
            {2: 0.12, 20: 0.057},
            {2: 0.0, 20: 0.65},
            {2: 0.04, 20: 0.13},
            tmp_path / "c.csv",
        )
        with path.open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        assert len(rows) == 4
        datasets = {r["dataset"] for r in rows}
        assert datasets == {"facebook", "enron"}
        enron_k20 = next(r for r in rows if r["dataset"] == "enron" and r["k"] == "20")
        assert float(enron_k20["bound_fraction"]) > 1.0  # B1 crossing
