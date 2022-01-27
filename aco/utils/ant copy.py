from dataclasses import dataclass
import random

from aco.graph import Graph


class Ant:
    def __init__(self, G: Graph, source: str, destination: str):
        self.graph = G
        self.source = source
        self.destination = destination
        self.current_node = self.source
        self.path_taken = []

    def update_destination(self, destination):
        self.destination = destination

    def update_source(self, source):
        self.source = source

    def update_current(self, curr):
        self.current_node = curr

    def reset_paths(self):
        self.path_taken = []
        self.path_to_take = []

    def take_step(self):
        # Return true if already reached destination
        if self.current_node == self.destination:
            return True

        self.graph.mark_node_as_visited(self.current_node)

        # Take a random neighbor from current position
        all_neighbors = self.graph.get_neighbors(self.current_node)
        phero_values = self.graph.get_pheromones(self.current_node)
        travel_length = self.graph.get_travel_times(self.current_node)
        alpha = self.graph.alpha
        beta = self.graph.beta

        # If there are no neighbors. Special case - isolated intersection
        if len(all_neighbors) == 0:
            return False

        # Already visited or not
        chosen_neighbors = []
        for neigh in all_neighbors:
            if self.graph.get_node(neigh).visited is False:
                chosen_neighbors.append(neigh)

        # Randomly select a neighbor from current node and add that in the
        # path_taken list
        total = 0.0
        probabilities = {}
        for i in range(len(all_neighbors)):
            print(phero_values[i])
            total += (phero_values[i] ** alpha) * ((1 / travel_length[i]) ** beta)

        # print(chosen_neighbors)
        for i in range(len(chosen_neighbors)):
            probabilities[chosen_neighbors[i]] = (
                (phero_values[i] ** alpha) * ((1 / travel_length[i]) ** beta)
            ) / total

        sorted_probabilities = {
            k: v for k, v in sorted(probabilities.items(), key=lambda item: -item[1])
        }
        sorted_neighbors = list(sorted_probabilities)
        sorted_values = list(sorted_probabilities.values())

        # Selection using a threshold value epsilon
        eps = 0.1
        candidates = []

        if len(sorted_probabilities) == 1:
            candidates.append(sorted_neighbors[0])
        else:
            for i in range(len(sorted_probabilities) - 1):
                if (sorted_values[i] - sorted_values[i + 1]) < eps:
                    candidates.append(sorted_neighbors[i])
                    if i == len(sorted_probabilities) - 2:
                        candidates.append(sorted_neighbors[i + 1])
                else:
                    candidates.append(sorted_neighbors[i])
                    break

        # Selection using random weighted choice with the probabilities
        selected_neighbor = random.choices(
            sorted_neighbors, weights=sorted_values, k=1
        )[0]

        self.graph.update_pheromones(self.current_node, selected_neighbor)

        self.path_taken.append(
            {
                "start": self.current_node,
                "end": selected_neighbor,
                "time_spent": self.graph.get_edge_time(
                    self.current_node, selected_neighbor
                ),
            }
        )

        # Update current position
        self.current_node = selected_neighbor

        return False

    def get_path_taken(self):
        return self.path_taken

    def get_time_spent(self):
        time_spent = 0
        for path in self.path_taken:
            time_spent += path["time_spent"]

        return time_spent


def runACO(G: Graph, source: str, destination: str):

    ant_paths = []
    iterations = 50

    ants = [
        Ant(G, source, destination),
        Ant(G, source, destination),
        Ant(G, source, destination),
        Ant(G, source, destination),
        Ant(G, source, destination),
        Ant(G, source, destination),
    ]

    for ant in ants:  # this should happen in parallel processes
        for node in G.get_all_nodes():
            G.mark_node_as_unvisited(node)
        print("ANT -----------")
        print(ant.graph.graph["A"], G.graph["A"])
        for i in range(iterations):
            # print(G.graph['A']['pheromones'])
            if ant.take_step():
                ant_paths.append(ant.get_path_taken())
                break
        print(ant.graph.graph["A"].pheromones, G.graph["A"].pheromones)

    # Update the pheromones values
    G.evaporate()
    for path_taken in ant_paths:
        for path in path_taken:
            G.add_phero(path["start"], path["end"])

    # Return list corresponding to the path
    path = [source]
    node = source
    while node != destination:
        G.mark_node_as_visited(node)
        pheros = G.graph[node]["pheromones"]
        max_neighbor = max(pheros, key=pheros.get)
        path.append(max_neighbor)
        node = max_neighbor

    return path
