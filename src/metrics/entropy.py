"""Entropy / degree-of-anonymity privacy metric.

Measures the **residual uncertainty** of an adversary who has narrowed a
target down to its equivalence group, expressed in bits of Shannon entropy.
Reuses the equivalence-group partition already produced by the He et al.
(2009) pipeline — it does **not** re-run any experiment.

Classification (decision D-17)
------------------------------
This is a **privacy metric**, not an autonomous structural attack: unlike
``degree_attack`` / ``subgraph_attack`` it uses **no** background knowledge
about the original graph ``G_orig`` — it is derived purely from the
equivalence partition.  The "entropy attack" of the operational plan is the
**adversarial reading** of this metric; ``src/attacks/entropy.py`` is a
cross-reference pointer to this module (see D-17 in docs/decision_log.md).

Model (uniform baseline, D-E2(a))
---------------------------------
For an equivalence group ``G_r`` holding ``n_r`` nodes, under the
equiprobable model (candidates uniform, ``p_i = 1/n_r``):

    H(G_r) = log2(n_r)        # uncertainty, in bits (Serjantov & Danezis 2002)

Every node ``v`` in ``G_r`` inherits ``H(v) = log2(n_r)``.  The uniform case
is the **maximum entropy** ``log2(N)`` of Serjantov & Danezis (2002) for a
candidate set of size ``N``, and aligns with the ``<= 1/k`` bound of He et al.
(2009), Def. 2-3.

Reported metrics
----------------
* ``entropy_mean`` — node-weighted mean of ``H(v) = log2(n_r)`` over the
  nodes covered by the groups.
* ``degree_of_anonymity`` — node-weighted mean of the **normalised degree of
  anonymity** ``H(v) / H_max`` (Díaz, Seys, Claessens & Preneel 2002), with
  ``H_max = log2(max_r n_r)``; a scalar in ``[0, 1]`` comparable across
  ``k`` / datasets and **not** redundant with the raw group size.
* ``reidentification_rate_entropy`` — fraction of covered nodes with
  ``H(v) <= tau``.  The default ``tau = 0`` recovers the "singleton group"
  criterion (``n_r <= 1``), comparable to ``count == 1`` of the structural
  attacks.

Methodological note (D-17)
--------------------------
Per group, ``H = log2(n_r)`` is a strictly monotone transform of the node
count already reported by ``equivalence_group_size`` — so on its own it adds
no new ordering.  Under full k-anonymity (``n_r >= k >= 2``) we have
``H >= 1`` bit, hence ``tau = 0`` only fires on degenerate/incomplete groups,
the same deficit residue captured by ``coverage_fraction`` /
``deficit_fully_structural`` (D-06).  The genuinely distinct outputs are
``degree_of_anonymity`` (Díaz et al.) and the non-uniform weighting path
(intra-group probabilities, e.g. degree-similarity to the target), the latter
declared an **exploratory, empirically validable** extension in D-17.

References
----------
* Serjantov, A.; Danezis, G. *Towards an Information Theoretic Metric for
  Anonymity.* PET 2002, LNCS 2482, pp. 41-53. DOI 10.1007/3-540-36467-6_4.
* Díaz, C.; Seys, S.; Claessens, J.; Preneel, B. *Towards Measuring
  Anonymity.* PET 2002, LNCS 2482, pp. 54-68. DOI 10.1007/3-540-36467-6_5.
* He, X. et al. (2009), Section 2.3 (Def. 2-3, ``<= 1/k`` bound).
* docs/metrics_definitions.md (§ entropy); docs/decision_log.md (D-17).
"""

from __future__ import annotations

import math

import networkx as nx


def entropy_metrics(
    groups: list[list[nx.Graph]],
    tau: float = 0.0,
) -> dict[str, float]:
    """Compute Shannon-entropy / degree-of-anonymity privacy metrics.

    Parameters
    ----------
    groups:
        Partition of Local Structures (LSs) into equivalence groups, in the
        same format as ``validate_k_anonymity`` and ``equivalence_group_size``:
        ``groups[r][j]`` is the j-th LS (induced subgraph of G') in group r.
        The group's node count ``n_r`` is the total number of nodes across all
        its LSs (decision D-E1(a) — node-counting, consistent with
        ``equivalence_group_size``).
    tau:
        Entropy threshold (bits) for ``reidentification_rate_entropy``: a node
        counts as re-identified when ``H(v) <= tau``.  Default ``0.0`` recovers
        the "singleton group" criterion (``n_r <= 1``).  Must be non-negative.
        Read from ``metrics.entropy_tau`` in the experiment YAML by the runner
        (decision D-E3(b)).

    Returns
    -------
    dict[str, float]
        ``{"entropy_mean", "degree_of_anonymity",
        "reidentification_rate_entropy", "tau"}``.  All node-weighted over the
        nodes covered by ``groups``.

    Raises
    ------
    ValueError
        If ``groups`` is empty, if the groups contain no nodes at all, or if
        ``tau`` is negative.

    Notes
    -----
    * Empty groups (``n_r == 0``, possible under the partitioner, D-08) carry
      zero weight and are skipped; they do not affect any reported value.
    * ``degree_of_anonymity`` is defined as ``0.0`` when ``H_max == 0`` (every
      group is a singleton → the system provides no anonymity), following the
      Díaz et al. convention for ``N == 1``.
    * Complexity: O(G) where G = total number of LSs across all groups.
    """
    if not groups:
        raise ValueError("groups must be non-empty; got an empty list.")
    if tau < 0:
        raise ValueError(f"tau must be non-negative; got {tau}.")

    sizes: list[int] = [sum(ls.number_of_nodes() for ls in group) for group in groups]
    total_nodes: int = sum(sizes)
    if total_nodes == 0:
        raise ValueError("groups contain no nodes; the entropy metric is undefined.")

    max_size: int = max(sizes)
    # H_max = log2(max n_r); 0 when every (non-empty) group is a singleton.
    h_max: float = math.log2(max_size) if max_size > 1 else 0.0

    weighted_entropy_sum: float = 0.0
    weighted_doa_sum: float = 0.0
    reidentified_nodes: int = 0
    for n_r in sizes:
        if n_r <= 0:
            continue  # empty group: zero weight, skip (avoids log2(0))
        h_r: float = math.log2(n_r)  # log2(1) == 0.0
        weighted_entropy_sum += n_r * h_r
        if h_max > 0:
            weighted_doa_sum += n_r * (h_r / h_max)
        if h_r <= tau:
            reidentified_nodes += n_r

    entropy_mean: float = weighted_entropy_sum / total_nodes
    degree_of_anonymity: float = (weighted_doa_sum / total_nodes) if h_max > 0 else 0.0
    reidentification_rate_entropy: float = reidentified_nodes / total_nodes

    return {
        "entropy_mean": entropy_mean,
        "degree_of_anonymity": degree_of_anonymity,
        "reidentification_rate_entropy": reidentification_rate_entropy,
        "tau": float(tau),
    }
