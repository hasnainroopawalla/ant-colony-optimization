import networkx as nx

from aco_routing import ACO


G = nx.DiGraph()

G.add_edge("A", "B", weight=2)
G.add_edge("B", "C", weight=2)
G.add_edge("A", "H", weight=2)
G.add_edge("H", "G", weight=2)
G.add_edge("C", "F", weight=1)
G.add_edge("F", "G", weight=1)
G.add_edge("G", "F", weight=1)
G.add_edge("F", "C", weight=1)
G.add_edge("C", "D", weight=10)
G.add_edge("E", "D", weight=2)
G.add_edge("G", "E", weight=2)

source = "A"
destination = "D"

aco = ACO(G)

aco_path, aco_cost = aco.find_shortest_path(
    source, destination, num_ants=100, max_iterations=50, cycles=100
)
