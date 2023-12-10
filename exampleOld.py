from aco_routing import Graph, Dijkstra, ACO

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

aco_path, aco_cost = aco.find_shortest_path(
    source, destination, num_ants=100, max_iterations=50, cycles=100
)
dijkstra_path, dijkstra_cost = dijkstra.find_shortest_path(source, destination)

print(f"ACO - path: {aco_path}, cost: {aco_cost}")
print(f"Dijkstra - path: {dijkstra_path}, cost: {dijkstra_cost}")
