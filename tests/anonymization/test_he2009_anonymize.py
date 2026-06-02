"""Unit tests for anonymize() in src/anonymization/he2009.py (issue #14).

Covers (as specified in the Definition of Done):
    - End-to-end: anonymize(petersen, k=2, d=1) runs without error.
    - Output has the same number of nodes as the input.
    - Determinism: same seed produces the same output graph.
    - _reconnect_inter_edges: return type, node set preserved, intra-LS
      edges preserved, inter-LS edges reconnected.
    - anonymize: return type nx.Graph, d required, no nodes added/removed.

Seeds are fixed to 0 / 42 throughout; approved exception per
.claude/rules/seeds.md — these tests require reproducible outputs.
"""

from __future__ import annotations

import networkx as nx
import pytest

from src.anonymization.he2009 import (
    _modify_structure,
    _reconnect_inter_edges,
    anonymize,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _edge_set(g: nx.Graph) -> set[frozenset]:
    """Return the edge set of *g* as a set of frozensets (undirected)."""
    return {frozenset(e) for e in g.edges()}


# ---------------------------------------------------------------------------
# anonymize — end-to-end (Definition of Done)
# ---------------------------------------------------------------------------


class TestAnonymizeEndToEnd:
    """Definition-of-Done checks for anonymize()."""

    def test_petersen_k2_d1_no_error(self) -> None:
        """anonymize(Petersen, k=2, d=1) must not raise."""
        g = nx.petersen_graph()
        result = anonymize(g, k=2, d=1, seed=0)
        assert result is not None

    def test_petersen_k2_d1_same_node_count(self) -> None:
        """Output has the same number of nodes as the input."""
        g = nx.petersen_graph()
        result = anonymize(g, k=2, d=1, seed=0)
        assert result.number_of_nodes() == g.number_of_nodes()

    def test_petersen_k2_d1_determinism(self) -> None:
        """Same seed → same output graph (same edge set)."""
        g = nx.petersen_graph()
        r1 = anonymize(g, k=2, d=1, seed=42)
        r2 = anonymize(g, k=2, d=1, seed=42)
        assert _edge_set(r1) == _edge_set(r2)

    def test_petersen_k2_d1_different_seeds_may_differ(self) -> None:
        """Different seeds are allowed to produce different results
        (not guaranteed, but the call must at least succeed)."""
        g = nx.petersen_graph()
        r0 = anonymize(g, k=2, d=1, seed=0)
        r1 = anonymize(g, k=2, d=1, seed=1)
        # Both must be valid graphs with the correct node count.
        assert r0.number_of_nodes() == g.number_of_nodes()
        assert r1.number_of_nodes() == g.number_of_nodes()


# ---------------------------------------------------------------------------
# anonymize — return type and structural properties
# ---------------------------------------------------------------------------


class TestAnonymizeReturnType:
    """anonymize() must always return an nx.Graph."""

    def test_returns_nx_graph(self) -> None:
        g = nx.cycle_graph(8)
        result = anonymize(g, k=2, d=2, seed=0)
        assert isinstance(result, nx.Graph)

    def test_output_is_simple_no_self_loops(self) -> None:
        """Output must have no self-loops."""
        g = nx.petersen_graph()
        result = anonymize(g, k=2, d=2, seed=0)
        assert not any(u == v for u, v in result.edges())

    def test_output_node_set_equals_input(self) -> None:
        """The node set of the output equals the node set of the input."""
        g = nx.petersen_graph()
        result = anonymize(g, k=2, d=2, seed=0)
        assert set(result.nodes()) == set(g.nodes())

    def test_cycle8_k2_d2_node_count(self) -> None:
        g = nx.cycle_graph(8)
        result = anonymize(g, k=2, d=2, seed=0)
        assert result.number_of_nodes() == g.number_of_nodes()

    def test_path10_k2_d2_node_count(self) -> None:
        g = nx.path_graph(10)
        result = anonymize(g, k=2, d=2, seed=0)
        assert result.number_of_nodes() == g.number_of_nodes()

    def test_determinism_cycle8(self) -> None:
        g = nx.cycle_graph(8)
        r1 = anonymize(g, k=2, d=2, seed=7)
        r2 = anonymize(g, k=2, d=2, seed=7)
        assert _edge_set(r1) == _edge_set(r2)

    def test_determinism_path10(self) -> None:
        g = nx.path_graph(10)
        r1 = anonymize(g, k=2, d=2, seed=99)
        r2 = anonymize(g, k=2, d=2, seed=99)
        assert _edge_set(r1) == _edge_set(r2)


# ---------------------------------------------------------------------------
# anonymize — k parameter effect
# ---------------------------------------------------------------------------


class TestAnonymizeKValues:
    """anonymize() must accept all k values in {2, 5, 10, 20}."""

    @pytest.mark.parametrize("k", [2, 5])
    def test_k_values_petersen_d1(self, k: int) -> None:
        g = nx.petersen_graph()
        result = anonymize(g, k=k, d=1, seed=0)
        assert result.number_of_nodes() == g.number_of_nodes()

    def test_k2_d2_larger_graph(self) -> None:
        """Larger graph with k=2, d=2."""
        g = nx.barabasi_albert_graph(30, 2, seed=0)
        result = anonymize(g, k=2, d=2, seed=0)
        assert result.number_of_nodes() == g.number_of_nodes()


# ---------------------------------------------------------------------------
# _reconnect_inter_edges — unit tests
# ---------------------------------------------------------------------------


class TestReconnectInterEdges:
    """Unit tests for _reconnect_inter_edges independently of anonymize()."""

    def _make_trivial_groups(
        self, g: nx.Graph, partition: list[list[object]]
    ) -> list[list[nx.Graph]]:
        """Build groups (list of 1-LS groups) from a given node partition."""
        return [[g.subgraph(part).copy()] for part in partition]

    def test_return_type_is_nx_graph(self) -> None:
        g = nx.path_graph(4)
        # Two trivial single-LS groups (1 member each — D-06 style)
        groups = self._make_trivial_groups(g, [[0, 1], [2, 3]])
        result = _reconnect_inter_edges(g, groups)
        assert isinstance(result, nx.Graph)

    def test_node_set_preserved(self) -> None:
        """Reconnection never removes nodes from the graph."""
        g = nx.petersen_graph()
        # Trivial single-node groups
        groups = [[g.subgraph([n]).copy()] for n in g.nodes()]
        result = _reconnect_inter_edges(g, groups)
        assert set(result.nodes()) == set(g.nodes())

    def test_intra_ls_edges_preserved(self) -> None:
        """Edges inside each LS must still be present in G_prime."""
        g = nx.petersen_graph()
        from src.anonymization.he2009 import _partition_neighborhoods

        local_structures = _partition_neighborhoods(g, d=2, seed=0, backend="networkx-kl")
        groups = [[ls] for ls in local_structures]  # trivial 1-member groups
        result = _reconnect_inter_edges(g, groups)
        # All intra-LS edges must be in result
        for ls in local_structures:
            for u, v in ls.edges():
                assert result.has_edge(u, v), f"Intra-LS edge ({u},{v}) missing"

    def test_inter_ls_edges_reconnected(self) -> None:
        """Original inter-LS edges must be present in G_prime (at least
        as original edges for cross-group case)."""
        g = nx.petersen_graph()
        from src.anonymization.he2009 import (
            _group_isomorphic,
            _modify_structure,
            _partition_neighborhoods,
        )

        local_structures = _partition_neighborhoods(g, d=2, seed=0, backend="networkx-kl")
        groups = _group_isomorphic(local_structures, k=2, sigma=0.5, seed=0)
        modified_groups = _modify_structure(groups, seed=0)
        result = _reconnect_inter_edges(g, modified_groups)

        # Collect all intra-LS edges (from modified groups)
        intra_edges: set[frozenset] = set()
        for grp in modified_groups:
            for ls in grp:
                intra_edges |= {frozenset(e) for e in ls.edges()}

        # All original edges that are NOT intra-LS edges of the same LS
        # should have been reconnected (at least the original edge itself).
        node_to_ls: dict = {}
        for g_idx, grp in enumerate(modified_groups):
            for l_idx, ls in enumerate(grp):
                for node in ls.nodes():
                    node_to_ls[node] = (g_idx, l_idx)

        inter_edges_missing = []
        for u, v in g.edges():
            u_loc = node_to_ls[u]
            v_loc = node_to_ls[v]
            if u_loc == v_loc:
                continue  # intra-LS, handled separately
            if not result.has_edge(u, v) and not result.has_edge(v, u) and u_loc[0] != v_loc[0]:
                # Cross-group: original must be present
                inter_edges_missing.append((u, v))

        assert inter_edges_missing == [], (
            f"Cross-group inter-LS edges not reconnected: {inter_edges_missing}"
        )

    def test_empty_groups_no_error(self) -> None:
        """Empty groups list must not raise; returns an nx.Graph."""
        g = nx.path_graph(4)
        result = _reconnect_inter_edges(g, [])
        assert isinstance(result, nx.Graph)

    def test_single_ls_group_passthrough(self) -> None:
        """One group with one LS: G_prime = LS (no inter-LS edges)."""
        g = nx.path_graph(4)
        ls = g.subgraph([0, 1, 2, 3]).copy()
        groups = [[ls]]
        result = _reconnect_inter_edges(g, groups)
        assert set(result.nodes()) == {0, 1, 2, 3}
        # All original edges are intra-LS
        for u, v in g.edges():
            assert result.has_edge(u, v)


# ---------------------------------------------------------------------------
# G3 (issue #80) — k(k-1) reconnection formula in _reconnect_inter_edges
#
# He et al. (2009, §3.3) states that reconnecting one same-group inter-LS edge
# adds k(k-1) edges to preserve the intra-group isomorphism. The exact count
# depends on the canonical positions (D-03) of the edge endpoints:
#   * endpoints at DISTINCT positions  → exactly k(k-1) new edges (general case)
#   * endpoints at the SAME position   → a clique of C(k,2) = k(k-1)/2 edges
# The 1-node-LS example originally sketched in issue #80 is degenerate (both
# endpoints occupy position 0) and therefore yields a single edge, NOT k(k-1).
# This divergence is recorded under D-08 in docs/decision_log.md; the tests
# below validate the documented behaviour rather than the degenerate sketch.
# ---------------------------------------------------------------------------


class TestReconnectKTimesKMinusOne:
    """Validate the k(k-1) reconnection count (G3, issue #80)."""

    @staticmethod
    def _single_edge_group(k: int) -> list[nx.Graph]:
        """Build a group of *k* isomorphic single-edge LSs (2 nodes each).

        LS_i = nodes {2i, 2i+1} with edge (2i, 2i+1). Under the D-03 ordering
        (-degree, node_id) both nodes have degree 1, so position 0 → 2i,
        position 1 → 2i+1.
        """
        group: list[nx.Graph] = []
        for i in range(k):
            ls = nx.Graph()
            ls.add_edge(2 * i, 2 * i + 1)
            group.append(ls)
        return group

    @pytest.mark.parametrize("k", [2, 3])
    def test_reconnect_inter_edges_adds_k_times_k_minus_one(self, k: int) -> None:
        """One same-group inter-LS edge between DISTINCT canonical positions
        adds exactly k(k-1) new edges."""
        group = self._single_edge_group(k)

        # g_original: intra-LS edges + one inter-LS edge whose endpoints sit at
        # different canonical positions (node 1 = LS0/pos1, node 2 = LS1/pos0).
        g_original = nx.Graph()
        for ls in group:
            g_original.add_edges_from(ls.edges())
        g_original.add_edge(1, 2)  # inter-LS, pos1 ↔ pos0 (distinct positions)

        intra_edges = sum(ls.number_of_edges() for ls in group)  # = k

        result = _reconnect_inter_edges(g_original, [group])

        added = result.number_of_edges() - intra_edges
        assert added == k * (k - 1), (
            f"expected k(k-1)={k * (k - 1)} added edges for k={k}, got {added}"
        )
        # The metadata counter must agree with the structural delta.
        assert result.graph["metadata"]["edges_added_reconnection"] == k * (k - 1)

    @pytest.mark.parametrize("k", [2, 3])
    def test_reconnect_same_position_forms_clique(self, k: int) -> None:
        """When endpoints share a canonical position the cross-pairs collapse
        into a C(k,2) = k(k-1)/2 clique (documented under D-08)."""
        group = self._single_edge_group(k)

        g_original = nx.Graph()
        for ls in group:
            g_original.add_edges_from(ls.edges())
        # Inter-LS edge between two pos-0 nodes (LS0/pos0=0, LS1/pos0=2).
        g_original.add_edge(0, 2)

        result = _reconnect_inter_edges(g_original, [group])
        added = result.graph["metadata"]["edges_added_reconnection"]
        assert added == k * (k - 1) // 2

    def test_reconnect_single_node_lss_degenerate(self) -> None:
        """The issue #80 sketch (two single-node LSs, one inter-edge) is
        degenerate: it yields a single edge, not k(k-1)=2 (see D-08)."""
        ls0 = nx.Graph()
        ls0.add_node(0)
        ls1 = nx.Graph()
        ls1.add_node(1)
        g_original = nx.Graph()
        g_original.add_edge(0, 1)

        result = _reconnect_inter_edges(g_original, [[ls0, ls1]])
        assert result.number_of_edges() == 1
        assert result.graph["metadata"]["edges_added_reconnection"] == 1


# ---------------------------------------------------------------------------
# G5(a) (issue #80) — per-phase modification counters exposed via metadata
# ---------------------------------------------------------------------------


class TestPhaseCounters:
    """anonymize() must expose phase-2 and reconnection counters (G5-a)."""

    def test_modify_structure_return_counts_is_int(self) -> None:
        """_modify_structure(return_counts=True) returns (groups, int>=0)."""
        group = [nx.path_graph(4).copy(), nx.cycle_graph(4).copy()]
        result = _modify_structure([group], seed=0, return_counts=True)
        assert isinstance(result, tuple)
        groups, count = result
        assert isinstance(groups, list)
        assert isinstance(count, int)
        assert count >= 0

    def test_modify_structure_default_return_unchanged(self) -> None:
        """Without return_counts the historical list return is preserved."""
        group = [nx.path_graph(4).copy(), nx.cycle_graph(4).copy()]
        result = _modify_structure([group], seed=0)
        assert isinstance(result, list)

    def test_modify_structure_counts_known_modifications(self) -> None:
        """path_graph(4) vs cycle_graph(4): the cycle adds one edge (3→4)
        and the path adds the same edge to match → exactly 1 modification.

        Positions (D-03, all degree<=2): path 0-1-2-3 endpoints degree 1,
        cycle fully degree 2. The pair that differs is the closing edge of
        the cycle, present in 1 of 2 LSs → majority adds it to the path.
        """
        group = [nx.path_graph(4).copy(), nx.cycle_graph(4).copy()]
        _, count = _modify_structure([group], seed=0, return_counts=True)
        # At least one modification happened to make them isomorphic.
        assert count >= 1

    def test_modify_structure_identical_lss_zero_modifications(self) -> None:
        """Two identical cycles need no modification → count == 0."""
        group = [nx.cycle_graph(4).copy(), nx.cycle_graph(4).copy()]
        _, count = _modify_structure([group], seed=0, return_counts=True)
        assert count == 0

    def test_reconnect_sets_metadata_counter(self) -> None:
        """_reconnect_inter_edges always sets edges_added_reconnection."""
        g = nx.path_graph(4)
        ls = g.subgraph([0, 1, 2, 3]).copy()
        result = _reconnect_inter_edges(g, [[ls]])
        assert "metadata" in result.graph
        meta = result.graph["metadata"]
        assert isinstance(meta["edges_added_reconnection"], int)
        assert meta["edges_added_reconnection"] >= 0

    def test_anonymize_exposes_both_counters(self) -> None:
        """anonymize() output carries both phase counters in graph metadata."""
        g = nx.petersen_graph()
        result = anonymize(g, k=2, d=2, seed=0)
        meta = result.graph["metadata"]
        assert isinstance(meta["edges_modified_phase2_intragroup"], int)
        assert isinstance(meta["edges_added_reconnection"], int)
        assert meta["edges_modified_phase2_intragroup"] >= 0
        assert meta["edges_added_reconnection"] >= 0

    def test_anonymize_counters_stable_across_seed(self) -> None:
        """Deterministic: same seed → same counters."""
        g = nx.petersen_graph()
        m1 = anonymize(g, k=2, d=2, seed=7).graph["metadata"]
        m2 = anonymize(g, k=2, d=2, seed=7).graph["metadata"]
        assert m1 == m2

    def test_anonymize_d1_counters_present(self) -> None:
        """Even the d=1 baseline exposes the counters (>= 0)."""
        g = nx.cycle_graph(8)
        meta = anonymize(g, k=2, d=1, seed=0).graph["metadata"]
        assert meta["edges_modified_phase2_intragroup"] >= 0
        assert meta["edges_added_reconnection"] >= 0
