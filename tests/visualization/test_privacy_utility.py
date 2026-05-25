"""Tests for src/visualization/privacy_utility.py.

Seeds are fixed in all fixtures because tests must be deterministic.
The actual seed values are irrelevant — they serve only to produce
distinguishable records with controlled metric values.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.visualization.privacy_utility import (
    aggregate_by_k,
    load_jsonl_records,
    plot_privacy_utility,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_record(
    k: int,
    seed: int,
    rr_degree: float = 0.1,
    rr_subgraph: float = 0.5,
    clust_var: float = 0.05,
    ks_d: float = 0.1,
) -> dict:
    """Build a minimal valid JSONL record with controllable metric values."""
    return {
        "k": k,
        "d": 1,
        "seed": seed,
        "reidentification_rate_degree": rr_degree,
        "reidentification_rate_subgraph": rr_subgraph,
        "clustering_variation": clust_var,
        "ks_test_degree": {"D": ks_d, "p": 0.5},
        "verdict": "SUCCESS_FULL",
    }


def _write_jsonl(path: Path, records: list[dict]) -> None:
    """Serialise *records* as one JSON line each to *path*."""
    with path.open("w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec) + "\n")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_records() -> list[dict]:
    """12 records: k in {2,5,10,20} x 3 seeds with predictable metric values."""
    records = []
    for k in [2, 5, 10, 20]:
        for seed in [42, 1337, 2718]:
            records.append(
                _make_record(
                    k=k,
                    seed=seed,
                    rr_degree=0.1 / k,
                    rr_subgraph=0.8 / k,
                    clust_var=0.02 * k,
                    ks_d=0.05 * k,
                )
            )
    return records


@pytest.fixture
def logs_dir(tmp_path: Path, sample_records: list[dict]) -> Path:
    """Temporary directory with a single JSONL file containing all records."""
    _write_jsonl(tmp_path / "runs.jsonl", sample_records)
    return tmp_path


# ---------------------------------------------------------------------------
# load_jsonl_records
# ---------------------------------------------------------------------------


class TestLoadJsonlRecords:
    def test_loads_all_valid_records(self, logs_dir: Path, sample_records: list[dict]):
        records = load_jsonl_records(logs_dir)
        assert len(records) == len(sample_records)

    def test_raises_file_not_found_on_missing_dir(self, tmp_path: Path):
        with pytest.raises(FileNotFoundError, match="logs_dir not found"):
            load_jsonl_records(tmp_path / "nonexistent")

    def test_skips_invalid_json_lines(self, tmp_path: Path):
        f = tmp_path / "mixed.jsonl"
        f.write_text(
            '{"k": 2, "reidentification_rate_degree": 0.1}\n'
            "NOT_JSON\n"
            '{"k": 5, "reidentification_rate_degree": 0.2}\n',
            encoding="utf-8",
        )
        records = load_jsonl_records(tmp_path)
        assert len(records) == 2

    def test_skips_record_missing_k(self, tmp_path: Path):
        f = tmp_path / "missing_k.jsonl"
        f.write_text(
            '{"reidentification_rate_degree": 0.1}\n'
            '{"k": 2, "reidentification_rate_degree": 0.1}\n',
            encoding="utf-8",
        )
        records = load_jsonl_records(tmp_path)
        assert len(records) == 1

    def test_skips_record_missing_rr_degree(self, tmp_path: Path):
        f = tmp_path / "missing_rr.jsonl"
        f.write_text(
            '{"k": 2}\n{"k": 2, "reidentification_rate_degree": 0.1}\n',
            encoding="utf-8",
        )
        records = load_jsonl_records(tmp_path)
        assert len(records) == 1

    def test_empty_directory_returns_empty_list(self, tmp_path: Path):
        records = load_jsonl_records(tmp_path)
        assert records == []

    def test_loads_from_nested_subdirectory(self, tmp_path: Path):
        nested = tmp_path / "deep" / "nested"
        nested.mkdir(parents=True)
        _write_jsonl(
            nested / "run.jsonl",
            [_make_record(k=2, seed=1)],
        )
        records = load_jsonl_records(tmp_path)
        assert len(records) == 1

    def test_skips_blank_lines(self, tmp_path: Path):
        f = tmp_path / "blanks.jsonl"
        f.write_text(
            '\n{"k": 2, "reidentification_rate_degree": 0.1}\n\n',
            encoding="utf-8",
        )
        records = load_jsonl_records(tmp_path)
        assert len(records) == 1

    def test_aggregates_across_multiple_jsonl_files(self, tmp_path: Path):
        _write_jsonl(tmp_path / "a.jsonl", [_make_record(k=2, seed=1)])
        _write_jsonl(tmp_path / "b.jsonl", [_make_record(k=5, seed=2)])
        records = load_jsonl_records(tmp_path)
        assert len(records) == 2


# ---------------------------------------------------------------------------
# aggregate_by_k
# ---------------------------------------------------------------------------


class TestAggregateByK:
    def test_k_values_match_records(self, sample_records: list[dict]):
        stats = aggregate_by_k(sample_records)
        assert set(stats.keys()) == {2, 5, 10, 20}

    def test_all_metric_keys_present(self, sample_records: list[dict]):
        stats = aggregate_by_k(sample_records)
        for k_stats in stats.values():
            assert set(k_stats.keys()) == {"rr_degree", "rr_subgraph", "clust_var", "ks_d"}
            for v in k_stats.values():
                assert "mean" in v and "std" in v

    def test_mean_value_correct(self, sample_records: list[dict]):
        # k=2: rr_degree = 0.1/2 = 0.05 for every seed
        stats = aggregate_by_k(sample_records)
        assert stats[2]["rr_degree"]["mean"] == pytest.approx(0.05)

    def test_std_zero_when_all_seeds_identical(self):
        records = [_make_record(k=5, seed=s, rr_degree=0.3) for s in [1, 2, 3]]
        stats = aggregate_by_k(records)
        assert stats[5]["rr_degree"]["std"] == pytest.approx(0.0)

    def test_std_nonzero_when_seeds_differ(self):
        records = [
            _make_record(k=5, seed=1, rr_degree=0.1),
            _make_record(k=5, seed=2, rr_degree=0.3),
            _make_record(k=5, seed=3, rr_degree=0.5),
        ]
        stats = aggregate_by_k(records)
        assert stats[5]["rr_degree"]["std"] > 0.0

    def test_raises_on_empty_records(self):
        with pytest.raises(ValueError, match="No records"):
            aggregate_by_k([])

    def test_single_k_single_seed(self):
        records = [_make_record(k=2, seed=42, rr_degree=0.25)]
        stats = aggregate_by_k(records)
        assert stats[2]["rr_degree"]["mean"] == pytest.approx(0.25)
        assert stats[2]["rr_degree"]["std"] == pytest.approx(0.0)

    def test_ks_nested_dict_parsed_correctly(self):
        records = [
            _make_record(k=5, seed=1, ks_d=0.42),
        ]
        stats = aggregate_by_k(records)
        assert stats[5]["ks_d"]["mean"] == pytest.approx(0.42)

    def test_result_keys_are_sorted(self, sample_records: list[dict]):
        stats = aggregate_by_k(sample_records)
        assert list(stats.keys()) == sorted(stats.keys())

    def test_missing_rr_subgraph_defaults_to_zero(self):
        rec = _make_record(k=5, seed=1)
        del rec["reidentification_rate_subgraph"]
        stats = aggregate_by_k([rec])
        assert stats[5]["rr_subgraph"]["mean"] == pytest.approx(0.0)

    def test_missing_clustering_variation_defaults_to_zero(self):
        rec = _make_record(k=5, seed=1)
        del rec["clustering_variation"]
        stats = aggregate_by_k([rec])
        assert stats[5]["clust_var"]["mean"] == pytest.approx(0.0)

    def test_clust_var_values_correct(self, sample_records: list[dict]):
        # k=10: clust_var = 0.02*10 = 0.2 for every seed
        stats = aggregate_by_k(sample_records)
        assert stats[10]["clust_var"]["mean"] == pytest.approx(0.2)

    def test_ks_d_values_correct(self, sample_records: list[dict]):
        # k=20: ks_d = 0.05*20 = 1.0 for every seed
        stats = aggregate_by_k(sample_records)
        assert stats[20]["ks_d"]["mean"] == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# plot_privacy_utility
# ---------------------------------------------------------------------------


class TestPlotPrivacyUtility:
    def test_creates_pdf_and_png(self, tmp_path: Path, sample_records: list[dict]):
        stats = aggregate_by_k(sample_records)
        pdf, png = plot_privacy_utility(stats, output_dir=tmp_path)
        assert pdf.exists()
        assert png.exists()

    def test_output_file_extensions(self, tmp_path: Path, sample_records: list[dict]):
        stats = aggregate_by_k(sample_records)
        pdf, png = plot_privacy_utility(stats, output_dir=tmp_path)
        assert pdf.suffix == ".pdf"
        assert png.suffix == ".png"

    def test_default_filename_stem(self, tmp_path: Path, sample_records: list[dict]):
        stats = aggregate_by_k(sample_records)
        pdf, png = plot_privacy_utility(stats, output_dir=tmp_path)
        assert pdf.name == "privacy_utility.pdf"
        assert png.name == "privacy_utility.png"

    def test_custom_filename_stem(self, tmp_path: Path, sample_records: list[dict]):
        stats = aggregate_by_k(sample_records)
        pdf, png = plot_privacy_utility(stats, output_dir=tmp_path, filename_stem="custom_plot")
        assert pdf.name == "custom_plot.pdf"
        assert png.name == "custom_plot.png"

    def test_output_dir_created_if_absent(self, tmp_path: Path, sample_records: list[dict]):
        stats = aggregate_by_k(sample_records)
        new_dir = tmp_path / "deep" / "nested"
        pdf, png = plot_privacy_utility(stats, output_dir=new_dir)
        assert new_dir.exists()
        assert pdf.exists() and png.exists()

    def test_pdf_file_is_nonempty(self, tmp_path: Path, sample_records: list[dict]):
        stats = aggregate_by_k(sample_records)
        pdf, _ = plot_privacy_utility(stats, output_dir=tmp_path)
        assert pdf.stat().st_size > 0

    def test_png_file_is_nonempty(self, tmp_path: Path, sample_records: list[dict]):
        stats = aggregate_by_k(sample_records)
        _, png = plot_privacy_utility(stats, output_dir=tmp_path)
        assert png.stat().st_size > 0

    def test_single_k_does_not_crash(self, tmp_path: Path):
        """Degenerate case: only one k value — no error bars, but must not raise."""
        records = [_make_record(k=5, seed=s) for s in [1, 2, 3]]
        stats = aggregate_by_k(records)
        pdf, _png = plot_privacy_utility(stats, output_dir=tmp_path)
        assert pdf.exists()

    def test_returns_absolute_paths(self, tmp_path: Path, sample_records: list[dict]):
        stats = aggregate_by_k(sample_records)
        pdf, png = plot_privacy_utility(stats, output_dir=tmp_path)
        assert pdf.is_absolute()
        assert png.is_absolute()

    def test_overwrites_existing_files(self, tmp_path: Path, sample_records: list[dict]):
        stats = aggregate_by_k(sample_records)
        # first call
        plot_privacy_utility(stats, output_dir=tmp_path)
        first_size = (tmp_path / "privacy_utility.png").stat().st_size
        # second call should overwrite without error
        plot_privacy_utility(stats, output_dir=tmp_path)
        second_size = (tmp_path / "privacy_utility.png").stat().st_size
        assert second_size > 0
        assert first_size == second_size  # identical data → identical output


# ---------------------------------------------------------------------------
# main (CLI integration)
# ---------------------------------------------------------------------------


class TestMain:
    def test_main_produces_output_files(self, tmp_path: Path, logs_dir: Path):
        from src.visualization.privacy_utility import main

        out_dir = tmp_path / "plots"
        main(["--logs", str(logs_dir), "--out", str(out_dir)])
        assert (out_dir / "privacy_utility.pdf").exists()
        assert (out_dir / "privacy_utility.png").exists()

    def test_main_custom_stem(self, tmp_path: Path, logs_dir: Path):
        from src.visualization.privacy_utility import main

        out_dir = tmp_path / "plots"
        main(["--logs", str(logs_dir), "--out", str(out_dir), "--stem", "baseline"])
        assert (out_dir / "baseline.pdf").exists()
        assert (out_dir / "baseline.png").exists()

    def test_main_raises_on_missing_logs_dir(self, tmp_path: Path):
        from src.visualization.privacy_utility import main

        with pytest.raises(FileNotFoundError):
            main(["--logs", str(tmp_path / "missing"), "--out", str(tmp_path)])
