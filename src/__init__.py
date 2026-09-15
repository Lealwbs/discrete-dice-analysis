"""
Módulos do Discrete Dice Analysis.
"""

from .dice_odds import exact_dice_odds, exact_dice_count, de_moivre_dice_probability, dice_distribution, what_are_the_odds
from .crossover import dice_parameters, exact_gaussian_crossover, discrete_crossover_point, gaussian_pdf
from .monte_carlo import monte_carlo_odds, mc_dice_odds
from .plot import plot_discrete, plot_comparison, plot_crossover

__all__ = [
    "exact_dice_odds",
    "exact_dice_count",
    "de_moivre_dice_probability",
    "dice_distribution",
    "what_are_the_odds",
    "dice_parameters",
    "exact_gaussian_crossover",
    "discrete_crossover_point",
    "gaussian_pdf",
    "monte_carlo_odds",
    "mc_dice_odds",
    "plot_discrete",
    "plot_comparison",
    "plot_crossover",
]
