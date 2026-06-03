"""Load the Email-Enron network from a SNAP edge list as an undirected graph.

The Email-Enron network is directed by nature (``A -> B`` means "A sent email to
B"), whereas the rest of the pipeline operates on undirected graphs. This loader
flattens the direction by **simple (OR) symmetrization**: an undirected edge
``A -- B`` exists whenever there is email in *either* direction. See decision
``D-11`` in ``docs/decision_log.md``.
"""

from pathlib import Path

import networkx as nx

# Name of the decompressed edge list produced by src.loaders.download_enron.
_EDGE_LIST_NAME = "email-Enron.txt"


def load_enron(data_dir: Path) -> nx.Graph:
    """Load the Email-Enron network as an undirected graph.

    The raw SNAP edge list is read as a directed graph and projected to an
    undirected graph by **simple (OR) symmetrization**: the undirected edge
    ``{u, v}`` is created whenever there is a directed edge ``u -> v`` *or*
    ``v -> u``. Reciprocal pairs and one-way pairs alike collapse to a single
    undirected edge; self-loops and multi-edges are collapsed. This is the
    SNAP convention and the decision recorded as ``D-11`` in
    ``docs/decision_log.md``.

    Parameters
    ----------
    data_dir:
        Directory containing the decompressed edge list
        (``data_dir/email-Enron.txt``), as produced by
        :func:`src.loaders.download_enron.download_enron`.

    Returns
    -------
    nx.Graph
        Undirected graph built from the edge list. Node labels are integers as
        read from the file. The contract matches
        :func:`src.loaders.facebook_ego.load_facebook_egonet`: a plain
        ``nx.Graph`` ready for the runner (LCC / ``min_nodes`` pre-processing is
        the runner's responsibility, not this loader's).

    Raises
    ------
    FileNotFoundError
        If ``data_dir/email-Enron.txt`` does not exist.
    """
    edges_file = data_dir / _EDGE_LIST_NAME
    if not edges_file.exists():
        raise FileNotFoundError(f"Edge list not found: {edges_file}")

    directed = nx.read_edgelist(str(edges_file), nodetype=int, create_using=nx.DiGraph())
    # OR symmetrization (D-11): to_undirected() keeps {u, v} if either direction
    # is present, collapsing reciprocal and one-way pairs to a single edge.
    return directed.to_undirected()
