from dataclasses import dataclass, field
import random
from typing import Dict, List, Set

from aco_routing.utils.graph import Edge, Graph


@dataclass
class Ant:
    """A class for an Ant that traverses the graph.

    Args:
        graph (Graph): The Graph object.
        source (str): The source node of the ant.
        destination (str): The destination node of the ant.
        alpha (float): The amount of importance given to the pheromone by the ant. Defaults to 0.9.
        beta (float): The amount of importance given to the travel time value by the ant. Defaults to 0.1.
        visited_nodes (Set): A set of nodes that have been visited by the ant.
        path (List[str]): A List of node IDs of the path taken by the ant so far.
        is_fit (bool): A flag which indicates if the ant has reached the destination (fit) or not (unfit). Defaults to False.
    """

    graph: Graph
    source: str
    destination: str
    alpha: float = 0.7
    beta: float = 0.3
    visited_nodes: Set = field(default_factory=set)
    path: List[str] = field(default_factory=list)
    is_fit: bool = False

    def __post_init__(self) -> None:
        self.current_node = self.source
        self.path.append(self.source)

    def reached_destination(self) -> bool:
        """Checks if the ant has reached the destination node in the graph.

        Returns:
            bool: True, if the ant has reached the destination.
        """
        return self.current_node == self.destination

    def _get_unvisited_neighbors(
        self, all_neighbors: Dict[str, Edge]
    ) -> Dict[str, Edge]:
        """Returns a subset of the all the neighbors of the node which are unvisited.

        Args:
            all_neighbors (Dict[str, Edge]): A set of all neighbors of the node.

        Returns:
            Dict[str, Edge]: A subset of all the unvisited neighbors.
        """
        unvisited_neighbors = {}
        for neighbor, edge in all_neighbors.items():
            if neighbor in self.visited_nodes:
                continue
            unvisited_neighbors[neighbor] = edge
        return unvisited_neighbors

    @staticmethod
    def _calculate_edges_total(
        unvisited_neighbors: Dict[str, Edge], alpha: float, beta: float
    ) -> float:
        """Computes the denominator of the transition probability equation for the ant.

        Args:
            unvisited_neighbors (Dict[str, Edge]): A set of unvisited neighbors of the current node.
            alpha (float): [description]: The alpha value.
            beta (float): [description]: The beta value.

        Returns:
            float: The summation of all the outgoing edges (to unvisited nodes) from the current node.
        """
        total = 0.0
        for neighbor, edge in unvisited_neighbors.items():
            total += (edge.pheromones ** alpha) * ((1 / edge.travel_time) ** beta)
        return total

    @staticmethod
    def _calculate_edge_probabilites(
        unvisited_neighbors: Dict[str, Edge], alpha: float, beta: float, total: float
    ) -> Dict[str, float]:
        """Computes the transition probabilities of all the edges from the current node.

        Args:
            unvisited_neighbors (Dict[str, Edge]): A set of unvisited neighbors of the current node.
            alpha (float): [description]: The alpha value.
            beta (float): [description]: The beta value.
            total (float): [description]: The summation of all the outgoing edges (to unvisited nodes) from the current node.

        Returns:
            Dict[str, float]: A dictionary mapping node IDs to their transition probabilities.
        """
        probabilities = {}
        for neighbor, edge in unvisited_neighbors.items():
            probabilities[neighbor] = (
                (edge.pheromones ** alpha) * ((1 / edge.travel_time) ** beta)
            ) / total
        return probabilities

    @staticmethod
    def _sort_edge_probabilites(probabilities: Dict[str, float]):
        """Sorts the probabilities of the edges in descending order.

        Args:
            probabilities (Dict[str, float]): A dictionary mapping the node IDs to their transition probabilities.

        Returns:
            [type]: A sorted dictionary mapping node IDs to their transition probabilities.
        """
        return {
            k: v for k, v in sorted(probabilities.items(), key=lambda item: -item[1])
        }

    @staticmethod
    def _choose_neighbor_using_roulette_wheel(
        sorted_probabilities: Dict[str, float]
    ) -> str:
        """Chooses the next node to be visited using the Roulette Wheel selection technique.

        Args:
            sorted_probabilities (Dict[str, Edge]): A sorted dictionary mapping node IDs to their transition probabilities.

        Returns:
            str: The ID of the next node to be visited by the ant.
        """
        pick = random.uniform(0, sum(sorted_probabilities.values()))
        current = 0.0
        next_node = ""
        for key, value in sorted_probabilities.items():
            current += value
            if current > pick:
                next_node = key
                break
        return next_node

    def _pick_next_node(
        self, unvisited_neighbors: Dict[str, Edge], alpha: float, beta: float
    ) -> str:
        """Chooses the next node to be visited by the ant using the Roulette Wheel selection technique.

        Args:
            unvisited_neighbors (Dict[str, Edge]): A set of unvisited neighbors of the current node.
            alpha (float): [description]: The alpha value.
            beta (float): [description]: The beta value.

        Returns:
            str: The ID of the next node to be visited by the ant.
        """
        edges_total = self._calculate_edges_total(unvisited_neighbors, alpha, beta)
        probabilities = self._calculate_edge_probabilites(
            unvisited_neighbors, edges_total, alpha, beta
        )
        sorted_probabilities = self._sort_edge_probabilites(probabilities)
        return self._choose_neighbor_using_roulette_wheel(sorted_probabilities)

    def take_step(self) -> None:
        """This method allows the ant to travel to a neighbor of the current node in the graph.
        """
        # Mark the node as visited.
        self.visited_nodes.add(self.current_node)

        # Find all the neighboring nodes of the current node.
        all_neighbors = self.graph.get_node_edges(self.current_node)

        # Check if the current node has no neighbors (isolated node).
        if len(all_neighbors) == 0:
            return

        # Find unvisited neighbors of the current node.
        unvisited_neighbors = self._get_unvisited_neighbors(all_neighbors)

        # Pick the next node based on the Roulette Wheel selection technique.
        next_node = self._pick_next_node(unvisited_neighbors, self.alpha, self.beta)

        self.path.append(next_node)
        self.current_node = next_node
