"""Unit tests for _modify_structure in src/anonymization/he2009.py.

Covers (as specified in issue #13):
    - Output is still valid: no self-loops, no multi-edges.
    - Determinism: same seed produces same output.
    - add_only=True: no edge is removed.
    - Return type: list[list[nx.Graph]].
    - Isomorphism: LSs in each complete group become isomorphic.
    - Incomplete groups (D-06): single-member groups pass through unchanged.
    - Mixed-size groups (D-07 violation): passed through without modification.
    - Empty / zero-node groups: handled gracefully.
    - Input graphs are not modified (function works on copies).

Seeds are fixed to 0 throughout; this is an approved exception per
.claude/rules/seeds.md — _modify_structure is deterministic by design
(no random choices in Phase 1 or Phase 2), so seed choice carries no
algorithmic significance for the tests below.
"""

from __future__ import annotations

import networkx as nx

from src.anonymization.he2009 import _modify_structure

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_group(factory, count: int) -> list[nx.Graph]:
    """Return *count* independent copies produced by *factory*."""
    return [factory() for _ in range(count)]


def _all_isomorphic(group: list[nx.Graph]) -> bool:
    """True iff every graph in *group* is isomorphic to every other."""
    if len(group) < 2:
        return True
    ref = group[0]
    return all(nx.is_isomorphic(ref, g) for g in group[1:])


def _has_self_loops(g: nx.Graph) -> bool:
    return any(u == v for u, v in g.edges())


def _is_simple(g: nx.Graph) -> bool:
    """True iff g has no self-loops and no multi-edges (i.e., is simple)."""
    return not _has_self_loops(g) and not isinstance(g, nx.MultiGraph)


# ---------------------------------------------------------------------------
# Return type
# ---------------------------------------------------------------------------


class TestReturnType:
    """_modify_structure always returns list[list[nx.Graph]]."""

    def test_empty_input_returns_empty_list(self) -> None:
        result = _modify_structure([], seed=0)
        assert result == []

    def test_nested_type_is_list_of_list_of_graph(self) -> None:
        group = _make_group(lambda: nx.cycle_graph(4).copy(), 2)
        result = _modify_structure([group], seed=0)
        assert isinstance(result, list)
        for grp in result:
            assert isinstance(grp, list)
            for g in grp:
                assert isinstance(g, nx.Graph)

    def test_multiple_groups_preserved(self) -> None:
        g1 = _make_group(lambda: nx.path_graph(3).copy(), 2)
        g2 = _make_group(lambda: nx.cycle_graph(4).copy(), 3)
        result = _modify_structure([g1, g2], seed=0)
        assert len(result) == 2


# ---------------------------------------------------------------------------
# No self-loops, no multi-edges (valid output)
# ---------------------------------------------------------------------------


class TestGraphValidity:
    """Output graphs must be simple (no self-loops, no multi-edges)."""

    def test_no_self_loops_after_add_delete(self) -> None:
        group = _make_group(lambda: nx.path_graph(4).copy(), 3)
        result = _modify_structure([group], seed=0)
        for ls in result[0]:
            assert not _has_self_loops(ls), "Self-loop found after _modify_structure"

    def test_no_self_loops_add_only(self) -> None:
        group = _make_group(lambda: nx.cycle_graph(5).copy(), 2)
        result = _modify_structure([group], seed=0, add_only=True)
        for ls in result[0]:
            assert not _has_self_loops(ls)

    def test_no_multi_edges_after_modify(self) -> None:
        """nx.Graph disallows multi-edges by construction; verify no exception
        was silently swallowed and edges are still simple."""
        group = _make_group(lambda: nx.complete_graph(4).copy(), 2)
        result = _modify_structure([group], seed=0)
        for ls in result[0]:
            assert _is_simple(ls)

    def test_no_self_loops_heterogeneous_group(self) -> None:
        """Group with structurally different LSs: no self-loops after modify."""
        ls_a = nx.path_graph(4).copy()
        ls_b = nx.cycle_graph(4).copy()
        result = _modify_structure([[ls_a, ls_b]], seed=0)
        for ls in result[0]:
            assert not _has_self_loops(ls)


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------


class TestDeterminism:
    """Same seed must produce the same output graphs."""

    def test_same_seed_same_edge_count(self) -> None:
        group = _make_group(lambda: nx.path_graph(5).copy(), 3)
        r1 = _modify_structure([group], seed=0)
        r2 = _modify_structure([group], seed=0)
        for ls1, ls2 in zip(r1[0], r2[0], strict=True):
            assert ls1.number_of_edges() == ls2.number_of_edges()

    def test_same_seed_same_edges(self) -> None:
        group = _make_group(lambda: nx.cycle_graph(4).copy(), 2)
        r1 = _modify_structure([group], seed=42)
        r2 = _modify_structure([group], seed=42)
        for ls1, ls2 in zip(r1[0], r2[0], strict=True):
            assert set(ls1.edges()) == set(ls2.edges())

    def test_same_seed_multiple_groups(self) -> None:
        g1 = _make_group(lambda: nx.path_graph(3).copy(), 2)
        g2 = _make_group(lambda: nx.star_graph(3).copy(), 2)
        r1 = _modify_structure([g1, g2], seed=7)
        r2 = _modify_structure([g1, g2], seed=7)
        for grp1, grp2 in zip(r1, r2, strict=True):
            for ls1, ls2 in zip(grp1, grp2, strict=True):
                assert set(ls1.edges()) == set(ls2.edges())


# ---------------------------------------------------------------------------
# add_only=True: no edges removed
# ---------------------------------------------------------------------------


class TestAddOnly:
    """With add_only=True, no edge present in any input LS should be removed."""

    def _original_edges(self, groups: list[list[nx.Graph]]) -> list[list[set]]:
        """Return the edge sets of all input LSs (as frozensets for symmetry)."""
        return [[frozenset(frozenset(e) for e in ls.edges()) for ls in grp] for grp in groups]

    def test_no_edge_removed_add_only_path(self) -> None:
        group = _make_group(lambda: nx.path_graph(4).copy(), 3)
        original_edges = [{frozenset(e) for e in ls.edges()} for ls in group]
        result = _modify_structure([group], seed=0, add_only=True)
        for orig, modified in zip(original_edges, result[0], strict=True):
            modified_edges = {frozenset(e) for e in modified.edges()}
            # Every original edge must still be present.
            assert orig.issubset(modified_edges), (
                f"Edge(s) removed under add_only=True: {orig - modified_edges}"
            )

    def test_no_edge_removed_add_only_cycle(self) -> None:
        group = _make_group(lambda: nx.cycle_graph(5).copy(), 2)
        original_edges = [{frozenset(e) for e in ls.edges()} for ls in group]
        result = _modify_structure([group], seed=0, add_only=True)
        for orig, modified in zip(original_edges, result[0], strict=True):
            modified_edges = {frozenset(e) for e in modified.edges()}
            assert orig.issubset(modified_edges)

    def test_add_only_edge_count_non_decreasing(self) -> None:
        """add_only must not decrease the edge count of any LS."""
        group = [nx.path_graph(4).copy(), nx.cycle_graph(4).copy()]
        original_counts = [ls.number_of_edges() for ls in group]
        result = _modify_structure([group], seed=0, add_only=True)
        for orig_count, modified in zip(original_counts, result[0], strict=True):
            assert modified.number_of_edges() >= orig_count

    def test_add_only_false_may_remove_edges(self) -> None:
        """add_only=False is allowed to reduce edge count (not obligated to)."""
        # Build a group where the majority-vote will remove edges:
        # 1 complete graph (all edges) vs 2 empty-ish graphs (no edges)
        # For most pairs, majority = no-edge → edges will be removed.
        complete = nx.complete_graph(4).copy()
        sparse1 = nx.Graph()
        sparse1.add_nodes_from(range(4))
        sparse2 = nx.Graph()
        sparse2.add_nodes_from(range(4))
        group = [complete, sparse1, sparse2]
        result = _modify_structure([group], seed=0, add_only=False)
        # complete graph should have fewer edges after modification
        result_complete = result[0][0]
        assert result_complete.number_of_edges() <= complete.number_of_edges()


# ---------------------------------------------------------------------------
# Isomorphism: LSs in each complete group become isomorphic
# ---------------------------------------------------------------------------


class TestIsomorphism:
    """After modification, all LSs in a complete group must be isomorphic."""

    def test_identical_lss_remain_isomorphic(self) -> None:
        """Identical LSs → output is still isomorphic (trivially)."""
        group = _make_group(lambda: nx.cycle_graph(4).copy(), 3)
        result = _modify_structure([group], seed=0)
        assert _all_isomorphic(result[0])

    def test_path_vs_cycle_same_size_becomes_isomorphic(self) -> None:
        """path_graph(4) and cycle_graph(4) have the same node count;
        after modification they should be isomorphic."""
        ls_a = nx.path_graph(4).copy()
        ls_b = nx.cycle_graph(4).copy()
        result = _modify_structure([[ls_a, ls_b]], seed=0)
        assert _all_isomorphic(result[0])

    def test_star_vs_path_same_size_becomes_isomorphic(self) -> None:
        # star_graph(3) = 4 nodes, path_graph(4) = 4 nodes
        ls_a = nx.star_graph(3).copy()
        ls_b = nx.path_graph(4).copy()
        result = _modify_structure([[ls_a, ls_b]], seed=0)
        assert _all_isomorphic(result[0])

    def test_three_different_graphs_become_isomorphic(self) -> None:
        ls_a = nx.path_graph(4).copy()
        ls_b = nx.cycle_graph(4).copy()
        ls_c = nx.star_graph(3).copy()
        result = _modify_structure([[ls_a, ls_b, ls_c]], seed=0)
        assert _all_isomorphic(result[0])

    def test_add_only_produces_isomorphic_group(self) -> None:
        ls_a = nx.path_graph(4).copy()
        ls_b = nx.cycle_graph(4).copy()
        result = _modify_structure([[ls_a, ls_b]], seed=0, add_only=True)
        assert _all_isomorphic(result[0])

    def test_multiple_groups_each_isomorphic(self) -> None:
        g1 = [nx.path_graph(3).copy(), nx.star_graph(2).copy()]  # both 3 nodes
        g2 = [nx.cycle_graph(5).copy(), nx.path_graph(5).copy()]
        result = _modify_structure([g1, g2], seed=0)
        for grp in result:
            assert _all_isomorphic(grp)


# ---------------------------------------------------------------------------
# D-06: incomplete groups (< k members) pass through unchanged
# ---------------------------------------------------------------------------


class TestIncompleteGroups:
    """Single-member groups must be returned unchanged (D-06)."""

    def test_single_member_group_passthrough(self) -> None:
        ls = nx.cycle_graph(5).copy()
        orig_edges = set(ls.edges())
        result = _modify_structure([[ls]], seed=0)
        assert len(result) == 1
        assert len(result[0]) == 1
        assert set(result[0][0].edges()) == orig_edges

    def test_empty_group_passthrough(self) -> None:
        result = _modify_structure([[]], seed=0)
        assert result == [[]]

    def test_mixed_complete_and_incomplete(self) -> None:
        complete_group = _make_group(lambda: nx.path_graph(3).copy(), 2)
        incomplete_group = [nx.cycle_graph(3).copy()]
        orig_inc_edges = set(incomplete_group[0].edges())
        result = _modify_structure([complete_group, incomplete_group], seed=0)
        assert len(result) == 2
        # Incomplete group unchanged
        assert set(result[1][0].edges()) == orig_inc_edges
        # Complete group isomorphic
        assert _all_isomorphic(result[0])


# ---------------------------------------------------------------------------
# D-07 violation: mixed-size groups passed through without modification
# ---------------------------------------------------------------------------


class TestMixedSizeGroups:
    """Groups with LSs of different sizes must not be modified."""

    def test_mixed_size_group_passthrough(self) -> None:
        ls_small = nx.path_graph(3).copy()
        ls_large = nx.path_graph(5).copy()
        orig_small = set(ls_small.edges())
        orig_large = set(ls_large.edges())
        result = _modify_structure([[ls_small, ls_large]], seed=0)
        assert set(result[0][0].edges()) == orig_small
        assert set(result[0][1].edges()) == orig_large

    def test_mixed_size_does_not_raise(self) -> None:
        ls_a = nx.complete_graph(3).copy()
        ls_b = nx.complete_graph(5).copy()
        # Must not raise, just pass through
        result = _modify_structure([[ls_a, ls_b]], seed=0)
        assert len(result[0]) == 2


# ---------------------------------------------------------------------------
# Input graphs not modified (function works on copies)
# ---------------------------------------------------------------------------


class TestImmutability:
    """Input graphs must not be mutated by _modify_structure."""

    def test_input_lss_not_modified_add_delete(self) -> None:
        ls_a = nx.path_graph(4).copy()
        ls_b = nx.cycle_graph(4).copy()
        orig_a_edges = set(ls_a.edges())
        orig_b_edges = set(ls_b.edges())
        _modify_structure([[ls_a, ls_b]], seed=0, add_only=False)
        assert set(ls_a.edges()) == orig_a_edges
        assert set(ls_b.edges()) == orig_b_edges

    def test_input_lss_not_modified_add_only(self) -> None:
        ls_a = nx.path_graph(4).copy()
        ls_b = nx.cycle_graph(4).copy()
        orig_a_edges = set(ls_a.edges())
        orig_b_edges = set(ls_b.edges())
        _modify_structure([[ls_a, ls_b]], seed=0, add_only=True)
        assert set(ls_a.edges()) == orig_a_edges
        assert set(ls_b.edges()) == orig_b_edges


# ---------------------------------------------------------------------------
# Edge cases: empty/zero-node graphs, complete graphs, edgeless graphs
# ---------------------------------------------------------------------------


class TestEdgeCases:
    """Boundary conditions for graph topology."""

    def test_zero_node_lss_no_error(self) -> None:
        ls_a, ls_b = nx.Graph(), nx.Graph()
        result = _modify_structure([[ls_a, ls_b]], seed=0)
        assert len(result[0]) == 2

    def test_complete_graphs_stay_complete(self) -> None:
        """Two K4: already isomorphic; no edges should change."""
        group = _make_group(lambda: nx.complete_graph(4).copy(), 2)
        n_edges_before = group[0].number_of_edges()
        result = _modify_structure([group], seed=0)
        assert result[0][0].number_of_edges() == n_edges_before
        assert result[0][1].number_of_edges() == n_edges_before

    def test_edgeless_graphs_stay_edgeless(self) -> None:
        """Two graphs with nodes but no edges: remain edgeless."""
        ls_a = nx.Graph()
        ls_a.add_nodes_from(range(4))
        ls_b = nx.Graph()
        ls_b.add_nodes_from(range(4))
        result = _modify_structure([[ls_a, ls_b]], seed=0)
        assert result[0][0].number_of_edges() == 0
        assert result[0][1].number_of_edges() == 0

    def test_single_node_graphs(self) -> None:
        ls_a = nx.Graph()
        ls_a.add_node(0)
        ls_b = nx.Graph()
        ls_b.add_node(1)
        result = _modify_structure([[ls_a, ls_b]], seed=0)
        for ls in result[0]:
            assert ls.number_of_nodes() == 1
            assert ls.number_of_edges() == 0

    def test_k2_two_identical_cycles_unchanged(self) -> None:
        """Two identical cycle_graph(4): output equals input."""
        group = _make_group(lambda: nx.cycle_graph(4).copy(), 2)
        n_edges = group[0].number_of_edges()
        result = _modify_structure([group], seed=0)
        for ls in result[0]:
            assert ls.number_of_edges() == n_edges
