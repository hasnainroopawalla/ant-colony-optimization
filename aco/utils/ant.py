from dataclasses import dataclass, field
import random
from typing import Dict, List

from aco.graph import Edge, Graph


@dataclass
class Ant:
    graph: Graph
    source: str
    destination: str = str
    path: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.current_node = self.source

    # def update_destination(self, destination):
    #     self.destination = destination

    # def update_source(self, source):
    #     self.source = source

    # def update_current(self, curr):
    #     self.current_node = curr

    # def reset_paths(self):
    #     self.path_taken = []
    #     self.path_to_take = []

    def reached_destination(self) -> bool:
        return self.current_node == self.destination

    def _get_unvisited_neighbors(self, all_neighbors) -> Dict[str, Edge]:
        unvisited_neighbors = {}
        for neighbor, edge in all_neighbors.items():
            if self.graph.get_node(neighbor).visited is False:
                unvisited_neighbors[neighbor] = edge
        return unvisited_neighbors

    @staticmethod
    def _calculate_edges_total(unvisited_neighbors, alpha, beta):
        total = 0.0
        for neighbor, edge in unvisited_neighbors.items():
            total += (edge.pheromone ** alpha) * ((1 / edge.travel_time) ** beta)
        return total

    @staticmethod
    def _calculate_edge_probabilites_and_sort(unvisited_neighbors, total, alpha, beta):
        probabilities = {}
        for neighbor, edge in unvisited_neighbors.items():
            probabilities[neighbor] = (
                (edge.pheromone ** alpha) * ((1 / edge.travel_time) ** beta)
            ) / total

        sorted_probabilities = {
            k: v for k, v in sorted(probabilities.items(), key=lambda item: -item[1])
        }

        return sorted_probabilities

    @staticmethod
    def _choose_next_node(cumulative_sum):
        max = sum(cumulative_sum.values())
        pick = random.uniform(0, max)
        current = 0
        for key, value in cumulative_sum.items():
            current += value
            if current > pick:
                return key

    def _choose_neighbor_using_roulette_wheel(self, sorted_probabilities):
        next_node = self._choose_next_node(sorted_probabilities)
        return next_node

    def take_step(self):
        self.graph.mark_node_as_visited(self.current_node)

        all_neighbors = self.graph.get_node_edges(self.current_node)

        # Check if there are no neighbors
        if len(all_neighbors) == 0:
            return False

        # Find unvisited neighbors
        unvisited_neighbors = self._get_unvisited_neighbors(all_neighbors)

        total = self._calculate_edges_total(
            unvisited_neighbors, self.graph.alpha, self.graph.beta
        )
        sorted_probabilities = self._calculate_edge_probabilites_and_sort(
            unvisited_neighbors, total, self.graph.alpha, self.graph.beta
        )

        next_node = self._roulette_wheel(sorted_probabilities)

        self.path.append((self.current_node, next_node))

        self.current_node = next_node

    def get_path_taken(self):
        return self.path_taken

    def get_time_spent(self):
        time_spent = 0
        for path in self.path_taken:
            time_spent += path["time_spent"]

        return time_spent


def runACO(G: Graph, source: str, destination: str):

    ant_paths = []
    max_iterations = 50

    # ants = [
    #     Ant(G, source, destination),
    #     Ant(G, source, destination),
    #     Ant(G, source, destination),
    #     Ant(G, source, destination),
    #     Ant(G, source, destination),
    #     Ant(G, source, destination),
    # ]

    ant = Ant(G, source, destination)

    for i in range(max_iterations):
        if ant.reached_destination():
            print(ant.path)
            pass
        ant.take_step()
