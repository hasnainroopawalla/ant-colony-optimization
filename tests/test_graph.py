from aco.graph import Graph

G = Graph()

G.add_node("A")
G.add_node("B")
G.add_node("C")


G.add_edge("A", "B", 5)
G.add_edge("A", "C", 8)
G.add_edge("B", "C", 56)
G.add_edge("C", "A", 33)


def test_get_nodes() -> None:
    assert G.get_all_nodes() == ["A", "B", "C"]


def test_get_all_edges() -> None:
    assert G.get_all_edges() == [
        ("A", "B", 5),
        ("A", "C", 8),
        ("B", "C", 56),
        ("C", "A", 33),
    ]


def test_get_neighbors() -> None:
    assert G.get_neighbors("A") == ["B", "C"]


def test_get_travel_times() -> None:
    assert G.get_travel_times("A") == [5, 8]
