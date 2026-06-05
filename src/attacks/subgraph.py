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
from collections.abc import Iterable

import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher

# Default number of Weisfeiler-Lehman refinement iterations used by the
# bucketing fast path (:func:`subgraph_candidate_counts`).  Three iterations
# are the networkx default and are more than enough to discriminate hop-1
# neighbourhoods (a star centre plus the edges among its neighbours).
_WL_ITERATIONS = 3


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


def _neighbourhood_wl_hash(
    g: nx.Graph, node: int, hop: int, iterations: int = _WL_ITERATIONS
) -> str:
    """Weisfeiler-Lehman graph hash of ``node``'s k-hop induced neighbourhood.

    The hash is a graph *invariant*: isomorphic neighbourhoods always share the
    same hash (necessary condition).  It is not, in general, *injective* — two
    non-isomorphic graphs may collide — which is why the bucketing fast path
    offers an optional VF2 refinement (see :func:`subgraph_candidate_counts`).
    Node labels are ignored (structure only), matching the VF2 brute force.
    """
    sub = _k_hop_induced_subgraph(g, node, hop)
    return nx.weisfeiler_lehman_graph_hash(sub, iterations=iterations)


class _AnonNeighbourhoodIndex:
    """WL-hash bucket index over the k-hop neighbourhoods of ``g_anon``.

    Built once per anonymised graph (O(n) neighbourhood extractions), it lets
    each target be resolved by a single hash lookup instead of re-scanning all
    ``n`` candidate neighbourhoods — the O(n²) cost that made the full subgraph
    attack prohibitive on the Enron LCC (decision D-15; issue #139).

    Buckets store node IDs (not subgraphs) to keep memory light; the few small
    neighbourhoods needed by VF2 refinement are re-extracted lazily.
    """

    def __init__(self, g_anon: nx.Graph, hop: int, iterations: int = _WL_ITERATIONS) -> None:
        self._g_anon = g_anon
        self._hop = hop
        self._iterations = iterations
        self._buckets: dict[str, list[int]] = {}
        for v in g_anon.nodes():
            h = _neighbourhood_wl_hash(g_anon, v, hop, iterations)
            self._buckets.setdefault(h, []).append(v)

    def candidate_count(self, s_target: nx.Graph, refine_max_size: int | None = None) -> int:
        """Count ``g_anon`` nodes whose neighbourhood matches ``s_target``.

        With ``refine_max_size=None`` (pure WL) the count is the size of the
        hash bucket — exact whenever the WL hash is collision-free for the
        graphs at hand (verified empirically; see issue #139).  With
        ``refine_max_size`` set, buckets whose target neighbourhood has at most
        that many nodes are confirmed with VF2 (exact); larger neighbourhoods
        (hubs) stay on pure WL — refining a hub with VF2 triggers the
        automorphism blow-up that the fast path exists to avoid.
        """
        h = nx.weisfeiler_lehman_graph_hash(s_target, iterations=self._iterations)
        bucket = self._buckets.get(h, [])
        if refine_max_size is None or s_target.number_of_nodes() > refine_max_size:
            return len(bucket)
        count = 0
        for v in bucket:
            s_v = _k_hop_induced_subgraph(self._g_anon, v, self._hop)
            if GraphMatcher(s_target, s_v).is_isomorphic():
                count += 1
        return count


def subgraph_candidate_counts(
    g_orig: nx.Graph,
    g_anon: nx.Graph,
    targets: Iterable[int],
    hop: int = 1,
    refine_max_size: int | None = None,
    wl_iterations: int = _WL_ITERATIONS,
) -> dict[int, int]:
    """Candidate counts for many targets at once via WL-hash bucketing.

    Batched, O(n) equivalent of calling :func:`subgraph_candidate_count` once
    per target: the k-hop neighbourhoods of ``g_anon`` are hashed a single time
    into buckets, then each target is resolved by a hash lookup.  This replaces
    the per-target O(n) re-scan (overall O(n²)) that made the full subgraph
    attack on the Enron LCC cost ~70 days (decision D-15); the bucketed path
    runs in seconds (issue #139).

    The returned count is identical to :func:`subgraph_candidate_count` whenever
    the WL hash is collision-free for the input graphs — the established case
    for the hop-1 neighbourhoods used here (exhaustively checked against VF2 on
    small graphs and verified on a large Enron node sample).  ``refine_max_size``
    optionally confirms small buckets with VF2 for an exact-by-construction
    result; hubs are never refined (the blow-up the fast path avoids).

    Parameters
    ----------
    g_orig, g_anon:
        Original and anonymised graphs (same node namespace as the brute force).
    targets:
        Iterable of target node IDs in ``g_orig`` to score.
    hop:
        Neighbourhood radius (positive integer).  Default 1.
    refine_max_size:
        If set, buckets whose target neighbourhood has at most this many nodes
        are confirmed with VF2 (exact); ``None`` (default) uses pure WL.
    wl_iterations:
        Weisfeiler-Lehman refinement iterations (default :data:`_WL_ITERATIONS`).

    Returns
    -------
    dict[int, int]
        Mapping ``target -> #isomorphic candidates in g_anon``.  A target is
        uniquely re-identified iff its count is exactly ``1``.

    Raises
    ------
    ValueError
        If ``hop`` is not a positive integer, or a target is absent from
        ``g_orig``.
    """
    if not isinstance(hop, int) or hop < 1:
        raise ValueError(f"hop must be a positive integer; got {hop!r}.")

    index = _AnonNeighbourhoodIndex(g_anon, hop, iterations=wl_iterations)
    counts: dict[int, int] = {}
    for target in targets:
        if target not in g_orig:
            raise ValueError(f"Target node {target!r} not found in G_orig.")
        s_target = _k_hop_induced_subgraph(g_orig, target, hop)
        counts[target] = index.candidate_count(s_target, refine_max_size=refine_max_size)
    return counts


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
