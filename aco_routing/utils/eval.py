from dataclasses import dataclass, field
from typing import List

import matplotlib.pyplot as plt
from aco_routing.utils.graph import Graph


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
    episodes: List[Episode] = field(default_factory=list)

    def show_plot(self):
        aco_costs, dijsktra_costs = [], []
        for episode in self.episodes:
            aco_costs.append(episode.aco_cost)
            dijsktra_costs.append(episode.dijkstra_cost)

        plt.scatter(aco_costs, dijsktra_costs)
        # plt.title(f"{len(self.episodes)} Episodes")
        # plt.legend()
        plt.show()
