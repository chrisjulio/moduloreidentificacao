"""Tests for src/attacks/degree.py (issue #19).

Definition-of-Done coverage:
    - Typical case: target uniquely identifiable → True.
    - Isolated node: multiple degree-0 nodes → not unique → False.
    - Tolerance != 0: wider window creates ambiguity → False; or allows
      a small degree shift while keeping unique identification → True.
    - Target not in G_orig: raises ValueError.
    - Negative tolerance: raises ValueError.

No random seeds needed: degree_attack() is deterministic and seed-free.
"""

from __future__ import annotations

import networkx as nx
import pytest

from src.attacks.degree import degree_attack

# ---------------------------------------------------------------------------
# Typical case — unique identification (True)
# ---------------------------------------------------------------------------


class TestDegreeAttackSuccess:
    """Attack returns True when exactly one candidate matches."""

    def test_star_center_uniquely_identified(self) -> None:
        """Star graph: centre has unique degree n-1 → unambiguously identified.

        nx.star_graph(4): centre=0 (degree 4), leaves 1-4 (degree 1 each).
        G_anon is identical so the degree fingerprint is preserved.
        """
        g_orig = nx.star_graph(4)
        g_anon = g_orig.copy()
        assert degree_attack(g_orig, g_anon, target=0) is True

    def test_unique_degree_node_identified(self) -> None:
        """Target's original degree uniquely matches exactly one node in g_anon.

        g_orig: path 0-1-2-3-4; target=2 has degree 2.
        g_anon: only node 2 retains degree 2 (nodes 1 and 3 reduced to 1).
        The adversary uses original degree 2 to search g_anon → one match.
        """
        g_orig = nx.path_graph(5)  # target=2 has degree 2
        # Build g_anon manually: edges (1,2) and (2,3) only.
        # Degrees: 0→0, 1→1, 2→2, 3→1, 4→0 — node 2 is the sole degree-2 node.
        g_anon = nx.Graph()
        g_anon.add_nodes_from(range(5))
        g_anon.add_edges_from([(1, 2), (2, 3)])
        assert degree_attack(g_orig, g_anon, target=2) is True


# ---------------------------------------------------------------------------
# Attack fails — target not uniquely identifiable (False)
# ---------------------------------------------------------------------------


class TestDegreeAttackFailure:
    """Attack returns False when zero or multiple candidates match."""

    def test_isolated_nodes_not_unique(self) -> None:
        """Multiple isolated nodes → all have degree 0 → 3 candidates → False.

        Represents a heavily anonymised graph where many nodes lose all edges.
        """
        g_orig = nx.Graph()
        g_orig.add_nodes_from([0, 1, 2])  # three isolated nodes, degree 0
        g_anon = g_orig.copy()
        assert degree_attack(g_orig, g_anon, target=0) is False

    def test_shared_degree_not_unique(self) -> None:
        """All nodes share the same degree (k-regular) → attack always fails."""
        g_orig = nx.cycle_graph(4)  # every node has degree 2
        g_anon = g_orig.copy()
        assert degree_attack(g_orig, g_anon, target=0) is False

    def test_no_matching_degree_in_g_anon(self) -> None:
        """Target's degree in G_orig exists nowhere in G_anon → zero
        candidates → False.

        Models an anonymisation that completely removes a node's edges.
        """
        g_orig = nx.path_graph(3)  # degrees: 1, 2, 1; target=1 (degree 2)
        g_anon = nx.Graph()
        g_anon.add_nodes_from([0, 1, 2])  # all isolated → max degree is 0
        assert degree_attack(g_orig, g_anon, target=1) is False


# ---------------------------------------------------------------------------
# Tolerance parameter
# ---------------------------------------------------------------------------


class TestDegreeAttackTolerance:
    """tolerance widens the candidate window; higher values trade precision
    for recall in the adversary's search."""

    def test_tolerance_zero_exact_match(self) -> None:
        """tolerance=0 (default): only exact degree matches count.

        path_graph(3): 0-1-2, degrees [1, 2, 1].
        Node 1 has degree 2 in G_orig; only node 1 in G_anon has degree 2.
        """
        g_orig = nx.path_graph(3)
        g_anon = g_orig.copy()
        assert degree_attack(g_orig, g_anon, target=1, tolerance=0) is True

    def test_tolerance_widens_to_ambiguous(self) -> None:
        """tolerance=1 expands the window to [1, 3] for target degree 2.

        Nodes 0 and 2 have degree 1, which falls inside [1, 3] → 3 candidates
        → attack fails.
        """
        g_orig = nx.path_graph(3)  # degrees: 1, 2, 1
        g_anon = g_orig.copy()
        assert degree_attack(g_orig, g_anon, target=1, tolerance=1) is False

    def test_tolerance_allows_degree_shift_and_stays_unique(self) -> None:
        """tolerance=1 still identifies target when its degree shifted by 1.

        G_orig: star(4), centre (0) degree=4.
        G_anon: remove one leaf edge → centre degree=3, leaves degree∈{0,1}.
        With tolerance=1 the window is [3, 5]; only node 0 qualifies.
        """
        g_orig = nx.star_graph(4)  # centre=0, degree 4
        g_anon = nx.star_graph(4)
        g_anon.remove_edge(0, 4)  # centre now has degree 3
        # In g_anon: node 0 → degree 3; nodes 1-3 → degree 1; node 4 → degree 0
        assert degree_attack(g_orig, g_anon, target=0, tolerance=1) is True


# ---------------------------------------------------------------------------
# Invalid inputs
# ---------------------------------------------------------------------------


class TestDegreeAttackInvalidInputs:
    """degree_attack() raises ValueError on invalid arguments."""

    def test_target_not_in_g_orig_raises(self) -> None:
        """A target absent from G_orig is an invalid query → ValueError."""
        g_orig = nx.path_graph(3)
        g_anon = g_orig.copy()
        with pytest.raises(ValueError, match="not found in G_orig"):
            degree_attack(g_orig, g_anon, target=99)

    def test_negative_tolerance_raises(self) -> None:
        """Negative tolerance is logically undefined → ValueError."""
        g_orig = nx.path_graph(3)
        g_anon = g_orig.copy()
        with pytest.raises(ValueError, match="non-negative"):
            degree_attack(g_orig, g_anon, target=0, tolerance=-1)
