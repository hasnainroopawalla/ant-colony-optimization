from dataclasses import dataclass
from typing import List
from aco_routing.utils.graph import Graph
from aco_routing.utils.ant import Ant


@dataclass
class ACO:
    graph: Graph

    def _deploy_search_ants(
        self, source: str, destination: str, cycles: int = 100, max_iterations: int = 50
    ) -> None:
        """Deploys search ants which traverse the graph to find the shortest path.

        Args:
            source (str): The source node in the graph.
            destination (str): The destination node in the graph.
            cycles (int, optional): The number of cycles of generating and deploying ants (forward and backward). Defaults to 100.
            max_iterations (int, optional): The maximum number of steps an ant is allowed is to take in order to reach the destination.
                If it fails to find a path, it is tagged as unfit. Defaults to 50.
        """
        for cycle in range(cycles):
            ants: List[Ant] = [
                Ant(self.graph, source, destination),
                Ant(self.graph, source, destination),
            ]

            # Forward ants.
            for idx, ant in enumerate(ants):
                for i in range(max_iterations):
                    if ant.reached_destination():
                        ant.is_fit = True
                        break
                    ant.take_step()
            self.graph.evaporate()

            # Backward ants.
            for idx, ant in enumerate(ants):
                if ant.is_fit:
                    self.graph.deposit_pheromones_along_path(ant.path)

    def _deploy_solution_ant(self, source: str, destination: str) -> List[str]:
        """Deploys the final ant that greedily w.r.t. the phermones finds the shortest path from the source to the destination.

        Args:
            source (str): The source node in the graph.
            destination (str): The destination node in the graph.

        Returns:
            List[str]: The shortest path found by the ants (A list of node IDs).
        """
        path = [source]
        current_node = source
        visited_nodes = set()
        while current_node != destination:
            visited_nodes.add(current_node)
            pheros = self.graph.get_node_edges(current_node)
            max_neighbor = max(pheros, key=lambda k: pheros[k].pheromones)
            path.append(max_neighbor)
            current_node = max_neighbor
        return path

    def find_shortest_path(self, source: str, destination: str) -> List[str]:
        """Finds the shortest path from the source to the destination in the graph using the traditional Ant Colony Optimization technique.

        Args:
            source (str): The source node in the graph.
            destination (str): The destination node in the graph.

        Returns:
            List[str]: The shortest path found by the ants (A list of node IDs).
        """
        self._deploy_search_ants(source, destination)
        shortest_path = self._deploy_solution_ant(source, destination)
        return shortest_path
