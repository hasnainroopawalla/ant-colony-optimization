from dataclasses import dataclass, field
from typing import Dict, List, Set, Union
import networkx as nx

from aco_routing import utils
from aco_routing.graph_api import GraphApi


# TODO: Fix function desc
@dataclass
class Ant:
    """A class for an Ant that traverses the graph

    Args:
        graph (Graph): The Graph object
        source (str): The source node of the ant
        destination (str): The destination node of the ant
        alpha (float, optional): The amount of importance given to the pheromone by the ant
        beta (float, optional): The amount of importance given to the travel time value by the ant
        visited_nodes (Set, optional): A set of nodes that have been visited by the ant
        path (List[str], optional): A List of node IDs of the path taken by the ant so far
        is_fit (bool, optional): Indicates if the ant has reached the destination (fit) or not (unfit)
        is_solution_ant (bool, optional): Indicates if the ant is the final/solution ant
    """

    graph_api: GraphApi
    source: str
    destination: str
    alpha: float = 0.7
    beta: float = 0.3
    visited_nodes: Set = field(default_factory=set)
    path: List[str] = field(default_factory=list)
    path_cost: float = 0.0
    is_fit: bool = False
    is_solution_ant: bool = False

    def __post_init__(self) -> None:
        self.current_node = self.source  # TODO: change to nx.Graph.Node
        self.path.append(self.source)

    def reached_destination(self) -> bool:
        """Returns if the ant has reached the destination node in the graph

        Returns:
            bool: True, if the ant has reached the destination
        """
        return self.current_node == self.destination

    def _get_unvisited_neighbors(self) -> List[str]:
        """Returns a subset of the all the neighbors of the node which are unvisited

        Args:
            all_neighbors (Dict[str, Edge]): A set of all neighbors of the node

        Returns:
            Dict[str, Edge]: A subset of all the unvisited neighbors
        """
        return [
            node
            for node in self.graph_api.get_neighbors(self.current_node)
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
        for neighbor in neighbors:
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
        """Chooses the next node to be visited by the ant

        Args:
            unvisited_neighbors (Dict[str, Edge]): A set of unvisited neighbors of the current node
            alpha (float): [description]: The alpha value
            beta (float): [description]: The beta value

        Returns:
            str: The ID of the next node to be visited by the ant
        """
        unvisited_neighbors = self._get_unvisited_neighbors()

        if self.is_solution_ant:
            # The final/solution ant greedily chooses the next node with the highest pheromone value
            return max(
                unvisited_neighbors,
                key=lambda neighbor: self.graph_api.get_edge_pheromones(
                    self.current_node, neighbor
                ),
            )

        # check if ant has no possible nodes to move to
        if len(unvisited_neighbors) == 0:
            return None
        probabilities = self._calculate_edge_probabilities(unvisited_neighbors)

        # Pick the next node based on the roulette wheel selection technique
        return utils.roulette_wheel_selection(probabilities)

    def take_step(self) -> None:
        """This method allows the ant to travel to a neighbor of the current node in the graph"""
        # Mark the current node as visited
        self.visited_nodes.add(self.current_node)

        # TODO: remove all_neighbors method call
        # Find all the neighbors of the current node
        all_neighbors = [
            node for node in self.graph_api.get_neighbors(self.current_node)
        ]

        # Check if the current node has no neighbors (isolated node)
        if len(all_neighbors) == 0:
            return

        # Pick the next node of the ant
        next_node = self._choose_next_node()

        if not next_node:
            return

        self.path.append(next_node)
        self.path_cost += self.graph_api.get_edge_cost(self.current_node, next_node)
        self.current_node = next_node

    def deposit_pheromones_on_path(self) -> None:
        # TODO: check formula
        """Updates the pheromones along all the edges in the path

        Args:
            path (List[str]): The path followed by the ant
        """
        for i in range(len(self.path) - 1):
            u, v = self.path[i], self.path[i + 1]
            old_pheromone_value = self.graph_api.get_edge_pheromones(u, v)
            new_pheromone_value = old_pheromone_value + (1 / self.path_cost)
            self.graph_api.set_edge_pheromones(u, v, new_pheromone_value)
