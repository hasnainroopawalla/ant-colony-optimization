import random
from utils.graph import Graph
from utils.antnet import AntNet
import json

G = Graph(0.9, 0.1)

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


# G.add_edge('A','B', 2)
# G.add_edge('B','C', 2)
# G.add_edge('C','D', 2)
# G.add_edge('A','D', 1)


G.set_antnet_hyperparams(0.6, 0.3, 0.7)

destination = "D"
sources = ["A", "B", "C", "D", "E", "F", "G", "H"]
# sources = ['A', 'B', 'C']
iterations = 50

ant_paths = []

ants = [
    AntNet("B", "D", 0.2),
    AntNet("C", "D", 0.2),
    AntNet("D", "D", 0.2),
    AntNet("D", "D", 0.2),
    AntNet("B", "D", 0.2),
]

# print(json.dumps(G.graph))

for _ in range(300):
    AntNet.graph = G

    for ant in ants:
        ant.reset_paths()
        ant.update_destination(destination)
        ant.update_source(random.choice(sources))
        ant.update_current(ant.source)

    for ant in ants:  # this should happen in parallel processes
        # print("Ant {} -> {}".format(ant.source, ant.destination))
        for i in range(iterations):
            node = ant.take_forward_step()
            if node == ant.destination:
                break

        # print("Forward step taken")
        # print(ant.get_path_taken())

        # Skip ants that did not reach destination
        if node != ant.destination:
            print("Ant did not reach destination!\n")
            continue

        # Backward ant
        ant.reverse_path()
        ant.update_destination(ant.source)
        ant.update_source(destination)

        ant.go_backward()
        # print()

print("=" * 50)
print("Graph Info")
print("=" * 50)
print(G.display_graph())

print()
print("Paths taken for lazy ants to reach {} from multiple sources".format(destination))
print("=" * 50)
for source in sources:
    lazy_ant = AntNet(source, destination, 0)
    print("Lazy Ant need to go from {} -> {}".format(source, destination))
    print("Path taken", end=" = ")
    for i in range(iterations):
        print(lazy_ant.current_node, end="->")
        node = lazy_ant.take_lazy_step()
        if node == destination:
            print(node)
            break

    print("-" * 50)
