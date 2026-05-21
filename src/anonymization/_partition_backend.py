"""Backend de particionamento de grafos para o anonimizador He et al. (2009).

Abstrai a lógica de particionamento com dois backends e fallback automático,
conforme D-04 revisado (20/05/2026) registrado em docs/algorithm_notes.md §7.

Decisões arquiteturais:
    D-04 — Motor primário: pymetis (multilevel k-way); fallback: networkx KL.
    D-07 — Opção A: tamanhos reais de cada partição reportados via ``meta["sizes"]``
            para que o agrupamento (#12) indexe LSs pelo tamanho e forme grupos
            apenas entre LSs com mesmo número de nós.

Referência
----------
He et al. (2009), Seção 3.1 — Graph Partition.
Karypis & Kumar [14] — algoritmo multilevel k-way (referência do artigo).
"""

from __future__ import annotations

import warnings

import networkx as nx

# ---------------------------------------------------------------------------
# Detecção de pymetis no momento do import
# ---------------------------------------------------------------------------
try:
    import pymetis  # type: ignore[import-untyped]  # noqa: F401

    _PYMETIS_AVAILABLE = True
except ImportError:
    _PYMETIS_AVAILABLE = False


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------


def partition_graph(
    g: nx.Graph,
    ck: int,
    seed: int,
    backend: str = "auto",
) -> tuple[list[set[int]], dict]:
    """Particiona *g* em *ck* subconjuntos minimizando inter-arestas.

    Parameters
    ----------
    g:
        Grafo não-direcionado a ser particionado.
    ck:
        Número de partições desejadas (``floor(n / d)``).
    seed:
        Semente aleatória para reprodutibilidade. Usada pelo backend KL;
        ignorada pelo pymetis (algoritmo determinístico dado o grafo).
    backend:
        ``"auto"``        — usa pymetis se disponível; caso contrário, KL
                            com ``UserWarning`` descrevendo a divergência.
        ``"pymetis"``     — força pymetis; levanta ``ImportError`` se ausente.
        ``"networkx-kl"`` — força Kernighan-Lin bissecção recursiva.

    Returns
    -------
    partitions:
        Lista de *ck* conjuntos de IDs de nós (disjuntos, cobrindo V).
    meta:
        Metadados de execução para log estruturado::

            {
              "backend_used":       "pymetis" | "networkx-kl",
              "ck":                 int,          # partições solicitadas
              "sizes":              list[int],    # tamanho real de cada partição
              "inter_edges_removed": int,         # arestas entre partições distintas
              "d_requested":        int,          # tamanho alvo = n // ck
              "d_actual_min":       int,
              "d_actual_max":       int,
            }

        ``meta["sizes"]`` é a entrada para a política D-07 Opção A:
        ``_group_isomorphic`` (#12) deve indexar LSs por tamanho e só
        agrupar LSs com o mesmo número de nós.

    Raises
    ------
    ImportError
        Se ``backend="pymetis"`` e pymetis não estiver instalado.
    ValueError
        Se *backend* não for um dos valores reconhecidos, ou se *ck* < 1.

    Notes
    -----
    D-04 (revisado 20/05/2026): o motor primário é ``pymetis`` (multilevel
    k-way, Karypis & Kumar [14]), fiel ao algoritmo de referência do artigo.
    O fallback KL é heurística aparentada mas distinta: bisseção recursiva,
    ``O(|E| · log |V|)`` vs ``O(|E|)`` do METIS; qualidade de partição e
    tamanhos das LSs podem divergir.  Reportar como parâmetro metodológico.

    D-07 (20/05/2026, Opção A): partições aproximadamente balanceadas são
    retornadas sem modificação; ``meta["sizes"]`` documenta o desbalanceamento
    para rastreabilidade.  A restrição de grupos a LSs do mesmo tamanho é
    responsabilidade de ``_group_isomorphic`` (#12), que consulta
    ``meta["sizes"]``.

    **Limitação do backend ``"networkx-kl"`` — partições não balanceadas:**
    A bissecção recursiva de Kernighan-Lin **NÃO garante partições de tamanho
    exatamente ``d = n // ck``** para ``ck > 2``. O backend garante apenas
    (a) o número de partições solicitado (``ck``) e (b) cobertura total dos
    nós (toda partição não-vazia). Tamanho exato por partição é propriedade
    exclusiva do backend ``"pymetis"`` — ver testes em
    ``tests/anonymization/test_partition_backend.py``.

    Implicação direta para k-anonimato: uma partição produzida pelo backend
    KL pode ter tamanho menor que ``d``, o que significa que o k-anonimato
    pretendido **pode não ser atingido** por esse backend. Por isso, a
    validação de sanidade da Seção 7 de ``docs/algorithm_notes.md``
    (marco 29/05/2026) **deve preferencialmente ser executada com**
    ``backend="pymetis"``; se executada com ``backend="networkx-kl"``,
    grupos com menos nós que ``d`` confirmam a limitação conhecida e não
    devem ser interpretados como falha do algoritmo — ver D-07 em
    ``docs/algorithm_notes.md`` §7.
    """
    if ck < 1:
        raise ValueError(f"ck deve ser >= 1; recebido: {ck}")
    if backend not in {"auto", "pymetis", "networkx-kl"}:
        raise ValueError(
            f"backend deve ser 'auto', 'pymetis' ou 'networkx-kl'; recebido: {backend!r}"
        )

    n = g.number_of_nodes()
    d_requested = n // ck if ck > 0 else n

    # ------------------------------------------------------------------
    # Selecionar e executar backend
    # ------------------------------------------------------------------
    backend_used: str
    partitions: list[set[int]]

    if backend == "pymetis":
        if not _PYMETIS_AVAILABLE:
            raise ImportError(
                "backend='pymetis' solicitado, mas pymetis não está instalado. "
                "No Windows, instale via conda: `conda install -c conda-forge pymetis`. "
                "No Linux/macOS: `pip install pymetis`. "
                "Alternativamente, use backend='networkx-kl' ou backend='auto'."
            )
        partitions = _partition_pymetis(g, ck)
        backend_used = "pymetis"

    elif backend == "networkx-kl":
        partitions = _partition_kl(g, ck, seed)
        backend_used = "networkx-kl"

    else:  # backend == "auto"
        if _PYMETIS_AVAILABLE:
            partitions = _partition_pymetis(g, ck)
            backend_used = "pymetis"
        else:
            warnings.warn(
                "pymetis não está disponível — usando fallback networkx KL "
                "(kernighan_lin_bisection recursivo). "
                "Implicação metodológica: o fallback KL é uma heurística de "
                "bissecção recursiva distinta do multilevel k-way (Karypis & Kumar [14]) "
                "referenciado em He et al. (2009). Qualidade de partição e tamanhos "
                "das LSs podem divergir do algoritmo de referência. "
                "Reportar como limitação metodológica. "
                "Decisão arquitetural: D-04 revisado (20/05/2026) em "
                "docs/algorithm_notes.md §7.",
                UserWarning,
                stacklevel=2,
            )
            partitions = _partition_kl(g, ck, seed)
            backend_used = "networkx-kl"

    # ------------------------------------------------------------------
    # Calcular metadados (D-07: sizes para indexação por tamanho)
    # ------------------------------------------------------------------
    sizes = [len(p) for p in partitions]
    inter_edges_removed = _count_inter_edges(g, partitions)

    meta: dict = {
        "backend_used": backend_used,
        "ck": ck,
        "sizes": sizes,
        "inter_edges_removed": inter_edges_removed,
        "d_requested": d_requested,
        "d_actual_min": min(sizes) if sizes else 0,
        "d_actual_max": max(sizes) if sizes else 0,
    }

    return partitions, meta


# ---------------------------------------------------------------------------
# Backends internos
# ---------------------------------------------------------------------------


def _partition_pymetis(g: nx.Graph, ck: int) -> list[set[int]]:
    """Particiona *g* via pymetis (multilevel k-way, Karypis & Kumar [14]).

    Parameters
    ----------
    g:
        Grafo não-direcionado.
    ck:
        Número de partições.

    Returns
    -------
    list[set[int]]
        Lista de *ck* conjuntos de IDs de nós.
    """
    import pymetis  # type: ignore[import-untyped]

    nodes = list(g.nodes())
    node_to_idx: dict = {node: idx for idx, node in enumerate(nodes)}

    # Formato de adjacência CSR esperado por pymetis: lista de listas de vizinhos
    adjacency = [[node_to_idx[v] for v in g.neighbors(u)] for u in nodes]

    _, membership = pymetis.part_graph(ck, adjacency=adjacency)

    partitions: list[set[int]] = [set() for _ in range(ck)]
    for idx, part_id in enumerate(membership):
        partitions[part_id].add(nodes[idx])

    return partitions


def _partition_kl(g: nx.Graph, ck: int, seed: int) -> list[set[int]]:
    """Particiona *g* via Kernighan-Lin bissecção recursiva (fallback D-04).

    Aplica ``nx.community.kernighan_lin_bisection`` recursivamente,
    dividindo a maior partição a cada passo até atingir *ck* partições.

    Parameters
    ----------
    g:
        Grafo não-direcionado.
    ck:
        Número de partições desejadas.
    seed:
        Semente para reprodutibilidade; passada em cada chamada de KL.

    Returns
    -------
    list[set[int]]
        Lista de *ck* conjuntos de IDs de nós.
    """
    if ck == 1:
        return [set(g.nodes())]

    # Bissecção inicial
    bisection = nx.community.kernighan_lin_bisection(g, seed=seed)
    partitions: list[set[int]] = [set(part) for part in bisection]

    # Bissecções adicionais até atingir ck partições
    while len(partitions) < ck:
        # Divide a maior partição
        largest_idx = max(range(len(partitions)), key=lambda i: len(partitions[i]))
        largest = partitions[largest_idx]

        subgraph = g.subgraph(largest)

        if subgraph.number_of_nodes() < 2:
            # Subgrafo muito pequeno para bipartir — parar recursão
            break

        sub_bisection = nx.community.kernighan_lin_bisection(subgraph, seed=seed)
        sub_parts = [set(part) for part in sub_bisection]

        partitions.pop(largest_idx)
        partitions.extend(sub_parts)

    return partitions


# ---------------------------------------------------------------------------
# Utilitário interno
# ---------------------------------------------------------------------------


def _count_inter_edges(g: nx.Graph, partitions: list[set[int]]) -> int:
    """Conta arestas de *g* que cruzam fronteiras de partição.

    Parameters
    ----------
    g:
        Grafo original (antes da remoção de inter-arestas).
    partitions:
        Lista de conjuntos de nós definindo as partições.

    Returns
    -------
    int
        Número de arestas com extremidades em partições distintas.
    """
    # Mapa nó → índice de partição para lookup O(1)
    node_to_part: dict = {}
    for part_idx, part in enumerate(partitions):
        for node in part:
            node_to_part[node] = part_idx

    count = 0
    for u, v in g.edges():
        if node_to_part.get(u) != node_to_part.get(v):
            count += 1
    return count
