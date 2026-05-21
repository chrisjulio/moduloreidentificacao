"""Anonimizador estrutural baseado em He et al. (2009).

Ref: He, X., Vaidya, J., Shafiq, B., Adam, N., & Atluri, V. (2009).
     Preserving Privacy in Social Networks: A Structure-Aware Approach.
     IEEE/WIC/ACM International Joint Conference on Web Intelligence
     and Intelligent Agent Technology (WI-IAT), pp. 647-653.

Pipeline de anonimizacao (Secao 3):
    1. _partition_neighborhoods  -- particiona G em Local Structures
    2. _group_isomorphic         -- agrupa LS por FSM + fator MF
    3. _modify_structure         -- torna grupos isomorfos (Fases 1 e 2)
    4. _reconnect_inter_edges    -- reconecta inter-arestas preservando isomorfismo
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterator
from typing import NamedTuple

import networkx as nx
import numpy as np

from src.anonymization._partition_backend import partition_graph

# ---------------------------------------------------------------------------
# Private helpers — Simplified FSM (D-01)
# ---------------------------------------------------------------------------


class _PatternEntry(NamedTuple):
    """Catalog entry for a frequent subgraph pattern (FSM, D-01).

    Attributes
    ----------
    rep:
        A representative copy of the subgraph (used to read ``number_of_edges``).
    ls_indices:
        Indices (into the current bucket) of Local Structures that contain
        this pattern.
    """

    rep: nx.Graph
    ls_indices: set[int]


def _connected_subsets(g: nx.Graph, max_size: int) -> Iterator[frozenset]:
    """Yield every distinct connected node-subset of *g* of size 1..max_size.

    Uses depth-first expansion with a ``seen`` set to avoid revisiting the
    same subset regardless of which starting node reached it first.
    Iteration order is deterministic: nodes are visited in sorted order
    before each expansion.

    Parameters
    ----------
    g:
        Input undirected graph.
    max_size:
        Maximum number of nodes per subset (inclusive).

    Yields
    ------
    frozenset
        A connected node-subset of *g* with at most *max_size* nodes.

    Notes
    -----
    For small graphs (|V| <= 20) and max_size <= 4 the total number of
    subsets is at most C(20, 4) = 4 845 — well within the practical
    performance envelope required by FSM (D-01).
    Complexity per call: O(C(|V|, max_size)).
    """
    seen: set[frozenset] = set()

    def _expand(current: frozenset) -> Iterator[frozenset]:
        if current in seen:
            return
        seen.add(current)
        yield current
        if len(current) < max_size:
            border: set = set()
            for v in current:
                border.update(g.neighbors(v))
            border -= set(current)
            for u in sorted(border):
                yield from _expand(current | frozenset([u]))

    for start in sorted(g.nodes()):
        yield from _expand(frozenset([start]))


def _group_within_bucket(
    bucket: list[nx.Graph],
    k: int,
    sigma: float,
    rng: np.random.Generator,
    fsm_max_size: int = 4,
) -> list[list[nx.Graph]]:
    """FSM + MF greedy grouping for a same-size bucket of Local Structures.

    Implements the core of Algorithm 1 (He et al., 2009, p. 650-651) for
    a homogeneous set of Local Structures with the same number of nodes
    (D-07 Opção A).

    Parameters
    ----------
    bucket:
        Local Structures to group, **all with the same number of nodes**.
    k:
        Target group size (k-anonymity parameter).
    sigma:
        Minimum support fraction for the simplified FSM (D-01).
        Pattern must appear in ``max(1, int(sigma * n))`` LSs to qualify.
    rng:
        Seeded NumPy Generator for reproducible random choices.
    fsm_max_size:
        Maximum subgraph size (nodes) for the simplified FSM (D-01).
        Default: 4 (``anonymization.fsm.max_size``).

    Returns
    -------
    list[list[nx.Graph]]
        Ordered list of groups. All complete groups have exactly *k*
        members. The last group may have fewer than *k* members (D-06).
    """
    n = len(bucket)
    groups: list[list[nx.Graph]] = []

    if n == 0:
        return groups

    min_support = max(1, int(sigma * n))

    # ------------------------------------------------------------------
    # Simplified FSM (D-01)
    # Enumerate every connected induced subgraph up to fsm_max_size nodes
    # for each LS and fingerprint it with the Weisfeiler-Lehman graph hash.
    # WL hash serves as the canonical form; collisions are negligible for
    # subgraphs with <= fsm_max_size nodes.
    # ------------------------------------------------------------------
    # pattern_catalog: wl_hash -> _PatternEntry(rep, ls_indices)
    pattern_catalog: dict[str, _PatternEntry] = {}

    for ls_idx, ls in enumerate(bucket):
        seen_hashes: set[str] = set()
        for node_subset in _connected_subsets(ls, fsm_max_size):
            sg = ls.subgraph(node_subset)
            h = nx.weisfeiler_lehman_graph_hash(sg)
            if h not in seen_hashes:
                seen_hashes.add(h)
                if h not in pattern_catalog:
                    pattern_catalog[h] = _PatternEntry(rep=sg.copy(), ls_indices=set())
                pattern_catalog[h].ls_indices.add(ls_idx)

    # Frequent patterns: support >= min_support; sorted by hash for determinism
    frequent: list[tuple[str, nx.Graph, list[int]]] = sorted(
        (
            (h, entry.rep, sorted(entry.ls_indices))
            for h, entry in pattern_catalog.items()
            if len(entry.ls_indices) >= min_support
        ),
        key=lambda x: x[0],
    )

    # ------------------------------------------------------------------
    # Greedy grouping — Algorithm 1 (He et al., 2009, Section 3.2)
    # ------------------------------------------------------------------
    available: set[int] = set(range(n))

    while len(available) >= k:
        # Compute MF for each frequent pattern restricted to available LSs.
        # Tiebreak on MF: smaller hash string → deterministic (D-03 style).
        best_mf: float = -1.0
        best_h: str = ""
        best_sls: list[int] = []

        for h, rep, ls_list in frequent:
            sls = [i for i in ls_list if i in available]
            if not sls:
                continue
            n_edges = rep.number_of_edges()
            mf = float(n_edges * k if len(sls) >= k else n_edges * len(sls))
            if mf > best_mf or (mf == best_mf and (not best_h or h < best_h)):
                best_mf = mf
                best_h = h
                best_sls = sls

        if not best_sls:
            # No frequent pattern covers remaining available LSs.
            # Fall back to random grouping to exhaust the available pool.
            remaining = sorted(available)
            perm = rng.permutation(len(remaining)).tolist()
            shuffled = [remaining[i] for i in perm]
            n_complete = len(shuffled) - len(shuffled) % k
            for i in range(0, n_complete, k):
                chunk = shuffled[i : i + k]
                groups.append([bucket[j] for j in chunk])
                for j in chunk:
                    available.discard(j)
            break

        # Form a group of k LSs from best_sls (Algorithm 1, lines 15-21)
        if len(best_sls) >= k:
            # |SLS(gj)| >= k: choose k LSs randomly from SLS(gj)
            chosen_pos = rng.choice(len(best_sls), size=k, replace=False)
            chosen = [best_sls[int(p)] for p in sorted(chosen_pos)]
        else:
            # |SLS(gj)| < k: use all from best_sls and complete with others
            chosen = list(best_sls)
            others = sorted(available - set(chosen))
            needed = k - len(chosen)
            # len(others) = len(available) - len(chosen) >= k - len(chosen) = needed
            extra_pos = rng.choice(len(others), size=needed, replace=False)
            chosen += [others[int(p)] for p in sorted(extra_pos)]

        groups.append([bucket[i] for i in chosen])
        for i in chosen:
            available.discard(i)

    # Remaining LSs (< k) → incomplete final group (D-06)
    if available:
        groups.append([bucket[i] for i in sorted(available)])

    return groups


# ---------------------------------------------------------------------------
# Public pipeline functions
# ---------------------------------------------------------------------------


def anonymize(g: nx.Graph, k: int, d: int, seed: int) -> nx.Graph:
    """Ponto de entrada principal do algoritmo de anonimizacao estrutural.

    Executa o pipeline completo de structure-aware kd-anonymity:
    (1) particiona G em Local Structures de tamanho d minimizando
    inter-arestas; (2) agrupa as Local Structures via FSM + fator MF;
    (3) torna cada grupo isomorfo por adicao/remocao de arestas;
    (4) reconecta as inter-arestas preservando o isomorfismo formado.

    Parametros
    ----------
    g : nx.Graph
        Grafo original nao direcionado a ser anonimizado.
    k : int
        Parametro de k-anonimato estrutural. Cada no devera ser
        indistinguivel de pelo menos k-1 outros nos com Local Structure
        isomorfa. Controla o nivel de privacidade.
    d : int
        Tamanho de cada Local Structure (numero de nos por particao).
        Define a granularidade da particao: ck = floor(n / d) particoes.
        Pode ser variado pelo publicador para minimizar perturbacao
        mantendo o mesmo nivel k.
    seed : int
        Semente aleatoria para reproducibilidade das escolhas nao
        deterministicas durante agrupamento e modificacao estrutural.

    Retorna
    -------
    nx.Graph
        Copia do grafo com estrutura modificada satisfazendo
        structure-aware k-anonimato (Definicao 3 do artigo).

    Referencia
    ----------
    He et al. (2009), Secao 3 -- Anonymization Techniques.
    Secoes 2.3 (Definicao 3) e 3 (visao geral do pipeline de 3 passos).
    """
    raise NotImplementedError


def _partition_neighborhoods(
    g: nx.Graph,
    d: int,
    seed: int = 0,
    backend: str = "auto",
) -> list[nx.Graph]:
    """Particiona G em Local Structures usando multilevel k-way partitioning.

    Divide o conjunto de nos V em ck = floor(n/d) subconjuntos disjuntos
    V1, V2, ..., Vck de tamanho aproximadamente d, minimizando o numero
    de inter-arestas entre particoes distintas (problema NP-completo,
    resolvido via heuristica multilevel k-way de Karypis & Kumar [14]).

    Apos a particao, as inter-arestas sao removidas temporariamente.
    Cada componente resultante Ci = (Vi, Ei) corresponde a uma
    Local Structure LSi, conforme a Definicao 1 do artigo.

    O particionamento e delegado a ``_partition_backend.partition_graph``,
    que seleciona automaticamente entre pymetis (motor primario, fiel ao
    artigo) e networkx KL (fallback D-04) conforme a disponibilidade do
    ambiente.

    Parametros
    ----------
    g : nx.Graph
        Grafo de entrada nao-direcionado.
    d : int
        Tamanho alvo de cada Local Structure em numero de nos.
        Determina o numero de particoes: ck = floor(n / d).
        Nao e profundidade de vizinhanca -- e tamanho de particao.
    seed : int, optional
        Semente aleatoria para reproducibilidade do backend KL.
        Ignorada pelo pymetis (deterministico). Propagada de
        ``anonymize`` via parametro ``seed``. Padrao: 0.
    backend : str, optional
        Motor de particionamento: ``"auto"`` (padrao), ``"pymetis"``
        ou ``"networkx-kl"``. Passado diretamente a ``partition_graph``.

    Retorna
    -------
    list[nx.Graph]
        Lista de ck subgrafos {C1, C2, ..., Cck}, cada um correspondendo
        a uma Local Structure LSi com as inter-arestas removidas.
        Os subgrafos sao copias independentes (``copy()``), nao views
        do grafo original.

    Raises
    ------
    ValueError
        Se d >= n (nao e possivel formar nenhuma particao).

    Referencia
    ----------
    He et al. (2009), Secao 3.1 -- Graph Partition.
    Algoritmo de particao: Karypis & Kumar [14] (multilevel k-way).
    Decisao D-04 (revisado 20/05/2026) em docs/algorithm_notes.md sec. 7.
    """
    n = g.number_of_nodes()
    if d >= n:
        raise ValueError(f"d={d} deve ser menor que n={n} para formar ao menos uma particao.")

    ck = n // d
    node_sets, _meta = partition_graph(g, ck, seed=seed, backend=backend)

    local_structures: list[nx.Graph] = []
    for node_set in node_sets:
        # subgraph() retorna apenas arestas cujos dois extremos estao em node_set,
        # excluindo automaticamente inter-arestas (Secao 3.1, passo 1.4).
        ls = g.subgraph(node_set).copy()
        local_structures.append(ls)

    return local_structures


def _group_isomorphic(
    local_structures: list[nx.Graph],
    k: int,
    sigma: float,
    seed: int,
) -> list[list[nx.Graph]]:
    """Agrupa Local Structures usando Frequent Subgraph Mining e fator MF.

    Executa o Algorithm 1 do artigo: aplica um algoritmo FSM simplificado
    (D-01) sobre o conjunto de Local Structures com suporte sigma para obter
    subgrafos frequentes g1, ..., gm. Para cada gi, calcula o fator de
    multiplicacao:

        MF(gi) = |E(gi)| x k           se |SLS(gi)| >= k
        MF(gi) = |E(gi)| x |SLS(gi)|   caso contrario

    onde SLS(gi) e o conjunto de Local Structures que contem gi.
    Iterativamente seleciona gi com maior MF e forma grupos de k
    Local Structures, priorizando aquelas que compartilham gi.
    Local Structures nao agrupadas ao final formam o ultimo grupo.

    Parametros
    ----------
    local_structures : list[nx.Graph]
        Lista de Local Structures retornada por _partition_neighborhoods.
    k : int
        Tamanho de cada grupo (parametro de k-anonimato).
    sigma : float
        Limiar de suporte para o FSM (ex.: 0.20 para 20%).
        Valores baixos permitem mais subgrafos frequentes candidatos.
        ``sigma=0`` → suporte minimo de 1 LS; ``sigma=1`` → apenas padroes
        presentes em todas as LSs sao frequentes.
    seed : int
        Semente aleatoria para escolhas nao-deterministicas no agrupamento
        (Algorithm 1, linhas 15, 17, 21 — Secao 3.3 deste documento).

    Retorna
    -------
    list[list[nx.Graph]]
        Lista de grupos. Grupos completos tem exatamente k membros.
        O ultimo grupo pode ter menos de k membros (D-06).

    Notas de implementacao
    ----------------------
    **Nao usa** ``nx.is_isomorphic`` como abordagem principal. O isomorfismo
    e aproximado via hash Weisfeiler-Lehman (D-01, ``fsm_max_size=4``).
    Colisoes de hash sao estatisticamente negligenciaveis para subgrafos
    com ate 4 nos.

    **D-07 Opcao A** (formalizado 20/05/2026): antes de executar o FSM,
    as LSs sao indexadas pelo numero de nos. Grupos sao formados
    exclusivamente entre LSs de mesmo tamanho. LSs sem grupo completo
    do mesmo tamanho formam o grupo final incompleto (D-06).

    **Custo computacional** (FSM simplificado vs. VF2 par-a-par):

    * **VF2 par-a-par** (abordagem evitada): O(ck^2) chamadas a
      ``nx.is_isomorphic``, cada uma com custo VF2 de O(d! / aut). Para
      ck=50 e d=10 sao 1 225 chamadas. Cresce quadraticamente com ck.
    * **FSM simplificado + MF** (esta implementacao): O(ck * C(d, s_max))
      para enumerar subgrafos (C(10,4) = 210 por LS) mais O(ck * m * 1)
      para calcular MF em cada iteracao, onde m e o numero de padroes
      frequentes (tipicamente << ck). Cresce linearmente com ck.

    Referencia
    ----------
    He et al. (2009), Secao 3.2 -- Local Structures Grouping.
    Algorithm 1 (Local Structure Grouping, p. 650-651).
    D-01, D-06, D-07 em docs/algorithm_notes.md §7.
    """
    rng = np.random.default_rng(seed)

    if not local_structures:
        return []

    # D-07 Opção A: index LSs by size; groups form only within same-size bins
    size_buckets: dict[int, list[int]] = defaultdict(list)
    for ls_idx, ls in enumerate(local_structures):
        size_buckets[ls.number_of_nodes()].append(ls_idx)

    all_groups: list[list[nx.Graph]] = []
    for size in sorted(size_buckets.keys()):
        bucket_indices = size_buckets[size]
        bucket_ls = [local_structures[i] for i in bucket_indices]
        bucket_groups = _group_within_bucket(bucket_ls, k, sigma, rng)
        all_groups.extend(bucket_groups)

    return all_groups


def _modify_structure(
    groups: list[list[nx.Graph]],
    seed: int,
    add_only: bool = False,
) -> list[list[nx.Graph]]:
    """Torna isomorfas as Local Structures de cada grupo (Fases 1 e 2).

    Implementa a anonimizacao intra-grupo em duas fases:

    Phase 1 -- Numeracao de nos (node matching):
        Para as Local Structures que compartilham o subgrafo comum gi,
        atribui numeros naturais crescentes aos nos de gi. Para as
        demais, realiza matching por grau (closeness de grau) em relacao
        aos nos ja numerados, propagando a numeracao pelos vizinhos.

    Phase 2 -- Modificacao de arestas:
        Com os nos numerados, torna as k Local Structures isomorfas:
        (i)  add_only=True:  apenas adiciona arestas;
        (ii) add_only=False: para cada par de nos correspondentes,
             escolhe adicao ou remocao de aresta conforme minimize
             o numero total de mudancas estruturais.

    Parametros
    ----------
    groups : list[list[nx.Graph]]
        Grupos de Local Structures retornados por _group_isomorphic.
    seed : int
        Semente aleatoria para desempates no matching de nos.
    add_only : bool, optional
        Se True, aplica apenas adicao de arestas (Edge Adding).
        Se False, aplica adicao e remocao (Edge Adding/Deleting),
        que gera menor perturbacao estrutural. Padrao: False.

    Retorna
    -------
    list[list[nx.Graph]]
        Grupos com Local Structures modificadas e isomorfas entre si,
        prontas para reconexao.

    Referencia
    ----------
    He et al. (2009), Secao 3.2 -- Local Structures Grouping and
    Anonymization, Phase 1 (p. 651) e Phase 2 (p. 652).
    """
    raise NotImplementedError


def _reconnect_inter_edges(
    g_original: nx.Graph,
    groups: list[list[nx.Graph]],
) -> nx.Graph:
    """Reconecta as inter-arestas removidas preservando o isomorfismo.

    Apos a anonimizacao intra-grupo, restaura as inter-arestas que foram
    removidas na etapa de particao. A simples restauracao quebraria o
    isomorfismo formado, pois alteraria as vizinhancas dos nos nas
    extremidades das inter-arestas. Por isso, para cada inter-aresta
    original reconectada, sao adicionadas k(k-1) arestas adicionais
    de forma a manter o isomorfismo entre os nos correspondentes nos
    demais grupos.

    Como a particao minimiza inter-arestas, o numero total de arestas
    adicionais nesta etapa e controlado.

    Parametros
    ----------
    g_original : nx.Graph
        Grafo original, usado para recuperar as inter-arestas removidas
        na particao.
    groups : list[list[nx.Graph]]
        Grupos de Local Structures ja anonimizadas por _modify_structure.

    Retorna
    -------
    nx.Graph
        Grafo final anonimizado e reconectado, satisfazendo
        structure-aware k-anonimato.

    Referencia
    ----------
    He et al. (2009), Secao 3.3 -- Reconnecting Local Structures (p. 652).
    Para cada inter-aresta reconectada: k(k-1) arestas adicionadas.
    """
    raise NotImplementedError
