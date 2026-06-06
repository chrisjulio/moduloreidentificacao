"""Tests for src/metrics/entropy.py (issue #30 / D-17).

Definition-of-Done coverage:
    - Empty groups list / no nodes / negative tau → ValueError.
    - Uniform groups: H = log2(n_r); node-weighted entropy_mean.
    - degree_of_anonymity = H/H_max ∈ [0, 1]; equals 1.0 when all groups
      share the same size > 1; 0.0 when every group is a singleton.
    - reidentification_rate_entropy with tau=0 = fraction of nodes in
      singleton groups (n_r == 1); raising tau widens the count.
    - Empty groups (n_r == 0) carry zero weight and are skipped.
    - Reuses the same `groups` format as equivalence_group_size.

entropy_metrics() is deterministic and seed-free.
"""

from __future__ import annotations

import math

import networkx as nx
import pytest

from src.metrics.entropy import entropy_metrics


def _ls(n: int, offset: int = 0) -> nx.Graph:
    """Return a path graph on n nodes starting from node ``offset``."""
    g = nx.path_graph(n)
    return nx.relabel_nodes(g, {i: i + offset for i in range(n)})


def _group_of(n_ls: int, ls_size: int, start: int = 0) -> list[nx.Graph]:
    """Build a group of ``n_ls`` LSs of ``ls_size`` nodes (total n_r nodes)."""
    return [_ls(ls_size, offset=start + i * ls_size) for i in range(n_ls)]


# ---------------------------------------------------------------------------
# Invalid inputs
# ---------------------------------------------------------------------------


class TestEntropyInvalidInputs:
    def test_empty_groups_raises(self) -> None:
        with pytest.raises(ValueError, match="non-empty"):
            entropy_metrics([])

    def test_groups_with_no_nodes_raises(self) -> None:
        """All groups empty → no nodes → metric undefined."""
        with pytest.raises(ValueError, match="no nodes"):
            entropy_metrics([[nx.Graph()], [nx.Graph()]])

    def test_negative_tau_raises(self) -> None:
        with pytest.raises(ValueError, match="non-negative"):
            entropy_metrics([[_ls(2)]], tau=-0.5)


# ---------------------------------------------------------------------------
# Uniform model — H = log2(n_r)
# ---------------------------------------------------------------------------


class TestEntropyUniform:
    def test_single_group_size_one_is_zero_entropy(self) -> None:
        """A singleton group: H = log2(1) = 0 → no anonymity."""
        out = entropy_metrics([[_ls(1)]])
        assert out["entropy_mean"] == pytest.approx(0.0)
        assert out["degree_of_anonymity"] == pytest.approx(0.0)
        # H(v)=0 <= tau=0 → the node is "re-identified".
        assert out["reidentification_rate_entropy"] == pytest.approx(1.0)

    def test_single_group_size_four(self) -> None:
        """One group of 4 nodes (k=2 LSs of 2) → H = log2(4) = 2 bits."""
        out = entropy_metrics([_group_of(2, 2)])
        assert out["entropy_mean"] == pytest.approx(2.0)
        # Single group → H_max == H → degree_of_anonymity == 1.0.
        assert out["degree_of_anonymity"] == pytest.approx(1.0)
        assert out["reidentification_rate_entropy"] == pytest.approx(0.0)

    def test_entropy_mean_is_node_weighted(self) -> None:
        """Two groups, sizes 2 and 4 → node-weighted mean of log2(n_r).

        H_2 = 1, H_4 = 2; weighted mean = (2*1 + 4*2) / 6 = 10/6.
        """
        groups = [_group_of(2, 1, start=0), _group_of(2, 2, start=2)]
        sizes = [sum(ls.number_of_nodes() for ls in g) for g in groups]
        assert sizes == [2, 4]
        out = entropy_metrics(groups)
        assert out["entropy_mean"] == pytest.approx(10.0 / 6.0)

    def test_degree_of_anonymity_uniform_sizes_is_one(self) -> None:
        """Equal-size groups (all > 1) → every H equals H_max → d = 1.0."""
        groups = [_group_of(2, 2, start=0), _group_of(2, 2, start=4)]
        out = entropy_metrics(groups)
        assert out["degree_of_anonymity"] == pytest.approx(1.0)

    def test_degree_of_anonymity_normalised_range(self) -> None:
        """Sizes 2 and 8 → H_max = log2(8) = 3; d node-weighted in (0,1)."""
        groups = [_group_of(2, 1, start=0), _group_of(2, 4, start=2)]
        sizes = [sum(ls.number_of_nodes() for ls in g) for g in groups]
        assert sizes == [2, 8]
        out = entropy_metrics(groups)
        h_max = math.log2(8)
        expected = (2 * (math.log2(2) / h_max) + 8 * (math.log2(8) / h_max)) / 10
        assert out["degree_of_anonymity"] == pytest.approx(expected)
        assert 0.0 < out["degree_of_anonymity"] < 1.0


# ---------------------------------------------------------------------------
# reidentification_rate_entropy and the tau threshold
# ---------------------------------------------------------------------------


class TestEntropyReidentificationRate:
    def test_tau_zero_counts_singleton_groups(self) -> None:
        """tau=0: only n_r == 1 groups count (H = 0 <= 0).

        Sizes [1, 1, 4] → 2 of 6 nodes re-identified = 1/3.
        """
        groups = [[_ls(1, 0)], [_ls(1, 1)], _group_of(2, 2, start=2)]
        out = entropy_metrics(groups, tau=0.0)
        assert out["reidentification_rate_entropy"] == pytest.approx(2.0 / 6.0)

    def test_higher_tau_widens_count(self) -> None:
        """tau=1 bit also captures n_r == 2 groups (H = 1 <= 1).

        Sizes [1, 2, 4]: tau=0 → only the singleton (1/7);
        tau=1 → singleton + size-2 group (3/7).
        """
        groups = [[_ls(1, 0)], _group_of(2, 1, start=1), _group_of(2, 2, start=3)]
        sizes = [sum(ls.number_of_nodes() for ls in g) for g in groups]
        assert sizes == [1, 2, 4]
        out0 = entropy_metrics(groups, tau=0.0)
        out1 = entropy_metrics(groups, tau=1.0)
        assert out0["reidentification_rate_entropy"] == pytest.approx(1.0 / 7.0)
        assert out1["reidentification_rate_entropy"] == pytest.approx(3.0 / 7.0)

    def test_tau_recorded_in_output(self) -> None:
        out = entropy_metrics([[_ls(2)]], tau=1.5)
        assert out["tau"] == pytest.approx(1.5)


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEntropyEdgeCases:
    def test_empty_groups_skipped(self) -> None:
        """An empty group (n_r == 0) carries zero weight and is ignored.

        [empty, size-4] must match [size-4] alone.
        """
        with_empty = entropy_metrics([[nx.Graph()], _group_of(2, 2, start=0)])
        without = entropy_metrics([_group_of(2, 2, start=0)])
        assert with_empty["entropy_mean"] == pytest.approx(without["entropy_mean"])
        assert with_empty["degree_of_anonymity"] == pytest.approx(without["degree_of_anonymity"])
        assert with_empty["reidentification_rate_entropy"] == pytest.approx(
            without["reidentification_rate_entropy"]
        )

    def test_all_singletons_degree_of_anonymity_zero(self) -> None:
        """Every group a singleton → H_max = 0 → d defined as 0.0 (no /0)."""
        out = entropy_metrics([[_ls(1, 0)], [_ls(1, 1)], [_ls(1, 2)]])
        assert out["degree_of_anonymity"] == pytest.approx(0.0)
        assert out["entropy_mean"] == pytest.approx(0.0)
        assert out["reidentification_rate_entropy"] == pytest.approx(1.0)

    def test_return_types(self) -> None:
        out = entropy_metrics([_group_of(2, 2)])
        assert set(out) == {
            "entropy_mean",
            "degree_of_anonymity",
            "reidentification_rate_entropy",
            "tau",
        }
        assert all(isinstance(v, float) for v in out.values())

    def test_multi_ls_group_counts_all_nodes(self) -> None:
        """n_r sums nodes across all LSs in the group (D-E1(a)).

        One group of 3 LSs of size 2 → n_r = 6 → H = log2(6).
        """
        out = entropy_metrics([_group_of(3, 2)])
        assert out["entropy_mean"] == pytest.approx(math.log2(6))
