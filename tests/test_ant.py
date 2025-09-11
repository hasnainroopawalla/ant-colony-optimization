import pytest
from unittest.mock import Mock

from aco_routing.ant import Ant
from aco_routing.graph_api import GraphApi


@pytest.fixture
def mock_graph_api():
    graph_api = Mock(spec=GraphApi)
    # Set up a simple graph for testing
    graph_api.get_neighbors.return_value = ["B", "C"]
    graph_api.get_edge_pheromones.return_value = 1.0
    graph_api.get_edge_cost.return_value = 1.0
    return graph_api


def test_ant_initialization(mock_graph_api):
    ant = Ant(mock_graph_api, source="A", destination="D")
    assert ant.source == "A"
    assert ant.destination == "D"
    assert ant.current_node == "A"
    assert ant.path == ["A"]
    assert ant.path_cost == 0.0
    assert not ant.is_fit
    assert not ant.is_solution_ant
    assert len(ant.visited_nodes) == 0


def test_reached_destination(mock_graph_api):
    ant = Ant(mock_graph_api, source="A", destination="D")
    assert not ant.reached_destination()
    ant.current_node = "D"
    assert ant.reached_destination()


def test_get_unvisited_neighbors(mock_graph_api):
    ant = Ant(mock_graph_api, source="A", destination="D")
    unvisited = ant._get_unvisited_neighbors()
    assert set(unvisited) == {"B", "C"}

    # Test with some visited nodes
    ant.visited_nodes.add("B")
    unvisited = ant._get_unvisited_neighbors()
    assert unvisited == ["C"]


def test_take_step_normal_case(mock_graph_api):
    ant = Ant(mock_graph_api, source="A", destination="D")
    ant.take_step()
    assert ant.current_node in ["B", "C"]  # Should move to one of the neighbors
    assert len(ant.path) == 2  # Should have two nodes in path [A, (B or C)]
    assert ant.path_cost == 1.0  # With our mock returning cost=1.0
    assert len(ant.visited_nodes) == 1  # Should have marked A as visited


def test_solution_ant_behavior(mock_graph_api):
    ant = Ant(mock_graph_api, source="A", destination="D", is_solution_ant=True)
    # Mock edge pheromones to make B more desirable
    mock_graph_api.get_edge_pheromones.side_effect = lambda src, dst: (
        2.0 if dst == "B" else 1.0
    )

    ant.take_step()
    assert ant.current_node == "B"  # Should always choose B as it has higher pheromone
    assert ant.path == ["A", "B"]


def test_deposit_pheromones(mock_graph_api):
    ant = Ant(mock_graph_api, source="A", destination="D")
    ant.path = ["A", "B", "C"]  # Manually set path for testing
    ant.path_cost = 2.0

    ant.deposit_pheromones_on_path()

    # Should deposit pheromones on A->B and B->C
    mock_graph_api.deposit_pheromones.assert_any_call("A", "B", 0.5)
    mock_graph_api.deposit_pheromones.assert_any_call("B", "C", 0.5)
    assert mock_graph_api.deposit_pheromones.call_count == 2
