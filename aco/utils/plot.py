import matplotlib.pyplot as plt


class PerfomancePlot:
    def __init__(self):
        self.graphs = []
        self.episodes = []
        self.antnet_paths, self.antnet_costs = [], []
        self.aco_paths, self.aco_costs = [], []
        self.dijkstra_paths, self.dijkstra_costs = [], []

    def show_plot(self):
        plt.plot(self.episodes, self.antnet_costs, label="AntNet")
        plt.plot(self.episodes, self.aco_costs, label="ACO")
        plt.plot(self.episodes, self.dijkstra_costs, label="Dijkstra")
        print(f"AntNet: {self.antnet_costs}")
        print(f"ACO: {self.aco_costs}")
        print(f"Dijkstra: {self.dijkstra_costs}")
        plt.xlabel("Episode")
        plt.ylabel("Shortest Path Cost")
        plt.title(f"{len(self.episodes)} Episodes")
        plt.legend()
        plt.show()
