from utils.ant import Ant
import random

MIN_VAL = -99999


class AntNet(Ant):
    graph = None

    def __init__(self, source, destination, alpha):
        super().__init__(source, destination)
        self.alpha = alpha

    def get_L(self, node, neighbor):
        cost = node["neighbors"][neighbor]
        sum_cost = 0
        for n in node["neighbors"]:
            sum_cost += node["neighbors"][n]

        return 1 - (cost / sum_cost)

    def get_neighbor_prob(self, node):
        node = AntNet.graph.get_node(node)

        chosen_neighbors = []
        all_neighbors = []
        for n in node["neighbors"]:
            all_neighbors.append(n)
            if not AntNet.graph.get_node(n)["visited"]:
                chosen_neighbors.append(n)

        probs = []
        if len(chosen_neighbors) > 0:
            for n in chosen_neighbors:
                L = self.get_L(node, n)
                prob = (node["routing_table"][n] + self.alpha * self.get_L(node, n)) / (
                    1 + self.alpha * (len(node["neighbors"]) - 1)
                )
                probs.append((n, prob))
            return probs

        next_neighbor = random.choice(all_neighbors)
        return [(next_neighbor, 1)]

    def remove_cycle_if_any(self):
        if len(self.path_taken) <= 1:
            return

        cycle_detected = False
        start_idx = 0
        end_idx = 1
        for i in range(len(self.path_taken)):
            start_idx = i
            for j in range(i + 1, len(self.path_taken)):
                end_idx = j
                start_path = self.path_taken[i]
                end_path = self.path_taken[j]

                if end_path["end"] == start_path["start"]:
                    cycle_detected = True
                    break
            if cycle_detected:
                break

        if cycle_detected:
            # print("CYCLE -> ", self.path_taken)
            del self.path_taken[start_idx + 1 :]
            # print("CYCLE REMOVED -> ", self.path_taken)
            self.current_node = self.path_taken[start_idx]["end"]

    def take_forward_step(self):
        self.remove_cycle_if_any()
        node = self.current_node

        AntNet.graph.get_node(node)["visited"] = True
        if node == self.destination:
            return node

        probs = self.get_neighbor_prob(node)

        next_neighbor = None
        max_prob = MIN_VAL
        for prob in probs:
            if not AntNet.graph.get_node(prob[0])["visited"]:
                next_neighbor = prob[0]
                break
            if prob[1] > max_prob:
                max_prob = prob[1]
                next_neighbor = prob[0]

        if next_neighbor is not None:
            self.path_taken.append(
                {
                    "start": self.current_node,
                    "end": next_neighbor,
                    "time_taken": AntNet.graph.get_edge_time(
                        self.current_node, next_neighbor
                    ),
                }
            )

        self.current_node = next_neighbor
        return self.current_node

    def take_lazy_step(self):
        if self.current_node == self.destination:
            return self.current_node

        routing_table = AntNet.graph.get_node(self.current_node)["routing_table"]
        # print(routing_table)
        # print(max(routing_table, key=routing_table.get))
        self.current_node = max(routing_table, key=routing_table.get)
        return self.current_node

    # Reverse the path taken
    def reverse_path(self):
        self.path_to_take = self.path_taken.copy()
        self.path_to_take.reverse()
        for path in self.path_to_take:
            path["start"], path["end"] = path["end"], path["start"]

    def go_backward(self):
        total_time_taken = 0
        # if len(self.path_to_take) == 0:
        #     print(self.source, self.destination)
        # print("path to take", self.path_to_take)
        for node in self.path_to_take:
            total_time_taken += node["time_taken"]
            # for backward ant, the actual destination is now the source since we swapped it earlier
            AntNet.graph.update_traffic_stat(
                node["end"], self.source, node["start"], total_time_taken
            )


def runAntNet(G, true_source, destination, c1, c2, lm):
    G.set_antnet_hyperparams(c1, c2, lm)
    iterations = 50
    sources = G.get_all_nodes()
    sources = [s for s in sources if s != destination]
    ants = []
    for s in sources:
        ants.append(AntNet(s, destination, 0.2))

    for _ in range(300):
        AntNet.graph = G
        for ant in ants:
            ant.reset_paths()
            ant.update_destination(destination)
            ant.update_source(random.choice(sources))
            ant.update_current(ant.source)

        for ant in ants:
            for i in range(iterations):
                node = ant.take_forward_step()
                if node == ant.destination:
                    break

            # Skip ants that did not reach destination
            if node != ant.destination:
                print("Ant did not reach destination!\n")
                continue

            # Backward ant
            ant.reverse_path()
            ant.update_destination(ant.source)
            ant.update_source(destination)

            ant.go_backward()

    lazy_ant = AntNet(true_source, destination, 0)
    path_taken = []
    for i in range(iterations):
        path_taken.append(lazy_ant.current_node)
        node = lazy_ant.take_lazy_step()
        if node == destination:
            path_taken.append(node)
            break

    return path_taken
