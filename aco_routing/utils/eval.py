from dataclasses import dataclass, field
from typing import List
import matplotlib.pyplot as plt

from aco_routing.utils.graph import Graph
from aco_routing.aco import ACO
from aco_routing.utils.dijkstra import Dijkstra


@dataclass
class Episode:
    episode_id: float
    graph: Graph
    aco_path: List[str]
    dijkstra_path: List[str]
    aco_cost: float
    dijkstra_cost: float


@dataclass
class Evaluator:
    """This class can be used to evaluate the performance of the algorithm (ACO/AntNet) with a baseline Dijkstra's Algorithm.

    Args:
        graph (Graph): The Graph object.
        episodes (List[Episode]): A List of all the episodes which were saved during the evaluation.
    """

    graph: Graph
    episodes: List[Episode] = field(default_factory=list)

    def show_evaluation_plot(self):
        aco_costs, dijkstra_costs = [], []
        for episode in self.episodes:
            aco_costs.append(episode.aco_cost)
            dijkstra_costs.append(episode.dijkstra_cost)

        plt.scatter(dijkstra_costs, aco_costs, s=4)
        plt.xlabel("Dijkstra Cost")
        plt.ylabel("ACO Cost")
        plt.title("Dijkstra Cost vs ACO Cost")
        plt.show()

    def compute_mse(self) -> float:
        summation = 0.0
        for episode in self.episodes:
            summation += (episode.dijkstra_cost - episode.aco_cost) ** 2
        return summation / len(self.episodes)

    def evaluate(
        self, source: str, destination: str, num_episodes: int, plot: bool = True
    ) -> None:
        aco = ACO(self.graph)
        dijkstra = Dijkstra(self.graph)
        for episode in range(1, num_episodes + 1):
            aco_path = aco.find_shortest_path(source, destination)
            dijkstra_path = dijkstra.find_shortest_path(source, destination)

            aco_cost = self.graph.compute_path_travel_time(aco_path)
            dijkstra_cost = self.graph.compute_path_travel_time(dijkstra_path)

            self.episodes.append(
                Episode(
                    episode,
                    self.graph,
                    aco_path,
                    dijkstra_path,
                    aco_cost,
                    dijkstra_cost,
                )
            )

            self.graph.update_edges_travel_time(
                max_delta_time=1, update_probability=0.7
            )

        print(f"Mean Squared Error: {self.compute_mse()}")
        if plot:
            self.show_evaluation_plot()
