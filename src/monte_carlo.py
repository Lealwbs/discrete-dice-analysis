"""
Simulação estocástica por amostragem de Monte Carlo.
"""

from typing import Optional
import numpy as np


def monte_carlo_odds(target_sum: int, num_dice: int, num_rolls: int = 100_000,
                     sides: int = 6, seed: Optional[int] = None) -> float:
    """
    Estima a probabilidade P(Soma = target_sum) simulando num_rolls lançamentos.
    """
    if num_dice < 1 or target_sum < num_dice or target_sum > sides * num_dice:
        return 0.0

    rng = np.random.default_rng(seed)
    rolls = rng.integers(1, sides + 1, size=(num_rolls, num_dice), dtype=np.int16)
    sums = np.sum(rolls, axis=1)
    hits = np.count_nonzero(sums == target_sum)
    return hits / float(num_rolls)


# Alias para compatibilidade
mc_dice_odds = monte_carlo_odds
