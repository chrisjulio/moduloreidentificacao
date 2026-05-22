"""Tests for src/metrics/equivalence_group_size.py (issue #21).

Definition-of-Done coverage:
    - Empty groups list → ValueError.
    - Single group, single LS → (size, size).
    - Uniform groups (k LSs of size d each) → mean == median == k*d.
    - Last group incomplete → mean pulled below k*d.
    - Groups with different sizes → correct mean and median.
    - Median rounds to nearest int.

equivalence_group_size() is deterministic and seed-free.
"""

from __future__ import annotations

import networkx as nx
import pytest

from src.metrics.equivalence_group_size import equivalence_group_size

# ---------------------------------------------------------------------------
# Helper to build a trivial LS (path graph on n nodes)
# ---------------------------------------------------------------------------


def _ls(n: int, offset: int = 0) -> nx.Graph:
    """Return a path graph on n nodes starting from node ``offset``."""
    g = nx.path_graph(n)
    return nx.relabel_nodes(g, {i: i + offset for i in range(n)})


# ---------------------------------------------------------------------------
# Invalid inputs
# ---------------------------------------------------------------------------


class TestEquivalenceGroupSizeInvalidInputs:
    """ValueError on empty group list."""

    def test_empty_groups_raises(self) -> None:
        """No groups → metric is undefined → ValueError."""
        with pytest.raises(ValueError, match="non-empty"):
            equivalence_group_size([])


# ---------------------------------------------------------------------------
# Single group
# ---------------------------------------------------------------------------


class TestEquivalenceGroupSizeSingleGroup:
    """Single group — mean and median are equal to that group's node count."""

    def test_single_group_single_ls(self) -> None:
        """One group containing one LS of 3 nodes → (3.0, 3)."""
        ls = _ls(3)
        groups = [[ls]]
        mean, median = equivalence_group_size(groups)
        assert mean == pytest.approx(3.0)
        assert median == 3

    def test_single_group_two_ls(self) -> None:
        """One group containing two LSs of 3 nodes each → total 6 nodes.

        k=2, d=3: group size = k*d = 6.
        """
        groups = [[_ls(3, offset=0), _ls(3, offset=3)]]
        mean, median = equivalence_group_size(groups)
        assert mean == pytest.approx(6.0)
        assert median == 6

    def test_single_group_five_ls(self) -> None:
        """One group containing 5 LSs of size 4 each → 20 nodes total.

        k=5, d=4: group size = 20.
        """
        groups = [[_ls(4, offset=i * 4) for i in range(5)]]
        mean, median = equivalence_group_size(groups)
        assert mean == pytest.approx(20.0)
        assert median == 20


# ---------------------------------------------------------------------------
# Uniform groups — mean == median == k*d
# ---------------------------------------------------------------------------


class TestEquivalenceGroupSizeUniform:
    """All groups have the same size; mean equals median."""

    def test_two_complete_groups(self) -> None:
        """Two groups, each with k=2 LSs of d=3 nodes → size 6 per group.

        Mean = median = 6.
        """
        g1 = [_ls(3, offset=0), _ls(3, offset=3)]
        g2 = [_ls(3, offset=6), _ls(3, offset=9)]
        mean, median = equivalence_group_size([g1, g2])
        assert mean == pytest.approx(6.0)
        assert median == 6

    def test_three_complete_groups_k3_d2(self) -> None:
        """Three groups, k=3 LSs of d=2 nodes each → 6 nodes per group.

        Mean = median = 6.
        """
        groups = [[_ls(2, offset=i * 6 + j * 2) for j in range(3)] for i in range(3)]
        mean, median = equivalence_group_size(groups)
        assert mean == pytest.approx(6.0)
        assert median == 6


# ---------------------------------------------------------------------------
# Non-uniform groups — last group incomplete (D-06 case)
# ---------------------------------------------------------------------------


class TestEquivalenceGroupSizeNonUniform:
    """Last group has fewer LSs; mean is pulled below k*d."""

    def test_two_complete_one_incomplete(self) -> None:
        """Two groups of 6 nodes + one incomplete group of 3 nodes.

        Sizes = [6, 6, 3]; mean = 5.0, median = 6.
        """
        g1 = [_ls(3, offset=0), _ls(3, offset=3)]
        g2 = [_ls(3, offset=6), _ls(3, offset=9)]
        g3_incomplete = [_ls(3, offset=12)]  # only 1 LS instead of 2
        mean, median = equivalence_group_size([g1, g2, g3_incomplete])
        assert mean == pytest.approx(5.0)
        assert median == 6

    def test_sizes_differ_by_half(self) -> None:
        """Two groups: sizes 4 and 2 → mean = 3.0, median = 3.

        Sizes = [4, 2]; mean = 3.0, median = int(round(3.0)) = 3.
        """
        g_large = [_ls(2, offset=0), _ls(2, offset=2)]  # 4 nodes
        g_small = [_ls(2, offset=4)]  # 2 nodes
        mean, median = equivalence_group_size([g_large, g_small])
        assert mean == pytest.approx(3.0)
        assert median == 3

    def test_four_groups_mixed_sizes(self) -> None:
        """Four groups with sizes [8, 8, 8, 4] → mean=7.0, median=8.

        Simulates three complete groups (k=4, d=2) + one half-complete.
        """
        complete = [[_ls(2, offset=i * 8 + j * 2) for j in range(4)] for i in range(3)]
        incomplete = [[_ls(2, offset=24), _ls(2, offset=26)]]  # 2 LSs instead of 4
        groups = complete + incomplete
        sizes = [sum(ls.number_of_nodes() for ls in g) for g in groups]
        assert sizes == [8, 8, 8, 4]
        mean, median = equivalence_group_size(groups)
        assert mean == pytest.approx(7.0)
        assert median == 8


# ---------------------------------------------------------------------------
# Return types
# ---------------------------------------------------------------------------


class TestEquivalenceGroupSizeReturnTypes:
    """Return types: (float, int)."""

    def test_mean_is_float(self) -> None:
        groups = [[_ls(3)]]
        mean, _ = equivalence_group_size(groups)
        assert isinstance(mean, float)

    def test_median_is_int(self) -> None:
        groups = [[_ls(3)]]
        _, median = equivalence_group_size(groups)
        assert isinstance(median, int)

    def test_median_rounds_correctly(self) -> None:
        """Even-count groups: median is average of two middle values → rounds.

        Sizes = [2, 4]; median of [2, 4] = 3.0 → int(round(3.0)) = 3.
        """
        g_small = [_ls(2, offset=0)]
        g_large = [_ls(2, offset=2), _ls(2, offset=4)]
        mean, median = equivalence_group_size([g_small, g_large])
        assert mean == pytest.approx(3.0)
        assert median == 3
        assert isinstance(median, int)
