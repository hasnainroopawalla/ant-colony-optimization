from dataclasses import dataclass, field
import random
from typing import Dict, List, Set

from aco_routing.utils.graph import Edge, Graph


@dataclass
class Ant:
    graph: Graph
    source: str
    destination: str
    visited_nodes: Set = field(default_factory=set)
    path: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.current_node = self.source
        self.path.append(self.source)

    def reached_destination(self) -> bool:
        return self.current_node == self.destination

    def _get_unvisited_neighbors(self, all_neighbors) -> Dict[str, Edge]:
        unvisited_neighbors = {}
        for neighbor, edge in all_neighbors.items():
            if neighbor in self.visited_nodes:
                continue
            # self.graph.get_node(neighbor).visited is False:
            unvisited_neighbors[neighbor] = edge
        return unvisited_neighbors

    @staticmethod
    def _calculate_edges_total(unvisited_neighbors, alpha, beta):
        total = 0.0
        for neighbor, edge in unvisited_neighbors.items():
            total += (edge.pheromones ** alpha) * ((1 / edge.travel_time) ** beta)
        return total

    @staticmethod
    def _calculate_edge_probabilites_and_sort(unvisited_neighbors, total, alpha, beta):
        probabilities = {}
        for neighbor, edge in unvisited_neighbors.items():
            probabilities[neighbor] = (
                (edge.pheromones ** alpha) * ((1 / edge.travel_time) ** beta)
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
        self.visited_nodes.add(self.current_node)
        # self.graph.mark_node_as_visited(self.current_node)

        all_neighbors = self.graph.get_node_edges(self.current_node)

        # Check if there are no neighbors
        if len(all_neighbors) == 0:
            return []

        # Find unvisited neighbors
        unvisited_neighbors = self._get_unvisited_neighbors(all_neighbors)

        total = self._calculate_edges_total(
            unvisited_neighbors, self.graph.alpha, self.graph.beta
        )
        sorted_probabilities = self._calculate_edge_probabilites_and_sort(
            unvisited_neighbors, total, self.graph.alpha, self.graph.beta
        )

        next_node = self._choose_neighbor_using_roulette_wheel(sorted_probabilities)

        self.path.append(next_node)
        self.current_node = next_node
