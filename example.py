import networkx as nx

from aco_routing import ACO
import matplotlib.pyplot as plt

G = nx.DiGraph()

# G.add_edge("A", "B", cost=2)
# G.add_edge("B", "C", cost=2)
# G.add_edge("A", "H", cost=2)
# G.add_edge("H", "G", cost=2)
# G.add_edge("C", "F", cost=1)
# G.add_edge("F", "G", cost=1)
# G.add_edge("G", "F", cost=1)
# G.add_edge("F", "C", cost=1)
# G.add_edge("C", "D", cost=10)
# G.add_edge("E", "D", cost=2)
# G.add_edge("G", "E", cost=2)

G.add_edge("2", "1", cost=1655)
G.add_edge("2", "3", cost=3230)
G.add_edge("2", "11", cost=2367)
G.add_edge("2", "10", cost=1368)
G.add_edge("3", "2", cost=3230)
G.add_edge("3", "10", cost=3230)
G.add_edge("4", "3", cost=1213)
G.add_edge("5", "3", cost=2472)
G.add_edge("5", "6", cost=152)
G.add_edge("6", "7", cost=2801)
G.add_edge("6", "20", cost=1319)
G.add_edge("7", "6", cost=2801)
G.add_edge("7", "8", cost=867)
G.add_edge("7", "19", cost=834)
G.add_edge("9", "8", cost=201)
G.add_edge("9", "10", cost=857)
G.add_edge("9", "19", cost=1203)
G.add_edge("10", "2", cost=1368)
G.add_edge("10", "3", cost=2541)
G.add_edge("10", "9", cost=857)
G.add_edge("11", "2", cost=2367)
G.add_edge("11", "12", cost=2368)
G.add_edge("11", "15", cost=1409)
G.add_edge("11", "19", cost=1653)
G.add_edge("12", "13", cost=711)
G.add_edge("12", "14", cost=541)
G.add_edge("15", "11", cost=1409)
G.add_edge("15", "14", cost=1678)
G.add_edge("15", "16", cost=2144)
G.add_edge("15", "18", cost=1487)
G.add_edge("16", "15", cost=2144)
G.add_edge("16", "17", cost=1585)
G.add_edge("16", "23", cost=2557)
G.add_edge("17", "16", cost=1585)
G.add_edge("17", "18", cost=477)
G.add_edge("17", "25", cost=156)
G.add_edge("18", "15", cost=1487)
G.add_edge("18", "17", cost=477)
G.add_edge("18", "19", cost=870)
G.add_edge("19", "20", cost=3977)
G.add_edge("19", "18", cost=870)
G.add_edge("19", "11", cost=1653)
G.add_edge("19", "9", cost=1203)
G.add_edge("19", "7", cost=834)
G.add_edge("20", "21", cost=2945)
G.add_edge("20", "23", cost=3054)
G.add_edge("20", "19", cost=3977)
G.add_edge("20", "6", cost=1319)
G.add_edge("23", "22", cost=2561)
G.add_edge("23", "16", cost=2557)
G.add_edge("24", "23", cost=984)
G.add_edge("24", "25", cost=2519)

source = "19"  # "4"
destination = "1"  # "1"

aco = ACO(G)

aco_path, aco_cost = aco.find_shortest_path(
    source, destination, num_ants=100, max_iterations=50, cycles=100
)


dijkstra_path = nx.dijkstra_path(G, source, destination)
dijkstra_cost = nx.path_weight(G, dijkstra_path, "cost")

print(f"ACO - path: {aco_path}, cost: {aco_cost}")
print(f"Dijkstra - path: {dijkstra_path}, cost: {dijkstra_cost}")


# for edge in G.edges:
#     source, destination = edge[0], edge[1]
#     G[source][destination]["pheromones"] = round(G[source][destination]["pheromones"])

# pos = nx.spring_layout(G, seed=2)
# nx.draw(G, pos, width=4)

# nx.draw_networkx_nodes(G, pos, node_size=700)

# # nx.draw_networkx_edges(G, pos, width=2)
# nx.draw_networkx_edges(
#     G, pos, edgelist=list(zip(aco_path, aco_path[1:])), edge_color="r", width=4
# )

# # node labels
# nx.draw_networkx_labels(G, pos, font_size=20)
# # edge cost labels
# edge_labels = nx.get_edge_attributes(G, "pheromones")
# nx.draw_networkx_edge_labels(G, pos, edge_labels)

# ax = plt.gca()
# ax.margins(0.08)
# plt.axis("off")
# plt.tight_layout()
# plt.show()
