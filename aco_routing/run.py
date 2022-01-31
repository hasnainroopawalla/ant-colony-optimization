from aco_routing.utils.graph import Graph
from aco_routing.utils.dijkstra import Dijkstra
from aco_routing.utils.eval import Evaluator, Episode
from aco_routing.aco import ACO

G = Graph()

# G.add_edge('A','B', 4)
# G.add_edge('B','C', 6)
# G.add_edge('C','D', 9)
# G.add_edge('D','A', 2)
# G.add_edge('B','D', 2)

G.add_edge("A", "B", 2)
G.add_edge("B", "C", 2)
G.add_edge("A", "H", 2)
G.add_edge("H", "G", 2)
G.add_edge("C", "F", 1)
G.add_edge("F", "G", 1)
G.add_edge("G", "F", 1)
G.add_edge("F", "C", 1)
G.add_edge("C", "D", 10)
G.add_edge("E", "D", 2)
G.add_edge("G", "E", 2)

source = "A"
destination = "D"
num_episodes = 100

Eval = Evaluator()

for episode in range(1, num_episodes + 1):
    aco_path = ACO(G).find_shortest_path(source, destination)
    dijkstra_path = Dijkstra(G).find_shortest_path(source, destination)

    aco_cost = G.compute_path_travel_time(aco_path)
    dijkstra_cost = G.compute_path_travel_time(dijkstra_path)

    Eval.episodes.append(
        Episode(episode, G, aco_path, dijkstra_path, aco_cost, dijkstra_cost)
    )

    G.update_edges_travel_time(max_delta_time=1, update_probability=0.7)


Eval.show_plot()
