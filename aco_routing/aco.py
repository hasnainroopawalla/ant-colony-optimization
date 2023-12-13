from dataclasses import dataclass
import random
from typing import List, Tuple
import networkx as nx

from aco_routing.ant import Ant
from aco_routing import graph_utils


@dataclass
class ACO:
    graph: nx.DiGraph
    evaporation_rate: float = 0.1

    def __post_init__(self):
        for edge in self.graph.edges:
            graph_utils.set_edge_pheromones(self.graph, edge[0], edge[1], 1.0)

    def _forward_ants(self, ants: List[Ant], max_iterations: int) -> None:
        """Deploys forward search ants in the graph

        Args:
            ants (List[Ant]): A List of Ants
            max_iterations (int): The maximum number of steps an ant is allowed is to take in order to reach the destination
                If it fails to find a path, it is tagged as unfit
        """
        for _, ant in enumerate(ants):
            for _ in range(max_iterations):
                if ant.reached_destination():
                    ant.is_fit = True
                    break
                ant.take_step()

    def _backward_ants(self, ants: List[Ant]) -> None:
        """Sends the ants (which are fit) backwards towards the source while they drop pheromones on the path

        Args:
            ants (List[Ant]): A List of Ants
        """
        for _, ant in enumerate(ants):
            if ant.is_fit:
                ant.deposit_pheromones_on_path()

    def _deploy_search_ants(
        self,
        source: str,
        destination: str,
        num_ants: int,
        cycles: int,
        random_spawns: bool,
        max_iterations: int = 50,
    ) -> None:
        """Deploys search ants which traverse the graph to find the shortest path

        Args:
            source (str): The source node in the graph
            destination (str): The destination node in the graph
            num_ants (int): The number of ants to be spawned
            cycles (int): The number of cycles of generating and deploying ants (forward and backward)
            random_spawns (bool): Indicates if the search ants should spawn at random nodes in the graph
            max_iterations (int, optional): The maximum number of steps an ant is allowed is to take in order to reach the destination,
                after which it is tagged as unfit
        """
        for _ in range(cycles):
            ants: List[Ant] = []
            for _ in range(num_ants):
                spawn_point = (
                    random.choice(graph_utils.get_all_nodes(self.graph))
                    if random_spawns
                    else source
                )
                ants.append(Ant(self.graph, spawn_point, destination))
            self._forward_ants(ants, max_iterations)
            self._evaporate_pheromones()
            self._backward_ants(ants)

    def _deploy_solution_ant(self, source: str, destination: str) -> Ant:
        """Deploys the final ant that greedily w.r.t. the pheromones finds the shortest path from the source to the destination

        Args:
            source (str): The source node in the graph
            destination (str): The destination node in the graph

        Returns:
            List[str]: The shortest path found by the ants (A list of node IDs)
        """
        # Spawn a pheromone-greedy ant
        ant = Ant(self.graph, source, destination, is_solution_ant=True)
        while not ant.reached_destination():
            ant.take_step()
        return ant

    def _evaporate_pheromones(self) -> None:
        """Evaporates the pheromone values of all the edges given the evaporation rate (rho)"""
        for edge in self.graph.edges:
            graph_utils.evaporate_edge_pheromones(
                self.graph, edge[0], edge[1], self.evaporation_rate
            )

    def find_shortest_path(
        self,
        source: str,
        destination: str,
        num_ants: int,
        max_iterations: int,
        cycles: int,
        random_spawn: bool = True,
    ) -> Tuple[List[str], float]:
        """Finds the shortest path from the source to the destination in the graph using the traditional Ant Colony Optimization technique

        Args:
            source (str): The source node in the graph
            destination (str): The destination node in the graph
            num_ants (int): The number of search ants to be deployed
            max_iterations (int): The maximum number of steps an ant is allowed is to take in order to reach the destination,
                after which it is tagged as unfit
            cycles (int): The number of cycles/waves of search ants to be deployed
            random_spawn (bool, optional): Indicates if the search ants should spawn at random nodes in the graph

        Returns:
            List[str]: The shortest path found by the ants (a list of node IDs)
            float: The total travel time of the shortest path
        """
        self._deploy_search_ants(
            source,
            destination,
            num_ants=num_ants,
            max_iterations=max_iterations,
            cycles=cycles,
            random_spawns=random_spawn,
        )
        solution_ant = self._deploy_solution_ant(source, destination)
        return solution_ant.path, solution_ant.path_cost
