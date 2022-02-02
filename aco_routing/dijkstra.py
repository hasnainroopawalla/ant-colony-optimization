from dataclasses import dataclass
from typing import List, Tuple

from aco_routing.utils.graph import Graph


@dataclass
class Dijkstra:
    """Reference: https://stackoverflow.com/a/61078380
    """

    graph: Graph

    def __post_init__(self) -> None:
        self.dijkstra_graph = self.graph.normalize_graph_for_dijkstra()
        self.vertices = self.graph.get_all_nodes()

    def find_route(self, start, end):
        unvisited = {n: float("inf") for n in self.vertices}
        unvisited[start] = 0  # set start vertex to 0
        visited = {}  # list of all visited nodes
        parents = {}  # predecessors
        while unvisited:
            min_vertex = min(unvisited, key=unvisited.get)  # get smallest distance
            for neighbor, _ in self.dijkstra_graph.get(min_vertex, {}).items():
                if neighbor in visited:
                    continue
                new_distance = unvisited[min_vertex] + self.dijkstra_graph[
                    min_vertex
                ].get(neighbor, float("inf"))
                if new_distance < unvisited[neighbor]:
                    unvisited[neighbor] = new_distance
                    parents[neighbor] = min_vertex
            visited[min_vertex] = unvisited[min_vertex]
            unvisited.pop(min_vertex)
            if min_vertex == end:
                break
        return parents

    def generate_path(self, parents, start, end):
        path = [end]
        while True:
            if not parents:
                return []
            key = parents[path[0]]
            path.insert(0, key)
            if key == start:
                break
        return path

    def find_shortest_path(self, source, destination) -> Tuple[List[str], float]:
        p = self.find_route(source, destination)
        path = self.generate_path(p, source, destination)
        return path, self.graph.compute_path_travel_time(path)
