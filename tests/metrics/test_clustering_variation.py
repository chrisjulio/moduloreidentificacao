"""Tests for src/metrics/clustering_variation.py (issue #21).

Definition-of-Done coverage:
    - Identical graphs → 0.0.
    - cc_orig = 0, cc_anon = 0 → 0.0.
    - cc_orig = 0, cc_anon > 0 → ValueError.
    - Known triangle structure → correct relative variation.
    - Removing triangles → positive variation.
    - Adding triangles → positive variation.
    - Return type: float.

clustering_variation() is deterministic and seed-free.
"""

from __future__ import annotations

import networkx as nx
import pytest

from src.metrics.clustering_variation import clustering_variation

# ---------------------------------------------------------------------------
# Identical graphs → 0.0
# ---------------------------------------------------------------------------


class TestClusteringVariationIdentical:
    """Same graph on both sides → no variation."""

    def test_triangle_graph_identical(self) -> None:
        """Complete graph K_3 (one triangle): cc = 1.0 on both sides → 0.0."""
        g = nx.complete_graph(3)
        assert clustering_variation(g, g.copy()) == pytest.approx(0.0)

    def test_path_graph_identical(self) -> None:
        """path_graph(5): no triangles, cc = 0.0 on both sides → 0.0.

        Both cc_orig and cc_anon are 0 → special-case returns 0.0.
        """
        g = nx.path_graph(5)
        assert clustering_variation(g, g.copy()) == pytest.approx(0.0)

    def test_complete_graph_k4_identical(self) -> None:
        """Complete graph K_4: cc = 1.0 on both sides → 0.0."""
        g = nx.complete_graph(4)
        assert clustering_variation(g, g.copy()) == pytest.approx(0.0)

    def test_star_graph_identical(self) -> None:
        """Star graph: leaves have no neighbours connected to each other.

        Average clustering is 0 on both sides → returns 0.0.
        """
        g = nx.star_graph(4)
        assert clustering_variation(g, g.copy()) == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# Zero clustering in original
# ---------------------------------------------------------------------------


class TestClusteringVariationZeroOrig:
    """cc_orig = 0 edge cases."""

    def test_zero_orig_zero_anon_returns_zero(self) -> None:
        """Both graphs have no triangles → 0.0 (defined by convention)."""
        g_orig = nx.path_graph(4)  # cc = 0
        g_anon = nx.path_graph(4)  # cc = 0
        assert clustering_variation(g_orig, g_anon) == pytest.approx(0.0)

    def test_zero_orig_nonzero_anon_raises(self) -> None:
        """cc_orig=0 but cc_anon>0 → undefined relative variation → ValueError."""
        g_orig = nx.path_graph(4)  # no triangles, cc = 0
        g_anon = nx.complete_graph(4)  # all triangles, cc = 1
        with pytest.raises(ValueError, match=r"cc_orig is 0\.0"):
            clustering_variation(g_orig, g_anon)


# ---------------------------------------------------------------------------
# Known values — correct relative variation
# ---------------------------------------------------------------------------


class TestClusteringVariationKnownValues:
    """Hand-computed reference cases."""

    def test_complete_k4_remove_all_triangles(self) -> None:
        """K_4 (cc=1.0) → path_graph(4) (cc=0.0): variation = 1.0.

        |0.0 - 1.0| / 1.0 = 1.0.
        """
        g_orig = nx.complete_graph(4)
        g_anon = nx.path_graph(4)
        result = clustering_variation(g_orig, g_anon)
        assert result == pytest.approx(1.0)

    def test_half_reduction_in_clustering(self) -> None:
        """g_orig cc = 1.0; g_anon cc = 0.5 → variation = 0.5.

        g_orig: two triangles sharing no nodes → average_clustering = 1.0.
        g_anon: remove one edge from each triangle → path-like; cc ≈ 0.

        We use a controlled graph where we know both clustering values exactly:
        g_orig = K_3 (cc=1.0 exactly for all 3 nodes).
        g_anon: keep K_3 but add an isolated node (cc = (1+1+1+0)/4 = 0.75).

        variation = |0.75 - 1.0| / 1.0 = 0.25.
        """
        g_orig = nx.complete_graph(3)  # cc = 1.0
        g_anon = nx.complete_graph(3)
        g_anon.add_node(3)  # isolated: cc = 0 for node 3
        # average_clustering: 3 nodes with cc=1, 1 node with cc=0 → mean = 0.75
        cc_anon = nx.average_clustering(g_anon)
        expected = abs(cc_anon - 1.0) / 1.0
        result = clustering_variation(g_orig, g_anon)
        assert result == pytest.approx(expected)

    def test_increase_in_clustering(self) -> None:
        """Anonymisation that *increases* clustering: variation is still positive.

        g_orig: path_graph(4) with one extra edge making cc small but > 0.
        g_anon: complete_graph on same 4 nodes → cc = 1.0 > cc_orig.

        Use g_orig = cycle_graph(4) (cc=0) which would raise; instead use
        a graph with two triangles as orig and a triangle plus isolated as anon.
        """
        # g_orig: K_4 with one edge removed (node 0-3 missing)
        # cc_orig > 0 and < 1 so both paths are valid.
        g_orig = nx.complete_graph(4)
        g_orig.remove_edge(0, 3)
        cc_orig = nx.average_clustering(g_orig)
        assert cc_orig > 0.0

        g_anon = nx.complete_graph(4)  # cc_anon = 1.0 > cc_orig
        cc_anon = nx.average_clustering(g_anon)

        expected = abs(cc_anon - cc_orig) / cc_orig
        result = clustering_variation(g_orig, g_anon)
        assert result == pytest.approx(expected)


# ---------------------------------------------------------------------------
# Return type
# ---------------------------------------------------------------------------


class TestClusteringVariationReturnType:
    """Return value must be a float."""

    def test_returns_float(self) -> None:
        g = nx.complete_graph(3)
        result = clustering_variation(g, g.copy())
        assert isinstance(result, float)

    def test_returns_non_negative(self) -> None:
        """Relative variation is absolute difference → always >= 0."""
        g_orig = nx.complete_graph(4)
        g_anon = nx.path_graph(4)
        result = clustering_variation(g_orig, g_anon)
        assert result >= 0.0
