"""Testes unitários para _partition_neighborhoods em src/anonymization/he2009.py.

Cobre:
    - n=10, d=2  → 5 Local Structures; todos os nós cobertos; sem inter-arestas
    - n=10, d=5  → 2 Local Structures com exatamente 5 nós cada
    - Sem arestas cruzando fronteiras de partição (invariante central da Seção 3.1)
    - d=5 produz LSs maiores que d=2 (verificação de number_of_nodes)
    - Grafo de caminho n=6, d=2 → 3 LSs com cobertura total
    - Tipo de retorno correto (list[nx.Graph])
    - ValueError quando d >= n

Nota sobre tamanhos exatos com d=2 (ck=5):
    O backend KL (fallback D-04) aplica bissecção recursiva e não garante
    partições de exatamente d nós para ck>2. A propriedade "exatamente d nós"
    é garantida pelo pymetis com tpwgts, testado separadamente em
    test_partition_backend.py. Aqui testa-se contagem e cobertura, não tamanho
    exato por partição, para ck=5. Para ck=2 (d=5), KL garante balanceamento.

Seeds fixadas são exceção controlada conforme .claude/rules/seeds.md.
"""

from __future__ import annotations

import networkx as nx
import pytest

from src.anonymization.he2009 import _partition_neighborhoods

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def petersen() -> nx.Graph:
    """Grafo de Petersen: 10 nós, 3-regular, conexo."""
    return nx.petersen_graph()


@pytest.fixture
def path6() -> nx.Graph:
    """Grafo de caminho com 6 nós: 0-1-2-3-4-5."""
    return nx.path_graph(6)


# ---------------------------------------------------------------------------
# Testes: n=10, d=2 (ck=5)
# ---------------------------------------------------------------------------


class TestPetersenD2:
    """Petersen (n=10) particionado com d=2 → ck=5 Local Structures."""

    def test_returns_five_local_structures(self, petersen: nx.Graph) -> None:
        """d=2 deve retornar exatamente 5 Local Structures."""
        ls = _partition_neighborhoods(petersen, d=2, seed=0, backend="networkx-kl")
        assert len(ls) == 5

    def test_all_nodes_covered(self, petersen: nx.Graph) -> None:
        """A união dos nós de todas as LSs deve cobrir V(G) exatamente."""
        ls = _partition_neighborhoods(petersen, d=2, seed=0, backend="networkx-kl")
        all_nodes = set(petersen.nodes())
        covered = set().union(*(set(li.nodes()) for li in ls))
        assert covered == all_nodes

    def test_partitions_are_disjoint(self, petersen: nx.Graph) -> None:
        """Nenhum nó deve aparecer em mais de uma Local Structure."""
        ls = _partition_neighborhoods(petersen, d=2, seed=0, backend="networkx-kl")
        seen: set = set()
        for li in ls:
            nodes = set(li.nodes())
            assert nodes.isdisjoint(seen), "Partições se sobrepõem"
            seen |= nodes

    def test_no_inter_edges_in_any_ls(self, petersen: nx.Graph) -> None:
        """Nenhuma aresta de LS deve cruzar fronteiras de partição.

        Para cada aresta (u, v) em qualquer LS retornada, ambos u e v
        devem pertencer à mesma LS.
        """
        ls = _partition_neighborhoods(petersen, d=2, seed=0, backend="networkx-kl")
        # Mapa nó → índice de partição para verificação cruzada
        node_to_part: dict[int, int] = {}
        for idx, li in enumerate(ls):
            for node in li.nodes():
                node_to_part[node] = idx
        for li in ls:
            for u, v in li.edges():
                assert node_to_part[u] == node_to_part[v], (
                    f"Inter-aresta detectada: ({u}, {v}) em partições "
                    f"{node_to_part[u]} e {node_to_part[v]}"
                )

    def test_returns_list_of_nx_graph(self, petersen: nx.Graph) -> None:
        """Retorno deve ser list[nx.Graph]."""
        ls = _partition_neighborhoods(petersen, d=2, seed=0, backend="networkx-kl")
        assert isinstance(ls, list)
        assert all(isinstance(li, nx.Graph) for li in ls)

    def test_subgraphs_are_copies_not_views(self, petersen: nx.Graph) -> None:
        """Subgrafos retornados devem ser cópias independentes do grafo original."""
        ls = _partition_neighborhoods(petersen, d=2, seed=0, backend="networkx-kl")
        for li in ls:
            # copy() retorna Graph, não SubGraph view
            assert type(li) is nx.Graph


# ---------------------------------------------------------------------------
# Testes: n=10, d=5 (ck=2)
# ---------------------------------------------------------------------------


class TestPetersenD5:
    """Petersen (n=10) particionado com d=5 → ck=2 Local Structures."""

    def test_returns_two_local_structures(self, petersen: nx.Graph) -> None:
        """d=5 deve retornar exatamente 2 Local Structures."""
        ls = _partition_neighborhoods(petersen, d=5, seed=0, backend="networkx-kl")
        assert len(ls) == 2

    def test_each_ls_has_five_nodes(self, petersen: nx.Graph) -> None:
        """Com ck=2 e n=10, KL bissecção balanceada produz exatamente 5 nós por LS."""
        ls = _partition_neighborhoods(petersen, d=5, seed=0, backend="networkx-kl")
        for li in ls:
            assert li.number_of_nodes() == 5

    def test_all_nodes_covered(self, petersen: nx.Graph) -> None:
        """A união deve cobrir todos os 10 nós do Petersen."""
        ls = _partition_neighborhoods(petersen, d=5, seed=0, backend="networkx-kl")
        all_nodes = set(petersen.nodes())
        covered = set().union(*(set(li.nodes()) for li in ls))
        assert covered == all_nodes

    def test_no_inter_edges_in_any_ls(self, petersen: nx.Graph) -> None:
        """Nenhuma aresta deve cruzar fronteiras de partição."""
        ls = _partition_neighborhoods(petersen, d=5, seed=0, backend="networkx-kl")
        node_to_part: dict[int, int] = {}
        for idx, li in enumerate(ls):
            for node in li.nodes():
                node_to_part[node] = idx
        for li in ls:
            for u, v in li.edges():
                assert node_to_part[u] == node_to_part[v]


# ---------------------------------------------------------------------------
# Teste comparativo: d=5 produz LSs maiores que d=2
# ---------------------------------------------------------------------------


class TestSizeOrdering:
    """Verifica que d maior produz Local Structures com mais nós."""

    def test_d5_ls_larger_than_d2_ls(self, petersen: nx.Graph) -> None:
        """Média de nós por LS com d=5 deve ser maior que com d=2."""
        ls_d2 = _partition_neighborhoods(petersen, d=2, seed=0, backend="networkx-kl")
        ls_d5 = _partition_neighborhoods(petersen, d=5, seed=0, backend="networkx-kl")
        avg_d2 = sum(li.number_of_nodes() for li in ls_d2) / len(ls_d2)
        avg_d5 = sum(li.number_of_nodes() for li in ls_d5) / len(ls_d5)
        assert avg_d5 > avg_d2


# ---------------------------------------------------------------------------
# Testes: grafo de caminho n=6, d=2 (ck=3)
# ---------------------------------------------------------------------------


class TestPathGraphD2:
    """Grafo de caminho (n=6) particionado com d=2 → ck=3 Local Structures."""

    def test_returns_three_local_structures(self, path6: nx.Graph) -> None:
        """d=2 em n=6 deve retornar 3 Local Structures."""
        ls = _partition_neighborhoods(path6, d=2, seed=0, backend="networkx-kl")
        assert len(ls) == 3

    def test_all_nodes_covered(self, path6: nx.Graph) -> None:
        """A união deve cobrir todos os 6 nós do grafo de caminho."""
        ls = _partition_neighborhoods(path6, d=2, seed=0, backend="networkx-kl")
        all_nodes = set(path6.nodes())
        covered = set().union(*(set(li.nodes()) for li in ls))
        assert covered == all_nodes

    def test_no_inter_edges(self, path6: nx.Graph) -> None:
        """Nenhuma aresta deve cruzar fronteiras de partição."""
        ls = _partition_neighborhoods(path6, d=2, seed=0, backend="networkx-kl")
        node_to_part: dict[int, int] = {}
        for idx, li in enumerate(ls):
            for node in li.nodes():
                node_to_part[node] = idx
        for li in ls:
            for u, v in li.edges():
                assert node_to_part[u] == node_to_part[v]

    def test_lss_may_have_distinct_structure(self, path6: nx.Graph) -> None:
        """LSs de um caminho podem ter estruturas distintas (densidades variáveis).

        Para cada LS de tamanho s, o número de arestas internas é no máximo s-1
        (caminho interno máximo). Verifica que o invariante structural é mantido
        independentemente de quais nós KL colocou em cada partição.
        """
        ls = _partition_neighborhoods(path6, d=2, seed=0, backend="networkx-kl")
        for li in ls:
            s = li.number_of_nodes()
            # Num caminho, subgrafo induzido de s nós tem no máximo s-1 arestas
            assert li.number_of_edges() <= s - 1


# ---------------------------------------------------------------------------
# Testes: validação de argumentos
# ---------------------------------------------------------------------------


class TestArgumentValidation:
    """Testes de validação de entradas."""

    def test_d_equal_n_raises_value_error(self, petersen: nx.Graph) -> None:
        """d == n não permite formar nenhuma partição válida."""
        with pytest.raises(ValueError, match="d="):
            _partition_neighborhoods(petersen, d=10)

    def test_d_greater_than_n_raises_value_error(self, petersen: nx.Graph) -> None:
        """d > n deve levantar ValueError."""
        with pytest.raises(ValueError, match="d="):
            _partition_neighborhoods(petersen, d=11)

    def test_d1_returns_n_single_node_ls(self, petersen: nx.Graph) -> None:
        """d=1 deve retornar n Local Structures de 1 nó cada."""
        ls = _partition_neighborhoods(petersen, d=1, seed=0, backend="networkx-kl")
        assert len(ls) == 10
        assert all(li.number_of_nodes() == 1 for li in ls)
        assert all(li.number_of_edges() == 0 for li in ls)
