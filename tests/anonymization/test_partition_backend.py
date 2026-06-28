"""Testes unitários para src/anonymization/_partition_backend.py.

Cobertura:
    - backend="networkx-kl": grafo Petersen (n=10, ck=2 e ck=5)
    - Invariante: partições disjuntas e cobrindo todos os nós
    - backend="auto" sem pymetis: emite UserWarning e usa KL
    - backend="pymetis" sem pymetis: levanta ImportError
    - meta["backend_used"] reflete o backend efetivamente usado
    - meta["sizes"] soma n total de nós
    - Determinismo: mesma seed → mesma partição (backend KL)

Seeds fixadas em testes são exceção controlada conforme docs/regras_sementes.md:
reprodutibilidade dos testes requer valores determinísticos.
"""

from __future__ import annotations

from unittest.mock import patch

import networkx as nx
import pytest

from src.anonymization._partition_backend import partition_graph, pymetis_available

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def petersen() -> nx.Graph:
    """Grafo de Petersen: 10 nós, 3-regular, conexo."""
    return nx.petersen_graph()


# ---------------------------------------------------------------------------
# Testes: backend networkx-kl
# ---------------------------------------------------------------------------


class TestNetworkxKL:
    """Testes do backend Kernighan-Lin sem dependência de pymetis."""

    def test_ck2_returns_two_partitions(self, petersen: nx.Graph) -> None:
        """ck=2 deve retornar exatamente 2 partições."""
        partitions, meta = partition_graph(petersen, ck=2, seed=0, backend="networkx-kl")
        assert len(partitions) == 2
        assert meta["ck"] == 2

    def test_ck5_returns_five_partitions(self, petersen: nx.Graph) -> None:
        """ck=5 deve retornar exatamente 5 partições."""
        partitions, meta = partition_graph(petersen, ck=5, seed=0, backend="networkx-kl")
        assert len(partitions) == 5
        assert meta["ck"] == 5

    def test_partitions_are_disjoint(self, petersen: nx.Graph) -> None:
        """Nenhum nó deve aparecer em mais de uma partição."""
        partitions, _ = partition_graph(petersen, ck=2, seed=0, backend="networkx-kl")
        seen: set = set()
        for part in partitions:
            assert part.isdisjoint(seen), "Partições se sobrepõem"
            seen |= part

    def test_partitions_cover_all_nodes(self, petersen: nx.Graph) -> None:
        """A união das partições deve cobrir exatamente V(G)."""
        partitions, _ = partition_graph(petersen, ck=2, seed=0, backend="networkx-kl")
        all_nodes = set(petersen.nodes())
        covered: set = set()
        for part in partitions:
            covered |= part
        assert covered == all_nodes

    def test_ck5_partitions_cover_all_nodes(self, petersen: nx.Graph) -> None:
        """ck=5 — a união deve cobrir todos os nós do grafo de Petersen."""
        partitions, _ = partition_graph(petersen, ck=5, seed=0, backend="networkx-kl")
        all_nodes = set(petersen.nodes())
        covered: set = set()
        for part in partitions:
            covered |= part
        assert covered == all_nodes

    def test_backend_used_is_kl(self, petersen: nx.Graph) -> None:
        """meta['backend_used'] deve ser 'networkx-kl'."""
        _, meta = partition_graph(petersen, ck=2, seed=0, backend="networkx-kl")
        assert meta["backend_used"] == "networkx-kl"

    def test_meta_sizes_sum_to_n(self, petersen: nx.Graph) -> None:
        """meta['sizes'] deve somar o número total de nós."""
        _, meta = partition_graph(petersen, ck=5, seed=0, backend="networkx-kl")
        assert sum(meta["sizes"]) == petersen.number_of_nodes()

    def test_meta_sizes_len_matches_ck(self, petersen: nx.Graph) -> None:
        """meta['sizes'] deve ter exatamente ck entradas."""
        _, meta = partition_graph(petersen, ck=5, seed=0, backend="networkx-kl")
        assert len(meta["sizes"]) == 5

    def test_meta_d_requested(self, petersen: nx.Graph) -> None:
        """meta['d_requested'] deve ser n // ck."""
        n = petersen.number_of_nodes()  # 10
        ck = 5
        _, meta = partition_graph(petersen, ck=ck, seed=0, backend="networkx-kl")
        assert meta["d_requested"] == n // ck

    def test_meta_d_actual_min_max_consistent(self, petersen: nx.Graph) -> None:
        """d_actual_min <= d_actual_max e ambos consistentes com sizes."""
        _, meta = partition_graph(petersen, ck=5, seed=0, backend="networkx-kl")
        assert meta["d_actual_min"] == min(meta["sizes"])
        assert meta["d_actual_max"] == max(meta["sizes"])
        assert meta["d_actual_min"] <= meta["d_actual_max"]

    def test_meta_inter_edges_removed_non_negative(self, petersen: nx.Graph) -> None:
        """inter_edges_removed deve ser inteiro não-negativo <= |E|."""
        _, meta = partition_graph(petersen, ck=2, seed=0, backend="networkx-kl")
        assert isinstance(meta["inter_edges_removed"], int)
        assert 0 <= meta["inter_edges_removed"] <= petersen.number_of_edges()

    def test_determinism_same_seed(self, petersen: nx.Graph) -> None:
        """Mesma seed deve produzir a mesma partição no backend KL."""
        partitions_a, _ = partition_graph(petersen, ck=2, seed=42, backend="networkx-kl")
        partitions_b, _ = partition_graph(petersen, ck=2, seed=42, backend="networkx-kl")
        # Compara conjuntos (independente de ordem na lista)
        assert sorted([frozenset(p) for p in partitions_a]) == sorted(
            [frozenset(p) for p in partitions_b]
        )

    def test_different_seeds_may_differ(self, petersen: nx.Graph) -> None:
        """Seeds diferentes devem ter chance de produzir partições distintas.

        Não é garantido (KL pode convergir à mesma solução), mas serve como
        fumaça para confirmar que a seed está sendo passada.
        """
        partitions_0, _ = partition_graph(petersen, ck=2, seed=0, backend="networkx-kl")
        partitions_99, _ = partition_graph(petersen, ck=2, seed=99, backend="networkx-kl")
        # Ambas devem ser válidas (cobertura total), independentemente de serem iguais
        all_nodes = set(petersen.nodes())
        assert set().union(*partitions_0) == all_nodes
        assert set().union(*partitions_99) == all_nodes


# ---------------------------------------------------------------------------
# Testes: fallback e backend="auto"
# ---------------------------------------------------------------------------


class TestAutoBackend:
    """Testes do roteamento automático e comportamento de fallback."""

    def test_auto_fallback_warns_when_pymetis_unavailable(self, petersen: nx.Graph) -> None:
        """backend='auto' sem pymetis deve emitir UserWarning."""
        with (
            patch("src.anonymization._partition_backend._PYMETIS_AVAILABLE", False),
            pytest.warns(UserWarning, match="pymetis"),
        ):
            partition_graph(petersen, ck=2, seed=0, backend="auto")

    def test_auto_fallback_uses_kl_when_pymetis_unavailable(self, petersen: nx.Graph) -> None:
        """backend='auto' sem pymetis deve usar 'networkx-kl'."""
        with (
            patch("src.anonymization._partition_backend._PYMETIS_AVAILABLE", False),
            pytest.warns(UserWarning),
        ):
            _, meta = partition_graph(petersen, ck=2, seed=0, backend="auto")
        assert meta["backend_used"] == "networkx-kl"

    def test_auto_fallback_warning_mentions_d04(self, petersen: nx.Graph) -> None:
        """O UserWarning deve mencionar D-04 (decisão de referência)."""
        with (
            patch("src.anonymization._partition_backend._PYMETIS_AVAILABLE", False),
            pytest.warns(UserWarning, match="D-04"),
        ):
            partition_graph(petersen, ck=2, seed=0, backend="auto")

    def test_auto_fallback_warning_mentions_methodological_implication(
        self, petersen: nx.Graph
    ) -> None:
        """O UserWarning deve mencionar a implicação metodológica."""
        with (
            patch("src.anonymization._partition_backend._PYMETIS_AVAILABLE", False),
            pytest.warns(UserWarning, match="metodológica|metodologica|algorithm"),
        ):
            partition_graph(petersen, ck=2, seed=0, backend="auto")

    def test_auto_uses_pymetis_when_available(self, petersen: nx.Graph) -> None:
        """backend='auto' com pymetis disponível deve usar 'pymetis'."""
        if not _pymetis_importable():
            pytest.skip("pymetis não instalado — teste requer pymetis")

        with patch("src.anonymization._partition_backend._PYMETIS_AVAILABLE", True):
            _, meta = partition_graph(petersen, ck=2, seed=0, backend="auto")
        assert meta["backend_used"] == "pymetis"


# ---------------------------------------------------------------------------
# Testes: backend="pymetis" forçado
# ---------------------------------------------------------------------------


class TestPymetisBackend:
    """Testes do backend pymetis forçado."""

    def test_pymetis_forced_raises_import_error_when_unavailable(self, petersen: nx.Graph) -> None:
        """backend='pymetis' sem pymetis deve levantar ImportError."""
        with (
            patch("src.anonymization._partition_backend._PYMETIS_AVAILABLE", False),
            pytest.raises(ImportError, match="pymetis"),
        ):
            partition_graph(petersen, ck=2, seed=0, backend="pymetis")

    def test_pymetis_backend_used_reflects_pymetis(self, petersen: nx.Graph) -> None:
        """meta['backend_used'] deve ser 'pymetis' quando backend='pymetis'."""
        if not _pymetis_importable():
            pytest.skip("pymetis não instalado — teste requer pymetis")

        _, meta = partition_graph(petersen, ck=2, seed=0, backend="pymetis")
        assert meta["backend_used"] == "pymetis"

    def test_pymetis_partitions_cover_all_nodes(self, petersen: nx.Graph) -> None:
        """Partições do pymetis devem cobrir todos os nós."""
        if not _pymetis_importable():
            pytest.skip("pymetis não instalado — teste requer pymetis")

        partitions, _ = partition_graph(petersen, ck=2, seed=0, backend="pymetis")
        all_nodes = set(petersen.nodes())
        assert set().union(*partitions) == all_nodes

    def test_pymetis_meta_sizes_sum_to_n(self, petersen: nx.Graph) -> None:
        """meta['sizes'] do pymetis deve somar n."""
        if not _pymetis_importable():
            pytest.skip("pymetis não instalado — teste requer pymetis")

        _, meta = partition_graph(petersen, ck=2, seed=0, backend="pymetis")
        assert sum(meta["sizes"]) == petersen.number_of_nodes()


# ---------------------------------------------------------------------------
# Testes: validação de argumentos
# ---------------------------------------------------------------------------


class TestArgumentValidation:
    """Testes de validação de entradas."""

    def test_invalid_backend_raises_value_error(self, petersen: nx.Graph) -> None:
        """Backend desconhecido deve levantar ValueError."""
        with pytest.raises(ValueError, match="backend"):
            partition_graph(petersen, ck=2, seed=0, backend="invalid-backend")

    def test_ck_zero_raises_value_error(self, petersen: nx.Graph) -> None:
        """ck=0 deve levantar ValueError."""
        with pytest.raises(ValueError, match="ck"):
            partition_graph(petersen, ck=0, seed=0)

    def test_ck_negative_raises_value_error(self, petersen: nx.Graph) -> None:
        """ck negativo deve levantar ValueError."""
        with pytest.raises(ValueError, match="ck"):
            partition_graph(petersen, ck=-1, seed=0)

    def test_ck1_returns_single_partition_with_all_nodes(self, petersen: nx.Graph) -> None:
        """ck=1 deve retornar uma única partição com todos os nós."""
        partitions, meta = partition_graph(petersen, ck=1, seed=0, backend="networkx-kl")
        assert len(partitions) == 1
        assert partitions[0] == set(petersen.nodes())
        assert meta["inter_edges_removed"] == 0


# ---------------------------------------------------------------------------
# Helpers de teste
# ---------------------------------------------------------------------------


def _pymetis_importable() -> bool:
    """Verifica se pymetis pode ser importado no ambiente atual."""
    try:
        import pymetis  # type: ignore[import-untyped]  # noqa: F401

        return True
    except ImportError:
        return False


class TestPymetisAvailable:
    """O helper público pymetis_available() reflete a importabilidade real."""

    def test_matches_actual_importability(self) -> None:
        """pymetis_available() deve concordar com a tentativa real de import."""
        assert pymetis_available() == _pymetis_importable()
