from dataclasses import dataclass, field
import random
import math
from typing import Dict, List, Optional, Tuple


@dataclass
class Edge:
    travel_time: float
    pheromone: float = 1.0
    traffic_stat: Dict[str, float] = field(default_factory=dict)


@dataclass
class Node:
    id: str
    visited: bool = False
    routing_table: Dict = field(default_factory=dict)
    edges: Dict[str, Edge] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.routing_table = {self.id: 0.0}

    def add_edge(self, destination: str, travel_time: float):
        self.edges[destination] = Edge(travel_time)
        self.routing_table[destination] = 0.0


# @dataclass
# class Graph:
#     def __init__(self) -> None:
#         self.graph = {}

#     def add_node(self, name):
#         node = Node(name)
#         self.graph[name] = node

#     def add_edge(self, src, dest):
#         self.graph[src].add_edge(dest)


@dataclass
class Graph:

    """
    graph:-
    {
        'A':{
            'visited': False,
            'neighbors':{
                'B': 3,
                'C': 9
            },
            'pheros': {
                'B': 5
            },
            'routing_table': {
                'B': 0.2,
                'C': 0.1
            },
            'traffic_stat': {
                'B': {
                    'mean': 0.4,
                    'std': 0.2,
                    'W': [3, 4, 5]
                },
                'C': {
                    'mean': 0.4,
                    'std': 0.2,
                    'W': [3, 4, 5]
                }
            }
        }
    }
    """

    graph: Dict[str, Node] = field(default_factory=dict)
    alpha: float = 0.9
    beta: float = 0.1
    evaporation_rate: float = 0.1
    w_max: int = 7

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

    def get_all_edges(self) -> List[Tuple[str, str, float]]:
        """Returns all the edges in the graph.

        Returns:
            List[Tuple[str, str, float]]: A List of Tuples -> (source, destination, travel_time)
        """
        edges = []
        for source in self.graph:
            for destination in self.graph[source].edges:
                edges.append(
                    (
                        source,
                        destination,
                        self.graph[source].edges[destination].travel_time,
                    )
                )
        return edges

    def get_node_edges(self, id: str) -> Dict[str, Edge]:
        return self.graph[id].edges

    def get_node(self, id: str) -> Optional[Node]:
        """Returns the Node if it is present in the graph.

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
        neighbors = []
        for neighbor in self.graph[id].edges:
            neighbors.append(neighbor)
        return neighbors

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

    def mark_node_as_visited(self, id: str) -> None:
        """Marks a Node as visited in the graph.

        Args:
            id (str): The ID of the Node.
        """
        self.graph[id].visited = True

    def mark_node_as_unvisited(self, id: str) -> None:
        """Marks a Node as unvisited in the graph.

        Args:
            id (str): The ID of the Node.
        """
        self.graph[id].visited = False

    def get_edge_travel_time(self, source: str, destination: str) -> float:
        """Returns the travel time of the specified edge if it exists.

        Args:
            source (str): The source node of the edge.
            destination (str): The destination of the edge.

        Returns:
            float: The travel time of that edge.
        """
        if not self.node_exists(source):
            return float("inf")
        if not self.node_exists(destination):
            return float("inf")
        if not destination in self.graph[source].edges:
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
        """Evaporates the phermone values of all the edges given the evaporation parameter (rho).
        """
        for node_id, node in self.graph.items():
            for neighbor, edge in self.graph[node_id].edges.items():
                edge.pheromone = (1 - self.evaporation_rate) * edge.pheromone

    def deposit_phermones_on_edge(
        self, source: str, destination: str, new_phermones: float
    ) -> None:
        """Updates the phermones on an edge in the graph.

        Args:
            source (str): The source node of the edge.
            destination (str): The destination node of the edge.
            new_phermones (float): The amount of phermones to be added to the existing value on the edge.
        """
        self.graph[source].edges[destination].pheromone += new_phermones

    def deposit_pheromones_along_path(self, path: List[str]) -> None:
        """Updates the phermones along all the edges in the path.

        Args:
            path (List[str]): The path followed by the ant.
        """
        path_cost = self.compute_path_travel_time(path)
        for i in range(len(path) - 1):
            self.deposit_phermones_on_edge(path[i], path[i + 1], 1 / path_cost)

    def delete_node(self, node):
        if self.node_exists(node):
            for n in self.graph:
                if node in self.graph[n]["neighbors"]:
                    del self.graph[n]["neighbors"][node]
            del self.graph[node]

    def delete_edge(self, source, destination):
        if self.edge_exists(source, destination):
            del self.graph[source]["neighbors"][destination]

    def update_travel_time(self, source, destination, new_travel_time):
        if self.edge_exists(source, destination):
            if new_travel_time <= 0:
                new_travel_time = 1
            self.graph[source]["neighbors"][destination] = new_travel_time

    def display_graph(self):
        for node in self.graph:
            print("--> NODE {} <--".format(node))
            for neighbor in self.graph[node]["neighbors"]:
                cost = self.graph[node]["neighbors"][neighbor]
                pheros = self.graph[node]["pheromones"][neighbor]
                print(
                    "{} -> {} Cost: {}, Pheros: {}".format(node, neighbor, cost, pheros)
                )

            print("Traffic Statistics to reach Destination")
            if "traffic_stat" in self.graph[node]:
                for dest in self.graph[node]["traffic_stat"]:
                    W = self.graph[node]["traffic_stat"][dest]["W"]
                    mean = self.graph[node]["traffic_stat"][dest]["mean"]
                    var = self.graph[node]["traffic_stat"][dest]["var"]
                    print("|- W = {}".format(W))
                    print("|- Mean = {}".format(mean))
                    print("|- Variance = {}".format(var))
                    print()

            print("Routing Table Information")
            for dest in self.graph[node]["routing_table"]:
                print(
                    " |- Prob. to reach {} = {}".format(
                        dest, self.graph[node]["routing_table"][dest]
                    )
                )

            print("-" * 50)
            print("-" * 50)

    def update_graph(self, max_delta_time=2, update_probability=0.7):
        """
            max_delta_time: maximum allowed change in travel time of an edge (in positive or negative direction)
            update_probability: probability that the travel time of an edge will change
        """
        for edge in self.get_all_edges():
            if random.random() <= update_probability:  # update the edge
                delta_time = random.choice(
                    [i for i in range(-max_delta_time, max_delta_time + 1, 1) if i != 0]
                )  # Change the travel time by delta_time units
                self.update_travel_time(edge[0], edge[1], edge[2] + delta_time)

    # updates the traffic_stat datastructure of the node
    def update_traffic_stat(self, node, destination, neighbor, t):
        # Update traffic status
        if destination in self.graph[node]["traffic_stat"]:
            self.graph[node]["traffic_stat"][destination]["W"].append(t)
            self.graph[node]["traffic_stat"][destination]["mean"] = sum(
                self.graph[node]["traffic_stat"][destination]["W"]
            ) / len(self.graph[node]["traffic_stat"][destination]["W"])
            self.graph[node]["traffic_stat"][destination]["var"] = (
                (t - self.graph[node]["traffic_stat"][destination]["mean"]) ** 2
            ) / len(self.graph[node]["traffic_stat"][destination]["W"])
        else:
            self.graph[node]["traffic_stat"][destination] = {
                "W": [t],
                "mean": t,
                "var": 0,
            }

        if len(self.graph[node]["traffic_stat"][destination]["W"]) > self.w_max:
            self.graph[node]["traffic_stat"][destination]["W"].pop(0)

        # Update routing table
        t_best = min(self.graph[node]["traffic_stat"][destination]["W"])
        first_term = self.c1 * (t_best / t)

        try:
            conf = math.sqrt(1 - self.gamma)
            W_max = len(self.graph[node]["traffic_stat"][destination]["W"])
            t_sup = self.graph[node]["traffic_stat"][destination]["mean"] + (
                self.graph[node]["traffic_stat"][destination]["var"]
                / (conf * math.sqrt(W_max))
            )
            second_term = self.c2 * (
                (t_sup - t_best) / ((t_sup - t_best) + (t - t_best))
            )
        except ZeroDivisionError as e:
            second_term = 0

        r = first_term + second_term

        # print("r for {} with neighbor {} -> {}".format(node, neighbor, r))
        # print(first_term, second_term)

        self.graph[node]["routing_table"][neighbor] += r * (
            1 - self.graph[node]["routing_table"][neighbor]
        )
        for n in self.graph[node]["routing_table"]:
            if n == neighbor:
                continue
            self.graph[node]["routing_table"][n] -= (
                r * self.graph[node]["routing_table"][n]
            )

    def set_window_size(self, w_max):
        self.w_max = w_max

    def set_antnet_hyperparams(self, c1, c2, gamma):
        self.c1 = c1
        self.c2 = c2
        self.gamma = gamma

    def get_alpha(self):
        return self.alpha

    def get_beta(self):
        return self.beta

    def get_evaporation(self):
        return self.evaporation_rate

    def __str__(self) -> str:
        display = []
        for node_id, node in self.graph.items():
            display.append("---")
            display.append(f"Node {node.id}")
            display.append(f"Visited: {node.visited}")
            display.append(f"Routing Table: {node.routing_table}")
            display.append("")
            display.append("Edges:")
            for edge_id, edge in node.edges.items():
                display.append(
                    f"{node_id} -> {edge_id}, Travel Time: {edge.travel_time}, Pheromones: {edge.pheromone}, Traffic Status: {edge.traffic_stat}"
                )
        return "\n".join(display)


# class Node:
#     def __init__(self, name) -> None:
#         self.name = name
#         self.edges = {}

#     def add_edge(self, to):
#         self.edges[to] = Edge(3, 7)

# class Edge:
#     def __init__(self, traffic, phero) -> None:
#         self.traffic = traffic
#         self.phero = phero


# class Graph:
#     def __init__(self) -> None:
#         self.graph = {}

#     def add_node(self, name):
#         node = Node(name)
#         self.graph[name] = node

#     def add_edge(self, src, dest):
#         self.graph[src].add_edge(dest)
