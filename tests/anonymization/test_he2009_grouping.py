"""Unit tests for _group_isomorphic in src/anonymization/he2009.py.

Covers:
    - Return type: list[list[nx.Graph]] in all cases.
    - Coverage invariant: every input LS appears in exactly one group.
    - Regular graph: k identical LSs form a single complete group.
    - Path graph: structural similarity drives grouping.
    - Petersen graph: all LSs covered; one group when n == k.
    - D-06 (incomplete group): when n % k != 0 the last group has < k
      members, but total coverage is still 100 %.
    - Determinism: two calls with the same seed return the same grouping.
    - D-07 (same-size policy): LSs with different node counts never share
      a group.
    - Edge cases: sigma=0, sigma=1, k=1, edgeless LSs (mf=0 tiebreak).

Seeds are fixed to 0 throughout (controlled exception per
.claude/rules/seeds.md — deterministic tests require reproducible
grouping; seed=0 carries no algorithmic significance).
"""

from __future__ import annotations

from collections.abc import Callable

import networkx as nx
import pytest

from src.anonymization.he2009 import _group_isomorphic

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_ls(graph_factory: Callable[[], nx.Graph], count: int) -> list[nx.Graph]:
    """Return *count* independent copies of the graph produced by *graph_factory*."""
    return [graph_factory().copy() for _ in range(count)]


def _all_nodes_covered(
    local_structures: list[nx.Graph],
    groups: list[list[nx.Graph]],
) -> bool:
    """True iff every LS object from *local_structures* appears exactly once."""
    covered_ids = [id(ls) for grp in groups for ls in grp]
    expected_ids = [id(ls) for ls in local_structures]
    return sorted(covered_ids) == sorted(expected_ids)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def cycle4() -> nx.Graph:
    return nx.cycle_graph(4)


@pytest.fixture
def path5() -> nx.Graph:
    return nx.path_graph(5)


# ---------------------------------------------------------------------------
# Return type
# ---------------------------------------------------------------------------


class TestReturnType:
    """_group_isomorphic always returns list[list[nx.Graph]]."""

    def test_empty_input_returns_empty_list(self) -> None:
        groups = _group_isomorphic([], k=2, sigma=0.2, seed=0)
        assert groups == []

    def test_single_ls_returns_one_group(self) -> None:
        """One LS, k=2: cannot form a complete group → one incomplete group."""
        ls = [nx.cycle_graph(4).copy()]
        groups = _group_isomorphic(ls, k=2, sigma=0.2, seed=0)
        assert isinstance(groups, list)
        assert len(groups) == 1
        assert isinstance(groups[0], list)
        assert all(isinstance(g, nx.Graph) for g in groups[0])

    def test_nested_type_is_list_of_list_of_graph(self, cycle4: nx.Graph) -> None:
        ls = [cycle4.copy() for _ in range(4)]
        groups = _group_isomorphic(ls, k=2, sigma=0.2, seed=0)
        assert isinstance(groups, list)
        for grp in groups:
            assert isinstance(grp, list)
            for g in grp:
                assert isinstance(g, nx.Graph)


# ---------------------------------------------------------------------------
# Coverage invariant
# ---------------------------------------------------------------------------


class TestCoverageInvariant:
    """Every input LS must appear in exactly one output group."""

    def test_k2_four_identical_all_covered(self, cycle4: nx.Graph) -> None:
        ls = [cycle4.copy() for _ in range(4)]
        groups = _group_isomorphic(ls, k=2, sigma=0.2, seed=0)
        assert _all_nodes_covered(ls, groups)

    def test_k3_seven_ls_all_covered(self, path5: nx.Graph) -> None:
        """7 LSs, k=3 → 2 complete groups + 1 incomplete (D-06); total 7."""
        ls = [path5.copy() for _ in range(7)]
        groups = _group_isomorphic(ls, k=3, sigma=0.1, seed=0)
        assert _all_nodes_covered(ls, groups)

    def test_no_duplicate_ls_in_groups(self, cycle4: nx.Graph) -> None:
        ls = [cycle4.copy() for _ in range(6)]
        groups = _group_isomorphic(ls, k=3, sigma=0.1, seed=0)
        all_ids = [id(g) for grp in groups for g in grp]
        assert len(all_ids) == len(set(all_ids)), "Duplicate LS object found in groups"

    def test_total_members_equals_input_size(self, path5: nx.Graph) -> None:
        n = 9
        ls = [path5.copy() for _ in range(n)]
        groups = _group_isomorphic(ls, k=4, sigma=0.1, seed=0)
        assert sum(len(grp) for grp in groups) == n


# ---------------------------------------------------------------------------
# Regular graph: identical LSs form a single complete group
# ---------------------------------------------------------------------------


class TestRegularGraph:
    """All-identical LSs → single group per k batch, no leftovers if k | n."""

    def test_k3_three_identical_cycles_one_group(self, cycle4: nx.Graph) -> None:
        """Exactly k identical LSs → exactly one complete group."""
        k = 3
        ls = [cycle4.copy() for _ in range(k)]
        groups = _group_isomorphic(ls, k=k, sigma=0.1, seed=0)
        complete = [grp for grp in groups if len(grp) == k]
        assert len(complete) == 1, f"Expected 1 complete group, got {len(complete)}"

    def test_k3_six_identical_cycles_two_groups(self, cycle4: nx.Graph) -> None:
        """2k identical LSs → exactly 2 complete groups."""
        k = 3
        ls = [cycle4.copy() for _ in range(2 * k)]
        groups = _group_isomorphic(ls, k=k, sigma=0.1, seed=0)
        complete = [grp for grp in groups if len(grp) == k]
        assert len(complete) == 2, f"Expected 2 complete groups, got {len(complete)}"

    def test_k2_eight_identical_no_incomplete_group(self, cycle4: nx.Graph) -> None:
        """When k divides n, no incomplete group should exist."""
        k, n = 2, 8
        ls = [cycle4.copy() for _ in range(n)]
        groups = _group_isomorphic(ls, k=k, sigma=0.1, seed=0)
        incomplete = [grp for grp in groups if len(grp) < k]
        assert incomplete == [], f"Unexpected incomplete groups: {incomplete}"
        assert len(groups) == n // k

    def test_complete_groups_have_exactly_k_members(self, path5: nx.Graph) -> None:
        k = 4
        ls = [path5.copy() for _ in range(2 * k)]
        groups = _group_isomorphic(ls, k=k, sigma=0.1, seed=0)
        for grp in groups:
            # All groups should be complete when k | n
            assert len(grp) == k


# ---------------------------------------------------------------------------
# Path graph: groups by structural similarity
# ---------------------------------------------------------------------------


class TestPathGraph:
    """Path-graph LSs: isomorphic structures are grouped together."""

    def test_k2_four_path3_two_groups(self) -> None:
        """4 identical path-3 LSs with k=2 → 2 complete groups of 2."""
        k = 2
        ls = _make_ls(lambda: nx.path_graph(3), 4)
        groups = _group_isomorphic(ls, k=k, sigma=0.1, seed=0)
        complete = [grp for grp in groups if len(grp) == k]
        assert len(complete) == 2

    def test_k3_six_path4_two_groups(self) -> None:
        """6 identical path-4 LSs with k=3 → 2 complete groups of 3."""
        k = 3
        ls = _make_ls(lambda: nx.path_graph(4), 6)
        groups = _group_isomorphic(ls, k=k, sigma=0.1, seed=0)
        complete = [grp for grp in groups if len(grp) == k]
        assert len(complete) == 2

    def test_all_path_ls_covered(self) -> None:
        """Coverage invariant holds for heterogeneous path-graph LSs."""
        ls = _make_ls(lambda: nx.path_graph(5), 7)
        groups = _group_isomorphic(ls, k=3, sigma=0.1, seed=0)
        assert _all_nodes_covered(ls, groups)

    def test_groups_contain_nx_graph_instances(self) -> None:
        ls = _make_ls(lambda: nx.path_graph(4), 5)
        groups = _group_isomorphic(ls, k=2, sigma=0.1, seed=0)
        for grp in groups:
            for item in grp:
                assert isinstance(item, nx.Graph)


# ---------------------------------------------------------------------------
# Petersen graph: uniform grouping when n == k
# ---------------------------------------------------------------------------


class TestPetersen:
    """Petersen-derived LSs: agrupamento uniforme (one group when n == k)."""

    def test_five_identical_lss_k5_one_complete_group(self) -> None:
        """5 identical 2-node LSs, k=5 → exactly one complete group of 5."""
        k = 5
        # Simulate the 5 two-node LSs produced by partitioning Petersen (d=2)
        ls = [nx.path_graph(2).copy() for _ in range(k)]
        groups = _group_isomorphic(ls, k=k, sigma=0.1, seed=0)
        complete = [grp for grp in groups if len(grp) == k]
        assert len(complete) == 1
        assert len(complete[0]) == k

    def test_five_identical_lss_k5_all_covered(self) -> None:
        k = 5
        ls = [nx.path_graph(2).copy() for _ in range(k)]
        groups = _group_isomorphic(ls, k=k, sigma=0.1, seed=0)
        assert _all_nodes_covered(ls, groups)

    def test_ten_identical_lss_k5_two_groups(self) -> None:
        """10 identical LSs, k=5 → exactly 2 complete groups."""
        k = 5
        ls = [nx.cycle_graph(3).copy() for _ in range(2 * k)]
        groups = _group_isomorphic(ls, k=k, sigma=0.1, seed=0)
        complete = [grp for grp in groups if len(grp) == k]
        assert len(complete) == 2

    def test_petersen_partitioned_all_lss_covered(self) -> None:
        """Integration: all LSs from partitioned Petersen are covered."""
        from src.anonymization.he2009 import _partition_neighborhoods

        petersen = nx.petersen_graph()
        # 5 partitions of size ~2 with KL backend (D-04 fallback)
        ls = _partition_neighborhoods(petersen, d=2, seed=0, backend="networkx-kl")
        groups = _group_isomorphic(ls, k=2, sigma=0.1, seed=0)
        assert _all_nodes_covered(ls, groups)


# ---------------------------------------------------------------------------
# D-06: incomplete final group
# ---------------------------------------------------------------------------


class TestIncompleteGroup:
    """When n % k != 0 the last group has < k members (D-06)."""

    def test_n_not_divisible_by_k_has_incomplete_group(self, cycle4: nx.Graph) -> None:
        """7 LSs, k=3 → 2 complete groups + 1 incomplete group of 1."""
        k, n = 3, 7
        ls = [cycle4.copy() for _ in range(n)]
        groups = _group_isomorphic(ls, k=k, sigma=0.1, seed=0)
        incomplete = [grp for grp in groups if len(grp) < k]
        assert len(incomplete) >= 1
        assert sum(len(grp) for grp in incomplete) == n % k

    def test_incomplete_group_members_are_graphs(self, path5: nx.Graph) -> None:
        k, n = 3, 5
        ls = [path5.copy() for _ in range(n)]
        groups = _group_isomorphic(ls, k=k, sigma=0.1, seed=0)
        for grp in groups:
            for item in grp:
                assert isinstance(item, nx.Graph)


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------


class TestDeterminism:
    """Same seed → same grouping structure."""

    def test_same_seed_same_groups(self, cycle4: nx.Graph) -> None:
        ls = [cycle4.copy() for _ in range(9)]
        groups_a = _group_isomorphic(ls, k=3, sigma=0.2, seed=42)
        groups_b = _group_isomorphic(ls, k=3, sigma=0.2, seed=42)
        sizes_a = [len(grp) for grp in groups_a]
        sizes_b = [len(grp) for grp in groups_b]
        assert sizes_a == sizes_b

    def test_different_seeds_may_differ(self, cycle4: nx.Graph) -> None:
        """Different seeds can produce different groupings (not guaranteed,
        but verified over a set where randomness matters)."""
        ls = [cycle4.copy() for _ in range(6)]
        # With 6 identical LSs and k=2 there are multiple valid groupings;
        # we only verify both runs are valid (coverage), not that they differ.
        groups_0 = _group_isomorphic(ls, k=2, sigma=0.2, seed=0)
        groups_1 = _group_isomorphic(ls, k=2, sigma=0.2, seed=1)
        assert _all_nodes_covered(ls, groups_0)
        assert _all_nodes_covered(ls, groups_1)


# ---------------------------------------------------------------------------
# D-07: same-size policy
# ---------------------------------------------------------------------------


class TestSameSizePolicy:
    """LSs of different sizes must never share a group (D-07 Opção A)."""

    def test_mixed_sizes_never_share_group(self) -> None:
        """LSs of 3 and 5 nodes must be in separate groups."""
        small = [nx.cycle_graph(3).copy() for _ in range(3)]
        large = [nx.cycle_graph(5).copy() for _ in range(3)]
        ls = small + large
        groups = _group_isomorphic(ls, k=3, sigma=0.1, seed=0)
        for grp in groups:
            sizes = {g.number_of_nodes() for g in grp}
            assert len(sizes) == 1, f"Group contains LSs of mixed sizes {sizes}: {grp}"

    def test_all_lss_covered_with_mixed_sizes(self) -> None:
        small = [nx.path_graph(3).copy() for _ in range(4)]
        large = [nx.path_graph(5).copy() for _ in range(4)]
        ls = small + large
        groups = _group_isomorphic(ls, k=2, sigma=0.1, seed=0)
        assert _all_nodes_covered(ls, groups)


# ---------------------------------------------------------------------------
# Edge cases: sigma=0, sigma=1, k=1, edgeless LSs
# ---------------------------------------------------------------------------


class TestEdgeCases:
    """Boundary conditions for sigma, k, and graph topology."""

    def test_sigma_zero_uses_min_support_one(self) -> None:
        """sigma=0 → min_support=max(1, int(0*n))=1; every single-node
        pattern qualifies as frequent — grouping still covers all LSs."""
        ls = _make_ls(lambda: nx.cycle_graph(4), 6)
        groups = _group_isomorphic(ls, k=2, sigma=0.0, seed=0)
        assert _all_nodes_covered(ls, groups)
        assert all(isinstance(g, nx.Graph) for grp in groups for g in grp)

    def test_sigma_zero_total_count_preserved(self) -> None:
        """sigma=0: total members == input size."""
        n = 7
        ls = _make_ls(lambda: nx.path_graph(3), n)
        groups = _group_isomorphic(ls, k=3, sigma=0.0, seed=0)
        assert sum(len(grp) for grp in groups) == n

    def test_sigma_one_only_universal_patterns(self) -> None:
        """sigma=1 → min_support=n; only patterns present in ALL LSs are
        frequent. With identical LSs every pattern qualifies, so grouping
        is identical to the standard case."""
        ls = _make_ls(lambda: nx.cycle_graph(4), 6)
        groups = _group_isomorphic(ls, k=2, sigma=1.0, seed=0)
        assert _all_nodes_covered(ls, groups)

    def test_sigma_one_heterogeneous_falls_back_to_random(self) -> None:
        """sigma=1 with structurally distinct LSs: no pattern can be
        universal across all of them, so the fallback random grouping
        activates. Coverage invariant must still hold."""
        ls = [
            nx.cycle_graph(4).copy(),
            nx.path_graph(4).copy(),
            nx.star_graph(3).copy(),
            nx.complete_graph(4).copy(),
            nx.cycle_graph(4).copy(),
            nx.path_graph(4).copy(),
        ]
        groups = _group_isomorphic(ls, k=2, sigma=1.0, seed=0)
        assert _all_nodes_covered(ls, groups)

    def test_k1_each_ls_forms_own_group(self) -> None:
        """k=1: every LS must be its own group (no grouping is needed)."""
        n = 5
        ls = _make_ls(lambda: nx.cycle_graph(4), n)
        groups = _group_isomorphic(ls, k=1, sigma=0.1, seed=0)
        assert sum(len(grp) for grp in groups) == n
        assert all(len(grp) == 1 for grp in groups), (
            f"Expected all groups of size 1 with k=1, got sizes: "
            f"{[len(grp) for grp in groups]}"
        )

    def test_k1_coverage_invariant(self) -> None:
        """k=1: coverage invariant holds — each LS appears exactly once."""
        ls = _make_ls(lambda: nx.path_graph(3), 4)
        groups = _group_isomorphic(ls, k=1, sigma=0.2, seed=0)
        assert _all_nodes_covered(ls, groups)

    def test_edgeless_lss_mf_zero_tiebreak_by_hash(self) -> None:
        """When all LSs have n_edges=0, mf=0.0 for every pattern and the
        tiebreak falls to the smallest WL hash string. Grouping must still
        cover all LSs and respect D-06."""
        n = 5
        # Isolated-node graphs: no edges, so every subgraph has 0 edges.
        ls = [nx.Graph() for _ in range(n)]
        for g in ls:
            g.add_nodes_from(range(3))  # 3 isolated nodes, 0 edges
        groups = _group_isomorphic(ls, k=2, sigma=0.1, seed=0)
        assert sum(len(grp) for grp in groups) == n
        assert _all_nodes_covered(ls, groups)

    def test_edgeless_lss_all_graphs_preserved(self) -> None:
        """Edgeless LSs: every returned element is still an nx.Graph."""
        ls = [nx.Graph() for _ in range(4)]
        for g in ls:
            g.add_nodes_from(range(2))
        groups = _group_isomorphic(ls, k=2, sigma=0.1, seed=0)
        for grp in groups:
            for item in grp:
                assert isinstance(item, nx.Graph)
