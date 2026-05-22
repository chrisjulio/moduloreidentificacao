"""Tests for src/metrics/ks_test_degree.py (issue #21).

Definition-of-Done coverage:
    - Identical graphs → D ≈ 0.0, large p-value.
    - Completely different degree distributions → D > 0, small p-value.
    - Empty graph → ValueError (both positions).
    - Return types: (float, float).
    - p_value always in [0.0, 1.0].
    - D always in [0.0, 1.0].

ks_test_degree() is deterministic and seed-free.
"""

from __future__ import annotations

import networkx as nx
import pytest

from src.metrics.ks_test_degree import ks_test_degree

# ---------------------------------------------------------------------------
# Invalid inputs
# ---------------------------------------------------------------------------


class TestKsTestDegreeInvalidInputs:
    """ValueError on empty graphs."""

    def test_empty_g_orig_raises(self) -> None:
        """g_orig with no nodes → ValueError."""
        g_empty = nx.Graph()
        g_anon = nx.path_graph(3)
        with pytest.raises(ValueError, match="g_orig has no nodes"):
            ks_test_degree(g_empty, g_anon)

    def test_empty_g_anon_raises(self) -> None:
        """g_anon with no nodes → ValueError."""
        g_orig = nx.path_graph(3)
        g_empty = nx.Graph()
        with pytest.raises(ValueError, match="g_anon has no nodes"):
            ks_test_degree(g_orig, g_empty)


# ---------------------------------------------------------------------------
# Identical graphs — D should be 0.0
# ---------------------------------------------------------------------------


class TestKsTestDegreeIdentical:
    """Same graph passed as both arguments → D = 0.0."""

    def test_path_graph_identical(self) -> None:
        """path_graph(5) vs itself → D = 0.0, p-value = 1.0."""
        g = nx.path_graph(5)
        d_stat, p_val = ks_test_degree(g, g.copy())
        assert d_stat == pytest.approx(0.0)
        assert p_val == pytest.approx(1.0)

    def test_star_graph_identical(self) -> None:
        """star_graph(4) vs itself → D = 0.0."""
        g = nx.star_graph(4)
        d_stat, _ = ks_test_degree(g, g.copy())
        assert d_stat == pytest.approx(0.0)

    def test_cycle_graph_identical(self) -> None:
        """cycle_graph(6) vs itself → D = 0.0.

        All nodes have degree 2 in a cycle → both distributions identical.
        """
        g = nx.cycle_graph(6)
        d_stat, _ = ks_test_degree(g, g.copy())
        assert d_stat == pytest.approx(0.0)

    def test_single_node_graph(self) -> None:
        """Single isolated node: degree distribution is [0] vs [0] → D = 0."""
        g = nx.Graph()
        g.add_node(0)
        d_stat, _ = ks_test_degree(g, g.copy())
        assert d_stat == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# Different degree distributions — D should be > 0
# ---------------------------------------------------------------------------


class TestKsTestDegreeDifferent:
    """Graphs with clearly different degree distributions → D > 0."""

    def test_star_vs_cycle_distinct(self) -> None:
        """Star(4) has degrees [4,1,1,1,1]; cycle(5) has all degrees 2.

        The two distributions are clearly different → D > 0.
        """
        g_orig = nx.star_graph(4)  # degrees: [4, 1, 1, 1, 1]
        g_anon = nx.cycle_graph(5)  # degrees: [2, 2, 2, 2, 2]
        d_stat, _ = ks_test_degree(g_orig, g_anon)
        assert d_stat > 0.0

    def test_complete_vs_empty_large_d(self) -> None:
        """Complete graph K_4 vs 4 isolated nodes.

        K_4: every degree = 3; isolated: every degree = 0 → D = 1.0.
        """
        g_orig = nx.complete_graph(4)  # degrees all 3
        g_anon = nx.Graph()
        g_anon.add_nodes_from(range(4))  # degrees all 0
        d_stat, _ = ks_test_degree(g_orig, g_anon)
        assert d_stat == pytest.approx(1.0)

    def test_path_vs_complete_differs(self) -> None:
        """path_graph(4) vs complete_graph(4) have different degree sequences."""
        g_orig = nx.path_graph(4)  # degrees: [1, 2, 2, 1]
        g_anon = nx.complete_graph(4)  # degrees: [3, 3, 3, 3]
        d_stat, _ = ks_test_degree(g_orig, g_anon)
        assert d_stat > 0.0


# ---------------------------------------------------------------------------
# Slight perturbation — D should be small but nonzero
# ---------------------------------------------------------------------------


class TestKsTestDegreeSlightPerturbation:
    """Small edge change → small but nonzero D."""

    def test_one_edge_added(self) -> None:
        """path_graph(4) vs the same graph + one extra edge.

        Adding edge (0, 3) increases degrees of 0 and 3 from 1 to 2.
        D should be positive but small.
        """
        g_orig = nx.path_graph(4)  # degrees: [1, 2, 2, 1]
        g_anon = g_orig.copy()
        g_anon.add_edge(0, 3)  # degrees now: [2, 2, 2, 2]
        d_stat, _ = ks_test_degree(g_orig, g_anon)
        assert 0.0 < d_stat <= 1.0


# ---------------------------------------------------------------------------
# Return types and value ranges
# ---------------------------------------------------------------------------


class TestKsTestDegreeReturnTypes:
    """D and p-value must always be floats in [0.0, 1.0]."""

    def test_both_values_are_float(self) -> None:
        g = nx.path_graph(4)
        d_stat, p_val = ks_test_degree(g, g.copy())
        assert isinstance(d_stat, float)
        assert isinstance(p_val, float)

    def test_d_stat_in_unit_interval(self) -> None:
        """D statistic ∈ [0.0, 1.0] for various graph pairs."""
        pairs = [
            (nx.path_graph(5), nx.cycle_graph(5)),
            (nx.star_graph(4), nx.complete_graph(5)),
            (nx.path_graph(3), nx.path_graph(3)),
        ]
        for g_orig, g_anon in pairs:
            d_stat, _ = ks_test_degree(g_orig, g_anon)
            assert 0.0 <= d_stat <= 1.0

    def test_p_value_in_unit_interval(self) -> None:
        """p-value ∈ [0.0, 1.0] for various graph pairs."""
        pairs = [
            (nx.path_graph(5), nx.cycle_graph(5)),
            (nx.star_graph(4), nx.complete_graph(5)),
            (nx.path_graph(3), nx.path_graph(3)),
        ]
        for g_orig, g_anon in pairs:
            _, p_val = ks_test_degree(g_orig, g_anon)
            assert 0.0 <= p_val <= 1.0
