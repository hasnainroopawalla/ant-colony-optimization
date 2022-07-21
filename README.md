<h1 align="center">Ant Colony Optimization</h1>


[![Develop](https://github.com/hasnainroopawalla/Ant-Colony-Optimization/actions/workflows/develop.yml/badge.svg)](https://github.com/hasnainroopawalla/Ant-Colony-Optimization/actions/workflows/develop.yml)
[![Deploy](https://github.com/hasnainroopawalla/Ant-Colony-Optimization/actions/workflows/deploy.yml/badge.svg)](https://github.com/hasnainroopawalla/Ant-Colony-Optimization/actions/workflows/deploy.yml)
[![PyPi version](https://img.shields.io/pypi/v/aco_routing.svg)](https://pypi.python.org/pypi/aco_routing/)
[![Python versions](https://img.shields.io/pypi/pyversions/aco_routing.svg?style=plastic)](https://img.shields.io/pypi/pyversions/aco_routing.svg?style=plastic)
![Downloads](https://img.shields.io/pypi/dm/aco_routing.svg)


A Python package to find the shortest path in a graph using Ant Colony Optimization (ACO).

The Ant colony Optimization algorithm is a probabilistic technique for solving computational problems which can be reduced to finding good paths through graphs ([source](https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms)).

## 📝 Table of Contents

- [Getting Started](#getting_started)
- [Usage](#usage)
- [Contents](#contents)


## 🏁 Getting Started <a name = "getting_started"></a>

### To install the package directly from PyPi:
```
$ pip install aco_routing
```


## 🎈 Usage <a name="usage"></a>
> **_Check out:_** [aco_routing/example.py](https://github.com/hasnainroopawalla/Ant-Colony-Optimization/tree/master/aco_routing/example.py)

Import all the dependencies.
```python
from aco_routing.utils.graph import Graph
from aco_routing.dijkstra import Dijkstra
from aco_routing.utils.simulator import Simulator
from aco_routing.aco import ACO
```

Create a `Graph` object.
```python
graph = Graph()
```

Create `Edges` between `Nodes` (nodes are implicitly created if they don't exist).
```python
graph.add_edge("A", "B", travel_time=2)
graph.add_edge("B", "C", travel_time=2)
graph.add_edge("A", "H", travel_time=2)
graph.add_edge("H", "G", travel_time=2)
graph.add_edge("C", "F", travel_time=1)
graph.add_edge("F", "G", travel_time=1)
graph.add_edge("G", "F", travel_time=1)
graph.add_edge("F", "C", travel_time=1)
graph.add_edge("C", "D", travel_time=10)
graph.add_edge("E", "D", travel_time=2)
graph.add_edge("G", "E", travel_time=2)
```

Define a `source` and `destination` as well create objects for the `Dijkstra` and `ACO` classes.
```python
source = "A"
destination = "D"

aco = ACO(graph)
dijkstra = Dijkstra(graph)
```

Find the shortest path between the `source` and `destination` as well the cost of the path using `Dijkstra` and `ACO`.
```python
dijkstra_path, dijkstra_cost = dijkstra.find_shortest_path(source, destination)
aco_path, aco_cost = aco.find_shortest_path(source, destination)

print(f"ACO - path: {aco_path}, cost: {aco_cost}")
print(f"Dijkstra - path: {dijkstra_path}, cost: {dijkstra_cost}")
```

Simulate a real-life scenario with various episodes of stochastically updating traffic conditions in a city.
```python
Simulator(graph).simulate(source, destination, num_episodes=100, plot=True)
```


## 📦 Contents <a name = "contents"></a>

### Graph
`aco_routing.utils.graph.Graph`
- A Directed Graph class which consists of `Nodes` and `Edges`.
- The `evaporation_rate` is initialized here.

### Node
`aco_routing.utils.graph.Node`
- A `Node` class which represents a node in the Graph and consists of various outgoing edges.

### Edge
`aco_routing.utils.graph.Edge`
- An `Edge` class which represents a link between 2 nodes in the Graph.
- Each `Edge` has 2 parameters:
    - `travel_time`: The amount of time it takes to traverse the edge. A high value indicates more traffic.
    - `pheromones`: A heuristic parameter i.e., the pheromone values deposited by the ants.

### Dijkstra
`aco_routing.dijkstra.Dijkstra`
- The baseline algorithm to compare the results of the candidate algorithm with.
- The Dijkstra's algorithm ([source](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)) returns the shortest path between any 2 nodes in a graph.

### Ant
`aco_routing.utils.ant.Ant`
- The `Ant` class representing an ant that traverses the graph.

### ACO
`aco_routing.aco.ACO`
- The traditional Ant Colony Optimization algorithm that spawns various ants at random nodes and tries to find the shortest path between the specified source and destination.

### Simulator
`aco_routing.utils.simulator.Simulator`
- The simulator class is used to simulate and evaluate the performance of the candidate algorithm (ACO) with a baseline Dijkstra's Algorithm.
- It simulates a real-life city, where the traffic conditions change every episode in a conditionally stochastic manner.
- The ants continue to find the shortest path even after the traffic conditions change.

<hr>

## Contributing


- Post any issues and suggestions on the GitHub [issues](https://github.com/hasnainroopawalla/Ant-Colony-Optimization/issues) page.
- To contribute, fork the project and then create a pull request back to master.


## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/hasnainroopawalla/Ant-Colony-Optimization/blob/73b65a6fd14e3e5517b479cfecac1140f0ae7899/LICENSE) file for details.
