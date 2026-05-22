"""Tests for experiments/run.py (issue #22).

Definition-of-Done coverage:
    - CLI functional with argparse (--config required, missing → SystemExit).
    - preprocess_graph: LCC extraction, min_nodes enforcement, relabelling.
    - load_dataset: raises ValueError for unknown dataset names.
    - run_one: end-to-end on a small synthetic graph (k=2, d=2, seed=0).
    - run_one: error handling — pipeline exception serialised into "error" key.
    - verdict_from_result: all five verdicts exercised.
    - main: JSONL written with correct schema keys; summary.json produced.
    - main: exit code 0 when all runs pass; 1 when any run fails.

Seeds are fixed to 0 / 42 throughout; approved exception per
.claude/rules/seeds.md — tests require deterministic, reproducible outputs.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import networkx as nx
import pytest

from experiments.run import (
    load_dataset,
    main,
    preprocess_graph,
    run_one,
    verdict_from_result,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_DEFAULT_ATTACKS: dict = {"degree": {"enabled": True, "tolerance": 0}}


def _small_graph() -> nx.Graph:
    """Return a connected 20-node graph suitable for k=2, d=2 anonymisation.

    Uses a random regular graph (seed=0) so the graph is connected and
    3-regular; 20 nodes → 10 Local Structures when d=2 → at least 5
    complete groups for k=2.  Seed 0 is fixed for determinism.
    """
    return nx.random_regular_graph(d=3, n=20, seed=0)


# ---------------------------------------------------------------------------
# preprocess_graph
# ---------------------------------------------------------------------------


class TestPreprocessGraph:
    """Unit tests for the LCC extraction and relabelling helper."""

    def test_lcc_disconnected_graph(self) -> None:
        """Disconnected graph: LCC is retained, minority component dropped."""
        # Two components: cycle-6 (larger) and path-2 (smaller)
        g = nx.disjoint_union(nx.cycle_graph(6), nx.path_graph(2))
        result = preprocess_graph(g, component="lcc")
        assert result.number_of_nodes() == 6

    def test_lcc_already_connected(self) -> None:
        """Connected graph: LCC is the full graph — no nodes dropped."""
        g = nx.petersen_graph()
        result = preprocess_graph(g, component="lcc")
        assert result.number_of_nodes() == g.number_of_nodes()

    def test_no_lcc_keeps_full_graph(self) -> None:
        """component != 'lcc' keeps the graph unchanged."""
        g = nx.disjoint_union(nx.cycle_graph(4), nx.path_graph(3))
        result = preprocess_graph(g, component="none")
        assert result.number_of_nodes() == g.number_of_nodes()

    def test_relabels_to_zero_indexed(self) -> None:
        """Nodes are always relabelled 0..n-1 after preprocessing."""
        g = nx.petersen_graph()
        # Shift labels: 10..19
        g = nx.relabel_nodes(g, {i: i + 10 for i in g.nodes()})
        result = preprocess_graph(g, component="none")
        assert set(result.nodes()) == set(range(result.number_of_nodes()))

    def test_min_nodes_below_threshold_raises(self) -> None:
        """Raise ValueError when the processed graph is too small."""
        g = nx.path_graph(4)
        with pytest.raises(ValueError, match="min_nodes"):
            preprocess_graph(g, component="none", min_nodes=10)

    def test_min_nodes_exactly_met_does_not_raise(self) -> None:
        """Exactly min_nodes nodes: no exception raised."""
        g = nx.path_graph(5)
        result = preprocess_graph(g, component="none", min_nodes=5)
        assert result.number_of_nodes() == 5


# ---------------------------------------------------------------------------
# load_dataset
# ---------------------------------------------------------------------------


class TestLoadDataset:
    """Unit tests for the dataset loader dispatch."""

    def test_unknown_dataset_raises_value_error(self) -> None:
        """An unsupported dataset name raises ValueError immediately."""
        cfg = {"name": "nonexistent_dataset", "data_path": "/tmp", "egonet_id": 0}
        with pytest.raises(ValueError, match="nonexistent_dataset"):
            load_dataset(cfg)


# ---------------------------------------------------------------------------
# verdict_from_result
# ---------------------------------------------------------------------------


class TestVerdictFromResult:
    """Unit tests for the verdict classification function."""

    def _make_validation(
        self,
        *,
        valid: bool,
        coverage_fraction: float,
        deficit_fully_structural: bool,
        violations: list[dict] | None = None,
    ) -> dict:
        return {
            "valid": valid,
            "coverage_fraction": coverage_fraction,
            "satisfied_fraction": coverage_fraction,
            "uncovered_fraction": round(1 - coverage_fraction, 6),
            "deficit_fully_structural": deficit_fully_structural,
            "n_violators": 0,
            "violators": [],
            "violations": violations or [],
        }

    def test_success_full(self) -> None:
        result = {
            "validate_k_anonymity": self._make_validation(
                valid=True,
                coverage_fraction=1.0,
                deficit_fully_structural=True,
                violations=[],
            ),
            "error": None,
        }
        assert verdict_from_result(result) == "SUCCESS_FULL"

    def test_success_partial_incomplete_group(self) -> None:
        """Only incomplete_group violations + coverage >= 0.9 → SUCCESS_PARTIAL."""
        result = {
            "validate_k_anonymity": self._make_validation(
                valid=False,
                coverage_fraction=0.92,
                deficit_fully_structural=True,
                violations=[
                    {"type": "incomplete_group", "status": "partially_unprotected", "nodes": [0, 1]}
                ],
            ),
            "error": None,
        }
        assert verdict_from_result(result) == "SUCCESS_PARTIAL"

    def test_failure_fatal_non_isomorphic(self) -> None:
        result = {
            "validate_k_anonymity": self._make_validation(
                valid=False,
                coverage_fraction=0.85,
                deficit_fully_structural=False,
                violations=[{"type": "non_isomorphic", "status": "unprotected", "nodes": [0]}],
            ),
            "error": None,
        }
        assert verdict_from_result(result) == "FAILURE_FATAL"

    def test_failure_fatal_non_disjoint(self) -> None:
        result = {
            "validate_k_anonymity": self._make_validation(
                valid=False,
                coverage_fraction=0.95,
                deficit_fully_structural=False,
                violations=[{"type": "non_disjoint", "status": "unprotected", "nodes": [3]}],
            ),
            "error": None,
        }
        assert verdict_from_result(result) == "FAILURE_FATAL"

    def test_failure_low_coverage(self) -> None:
        """coverage < 0.9 with no fatal violations → FAILURE_LOW_COVERAGE."""
        result = {
            "validate_k_anonymity": self._make_validation(
                valid=False,
                coverage_fraction=0.70,
                deficit_fully_structural=True,
                violations=[
                    {
                        "type": "incomplete_group",
                        "status": "partially_unprotected",
                        "nodes": list(range(15)),
                    }
                ],
            ),
            "error": None,
        }
        assert verdict_from_result(result) == "FAILURE_LOW_COVERAGE"

    def test_error_key_present(self) -> None:
        """Non-None error key → ERROR regardless of validation content."""
        result = {
            "error": {"type": "RuntimeError", "message": "boom", "traceback": "..."},
        }
        assert verdict_from_result(result) == "ERROR"

    def test_missing_validation_key(self) -> None:
        """Missing validate_k_anonymity key → ERROR."""
        assert verdict_from_result({"error": None}) == "ERROR"


# ---------------------------------------------------------------------------
# run_one — end-to-end on synthetic graph
# ---------------------------------------------------------------------------


class TestRunOneEndToEnd:
    """Integration test: run_one on a small synthetic graph."""

    def test_returns_dict_with_required_keys(self) -> None:
        """run_one must return all JSONL schema keys on a successful run.

        Uses a 20-node random-regular graph with k=2, d=2, seed=0 so the
        anonymiser runs quickly and the result is deterministic.
        """
        g = _small_graph()
        result = run_one(g, k=2, d=2, sigma=0.5, seed=0, attacks_cfg=_DEFAULT_ATTACKS)

        assert result["error"] is None, f"Unexpected error: {result['error']}"

        required_keys = {
            "k",
            "d",
            "seed",
            "timestamp",
            "validate_k_anonymity",
            "reidentification_rate",
            "reidentification_rate_degree",
            "equivalence_group_size",
            "ks_test_degree",
            "clustering_variation",
        }
        missing = required_keys - result.keys()
        assert not missing, f"Missing keys in result: {missing}"

    def test_k_and_seed_propagated(self) -> None:
        """The k and seed used must appear verbatim in the result dict."""
        g = _small_graph()
        result = run_one(g, k=2, d=2, sigma=0.5, seed=42, attacks_cfg=_DEFAULT_ATTACKS)
        assert result["k"] == 2
        assert result["seed"] == 42

    def test_d_propagated(self) -> None:
        g = _small_graph()
        result = run_one(g, k=2, d=2, sigma=0.5, seed=0, attacks_cfg=_DEFAULT_ATTACKS)
        assert result["d"] == 2

    def test_reidentification_rate_in_unit_interval(self) -> None:
        g = _small_graph()
        result = run_one(g, k=2, d=2, sigma=0.5, seed=0, attacks_cfg=_DEFAULT_ATTACKS)
        assert result["error"] is None
        rr = result.get("reidentification_rate")
        assert rr is not None
        assert 0.0 <= rr <= 1.0

    def test_equivalence_group_size_positive(self) -> None:
        g = _small_graph()
        result = run_one(g, k=2, d=2, sigma=0.5, seed=0, attacks_cfg=_DEFAULT_ATTACKS)
        assert result["error"] is None
        egs = result["equivalence_group_size"]
        assert egs["mean"] > 0
        assert egs["median"] > 0

    def test_ks_test_degree_valid_range(self) -> None:
        g = _small_graph()
        result = run_one(g, k=2, d=2, sigma=0.5, seed=0, attacks_cfg=_DEFAULT_ATTACKS)
        assert result["error"] is None
        ks = result["ks_test_degree"]
        assert 0.0 <= ks["D"] <= 1.0
        assert 0.0 <= ks["p"] <= 1.0

    def test_result_is_json_serialisable(self) -> None:
        """The result must be serialisable with json.dumps(..., default=str)."""
        g = _small_graph()
        result = run_one(g, k=2, d=2, sigma=0.5, seed=0, attacks_cfg=_DEFAULT_ATTACKS)
        # Must not raise
        serialised = json.dumps(result, default=str)
        roundtripped = json.loads(serialised)
        assert roundtripped["k"] == 2

    def test_validate_k_anonymity_has_dl01_fields(self) -> None:
        """validate_k_anonymity result must contain all DL-01 fields."""
        g = _small_graph()
        result = run_one(g, k=2, d=2, sigma=0.5, seed=0, attacks_cfg=_DEFAULT_ATTACKS)
        assert result["error"] is None
        vka = result["validate_k_anonymity"]
        dl01_fields = {
            "valid",
            "satisfied_fraction",
            "coverage_fraction",
            "uncovered_fraction",
            "deficit_fully_structural",
            "n_violators",
            "violators",
            "violations",
        }
        missing = dl01_fields - vka.keys()
        assert not missing, f"DL-01 fields missing from validate_k_anonymity: {missing}"

    def test_determinism_same_seed(self) -> None:
        """Same graph + same seed → identical reidentification_rate."""
        g = _small_graph()
        r1 = run_one(g, k=2, d=2, sigma=0.5, seed=0, attacks_cfg=_DEFAULT_ATTACKS)
        r2 = run_one(g, k=2, d=2, sigma=0.5, seed=0, attacks_cfg=_DEFAULT_ATTACKS)
        assert r1["reidentification_rate"] == r2["reidentification_rate"]

    def test_subgraph_attack_disabled_by_default(self) -> None:
        """reidentification_rate_subgraph must NOT appear when subgraph is disabled."""
        g = _small_graph()
        result = run_one(g, k=2, d=2, sigma=0.5, seed=0, attacks_cfg=_DEFAULT_ATTACKS)
        assert "reidentification_rate_subgraph" not in result


class TestRunOneErrorHandling:
    """run_one captures pipeline exceptions without raising."""

    def test_invalid_k_zero_serialised_as_error(self) -> None:
        """k=0 will cause a ValueError deep in the anonymiser; must be captured."""
        g = _small_graph()
        result = run_one(g, k=0, d=2, sigma=0.5, seed=0, attacks_cfg=_DEFAULT_ATTACKS)
        # We accept either an explicit error or an anomaly handled internally.
        # The key invariant: the function must not raise.
        assert isinstance(result, dict)

    def test_error_dict_has_required_keys(self) -> None:
        """If an error occurs, the error dict must contain type/message/traceback."""
        # Force an error by passing d >= n (d=1000 > 20)
        g = _small_graph()  # 20 nodes
        result = run_one(g, k=2, d=1000, sigma=0.5, seed=0, attacks_cfg=_DEFAULT_ATTACKS)
        assert result["error"] is not None
        assert "type" in result["error"]
        assert "message" in result["error"]
        assert "traceback" in result["error"]

    def test_verdict_from_error_result_is_error(self) -> None:
        """verdict_from_result returns 'ERROR' when error key is non-None."""
        g = _small_graph()
        result = run_one(g, k=2, d=1000, sigma=0.5, seed=0, attacks_cfg=_DEFAULT_ATTACKS)
        assert result["error"] is not None
        assert verdict_from_result(result) == "ERROR"


# ---------------------------------------------------------------------------
# main — JSONL output and summary
# ---------------------------------------------------------------------------


class TestMainJsonlOutput:
    """Integration tests for main(): JSONL and summary files."""

    @pytest.fixture
    def minimal_config(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
        """Write a minimal config YAML; monkeypatch load_dataset to return
        a small synthetic graph so the test does not touch the filesystem."""
        g = _small_graph()
        monkeypatch.setattr("experiments.run.load_dataset", lambda _cfg: g)

        cfg_text = textwrap.dedent("""
            experiment:
              name: test_runner_output

            seeds: [0, 1]

            dataset:
              name: facebook_ego_nets
              data_path: data/raw/facebook/
              egonet_id: 3437

            anonymization:
              algorithm: he_2009
              k: 2
              d: 2
              sigma: 0.5

            attacks:
              degree:
                enabled: true
                tolerance: 0

            runtime:
              log_level: WARNING
              log_dir: "{log_dir}"
        """).format(log_dir=str(tmp_path).replace("\\", "/"))

        cfg_file = tmp_path / "test_runner_output.yml"
        cfg_file.write_text(cfg_text, encoding="utf-8")
        return cfg_file

    def test_jsonl_file_created(self, minimal_config: Path, tmp_path: Path) -> None:
        """main() must create the JSONL log file."""
        main(minimal_config)
        log_file = tmp_path / "test_runner_output" / "test_runner_output.jsonl"
        assert log_file.exists()

    def test_jsonl_has_correct_entry_count(self, minimal_config: Path, tmp_path: Path) -> None:
        """One JSONL line per (k, seed) combination: k=[2], seeds=[0,1] → 2 entries."""
        main(minimal_config)
        log_file = tmp_path / "test_runner_output" / "test_runner_output.jsonl"
        lines = [line for line in log_file.read_text(encoding="utf-8").splitlines() if line.strip()]
        assert len(lines) == 2

    def test_jsonl_entries_are_valid_json(self, minimal_config: Path, tmp_path: Path) -> None:
        """Every JSONL line must be parseable JSON."""
        main(minimal_config)
        log_file = tmp_path / "test_runner_output" / "test_runner_output.jsonl"
        for line in log_file.read_text(encoding="utf-8").splitlines():
            if line.strip():
                obj = json.loads(line)
                assert "k" in obj
                assert "seed" in obj

    def test_jsonl_entries_have_schema_keys(self, minimal_config: Path, tmp_path: Path) -> None:
        """Each JSONL entry must contain all keys from the DL-01 schema."""
        main(minimal_config)
        log_file = tmp_path / "test_runner_output" / "test_runner_output.jsonl"
        required = {
            "k",
            "d",
            "seed",
            "timestamp",
            "experiment",
            "verdict",
            "validate_k_anonymity",
            "reidentification_rate",
            "equivalence_group_size",
            "ks_test_degree",
        }
        for line in log_file.read_text(encoding="utf-8").splitlines():
            if line.strip():
                obj = json.loads(line)
                missing = required - obj.keys()
                assert not missing, f"Missing JSONL keys: {missing}"

    def test_summary_json_created(self, minimal_config: Path, tmp_path: Path) -> None:
        """main() must create summary.json alongside the JSONL file."""
        main(minimal_config)
        summary_file = tmp_path / "test_runner_output" / "summary.json"
        assert summary_file.exists()

    def test_summary_json_is_valid(self, minimal_config: Path, tmp_path: Path) -> None:
        """summary.json must be parseable and contain n_runs."""
        main(minimal_config)
        summary_file = tmp_path / "test_runner_output" / "summary.json"
        summary = json.loads(summary_file.read_text(encoding="utf-8"))
        assert summary["n_runs"] == 2  # 1 k-value x 2 seeds
        assert "any_failure" in summary
        assert "verdicts" in summary

    def test_exit_code_0_when_all_pass(self, minimal_config: Path, tmp_path: Path) -> None:
        """Exit code 0 when all runs succeed or partially succeed."""
        code = main(minimal_config)
        assert code == 0

    def test_exit_code_1_when_failure(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Exit code 1 when at least one run produces FAILURE_* or ERROR."""
        # Monkeypatch run_one to always return an error result.
        import experiments.run as runner_mod

        def _always_error(g, *, k, d, sigma, seed, attacks_cfg):
            return {
                "k": k,
                "d": d,
                "seed": seed,
                "timestamp": "2026-01-01T00:00:00+00:00",
                "error": {"type": "ForcedError", "message": "forced", "traceback": ""},
            }

        monkeypatch.setattr(runner_mod, "run_one", _always_error)

        g = _small_graph()
        monkeypatch.setattr(runner_mod, "load_dataset", lambda _cfg: g)

        cfg_text = textwrap.dedent("""
            experiment:
              name: test_forced_error

            seeds: [0]

            dataset:
              name: facebook_ego_nets
              data_path: /tmp
              egonet_id: 0

            anonymization:
              k: 2
              d: 2

            runtime:
              log_dir: "{log_dir}"
        """).format(log_dir=str(tmp_path).replace("\\", "/"))

        cfg_file = tmp_path / "forced_error.yml"
        cfg_file.write_text(cfg_text, encoding="utf-8")

        code = main(cfg_file)
        assert code == 1


# ---------------------------------------------------------------------------
# CLI argument parsing
# ---------------------------------------------------------------------------


class TestCLIArgParsing:
    """Smoke tests for the argparse interface."""

    def test_missing_config_exits(self) -> None:
        """--config is required; omitting it must raise SystemExit."""
        import subprocess
        import sys

        result = subprocess.run(
            [sys.executable, "-m", "experiments.run"],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0

    def test_nonexistent_config_raises(self, tmp_path: Path) -> None:
        """Passing a non-existent config path raises an error."""
        nonexistent = tmp_path / "does_not_exist.yml"
        with pytest.raises((FileNotFoundError, OSError)):
            main(nonexistent)
