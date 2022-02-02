from dataclasses import dataclass, field
from typing import List
import matplotlib.pyplot as plt
from tqdm import tqdm

from aco_routing.utils.graph import Graph
from aco_routing.aco import ACO
from aco_routing.dijkstra import Dijkstra


@dataclass
class Episode:
    episode_id: float
    graph: Graph
    aco_path: List[str]
    dijkstra_path: List[str]
    aco_cost: float
    dijkstra_cost: float


@dataclass
class Simulator:
    """This class can be used to simulate and evaluate the performance of the candidate algorithm (ACO) with a baseline Dijkstra's Algorithm.
    It simulates a real-life city, where the traffic conditions change every episode in a conditionally stochastic manner.
    The ants continue to find the shortest path even after the traffic conditions change.

    Args:
        graph (Graph): The Graph object.
        episodes (List[Episode]): A List of all the episodes which were saved during the simulation.
    """

    graph: Graph
    episodes: List[Episode] = field(default_factory=list)

    def show_simulation_plot(self) -> None:
        """Displays a plot to compare the path costs of the candidate algorithm with the baseline Dijkstra's algorithm across all episodes.
        """
        dijkstra_costs, aco_costs = [], []
        for episode in self.episodes:
            dijkstra_costs.append(episode.dijkstra_cost)
            aco_costs.append(episode.aco_cost)

        plt.scatter(dijkstra_costs, aco_costs, s=4)
        plt.xlabel("Dijkstra Cost")
        plt.ylabel("ACO Cost")
        plt.title(f"Dijkstra Cost vs ACO Cost ({len(self.episodes)} episodes)")
        plt.show()

    def compute_mse(self) -> float:
        """Computes the Mean Squared Error between the baseline and candidate algorithm path costs.
        A low value indicates very good performance.

        Returns:
            float: The Mean Squared Error value.
        """
        summation = 0.0
        for episode in self.episodes:
            summation += (episode.dijkstra_cost - episode.aco_cost) ** 2
        mse = summation / len(self.episodes)
        print(f"Mean Squared Error: {mse}")
        return mse

    def simulate(
        self, source: str, destination: str, num_episodes: int, plot: bool = True
    ) -> None:
        """Simulates and Evaluates the candidate algorithm across several episodes.

        Args:
            source (str): The source node.
            destination (str): The destination node.
            num_episodes (int): The number of episodes used in the simulation.
            plot (bool, optional): A flag which determines if the plot should be displayed. Defaults to True.
        """
        print("-" * 5)
        print(f"Simulating {num_episodes} episodes..")
        dijkstra = Dijkstra(self.graph)
        aco = ACO(self.graph)
        for episode in tqdm(range(1, num_episodes + 1)):
            dijkstra_path, dijkstra_cost = dijkstra.find_shortest_path(
                source, destination
            )
            aco_path, aco_cost = aco.find_shortest_path(source, destination)

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

        self.compute_mse()
        if plot:
            self.show_simulation_plot()
