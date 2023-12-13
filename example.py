import networkx as nx

from aco_routing import ACO
import matplotlib.pyplot as plt

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

# G.add_edge("2", "1", weight=1655)
# G.add_edge("2", "3", weight=3230)
# G.add_edge("2", "11", weight=2367)
# G.add_edge("2", "10", weight=1368)
# G.add_edge("3", "2", weight=3230)
# G.add_edge("3", "10", weight=3230)
# G.add_edge("4", "3", weight=1213)
# G.add_edge("5", "3", weight=2472)
# G.add_edge("5", "6", weight=152)
# G.add_edge("6", "7", weight=2801)
# G.add_edge("6", "20", weight=1319)
# G.add_edge("7", "6", weight=2801)
# G.add_edge("7", "8", weight=867)
# G.add_edge("7", "19", weight=834)
# G.add_edge("9", "8", weight=201)
# G.add_edge("9", "10", weight=857)
# G.add_edge("9", "19", weight=1203)
# G.add_edge("10", "2", weight=1368)
# G.add_edge("10", "3", weight=2541)
# G.add_edge("10", "9", weight=857)
# G.add_edge("11", "2", weight=2367)
# G.add_edge("11", "12", weight=2368)
# G.add_edge("11", "15", weight=1409)
# G.add_edge("11", "19", weight=1653)
# G.add_edge("12", "13", weight=711)
# G.add_edge("12", "14", weight=541)
# G.add_edge("15", "11", weight=1409)
# G.add_edge("15", "14", weight=1678)
# G.add_edge("15", "16", weight=2144)
# G.add_edge("15", "18", weight=1487)
# G.add_edge("16", "15", weight=2144)
# G.add_edge("16", "17", weight=1585)
# G.add_edge("16", "23", weight=2557)
# G.add_edge("17", "16", weight=1585)
# G.add_edge("17", "18", weight=477)
# G.add_edge("17", "25", weight=156)
# G.add_edge("18", "15", weight=1487)
# G.add_edge("18", "17", weight=477)
# G.add_edge("18", "19", weight=870)
# G.add_edge("19", "20", weight=3977)
# G.add_edge("19", "18", weight=870)
# G.add_edge("19", "11", weight=1653)
# G.add_edge("19", "9", weight=1203)
# G.add_edge("19", "7", weight=834)
# G.add_edge("20", "21", weight=2945)
# G.add_edge("20", "23", weight=3054)
# G.add_edge("20", "19", weight=3977)
# G.add_edge("20", "6", weight=1319)
# G.add_edge("23", "22", weight=2561)
# G.add_edge("23", "16", weight=2557)
# G.add_edge("24", "23", weight=984)
# G.add_edge("24", "25", weight=2519)

source = "A"  # "4"
destination = "D"  # "1"

# aco = ACO(G)

# aco_path, aco_cost = aco.find_shortest_path(
#     source, destination, num_ants=100, max_iterations=50, cycles=100
# )


# dijkstra_path = nx.dijkstra_path(G, source, destination)
# dijkstra_cost = nx.path_weight(G, dijkstra_path, "cost")

# print(aco_path, aco_cost)
# print(dijkstra_path, dijkstra_cost)


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
# # edge weight labels
# edge_labels = nx.get_edge_attributes(G, "pheromones")
# nx.draw_networkx_edge_labels(G, pos, edge_labels)

# ax = plt.gca()
# ax.margins(0.08)
# plt.axis("off")
# plt.tight_layout()
# plt.show()
