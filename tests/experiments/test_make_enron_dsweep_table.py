"""Unit tests for experiments/make_enron_dsweep_table.py (issue #214).

Covers:
    - load_results: parses valid JSONL; skips blank lines; raises on bad JSON.
    - group_by_kd: groups runs by (k, d) pair correctly.
    - mean_std: correct mean/std; std=0 for single-element list.
    - fmt: formatting with correct digits and None handling.
    - main(): end-to-end — writes the output file with expected sections.

Seeds fixed to small deterministic values per docs/regras_sementes.md (tests
require deterministic outputs, not production runs).
"""

from __future__ import annotations

import json
import statistics
from pathlib import Path

import pytest

from experiments.make_enron_dsweep_table import (
    fmt,
    group_by_kd,
    load_results,
    main,
    mean_std,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_run(k: int, d: int, seed: int, rr_sub: float = 0.10, rr_deg: float = 0.01) -> dict:
    """Return a minimal JSONL-like run dict with all keys the parser reads."""
    return {
        "k": k,
        "d": d,
        "seed": seed,
        "experiment": "test_dsweep",
        "verdict": "SUCCESS_PARTIAL",
        "partition_backend": "pymetis",
        "validate_k_anonymity": {
            "valid": False,
            "coverage_fraction": 0.999,
            "deficit_fully_structural": True,
        },
        "reidentification_rate_degree": rr_deg,
        "reidentification_rate_subgraph": rr_sub,
        "equivalence_group_size": {"mean": float(k * d), "median": k * d},
        "ks_test_degree": {"D": 0.05, "p": 1e-10},
        "clustering_variation": 0.02,
    }


def _write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(r) for r in records) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# load_results
# ---------------------------------------------------------------------------


class TestLoadResults:
    def test_parses_all_records(self, tmp_path: Path) -> None:
        records = [_make_run(2, 2, 42), _make_run(2, 2, 1337)]
        log = tmp_path / "test.jsonl"
        _write_jsonl(log, records)
        loaded = load_results(log)
        assert len(loaded) == 2
        assert loaded[0]["k"] == 2
        assert loaded[0]["d"] == 2
        assert loaded[0]["seed"] == 42

    def test_skips_blank_lines(self, tmp_path: Path) -> None:
        log = tmp_path / "test.jsonl"
        log.write_text(
            json.dumps(_make_run(2, 5, 42)) + "\n\n" + json.dumps(_make_run(5, 5, 42)) + "\n",
            encoding="utf-8",
        )
        loaded = load_results(log)
        assert len(loaded) == 2

    def test_raises_on_invalid_json(self, tmp_path: Path) -> None:
        log = tmp_path / "bad.jsonl"
        log.write_text("not-json\n", encoding="utf-8")
        with pytest.raises(json.JSONDecodeError):
            load_results(log)

    def test_empty_file_returns_empty_list(self, tmp_path: Path) -> None:
        log = tmp_path / "empty.jsonl"
        log.write_text("", encoding="utf-8")
        assert load_results(log) == []


# ---------------------------------------------------------------------------
# group_by_kd
# ---------------------------------------------------------------------------


class TestGroupByKd:
    def test_groups_by_k_and_d(self) -> None:
        runs = [
            _make_run(2, 2, 42),
            _make_run(2, 2, 1337),
            _make_run(5, 5, 42),
        ]
        by_kd = group_by_kd(runs)
        assert set(by_kd.keys()) == {(2, 2), (5, 5)}
        assert len(by_kd[(2, 2)]) == 2
        assert len(by_kd[(5, 5)]) == 1

    def test_three_seeds_in_one_cell(self) -> None:
        runs = [_make_run(10, 5, s) for s in (42, 1337, 2718)]
        by_kd = group_by_kd(runs)
        assert len(by_kd[(10, 5)]) == 3

    def test_empty_input(self) -> None:
        assert group_by_kd([]) == {}


# ---------------------------------------------------------------------------
# mean_std
# ---------------------------------------------------------------------------


class TestMeanStd:
    def test_single_value_std_is_zero(self) -> None:
        m, s = mean_std([3.5])
        assert m == pytest.approx(3.5)
        assert s == 0.0

    def test_two_values(self) -> None:
        m, s = mean_std([1.0, 3.0])
        assert m == pytest.approx(2.0)
        assert s == pytest.approx(statistics.stdev([1.0, 3.0]))

    def test_three_values_mean(self) -> None:
        m, _ = mean_std([0.1, 0.2, 0.3])
        assert m == pytest.approx(0.2)


# ---------------------------------------------------------------------------
# fmt
# ---------------------------------------------------------------------------


class TestFmt:
    def test_none_returns_na(self) -> None:
        assert fmt(None) == "N/A"

    def test_default_4_digits(self) -> None:
        assert fmt(0.123456) == "0.1235"

    def test_custom_digits(self) -> None:
        assert fmt(0.123456, 2) == "0.12"
        assert fmt(0.123456, 6) == "0.123456"


# ---------------------------------------------------------------------------
# main() — end-to-end
# ---------------------------------------------------------------------------


class TestMain:
    def test_output_file_created(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        dsweep_log = tmp_path / "he2009_enron_dsweep.jsonl"
        out_file = tmp_path / "results_enron_dsweep.md"

        runs = [_make_run(k, d, s) for k in (2, 5) for d in (2, 5) for s in (42, 1337, 2718)]
        _write_jsonl(dsweep_log, runs)

        import experiments.make_enron_dsweep_table as mod

        monkeypatch.setattr(mod, "DSWEEP_LOG", dsweep_log)
        monkeypatch.setattr(mod, "SECONDARY_LOG", tmp_path / "absent.jsonl")
        monkeypatch.setattr(mod, "OUT_FILE", out_file)

        main()

        assert out_file.exists()
        content = out_file.read_text(encoding="utf-8")
        assert "# Resultados — d-sweep Enron" in content
        assert "## 1. Cobertura do grid" in content
        assert "## 2. Resultados consolidados" in content
        assert "## 3. Tabela bruta" in content
        assert "## 4. Análise" in content
        assert "## 5. Reprodutibilidade" in content

    def test_output_includes_all_k_sections(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        dsweep_log = tmp_path / "dsweep.jsonl"
        out_file = tmp_path / "out.md"

        runs = [
            _make_run(k, d, s) for k in (2, 5, 10, 20) for d in (2, 5) for s in (42, 1337, 2718)
        ]
        _write_jsonl(dsweep_log, runs)

        import experiments.make_enron_dsweep_table as mod

        monkeypatch.setattr(mod, "DSWEEP_LOG", dsweep_log)
        monkeypatch.setattr(mod, "SECONDARY_LOG", tmp_path / "absent.jsonl")
        monkeypatch.setattr(mod, "OUT_FILE", out_file)

        main()

        content = out_file.read_text(encoding="utf-8")
        for k in (2, 5, 10, 20):
            assert f"### k = {k}" in content

    def test_secondary_anchor_incorporated(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        dsweep_log = tmp_path / "dsweep.jsonl"
        secondary_log = tmp_path / "secondary.jsonl"
        out_file = tmp_path / "out.md"

        dsweep_runs = [_make_run(2, 2, s) for s in (42, 1337, 2718)]
        secondary_runs = [_make_run(2, 1, s) for s in (42, 1337, 2718)]
        _write_jsonl(dsweep_log, dsweep_runs)
        _write_jsonl(secondary_log, secondary_runs)

        import experiments.make_enron_dsweep_table as mod

        monkeypatch.setattr(mod, "DSWEEP_LOG", dsweep_log)
        monkeypatch.setattr(mod, "SECONDARY_LOG", secondary_log)
        monkeypatch.setattr(mod, "OUT_FILE", out_file)

        main()

        content = out_file.read_text(encoding="utf-8")
        assert "d=1" in content
        assert "carregado como âncora d=1" in content
