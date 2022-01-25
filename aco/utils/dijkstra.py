"""
https://stackoverflow.com/a/61078380
"""


class Dijkstra:
    def __init__(self, G):
        self.graph = self.normalize_graph(G.graph)
        self.vertices = G.get_all_nodes()

    def find_route(self, start, end):
        unvisited = {n: float("inf") for n in self.vertices}
        unvisited[start] = 0  # set start vertex to 0
        visited = {}  # list of all visited nodes
        parents = {}  # predecessors
        while unvisited:
            min_vertex = min(unvisited, key=unvisited.get)  # get smallest distance
            for neighbour, _ in self.graph.get(min_vertex, {}).items():
                if neighbour in visited:
                    continue
                new_distance = unvisited[min_vertex] + self.graph[min_vertex].get(
                    neighbour, float("inf")
                )
                if new_distance < unvisited[neighbour]:
                    unvisited[neighbour] = new_distance
                    parents[neighbour] = min_vertex
            visited[min_vertex] = unvisited[min_vertex]
            unvisited.pop(min_vertex)
            if min_vertex == end:
                break
        return parents, visited

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

    def normalize_graph(self, input_graph):
        d = {}
        for node in input_graph:
            d[node] = input_graph[node]["neighbors"]
        return d

    def get_shortest_path(self, source, destination):
        if (
            source not in self.vertices or destination not in self.vertices
        ):  # Vertex does not exist
            return float("inf"), []
        p, cost = self.find_route(source, destination)
        path = self.generate_path(p, source, destination)
        return path  # cost[destination]
