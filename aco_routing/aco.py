from dataclasses import dataclass, field
import random
from typing import List, Tuple
import networkx as nx

from aco_routing.ant import Ant
from aco_routing.graph_api import GraphApi


@dataclass
class ACO:
    graph: nx.DiGraph
    # Maximum number of steps an ant is allowed is to take in order to reach the destination
    ant_max_steps: int
    # Number of cycles/waves of search ants to be deployed
    num_iterations: int
    # Indicates if the search ants should spawn at random nodes in the graph
    ant_random_spawn: bool = True
    # Evaporation rate (rho)
    evaporation_rate: float = 0.1
    # Pheromone bias
    alpha: float = 0.7
    # Edge cost bias
    beta: float = 0.3
    # Search ants
    search_ants: List[Ant] = field(default_factory=list)

    def __post_init__(self):
        # Initialize the Graph API
        self.graph_api = GraphApi(self.graph, self.evaporation_rate)
        # Initialize all edges of the graph with a pheromone value of 1.0
        for edge in self.graph.edges:
            self.graph_api.set_edge_pheromones(edge[0], edge[1], 1.0)

    def _deploy_forward_search_ants(self) -> None:
        """Deploy forward search ants in the graph"""
        for ant in self.search_ants:
            for _ in range(self.ant_max_steps):
                if ant.reached_destination():
                    ant.is_fit = True
                    break
                ant.take_step()

    def _deploy_backward_search_ants(self) -> None:
        """Deploy fit search ants back towards their source node while dropping pheromones on the path"""
        for ant in self.search_ants:
            if ant.is_fit:
                ant.deposit_pheromones_on_path()

    def _deploy_search_ants(
        self,
        source: str,
        destination: str,
        num_ants: int,
    ) -> None:
        """Deploy search ants that traverse the graph to find the shortest path

        Args:
            source (str): The source node in the graph
            destination (str): The destination node in the graph
            num_ants (int): The number of ants to be spawned
        """
        for _ in range(self.num_iterations):
            self.search_ants.clear()

            for _ in range(num_ants):
                spawn_point = (
                    random.choice(self.graph_api.get_all_nodes())
                    if self.ant_random_spawn
                    else source
                )

                ant = Ant(
                    self.graph_api,
                    spawn_point,
                    destination,
                    alpha=self.alpha,
                    beta=self.beta,
                )
                self.search_ants.append(ant)

            self._deploy_forward_search_ants()
            self._deploy_backward_search_ants()

    def _deploy_solution_ant(self, source: str, destination: str) -> Ant:
        """Deploy the pheromone-greedy solution to find the shortest path

        Args:
            source (str): The source node in the graph
            destination (str): The destination node in the graph

        Returns:
            Ant: The solution ant with the computed shortest path and cost
        """
        ant = Ant(
            self.graph_api,
            source,
            destination,
            is_solution_ant=True,
        )
        while not ant.reached_destination():
            ant.take_step()
        return ant

    def find_shortest_path(
        self,
        source: str,
        destination: str,
        num_ants: int,
    ) -> Tuple[List[str], float]:
        """Finds the shortest path from the source to the destination in the graph

        Args:
            source (str): The source node in the graph
            destination (str): The destination node in the graph
            num_ants (int): The number of search ants to be deployed

        Returns:
            List[str]: The shortest path found by the ants
            float: The cost of the computed shortest path
        """
        self._deploy_search_ants(
            source,
            destination,
            num_ants,
        )
        solution_ant = self._deploy_solution_ant(source, destination)
        return solution_ant.path, solution_ant.path_cost
