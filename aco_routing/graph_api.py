from dataclasses import dataclass
from typing import List
import networkx as nx
import matplotlib.pyplot as plt


@dataclass
class GraphApi:
    graph: nx.DiGraph
    evaporation_rate: float

    def set_edge_pheromones(self, u: str, v: str, pheromone_value: float) -> None:
        self.graph[u][v]["pheromones"] = pheromone_value

    def get_edge_pheromones(self, u: str, v: str) -> float:
        return self.graph[u][v]["pheromones"]

    def deposit_pheromones(self, u: str, v: str, pheromone_amount: float) -> None:
        self.graph[u][v]["pheromones"] += max(
            (1 - self.evaporation_rate) + pheromone_amount, 1e-13
        )

    def get_edge_cost(self, u: str, v: str) -> float:
        return self.graph[u][v]["cost"]

    def get_all_nodes(self) -> List[str]:
        return list(self.graph.nodes)

    def get_neighbors(self, node: str) -> List[str]:
        return list(self.graph.neighbors(node))

    def visualize_graph(self, shortest_path: List[str]) -> None:
        for edge in self.graph.edges:
            source, destination = edge[0], edge[1]
            self.graph[source][destination]["pheromones"] = round(
                self.graph[source][destination]["pheromones"]
            )

        pos = nx.spring_layout(self.graph, seed=2)
        nx.draw(self.graph, pos, width=4)

        nx.draw_networkx_nodes(self.graph, pos, node_size=700)

        # nx.draw_networkx_edges(G, pos, width=2)
        nx.draw_networkx_edges(
            self.graph,
            pos,
            edgelist=list(zip(shortest_path, shortest_path[1:])),
            edge_color="r",
            width=4,
        )

        # node labels
        nx.draw_networkx_labels(self.graph, pos, font_size=20)
        # edge cost labels
        edge_labels = nx.get_edge_attributes(self.graph, "pheromones")
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels)

        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        plt.tight_layout()
        plt.show()
