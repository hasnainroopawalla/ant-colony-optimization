from dataclasses import dataclass, field
import random
from typing import Dict, List, Set
import networkx as nx

from aco_routing import utils


@dataclass
class Ant:
    """A class for an Ant that traverses the graph.

    Args:
        graph (Graph): The Graph object.
        source (str): The source node of the ant.
        destination (str): The destination node of the ant.
        alpha (float, optional): The amount of importance given to the pheromone by the ant. Defaults to 0.9.
        beta (float, optional): The amount of importance given to the travel time value by the ant. Defaults to 0.1.
        visited_nodes (Set, optional): A set of nodes that have been visited by the ant.
        path (List[str], optional): A List of node IDs of the path taken by the ant so far.
        is_fit (bool, optional): Indicates if the ant has reached the destination (fit) or not (unfit). Defaults to False.
        is_solution_ant (bool, optional): Indicates if the ant is the final/solution ant. Defaults to False.
    """

    graph: nx.DiGraph
    source: str
    destination: str
    alpha: float = 0.7
    beta: float = 0.3
    visited_nodes: Set = field(default_factory=set)
    path: List[str] = field(default_factory=list)
    is_fit: bool = False
    is_solution_ant: bool = False

    def __post_init__(self) -> None:
        self.current_node = self.source  # TODO: change to nx.Graph.Node
        self.path.append(self.source)

    def reached_destination(self) -> bool:
        """Checks if the ant has reached the destination node in the graph.

        Returns:
            bool: True, if the ant has reached the destination.
        """
        return self.current_node == self.destination

    def _get_unvisited_neighbors(self) -> List[str]:
        """Returns a subset of the all the neighbors of the node which are unvisited.

        Args:
            all_neighbors (Dict[str, Edge]): A set of all neighbors of the node.

        Returns:
            Dict[str, Edge]: A subset of all the unvisited neighbors.
        """
        return [
            node
            for node in self.graph.neighbors(self.current_node)
            if node not in self.visited_nodes
        ]

    def _compute_all_edges_desirability(
        self,
        # unvisited_neighbors: Dict[str, Edge], alpha: float, beta: float
        neighbors: List[str],
    ) -> float:
        """Computes the denominator of the transition probability equation for the ant

        Args:
            unvisited_neighbors (Dict[str, Edge]): A set of unvisited neighbors of the current node
            alpha (float): [description]: The alpha value
            beta (float): [description]: The beta value

        Returns:
            float: The summation of all the outgoing edges (to unvisited nodes) from the current node
        """
        total = 0.0
        for node in neighbors:
            edge = self.graph.get_edge_data(node)
            total += utils.compute_edge_desirability(
                edge.pheromone, edge.weight, self.alpha, self.beta
            )
        return total

    def _calculate_edge_probabilities(
        self,
        unvisited_neighbors: List[str]
        # unvisited_neighbors: Dict[str, Edge], alpha: float, beta: float, total: float
    ) -> Dict[str, float]:
        """Computes the transition probabilities of all the edges from the current node

        Args:
            unvisited_neighbors (Dict[str, Edge]): A set of unvisited neighbors of the current node.
            alpha (float): [description]: The alpha value.
            beta (float): [description]: The beta value.
            total (float): [description]: The summation of all the outgoing edges (to unvisited nodes) from the current node.

        Returns:
            Dict[str, float]: A dictionary mapping node IDs to their transition probabilities.
        """

        probabilities: Dict[
            str, float
        ] = {}  # TODO: Replace all str with Any for nx.Graph

        all_edges_desirability = self._compute_all_edges_desirability(
            unvisited_neighbors
        )

        for node in unvisited_neighbors:
            edge = self.graph.get_edge_data(node)
            current_edge_desirability = utils.compute_edge_desirability(
                edge.pheromone, edge.weight, self.alpha, self.beta
            )
            probabilities[node] = current_edge_desirability / all_edges_desirability

        return probabilities

    def _pick_next_node(
        # self, unvisited_neighbors: Dict[str, Edge], alpha: float, beta: float
        self,
    ) -> str:
        """Chooses the next node to be visited by the ant using the Roulette Wheel selection technique.

        Args:
            unvisited_neighbors (Dict[str, Edge]): A set of unvisited neighbors of the current node.
            alpha (float): [description]: The alpha value.
            beta (float): [description]: The beta value.

        Returns:
            str: The ID of the next node to be visited by the ant.
        """
        unvisited_neighbors = self._get_unvisited_neighbors()

        if self.is_solution_ant:
            # The final/solution ant greedily chooses the next node with the highest pheromone value
            return max(
                unvisited_neighbors,
                key=lambda k: self.graph.get_edge_data(k).pheromones,
            )

        probabilities = self._calculate_edge_probabilities(unvisited_neighbors)

        # Pick the next node based on the roulette wheel selection technique
        return utils.roulette_wheel_selection(probabilities)

    def take_step(self) -> None:
        """This method allows the ant to travel to a neighbor of the current node in the graph."""
        # Mark the current node as visited
        self.visited_nodes.add(self.current_node)

        # TODO: remove all_neighbors method call
        # Find all the neighbors of the current node
        all_neighbors = [node for node in self.graph.neighbors(self.current_node)]

        # Check if the current node has no neighbors (isolated node)
        if len(all_neighbors) == 0:
            return

        # Pick the next node of the ant
        next_node = self._pick_next_node()

        if not next_node:
            return

        self.path.append(next_node)
        self.current_node = next_node
