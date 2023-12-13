from typing import List
import networkx as nx

# TODO: Add unit tests


def set_edge_pheromones(
    graph: nx.DiGraph, u: str, v: str, pheromone_value: float
) -> None:
    graph[u][v]["pheromones"] = pheromone_value


def get_edge_pheromones(graph: nx.DiGraph, u: str, v: str) -> float:
    return graph[u][v]["pheromones"]


def get_edge_cost(graph: nx.DiGraph, u: str, v: str) -> float:
    return graph[u][v]["cost"]


def evaporate_edge_pheromones(
    graph: nx.DiGraph, u: str, v: str, evaporation_rate: float
) -> None:
    old_pheromone_value = get_edge_pheromones(graph, u, v)
    new_pheromone_value = old_pheromone_value * 1 - evaporation_rate
    set_edge_pheromones(graph, u, v, new_pheromone_value)


def get_all_nodes(graph: nx.DiGraph) -> List[str]:
    return list(graph.nodes)
