"""Relative variation of mean clustering coefficient (utility metric).

Measures how much the anonymisation perturbs the global clustering structure
of the graph.  Lower is better (higher utility on this metric).

Utility interpretation
----------------------
* 0.0 → no change in clustering; anonymisation preserved triangle structure
  perfectly.
* > 0.0 → anonymisation added or removed edges that affected triangle counts;
  the larger the value the more the clustering structure was disrupted.

Reference: docs/metrics_definitions.md (variação relativa do clustering).
NetworkX: ``nx.average_clustering``.
"""

from __future__ import annotations

import networkx as nx


def clustering_variation(
    g_orig: nx.Graph,
    g_anon: nx.Graph,
) -> float:
    """Compute the relative variation in mean clustering coefficient.

    The mean clustering coefficient is computed via ``nx.average_clustering``
    (average of per-node local clustering coefficients across all nodes in
    the graph).

    Parameters
    ----------
    g_orig:
        Original (pre-anonymisation) graph.
    g_anon:
        Anonymised graph (same node set; edges may differ).

    Returns
    -------
    float
        Relative change: ``|cc_anon - cc_orig| / cc_orig``.

        * 0.0 → no change in clustering.
        * Values > 1.0 are possible when anonymisation drastically increases
          clustering beyond twice the original value.
        * Returns 0.0 when both ``cc_orig == 0`` and ``cc_anon == 0``
          (no triangles in either graph; variation is trivially zero).

    Raises
    ------
    ValueError
        If ``cc_orig == 0`` but ``cc_anon > 0``.  The original graph has no
        triangle structure while the anonymised graph introduced some; the
        relative variation is infinite (undefined).

    Notes
    -----
    * ``nx.average_clustering`` returns 0.0 for isolated nodes and for graphs
      with no edges (all local clustering coefficients are 0 by convention).
    * The denominator is always ``cc_orig`` (the original graph as reference),
      so the metric is not symmetric.  If the inverse ratio is needed (using
      ``cc_anon`` as reference), call the function with swapped arguments.
    * Complexity: O(n · Δ²) where Δ is the maximum degree, matching
      ``nx.average_clustering``.
    """
    cc_orig: float = nx.average_clustering(g_orig)
    cc_anon: float = nx.average_clustering(g_anon)

    if cc_orig == 0.0:
        if cc_anon == 0.0:
            return 0.0
        raise ValueError(
            f"cc_orig is 0.0 but cc_anon={cc_anon:.6f}; relative variation "
            "is undefined (infinite). The original graph has no triangle "
            "structure and the anonymised graph introduced some."
        )

    return abs(cc_anon - cc_orig) / cc_orig
