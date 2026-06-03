"""Runner integration tests for the Enron dataset branch (issue #125, S9-3).

Issue #125 added an ``elif name == "enron"`` branch to
``experiments.run.load_dataset`` so the runner can dispatch a
``dataset.name == "enron"`` config to ``src.loaders.enron.load_enron``. This is
the single integration point between the Enron loader and the pipeline core;
``component`` / ``min_nodes`` post-processing is dataset-agnostic and already
covered elsewhere.

This module mirrors ``test_run_config_propagation.py`` for the dataset layer,
verifying:

    * ``load_dataset`` dispatches an ``enron`` config to ``load_enron``, reading
      a real edge list on disk and applying OR symmetrization (D-11);
    * ``component`` / ``min_nodes`` post-processing flows through the new branch;
    * an unknown dataset name still fails, and the error lists *both* supported
      datasets (``facebook_ego_nets`` and ``enron``);
    * a full ``main()`` run with an Enron config propagates through the runner
      end-to-end (summary.json + JSONL produced).

Seeds are fixed; approved exception per .claude/rules/seeds.md (tests must be
deterministic). Edge lists are written to ``tmp_path`` so the tests never touch
the real ``data/raw`` tree or the network.
"""

from __future__ import annotations

import json
from pathlib import Path

import networkx as nx
import pytest
import yaml

from experiments.run import load_dataset, main


def _write_edge_list(data_dir: Path, lines: list[str]) -> Path:
    """Write a SNAP-style ``email-Enron.txt`` edge list under ``data_dir``."""
    data_dir.mkdir(parents=True, exist_ok=True)
    edge_file = data_dir / "email-Enron.txt"
    edge_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return edge_file


def _regular_edges() -> list[str]:
    """Directed edge list whose OR symmetrization is a 3-regular 20-node graph.

    Mirrors the ``_small_graph`` used in ``test_run_config_propagation.py``: a
    connected, well-anonymisable graph so the end-to-end run reaches SUCCESS
    rather than failing on coverage. Each undirected edge is written once (one
    direction); the loader's OR symmetrization restores the undirected graph.
    """
    g = nx.random_regular_graph(d=3, n=20, seed=0)
    return [f"{u} {v}" for u, v in g.edges()]


# ---------------------------------------------------------------------------
# load_dataset dispatch
# ---------------------------------------------------------------------------


class TestEnronDispatch:
    """``load_dataset`` routes ``name == "enron"`` to ``load_enron``."""

    def test_dispatches_to_load_enron_with_or_symmetrization(self, tmp_path: Path) -> None:
        # Reciprocal pair (1<->2), one-way (2->3), plus a comment line.
        data_dir = tmp_path / "enron"
        _write_edge_list(
            data_dir,
            ["# Directed Enron email graph", "1 2", "2 1", "2 3"],
        )
        cfg = {"name": "enron", "data_path": str(data_dir), "component": "none"}

        g = load_dataset(cfg)

        # component="none" keeps every node, though preprocess relabels to 0..n-1.
        assert not g.is_directed()
        assert g.number_of_nodes() == 3
        # OR symmetrization: reciprocal pair (1<->2) collapses to a single edge
        # and the one-way (2->3) is kept → a 2-edge path, not 3 directed arcs.
        assert g.number_of_edges() == 2
        assert sorted(d for _, d in g.degree()) == [1, 1, 2]

    def test_lcc_post_processing_flows_through_branch(self, tmp_path: Path) -> None:
        # Two components: a triangle {1,2,3} and an isolated edge {10,11}.
        data_dir = tmp_path / "enron"
        _write_edge_list(data_dir, ["1 2", "2 3", "3 1", "10 11"])
        cfg = {"name": "enron", "data_path": str(data_dir), "component": "lcc"}

        g = load_dataset(cfg)

        # LCC = the triangle (3 nodes); relabelled 0..n-1.
        assert g.number_of_nodes() == 3
        assert set(g.nodes()) == {0, 1, 2}

    def test_min_nodes_below_threshold_raises(self, tmp_path: Path) -> None:
        data_dir = tmp_path / "enron"
        _write_edge_list(data_dir, ["1 2", "2 3", "3 1"])
        cfg = {
            "name": "enron",
            "data_path": str(data_dir),
            "component": "lcc",
            "min_nodes": 10,
        }

        with pytest.raises(ValueError, match="min_nodes"):
            load_dataset(cfg)

    def test_missing_edge_list_raises_file_not_found(self, tmp_path: Path) -> None:
        cfg = {"name": "enron", "data_path": str(tmp_path / "absent")}

        with pytest.raises(FileNotFoundError):
            load_dataset(cfg)


# ---------------------------------------------------------------------------
# Unknown dataset error message
# ---------------------------------------------------------------------------


class TestUnknownDatasetMessage:
    """An unsupported dataset name lists both supported datasets."""

    def test_error_lists_both_datasets(self) -> None:
        with pytest.raises(ValueError) as exc:
            load_dataset({"name": "twitter"})
        message = str(exc.value)
        assert "facebook_ego_nets" in message
        assert "enron" in message


# ---------------------------------------------------------------------------
# End-to-end propagation through main()
# ---------------------------------------------------------------------------


class TestEnronEndToEnd:
    """A full ``main()`` run with an Enron config produces logs."""

    def test_main_runs_with_enron_config(self, tmp_path: Path) -> None:
        data_dir = tmp_path / "enron"
        _write_edge_list(data_dir, _regular_edges())

        name = "enron_e2e"
        config = {
            "experiment": {"name": name},
            "seeds": [0, 1],
            "dataset": {
                "name": "enron",
                "data_path": str(data_dir).replace("\\", "/"),
                "component": "lcc",
            },
            "anonymization": {"k": 2, "d": 1, "sigma": 0.5},
            "attacks": {"degree": {"enabled": True, "tolerance": 0}},
            "runtime": {
                "log_level": "WARNING",
                "log_dir": str(tmp_path).replace("\\", "/"),
            },
        }
        cfg_file = tmp_path / f"{name}.yml"
        cfg_file.write_text(yaml.safe_dump(config), encoding="utf-8")

        rc = main(cfg_file)

        assert rc == 0
        summary = json.loads((tmp_path / name / "summary.json").read_text(encoding="utf-8"))
        assert summary["n_runs"] == 2
        assert summary["seeds"] == [0, 1]
