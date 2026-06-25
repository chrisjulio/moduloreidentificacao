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
    aggregate_by_k_d,
    load_jsonl_records,
    load_jsonl_records_combined,
    plot_privacy_utility,
    plot_privacy_utility_dsweep,
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
    d: int = 1,
) -> dict:
    """Build a minimal valid JSONL record with controllable metric values."""
    return {
        "k": k,
        "d": d,
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


@pytest.fixture
def dsweep_records() -> list[dict]:
    """48 records: k in {2,5,10,20} x d in {1,2,5,10} x 3 seeds (the d-sweep grid)."""
    records = []
    for k in [2, 5, 10, 20]:
        for d in [1, 2, 5, 10]:
            for seed in [42, 1337, 2718]:
                records.append(
                    _make_record(
                        k=k,
                        seed=seed,
                        d=d,
                        # Values depend on both k and d so cells are distinguishable.
                        rr_degree=0.1 / k + 0.001 * d,
                        rr_subgraph=0.8 / k + 0.001 * d,
                        clust_var=0.02 * k + 0.005 * d,
                        ks_d=0.05 * k,
                    )
                )
    return records


@pytest.fixture
def dsweep_logs_dir(tmp_path: Path, dsweep_records: list[dict]) -> Path:
    """Temporary directory with a single JSONL file containing the d-sweep grid."""
    _write_jsonl(tmp_path / "dsweep.jsonl", dsweep_records)
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
# aggregate_by_k_d (d-aware)
# ---------------------------------------------------------------------------


class TestAggregateByKD:
    def test_keys_are_k_d_pairs(self, dsweep_records: list[dict]):
        stats = aggregate_by_k_d(dsweep_records)
        assert set(stats.keys()) == {(k, d) for k in [2, 5, 10, 20] for d in [1, 2, 5, 10]}

    def test_sixteen_cells(self, dsweep_records: list[dict]):
        stats = aggregate_by_k_d(dsweep_records)
        assert len(stats) == 16

    def test_keys_are_sorted(self, dsweep_records: list[dict]):
        stats = aggregate_by_k_d(dsweep_records)
        assert list(stats.keys()) == sorted(stats.keys())

    def test_all_metric_keys_present(self, dsweep_records: list[dict]):
        stats = aggregate_by_k_d(dsweep_records)
        for cell in stats.values():
            assert set(cell.keys()) == {"rr_degree", "rr_subgraph", "clust_var", "ks_d"}
            for v in cell.values():
                assert "mean" in v and "std" in v

    def test_cell_mean_isolates_k_and_d(self, dsweep_records: list[dict]):
        # rr_degree = 0.1/k + 0.001*d ; for (k=2, d=5): 0.05 + 0.005 = 0.055
        stats = aggregate_by_k_d(dsweep_records)
        assert stats[(2, 5)]["rr_degree"]["mean"] == pytest.approx(0.055)

    def test_distinct_d_give_distinct_means(self, dsweep_records: list[dict]):
        stats = aggregate_by_k_d(dsweep_records)
        means = {d: stats[(2, d)]["rr_degree"]["mean"] for d in [1, 2, 5, 10]}
        assert len(set(means.values())) == 4

    def test_std_zero_within_balanced_cell(self, dsweep_records: list[dict]):
        # Each (k, d) cell has 3 seeds with identical metric values → std 0.
        stats = aggregate_by_k_d(dsweep_records)
        assert stats[(10, 2)]["rr_degree"]["std"] == pytest.approx(0.0)

    def test_raises_on_empty_records(self):
        with pytest.raises(ValueError, match="No records"):
            aggregate_by_k_d([])

    def test_fallback_d_one_when_field_absent(self):
        records = []
        for seed in range(3):
            rec = _make_record(k=5, seed=seed)
            del rec["d"]
            records.append(rec)
        stats = aggregate_by_k_d(records)
        assert set(stats.keys()) == {(5, 1)}


class TestAggregateByKBackCompat:
    """aggregate_by_k must keep its pre-d-sweep behaviour (pools across d)."""

    def test_keys_are_plain_k(self, sample_records: list[dict]):
        stats = aggregate_by_k(sample_records)
        assert set(stats.keys()) == {2, 5, 10, 20}

    def test_unchanged_for_baseline_logs(self, sample_records: list[dict]):
        # sample_records are uniform d=1, so per-k stats are unaffected.
        stats = aggregate_by_k(sample_records)
        assert stats[2]["rr_degree"]["mean"] == pytest.approx(0.05)

    def test_pools_across_d(self, dsweep_records: list[dict]):
        # For k=2, rr_degree spans d in {1,2,5,10}: 0.0501..0.0510 → mean 0.05055.
        stats = aggregate_by_k(dsweep_records)
        expected = sum(0.05 + 0.001 * d for d in [1, 2, 5, 10]) / 4
        assert stats[2]["rr_degree"]["mean"] == pytest.approx(expected)


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

    def test_no_suptitle_still_produces_files(self, tmp_path: Path, sample_records: list[dict]):
        """show_suptitle=False (LaTeX inclusion) must produce valid files."""
        stats = aggregate_by_k(sample_records)
        pdf, png = plot_privacy_utility(stats, output_dir=tmp_path, show_suptitle=False)
        assert pdf.exists() and pdf.stat().st_size > 0
        assert png.exists() and png.stat().st_size > 0

    def _capture_subplots(self, monkeypatch) -> dict:
        """Patch plt.subplots in the module to record the (nrows, ncols, figsize)."""
        import src.visualization.privacy_utility as mod

        captured: dict = {}
        real_subplots = mod.plt.subplots

        def spy(nrows=1, ncols=1, *args, **kwargs):
            captured["nrows"], captured["ncols"] = nrows, ncols
            captured["figsize"] = kwargs.get("figsize")
            return real_subplots(nrows, ncols, *args, **kwargs)

        monkeypatch.setattr(mod.plt, "subplots", spy)
        return captured

    def test_default_layout_is_stacked(
        self, tmp_path: Path, sample_records: list[dict], monkeypatch
    ):
        """Default layout must be the canonical stacked geometry (2x1, portrait 7x8)."""
        captured = self._capture_subplots(monkeypatch)
        stats = aggregate_by_k(sample_records)
        plot_privacy_utility(stats, output_dir=tmp_path)
        assert (captured["nrows"], captured["ncols"]) == (2, 1)
        assert captured["figsize"] == (7, 8)

    def test_side_by_side_layout_geometry(
        self, tmp_path: Path, sample_records: list[dict], monkeypatch
    ):
        """layout='side-by-side' must lay panels in a 1x2 grid sized to \\textwidth."""
        captured = self._capture_subplots(monkeypatch)
        stats = aggregate_by_k(sample_records)
        plot_privacy_utility(stats, output_dir=tmp_path, layout="side-by-side")
        assert (captured["nrows"], captured["ncols"]) == (1, 2)
        assert captured["figsize"] == (6.1, 2.7)

    def test_side_by_side_layout_produces_files(self, tmp_path: Path, sample_records: list[dict]):
        """The opt-in side-by-side layout must produce valid files."""
        stats = aggregate_by_k(sample_records)
        pdf, png = plot_privacy_utility(stats, output_dir=tmp_path, layout="side-by-side")
        assert pdf.exists() and pdf.stat().st_size > 0
        assert png.exists() and png.stat().st_size > 0

    def test_unknown_layout_raises(self, tmp_path: Path, sample_records: list[dict]):
        stats = aggregate_by_k(sample_records)
        with pytest.raises(ValueError, match="Unknown layout"):
            plot_privacy_utility(stats, output_dir=tmp_path, layout="diagonal")


# ---------------------------------------------------------------------------
# plot_privacy_utility_dsweep (d-aware)
# ---------------------------------------------------------------------------


class TestPlotPrivacyUtilityDSweep:
    def test_series_creates_pdf_and_png(self, tmp_path: Path, dsweep_records: list[dict]):
        stats = aggregate_by_k_d(dsweep_records)
        pdf, png = plot_privacy_utility_dsweep(stats, output_dir=tmp_path, layout="series")
        assert pdf.exists()
        assert png.exists()

    def test_facets_creates_pdf_and_png(self, tmp_path: Path, dsweep_records: list[dict]):
        stats = aggregate_by_k_d(dsweep_records)
        pdf, png = plot_privacy_utility_dsweep(stats, output_dir=tmp_path, layout="facets")
        assert pdf.exists()
        assert png.exists()

    def test_default_layout_is_series(self, tmp_path: Path, dsweep_records: list[dict]):
        stats = aggregate_by_k_d(dsweep_records)
        pdf, _png = plot_privacy_utility_dsweep(stats, output_dir=tmp_path)
        assert pdf.exists()

    def test_default_filename_stem(self, tmp_path: Path, dsweep_records: list[dict]):
        stats = aggregate_by_k_d(dsweep_records)
        pdf, png = plot_privacy_utility_dsweep(stats, output_dir=tmp_path)
        assert pdf.name == "privacy_utility_dsweep.pdf"
        assert png.name == "privacy_utility_dsweep.png"

    def test_custom_filename_stem(self, tmp_path: Path, dsweep_records: list[dict]):
        stats = aggregate_by_k_d(dsweep_records)
        pdf, png = plot_privacy_utility_dsweep(stats, output_dir=tmp_path, filename_stem="custom_d")
        assert pdf.name == "custom_d.pdf"
        assert png.name == "custom_d.png"

    def test_files_are_nonempty(self, tmp_path: Path, dsweep_records: list[dict]):
        stats = aggregate_by_k_d(dsweep_records)
        for layout in ("series", "facets"):
            pdf, png = plot_privacy_utility_dsweep(
                stats, output_dir=tmp_path, layout=layout, filename_stem=f"x_{layout}"
            )
            assert pdf.stat().st_size > 0
            assert png.stat().st_size > 0

    def test_output_dir_created_if_absent(self, tmp_path: Path, dsweep_records: list[dict]):
        stats = aggregate_by_k_d(dsweep_records)
        new_dir = tmp_path / "deep" / "nested"
        pdf, png = plot_privacy_utility_dsweep(stats, output_dir=new_dir)
        assert new_dir.exists()
        assert pdf.exists() and png.exists()

    def test_returns_absolute_paths(self, tmp_path: Path, dsweep_records: list[dict]):
        stats = aggregate_by_k_d(dsweep_records)
        pdf, png = plot_privacy_utility_dsweep(stats, output_dir=tmp_path)
        assert pdf.is_absolute()
        assert png.is_absolute()

    def test_raises_on_unknown_layout(self, tmp_path: Path, dsweep_records: list[dict]):
        stats = aggregate_by_k_d(dsweep_records)
        with pytest.raises(ValueError, match="Unknown layout"):
            plot_privacy_utility_dsweep(stats, output_dir=tmp_path, layout="spiral")

    def test_raises_on_empty_stats(self, tmp_path: Path):
        with pytest.raises(ValueError, match="No stats"):
            plot_privacy_utility_dsweep({}, output_dir=tmp_path)

    def test_single_d_does_not_crash(self, tmp_path: Path):
        # Degenerate facet grid (one column) must not raise.
        records = [_make_record(k=k, seed=s, d=2) for k in [2, 5] for s in [1, 2, 3]]
        stats = aggregate_by_k_d(records)
        pdf, _png = plot_privacy_utility_dsweep(stats, output_dir=tmp_path, layout="facets")
        assert pdf.exists()

    def test_fallback_d_one_records(self, tmp_path: Path):
        records = []
        for k in [2, 5]:
            for s in range(3):
                rec = _make_record(k=k, seed=s)
                del rec["d"]
                records.append(rec)
        stats = aggregate_by_k_d(records)
        assert set(stats.keys()) == {(2, 1), (5, 1)}
        pdf, _png = plot_privacy_utility_dsweep(stats, output_dir=tmp_path)
        assert pdf.exists()


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

    def test_main_no_suptitle_flag(self, tmp_path: Path, logs_dir: Path):
        from src.visualization.privacy_utility import main

        out_dir = tmp_path / "plots"
        main(["--logs", str(logs_dir), "--out", str(out_dir), "--no-suptitle"])
        assert (out_dir / "privacy_utility.pdf").exists()
        assert (out_dir / "privacy_utility.png").exists()

    def test_main_raises_on_missing_logs_dir(self, tmp_path: Path):
        from src.visualization.privacy_utility import main

        with pytest.raises(FileNotFoundError):
            main(["--logs", str(tmp_path / "missing"), "--out", str(tmp_path)])

    def test_main_autodetects_dsweep(self, tmp_path: Path, dsweep_logs_dir: Path):
        from src.visualization.privacy_utility import main

        out_dir = tmp_path / "plots"
        main(["--logs", str(dsweep_logs_dir), "--out", str(out_dir)])
        # More than one distinct d → d-aware plot produced by default.
        assert (out_dir / "privacy_utility_dsweep.pdf").exists()
        assert (out_dir / "privacy_utility_dsweep.png").exists()

    def test_main_dsweep_facets_layout(self, tmp_path: Path, dsweep_logs_dir: Path):
        from src.visualization.privacy_utility import main

        out_dir = tmp_path / "plots"
        main(["--logs", str(dsweep_logs_dir), "--out", str(out_dir), "--layout", "facets"])
        assert (out_dir / "privacy_utility_dsweep.pdf").exists()

    def test_main_dsweep_flag_forces_d_aware_on_single_d(self, tmp_path: Path, logs_dir: Path):
        from src.visualization.privacy_utility import main

        out_dir = tmp_path / "plots"
        # logs_dir is uniform d=1; --dsweep forces the d-aware path anyway.
        main(["--logs", str(logs_dir), "--out", str(out_dir), "--dsweep"])
        assert (out_dir / "privacy_utility_dsweep.pdf").exists()

    def test_main_baseline_path_for_single_d(self, tmp_path: Path, logs_dir: Path):
        from src.visualization.privacy_utility import main

        out_dir = tmp_path / "plots"
        # Without --dsweep and only d=1 present → baseline plot.
        main(["--logs", str(logs_dir), "--out", str(out_dir)])
        assert (out_dir / "privacy_utility.pdf").exists()
        assert not (out_dir / "privacy_utility_dsweep.pdf").exists()

    def test_main_anchor_logs_combined_with_dsweep_dir(self, tmp_path: Path) -> None:
        from src.visualization.privacy_utility import main

        anchor_dir = tmp_path / "anchor"
        anchor_dir.mkdir()
        dsweep_dir = tmp_path / "dsweep"
        dsweep_dir.mkdir()
        out_dir = tmp_path / "plots"

        anchor_records = [_make_record(k=k, seed=s, d=1) for k in [2, 5] for s in [1, 2, 3]]
        dsweep_records_local = [
            _make_record(k=k, seed=s, d=d) for k in [2, 5] for d in [2, 5] for s in [1, 2, 3]
        ]
        _write_jsonl(anchor_dir / "anchor.jsonl", anchor_records)
        _write_jsonl(dsweep_dir / "dsweep.jsonl", dsweep_records_local)

        main(
            [
                "--logs",
                str(dsweep_dir),
                "--anchor-logs",
                str(anchor_dir),
                "--out",
                str(out_dir),
            ]
        )
        assert (out_dir / "privacy_utility_dsweep.pdf").exists()


# ---------------------------------------------------------------------------
# load_jsonl_records_combined
# ---------------------------------------------------------------------------


class TestLoadJsonlRecordsCombined:
    def test_combines_records_from_two_dirs(self, tmp_path: Path) -> None:
        dir_a = tmp_path / "a"
        dir_a.mkdir()
        dir_b = tmp_path / "b"
        dir_b.mkdir()
        _write_jsonl(dir_a / "a.jsonl", [_make_record(k=2, seed=1, d=1)])
        _write_jsonl(dir_b / "b.jsonl", [_make_record(k=2, seed=1, d=2)])
        records = load_jsonl_records_combined([dir_a, dir_b])
        assert len(records) == 2

    def test_preserves_directory_order(self, tmp_path: Path) -> None:
        dir_a = tmp_path / "a"
        dir_a.mkdir()
        dir_b = tmp_path / "b"
        dir_b.mkdir()
        _write_jsonl(dir_a / "a.jsonl", [_make_record(k=2, seed=1, d=1)])
        _write_jsonl(dir_b / "b.jsonl", [_make_record(k=5, seed=1, d=2)])
        records = load_jsonl_records_combined([dir_a, dir_b])
        assert records[0]["k"] == 2
        assert records[1]["k"] == 5

    def test_skips_missing_dir_silently(self, tmp_path: Path) -> None:
        existing = tmp_path / "existing"
        existing.mkdir()
        _write_jsonl(existing / "run.jsonl", [_make_record(k=5, seed=1)])
        records = load_jsonl_records_combined([tmp_path / "nonexistent", existing])
        assert len(records) == 1

    def test_empty_list_returns_empty(self) -> None:
        assert load_jsonl_records_combined([]) == []

    def test_single_dir_behaves_like_load_jsonl_records(self, tmp_path: Path) -> None:
        _write_jsonl(tmp_path / "run.jsonl", [_make_record(k=2, seed=42)])
        assert load_jsonl_records_combined([tmp_path]) == load_jsonl_records(tmp_path)


# ---------------------------------------------------------------------------
# Enron d-sweep geometry (d∈{2,5,10}, with and without d=1 anchor)
# ---------------------------------------------------------------------------


class TestEnronDSweepPlot:
    @pytest.fixture
    def enron_dsweep_records(self) -> list[dict]:
        """36 records: k in {2,5,10,20} x d in {2,5,10} x 3 seeds (no d=1 anchor)."""
        return [
            _make_record(k=k, seed=s, d=d)
            for k in [2, 5, 10, 20]
            for d in [2, 5, 10]
            for s in [42, 1337, 2718]
        ]

    @pytest.fixture
    def enron_combined_records(self) -> list[dict]:
        """48 records: d=1 anchor from secondary + d∈{2,5,10} from dsweep."""
        anchor = [_make_record(k=k, seed=s, d=1) for k in [2, 5, 10, 20] for s in [42, 1337, 2718]]
        dsweep = [
            _make_record(k=k, seed=s, d=d)
            for k in [2, 5, 10, 20]
            for d in [2, 5, 10]
            for s in [42, 1337, 2718]
        ]
        return anchor + dsweep

    def test_dsweep_without_anchor_series_produces_files(
        self, tmp_path: Path, enron_dsweep_records: list[dict]
    ) -> None:
        stats = aggregate_by_k_d(enron_dsweep_records)
        pdf, png = plot_privacy_utility_dsweep(
            stats,
            output_dir=tmp_path,
            layout="series",
            filename_stem="enron_dsweep_series",
        )
        assert pdf.exists() and pdf.stat().st_size > 0
        assert png.exists() and png.stat().st_size > 0
        assert pdf.name == "enron_dsweep_series.pdf"

    def test_dsweep_without_anchor_facets_produces_files(
        self, tmp_path: Path, enron_dsweep_records: list[dict]
    ) -> None:
        stats = aggregate_by_k_d(enron_dsweep_records)
        pdf, _png = plot_privacy_utility_dsweep(
            stats,
            output_dir=tmp_path,
            layout="facets",
            filename_stem="enron_dsweep_facets",
        )
        assert pdf.exists() and pdf.stat().st_size > 0
        assert pdf.name == "enron_dsweep_facets.pdf"

    def test_dsweep_no_d1_in_stats(self, enron_dsweep_records: list[dict]) -> None:
        stats = aggregate_by_k_d(enron_dsweep_records)
        d_values = {d for (_k, d) in stats}
        assert 1 not in d_values
        assert d_values == {2, 5, 10}

    def test_combined_includes_d1_anchor(self, enron_combined_records: list[dict]) -> None:
        stats = aggregate_by_k_d(enron_combined_records)
        d_values = {d for (_k, d) in stats}
        assert d_values == {1, 2, 5, 10}

    def test_combined_series_produces_files(
        self, tmp_path: Path, enron_combined_records: list[dict]
    ) -> None:
        stats = aggregate_by_k_d(enron_combined_records)
        pdf, png = plot_privacy_utility_dsweep(
            stats,
            output_dir=tmp_path,
            layout="series",
            filename_stem="enron_dsweep_combined_series",
        )
        assert pdf.exists() and pdf.stat().st_size > 0
        assert png.exists() and png.stat().st_size > 0
