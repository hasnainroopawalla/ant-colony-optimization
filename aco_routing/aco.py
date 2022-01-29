from dataclasses import dataclass
from typing import List
from aco_routing.utils.graph import Graph
from aco_routing.utils.ant import Ant


@dataclass
class ACO:
    graph: Graph

    def find_shortest_path(self, source: str, destination: str, cycles: int = 100):
        max_iterations = 50

        for cycle in range(cycles):
            ants: List[Ant] = [
                Ant(self.graph, source, destination),
                Ant(self.graph, source, destination),
            ]

            # Forward ants
            for idx, ant in enumerate(ants):
                for i in range(max_iterations):
                    if ant.reached_destination():
                        ant.is_fit = True
                        break
                    ant.take_step()
            self.graph.evaporate()

            # Backward ants
            for idx, ant in enumerate(ants):
                if ant.is_fit:
                    self.graph.deposit_pheromones_along_path(ant.path)

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
