import random
from typing import Dict


def compute_edge_desirability(
    pheromone_value: float, edge_cost: float, alpha: float, beta: float
) -> float:
    return pheromone_value**alpha * (1 / edge_cost) ** beta


def roulette_wheel_selection(probabilities: Dict[str, float]) -> str:
    # TODO: Add desc
    sorted_probabilities = {
        k: v for k, v in sorted(probabilities.items(), key=lambda item: -item[1])
    }
    pick = random.random()
    current = 0.0
    for node, fitness in sorted_probabilities.items():
        current += fitness
        if current > pick:
            return node
    raise Exception("Edge case for roulette wheel selection")
