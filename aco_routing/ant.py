from dataclasses import dataclass, field
from typing import Dict, List, Set, Union

from aco_routing import utils
from aco_routing.graph_api import GraphApi


@dataclass
class Ant:
    graph_api: GraphApi
    source: str
    destination: str
    # Pheromone bias
    alpha: float = 0.7
    # Edge cost bias
    beta: float = 0.3
    # Set of nodes that have been visited by the ant
    visited_nodes: Set = field(default_factory=set)
    # Path taken by the ant so far
    path: List[str] = field(default_factory=list)
    # Cost of the path taken by the ant so far
    path_cost: float = 0.0
    # Indicates if the ant has reached the destination (fit) or not (unfit)
    is_fit: bool = False
    # Indicates if the ant is the pheromone-greedy solution ant
    is_solution_ant: bool = False

    def __post_init__(self) -> None:
        # Set the spawn node as the current and first node
        self.current_node = self.source
        self.path.append(self.source)

    def reached_destination(self) -> bool:
        """Returns if the ant has reached the destination node in the graph

        Returns:
            bool: returns True if the ant has reached the destination
        """
        return self.current_node == self.destination

    def _get_unvisited_neighbors(self) -> List[str]:
        """Returns a subset of the neighbors of the node which are unvisited

        Returns:
            List[str]: A list of all the unvisited neighbors
        """
        return [
            node
            for node in self.graph_api.get_neighbors(self.current_node)
            if node not in self.visited_nodes
        ]

    def _compute_all_edges_desirability(
        self,
        unvisited_neighbors: List[str],
    ) -> float:
        """Computes the denominator of the transition probability equation for the ant

        Args:
            unvisited_neighbors (List[str]): All unvisited neighbors of the current node

        Returns:
            float: The summation of all the outgoing edges (to unvisited nodes) from the current node
        """
        total = 0.0
        for neighbor in unvisited_neighbors:
            edge_pheromones = self.graph_api.get_edge_pheromones(
                self.current_node, neighbor
            )
            edge_cost = self.graph_api.get_edge_cost(self.current_node, neighbor)
            total += utils.compute_edge_desirability(
                edge_pheromones, edge_cost, self.alpha, self.beta
            )

        return total

    def _calculate_edge_probabilities(
        self, unvisited_neighbors: List[str]
    ) -> Dict[str, float]:
        """Computes the transition probabilities of all the edges from the current node

        Args:
            unvisited_neighbors (List[str]): A list of unvisited neighbors of the current node

        Returns:
            Dict[str, float]: A dictionary mapping nodes to their transition probabilities
        """
        probabilities: Dict[str, float] = {}

        all_edges_desirability = self._compute_all_edges_desirability(
            unvisited_neighbors
        )

        for neighbor in unvisited_neighbors:
            edge_pheromones = self.graph_api.get_edge_pheromones(
                self.current_node, neighbor
            )
            edge_cost = self.graph_api.get_edge_cost(self.current_node, neighbor)

            current_edge_desirability = utils.compute_edge_desirability(
                edge_pheromones, edge_cost, self.alpha, self.beta
            )
            probabilities[neighbor] = current_edge_desirability / all_edges_desirability

        return probabilities

    def _choose_next_node(self) -> Union[str, None]:
        """Choose the next node to be visited by the ant

        Returns:
            [str, None]: The computed next node to be visited by the ant or None if no possible moves
        """
        unvisited_neighbors = self._get_unvisited_neighbors()

        if self.is_solution_ant:
            if len(unvisited_neighbors) == 0:
                raise Exception(
                    f"No path found from {self.source} to {self.destination}"
                )

            # The final/solution ant greedily chooses the next node with the highest pheromone value
            return max(
                unvisited_neighbors,
                key=lambda neighbor: self.graph_api.get_edge_pheromones(
                    self.current_node, neighbor
                ),
            )

        # Check if ant has no possible nodes to move to
        if len(unvisited_neighbors) == 0:
            return None

        probabilities = self._calculate_edge_probabilities(unvisited_neighbors)

        # Pick the next node based on the roulette wheel selection technique
        return utils.roulette_wheel_selection(probabilities)

    def take_step(self) -> None:
        """Compute and update the ant position"""
        # Mark the current node as visited
        self.visited_nodes.add(self.current_node)

        # Pick the next node of the ant
        next_node = self._choose_next_node()

        # Check if ant is stuck at current node
        if not next_node:
            # TODO: optimization: set ant as unfit
            return

        self.path.append(next_node)
        self.path_cost += self.graph_api.get_edge_cost(self.current_node, next_node)
        self.current_node = next_node

    def deposit_pheromones_on_path(self) -> None:
        """Updates the pheromones along all the edges in the path"""
        for i in range(len(self.path) - 1):
            u, v = self.path[i], self.path[i + 1]
            new_pheromone_value = 1 / self.path_cost
            self.graph_api.deposit_pheromones(u, v, new_pheromone_value)
