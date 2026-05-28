"""End-to-end integration tests for anonymize() with d > 1 (issue #75, G1).

Exercises the full pipeline anonymize(g, k=2, d=2) and anonymize(g, k=2, d=5)
on a small deterministic graph (~20 nodes).  Verifies:

1. No exception raised.
2. Output type and node count preserved.
3. Validator coherent: report is valid or deficit_fully_structural=True (D-06).
4. No non_isomorphic violations in complete groups (condition 4.3, VF2).

Seeds fixed to 0 and 7; approved exception per .claude/rules/seeds.md —
integration tests require reproducible pipeline state.
"""

from __future__ import annotations

import networkx as nx
import pytest

from src.anonymization.he2009 import (
    _group_isomorphic,
    _modify_structure,
    _partition_neighborhoods,
    anonymize,
)
from src.anonymization.validation import validate_k_anonymity

# ---------------------------------------------------------------------------
# Shared fixture
# ---------------------------------------------------------------------------

BASE_GRAPH = nx.cycle_graph(20)  # 20 nodes, deterministic, no seed needed


def _pipeline_groups(g: nx.Graph, k: int, d: int, seed: int) -> list[list[nx.Graph]]:
    """Run internal pipeline steps and return modified_groups for the validator."""
    local_structures = _partition_neighborhoods(g, d, seed=seed, backend="auto")
    groups = _group_isomorphic(local_structures, k=k, sigma=0.5, seed=seed)
    return _modify_structure(groups, seed=seed, add_only=False)


# ---------------------------------------------------------------------------
# G1a — black-box tests for anonymize() with d=2
# ---------------------------------------------------------------------------


class TestE2eD2:
    """anonymize(cycle_graph(20), k=2, d=2) must complete coherently."""

    def test_no_exception(self) -> None:
        result = anonymize(BASE_GRAPH, k=2, d=2, seed=0)
        assert result is not None

    def test_returns_nx_graph(self) -> None:
        result = anonymize(BASE_GRAPH, k=2, d=2, seed=0)
        assert isinstance(result, nx.Graph)

    def test_node_count_preserved(self) -> None:
        result = anonymize(BASE_GRAPH, k=2, d=2, seed=0)
        assert result.number_of_nodes() == BASE_GRAPH.number_of_nodes()

    def test_node_set_unchanged(self) -> None:
        result = anonymize(BASE_GRAPH, k=2, d=2, seed=0)
        assert set(result.nodes()) == set(BASE_GRAPH.nodes())

    def test_no_self_loops(self) -> None:
        result = anonymize(BASE_GRAPH, k=2, d=2, seed=0)
        assert not any(u == v for u, v in result.edges())

    def test_determinism(self) -> None:
        r1 = anonymize(BASE_GRAPH, k=2, d=2, seed=7)
        r2 = anonymize(BASE_GRAPH, k=2, d=2, seed=7)
        assert set(r1.edges()) == set(r2.edges())


# ---------------------------------------------------------------------------
# G1b — black-box tests for anonymize() with d=5
# ---------------------------------------------------------------------------


class TestE2eD5:
    """anonymize(cycle_graph(20), k=2, d=5) must complete coherently."""

    def test_no_exception(self) -> None:
        result = anonymize(BASE_GRAPH, k=2, d=5, seed=0)
        assert result is not None

    def test_returns_nx_graph(self) -> None:
        result = anonymize(BASE_GRAPH, k=2, d=5, seed=0)
        assert isinstance(result, nx.Graph)

    def test_node_count_preserved(self) -> None:
        result = anonymize(BASE_GRAPH, k=2, d=5, seed=0)
        assert result.number_of_nodes() == BASE_GRAPH.number_of_nodes()

    def test_node_set_unchanged(self) -> None:
        result = anonymize(BASE_GRAPH, k=2, d=5, seed=0)
        assert set(result.nodes()) == set(BASE_GRAPH.nodes())

    def test_no_self_loops(self) -> None:
        result = anonymize(BASE_GRAPH, k=2, d=5, seed=0)
        assert not any(u == v for u, v in result.edges())

    def test_determinism(self) -> None:
        r1 = anonymize(BASE_GRAPH, k=2, d=5, seed=7)
        r2 = anonymize(BASE_GRAPH, k=2, d=5, seed=7)
        assert set(r1.edges()) == set(r2.edges())


# ---------------------------------------------------------------------------
# G1c — validator coherence (condition 4.3)
# ---------------------------------------------------------------------------


class TestValidatorCoherence:
    """Validator must return a coherent report for both d=2 and d=5."""

    @pytest.mark.parametrize("d", [2, 5])
    def test_validator_valid_or_structural(self, d: int) -> None:
        """Report must be valid or deficit attributable to structural causes only (D-06)."""
        modified_groups = _pipeline_groups(BASE_GRAPH, k=2, d=d, seed=0)
        report = validate_k_anonymity(modified_groups, k=2)
        assert report["valid"] or report["deficit_fully_structural"], (
            f"d={d}: validator returned non-structural violations: {report['violations']}"
        )

    @pytest.mark.parametrize("d", [2, 5])
    def test_no_non_isomorphic_violations(self, d: int) -> None:
        """Complete groups must have mutually isomorphic LSs (VF2, condition 4.3)."""
        modified_groups = _pipeline_groups(BASE_GRAPH, k=2, d=d, seed=0)
        report = validate_k_anonymity(modified_groups, k=2)
        non_iso = [v for v in report["violations"] if v["type"] == "non_isomorphic"]
        assert non_iso == [], f"d={d}: non_isomorphic violations found: {non_iso}"

    @pytest.mark.parametrize("d", [2, 5])
    def test_coverage_fraction_in_range(self, d: int) -> None:
        """coverage_fraction must be in [0, 1]."""
        modified_groups = _pipeline_groups(BASE_GRAPH, k=2, d=d, seed=0)
        report = validate_k_anonymity(modified_groups, k=2)
        assert 0.0 <= report["coverage_fraction"] <= 1.0

    @pytest.mark.parametrize("d", [2, 5])
    def test_n_violators_consistent(self, d: int) -> None:
        """n_violators must be consistent with coverage_fraction."""
        modified_groups = _pipeline_groups(BASE_GRAPH, k=2, d=d, seed=0)
        report = validate_k_anonymity(modified_groups, k=2)
        n = BASE_GRAPH.number_of_nodes()
        expected_covered = n - report["n_violators"]
        assert abs(report["coverage_fraction"] - expected_covered / n) < 1e-5
