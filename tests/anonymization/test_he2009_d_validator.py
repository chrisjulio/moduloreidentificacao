"""Issue #76 / G5(a): deficit_fully_structural and equivalence_group_size for d > 1.

Validates the three mandatory checkboxes of issue #76:

1. ``deficit_fully_structural`` in d > 1 (pipeline: True when only D-06 violations;
   synthetic: False when non_isomorphic violations are present).
2. ``equivalence_group_size`` in d > 1 (mean == k·d for complete groups; mean != k·d
   for mixed-size groups — KL approximation limitation, registered in PR).
3. Degenerate combo d=10, k=20 on cycle_graph(20): all nodes land in incomplete
   groups (D-06), producing deficit_fully_structural=True — not a bug.

Seeds fixed to 0; integration tests require reproducible pipeline state
(approved exception per docs/regras_sementes.md).
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
from src.metrics.equivalence_group_size import equivalence_group_size

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

BASE_GRAPH = nx.cycle_graph(20)  # 20 nodes, deterministic, no seed needed


def _pipeline_groups(g: nx.Graph, k: int, d: int, seed: int = 0) -> list[list[nx.Graph]]:
    """Run the internal anonymizer pipeline and return modified groups for the validator."""
    local_structures = _partition_neighborhoods(g, d, seed=seed, backend="auto")
    groups = _group_isomorphic(local_structures, k=k, sigma=0.5, seed=seed)
    return _modify_structure(groups, seed=seed, add_only=False)


def _complete_groups(d: int, k: int, n_groups: int) -> list[list[nx.Graph]]:
    """Build *n_groups* complete equivalence groups, each with *k* LSs of exactly *d* nodes.

    Node IDs are assigned sequentially with no overlap across all groups.
    """
    groups: list[list[nx.Graph]] = []
    node_offset = 0
    for _ in range(n_groups):
        group: list[nx.Graph] = []
        for _ in range(k):
            ls = nx.relabel_nodes(nx.path_graph(d), {i: i + node_offset for i in range(d)})
            group.append(ls)
            node_offset += d
        groups.append(group)
    return groups


# ---------------------------------------------------------------------------
# Checkbox 1 — deficit_fully_structural in d > 1
# ---------------------------------------------------------------------------


class TestDeficitFullyStructuralD:
    """Verify deficit_fully_structural behaviour for d ∈ {2, 5}.

    Pipeline path: True when only D-06 incomplete_group violations.
    Synthetic path: False when non_isomorphic violations are present.
    """

    # --- Pipeline tests (True case) ---

    @pytest.mark.parametrize("d", [2, 5])
    def test_pipeline_violations_all_structural(self, d: int) -> None:
        """Pipeline d∈{2,5}: any violation must be of type incomplete_group."""
        modified = _pipeline_groups(BASE_GRAPH, k=2, d=d)
        report = validate_k_anonymity(modified, k=2)
        violation_types = {v["type"] for v in report["violations"]}
        assert violation_types <= {"incomplete_group"}, (
            f"d={d}: unexpected violation types {violation_types - {'incomplete_group'}}"
        )

    @pytest.mark.parametrize("d", [2, 5])
    def test_pipeline_deficit_fully_structural_true_when_invalid(self, d: int) -> None:
        """Pipeline d∈{2,5}: if invalid, deficit_fully_structural must be True."""
        modified = _pipeline_groups(BASE_GRAPH, k=2, d=d)
        report = validate_k_anonymity(modified, k=2)
        if not report["valid"]:
            assert report["deficit_fully_structural"] is True, (
                f"d={d}: invalid but deficit_fully_structural=False — "
                f"violations: {report['violations']}"
            )

    @pytest.mark.parametrize("d", [2, 5])
    def test_pipeline_no_non_isomorphic_violations(self, d: int) -> None:
        """Pipeline d∈{2,5}: no non_isomorphic violations in output (VF2 condition 4.3)."""
        modified = _pipeline_groups(BASE_GRAPH, k=2, d=d)
        report = validate_k_anonymity(modified, k=2)
        non_iso = [v for v in report["violations"] if v["type"] == "non_isomorphic"]
        assert non_iso == [], f"d={d}: non_isomorphic violations: {non_iso}"

    # --- Synthetic tests (False case) ---

    def test_deficit_false_size_mismatch_d2(self) -> None:
        """Simulate d=2: LSs of size 2 vs 3 — non-isomorphic by size → False."""
        ls_a = nx.path_graph(2).copy()  # 2 nodes (matches d=2)
        ls_b = nx.path_graph(3).copy()  # 3 nodes (≠ d=2) → non-isomorphic
        report = validate_k_anonymity([[ls_a, ls_b]], k=2)
        assert report["deficit_fully_structural"] is False

    def test_deficit_false_size_mismatch_d5(self) -> None:
        """Simulate d=5: LSs of size 5 vs 6 — non-isomorphic by size → False."""
        ls_a = nx.path_graph(5).copy()  # 5 nodes (matches d=5)
        ls_b = nx.path_graph(6).copy()  # 6 nodes (≠ d=5) → non-isomorphic
        report = validate_k_anonymity([[ls_a, ls_b]], k=2)
        assert report["deficit_fully_structural"] is False

    def test_deficit_false_non_isomorphic_same_size(self) -> None:
        """Same-size non-isomorphic LSs: path_graph(4) vs cycle_graph(4) → False."""
        ls_a = nx.path_graph(4).copy()
        ls_b = nx.cycle_graph(4).copy()
        report = validate_k_anonymity([[ls_a, ls_b]], k=2)
        violation_types = {v["type"] for v in report["violations"]}
        assert "non_isomorphic" in violation_types
        assert report["deficit_fully_structural"] is False


# ---------------------------------------------------------------------------
# Checkbox 2 — equivalence_group_size in d > 1
# ---------------------------------------------------------------------------


class TestEquivalenceGroupSizeD:
    """Verify equivalence_group_size behaviour for d ∈ {2, 5}.

    Complete groups with k LSs of size d each: mean == k·d.
    Mixed-size groups (KL backend approximation): mean ≠ k·d — limitation.
    """

    # --- Complete-groups tests (mean == k·d) ---

    def test_mean_equals_kd_d2_k2_complete(self) -> None:
        """d=2, k=2, 3 complete groups → mean = k·d = 4."""
        groups = _complete_groups(d=2, k=2, n_groups=3)
        mean, _ = equivalence_group_size(groups)
        assert mean == pytest.approx(2 * 2)  # k·d = 4

    def test_mean_equals_kd_d5_k2_complete(self) -> None:
        """d=5, k=2, 2 complete groups → mean = k·d = 10."""
        groups = _complete_groups(d=5, k=2, n_groups=2)
        mean, _ = equivalence_group_size(groups)
        assert mean == pytest.approx(2 * 5)  # k·d = 10

    def test_median_equals_kd_d2_uniform(self) -> None:
        """d=2, k=2, uniform complete groups: median == mean == k·d."""
        groups = _complete_groups(d=2, k=2, n_groups=4)
        mean, median = equivalence_group_size(groups)
        assert mean == pytest.approx(2 * 2)
        assert median == 2 * 2

    def test_median_equals_kd_d5_uniform(self) -> None:
        """d=5, k=2, uniform complete groups: median == mean == k·d."""
        groups = _complete_groups(d=5, k=2, n_groups=2)
        mean, median = equivalence_group_size(groups)
        assert mean == pytest.approx(2 * 5)
        assert median == 2 * 5

    # --- Mixed-size test (mean ≠ k·d — KL approximation limitation) ---

    def test_mean_not_kd_mixed_ls_sizes_d2(self) -> None:
        """Mixed LS sizes within one group: mean ≠ k·d (KL backend approximation).

        This is the expected limitation documented in issue #76 checkbox 2:
        when the KL backend produces partitions of unequal node counts, LSs
        in the same equivalence group have different sizes, pulling mean away
        from k·d.  Registered as a prototype limitation, not a bug.
        """
        # Group with 2 LSs: sizes 2 and 3 → group_size = 5 ≠ k·d = 2·2 = 4
        ls_small = nx.path_graph(2).copy()  # 2 nodes
        ls_large = nx.path_graph(3).copy()  # 3 nodes
        groups = [[ls_small, ls_large]]
        mean, _ = equivalence_group_size(groups)
        assert mean != pytest.approx(2 * 2), (
            "mean should be 5 (group_size=5) not 4 (k·d=4) when LS sizes differ"
        )

    # --- Pipeline smoke tests ---

    @pytest.mark.parametrize("d", [2, 5])
    def test_pipeline_mean_strictly_positive(self, d: int) -> None:
        """Pipeline d∈{2,5}: mean_size must be strictly positive."""
        modified = _pipeline_groups(BASE_GRAPH, k=2, d=d)
        mean, _ = equivalence_group_size(modified)
        assert mean > 0

    @pytest.mark.parametrize("d", [2, 5])
    def test_pipeline_mean_finite(self, d: int) -> None:
        """Pipeline d∈{2,5}: mean_size must be finite."""
        modified = _pipeline_groups(BASE_GRAPH, k=2, d=d)
        mean, _ = equivalence_group_size(modified)
        assert mean < float("inf")


# ---------------------------------------------------------------------------
# Checkbox 3 — Degenerate combo d=10, k=20
# ---------------------------------------------------------------------------


class TestDegenerateComboD10K20:
    """Degenerate combo: cycle_graph(20), d=10, k=20.

    c_k = 20 // 10 = 2 partitions → only 2 LSs total.
    k=20 requires 20 LSs per group; 2 < 20 → both LSs land in one incomplete
    group (D-06).  The validator correctly reports deficit_fully_structural=True.
    This is expected behaviour, not a bug (see D-09 and D-10 in decision_log.md).
    """

    def test_anonymize_no_exception(self) -> None:
        """anonymize(cycle_graph(20), k=20, d=10) must complete without exception."""
        result = anonymize(BASE_GRAPH, k=20, d=10, seed=0)
        assert isinstance(result, nx.Graph)

    def test_anonymize_preserves_node_count(self) -> None:
        """Output graph must preserve the original node count."""
        result = anonymize(BASE_GRAPH, k=20, d=10, seed=0)
        assert result.number_of_nodes() == BASE_GRAPH.number_of_nodes()

    def test_validator_violations_only_incomplete_group(self) -> None:
        """Degenerate combo: all violations must be of type incomplete_group (D-06)."""
        modified = _pipeline_groups(BASE_GRAPH, k=20, d=10)
        report = validate_k_anonymity(modified, k=20)
        violation_types = {v["type"] for v in report["violations"]}
        assert violation_types <= {"incomplete_group"}, (
            f"Unexpected violation types in degenerate combo: "
            f"{violation_types - {'incomplete_group'}}"
        )

    def test_deficit_fully_structural_true(self) -> None:
        """Degenerate combo: deficit_fully_structural must be True."""
        modified = _pipeline_groups(BASE_GRAPH, k=20, d=10)
        report = validate_k_anonymity(modified, k=20)
        assert report["deficit_fully_structural"] is True

    def test_all_nodes_are_violators(self) -> None:
        """All 20 nodes must be in incomplete groups (none can satisfy k=20)."""
        modified = _pipeline_groups(BASE_GRAPH, k=20, d=10)
        report = validate_k_anonymity(modified, k=20)
        assert report["n_violators"] == BASE_GRAPH.number_of_nodes()
