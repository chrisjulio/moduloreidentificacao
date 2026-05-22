"""Equivalence-group-size metric (privacy).

Measures the mean and median number of nodes per equivalence group in the
anonymised graph as produced by He et al. (2009).

Background
----------
In structure-aware k-anonymity each equivalence group G_r consists of k
Local Structures (LSs) that are mutually isomorphic.  Every node belongs to
exactly one LS and therefore to exactly one equivalence group.  The "size"
of a group is the total number of nodes it contains across all its LSs.

Adversarial interpretation: an adversary who knows the target's local
structure can narrow the candidates to one group.  A group with N nodes
forces the adversary to guess among N candidates → larger groups provide
better privacy.  For complete groups with exactly k LSs of size d this
equals k·d.

Reference: He et al. (2009), Section 2.3 (Definition 3); docs/metrics_definitions.md.
"""

from __future__ import annotations

import statistics

import networkx as nx


def equivalence_group_size(
    groups: list[list[nx.Graph]],
) -> tuple[float, int]:
    """Compute the mean and median node count across equivalence groups.

    Parameters
    ----------
    groups:
        Partition of Local Structures (LSs) into equivalence groups, in
        the same format as ``validate_k_anonymity``:
        ``groups[r][j]`` is the j-th LS (induced subgraph of G') in group
        r, carrying the original node IDs from the anonymised graph.

    Returns
    -------
    tuple[float, int]
        ``(mean_size, median_size)`` where each value is the total number
        of nodes across all LSs in a group.  ``median_size`` is rounded to
        the nearest integer.

    Raises
    ------
    ValueError
        If ``groups`` is empty (no groups → metric is undefined).

    Notes
    -----
    * For a fully complete anonymisation with k LSs of size d per group,
      every group has exactly k·d nodes → mean == median == k·d.
    * If the last group is incomplete (fewer than k LSs, as per decision
      D-06 in docs/algorithm_notes.md §7), its node count is less than
      k·d; this pulls the mean below k·d and may shift the median.
    * The group structure comes from the anonymiser's internal
      ``_group_isomorphic`` + ``_modify_structure`` pipeline, not from
      ``G_anon`` alone.  Pass the same ``groups`` argument used in
      ``validate_k_anonymity``.
    """
    if not groups:
        raise ValueError("groups must be non-empty; got an empty list.")

    sizes: list[int] = [sum(ls.number_of_nodes() for ls in group) for group in groups]
    mean_size: float = float(statistics.mean(sizes))
    median_size: int = round(statistics.median(sizes))
    return (mean_size, median_size)
