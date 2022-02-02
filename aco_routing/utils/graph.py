from dataclasses import dataclass, field
import random
from typing import Dict, List, Optional


@dataclass
class Edge:
    """An edge of the graph.

    Args:
        travel_time (float): The time it takes to travel the edge. A high value indicates more traffic.
        pheromones: (float): The amount of pheromones deposited by the ants on the edge. Defaults to 1.0.
    """

    travel_time: float
    pheromones: float = 1.0


@dataclass
class Node:
    """A node in the graph.

    Args:
        id (str): The unique ID of the node.
        edges (Dict[str, Edge]): Stores all the outgoing edges from this node.
    """

    id: str
    edges: Dict[str, Edge] = field(default_factory=dict)

    def add_edge(self, destination: str, travel_time: float):
        self.edges[destination] = Edge(travel_time)


@dataclass
class Graph:
    """A Directed Graph made up of Nodes and Edges.

    Args:
        graph (Dict[str, Node]): The actual graph.
        evaporation_rate (float): The evaporation rate of the pheromones. Defaults to 0.1
    """

    graph: Dict[str, Node] = field(default_factory=dict)
    evaporation_rate: float = 0.1

    def node_exists(self, id: str) -> bool:
        """Checks if the node exists in the graph.

        Args:
            id (str): The ID of the node.

        Returns:
            bool: True if the node exists in the graph, else False.
        """
        return id in self.graph

    def edge_exists(self, source: str, destination: str) -> bool:
        """Checks if the edge exists in the graph.

        Args:
            source (str): The ID of the source node.
            destination (str): The ID of the destination node.

        Returns:
            bool: True if the edge exists in the graph, else False.
        """
        if not self.node_exists(source) or not self.node_exists(destination):
            return False
        return destination in self.graph[source].edges.keys()

    def add_node(self, id: str) -> None:
        """Add a node to the graph.

        Args:
            id (str): The ID of the node to be added to the graph.
        """
        self.graph[id] = Node(id)

    def add_edge(self, source: str, destination: str, travel_time: float) -> None:
        """Add an edge connecting 2 nodes in the graph.

        Args:
            source (str): The source node of the edge.
            destination (str): The destination node of the edge.
            travel_time (float): The amount of time it takes to travel that edge.
        """
        if not self.node_exists(source):
            self.add_node(source)
        if not self.node_exists(destination):
            self.add_node(destination)
        self.graph[source].add_edge(destination, travel_time)

    def get_all_nodes(self) -> List[str]:
        """Returns a List of all the nodes in the graph.

        Returns:
            List[str]: A List of all the nodes in the graph.
        """
        return list(self.graph.keys())

    def get_all_edges(self) -> List[Edge]:
        """Returns all the edges in the graph.

        Returns:
            List[Tuple[str, str, float]]: A List of Tuples -> (source, destination, travel_time)
        """
        edges: List[Edge] = []
        for source in self.graph:
            for destination in self.graph[source].edges:
                edges.append(self.get_edge(source, destination))
        return edges

    def get_edge(self, source: str, destination: str) -> Edge:
        """Returns the Edge if it exists in the graph.

        Args:
            source (str): The ID of the source node.
            destination (str): The ID of the destination node.

        Returns:
            Edge: The Edge object.
        """
        return self.graph[source].edges[destination]

    def get_node_edges(self, id: str) -> Dict[str, Edge]:
        """Returns all the edges of a node.

        Args:
            id (str): The ID of the node.

        Returns:
            Dict[str, Edge]: The outgoing edges of the node.
        """
        return self.graph[id].edges

    def get_node(self, id: str) -> Optional[Node]:
        """Returns the Node if it exists in the graph.

        Args:
            id (str): The ID of the Node.

        Returns:
            Optional[Node]: The Node if it exists otherwise returns None.
        """
        if self.node_exists(id):
            return self.graph[id]
        return None

    def get_neighbors(self, id: str) -> List[str]:
        """Returns all the neighbors of a Node in the graph.

        Args:
            id (str): The ID of the Node.

        Returns:
            List[str]: A List of all the neighbors of that Node.
        """
        if not self.node_exists(id):
            return []
        return [neighbor for neighbor in self.graph[id].edges]

    def get_travel_times(self, id: str) -> List[float]:
        """Returns a List of travel times of all the edges of the Node.

        Args:
            id (str): The ID of the Node.

        Returns:
            List[float]: A List of travel times of all the edges of the Node.
        """
        if not self.node_exists(id):
            return []
        travel_times = []
        for _, edge in self.graph[id].edges.items():
            travel_times.append(edge.travel_time)
        return travel_times

    def get_edge_travel_time(self, source: str, destination: str) -> float:
        """Returns the travel time of the specified edge if it exists.

        Args:
            source (str): The source node of the edge.
            destination (str): The destination of the edge.

        Returns:
            float: The travel time of that edge.
        """
        if (
            not self.node_exists(source)
            or not self.node_exists(destination)
            or not destination in self.graph[source].edges
        ):
            return float("inf")
        return self.graph[source].edges[destination].travel_time

    def compute_path_travel_time(self, path: List[str]) -> float:
        """Computes the cost of a path (a list of node IDs).

        Args:
            path (List[str]): The ID of the nodes in the path.

        Returns:
            float: The total travel time of the specified path.
        """
        cost = 0.0
        for i in range(len(path) - 1):
            if self.edge_exists(path[i], path[i + 1]):
                cost += self.get_edge_travel_time(path[i], path[i + 1])
            else:
                return float("inf")
        return cost

    def evaporate(self) -> None:
        """Evaporates the pheromone values of all the edges given the evaporation parameter (rho).
        """
        for node_id, node in self.graph.items():
            for neighbor, edge in self.graph[node_id].edges.items():
                edge.pheromones = (1 - self.evaporation_rate) * edge.pheromones

    def deposit_pheromones_on_edge(
        self, source: str, destination: str, new_pheromones: float
    ) -> None:
        """Updates the pheromones on an edge in the graph.

        Args:
            source (str): The source node of the edge.
            destination (str): The destination node of the edge.
            new_pheromones (float): The amount of pheromones to be added to the existing value on the edge.
        """
        self.graph[source].edges[destination].pheromones += new_pheromones

    def deposit_pheromones_along_path(self, path: List[str]) -> None:
        """Updates the pheromones along all the edges in the path.

        Args:
            path (List[str]): The path followed by the ant.
        """
        path_cost = self.compute_path_travel_time(path)
        for i in range(len(path) - 1):
            self.deposit_pheromones_on_edge(path[i], path[i + 1], 1 / path_cost)

    def normalize_graph_for_dijkstra(self) -> Dict[str, Dict[str, float]]:
        """Normalizes the graph for the Dijkstra's algorithm implementation.

        Returns:
            Dict[str, Dict[str, float]]: A simple, dictionary-structured graph with only the travel times of the edges.
        """
        dijkstra_graph: Dict[str, Dict[str, float]] = {}
        for node in self.get_all_nodes():
            dijkstra_graph[node] = {}
            for edge in self.graph[node].edges:
                dijkstra_graph[node][edge] = self.graph[node].edges[edge].travel_time
        return dijkstra_graph

    def update_edge_travel_time(self, edge: Edge, new_travel_time: float) -> None:
        """Updates the travel time of an edge in the graph.

        Args:
            edge (Edge): The Edge object.
            new_travel_time (float): The new travel time.
        """
        if new_travel_time <= 0:
            new_travel_time = 1
        edge.travel_time = new_travel_time

    def update_edges_travel_time(
        self, max_delta_time: int = 2, update_probability: float = 0.7
    ) -> None:
        """Stochastically updates the travel time of the edges in the graph.

        Args:
            max_delta_time (int, optional): The maximum allowed change in travel time of an edge (in positive or negative direction). Defaults to 2.
            update_probability (float, optional): The probability that the travel time of an edge will be updated. Defaults to 0.7.
        """
        for edge in self.get_all_edges():
            if random.random() > update_probability:
                continue
            delta_time = random.choice(
                [i for i in range(-max_delta_time, max_delta_time + 1, 1) if i != 0]
            )
            self.update_edge_travel_time(edge, edge.travel_time + delta_time)

    def __str__(self) -> str:
        """Displays the graph.

        Returns:
            str: The string representation of the graph.
        """
        display = []
        for node_id, node in self.graph.items():
            display.append("---")
            display.append(f"Node {node.id}")
            display.append("")
            display.append("Edges:")
            for edge_id, edge in node.edges.items():
                display.append(
                    f"{node_id} -> {edge_id}, Travel Time: {edge.travel_time}, Pheromones: {edge.pheromones}"
                )
        return "\n".join(display)
