import networkx as nx
from aco_routing import ACO


G = nx.DiGraph()

G.add_edge("A", "B", cost=2)
G.add_edge("B", "C", cost=2)
G.add_edge("A", "H", cost=2)
G.add_edge("H", "G", cost=2)
G.add_edge("C", "F", cost=1)
G.add_edge("F", "G", cost=1)
G.add_edge("G", "F", cost=1)
G.add_edge("F", "C", cost=1)
G.add_edge("C", "D", cost=10)
G.add_edge("E", "D", cost=2)
G.add_edge("G", "E", cost=2)

source = "A"
destination = "D"

dijkstra_path = nx.dijkstra_path(G, source, destination)
dijkstra_cost = nx.path_weight(G, dijkstra_path, "cost")

aco = ACO(G, ant_max_steps=100, num_iterations=100, ant_random_spawn=True)

aco_path, aco_cost = aco.find_shortest_path(
    source,
    destination,
    num_ants=100,
)

print(f"Dijkstra - path: {dijkstra_path}, cost: {dijkstra_cost}")
print(f"ACO - path: {aco_path}, cost: {aco_cost}")

aco.graph_api.visualize_graph(aco_path)
