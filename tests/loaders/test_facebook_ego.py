"""Tests for src/loaders/facebook_ego.py.

Raw data (data/raw/facebook/) is not versioned, so all tests use a synthetic
fixture (tmp_path + _make_ego_dir) that replicates the SNAP .edges format.
This avoids a download dependency in CI while still exercising the real parser.
"""

from pathlib import Path

import networkx as nx
import pytest

from src.loaders.facebook_ego import load_facebook_egonet


def _make_ego_dir(root: Path, egonet_id: int, edges: list[tuple[int, int]]) -> None:
    ego_dir = root / str(egonet_id)
    ego_dir.mkdir(parents=True)
    lines = "\n".join(f"{u} {v}" for u, v in edges)
    (ego_dir / f"{egonet_id}.edges").write_text(lines)


class TestLoadFacebookEgonet:
    def test_returns_undirected_graph(self, tmp_path: Path) -> None:
        _make_ego_dir(tmp_path, 0, [(1, 2), (2, 3)])
        graph = load_facebook_egonet(0, tmp_path)
        assert isinstance(graph, nx.Graph)
        assert not graph.is_directed()

    def test_correct_edges(self, tmp_path: Path) -> None:
        _make_ego_dir(tmp_path, 107, [(10, 20), (20, 30), (10, 30)])
        graph = load_facebook_egonet(107, tmp_path)
        assert graph.number_of_nodes() == 3
        assert graph.number_of_edges() == 3
        assert graph.has_edge(10, 20)

    def test_node_labels_are_integers(self, tmp_path: Path) -> None:
        _make_ego_dir(tmp_path, 0, [(1, 2)])
        graph = load_facebook_egonet(0, tmp_path)
        assert all(isinstance(n, int) for n in graph.nodes())

    def test_missing_egonet_raises(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError, match="999"):
            load_facebook_egonet(999, tmp_path)

    def test_empty_edge_list(self, tmp_path: Path) -> None:
        _make_ego_dir(tmp_path, 0, [])
        graph = load_facebook_egonet(0, tmp_path)
        assert graph.number_of_edges() == 0
