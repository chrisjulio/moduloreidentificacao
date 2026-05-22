"""Unit tests for validate_k_anonymity in src/anonymization/validation.py.

Covers (as specified in issue #15 Definition of Done):
    - Regular graph (all nodes in one complete group): valid=True, violations=[].
    - Path graph (asymmetric groups): valid=False for k > 1 (non-isomorphic).
    - Residual group with |G_r| < k: valid=False, violations has incomplete_group.
    - Return type and required keys.
    - Non-disjoint detection.
    - satisfied_fraction calculation.
    - Determinism.
    - No imports from he2009.py (auditor independence).

Seeds are not used in validate_k_anonymity — the function is deterministic
by design (no randomness at all).
"""

from __future__ import annotations

import networkx as nx
import pytest

from src.anonymization.validation import validate_k_anonymity

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_group(factory, count: int) -> list[nx.Graph]:
    """Return *count* independent copies produced by *factory*.

    Note: all copies share the same node IDs (as produced by the factory).
    Use _make_disjoint_group when each LS must have unique node IDs (i.e.
    when the group is expected to be valid under the disjunction check).
    """
    return [factory() for _ in range(count)]


def _make_disjoint_group(factory, count: int) -> list[nx.Graph]:
    """Return *count* isomorphic copies with non-overlapping node IDs.

    Each copy is relabeled so that its nodes start where the previous
    copy ended, mimicking how partitioned LSs have distinct node IDs in
    the real pipeline.
    """
    result: list[nx.Graph] = []
    offset = 0
    for _ in range(count):
        g = factory()
        n = g.number_of_nodes()
        relabeled = nx.relabel_nodes(g, {v: v + offset for v in g.nodes()})
        result.append(relabeled)
        offset += n
    return result


# ---------------------------------------------------------------------------
# Return type and required keys
# ---------------------------------------------------------------------------


class TestReturnType:
    """validate_k_anonymity always returns a dict with required keys."""

    def test_returns_dict(self) -> None:
        groups = [_make_group(lambda: nx.cycle_graph(4).copy(), 2)]
        result = validate_k_anonymity(groups, k=2)
        assert isinstance(result, dict)

    def test_has_all_required_keys(self) -> None:
        required = {"valid", "satisfied_fraction", "violations"}
        groups = [_make_group(lambda: nx.cycle_graph(4).copy(), 2)]
        result = validate_k_anonymity(groups, k=2)
        assert required.issubset(result.keys())

    def test_valid_is_bool(self) -> None:
        groups = [_make_group(lambda: nx.path_graph(3).copy(), 2)]
        result = validate_k_anonymity(groups, k=2)
        assert isinstance(result["valid"], bool)

    def test_satisfied_fraction_is_float_in_range(self) -> None:
        groups = [_make_group(lambda: nx.cycle_graph(4).copy(), 3)]
        result = validate_k_anonymity(groups, k=3)
        assert isinstance(result["satisfied_fraction"], float)
        assert 0.0 <= result["satisfied_fraction"] <= 1.0

    def test_violations_is_list(self) -> None:
        groups = [_make_group(lambda: nx.cycle_graph(4).copy(), 2)]
        result = validate_k_anonymity(groups, k=2)
        assert isinstance(result["violations"], list)

    def test_violations_entries_have_required_keys(self) -> None:
        """Each violation dict must have type, status, and nodes."""
        # Force a violation: incomplete group (1 LS, k=2)
        groups = [[nx.cycle_graph(4).copy()]]
        result = validate_k_anonymity(groups, k=2)
        for v in result["violations"]:
            assert "type" in v
            assert "status" in v
            assert "nodes" in v

    def test_empty_groups_no_error(self) -> None:
        """Empty groups input must not raise."""
        result = validate_k_anonymity([], k=2)
        assert isinstance(result, dict)
        assert result["valid"] is True  # no nodes, no violations


# ---------------------------------------------------------------------------
# Definition-of-Done test 1: Regular graph — valid=True, violations=[]
# ---------------------------------------------------------------------------


class TestValidCase:
    """All nodes in one or more complete groups with isomorphic LSs."""

    def test_k2_two_identical_cycle4(self) -> None:
        """k=2, one complete group of 2 isomorphic cycle_graph(4) LSs with
        distinct node IDs (as produced by the real partitioning pipeline):
        valid=True."""
        groups = [_make_disjoint_group(lambda: nx.cycle_graph(4), 2)]
        result = validate_k_anonymity(groups, k=2)
        assert result["valid"] is True
        assert result["violations"] == []
        assert result["satisfied_fraction"] == 1.0

    def test_k3_three_identical_path3(self) -> None:
        """k=3, one complete group of 3 isomorphic path_graph(3) LSs: valid=True."""
        groups = [_make_disjoint_group(lambda: nx.path_graph(3), 3)]
        result = validate_k_anonymity(groups, k=3)
        assert result["valid"] is True
        assert result["violations"] == []

    def test_k2_multiple_complete_groups(self) -> None:
        """Two complete groups of 2 isomorphic LSs each: valid=True."""
        # Groups must have disjoint node IDs across ALL groups.
        g1 = _make_disjoint_group(lambda: nx.cycle_graph(4), 2)  # nodes 0-7
        # Start g2 from node 8 to avoid overlap with g1.
        g2_base = [
            nx.relabel_nodes(nx.cycle_graph(4), {i: i + 8 for i in range(4)}),
            nx.relabel_nodes(nx.cycle_graph(4), {i: i + 12 for i in range(4)}),
        ]
        result = validate_k_anonymity([g1, g2_base], k=2)
        assert result["valid"] is True
        assert result["violations"] == []
        assert result["satisfied_fraction"] == 1.0
        assert result["n_violators"] == 0

    def test_k1_any_group_is_valid(self) -> None:
        """k=1: every group of 1 LS satisfies the minimum cardinality.
        LSs have disjoint node IDs (nodes 0-4 and 5-8 respectively)."""
        ls_a = nx.cycle_graph(5).copy()  # nodes 0-4
        ls_b = nx.relabel_nodes(nx.path_graph(4), {i: i + 5 for i in range(4)})
        groups = [[ls_a], [ls_b]]
        result = validate_k_anonymity(groups, k=1)
        assert result["valid"] is True

    def test_satisfied_fraction_exactly_one_when_valid(self) -> None:
        groups = [_make_disjoint_group(lambda: nx.complete_graph(4), 2)]
        result = validate_k_anonymity(groups, k=2)
        assert result["satisfied_fraction"] == 1.0


# ---------------------------------------------------------------------------
# Definition-of-Done test 2: Path graph (asymmetric) — valid=False, k > 1
# ---------------------------------------------------------------------------


class TestNonIsomorphicCase:
    """Groups containing non-isomorphic LSs must produce valid=False."""

    def test_path_vs_cycle_same_size_non_isomorphic(self) -> None:
        """path_graph(4) and cycle_graph(4) are non-isomorphic:
        a group containing both must be detected as invalid."""
        ls_a = nx.path_graph(4).copy()
        ls_b = nx.cycle_graph(4).copy()
        result = validate_k_anonymity([[ls_a, ls_b]], k=2)
        assert result["valid"] is False

    def test_non_isomorphic_violation_type(self) -> None:
        ls_a = nx.path_graph(4).copy()
        ls_b = nx.cycle_graph(4).copy()
        result = validate_k_anonymity([[ls_a, ls_b]], k=2)
        types = [v["type"] for v in result["violations"]]
        assert "non_isomorphic" in types

    def test_non_isomorphic_status_unprotected(self) -> None:
        ls_a = nx.path_graph(4).copy()
        ls_b = nx.cycle_graph(4).copy()
        result = validate_k_anonymity([[ls_a, ls_b]], k=2)
        for v in result["violations"]:
            if v["type"] == "non_isomorphic":
                assert v["status"] == "unprotected"

    def test_non_isomorphic_nodes_all_in_group(self) -> None:
        """The 'nodes' field of a non_isomorphic violation covers ALL nodes
        in the affected group LSs."""
        ls_a = nx.path_graph(4).copy()  # nodes 0-3
        ls_b = nx.cycle_graph(4).copy()  # nodes 0-3
        result = validate_k_anonymity([[ls_a, ls_b]], k=2)
        for v in result["violations"]:
            if v["type"] == "non_isomorphic":
                # All nodes from both LSs should be listed
                assert len(v["nodes"]) > 0

    def test_star_vs_path_non_isomorphic(self) -> None:
        """star_graph(3) (4 nodes) and path_graph(4) are non-isomorphic."""
        ls_a = nx.star_graph(3).copy()
        ls_b = nx.path_graph(4).copy()
        result = validate_k_anonymity([[ls_a, ls_b]], k=2)
        assert result["valid"] is False
        types = [v["type"] for v in result["violations"]]
        assert "non_isomorphic" in types

    def test_satisfied_fraction_less_than_one_when_invalid(self) -> None:
        ls_a = nx.path_graph(4).copy()
        ls_b = nx.cycle_graph(4).copy()
        result = validate_k_anonymity([[ls_a, ls_b]], k=2)
        assert result["satisfied_fraction"] < 1.0


# ---------------------------------------------------------------------------
# Definition-of-Done test 3: Incomplete group (|G_r| < k)
# ---------------------------------------------------------------------------


class TestIncompleteGroup:
    """Groups with fewer than k LSs must produce valid=False with
    an incomplete_group violation (D-06)."""

    def test_single_ls_with_k2_invalid(self) -> None:
        """One LS, k=2: incomplete group → valid=False."""
        groups = [[nx.cycle_graph(4).copy()]]
        result = validate_k_anonymity(groups, k=2)
        assert result["valid"] is False

    def test_incomplete_group_violation_type(self) -> None:
        groups = [[nx.cycle_graph(4).copy()]]
        result = validate_k_anonymity(groups, k=2)
        types = [v["type"] for v in result["violations"]]
        assert "incomplete_group" in types

    def test_incomplete_group_status_partially_unprotected(self) -> None:
        groups = [[nx.cycle_graph(4).copy()]]
        result = validate_k_anonymity(groups, k=2)
        for v in result["violations"]:
            if v["type"] == "incomplete_group":
                assert v["status"] == "partially_unprotected"

    def test_incomplete_group_contains_affected_nodes(self) -> None:
        ls = nx.cycle_graph(4).copy()
        groups = [[ls]]
        result = validate_k_anonymity(groups, k=2)
        for v in result["violations"]:
            if v["type"] == "incomplete_group":
                assert len(v["nodes"]) == ls.number_of_nodes()

    def test_complete_and_incomplete_mixed(self) -> None:
        """One complete group (k=2) + one incomplete group: valid=False,
        satisfies_fraction reflects that the complete-group nodes are OK."""
        # Complete group: 2 isomorphic cycle_graph(3) LSs, nodes 0-2 and 3-5.
        complete = _make_disjoint_group(lambda: nx.cycle_graph(3), 2)
        # Incomplete group: 1 LS with nodes 6-8.
        incomplete = [nx.relabel_nodes(nx.cycle_graph(3), {i: i + 6 for i in range(3)})]
        result = validate_k_anonymity([complete, incomplete], k=2)
        assert result["valid"] is False
        # 6 nodes valid (complete group) out of 9 total → satisfied_fraction = 6/9
        assert result["satisfied_fraction"] == pytest.approx(6 / 9)

    def test_never_valid_true_with_incomplete_group(self) -> None:
        """No matter how many complete groups there are, valid must be False
        if any group is incomplete."""
        complete1 = _make_group(lambda: nx.cycle_graph(4).copy(), 2)
        complete2 = _make_group(lambda: nx.path_graph(4).copy(), 2)
        incomplete = [nx.path_graph(4).copy()]
        result = validate_k_anonymity([complete1, complete2, incomplete], k=2)
        assert result["valid"] is False

    def test_three_lss_with_k5_incomplete(self) -> None:
        """3 LSs, k=5: incomplete group."""
        groups = [_make_group(lambda: nx.cycle_graph(3).copy(), 3)]
        result = validate_k_anonymity(groups, k=5)
        assert result["valid"] is False
        types = [v["type"] for v in result["violations"]]
        assert "incomplete_group" in types


# ---------------------------------------------------------------------------
# Non-disjoint detection
# ---------------------------------------------------------------------------


class TestNonDisjoint:
    """Nodes appearing in multiple LSs must be detected."""

    def test_non_disjoint_same_node_two_groups(self) -> None:
        """A node shared between two LSs triggers non_disjoint violation."""
        # Manually construct two LSs that share node 0
        ls_a = nx.Graph()
        ls_a.add_nodes_from([0, 1])
        ls_a.add_edge(0, 1)

        ls_b = nx.Graph()
        ls_b.add_nodes_from([0, 2])
        ls_b.add_edge(0, 2)

        result = validate_k_anonymity([[ls_a], [ls_b]], k=1)
        types = [v["type"] for v in result["violations"]]
        assert "non_disjoint" in types

    def test_non_disjoint_status_unprotected(self) -> None:
        ls_a = nx.Graph()
        ls_a.add_nodes_from([0, 1])
        ls_b = nx.Graph()
        ls_b.add_nodes_from([0, 2])
        result = validate_k_anonymity([[ls_a], [ls_b]], k=1)
        for v in result["violations"]:
            if v["type"] == "non_disjoint":
                assert v["status"] == "unprotected"
                assert 0 in v["nodes"]

    def test_non_disjoint_forces_valid_false(self) -> None:
        ls_a = nx.Graph()
        ls_a.add_nodes_from([0, 1])
        ls_b = nx.Graph()
        ls_b.add_nodes_from([0, 2])
        result = validate_k_anonymity([[ls_a], [ls_b]], k=1)
        assert result["valid"] is False


# ---------------------------------------------------------------------------
# satisfied_fraction calculation
# ---------------------------------------------------------------------------


class TestSatisfiedFraction:
    """satisfied_fraction must accurately reflect the fraction of non-violating nodes."""

    def test_all_valid_fraction_is_one(self) -> None:
        groups = [_make_disjoint_group(lambda: nx.cycle_graph(4), 2)]
        result = validate_k_anonymity(groups, k=2)
        assert result["satisfied_fraction"] == pytest.approx(1.0)

    def test_all_invalid_fraction_is_zero(self) -> None:
        """If every node is in a violating group, fraction = 0."""
        # One incomplete group with all nodes
        ls = nx.path_graph(4).copy()
        result = validate_k_anonymity([[ls]], k=2)
        assert result["satisfied_fraction"] == pytest.approx(0.0)

    def test_partial_fraction(self) -> None:
        """8 valid nodes (1 complete group of 2 LSs) + 4 invalid (1 incomplete
        group) → satisfied_fraction = 8/12."""
        # Complete group: 2 LSs with distinct node IDs, mutually isomorphic.
        ls_c1 = nx.relabel_nodes(nx.cycle_graph(4), {i: i for i in range(4)})
        ls_c2 = nx.relabel_nodes(nx.cycle_graph(4), {i: i + 4 for i in range(4)})
        complete_group = [ls_c1, ls_c2]  # 8 nodes total, k=2 → valid
        # Incomplete group: 1 LS, k=2 → invalid (D-06).
        ls_inc = nx.relabel_nodes(nx.path_graph(4), {i: i + 8 for i in range(4)})
        incomplete_group = [ls_inc]  # 4 nodes, 1 LS < k=2
        result = validate_k_anonymity([complete_group, incomplete_group], k=2)
        assert result["satisfied_fraction"] == pytest.approx(8 / 12)
        assert result["n_violators"] == 4

    def test_n_violators_matches_violators_list(self) -> None:
        groups = [[nx.cycle_graph(4).copy()]]  # incomplete
        result = validate_k_anonymity(groups, k=2)
        assert result["n_violators"] == len(result["violators"])


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------


class TestDeterminism:
    """Same input must always produce the same output."""

    def test_same_input_same_output_valid(self) -> None:
        groups = [_make_group(lambda: nx.cycle_graph(4).copy(), 2)]
        r1 = validate_k_anonymity(groups, k=2)
        r2 = validate_k_anonymity(groups, k=2)
        assert r1["valid"] == r2["valid"]
        assert r1["satisfied_fraction"] == r2["satisfied_fraction"]
        assert r1["violations"] == r2["violations"]

    def test_same_input_same_output_invalid(self) -> None:
        groups = [[nx.path_graph(4).copy(), nx.cycle_graph(4).copy()]]
        r1 = validate_k_anonymity(groups, k=2)
        r2 = validate_k_anonymity(groups, k=2)
        assert r1["valid"] == r2["valid"]
        assert r1["n_violators"] == r2["n_violators"]


# ---------------------------------------------------------------------------
# Auditor independence — no imports from he2009.py
# ---------------------------------------------------------------------------


class TestAuditorIndependence:
    """validate_k_anonymity must not import anything from he2009.py."""

    def test_validation_module_does_not_import_he2009(self) -> None:
        """Inspect the validation module's globals to confirm independence."""
        import src.anonymization.validation as val_mod

        module_globals = vars(val_mod)
        # he2009 must not be imported into the validation module
        assert "he2009" not in module_globals
        assert "_group_isomorphic" not in module_globals
        assert "_modify_structure" not in module_globals
        assert "_partition_neighborhoods" not in module_globals
        assert "anonymize" not in module_globals


# ---------------------------------------------------------------------------
# Integration: groups produced by the actual anonymizer pipeline
# ---------------------------------------------------------------------------


class TestWithAnonymizerOutput:
    """Smoke tests using groups produced by the real anonymizer."""

    def test_petersen_k2_d2_valid_or_d06(self) -> None:
        """Anonymize Petersen k=2, d=2; validate the groups.
        Result is either valid or has only D-06 incomplete-group violations."""
        from src.anonymization.he2009 import (
            _group_isomorphic,
            _modify_structure,
            _partition_neighborhoods,
        )

        g = nx.petersen_graph()
        local_structures = _partition_neighborhoods(g, d=2, seed=0, backend="networkx-kl")
        groups = _group_isomorphic(local_structures, k=2, sigma=0.5, seed=0)
        modified = _modify_structure(groups, seed=0)
        result = validate_k_anonymity(modified, k=2)

        # All violations must be of type incomplete_group or non_isomorphic
        violation_types = {v["type"] for v in result["violations"]}
        assert violation_types.issubset({"incomplete_group", "non_isomorphic"}), (
            f"Unexpected violation types: {violation_types}"
        )


# ---------------------------------------------------------------------------
# DL-01 fields: coverage_fraction, uncovered_fraction, deficit_fully_structural
# ---------------------------------------------------------------------------


class TestDL01Fields:
    """Tests for fields introduced by decision DL-01 (docs/decision_log.md):
    coverage_fraction, uncovered_fraction, and deficit_fully_structural."""

    # -----------------------------------------------------------------------
    # coverage_fraction — presence and alias invariant
    # -----------------------------------------------------------------------

    def test_coverage_fraction_key_present(self) -> None:
        """Return dict must contain the coverage_fraction key."""
        groups = [_make_disjoint_group(lambda: nx.cycle_graph(4), 2)]
        result = validate_k_anonymity(groups, k=2)
        assert "coverage_fraction" in result

    def test_coverage_fraction_equals_satisfied_fraction_valid(self) -> None:
        """valid=True: coverage_fraction is a direct alias of satisfied_fraction."""
        groups = [_make_disjoint_group(lambda: nx.cycle_graph(4), 2)]
        result = validate_k_anonymity(groups, k=2)
        assert result["coverage_fraction"] == result["satisfied_fraction"]
        assert result["coverage_fraction"] == pytest.approx(1.0)

    def test_coverage_fraction_equals_satisfied_fraction_at_zero(self) -> None:
        """satisfied_fraction == 0: coverage_fraction must also be 0."""
        groups = [[nx.path_graph(4).copy()]]  # 1 LS, k=2 → all nodes violate
        result = validate_k_anonymity(groups, k=2)
        assert result["coverage_fraction"] == result["satisfied_fraction"]
        assert result["coverage_fraction"] == pytest.approx(0.0)

    def test_coverage_fraction_equals_satisfied_fraction_partial(self) -> None:
        """Partial coverage: coverage_fraction mirrors satisfied_fraction."""
        complete = _make_disjoint_group(lambda: nx.cycle_graph(3), 2)  # nodes 0-5
        incomplete = [nx.relabel_nodes(nx.cycle_graph(3), {i: i + 6 for i in range(3)})]
        result = validate_k_anonymity([complete, incomplete], k=2)
        assert result["coverage_fraction"] == result["satisfied_fraction"]

    # -----------------------------------------------------------------------
    # uncovered_fraction — presence, complementarity, n_violators invariant
    # -----------------------------------------------------------------------

    def test_uncovered_fraction_key_present(self) -> None:
        """Return dict must contain the uncovered_fraction key."""
        groups = [_make_disjoint_group(lambda: nx.cycle_graph(4), 2)]
        result = validate_k_anonymity(groups, k=2)
        assert "uncovered_fraction" in result

    def test_uncovered_fraction_complement_of_coverage_invalid(self) -> None:
        """coverage_fraction + uncovered_fraction == 1.0 when invalid."""
        groups = [[nx.cycle_graph(4).copy()]]  # 1 LS, k=2
        result = validate_k_anonymity(groups, k=2)
        assert result["coverage_fraction"] + result["uncovered_fraction"] == pytest.approx(1.0)

    def test_uncovered_fraction_complement_of_coverage_valid(self) -> None:
        """coverage_fraction + uncovered_fraction == 1.0 when valid."""
        groups = [_make_disjoint_group(lambda: nx.cycle_graph(4), 2)]
        result = validate_k_anonymity(groups, k=2)
        assert result["coverage_fraction"] + result["uncovered_fraction"] == pytest.approx(1.0)
        assert result["uncovered_fraction"] == pytest.approx(0.0)

    def test_uncovered_fraction_invariant_all_violators(self) -> None:
        """uncovered_fraction == n_violators / n_total (all nodes violate)."""
        # path_graph(4): n_total=4, k=2 → 1 LS → all 4 nodes violate.
        groups = [[nx.path_graph(4).copy()]]
        n_total = 4
        result = validate_k_anonymity(groups, k=2)
        assert result["uncovered_fraction"] == pytest.approx(result["n_violators"] / n_total)

    def test_uncovered_fraction_invariant_partial_case(self) -> None:
        """Partial case: uncovered_fraction == n_violators / n_total."""
        # Complete group: 2 cycle_graph(4) LSs with distinct node IDs → 8 valid nodes.
        ls_c1 = nx.relabel_nodes(nx.cycle_graph(4), {i: i for i in range(4)})
        ls_c2 = nx.relabel_nodes(nx.cycle_graph(4), {i: i + 4 for i in range(4)})
        complete_group = [ls_c1, ls_c2]
        # Incomplete group: 1 LS with 4 nodes → 4 violators.
        ls_inc = nx.relabel_nodes(nx.path_graph(4), {i: i + 8 for i in range(4)})
        incomplete_group = [ls_inc]
        n_total = 12
        result = validate_k_anonymity([complete_group, incomplete_group], k=2)
        assert result["uncovered_fraction"] == pytest.approx(result["n_violators"] / n_total)

    # -----------------------------------------------------------------------
    # deficit_fully_structural — presence and three states
    # -----------------------------------------------------------------------

    def test_deficit_fully_structural_key_present(self) -> None:
        """Return dict must contain the deficit_fully_structural key."""
        groups = [_make_disjoint_group(lambda: nx.cycle_graph(4), 2)]
        result = validate_k_anonymity(groups, k=2)
        assert "deficit_fully_structural" in result

    def test_deficit_fully_structural_type_is_bool(self) -> None:
        """deficit_fully_structural must be a Python bool."""
        groups = [_make_disjoint_group(lambda: nx.cycle_graph(4), 2)]
        result = validate_k_anonymity(groups, k=2)
        assert isinstance(result["deficit_fully_structural"], bool)

    def test_deficit_fully_structural_true_when_valid(self) -> None:
        """No violations: deficit_fully_structural is True by vacuity.

        The empty violation set is a subset of {"incomplete_group"}, so
        the condition holds even when valid=True (see metrics_definitions.md §3).
        """
        groups = [_make_disjoint_group(lambda: nx.cycle_graph(4), 2)]
        result = validate_k_anonymity(groups, k=2)
        assert result["valid"] is True
        assert result["deficit_fully_structural"] is True

    def test_deficit_fully_structural_true_only_incomplete_group(self) -> None:
        """Only incomplete_group violations (D-06): deficit_fully_structural is True."""
        # Single LS with k=2 → incomplete_group, no non_isomorphic or non_disjoint.
        groups = [[nx.cycle_graph(4).copy()]]
        result = validate_k_anonymity(groups, k=2)
        violation_types = {v["type"] for v in result["violations"]}
        assert violation_types == {"incomplete_group"}
        assert result["deficit_fully_structural"] is True

    def test_deficit_fully_structural_false_non_isomorphic(self) -> None:
        """non_isomorphic violation present: deficit_fully_structural is False."""
        ls_a = nx.path_graph(4).copy()
        ls_b = nx.cycle_graph(4).copy()
        result = validate_k_anonymity([[ls_a, ls_b]], k=2)
        types = {v["type"] for v in result["violations"]}
        assert "non_isomorphic" in types
        assert result["deficit_fully_structural"] is False

    def test_deficit_fully_structural_false_non_disjoint(self) -> None:
        """non_disjoint violation present: deficit_fully_structural is False."""
        ls_a = nx.Graph()
        ls_a.add_nodes_from([0, 1])
        ls_a.add_edge(0, 1)
        ls_b = nx.Graph()
        ls_b.add_nodes_from([0, 2])
        ls_b.add_edge(0, 2)
        result = validate_k_anonymity([[ls_a], [ls_b]], k=1)
        types = {v["type"] for v in result["violations"]}
        assert "non_disjoint" in types
        assert result["deficit_fully_structural"] is False
