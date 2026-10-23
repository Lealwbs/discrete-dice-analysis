"""
Pacote principal para analise de probabilidades de somas de dados discretos.
"""

from .dice_odds import (
    exact_dice_odds,
    exact_dice_count,
    de_moivre_dice_probability,
    dice_distribution,
    what_are_the_odds,
)
from .crossover import (
    dice_parameters,
    logarithmic_mean,
    classical_means_summary,
    exact_gaussian_crossover,
    numerical_gaussian_crossover,
    verify_gaussian_crossover,
    discrete_crossover_point,
    gaussian_pdf,
)
from .monte_carlo import monte_carlo_odds, mc_dice_odds
from .plot import (
    plot_discrete,
    plot_comparison,
    plot_crossover,
    generate_project_figures,
)

__all__ = [
    "exact_dice_odds",
    "exact_dice_count",
    "de_moivre_dice_probability",
    "dice_distribution",
    "what_are_the_odds",
    "dice_parameters",
    "logarithmic_mean",
    "classical_means_summary",
    "exact_gaussian_crossover",
    "numerical_gaussian_crossover",
    "verify_gaussian_crossover",
    "discrete_crossover_point",
    "gaussian_pdf",
    "monte_carlo_odds",
    "mc_dice_odds",
    "plot_discrete",
    "plot_comparison",
    "plot_crossover",
    "generate_project_figures",
]
