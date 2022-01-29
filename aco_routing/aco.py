from dataclasses import dataclass
from typing import List
from aco_routing.utils.graph import Graph
from aco_routing.utils.ant import Ant


@dataclass
class ACO:
    graph: Graph

    def find_shortest_path(self, source: str, destination: str, cycles: int = 50):
        max_iterations = 50

        for cycle in range(cycles):
            ants: List[Ant] = [
                Ant(self.graph, source, destination),
                Ant(self.graph, source, destination),
            ]
            print("-----")
            print(f"Cycle {cycle}")

            # Forward ants
            for idx, ant in enumerate(ants):
                print(f"Ant {idx}")
                for i in range(max_iterations):
                    if ant.reached_destination():
                        print(ant.path)
                        break
                    ant.take_step()

            self.graph.evaporate()
            print(self.graph)
            print("--- BACKWARD ---")
            # Backward ants
            for idx, ant in enumerate(ants):
                print(f"Ant {idx}")
                print(ant.path)
                self.graph.deposit_pheromones_along_path(ant.path)

        print()
        print()
        print(self.graph)
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
