from dataclasses import dataclass
from typing import List
import networkx as nx


# TODO: Add unit tests


@dataclass
class GraphApi:
    graph: nx.DiGraph

    def set_edge_pheromones(self, u: str, v: str, pheromone_value: float) -> None:
        self.graph[u][v]["pheromones"] = pheromone_value

    def get_edge_pheromones(self, u: str, v: str) -> float:
        return self.graph[u][v]["pheromones"]

    def get_edge_cost(self, u: str, v: str) -> float:
        return self.graph[u][v]["cost"]

    def evaporate_edge_pheromones(
        self, u: str, v: str, evaporation_rate: float
    ) -> None:
        old_pheromone_value = self.get_edge_pheromones(u, v)
        new_pheromone_value = max(old_pheromone_value * 1 - evaporation_rate, 0)
        self.set_edge_pheromones(u, v, new_pheromone_value)

    def get_all_nodes(self) -> List[str]:
        return list(self.graph.nodes)

    def get_neighbors(self, node: str) -> List[str]:
        return self.graph.neighbors(node)
