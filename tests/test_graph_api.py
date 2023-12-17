from aco_routing.graph_api import GraphApi
import networkx as nx

G = nx.DiGraph()

G.add_edge("A", "B", cost=2)
G.add_edge("B", "C", cost=5)
G.add_edge("C", "D", cost=3)
G.add_edge("C", "E", cost=7)
G.add_edge("E", "A", cost=1)

graph_api = GraphApi(G, evaporation_rate=0.1)


def test_get_nodes() -> None:
    assert graph_api.get_all_nodes() == ["A", "B", "C", "D", "E"]


def test_get_neighbors() -> None:
    assert graph_api.get_neighbors("C") == ["D", "E"]


def test_get_edge_cost() -> None:
    assert graph_api.get_edge_cost("C", "E") == 7


def test_set_edge_pheromones() -> None:
    graph_api.set_edge_pheromones("E", "A", 6.0)
    assert graph_api.get_edge_pheromones("E", "A") == 6.0
