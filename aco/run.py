from graph import Graph
from utils.ant import Ant
from utils.dijkstra import Dijkstra
from utils.plot import PerfomancePlot
from utils.antnet import runAntNet
from utils.ant import runACO

G = Graph()

G.add_node("A")
G.add_node("B")

# print(G.nodes)

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

Ant.graph = G

source = "A"
destination = "D"
iterations = 20
num_episodes = 100

# ant_paths = []

# ants = [
#     Ant(G, source, destination),
#     Ant(G, source, destination),
#     Ant(G, source, destination),
#     Ant(G, source, destination),
#     Ant(G, source, destination)
# ]

# for ant in ants:  # this should happen in parallel processes
#     for i in range(iterations):
#         if ant.take_step():
#             ant_paths.append(ant.get_path_taken())
#             break

# for path_taken in ant_paths:
#     print("Path taken")
#     print(path_taken)
#     print()
#     for path in path_taken:
#         G.add_phero(path['start'], path['end'])

"""
Insert AntNet, ACO and Dijkstra function calls in this loop:
"""
P = PerfomancePlot()
aco_path = runACO(G, source, destination)
# dijkstra_path = Dijkstra(G).get_shortest_path(source=source, destination=destination)

print(f"ACO: {aco_path}")
# print(f"Dij: {dijkstra_path}")

# antnet_dj_same_cost_counter = 0

# for episode in range(1, num_episodes+1):

#     antnet_path = runAntNet(G, source, destination, 0.6, 0.3, 0.7) # Replace with -> antnet_path = antnet(G, source, destination)
#     aco_path = runACO(G, source, destination)
#     dijkstra_path = Dijkstra(G).get_shortest_path(source=source, destination=destination)

#     P.graphs.append(G)
#     P.antnet_paths.append(antnet_path)
#     ant_net_cost = G.get_path_cost(antnet_path)
#     P.antnet_costs.append(ant_net_cost)

#     P.aco_paths.append(aco_path)
#     P.aco_costs.append(G.get_path_cost(aco_path))

#     P.dijkstra_paths.append(dijkstra_path)
#     dj_cost = G.get_path_cost(dijkstra_path)
#     P.dijkstra_costs.append(dj_cost)

#     P.episodes.append(episode)

#     G.update_graph(max_delta_time=1, update_probability=0.7)
#     # G.display_graph()

#     if(dj_cost == ant_net_cost):
#         antnet_dj_same_cost_counter += 1

# P.show_plot()

# print("Number of times AntNet and DJ performed same = {}".format(antnet_dj_same_cost_counter))
