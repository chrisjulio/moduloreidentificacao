"""Subgraph-based re-identification attack via induced k-hop neighbourhood isomorphism.

Adversary background knowledge: the induced k-hop neighbourhood subgraph of
the target node in the original (pre-anonymisation) graph ``G_orig``.

Attack procedure
----------------
1. Extract the induced subgraph ``S_target`` of the target's k-hop
   neighbourhood in ``G_orig``.
2. For every node ``v`` in ``G_anon``, extract its k-hop neighbourhood
   induced subgraph ``S_v``.
3. Test whether ``S_target ≅ S_v`` using the VF2 algorithm
   (``networkx.algorithms.isomorphism.GraphMatcher``).
4. Return ``True`` iff exactly one node in ``G_anon`` yields an isomorphic
   neighbourhood (unique identification).

This attack is strictly stronger than the degree attack: a degree match is
necessary but not sufficient for isomorphic neighbourhoods.  He et al. (2009)
motivate neighbourhood-structure anonymisation specifically to defeat this
class of attack.

Reference: He, X. et al. (2009), Section 3 (neighbourhood background knowledge).
"""

from __future__ import annotations

import concurrent.futures

import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher


def _k_hop_induced_subgraph(g: nx.Graph, node: int, hop: int) -> nx.Graph:
    """Return the induced subgraph containing ``node`` and all nodes within
    ``hop`` hops.

    Parameters
    ----------
    g:
        Source graph.
    node:
        Centre of the neighbourhood.
    hop:
        Maximum hop distance from ``node`` (inclusive).

    Returns
    -------
    nx.Graph
        Induced subgraph with the same node IDs as ``g``.
    """
    reachable = nx.single_source_shortest_path_length(g, node, cutoff=hop)
    return g.subgraph(reachable.keys()).copy()


def subgraph_candidate_count(
    g_orig: nx.Graph,
    g_anon: nx.Graph,
    target: int,
    hop: int = 1,
    timeout: float | None = None,
) -> int:
    """Count nodes in ``g_anon`` whose k-hop neighbourhood is isomorphic to the
    target's neighbourhood in ``g_orig``.

    This is the raw observable behind :func:`subgraph_attack`: the attack
    succeeds iff this count is exactly ``1`` (unique identification).  Exposing
    the count separately lets callers distinguish *why* an attack fails —
    ``0`` candidates (the original neighbourhood fingerprint matches nothing in
    the anonymised graph) versus ``>1`` candidates (the fingerprint is shared
    by several nodes) — which a bare ``bool`` collapses together.  See issue #93
    (diagnostic of ``reidentification_rate_subgraph`` zeros).

    Parameters
    ----------
    g_orig, g_anon, target, hop, timeout:
        As in :func:`subgraph_attack`.

    Returns
    -------
    int
        Number of nodes in ``g_anon`` with a k-hop neighbourhood isomorphic to
        the target's neighbourhood in ``g_orig`` (``0`` if none, ``>=1`` otherwise).

    Raises
    ------
    ValueError
        If ``target`` is not a node in ``g_orig``, or ``hop`` is not a positive
        integer.
    TimeoutError
        If ``timeout`` is set and the candidate-search loop exceeds it.
    """
    if target not in g_orig:
        raise ValueError(f"Target node {target!r} not found in G_orig.")
    if not isinstance(hop, int) or hop < 1:
        raise ValueError(f"hop must be a positive integer; got {hop!r}.")

    s_target = _k_hop_induced_subgraph(g_orig, target, hop)

    def _find_candidates() -> list[int]:
        candidates: list[int] = []
        for v in g_anon.nodes():
            s_v = _k_hop_induced_subgraph(g_anon, v, hop)
            gm = GraphMatcher(s_target, s_v)
            if gm.is_isomorphic():
                candidates.append(v)
        return candidates

    if timeout is None:
        candidates = _find_candidates()
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_find_candidates)
            try:
                candidates = future.result(timeout=timeout)
            except concurrent.futures.TimeoutError as exc:
                raise TimeoutError(
                    f"subgraph_attack exceeded timeout of {timeout}s while "
                    "searching for candidates."
                ) from exc

    return len(candidates)


def subgraph_attack(
    g_orig: nx.Graph,
    g_anon: nx.Graph,
    target: int,
    hop: int = 1,
    timeout: float | None = None,
) -> bool:
    """Re-identify a target node using its k-hop induced neighbourhood as
    background knowledge.

    Determines whether an adversary who knows the structural neighbourhood of
    the target in ``g_orig`` can uniquely locate that target in ``g_anon`` by
    finding a single node whose neighbourhood subgraph is isomorphic (VF2).

    Parameters
    ----------
    g_orig:
        Original (pre-anonymisation) graph.  Used only to extract the
        target's neighbourhood — the adversary's background knowledge.
    g_anon:
        Anonymised graph in which the adversary searches for the target.
    target:
        Node identifier whose re-identification is tested.  Must be present
        in ``g_orig``.
    hop:
        Neighbourhood radius (number of hops).  Default: 1.  Larger values
        give the adversary more structural information but increase cost
        exponentially (VF2 worst-case is exponential in subgraph size).
        Restrict to ``hop=1`` for production use on large graphs.

        Trade-off summary
        ~~~~~~~~~~~~~~~~~
        * ``hop=1``: neighbourhood = target + direct neighbours.  Fast;
          often sufficient when node degrees vary widely.
        * ``hop=2``: includes friends-of-friends.  Much more discriminating
          but can be 10-100x slower on dense graphs.
        * ``hop>=3``: rarely needed; risk of spanning the entire graph for
          low-diameter networks.

    timeout:
        Maximum wall-clock seconds for the candidate-search loop.  If the
        loop is still running after ``timeout`` seconds a ``TimeoutError``
        is raised.  ``None`` (default) means no limit.

    Returns
    -------
    bool
        ``True`` if exactly one node in ``g_anon`` has a k-hop neighbourhood
        isomorphic to the target's neighbourhood in ``g_orig``; ``False``
        otherwise (zero or multiple candidates → attack fails to uniquely
        identify the target).

    Raises
    ------
    ValueError
        If ``target`` is not a node in ``g_orig``.
    ValueError
        If ``hop`` is not a positive integer.
    TimeoutError
        If ``timeout`` is set and the candidate-search loop exceeds it.

    Notes
    -----
    * Backend: VF2 via ``networkx.algorithms.isomorphism.GraphMatcher``
      (``is_isomorphic``).  Node labels are ignored; only structure is compared.
    * Complexity: O(|V_anon| · VF2(|S_target|)) where VF2 is worst-case
      exponential in the size of ``S_target``.  For ``hop=1`` the subgraph
      is bounded by max-degree + 1 nodes, which is typically manageable.
    * The attack does **not** depend on which node in ``g_anon`` actually
      *is* the target — it tests whether the neighbourhood fingerprint is
      sufficient to single out one node.
    * Node IDs in ``g_orig`` and ``g_anon`` share the same namespace;
      anonymisation (He et al.) preserves node IDs.
    * Implemented on top of :func:`subgraph_candidate_count`: a node is
      uniquely identified iff it has exactly one isomorphic candidate.
    """
    return subgraph_candidate_count(g_orig, g_anon, target, hop=hop, timeout=timeout) == 1
