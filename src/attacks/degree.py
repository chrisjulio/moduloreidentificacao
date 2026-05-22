"""Degree-based re-identification attack.

Adversary background knowledge: the degree of the target node in the
original (pre-anonymisation) graph ``G_orig``.

Attack procedure
----------------
1. Read the target's degree from ``G_orig``.
2. Enumerate every node in ``G_anon`` whose degree falls within
   ``tolerance`` of that original degree.
3. Return ``True`` iff exactly one candidate exists (unique identification).

This is the simplest structural attack and serves as a baseline: it
models an adversary who knows only a single scalar attribute (degree)
about the target.  He et al. (2009) use degree-based identification
as the primary threat model motivating structure-aware anonymisation.

Reference: He, X. et al. (2009), Section 1-2 (threat model).
"""

from __future__ import annotations

import networkx as nx


def degree_attack(
    g_orig: nx.Graph,
    g_anon: nx.Graph,
    target: int,
    tolerance: int = 0,
) -> bool:
    """Re-identify a target node using degree as background knowledge.

    Determines whether an adversary who knows the target node's degree in
    the original graph can uniquely identify that node in the anonymised
    graph by matching degrees within ``tolerance``.

    Parameters
    ----------
    g_orig:
        Original (pre-anonymisation) graph.  Used only to read the
        target's degree — the adversary's background knowledge.
    g_anon:
        Anonymised graph in which the adversary searches for the target.
    target:
        Node identifier whose re-identification is tested.  Must be
        present in ``g_orig``.
    tolerance:
        Maximum allowed absolute difference between the target's original
        degree and a candidate's degree in ``g_anon``.  Default: 0
        (exact match).  Larger values model an adversary with imprecise
        or stale degree knowledge.

    Returns
    -------
    bool
        ``True`` if exactly one node in ``g_anon`` has a degree within
        ``[original_degree - tolerance, original_degree + tolerance]``
        (inclusive); ``False`` otherwise (zero or multiple candidates →
        the attack fails to uniquely identify the target).

    Raises
    ------
    ValueError
        If ``target`` is not a node in ``g_orig``.
    ValueError
        If ``tolerance`` is negative.

    Notes
    -----
    * The attack does **not** depend on which node in ``g_anon`` actually
      *is* the target — it tests whether the degree fingerprint is
      sufficient to single out one node.
    * Node IDs in ``g_orig`` and ``g_anon`` are assumed to share the same
      namespace; anonymisation (He et al.) preserves node IDs.
    * Complexity: O(n) where n = ``g_anon.number_of_nodes()``.
    """
    if target not in g_orig:
        raise ValueError(f"Target node {target!r} not found in G_orig.")
    if tolerance < 0:
        raise ValueError(f"tolerance must be non-negative; got {tolerance}.")

    original_degree: int = g_orig.degree(target)
    lo = original_degree - tolerance
    hi = original_degree + tolerance

    candidates = [v for v in g_anon.nodes() if lo <= g_anon.degree(v) <= hi]
    return len(candidates) == 1
