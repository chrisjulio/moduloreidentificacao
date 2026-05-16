"""Test fixtures shared across the suite."""

from __future__ import annotations

import networkx as nx
import pytest


@pytest.fixture
def small_graph() -> nx.Graph:
    """Petersen graph: small, well-known, 10 nodes and 15 edges, 3-regular."""
    return nx.petersen_graph()


@pytest.fixture
def path_graph() -> nx.Graph:
    """Path of 5 nodes — minimal graph with non-uniform degree distribution."""
    return nx.path_graph(5)


@pytest.fixture
def regular_graph() -> nx.Graph:
    """k-regular graph where all nodes share the same local degree (3-regular, 10 nodes)."""
    return nx.random_regular_graph(d=3, n=10, seed=0)


@pytest.fixture
def disconnected_graph() -> nx.Graph:
    """Disjoint union of two small graphs — exercises the disconnected case."""
    g = nx.disjoint_union(nx.cycle_graph(4), nx.complete_graph(3))
    return g
