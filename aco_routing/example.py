from aco_routing.utils.graph import Graph
from aco_routing.dijkstra import Dijkstra
from aco_routing.utils.simulator import Simulator
from aco_routing.aco import ACO

G = Graph()

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

aco = ACO(G)
dijkstra = Dijkstra(G)

aco_path = aco.find_shortest_path(source, destination)
aco_cost = G.compute_path_travel_time(aco_path)

dijkstra_path = dijkstra.find_shortest_path(source, destination)
dijkstra_cost = G.compute_path_travel_time(dijkstra_path)

print(f"ACO - path: {aco_path}, cost: {aco_cost}")
print(f"Dijkstra - path: {dijkstra_path}, cost: {dijkstra_cost}")

# Simulator(G).evaluate(source, destination, num_episodes=100, plot=True)
