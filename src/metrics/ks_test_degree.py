"""KS-test on degree distributions (utility metric).

Computes the two-sample Kolmogorov-Smirnov (KS) test comparing the degree
distributions of the original and anonymised graphs.

Utility interpretation
----------------------
* D ≈ 0 + large p-value → anonymisation preserved degree structure well
  (high utility).
* D ≈ 1 + small p-value → degree distributions are significantly different
  (low utility; anonymisation strongly perturbed the degree sequence).

Reference: docs/metrics_definitions.md (KS-test, estatística D).
scipy.stats.ks_2samp (Kolmogorov 1933; Smirnov 1948).
"""

from __future__ import annotations

import networkx as nx
from scipy.stats import ks_2samp


def ks_test_degree(
    g_orig: nx.Graph,
    g_anon: nx.Graph,
) -> tuple[float, float]:
    """Compare degree distributions of original and anonymised graphs via KS test.

    Applies the two-sample Kolmogorov-Smirnov test
    (``scipy.stats.ks_2samp``) to the degree sequences of ``g_orig`` and
    ``g_anon``.  The D statistic measures the maximum absolute difference
    between the two empirical CDFs.

    Parameters
    ----------
    g_orig:
        Original (pre-anonymisation) graph.
    g_anon:
        Anonymised graph (same node set; edges may differ).

    Returns
    -------
    tuple[float, float]
        ``(D, p_value)`` where:

        * ``D`` — KS statistic ∈ [0.0, 1.0].  0.0 indicates identical
          empirical CDFs; 1.0 indicates completely non-overlapping distributions.
        * ``p_value`` — two-sided p-value for the null hypothesis that both
          degree sequences are drawn from the same distribution.  A large
          p-value (≥ 0.05) means insufficient evidence to reject H0 (good
          utility); a small p-value (< 0.05) indicates significant divergence.

    Raises
    ------
    ValueError
        If either graph has no nodes (degree distribution undefined).

    Notes
    -----
    * ``ks_2samp`` operates on two independent samples; node counts in
      ``g_orig`` and ``g_anon`` need not match.
    * Degree is discrete; the p-value from ``ks_2samp`` is exact for
      continuous distributions and conservative (overcautious) for discrete
      ones.  This is appropriate for this application: a conservative test
      avoids declaring utility-loss falsely.
    * Complexity: O(n log n) for sorting the degree sequences.
    """
    if g_orig.number_of_nodes() == 0:
        raise ValueError("g_orig has no nodes; degree distribution is undefined.")
    if g_anon.number_of_nodes() == 0:
        raise ValueError("g_anon has no nodes; degree distribution is undefined.")

    orig_degrees = [d for _, d in g_orig.degree()]
    anon_degrees = [d for _, d in g_anon.degree()]

    stat, pval = ks_2samp(orig_degrees, anon_degrees)
    return (float(stat), float(pval))
