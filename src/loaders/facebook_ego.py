"""Load a Facebook ego-network from SNAP files as an undirected NetworkX graph."""

from pathlib import Path

import networkx as nx


def load_facebook_egonet(egonet_id: int, data_dir: Path) -> nx.Graph:
    """Load a Facebook ego-network as an undirected graph.

    Parameters
    ----------
    egonet_id:
        Integer identifier of the ego-node (e.g. 0, 107, 1684).
    data_dir:
        Root directory produced by the download script, containing one
        subdirectory per ego-node (``data_dir/<egonet_id>/``).

    Returns
    -------
    nx.Graph
        Undirected graph built from the ``.edges`` file.  Node labels are
        integers as read from the file.

    Raises
    ------
    FileNotFoundError
        If ``data_dir/<egonet_id>/<egonet_id>.edges`` does not exist.
    """
    edges_file = data_dir / str(egonet_id) / f"{egonet_id}.edges"
    if not edges_file.exists():
        raise FileNotFoundError(f"Edge list not found: {edges_file}")

    return nx.read_edgelist(str(edges_file), nodetype=int, create_using=nx.Graph())
