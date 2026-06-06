"""Config-to-runner propagation tests for s_max / isomorphism_mode (issue #112).

Issues #104 (S8-1 / B5) and #105 (S8-2 / B6) made the simplified-FSM max
subgraph size (``s_max`` / ``fsm_max_size``) and the Phase-2 isomorphization
variant (``isomorphism_mode``) YAML-read parameters instead of hardcoded
constants. This module verifies the *runner* half of that change — the path
``config YAML -> experiments.run.main -> run_one -> {_group_isomorphic,
_modify_structure}`` — by:

    * confirming each effective value is recorded in every JSONL entry and in
      summary.json;
    * confirming the absence of a key falls back to the historical default
      (s_max=4, isomorphism_mode="add_or_delete");
    * confirming the ``fsm_max_size`` alias is accepted for ``s_max``;
    * confirming an invalid ``isomorphism_mode`` aborts main() before the run
      loop (fail fast);
    * confirming each value actually reaches the helper that realises it
      (_group_isomorphic for s_max, _modify_structure for isomorphism_mode),
      not merely the JSONL record.

The behavioural propagation through ``anonymize()`` itself is covered in
tests/anonymization/test_he2009_modify.py; this module is the config layer.

Seeds are fixed; approved exception per .claude/rules/seeds.md (tests must be
deterministic). load_dataset is monkeypatched to a small synthetic graph so the
tests never touch the filesystem.
"""

from __future__ import annotations

import json
from pathlib import Path

import networkx as nx
import pytest
import yaml

import experiments.run as runner_mod
from experiments.run import main
from src.anonymization.he2009 import _group_isomorphic, _modify_structure


def _small_graph() -> nx.Graph:
    """Connected 20-node 3-regular graph (seed=0); fast to anonymise."""
    return nx.random_regular_graph(d=3, n=20, seed=0)


def _write_config(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    name: str,
    anonymization: dict,
    seeds: tuple[int, ...] = (0, 1),
    metrics: dict | None = None,
) -> Path:
    """Write an experiment YAML and monkeypatch load_dataset to a small graph.

    Only the ``anonymization`` block (and optionally ``metrics``) varies
    between tests; everything else is held constant so a single helper covers
    every case.
    """
    monkeypatch.setattr("experiments.run.load_dataset", lambda _cfg: _small_graph())
    config = {
        "experiment": {"name": name},
        "seeds": list(seeds),
        "dataset": {
            "name": "facebook_ego_nets",
            "data_path": "data/raw/facebook/",
            "egonet_id": 3437,
        },
        "anonymization": anonymization,
        "attacks": {"degree": {"enabled": True, "tolerance": 0}},
        "runtime": {"log_level": "WARNING", "log_dir": str(tmp_path).replace("\\", "/")},
    }
    if metrics is not None:
        config["metrics"] = metrics
    cfg_file = tmp_path / f"{name}.yml"
    cfg_file.write_text(yaml.safe_dump(config), encoding="utf-8")
    return cfg_file


def _read_jsonl(tmp_path: Path, name: str) -> list[dict]:
    log_file = tmp_path / name / f"{name}.jsonl"
    return [
        json.loads(line)
        for line in log_file.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _read_summary(tmp_path: Path, name: str) -> dict:
    summary_file = tmp_path / name / "summary.json"
    return json.loads(summary_file.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# isomorphism_mode (B6, issue #105)
# ---------------------------------------------------------------------------


class TestIsomorphismModePropagation:
    """``anonymization.isomorphism_mode`` flows from YAML to runner outputs."""

    def test_add_only_recorded_in_jsonl(self, tmp_path: Path, monkeypatch) -> None:
        name = "iso_add_only_jsonl"
        cfg = _write_config(
            tmp_path,
            monkeypatch,
            name,
            {"k": 2, "d": 2, "sigma": 0.5, "isomorphism_mode": "add_only"},
        )
        main(cfg)
        entries = _read_jsonl(tmp_path, name)
        assert entries
        assert all(e["isomorphism_mode"] == "add_only" for e in entries)

    def test_add_only_recorded_in_summary(self, tmp_path: Path, monkeypatch) -> None:
        name = "iso_add_only_summary"
        cfg = _write_config(
            tmp_path,
            monkeypatch,
            name,
            {"k": 2, "d": 2, "sigma": 0.5, "isomorphism_mode": "add_only"},
        )
        main(cfg)
        assert _read_summary(tmp_path, name)["isomorphism_mode"] == "add_only"

    def test_absent_key_defaults_to_add_or_delete(self, tmp_path: Path, monkeypatch) -> None:
        name = "iso_default"
        cfg = _write_config(tmp_path, monkeypatch, name, {"k": 2, "d": 2, "sigma": 0.5})
        main(cfg)
        entries = _read_jsonl(tmp_path, name)
        assert entries
        assert all(e["isomorphism_mode"] == "add_or_delete" for e in entries)
        assert _read_summary(tmp_path, name)["isomorphism_mode"] == "add_or_delete"

    def test_invalid_mode_aborts_before_run_loop(self, tmp_path: Path, monkeypatch) -> None:
        """A typo in isomorphism_mode raises ValueError in main() (fail fast)."""
        name = "iso_invalid"
        cfg = _write_config(
            tmp_path,
            monkeypatch,
            name,
            {"k": 2, "d": 2, "sigma": 0.5, "isomorphism_mode": "foo"},
        )
        with pytest.raises(ValueError, match="isomorphism_mode"):
            main(cfg)

    def test_add_only_reaches_modify_structure(self, tmp_path: Path, monkeypatch) -> None:
        """The config value reaches _modify_structure(add_only=True), not just
        the JSONL record."""
        name = "iso_reaches_modify"
        cfg = _write_config(
            tmp_path,
            monkeypatch,
            name,
            {"k": 2, "d": 2, "sigma": 0.5, "isomorphism_mode": "add_only"},
            seeds=(0,),
        )
        with monkeypatch.context() as m:
            spy = _SpyWrapper(_modify_structure)
            m.setattr(runner_mod, "_modify_structure", spy)
            main(cfg)
        assert spy.calls, "_modify_structure was never called"
        assert spy.calls[-1].kwargs["add_only"] is True

    def test_default_reaches_modify_structure_as_add_only_false(
        self, tmp_path: Path, monkeypatch
    ) -> None:
        name = "iso_default_reaches_modify"
        cfg = _write_config(tmp_path, monkeypatch, name, {"k": 2, "d": 2, "sigma": 0.5}, seeds=(0,))
        with monkeypatch.context() as m:
            spy = _SpyWrapper(_modify_structure)
            m.setattr(runner_mod, "_modify_structure", spy)
            main(cfg)
        assert spy.calls
        assert spy.calls[-1].kwargs["add_only"] is False


# ---------------------------------------------------------------------------
# s_max / fsm_max_size (B5, issue #104)
# ---------------------------------------------------------------------------


class TestSMaxPropagation:
    """``anonymization.s_max`` (alias ``fsm_max_size``) flows to runner outputs."""

    def test_s_max_recorded_in_jsonl(self, tmp_path: Path, monkeypatch) -> None:
        name = "smax_jsonl"
        cfg = _write_config(tmp_path, monkeypatch, name, {"k": 2, "d": 2, "sigma": 0.5, "s_max": 5})
        main(cfg)
        entries = _read_jsonl(tmp_path, name)
        assert entries
        assert all(e["fsm_max_size"] == 5 for e in entries)

    def test_s_max_recorded_in_summary(self, tmp_path: Path, monkeypatch) -> None:
        name = "smax_summary"
        cfg = _write_config(tmp_path, monkeypatch, name, {"k": 2, "d": 2, "sigma": 0.5, "s_max": 5})
        main(cfg)
        assert _read_summary(tmp_path, name)["fsm_max_size"] == 5

    def test_fsm_max_size_alias_accepted(self, tmp_path: Path, monkeypatch) -> None:
        """The historical key name ``fsm_max_size`` is accepted as an alias."""
        name = "smax_alias"
        cfg = _write_config(
            tmp_path, monkeypatch, name, {"k": 2, "d": 2, "sigma": 0.5, "fsm_max_size": 6}
        )
        main(cfg)
        entries = _read_jsonl(tmp_path, name)
        assert entries
        assert all(e["fsm_max_size"] == 6 for e in entries)

    def test_absent_key_defaults_to_4(self, tmp_path: Path, monkeypatch) -> None:
        name = "smax_default"
        cfg = _write_config(tmp_path, monkeypatch, name, {"k": 2, "d": 2, "sigma": 0.5})
        main(cfg)
        entries = _read_jsonl(tmp_path, name)
        assert entries
        assert all(e["fsm_max_size"] == 4 for e in entries)
        assert _read_summary(tmp_path, name)["fsm_max_size"] == 4

    def test_s_max_reaches_group_isomorphic(self, tmp_path: Path, monkeypatch) -> None:
        """The config value reaches _group_isomorphic(fsm_max_size=5), not just
        the JSONL record."""
        name = "smax_reaches_group"
        cfg = _write_config(
            tmp_path,
            monkeypatch,
            name,
            {"k": 2, "d": 2, "sigma": 0.5, "s_max": 5},
            seeds=(0,),
        )
        with monkeypatch.context() as m:
            spy = _SpyWrapper(_group_isomorphic)
            m.setattr(runner_mod, "_group_isomorphic", spy)
            main(cfg)
        assert spy.calls, "_group_isomorphic was never called"
        assert spy.calls[-1].kwargs["fsm_max_size"] == 5


# ---------------------------------------------------------------------------
# entropy metric / entropy_tau (issue #30, D-17)
# ---------------------------------------------------------------------------


class TestEntropyMetricPropagation:
    """The entropy metric is computed from the equivalence groups and written
    to every JSONL entry; ``metrics.entropy_tau`` flows from YAML to its tau."""

    def test_entropy_block_recorded_in_jsonl(self, tmp_path: Path, monkeypatch) -> None:
        name = "entropy_block"
        cfg = _write_config(tmp_path, monkeypatch, name, {"k": 2, "d": 2, "sigma": 0.5})
        main(cfg)
        entries = _read_jsonl(tmp_path, name)
        assert entries
        for e in entries:
            assert set(e["entropy"]) == {
                "entropy_mean",
                "degree_of_anonymity",
                "reidentification_rate_entropy",
                "tau",
            }

    def test_absent_metrics_defaults_tau_zero(self, tmp_path: Path, monkeypatch) -> None:
        name = "entropy_default_tau"
        cfg = _write_config(tmp_path, monkeypatch, name, {"k": 2, "d": 2, "sigma": 0.5})
        main(cfg)
        entries = _read_jsonl(tmp_path, name)
        assert entries
        assert all(e["entropy"]["tau"] == 0.0 for e in entries)

    def test_entropy_tau_flows_from_yaml(self, tmp_path: Path, monkeypatch) -> None:
        name = "entropy_tau_yaml"
        cfg = _write_config(
            tmp_path,
            monkeypatch,
            name,
            {"k": 2, "d": 2, "sigma": 0.5},
            metrics={"entropy_tau": 1.0},
        )
        main(cfg)
        entries = _read_jsonl(tmp_path, name)
        assert entries
        assert all(e["entropy"]["tau"] == 1.0 for e in entries)


# ---------------------------------------------------------------------------
# Regression — without the new keys, the baseline is unchanged
# ---------------------------------------------------------------------------


class TestRegressionBaselineUnchanged:
    """Omitting both new keys reproduces the historical d=1 baseline determinism."""

    def test_baseline_d1_deterministic_across_runs(self, tmp_path: Path, monkeypatch) -> None:
        """Two identical configs (no new keys, d=1) yield identical JSONL metrics."""
        results = []
        for i in range(2):
            name = f"baseline_d1_{i}"
            cfg = _write_config(
                tmp_path, monkeypatch, name, {"k": 2, "d": 1, "sigma": 0.5}, seeds=(0,)
            )
            main(cfg)
            entry = _read_jsonl(tmp_path, name)[0]
            results.append(entry)
        a, b = results
        assert a["reidentification_rate"] == b["reidentification_rate"]
        assert a["fsm_max_size"] == b["fsm_max_size"] == 4
        assert a["isomorphism_mode"] == b["isomorphism_mode"] == "add_or_delete"
        assert a["ks_test_degree"] == b["ks_test_degree"]


# ---------------------------------------------------------------------------
# Spy helper
# ---------------------------------------------------------------------------


class _Call:
    """A single recorded call: positional args and keyword args."""

    __slots__ = ("args", "kwargs")

    def __init__(self, args: tuple, kwargs: dict) -> None:
        self.args = args
        self.kwargs = kwargs


class _SpyWrapper:
    """Callable that records each invocation and delegates to the real function.

    Used in place of unittest.mock so the wrapped helper still executes (the
    runner needs its real return value) while every call's kwargs are captured
    for assertion. Recording keeps tests independent of mock internals.
    """

    def __init__(self, func) -> None:
        self._func = func
        self.calls: list[_Call] = []

    def __call__(self, *args, **kwargs):
        self.calls.append(_Call(args, kwargs))
        return self._func(*args, **kwargs)
