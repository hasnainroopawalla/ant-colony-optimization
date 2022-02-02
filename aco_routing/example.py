from aco_routing.utils.graph import Graph
from aco_routing.dijkstra import Dijkstra
from aco_routing.utils.simulator import Simulator
from aco_routing.aco import ACO

graph = Graph()

graph.add_edge("A", "B", 2)
graph.add_edge("B", "C", 2)
graph.add_edge("A", "H", 2)
graph.add_edge("H", "G", 2)
graph.add_edge("C", "F", 1)
graph.add_edge("F", "G", 1)
graph.add_edge("G", "F", 1)
graph.add_edge("F", "C", 1)
graph.add_edge("C", "D", 10)
graph.add_edge("E", "D", 2)
graph.add_edge("G", "E", 2)

source = "A"
destination = "D"

dijkstra = Dijkstra(graph)
aco = ACO(graph)

dijkstra_path, dijkstra_cost = dijkstra.find_shortest_path(source, destination)
aco_path, aco_cost = aco.find_shortest_path(source, destination)

print(f"ACO - path: {aco_path}, cost: {aco_cost}")
print(f"Dijkstra - path: {dijkstra_path}, cost: {dijkstra_cost}")

Simulator(graph).simulate(source, destination, num_episodes=100, plot=True)
