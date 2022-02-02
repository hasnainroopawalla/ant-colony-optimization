from dataclasses import dataclass
import random
from typing import List, Tuple

from aco_routing.utils.graph import Graph
from aco_routing.utils.ant import Ant


@dataclass
class ACO:
    graph: Graph

    def _forward_ants(self, ants: List[Ant], max_iterations: int) -> None:
        """Deploys forward search ants in the graph.

        Args:
            ants (List[Ant]): A List of Ants.
            max_iterations (int, optional): The maximum number of steps an ant is allowed is to take in order to reach the destination.
                If it fails to find a path, it is tagged as unfit. Defaults to 50.
        """
        for idx, ant in enumerate(ants):
            for i in range(max_iterations):
                if ant.reached_destination():
                    ant.is_fit = True
                    break
                ant.take_step()

    def _backward_ants(self, ants: List[Ant]) -> None:
        """Sends the ants (which are fit) backwards towards the source while they drop pheromones on the path.

        Args:
            ants (List[Ant]): A List of Ants.
        """
        for idx, ant in enumerate(ants):
            if ant.is_fit:
                self.graph.deposit_pheromones_along_path(ant.path)

    def _deploy_search_ants(
        self,
        source: str,
        destination: str,
        num_ants: int,
        random_spawns: bool = False,
        cycles: int = 100,
        max_iterations: int = 50,
    ) -> None:
        """Deploys search ants which traverse the graph to find the shortest path.

        Args:
            source (str): The source node in the graph.
            destination (str): The destination node in the graph.
            num_ants (int): The number of ants to be spawned.
            random_spawns (bool): A flag to determine if the ants should be spawned at random nodes or always at the source node.
            cycles (int, optional): The number of cycles of generating and deploying ants (forward and backward). Defaults to 100.
            max_iterations (int, optional): The maximum number of steps an ant is allowed is to take in order to reach the destination.
                If it fails to find a path, it is tagged as unfit. Defaults to 50.
        """
        for cycle in range(cycles):
            ants: List[Ant] = []
            for _ in range(num_ants):
                spawn_point = (
                    random.choice(self.graph.get_all_nodes())
                    if random_spawns
                    else source
                )
                ants.append(Ant(self.graph, spawn_point, destination))
            self._forward_ants(ants, max_iterations)
            self.graph.evaporate()
            self._backward_ants(ants)

    def _deploy_solution_ant(self, source: str, destination: str) -> List[str]:
        """Deploys the final ant that greedily w.r.t. the pheromones finds the shortest path from the source to the destination.

        Args:
            source (str): The source node in the graph.
            destination (str): The destination node in the graph.

        Returns:
            List[str]: The shortest path found by the ants (A list of node IDs).
        """
        # Spawn an ant which favors pheromone values over edge costs.
        ant = Ant(self.graph, source, destination, alpha=0.99, beta=0.01)
        while not ant.reached_destination():
            ant.take_step()
        return ant.path

    def find_shortest_path(
        self, source: str, destination: str
    ) -> Tuple[List[str], float]:
        """Finds the shortest path from the source to the destination in the graph using the traditional Ant Colony Optimization technique.

        Args:
            source (str): The source node in the graph.
            destination (str): The destination node in the graph.

        Returns:
            List[str]: The shortest path found by the ants (A list of node IDs).
            float: The total travel time of the shortest path.
        """
        self._deploy_search_ants(source, destination, num_ants=20, random_spawns=True)
        shortest_path = self._deploy_solution_ant(source, destination)
        return shortest_path, self.graph.compute_path_travel_time(shortest_path)
