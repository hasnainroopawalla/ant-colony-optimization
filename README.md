<h1 align="center">Ant Colony Optimization</h1>


[![Develop](https://github.com/hasnainroopawalla/Ant-Colony-Optimization/actions/workflows/develop.yml/badge.svg)](https://github.com/hasnainroopawalla/Ant-Colony-Optimization/actions/workflows/develop.yml)
[![Deploy](https://github.com/hasnainroopawalla/Ant-Colony-Optimization/actions/workflows/deploy.yml/badge.svg)](https://github.com/hasnainroopawalla/Ant-Colony-Optimization/actions/workflows/deploy.yml)
[![PyPi version](https://img.shields.io/pypi/v/aco_routing.svg)](https://pypi.python.org/pypi/aco_routing/)
![Downloads](https://img.shields.io/pypi/dm/aco_routing.svg)
<!-- [![Python versions](https://img.shields.io/pypi/pyversions/aco_routing.svg?style=plastic)](https://img.shields.io/pypi/pyversions/aco_routing.svg?style=plastic) -->


A Python package to find the shortest path in a graph using Ant Colony Optimization (ACO).


The Ant colony Optimization algorithm is a probabilistic technique for solving computational problems which can be reduced to finding good paths through graphs ([source](https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms)).

This implementation of the ACO algorithm uses the [NetworkX](https://networkx.org/) graph environment.

## 🏁 Getting Started <a name = "getting_started"></a>

### To install the package directly from PyPi:
```
$ pip install aco_routing
```

## 🎈 Usage <a name="usage"></a>
> **_Check out:_** [example.py](https://github.com/hasnainroopawalla/Ant-Colony-Optimization/blob/00cd068597ab9a69a8eb81c8a3fd984797d2eefd/example.py)

Import all the dependencies:
```python
from aco_routing import ACO
import networkx as nx
```

Create a `NetworkX.Graph` object with nodes and edges:
```python
G = nx.DiGraph()

G.add_edge("A", "B", cost=2)
G.add_edge("B", "C", cost=2)
G.add_edge("A", "H", cost=2)
G.add_edge("H", "G", cost=2)
G.add_edge("C", "F", cost=1)
G.add_edge("F", "G", cost=1)
G.add_edge("G", "F", cost=1)
G.add_edge("F", "C", cost=1)
G.add_edge("C", "D", cost=10)
G.add_edge("E", "D", cost=2)
G.add_edge("G", "E", cost=2)
```

Use ACO to find the shortest path and cost between the `source` and `destination`:
```python
aco = ACO(G, ant_max_steps=100, num_iterations=100, ant_random_spawn=True)

aco_path, aco_cost = aco.find_shortest_path(
    source="A",
    destination="D",
    num_ants=100,
)
```

Output:
```
ACO path: A -> H -> G -> E -> D
ACO path cost: 8.0
```

## 📦 Contents <a name = "contents"></a>

### Ant
`aco_routing.Ant`
- An `Ant` that traverses the graph.

### ACO
`aco_routing.ACO`
- The traditional Ant Colony Optimization algorithm that spawns ants at various nodes in the graph and finds the shortest path between the specified source and destination ([pseudo code](https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms#Algorithm_and_formula)).


## Contributing

- Post any issues and suggestions on the GitHub [issues](https://github.com/hasnainroopawalla/Ant-Colony-Optimization/issues) page.
- To contribute, fork the project and then create a pull request back to master.


## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/hasnainroopawalla/Ant-Colony-Optimization/blob/73b65a6fd14e3e5517b479cfecac1140f0ae7899/LICENSE) file for details.
