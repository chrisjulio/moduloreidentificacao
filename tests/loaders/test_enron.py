"""Tests for src/loaders/enron.py.

Raw data (data/raw/enron/) is not versioned, so all tests use a synthetic
fixture (tmp_path + _write_edge_list) that replicates the SNAP edge-list format.
This avoids a download dependency in CI while still exercising the real parser
and the OR symmetrization decided in D-11.
"""

from pathlib import Path

import networkx as nx
import pytest

from src.loaders.enron import load_enron

_EDGE_LIST_NAME = "email-Enron.txt"


def _write_edge_list(root: Path, lines: list[str]) -> None:
    """Write *lines* as data_dir/email-Enron.txt (one directed edge per line)."""
    (root / _EDGE_LIST_NAME).write_text("\n".join(lines) + "\n")


class TestLoadEnron:
    def test_returns_undirected_graph(self, tmp_path: Path) -> None:
        _write_edge_list(tmp_path, ["1 2", "2 3"])
        graph = load_enron(tmp_path)
        assert isinstance(graph, nx.Graph)
        assert not graph.is_directed()

    def test_node_labels_are_integers(self, tmp_path: Path) -> None:
        _write_edge_list(tmp_path, ["1 2"])
        graph = load_enron(tmp_path)
        assert all(isinstance(n, int) for n in graph.nodes())

    def test_or_symmetrization_reciprocal_pair(self, tmp_path: Path) -> None:
        """A reciprocal pair (1->2 and 2->1) collapses to a single edge (D-11)."""
        _write_edge_list(tmp_path, ["1 2", "2 1"])
        graph = load_enron(tmp_path)
        assert graph.number_of_edges() == 1
        assert graph.has_edge(1, 2)

    def test_or_symmetrization_one_way_pair(self, tmp_path: Path) -> None:
        """A one-way edge (1->2) becomes a single undirected edge (D-11)."""
        _write_edge_list(tmp_path, ["1 2"])
        graph = load_enron(tmp_path)
        assert graph.number_of_edges() == 1
        assert graph.has_edge(1, 2)

    def test_comments_are_ignored(self, tmp_path: Path) -> None:
        """Lines starting with '#' (SNAP header) are skipped by read_edgelist."""
        _write_edge_list(
            tmp_path,
            ["# Directed graph: email-Enron.txt", "# Nodes: ... Edges: ...", "1 2"],
        )
        graph = load_enron(tmp_path)
        assert graph.number_of_nodes() == 2
        assert graph.number_of_edges() == 1

    def test_missing_file_raises(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError, match=_EDGE_LIST_NAME):
            load_enron(tmp_path)
