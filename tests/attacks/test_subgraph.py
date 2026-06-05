"""Tests for src/attacks/subgraph.py (issue #20).

Definition-of-Done coverage:
    - Typical case: target uniquely identifiable via hop-1 neighbourhood → True.
    - Multiple candidates: identical neighbourhood structures → False.
    - Zero candidates: neighbourhood absent from G_anon → False.
    - hop parameter: hop=2 discriminates when hop=1 fails (asymmetric lollipops).
    - Timeout: near-zero limit raises TimeoutError.
    - Invalid inputs: target not in G_orig → ValueError; hop < 1 → ValueError.

No random seeds needed: subgraph_attack() is deterministic and seed-free.
"""

from __future__ import annotations

import concurrent.futures
from unittest.mock import patch

import networkx as nx
import pytest

import src.attacks.subgraph as subgraph_mod
from src.attacks.subgraph import (
    _k_hop_induced_subgraph,
    subgraph_attack,
    subgraph_candidate_count,
    subgraph_candidate_counts,
)

# ---------------------------------------------------------------------------
# Helper: k-hop induced subgraph
# ---------------------------------------------------------------------------


class TestKHopInducedSubgraph:
    """Unit tests for the internal _k_hop_induced_subgraph helper."""

    def test_hop1_star_center(self) -> None:
        """hop=1 from the centre of a star includes centre + all leaves.

        star_graph(3): centre=0, leaves=1,2,3.
        """
        g = nx.star_graph(3)  # centre=0, leaves=1,2,3
        sub = _k_hop_induced_subgraph(g, node=0, hop=1)
        assert set(sub.nodes()) == {0, 1, 2, 3}
        assert sub.number_of_edges() == 3

    def test_hop1_star_leaf_excludes_other_leaves(self) -> None:
        """hop=1 from a leaf only includes that leaf and the centre."""
        g = nx.star_graph(3)
        sub = _k_hop_induced_subgraph(g, node=1, hop=1)
        assert set(sub.nodes()) == {0, 1}
        assert sub.number_of_edges() == 1

    def test_hop2_path_graph(self) -> None:
        """hop=2 from node 2 in a path 0-1-2-3-4 spans the whole graph."""
        g = nx.path_graph(5)
        sub = _k_hop_induced_subgraph(g, node=2, hop=2)
        assert set(sub.nodes()) == {0, 1, 2, 3, 4}

    def test_isolated_node_hop1(self) -> None:
        """An isolated node's 1-hop neighbourhood is just itself."""
        g = nx.Graph()
        g.add_nodes_from([0, 1, 2])
        sub = _k_hop_induced_subgraph(g, node=0, hop=1)
        assert set(sub.nodes()) == {0}
        assert sub.number_of_edges() == 0


# ---------------------------------------------------------------------------
# Typical case — unique identification (True)
# ---------------------------------------------------------------------------


class TestSubgraphAttackSuccess:
    """Attack returns True when exactly one candidate matches."""

    def test_star_center_unique_hop1(self) -> None:
        """Star graph: the centre has a unique degree-4 neighbourhood.

        nx.star_graph(4): centre=0 (degree 4), leaves 1-4 (degree 1 each).
        Centre's hop-1 neighbourhood is a star(4); no leaf has an isomorphic
        neighbourhood (leaf's hop-1 is a 2-node path).
        G_anon is identical, so the fingerprint is preserved → True.
        """
        g_orig = nx.star_graph(4)
        g_anon = g_orig.copy()
        assert subgraph_attack(g_orig, g_anon, target=0) is True

    def test_unique_neighbourhood_after_anonymisation(self) -> None:
        """Attack succeeds when anonymisation breaks symmetry in G_anon.

        G_orig: two degree-3 star centres (0 and 5); hop-1 of both are
                star(3) — the adversary cannot distinguish them on G_orig.
        G_anon: node 5's edges are restructured into a chain (5-6-7-8),
                so node 5 no longer has a star neighbourhood.

        On G_orig alone the attack fails (2 candidates).  When searching
        G_anon with the G_orig fingerprint, only node 0 has a matching
        star(3) neighbourhood → one candidate → True.
        """
        g_orig = nx.Graph()
        g_orig.add_edges_from([(0, 1), (0, 2), (0, 3), (5, 6), (5, 7), (5, 8)])

        g_anon = nx.Graph()
        # Node 5's structure changed from star to chain in G_anon
        g_anon.add_edges_from([(0, 1), (0, 2), (0, 3), (5, 6), (6, 7), (7, 8)])

        # Ambiguous on G_orig — two star(3) centres
        assert subgraph_attack(g_orig, g_orig, target=0) is False
        # Unique in G_anon — only node 0 retains star(3)
        assert subgraph_attack(g_orig, g_anon, target=0) is True


# ---------------------------------------------------------------------------
# Attack fails — target not uniquely identifiable (False)
# ---------------------------------------------------------------------------


class TestSubgraphAttackFailure:
    """Attack returns False when zero or multiple candidates match."""

    def test_symmetric_graph_multiple_candidates(self) -> None:
        """Path graph: nodes 1 and 3 have identical hop-1 neighbourhoods.

        path_graph(5): 0-1-2-3-4.
        Node 1's hop-1: {0,1,2} — path of 3 nodes, centre degree 2.
        Node 3's hop-1: {2,3,4} — path of 3 nodes, centre degree 2.
        Both are isomorphic → 2 candidates → False.
        """
        g_orig = nx.path_graph(5)
        g_anon = g_orig.copy()
        assert subgraph_attack(g_orig, g_anon, target=1) is False

    def test_regular_graph_all_candidates(self) -> None:
        """Cycle graph: every node has an identical hop-1 neighbourhood.

        cycle_graph(5): each node has degree 2 and its hop-1 subgraph is
        always a path of 3 nodes → all 5 nodes are candidates → False.
        """
        g_orig = nx.cycle_graph(5)
        g_anon = g_orig.copy()
        assert subgraph_attack(g_orig, g_anon, target=0) is False

    def test_zero_candidates_all_isolated_in_anon(self) -> None:
        """Target's rich neighbourhood in G_orig has no match in G_anon.

        G_orig: star(3), target=0 (degree 3, hop-1 = 4-node star).
        G_anon: all nodes isolated.  No node in G_anon has a hop-1 subgraph
        isomorphic to a 4-node star → 0 candidates → False.
        """
        g_orig = nx.star_graph(3)
        g_anon = nx.Graph()
        g_anon.add_nodes_from(g_orig.nodes())  # same nodes, no edges
        assert subgraph_attack(g_orig, g_anon, target=0) is False


# ---------------------------------------------------------------------------
# hop parameter
# ---------------------------------------------------------------------------


class TestSubgraphAttackHop:
    """Deeper hop gives a more discriminating neighbourhood fingerprint."""

    def test_hop1_fails_hop2_succeeds(self) -> None:
        """hop=2 discriminates targets that are indistinguishable at hop=1.

        Graph: two "lollipop" structures (K3 triangle + path tail):
          Lollipop A (target=0): K3 at {0,1,2}, tail 0-3-4-5 (length 3).
          Lollipop B:            K3 at {6,7,8}, tail 6-9     (length 1).

        hop=1: both K3-path junction nodes (0 and 6) have hop-1 subgraphs
               isomorphic to K3+pendant (4 nodes, 4 edges) → 2 candidates
               → False.
        hop=2: node 0's 2-hop = K3 + 2-step tail = 5 nodes, 5 edges.
               node 6's 2-hop = K3 + 1-step tail = 4 nodes, 4 edges.
               Different sizes → not isomorphic → only node 0 qualifies → True.
        """
        g = nx.Graph()
        # Lollipop A: triangle + tail of 3
        g.add_edges_from([(0, 1), (0, 2), (1, 2), (0, 3), (3, 4), (4, 5)])
        # Lollipop B: triangle + tail of 1
        g.add_edges_from([(6, 7), (6, 8), (7, 8), (6, 9)])

        # hop=1: both junction nodes 0 and 6 are candidates
        assert subgraph_attack(g, g, target=0, hop=1) is False
        # hop=2: only node 0 qualifies (unique 5-node neighbourhood)
        assert subgraph_attack(g, g, target=0, hop=2) is True

    def test_hop2_fails_for_vertex_transitive_graph(self) -> None:
        """hop=2 still fails when every node has the same local structure.

        cycle_graph(8) is vertex-transitive: all nodes are structurally
        equivalent at any hop.  With hop=1 all 8 nodes are candidates;
        with hop=2 all 8 nodes still have isomorphic P5 neighbourhoods
        → False at both hops.
        """
        g = nx.cycle_graph(8)
        assert subgraph_attack(g, g, target=0, hop=1) is False
        assert subgraph_attack(g, g, target=0, hop=2) is False


# ---------------------------------------------------------------------------
# Timeout
# ---------------------------------------------------------------------------


class TestSubgraphAttackTimeout:
    """Exceeding the timeout raises TimeoutError."""

    def test_timeout_raises_timeout_error(self) -> None:
        """Mocking TimeoutError from future.result() propagates correctly.

        Uses unittest.mock to simulate a slow search without actually
        waiting, ensuring the TimeoutError path is exercised deterministically.
        """
        g = nx.cycle_graph(5)
        with (
            patch(
                "concurrent.futures.Future.result",
                side_effect=concurrent.futures.TimeoutError,
            ),
            pytest.raises(TimeoutError, match="exceeded timeout"),
        ):
            subgraph_attack(g, g, target=0, hop=1, timeout=0.001)

    def test_no_timeout_completes_normally(self) -> None:
        """timeout=None (default) does not wrap execution in a Future."""
        g = nx.star_graph(3)
        # Centre is unique → True, no TimeoutError expected
        result = subgraph_attack(g, g, target=0, timeout=None)
        assert result is True


# ---------------------------------------------------------------------------
# Invalid inputs
# ---------------------------------------------------------------------------


class TestSubgraphAttackInvalidInputs:
    """subgraph_attack() raises ValueError on invalid arguments."""

    def test_target_not_in_g_orig_raises(self) -> None:
        """A target absent from G_orig is an invalid query → ValueError."""
        g_orig = nx.path_graph(3)
        g_anon = g_orig.copy()
        with pytest.raises(ValueError, match="not found in G_orig"):
            subgraph_attack(g_orig, g_anon, target=99)

    def test_hop_zero_raises(self) -> None:
        """hop=0 is not a positive integer → ValueError."""
        g = nx.path_graph(3)
        with pytest.raises(ValueError, match="positive integer"):
            subgraph_attack(g, g, target=0, hop=0)

    def test_hop_negative_raises(self) -> None:
        """Negative hop is undefined → ValueError."""
        g = nx.path_graph(3)
        with pytest.raises(ValueError, match="positive integer"):
            subgraph_attack(g, g, target=0, hop=-1)

    def test_hop_float_raises(self) -> None:
        """Float hop (e.g., 1.5) is not a valid integer → ValueError."""
        g = nx.path_graph(3)
        with pytest.raises(ValueError, match="positive integer"):
            subgraph_attack(g, g, target=0, hop=1.5)


# ---------------------------------------------------------------------------
# subgraph_candidate_count — diagnostic observable (issue #93)
# ---------------------------------------------------------------------------


class TestSubgraphCandidateCount:
    """subgraph_candidate_count returns the raw #isomorphic candidates.

    This is the observable that distinguishes a *zero* re-identification rate
    as "no candidates" (H1/H2) vs "many candidates", which subgraph_attack's
    bool collapses.
    """

    def test_unique_candidate_count_one(self) -> None:
        """A uniquely identifiable target has exactly one candidate."""
        g = nx.star_graph(4)
        assert subgraph_candidate_count(g, g, target=0) == 1

    def test_zero_candidates_when_absent_from_anon(self) -> None:
        """Rich neighbourhood absent from G_anon → zero candidates (H1/H2)."""
        g_orig = nx.star_graph(3)
        g_anon = nx.Graph()
        g_anon.add_nodes_from(g_orig.nodes())  # same nodes, no edges
        assert subgraph_candidate_count(g_orig, g_anon, target=0) == 0

    def test_multiple_candidates_in_symmetric_graph(self) -> None:
        """path_graph(5): nodes 1 and 3 share node 1's hop-1 fingerprint.

        The three interior nodes (1, 2, 3) all have a P3 hop-1 neighbourhood,
        so node 1's fingerprint matches three candidates.
        """
        g = nx.path_graph(5)
        assert subgraph_candidate_count(g, g, target=1) == 3

    def test_all_candidates_in_regular_graph(self) -> None:
        """cycle_graph(5): every node matches → count equals |V|."""
        g = nx.cycle_graph(5)
        assert subgraph_candidate_count(g, g, target=0) == 5

    def test_attack_is_count_equals_one(self) -> None:
        """subgraph_attack is exactly the predicate count == 1."""
        for g, target in [
            (nx.star_graph(4), 0),  # unique → 1
            (nx.path_graph(5), 1),  # 3 candidates
            (nx.cycle_graph(5), 0),  # 5 candidates
        ]:
            count = subgraph_candidate_count(g, g, target=target)
            assert subgraph_attack(g, g, target=target) is (count == 1)

    def test_invalid_target_raises(self) -> None:
        """Same validation contract as subgraph_attack."""
        g = nx.path_graph(3)
        with pytest.raises(ValueError, match="not found in G_orig"):
            subgraph_candidate_count(g, g, target=99)

    def test_invalid_hop_raises(self) -> None:
        g = nx.path_graph(3)
        with pytest.raises(ValueError, match="positive integer"):
            subgraph_candidate_count(g, g, target=0, hop=0)

    def test_timeout_raises_timeout_error(self) -> None:
        """A timed-out search raises TimeoutError (caller decides how to count)."""
        g = nx.cycle_graph(5)
        with (
            patch(
                "concurrent.futures.Future.result",
                side_effect=concurrent.futures.TimeoutError,
            ),
            pytest.raises(TimeoutError, match="exceeded timeout"),
        ):
            subgraph_candidate_count(g, g, target=0, hop=1, timeout=0.001)


# ---------------------------------------------------------------------------
# subgraph_candidate_counts — WL-hash bucketing fast path (issue #139)
# ---------------------------------------------------------------------------


def _battery_graphs() -> list[tuple[str, nx.Graph]]:
    """A spread of small graphs exercising distinct neighbourhood fingerprints.

    Covers: stars (unique hub), paths (interior twins), cycles
    (vertex-transitive), a two-lollipop graph (degree-matched but
    structurally distinct neighbourhoods), a complete graph, a Petersen graph,
    and a small dense random graph — the structures most likely to surface a
    WL-hash collision if one existed for hop-1 neighbourhoods.
    """
    rnd = nx.gnp_random_graph(18, 0.35, seed=7)
    return [
        ("star4", nx.star_graph(4)),
        ("path7", nx.path_graph(7)),
        ("cycle6", nx.cycle_graph(6)),
        ("complete5", nx.complete_graph(5)),
        ("petersen", nx.petersen_graph()),
        ("balanced_tree", nx.balanced_tree(2, 3)),
        ("barbell", nx.barbell_graph(4, 2)),
        ("gnp18", rnd),
    ]


class TestWLBucketingEquivalence:
    """Pure WL bucketing reproduces the brute-force count on every node.

    This is the objective exactness criterion of issue #139: if pure WL
    matches VF2 brute force 100% on the small-graph battery (counts *and*
    booleans), the runner adopts pure WL; any divergence would force the
    hybrid (VF2-refined) safeguard.
    """

    def test_counts_match_brute_force_self_attack(self) -> None:
        """For G_orig == G_anon, bucketed counts equal brute-force counts."""
        for name, g in _battery_graphs():
            nodes = list(g.nodes())
            fast = subgraph_candidate_counts(g, g, nodes, hop=1)
            for v in nodes:
                brute = subgraph_candidate_count(g, g, v, hop=1)
                assert fast[v] == brute, f"{name}: node {v} count mismatch"

    def test_booleans_match_brute_force_self_attack(self) -> None:
        """The count==1 re-identification verdict matches the brute force."""
        for name, g in _battery_graphs():
            nodes = list(g.nodes())
            fast = subgraph_candidate_counts(g, g, nodes, hop=1)
            for v in nodes:
                assert (fast[v] == 1) is subgraph_attack(g, g, v, hop=1), (
                    f"{name}: node {v} verdict mismatch"
                )

    def test_counts_match_when_anonymisation_breaks_symmetry(self) -> None:
        """G_orig != G_anon: bucketed counts still equal the brute force.

        Mirrors test_unique_neighbourhood_after_anonymisation: node 5's star
        becomes a chain in G_anon, so only node 0 keeps a star(3) fingerprint.
        """
        g_orig = nx.Graph()
        g_orig.add_edges_from([(0, 1), (0, 2), (0, 3), (5, 6), (5, 7), (5, 8)])
        g_anon = nx.Graph()
        g_anon.add_edges_from([(0, 1), (0, 2), (0, 3), (5, 6), (6, 7), (7, 8)])

        targets = list(g_orig.nodes())
        fast = subgraph_candidate_counts(g_orig, g_anon, targets, hop=1)
        for v in targets:
            assert fast[v] == subgraph_candidate_count(g_orig, g_anon, v, hop=1)
        assert fast[0] == 1  # node 0 uniquely re-identified

    def test_hop2_matches_brute_force(self) -> None:
        """The fast path is exact at hop=2 as well (two-lollipop graph)."""
        g = nx.Graph()
        g.add_edges_from([(0, 1), (0, 2), (1, 2), (0, 3), (3, 4), (4, 5)])
        g.add_edges_from([(6, 7), (6, 8), (7, 8), (6, 9)])
        nodes = list(g.nodes())
        fast = subgraph_candidate_counts(g, g, nodes, hop=2)
        for v in nodes:
            assert fast[v] == subgraph_candidate_count(g, g, v, hop=2)


class TestWLBucketingBehaviour:
    """Bucketing correctness, refinement, determinism and validation."""

    def test_isomorphic_neighbourhoods_share_count(self) -> None:
        """cycle_graph(6): vertex-transitive → every node counts all 6."""
        g = nx.cycle_graph(6)
        counts = subgraph_candidate_counts(g, g, list(g.nodes()), hop=1)
        assert set(counts.values()) == {6}

    def test_unique_hub_counts_one(self) -> None:
        """A star centre has a unique hub neighbourhood → exactly one candidate."""
        g = nx.star_graph(6)
        counts = subgraph_candidate_counts(g, g, [0], hop=1)
        assert counts[0] == 1

    def test_refine_matches_pure_wl_on_small_graphs(self) -> None:
        """VF2 refinement returns the same exact counts as pure WL here."""
        for name, g in _battery_graphs():
            nodes = list(g.nodes())
            pure = subgraph_candidate_counts(g, g, nodes, hop=1)
            refined = subgraph_candidate_counts(g, g, nodes, hop=1, refine_max_size=8)
            assert pure == refined, f"{name}: refine diverged from pure WL"

    def test_hub_is_never_refined_with_vf2(self) -> None:
        """With refine_max_size set, a hub larger than the cap stays on pure WL.

        Refining a hub with VF2 is the automorphism blow-up the fast path
        exists to avoid (issue #139). We spy on GraphMatcher to assert it is
        never constructed for a star centre whose neighbourhood (8 nodes)
        exceeds refine_max_size=4, while still returning the correct count.
        """
        g = nx.star_graph(7)  # centre 0, neighbourhood = 8 nodes
        calls = {"n": 0}
        real_matcher = subgraph_mod.GraphMatcher

        def _spy(*args, **kwargs):  # type: ignore[no-untyped-def]
            calls["n"] += 1
            return real_matcher(*args, **kwargs)

        with patch.object(subgraph_mod, "GraphMatcher", side_effect=_spy):
            counts = subgraph_candidate_counts(g, g, [0], hop=1, refine_max_size=4)
        assert counts[0] == 1
        assert calls["n"] == 0  # hub never sent to VF2

    def test_small_neighbourhood_is_refined_with_vf2(self) -> None:
        """A neighbourhood within the cap is confirmed via VF2 (refinement on)."""
        g = nx.path_graph(5)  # interior nodes have 3-node neighbourhoods
        calls = {"n": 0}
        real_matcher = subgraph_mod.GraphMatcher

        def _spy(*args, **kwargs):  # type: ignore[no-untyped-def]
            calls["n"] += 1
            return real_matcher(*args, **kwargs)

        with patch.object(subgraph_mod, "GraphMatcher", side_effect=_spy):
            subgraph_candidate_counts(g, g, [1], hop=1, refine_max_size=8)
        assert calls["n"] > 0  # small bucket confirmed with VF2

    def test_determinism(self) -> None:
        """Repeated calls on identical inputs yield identical counts."""
        g = nx.gnp_random_graph(20, 0.3, seed=11)
        nodes = list(g.nodes())
        first = subgraph_candidate_counts(g, g, nodes, hop=1)
        second = subgraph_candidate_counts(g, g, nodes, hop=1)
        assert first == second

    def test_invalid_hop_raises(self) -> None:
        g = nx.path_graph(3)
        with pytest.raises(ValueError, match="positive integer"):
            subgraph_candidate_counts(g, g, [0], hop=0)

    def test_target_not_in_g_orig_raises(self) -> None:
        g = nx.path_graph(3)
        with pytest.raises(ValueError, match="not found in G_orig"):
            subgraph_candidate_counts(g, g, [99], hop=1)

    def test_empty_targets_returns_empty(self) -> None:
        """No targets → empty mapping (index still builds without error)."""
        g = nx.star_graph(3)
        assert subgraph_candidate_counts(g, g, [], hop=1) == {}
