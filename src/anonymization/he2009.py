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


def anonymize(g: nx.Graph, k: int, d: int, seed: int, fsm_max_size: int = 4) -> nx.Graph:
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
    fsm_max_size : int
        Tamanho maximo (em nos) dos subgrafos enumerados pelo FSM
        simplificado no Passo 2 (D-01). Lido da chave YAML
        ``anonymization.s_max`` (alias ``fsm_max_size``) pelo runner de
        experimentos; default 4. Ver docs/algorithm_notes.md §5.1 (B5).

    Retorna
    -------
    nx.Graph
        Copia do grafo com estrutura modificada satisfazendo
        structure-aware k-anonimato (Definicao 3 do artigo). O atributo
        ``g_prime.graph["metadata"]`` carrega os contadores de modificacao
        por fase (G5-a, issue #80):

        * ``edges_modified_phase2_intragroup``: total de arestas
          adicionadas/removidas pela isomorfizacao intra-grupo (Fase 2).
        * ``edges_added_reconnection``: total de arestas novas adicionadas
          pela reconexao de inter-arestas (Secao 3.3).

        Ambos sao inteiros >= 0 e permitem atribuir o efeito sobre a
        utilidade entre isomorfizacao e reconexao.

    Notas
    -----
    Parametros internos fixados nesta chamada de alto nivel:
    * ``sigma=0.5``: suporte minimo de 50 % para o FSM simplificado
      (D-01). Valor conservador que garante padroes estruturalmente
      representativos sem restringir demais o agrupamento.
    * ``add_only=False``: variante Edge Adding/Deleting para menor
      perturbacao media (``anonymization.isomorphism_mode="add_or_delete"``
      na Tabela de parametros, Secao 5 de docs/algorithm_notes.md).
    * ``backend="auto"``: pymetis quando disponivel, fallback KL (D-04).

    Referencia
    ----------
    He et al. (2009), Secao 3 -- Anonymization Techniques.
    Secoes 2.3 (Definicao 3) e 3 (visao geral do pipeline de 3 passos).
    """
    # ------------------------------------------------------------------
    # Step 1 — Partition G into Local Structures (Section 3.1)
    # ------------------------------------------------------------------
    local_structures = _partition_neighborhoods(g, d, seed=seed, backend="auto")

    # ------------------------------------------------------------------
    # Step 2 — Group Local Structures via FSM + MF factor (Section 3.2)
    # ------------------------------------------------------------------
    groups = _group_isomorphic(
        local_structures, k=k, sigma=0.5, seed=seed, fsm_max_size=fsm_max_size
    )

    # ------------------------------------------------------------------
    # Step 3 — Make each group isomorphic (Section 3.2, Phases 1 & 2)
    # ------------------------------------------------------------------
    modified_groups, edges_modified_phase2 = _modify_structure(
        groups, seed=seed, add_only=False, return_counts=True
    )

    # ------------------------------------------------------------------
    # Step 4 — Reconnect inter-partition edges (Section 3.3)
    # ------------------------------------------------------------------
    g_prime = _reconnect_inter_edges(g, modified_groups)

    # G5-a (issue #80): expose per-phase modification counters via a graph
    # attribute so downstream consumers (e.g. the experiment runner, G5-b in
    # issue #77) can attribute perturbation to isomorphization vs. reconnection
    # without changing the return signature of anonymize().
    g_prime.graph.setdefault("metadata", {})
    g_prime.graph["metadata"]["edges_modified_phase2_intragroup"] = edges_modified_phase2

    return g_prime


def _partition_neighborhoods(
    g: nx.Graph,
    d: int,
    seed: int = 0,
    backend: str = "auto",
    return_meta: bool = False,
) -> list[nx.Graph] | tuple[list[nx.Graph], dict]:
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
    return_meta : bool, optional
        Se ``True``, retorna tambem o dicionario de metadados de
        ``partition_graph`` (que inclui ``backend_used`` -- o motor de
        fato utilizado nesta particao). Padrao: ``False`` (mantem a
        assinatura historica que retorna apenas a lista de LSs).

    Retorna
    -------
    list[nx.Graph]
        Quando ``return_meta=False`` (padrao): lista de ck subgrafos
        {C1, C2, ..., Cck}, cada um correspondendo a uma Local Structure
        LSi com as inter-arestas removidas. Os subgrafos sao copias
        independentes (``copy()``), nao views do grafo original.
    tuple[list[nx.Graph], dict]
        Quando ``return_meta=True``: a lista acima e o ``meta`` retornado
        por ``partition_graph`` (ver chaves em ``_partition_backend``;
        ``meta["backend_used"]`` registra o motor efetivo para o log
        estruturado do experimento).

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
    node_sets, meta = partition_graph(g, ck, seed=seed, backend=backend)

    local_structures: list[nx.Graph] = []
    for node_set in node_sets:
        # subgraph() retorna apenas arestas cujos dois extremos estao em node_set,
        # excluindo automaticamente inter-arestas (Secao 3.1, passo 1.4).
        ls = g.subgraph(node_set).copy()
        local_structures.append(ls)

    if return_meta:
        return local_structures, meta
    return local_structures


def _group_isomorphic(
    local_structures: list[nx.Graph],
    k: int,
    sigma: float,
    seed: int,
    fsm_max_size: int = 4,
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
    fsm_max_size : int
        Tamanho maximo (em nos) dos subgrafos enumerados pelo FSM
        simplificado (D-01). Propagado a ``_group_within_bucket``. Lido da
        chave YAML ``anonymization.s_max`` (alias ``fsm_max_size``) pelo
        runner; default 4. Ver docs/algorithm_notes.md §5.1 (B5).

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
    if k < 1:
        raise ValueError(f"k must be >= 1, got {k!r}")

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
        bucket_groups = _group_within_bucket(bucket_ls, k, sigma, rng, fsm_max_size=fsm_max_size)
        all_groups.extend(bucket_groups)

    return all_groups


def _modify_structure(
    groups: list[list[nx.Graph]],
    seed: int,
    add_only: bool = False,
    return_counts: bool = False,
) -> list[list[nx.Graph]] | tuple[list[list[nx.Graph]], int]:
    """Torna isomorfas as Local Structures de cada grupo (Fases 1 e 2).

    Implementa a anonimizacao intra-grupo em duas fases:

    Phase 1 -- Numeracao de nos (node matching):
        Atribui uma posicao canonica (0-indexed) a cada no em cada LS
        do grupo, ordenando por (grau descendente, id do no ascendente)
        conforme D-03.  Essa numeracao define a correspondencia entre
        nos de LSs distintas: a posicao i da LS_a corresponde a posicao
        i da LS_b, independentemente dos ids reais dos nos.

    Phase 2 -- Modificacao de arestas:
        Para cada par de posicoes (i, j) com i < j, verifica em quantas
        LSs existe a aresta entre os nos nessas posicoes.
        * add_only=False (padrao, Edge Adding/Deleting):
            se count_com_aresta >= count_sem_aresta, adiciona a aresta
            em todas as LSs que nao a tem; caso contrario, remove das
            que a tem.  Minimiza o numero total de modificacoes por par
            (greedy local, conforme descricao do artigo p. 651).
        * add_only=True (Edge Adding only):
            se pelo menos uma LS tem a aresta, adiciona-a a todas.

    Parametros
    ----------
    groups : list[list[nx.Graph]]
        Grupos de Local Structures retornados por _group_isomorphic.
        Todos os grupos completos devem ter LSs com o mesmo numero de
        nos (D-07 Opcao A, garantido por _group_isomorphic).  Grupos
        com um unico membro (D-06) sao passados sem modificacao.
    seed : int
        Semente aleatoria aceita para consistencia de API; reservada
        para desempate em extensoes futuras.  Nao ha escolhas
        aleatorias na implementacao atual de Phase 1 e Phase 2.
    add_only : bool, optional
        Se True, aplica apenas adicao de arestas (Edge Adding).
        Se False, aplica adicao e remocao (Edge Adding/Deleting),
        que gera menor perturbacao estrutural. Padrao: False.
    return_counts : bool, optional
        Se ``True``, retorna tambem o numero total de operacoes de aresta
        (adicoes + remocoes) aplicadas na Fase 2 sobre todos os grupos
        completos -- o contador ``edges_modified_phase2_intragroup``
        exposto por ``anonymize`` (G5-a, issue #80). Padrao: ``False``
        (mantem a assinatura historica que retorna apenas a lista).

    Retorna
    -------
    list[list[nx.Graph]]
        Quando ``return_counts=False`` (padrao): grupos com Local
        Structures modificadas e isomorfas entre si, prontas para
        reconexao.  Grupos incompletos (D-06) sao retornados sem
        modificacao.
    tuple[list[list[nx.Graph]], int]
        Quando ``return_counts=True``: a lista acima e o total de arestas
        adicionadas/removidas pela isomorfizacao intra-grupo (Fase 2).
        Cada adicao ou remocao efetiva conta como uma modificacao;
        grupos incompletos e de tamanho misto nao contribuem.

    Notas
    -----
    * A funcao **nao modifica** os grafos de entrada; trabalha sobre
      copias independentes.
    * A correspondencia de nos e puramente posicional (D-03); nao
      depende da existencia de um subgrafo comum calculado por FSM.
    * Grupos de tamanhos mistos (violacao de D-07) sao passados sem
      modificacao para nao propagar erros silenciosos.
    * Arestas self-loop nunca sao adicionadas (posicoes distintas
      implicam nos distintos dentro de cada LS).

    Referencia
    ----------
    He et al. (2009), Secao 3.2 -- Local Structures Grouping and
    Anonymization, Phase 1 (p. 651) e Phase 2 (p. 652).
    D-03 em docs/algorithm_notes.md §7.
    """
    _rng = np.random.default_rng(seed)  # reserved for future tie-break use

    result_groups: list[list[nx.Graph]] = []
    edges_modified = 0  # G5-a: Phase 2 add/remove operations across complete groups

    for group in groups:
        # Grupos com menos de 2 LSs nao precisam de isomorfizacao (D-06).
        if len(group) < 2:
            result_groups.append([ls.copy() for ls in group])
            continue

        # Verificar homogeneidade de tamanho (D-07 Opcao A).
        # Se violada, passar sem modificacao para nao mascarar erros.
        sizes = {ls.number_of_nodes() for ls in group}
        if len(sizes) > 1:
            result_groups.append([ls.copy() for ls in group])
            continue

        # Trabalhar sobre copias independentes.
        modified: list[nx.Graph] = [ls.copy() for ls in group]
        n_nodes = modified[0].number_of_nodes()

        if n_nodes == 0:
            result_groups.append(modified)
            continue

        # ------------------------------------------------------------------
        # Phase 1 -- Canonical node ordering per LS (D-03)
        # Sort nodes by (-degree, node_id); assign position 0..n_nodes-1.
        # inv_maps[ls_idx][pos] -> node_id in modified[ls_idx]
        # ------------------------------------------------------------------
        inv_maps: list[dict[int, object]] = []
        for ls in modified:
            sorted_nodes = sorted(ls.nodes(), key=lambda v: (-ls.degree(v), v))
            inv_maps.append(dict(enumerate(sorted_nodes)))

        # ------------------------------------------------------------------
        # Phase 2 -- Make isomorphic (greedy per pair, He et al. p. 651)
        # ------------------------------------------------------------------
        k_size = len(modified)
        for pos_i in range(n_nodes):
            for pos_j in range(pos_i + 1, n_nodes):
                # Check edge existence at this position pair in every LS.
                has_edge = [
                    modified[ls_idx].has_edge(
                        inv_maps[ls_idx][pos_i],
                        inv_maps[ls_idx][pos_j],
                    )
                    for ls_idx in range(k_size)
                ]
                count_with = sum(has_edge)
                count_without = k_size - count_with

                if add_only:
                    # Edge Adding only: if any LS has the edge, add to all.
                    if count_with > 0:
                        for ls_idx in range(k_size):
                            if not has_edge[ls_idx]:
                                u = inv_maps[ls_idx][pos_i]
                                v = inv_maps[ls_idx][pos_j]
                                modified[ls_idx].add_edge(u, v)
                                edges_modified += 1
                else:
                    # Edge Adding/Deleting: majority-vote per pair.
                    if count_with >= count_without:
                        # Add to all LSs that lack the edge.
                        for ls_idx in range(k_size):
                            if not has_edge[ls_idx]:
                                u = inv_maps[ls_idx][pos_i]
                                v = inv_maps[ls_idx][pos_j]
                                modified[ls_idx].add_edge(u, v)
                                edges_modified += 1
                    else:
                        # Remove from all LSs that have the edge.
                        for ls_idx in range(k_size):
                            if has_edge[ls_idx]:
                                u = inv_maps[ls_idx][pos_i]
                                v = inv_maps[ls_idx][pos_j]
                                modified[ls_idx].remove_edge(u, v)
                                edges_modified += 1

        result_groups.append(modified)

    if return_counts:
        return result_groups, edges_modified
    return result_groups


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
        structure-aware k-anonimato. O atributo
        ``g_prime.graph["metadata"]["edges_added_reconnection"]`` registra
        o numero de arestas efetivamente adicionadas nesta etapa de
        reconexao (G5-a, issue #80) -- novas arestas apenas, exclui as
        intra-LS ja presentes na uniao das LSs modificadas.

    Notas
    -----
    **Contagem k(k-1) (G3, issue #80).** Para uma inter-aresta de mesmo
    grupo cujos extremos ocupam **posicoes canonicas distintas** (D-03) em
    suas LSs, a reconexao adiciona exatamente ``k(k-1)`` arestas novas
    (verificado empiricamente para k in {2,3}). Quando os extremos
    compartilham a mesma posicao canonica, os pares ordenados (i, j)
    colapsam e a construcao forma um clique de ``C(k,2)=k(k-1)/2`` arestas
    entre os nos daquela posicao (no caso degenerate de LSs de 1 no, isso
    se reduz a propria inter-aresta original). Ver nota sob D-08 em
    ``docs/decision_log.md``.

    Referencia
    ----------
    He et al. (2009), Secao 3.3 -- Reconnecting Local Structures (p. 652).
    Para cada inter-aresta reconectada (extremos em posicoes distintas):
    k(k-1) arestas adicionadas.
    """
    # ------------------------------------------------------------------
    # Build lookup: node_id → (group_idx, ls_idx)
    # ------------------------------------------------------------------
    node_location: dict[object, tuple[int, int]] = {}
    for g_idx, group in enumerate(groups):
        for ls_idx, ls in enumerate(group):
            for node in ls.nodes():
                node_location[node] = (g_idx, ls_idx)

    # ------------------------------------------------------------------
    # Build position maps for each LS using the same D-03 ordering as
    # _modify_structure: sort by (-degree, node_id) on the modified LS.
    #
    # inv_maps[g_idx][ls_idx][pos] -> node_id
    # pos_maps[g_idx][ls_idx][node_id] -> pos
    # ------------------------------------------------------------------
    inv_maps: list[list[dict[int, object]]] = []
    pos_maps: list[list[dict[object, int]]] = []
    for group in groups:
        grp_inv: list[dict[int, object]] = []
        grp_pos: list[dict[object, int]] = []
        for ls in group:
            sorted_nodes = sorted(ls.nodes(), key=lambda v: (-ls.degree(v), v))
            inv = dict(enumerate(sorted_nodes))
            pos = {v: p for p, v in inv.items()}
            grp_inv.append(inv)
            grp_pos.append(pos)
        inv_maps.append(grp_inv)
        pos_maps.append(grp_pos)

    # ------------------------------------------------------------------
    # Build G_prime = union of all modified Local Structures.
    # At this point G_prime contains all n nodes and the intra-LS edges.
    # ------------------------------------------------------------------
    g_prime = nx.Graph()
    for group in groups:
        for ls in group:
            g_prime.add_nodes_from(ls.nodes())
            g_prime.add_edges_from(ls.edges())

    # ------------------------------------------------------------------
    # Reconnect inter-partition edges (Section 3.3).
    #
    # For each edge (u, v) in g_original:
    #   * Intra-LS edge: both endpoints in the same LS → already in
    #     g_prime via the union above; skip.
    #   * Same-group inter-LS edge: endpoints in DIFFERENT LSs of the
    #     SAME group → add the k(k-1) cross-LS position pairs (i≠j)
    #     to preserve the isomorphism inside the group (He et al. p.652).
    #   * Cross-group inter-LS edge: endpoints in DIFFERENT groups →
    #     add back the original edge only (isomorphism across groups is
    #     not enforced by the He et al. algorithm).
    # ------------------------------------------------------------------
    edges_added_reconnection = 0  # G5-a: new edges introduced by reconnection only

    def _add_reconnection_edge(a: object, b: object) -> None:
        """Add edge (a, b) to g_prime, counting it only if it is new."""
        nonlocal edges_added_reconnection
        if not g_prime.has_edge(a, b):
            g_prime.add_edge(a, b)
            edges_added_reconnection += 1

    for u, v in g_original.edges():
        u_loc = node_location.get(u)
        v_loc = node_location.get(v)
        if u_loc is None or v_loc is None:
            # Node absent from all LSs — should not happen for valid input.
            _add_reconnection_edge(u, v)
            continue

        u_g, u_l = u_loc
        v_g, v_l = v_loc

        if u_g == v_g and u_l == v_l:
            # Intra-LS edge: already present in g_prime; nothing to do.
            continue

        if u_g == v_g:
            # Same-group inter-LS edge: add all k(k-1) cross-LS pairs.
            k_size = len(groups[u_g])
            u_pos = pos_maps[u_g][u_l][u]
            v_pos = pos_maps[v_g][v_l][v]
            for i in range(k_size):
                for j in range(k_size):
                    if i == j:
                        continue  # skip intra-LS pairs
                    node_u = inv_maps[u_g][i][u_pos]  # u-equivalent in LS_i
                    node_v = inv_maps[v_g][j][v_pos]  # v-equivalent in LS_j
                    if node_u != node_v:
                        _add_reconnection_edge(node_u, node_v)
        else:
            # Cross-group inter-LS edge: restore original edge.
            _add_reconnection_edge(u, v)

    g_prime.graph["metadata"] = {"edges_added_reconnection": edges_added_reconnection}

    return g_prime
